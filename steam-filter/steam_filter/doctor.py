"""Diagnostico: bate uma vez em cada endpoint externo e diz o que funcionou.

Existe porque a busca no catalogo depende de endpoints publicos da loja que a Valve nao
documenta formalmente. Se algum dia um deles mudar de formato, este comando aponta qual —
em vez de a interface so mostrar "nenhum resultado".
"""

from __future__ import annotations

import asyncio

from . import db
from .config import Config, load_config
from .steam_api import SteamClient, SteamError

VERDE, VERMELHO, AMARELO, FIM = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def _linha(ok: bool | None, titulo: str, detalhe: str = "") -> None:
    if ok is None:
        marca, cor = "--", AMARELO
    else:
        marca, cor = ("OK", VERDE) if ok else ("XX", VERMELHO)
    print(f"  {cor}[{marca}]{FIM} {titulo}" + (f" — {detalhe}" if detalhe else ""))


async def _checar(nome: str, coro, formatar=None) -> bool:
    try:
        resultado = await coro
    except SteamError as exc:
        _linha(False, nome, str(exc))
        return False
    except Exception as exc:  # noqa: BLE001
        _linha(False, nome, f"{type(exc).__name__}: {exc}")
        return False
    _linha(True, nome, formatar(resultado) if formatar else "")
    return True


async def executar(cfg: Config) -> int:
    falhas = 0
    print("\n  Diagnostico do Steam Game Filter\n")

    if not cfg.api_key:
        _linha(None, "Chave da Web API", "nao configurada — os testes 1 a 3 serao pulados")
    if not cfg.steam_id:
        _linha(None, "SteamID", "nao configurado")

    async with SteamClient(
        cfg.api_key or "sem-chave",
        api_rate_per_sec=cfg.api_rate_per_sec,
        store_rate_per_sec=cfg.store_rate_per_sec,
        store_country=cfg.store_country,
        store_language=cfg.store_language,
    ) as client:
        steamid = ""
        if cfg.api_key and cfg.steam_id:
            try:
                steamid = await client.resolve_steam_id(cfg.steam_id)
                _linha(True, "1. Identificar o seu SteamID", steamid)
            except Exception as exc:  # noqa: BLE001
                _linha(False, "1. Identificar o seu SteamID", str(exc))
                falhas += 1

        if steamid:
            propria = await client.get_owned_games(steamid)
            ok = propria.state == "public"
            _linha(ok, "2. Ler a sua biblioteca",
                   f"{len(propria.games)} jogos" if ok else f"{propria.state}: {propria.detail}")
            falhas += 0 if ok else 1

            try:
                amigos = await client.get_friend_list(steamid)
                _linha(True, "3. Ler a sua lista de amigos", f"{len(amigos)} amigos")
            except Exception as exc:  # noqa: BLE001
                _linha(False, "3. Ler a sua lista de amigos", str(exc))
                falhas += 1

        # --- endpoints publicos da loja (nao usam a chave) --------------------
        estado, dados = await client.get_app_details(620)          # Portal 2
        ok = estado == "ok" and bool(dados)
        preco = (dados or {}).get("price_overview") or {}
        _linha(ok, "4. Detalhes e preço na loja",
               f"{(dados or {}).get('name')} · {preco.get('final_formatted') or 'sem preço'}"
               if ok else f"estado={estado}")
        falhas += 0 if ok else 1

        estado, resumo = await client.get_app_reviews(620)
        ok = estado == "ok" and bool(resumo)
        _linha(ok, "5. Avaliações dos usuários",
               f"{resumo.get('total_reviews')} análises, {resumo.get('review_score_desc')}"
               if ok else f"estado={estado}")
        falhas += 0 if ok else 1

        falhas += 0 if await _checar(
            "6. Catálogo de etiquetas",
            client.get_popular_tags(),
            lambda tags: f"{len(tags)} etiquetas (ex.: {tags[0].get('name')})",
        ) else 1

        try:
            appids, total = await client.search_store(tag_ids=[3959], sort="avaliacoes", count=10)
            ok = bool(appids)
            _linha(ok, "7. Busca no catálogo (etiqueta Roguelite)",
                   f"{len(appids)} de {total} jogos; primeiro appid {appids[0]}" if ok
                   else "a busca respondeu, mas nenhum jogo foi reconhecido no HTML")
            falhas += 0 if ok else 1
        except Exception as exc:  # noqa: BLE001
            _linha(False, "7. Busca no catálogo (etiqueta Roguelite)", str(exc))
            falhas += 1

    with db.closing_conn() as conn:
        total_apps = conn.execute("SELECT COUNT(*) AS n FROM app").fetchone()["n"]
        com_preco = conn.execute("SELECT COUNT(*) AS n FROM app WHERE price_synced IS NOT NULL").fetchone()["n"]
        com_review = conn.execute("SELECT COUNT(*) AS n FROM app WHERE reviews_synced IS NOT NULL").fetchone()["n"]
    print(f"\n  Cache local: {total_apps} jogos, {com_preco} com preço, {com_review} com avaliação.")

    if falhas:
        print(f"\n  {VERMELHO}{falhas} verificação(ões) falharam.{FIM} Copie esta saída inteira ao pedir ajuda.\n")
    else:
        print(f"\n  {VERDE}Tudo funcionando.{FIM}\n")
    return 1 if falhas else 0


def main() -> int:
    db.init_db()
    return asyncio.run(executar(load_config()))
