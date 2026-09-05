"""Consultas de leitura usadas pela UI (a parte que realmente filtra os jogos)."""

from __future__ import annotations

import json
import sqlite3
from typing import Iterable

from . import db

SORTS = {
    "friends": "friends DESC, friends_recent DESC, name COLLATE NOCASE",
    "review_wilson": "COALESCE(review_wilson, -1) DESC, COALESCE(review_total, 0) DESC",
    "review_percent": "COALESCE(review_percent, -1) DESC, COALESCE(review_total, 0) DESC",
    "review_total": "COALESCE(review_total, 0) DESC",
    "price_asc": "CASE WHEN price_final IS NULL THEN 1 ELSE 0 END, price_final ASC, name COLLATE NOCASE",
    "price_desc": "CASE WHEN price_final IS NULL THEN 1 ELSE 0 END, price_final DESC",
    "discount": "COALESCE(discount_percent, 0) DESC, COALESCE(review_wilson, 0) DESC",
    "release": "COALESCE(release_date, '') DESC",
    "friends_online": "friends_online DESC, friends DESC, name COLLATE NOCASE",
    "friends_recent": "friends_recent DESC, friends DESC, name COLLATE NOCASE",
    "name": "name COLLATE NOCASE",
    "my_playtime": "my_playtime DESC, friends DESC",
    "my_playtime_asc": "my_playtime ASC, friends DESC",
    "last_played": "COALESCE(my_last_played, 0) DESC, friends DESC",
    "metacritic": "COALESCE(metacritic, -1) DESC, friends DESC",
}



def _price_label(item: dict) -> str:
    """Texto curto de preco, na moeda que a loja devolveu."""
    if item.get("is_free") or item.get("price_final") == 0:
        return "Gratuito"
    final = item.get("price_final")
    if final is None:
        return ""
    symbol = {"BRL": "R$", "USD": "US$", "EUR": "€", "GBP": "£"}.get(item.get("currency") or "", "")
    value = f"{final / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    return f"{symbol} {value}".strip()


def _attach_tags(conn: sqlite3.Connection, games: list[dict]) -> None:
    if not games:
        return
    ids = [g["appid"] for g in games]
    placeholders = ",".join("?" * len(ids))
    por_app: dict[int, list[str]] = {}
    for row in conn.execute(
        f"SELECT appid, tag FROM app_tag WHERE appid IN ({placeholders}) ORDER BY tag COLLATE NOCASE",
        ids,
    ):
        por_app.setdefault(row["appid"], []).append(row["tag"])
    for game in games:
        game["tags"] = por_app.get(game["appid"], [])


def genres_in_db(conn: sqlite3.Connection) -> list[str]:
    """Generos presentes no cache, para montar o seletor da interface."""
    encontrados: set[str] = set()
    for row in conn.execute("SELECT genres FROM app WHERE genres IS NOT NULL AND genres != '[]'"):
        try:
            encontrados.update(json.loads(row["genres"] or "[]"))
        except json.JSONDecodeError:
            continue
    return sorted(g for g in encontrados if g)


def tags_in_db(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT tag, COUNT(*) AS n FROM app_tag GROUP BY tag ORDER BY n DESC, tag COLLATE NOCASE LIMIT 60"
    )
    return [r["tag"] for r in rows]


def self_steamid(conn: sqlite3.Connection) -> str:
    return db.get_meta(conn, "self_steamid") or ""


def _apply_online(conn: sqlite3.Connection, online_ids: Iterable[str] | None) -> bool:
    conn.execute("DROP TABLE IF EXISTS temp.online_now")
    conn.execute("CREATE TEMP TABLE online_now (steamid TEXT PRIMARY KEY)")
    ids = [(str(i),) for i in (online_ids or [])]
    if ids:
        conn.executemany("INSERT OR IGNORE INTO temp.online_now (steamid) VALUES (?)", ids)
    return True


def list_games(
    conn: sqlite3.Connection,
    *,
    online_ids: Iterable[str] | None = None,
    ownership: str = "mine",          # mine | library | friends | not_mine | any
    min_friends: int = 0,
    min_friends_online: int = 0,
    multiplayer: str = "any",         # any | multiplayer | coop | online_coop | local_coop | pvp | remote_together
    search: str = "",
    unplayed_by_me: bool = False,
    played_recently_by_friends: bool = False,
    include_unknown_details: bool = True,
    # --- catalogo: preco, avaliacao, estilo -----------------------------------
    max_price: float | None = None,   # na moeda da loja (ex.: 40 = R$ 40,00); 0 = so gratuitos
    only_discounted: bool = False,
    min_discount: int = 0,
    include_free: bool = True,
    min_review_percent: int = 0,
    min_reviews: int = 0,
    include_unrated: bool = True,
    tag: str = "",
    genre: str = "",
    sort: str = "friends",
    limit: int = 300,
    offset: int = 0,
) -> dict:
    me = self_steamid(conn)
    _apply_online(conn, online_ids)

    where: list[str] = ["COALESCE(a.type,'game') != 'dlc'"]
    params: dict = {"me": me}

    if ownership == "mine":
        where.append("mine.appid IS NOT NULL")
    elif ownership == "not_mine":
        where.append("mine.appid IS NULL")
    elif ownership in ("library", "all"):   # "all" e o nome antigo, mantido por compatibilidade
        where.append("(mine.appid IS NOT NULL OR COALESCE(fo.friends, 0) > 0)")
    elif ownership == "friends":
        where.append("COALESCE(fo.friends, 0) > 0")
    # "any" nao restringe: inclui o que veio da busca no catalogo

    if max_price is not None:
        if max_price <= 0:
            where.append("(a.is_free = 1 OR a.price_final = 0)")
        else:
            params["max_price"] = int(round(max_price * 100))
            free_clause = " OR a.is_free = 1 OR a.price_final = 0" if include_free else ""
            where.append(f"((a.price_final IS NOT NULL AND a.price_final <= :max_price){free_clause})")
    elif not include_free:
        where.append("COALESCE(a.is_free, 0) = 0 AND COALESCE(a.price_final, 1) > 0")

    if only_discounted or min_discount > 0:
        params["min_discount"] = max(1, min_discount)
        where.append("COALESCE(a.discount_percent, 0) >= :min_discount")

    if min_review_percent > 0 or min_reviews > 0:
        conds = []
        if min_review_percent > 0:
            params["min_review_percent"] = min_review_percent
            conds.append("a.review_percent >= :min_review_percent")
        if min_reviews > 0:
            params["min_reviews"] = min_reviews
            conds.append("COALESCE(a.review_total, 0) >= :min_reviews")
        rated = " AND ".join(conds)
        if include_unrated:
            where.append(f"(({rated}) OR a.reviews_synced IS NULL)")
        else:
            where.append(f"({rated})")

    if tag.strip():
        params["tag"] = tag.strip()
        where.append(
            "EXISTS (SELECT 1 FROM app_tag t WHERE t.appid = a.appid AND t.tag = :tag COLLATE NOCASE)"
        )

    if genre.strip():
        params["genre"] = f'%"{genre.strip()}"%'
        where.append("a.genres LIKE :genre COLLATE NOCASE")

    # Filtros sobre colunas agregadas ficam num WHERE externo (SQLite nao aceita
    # HAVING sem GROUP BY do jeito que a gente quer aqui).
    outer: list[str] = []
    if min_friends > 0:
        outer.append("friends >= :min_friends")
        params["min_friends"] = min_friends
    if min_friends_online > 0:
        outer.append("friends_online >= :min_friends_online")
        params["min_friends_online"] = min_friends_online
    if played_recently_by_friends:
        outer.append("friends_recent > 0")

    flag_column = {
        "multiplayer": "a.is_multiplayer",
        "coop": "a.is_coop",
        "online_coop": "a.is_online_coop",
        "local_coop": "a.is_local_coop",
        "pvp": "a.is_pvp",
        "remote_together": "a.is_remote_together",
    }.get(multiplayer)
    if flag_column:
        if include_unknown_details:
            where.append(f"({flag_column} = 1 OR a.details_state IS NULL OR a.details_state != 'ok')")
        else:
            where.append(f"{flag_column} = 1")

    if search.strip():
        where.append("a.name LIKE :search COLLATE NOCASE")
        params["search"] = f"%{search.strip()}%"

    if unplayed_by_me:
        where.append("COALESCE(mine.playtime_forever, 0) = 0")

    order = SORTS.get(sort, SORTS["friends"])
    params["limit"] = max(1, min(limit, 2000))
    params["offset"] = max(0, offset)

    base = f"""
        FROM app a
        LEFT JOIN ownership mine ON mine.appid = a.appid AND mine.steamid = :me
        LEFT JOIN (
            SELECT o.appid,
                   COUNT(*) AS friends,
                   SUM(CASE WHEN o.playtime_2weeks > 0 THEN 1 ELSE 0 END) AS friends_recent,
                   SUM(CASE WHEN on_now.steamid IS NOT NULL THEN 1 ELSE 0 END) AS friends_online
            FROM ownership o
            JOIN player p ON p.steamid = o.steamid AND p.is_friend = 1
            LEFT JOIN temp.online_now on_now ON on_now.steamid = o.steamid
            GROUP BY o.appid
        ) fo ON fo.appid = a.appid
        WHERE {' AND '.join(where)}
    """

    inner = f"""
        SELECT a.appid, a.name, a.icon, a.categories, a.genres, a.type, a.metacritic,
               a.release_date, a.details_state, a.discovered_at,
               a.price_final, a.price_initial, a.discount_percent, a.currency, a.is_free,
               a.review_score, a.review_desc, a.review_positive, a.review_total,
               a.review_percent, a.review_wilson, a.reviews_synced,
               a.is_multiplayer, a.is_coop, a.is_online_coop, a.is_local_coop, a.is_pvp,
               a.is_remote_together,
               COALESCE(fo.friends, 0)        AS friends,
               COALESCE(fo.friends_recent, 0) AS friends_recent,
               COALESCE(fo.friends_online, 0) AS friends_online,
               CASE WHEN mine.appid IS NULL THEN 0 ELSE 1 END AS i_own,
               COALESCE(mine.playtime_forever, 0) AS my_playtime,
               COALESCE(mine.playtime_2weeks, 0)  AS my_playtime_2weeks,
               mine.last_played AS my_last_played
        {base}
    """
    outer_where = f"WHERE {' AND '.join(outer)}" if outer else ""

    rows = conn.execute(
        f"SELECT * FROM ({inner}) {outer_where} ORDER BY {order} LIMIT :limit OFFSET :offset", params
    ).fetchall()
    total = conn.execute(
        f"SELECT COUNT(*) AS total FROM ({inner}) {outer_where}", params
    ).fetchone()["total"]

    games = []
    for r in rows:
        item = dict(r)
        item["categories"] = json.loads(item["categories"] or "[]")
        item["genres"] = json.loads(item["genres"] or "[]")
        item["tags"] = []
        item["price_label"] = _price_label(item)
        item["header"] = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{item['appid']}/header.jpg"
        item["store_url"] = f"https://store.steampowered.com/app/{item['appid']}"
        item["run_url"] = f"steam://run/{item['appid']}"
        games.append(item)
    _attach_tags(conn, games)
    return {"total": total, "games": games}


def friends_of_game(conn: sqlite3.Connection, appid: int, online_ids: Iterable[str] | None = None) -> list[dict]:
    _apply_online(conn, online_ids)
    rows = conn.execute(
        """
        SELECT p.steamid, p.personaname, p.avatar, p.profileurl,
               o.playtime_forever, o.playtime_2weeks, o.last_played,
               CASE WHEN on_now.steamid IS NULL THEN 0 ELSE 1 END AS online
        FROM ownership o
        JOIN player p ON p.steamid = o.steamid AND p.is_friend = 1
        LEFT JOIN temp.online_now on_now ON on_now.steamid = o.steamid
        WHERE o.appid = ?
        ORDER BY online DESC, o.playtime_2weeks DESC, o.playtime_forever DESC,
                 p.personaname COLLATE NOCASE
        """,
        (appid,),
    ).fetchall()
    return [dict(r) for r in rows]


def friends_overview(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT p.steamid, p.personaname, p.avatar, p.profileurl, p.library_state, p.games_count,
               p.last_synced,
               (SELECT COUNT(*) FROM ownership o
                 WHERE o.steamid = p.steamid
                   AND o.appid IN (SELECT appid FROM ownership WHERE steamid = ?)) AS shared_with_me
        FROM player p
        WHERE p.is_friend = 1
        ORDER BY (p.library_state = 'public') DESC, shared_with_me DESC,
                 p.personaname COLLATE NOCASE
        """,
        (self_steamid(conn),),
    ).fetchall()
    return [dict(r) for r in rows]


def overview(conn: sqlite3.Connection) -> dict:
    me = self_steamid(conn)
    row = conn.execute(
        """
        SELECT
          (SELECT personaname FROM player WHERE is_self = 1)                              AS me_name,
          (SELECT avatar FROM player WHERE is_self = 1)                                   AS me_avatar,
          (SELECT COUNT(*) FROM ownership WHERE steamid = ?)                              AS my_games,
          (SELECT COUNT(*) FROM player WHERE is_friend = 1)                               AS friends,
          (SELECT COUNT(*) FROM player WHERE is_friend = 1 AND library_state = 'public')  AS friends_public,
          (SELECT COUNT(*) FROM player WHERE is_friend = 1 AND library_state = 'private') AS friends_private,
          (SELECT COUNT(*) FROM app)                                                      AS apps,
          (SELECT COUNT(*) FROM app WHERE details_state = 'ok')                           AS apps_detailed
        """,
        (me,),
    ).fetchone()
    data = dict(row)
    data["self_steamid"] = me
    data["last_sync_at"] = int(db.get_meta(conn, "last_sync_at") or 0) or None
    return data
