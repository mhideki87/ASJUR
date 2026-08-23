"""Camada SQLite: cache local da biblioteca, dos amigos e dos detalhes de loja."""

from __future__ import annotations

import json
import math
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from .config import DB_PATH

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS player (
    steamid       TEXT PRIMARY KEY,
    personaname   TEXT,
    avatar        TEXT,
    profileurl    TEXT,
    is_self       INTEGER NOT NULL DEFAULT 0,
    is_friend     INTEGER NOT NULL DEFAULT 0,
    friend_since  INTEGER,
    library_state TEXT,               -- 'public' | 'private' | 'error' | NULL (nunca tentado)
    games_count   INTEGER,
    last_synced   INTEGER
);

CREATE TABLE IF NOT EXISTS app (
    appid              INTEGER PRIMARY KEY,
    name               TEXT,
    icon               TEXT,
    type               TEXT,
    categories         TEXT,          -- JSON: lista de nomes de categoria
    genres             TEXT,          -- JSON: lista de nomes de genero
    is_multiplayer     INTEGER,
    is_coop            INTEGER,
    is_online_coop     INTEGER,
    is_local_coop      INTEGER,
    is_pvp             INTEGER,
    is_remote_together INTEGER,
    is_free            INTEGER,
    release_date       TEXT,
    metacritic         INTEGER,
    details_state      TEXT,          -- 'ok' | 'missing' | 'error' | NULL
    details_synced     INTEGER,
    -- preco (centavos da moeda da loja configurada)
    price_final        INTEGER,
    price_initial      INTEGER,
    discount_percent   INTEGER,
    currency           TEXT,
    price_synced       INTEGER,
    -- avaliacoes dos usuarios
    review_score       INTEGER,       -- 0..9, escala da propria Steam
    review_desc        TEXT,
    review_positive    INTEGER,
    review_total       INTEGER,
    review_percent     INTEGER,       -- % de positivas, calculado aqui
    review_wilson      REAL,          -- limite inferior de Wilson: ranking honesto
    reviews_synced     INTEGER,
    -- proveniencia
    discovered_at      INTEGER        -- veio da busca no catalogo, nao de uma biblioteca
);

CREATE TABLE IF NOT EXISTS app_tag (
    appid INTEGER NOT NULL,
    tag   TEXT NOT NULL,
    PRIMARY KEY (appid, tag)
);
CREATE INDEX IF NOT EXISTS app_tag_tag ON app_tag(tag COLLATE NOCASE);

CREATE TABLE IF NOT EXISTS tag (
    tagid  INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    synced INTEGER
);
CREATE INDEX IF NOT EXISTS tag_name ON tag(name COLLATE NOCASE);

CREATE TABLE IF NOT EXISTS ownership (
    steamid          TEXT NOT NULL,
    appid            INTEGER NOT NULL,
    playtime_forever INTEGER NOT NULL DEFAULT 0,
    playtime_2weeks  INTEGER NOT NULL DEFAULT 0,
    last_played      INTEGER,
    PRIMARY KEY (steamid, appid)
);
CREATE INDEX IF NOT EXISTS ownership_appid ON ownership(appid);

CREATE TABLE IF NOT EXISTS sync_run (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at  INTEGER NOT NULL,
    finished_at INTEGER,
    status      TEXT NOT NULL,        -- 'running' | 'done' | 'error' | 'cancelled'
    message     TEXT,
    stats       TEXT
);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

_MULTI_CATEGORIES = {
    "multi-player": "is_multiplayer",
    "multiplayer": "is_multiplayer",
    "multijogador": "is_multiplayer",
    "co-op": "is_coop",
    "cooperativo": "is_coop",
    "online co-op": "is_online_coop",
    "cooperativo online": "is_online_coop",
    "shared/split screen co-op": "is_local_coop",
    "cooperativo em tela dividida/compartilhada": "is_local_coop",
    "shared/split screen": "is_local_coop",
    "tela dividida/compartilhada": "is_local_coop",
    "pvp": "is_pvp",
    "online pvp": "is_pvp",
    "pvp online": "is_pvp",
    "shared/split screen pvp": "is_pvp",
    "pvp em tela dividida/compartilhada": "is_pvp",
    "lan co-op": "is_online_coop",
    "lan pvp": "is_pvp",
    "cross-platform multiplayer": "is_multiplayer",
    "multijogador multiplataforma": "is_multiplayer",
    "remote play together": "is_remote_together",
    "steam remote play together": "is_remote_together",
    "jogo remoto em conjunto": "is_remote_together",
}


def classify_categories(names: Iterable[str]) -> dict[str, int]:
    flags = {
        "is_multiplayer": 0,
        "is_coop": 0,
        "is_online_coop": 0,
        "is_local_coop": 0,
        "is_pvp": 0,
        "is_remote_together": 0,
    }
    for raw in names:
        key = (raw or "").strip().lower()
        field = _MULTI_CATEGORIES.get(key)
        if field:
            flags[field] = 1
    # Co-op online / local / PvP implicam multiplayer, mesmo quando a Steam nao marca "Multi-player".
    if any(flags[f] for f in ("is_coop", "is_online_coop", "is_local_coop", "is_pvp")):
        flags["is_multiplayer"] = 1
    if flags["is_online_coop"] or flags["is_local_coop"]:
        flags["is_coop"] = 1
    return flags


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = Path(path or DB_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


# Colunas acrescentadas depois da primeira versao — bases antigas recebem ALTER TABLE.
_APP_COLUMNS_V2 = {
    "price_final": "INTEGER",
    "price_initial": "INTEGER",
    "discount_percent": "INTEGER",
    "currency": "TEXT",
    "price_synced": "INTEGER",
    "review_score": "INTEGER",
    "review_desc": "TEXT",
    "review_positive": "INTEGER",
    "review_total": "INTEGER",
    "review_percent": "INTEGER",
    "review_wilson": "REAL",
    "reviews_synced": "INTEGER",
    "discovered_at": "INTEGER",
}


def _migrate(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(app)")}
    for column, kind in _APP_COLUMNS_V2.items():
        if column not in existing:
            conn.execute(f"ALTER TABLE app ADD COLUMN {column} {kind}")


def init_db(path: Path | None = None) -> None:
    with closing_conn(path) as conn:
        conn.executescript(SCHEMA)
        _migrate(conn)
        conn.commit()


@contextmanager
def closing_conn(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(path)
    try:
        yield conn
    finally:
        conn.close()


def now() -> int:
    return int(time.time())


# --------------------------------------------------------------------------- writes


def upsert_player(conn: sqlite3.Connection, steamid: str, **fields) -> None:
    fields = {k: v for k, v in fields.items() if v is not None}
    cols = ", ".join(fields)
    placeholders = ", ".join(f":{k}" for k in fields)
    updates = ", ".join(f"{k}=excluded.{k}" for k in fields)
    sql = f"INSERT INTO player (steamid{', ' + cols if cols else ''}) VALUES (:steamid{', ' + placeholders if cols else ''})"
    if updates:
        sql += f" ON CONFLICT(steamid) DO UPDATE SET {updates}"
    else:
        sql += " ON CONFLICT(steamid) DO NOTHING"
    conn.execute(sql, {"steamid": steamid, **fields})


def replace_ownership(conn: sqlite3.Connection, steamid: str, games: list[dict]) -> int:
    conn.execute("DELETE FROM ownership WHERE steamid = ?", (steamid,))
    rows = [
        (
            steamid,
            int(g["appid"]),
            int(g.get("playtime_forever") or 0),
            int(g.get("playtime_2weeks") or 0),
            int(g["rtime_last_played"]) if g.get("rtime_last_played") else None,
        )
        for g in games
        if g.get("appid")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO ownership (steamid, appid, playtime_forever, playtime_2weeks, last_played)"
        " VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def upsert_apps_basic(conn: sqlite3.Connection, games: list[dict]) -> None:
    """Nome/icone vindos do GetOwnedGames (include_appinfo=1) — barato e sem rate limit da loja."""
    rows = []
    for g in games:
        appid = g.get("appid")
        name = (g.get("name") or "").strip()
        if not appid or not name:
            continue
        rows.append((int(appid), name, g.get("img_icon_url") or ""))
    conn.executemany(
        "INSERT INTO app (appid, name, icon) VALUES (?, ?, ?)"
        " ON CONFLICT(appid) DO UPDATE SET name=COALESCE(NULLIF(excluded.name,''), app.name),"
        " icon=COALESCE(NULLIF(excluded.icon,''), app.icon)",
        rows,
    )


def save_app_details(conn: sqlite3.Connection, appid: int, data: dict | None, state: str) -> None:
    if state != "ok" or not data:
        conn.execute(
            "INSERT INTO app (appid, details_state, details_synced) VALUES (?, ?, ?)"
            " ON CONFLICT(appid) DO UPDATE SET details_state=excluded.details_state,"
            " details_synced=excluded.details_synced",
            (appid, state, now()),
        )
        return

    price = data.get("price_overview") or {}
    categories = [c.get("description", "") for c in data.get("categories") or []]
    genres = [g.get("description", "") for g in data.get("genres") or []]
    flags = classify_categories(categories)
    metacritic = (data.get("metacritic") or {}).get("score")
    conn.execute(
        """
        INSERT INTO app (appid, name, type, categories, genres, is_multiplayer, is_coop, is_online_coop,
                         is_local_coop, is_pvp, is_remote_together, is_free, release_date, metacritic,
                         details_state, details_synced,
                         price_final, price_initial, discount_percent, currency, price_synced)
        VALUES (:appid, :name, :type, :categories, :genres, :is_multiplayer, :is_coop, :is_online_coop,
                :is_local_coop, :is_pvp, :is_remote_together, :is_free, :release_date, :metacritic,
                'ok', :synced,
                :price_final, :price_initial, :discount_percent, :currency, :synced)
        ON CONFLICT(appid) DO UPDATE SET
            name=COALESCE(NULLIF(excluded.name,''), app.name),
            type=excluded.type, categories=excluded.categories, genres=excluded.genres,
            is_multiplayer=excluded.is_multiplayer, is_coop=excluded.is_coop,
            is_online_coop=excluded.is_online_coop, is_local_coop=excluded.is_local_coop,
            is_pvp=excluded.is_pvp, is_remote_together=excluded.is_remote_together,
            is_free=excluded.is_free, release_date=excluded.release_date,
            metacritic=excluded.metacritic, details_state='ok', details_synced=excluded.details_synced,
            price_final=excluded.price_final, price_initial=excluded.price_initial,
            discount_percent=excluded.discount_percent, currency=excluded.currency,
            price_synced=excluded.price_synced
        """,
        {
            "appid": appid,
            "name": (data.get("name") or "").strip(),
            "type": data.get("type"),
            "categories": json.dumps(categories, ensure_ascii=False),
            "genres": json.dumps(genres, ensure_ascii=False),
            "is_free": 1 if data.get("is_free") else 0,
            "release_date": (data.get("release_date") or {}).get("date"),
            "metacritic": metacritic,
            "price_final": price.get("final") if price else (0 if data.get("is_free") else None),
            "price_initial": price.get("initial") if price else (0 if data.get("is_free") else None),
            "discount_percent": price.get("discount_percent") if price else (0 if data.get("is_free") else None),
            "currency": price.get("currency") if price else None,
            "synced": now(),
            **flags,
        },
    )


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def start_run(conn: sqlite3.Connection) -> int:
    cur = conn.execute(
        "INSERT INTO sync_run (started_at, status) VALUES (?, 'running')", (now(),)
    )
    conn.commit()
    return int(cur.lastrowid)


def finish_run(conn: sqlite3.Connection, run_id: int, status: str, message: str, stats: dict) -> None:
    conn.execute(
        "UPDATE sync_run SET finished_at=?, status=?, message=?, stats=? WHERE id=?",
        (now(), status, message, json.dumps(stats, ensure_ascii=False), run_id),
    )
    conn.commit()


# ------------------------------------------------------- avaliacoes e etiquetas


def wilson_lower_bound(positive: int, total: int, z: float = 1.96) -> float:
    """Limite inferior do intervalo de Wilson (95%).

    Ordenar por "% de positivas" premia o jogo com 3 análises e 100%. O limite de
    Wilson desconta a incerteza de quem tem poucas análises, que é o que "melhor
    avaliado" deveria significar.
    """
    if total <= 0:
        return 0.0
    phat = positive / total
    denom = 1 + z * z / total
    centre = phat + z * z / (2 * total)
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total)
    return max(0.0, (centre - margin) / denom)


def save_app_reviews(conn: sqlite3.Connection, appid: int, summary: dict | None, state: str) -> None:
    if state != "ok" or not summary:
        conn.execute(
            "INSERT INTO app (appid, reviews_synced) VALUES (?, ?)"
            " ON CONFLICT(appid) DO UPDATE SET reviews_synced=excluded.reviews_synced",
            (appid, now()),
        )
        return
    positive = int(summary.get("total_positive") or 0)
    total = int(summary.get("total_reviews") or 0)
    percent = round(positive / total * 100) if total else None
    conn.execute(
        """
        INSERT INTO app (appid, review_score, review_desc, review_positive, review_total,
                         review_percent, review_wilson, reviews_synced)
        VALUES (:appid, :score, :desc, :positive, :total, :percent, :wilson, :synced)
        ON CONFLICT(appid) DO UPDATE SET
            review_score=excluded.review_score, review_desc=excluded.review_desc,
            review_positive=excluded.review_positive, review_total=excluded.review_total,
            review_percent=excluded.review_percent, review_wilson=excluded.review_wilson,
            reviews_synced=excluded.reviews_synced
        """,
        {
            "appid": appid,
            "score": summary.get("review_score"),
            "desc": summary.get("review_score_desc"),
            "positive": positive,
            "total": total,
            "percent": percent,
            "wilson": wilson_lower_bound(positive, total),
            "synced": now(),
        },
    )


def add_app_tags(conn: sqlite3.Connection, appid: int, tags: Iterable[str]) -> None:
    rows = [(appid, t.strip()) for t in tags if (t or "").strip()]
    if rows:
        conn.executemany("INSERT OR IGNORE INTO app_tag (appid, tag) VALUES (?, ?)", rows)


def mark_discovered(conn: sqlite3.Connection, appids: Iterable[int]) -> None:
    stamp = now()
    conn.executemany(
        "INSERT INTO app (appid, discovered_at) VALUES (?, ?)"
        " ON CONFLICT(appid) DO UPDATE SET discovered_at=COALESCE(app.discovered_at, excluded.discovered_at)",
        [(int(a), stamp) for a in appids],
    )


def save_tags(conn: sqlite3.Connection, tags: list[dict]) -> int:
    rows = [
        (int(t["tagid"]), str(t.get("name") or "").strip(), now())
        for t in tags
        if t.get("tagid") and (t.get("name") or "").strip()
    ]
    conn.executemany(
        "INSERT INTO tag (tagid, name, synced) VALUES (?, ?, ?)"
        " ON CONFLICT(tagid) DO UPDATE SET name=excluded.name, synced=excluded.synced",
        rows,
    )
    return len(rows)


def find_tags(conn: sqlite3.Connection, term: str, limit: int = 20) -> list[dict]:
    term = (term or "").strip()
    if not term:
        rows = conn.execute("SELECT tagid, name FROM tag ORDER BY name COLLATE NOCASE LIMIT ?", (limit,))
    else:
        rows = conn.execute(
            "SELECT tagid, name FROM tag WHERE name LIKE ? COLLATE NOCASE"
            " ORDER BY (name LIKE ? COLLATE NOCASE) DESC, LENGTH(name), name COLLATE NOCASE LIMIT ?",
            (f"%{term}%", f"{term}%", limit),
        )
    return [dict(r) for r in rows]
