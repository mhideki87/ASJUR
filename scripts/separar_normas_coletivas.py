#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Separa os .md das normas coletivas em um arquivo por instrumento.

A pasta de origem tem um PDF por *lote* de digitalização, não por norma: alguns arquivos
trazem dois acordos, e os volumes de "Normas Coletivas 2013-2026" trazem quase uma dúzia de
instrumentos cada. Este script recorta cada norma para um arquivo próprio, nomeado pelo
período de vigência, em `<pasta>/Por norma/`.

Os cortes ficam na tabela MAPA abaixo — explícita e conferível, com a faixa de páginas de
cada norma. Foram levantados com o modo `--detectar`, que localiza títulos de ACT/CCT/termo
aditivo e trocas de número de processo no cabeçalho das páginas. Ao acrescentar PDFs novos à
pasta, rode `--detectar` e estenda a tabela.

Uso:
    python scripts/separar_normas_coletivas.py            # grava o que faltar
    python scripts/separar_normas_coletivas.py --listar   # mostra o plano, sem gravar
    python scripts/separar_normas_coletivas.py --detectar # só analisa a estrutura

Arquivo de saída já existente é mantido como está — nunca sobrescrito nem duplicado.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PASTA_PADRAO = r"D:\ASJUR\Ações - Trabalhistas\Normas Coletivas"
SUBPASTA_SAIDA = "Por norma"

# origem .md (sem extensão) -> lista de (nome de saída, página inicial, página final)
# Página final None significa "até o fim do arquivo". As páginas são as do PDF de origem,
# as mesmas dos marcadores <!-- página N -->.
MAPA: dict[str, list[tuple[str, int, "int | None"]]] = {
    "02 - Acordo Coletivo 88-89": [("1988-1989 — ACT", 1, None)],
    "03 - Acordo Coletivo 89-90": [("1989-1990 — ACT", 1, None)],
    "04 - Acordo Coletivo 90-91": [("1990-1991 — ACT", 1, None)],
    "05 - Acordo Coletivo 91-92": [("1991-1992 — ACT", 1, None)],
    "06 - Acordo Coletivo 92-93": [("1992-1993 — ACT", 1, None)],
    "07 - Acordo Coletivo 93-94": [("1993-1994 — ACT", 1, None)],
    "08 - Acordos coletivos 94-95 e 95-96": [
        ("1994-1995 — ACT", 1, 15),
        ("1995-1996 — ACT (aditamento)", 16, None),
    ],
    "09 - Acordos coletivos 97-98 e 98-99": [
        ("1997-1998 — ACT", 1, 19),
        ("1998-1999 — ACT", 20, None),
    ],
    "10 - Acordo Coletivo 99-00": [("1999-2000 — ACT", 1, None)],
    "11 - Acordo Coletivo 00-01": [("2000-2001 — ACT", 1, None)],
    "12 - Acordo Coletivo 2001-2002": [("2001-2002 — ACT", 1, None)],
    "13 - Acordo Coletivo 02-03": [("2002-2003 — ACT", 1, None)],
    "14 - Acordo Coletivo 2003-2004": [("2003-2004 — ACT", 1, None)],
    "15 - Acordo Coletivo 2004-2005": [("2004-2005 — ACT", 1, None)],
    "16 - Acordo Coletivo 2005 2006": [("2005-2006 — ACT", 1, None)],
    "17 - Acordo Coletivo 06-07": [("2006-2007 — ACT", 1, None)],
    "18 - Acordo Coletivo 2007-2008": [("2007-2008 — ACT", 1, None)],
    "19 - Acordo Coletivo 2008-2009": [("2008-2009 — ACT", 1, None)],
    "20 - Acordo Coletivo 2009-2011": [("2009-2011 — ACT", 1, None)],
    "21 - Acordaos TST 11-12 e 12-13": [
        ("2011-2012 — Sentença Normativa (TST DC 6535-37.2011)", 1, 78),
        ("2012-2013 — Sentença Normativa (TST DC 8981-76.2012)", 79, None),
    ],
    "22 - Normas Coletivas 2013-2026 pt 1": [
        ("2013-2014 — Sentença Normativa (TST DC 6942-72.2013)", 1, 144),
        ("2014-2015 — ACT", 145, 181),
        ("2015-2016 — ACT", 182, 225),
        ("2016-2017 — ACT", 226, 361),
        ("2017-2018 — ACT (mediado pelo TST)", 362, 407),
        ("2018-2019 — ACT", 408, 449),
        ("2019-2020 — Sentença Normativa (TST DC 1000662-58.2019)", 450, 593),
        ("2020 — STF, acórdão do Plenário de 24-08-2020", 594, 609),
        ("2020-2021 — TST DC 1001203-57.2020", 610, None),
    ],
    # O arquivo 23 (pt 2) está integralmente contido nas 117 primeiras páginas do 24 (pt 3):
    # recortar os dois geraria pares idênticos, então só o 24 entra (ver IGNORAR).
    "24 - Normas Coletivas 2013-2026 pt 3": [
        ("2019-2021 — Dissídios TST (DCG 1000662-58.2019 e conexos)", 1, 117),
        ("2022-2023 — ACT (mediado pelo TST, com aditivos até 2024)", 118, 165),
        ("2025 — Dissídio Coletivo (TST DC 1001307-73.2025 e STF SS 5731)", 166, None),
    ],
}

IGNORAR = {"23 - Normas Coletivas 2013-2026 pt 2"}

MARCADOR = re.compile(r"<!-- página (\d+)( \(OCR\))? -->")


def paginas_do_md(texto: str) -> list[str]:
    """Devolve os blocos de página, com o marcador `<!-- página N -->` preservado."""
    pedacos = MARCADOR.split(texto)  # [cabeçalho, num, ocr, corpo, num, ocr, corpo, ...]
    paginas = []
    for i in range(1, len(pedacos), 3):
        numero, ocr, corpo = pedacos[i], pedacos[i + 1] or "", pedacos[i + 2]
        paginas.append(f"<!-- página {numero}{ocr} -->\n{corpo.strip()}")
    return paginas


def detectar(pasta: Path) -> None:
    """Localiza candidatos a início de norma. Só relata — não grava nada."""
    titulo = re.compile(
        r"(?m)^[^\n]{0,25}?((?:ACORDO|ACÔRDO)\s+COLETIVO\s+DE\s+TRABALHO"
        r"|TERMO\s+ADITIVO|CONVEN[ÇC][ÃA]O\s+COLETIVA\s+DE\s+TRABALHO)[^\n]{0,70}$"
    )
    processo = re.compile(r"\b(\d{4,8}-\d{2}\.\d{4}\.5\.\d{2}\.\d{4})")

    def so_maiusculas(s: str) -> float:
        letras = [c for c in s if c.isalpha()]
        return sum(c.isupper() for c in letras) / max(1, len(letras))

    for md in sorted(pasta.glob("*.md")):
        texto = md.read_text(encoding="utf-8")
        paginas = paginas_do_md(texto)
        achados: dict[int, str] = {}

        for m in titulo.finditer(texto):
            linha = re.sub(r"\s+", " ", m.group(0)).strip()
            if so_maiusculas(linha) < 0.75 or "...." in linha:
                continue  # minúscula = citação no corpo; pontilhado = linha de índice
            pag = texto.count("<!-- página", 0, m.start())
            achados.setdefault(pag, f"título: {linha[:80]}")

        anterior = None
        for numero, pagina in enumerate(paginas, 1):
            m = processo.search(pagina[:600])  # só o cabeçalho da página
            atual = m.group(1) if m else None
            if atual and atual != anterior:
                achados.setdefault(numero, f"processo: {atual}")
            if atual:
                anterior = atual

        if achados:
            print(f"\n## {md.name}  ({len(paginas)} páginas)")
            for pag in sorted(achados):
                print(f"   p{pag:>4} | {achados[pag]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pasta", default=PASTA_PADRAO)
    parser.add_argument("--detectar", action="store_true", help="só analisa a estrutura")
    parser.add_argument("--listar", action="store_true", help="mostra o plano, sem gravar")
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_dir():
        print(f"ERRO: pasta não encontrada: {pasta}", file=sys.stderr)
        return 1

    if args.detectar:
        detectar(pasta)
        return 0

    saida = pasta / SUBPASTA_SAIDA
    if not args.listar:
        saida.mkdir(exist_ok=True)

    criados: list[tuple[str, str, int]] = []
    mantidos: list[str] = []
    faltando: list[str] = []

    for md in sorted(pasta.glob("*.md")):
        if md.stem in IGNORAR:
            continue
        cortes = MAPA.get(md.stem)
        if cortes is None:
            faltando.append(md.name)
            continue

        texto = md.read_text(encoding="utf-8")
        paginas = paginas_do_md(texto)
        total = len(paginas)

        for nome, inicio, fim in cortes:
            fim = fim or total
            if inicio > total:
                print(f"AVISO: {md.name} tem {total} páginas; o corte {nome} começa em {inicio}")
                continue
            destino = saida / f"{nome}.md"

            if destino.exists():
                mantidos.append(destino.name)
                continue
            if args.listar:
                criados.append((destino.name, md.name, fim - inicio + 1))
                continue

            corpo = "\n\n".join(paginas[inicio - 1 : fim])
            destino.write_text(
                f"# {nome}\n\n"
                f"> Recortado de `{md.stem}.pdf` (páginas {inicio}–{fim} de {total}).\n"
                f"> Os marcadores `<!-- página N -->` são os do PDF de origem — cite por eles.\n"
                f"> O PDF original é a fonte oficial; parte do texto vem de OCR.\n\n"
                f"{corpo}\n",
                encoding="utf-8",
            )
            criados.append((destino.name, md.name, fim - inicio + 1))

    verbo = "seriam criados" if args.listar else "criados"
    print(f"\n{len(criados)} arquivo(s) {verbo} em {saida}:")
    for nome, origem, n in criados:
        print(f"   + {nome}  ({n} pgs, de {origem})")
    if mantidos:
        print(f"\n{len(mantidos)} já existiam e foram mantidos:")
        for nome in mantidos:
            print(f"   = {nome}")
    if faltando:
        print(f"\n{len(faltando)} arquivo(s) sem entrada no MAPA (rode --detectar e complete):")
        for nome in faltando:
            print(f"   ? {nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
