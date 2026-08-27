# Teste de acionamento da skill

Mede uma coisa só: **a skill dispara nas situações certas e fica quieta nas erradas?** Não avalia a
qualidade da consolidação — só o gatilho, que é o que a `description` do `SKILL.md` controla.

## Rodar

O teste executa `claude -p` de verdade, e a skill commita. Rode sempre numa **cópia isolada sem remote**,
para nenhum teste commitar ou dar push no repositório real:

```bash
SB=/tmp/asjur-eval
rm -rf $SB && mkdir -p $SB
tar -C /caminho/para/ASJUR --exclude=.git -cf - . | tar -C $SB -xf -
cd $SB && git init -q && git checkout -q -b claude/eval-trigger && git add -A && git commit -qm base

python3 .claude/skills/atualizar-base-conhecimento/evals/runner.py \
    $SB .claude/skills/atualizar-base-conhecimento/evals/trigger_eval.json 3
```

O terceiro argumento é quantas vezes cada query roda (3 dá uma leitura razoável de instabilidade).
Resultado agregado vai no stdout (JSON); o resumo linha a linha, no stderr.

## Como a detecção funciona

Cada query roda em `claude -p --output-format stream-json`. A query **disparou** se, entre os primeiros
tool_use da resposta, houver `Skill(atualizar-base-conhecimento)` ou um `Read` do `SKILL.md`. Depois do
terceiro tool_use sem isso, conta como não disparou — skill invocada só no fim de uma investigação longa
não é o comportamento que se quer.

## Por que não usar o `run_eval.py` do skill-creator

Aquele script registra a skill como um comando temporário `<nome>-skill-<uuid>` e procura esse nome na
chamada de ferramenta. Como esta skill **já está instalada** em `.claude/skills/`, o Claude invoca o nome
real e a detecção nunca casa: o resultado é `0/3` em todas as queries, inclusive nas que citam
literalmente os gatilhos da descrição. É falso negativo de medição, não falha da skill. O `runner.py`
daqui casa pelo nome real, e por isso mede o comportamento de produção — inclusive o reforço que o
`CLAUDE.md` dá ao gatilho.

## Conjunto de queries

`trigger_eval.json` tem 20 queries, metade que **deve** disparar e metade que **não deve**. As negativas
são de propósito quase-acertos — pedido de análise (que usa o índice, não a consolidação), pergunta de
roteamento, ordem direta de rodar o script, conversão de PDF, redação no meio da tarefa, edição de README.
Negativa óbvia não testa nada; o valor está nas que um casamento por palavra-chave erraria.

Ao mexer na `description` do `SKILL.md`, rode o teste antes e depois — o ganho numa ponta costuma custar
na outra.
