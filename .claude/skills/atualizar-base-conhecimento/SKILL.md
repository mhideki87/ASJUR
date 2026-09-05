---
name: atualizar-base-conhecimento
description: >-
  Consolida na base do repositório ASJUR o que a sessão descobriu e commita na branch da sessão: tese nova,
  tese que não foi aceita, jurisprudência dos autos ausente da base, gatilho de roteamento que faltou,
  estrutura de peça — gravando cada achado no arquivo certo (teses/, modelos/, CONTEXTO.md, playbook) e
  regenerando o INDICE.md. DISPARE ao final de qualquer sessão em que uma peça foi analisada ou minutada
  (contestação, contrarrazões, recurso, quesitos, manifestação, embargos), mesmo sem o usuário pedir e mesmo
  que ele só sinalize que acabou: "pode encerrar", "ficou boa assim", "minuta pronta", "é isso", "valeu",
  "amanhã eu volto", "roda o protocolo", "atualize a base", "consolide isso". DISPARE também quando surgir
  achado que a base deveria guardar: tese que o juiz não aceitou, precedente dos autos que não consta da base,
  ficha errada aberta por gatilho faltando, peça sem modelo salvo, ficha ou índice mexido à mão. NÃO dispare
  no meio da minuta, nem para pergunta de roteamento ou dúvida jurídica.
---

# Atualizar a base de conhecimento (ASJUR)

## O que esta skill resolve

A base cresce **por demanda**: só aprende o que for consolidado ao fim de uma sessão real. O risco é duplo e
simétrico — perder o que foi descoberto, ou inventar achado para parecer produtivo. As duas falhas custam
caro: a primeira faz a base estagnar; a segunda a envenena, porque tese não conferida vira citação errada em
peça protocolada.

Então o critério é: **consolidar só o que apareceu de fato nesta sessão, e dizer com clareza quando nada
apareceu.** "Nada novo" é resultado legítimo e frequente — a maioria das sessões repete tese conhecida.

## Passo 1 — Levantar os achados

Reveja a conversa (não a base) e responda, separadamente, cada pergunta abaixo. Se a resposta for "nada",
escreva "nada" e siga:

1. **Tese nova** — algum argumento usado aqui não está nas fichas que você abriu?
2. **Correção** — alguma tese da base se mostrou errada, incompleta, ou foi rebatida com sucesso pela parte
   contrária neste processo?
3. **Jurisprudência nova** — algum precedente **dos autos ou anexado pelo usuário** ainda não consta da ficha
   do tema? (Aresto que você "lembra" não conta — só entra o que está nos documentos da sessão.)
4. **Roteamento** — o índice levou você até a ficha certa sozinho? Se o usuário teve que dizer do que se
   tratava, ou se você abriu ficha que não servia, faltou ou sobrou gatilho.
5. **Modelo de peça** — a estrutura usada já está em `modelos/`? O caso revelou variação que valha preservar?
6. **Regra de trabalho** — o usuário corrigiu *como* você trabalha (formato, ordem das etapas, o que nunca
   fazer)? Isso não é tese, é `CONTEXTO.md`.

## Passo 2 — Mandar cada achado para o arquivo certo

| Achado | Destino |
|---|---|
| Tese nova, tema **já tem** ficha | seção correspondente da ficha (`Tese central`, `Fundamentos`, `Pontos sensíveis`) |
| Tese nova, tema **sem** ficha | ficha nova em `teses/<área>/<slug>.md`, a partir de `teses/_TEMPLATE_TESE.md` |
| Jurisprudência confirmada | seção `Jurisprudência` da ficha do tema |
| Tese que se mostrou errada | corrige o corpo da ficha, muda `status` para `revisar` e registra o motivo em `Lacunas` |
| Gatilho que faltou / sobrou | metadado `gatilhos:` da ficha (é o que faz o roteamento funcionar na próxima vez) |
| Estrutura de peça nova ou variação | `modelos/<área>/<tipo_peca>__<tema>.md` (+ `.docx` anonimizado, se houver peça real anexada) — e acrescente o caminho no metadado `modelos:` da ficha |
| Regra de trabalho ou perfil | `CONTEXTO.md` |
| Padrão formal da peça (fonte, margens, espaçamento, tópico em retângulo, numeração, cabeçalho, rodapé, assinatura) | `.claude/skills/formatar-minuta/` — SKILL.md e `referencia/especificacao_formatacao.md`. **Não** descreva formatação em `modelos/README.md`, que só aponta para a skill |
| Nomenclatura do arquivo final, tipo de peça novo | `playbook_prompts_ECT.md` (seção 5.1) |
| Lacuna que não é de um tema | `LACUNAS.md` |
| Prompt que funcionou bem / erro de pedido a evitar | `playbook_prompts_ECT.md` |
| Rotina de sessão do Claude Code (automação, título, conversão) | `CLAUDE.md` |
| Protocolo de leitura do índice (a prosa, não a tabela) | `INDICE.md` — a tabela é gerada, não se edita à mão |

Área é `trabalhista`, `civel` ou `transversal` (vale nas duas). Convenções de ficha, metadados e seções:
`teses/README.md`.

Uma ficha é a **unidade de leitura**: se o achado não cabe na ficha existente sem inflá-la, ou se o tema tem
gatilho próprio na inicial, é ficha nova — não apêndice de uma ficha alheia.

## Passo 3 — Aplicar as edições

- **Somar, não substituir.** Tese nova entra ao lado do que já existe. Só reescreva ou apague o que estava
  lá se o usuário confirmar que estava errado ou desatualizado.
- Atualize o campo `atualizado:` (formato `AAAA-MM-DD`) de toda ficha que você tocar.
- `status:` da ficha: `validada` (usada em peça real, conferida) · `rascunho` (candidata a tese) ·
  `revisar` (algo se mostrou errado). Ficha nova nascida de uma sessão real de minuta é `validada`;
  nascida de hipótese ou de levantamento é `rascunho`.
- **Nada inventado.** Norma, súmula e aresto só entram com a fonte exata. Faltando informação, deixe
  `[REVISAR: o que conferir]` no corpo — não preencha com conteúdo plausível.
- **Nenhum dado que identifique parte real** — nome, nº de processo, CPF, Id de documento de caso concreto.
  O repositório é **público**. Vale para o corpo do `.md`, para o `.docx` e para os **metadados** do `.docx`
  (autor, revisões, comentários).

## Passo 4 — Regenerar o índice

Toda vez que uma ficha for criada, renomeada, ou tiver metadado alterado:

```bash
python scripts/atualizar_indice.py           # revalida os metadados e reescreve a tabela do INDICE.md
python scripts/atualizar_indice.py --check   # confere sincronia — rode antes de propor o commit
```

O script também mede o **pedágio** (`CONTEXTO.md` + `INDICE.md`, lidos em toda sessão) e avisa quando
ele passa de 40% de uma sessão típica, listando as fichas com mais gatilhos. Se esse aviso aparecer,
**repasse-o ao usuário** no relatório do Passo 5 — não enxugue por conta própria no meio de uma
consolidação: cortar gatilho custa recall e é decisão à parte, com o critério de `teses/README.md`.

O script recusa metadado faltando, `slug` diferente do nome do arquivo, `area` diferente da pasta, `status`
inválido, data fora do formato e referência para arquivo inexistente. Se ele reclamar, corrija a ficha — não
edite a tabela do `INDICE.md` à mão, ela é sobrescrita.

## Passo 5 — Commitar na branch da sessão

Aplique as edições, rode o script do Passo 4 e **commite sozinho** — sem pedir autorização. A revisão do
usuário acontece depois, no diff do commit ou no Pull Request; travar a consolidação esperando um "ok"
é o que fazia o aprendizado da sessão se perder.

Antes de commitar, três conferências que existem porque o repositório é **público** e o erro aqui é
irreversível:

```bash
git branch --show-current      # tem de ser uma branch claude/*, nunca main
git diff --stat                # o que mudou
git diff                       # leia de fato, procurando dado de parte real
```

1. **Branch.** Só commite em branch `claude/*`. Se estiver em `main`, crie a branch da sessão primeiro
   (`git checkout -b claude/<assunto>`) — nunca commite direto na `main`.
2. **Escopo.** Só entram no commit arquivos da base: `teses/`, `modelos/`, `CONTEXTO.md`, `INDICE.md`,
   `playbook_prompts_ECT.md`, `CLAUDE.md`, `README.md`, `scripts/`, `.claude/`. Apareceu outro arquivo no
   `git status`? Deixe fora e diga ao usuário o que ficou de fora e por quê — em especial qualquer
   PDF/DOC/DOCX de processo, que **nunca** entra (`.gitignore` cobre o caso comum, não todos).
3. **Dado identificável.** Releia o próprio diff procurando nome de parte, nº de processo, CPF, Id de
   documento, nome de arquivo de caso concreto. Achou? Anonimize antes de commitar. Um commit já
   publicado não se desfaz apagando a linha depois — fica no histórico de um repositório público.

Commit e push:

```bash
git add <apenas os arquivos da base que você tocou>
git commit -m "<Tema>: <o que foi consolidado>"
git push -u origin <branch da sessão>
```

Mensagem que diga o **tema**, não "atualiza base": `Afastamentos: acrescenta tese de bis in idem do ACT` é
útil daqui a seis meses; `Atualiza base de conhecimento` não é. Push falhando por rede: repetir com espera
crescente (2s, 4s, 8s, 16s).

Feito o commit, relate ao usuário:

1. o resumo por achado — o que entrou, em qual arquivo, e por quê;
2. o hash e a mensagem do commit;
3. o que ficou marcado `[REVISAR: ...]` e depende de conferência humana;
4. o que você deixou fora do commit, se algo ficou.

**A única exceção que ainda espera aprovação: `.docx` anonimizado.** Modelo visual sai de uma peça real, e
conferir que nada sobrou em texto oculto, propriedade do documento, comentário ou revisão é verificação
humana — um `.docx` com nome de cliente num repositório público é vazamento. Produza o arquivo, diga
exatamente o que precisa ser conferido, e deixe o commit dele para quando o usuário aprovar. Os `.md`
seguem normalmente no commit automático.

## Tarefa que não é minuta

Se a sessão foi de manutenção do repositório (criou ficha, mexeu em modelo, mudou estrutura), o Passo 1 não
se aplica — vá direto ao Passo 4 e ao Passo 5: garanta que o índice está em sincronia, que os metadados
`modelos:`/`ver_tambem:` apontam para arquivos existentes, e que nenhum arquivo ficou órfão do roteamento.

## Quando não há nada a consolidar

Diga isso em uma linha ("nada novo nesta sessão — tese X já estava na ficha Y") e encerre. Não crie ficha
para tema que já tem uma, não acrescente gatilho redundante, não promova a "achado" o que era apenas a base
funcionando como devia. Uma base pequena e confiável vale mais que uma grande e duvidosa.

## Fora do Claude Code

No Project do claude.ai não há como gravar arquivo nem rodar o script. Ali o equivalente é o protocolo da
seção 6.2 de `playbook_prompts_ECT.md`: escrever o **trecho exato** a acrescentar em cada arquivo, incluindo
o bloco de metadados completo da ficha, para o usuário colar e commitar — e lembrar que ele precisa rodar
`python scripts/atualizar_indice.py` depois.
