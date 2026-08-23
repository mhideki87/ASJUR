"""Ponto de entrada: `python -m steam_filter` sobe o app local; `... sync` sincroniza pelo terminal."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import threading
import webbrowser

from . import db
from .config import load_config
from .sync import STATE, run_sync


def _cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    db.init_db()
    url = f"http://{args.host}:{args.port}"
    cfg = load_config()
    print(f"\n  Steam Game Filter  ->  {url}")
    if not cfg.is_ready:
        print("  (chave da API / SteamID ainda nao configurados — a propria tela pede isso)")
    print("  Ctrl+C para parar.\n")
    if not args.no_browser:
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    uvicorn.run("steam_filter.server:app", host=args.host, port=args.port, log_level=args.log_level)
    return 0


def _cmd_sync(args: argparse.Namespace) -> int:
    cfg = load_config()
    if not cfg.is_ready:
        print("Erro: defina STEAM_API_KEY e STEAM_ID no .env (veja .env.example).", file=sys.stderr)
        return 2

    async def main() -> None:
        task = asyncio.create_task(run_sync(cfg, mode=args.mode))
        last = ""
        while not task.done():
            snap = STATE.snapshot()
            line = f"[{snap['phase']}] {snap['current']}/{snap['total']} {snap['message']}"[:110]
            if line != last:
                print(line.ljust(110), end="\r", flush=True)
                last = line
            await asyncio.sleep(0.4)
        print()
        stats = await task
        for key, value in stats.items():
            print(f"  {key}: {value}")
        for warning in STATE.warnings:
            print(f"  ! {warning}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCancelado.")
        return 130
    except Exception as exc:  # noqa: BLE001
        print(f"\nErro: {exc}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="steam_filter", description="Filtra jogos da Steam por quantos amigos os têm.")
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="sobe a interface web local (padrao)")
    serve.add_argument("--host", default=os.environ.get("STEAM_FILTER_HOST", "127.0.0.1"))
    serve.add_argument("--port", type=int, default=int(os.environ.get("STEAM_FILTER_PORT", "8777")))
    serve.add_argument("--no-browser", action="store_true", help="nao abrir o navegador sozinho")
    serve.add_argument("--log-level", default="warning")
    serve.set_defaults(func=_cmd_serve)

    syn = sub.add_parser("sync", help="sincroniza pelo terminal, sem abrir a interface")
    syn.add_argument("--mode", choices=["full", "details"], default="full")
    syn.set_defaults(func=_cmd_sync)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0].startswith("-"):
        argv = ["serve", *argv]
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
