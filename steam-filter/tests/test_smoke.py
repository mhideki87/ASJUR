"""Teste de ponta a ponta com a Steam falsificada (nenhuma chamada real de rede).

    python tests/test_smoke.py     # ou: pytest tests/test_smoke.py
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_EXISTING = os.environ.get("STEAM_FILTER_DATA")
WORKDIR = Path(_EXISTING or tempfile.mkdtemp(prefix="steam-filter-test-"))
os.environ["STEAM_FILTER_DATA"] = str(WORKDIR)
os.environ["STEAM_API_KEY"] = "TESTKEY"
os.environ["STEAM_ID"] = "76561197960287930"

from steam_filter import db, queries, sync  # noqa: E402
from steam_filter.config import Config  # noqa: E402
from steam_filter.steam_api import SteamClient  # noqa: E402

ME = "76561197960287930"
FRIENDS = {
    "76561198000000001": "Ana",
    "76561198000000002": "Bruno",
    "76561198000000003": "Carla",   # biblioteca privada
}
LIBRARIES = {
    ME: [
        {"appid": 10, "name": "Counter-Strike", "playtime_forever": 600, "playtime_2weeks": 30},
        {"appid": 20, "name": "Portal 2", "playtime_forever": 0},
        {"appid": 40, "name": "Stardew Valley", "playtime_forever": 120},
    ],
    "76561198000000001": [
        {"appid": 10, "name": "Counter-Strike", "playtime_forever": 900, "playtime_2weeks": 60},
        {"appid": 20, "name": "Portal 2", "playtime_forever": 300},
        {"appid": 30, "name": "Deep Rock Galactic", "playtime_forever": 400},
    ],
    "76561198000000002": [
        {"appid": 10, "name": "Counter-Strike", "playtime_forever": 100},
        {"appid": 30, "name": "Deep Rock Galactic", "playtime_forever": 50, "playtime_2weeks": 10},
    ],
}
STORE = {
    10: {"name": "Counter-Strike", "type": "game",
         "categories": [{"description": "Multi-player"}, {"description": "Online PvP"}],
         "genres": [{"description": "Action"}], "metacritic": {"score": 88}},
    20: {"name": "Portal 2", "type": "game",
         "categories": [{"description": "Online Co-op"}, {"description": "Shared/Split Screen Co-op"}],
         "genres": [{"description": "Puzzle"}]},
    30: {"name": "Deep Rock Galactic", "type": "game",
         "categories": [{"description": "Online Co-op"}], "genres": [{"description": "Action"}]},
    40: {"name": "Stardew Valley", "type": "game",
         "categories": [{"description": "Single-player"}], "genres": [{"description": "RPG"}]},
}
CALLS: dict[str, int] = {}


def handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    params = dict(request.url.params)
    CALLS[path] = CALLS.get(path, 0) + 1

    if path.endswith("GetPlayerSummaries/v2/"):
        ids = params["steamids"].split(",")
        players = []
        for i, sid in enumerate(ids):
            name = "Eu" if sid == ME else FRIENDS.get(sid, sid)
            players.append({
                "steamid": sid, "personaname": name,
                "avatarfull": f"https://avatars/{sid}.jpg",
                "profileurl": f"https://steamcommunity.com/profiles/{sid}/",
                "personastate": 1 if i % 2 == 0 else 0,
            })
        return httpx.Response(200, json={"response": {"players": players}})

    if path.endswith("GetFriendList/v1/"):
        return httpx.Response(200, json={"friendslist": {"friends": [
            {"steamid": sid, "relationship": "friend", "friend_since": 1500000000} for sid in FRIENDS
        ]}})

    if path.endswith("GetOwnedGames/v1/"):
        sid = params["steamid"]
        if sid not in LIBRARIES:                      # Carla: perfil privado
            return httpx.Response(200, json={"response": {}})
        games = LIBRARIES[sid]
        return httpx.Response(200, json={"response": {"game_count": len(games), "games": games}})

    if path.endswith("/api/appdetails"):
        appid = int(params["appids"])
        data = STORE.get(appid)
        if not data:
            return httpx.Response(200, json={str(appid): {"success": False}})
        return httpx.Response(200, json={str(appid): {"success": True, "data": data}})

    return httpx.Response(404, json={"error": f"rota falsa nao mapeada: {path}"})


def make_client() -> SteamClient:
    return SteamClient(
        "TESTKEY",
        api_rate_per_sec=1000,
        store_rate_per_sec=1000,
        transport=httpx.MockTransport(handler),
    )


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(f"FALHOU: {label}")
    print(f"  ok — {label}")


def test_everything() -> None:
    cfg = Config(api_key="TESTKEY", steam_id=ME, store_budget_per_sync=100, details_min_friends=1)
    stats = asyncio.run(sync.run_sync(cfg, mode="full", client_factory=make_client))
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    check(stats["my_games"] == 3, "minha biblioteca com 3 jogos")
    check(stats["friends"] == 3, "3 amigos encontrados")
    check(stats["friends_public"] == 2 and stats["friends_private"] == 1, "1 amigo privado detectado")
    check(stats["details_ok"] == 4, "detalhes de loja gravados para os 4 apps")

    conn = db.connect()

    # Contagem de amigos por jogo -----------------------------------------
    result = queries.list_games(conn, ownership="mine", min_friends=0, sort="friends")
    by_name = {g["name"]: g for g in result["games"]}
    check(by_name["Counter-Strike"]["friends"] == 2, "Counter-Strike: 2 amigos")
    check(by_name["Portal 2"]["friends"] == 1, "Portal 2: 1 amigo")
    check(by_name["Stardew Valley"]["friends"] == 0, "Stardew Valley: 0 amigos")
    check(result["games"][0]["name"] == "Counter-Strike", "ordenacao por nº de amigos")

    # Filtro por minimo de amigos ------------------------------------------
    only2 = queries.list_games(conn, ownership="mine", min_friends=2)
    check(only2["total"] == 1, "min_friends=2 deixa so 1 jogo")

    # Jogos que so os amigos tem -------------------------------------------
    theirs = queries.list_games(conn, ownership="not_mine", min_friends=1)
    check([g["name"] for g in theirs["games"]] == ["Deep Rock Galactic"], "sugestao do que eu nao tenho")

    # Filtro por categoria -------------------------------------------------
    coop = queries.list_games(conn, ownership="all", multiplayer="online_coop",
                              include_unknown_details=False, min_friends=1)
    check({g["name"] for g in coop["games"]} == {"Portal 2", "Deep Rock Galactic"}, "filtro co-op online")
    pvp = queries.list_games(conn, ownership="all", multiplayer="pvp", include_unknown_details=False)
    check({g["name"] for g in pvp["games"]} == {"Counter-Strike"}, "filtro PvP")
    check(by_name["Stardew Valley"]["is_multiplayer"] == 0, "single-player nao vira multiplayer")

    # Amigos online agora --------------------------------------------------
    online = {"76561198000000001"}
    live = queries.list_games(conn, ownership="mine", online_ids=online, min_friends_online=1,
                              sort="friends_online")
    check([g["name"] for g in live["games"]] == ["Counter-Strike", "Portal 2"], "filtro por amigo online")

    # Nunca joguei ---------------------------------------------------------
    unplayed = queries.list_games(conn, ownership="mine", unplayed_by_me=True, min_friends=1)
    check([g["name"] for g in unplayed["games"]] == ["Portal 2"], "filtro 'eu nunca joguei'")

    # Busca ----------------------------------------------------------------
    found = queries.list_games(conn, ownership="all", search="portal", min_friends=0)
    check(found["total"] == 1, "busca por nome")

    # Quem tem o jogo ------------------------------------------------------
    who = queries.friends_of_game(conn, 10, online)
    check([f["personaname"] for f in who] == ["Ana", "Bruno"], "lista de quem tem o jogo (online primeiro)")

    # Panorama -------------------------------------------------------------
    ov = queries.overview(conn)
    check(ov["friends_public"] == 2 and ov["friends_private"] == 1, "panorama de cobertura")
    check(queries.friends_overview(conn)[0]["shared_with_me"] == 2, "jogos em comum com o amigo")

    # Reexecucao: nao rebusca detalhes ja gravados --------------------------
    before = CALLS.get("/api/appdetails", 0)
    asyncio.run(sync.run_sync(cfg, mode="details", client_factory=make_client))
    check(CALLS.get("/api/appdetails", 0) == before, "cache da loja evita rebuscar detalhes")

    # Sincronizar de novo nao duplica ---------------------------------------
    asyncio.run(sync.run_sync(cfg, mode="full", client_factory=make_client))
    again = queries.list_games(conn, ownership="mine", min_friends=0)
    check(again["total"] == result["total"], "resincronizar nao duplica jogos")

    conn.close()


def test_http_api() -> None:
    from fastapi.testclient import TestClient
    from steam_filter.server import app

    with TestClient(app) as client:
        resp = client.get("/api/overview")
        check(resp.status_code == 200 and resp.json()["my_games"] == 3, "GET /api/overview")

        resp = client.get("/api/games", params={"ownership": "mine", "min_friends": 1, "sort": "friends"})
        payload = resp.json()
        check(resp.status_code == 200 and payload["games"][0]["name"] == "Counter-Strike", "GET /api/games")

        resp = client.get("/api/games/10/friends")
        check(len(resp.json()["friends"]) == 2, "GET /api/games/{id}/friends")

        resp = client.get("/api/friends")
        check(len(resp.json()["friends"]) == 3, "GET /api/friends")

        resp = client.get("/api/config")
        check("*" in resp.json()["api_key"], "GET /api/config mascara a chave")

        resp = client.get("/")
        check(resp.status_code == 200 and "Steam Game Filter" in resp.text, "GET / entrega a interface")


if __name__ == "__main__":
    try:
        print("\n== sincronizacao + consultas ==")
        test_everything()
        print("\n== API HTTP ==")
        test_http_api()
        print("\nTODOS OS TESTES PASSARAM")
    finally:
        if not _EXISTING:
            shutil.rmtree(WORKDIR, ignore_errors=True)
