#!/usr/bin/env python3
"""Confere se a branch da sessão está atualizada em relação ao `main`.

Por que existe
--------------
As instruções do projeto (`CLAUDE.md`), as fichas de `teses/` e as próprias skills
(`.claude/skills/`) são lidas **do repositório**, na branch da sessão. Numa branch
atrasada elas não existem, ou existem numa versão superada — e a sessão então minuta
com formatação, nome de arquivo e teses errados sem ter como perceber. O aviso que
manda sincronizar mora justamente no arquivo que a branch atrasada não tem.

Este script quebra esse círculo: não depende de nenhum texto do repositório, só do
git. Roda no hook de início de sessão e como guarda do gerador de minutas.

Uso
---
    python scripts/verificar_branch.py            # relatório legível
    python scripts/verificar_branch.py --check    # idem, e sai com 1 se atrasada
    python scripts/verificar_branch.py --quieto   # só fala se houver problema

Saída: 0 = em dia (ou impossível conferir); 1 = atrasada, só com --check.
Só stdlib — roda local e no cloud, em qualquer Python 3.8+.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE = "main"
REMOTO = "origin"


def _git(*args: str, timeout: int = 45) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(_raiz()),
        )
        return p.returncode, (p.stdout or p.stderr).strip()
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def _raiz() -> Path:
    try:
        p = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=15,
        )
        if p.returncode == 0 and p.stdout.strip():
            return Path(p.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.cwd()


def marcadores_de_atraso(raiz: Path) -> list[str]:
    """Sinais, no próprio disco, de que a branch é anterior a reestruturações."""
    achados = []
    if list(raiz.glob("base_conhecimento_juridico_*.md")):
        achados.append(
            "existe base_conhecimento_juridico_*.md — a base já foi fatiada em teses/"
        )
    if not (raiz / "teses").is_dir():
        achados.append("não existe teses/ — a branch é anterior ao fatiamento da base")
    if not (raiz / ".claude" / "skills" / "formatar-minuta").is_dir():
        achados.append(
            "não existe .claude/skills/formatar-minuta — a peça sairia fora do padrão visual"
        )
    if not (raiz / "CLAUDE.md").is_file():
        achados.append("não existe CLAUDE.md — as instruções do projeto não estão nesta branch")
    if not (raiz / "INDICE.md").is_file():
        achados.append("não existe INDICE.md — não há roteamento de teses nesta branch")
    return achados


def relatorio(quieto: bool = False) -> bool:
    """Imprime o diagnóstico. Devolve True se a branch estiver em dia."""
    raiz = _raiz()
    if not (raiz / ".git").exists():
        return True  # fora de repositório git: nada a conferir

    codigo, _ = _git("fetch", REMOTO, BASE)
    fetch_ok = codigo == 0

    atras: list[str] = []
    if fetch_ok:
        c, saida = _git("log", "--oneline", f"HEAD..{REMOTO}/{BASE}")
        if c == 0 and saida:
            atras = saida.splitlines()

    marcadores = marcadores_de_atraso(raiz)
    _, branch = _git("rev-parse", "--abbrev-ref", "HEAD")

    if not atras and not marcadores:
        if not quieto:
            estado = "em dia com origin/main" if fetch_ok else "sem rede para conferir o remoto"
            print(f"[branch] {branch or 'HEAD'} — {estado}.")
        return True

    print("=" * 78)
    print("  ATENÇÃO — A BRANCH DESTA SESSÃO ESTÁ DESATUALIZADA")
    print("=" * 78)
    print(f"  branch: {branch or 'HEAD'}")
    if atras:
        print(f"  atrás de {REMOTO}/{BASE} em {len(atras)} commit(s). Os mais recentes:")
        for linha in atras[:5]:
            print(f"      {linha}")
        if len(atras) > 5:
            print(f"      … e outros {len(atras) - 5}")
    if marcadores:
        print("  sinais no disco:")
        for m in marcadores:
            print(f"      - {m}")
    if not fetch_ok:
        print("  (o fetch falhou — o diagnóstico acima veio só dos sinais de disco)")
    print("-" * 78)
    print("  NÃO minute, não gere .docx e não leia a base nesta branch antes de sincronizar.")
    print("  Nesta branch, CLAUDE.md, as fichas de teses/ e as skills podem não existir —")
    print("  e a peça sai com formatação, nome de arquivo e teses errados.")
    print()
    print(f"    git fetch {REMOTO} {BASE} && git rebase {REMOTO}/{BASE}")
    print(f"    # branch que só tem histórico já mergeado:")
    print(f"    git checkout -B <mesma-branch> {REMOTO}/{BASE}")
    print("=" * 78)
    return False


def _saida_hook() -> int:
    """Modo hook: emite JSON para o Claude Code injetar o aviso no contexto da sessão."""
    import io
    import json
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        em_dia = relatorio(quieto=True)
    diagnostico = buf.getvalue().strip()

    if em_dia:
        print(json.dumps({"suppressOutput": True}))
        return 0

    aviso = (
        "A branch desta sessão está DESATUALIZADA em relação a origin/main. "
        "Antes de ler a base de teses ou minutar qualquer peça, sincronize "
        "(git fetch origin main && git rebase origin/main): nesta branch o CLAUDE.md, "
        "as fichas de teses/ e as skills formatar-minuta/nomear-minuta podem não existir "
        "ou estar superados, e a peça sai com formatação, nome de arquivo e teses errados.\n\n"
        + diagnostico
    )
    print(json.dumps({
        "systemMessage": "Branch desatualizada em relação ao main — sincronize antes de minutar.",
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": aviso},
    }, ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Confere se a branch está atualizada com o main.")
    ap.add_argument("--check", action="store_true",
                    help="sai com código 1 se a branch estiver atrasada")
    ap.add_argument("--quieto", action="store_true",
                    help="não imprime nada quando a branch está em dia")
    ap.add_argument("--hook", action="store_true",
                    help="emite JSON de hook do Claude Code (injeta o aviso no contexto)")
    args = ap.parse_args()

    if os.environ.get("ASJUR_SEM_VERIFICAR_BRANCH"):
        if args.hook:
            import json
            print(json.dumps({"suppressOutput": True}))
        return 0

    if args.hook:
        return _saida_hook()

    em_dia = relatorio(quieto=args.quieto)
    return 0 if (em_dia or not args.check) else 1


if __name__ == "__main__":
    sys.exit(main())
