# Modelo: <Tipo de peça> — <Tema>

> Este é o template vazio. Ao consolidar um modelo real, copie esta estrutura para
> `modelos/<area>/<tipo_peca>__<tema_em_snake_case>.md` (área = `trabalhista` ou `civel`).
> Preencha só com o que foi de fato aprovado pelo usuário — nada de conteúdo inventado.

**Consolidado de:** <quantidade> caso(s)-fonte, identificados só por nº interno ou tema
(nunca por nome de cliente real neste arquivo).
**Última atualização:** <data> — <o que mudou desde a versão anterior, se houver>

---

## Quando usar este modelo

<Em que situação fática/processual esta peça se aplica. Ex.: "Contestação de ação em que o
Reclamante pede incorporação de gratificação de função extinta pelo Módulo 55/36".>

## Estrutura padrão

```
I   — <bloco>
II  — <bloco>
III — <bloco>
...
```

<Uma linha por bloco explicando o que entra ali, sem copiar o texto literal de nenhum processo real.>

## Linguagem / trechos-padrão reaproveitáveis

<Frases ou parágrafos genéricos, sem nome de parte, nº de processo ou dado identificável, que se
repetem de caso para caso e podem ser reaproveitados quase literalmente. Se o trecho citar norma
interna ou jurisprudência, cite a fonte (norma, súmula, nº do acórdão) — nunca invente citação.>

## Variações observadas

<Quando este modelo NÃO se aplica integralmente, ou precisa de ajuste — ex.: "se o autor já tinha
o requisito temporal implementado antes da revogação, este bloco de defesa muda para X">

## Ligação com a base de teses

<Qual(is) ficha(s) de `teses/<área>/<tema>.md` este modelo normalmente sustenta. Confira também se a
ficha lista este modelo no metadado `modelos:` — se não listar, acrescente e rode
`python scripts/atualizar_indice.py`.>
