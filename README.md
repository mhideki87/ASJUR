# ASJUR — Assessoria Jurídica

Base de conhecimento jurídico da assessoria (ECT), construída por demanda: cresce a cada sessão real de
minuta, não por processamento em massa das petições antigas.

## Estrutura

| Arquivo/pasta | Conteúdo |
|---|---|
| [base_conhecimento_juridico_ECT.md](base_conhecimento_juridico_ECT.md) | Teses recorrentes — contencioso **trabalhista** (validada, uso real) |
| [base_conhecimento_juridico_CIVEL.md](base_conhecimento_juridico_CIVEL.md) | Teses recorrentes — contencioso **cível** (rascunho, itens `[REVISAR]` pendentes de validação) |
| [modelos/](modelos/README.md) | `_FORMATO_BASE.docx` (formatação de qualquer peça) + esqueleto estrutural por tipo + tema — para não precisar reanexar peça-modelo antiga |
| [playbook_prompts_ECT.md](playbook_prompts_ECT.md) | Prompts de uso diário + protocolo de atualização da base |
| [CLAUDE.md](CLAUDE.md) | Instruções para sessões de **Claude Code** (local e cloud): conversão automática dos documentos da parte (PDF/DOC) para `.md` + título da sessão com o nome do Reclamante |
| [scripts/converter_parte_para_md.py](scripts/converter_parte_para_md.py) | Script usado por essa automação — não roda no Project do claude.ai, só localmente |

## Como usar (resumo)

1. Crie um Projeto no claude.ai e conecte este repositório via GitHub connector — os `.md` viram
   Project knowledge, buscados sob demanda.
2. No dia a dia: anexe os documentos do processo (inicial, sentença, laudos etc.). Peça-modelo antiga só
   é necessária se ainda não existir modelo salvo para aquele tipo de peça + tema (ver seção 6.1 do playbook).
3. Ao final de cada sessão em que algo foi minutado, rode o protocolo da seção 6.2 do playbook — o Claude
   aponta tese nova, correção, jurisprudência nova e atualização de modelo, em formato de diff para você
   revisar e commitar.

## Regra permanente

Nenhum arquivo aqui deve conter nome de cliente, número de processo, CPF ou qualquer dado que identifique
uma parte real. Teses e modelos são generalizados; se precisar citar norma ou jurisprudência, cite a fonte
exata — nunca invente.

## Automação local (Claude Code): conversão de PDF/DOC para .md

Os documentos reais de cada processo (inicial, sentença, laudos etc.) ficam **fora deste repositório**, em
`D:\Claude\00 caso_atual\<nome da parte>`. Numa sessão de Claude Code, assim que o nome da parte adversa é
informado ou identificado num documento, o Claude roda `scripts/converter_parte_para_md.py` para gerar um
`.md` de cada PDF/DOC daquela pasta e passa a ler o `.md` em vez do original — poupa tokens e evita reler o
mesmo PDF em várias mensagens. Detalhes e gatilho exato em [CLAUDE.md](CLAUDE.md). Pré-requisito:
`pip install -r scripts/requirements.txt`.
