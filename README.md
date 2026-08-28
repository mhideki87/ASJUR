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
| [.claude/skills/peca-ect/](.claude/skills/peca-ect/SKILL.md) | Skill que gera as peças em .docx com a formatação da casa — carregada automaticamente pelo Claude Code neste repositório |

## Como usar (resumo)

1. Crie um Projeto no claude.ai e conecte este repositório via GitHub connector — os `.md` viram
   Project knowledge, buscados sob demanda.
2. No dia a dia: anexe os documentos do processo (inicial, sentença, laudos etc.). Peça-modelo antiga só
   é necessária se ainda não existir modelo salvo para aquele tipo de peça + tema (ver seção 6.1 do playbook).
3. Ao final de cada sessão em que algo foi minutado, rode o protocolo da seção 6.2 do playbook — o Claude
   aponta tese nova, correção, jurisprudência nova e atualização de modelo, em formato de diff para você
   revisar e commitar.

## Formatação das peças

A formatação não é descrita em prosa: ela é **executável**. A skill `peca-ect` traz o módulo
`peca_fmt.py`, que monta o `.docx` reaproveitando `modelos/_FORMATO_BASE.docx`, e o `conferir.py`, que
valida a peça antes do protocolo. Trabalhando dentro deste repositório, o Claude Code carrega a skill
sozinho — não é preciso pedir.

No claude.ai, a pasta `.claude/skills/` não vira skill: lá os `.md` entram como Project knowledge. Para as
peças em `.docx`, use o Claude Code.

## Regra permanente

Nenhum arquivo aqui deve conter nome de cliente, número de processo, CPF ou qualquer dado que identifique
uma parte real. Teses e modelos são generalizados; se precisar citar norma ou jurisprudência, cite a fonte
exata — nunca invente.
