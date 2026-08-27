# -*- coding: utf-8 -*-
"""Confere se uma peça .docx cumpre as três diretrizes permanentes do usuário.

    python3 conferir_peca.py "Quesitos - Perícia Médica - FULANO DE TAL.docx"

Sai com código 0 se estiver tudo certo, 1 se houver falha.
"""
import os
import re
import sys
import zipfile

BORDA = re.compile(r"<w:pBdr>.*?</w:pBdr>", re.S)
PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)


def _texto(p):
    return re.sub(r"<[^>]+>", "", p).strip()


def conferir(caminho):
    falhas, avisos = [], []
    base = os.path.basename(caminho)
    nome, ext = os.path.splitext(base)

    # --- diretriz 1: formato do arquivo ----------------------------------
    if ext.lower() != ".docx":
        falhas.append("minuta tem de ser .docx — extensão encontrada: %r" % ext)
        print("Arquivo : %s" % base)
        for f in falhas:
            print("FALHA : %s" % f)
        print("\nREPROVADA — %d falha(s)." % len(falhas))
        return 1

    # --- diretriz 2: nome do arquivo -------------------------------------
    if "_" in nome:
        falhas.append('nome do arquivo contém "_" — use espaço simples: %r' % base)
    if re.search(r"\S-\S", nome):
        falhas.append('nome do arquivo usa "-" sem espaços — use " - ": %r' % base)
    if " - " not in nome:
        avisos.append('nome sem " - " entre designações; confira se é peça de uma só '
                      "designação: %r" % base)
    else:
        parte = nome.rsplit(" - ", 1)[1].strip()
        if parte != parte.upper():
            falhas.append(
                "nome da parte deve estar em CAIXA ALTA: %r — use %r"
                % (parte, parte.upper()))

    # --- diretriz 3: formatação ------------------------------------------
    z = zipfile.ZipFile(caminho)
    nomes = z.namelist()
    doc = z.read("word/document.xml").decode("utf-8")

    n_bordas = len(BORDA.findall(doc))
    if n_bordas == 0:
        falhas.append("nenhum tópico em retângulo (w:pBdr) — todo tópico principal "
                      "deve estar dentro de uma caixa")

    for exigido, rotulo in [("word/header1.xml", "cabeçalho"),
                            ("word/footer1.xml", "rodapé"),
                            ("word/media/image1.png", "logotipo")]:
        if exigido not in nomes:
            falhas.append("%s ausente (%s) — a peça não foi gerada a partir de "
                          "_FORMATO_BASE.docx" % (rotulo, exigido))

    m = re.search(r'<w:pgMar[^>]*/>', doc)
    if m and 'w:left="1701"' not in m.group(0):
        falhas.append("margens fora do padrão: %s" % m.group(0))

    texto = re.sub(r"<[^>]+>", " ", doc)
    if "Marcos Hideki Kamibayashi" not in texto:
        falhas.append("bloco de assinatura ausente")

    pendentes = [p for p in re.findall(r"\[[^\]\n]{2,60}\]", texto)
                 if "REVISAR" not in p]
    if pendentes:
        falhas.append("placeholder não substituído: %s" % ", ".join(sorted(set(pendentes))))

    revisar = sorted({p for p in re.findall(r"\[[^\]\n]{2,60}\]", texto) if "REVISAR" in p})
    if revisar:
        avisos.append("campos deixados para o usuário preencher: %s" % ", ".join(revisar))

    # --- relatório --------------------------------------------------------
    print("Arquivo : %s" % base)
    print("Tópicos em retângulo : %d" % n_bordas)
    print("Parágrafos : %d" % len(PARA.findall(doc)))
    for t in [_texto(p) for p in PARA.findall(doc) if "<w:pBdr>" in p]:
        print("   ▭ %s" % t)
    for a in avisos:
        print("AVISO : %s" % a)
    for f in falhas:
        print("FALHA : %s" % f)
    print("\n%s" % ("OK — peça no padrão." if not falhas
                    else "REPROVADA — %d falha(s)." % len(falhas)))
    return 0 if not falhas else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(conferir(sys.argv[1]))
