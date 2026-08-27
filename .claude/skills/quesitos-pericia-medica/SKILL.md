---
name: quesitos-pericia-medica
description: Estrutura e texto aprovados dos quesitos de perícia médica da ECT em ações de doença ocupacional e acidente do trabalho (LER/DORT, coluna, joelhos, ombros, acidente típico, agravamento). Use SEMPRE que for formular, revisar ou adaptar quesitos para perícia médica judicial — inclusive quando o usuário só disser "faça os quesitos", "elabore quesitos para a perícia" ou anexar uma contestação pedindo quesitos. Traz os 12 quesitos já validados pelo usuário, o preâmbulo obrigatório e os requerimentos finais, prontos para receber os fatos do caso.
---

# Quesitos de perícia médica — modelo aprovado

Este é o **texto de referência já aprovado pelo usuário**, resultado de revisão manual dele
sobre uma versão anterior. Reproduza a estrutura; troque apenas os fatos.

Carregue **junto** a skill `minuta-peca` — ela dá o formato `.docx`, o nome do arquivo e a
formatação visual. Esta aqui dá o conteúdo.

## Estrutura — sem blocos temáticos

Ao contrário do que possa parecer natural, os quesitos **não** são divididos em blocos com
tópico em retângulo (I – Metodologia, II – Diagnóstico...). Eles correm em **lista contínua
numerada**, e há **um único retângulo na peça inteira**: `DOS REQUERIMENTOS`, ao final.

```
[qualificação resumida — "já qualificada nos autos"]
  ↓
síntese da demanda (1 parágrafo)
exigência de fonte objetiva por quesito (1 parágrafo)
exigência de resposta discriminada, sob pena de nulidade (1 parágrafo)
  ↓
1. … 12.   ← corridos, numerados, sem títulos de bloco; alíneas a) b) c) onde couber
  ↓
▭ DOS REQUERIMENTOS
a) b) c)
```

## Regras de redação

- **Tratamento: `o(a) Sr(a). Perito(a)`** — sempre nessa forma, nunca "o Sr. Perito".
- **Numeração corrida e sem lacunas**: `1.`, `2.`, `3.`… O número vai em negrito, o texto do
  quesito não. O gerador numera sozinho — não escreva o número à mão.
- **Nada de perícia de engenharia.** Não pergunte ao perito médico sobre NR violada, item e
  subitem, EPI, manutenção de veículo ou ergonomia do posto: é matéria de perícia técnica e o
  usuário retira esses quesitos. O mesmo vale para PCMSO/ASOs, que se provam por documento.
- **Transcreva o laudo literalmente.** Os quesitos mais produtivos citam entre aspas o trecho
  degenerativo do exame do próprio autor e opõem esse achado à tese de origem traumática. Sem
  a transcrição, o quesito perde a força.
- **Teto de 10 a 15 quesitos.** O modelo tem 12. Acima disso o juízo indefere ou o perito
  responde em bloco.
- **Quesito sem suporte fático sai.** Se o caso não tem afastamento previdenciário, plano de
  saúde ou exame recente favorável, remova o quesito correspondente — não o preencha com
  suposição.

## Os 12 quesitos

| # | Objeto | Tese que sustenta |
|---|---|---|
| 1 | Diagnóstico, CID-10, natureza e tempo de evolução — com a metodologia embutida | separa achado objetivo de relato |
| 2 | Achados degenerativos nos exames do autor (alíneas por exame) | degeneração preexistente |
| 3 | Existência e classificação da incapacidade × autor em atividade | não há incapacidade |
| 4 | Dano funcional sem repercussão laborativa — art. 104, §4º, I, Dec. 3.048/99 | imagem não é incapacidade |
| 5 | Sucesso do tratamento; sequela provada por teste objetivo | quadro estabilizado |
| 6 | Anamnese e fatores extralaborais | etiologia multifatorial |
| 7 | Art. 20, §1º, "a", Lei 8.213/91 e Listas do Anexo II | exclusão legal |
| 8 | Nexo individualizado por evento; DORT autônoma? | sequela de acidente ≠ doença ocupacional |
| 9 | Espécie 31 × 91, NTEP e ciência inequívoca | prova previdenciária; prescrição |
| 10 | Tratamento futuro não coberto pelo plano | fecha as despesas médicas |
| 11 | Concausa quantificada e tabela objetiva por segmento | art. 945 do CC |
| 12 | Capacidade residual e aproveitamento em outra função | afasta pensão integral |

O texto integral está em `scripts/corpo_padrao.py`, com `[PLACEHOLDER]` nos pontos que mudam
por caso. **Não reescreva os quesitos do zero** — parta desse arquivo.

## Requerimentos finais — só três

`a)` respostas uma a uma, fundamentadas · `b)` laudo com a antecedência do art. 477 do CPC ·
`c)` reserva de quesitos suplementares (art. 469 do CPC).

Não inclua intimação prévia da perícia nem indicação de assistente técnico: o usuário as
retirou. Nada de pedido de juntada de documento (carta de preposição, procuração) — isso é
circunstância de um processo específico, não do modelo.

## Como gerar

```python
import sys
sys.path.insert(0, ".claude/skills/minuta-peca/scripts")
sys.path.insert(0, ".claude/skills/quesitos-pericia-medica/scripts")
from montar_peca import montar, nome_arquivo
from corpo_padrao import montar_corpo

montar(
    saida=nome_arquivo("Quesitos", "Perícia Médica", "NOME DA PARTE"),
    enderecamento="JUIZ(A) FEDERAL DA Nª VARA DO TRABALHO DE CAMPO GRANDE/MS.",
    autos="0000000-00.0000.5.24.0000",
    reclamante="NOME DA PARTE",
    tipo_peca="QUESITOS PARA A PERÍCIA MÉDICA",
    qualificacao="resumida",          # "já qualificada nos autos"
    corpo=montar_corpo(sintese="Trata-se de reclamação trabalhista em que ..."),
)
```

`qualificacao="resumida"` é obrigatório aqui: em quesitos a Reclamada já está qualificada na
contestação, e não se repete CNPJ, endereço e Decreto-Lei de criação nem se declina
fundamentação de admissibilidade.

Antes de entregar, rode o validador da `minuta-peca`:

```bash
python3 .claude/skills/minuta-peca/scripts/conferir_peca.py "<arquivo>.docx"
```

## De onde vêm os fatos

Contestação · laudos e exames de imagem juntados pela parte · documentos do INSS. CIDs, datas
e transcrições de laudo **saem dos documentos**; não constando dos autos, marque `[REVISAR]`
em vez de presumir.
