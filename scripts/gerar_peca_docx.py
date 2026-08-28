#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o .docx de uma peça a partir do modelo visual e de um arquivo de conteúdo.

Por que existe: a formatação das peças (fonte, recuos, entrelinha, caixa dos marcadores de
seção, sublinhado dos títulos, recuo das citações) é rígida e não se acerta "no olho". Este
script parte do .docx modelo — preservando cabeçalho, logotipo, rodapé e estilos byte a byte —
e escreve só o corpo, com o pPr/rPr exato de cada tipo de parágrafo.

Uso:
    python scripts/gerar_peca_docx.py conteudo.txt -o "Cont - Inc Fun - ATSum - NOME.docx"
    python scripts/gerar_peca_docx.py conteudo.txt -o saida.docx --base modelos/_FORMATO_BASE.docx

Formato do arquivo de conteúdo: uma marca por parágrafo, no início da linha.

    @vara            2ª Vara do Trabalho de Campo Grande/MS   (só o miolo do endereçamento)
    @autos           0000000-00.0000.5.24.0000
    @reclamante      NOME DA PARTE
    @admissibilidade arts. 847 da CLT e 336 do CPC
    @tipo            CONTESTAÇÃO
    @caixa    MARCADOR DE SEÇÃO (centralizado, negrito, com borda)
    @titulo   1 – TÍTULO DE TÓPICO (negrito + sublinhado, recuo 3 cm)
    @p        parágrafo de corpo (justificado, recuo de 1ª linha 3 cm)
    @cit      citação de jurisprudência/norma (itálico 10 pt, bloco recuado 3 cm)
    @lista    – item de lista (recuo 3,6 cm com pendente)
    @centro   texto centralizado
    @vazio    linha em branco

Linhas iniciadas por # são comentário. Linha sem marca é continuação do parágrafo anterior.
Somente stdlib — roda em qualquer ambiente com Python 3, inclusive no cloud/web.
"""
import argparse
import pathlib
import re
import shutil
import sys
import zipfile

RF = '<w:rFonts w:eastAsia="Arial" w:cs="Arial"/>'
BORDA = ('<w:pBdr>'
         '<w:top w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:left w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:right w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '</w:pBdr>')

# pPr e rPr extraídos de peça real aprovada — não alterar sem conferir contra o modelo.
ESTILOS = {
    "p": ('<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
          '<w:ind w:left="0" w:right="0" w:firstLine="1701"/><w:jc w:val="both"/>',
          f'{RF}<w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "titulo": ('<w:spacing w:lineRule="exact" w:line="360" w:before="200" w:after="120"/>'
               '<w:ind w:left="1701" w:hanging="0"/><w:jc w:val="both"/>',
               f'{RF}<w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/><w:u w:val="single"/>'),
    "cit": ('<w:spacing w:lineRule="exact" w:line="260" w:before="0" w:after="160"/>'
            '<w:ind w:left="1701" w:right="0" w:hanging="0"/><w:jc w:val="both"/>',
            f'{RF}<w:i/><w:sz w:val="20"/><w:szCs w:val="20"/>'),
    "caixa": (BORDA + '<w:spacing w:lineRule="exact" w:line="240" w:before="320" w:after="260"/>'
              '<w:ind w:left="0" w:right="0" w:hanging="0"/><w:jc w:val="center"/>',
              f'{RF}<w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "lista": ('<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
              '<w:ind w:left="2041" w:right="0" w:hanging="340"/><w:jc w:val="both"/>',
              f'{RF}<w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "centro": ('<w:spacing w:before="0" w:after="60"/><w:jc w:val="center"/>',
               f'{RF}<w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "semrecuo": ('<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
                 '<w:ind w:left="0" w:right="0" w:hanging="0"/><w:jc w:val="both"/>',
                 f'{RF}<w:sz w:val="22"/><w:szCs w:val="22"/>'),
}
VAZIO = ('<w:p><w:pPr><w:pStyle w:val="Normal"/><w:spacing w:before="0" w:after="200"/>'
         '<w:rPr></w:rPr></w:pPr><w:r><w:rPr></w:rPr></w:r></w:p>')

CAMPOS = ("vara", "autos", "reclamante", "admissibilidade", "tipo")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def paragrafo(marca, texto):
    if marca == "vazio":
        return VAZIO
    ppr, rpr = ESTILOS[marca]
    return (f'<w:p><w:pPr><w:pStyle w:val="Normal"/><w:widowControl/>{ppr}<w:rPr></w:rPr></w:pPr>'
            f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{esc(texto)}</w:t></w:r></w:p>')


def ler_conteudo(caminho):
    campos, corpo = {}, []
    for linha in pathlib.Path(caminho).read_text(encoding="utf-8").splitlines():
        if linha.lstrip().startswith("#"):
            continue
        m = re.match(r"^@(\w+)\s?(.*)$", linha)
        if m:
            marca, texto = m.group(1), m.group(2).strip()
            if marca in CAMPOS:
                campos[marca] = texto
            elif marca == "vazio":
                corpo.append(["vazio", ""])
            elif marca in ESTILOS:
                corpo.append([marca, texto])
            else:
                sys.exit(f"ERRO: marca @{marca} desconhecida. Válidas: "
                         f"{', '.join(sorted(set(ESTILOS) | set(CAMPOS) | {'vazio'}))}")
        elif linha.strip():
            if not corpo:
                sys.exit("ERRO: texto sem marca antes do primeiro parágrafo.")
            corpo[-1][1] = (corpo[-1][1] + " " + linha.strip()).strip()
    return campos, corpo


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("conteudo")
    ap.add_argument("-o", "--saida", required=True)
    ap.add_argument("--base", default="modelos/_FORMATO_BASE.docx")
    args = ap.parse_args()

    base = pathlib.Path(args.base)
    if not base.exists():
        sys.exit(f"ERRO: modelo visual não encontrado: {base}")
    campos, corpo = ler_conteudo(args.conteudo)
    if not corpo:
        sys.exit("ERRO: arquivo de conteúdo sem nenhum parágrafo.")

    xml = zipfile.ZipFile(base).read("word/document.xml").decode("utf-8")
    subs = {
        "[Nº]ª VARA DO TRABALHO DE CAMPO GRANDE/MS": campos.get("vara", "[Nº]ª VARA DO TRABALHO DE CAMPO GRANDE/MS"),
        "[Nº DO PROCESSO]": campos.get("autos", "[Nº DO PROCESSO]"),
        "[NOME DA RECLAMANTE]": campos.get("reclamante", "[NOME DA RECLAMANTE]"),
        "[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE — ex.: arts. 847 CLT c/c 336 CPC para contestação]":
            campos.get("admissibilidade", "[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]"),
        "[TIPO DE PEÇA]": campos.get("tipo", "[TIPO DE PEÇA]"),
    }
    for k, v in subs.items():
        xml = xml.replace(esc(k), esc(v))

    m = re.search(r"<w:p>(?:(?!</w:p>).)*\[CORPO DA PEÇA.*?</w:p>", xml, re.S)
    if not m:
        sys.exit("ERRO: o modelo visual não tem o parágrafo marcador '[CORPO DA PEÇA ...]'. "
                 "Use um .docx base que o contenha (ver modelos/README.md).")
    xml = xml[:m.start()] + "".join(paragrafo(m_, t) for m_, t in corpo) + xml[m.end():]

    restantes = [k for k in ("[Nº DO PROCESSO]", "[NOME DA RECLAMANTE]", "[TIPO DE PEÇA]") if k in xml]
    saida = pathlib.Path(args.saida)
    zin = zipfile.ZipFile(base)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zin.infolist():
            dados = xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
            zo.writestr(item, dados)

    print(f"OK: {saida} — {len(corpo)} parágrafos, base {base.name}.")
    if restantes:
        print(f"ATENÇÃO: placeholders não preenchidos: {', '.join(restantes)}")
    marcados = len(re.findall(r"\[(?:REVISAR|INSERIR)", xml))
    if marcados:
        print(f"ATENÇÃO: {marcados} marcações [REVISAR]/[INSERIR] no corpo — conferência humana pendente.")


if __name__ == "__main__":
    main()
