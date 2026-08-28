# ASJUR — Assessoria Jurídica

Base de conhecimento jurídico da assessoria (ECT), construída por demanda: cresce a cada sessão real de
minuta, não por processamento em massa das petições antigas.

## Estrutura

A base é **fatiada por tema** e lida sob demanda: nenhuma sessão lê a base inteira. O caminho é sempre
`CONTEXTO.md` → `INDICE.md` → só as fichas que o índice indicar.

| Arquivo/pasta | Conteúdo | Quando é lido |
|---|---|---|
| [CONTEXTO.md](CONTEXTO.md) | Perfil do usuário e regras inegociáveis | **Sempre**, por inteiro (é curto) |
| [INDICE.md](INDICE.md) | Roteamento `gatilho → ficha de tese`; tabela gerada por script | Sempre, logo depois do CONTEXTO |
| [teses/](teses/README.md) | Uma **ficha por tema**, em `trabalhista/`, `civel/` e `transversal/` | Só as fichas cujo gatilho bateu com o objeto da demanda |
| [modelos/](modelos/README.md) | `_FORMATO_BASE.docx` (formatação de qualquer peça) + esqueleto estrutural por tipo + tema — para não precisar reanexar peça-modelo antiga | Só o modelo do tipo de peça + tema da sessão |
| [playbook_prompts_ECT.md](playbook_prompts_ECT.md) | Prompts de uso diário + protocolo de atualização da base | Só a seção do tipo de peça |
| [CLAUDE.md](CLAUDE.md) | Instruções para sessões de **Claude Code** (local e cloud): protocolo de consulta à base, conversão automática dos documentos da parte (PDF/DOC) para `.md`, título da sessão com o nome do Reclamante | Automático |
| [.claude/skills/atualizar-base-conhecimento/](.claude/skills/atualizar-base-conhecimento/SKILL.md) | Skill que consolida na base o que a sessão produziu de novo e regenera o índice | Ao final de cada tarefa |
| [LACUNAS.md](LACUNAS.md) | O que falta validar na base e não pertence a nenhum tema | Em sessão de manutenção |
| [scripts/atualizar_indice.py](scripts/atualizar_indice.py) | Valida os metadados das fichas e regenera a tabela do `INDICE.md` | Ao criar/alterar ficha |
| [scripts/converter_parte_para_md.py](scripts/converter_parte_para_md.py) | Conversão de PDF/DOC do processo para `.md` — não roda no Project do claude.ai, só localmente | Automático (local) |

As fichas de tese substituíram os antigos `base_conhecimento_juridico_ECT.md` e
`base_conhecimento_juridico_CIVEL.md` (conteúdo migrado para `teses/`, histórico no Git).

## Como usar (resumo)

1. Crie um Projeto no claude.ai e conecte este repositório via GitHub connector — os `.md` viram
   Project knowledge, buscados sob demanda. Nas **instruções personalizadas** do Projeto, cole apenas o
   [CONTEXTO.md](CONTEXTO.md) (não a base inteira) e o protocolo de leitura do topo do
   [INDICE.md](INDICE.md).
2. No dia a dia: anexe os documentos do processo (inicial, sentença, laudos etc.). O Claude identifica os
   pedidos, casa cada um com um gatilho do índice e abre **só** as fichas correspondentes. Peça-modelo
   antiga só é necessária se ainda não existir modelo salvo para aquele tipo de peça + tema (seção 6.1 do
   playbook).
3. Ao final de cada sessão em que algo foi minutado, rode o protocolo da seção 6.2 do playbook — o Claude
   aponta tese nova, correção, jurisprudência nova, ficha a criar/atualizar e modelo a consolidar, em
   formato de diff para você revisar e commitar.
4. Depois de criar ou editar qualquer ficha: `python scripts/atualizar_indice.py` (regenera a tabela do
   índice e valida os metadados).

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
