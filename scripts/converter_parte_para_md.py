#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converte para Markdown os documentos de uma parte (adversa ou nao), localizados por padrao em
`F:\\Claude\\00 caso_atual\\<pasta da parte>` (se essa unidade nao existir, tenta `D:\\`).

Por que: evita que o Claude precise reler/reinterpretar PDF ou DOCX a cada mensagem (mais caro em
tokens e mais sujeito a erro de extracao inline) — o `.md` gerado uma vez fica pronto para leitura
direta em qualquer sessao futura. Alem de extrair o texto, o script tira o que so gasta token e nao
informa: cabecalho/rodape repetido em toda pagina, numero de pagina e "Fls. N" isolados, tarja de
assinatura eletronica e hash de validacao do PJe, hifenizacao de fim de linha e quebra de linha no
meio da frase. O conteudo juridico nao e resumido nem reescrito.

Uso tipico (a partir de qualquer diretorio):

    python scripts/converter_parte_para_md.py "NOME DA PARTE"

    # pasta base diferente do padrao
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --base "F:\\Claude\\00 caso_atual"

    # PDF digitalizado / foto de documento (exige Tesseract instalado)
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --ocr

    # forcar reconversao mesmo se o .md ja existir e estiver atualizado
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --force

    # depois de converter com sucesso, manda o original para a Lixeira do Windows
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --mover-para-lixeira

Comportamento:
- Busca (case/acento-insensivel) por subpastas de --base cujo nome contenha o termo informado. Se
  achar mais de uma, lista as opcoes e nao converte nada (evita converter a pasta errada).
- Para cada documento encontrado (recursivo dentro da pasta da parte), gera um `.md` irmao — mesmo
  nome, extensao `.md` —, so se o `.md` nao existir ou se o original for mais novo que ele (ou com
  --force). Cada pagina vira um marcador `[p.N]` no texto, para continuar sendo possivel citar a
  folha correta na peca.
- Formatos: `.pdf`, `.docx`, `.doc`, `.rtf`, `.odt`, `.xlsx`/`.xlsm`, `.csv`/`.tsv`, `.pptx`,
  `.html`, `.eml`, `.msg` e `.txt`. Imagem (`.jpg`, `.png`, `.tif`…) so entra com --ocr.
- Cada formato depende de uma biblioteca (`pip install -r scripts/requirements.txt`). O que faltar e
  listado no inicio da execucao e o lote segue com o que da para converter; `markitdown` e usado como
  ultimo recurso quando a biblioteca especifica nao esta instalada.
- Por padrao nunca apaga nem move o arquivo original. Com --mover-para-lixeira, todo original
  convertido com sucesso NESTA execucao e enviado a Lixeira do Windows (reversivel — nunca exclusao
  definitiva; requer confirmacao do usuario na sessao, nao e comportamento automatico por padrao).
  Original que falhou, que saiu sem texto algum (PDF digitalizado sem --ocr, `.doc` antigo) ou que
  ja estava atualizado nunca e movido.
- Nunca escreve fora da pasta da parte.
- Arquivo `.doc` antigo (binario do Word 97-2003) so converte no Windows com o Word instalado e
  `pip install pywin32`; sem isso, o script avisa e sugere salvar como `.docx`.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from shutil import rmtree

# ---------------------------------------------------------------------------
# Parametros gerais
# ---------------------------------------------------------------------------

# A pasta de trabalho migrou de D: para F:; tenta as duas, na ordem, e usa a primeira que existir.
BASES_PADRAO = (r"F:\Claude\00 caso_atual", r"D:\Claude\00 caso_atual")

EXTENSOES = {
    ".pdf",
    ".docx",
    ".doc",
    ".rtf",
    ".odt",
    ".xlsx",
    ".xlsm",
    ".csv",
    ".tsv",
    ".pptx",
    ".html",
    ".htm",
    ".eml",
    ".msg",
    ".txt",
}

# Imagem so entra em cena com --ocr: sem OCR o `.md` sairia vazio e ainda poluiria a pasta.
EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}

ARQUIVOS_IGNORADOS = {"thumbs.db", "desktop.ini", ".ds_store"}

# Estimativa de tokens por caractere em portugues, so para dimensionar o resumo da execucao;
# nao substitui a contagem real do tokenizador.
CARACTERES_POR_TOKEN = 3.6

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


def normalizar_texto(texto: str, *, reflow: bool = True) -> str:
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
    "markitdown": ("ultimo recurso, quando falta a lib do formato", "markitdown[pdf,docx]"),
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

def montar_markdown(
    relativo: Path, extracao: Extracao, opcoes: argparse.Namespace
) -> tuple[str, bool]:
    """Devolve o Markdown do documento e se ele saiu sem texto util."""
    paginas = list(extracao.paginas) if extracao.preservar else limpar_paginas(extracao.paginas)
    reflow = not (opcoes.sem_reflow or extracao.preservar)

    blocos: list[str] = []
    for indice, pagina in enumerate(paginas, start=1):
        texto = normalizar_texto(pagina, reflow=reflow)
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
# Execucao — achar a pasta da parte e converter o que esta dentro dela
# ---------------------------------------------------------------------------


def simplificar(txt: str) -> str:
    """Minusculas e sem acento, para comparacao tolerante de nomes de pasta."""
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return txt.lower().strip()


def base_padrao() -> str:
    for candidata in BASES_PADRAO:
        if Path(candidata).is_dir():
            return candidata
    return BASES_PADRAO[0]


def encontrar_pasta_parte(base: Path, nome_parte: str) -> Path:
    if not base.is_dir():
        sys.exit(f"[erro] pasta base não encontrada: {base}")

    alvo = simplificar(nome_parte)
    candidatas = [p for p in base.iterdir() if p.is_dir() and alvo in simplificar(p.name)]

    if not candidatas:
        existentes = ", ".join(p.name for p in base.iterdir() if p.is_dir()) or "(nenhuma)"
        sys.exit(
            f'[erro] nenhuma pasta em {base} corresponde a "{nome_parte}".\n'
            f"       Pastas existentes: {existentes}"
        )
    if len(candidatas) > 1:
        nomes = "\n  - ".join(p.name for p in candidatas)
        sys.exit(
            f'[erro] mais de uma pasta corresponde a "{nome_parte}" — seja mais específico:\n'
            f"  - {nomes}"
        )
    return candidatas[0]


def listar_documentos(pasta: Path, extensoes: set[str]) -> list[Path]:
    encontrados = []
    for caminho in sorted(pasta.rglob("*")):
        if not caminho.is_file():
            continue
        nome = caminho.name
        if nome.startswith(("~$", ".")) or nome.lower() in ARQUIVOS_IGNORADOS:
            continue
        if caminho.suffix.lower() in extensoes:
            encontrados.append(caminho)
    return encontrados


def mapear_destinos(arquivos: list[Path]) -> dict[Path, Path]:
    """`peticao.pdf` -> `peticao.md`. Quando dois originais disputam o mesmo nome (`x.pdf` e
    `x.docx` na mesma pasta), a extensao entra no nome (`x.pdf.md`) para nenhum sobrescrever o outro.
    """
    disputas = Counter((arquivo.parent, arquivo.stem.lower()) for arquivo in arquivos)
    destinos: dict[Path, Path] = {}
    for arquivo in arquivos:
        if disputas[(arquivo.parent, arquivo.stem.lower())] > 1:
            destinos[arquivo] = arquivo.with_name(arquivo.name + ".md")
        else:
            destinos[arquivo] = arquivo.with_suffix(".md")
    return destinos


def precisa_converter(origem: Path, destino: Path, force: bool) -> bool:
    if force or not destino.exists():
        return True
    return origem.stat().st_mtime > destino.stat().st_mtime


def extrair_documento(
    caminho: Path, mods: dict, opcoes: argparse.Namespace, pasta_tmp: Path
) -> Extracao:
    """Extrator especifico do formato; markitdown fica como ultimo recurso."""
    try:
        extracao = extrair(caminho, mods, opcoes, pasta_tmp)
    except Exception as erro:  # nunca aborta o lote por causa de um arquivo
        extracao = Extracao(observacao=f"falha na leitura: {type(erro).__name__}: {erro}")

    saiu_texto = any(pagina.strip() for pagina in extracao.paginas)
    if saiu_texto or caminho.suffix.lower() in EXTENSOES_IMAGEM:
        return extracao

    texto = extrair_com_markitdown(caminho, mods)
    if texto:
        return Extracao(paginas=[texto], observacao="extraido com markitdown")
    return extracao


def texto_util(texto: str) -> bool:
    """Filtra o que o ultimo recurso as vezes devolve em vez de falhar: a string "None" para
    `.doc` antigo, ou o proprio binario do arquivo vazando como texto. Um documento de processo
    com menos de 20 caracteres nao existe — e um `.md` desses mandaria o original para a Lixeira
    (com --mover-para-lixeira) sem que a informacao tivesse sido salva em lugar nenhum.
    """
    texto = texto.strip()
    if len(texto) < 20 or texto.lower() == "none":
        return False
    legiveis = sum(1 for c in texto if c.isprintable() or c in "\n\r\t")
    return legiveis / len(texto) >= 0.8


def extrair_com_markitdown(caminho: Path, mods: dict) -> str:
    markitdown = mods.get("markitdown")
    if markitdown is None:
        return ""
    try:
        resultado = markitdown.MarkItDown().convert(str(caminho))
        texto = (resultado.text_content or "").strip()
    except Exception:
        return ""
    return texto if texto_util(texto) else ""


def montar_argumentos(argv: list[str] | None = None) -> argparse.Namespace:
    padrao = base_padrao()
    analisador = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    analisador.add_argument(
        "nome_parte", help='nome (ou parte do nome) da pasta da parte, ex.: "NOME DA PARTE"'
    )
    analisador.add_argument(
        "--base",
        default=padrao,
        help=f"pasta que contém as pastas por parte (padrão: {padrao})",
    )
    analisador.add_argument(
        "--force", action="store_true", help="reconverte mesmo se o .md já estiver atualizado"
    )
    analisador.add_argument(
        "--mover-para-lixeira",
        action="store_true",
        help="envia à Lixeira do Windows (reversível) o original de cada arquivo convertido com "
        "sucesso nesta execução",
    )
    analisador.add_argument(
        "--ocr",
        action="store_true",
        help="tenta OCR nas páginas de PDF sem texto e nas imagens da pasta (exige Tesseract)",
    )
    analisador.add_argument(
        "--anonimizar", action="store_true", help="mascara CPF, CNPJ e número de processo no .md"
    )
    analisador.add_argument(
        "--sem-reflow",
        action="store_true",
        help="preserva as quebras de linha originais (mantém o layout, gasta mais token)",
    )
    analisador.add_argument(
        "--max-linhas-tabela",
        type=int,
        default=300,
        help="limite de linhas por tabela/planilha (padrão: 300)",
    )
    return analisador.parse_args(argv)


def avisar_dependencias(faltando: list[str]) -> None:
    if not faltando:
        return
    print("[aviso] bibliotecas ausentes — cada formato depende da sua:")
    for modulo, (uso, pacote) in DEPENDENCIAS.items():
        if pacote in faltando:
            print(f"          {pacote:<14} {uso}")
    print("        pip install -r scripts/requirements.txt (ou: pip install " + " ".join(sorted(set(faltando))) + ")\n")


def main(argv: list[str] | None = None) -> int:
    opcoes = montar_argumentos(argv)
    pasta_parte = encontrar_pasta_parte(Path(opcoes.base), opcoes.nome_parte)

    send2trash_func = None
    if opcoes.mover_para_lixeira:
        try:
            from send2trash import send2trash as send2trash_func  # noqa: N813
        except ImportError:
            sys.exit(
                "[erro] --mover-para-lixeira exige a lib 'send2trash' "
                "(pip install -r scripts/requirements.txt)"
            )

    mods, faltando = relatorio_dependencias()
    avisar_dependencias(faltando)

    extensoes = EXTENSOES | (EXTENSOES_IMAGEM if opcoes.ocr else set())
    arquivos = listar_documentos(pasta_parte, extensoes)
    if not arquivos:
        print(f"[aviso] nenhum documento suportado em {pasta_parte}")
        return 0

    destinos = mapear_destinos(arquivos)
    pasta_tmp = Path(tempfile.mkdtemp(prefix="converter_parte_"))
    convertidos, pulados, falhas, movidos, tokens = 0, 0, 0, 0, 0
    sem_texto_algum: list[tuple[Path, str]] = []

    try:
        for origem in arquivos:
            destino = destinos[origem]
            if not precisa_converter(origem, destino, opcoes.force):
                print(f"IGUAL  {origem.name} (já convertido e atualizado)")
                pulados += 1
                continue

            extracao = extrair_documento(origem, mods, opcoes, pasta_tmp)
            markdown, vazio = montar_markdown(
                origem.relative_to(pasta_parte), extracao, opcoes
            )
            destino.write_text(markdown, encoding="utf-8")

            if vazio:
                # `.md` fica gravado com a observacao do motivo, mas o original nunca vai
                # para a Lixeira: e justamente o caso em que so o original tem a informacao.
                print(f"VAZIO  {origem.name}: {extracao.observacao or 'nenhum texto extraído'}")
                sem_texto_algum.append((origem, extracao.observacao))
                falhas += 1
                continue

            paginas = f", {len(extracao.paginas)} pág." if len(extracao.paginas) > 1 else ""
            print(f"OK     {origem.name} -> {destino.name}{paginas}")
            convertidos += 1
            tokens += estimar_tokens(markdown)

            if send2trash_func is not None:
                try:
                    send2trash_func(str(origem))
                    print(f"LIXEIRA {origem.name}")
                    movidos += 1
                except Exception as exc:  # nao derruba o lote por falha ao mover
                    print(f"[aviso] não consegui mover {origem.name} para a Lixeira: {exc}")
    finally:
        rmtree(pasta_tmp, ignore_errors=True)

    print(f"\nPasta: {pasta_parte}")
    resumo = f"Convertidos: {convertidos} | Já atualizados: {pulados} | Sem texto: {falhas}"
    if opcoes.mover_para_lixeira:
        resumo += f" | Movidos p/ Lixeira: {movidos}"
    print(resumo)
    if convertidos:
        print(f"~{formatar_milhares(tokens)} tokens estimados no texto gerado nesta execução.")

    if sem_texto_algum:
        print("\nSem texto — leia o original ou converta de outro jeito:")
        for origem, observacao in sem_texto_algum:
            print(f"  - {origem.relative_to(pasta_parte)}: {observacao or 'nenhum texto extraído'}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
