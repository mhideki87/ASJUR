"""API HTTP local (FastAPI) + entrega da interface web."""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import db, discover, queries, sync
from .config import WEB_DIR, load_config, save_config
from .steam_api import SteamClient, SteamError, persona_state_label

_sync_task: asyncio.Task | None = None
_online_cache: dict[str, Any] = {"at": 0.0, "players": {}, "failed_at": 0.0, "error": ""}
ONLINE_TTL = 45.0        # segundos de cache do "quem esta online"
ONLINE_COOLDOWN = 120.0  # apos uma falha, nao tenta de novo por esse tempo
ONLINE_TIMEOUT = 8.0     # a UI nunca fica pendurada esperando a Steam


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Steam Game Filter", version="1.0.0", lifespan=lifespan)


def _conn():
    return db.connect()


@app.exception_handler(SteamError)
async def steam_error_handler(request, exc: SteamError):  # pragma: no cover - passagem simples
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# --------------------------------------------------------------------- config


@app.get("/api/config")
def get_config():
    cfg = load_config()
    return cfg.public_dict()


@app.post("/api/config")
def post_config(payload: dict):
    cfg = save_config(payload or {})
    return cfg.public_dict()


# --------------------------------------------------------------------- estado


@app.get("/api/overview")
def get_overview():
    cfg = load_config()
    with db.closing_conn() as conn:
        data = queries.overview(conn)
        data["details_pending"] = sync.details_pending_count(conn, cfg)
    data["is_ready"] = cfg.is_ready
    data["sync"] = sync.STATE.snapshot()
    return data


# ----------------------------------------------------------------------- sync


@app.post("/api/sync")
async def post_sync(payload: dict | None = None):
    global _sync_task
    mode = ((payload or {}).get("mode") or "full").lower()
    if mode not in ("full", "details"):
        raise HTTPException(400, "mode deve ser 'full' ou 'details'.")
    if _sync_task and not _sync_task.done():
        raise HTTPException(409, "Ja existe uma sincronizacao em andamento.")

    cfg = load_config()
    if not cfg.is_ready:
        raise HTTPException(400, "Configure a chave da Steam Web API e o seu SteamID antes de sincronizar.")

    async def runner():
        try:
            await sync.run_sync(cfg, mode=mode)
        except asyncio.CancelledError:
            pass
        except Exception:  # o estado ja carrega a mensagem de erro para a UI
            pass

    _sync_task = asyncio.create_task(runner())
    await asyncio.sleep(0.05)
    return sync.STATE.snapshot()


@app.post("/api/sync/cancel")
async def post_sync_cancel():
    await sync.cancel_sync()
    return sync.STATE.snapshot()


@app.get("/api/sync/status")
def get_sync_status():
    return sync.STATE.snapshot()


# ---------------------------------------------------------------------- steam


def _online_from_cache() -> tuple[set[str], dict[str, dict]]:
    players = _online_cache["players"]
    return {sid for sid, p in players.items() if int(p.get("personastate") or 0) != 0}, players


async def _fetch_online() -> None:
    cfg = load_config()
    if not cfg.is_ready:
        raise SteamError("Chave da API / SteamID nao configurados.")
    with db.closing_conn() as conn:
        ids = [r["steamid"] for r in conn.execute("SELECT steamid FROM player WHERE is_friend = 1")]
    if not ids:
        _online_cache.update(at=time.time(), players={}, error="")
        return

    async with SteamClient(
        cfg.api_key,
        api_rate_per_sec=cfg.api_rate_per_sec,
        store_rate_per_sec=cfg.store_rate_per_sec,
    ) as client:
        players = await client.get_player_summaries(ids)
    _online_cache.update(at=time.time(), players=players, error="", failed_at=0.0)


async def _online_friend_ids(force: bool = False) -> tuple[set[str], dict[str, dict]]:
    """Amigos online agora. Nunca levanta excecao e nunca segura a UI:

    cache curto de sucesso, cooldown apos falha e timeout duro na chamada.
    """
    now = time.time()
    fresh = now - _online_cache["at"] < ONLINE_TTL
    cooling = now - _online_cache["failed_at"] < ONLINE_COOLDOWN
    if not force and (fresh or cooling):
        return _online_from_cache()

    try:
        await asyncio.wait_for(_fetch_online(), timeout=ONLINE_TIMEOUT)
    except Exception as exc:  # noqa: BLE001 — falha aqui vira 'sem dado de online', nunca erro na UI
        _online_cache["failed_at"] = now
        _online_cache["error"] = "tempo esgotado ao consultar a Steam" if isinstance(
            exc, asyncio.TimeoutError
        ) else str(exc)
    return _online_from_cache()


@app.get("/api/online")
async def get_online(force: bool = False):
    online_ids, players = await _online_friend_ids(force=force)
    error = _online_cache["error"]
    with db.closing_conn() as conn:
        names = {
            r["steamid"]: r["personaname"]
            for r in conn.execute("SELECT steamid, personaname FROM player WHERE is_friend = 1")
        }
    friends = []
    for sid in sorted(online_ids, key=lambda s: (names.get(s) or "").lower()):
        p = players.get(sid, {})
        friends.append(
            {
                "steamid": sid,
                "personaname": p.get("personaname") or names.get(sid) or sid,
                "avatar": p.get("avatarfull") or p.get("avatar"),
                "state": persona_state_label(p.get("personastate"), p.get("gameextrainfo")),
                "playing": p.get("gameextrainfo"),
                "playing_appid": int(p["gameid"]) if str(p.get("gameid") or "").isdigit() else None,
            }
        )
    return {"count": len(friends), "cached_at": _online_cache["at"], "error": error, "friends": friends}


# ---------------------------------------------------------------------- jogos


@app.get("/api/games")
async def get_games(
    ownership: str = "mine",
    min_friends: int = 0,
    min_friends_online: int = 0,
    multiplayer: str = "any",
    search: str = "",
    unplayed_by_me: bool = False,
    played_recently_by_friends: bool = False,
    include_unknown_details: bool = True,
    max_price: float | None = None,
    only_discounted: bool = False,
    min_discount: int = 0,
    include_free: bool = True,
    min_review_percent: int = 0,
    min_reviews: int = 0,
    include_unrated: bool = True,
    tag: str = "",
    genre: str = "",
    online: bool = False,
    sort: str = "friends",
    limit: int = Query(300, ge=1, le=2000),
    offset: int = Query(0, ge=0),
):
    online_ids: set[str] = set()
    online_error = ""
    if online or min_friends_online > 0 or sort == "friends_online":
        online_ids, _ = await _online_friend_ids()
        online_error = _online_cache["error"]

    with db.closing_conn() as conn:
        result = queries.list_games(
            conn,
            online_ids=online_ids,
            ownership=ownership,
            min_friends=min_friends,
            min_friends_online=min_friends_online,
            multiplayer=multiplayer,
            search=search,
            unplayed_by_me=unplayed_by_me,
            played_recently_by_friends=played_recently_by_friends,
            include_unknown_details=include_unknown_details,
            max_price=max_price,
            only_discounted=only_discounted,
            min_discount=min_discount,
            include_free=include_free,
            min_review_percent=min_review_percent,
            min_reviews=min_reviews,
            include_unrated=include_unrated,
            tag=tag,
            genre=genre,
            sort=sort,
            limit=limit,
            offset=offset,
        )
    result["online_friends"] = len(online_ids)
    if online_error:
        result["online_error"] = online_error
    return result


@app.get("/api/games/{appid}/friends")
async def get_game_friends(appid: int):
    online_ids, players = await _online_friend_ids()
    with db.closing_conn() as conn:
        friends = queries.friends_of_game(conn, appid, online_ids)
        row = conn.execute("SELECT appid, name, categories FROM app WHERE appid = ?", (appid,)).fetchone()
    for f in friends:
        p = players.get(f["steamid"], {})
        f["state"] = persona_state_label(p.get("personastate"), p.get("gameextrainfo"))
        f["playing"] = p.get("gameextrainfo")
    return {"appid": appid, "name": row["name"] if row else str(appid), "friends": friends}


@app.get("/api/friends")
def get_friends():
    with db.closing_conn() as conn:
        return {"friends": queries.friends_overview(conn)}


# ------------------------------------------------------------------ descoberta

_discover_task: asyncio.Task | None = None


@app.post("/api/discover")
async def post_discover(payload: dict | None = None):
    """Dispara a busca no catalogo da Steam com os criterios da interface."""
    global _discover_task
    if _discover_task and not _discover_task.done():
        raise HTTPException(409, "Ja existe uma busca em andamento.")
    if sync.STATE.running:
        raise HTTPException(409, "Espere a sincronizacao terminar para buscar no catalogo.")

    cfg = load_config()
    criteria = dict(payload or {})
    criteria.setdefault("enrich_limit", cfg.discover_enrich_limit)

    async def runner():
        try:
            await discover.run_discover(cfg, criteria)
        except asyncio.CancelledError:
            pass
        except Exception:   # o estado ja carrega a mensagem para a interface
            pass

    _discover_task = asyncio.create_task(runner())
    await asyncio.sleep(0.05)
    return discover.STATE.snapshot()


@app.get("/api/discover/status")
def get_discover_status():
    return discover.STATE.snapshot()


@app.post("/api/discover/cancel")
async def post_discover_cancel():
    await discover.cancel_discover()
    return discover.STATE.snapshot()


@app.get("/api/tags")
async def get_tags(q: str = "", refresh: bool = False):
    """Etiquetas da Steam (roguelite, soulslike...) para o autocompletar."""
    cfg = load_config()
    db.init_db()
    with db.closing_conn() as conn:
        conhecidas = conn.execute("SELECT COUNT(*) AS n FROM tag").fetchone()["n"]
    erro = ""
    if refresh or not conhecidas:
        try:
            await discover.refresh_tags(cfg)
        except SteamError as exc:
            erro = str(exc)
        except Exception as exc:  # noqa: BLE001
            erro = f"Falha ao baixar as etiquetas: {exc}"
    with db.closing_conn() as conn:
        tags = db.find_tags(conn, q, limit=25)
    return {"tags": tags, "error": erro}


@app.get("/api/facets")
def get_facets():
    """Generos e etiquetas ja presentes no cache, para montar os seletores."""
    with db.closing_conn() as conn:
        return {"genres": queries.genres_in_db(conn), "tags": queries.tags_in_db(conn)}


# ------------------------------------------------------------------- frontend

app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


@app.get("/")
def index():
    return FileResponse(str(WEB_DIR / "index.html"))
