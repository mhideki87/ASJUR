---
area: civel
tema: Panorama do acervo cível (levantamento estatístico)
slug: panorama_acervo_civel
status: rascunho
gatilhos: [panorama cível, volume de processos cível, tipos de peça cível, acervo, estatística do acervo]
pecas: []
modelos: []
ver_tambem: [teses/civel/indenizatoria_servico_postal.md]
atualizado: 2026-08-27
---

# Panorama do acervo cível

> **STATUS: RASCUNHO NÃO VALIDADO.** Gerado a partir de estatística determinística (regex/contagem de
> pastas) sobre os metadados de `3_acervo_com_fichas/_indice/metadados.jsonl` (arquivo local, fora deste
> repositório) — **nenhum arquivo foi lido/analisado por LLM**. Isto não é tese: é mapa de volume, para
> orientar onde investir esforço de validação.

## Tipos de peça no catálogo (461 arquivos classificados como "Cível")

| Peça | Ocorrências |
|---|---|
| Contestação / Defesa | ~127 |
| Sentença (anexada como modelo/precedente) | 24 |
| Manifestação (cálculo, RPV, audiência) | 22 |
| Acórdão (anexado como precedente) | 19 |
| Petição (avulsa) | 14 |
| Contrarrazões (recurso) | 12 |
| Petição inicial (raramente — polo ativo?) | 3 |
| Impugnação aos cálculos | 3 |
| Embargos à execução | 1 |

`[REVISAR]`: 236 dos 461 arquivos não tiveram o tipo de peça identificado automaticamente (nomes de
pasta, documentos de apoio, jurisprudência solta etc.) — não incluídos na tabela.

## Concentração temática

A imensa maioria dos casos está na pasta `AÇÕES INDENIZATÓRIAS SERVIÇO POSTAL` — ver
[teses/civel/indenizatoria_servico_postal.md](indenizatoria_servico_postal.md).

## Lacunas

- [ ] Confirmar se a ECT é sempre polo passivo em cível, ou se há atuação no polo ativo.
- [ ] Existência de outras matérias cíveis além de indenização por serviço postal (embargos à execução e
      improbidade administrativa aparecem citados — volume e relevância desconhecidos).
