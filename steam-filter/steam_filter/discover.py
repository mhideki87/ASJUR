"""Busca no catalogo da Steam: encontra jogos por etiqueta/preco/avaliacao e enriquece o cache.

A busca da loja so devolve *quais* jogos batem com os criterios estruturais (etiqueta, preco,
promocao). Preco exato, categorias (co-op/PvP) e avaliacoes vem em seguida dos endpoints JSON
oficiais, uma vez por jogo, e ficam no banco — a segunda busca com os mesmos jogos e instantanea.
"""

from __future__ import annotations

import asyncio
import sqlite3
import time
from dataclasses import dataclass, field

from . import db
from .config import Config
from .steam_api import SteamClient, SteamError


@dataclass
class DiscoverState:
    running: bool = False
    phase: str = "ocioso"
    message: str = ""
    current: int = 0
    total: int = 0
    status: str = "idle"          # idle | running | done | error | cancelled
    started_at: float | None = None
    finished_at: float | None = None
    stats: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    criteria: dict = field(default_factory=dict)
    cancel: bool = False

    def snapshot(self) -> dict:
        percent = round(min(100.0, self.current / self.total * 100), 1) if self.total else 0.0
        return {
            "running": self.running,
            "phase": self.phase,
            "message": self.message,
            "current": self.current,
            "total": self.total,
            "percent": percent,
            "status": self.status,
            "elapsed": round((self.finished_at or time.time()) - self.started_at, 1)
            if self.started_at
            else 0,
            "stats": self.stats,
            "warnings": self.warnings[-10:],
            "criteria": self.criteria,
        }

    def warn(self, text: str) -> None:
        if text not in self.warnings:
            self.warnings.append(text)


STATE = DiscoverState()


def _check_cancel() -> None:
    if STATE.cancel:
        raise asyncio.CancelledError()


async def refresh_tags(cfg: Config, client_factory=None) -> int:
    """Baixa o catalogo de etiquetas da Steam (uma vez; depois so quando o usuario pedir)."""
    make = client_factory or (lambda: _client(cfg))
    async with make() as client:
        tags = await client.get_popular_tags()
    db.init_db()
    with db.closing_conn() as conn:
        saved = db.save_tags(conn, tags)
        conn.commit()
    return saved


def _client(cfg: Config) -> SteamClient:
    return SteamClient(
        cfg.api_key or "sem-chave",   # busca e avaliacoes nao usam a chave da Web API
        api_rate_per_sec=cfg.api_rate_per_sec,
        store_rate_per_sec=cfg.store_rate_per_sec,
        store_country=cfg.store_country,
        store_language=cfg.store_language,
    )


def _needs_details(row: sqlite3.Row, max_age: int) -> bool:
    if row["details_state"] != "ok":
        return row["details_state"] != "missing"
    return (row["details_synced"] or 0) < max_age


def _needs_reviews(row: sqlite3.Row, max_age: int) -> bool:
    return (row["reviews_synced"] or 0) < max_age


async def run_discover(
    cfg: Config,
    criteria: dict,
    client_factory=None,
) -> dict:
    """criteria: term, tag_ids, maxprice, specials, sort, pages, enrich_limit."""
    if STATE.running:
        raise SteamError("Ja existe uma busca em andamento.")

    db.init_db()
    conn = db.connect()
    STATE.__init__()
    STATE.running = True
    STATE.status = "running"
    STATE.started_at = time.time()
    STATE.criteria = dict(criteria)
    stats: dict = {}

    term = str(criteria.get("term") or "").strip()
    tag_ids = [int(t) for t in (criteria.get("tag_ids") or [])]
    maxprice = criteria.get("maxprice")
    specials = bool(criteria.get("specials"))
    sort = str(criteria.get("sort") or "avaliacoes")
    pages = max(1, min(int(criteria.get("pages") or 2), 10))
    enrich_limit = max(0, min(int(criteria.get("enrich_limit") or 60), 400))
    page_size = 50

    make = client_factory or (lambda: _client(cfg))
    try:
        async with make() as client:
            # 1) quais jogos batem com os criterios estruturais -----------------
            STATE.phase = "busca"
            STATE.message = "Consultando o catalogo da Steam..."
            STATE.total = pages
            appids: list[int] = []
            total_found = 0
            for page in range(pages):
                _check_cancel()
                found, total_found = await client.search_store(
                    term=term,
                    tag_ids=tag_ids,
                    maxprice=maxprice,
                    specials=specials,
                    sort=sort,
                    start=page * page_size,
                    count=page_size,
                )
                for appid in found:
                    if appid not in appids:
                        appids.append(appid)
                STATE.current = page + 1
                STATE.message = f"{len(appids)} jogo(s) encontrados de {total_found}"
                if len(found) < page_size:
                    break

            db.mark_discovered(conn, appids)
            tag_names = [t for t in (criteria.get("tag_names") or []) if t]
            for appid in appids:
                db.add_app_tags(conn, appid, tag_names)
            conn.commit()
            stats["encontrados"] = len(appids)
            stats["total_no_catalogo"] = total_found
            if not appids:
                STATE.warn("A busca nao devolveu nenhum jogo. Tente afrouxar os critérios.")

            # 2) o que ainda falta saber sobre esses jogos ----------------------
            max_age = db.now() - cfg.store_details_max_age_days * 86400
            placeholders = ",".join("?" * len(appids)) or "NULL"
            rows = {
                r["appid"]: r
                for r in conn.execute(
                    f"SELECT appid, details_state, details_synced, reviews_synced FROM app"
                    f" WHERE appid IN ({placeholders})",
                    appids,
                )
            }
            fila = [
                appid
                for appid in appids
                if appid not in rows
                or _needs_details(rows[appid], max_age)
                or _needs_reviews(rows[appid], max_age)
            ][:enrich_limit]

            # 3) preco, categorias e avaliacoes, na ordem do resultado ----------
            STATE.phase = "detalhes"
            STATE.current = 0
            STATE.total = len(fila)
            STATE.message = f"Buscando preço e avaliações de {len(fila)} jogo(s)..."
            detalhes = avaliacoes = 0
            for appid in fila:
                _check_cancel()
                row = rows.get(appid)
                if row is None or _needs_details(row, max_age):
                    state, data = await client.get_app_details(appid)
                    db.save_app_details(conn, appid, data, state)
                    if state == "ok":
                        detalhes += 1
                _check_cancel()
                if row is None or _needs_reviews(row, max_age):
                    state, summary = await client.get_app_reviews(appid)
                    db.save_app_reviews(conn, appid, summary, state)
                    if state == "ok":
                        avaliacoes += 1
                STATE.current += 1
                if STATE.current % 5 == 0:
                    conn.commit()
            conn.commit()

            stats["detalhes"] = detalhes
            stats["avaliacoes"] = avaliacoes
            if len(appids) > enrich_limit:
                restante = len(appids) - enrich_limit
                STATE.warn(
                    f"{restante} jogo(s) ficaram sem preço/avaliação nesta rodada (limite por busca)."
                    " Rode a busca de novo para completar — o que já veio fica em cache."
                )

        STATE.status = "done"
        STATE.phase = "concluido"
        STATE.message = f"{len(appids)} jogo(s) no resultado."
        STATE.stats = stats
        return stats

    except asyncio.CancelledError:
        conn.commit()
        STATE.status = "cancelled"
        STATE.phase = "cancelado"
        STATE.message = "Busca cancelada. O que já veio ficou salvo."
        return stats
    except Exception as exc:  # noqa: BLE001 — a mensagem vai para a interface
        conn.commit()
        STATE.status = "error"
        STATE.phase = "erro"
        STATE.message = str(exc)
        raise
    finally:
        STATE.running = False
        STATE.finished_at = time.time()
        STATE.stats = stats or STATE.stats
        conn.close()


async def cancel_discover() -> None:
    STATE.cancel = True
