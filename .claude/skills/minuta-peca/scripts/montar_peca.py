# -*- coding: utf-8 -*-
"""Monta uma petição .docx no padrão visual da Assessoria Jurídica MS/DEJUR/SEJUR.

Toda minuta é entregue em .docx — nunca .md, .txt, .pdf ou .odt. `nome_arquivo` e
`montar` recusam qualquer outra extensão.

Reaproveita cabeçalho (logotipo), rodapé, estilos e margens de modelos/_FORMATO_BASE.docx
e escreve o corpo com os tipos de parágrafo do padrão aprovado — em especial os tópicos
em RETÂNGULO (borda simples nos quatro lados, centralizados, negrito).

Uso:
    from montar_peca import montar, nome_arquivo

    montar(
        saida=nome_arquivo("Contestação", "Doença Ocupacional", "FULANO DE TAL"),
        vara="5ª VARA DO TRABALHO DE CAMPO GRANDE/MS",
        autos="0000000-00.0000.5.24.0000",
        reclamante="FULANO DE TAL",
        admissibilidade="fundamento nos arts. 847 da CLT c/c 336 do CPC",
        tipo_peca="CONTESTAÇÃO",
        corpo=[("T", "DO MÉRITO"), ("P", "Texto do parágrafo com **negrito** e *itálico*.")],
    )

Tipos de parágrafo aceitos em `corpo`:
    T  tópico em retângulo  — centralizado, negrito, borda nos 4 lados
    S  subtópico            — negrito + sublinhado, recuo 1701
    P  parágrafo de texto   — justificado, 1ª linha 1701, entrelinha 360
    C  citação/ementa       — recuo 1701, itálico, corpo 10, entrelinha 260
    A  alínea / requerimento — bloco recuado em 1701, sem recuo de 1ª linha
    M  marcador (travessão) — recuo 2041 com deslocamento 340
    Q  quesito numerado     — numera automaticamente "QUESITO n. " em negrito
    B  linha em branco

Marcação inline: **negrito**, *itálico*, ***negrito itálico***.
"""
import os
import re
import zipfile
from xml.sax.saxutils import escape

BASE_PADRAO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..", "modelos", "_FORMATO_BASE.docx",
)

# ---------------------------------------------------------------- nome do arquivo

_INVALIDOS = r'[<>:"/\\|?*]'


def nome_arquivo(*designacoes, ext=".docx"):
    """Monta o nome do arquivo no padrão do usuário.

    Espaços simples nas separações internas (nunca "_") e " - " entre as designações:
        nome_arquivo("Quesitos", "Perícia Médica", "JOÃO DA SILVA SANTOS")
        -> "Quesitos - Perícia Médica - JOÃO DA SILVA SANTOS.docx"

    Minuta é sempre .docx; outra extensão é recusada.
    """
    if ext.lower() != ".docx":
        raise ValueError(
            "minuta é sempre entregue em .docx — extensão recusada: %r" % ext)
    partes = []
    for d in designacoes:
        if d is None:
            continue
        d = str(d).replace("_", " ")
        d = re.sub(_INVALIDOS, " ", d)
        d = re.sub(r"\s+", " ", d).strip(" -")
        if d:
            partes.append(d)
    if not partes:
        raise ValueError("nome_arquivo exige ao menos uma designação")
    return " - ".join(partes) + ext


# ---------------------------------------------------------------- runs e parágrafos

def _rpr(bold=False, italic=False, underline=False, sz=22):
    p = '<w:rPr><w:rFonts w:eastAsia="Arial" w:cs="Arial"/>'
    if bold:
        p += "<w:b/><w:bCs/>"
    if italic:
        p += "<w:i/><w:iCs/>"
    p += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    if underline:
        p += '<w:u w:val="single"/>'
    return p + "</w:rPr>"


_TOKEN = re.compile(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*)", re.S)


def _runs(texto, bold=False, italic=False, underline=False, sz=22):
    """Converte marcação inline **negrito** / *itálico* em runs do OOXML."""
    out = []
    for parte in _TOKEN.split(texto):
        if not parte:
            continue
        b, i, t = bold, italic, parte
        if parte.startswith("***") and parte.endswith("***") and len(parte) > 6:
            b, i, t = True, True, parte[3:-3]
        elif parte.startswith("**") and parte.endswith("**") and len(parte) > 4:
            b, t = True, parte[2:-2]
        elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
            i, t = True, parte[1:-1]
        out.append(
            "<w:r>" + _rpr(b, i, underline, sz)
            + '<w:t xml:space="preserve">' + escape(t) + "</w:t></w:r>"
        )
    return "".join(out) or ("<w:r>" + _rpr(bold, italic, underline, sz) + "<w:t/></w:r>")


_BORDA = (
    "<w:pBdr>"
    + "".join(
        '<w:%s w:val="single" w:sz="6" w:space="4" w:color="000000"/>' % lado
        for lado in ("top", "left", "bottom", "right")
    )
    + "</w:pBdr>"
)


def _p(runs, *, bdr="", line=360, before=0, after=160, left=0, right=0,
       first=0, hanging=None, jc="both", rpr=""):
    ind = '<w:ind w:left="%d" w:right="%d"' % (left, right)
    if hanging is not None:
        ind += ' w:hanging="%d"' % hanging
    elif first:
        ind += ' w:firstLine="%d"' % first
    else:
        ind += ' w:hanging="0"'
    ind += "/>"
    ppr = (
        '<w:pPr><w:pStyle w:val="Normal"/>' + bdr
        + '<w:spacing w:lineRule="exact" w:line="%d" w:before="%d" w:after="%d"/>'
        % (line, before, after)
        + ind + '<w:jc w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>' % (jc, rpr)
    )
    return "<w:p>" + ppr + runs + "</w:p>"


# --------------------------------------------------------- tipos de parágrafo

def _topico(texto):                      # T — retângulo
    return _p(_runs(texto, bold=True), bdr=_BORDA, line=240, before=320,
              after=260, jc="center")


def _subtopico(texto):                   # S
    return _p(_runs(texto, bold=True, underline=True), before=200, after=120,
              left=1701, rpr='<w:u w:val="single"/>')


def _paragrafo(texto):                   # P
    return _p(_runs(texto), first=1701)


def _citacao(texto):                     # C
    return _p(_runs(texto, italic=True, sz=20), line=260, left=1701)


def _alinea(texto):                      # A
    return _p(_runs(texto), left=1701)


def _marcador(texto):                    # M
    corpo = texto.lstrip("–- ")
    return _p(_runs("– " + corpo), left=2041, hanging=340)


def _branco():                           # B
    return ('<w:p><w:pPr><w:pStyle w:val="Normal"/>'
            '<w:spacing w:before="0" w:after="200"/></w:pPr></w:p>')


# ---------------------------------------------------------------- montagem

def _corpo_xml(corpo):
    blocos, n = [], 0
    for tipo, *resto in corpo:
        texto = resto[0] if resto else ""
        tipo = tipo.upper()
        if tipo == "T":
            blocos.append(_topico(texto))
        elif tipo == "S":
            blocos.append(_subtopico(texto))
        elif tipo == "P":
            blocos.append(_paragrafo(texto))
        elif tipo == "C":
            blocos.append(_citacao(texto))
        elif tipo == "A":
            blocos.append(_alinea(texto))
        elif tipo == "M":
            blocos.append(_marcador(texto))
        elif tipo == "B":
            blocos.append(_branco())
        elif tipo == "Q":
            n += 1
            blocos.append(_p(_runs("QUESITO %d. " % n, bold=True) + _runs(texto)))
        else:
            raise ValueError("tipo de parágrafo desconhecido: %r" % tipo)
    return "".join(blocos), n


def montar(saida, *, corpo, autos, reclamante, tipo_peca, admissibilidade,
           vara=None, enderecamento=None,
           reclamada="EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS",
           rotulo_autor="RECLAMANTE", base=None):
    """Gera o .docx e devolve (caminho, nº de quesitos numerados).

    Informe `vara` ("5ª VARA DO TRABALHO DE CAMPO GRANDE/MS") para manter o
    endereçamento padrão do modelo, ou `enderecamento` com a linha inteira
    quando o juízo tiver designação própria (ex.: "JUIZ(A) FEDERAL DA 5ª VARA
    DO TRABALHO DE CAMPO GRANDE/MS"). Um dos dois é obrigatório.
    """
    if not saida.lower().endswith(".docx"):
        raise ValueError(
            "minuta é sempre entregue em .docx — saída recusada: %r" % saida)
    if not (vara or enderecamento):
        raise ValueError("informe `vara` ou `enderecamento`")
    base = base or os.path.normpath(BASE_PADRAO)
    zin = zipfile.ZipFile(base)
    doc = zin.read("word/document.xml").decode("utf-8")

    LINHA = ("EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DO TRABALHO "
             "DA [Nº]ª VARA DO TRABALHO DE CAMPO GRANDE/MS")
    if enderecamento:
        doc = doc.replace(LINHA, "EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) "
                          + enderecamento.strip().rstrip("."))
    else:
        doc = doc.replace("DA [Nº]ª VARA DO TRABALHO DE CAMPO GRANDE/MS", "DA " + vara)
    doc = doc.replace("[Nº DO PROCESSO]", autos)
    doc = doc.replace("[NOME DA RECLAMANTE]", reclamante)
    doc = doc.replace("RECLAMANTE:", rotulo_autor + ":")
    doc = doc.replace(
        "[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE — ex.: arts. 847 CLT c/c 336 CPC "
        "para contestação]", admissibilidade)
    doc = doc.replace("[TIPO DE PEÇA]", tipo_peca)
    if reclamada != "EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS":
        doc = doc.replace("RECLAMADA: EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS.",
                          "RECLAMADA: " + reclamada + ".")

    corpo_xml, n = _corpo_xml(corpo)
    paras = re.findall(r"<w:p[ >].*?</w:p>", doc, re.S)
    alvo = next(p for p in paras if "CORPO DA PE" in re.sub(r"<[^>]+>", "", p))
    doc = doc.replace(alvo, corpo_xml)

    resto = re.findall(r"\[[A-ZÀ-Ú][^\]]*\]", re.sub(r"<[^>]+>", "", doc))
    resto = [r for r in resto if "REVISAR" not in r]
    if resto:
        raise ValueError("placeholder do modelo não substituído: %s" % resto)

    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = doc.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    return saida, n
