"""Cliente assincrono da Steam Web API + da API publica da loja, com controle de taxa e retry."""

from __future__ import annotations

import asyncio
import re
import time
from dataclasses import dataclass
from typing import Any

import httpx

WEB_API = "https://api.steampowered.com"
STORE_API = "https://store.steampowered.com/api"
STEAMID64_RE = re.compile(r"^7656119\d{10}$")


class SteamError(RuntimeError):
    """Erro que o usuario precisa ver (chave invalida, perfil privado, rede fora)."""


class PrivateProfile(SteamError):
    pass


class RateLimiter:
    """Token bucket simples: no maximo `rate` chamadas por segundo, em media."""

    def __init__(self, rate: float, burst: int | None = None) -> None:
        self.rate = max(rate, 0.05)
        self.capacity = max(1.0, float(burst if burst is not None else max(1, int(self.rate))))
        self._tokens = self.capacity
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                self._tokens = min(self.capacity, self._tokens + (now - self._updated) * self.rate)
                self._updated = now
                if self._tokens >= 1:
                    self._tokens -= 1
                    return
                await asyncio.sleep((1 - self._tokens) / self.rate)


@dataclass
class OwnedGames:
    state: str            # 'public' | 'private' | 'error'
    games: list[dict]
    detail: str = ""


class SteamClient:
    def __init__(
        self,
        api_key: str,
        *,
        api_rate_per_sec: float = 8.0,
        store_rate_per_sec: float = 0.6,
        store_country: str = "br",
        store_language: str = "brazilian",
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not api_key:
            raise SteamError("Chave da Steam Web API nao configurada.")
        self.api_key = api_key
        self.store_country = store_country
        self.store_language = store_language
        self._api_limiter = RateLimiter(api_rate_per_sec)
        self._store_limiter = RateLimiter(store_rate_per_sec, burst=2)
        self._client = httpx.AsyncClient(
            transport=transport,
            timeout=timeout,
            headers={"User-Agent": "steam-game-filter/1.0 (+local)"},
            follow_redirects=True,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "SteamClient":
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()

    # ------------------------------------------------------------------ HTTP

    async def _get(self, url: str, params: dict, *, limiter: RateLimiter, attempts: int = 4) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(attempts):
            await limiter.acquire()
            try:
                resp = await self._client.get(url, params=params)
            except httpx.HTTPError as exc:
                last_exc = exc
                await asyncio.sleep(min(2 ** attempt, 15))
                continue

            if resp.status_code == 429 or resp.status_code >= 500:
                retry_after = resp.headers.get("retry-after")
                delay = float(retry_after) if (retry_after or "").isdigit() else min(2 ** attempt * 2, 30)
                last_exc = SteamError(f"HTTP {resp.status_code} em {url}")
                if attempt < attempts - 1:
                    await asyncio.sleep(delay)
                    continue
            return resp
        raise SteamError(f"Falha de rede ao chamar {url}: {last_exc}")

    async def _api(self, path: str, params: dict) -> dict:
        resp = await self._get(f"{WEB_API}/{path}", {**params, "key": self.api_key}, limiter=self._api_limiter)
        if resp.status_code == 401:
            raise PrivateProfile("Acesso negado (401): perfil privado ou chave sem permissao.")
        if resp.status_code == 403:
            raise SteamError("Chave da Steam Web API invalida ou revogada (403).")
        if resp.status_code != 200:
            raise SteamError(f"Steam Web API respondeu HTTP {resp.status_code} em {path}.")
        try:
            return resp.json()
        except ValueError as exc:
            raise SteamError(f"Resposta invalida da Steam em {path}: {exc}") from exc

    # ------------------------------------------------------------- endpoints

    async def resolve_steam_id(self, value: str) -> str:
        """Aceita SteamID64, URL de perfil ou vanity name e devolve sempre o SteamID64."""
        value = (value or "").strip().rstrip("/")
        if not value:
            raise SteamError("SteamID nao informado.")
        if "steamcommunity.com" in value:
            tail = value.split("steamcommunity.com/", 1)[1]
            parts = [p for p in tail.split("/") if p]
            if len(parts) >= 2 and parts[0] in ("profiles", "id"):
                value = parts[1]
        if STEAMID64_RE.match(value):
            return value
        data = await self._api("ISteamUser/ResolveVanityURL/v1/", {"vanityurl": value})
        resp = data.get("response") or {}
        if resp.get("success") == 1 and resp.get("steamid"):
            return str(resp["steamid"])
        raise SteamError(
            f"Nao consegui resolver '{value}' para um SteamID64. Use os 17 digitos do seu perfil."
        )

    async def get_player_summaries(self, steamids: list[str]) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for i in range(0, len(steamids), 100):
            chunk = steamids[i : i + 100]
            data = await self._api("ISteamUser/GetPlayerSummaries/v2/", {"steamids": ",".join(chunk)})
            for player in (data.get("response") or {}).get("players") or []:
                out[str(player.get("steamid"))] = player
        return out

    async def get_friend_list(self, steamid: str) -> list[dict]:
        try:
            data = await self._api(
                "ISteamUser/GetFriendList/v1/", {"steamid": steamid, "relationship": "friend"}
            )
        except PrivateProfile as exc:
            raise PrivateProfile(
                "Sua lista de amigos esta privada. Em Perfil > Editar perfil > Privacidade,"
                " deixe 'Lista de amigos' como Publica e sincronize de novo."
            ) from exc
        return (data.get("friendslist") or {}).get("friends") or []

    async def get_owned_games(self, steamid: str) -> OwnedGames:
        try:
            data = await self._api(
                "IPlayerService/GetOwnedGames/v1/",
                {
                    "steamid": steamid,
                    "include_appinfo": 1,
                    "include_played_free_games": 1,
                    "skip_unvetted_apps": 0,
                },
            )
        except PrivateProfile as exc:
            return OwnedGames("private", [], str(exc))
        except SteamError as exc:
            return OwnedGames("error", [], str(exc))

        response = data.get("response")
        if not isinstance(response, dict) or "games" not in response:
            # Perfil com "Detalhes do jogo" privado devolve 200 com response vazio.
            return OwnedGames("private", [], "Detalhes do jogo nao sao publicos.")
        return OwnedGames("public", response.get("games") or [], "")

    async def get_app_details(self, appid: int) -> tuple[str, dict | None]:
        """('ok', dados) | ('missing', None) para app removido/DLC | ('error', None)."""
        try:
            resp = await self._get(
                f"{STORE_API}/appdetails",
                {
                    "appids": appid,
                    "cc": self.store_country,
                    "l": self.store_language,
                    "filters": "basic,categories,genres,metacritic,release_date",
                },
                limiter=self._store_limiter,
            )
        except SteamError:
            return "error", None
        if resp.status_code == 429:
            return "error", None
        if resp.status_code != 200:
            return "missing" if resp.status_code == 404 else "error", None
        try:
            payload = resp.json()
        except ValueError:
            return "error", None
        entry = (payload or {}).get(str(appid)) or {}
        if not entry.get("success"):
            return "missing", None
        return "ok", entry.get("data") or {}


def persona_state_label(state: Any, game_extra: str | None = None) -> str:
    if game_extra:
        return "jogando"
    return {
        0: "offline",
        1: "online",
        2: "ocupado",
        3: "ausente",
        4: "soneca",
        5: "quer trocar",
        6: "quer jogar",
    }.get(int(state or 0), "offline")
