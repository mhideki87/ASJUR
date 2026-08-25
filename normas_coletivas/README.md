# Normas coletivas — ECT (1988 – 2026)

Íntegra dos instrumentos coletivos da ECT convertida para Markdown, para consulta pelo Claude a
partir de qualquer ambiente (Claude Code local, cloud/web ou Project do claude.ai).

## O que há aqui

Um `.md` por PDF de origem, mantendo a numeração da pasta local
`D:\ASJUR\Ações - Trabalhistas\Normas Coletivas`. Cada arquivo preserva a divisão de páginas do
original em comentários `<!-- página N -->`, para citação precisa.

| Arquivos | Conteúdo | Origem do texto |
|---|---|---|
| `02` a `20` | Acordos coletivos de 1988/89 a 2009/2011 | **OCR** — os PDFs são digitalizações sem camada de texto |
| `21` | Acórdãos TST dos dissídios 2011/12 e 2012/13 | texto do PDF |
| `22` a `24` | Normas coletivas 2013–2026 (ACTs, dissídios TST, decisões do STF) | texto do PDF, com OCR nas páginas digitalizadas |

## Ressalvas de uso

- Os arquivos `02` a `20` vêm de OCR (Tesseract 5.4, português, 300 DPI) de digitalizações antigas,
  algumas datilografadas. O texto é legível e as cláusulas são identificáveis, mas **há ruído**:
  carimbos, marginálias e rubricas viram caracteres soltos, e a quebra de linha do original é
  preservada (palavras partidas no fim da linha).
- **O PDF original continua sendo a fonte oficial.** Antes de transcrever uma cláusula em peça
  processual, confira o trecho no PDF correspondente pela página indicada.
- O arquivo `23` está integralmente contido nas primeiras 117 páginas do `24` — é duplicata parcial,
  mantida por fidelidade à pasta de origem.

## Como foi gerado

`python scripts/converter_normas_coletivas.py` (na raiz do repositório). Reconverte só o que mudou.

## Um arquivo por norma (só local)

`python scripts/separar_normas_coletivas.py` recorta esses mesmos `.md` em **um arquivo por
instrumento** — `1988-1989 — ACT.md`, `2016-2017 — ACT.md`, `2019-2020 — Sentença Normativa
(TST DC 1000662-58.2019).md` etc. — na subpasta local `Por norma/`. Arquivo já existente é
mantido, nunca sobrescrito; rodar de novo não duplica nada.

Essa subpasta **não é versionada**: no repositório fica a íntegra por volume de origem, que é a
forma fiel ao PDF. Os cortes ficam na tabela `MAPA` do script, com a faixa de páginas de cada
norma — é lá que se corrige uma fronteira ou se acrescenta um PDF novo (`--detectar` ajuda a
localizar os inícios; `--listar` mostra o plano antes de gravar).

## Sobre a "Regra permanente" do repositório

A regra do [README raiz](../README.md) veda dado que identifique **parte de processo do escritório**.
Os documentos desta pasta são instrumentos normativos e decisões públicas (ACTs registrados, dissídios
coletivos do TST, decisões do STF), que valem para toda a categoria — não são autos de cliente. Os
números de processo aqui são dos dissídios coletivos, públicos por natureza.
