# Modelos estruturais

Esta pasta guarda o **esqueleto de cada tipo de peça**, por tema — a parte que a
`base_conhecimento_juridico_*.md` não cobre. A base diz *o que* argumentar; aqui fica *como* montar a peça,
para que uma peça-modelo antiga não precise ser reanexada toda vez que o tema se repetir.

## Convenção de nomes

```
modelos/<area>/<tipo_peca>__<tema_em_snake_case>.md
```

- `<area>` = `trabalhista` ou `civel`.
- `<tipo_peca>` = mesma abreviação/nome usado na seção 6 de `playbook_prompts_ECT.md`
  (ex.: `contestacao`, `contrarrazoes`, `recurso_revista`, `quesitos_pericia_medica`, `embargos_declaracao`).
- `<tema>` = mesmo nome de tema da base de teses (ex.: `incorporacao_funcao`, `doenca_ocupacional`,
  `extravio_sem_declaracao_valor`).

Exemplos: `modelos/trabalhista/contestacao__incorporacao_funcao.md`,
`modelos/civel/contestacao__extravio_sem_declaracao_valor.md`.

## Regra de conteúdo

- **Nunca** incluir nome de cliente, número de processo, CPF, ou qualquer dado que identifique uma parte real.
  Trechos reaproveitáveis devem ser genéricos o suficiente para servir a qualquer caso do mesmo tema.
- Um modelo só é criado ou atualizado depois de **aprovação explícita do usuário** — nunca criado
  proativamente ou "por completude".
- Use `modelos/_TEMPLATE.md` como ponto de partida.
- Se uma peça citar norma interna, súmula ou precedente, cite a fonte exata — nunca parafrasear como se
  fosse citação literal.

## Como isso é usado no dia a dia

Ver seção 6 de `playbook_prompts_ECT.md` ("Protocolo de atualização da base"): ao final de uma sessão em que
uma peça-modelo foi anexada, o Claude verifica se já existe modelo salvo para aquele tipo de peça + tema;
se não existir (ou se o anexado revelar uma variação relevante), propõe a criação/atualização do arquivo aqui,
para revisão do usuário antes do commit.
