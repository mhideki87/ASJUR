# Modelo: Contraminuta a embargos de declaração — honorários sucumbenciais omitidos

**Consolidado de:** 1 caso-fonte — obrigação de fazer em rito sumaríssimo, sentença procedente omissa quanto
aos honorários pedidos na inicial (caso identificado só pelo tema; nenhum dado de parte ou processo aqui).
**Última atualização:** 07/09/2026 — criação do modelo.

---

## Quando usar este modelo

A parte contrária opõe embargos de declaração para suprir omissão da sentença quanto a **verba cujo valor
depende de arbitramento judicial** — tipicamente honorários de sucumbência — e a ECT é intimada na forma do
**art. 897-A, § 2º, da CLT** e do **art. 1.023, § 2º, do CPC**, porque o acolhimento acrescentaria capítulo
condenatório.

Não se aplica quando os embargos atacam o mérito do capítulo principal: aí a peça é defesa do julgado, não
disputa de critério de cálculo.

Distingue-se dos modelos `embargos_declaracao__*`, que são para **opor** embargos. Este é para **responder**.

## Postura que o modelo assume

A omissão em geral é real. Negá-la em bloco desgasta a defesa e não evita a condenação. O modelo **concede o
suprimento e disputa o critério de cálculo**, que é onde está o dinheiro.

Antes disso, e fora desta peça: se a sentença é omissa quanto aos honorários do Reclamante, a ECT **nunca**
suscita essa omissão por conta própria — ver a regra de postura na ficha de teses.

## Estrutura padrão

Formatação: não repetir medidas aqui — o padrão visual vem da skill `formatar-minuta`
(`.claude/skills/formatar-minuta/referencia/especificacao_formatacao.md`).

```
Endereçamento — Juízo da Vara (sentença) ou Relator/Turma (acórdão)
Autos nº / EMBARGANTE / EMBARGADA
Preâmbulo — qualificação da ECT + art. 897-A, § 2º, da CLT c/c art. 1.023, § 2º, do CPC

[RETÂNGULO] DOS EMBARGOS DE DECLARAÇÃO
             1 – DA DELIMITAÇÃO DO OBJETO DOS EMBARGOS
             2 – DOS LIMITES DO SUPRIMENTO PRETENDIDO
[RETÂNGULO] DO MÉRITO
             1 – DA NORMA DE REGÊNCIA: ART. 791-A DA CLT, E NÃO ART. 85 DO CPC
             2 – SUBSIDIARIAMENTE: SE APLICADO O CPC, QUE O SEJA POR INTEIRO
             3 – DA BASE DE CÁLCULO
             4 – DO PERCENTUAL: CRITÉRIOS DO ART. 791-A, § 2º, DA CLT
             5 – DA IMPOSSIBILIDADE DE MAJORAÇÃO POR RESISTÊNCIA E ATOS FUTUROS
             6 – [BLOCO CONDICIONAL] DA DESTINAÇÃO DA VERBA – ASSISTÊNCIA SINDICAL
             7 – DO PRAZO DO ART. 1.024, § 4º, DO CPC
[RETÂNGULO] DOS REQUERIMENTOS
Fecho + assinatura
```

- **Delimitação do objeto** — fixar que os embargos alegam vício único e que nenhum outro capítulo foi
  impugnado. Impede que a via declaratória se amplie na decisão.
- **Limites do suprimento** — não se opor à integração, mas recusar que os critérios de cálculo do embargante
  sejam acolhidos sem exame; consignar que o arbitramento é subordinado à sobrevivência do capítulo principal.
- **Norma de regência** — especialidade e posterioridade do art. 791-A; ausência de omissão afasta o processo
  comum (art. 769 da CLT, art. 15 do CPC). Reforçar com o **capítulo de direito intertemporal da própria
  sentença**, que costuma não ser embargado — é o argumento mais forte, e **só existe se a sentença tiver
  esse tópico**: conferir antes de escrevê-lo.
- **CPC por inteiro** — se o embargante quer o art. 85, vem também o § 8º.
- **Base de cálculo** — ordem do *caput*: liquidação → proveito econômico → *residualmente* valor da causa.
  Havendo valor arbitrado à condenação, é ele que prevalece.
- **Percentual** — mínimo legal, percorrendo um a um os quatro critérios do § 2º.
- **Resistência e atos futuros** — desmentir com o próprio julgado e com o art. 5º, LV, da CF.
- **Requerimentos** — alíneas na ordem das teses, encerrando com prequestionamento (Súmula 297 do TST).

## Linguagem / trechos-padrão reaproveitáveis

- Concessão delimitada: *"A Embargada não se opõe a que o r. Juízo integre a prestação jurisdicional quanto
  ao pedido não apreciado. O que não pode ocorrer é que, a pretexto de suprir omissão, sejam acolhidos sem
  qualquer exame os critérios de cálculo unilateralmente propostos pelo Embargante."*
- Pinça do CPC: *"A aplicação do art. 85 do CPC não se faz por fragmentos: não é dado invocar o dispositivo
  apenas naquilo que amplia percentuais e desprezar o seu § 8º."*
- Atos futuros: *"Honorários não se arbitram sobre atos processuais futuros e hipotéticos. O trabalho
  eventualmente desenvolvido em grau recursal tem sede e momento próprios de apreciação, não podendo ser
  antecipado na fixação da verba de primeiro grau, sob pena de arbitramento fundado em prognóstico, e não em
  serviço efetivamente prestado."*
- Direito de recorrer: *"A interposição de recurso é exercício regular de direito assegurado pelo art. 5º,
  LV, da Constituição Federal, e não conduta a ser apenada. Fosse de outro modo, a garantia do contraditório
  e da ampla defesa converter-se-ia, ela própria, em fator de agravamento da sucumbência."*
- Contra o próprio pedido do embargante, quando ele pediu percentual sobre o valor da causa "em razão de o
  direito pleiteado não ter efeito pecuniário": citar a frase dele e concluir pelo arbitramento equitativo.

## Variações observadas

- **Sem valor arbitrado à condenação** — cai o subtópico 3; concentrar no arbitramento equitativo.
- **Sentença sem capítulo de direito intertemporal** — suprimir esse parágrafo do subtópico 1.
- **Sem assistência sindical** — suprimir o subtópico 6 (por isso ele é condicional).
- **Recurso ainda não interposto** — ajustar o subtópico 7 para "a ser interposto".
- **Embargos que também atacam o mérito** — modelo inaplicável.

## Ligação com a base de teses

- Teses e a regra de postura:
  [teses/trabalhista/honorarios_sucumbenciais_omissao_da_sentenca.md](../../teses/trabalhista/honorarios_sucumbenciais_omissao_da_sentenca.md)
- Honorários dentro da contestação:
  [teses/trabalhista/temas_acessorios.md](../../teses/trabalhista/temas_acessorios.md)
- Padrão visual: skill `formatar-minuta`; nome do arquivo entregue: skill `nomear-minuta`.

## Par `.docx`

Ainda não existe. A peça do caso-fonte foi gerada fora do padrão da skill `formatar-minuta` e não serve de
base visual. Gerar o `.docx` anonimizado na próxima vez que a peça for produzida pela skill.
