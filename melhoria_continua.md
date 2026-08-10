# Melhoria contínua — como o sistema aprende com o uso

> Complemento de todos os demais arquivos deste repositório.
> Objetivo: transformar erro apontado, correção feita ou peça nova produzida
> em conhecimento permanente do sistema, sem depender de memória automática
> do Claude entre conversas.

---

## 1. Por que isso não é automático

O Claude não guarda memória própria entre conversas. Numa conversa dentro de
um Projeto, ele só enxerga o que está subido como **Conhecimento do
Projeto** naquele momento. Se você corrige um erro numa conversa de terça, e
essa correção não for gravada em algum arquivo deste repositório e
re-subida ao Projeto, na conversa de quinta o mesmo erro pode se repetir.

Este arquivo existe para resolver isso com um processo simples, não com
promessa de "aprendizado automático" que o sistema não tem.

---

## 2. O ciclo de melhoria contínua

```
[1] Uso diário no Projeto Claude
    → você aponta um erro, corrige uma minuta, valida uma tese nova,
      ou finaliza uma peça nova.
         │
         ▼
[2] Na mesma conversa: rode o "prompt de registro de aprendizado" (seção 5)
    → o Claude devolve uma linha pronta para colar na tabela deste arquivo
      (seção 4), já indicando qual arquivo mestre deveria ser atualizado.
         │
         ▼
[3] Você cola a linha na tabela (seção 4) — rápido, sem decisão imediata.
         │
         ▼
[4] Periodicamente (sugestão: a cada peça nova ou a cada 1-2 semanas), numa
    sessão com acesso ao repositório (como uma sessão de Claude Code, não
    o chat comum do Projeto), rode o "prompt de consolidação" (seção 6)
    → o Claude edita de fato os arquivos mestres (base de conhecimento,
      banco de teses, checklist de formatação, índice de peças) e comita.
         │
         ▼
[5] Você re-sobe os arquivos mestres atualizados como Conhecimento do
    Projeto no claude.ai (substituindo as versões antigas).
         │
         ▼
[6] Marque a(s) entrada(s) consolidada(s) na tabela — vira histórico,
    não é apagada.
```

**Only na etapa [4] a mudança se torna permanente.** As etapas [1]-[3]
apenas capturam o aprendizado para não se perder — se pararem por aí, o
Projeto não melhora sozinho.

---

## 3. O que registrar

| Tipo | Exemplo | Arquivo mestre normalmente afetado |
|---|---|---|
| Erro corrigido | Claude citou uma súmula já cancelada | `banco_teses_jurisprudencia.md` (campo "Status atual") |
| Tese nova validada | Argumento novo que funcionou e deve virar padrão | `base_conhecimento_juridico_ECT.md` (seção 3) |
| Precedente novo | Jurisprudência usada e conferida numa peça | `banco_teses_jurisprudencia.md` (tabela de precedentes) |
| Peça nova produzida | Peça protocolada que deve virar modelo/busca futura | `banco_pecas_indice.md` |
| Falha de formatação recorrente | Mesmo erro de conversão .odt→.docx acontece sempre | `checklist_formatacao_pecas.md` |
| Preferência de redação | Você prefere uma estrutura diferente da que está no playbook | `playbook_prompts_ECT.md` |
| Regra de comportamento do Claude | Ex.: "sempre pergunte X antes de Y" | `instrucoes_personalizadas_projeto.md` |

---

## 4. Registro de aprendizado (log bruto)

| Data | Tipo | Contexto (sem dado sensível) | O que aprender / mudar | Arquivo mestre afetado | Status |
|---|---|---|---|---|---|
| _(preencher ao usar)_ | | | | | pendente |

Status possíveis: `pendente` (ainda não virou edição real) · `consolidado`
(já incorporado ao arquivo mestre, com data).

---

## 5. Prompt de registro de aprendizado

Rode assim que notar um erro, corrigir algo, ou concluir uma peça nova,
ainda na mesma conversa do Projeto:

```
Registre este aprendizado para o sistema. Não reproduza nome completo de
parte, número de processo ou dado de saúde. Devolva uma linha pronta para
colar na tabela da seção 4 de melhoria_continua.md, no formato:

| Data | Tipo | Contexto | O que aprender/mudar | Arquivo mestre afetado | Status |

Contexto do que aconteceu: <descreva o erro, a correção, a tese nova ou a
peça concluída>.
```

---

## 6. Prompt de consolidação (rodar numa sessão com acesso ao repositório)

Este prompt só funciona onde há acesso real aos arquivos e ao Git — por
exemplo, uma sessão de Claude Code apontada para este repositório. **Não
funciona no chat comum do Projeto**, porque lá o Claude não pode editar os
arquivos de conhecimento.

```
Leia melhoria_continua.md e liste todas as entradas com status "pendente".
Para cada uma:
1. Edite o arquivo mestre indicado, incorporando o aprendizado de forma
   compatível com o estilo e a estrutura já existentes no arquivo.
2. Se a entrada estiver ambígua ou incompleta para virar uma edição segura,
   NÃO edite — pergunte antes.
3. Marque a entrada como "consolidado" na tabela, com a data de hoje.
Ao final, resuma o que foi alterado em cada arquivo mestre, para eu revisar
antes de subir as versões novas como Conhecimento do Projeto.
```

Depois de rodar isso e revisar o diff, faça commit/push (ou peça para o
Claude fazer) e **lembre-se do passo [5] do ciclo**: re-subir os arquivos
mestres atualizados no Projeto Claude — sem isso, a melhoria não chega ao
dia a dia.

---

## Lacunas deste protocolo (preencher com o uso)

- [ ] Definir periodicidade fixa de consolidação (sugestão inicial: quinzenal)
- [ ] Avaliar se compensa automatizar a etapa [4] com uma rotina agendada
      (possível em ambientes Claude Code com suporte a rotinas/triggers)
