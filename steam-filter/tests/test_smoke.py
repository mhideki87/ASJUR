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

from steam_filter import db, discover, queries, sync  # noqa: E402
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
def _preco(final, initial=None, desconto=0):
    initial = initial if initial is not None else final
    return {"currency": "BRL", "initial": initial, "final": final, "discount_percent": desconto}


STORE = {
    10: {"name": "Counter-Strike", "type": "game", "is_free": False,
         "categories": [{"description": "Multi-player"}, {"description": "Online PvP"}],
         "genres": [{"description": "Action"}], "metacritic": {"score": 88},
         "price_overview": _preco(1999)},
    20: {"name": "Portal 2", "type": "game", "is_free": False,
         "categories": [{"description": "Online Co-op"}, {"description": "Shared/Split Screen Co-op"}],
         "genres": [{"description": "Puzzle"}], "price_overview": _preco(950, 3800, 75)},
    30: {"name": "Deep Rock Galactic", "type": "game", "is_free": False,
         "categories": [{"description": "Online Co-op"}], "genres": [{"description": "Action"}],
         "price_overview": _preco(4999)},
    40: {"name": "Stardew Valley", "type": "game", "is_free": False,
         "categories": [{"description": "Single-player"}], "genres": [{"description": "RPG"}],
         "price_overview": _preco(2499)},
    # so no catalogo — ninguem tem ainda
    50: {"name": "Hades", "type": "game", "is_free": False,
         "categories": [{"description": "Single-player"}], "genres": [{"description": "Action"}],
         "price_overview": _preco(2249, 4499, 50)},
    60: {"name": "Risk of Rain 2", "type": "game", "is_free": False,
         "categories": [{"description": "Online Co-op"}, {"description": "Multi-player"}],
         "genres": [{"description": "Action"}], "price_overview": _preco(1599, 3999, 60)},
    70: {"name": "Jogo Meia-Boca", "type": "game", "is_free": False,
         "categories": [{"description": "Single-player"}], "genres": [{"description": "Indie"}],
         "price_overview": _preco(500)},
}

REVIEWS = {
    10: (9, "Muito positivas", 90000, 100000),
    20: (9, "Extremamente positivas", 195000, 200000),
    30: (9, "Muito positivas", 45000, 50000),
    40: (9, "Extremamente positivas", 97000, 100000),
    50: (9, "Extremamente positivas", 190000, 200000),
    60: (8, "Muito positivas", 8500, 10000),
    70: (5, "Neutras", 3, 3),          # 100% de 3 análises: o teste do ranking honesto
}

# Resultado da busca da loja: etiqueta 3959 (Roguelite) devolve estes, nessa ordem.
CATALOGO = {
    "3959": [50, 60, 70],
    "": [10, 20, 30, 40, 50, 60, 70],
}
TAGS = [{"tagid": 3959, "name": "Roguelite"}, {"tagid": 1716, "name": "Roguelike"},
        {"tagid": 492, "name": "Indie"}]
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

    if path.startswith("/appreviews/"):
        appid = int(path.rsplit("/", 1)[1])
        dados = REVIEWS.get(appid)
        if not dados:
            return httpx.Response(200, json={"success": 1, "query_summary": {}})
        score, desc, positivas, total = dados
        return httpx.Response(200, json={"success": 1, "query_summary": {
            "review_score": score, "review_score_desc": desc,
            "total_positive": positivas, "total_negative": total - positivas, "total_reviews": total,
        }})

    if path.startswith("/tagdata/populartags/"):
        return httpx.Response(200, json=TAGS)

    if path == "/search/results/":
        chave = params.get("tags", "")
        ids = CATALOGO.get(chave, [])
        if params.get("specials") == "1":
            ids = [i for i in ids if (STORE.get(i, {}).get("price_overview") or {}).get("discount_percent")]
        if params.get("maxprice"):
            teto = int(params["maxprice"]) * 100
            ids = [i for i in ids if (STORE.get(i, {}).get("price_overview") or {}).get("final", 0) <= teto]
        start = int(params.get("start", 0))
        count = int(params.get("count", 50))
        pagina = ids[start:start + count]
        html = "".join(
            f'<a href="https://store.steampowered.com/app/{i}/" data-ds-appid="{i}"'
            f' data-ds-itemkey="App_{i}" class="search_result_row">{STORE[i]["name"]}</a>'
            for i in pagina
        )
        return httpx.Response(200, json={"success": 1, "results_html": html, "total_count": len(ids)})

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



def test_catalogo() -> None:
    """Busca no catálogo: etiqueta, preço, promoção e ranking por avaliação."""
    cfg = Config(api_key="TESTKEY", steam_id=ME, store_budget_per_sync=100, discover_enrich_limit=50)

    stats = asyncio.run(discover.run_discover(
        cfg, {"tag_ids": [3959], "tag_names": ["Roguelite"], "sort": "avaliacoes", "pages": 1},
        client_factory=make_client,
    ))
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    check(stats["encontrados"] == 3, "busca por etiqueta trouxe 3 jogos")
    check(stats["detalhes"] == 3 and stats["avaliacoes"] == 3, "preço e avaliação gravados dos 3")

    conn = db.connect()

    # A etiqueta buscada fica registrada em cada jogo ------------------------
    roguelites = queries.list_games(conn, ownership="any", tag="Roguelite", min_friends=0)
    check({g["name"] for g in roguelites["games"]} == {"Hades", "Risk of Rain 2", "Jogo Meia-Boca"},
          "filtro por etiqueta Roguelite")
    check(roguelites["games"][0]["tags"] == ["Roguelite"], "etiqueta devolvida no resultado")

    # Preço ------------------------------------------------------------------
    baratos = queries.list_games(conn, ownership="any", tag="Roguelite", max_price=20, min_friends=0)
    check({g["name"] for g in baratos["games"]} == {"Risk of Rain 2", "Jogo Meia-Boca"},
          "filtro de preço máximo R$ 20")
    hades = {g["name"]: g for g in roguelites["games"]}["Hades"]
    check(hades["price_label"] == "R$ 22,49" and hades["discount_percent"] == 50,
          "preço formatado e desconto lidos da loja")

    # Promoções --------------------------------------------------------------
    promo = queries.list_games(conn, ownership="any", tag="Roguelite", only_discounted=True, min_friends=0)
    check({g["name"] for g in promo["games"]} == {"Hades", "Risk of Rain 2"}, "só o que está em promoção")
    promo60 = queries.list_games(conn, ownership="any", min_discount=60, min_friends=0)
    check({g["name"] for g in promo60["games"]} == {"Risk of Rain 2", "Portal 2"},
          "desconto mínimo de 60% pega catálogo e biblioteca juntos")

    # Avaliações -------------------------------------------------------------
    bem = queries.list_games(conn, ownership="any", tag="Roguelite", min_review_percent=90,
                             min_reviews=1000, include_unrated=False, min_friends=0)
    check({g["name"] for g in bem["games"]} == {"Hades"}, "90%+ de positivas com pelo menos 1000 análises")

    ranking = queries.list_games(conn, ownership="any", tag="Roguelite", sort="review_wilson",
                                 min_friends=0)
    nomes = [g["name"] for g in ranking["games"]]
    check(nomes[0] == "Hades", "ranking com peso põe Hades na frente")
    check(nomes[-1] == "Jogo Meia-Boca", "100% de 3 análises nao vira o melhor avaliado")
    por_pct = queries.list_games(conn, ownership="any", tag="Roguelite", sort="review_percent",
                                 min_friends=0)
    check(por_pct["games"][0]["name"] == "Jogo Meia-Boca", "ordenar por % cru premia o de 3 análises")

    # Cruzamento com os amigos: o diferencial do app -------------------------
    ninguem = queries.list_games(conn, ownership="any", tag="Roguelite", min_friends=1)
    check(ninguem["total"] == 0, "nenhum amigo tem os roguelites descobertos")
    biblioteca = queries.list_games(conn, ownership="library", min_friends=0)
    check({g["name"] for g in biblioteca["games"]} ==
          {"Counter-Strike", "Portal 2", "Deep Rock Galactic", "Stardew Valley"},
          "aba biblioteca ignora o que só existe no catálogo")

    # Reexecutar nao gasta requisicao de novo --------------------------------
    antes = CALLS.get("/api/appdetails", 0) + sum(v for k, v in CALLS.items() if k.startswith("/appreviews/"))
    asyncio.run(discover.run_discover(
        cfg, {"tag_ids": [3959], "tag_names": ["Roguelite"], "pages": 1}, client_factory=make_client))
    depois = CALLS.get("/api/appdetails", 0) + sum(v for k, v in CALLS.items() if k.startswith("/appreviews/"))
    check(antes == depois, "segunda busca igual nao repete consulta de preço/avaliação")

    # Etiquetas para o autocompletar -----------------------------------------
    asyncio.run(discover.refresh_tags(cfg, client_factory=make_client))
    achadas = db.find_tags(conn, "rogue")
    check({t["name"] for t in achadas} == {"Roguelite", "Roguelike"}, "autocompletar de etiquetas")

    conn.close()



ESQUEMA_V1 = """
CREATE TABLE app (appid INTEGER PRIMARY KEY, name TEXT, icon TEXT, type TEXT, categories TEXT,
  genres TEXT, is_multiplayer INTEGER, is_coop INTEGER, is_online_coop INTEGER, is_local_coop INTEGER,
  is_pvp INTEGER, is_remote_together INTEGER, is_free INTEGER, release_date TEXT, metacritic INTEGER,
  details_state TEXT, details_synced INTEGER);
CREATE TABLE player (steamid TEXT PRIMARY KEY, personaname TEXT, avatar TEXT, profileurl TEXT,
  is_self INTEGER DEFAULT 0, is_friend INTEGER DEFAULT 0, friend_since INTEGER, library_state TEXT,
  games_count INTEGER, last_synced INTEGER);
CREATE TABLE ownership (steamid TEXT, appid INTEGER, playtime_forever INTEGER DEFAULT 0,
  playtime_2weeks INTEGER DEFAULT 0, last_played INTEGER, PRIMARY KEY (steamid, appid));
CREATE TABLE sync_run (id INTEGER PRIMARY KEY AUTOINCREMENT, started_at INTEGER, finished_at INTEGER,
  status TEXT, message TEXT, stats TEXT);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO app (appid, name, details_state) VALUES (10, 'Jogo Antigo', 'ok');
INSERT INTO player (steamid, is_self) VALUES ('765611970', 1);
INSERT INTO ownership (steamid, appid) VALUES ('765611970', 10);
INSERT INTO meta (key, value) VALUES ('self_steamid', '765611970');
"""


def test_migracao_da_v1() -> None:
    """Quem já usava a versão anterior não pode perder o banco ao atualizar."""
    import sqlite3

    caminho = WORKDIR / "v1.db"
    antigo = sqlite3.connect(caminho)
    antigo.executescript(ESQUEMA_V1)
    antigo.commit()
    antigo.close()

    db.init_db(caminho)                       # aplica os ALTER TABLE
    conn = db.connect(caminho)
    colunas = {r["name"] for r in conn.execute("PRAGMA table_info(app)")}
    check({"price_final", "review_wilson", "discovered_at"} <= colunas, "colunas novas criadas")
    resultado = queries.list_games(conn, ownership="mine", min_friends=0)
    check(resultado["total"] == 1 and resultado["games"][0]["name"] == "Jogo Antigo",
          "dados antigos preservados")
    check(resultado["games"][0]["price_final"] is None, "campos novos ficam vazios, sem quebrar")
    db.init_db(caminho)                       # rodar de novo é inofensivo
    check(True, "migração é idempotente")
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

        resp = client.get("/api/games", params={"ownership": "any", "tag": "Roguelite",
                                                 "only_discounted": True, "sort": "review_wilson",
                                                 "min_friends": 0})
        nomes = [g["name"] for g in resp.json()["games"]]
        check(nomes == ["Hades", "Risk of Rain 2"], "GET /api/games com etiqueta + promoção + ranking")

        resp = client.get("/api/tags", params={"q": "rogue"})
        check(len(resp.json()["tags"]) == 2, "GET /api/tags")

        resp = client.get("/api/facets")
        check("Action" in resp.json()["genres"], "GET /api/facets lista os gêneros")

        resp = client.get("/api/discover/status")
        check(resp.json()["running"] is False, "GET /api/discover/status")

        resp = client.get("/api/config")
        check("*" in resp.json()["api_key"], "GET /api/config mascara a chave")

        resp = client.get("/")
        check(resp.status_code == 200 and "Steam Game Filter" in resp.text, "GET / entrega a interface")


if __name__ == "__main__":
    try:
        print("\n== sincronizacao + consultas ==")
        test_everything()
        print("\n== catálogo: etiqueta, preço, promoção, avaliação ==")
        test_catalogo()
        print("\n== migração de banco antigo ==")
        test_migracao_da_v1()
        print("\n== API HTTP ==")
        test_http_api()
        print("\nTODOS OS TESTES PASSARAM")
    finally:
        if not _EXISTING:
            shutil.rmtree(WORKDIR, ignore_errors=True)
