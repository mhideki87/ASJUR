#!/usr/bin/env python3
"""Roteia o objeto da demanda até as fichas de tese — sem carregar o INDICE.md no contexto.

Uso:
    python scripts/rotear.py "pede insalubridade em grau máximo e horas extras de motorista"
    python scripts/rotear.py --arquivo "D:/Claude/00 caso_atual/FULANO/inicial.md"
    python scripts/rotear.py --por-pedido --arquivo pedidos.txt
    cat pedidos.txt | python scripts/rotear.py

Por que existe: o roteamento por índice já economiza muito (abrir 3 fichas em vez de 26), mas o
INDICE.md em si é lido por inteiro em toda sessão — hoje ~16 KB, e crescendo a cada ficha nova. Este
script faz a busca **fora** do contexto: recebe os pedidos, casa com os `gatilhos` e devolve só os
caminhos das fichas que interessam. Nenhuma linha da tabela entra na conversa, e o custo do roteamento
para de crescer junto com a base.

Lê o bloco de metadados das próprias fichas (`teses/**/*.md`), não a tabela do INDICE.md: continua
acertando mesmo que o índice esteja desatualizado.

Não escreve nada, não altera arquivo e não repete o texto de entrada na saída — só os `gatilhos` que
casaram, que são conteúdo do repositório. É seguro apontar para um `.md` com dado real da parte.

Sem dependência externa — só a biblioteca padrão do Python.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from atualizar_indice import ROTULO_STATUS, coletar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

# --- Fichas que não dependem de gatilho ------------------------------------------------------------
# Espelham a seção "Sempre aplicável" do INDICE.md. Se aquela seção mudar, mude aqui junto.
SEMPRE = {
    "teses/transversal/prerrogativas_processuais_ect.md":
        "prazo em dobro, preparo, equiparação à Fazenda — conferir tempestividade antes de tudo",
}
CONDICIONAIS = {
    "teses/trabalhista/prescricao.md":
        "só na trabalhista com parcela de norma interna revogada, ou cuja condição de pagamento "
        "deixou de ser preenchida por ato único do empregador",
}

# --- Casamento -------------------------------------------------------------------------------------
# Conectivos tolerados entre as palavras de um gatilho: o gatilho `art. 11 § 2º CLT` tem de casar com
# "art. 11, § 2º, da CLT" no texto da inicial. Até dois, para não afrouxar demais.
CONECTIVOS = ("da", "de", "do", "das", "dos", "na", "no", "nas", "nos", "em", "e", "a", "o")
_SEP = r"[^a-z0-9]+(?:(?:%s)[^a-z0-9]+){0,2}" % "|".join(CONECTIVOS)

PESO = 1.0
PESO_FRACO = 0.5   # gatilho que é só número (`40`, `200 litros` vira `200`): não discrimina sozinho


def normalizar(texto: str) -> str:
    """Minúsculas e sem acento — `Súmula 372, I` e `sumula 372 i` têm de casar."""
    decomposto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def _plural(token: str) -> str:
    """Aceita o plural da palavra sem exigir que a ficha liste as duas formas.

    `teses/README.md` manda cortar gatilho que é só flexão do vizinho (`afastamento` +
    `afastamentos`); então quem tem de saber virar o plural é o roteamento, não a ficha.
    """
    esc = re.escape(token)
    if token.isdigit() or len(token) <= 2:
        return esc                                        # número e sigla curta não flexionam
    if token.endswith(("al", "el", "ol", "ul")):
        return f"(?:{esc}|{re.escape(token[:-1])}is)"     # postal → postais
    if token.endswith("ao"):
        return f"(?:{esc}|{re.escape(token[:-2])}(?:oes|aes|aos))"   # indenizacao → indenizacoes
    if token.endswith("s"):
        return esc                                        # já está no plural
    if token.endswith(("r", "z")):
        return f"{esc}(?:es)?"                            # motor → motores
    return f"{esc}s?"


def compilar(frase: str) -> tuple[re.Pattern, float] | None:
    """Transforma um gatilho em expressão de busca com fronteira de palavra.

    A fronteira é o que impede `CAT` de casar dentro de "categoria" e `AAT` dentro de "atacado".
    """
    tokens = [t for t in re.split(r"[^a-z0-9]+", normalizar(frase)) if t]
    if not tokens:
        return None
    corpo = _SEP.join(_plural(t) for t in tokens)
    peso = PESO_FRACO if len(tokens) == 1 and tokens[0].isdigit() else PESO
    return re.compile(rf"(?<![a-z0-9]){corpo}(?![a-z0-9])"), peso


_CACHE: dict[str, list[tuple[str, re.Pattern, float]]] = {}


def padroes_da_ficha(ficha: dict) -> list[tuple[str, re.Pattern, float]]:
    """Gatilhos declarados + o `tema` da ficha, que o roteamento lê junto.

    Do `tema` só entra o trecho antes do primeiro travessão, parêntese ou dois-pontos: é o nome do
    assunto ("Adicional de insalubridade"), não o subtítulo que o detalha.
    """
    if ficha["_caminho"] in _CACHE:      # --por-pedido roteia N vezes: compilar uma só
        return _CACHE[ficha["_caminho"]]

    frases = list(ficha.get("gatilhos", []))
    tema = re.split(r"[—\-–(:/]", ficha.get("tema", ""), maxsplit=1)[0].strip()
    if tema:
        frases.append(tema)

    padroes, vistos = [], set()
    for frase in frases:
        chave = normalizar(frase)
        if chave in vistos:       # o `tema` costuma repetir um gatilho: não pontuar duas vezes
            continue
        vistos.add(chave)
        compilado = compilar(frase)
        if compilado:
            padroes.append((frase, compilado[0], compilado[1]))
    _CACHE[ficha["_caminho"]] = padroes
    return padroes


def rotear(texto: str, fichas: list[dict], minimo: float) -> list[dict]:
    alvo = normalizar(texto)
    resultados = []
    for ficha in fichas:
        achados = [(frase, peso) for frase, padrao, peso in padroes_da_ficha(ficha)
                   if padrao.search(alvo)]
        casados = [frase for frase, _ in achados]
        pontos = sum(peso for _, peso in achados)
        if pontos >= minimo:
            resultados.append({**ficha, "_pontos": pontos, "_casados": casados})
    resultados.sort(key=lambda f: (-f["_pontos"], f["_caminho"]))
    return resultados


# --- Entrada ---------------------------------------------------------------------------------------

def ler_entrada(args) -> str:
    partes = list(args.texto)
    for caminho in args.arquivo:
        arquivo = Path(caminho)
        if not arquivo.exists():
            raise SystemExit(f"ERRO: arquivo não encontrado — {caminho}")
        partes.append(arquivo.read_text(encoding="utf-8", errors="replace"))
    if not partes and not sys.stdin.isatty():
        partes.append(sys.stdin.read())
    texto = "\n".join(partes).strip()
    if not texto:
        raise SystemExit(
            "ERRO: nada para rotear. Passe o texto como argumento, use --arquivo ou mande pelo pipe."
        )
    return texto


# --- Saída -----------------------------------------------------------------------------------------

def formatar(resultados: list[dict], total: int, limite: int, max_gatilhos: int) -> list[str]:
    if not resultados:
        return [
            "Nenhum gatilho bateu.",
            "",
            "Protocolo: dizer isso explicitamente e tratar como TEMA NOVO — analisar a partir dos autos,",
            "sem forçar encaixe em ficha existente, e ao final propor ficha nova a partir de",
            "teses/_TEMPLATE_TESE.md. (Se o texto passado foi curto, tente de novo com a lista completa",
            "de pedidos antes de concluir que é tema novo.)",
        ]

    mostrados = resultados[:limite]
    linhas = [f"{len(resultados)} ficha(s) casaram de {total}"
              + (f" — mostrando as {limite} mais fortes" if len(resultados) > limite else "") + ":", ""]
    for f in mostrados:
        marca = "" if f["status"] == "validada" else f"  [{f['status']}]"
        linhas.append(f"  {f['_pontos']:>4.1f}  {f['_caminho']}{marca}")
        amostra = f["_casados"][:max_gatilhos]
        resto = len(f["_casados"]) - len(amostra)
        sufixo = f" (+{resto})" if resto > 0 else ""
        linhas.append(f"        {' · '.join(amostra)}{sufixo}")
        if f["_pontos"] <= 1.0:
            linhas.append("        casamento fraco — confira se o tema é mesmo esse antes de abrir")
    return linhas


def formatar_fixas(caminhos_casados: set[str], no_escopo: set[str]) -> list[str]:
    """`no_escopo` evita lembrar da prescrição (trabalhista) numa rodada com --area civel."""
    linhas = ["", "Sempre aplicável (abrir junto, independentemente de gatilho):"]
    for caminho, nota in SEMPRE.items():
        if caminho not in no_escopo:
            continue
        linhas.append(f"  {caminho}")
        linhas.append(f"        {nota}")
    pendentes = {c: n for c, n in CONDICIONAIS.items()
                 if c not in caminhos_casados and c in no_escopo}
    if pendentes:
        linhas.append("")
        linhas.append("Conferir se cabe:")
        for caminho, nota in pendentes.items():
            linhas.append(f"  {caminho}")
            linhas.append(f"        {nota}")
    return linhas


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diz quais fichas de tese abrir para um processo, sem carregar o INDICE.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Alimente o script com a LISTA DE PEDIDOS, não com a inicial inteira: a inicial menciona\n"
               "de passagem meia dúzia de temas que não são pedido nenhum, e cada um vira ficha aberta à toa.",
    )
    parser.add_argument("texto", nargs="*", help="o objeto da demanda / a lista de pedidos")
    parser.add_argument("-a", "--arquivo", action="append", default=[],
                        help="ler de um arquivo (pode repetir); aceita caminho fora do repositório")
    parser.add_argument("--por-pedido", action="store_true",
                        help="tratar cada linha da entrada como um pedido e rotear uma a uma")
    parser.add_argument("--area", choices=("trabalhista", "civel"),
                        help="restringir à área (transversal entra sempre)")
    parser.add_argument("--min", type=float, default=1.0, dest="minimo",
                        help="pontuação mínima para a ficha entrar (padrão 1.0)")
    parser.add_argument("--limite", type=int, default=8, help="máximo de fichas na saída (padrão 8)")
    parser.add_argument("--gatilhos", type=int, default=5, dest="max_gatilhos",
                        help="quantos gatilhos casados mostrar por ficha (padrão 5)")
    parser.add_argument("--paths", action="store_true",
                        help="imprimir só os caminhos, um por linha — para encadear com outro comando")
    args = parser.parse_args()

    texto = ler_entrada(args)

    fichas, erros = coletar()
    if erros:
        print("AVISO: há fichas com metadado inválido — o roteamento pode perder tema.", file=sys.stderr)
        for erro in erros:
            print(f"  - {erro}", file=sys.stderr)
    if not fichas:
        raise SystemExit("ERRO: nenhuma ficha encontrada em teses/.")

    if args.area:
        fichas = [f for f in fichas if f.get("area") in (args.area, "transversal")]
    total = len(fichas)
    no_escopo = {f["_caminho"] for f in fichas}

    resultados = rotear(texto, fichas, args.minimo)
    casados = {f["_caminho"] for f in resultados}

    if args.paths:
        fixas = [c for c in SEMPRE if c in no_escopo]
        for caminho in [f["_caminho"] for f in resultados[:args.limite]] + fixas:
            print(caminho)
        return 0

    saida: list[str] = []
    if args.por_pedido:
        pedidos = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        saida.append(f"Roteamento por pedido ({len(pedidos)} linha(s)):")
        for pedido in pedidos:
            rotulo = pedido if len(pedido) <= 70 else pedido[:67] + "..."
            achados = rotear(pedido, fichas, args.minimo)
            saida.append("")
            saida.append(f"  · {rotulo}")
            if not achados:
                saida.append("      nenhum gatilho — candidato a tema novo")
            for f in achados[:3]:
                saida.append(f"      → {f['_caminho']}  ({f['_pontos']:.1f})")
        saida.append("")
        saida.append("-" * 70)
        saida.append("")

    saida += formatar(resultados, total, args.limite, args.max_gatilhos)
    saida += formatar_fixas(casados, no_escopo)
    saida += ["", "Abra SÓ os caminhos acima. Depois deles, o modelo estrutural indicado na ficha."]
    print("\n".join(saida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
