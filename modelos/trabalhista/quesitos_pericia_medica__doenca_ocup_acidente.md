# Quesitos de perícia médica — doença ocupacional / acidente do trabalho

Tipo de peça: **quesitos** · Tema: **doença ocupacional e acidente do trabalho** · Área: **trabalhista**

> **O modelo vivo está na skill `quesitos-pericia-medica`** — texto integral dos quesitos em
> `.claude/skills/quesitos-pericia-medica/scripts/corpo_padrao.py`, estrutura e regras de
> redação em `SKILL.md`. Este arquivo é o resumo para consulta rápida; ao gerar a peça, use a
> skill, não este `.md`.

Formatação e nome do arquivo: skill `minuta-peca`. Versão aprovada pelo usuário em 27/08/2026,
após revisão manual dele sobre uma primeira minuta.

## Estrutura — lista corrida, um único retângulo

Nada de blocos temáticos (I – Metodologia, II – Diagnóstico...). Os quesitos correm numerados,
e o **único tópico em retângulo da peça é `DOS REQUERIMENTOS`**, ao final.

```
qualificação resumida ("já qualificada nos autos", sem admissibilidade)
síntese da demanda · exigência de fonte objetiva · exigência de resposta discriminada
1. … 12.   (alíneas a) b) c) onde o quesito se desdobra por exame)
▭ DOS REQUERIMENTOS  →  a) b) c)
```

## Os 12 quesitos

| # | Objeto | Tese |
|---|---|---|
| 1 | Diagnóstico, CID-10, natureza, tempo de evolução; metodologia embutida | achado objetivo × relato |
| 2 | Achados degenerativos nos exames do autor (uma alínea por exame) | degeneração preexistente |
| 3 | Incapacidade: existência e classificação × autor em atividade | não há incapacidade |
| 4 | Dano funcional sem repercussão laborativa (art. 104, §4º, I, Dec. 3.048/99) | imagem não é incapacidade |
| 5 | Sucesso do tratamento; sequela só por teste objetivo | quadro estabilizado |
| 6 | Anamnese ocupacional e fatores extralaborais | etiologia multifatorial |
| 7 | Art. 20, §1º, "a", da Lei 8.213/91; Listas do Anexo II | exclusão legal |
| 8 | Nexo individualizado por evento; existe DORT autônoma? | sequela de acidente ≠ doença ocupacional |
| 9 | Espécie 31 × 91; NTEP; ciência inequívoca | prova previdenciária e prescrição |
| 10 | Tratamento futuro não coberto pelo plano | fecha as despesas médicas |
| 11 | Concausa quantificada; tabela objetiva por segmento | art. 945 do CC |
| 12 | Capacidade residual; aproveitamento em outra função | afasta pensão integral |

## O que NÃO entra

Aprendido na revisão do usuário — estes pontos foram cortados de uma versão anterior:

- **Perícia de engenharia disfarçada de perícia médica**: NR violada com item e subitem, EPI,
  manutenção de veículo, ergonomia do posto, NR-36. Não se pergunta ao perito médico.
- **PCMSO, ASOs e exames ocupacionais** — provam-se por documento, não por perícia.
- **Bloco separado de metodologia** — virou parágrafo de preâmbulo e ficou embutido no quesito 1.
- **Requerimento de intimação prévia da perícia e de indicação de assistente técnico**.
- **Pedido de juntada de documento avulso** (carta de preposição, procuração) — é circunstância
  de um processo específico, não do modelo.

## Regras de redação

- Tratamento sempre `o(a) Sr(a). Perito(a)`.
- Numeração corrida e sem lacunas; número em negrito, texto do quesito não.
- Transcrever **literalmente**, entre aspas, o trecho degenerativo do exame do próprio autor —
  é o que dá força ao quesito.
- Teto de 10 a 15 quesitos; o modelo tem 12.
- Quesito sem suporte fático nos autos é removido, nunca preenchido por suposição.

## Insumos

Contestação · laudos e exames de imagem juntados pela parte · documentos do INSS (CNIS, carta
de concessão). CIDs, datas e transcrições saem dos documentos; não constando dos autos, marcar
`[REVISAR]`.

## Cuidado com dado real

Este arquivo e a skill são modelo: sem nome de parte, número de processo ou dado clínico de caso
concreto. A peça pronta **não entra no repositório** (ver `CLAUDE.md` e `README.md`).
