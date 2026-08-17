#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte os documentos de uma pasta de caso em Markdown enxuto, para anexar ao Claude
gastando uma fracao dos tokens do arquivo original.

Uso tipico (Windows):

    python converter_documentos.py "F:\\Claude\\00 caso_atual\\Arionaldo Espinoza"

Gera, dentro de `<pasta>/_convertido`:

  * um `.md` por documento, com marcador de pagina `[p.N]` preservado (para citar fls.);
  * `_INDICE.md`  — indice com paginas, palavras e tokens estimados de cada documento;
  * `_CASO_COMPLETO.md` — todos os documentos concatenados, para anexar em um unico arquivo;
  * `_MANIFESTO.json` — controle interno; permite reexecutar so o que mudou.

O texto passa por uma limpeza que remove o que so gasta token e nao informa: cabecalho/rodape
repetido em toda pagina, numero de pagina isolado, tarja de assinatura eletronica do PJe, hash
de validacao, linha de separacao, espaco em excesso, e quebra de linha no meio da frase.

ATENCAO: a saida contem dados reais do processo (nome de parte, CPF, numero de autos). Nao
comite esses arquivos neste repositorio — ver a "Regra permanente" do README.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# Parametros gerais
# ---------------------------------------------------------------------------

# Suba este numero ao mudar a limpeza/formatacao: invalida o cache do manifesto e a proxima
# execucao reconverte tudo com as regras novas.
VERSAO_FORMATO = 1

NOME_PASTA_SAIDA = "_convertido"
NOME_INDICE = "_INDICE.md"
NOME_CONSOLIDADO = "_CASO_COMPLETO.md"
NOME_MANIFESTO = "_MANIFESTO.json"

# Estimativa de tokens por caractere em portugues. Serve para dimensionar o anexo,
# nao substitui a contagem real do tokenizador.
CARACTERES_POR_TOKEN = 3.6

EXTENSOES_SUPORTADAS = {
    ".pdf",
    ".docx",
    ".doc",
    ".rtf",
    ".odt",
    ".txt",
    ".md",
    ".csv",
    ".tsv",
    ".xlsx",
    ".xlsm",
    ".pptx",
    ".html",
    ".htm",
    ".eml",
    ".msg",
    ".json",
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
    ".bmp",
}

EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}

ARQUIVOS_IGNORADOS = {"thumbs.db", "desktop.ini", ".ds_store"}

# ---------------------------------------------------------------------------
# Limpeza de texto
# ---------------------------------------------------------------------------

# Linhas que so ocupam espaco em peca de processo eletronico.
PADROES_DESCARTE = [
    re.compile(r"^\s*$"),
    re.compile(r"^\s*p[aá]g(ina)?\.?\s*\d+\s*(de\s*\d+)?\s*$", re.I),
    re.compile(r"^\s*fls?\.?\s*\d+\s*$", re.I),
    re.compile(r"^\s*\d{1,4}\s*$"),
    re.compile(r"^\s*n[uú]mero do documento:\s*\S+\s*$", re.I),
    re.compile(r"^\s*(documento|peti[cç][aã]o)\s+assinad[oa]\s+(eletronicamente|digitalmente)\b", re.I),
    re.compile(r"^\s*assinado\s+(eletronicamente|digitalmente)\b", re.I),
    re.compile(r"^\s*conforme\s+(o\s+)?art\.?\s*1[oº]?,?\s*.{0,40}lei\s*n?[oº]?\s*11\.?419", re.I),
    re.compile(r"^\s*a\s+autenticidade\s+d[oe]st[ea]\s+documento\s+pode\s+ser", re.I),
    re.compile(r"^\s*https?://\S*(pje|eproc|esaj|projudi|validad|autenticid)\S*\s*$", re.I),
    re.compile(r"^\s*[0-9A-Fa-f]{16,}\s*$"),  # hash de validacao
    re.compile(r"^\s*[-_=.·*~]{4,}\s*$"),  # linha de separacao
]

RE_ESPACOS = re.compile(r"[ \t\u00a0\u200b]{2,}")
RE_HIFEN_QUEBRA = re.compile(r"([A-Za-zÀ-ÿ])-\n([a-zà-ÿ])")
RE_LINHAS_VAZIAS = re.compile(r"\n{3,}")
RE_FIM_DE_FRASE = re.compile(r"[.!?:;»”\"')\]]$")
RE_INICIO_ESTRUTURAL = re.compile(
    r"^(#|\||>|\[p\.\d+\]|[-*+]\s|\d+[.)]\s|[IVXLC]+[.)\-]\s|§|Art\.|CL[AÁ]USULA\b|[A-ZÀ-Ý]{5,}\b)"
)

RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
RE_CNPJ = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
RE_PROCESSO_CNJ = re.compile(r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b")


def descartar_linha(linha: str) -> bool:
    return any(padrao.match(linha) for padrao in PADROES_DESCARTE)


def limpar_paginas(paginas: list[str]) -> list[str]:
    """Remove cabecalho/rodape que se repete nas paginas e linhas de puro ruido."""
    linhas_por_pagina = [
        [linha.strip() for linha in pagina.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
        for pagina in paginas
    ]

    repetidas: set[str] = set()
    if len(linhas_por_pagina) >= 3:
        contagem: Counter[str] = Counter()
        for linhas in linhas_por_pagina:
            # Cabecalho/rodape: 4 primeiras e 4 ultimas linhas nao vazias da pagina.
            uteis = [linha for linha in linhas if linha]
            for linha in uteis[:4] + uteis[-4:]:
                if 3 <= len(linha) <= 140:
                    contagem[linha] += 1
        limite = max(3, int(0.6 * len(linhas_por_pagina)))
        repetidas = {linha for linha, vezes in contagem.items() if vezes >= limite}

    saida: list[str] = []
    for linhas in linhas_por_pagina:
        mantidas = [
            linha for linha in linhas if linha not in repetidas and not descartar_linha(linha)
        ]
        saida.append("\n".join(mantidas))
    return saida


def rejuntar_paragrafos(texto: str) -> str:
    """Junta linhas quebradas no meio da frase — cada quebra desnecessaria custa token."""
    resultado: list[str] = []
    for linha in texto.split("\n"):
        linha = linha.rstrip()
        anterior = resultado[-1] if resultado else ""
        pode_juntar = (
            linha
            and anterior
            and len(anterior) >= 45
            and not RE_FIM_DE_FRASE.search(anterior)
            and not anterior.startswith(("#", "|", "[p."))
            and not RE_INICIO_ESTRUTURAL.match(linha)
        )
        if pode_juntar:
            resultado[-1] = anterior + " " + linha.lstrip()
        else:
            resultado.append(linha)
    return "\n".join(resultado)


def normalizar(texto: str, *, reflow: bool = True) -> str:
    texto = texto.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", " ")
    texto = RE_HIFEN_QUEBRA.sub(r"\1\2", texto)
    texto = "\n".join(RE_ESPACOS.sub(" ", linha).rstrip() for linha in texto.split("\n"))
    if reflow:
        texto = rejuntar_paragrafos(texto)
    texto = RE_LINHAS_VAZIAS.sub("\n\n", texto)
    return texto.strip()


def anonimizar(texto: str) -> str:
    texto = RE_PROCESSO_CNJ.sub("[PROCESSO]", texto)
    texto = RE_CPF.sub("[CPF]", texto)
    texto = RE_CNPJ.sub("[CNPJ]", texto)
    return texto


def estimar_tokens(texto: str) -> int:
    return max(1, round(len(texto) / CARACTERES_POR_TOKEN))


def formatar_milhares(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Dependencias opcionais
# ---------------------------------------------------------------------------


def importar(nome: str):
    try:
        return __import__(nome)
    except Exception:  # ImportError, mas tambem falha de DLL no Windows
        return None


DEPENDENCIAS = {
    "pdfplumber": ("PDF (melhor extracao)", "pdfplumber"),
    "fitz": ("PDF (alternativa rapida) / render p/ OCR", "pymupdf"),
    "pypdf": ("PDF (ultimo recurso)", "pypdf"),
    "docx": (".docx", "python-docx"),
    "openpyxl": (".xlsx / .xlsm", "openpyxl"),
    "pptx": (".pptx", "python-pptx"),
    "striprtf": (".rtf", "striprtf"),
    "odf": (".odt", "odfpy"),
    "extract_msg": (".msg (Outlook)", "extract-msg"),
    "pytesseract": ("OCR de PDF digitalizado e imagem", "pytesseract"),
    "PIL": ("OCR (leitura da imagem)", "pillow"),
}


def relatorio_dependencias() -> tuple[dict[str, object], list[str]]:
    disponiveis: dict[str, object] = {}
    faltando: list[str] = []
    for modulo, (_uso, pacote) in DEPENDENCIAS.items():
        mod = importar(modulo)
        if mod is None:
            faltando.append(pacote)
        else:
            disponiveis[modulo] = mod
    return disponiveis, faltando


# ---------------------------------------------------------------------------
# Extratores — cada um devolve (lista de paginas, observacao)
# ---------------------------------------------------------------------------


@dataclass
class Extracao:
    paginas: list[str] = field(default_factory=list)
    observacao: str = ""
    ocr: bool = False
    # Texto que ja vem estruturado (.txt, .md, .json): nao filtra linha nem rejunta paragrafo,
    # senao quebra lista aninhada e indentacao de JSON.
    preservar: bool = False


def ocr_imagem(imagem, mods: dict) -> str:
    pytesseract = mods.get("pytesseract")
    if pytesseract is None:
        return ""
    try:
        return pytesseract.image_to_string(imagem, lang="por")
    except Exception:
        try:
            return pytesseract.image_to_string(imagem)
        except Exception:
            return ""


def ocr_pagina_pdf(caminho: Path, indice: int, mods: dict) -> str:
    """Renderiza uma pagina do PDF e passa no OCR. Exige pymupdf + pytesseract."""
    fitz = mods.get("fitz")
    if fitz is None:
        return ""
    try:
        from io import BytesIO

        from PIL import Image  # type: ignore

        with fitz.open(str(caminho)) as documento:
            pagina = documento[indice]
            pixmap = pagina.get_pixmap(dpi=300)
            imagem = Image.open(BytesIO(pixmap.tobytes("png")))
        return ocr_imagem(imagem, mods)
    except Exception:
        return ""


def extrair_pdf(caminho: Path, mods: dict, usar_ocr: bool) -> Extracao:
    paginas: list[str] = []
    motor = ""

    if "pdfplumber" in mods:
        motor = "pdfplumber"
        with mods["pdfplumber"].open(str(caminho)) as pdf:
            for pagina in pdf.pages:
                try:
                    paginas.append(pagina.extract_text() or "")
                except Exception:
                    paginas.append("")
    elif "fitz" in mods:
        motor = "pymupdf"
        with mods["fitz"].open(str(caminho)) as documento:
            for pagina in documento:
                paginas.append(pagina.get_text("text") or "")
    elif "pypdf" in mods:
        motor = "pypdf"
        leitor = mods["pypdf"].PdfReader(str(caminho))
        for pagina in leitor.pages:
            try:
                paginas.append(pagina.extract_text() or "")
            except Exception:
                paginas.append("")
    else:
        return Extracao(observacao="sem biblioteca de PDF (instale pdfplumber)")

    vazias = [i for i, texto in enumerate(paginas) if len(texto.strip()) < 80]
    houve_ocr = False
    if vazias and usar_ocr:
        for i in vazias:
            texto = ocr_pagina_pdf(caminho, i, mods)
            if texto.strip():
                paginas[i] = texto
                houve_ocr = True

    observacao = f"extraido com {motor}"
    restantes = [i for i, texto in enumerate(paginas) if len(texto.strip()) < 80]
    if restantes:
        amostra = ", ".join(str(i + 1) for i in restantes[:8])
        sufixo = "..." if len(restantes) > 8 else ""
        observacao += (
            f"; {len(restantes)} pagina(s) sem texto (p.{amostra}{sufixo})"
            f"{' — rode com --ocr' if not usar_ocr else ' — OCR nao resolveu'}"
        )
    if houve_ocr:
        observacao += "; parte via OCR"
    return Extracao(paginas=paginas, observacao=observacao, ocr=houve_ocr)


def tabela_markdown(linhas: list[list[str]], max_linhas: int) -> str:
    linhas = [
        [(celula or "").strip().replace("\n", " ").replace("|", "\\|") for celula in linha]
        for linha in linhas
    ]
    linhas = [linha for linha in linhas if any(linha)]
    if not linhas:
        return ""
    cortada = len(linhas) > max_linhas
    if cortada:
        linhas = linhas[:max_linhas]
    largura = max(len(linha) for linha in linhas)
    linhas = [linha + [""] * (largura - len(linha)) for linha in linhas]

    partes = ["| " + " | ".join(linhas[0]) + " |", "|" + "---|" * largura]
    for linha in linhas[1:]:
        partes.append("| " + " | ".join(linha) + " |")
    if cortada:
        partes.append(f"_(tabela truncada em {max_linhas} linhas)_")
    return "\n".join(partes)


def extrair_docx(caminho: Path, mods: dict, max_linhas: int) -> Extracao:
    docx = mods.get("docx")
    if docx is None:
        return Extracao(observacao="sem biblioteca (instale python-docx)")

    documento = docx.Document(str(caminho))
    corpo = documento.element.body
    mapa_paragrafos = {p._p: p for p in documento.paragraphs}
    mapa_tabelas = {t._tbl: t for t in documento.tables}

    partes: list[str] = []
    for elemento in corpo.iterchildren():
        if elemento in mapa_paragrafos:
            paragrafo = mapa_paragrafos[elemento]
            texto = (paragrafo.text or "").strip()
            if not texto:
                continue
            estilo = (paragrafo.style.name or "") if paragrafo.style is not None else ""
            nivel = re.search(r"(\d+)$", estilo)
            if estilo.lower().startswith(("heading", "titulo", "título")) and nivel:
                partes.append("#" * min(6, int(nivel.group(1)) + 1) + " " + texto)
            else:
                partes.append(texto)
        elif elemento in mapa_tabelas:
            tabela = mapa_tabelas[elemento]
            linhas = [[celula.text for celula in linha.cells] for linha in tabela.rows]
            markdown = tabela_markdown(linhas, max_linhas)
            if markdown:
                partes.append(markdown)

    return Extracao(paginas=["\n\n".join(partes)], observacao="paragrafos e tabelas")


def extrair_xlsx(caminho: Path, mods: dict, max_linhas: int) -> Extracao:
    openpyxl = mods.get("openpyxl")
    if openpyxl is None:
        return Extracao(observacao="sem biblioteca (instale openpyxl)")

    planilha = openpyxl.load_workbook(str(caminho), data_only=True, read_only=True)
    partes: list[str] = []
    try:
        for aba in planilha.worksheets:
            linhas: list[list[str]] = []
            for valores in aba.iter_rows(values_only=True):
                if valores is None:
                    continue
                celulas = ["" if v is None else str(v) for v in valores]
                if any(celula.strip() for celula in celulas):
                    linhas.append(celulas)
                if len(linhas) > max_linhas + 1:
                    break
            if not linhas:
                continue
            # Descarta colunas totalmente vazias.
            largura = max(len(linha) for linha in linhas)
            linhas = [linha + [""] * (largura - len(linha)) for linha in linhas]
            usadas = [c for c in range(largura) if any(linha[c].strip() for linha in linhas)]
            linhas = [[linha[c] for c in usadas] for linha in linhas]
            markdown = tabela_markdown(linhas, max_linhas)
            if markdown:
                partes.append(f"## Aba: {aba.title}\n\n{markdown}")
    finally:
        planilha.close()

    return Extracao(paginas=["\n\n".join(partes)], observacao=f"{len(partes)} aba(s) com dados")


def extrair_csv(caminho: Path, max_linhas: int) -> Extracao:
    texto = ler_texto(caminho)
    amostra = texto[:8192]
    try:
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t|")
        delimitador = dialeto.delimiter
    except Exception:
        delimitador = "\t" if caminho.suffix.lower() == ".tsv" else ";"
    linhas = list(csv.reader(texto.splitlines(), delimiter=delimitador))
    markdown = tabela_markdown(linhas, max_linhas)
    return Extracao(paginas=[markdown], observacao=f"delimitador {delimitador!r}")


def extrair_pptx(caminho: Path, mods: dict) -> Extracao:
    pptx = mods.get("pptx")
    if pptx is None:
        return Extracao(observacao="sem biblioteca (instale python-pptx)")

    apresentacao = pptx.Presentation(str(caminho))
    paginas: list[str] = []
    for slide in apresentacao.slides:
        textos = []
        for forma in slide.shapes:
            if getattr(forma, "has_text_frame", False):
                texto = (forma.text_frame.text or "").strip()
                if texto:
                    textos.append(texto)
        paginas.append("\n".join(textos))
    return Extracao(paginas=paginas, observacao=f"{len(paginas)} slide(s)")


class ExtratorHTML(HTMLParser):
    IGNORAR = {"script", "style", "head", "noscript"}
    BLOCO = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self._pular = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.IGNORAR:
            self._pular += 1
        elif tag in self.BLOCO:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in self.IGNORAR and self._pular:
            self._pular -= 1
        elif tag in self.BLOCO:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self._pular and data.strip():
            self.partes.append(data)

    def texto(self) -> str:
        return "".join(self.partes)


def extrair_html(caminho: Path) -> Extracao:
    parser = ExtratorHTML()
    parser.feed(ler_texto(caminho))
    return Extracao(paginas=[parser.texto()], observacao="tags removidas")


def extrair_eml(caminho: Path) -> Extracao:
    import email
    from email import policy

    with caminho.open("rb") as arquivo:
        mensagem = email.message_from_binary_file(arquivo, policy=policy.default)

    cabecalho = [
        f"**{rotulo}:** {mensagem.get(campo, '')}"
        for rotulo, campo in (("De", "From"), ("Para", "To"), ("Data", "Date"), ("Assunto", "Subject"))
        if mensagem.get(campo)
    ]
    corpo = ""
    try:
        parte = mensagem.get_body(preferencelist=("plain", "html"))
        if parte is not None:
            conteudo = parte.get_content()
            if parte.get_content_subtype() == "html":
                parser = ExtratorHTML()
                parser.feed(conteudo)
                conteudo = parser.texto()
            corpo = conteudo
    except Exception:
        corpo = ""

    anexos = [
        nome
        for parte in mensagem.walk()
        if (nome := parte.get_filename())
    ]
    rodape = f"\n\n_Anexos: {', '.join(anexos)}_" if anexos else ""
    return Extracao(paginas=["\n".join(cabecalho) + "\n\n" + corpo + rodape], observacao="e-mail")


def extrair_msg(caminho: Path, mods: dict) -> Extracao:
    extract_msg = mods.get("extract_msg")
    if extract_msg is None:
        return Extracao(observacao="sem biblioteca (instale extract-msg)")
    mensagem = extract_msg.Message(str(caminho))
    try:
        cabecalho = [
            f"**De:** {mensagem.sender or ''}",
            f"**Para:** {mensagem.to or ''}",
            f"**Data:** {mensagem.date or ''}",
            f"**Assunto:** {mensagem.subject or ''}",
        ]
        corpo = mensagem.body or ""
        anexos = [a.longFilename or a.shortFilename or "?" for a in mensagem.attachments]
    finally:
        mensagem.close()
    rodape = f"\n\n_Anexos: {', '.join(anexos)}_" if anexos else ""
    return Extracao(paginas=["\n".join(cabecalho) + "\n\n" + corpo + rodape], observacao="e-mail Outlook")


def extrair_rtf(caminho: Path, mods: dict) -> Extracao:
    striprtf = mods.get("striprtf")
    if striprtf is None:
        return Extracao(observacao="sem biblioteca (instale striprtf)")
    from striprtf.striprtf import rtf_to_text  # type: ignore

    return Extracao(paginas=[rtf_to_text(ler_texto(caminho), errors="ignore")], observacao="RTF")


def extrair_odt(caminho: Path, mods: dict) -> Extracao:
    if "odf" not in mods:
        return Extracao(observacao="sem biblioteca (instale odfpy)")
    from odf import teletype, text  # type: ignore
    from odf.opendocument import load  # type: ignore

    documento = load(str(caminho))
    paragrafos = [
        teletype.extractText(p) for p in documento.getElementsByType(text.P)
    ]
    return Extracao(paginas=["\n".join(paragrafos)], observacao="ODT")


def converter_com_word(caminho: Path, destino_tmp: Path) -> Path | None:
    """.doc antigo: pede ao Word instalado para salvar como .docx. So funciona no Windows."""
    if sys.platform != "win32":
        return None
    try:
        import pythoncom  # type: ignore
        import win32com.client  # type: ignore
    except Exception:
        return None

    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        documento = word.Documents.Open(str(caminho), ReadOnly=True)
        destino_tmp.parent.mkdir(parents=True, exist_ok=True)
        documento.SaveAs2(str(destino_tmp), FileFormat=16)  # 16 = wdFormatDocumentDefault (.docx)
        documento.Close(False)
        return destino_tmp
    except Exception:
        return None
    finally:
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def extrair_doc(caminho: Path, mods: dict, max_linhas: int, pasta_tmp: Path) -> Extracao:
    convertido = converter_com_word(caminho, pasta_tmp / (caminho.stem + ".docx"))
    if convertido is not None and convertido.exists():
        extracao = extrair_docx(convertido, mods, max_linhas)
        try:
            convertido.unlink()
        except OSError:
            pass
        extracao.observacao = "convertido via Word (.doc -> .docx)"
        return extracao
    return Extracao(
        observacao=".doc antigo: nao convertido — abra e salve como .docx, ou rode no Windows "
        "com Word instalado e `pip install pywin32`"
    )


def extrair_imagem(caminho: Path, mods: dict, usar_ocr: bool) -> Extracao:
    if not usar_ocr:
        return Extracao(observacao="imagem: rode com --ocr para extrair o texto")
    if "PIL" not in mods or "pytesseract" not in mods:
        return Extracao(observacao="imagem: instale pillow + pytesseract (e o Tesseract)")
    from PIL import Image  # type: ignore

    with Image.open(str(caminho)) as imagem:
        texto = ocr_imagem(imagem, mods)
    return Extracao(paginas=[texto], observacao="OCR de imagem", ocr=bool(texto.strip()))


def ler_texto(caminho: Path) -> str:
    dados = caminho.read_bytes()
    for codificacao in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return dados.decode(codificacao)
        except UnicodeDecodeError:
            continue
    return dados.decode("utf-8", errors="replace")


def extrair(caminho: Path, mods: dict, opcoes: argparse.Namespace, pasta_tmp: Path) -> Extracao:
    extensao = caminho.suffix.lower()
    if extensao == ".pdf":
        return extrair_pdf(caminho, mods, opcoes.ocr)
    if extensao == ".docx":
        return extrair_docx(caminho, mods, opcoes.max_linhas_tabela)
    if extensao == ".doc":
        return extrair_doc(caminho, mods, opcoes.max_linhas_tabela, pasta_tmp)
    if extensao == ".rtf":
        return extrair_rtf(caminho, mods)
    if extensao == ".odt":
        return extrair_odt(caminho, mods)
    if extensao in {".xlsx", ".xlsm"}:
        return extrair_xlsx(caminho, mods, opcoes.max_linhas_tabela)
    if extensao in {".csv", ".tsv"}:
        return extrair_csv(caminho, opcoes.max_linhas_tabela)
    if extensao == ".pptx":
        return extrair_pptx(caminho, mods)
    if extensao in {".html", ".htm"}:
        return extrair_html(caminho)
    if extensao == ".eml":
        return extrair_eml(caminho)
    if extensao == ".msg":
        return extrair_msg(caminho, mods)
    if extensao in {".txt", ".md", ".json"}:
        return Extracao(paginas=[ler_texto(caminho)], observacao="texto puro", preservar=True)
    if extensao in EXTENSOES_IMAGEM:
        return extrair_imagem(caminho, mods, opcoes.ocr)
    return Extracao(observacao=f"extensao {extensao} nao suportada")


# ---------------------------------------------------------------------------
# Montagem do Markdown
# ---------------------------------------------------------------------------

RE_NOME_SEGURO = re.compile(r"[^\w.\-]+", re.UNICODE)


def nome_de_saida(relativo: Path, usados: set[str]) -> str:
    base = RE_NOME_SEGURO.sub("_", relativo.with_suffix("").as_posix().replace("/", "__")).strip("_")
    base = base[:120] or "documento"
    candidato = f"{base}.md"
    contador = 2
    while candidato.lower() in usados:
        candidato = f"{base}-{contador}.md"
        contador += 1
    usados.add(candidato.lower())
    return candidato


def montar_markdown(
    relativo: Path, extracao: Extracao, opcoes: argparse.Namespace
) -> tuple[str, bool]:
    """Devolve o Markdown do documento e se ele saiu sem texto util."""
    paginas = list(extracao.paginas) if extracao.preservar else limpar_paginas(extracao.paginas)
    reflow = not (opcoes.sem_reflow or extracao.preservar)

    blocos: list[str] = []
    for indice, pagina in enumerate(paginas, start=1):
        texto = normalizar(pagina, reflow=reflow)
        if not texto:
            continue
        if len(paginas) > 1:
            blocos.append(f"[p.{indice}]\n{texto}")
        else:
            blocos.append(texto)

    corpo = "\n\n".join(blocos)
    if opcoes.anonimizar:
        corpo = anonimizar(corpo)

    detalhes = [f"origem: `{relativo.as_posix()}`"]
    if len(extracao.paginas) > 1:
        detalhes.append(f"{len(extracao.paginas)} pág.")
    if extracao.observacao:
        detalhes.append(extracao.observacao)

    # A linha em branco depois do bloco `>` e obrigatoria: sem ela o Markdown puxa
    # a primeira linha do texto para dentro da citacao.
    cabecalho = f"# {relativo.name}\n\n> {' · '.join(detalhes)}\n\n"
    vazio = not corpo
    return cabecalho + (corpo or "_(nenhum texto extraido)_") + "\n", vazio


# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------


def hash_arquivo(caminho: Path) -> str:
    digest = hashlib.sha1()
    with caminho.open("rb") as arquivo:
        for pedaco in iter(lambda: arquivo.read(1 << 20), b""):
            digest.update(pedaco)
    return digest.hexdigest()


def listar_documentos(pasta: Path, saida: Path) -> list[Path]:
    encontrados: list[Path] = []
    for caminho in sorted(pasta.rglob("*")):
        if not caminho.is_file():
            continue
        if saida in caminho.parents or caminho.parent == saida:
            continue
        nome = caminho.name
        if nome.startswith("~$") or nome.lower() in ARQUIVOS_IGNORADOS or nome.startswith("."):
            continue
        if caminho.suffix.lower() not in EXTENSOES_SUPORTADAS:
            continue
        encontrados.append(caminho)
    return encontrados


def carregar_manifesto(caminho: Path) -> dict:
    if not caminho.exists():
        return {}
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return dados.get("documentos", {}) if isinstance(dados, dict) else {}
    except Exception:
        return {}


def escrever_indice(saida: Path, registros: list[dict], pasta: Path) -> None:
    total_tokens = sum(r["tokens"] for r in registros)
    total_bytes = sum(r["bytes_origem"] for r in registros)
    com_problema = [r for r in registros if r.get("sem_texto")]
    megabytes = f"{total_bytes / 1_048_576:.1f}".replace(".", ",")

    linhas = [
        f"# Índice do caso — {pasta.name}",
        "",
        f"> {len(registros)} documento(s) · {formatar_milhares(total_tokens)} tokens estimados no "
        f"texto extraído · {megabytes} MB de originais",
        "",
        "Anexe o `.md` do documento que interessa — ou `_CASO_COMPLETO.md` para o caso inteiro.",
        "A contagem de tokens é estimada (≈1 token por 3,6 caracteres em português), serve para",
        "dimensionar o anexo.",
        "",
        "| Documento | Tipo | Pág. | Palavras | Tokens (est.) | Convertido em | Observação |",
        "|---|---|---|---|---|---|---|",
    ]
    for registro in sorted(registros, key=lambda r: r["origem"].lower()):
        linhas.append(
            "| {origem} | {tipo} | {paginas} | {palavras} | {tokens} | [{saida}]({saida}) | {obs} |".format(
                origem=registro["origem"].replace("|", "\\|"),
                tipo=registro["tipo"],
                paginas=registro["paginas"] or "—",
                palavras=formatar_milhares(registro["palavras"]),
                tokens=formatar_milhares(registro["tokens"]),
                saida=registro["saida"],
                obs=registro["observacao"].replace("|", "\\|") or "—",
            )
        )

    if com_problema:
        linhas += [
            "",
            "## Revisar manualmente",
            "",
            "Documentos de que saiu pouco ou nenhum texto — provavelmente digitalizados (rode com",
            "`--ocr`) ou em formato antigo:",
            "",
        ]
        linhas += [f"- `{r['origem']}` — {r['observacao'] or 'sem texto'}" for r in com_problema]

    linhas += ["", f"_Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}._", ""]
    (saida / NOME_INDICE).write_text("\n".join(linhas), encoding="utf-8")


def escrever_consolidado(saida: Path, registros: list[dict], pasta: Path) -> None:
    partes = [
        f"# Caso {pasta.name} — documentos consolidados",
        "",
        f"> {len(registros)} documento(s) · gerado em "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')} · índice detalhado em `{NOME_INDICE}`",
        "",
        "## Sumário",
        "",
    ]
    ordenados = sorted(registros, key=lambda r: r["origem"].lower())
    partes += [f"{i}. {r['origem']}" for i, r in enumerate(ordenados, start=1)]
    partes.append("")

    for indice, registro in enumerate(ordenados, start=1):
        conteudo = (saida / registro["saida"]).read_text(encoding="utf-8")
        # O titulo de nivel 1 de cada documento vira nivel 2 no consolidado.
        conteudo = re.sub(r"^# ", f"## {indice}. ", conteudo, count=1)
        partes += ["\n---\n", conteudo.rstrip(), ""]

    (saida / NOME_CONSOLIDADO).write_text("\n".join(partes) + "\n", encoding="utf-8")


def montar_argumentos(argv: list[str] | None = None) -> argparse.Namespace:
    analisador = argparse.ArgumentParser(
        description="Converte os documentos de uma pasta de caso em Markdown enxuto, "
        "para anexar ao Claude gastando menos tokens.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Exemplo: python converter_documentos.py "F:\\Claude\\00 caso_atual\\Cliente" --ocr',
    )
    analisador.add_argument("pasta", help="pasta do caso (varre subpastas)")
    analisador.add_argument(
        "-s", "--saida", help=f"pasta de saida (padrao: <pasta>/{NOME_PASTA_SAIDA})"
    )
    analisador.add_argument(
        "--forcar", action="store_true", help="reconverte tudo, ignorando o cache do manifesto"
    )
    analisador.add_argument(
        "--ocr", action="store_true", help="tenta OCR em PDF digitalizado e imagem (exige Tesseract)"
    )
    analisador.add_argument(
        "--anonimizar", action="store_true", help="mascara CPF, CNPJ e numero de processo na saida"
    )
    analisador.add_argument(
        "--sem-reflow",
        action="store_true",
        help="preserva as quebras de linha originais (gasta mais token, mantem o layout)",
    )
    analisador.add_argument(
        "--sem-consolidado", action="store_true", help=f"nao gera o {NOME_CONSOLIDADO}"
    )
    analisador.add_argument(
        "--max-linhas-tabela",
        type=int,
        default=300,
        help="limite de linhas por tabela/planilha (padrao: 300)",
    )
    analisador.add_argument("--silencioso", action="store_true", help="imprime menos")
    return analisador.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    opcoes = montar_argumentos(argv)
    pasta = Path(opcoes.pasta).expanduser()
    if not pasta.is_dir():
        print(f"ERRO: pasta nao encontrada: {pasta}", file=sys.stderr)
        return 2

    saida = Path(opcoes.saida).expanduser() if opcoes.saida else pasta / NOME_PASTA_SAIDA
    saida.mkdir(parents=True, exist_ok=True)
    pasta_tmp = saida / "_tmp"

    mods, faltando = relatorio_dependencias()
    if faltando and not opcoes.silencioso:
        print("Bibliotecas ausentes (cada formato depende da sua):")
        for modulo, (uso, pacote) in DEPENDENCIAS.items():
            if pacote in faltando:
                print(f"  - {pacote:<14} {uso}")
        print(f"\n  pip install {' '.join(sorted(set(faltando)))}\n")

    documentos = listar_documentos(pasta, saida)
    if not documentos:
        print(f"Nenhum documento suportado em {pasta}")
        return 1

    manifesto_antigo = {} if opcoes.forcar else carregar_manifesto(saida / NOME_MANIFESTO)
    manifesto_novo: dict[str, dict] = {}
    registros: list[dict] = []
    usados: set[str] = set()
    reaproveitados = 0

    for numero, caminho in enumerate(documentos, start=1):
        relativo = caminho.relative_to(pasta)
        chave = relativo.as_posix()
        assinatura = hash_arquivo(caminho)
        anterior = manifesto_antigo.get(chave)

        if (
            anterior
            and anterior.get("sha1") == assinatura
            and anterior.get("opcoes") == assinatura_das_opcoes(opcoes)
            and (saida / anterior.get("saida", "")).exists()
        ):
            usados.add(anterior["saida"].lower())
            registros.append(anterior["registro"])
            manifesto_novo[chave] = anterior
            reaproveitados += 1
            if not opcoes.silencioso:
                print(f"[{numero}/{len(documentos)}] = {chave} (sem alteracao)")
            continue

        if not opcoes.silencioso:
            print(f"[{numero}/{len(documentos)}] > {chave}", flush=True)

        try:
            extracao = extrair(caminho, mods, opcoes, pasta_tmp)
        except Exception as erro:  # nunca aborta o lote por causa de um arquivo
            extracao = Extracao(observacao=f"falha na leitura: {type(erro).__name__}: {erro}")

        markdown, sem_texto = montar_markdown(relativo, extracao, opcoes)
        nome = nome_de_saida(relativo, usados)
        (saida / nome).write_text(markdown, encoding="utf-8")

        registro = {
            "origem": chave,
            "saida": nome,
            "tipo": caminho.suffix.lower().lstrip(".") or "?",
            "paginas": len(extracao.paginas) if len(extracao.paginas) > 1 else 0,
            "palavras": len(markdown.split()),
            "tokens": estimar_tokens(markdown),
            "bytes_origem": caminho.stat().st_size,
            "observacao": extracao.observacao,
            "sem_texto": sem_texto,
        }
        registros.append(registro)
        manifesto_novo[chave] = {
            "sha1": assinatura,
            "saida": nome,
            "opcoes": assinatura_das_opcoes(opcoes),
            "registro": registro,
        }

    escrever_indice(saida, registros, pasta)
    if not opcoes.sem_consolidado:
        escrever_consolidado(saida, registros, pasta)

    (saida / NOME_MANIFESTO).write_text(
        json.dumps(
            {"gerado_em": datetime.now().isoformat(timespec="seconds"), "documentos": manifesto_novo},
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    if pasta_tmp.exists():
        try:
            pasta_tmp.rmdir()
        except OSError:
            pass

    total_tokens = sum(r["tokens"] for r in registros)
    falhas = sum(1 for r in registros if r.get("sem_texto"))
    print(
        f"\nOK: {len(registros)} documento(s) em {saida}"
        f" ({reaproveitados} reaproveitado(s) do cache)."
        f"\n  ~{formatar_milhares(total_tokens)} tokens estimados no texto extraido."
        f"\n  Indice: {saida / NOME_INDICE}"
    )
    if not opcoes.sem_consolidado:
        print(f"  Caso inteiro em um arquivo: {saida / NOME_CONSOLIDADO}")
    if falhas:
        print(
            f"  ATENCAO: {falhas} documento(s) sem texto util — ver 'Revisar manualmente' no indice."
        )
    print("\n  A saida contem dados do processo: nao comite no repositorio ASJUR.")
    return 0


def assinatura_das_opcoes(opcoes: argparse.Namespace) -> str:
    """Muda quando uma opcao afeta o conteudo gerado — invalida o cache do manifesto."""
    return "|".join(
        str(valor)
        for valor in (
            VERSAO_FORMATO,
            opcoes.ocr,
            opcoes.anonimizar,
            opcoes.sem_reflow,
            opcoes.max_linhas_tabela,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
