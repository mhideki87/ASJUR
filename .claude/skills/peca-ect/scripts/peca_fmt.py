# -*- coding: utf-8 -*-
"""Construtor de peças da Assessoria Jurídica ECT/MS.

Gera .docx reaproveitando modelos/_FORMATO_BASE.docx: cabeçalho, rodapé, estilos,
logotipo e configuração de página são copiados byte a byte; só word/document.xml
é substituído. Os sete papéis de parágrafo abaixo foram extraídos de peças reais
aprovadas — não altere os valores sem conferir contra uma peça nova.

    box("DO MÉRITO")                  tópico principal, em retângulo
    sub("1 – DA PRESCRIÇÃO")          subtópico numerado, negrito + sublinhado
    p("texto...")                     corpo, recuo de 1ª linha de 3 cm
    cit("texto...")                   citação em bloco, 10 pt, itálico, recuo 3 cm
    alinea("a)", "texto...")          alínea do rol de requerimentos
    travessao("texto...")             item de lista com travessão
    hdr("Autos nº ...")               endereçamento e qualificação, sem recuo
    fecho()                           N. Termos / P. Deferimento / assinatura
    montar(blocos, "saida.docx")      empacota o .docx final
"""
import os
import re
import zipfile
from xml.sax.saxutils import escape

# _FORMATO_BASE.docx: dois níveis acima de scripts/, na raiz do repositório
_AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("ASJUR_FORMATO_BASE") or os.path.abspath(
    os.path.join(_AQUI, "..", "..", "..", "..", "modelos", "_FORMATO_BASE.docx"))

RF = '<w:rFonts w:eastAsia="Arial" w:cs="Arial"/>'
BORDA = ('<w:pBdr>'
         '<w:top w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:left w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '<w:right w:val="single" w:sz="6" w:space="4" w:color="000000"/>'
         '</w:pBdr>')

# ---------------------------------------------------------------- parágrafos
PPR = {
    # endereçamento, autos, rótulos de polo: sem recuo, justificado
    "hdr": '<w:pPr><w:pStyle w:val="Normal"/>'
           '<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
           '<w:ind w:left="0" w:right="0" w:hanging="0"/><w:jc w:val="both"/><w:rPr/></w:pPr>',
    # corpo: recuo de 1ª linha de 3 cm (1701 twips), entrelinha 1,5 exata
    "p": '<w:pPr><w:pStyle w:val="Normal"/>'
         '<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
         '<w:ind w:left="0" w:right="0" w:firstLine="1701"/><w:jc w:val="both"/><w:rPr/></w:pPr>',
    # tópico principal: retângulo, centralizado, negrito (SEM sublinhado)
    "box": '<w:pPr><w:pStyle w:val="Normal"/><w:keepNext/>' + BORDA +
           '<w:spacing w:lineRule="exact" w:line="240" w:before="320" w:after="260"/>'
           '<w:ind w:left="0" w:right="0" w:hanging="0"/><w:jc w:val="center"/><w:rPr/></w:pPr>',
    # subtópico numerado: recuo de bloco de 3 cm, negrito + sublinhado
    "sub": '<w:pPr><w:pStyle w:val="Normal"/><w:keepNext/>'
           '<w:spacing w:lineRule="exact" w:line="360" w:before="200" w:after="120"/>'
           '<w:ind w:left="1701" w:hanging="0"/><w:jc w:val="both"/>'
           '<w:rPr><w:u w:val="single"/></w:rPr></w:pPr>',
    # citação em bloco: recuo 3 cm, entrelinha 260, corpo 10 pt e itálico (ver run)
    "cit": '<w:pPr><w:pStyle w:val="Normal"/>'
           '<w:spacing w:lineRule="exact" w:line="260" w:before="0" w:after="160"/>'
           '<w:ind w:left="1701" w:right="0" w:hanging="0"/><w:jc w:val="both"/><w:rPr/></w:pPr>',
    # alínea do rol de requerimentos: mesmo bloco de 3 cm, sem recuo de 1ª linha
    "alin": '<w:pPr><w:pStyle w:val="Normal"/>'
            '<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
            '<w:ind w:left="1701" w:right="0" w:hanging="0"/><w:jc w:val="both"/><w:rPr/></w:pPr>',
    # item de lista com travessão: recuo 3,6 cm com pendente de 0,6 cm
    "trav": '<w:pPr><w:pStyle w:val="Normal"/>'
            '<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="160"/>'
            '<w:ind w:left="2041" w:right="0" w:hanging="340"/><w:jc w:val="both"/><w:rPr/></w:pPr>',
    # centralizado (bloco de assinatura)
    "c": '<w:pPr><w:pStyle w:val="Normal"/><w:spacing w:before="0" w:after="60"/>'
         '<w:jc w:val="center"/><w:rPr/></w:pPr>',
    "c2": '<w:pPr><w:pStyle w:val="Normal"/><w:spacing w:before="0" w:after="200"/>'
          '<w:jc w:val="center"/><w:rPr/></w:pPr>',
    # linha em branco
    "v": '<w:pPr><w:pStyle w:val="Normal"/><w:spacing w:before="0" w:after="200"/><w:rPr/></w:pPr>',
}


def run(texto, estilo="", sz=22):
    """estilo: 'b' negrito, 'i' itálico, 'u' sublinhado (combináveis: 'bu')."""
    texto = re.sub(r"[ ]{2,}", " ", texto)
    b = "<w:b/><w:bCs/>" if "b" in estilo else ""
    i = "<w:i/>" if "i" in estilo else ""
    u = '<w:u w:val="single"/>' if "u" in estilo else ""
    esp = ' xml:space="preserve"' if (texto != texto.strip() or not texto) else ""
    return (f'<w:r><w:rPr>{RF}{b}{i}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>{u}</w:rPr>'
            f'<w:t{esp}>{escape(texto)}</w:t></w:r>')


def par(papel, trechos, sz=22):
    """trechos: str, ou lista de (texto, estilo)."""
    if isinstance(trechos, str):
        trechos = [(trechos, "")]
    return f'<w:p>{PPR[papel]}' + "".join(run(t, e, sz) for t, e in trechos) + '</w:p>'


# ------------------------------------------------------------------ atalhos
def hdr(trechos):
    return par("hdr", trechos)


def p(trechos):
    return par("p", trechos)


def box(titulo):
    """Tópico principal em retângulo: negrito, centralizado, SEM sublinhado."""
    return par("box", [(titulo, "b")])


def sub(titulo):
    """Subtópico numerado: negrito e sublinhado, sempre.

    Normaliza a convenção da casa: '1. Título.' vira '1 – TÍTULO', com travessão
    e sem ponto final. Assim o ponto de chamada não consegue divergir do padrão.
    """
    if isinstance(titulo, str):
        titulo = [(titulo, "bu")]
    titulo = [(t, "bu" if e in ("", "b", "u", "bu") else e) for t, e in titulo]
    if titulo:
        t0, e0 = titulo[0]
        titulo[0] = (re.sub(r"^(\d+)[.)]\s+", r"\1 – ", t0), e0)
        tn, en = titulo[-1]
        titulo[-1] = (tn.rstrip().rstrip("."), en)
    return par("sub", titulo)


def cit(trechos):
    """Citação em bloco: 10 pt, itálico, recuo de 3 cm."""
    if isinstance(trechos, str):
        trechos = [(trechos, "i")]
    trechos = [(t, e if e else "i") for t, e in trechos]
    return par("cit", trechos, sz=20)


def alinea(rotulo, trechos):
    """Alínea do rol de requerimentos; o rótulo ('a)') sai em negrito."""
    if isinstance(trechos, str):
        trechos = [(trechos, "")]
    trechos = list(trechos)
    trechos[0] = (trechos[0][0].lstrip(), trechos[0][1])   # evita espaço duplo após o rótulo
    return par("alin", [(rotulo + " ", "b")] + trechos)


def travessao(trechos):
    if isinstance(trechos, str):
        trechos = [(trechos, "")]
    return par("trav", [("– ", "")] + list(trechos))


def vazio(n=1):
    return "".join(f'<w:p>{PPR["v"]}<w:r><w:rPr/></w:r></w:p>' for _ in range(n))


def quebra():
    return ('<w:p><w:pPr><w:pStyle w:val="Normal"/><w:spacing w:before="0" w:after="0"/>'
            '<w:rPr/></w:pPr><w:r><w:rPr/><w:br w:type="page"/></w:r></w:p>')


def assinatura():
    return par("c", [("Marcos Hideki Kamibayashi", "b")]) + par("c2", [("OAB/MS 14.580", "b")])


def fecho():
    return (p("Nesses Termos,") + p("Pede Deferimento.") +
            p("Campo Grande/MS, data de assinatura eletrônica.") + vazio(2) + assinatura())


# ---------------------------------------------------------------- empacotar
def montar(blocos, saida, base=None):
    """Injeta os parágrafos no document.xml do modelo, preservando o resto."""
    base = base or BASE
    zin = zipfile.ZipFile(base, "r")
    doc = zin.read("word/document.xml").decode("utf-8")
    ini = doc.index("<w:body>") + len("<w:body>")
    fim = doc.index("<w:sectPr")
    novo = doc[:ini] + "".join(blocos) + doc[fim:]
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            dados = zin.read(item.filename)
            if item.filename == "word/document.xml":
                dados = novo.encode("utf-8")
            elif item.filename == "docProps/app.xml":
                dados = re.sub(rb"<(Pages|Words|Characters|CharactersWithSpaces|Paragraphs|TotalTime)>"
                               rb"\d+</\1>", rb"<\1>0</\1>", dados)
            zout.writestr(item, dados)
    zin.close()
    return saida
