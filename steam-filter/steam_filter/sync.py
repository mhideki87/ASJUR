"""Orquestracao da sincronizacao: eu -> amigos -> bibliotecas -> detalhes da loja."""

from __future__ import annotations

import asyncio
import sqlite3
import time
from dataclasses import dataclass, field

from . import db
from .config import Config
from .steam_api import PrivateProfile, SteamClient, SteamError


@dataclass
class SyncState:
    running: bool = False
    run_id: int | None = None
    mode: str = "full"
    phase: str = "ocioso"
    message: str = ""
    current: int = 0
    total: int = 0
    started_at: float | None = None
    finished_at: float | None = None
    status: str = "idle"          # idle | running | done | error | cancelled
    stats: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    cancel: bool = False

    def snapshot(self) -> dict:
        pct = 0.0
        if self.total:
            pct = round(min(100.0, self.current / self.total * 100), 1)
        return {
            "running": self.running,
            "run_id": self.run_id,
            "mode": self.mode,
            "phase": self.phase,
            "message": self.message,
            "current": self.current,
            "total": self.total,
            "percent": pct,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "elapsed": round((self.finished_at or time.time()) - self.started_at, 1)
            if self.started_at
            else 0,
            "stats": self.stats,
            "warnings": self.warnings[-20:],
        }

    def set_phase(self, phase: str, message: str = "", total: int = 0) -> None:
        self.phase = phase
        self.message = message
        self.current = 0
        self.total = total

    def warn(self, text: str) -> None:
        if text not in self.warnings:
            self.warnings.append(text)


STATE = SyncState()


def _check_cancel() -> None:
    if STATE.cancel:
        raise asyncio.CancelledError()


async def run_sync(cfg: Config, mode: str = "full", client_factory=None) -> dict:
    """mode='full' refaz tudo; mode='details' so continua a fila de detalhes da loja.

    client_factory existe para os testes injetarem um SteamClient com transporte falso.
    """
    if STATE.running:
        raise SteamError("Ja existe uma sincronizacao em andamento.")

    db.init_db()
    conn = db.connect()
    STATE.__init__()  # zera o estado anterior
    STATE.running = True
    STATE.mode = mode
    STATE.status = "running"
    STATE.started_at = time.time()
    STATE.run_id = db.start_run(conn)
    stats: dict = {}

    try:
        make_client = client_factory or (
            lambda: SteamClient(
                cfg.api_key,
                api_rate_per_sec=cfg.api_rate_per_sec,
                store_rate_per_sec=cfg.store_rate_per_sec,
                store_country=cfg.store_country,
                store_language=cfg.store_language,
            )
        )
        async with make_client() as client:
            if mode == "full":
                stats.update(await _sync_full(conn, client, cfg))
            stats.update(await _sync_store_details(conn, client, cfg))

        conn.commit()
        STATE.stats = stats
        STATE.status = "done"
        STATE.set_phase("concluido", "Sincronizacao concluida.")
        db.finish_run(conn, STATE.run_id, "done", "ok", stats)
        db.set_meta(conn, "last_sync_at", str(db.now()))
        conn.commit()
        return stats

    except asyncio.CancelledError:
        conn.commit()
        STATE.status = "cancelled"
        STATE.set_phase("cancelado", "Sincronizacao cancelada. O que ja veio ficou salvo.")
        db.finish_run(conn, STATE.run_id, "cancelled", "cancelada pelo usuario", stats)
        return stats
    except Exception as exc:  # noqa: BLE001 — o erro vai para a UI
        conn.commit()
        STATE.status = "error"
        STATE.set_phase("erro", str(exc))
        db.finish_run(conn, STATE.run_id, "error", str(exc), stats)
        raise
    finally:
        STATE.running = False
        STATE.finished_at = time.time()
        STATE.stats = stats or STATE.stats
        conn.close()


async def _sync_full(conn: sqlite3.Connection, client: SteamClient, cfg: Config) -> dict:
    stats: dict = {}

    # 1) Quem sou eu -------------------------------------------------------
    STATE.set_phase("perfil", "Validando chave e SteamID...", 1)
    steamid = await client.resolve_steam_id(cfg.steam_id)
    summaries = await client.get_player_summaries([steamid])
    me = summaries.get(steamid)
    if not me:
        raise SteamError(
            "A Steam nao devolveu nenhum perfil para esse SteamID. Confira o ID e a chave da API."
        )
    conn.execute("UPDATE player SET is_self = 0 WHERE is_self = 1")
    db.upsert_player(
        conn,
        steamid,
        personaname=me.get("personaname"),
        avatar=me.get("avatarfull") or me.get("avatar"),
        profileurl=me.get("profileurl"),
        is_self=1,
        last_synced=db.now(),
    )
    db.set_meta(conn, "self_steamid", steamid)
    conn.commit()
    STATE.current = 1
    stats["me"] = me.get("personaname") or steamid
    stats["steamid"] = steamid

    # 2) Minha biblioteca --------------------------------------------------
    STATE.set_phase("biblioteca", "Baixando a sua biblioteca...", 1)
    mine = await client.get_owned_games(steamid)
    if mine.state != "public":
        raise SteamError(
            "Nao consegui ler a SUA biblioteca. Em Perfil > Editar perfil > Privacidade, deixe"
            " 'Detalhes do jogo' como Publico (a chave da API respeita a privacidade, mesmo sendo sua)."
        )
    db.upsert_apps_basic(conn, mine.games)
    count = db.replace_ownership(conn, steamid, mine.games)
    db.upsert_player(conn, steamid, library_state="public", games_count=count, last_synced=db.now())
    conn.commit()
    STATE.current = 1
    stats["my_games"] = count

    # 3) Lista de amigos ---------------------------------------------------
    STATE.set_phase("amigos", "Baixando a lista de amigos...", 1)
    friends = await client.get_friend_list(steamid)
    friend_ids = [str(f["steamid"]) for f in friends if f.get("steamid")]
    conn.execute("UPDATE player SET is_friend = 0 WHERE is_friend = 1")
    for f in friends:
        db.upsert_player(
            conn,
            str(f["steamid"]),
            is_friend=1,
            friend_since=int(f.get("friend_since") or 0) or None,
        )
    conn.commit()
    STATE.current = 1
    stats["friends"] = len(friend_ids)
    if not friend_ids:
        STATE.warn("Sua lista de amigos veio vazia.")
        return stats

    # 4) Nomes e avatares --------------------------------------------------
    STATE.set_phase("perfis", "Baixando nomes e avatares dos amigos...", len(friend_ids))
    profiles = await client.get_player_summaries(friend_ids)
    for sid, player in profiles.items():
        db.upsert_player(
            conn,
            sid,
            personaname=player.get("personaname"),
            avatar=player.get("avatarfull") or player.get("avatar"),
            profileurl=player.get("profileurl"),
        )
    conn.commit()
    STATE.current = len(friend_ids)

    # 5) Biblioteca de cada amigo -----------------------------------------
    STATE.set_phase("bibliotecas", "Lendo a biblioteca de cada amigo...", len(friend_ids))
    semaphore = asyncio.Semaphore(max(1, cfg.friend_concurrency))
    public = private = errors = 0
    lock = asyncio.Lock()

    async def fetch(sid: str) -> None:
        nonlocal public, private, errors
        _check_cancel()
        async with semaphore:
            _check_cancel()
            owned = await client.get_owned_games(sid)
        async with lock:
            if owned.state == "public":
                db.upsert_apps_basic(conn, owned.games)
                n = db.replace_ownership(conn, sid, owned.games)
                db.upsert_player(conn, sid, library_state="public", games_count=n, last_synced=db.now())
                public += 1
            else:
                db.upsert_player(conn, sid, library_state=owned.state, last_synced=db.now())
                if owned.state == "private":
                    private += 1
                else:
                    errors += 1
            STATE.current += 1
            name = profiles.get(sid, {}).get("personaname") or sid
            STATE.message = f"{STATE.current}/{len(friend_ids)} — {name}"
            if STATE.current % 10 == 0:
                conn.commit()

    tasks = [asyncio.create_task(fetch(sid)) for sid in friend_ids]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
    conn.commit()

    stats["friends_public"] = public
    stats["friends_private"] = private
    stats["friends_error"] = errors
    if private:
        STATE.warn(
            f"{private} amigo(s) estao com 'Detalhes do jogo' privado — os jogos deles nao entram na conta."
        )
    return stats


def _details_queue(conn: sqlite3.Connection, cfg: Config) -> list[int]:
    max_age = cfg.store_details_max_age_days * 86400
    cutoff = db.now() - max_age
    missing_cutoff = db.now() - max_age * 3
    self_sid = db.get_meta(conn, "self_steamid") or ""
    rows = conn.execute(
        """
        WITH friend_counts AS (
            SELECT o.appid, COUNT(*) AS friends
            FROM ownership o
            JOIN player p ON p.steamid = o.steamid AND p.is_friend = 1
            GROUP BY o.appid
        ),
        mine AS (
            SELECT appid, playtime_forever FROM ownership WHERE steamid = ?
        )
        SELECT a.appid,
               COALESCE(fc.friends, 0) AS friends,
               CASE WHEN mine.appid IS NULL THEN 0 ELSE 1 END AS i_own
        FROM app a
        LEFT JOIN friend_counts fc ON fc.appid = a.appid
        LEFT JOIN mine ON mine.appid = a.appid
        WHERE (
                  (? = 1 AND mine.appid IS NOT NULL)
                  OR COALESCE(fc.friends, 0) >= ?
              )
          AND (
                  a.details_state IS NULL
                  OR (a.details_state = 'ok' AND COALESCE(a.details_synced, 0) < ?)
                  OR (a.details_state = 'error')
                  OR (a.details_state = 'missing' AND COALESCE(a.details_synced, 0) < ?)
              )
        ORDER BY friends DESC, i_own DESC, COALESCE(mine.playtime_forever, 0) DESC, a.appid
        """,
        (
            self_sid,
            1 if cfg.details_include_my_games else 0,
            max(1, cfg.details_min_friends),
            cutoff,
            missing_cutoff,
        ),
    ).fetchall()
    return [int(r["appid"]) for r in rows]


def details_pending_count(conn: sqlite3.Connection, cfg: Config) -> int:
    return len(_details_queue(conn, cfg))


async def _sync_store_details(conn: sqlite3.Connection, client: SteamClient, cfg: Config) -> dict:
    queue = _details_queue(conn, cfg)
    budget = max(0, cfg.store_budget_per_sync)
    batch = queue[:budget] if budget else queue
    remaining = len(queue) - len(batch)

    STATE.set_phase(
        "detalhes",
        f"Buscando categorias (multiplayer/co-op) de {len(batch)} jogos na loja...",
        len(batch),
    )
    ok = missing = errors = 0
    for appid in batch:
        _check_cancel()
        state, data = await client.get_app_details(appid)
        db.save_app_details(conn, appid, data, state)
        if state == "ok":
            ok += 1
        elif state == "missing":
            missing += 1
        else:
            errors += 1
        STATE.current += 1
        if STATE.current % 10 == 0:
            conn.commit()
    conn.commit()

    if remaining:
        STATE.warn(
            f"Faltam detalhes de {remaining} jogo(s) — a loja limita ~200 consultas a cada 5 min."
            " Use 'Continuar detalhes' para seguir de onde parou."
        )
    return {
        "details_ok": ok,
        "details_missing": missing,
        "details_error": errors,
        "details_pending": remaining,
    }


async def cancel_sync() -> None:
    STATE.cancel = True
