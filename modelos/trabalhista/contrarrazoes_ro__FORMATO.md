# Modelo: Contrarrazões de Recurso Ordinário — FORMATAÇÃO E ESTILÍSTICA

> Este é o modelo **de formatação e estilística** de contrarrazões de RO, válido para **qualquer tema**.
> O par `.docx` é o arquivo a abrir e usar como base — não recriar a formatação a partir desta descrição.
> Modelos de **tese/estrutura por tema** (quando existirem) ficam em arquivos próprios
> `contrarrazoes_ro__<tema>.md` e usam esta formatação.

**Consolidado de:** 1 caso-fonte (contrarrazões a RO do Reclamante, rito ordinário, TRT24, capítulo único
de base de cálculo de multa rescisória).
**Última atualização:** 21/08/2026 — criação, a partir de peça real revisada e aprovada pelo usuário.

---

## Quando usar este modelo

Sempre que a peça for **contrarrazões a Recurso Ordinário** (do Reclamante ou adesivo), com a ECT na
posição de Recorrida, endereçadas ao TRT da 24ª Região. Independe do tema de mérito.

Para os demais tipos de peça, a formatação geral vem de `modelos/_FORMATO_BASE.docx`. Este arquivo existe
porque as contrarrazões têm particularidades de corpo que valem preservar: a peça é **dupla** (petição de
juntada à Vara + razões ao Tribunal, separadas por quebra de página) e a hierarquia de títulos tem dois
níveis próprios (ver abaixo).

## Formatação (idêntica à do `.docx`)

| Elemento | Especificação |
|---|---|
| Página | A4 (11906 × 16838 twips) |
| Margens | esquerda 2 cm (1134) · direita 1,25 cm (707) · superior 2,28 cm (1292) · inferior 1,35 cm (769) |
| Cabeçalho | logotipo dos Correios + "Empresa Brasileira de Correios e Telégrafos / Assessoria Jurídica" (284 do topo) |
| Rodapé | endereço da Assessoria + numeração de páginas (712 da base) |
| Fonte | Arial 11 (`w:sz` 22) em todo o corpo |
| Entrelinha | 1,5 (`w:line="360" w:lineRule="auto"`) |
| Corpo | justificado, recuo de primeira linha de 3 cm (`firstLine="1701"`) |
| Alíneas e qualificação | justificado, recuo esquerdo de 3 cm (`start="1701"`), sem recuo de 1ª linha |
| Citações em bloco | recuo esquerdo 3 cm, **entrelinha simples** (`before/after="85"`), **itálico**, entre aspas |
| Fecho | "N. Termos / P. Deferimento." (juntada) · "Termos em que, / Pede deferimento." (razões) + "Campo Grande/MS, data de assinatura eletrônica." |
| Assinatura | centralizada, negrito: Marcos Hideki Kamibayashi — OAB/MS 14.580 |

### Hierarquia de títulos — dois níveis, e só dois

1. **Seção** — centralizado, negrito, CAIXA ALTA, **dentro de moldura** (borda simples nos quatro lados,
   `sz="8"`, `space="4"`), espaçamento antes 360 / depois 240. Usado apenas em:
   `SÍNTESE DA CONTROVÉRSIA E DOS ESTREITOS LIMITES DO APELO` · `MÉRITO RECURSAL` · `REQUERIMENTOS`.
2. **Tópico** — justificado, negrito, CAIXA ALTA, recuo esquerdo de 3 cm, **sem moldura**, numeração
   **árabe** (`1.`, `2.`, `3.` ...). Vive apenas dentro de `MÉRITO RECURSAL`.

Não há terceiro nível. Quando um tópico se desdobra, **não** usar `1.1` / `1.2`: promove-se cada desdobramento
a tópico numerado próprio, repetindo o título do tema e acrescentando o recorte depois de um travessão
(ex.: `2. DA X – VERBAS QUE NÃO INTEGRARAM O PEDIDO` / `3. DA X – SUBSIDIARIAMENTE: ...`).

Não usar numeração romana nos títulos.

## Estrutura padrão

```
── Petição de juntada (endereçada à Vara) ──────────────────────
   Endereçamento à [Nª] Vara do Trabalho de Campo Grande/MS
   Proc. nº · RECLAMANTE: · RECLAMADA:            (qualificação recuada 3 cm)
   Parágrafo de apresentação (intimação do RO → juntada → remessa ao TRT24)
   Parágrafo de tempestividade e dispensa de preparo
   Fecho + assinatura
── QUEBRA DE PÁGINA ────────────────────────────────────────────
── Razões (endereçadas ao TRT24) ───────────────────────────────
   EGRÉGIO TRIBUNAL REGIONAL DO TRABALHO DA 24ª REGIÃO
   C O N T R A R R A Z Õ E S   D E   R E C U R S O   O R D I N Á R I O
   Processo / Recorrente / Recorrida / Origem     (qualificação recuada 3 cm)
   "Egrégia Turma," / "Eminentes Desembargadores,"  (dois parágrafos de corpo)
   [SEÇÃO] SÍNTESE DA CONTROVÉRSIA E DOS ESTREITOS LIMITES DO APELO
   [SEÇÃO] MÉRITO RECURSAL
       1. tópicos-limite (inovação recursal, limite do pedido, preclusão, matéria não devolvida)
       2. mérito propriamente dito (acerto da sentença)
       3. distinguishing dos arestos do apelo
       4. AD CAUTELAM – limites em caso de provimento
   [SEÇÃO] REQUERIMENTOS
   Fecho + assinatura
```

Observações de estilo, extraídas da peça aprovada:

- **Sem parágrafo de abertura** entre o vocativo e a primeira seção. A peça vai direto do
  "Eminentes Desembargadores," para a moldura da `SÍNTESE`. Não abrir com resumo da tese.
- O vocativo é **duplo e em duas linhas** ("Egrégia Turma," / "Eminentes Desembargadores,"), formatado
  como corpo, não como título.
- **Não** usar a linha "RAZÕES DA RECORRIDA – ECT" (constava do modelo anterior e foi suprimida).
- A `SÍNTESE` encerra-se com o registro expresso dos **capítulos não impugnados** e do trânsito em julgado
  parcial, em alíneas — é o que delimita a devolutividade e sustenta o requerimento "c".
- Ordem do mérito: primeiro os tópicos que operam como **limite** ao apelo (admissibilidade, inovação,
  teto do pedido), depois o mérito de fundo. Quando essa inversão puder parecer contraditória, abrir o
  tópico de mérito com uma frase articulando que os tópicos são **cumulativos**.

## Linguagem / trechos-padrão reaproveitáveis

**Tempestividade e preparo** (petição de juntada — reaproveitar quase literalmente):

> Registra a Recorrida que o prazo para a apresentação das presentes contrarrazões conta-se em dobro, por
> força do art. 1º do Decreto-lei 779/69 e da equiparação da ECT à Fazenda Pública prevista no art. 12 do
> Decreto-lei 509/69, recepcionado pela CF/88 nos termos da decisão proferida pelo STF no julgamento do
> RE 220.906/DF, sendo, ademais, desnecessário qualquer preparo.

**Abertura do bloco *ad cautelam***:

> Na hipótese — que se reputa improvável — de provimento, ainda que parcial, do apelo, a Recorrida reitera
> expressamente, para apreciação por essa Egrégia Turma, dada a ampla devolutividade do recurso ordinário,
> os seguintes limites:

**Prerrogativas da Fazenda Pública** (alínea final do *ad cautelam*):

> prerrogativas da Fazenda Pública: observância da execução por precatório, da isenção de custas e de
> depósito recursal (art. 12 do Decreto-lei 509/69 e Decreto-lei 779/69; art. 790-A da CLT) e da atualização
> na forma do art. 3º da Emenda Constitucional nº 113/2021.

Atenção: **não** reproduzir o pedido de "correção monetária pela TR, nos termos da OJ 300 da SDI-1", que
ainda aparece em contestações antigas — critério superado pelas ADIs 4357 e 4425, pelo RE 870.947
(Tema 810) e pela EC 113/2021.

**Prequestionamento** (alínea final dos requerimentos):

> para fins de prequestionamento (Súmula 297 do C. TST), o pronunciamento explícito sobre [...]

Listar apenas dispositivos e verbetes **efetivamente debatidos na peça**. É a alínea que viabiliza eventual
recurso de revista: sem ela, matéria de defesa não prequestionada não sobe.

## Variações observadas

- **Sentença integrada por embargos de declaração** — o parágrafo de apresentação ganha ", integrada pela
  r. decisão de embargos de declaração de Id [...]", e todas as remissões passam a mencionar as duas decisões.
- **Recurso ordinário adesivo** — o título central vira
  `C O N T R A R R A Z Õ E S   D E   R E C U R S O   O R D I N Á R I O   A D E S I V O`, e o corpo trata o
  apelo como "apelo adesivo".
- **Recurso próprio da ECT no mesmo processo** — nos tópicos em que a Recorrida também pede reforma,
  registrar que a tese é sustentada "em seu recurso próprio", para não parecer contradição.
- **Rito sumaríssimo** — ajustar `ATSum` na qualificação; e, se houver perspectiva de revista, lembrar que
  o art. 896, §9º, da CLT admite apenas ofensa direta à CF ou contrariedade a súmula do TST/vinculante.
- **Recurso monotemático** — a estrutura comporta 4 a 6 tópicos; não inflar com capítulos sem impugnação
  correspondente. Peça de ~8 páginas foi suficiente no caso-fonte.

## Regras de conteúdo que este modelo pressupõe

- **Ad cautelam só reitera tese deduzida na contestação.** Tese nova em contrarrazões é atacável por
  preclusão (art. 342 do CPC; art. 847 da CLT). Quando a defesa original não deduziu a matéria, formular
  o argumento como **ausência de demonstração pelo Recorrente** (ônus dele), não como defesa nova.
- **Não negar eficácia de precedente vinculante** (IRR/IAC do C. TST, repetitivos, repercussão geral) que a
  ECT invoque em outros temas. Quando o Recorrente invocar tese vinculante, dizer expressamente que a
  Recorrida não a contesta e sustentar que a r. sentença já a observou.
- **Jurisprudência**: apenas ementas constantes dos autos, do modelo ou do próprio recurso adversário.

## Ligação com a base de teses

- `base_conhecimento_juridico_ECT.md`, item 3.3 — prerrogativas processuais da ECT (prazo em dobro,
  dispensa de preparo), que alimentam a petição de juntada e a alínea final do *ad cautelam*.
- `base_conhecimento_juridico_ECT.md`, item 3.7 — limites do valor do pedido e inovação recursal, tese
  desenvolvida no caso-fonte deste modelo.
- `playbook_prompts_ECT.md`, itens 1.3 (análise de RO do Reclamante) e 2.2 (redação de contrarrazões).
