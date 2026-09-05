"""Configuracao do app: chave da Web API, SteamID e ajustes de sincronizacao.

Ordem de precedencia: variaveis de ambiente > .env na raiz do projeto > data/config.json
(gravado pela propria tela de configuracao) > padroes.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("STEAM_FILTER_DATA") or PROJECT_DIR / "data")
CONFIG_PATH = DATA_DIR / "config.json"
DB_PATH = Path(os.environ.get("STEAM_FILTER_DB") or DATA_DIR / "steam.db")
WEB_DIR = Path(__file__).resolve().parent / "web"


@dataclass
class Config:
    api_key: str = ""
    steam_id: str = ""
    # Sincronizacao
    friend_concurrency: int = 4          # requisicoes simultaneas na Web API
    api_rate_per_sec: float = 8.0        # teto de chamadas/s na Web API (limite oficial: 100k/dia)
    store_rate_per_sec: float = 0.6      # store.steampowered.com aceita ~200 req / 5 min
    store_budget_per_sync: int = 500     # quantos jogos buscar detalhes por sincronizacao
    store_details_max_age_days: int = 60
    store_country: str = "br"
    store_language: str = "brazilian"
    # Quais jogos merecem detalhes da loja (categoria multiplayer/co-op)
    details_min_friends: int = 1         # jogos com >= N amigos donos entram na fila
    details_include_my_games: bool = True
    # Busca no catalogo da loja
    discover_enrich_limit: int = 60      # jogos que ganham preco/avaliacao por busca

    _sources: dict = field(default_factory=dict, repr=False, compare=False)

    @property
    def is_ready(self) -> bool:
        return bool(self.api_key) and bool(self.steam_id)

    def public_dict(self) -> dict:
        """Versao para a UI: a chave da API nunca sai inteira do servidor."""
        data = {f.name: getattr(self, f.name) for f in fields(self) if not f.name.startswith("_")}
        data["api_key"] = mask_key(self.api_key)
        data["api_key_set"] = bool(self.api_key)
        data["api_key_from_env"] = self._sources.get("api_key") in ("env", "dotenv")
        data["steam_id_from_env"] = self._sources.get("steam_id") in ("env", "dotenv")
        data["is_ready"] = self.is_ready
        return data


def mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 8:
        return "*" * len(key)
    return f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"


def _read_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        if value:
            out[key.strip().upper()] = value
    return out


_NUMERIC = {f.name: f.type for f in fields(Config) if f.type in ("int", "float")}


def _coerce(name: str, value):
    kind = _NUMERIC.get(name)
    try:
        if kind == "int":
            return int(value)
        if kind == "float":
            return float(value)
    except (TypeError, ValueError):
        return None
    return value


# Nomes de variavel de ambiente aceitos por campo (o primeiro que existir vence).
_ENV_ALIASES = {
    "api_key": ("STEAM_API_KEY", "STEAM_WEB_API_KEY", "STEAM_FILTER_API_KEY"),
    "steam_id": ("STEAM_ID", "STEAM_ID64", "STEAM_FILTER_STEAM_ID"),
}


def _env_aliases(name: str) -> tuple[str, ...]:
    return _ENV_ALIASES.get(name, (f"STEAM_FILTER_{name.upper()}",))


def load_config() -> Config:
    cfg = Config()
    sources: dict[str, str] = {}

    if CONFIG_PATH.exists():
        try:
            stored = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stored = {}
        for name, value in stored.items():
            if name.startswith("_") or not hasattr(cfg, name) or value in (None, ""):
                continue
            coerced = _coerce(name, value)
            if coerced is not None:
                setattr(cfg, name, coerced)
                sources[name] = "file"

    dotenv = _read_dotenv(PROJECT_DIR / ".env")
    env = {**dotenv, **{k: v for k, v in os.environ.items()}}
    for name in (f.name for f in fields(cfg) if not f.name.startswith("_")):
        for candidate in _env_aliases(name):
            if env.get(candidate):
                coerced = _coerce(name, env[candidate])
                if coerced is not None:
                    setattr(cfg, name, coerced)
                    sources[name] = "env" if candidate in os.environ else "dotenv"
                break

    cfg.steam_id = cfg.steam_id.strip()
    cfg.api_key = cfg.api_key.strip()
    cfg._sources = sources
    return cfg


def save_config(updates: dict) -> Config:
    """Grava em data/config.json apenas o que a UI mandou (campos vazios sao ignorados)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    current: dict = {}
    if CONFIG_PATH.exists():
        try:
            current = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            current = {}

    valid = {f.name for f in fields(Config) if not f.name.startswith("_")}
    for name, value in updates.items():
        if name not in valid:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue  # nao apaga valor existente com string vazia
        coerced = _coerce(name, value)
        if coerced is not None:
            current[name] = coerced

    CONFIG_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass
    return load_config()


__all__ = ["Config", "load_config", "save_config", "DATA_DIR", "DB_PATH", "WEB_DIR", "asdict"]
