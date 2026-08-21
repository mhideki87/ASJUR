# Modelo: Contestação — Afastamentos (atestado médico / auxílio-doença)

**Consolidado de:** 1 caso-fonte (contestação real, anonimizada — ver `contestacao__afastamentos.docx` neste
mesmo diretório).
**Última atualização:** 2026-08-15 — criação inicial.

---

## Quando usar este modelo

Contestação de reclamação trabalhista em que a Reclamante pede pagamento de dias de afastamento por atestado
médico/auxílio-doença que a ECT teria descontado "indevidamente", tipicamente combinado com pedidos acessórios
do mesmo período (vale-alimentação, reajuste de ACT já pago, férias, FGTS, retificação do CNIS, dano moral,
honorários). Aplica-se sempre que a linha do tempo do afastamento envolver: atestado médico → homologação pela
Medicina do Trabalho da ECT → encaminhamento ao INSS → decisão do INSS (deferimento/indeferimento de benefício).

## Estrutura padrão

```
DA EQUIPARAÇÃO À FAZENDA PÚBLICA        (preliminar padrão de toda contestação da ECT — ver seção 3.3
                                          de base_conhecimento_juridico_ECT.md)
RESUMO DA VESTIBULAR
PRELIMINARMENTE
  1 — DA CARÊNCIA PARCIAL DE AÇÃO       (quando parte do período pleiteado já foi paga espontaneamente
                                          na folha — demonstrar com aritmética exata de avos/dias)
DO MÉRITO
  1 — Limite legal de 15 dias de responsabilidade do empregador e suspensão do contrato
  2 — Lacuna previdenciária no período não coberto, atribuída a ato/omissão da própria Reclamante
  3 — Inexistência de desconto de vale-alimentação/vale-cesta (rebater com os próprios contracheques
      juntados pela parte autora)
  4 — Reajuste do ACT já pago / risco de bis in idem (quando a inicial usa valor já reajustado para
      período anterior ao reajuste)
  5 — Férias: exclusão automática por afastamento + eventual concorrência da própria autora na
      definição do período de gozo
  6 — FGTS: não incide sobre benefício previdenciário comum (espécie 31) durante suspensão contratual
  7 — Retificação do CNIS / impugnação de multa diária (astreintes)
  8 — Inexistência de danos morais
  9 — Honorários advocatícios (base de cálculo)
DOS REQUERIMENTOS                        (a-e: extinção parcial se cabível; improcedência total; compensação
                                          eventual; equiparação à Fazenda Pública; honorários de sucumbência)
Fecho + assinatura
```

## Linguagem / trechos-padrão reaproveitáveis

- Bloco "DA EQUIPARAÇÃO À FAZENDA PÚBLICA": cita RE 220699/SP (Rel. Min. Moreira Alves, DJ 16/03/2001) e o rol
  de acórdãos no mesmo sentido — texto genérico, sem dado de caso, reaproveitável literalmente.
- Fecho de requerimentos (alíneas a-e) e o parágrafo de protesto por provas/pedido de intimação exclusiva ao
  procurador — texto padrão, reaproveitável literalmente.
- Técnica de defesa "aritmética exata": quando parte do período já foi paga, demonstrar com divisor mensal
  (art. 64 da CLT — mês de 30 dias) o cálculo de avos pagos vs. avos ainda em discussão, citando as rubricas
  exatas do contracheque juntado pela própria parte autora.
- Técnica de defesa "documento da própria autora": sempre que possível, rebater o pedido com prova que a
  própria parte juntou aos autos (contracheque, atestado, formulário assinado eletronicamente) — evita
  necessidade de prova adicional da Reclamada.

## Variações observadas

**Resultado do caso-fonte (sentença de 08/2026 — parcialmente desfavorável).** Vale registrar o que a
sentença fez com cada tópico, porque é o único teste real que este modelo já sofreu:

| Tópico do mérito | Resultado |
|---|---|
| Carência parcial (dias já pagos) | **acolhida na prática** — a sentença reconheceu o pagamento e limitou a condenação, embora tenha rejeitado a preliminar por fórmula genérica |
| 1 — limite de 15 dias / suspensão do contrato | **não rejeitado** — a sentença reconheceu correto o encaminhamento ao INSS |
| 2 — lacuna previdenciária imputável à autora | **rejeitado** — havia ordem da chefia dispensando do labor, confirmada por testemunha (ver correção na seção 3.6 da base) |
| 3 — inexistência de desconto de vales | **não enfrentado** — omissão; gerou tópico 1 dos embargos |
| 4 — reajuste do ACT / *bis in idem* | **não enfrentado** |
| 5 — férias / exclusão automática | **acolhido** — dobra indeferida |
| 6 — FGTS espécie 31 | **não enfrentado**, e prejudicado pela requalificação da parcela como indenização |
| 7 — CNIS / astreintes | **astreinte não fixada** (impugnação acolhida por via oblíqua); obrigação de fazer deferida sem delimitação |
| 8 — danos morais | **rejeitado no fundamento** — houve condenação, mas em fração pequena do valor pleiteado, e **sem fixação do grau da ofensa** (art. 223-G, §1º, CLT) |
| 9 — honorários | pedido de sucumbência recíproca em favor da ECT **não apreciado** |

**Lacuna do modelo detectada neste caso — corrigir no próximo uso:** a estrutura de 9 tópicos **não prevê
tópico de mérito sobre previdência complementar (POSTALPREV/POSTALIS)**, embora o pedido de recolhimento da
cota patronal acompanhe rotineiramente os pedidos de diferenças salariais do período de afastamento. No
caso-fonte o pedido foi deferido sem fundamentação alguma, e a ausência de impugnação específica na
contestação restringiu o ataque recursal à nulidade por falta de fundamentação (art. 489, §1º, do CPC) e à
iliquidez do título (art. 492 do CPC), impedindo a discussão de fundo — entidade que não integra a lide,
regulamento do plano, base de cálculo e contribuição correspondente do participante. **Incluir tópico próprio
sempre que a inicial postular recolhimento a plano de previdência complementar.**

Ao usar de novo em outro processo, anotar aqui se a sequência fática (atestado → homologação → INSS) variar,
ou se algum dos tópicos do mérito não se aplicar.

## Desdobramento recursal

Sentença desfavorável neste tema tende a gerar embargos de declaração antes do recurso ordinário — ver
`embargos_declaracao__sentenca_primeiro_grau.md` neste mesmo diretório, cujo caso-fonte é justamente o
desdobramento deste modelo.

## Ligação com a base de teses

Tema "Afastamentos" ainda não constava em `base_conhecimento_juridico_ECT.md` — proposta de nova seção 3.6
enviada junto com este modelo para aprovação.
