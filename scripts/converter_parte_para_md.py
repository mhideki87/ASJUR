#!/usr/bin/env python3
"""
Converte para Markdown os arquivos PDF/DOC/DOCX de uma parte (adversa ou não),
localizados por padrão em D:\\Claude\\00 caso_atual\\<pasta da parte>.

Por quê: evita que o Claude precise reler/reinterpretar PDF ou DOCX a cada
mensagem (mais caro em tokens e mais sujeito a erro de extração inline) — o
.md gerado uma vez fica pronto para leitura direta em qualquer sessão futura.

Uso típico (a partir de qualquer diretório):

    python scripts/converter_parte_para_md.py "NOME DA PARTE"

    # pasta base diferente do padrão
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --base "D:\\Claude\\00 caso_atual"

    # forçar reconversão mesmo se o .md já existir e estiver atualizado
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --force

    # depois de converter com sucesso, manda o original (PDF/DOC/DOCX) para a Lixeira do Windows
    python scripts/converter_parte_para_md.py "NOME DA PARTE" --mover-para-lixeira

Comportamento:
- Busca (case/acento-insensível) por subpastas de --base cujo nome contenha o
  termo informado. Se achar mais de uma, lista as opções e não converte nada
  (evita converter a pasta errada).
- Para cada .pdf/.doc/.docx encontrado (recursivo dentro da pasta da parte),
  gera um .md irmão (mesmo nome, extensão .md), só se o .md não existir ou se
  o original for mais novo que o .md (ou com --force).
- Por padrão nunca apaga nem move o arquivo original. Com --mover-para-lixeira,
  todo original convertido com sucesso NESTA execução é enviado à Lixeira do
  Windows (reversível — nunca exclusão definitiva; requer confirmação do
  usuário na sessão, não é comportamento automático por padrão). Original que
  falhou a conversão, ou que já estava atualizado (pulado), nunca é movido.
- Nunca escreve fora da pasta da parte.
- Arquivos .doc antigos (formato binário do Word 97-2003) frequentemente não
  são suportados pela biblioteca de conversão; nesse caso o script avisa e
  sugere salvar como .docx ou .pdf antes de tentar de novo.
"""

import argparse
import sys
import unicodedata
from pathlib import Path

DEFAULT_BASE = r"D:\Claude\00 caso_atual"
EXTENSOES = {".pdf", ".doc", ".docx"}


def normalizar(txt: str) -> str:
    """minúsculas e sem acento, para comparação tolerante de nomes."""
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return txt.lower().strip()


def encontrar_pasta_parte(base: Path, nome_parte: str) -> Path:
    if not base.is_dir():
        sys.exit(f"[erro] pasta base não encontrada: {base}")

    alvo = normalizar(nome_parte)
    candidatas = [
        p for p in base.iterdir() if p.is_dir() and alvo in normalizar(p.name)
    ]

    if not candidatas:
        sys.exit(
            f"[erro] nenhuma pasta em {base} corresponde a \"{nome_parte}\".\n"
            f"       Pastas existentes: {', '.join(p.name for p in base.iterdir() if p.is_dir()) or '(nenhuma)'}"
        )
    if len(candidatas) > 1:
        nomes = "\n  - ".join(p.name for p in candidatas)
        sys.exit(
            f"[erro] mais de uma pasta corresponde a \"{nome_parte}\" — seja mais específico:\n  - {nomes}"
        )
    return candidatas[0]


def precisa_converter(origem: Path, destino: Path, force: bool) -> bool:
    if force:
        return True
    if not destino.exists():
        return True
    return origem.stat().st_mtime > destino.stat().st_mtime


def converter_arquivo(md_engine, origem: Path, destino: Path) -> tuple[bool, str]:
    try:
        resultado = md_engine.convert(str(origem))
        destino.write_text(resultado.text_content, encoding="utf-8")
        return True, f"OK   {origem.name} -> {destino.name}"
    except Exception as exc:  # noqa: BLE001 — reportar qualquer falha de conversão, sem derrubar o lote
        dica = ""
        if origem.suffix.lower() == ".doc":
            dica = " (dica: .doc antigo do Word costuma falhar; salve como .docx ou .pdf e rode de novo)"
        return False, f"FALHOU {origem.name}: {exc}{dica}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("nome_parte", help="nome (ou parte do nome) da pasta da parte, ex.: \"NOME DA PARTE\"")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"pasta que contém as pastas por parte (padrão: {DEFAULT_BASE})")
    parser.add_argument("--force", action="store_true", help="reconverte mesmo se o .md já existir e estiver atualizado")
    parser.add_argument(
        "--mover-para-lixeira",
        action="store_true",
        help="envia à Lixeira do Windows (reversível) o original de cada arquivo convertido com sucesso nesta execução",
    )
    args = parser.parse_args()

    base = Path(args.base)
    pasta_parte = encontrar_pasta_parte(base, args.nome_parte)

    arquivos = sorted(
        p for p in pasta_parte.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSOES
    )
    if not arquivos:
        print(f"[aviso] nenhum PDF/DOC/DOCX encontrado em {pasta_parte}")
        return

    from markitdown import MarkItDown  # import tardio: falha rápido e claro se a lib não estiver instalada

    send2trash_func = None
    if args.mover_para_lixeira:
        try:
            from send2trash import send2trash as send2trash_func  # noqa: N813
        except ImportError:
            sys.exit(
                "[erro] --mover-para-lixeira exige a lib 'send2trash' (pip install -r scripts/requirements.txt)"
            )

    md_engine = MarkItDown()

    convertidos, pulados, falhas, movidos = 0, 0, 0, 0
    for origem in arquivos:
        destino = origem.with_suffix(".md")
        if not precisa_converter(origem, destino, args.force):
            print(f"IGUAL {origem.name} (já convertido e atualizado)")
            pulados += 1
            continue
        ok, msg = converter_arquivo(md_engine, origem, destino)
        print(msg)
        if not ok:
            falhas += 1
            continue
        convertidos += 1
        if send2trash_func is not None:
            try:
                send2trash_func(str(origem))
                print(f"LIXEIRA {origem.name}")
                movidos += 1
            except Exception as exc:  # noqa: BLE001 — não derruba o lote por falha ao mover
                print(f"[aviso] não consegui mover {origem.name} para a Lixeira: {exc}")

    print(f"\nPasta: {pasta_parte}")
    resumo = f"Convertidos: {convertidos} | Já atualizados: {pulados} | Falhas: {falhas}"
    if args.mover_para_lixeira:
        resumo += f" | Movidos p/ Lixeira: {movidos}"
    print(resumo)
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
