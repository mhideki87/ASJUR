# Modelo: Contestação — vale-alimentação/refeição e vale-cesta em afastamento (cláusula 48 do ACT)

**Consolidado de:** 1 caso-fonte (rito sumaríssimo, 6ª VT de Campo Grande, TRT24, contestação minutada em
09/2026 e ainda **não decidida**).
**Última atualização:** 2026-09-10 — criação inicial.
**Formatação:** vem de `modelos/_FORMATO_BASE.docx`, pela skill `formatar-minuta`. Este tema não tem
`.docx` próprio — o corpo não traz nada estruturalmente distinto que justifique um arquivo binário separado.

---

## Quando usar este modelo

Contestação de reclamação em que o empregado, **afastado** por licença médica ou benefício previdenciário,
pede (i) obrigação de fazer para que a ECT credite os vales, em regra por tutela de urgência com multa
diária; (ii) a indenização em pecúnia do período não creditado; e (iii) dano moral pelo inadimplemento.
Costuma vir com "anuidade" de prestações vincendas somada ao valor da causa, justiça gratuita e honorários.

Tese e jurisprudência:
[`teses/trabalhista/vale_alimentacao_cesta_afastamento.md`](../../teses/trabalhista/vale_alimentacao_cesta_afastamento.md).

Distingue-se de `contestacao__limbo_previdenciario.md`, onde os vales são **pedido acessório** do intervalo
pós-alta, e de `contestacao__afastamentos.md`, cujo eixo é o limite de 15 dias e o desconto de dias. Aqui os
vales **são o objeto principal**, e a defesa se resolve na leitura da cláusula coletiva e na aritmética.

## A bifurcação que define a peça

Antes de redigir, é obrigatório obter da área o **histórico previdenciário completo** (Comunicação de Decisão
do INSS, Carta de Concessão e CNIS), com **espécie, DIB e DCB de cada benefício**. É esse documento, e não a
tese, que decide o quantum:

- **Afastamento acidentário (espécie 91) desde a origem** → a cláusula concede os vales "até o retorno", e
  negar o período é briga perdida. A defesa passa a ser de **depuração** (quantidade de vales,
  compartilhamento) e de dano moral, e convém avaliar o **reconhecimento parcial**.
- **Afastamento que começa comum (espécie 31) e só depois é convertido em 91** → abre-se a **janela
  intermediária** entre o 90º dia e a DIB do acidentário, e é ali que está o ganho de mérito. É o caso-fonte.

Sem esse documento, não construir a hipótese como fato: a marcação `[INSERIR: ...]` no corpo é o caminho
correto (regra 4 do `CONTEXTO.md`).

## Estrutura padrão (variante de improcedência com rescisão superveniente)

```
DA EQUIPARAÇÃO À FAZENDA PÚBLICA          (bloco literal de contestacao__afastamentos.docx + os quatro
                                           itens numerados; ver prerrogativas_processuais_ect)
RESUMO DA VESTIBULAR E DELIMITAÇÃO DA CONTROVÉRSIA
                                          (pedidos com valores; o fato superveniente; delimitação
                                           afirmativa em (a) a (e))
PRELIMINARMENTE
  1 — Perda superveniente de objeto da obrigação de fazer e da tutela (art. 493 e 485, VI, do CPC)
  2 — Inépcia parcial: obrigação de fazer e astreinte sem indicação de valor (art. 840, §§1º e 3º, CLT)
  3 — Limitação da condenação aos valores indicados (art. 852-B, I, CLT — rito sumaríssimo)
  4 — Impugnação ao pedido de justiça gratuita
DO MÉRITO
  1 — A cláusula 48, §6º, tem DUAS hipóteses, não uma regra única
  2 — Delimitação do período pela espécie do benefício previdenciário   ← capítulo que decide o quantum
  3 — Improcedência das prestações vincendas ("anuidade")
  4 — Ad cautelam: depuração do cálculo (quantidade de vales + compartilhamento do §1º)
  5 — Natureza indenizatória das parcelas e ausência de reflexos
  6 — Inexistência de dano moral indenizável                            ← capítulo realmente disputável
  7 — Impugnação à multa diária
  8 — Correção monetária e juros de mora (art. 3º da EC 113/2021)
  9 — Honorários advocatícios (art. 791-A da CLT, não art. 85, §3º, do CPC)
 10 — Impugnação aos documentos e ao valor da causa
DOS REQUERIMENTOS                         (a-h; a eventualidade em f.1 a f.5)
Fecho + assinatura
```

## Linguagem / trechos-padrão reaproveitáveis

- **Bloco "DA EQUIPARAÇÃO À FAZENDA PÚBLICA"**: literal de `contestacao__afastamentos.md` (e do `.docx`
  correspondente) — RE 220699/SP, o rol de acórdãos e o art. 3º da EC 113/2021. Acrescentar, quando a
  inicial pedir honorários ou juros "da Fazenda Pública", o parágrafo que registra a **admissão da
  equiparação pelo próprio autor**: torna o ponto incontroverso de graça.
- **Fecho do bloco:** pedir pronunciamento **expresso e individualizado** sobre as quatro prerrogativas,
  "sob pena de omissão a ser suprida por embargos de declaração" — a 6ª VT já deferiu pela metade uma vez.
- **Argumento de utilidade das expressões da cláusula:** *"a tese autoral, ao projetar a segunda hipótese
  sobre todo o afastamento, torna letra morta o limite dos noventa dias"* — somado ao **art. 8º, § 3º, da
  CLT** (intervenção mínima na autonomia coletiva), que impede ampliar por via judicial benefício
  convencionado com limite expresso.
- **Decomposição do período em alíneas (a), (b) e (c)**, com a alínea do meio isolando o interregno
  indevido. É a forma que deixa a conta pronta para o juízo e evita improcedência "em bloco".
- **Dedução do compartilhamento não pode ser diferida:** com o contrato extinto não haverá retorno nem folha
  sobre a qual descontar, logo a dedução tem de ser determinada **no próprio cálculo** — "sob pena de o
  Reclamante receber mais do que receberia se em atividade".
- **Técnica "aritmética exata", em três serviços na mesma peça:** os cálculos que fecham ao centavo sustentam
  a limitação da condenação; a divisão valor ÷ valor facial revela a quantidade de vales adotada; e a
  comparação astreinte/mês × obrigação/mês sustenta a redução da multa. Tudo em blocos `>>`.
- **Dano moral em cinco parágrafos numerados:** regime do Título II-A (arts. 223-A e 223-B da CLT, que a
  inicial ignora ao fundar-se só no Código Civil); ausência de dano presumido; a redução de renda decorre do
  art. 476 da CLT e não de ato patronal, com o discriminativo de créditos do INSS a provar que houve
  recebimento; desproporção entre a narrativa e o valor mensal da parcela; e ausência de indicação do grau da
  ofensa (art. 223-G, § 1º, da CLT). Fecha bem citar de volta a **doutrina transcrita pela própria inicial**
  ("existe um piso de inconvenientes que o ser humano tem de tolerar").

## Variações observadas

- **Sem rescisão superveniente.** Suprimir a preliminar 1 e o primeiro fundamento do tópico 3 do mérito; as
  prestações vincendas passam a cair só pela **ultratividade** (art. 614, § 3º, da CLT; ADPF 323), e a tutela
  se combate pelos requisitos do art. 300 do CPC.
- **Com débito reconhecido pela área.** Converter em **reconhecimento parcial** (art. 487, III, "a", do CPC),
  na forma de `contestacao__limbo_previdenciario.md`: é o melhor argumento contra o dano moral, e mais forte
  se o reconhecimento for **anterior à citação**.
- **Rito ordinário.** Cai o reforço do art. 852-B, I, da CLT na preliminar 3, restando o art. 840, § 1º, e a
  tese prevalecente nº 13 do TRT24 — com a ressalva de que a exceção da estimativa costuma ser aplicada.
- **Gratuidade — quando abrir o tópico.** Abriu-se no caso-fonte porque a parte é **empregado público de
  carreira longa, com remuneração documentada em ficha cadastral**, ainda que a causa fosse de valor médio.
  É a calibração inversa à do acervo de terceirização (parte de baixa renda), em que a ficha manda não abrir
  ou abrir só com o pedido sucessivo do art. 99, § 2º, do CPC. Conferir sempre a **data do ajuizamento**
  contra o marco da ADC 80 antes de escolher o regime.

## Ligação com a base de teses

Sustenta [`teses/trabalhista/vale_alimentacao_cesta_afastamento.md`](../../teses/trabalhista/vale_alimentacao_cesta_afastamento.md),
e depende de
[`afastamentos_auxilio_doenca.md`](../../teses/trabalhista/afastamentos_auxilio_doenca.md) (suspensão do
contrato, espécie do benefício),
[`justa_causa_durante_suspensao_contratual.md`](../../teses/trabalhista/justa_causa_durante_suspensao_contratual.md)
(rescisão superveniente e perda de objeto),
[`vale_cultura_supressao.md`](../../teses/trabalhista/vale_cultura_supressao.md) (ultratividade),
[`preliminares_processuais_defesa.md`](../../teses/transversal/preliminares_processuais_defesa.md),
[`justica_gratuita_adc80.md`](../../teses/transversal/justica_gratuita_adc80.md) e
[`prerrogativas_processuais_ect.md`](../../teses/transversal/prerrogativas_processuais_ect.md).

## Pontos que sempre exigem conferência humana antes do protocolo

1. **Espécie, DIB e DCB de cada benefício** do período — o dado que decide o quantum. Sem ele a peça não sai
   de `[INSERIR]`.
2. **Jornada semanal** (5 ou 6 dias), na ficha cadastral e na escala: define 22 ou 26 vales/mês e costuma
   valer dois dígitos percentuais do principal.
3. **Nível salarial**, para o percentual de compartilhamento do § 1º (5%, 10% ou 15%).
4. **Instrumento coletivo integral**, com vigência e valores faciais — a inicial transcreve a cláusula sem
   juntar o ACT, e é da vigência que depende o capítulo das vincendas.
5. **Extrato dos créditos** de VA/VR/VC no período, para a dedução do art. 767 da CLT e para saber se cabe
   reconhecimento parcial.
6. **Remuneração e o teto do RGPS do ano do ajuizamento**, para a impugnação à gratuidade.
7. Havendo **rescisão superveniente**, a juntada da comunicação de rescisão, da decisão do PAD e da liminar
   do mandado de segurança — e conferir se o ato rescisório segue eficaz na data do protocolo.
