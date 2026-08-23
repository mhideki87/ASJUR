"""Consultas de leitura usadas pela UI (a parte que realmente filtra os jogos)."""

from __future__ import annotations

import json
import sqlite3
from typing import Iterable

from . import db

SORTS = {
    "friends": "friends DESC, friends_recent DESC, name COLLATE NOCASE",
    "friends_online": "friends_online DESC, friends DESC, name COLLATE NOCASE",
    "friends_recent": "friends_recent DESC, friends DESC, name COLLATE NOCASE",
    "name": "name COLLATE NOCASE",
    "my_playtime": "my_playtime DESC, friends DESC",
    "my_playtime_asc": "my_playtime ASC, friends DESC",
    "last_played": "COALESCE(my_last_played, 0) DESC, friends DESC",
    "metacritic": "COALESCE(metacritic, -1) DESC, friends DESC",
}


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
    ownership: str = "mine",          # mine | all | not_mine
    min_friends: int = 0,
    min_friends_online: int = 0,
    multiplayer: str = "any",         # any | multiplayer | coop | online_coop | local_coop | pvp | remote_together
    search: str = "",
    unplayed_by_me: bool = False,
    played_recently_by_friends: bool = False,
    include_unknown_details: bool = True,
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
               a.release_date, a.details_state,
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
        item["header"] = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{item['appid']}/header.jpg"
        item["store_url"] = f"https://store.steampowered.com/app/{item['appid']}"
        item["run_url"] = f"steam://run/{item['appid']}"
        games.append(item)
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
