#!/usr/bin/env python3
"""Valida as fichas de tese e regenera a tabela de roteamento do INDICE.md.

Uso:
    python scripts/atualizar_indice.py            # valida e reescreve a tabela do INDICE.md
    python scripts/atualizar_indice.py --check    # só valida; falha se o INDICE.md estiver desatualizado

Por que existe: o índice só serve se estiver sempre em sincronia com as fichas. Em vez de manter a
tabela à mão (e ela envelhecer em silêncio), a tabela é derivada do bloco de metadados no topo de cada
`teses/**/*.md`. Sem dependência externa — só a biblioteca padrão do Python.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_TESES = RAIZ / "teses"
INDICE = RAIZ / "INDICE.md"

MARCA_INICIO = "<!-- TABELA-GERADA:INICIO -->"
MARCA_FIM = "<!-- TABELA-GERADA:FIM -->"

# `pecas`, `modelos` e `ver_tambem` podem vir vazios (ex.: ficha panorâmica, tema ainda sem modelo).
CAMPOS_OBRIGATORIOS = ("area", "tema", "slug", "status", "gatilhos", "atualizado")
CAMPOS_LISTA = ("gatilhos", "pecas", "modelos", "ver_tambem")
AREAS = ("trabalhista", "civel", "transversal")
STATUS_VALIDOS = ("validada", "rascunho", "revisar")

ROTULO_AREA = {
    "trabalhista": "Trabalhista",
    "civel": "Cível",
    "transversal": "Transversal",
}
ROTULO_STATUS = {
    "validada": "validada",
    "rascunho": "**rascunho**",
    "revisar": "**revisar**",
}


def ler_frontmatter(caminho: Path) -> tuple[dict, list[str]]:
    """Lê o bloco entre as duas linhas `---` no topo do arquivo.

    Formato aceito de propósito restrito: uma chave por linha, `chave: valor`, e listas na forma
    `chave: [a, b, c]`. Nada de YAML aninhado — o objetivo é ser óbvio de escrever à mão.
    """
    erros: list[str] = []
    linhas = caminho.read_text(encoding="utf-8").splitlines()

    if not linhas or linhas[0].strip() != "---":
        return {}, [f"{caminho}: falta o bloco de metadados `---` na primeira linha"]

    try:
        fim = linhas.index("---", 1)
    except ValueError:
        return {}, [f"{caminho}: bloco de metadados aberto e não fechado com `---`"]

    dados: dict = {}
    for numero, linha in enumerate(linhas[1:fim], start=2):
        if not linha.strip():
            continue
        if ":" not in linha:
            erros.append(f"{caminho}:{numero}: linha de metadado sem `:` — {linha!r}")
            continue
        chave, _, valor = linha.partition(":")
        chave, valor = chave.strip(), valor.strip()
        if chave in CAMPOS_LISTA:
            if not (valor.startswith("[") and valor.endswith("]")):
                erros.append(f"{caminho}:{numero}: `{chave}` deve ser uma lista `[a, b]`")
                continue
            itens = [i.strip() for i in valor[1:-1].split(",")]
            dados[chave] = [i for i in itens if i]
        else:
            dados[chave] = valor
    return dados, erros


def validar(caminho: Path, dados: dict) -> list[str]:
    erros = []
    relativo = caminho.relative_to(RAIZ).as_posix()

    for campo in CAMPOS_OBRIGATORIOS:
        if not dados.get(campo):
            erros.append(f"{relativo}: campo obrigatório ausente ou vazio — `{campo}`")

    area = dados.get("area")
    pasta = caminho.parent.name
    if area and area not in AREAS:
        erros.append(f"{relativo}: `area` inválida ({area!r}) — use uma de {AREAS}")
    elif area and area != pasta:
        erros.append(f"{relativo}: `area` ({area!r}) não corresponde à pasta ({pasta!r})")

    slug = dados.get("slug")
    if slug and slug != caminho.stem:
        erros.append(f"{relativo}: `slug` ({slug!r}) diferente do nome do arquivo ({caminho.stem!r})")

    status = dados.get("status")
    if status and status not in STATUS_VALIDOS:
        erros.append(f"{relativo}: `status` inválido ({status!r}) — use um de {STATUS_VALIDOS}")

    data = dados.get("atualizado", "")
    partes = data.split("-")
    if data and not (len(partes) == 3 and all(p.isdigit() for p in partes) and len(partes[0]) == 4):
        erros.append(f"{relativo}: `atualizado` deve estar no formato AAAA-MM-DD (veio {data!r})")

    for referencia in dados.get("modelos", []) + dados.get("ver_tambem", []):
        if not (RAIZ / referencia).exists():
            erros.append(f"{relativo}: referência inexistente em metadado — {referencia}")

    return erros


def coletar() -> tuple[list[dict], list[str]]:
    fichas, erros = [], []
    for caminho in sorted(DIR_TESES.rglob("*.md")):
        nome = caminho.name
        if nome.startswith("_") or nome == "README.md":
            continue
        dados, erros_leitura = ler_frontmatter(caminho)
        erros.extend(erros_leitura)
        if not dados:
            continue
        erros.extend(validar(caminho, dados))
        dados["_caminho"] = caminho.relative_to(RAIZ).as_posix()
        fichas.append(dados)

    ordem = {area: i for i, area in enumerate(AREAS)}
    fichas.sort(key=lambda f: (ordem.get(f.get("area", ""), 99), f.get("tema", "")))
    return fichas, erros


def montar_tabela(fichas: list[dict]) -> str:
    linhas = [
        MARCA_INICIO,
        "",
        "<!-- Gerado por scripts/atualizar_indice.py a partir dos metadados das fichas."
        " Não editar à mão: edite a ficha e rode o script. -->",
        "",
        "| Área | Tema | Gatilhos (o que procurar no objeto da demanda) | Ficha | Modelo de peça | Status |",
        "|---|---|---|---|---|---|",
    ]
    for f in fichas:
        gatilhos = " · ".join(f.get("gatilhos", []))
        modelos = f.get("modelos", [])
        coluna_modelo = (
            "<br>".join(f"[`{Path(m).name}`]({m})" for m in modelos) if modelos else "—"
        )
        linhas.append(
            f"| {ROTULO_AREA.get(f['area'], f['area'])} "
            f"| **{f['tema']}** "
            f"| {gatilhos} "
            f"| [`{Path(f['_caminho']).name}`]({f['_caminho']}) "
            f"| {coluna_modelo} "
            f"| {ROTULO_STATUS.get(f['status'], f['status'])} |"
        )
    linhas += ["", MARCA_FIM]
    return "\n".join(linhas)


def aplicar(tabela: str) -> tuple[str, str]:
    texto = INDICE.read_text(encoding="utf-8")
    inicio = texto.find(MARCA_INICIO)
    fim = texto.find(MARCA_FIM)
    if inicio == -1 or fim == -1:
        raise SystemExit(
            f"ERRO: {INDICE.name} precisa conter as marcas {MARCA_INICIO} e {MARCA_FIM}."
        )
    novo = texto[:inicio] + tabela + texto[fim + len(MARCA_FIM):]
    return texto, novo


def main() -> int:
    checar = "--check" in sys.argv[1:]

    fichas, erros = coletar()
    if erros:
        print("Problemas nas fichas de tese:")
        for erro in erros:
            print(f"  - {erro}")
        return 1

    if not fichas:
        print(f"ERRO: nenhuma ficha encontrada em {DIR_TESES}.")
        return 1

    antigo, novo = aplicar(montar_tabela(fichas))

    if checar:
        if antigo != novo:
            print("INDICE.md está desatualizado — rode: python scripts/atualizar_indice.py")
            return 1
        print(f"OK: {len(fichas)} fichas válidas e INDICE.md em sincronia.")
        return 0

    if antigo == novo:
        print(f"OK: {len(fichas)} fichas válidas; INDICE.md já estava em sincronia.")
        return 0

    INDICE.write_text(novo, encoding="utf-8")
    print(f"INDICE.md atualizado com {len(fichas)} fichas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
