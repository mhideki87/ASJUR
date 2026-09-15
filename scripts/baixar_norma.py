#!/usr/bin/env python3
"""Baixa o texto de uma norma em fonte oficial e devolve texto limpo.

Por que existe
--------------
Liberados os domínios oficiais no ambiente cloud/web (ver a seção "Conferência de
texto legal" do `CLAUDE.md`), o túnel abre — mas o acesso ainda esbarra em três
obstáculos que nada têm a ver com a lista de domínios, e que toda sessão nova
redescobriria do zero:

1. **Cliente recusado.** Planalto e `in.gov.br` fecham a conexão para quem não se
   apresenta como navegador. O sintoma engana: `Empty reply from server` e
   `PROTOCOL_ERROR`, ambos com código HTTP `000`, que parecem bloqueio de rede.
2. **Cadeia de certificado incompleta.** O STF envia só o certificado final, sem o
   intermediário. O `curl` recusa com `unable to get local issuer certificate`. O elo
   que falta está publicado pela própria autoridade certificadora, no endereço que o
   certificado indica (extensão AIA), e a raiz já está no sistema — então dá para
   completar a cadeia **sem desligar a verificação**, que é o que este script faz.
3. **Página gigante.** O decreto-lei da CLT tem 3,5 MB de HTML e a Constituição, 1,8 MB.
   Ler o arquivo bruto estoura contexto à toa.

Uso
---
    python scripts/baixar_norma.py <url> [--artigo "Art. 62"] [--contexto 650]
    python scripts/baixar_norma.py <url> --saida norma.txt
    python scripts/baixar_norma.py <url> --bruto        # guarda o HTML original

Sem `--artigo`, imprime o texto inteiro já limpo. Com `--artigo`, imprime só os trechos
que começam naquela expressão, com `--contexto` caracteres de cada ocorrência.

Armadilha do Planalto
---------------------
A página de uma lei antiga traz a redação original **e** todas as sucessivas, empilhadas.
Buscar pelo número do artigo devolve a redação de 1943. Por isso `--artigo` imprime
**todas** as ocorrências, numeradas, em vez da primeira: cabe a quem lê escolher a que
vem acompanhada da nota `(Redação dada pela Lei nº ...)` mais recente.

Só stdlib e `curl`/`openssl`, que existem no ambiente cloud/web.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

NAVEGADOR = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

# Erro de TLS que indica cadeia incompleta — é remediável buscando o intermediário.
FALTA_INTERMEDIARIO = "unable to get local issuer certificate"


def _curl(url: str, destino: Path, cacert: Path | None = None) -> tuple[int, str]:
    """Roda o curl com a receita que funciona. Devolve (código HTTP, stderr)."""
    cmd = [
        "curl", "-sSL", "--http1.1",
        "-A", NAVEGADOR,
        "-o", str(destino),
        "-w", "%{http_code}",
        "--max-time", "90",
        url,
    ]
    if cacert is not None:
        cmd[1:1] = ["--cacert", str(cacert)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    codigo = p.stdout.strip() or "000"
    return (int(codigo) if codigo.isdigit() else 0), p.stderr


def _remendar_cadeia(url: str, trabalho: Path) -> Path | None:
    """Busca o certificado intermediário que o servidor deixou de enviar.

    O endereço vem da extensão AIA do próprio certificado apresentado, então não há
    nada adivinhado aqui: é a autoridade certificadora dizendo onde está o elo. A
    verificação continua ativa — só se completa a corrente até a raiz já confiável.
    """
    host = re.sub(r"^https?://", "", url).split("/")[0]
    proxy = ""
    import os
    if os.environ.get("HTTPS_PROXY"):
        proxy = os.environ["HTTPS_PROXY"].replace("http://", "")

    cmd = ["openssl", "s_client", "-connect", f"{host}:443", "-servername", host]
    if proxy:
        cmd += ["-proxy", proxy]
    p = subprocess.run(cmd, input="", capture_output=True, text=True, timeout=60)
    pem = re.search(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
                    p.stdout, re.S)
    if not pem:
        return None

    folha = trabalho / "folha.pem"
    folha.write_text(pem.group(0))
    texto = subprocess.run(
        ["openssl", "x509", "-in", str(folha), "-noout", "-text"],
        capture_output=True, text=True).stdout
    aia = re.search(r"CA Issuers - URI:(\S+)", texto)
    if not aia:
        return None

    bruto = trabalho / "inter.crt"
    codigo, _ = _curl(aia.group(1), bruto)
    if codigo != 200 or not bruto.exists() or bruto.stat().st_size == 0:
        print(f"  [!] o intermediário está em {aia.group(1)} e o download devolveu "
              f"{codigo} — acrescente esse domínio à lista do ambiente",
              file=sys.stderr)
        return None

    inter = trabalho / "inter.pem"
    # O arquivo pode vir em DER (binário) ou já em PEM.
    for forma in ("DER", "PEM"):
        r = subprocess.run(
            ["openssl", "x509", "-inform", forma, "-in", str(bruto), "-out", str(inter)],
            capture_output=True)
        if r.returncode == 0:
            break
    else:
        return None

    bundle = trabalho / "bundle.pem"
    base = Path("/root/.ccr/ca-bundle.crt")
    partes = [base.read_text()] if base.exists() else []
    partes.append(inter.read_text())
    bundle.write_text("\n".join(partes))
    return bundle


def baixar(url: str, trabalho: Path) -> str:
    """Devolve o HTML da norma, remendando a cadeia de certificado se preciso."""
    destino = trabalho / "pagina.html"
    codigo, erro = _curl(url, destino)

    if FALTA_INTERMEDIARIO in erro:
        print("  [i] servidor enviou cadeia incompleta; buscando o intermediário",
              file=sys.stderr)
        bundle = _remendar_cadeia(url, trabalho)
        if bundle is None:
            raise SystemExit("Não foi possível completar a cadeia de certificado. "
                             "Nunca contorne isso desligando a verificação.")
        codigo, erro = _curl(url, destino, cacert=bundle)

    if codigo != 200:
        detalhe = erro.strip().splitlines()[-1] if erro.strip() else ""
        raise SystemExit(
            f"HTTP {codigo} em {url}\n{detalhe}\n\n"
            "Códigos que aparecem muito:\n"
            "  403 no CONNECT → domínio fora da lista do ambiente\n"
            "  502 no CONNECT → host não existe ou está fora do ar\n"
            "  202 com corpo vazio → desafio anti-robô (AWS WAF); não há contorno aqui"
        )
    return _decodificar(destino.read_bytes())


def _decodificar(dados: bytes) -> str:
    """Descobre a codificação da página antes de virar texto.

    Não é detalhe: o Planalto serve latin-1 e o STF, UTF-8. Fixar uma das duas faz a
    outra sair como `SÃºmula` — e uma busca por "Súmula Vinculante 9" simplesmente não
    encontra nada, dando a falsa impressão de que a página não tem o verbete.
    """
    # A declaração da própria página manda; ela aparece em ASCII puro no topo.
    cabeca = dados[:4096].decode("ascii", errors="ignore").lower()
    m = re.search(r'charset=["\']?\s*([\w-]+)', cabeca)
    candidatos = []
    if m:
        candidatos.append(m.group(1))
    candidatos += ["utf-8", "cp1252", "latin-1"]

    for cod in candidatos:
        try:
            return dados.decode(cod)
        except (UnicodeDecodeError, LookupError):
            continue
    return dados.decode("latin-1", errors="replace")


def limpar(bruto: str) -> str:
    """Tira marcação e normaliza espaço, sem resumir nem reescrever o conteúdo."""
    texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", bruto, flags=re.S | re.I)
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)
    texto = texto.replace("​", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", texto).strip()


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Baixa norma em fonte oficial e devolve texto limpo.")
    ap.add_argument("url")
    ap.add_argument("--artigo", help='Trecho inicial, ex.: "Art. 62"')
    ap.add_argument("--contexto", type=int, default=650,
                    help="Caracteres após o trecho (padrão: 650)")
    ap.add_argument("--saida", type=Path, help="Grava em arquivo em vez da tela")
    ap.add_argument("--bruto", type=Path, help="Guarda também o HTML original")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        trabalho = Path(tmp)
        bruto = baixar(args.url, trabalho)

    if args.bruto:
        args.bruto.write_text(bruto, encoding="utf-8", errors="replace")

    texto = limpar(bruto)

    if args.artigo:
        # "Art. 62" não pode casar com "Art. 620": se a busca termina em dígito,
        # exige que o próximo caractere não seja dígito.
        alvo = re.escape(args.artigo)
        if args.artigo and args.artigo[-1].isdigit():
            alvo += r"(?![\d])"
        achados = [m.group(0) for m in
                   re.finditer(alvo + r".{0," + str(args.contexto) + r"}", texto)]
        if not achados:
            raise SystemExit(f'Nada encontrado para "{args.artigo}".')
        partes = []
        for i, t in enumerate(achados, 1):
            partes.append(f"--- ocorrência {i} de {len(achados)} ---\n{t}")
        if len(achados) > 1:
            partes.append(
                "\n[!] Mais de uma ocorrência: a página provavelmente empilha a redação\n"
                "    original e as sucessivas. Vale a que traz a nota\n"
                '    "(Redação dada pela Lei nº ...)" mais recente.')
        texto = "\n\n".join(partes)

    if args.saida:
        args.saida.write_text(texto, encoding="utf-8")
        print(f"gravado em {args.saida} ({len(texto)} caracteres)")
    else:
        print(texto)


if __name__ == "__main__":
    main()
