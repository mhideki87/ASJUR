# Modelo: Quesitos de perícia médica — Doença ocupacional

**Consolidado de:** 1 caso-fonte (doença ocupacional por exposição solar em carteiro motorizado, com
acidente de trajeto cumulado).
**Última atualização:** 2026-09-02 — criação do modelo; fecha a lacuna registrada em
`teses/trabalhista/doenca_ocupacional.md`.

---

## Quando usar este modelo

Deferida perícia médica em ação na qual o Reclamante atribui doença ou incapacidade ao trabalho na ECT.
Serve tanto para quesitos apresentados junto com a contestação quanto para os apresentados depois, quando a
perícia é deferida em audiência — nesse caso, a peça é autônoma e o fundamento é o art. 465, § 1º, incisos
II e III, do CPC, aplicável por força do art. 769 da CLT.

Havendo **duas situações fáticas distintas** no mesmo processo (por exemplo, uma doença e um acidente de
trajeto), delimitar o objeto logo no início e dar bloco próprio a cada uma — o perito tende a responder em
conjunto e a contaminar as conclusões de uma com as da outra.

## Estrutura padrão

```
Delimitação do objeto da perícia   — o que se apura, separadamente; fatos incontroversos e confissões
I   — Metodologia e fontes          — separar achado objetivo de relato do periciando
II  — Diagnóstico e capacidade      — parcial/temporária, reversibilidade, DCB, espécie do benefício
III — Nexo causal                   — multifatorialidade, latência, extralaboral, NTEP, art. 20 §1º
IV  — Fatores pessoais              — predisposição constitucional preexistente à admissão
V   — EPI e ausência de culpa       — fornecimento, uso efetivo, e a norma específica alegadamente violada
VI  — Bloco do evento cumulado      — quando houver acidente autônomo (trajeto, fato da natureza)
VII — Ad cautelam                   — quantificação por tabela, capacidade residual, dano estético
Requerimentos finais                — resposta individualizada, assistente técnico, prazos, honorários
```

Numeração dos quesitos **corrida do primeiro ao último**, atravessando os blocos: o perito e a sentença se
referem a eles por número ("quesito 12 da ré"), e numeração reiniciada por bloco gera ambiguidade. Os
blocos são subtópicos numerados; os quesitos, alíneas (`- **1)** ...` na marcação da skill
`formatar-minuta`).

## Linguagem / trechos-padrão reaproveitáveis

**Abertura de bloco que aproveita confissão da parte** — a confissão vira premissa expressa do quesito,
obrigando o perito a se pronunciar sobre ela e não só sobre a versão da inicial:

> "Confirmado nos autos, pelo próprio depoimento pessoal do Reclamante, que a Reclamada fornecia e que ele
> efetivamente utilizava [equipamentos]: esses equipamentos são adequados e eficazes à proteção contra
> [agente] na atividade de [função]?"

**Fórmula que barra a afirmação genérica de culpa** — a mais importante do modelo:

> "Existe norma legal ou regulamentar de observância obrigatória que estabeleça [parâmetro objetivo]? Em
> caso positivo, queira o Sr. Perito indicar o dispositivo, com o número do item, e dizer, de forma
> expressa, se a Reclamada o descumpriu — não bastando, para tanto, afirmação genérica de culpa ou de
> 'falta de proteção adequada'."

**Fórmula que separa recomendação de dever jurídico** — usar sempre que o laudo puder invocar diretriz de
sociedade médica:

> "Caso o Sr. Perito entenda que [parâmetro] seria insuficiente, queira indicar qual seria o exigível e com
> base em que fonte normativa de cumprimento obrigatório pelo empregador, distinguindo-a de mera
> recomendação de sociedade médica ou de diretriz de boa prática, que não gera dever jurídico."

**Fórmula que impede a conclusão apoiada só no relato do periciando:**

> "Queira o Sr. Perito distinguir expressamente, em cada uma das conclusões do laudo, o que decorre de
> (i) exame clínico objetivo por ele realizado, (ii) exame complementar ou documento médico juntado aos
> autos e (iii) mero relato do periciando, informando quais conclusões se apoiam exclusivamente na terceira
> hipótese."

**Fórmula da concausa quantificada** — nunca aceitar concausa por presunção:

> "É possível afirmar, com base científica e não por presunção, que o trabalho foi causa determinante da
> patologia? Ou, no máximo, teria atuado como concausa? Caracterizada apenas a concausa, qual o percentual
> de contribuição da atividade laboral, e qual a metodologia empregada para chegar a ele?"

**Fórmula da restrição preventiva** — distingue restrição profilática de incapacidade instalada:

> "A restrição médica constitui restrição decorrente de incapacidade instalada ou medida de caráter
> preventivo/profilático? Ela impede em absoluto o exercício da atividade, ou apenas condiciona esse
> exercício à adoção de medidas de proteção?"

**Requerimentos finais** — os sete que fecham a peça: resposta individualizada e fundamentada (art. 473,
II, III e IV, e § 1º, do CPC); indicação de assistente técnico (art. 465, § 1º, II, do CPC); intimação
prévia da data do exame (art. 466, § 2º, do CPC); quesitos suplementares (art. 469 do CPC); manifestação
sobre o laudo e esclarecimentos (art. 477, §§ 1º e 2º, do CPC); honorários periciais a cargo do sucumbente
no objeto da perícia (art. 790-B da CLT); reiteração das prerrogativas processuais da ECT.

## Variações observadas

- **Quesitos junto com a contestação:** não há peça autônoma — os quesitos entram como tópico da própria
  contestação e o preâmbulo desaparece.
- **Quadro psiquiátrico:** o bloco IV muda de foco — em vez de predisposição constitucional, investigar
  fatores familiares, sociais e extralaborais, e a **reversibilidade** passa a ser o argumento mais forte
  do bloco II (ver `teses/trabalhista/doenca_ocupacional.md`).
- **LER/DORT:** acrescentar ao bloco I a vistoria ergonômica do posto de trabalho, e ao bloco V a
  cronologia das medidas preventivas — é nela que a ECT já perdeu no TRT24.
- **Sem evento cumulado:** o bloco VI simplesmente não existe; a numeração corrida se ajusta sozinha.
- **Perícia técnica (insalubridade/periculosidade):** modelo diferente — ver playbook, seção 2.5.

## Ligação com a base de teses

Sustenta [teses/trabalhista/doenca_ocupacional.md](../../teses/trabalhista/doenca_ocupacional.md) (moldura
das três frentes: incapacidade → nexo → culpa) e
[teses/trabalhista/cancer_pele_exposicao_solar.md](../../teses/trabalhista/cancer_pele_exposicao_solar.md)
(arsenal técnico do subtema dermatológico). Ambas listam este modelo no metadado `modelos:`.
