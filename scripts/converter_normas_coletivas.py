#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Converte os PDFs de normas coletivas para Markdown, com OCR quando necessário.

Os PDFs anteriores a 2011 são digitalizações sem camada de texto: para eles a extração
direta devolve zero caractere e a página precisa passar por OCR (Tesseract, idioma
português). Os mais recentes já têm texto embutido e são extraídos direto — muito mais
rápido e fiel.

Uso:
    python scripts/converter_normas_coletivas.py
    python scripts/converter_normas_coletivas.py --pasta "D:\outra\pasta" --forcar

Regravação: por padrão só converte PDF novo ou modificado depois do .md correspondente.
Pré-requisitos: ver scripts/requirements.txt (pypdfium2, pytesseract) + binário do
Tesseract instalado e o por.traineddata disponível (ver README de scripts).
"""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

PASTA_PADRAO = r"D:\ASJUR\Ações - Trabalhistas\Normas Coletivas"

# Caminhos do Tesseract. Podem ser sobrescritos por variável de ambiente.
TESSERACT_EXE = os.environ.get(
    "TESSERACT_EXE", r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
TESSDATA = os.environ.get("TESSDATA_PREFIX", str(Path.home() / "AppData/Local/tessdata"))

# Abaixo disto a página é tratada como digitalização e vai para o OCR.
MIN_CHARS_PAGINA = 80
DPI_PADRAO = 300


def _prepara_ocr() -> None:
    os.environ["TESSDATA_PREFIX"] = TESSDATA
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE


_doc_cache: dict[str, object] = {}


def _documento(caminho: str):
    """Mantém um handle de PDF por processo — abrir a cada página seria caro."""
    import pypdfium2 as pdfium

    if caminho not in _doc_cache:
        _doc_cache[caminho] = pdfium.PdfDocument(caminho)
    return _doc_cache[caminho]


def processa_pagina(tarefa: tuple[str, int, int]) -> tuple[int, str, str]:
    """Devolve (índice, texto, método) de uma página. Roda em processo separado."""
    caminho, indice, dpi = tarefa
    pagina = _documento(caminho)[indice]

    textpage = pagina.get_textpage()
    texto = textpage.get_text_range() or ""
    textpage.close()
    if len(texto.strip()) >= MIN_CHARS_PAGINA:
        return indice, texto.strip(), "texto"

    _prepara_ocr()
    import pytesseract

    imagem = pagina.render(scale=dpi / 72).to_pil().convert("L")
    texto_ocr = pytesseract.image_to_string(imagem, lang="por", config="--psm 6")
    return indice, texto_ocr.strip(), "ocr"


def converte_pdf(pdf: Path, destino: Path, dpi: int, jobs: int) -> tuple[int, int]:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf))
    total = len(doc)
    doc.close()

    tarefas = [(str(pdf), i, dpi) for i in range(total)]
    paginas: dict[int, tuple[str, str]] = {}

    with ProcessPoolExecutor(max_workers=jobs) as executor:
        for concluidas, (indice, texto, metodo) in enumerate(
            executor.map(processa_pagina, tarefas), start=1
        ):
            paginas[indice] = (texto, metodo)
            if concluidas % 25 == 0 or concluidas == total:
                print(f"      {concluidas}/{total} páginas", flush=True)

    n_ocr = sum(1 for _, metodo in paginas.values() if metodo == "ocr")

    partes = [
        f"# {pdf.stem}",
        "",
        f"> Origem: `{pdf.name}` — {total} páginas "
        f"({total - n_ocr} extraídas do texto do PDF, {n_ocr} por OCR).",
        "> Conversão automática; o PDF original continua sendo a fonte oficial.",
        "",
    ]
    for indice in range(total):
        texto, metodo = paginas[indice]
        marca = " (OCR)" if metodo == "ocr" else ""
        partes.append(f"<!-- página {indice + 1}{marca} -->")
        partes.append("")
        partes.append(texto if texto else "_[página sem texto reconhecível]_")
        partes.append("")

    destino.write_text("\n".join(partes), encoding="utf-8")
    return total, n_ocr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pasta", default=PASTA_PADRAO)
    parser.add_argument("--dpi", type=int, default=DPI_PADRAO)
    parser.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) - 1))
    parser.add_argument(
        "--forcar", action="store_true", help="reconverte mesmo se o .md estiver atual"
    )
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_dir():
        print(f"ERRO: pasta não encontrada: {pasta}", file=sys.stderr)
        return 1

    if not Path(TESSERACT_EXE).exists():
        print(f"ERRO: Tesseract não encontrado em {TESSERACT_EXE}", file=sys.stderr)
        return 1

    pdfs = sorted(pasta.glob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF em {pasta}")
        return 0

    print(f"{len(pdfs)} PDF(s) em {pasta} | {args.jobs} processos | {args.dpi} DPI\n")
    convertidos = pulados = 0

    for pdf in pdfs:
        destino = pdf.with_suffix(".md")
        if (
            not args.forcar
            and destino.exists()
            and destino.stat().st_mtime >= pdf.stat().st_mtime
        ):
            print(f"  [atual]  {pdf.name}")
            pulados += 1
            continue

        print(f"  [converte] {pdf.name}", flush=True)
        total, n_ocr = converte_pdf(pdf, destino, args.dpi, args.jobs)
        print(f"      -> {destino.name} ({total} páginas, {n_ocr} por OCR)\n", flush=True)
        convertidos += 1

    print(f"\nConcluído: {convertidos} convertido(s), {pulados} já atualizado(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
