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
ROTULO_STATUS = {"rascunho": "**rascunho**", "revisar": "**revisar**"}

# --- Orçamento do pedágio ------------------------------------------------------------------------
# `CONTEXTO.md` + `INDICE.md` são lidos por inteiro em toda sessão, antes de abrir qualquer ficha:
# é o pedágio do roteamento. Ele cresce por linha da tabela, enquanto o conteúdo útil (as fichas
# abertas) não cresce junto — cada tema novo encarece todas as sessões, inclusive as que nada têm a
# ver com ele. O que mede o incômodo não é o tamanho absoluto e sim a **fração da sessão gasta em
# navegação em vez de conteúdo**: em 50% metade do que se carrega é índice.
FICHAS_POR_SESSAO = 3        # roteamento típico: o tema do pedido + as duas de "sempre aplicável"
FRACAO_ALERTA = 0.40         # avisa: dá para enxugar sem pressa
FRACAO_CORTE = 0.50          # enxugar agora
GATILHOS_CONFORTAVEIS = 12   # acima disso a ficha costuma ter sinônimo redundante a cortar


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
    # Sem coluna de modelo: a ficha já lista o dela em `modelos:`, e o modelo só é aberto depois dela.
    # Status só aparece quando não é `validada` — o silêncio é o caso comum e não precisa ocupar linha.
    linhas = [
        MARCA_INICIO,
        "",
        "<!-- Gerado por scripts/atualizar_indice.py. Não editar à mão: edite a ficha e rode o script. -->",
        "",
        "| Área | Tema | Gatilhos | Ficha |",
        "|---|---|---|---|",
    ]
    for f in fichas:
        gatilhos = " · ".join(f.get("gatilhos", []))
        marca = "" if f["status"] == "validada" else f" ({ROTULO_STATUS[f['status']]})"
        linhas.append(
            f"| {ROTULO_AREA.get(f['area'], f['area'])} "
            f"| {f['tema']}{marca} "
            f"| {gatilhos} "
            f"| [{f['_caminho']}]({f['_caminho']}) |"
        )
    linhas += ["", MARCA_FIM]
    return "\n".join(linhas)


def medir_pedagio(fichas: list[dict], indice_novo: str) -> dict:
    """Mede o custo fixo do roteamento contra o de uma sessão típica.

    Usa o INDICE.md que *vai* existir (não o do disco), para o aviso valer já nesta execução.
    """
    tamanhos = sorted((RAIZ / f["_caminho"]).stat().st_size for f in fichas)
    meio = len(tamanhos) // 2
    mediana = tamanhos[meio] if len(tamanhos) % 2 else (tamanhos[meio - 1] + tamanhos[meio]) // 2

    pedagio = (RAIZ / "CONTEXTO.md").stat().st_size + len(indice_novo.encode("utf-8"))
    sessao = pedagio + mediana * FICHAS_POR_SESSAO
    return {"pedagio": pedagio, "mediana": mediana, "sessao": sessao,
            "fracao": pedagio / sessao if sessao else 0.0}


def relatar_pedagio(fichas: list[dict], indice_novo: str) -> list[str]:
    """Uma linha de status sempre; o chamado ao enxugamento só quando passa do orçamento."""
    m = medir_pedagio(fichas, indice_novo)
    pct = 100 * m["fracao"]
    linhas = [f"Pedágio: {m['pedagio'] / 1024:.1f} KB = {pct:.0f}% de uma sessão típica "
              f"({FICHAS_POR_SESSAO} fichas) — alerta em {FRACAO_ALERTA:.0%}."]
    if m["fracao"] < FRACAO_ALERTA:
        return linhas

    urgencia = "PASSOU DO CORTE" if m["fracao"] >= FRACAO_CORTE else "ALERTA"
    linhas += [
        "",
        f"{urgencia}: {pct:.0f}% de cada sessão é índice, não conteúdo — *quando o índice é lido*.",
        "Primeiro caminho, e o barato: rotear por `scripts/rotear.py`, que casa os gatilhos fora do",
        "contexto e devolve só os caminhos. Aí o pedágio some sem custar recall nenhum, e a lista",
        "abaixo vira só um sintoma de ficha com sinônimo redundante — não uma dívida a pagar.",
        "Só se o roteamento continuar sendo feito à mão pela tabela é que vale enxugar os gatilhos",
        'das fichas abaixo (critério em teses/README.md, "Gatilho é chave de busca, não resumo");',
        "cortar gatilho custa recall: tire só o redundante.",
    ]
    gordas = sorted(((len(f.get("gatilhos", [])), f["_caminho"]) for f in fichas), reverse=True)
    gordas = [(n, c) for n, c in gordas if n > GATILHOS_CONFORTAVEIS]
    if gordas:
        linhas.append("")
        linhas += [f"  {n:>3} gatilhos  {c}" for n, c in gordas]
    else:
        linhas += ["", "  Nenhuma ficha acima de "
                   f"{GATILHOS_CONFORTAVEIS} gatilhos: o peso está no número de fichas, não nas",
                   "  listas. Reveja a prosa do INDICE.md e do CONTEXTO.md em vez dos gatilhos."]
    return linhas


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
        print("\n".join(relatar_pedagio(fichas, novo)))
        return 0

    if antigo == novo:
        print(f"OK: {len(fichas)} fichas válidas; INDICE.md já estava em sincronia.")
        print("\n".join(relatar_pedagio(fichas, novo)))
        return 0

    INDICE.write_text(novo, encoding="utf-8")
    print(f"INDICE.md atualizado com {len(fichas)} fichas.")
    print("\n".join(relatar_pedagio(fichas, novo)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
