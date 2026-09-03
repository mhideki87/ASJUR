#!/usr/bin/env python3
"""Gera a minuta em .docx no padrão ASJUR/ECT a partir de um .md com marcação.

Clona todas as partes de `modelos/_FORMATO_BASE.docx` (cabeçalho com logotipo, rodapé com endereço e
numeracao, estilos, configuração de página) e regrava apenas `word/document.xml`. Assim a formatação nunca
se degrada de uma geração para a outra.

Uso:
    python .claude/skills/formatar-minuta/scripts/gerar_minuta_docx.py <minuta.md> <saida.docx>
    python ... <minuta.md> <saida.docx> --base <outro_formato_base.docx>
    python ... <minuta.md> --check          # só valida a marcação, não escreve arquivo

Só stdlib (Python 3.8+). A especificação das medidas está em
`.claude/skills/formatar-minuta/referencia/especificacao_formatacao.md`.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

REPO_RAIZ = Path(__file__).resolve().parents[4]
BASE_PADRAO = REPO_RAIZ / "modelos" / "_FORMATO_BASE.docx"

ASSINATURA_PADRAO = ("Marcos Hideki Kamibayashi", "OAB/MS 14.580")
LOCAL_PADRAO = "Campo Grande/MS, data de assinatura eletrônica."

# --- medidas do padrão, em twips (ver referencia/especificacao_formatacao.md) -------------------------
RECUO_3CM = 1701
RECUO_4CM = 2268
SZ_CORPO = 22   # 11 pt
SZ_CITACAO = 20  # 10 pt


# --- XML ---------------------------------------------------------------------------------------------
def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# Ordem dos filhos de w:rPr e w:pPr é imposta pelo schema OOXML (CT_RPr / CT_PPr) e é a mesma da peça
# de referência: rPr = rFonts, b, bCs, i, iCs, sz, szCs, u · pPr = pStyle, pBdr, spacing, ind, jc, rPr.
FONTE = '<w:rFonts w:eastAsia="Arial" w:cs="Arial"/>'


def rpr(flags, sz: int) -> str:
    x = FONTE
    if "b" in flags:
        x += "<w:b/><w:bCs/>"
    if "i" in flags:
        x += "<w:i/><w:iCs/>"
    elif sz == SZ_CITACAO:
        # citação e bloco de cálculo desligam o itálico explicitamente, como na peça de referência
        x += '<w:i w:val="false"/><w:iCs w:val="false"/>'
    x += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    if "u" in flags:
        x += '<w:u w:val="single"/>'
    return f"<w:rPr>{x}</w:rPr>"


def run(flags, texto: str, sz: int) -> str:
    return f'<w:r>{rpr(flags, sz)}<w:t xml:space="preserve">{esc(texto)}</w:t></w:r>'


def ppr(jc=None, line=None, before=0, after=0, ind=None, caixa=False, marca_u=False, wc=False) -> str:
    x = '<w:pStyle w:val="Normal"/>'
    if wc:
        x += '<w:widowControl/><w:bidi w:val="0"/>'
    if caixa:
        x += "<w:pBdr>" + "".join(
            f'<w:{l} w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
            for l in ("top", "left", "bottom", "right")
        ) + "</w:pBdr>"
    if line:
        x += f'<w:spacing w:lineRule="exact" w:line="{line}" w:before="{before}" w:after="{after}"/>'
    else:
        x += f'<w:spacing w:before="{before}" w:after="{after}"/>'
    if ind:
        ordem = ("left", "right", "firstLine", "hanging")
        atrs = " ".join(f'w:{k}="{ind[k]}"' for k in ordem if k in ind)
        x += f"<w:ind {atrs}/>"
    if jc:
        x += f'<w:jc w:val="{jc}"/>'
    x += '<w:rPr><w:u w:val="single"/></w:rPr>' if marca_u else "<w:rPr></w:rPr>"
    return f"<w:pPr>{x}</w:pPr>"


def para(texto_inline: str, *, sz=SZ_CORPO, flags_base=frozenset(), maiuscula=False, **kw) -> str:
    partes = parse_inline(texto_inline, frozenset(flags_base))
    runs = "".join(run(f, t.upper() if maiuscula else t, sz) for f, t in partes if t)
    return f"<w:p>{ppr(**kw)}{runs}</w:p>"


def vazio(after=200) -> str:
    return f"<w:p>{ppr(after=after)}<w:r><w:rPr></w:rPr></w:r></w:p>"


def quebra_pagina() -> str:
    return f'<w:p>{ppr(after=0)}<w:r><w:br w:type="page"/></w:r></w:p>'


# --- ênfase inline: **negrito**, *itálico*, __sublinhado__ --------------------------------------------
MARCAS = (("**", "b"), ("__", "u"), ("*", "i"))


def parse_inline(s: str, flags=frozenset()):
    saida, buf, i = [], "", 0
    while i < len(s):
        for marca, flag in MARCAS:
            if s.startswith(marca, i):
                fim = s.find(marca, i + len(marca))
                if fim != -1:
                    if buf:
                        saida.append((flags, buf))
                        buf = ""
                    saida.extend(parse_inline(s[i + len(marca):fim], flags | {flag}))
                    i = fim + len(marca)
                    break
        else:
            buf += s[i]
            i += 1
            continue
    if buf:
        saida.append((flags, buf))
    return saida


# --- blocos do padrão --------------------------------------------------------------------------------
def p_enderecamento(t):
    return para(t, flags_base={"b"}, maiuscula=True, jc="both", line=360, after=160,
                ind={"hanging": 0})


def p_autos(t):
    t = t if t.rstrip().endswith(".") else t.rstrip() + "."
    return para(f"Autos nº. {t}", flags_base={"b"}, jc="both", line=360, after=160,
                ind={"hanging": 0})


def p_polo(t):
    rotulo, _, valor = t.partition(":")
    corpo = f"**{rotulo.strip()}: **{valor.strip()}" if valor.strip() else f"**{rotulo.strip()}**"
    return para(corpo, jc="both", line=360, after=160, ind={"hanging": 0})


def p_preambulo(t):
    return para(t, jc="both", line=360, after=120, ind={"firstLine": RECUO_3CM})


def p_topico(t):
    return para(t, flags_base={"b"}, maiuscula=True, jc="center", line=240, before=320, after=260,
                ind={"left": 0, "right": 0, "hanging": 0}, caixa=True)


def p_subtopico(t):
    return para(t, flags_base={"b", "u"}, maiuscula=True, jc="both", line=360, before=200, after=120,
                ind={"left": RECUO_3CM, "hanging": 0}, marca_u=True)


def p_corpo(t):
    return para(t, jc="both", line=360, after=120, ind={"firstLine": RECUO_3CM})


def p_citacao(t):
    return para(t, sz=SZ_CITACAO, jc="both", line=240, before=100, after=160,
                ind={"left": RECUO_4CM, "hanging": 0})


def p_calculo(t, before, after):
    return para(t, sz=SZ_CITACAO, jc="left", line=240, before=before, after=after,
                ind={"left": RECUO_4CM, "hanging": 0})


def p_alinea(t, after):
    return para(t, jc="both", line=360, after=after,
                ind={"left": RECUO_3CM, "right": 0, "hanging": 0}, wc=True)


def p_fecho(local):
    ps = [
        para(t, jc="both", line=360, after=160,
             ind={"left": 0, "right": 0, "firstLine": RECUO_3CM}, wc=True)
        for t in ("Nesses Termos,", "Pede Deferimento.", local)
    ]
    return ps


def p_assinatura(nome, oab):
    return [
        para(nome, flags_base={"b"}, jc="center", after=60),
        para(oab, flags_base={"b"}, jc="center", after=200),
    ]


# --- parser da minuta --------------------------------------------------------------------------------
CAMPOS = ("ENDERECAMENTO", "AUTOS", "POLO", "PREAMBULO", "FECHO", "ASSINATURA", "QUEBRA")


def blocos(texto: str):
    """Fatia o .md em blocos separados por linha em branco, juntando continuações indentadas."""
    bruto, atual = [], []
    em_comentario = False
    for linha in texto.splitlines():
        if em_comentario:
            em_comentario = "-->" not in linha
            continue
        if linha.lstrip().startswith("<!--"):
            em_comentario = "-->" not in linha
            continue
        if not linha.strip():
            if atual:
                bruto.append(atual)
                atual = []
            continue
        atual.append(linha)
    if atual:
        bruto.append(atual)
    return bruto


def itens(linhas, marcadores):
    """Dentro de um bloco de lista, cada linha com marcador é um item; linha indentada continua o item."""
    saida = []
    for linha in linhas:
        nu = linha.strip()
        eh_novo = any(nu.startswith(m) for m in marcadores)
        if eh_novo or not saida:
            for m in marcadores:
                if nu.startswith(m):
                    nu = nu[len(m):].strip()
                    break
            saida.append(nu)
        else:
            saida[-1] += " " + nu
    return saida


def converter(texto: str):
    corpo, avisos = [], []
    assinatura = list(ASSINATURA_PADRAO)
    local = LOCAL_PADRAO
    contexto = {"topico": None, "numeros": []}
    grupo_qualificacao = False
    tem_fecho = False

    def fechar_qualificacao():
        nonlocal grupo_qualificacao
        if grupo_qualificacao:
            corpo.extend([vazio(), vazio()])
            grupo_qualificacao = False

    for bloco in blocos(texto):
        primeira = bloco[0].strip()

        # campos @CAMPO: valor
        m = re.match(r"@([A-Z_]+)\s*:?\s*(.*)$", primeira)
        if m and m.group(1) in CAMPOS:
            campo, valor = m.group(1), " ".join([m.group(2).strip()] + [l.strip() for l in bloco[1:]]).strip()
            if campo == "ENDERECAMENTO":
                fechar_qualificacao()
                corpo.append(p_enderecamento(valor))
                corpo.extend([vazio() for _ in range(4)])
            elif campo == "AUTOS":
                corpo.append(p_autos(valor))
                grupo_qualificacao = True
            elif campo == "POLO":
                corpo.append(p_polo(valor))
                grupo_qualificacao = True
            elif campo == "PREAMBULO":
                fechar_qualificacao()
                corpo.append(p_preambulo(valor))
            elif campo == "ASSINATURA":
                partes = [x.strip() for x in valor.split("|")]
                if len(partes) == 2:
                    assinatura = partes
                else:
                    avisos.append('@ASSINATURA precisa do formato "Nome | OAB/UF 00.000" — mantida a padrão.')
            elif campo == "QUEBRA":
                fechar_qualificacao()
                corpo.append(quebra_pagina())
            elif campo == "FECHO":
                fechar_qualificacao()
                if valor:
                    local = valor
                corpo.extend(p_fecho(local))
                corpo.extend([vazio(), vazio()])
                corpo.extend(p_assinatura(*assinatura))
                tem_fecho = True
            continue

        fechar_qualificacao()

        # títulos
        if primeira.startswith("#"):
            for linha in bloco:
                nu = linha.strip()
                nivel = len(nu) - len(nu.lstrip("#"))
                txt = nu.lstrip("#").strip()
                if nivel == 1:
                    corpo.append(p_topico(txt))
                    contexto["topico"] = txt
                    contexto["numeros"] = []
                else:
                    corpo.append(p_subtopico(txt))
                    checar_numeracao(txt, contexto, avisos)
            continue

        # bloco de cálculo/enumeração  >>
        if primeira.startswith(">>"):
            linhas = itens(bloco, (">>",))
            for idx, t in enumerate(linhas):
                before = 100 if idx == 0 else 0
                after = 160 if idx == len(linhas) - 1 else 40
                corpo.append(p_calculo(t, before, after))
            continue

        # citação  >
        if primeira.startswith(">"):
            t = " ".join(l.strip().lstrip(">").strip() for l in bloco).strip()
            corpo.append(p_citacao(t))
            continue

        # alíneas do corpo  -   /  de requerimento  +
        if primeira.startswith("- ") or primeira.startswith("+ "):
            marcador = primeira[0]
            after = 120 if marcador == "-" else 160
            for t in itens(bloco, (marcador + " ",)):
                corpo.append(p_alinea(t, after))
            continue

        # corpo do texto
        corpo.append(p_corpo(" ".join(l.strip() for l in bloco)))

    if not tem_fecho:
        avisos.append("Nenhum @FECHO na minuta — a peça saiu sem fecho e sem bloco de assinatura.")
    if "[^" in texto or re.search(r"\n\[\d+\]:", texto):
        avisos.append("Marcação de nota de rodapé encontrada: o padrão ASJUR não usa nota de rodapé — "
                      "traga a referência para o corpo, entre parênteses.")
    pendencias = len(re.findall(r"\[(?:REVISAR|INSERIR):", texto))
    return corpo, avisos, pendencias


def checar_numeracao(titulo, contexto, avisos):
    m = re.match(r"^(\d+(?:\.\d+)*)\s*(.)", titulo)
    if not m:
        avisos.append(f'Subtópico sem numeração no formato "N – TÍTULO": {titulo[:60]!r}')
        return
    if m.group(2) not in "–—":
        avisos.append(f'Subtópico deve separar número e título por " – " (travessão): {titulo[:60]!r}')
    numero = m.group(1)
    if "." not in numero:
        esperado = str(len([n for n in contexto["numeros"] if "." not in n]) + 1)
        if numero != esperado:
            avisos.append(
                f'Numeração fora de sequência em "{contexto["topico"] or "(sem tópico)"}": '
                f"veio {numero}, esperado {esperado}."
            )
    contexto["numeros"].append(numero)


# --- montagem do .docx -------------------------------------------------------------------------------
def gerar(md: Path, saida: Path, base: Path):
    corpo, avisos, pendencias = converter(md.read_text(encoding="utf-8"))

    with zipfile.ZipFile(base) as z:
        doc = z.read("word/document.xml").decode("utf-8")
        itens_zip = [(i, z.read(i.filename)) for i in z.infolist()]

    abertura = re.match(r"<\?xml[^>]*\?>\s*<w:document[^>]*>", doc)
    sect = re.search(r"<w:sectPr>.*?</w:sectPr>", doc, re.S)
    if not abertura or not sect:
        raise SystemExit(f"ERRO: {base} não parece ser o .docx base do padrão (sem w:document/w:sectPr).")

    novo = f"{abertura.group(0)}<w:body>{''.join(corpo)}{sect.group(0)}</w:body></w:document>"

    saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for info, dados in itens_zip:
            z.writestr(info, novo.encode("utf-8") if info.filename == "word/document.xml" else dados)

    return corpo, avisos, pendencias


def main():
    ap = argparse.ArgumentParser(description="Gera a minuta .docx no padrão ASJUR/ECT.")
    ap.add_argument("minuta", type=Path, help="arquivo .md com a marcação da minuta")
    ap.add_argument("saida", type=Path, nargs="?", help="arquivo .docx a gravar")
    ap.add_argument("--base", type=Path, default=BASE_PADRAO, help="docx base (padrão: modelos/_FORMATO_BASE.docx)")
    ap.add_argument("--check", action="store_true", help="só valida a marcação, não grava arquivo")
    a = ap.parse_args()

    if not a.minuta.exists():
        raise SystemExit(f"ERRO: minuta não encontrada: {a.minuta}")
    if a.check:
        corpo, avisos, pendencias = converter(a.minuta.read_text(encoding="utf-8"))
    else:
        if not a.saida:
            raise SystemExit("ERRO: informe o .docx de saída (ou use --check).")
        if not a.base.exists():
            raise SystemExit(f"ERRO: formato base não encontrado: {a.base}")
        corpo, avisos, pendencias = gerar(a.minuta, a.saida, a.base)
        print(f"Gravado: {a.saida}  ({len(corpo)} parágrafos)")

    if pendencias:
        print(f"{pendencias} marcação(ões) [REVISAR/INSERIR] no texto — repita-as na lista de "
              f"conferência humana da resposta.", file=sys.stderr)
    for av in avisos:
        print(f"AVISO: {av}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
