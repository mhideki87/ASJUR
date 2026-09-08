# Lacunas da base

O que ainda falta validar e não pertence a nenhum tema específico. Lacuna de um tema fica na seção
"Lacunas" da própria ficha, em `teses/<área>/`.

Este arquivo é lido em sessão de **manutenção da base**, não em sessão de peça — por isso saiu do
`CONTEXTO.md`, que é lido sempre.

- [ ] Estrutura da equipe e distribuição de processos
- [ ] Volume mensal e prazos internos de entrega
- [ ] Orientações da Consultoria Jurídica nacional da ECT que vinculam a defesa local
- [ ] Teses que a ECT decidiu *não* sustentar (trabalhista e cível)
- [ ] Outras matérias além de trabalhista e cível (consumidor? improbidade?)
- [x] ~~Confirmar a assinatura usada nas peças cíveis~~ — confirmado: cível usa a mesma assinatura
      (Marcos Hideki Kamibayashi — OAB/MS 14.580) e o mesmo padrão visual da trabalhista
- [ ] Confirmar se há atuação no polo ativo em cível
- [ ] Confirmar se há atuação em Justiça Estadual / Juizados Estaduais, além do JEF e da Justiça Federal
- [x] ~~**Tema sem ficha: AADC (Adicional de Atividade de Distribuição e/ou Coleta Externa).**~~ —
      fechada: a ficha `teses/trabalhista/supressao_adicional_atividade_readaptacao.md` cobre AAT e AADC
      (salário-condição, itens 4.8 e 4.10 do PCCS/2008, Súmulas 248 e 265 do TST, readaptação), com os
      gatilhos previstos aqui. A conferência do inteiro teor dos arestos segue pendente, marcada
      `[REVISAR]` na própria ficha.

## Peça aprovada em 09/2026 diverge do padrão da skill `formatar-minuta`

Numa sessão de contrarrazões de RO, o usuário revisou e aprovou a minuta partindo de uma peça-modelo
anexada — e a peça resultante **não segue** a especificação da skill. Divergências medidas no XML:

| Item | Peça aprovada | Especificação da skill |
|---|---|---|
| Entrelinha | `lineRule="auto" line="360"` (1,5 múltipla) | `lineRule="exact" line="360"` (18 pt exatos) |
| Margens E/D/S/I | 1134 / 707 / 1292 / 769 (2,0 / 1,25 / 2,28 / 1,36 cm) | 1701 / 1134 / 1701 / 1134 (3 / 2 / 3 / 2 cm) |
| Citações | Arial 11, recuo 3 cm | Arial 10, recuo 4 cm |
| Subtópicos | negrito, numeração `1.` | negrito **sublinhado**, numeração `1 – ` |
| Fecho | "Termos em que, / Pede deferimento." | "Nesses Termos, / Pede Deferimento." |

A entrelinha é exatamente o erro que a especificação nomeia ("não é '1,5 linha'"). Um modelo de formatação
chegou a ser extraído dessa peça e **não foi commitado**, por contrariar a regra de que a skill é a fonte
única — decisão registrada no PR #47.

- [ ] **Decidir qual das duas cede.** Ou a peça passa a ser gerada pela skill (`gerar_minuta_docx.py`), ou a
      especificação é atualizada para reproduzir o formato que o usuário de fato usa e aprova. Enquanto a
      divergência existir, toda sessão que reaproveitar peça recente reintroduz o formato antigo — foi o que
      aconteceu aqui.
- [ ] A mesma sessão entregou arquivo nomeado com underscores (`CRRO_-_Multa_477_-_...`), contra a skill
      `nomear-minuta` (espaços e `" - "`). Sintoma do mesmo problema: branch atrasada não carrega as skills.

## ADC 80 (STF, 03/09/2026) — novo regime da justiça gratuita

Varrida a base em 06/09/2026. O tema ganhou ficha própria,
`teses/transversal/justica_gratuita_adc80.md`, com o dispositivo transcrito da ata e os blocos prontos para
os dois regimes (antes e depois do marco da modulação). Ajustados na mesma passagem:
`teses/transversal/preliminares_processuais_defesa.md` (o bloco antigo da ADC 80, que descrevia julgamento
em curso, foi **removido** por ter ficado factualmente falso), `teses/civel/indenizatoria_servico_postal.md`,
`teses/trabalhista/responsabilidade_civil_acidente_tipico.md` e os modelos de contestação de incorporação de
função, doença ocupacional e supressão de adicional.

Pendência que sobra e não é de um tema só: **a data de publicação da ata do julgamento de mérito**, que é o
marco da modulação e define qual dos dois regimes se aplica a cada processo. Não foi possível conferir em
sessão cloud (egresso de rede bloqueado para `noticias.stf.jus.br`). **Conferir em sessão local** e anotar na
ficha.

## Resolução nº 225/2025 do Pleno do TST — enunciados cancelados

Conferida contra a base inteira em 02/09/2026 (PDF oficial: DEJT, caderno administrativo, nº 4253,
p. 2-3, 30/06/2025). Cancelou as Súmulas 6 (itens I, II, VI "b" e X), 90, 114, 152, 219, 228, 268, 277,
**294**, 307, 311, 320, 329, **331 item I**, 366, **372 item I**, 375, 377, 423, 426, 429, 437, 439, 444,
449, 450 e 452; as OJs 14, 270, 355, 383 e 418 da SBDI-I; a OJ Transitória 36 da SBDI-I; a OJ 16 da SDC;
a OJ 13 do Pleno/Órgão Especial; e o Precedente Normativo 100.

Três atingiam a base e já foram corrigidos: **294** (prescrição total → art. 11, § 2º, da CLT),
**331, I** (a ficha usa os itens IV, V e VI, que sobreviveram) e **372, I**. Nenhuma OJ cancelada nem o
PN 100 aparecem na base.

- [ ] Reconferir esta lista sempre que uma ficha nova citar súmula do TST.
- [ ] Vale a mesma varredura para peças antigas reaproveitadas: modelo de 2018 pode citar verbete morto.
