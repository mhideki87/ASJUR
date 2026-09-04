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

- **Litígio sobre a fase posterior à alta.** Quando o pedido não é sobre os dias descontados durante o
  afastamento, mas sobre o intervalo entre a cessação do benefício e o exame médico de retorno, o tema é
  outro: usar `contestacao__limbo_previdenciario.md`. Se as duas fases estiverem em litígio no mesmo
  processo, combinar os dois modelos — este para o enquadramento do afastamento e o limite de 15 dias,
  aquele para a lacuna posterior à alta.
- Ao usar de novo em outro processo, anotar aqui se a sequência fática (atestado → homologação → INSS)
  variar, ou se algum dos 9 tópicos do mérito não se aplicar.

## Ligação com a base de teses

Seção 3.6 de `base_conhecimento_juridico_ECT.md` (afastamentos e limite de responsabilidade do empregador).
A fase posterior à alta previdenciária está na seção 3.7.
