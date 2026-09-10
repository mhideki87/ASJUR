# Modelo: Complementação das razões do Recurso Ordinário — embargos da parte adversa acolhidos com efeito infringente

**Consolidado de:** 1 caso-fonte — rito sumaríssimo, ECT no polo passivo, recurso ordinário já interposto
quando os embargos da parte adversa foram acolhidos com efeito infringente (caso identificado só pelo tema;
nenhum dado de parte ou processo aqui).
**Última atualização:** 2026-09-10 — criação do modelo.

---

## Quando usar este modelo

A ECT **já interpôs** o recurso ordinário, e só depois a parte adversa obteve, em embargos de declaração,
**efeito infringente** — um capítulo indeferido na sentença passa a deferido. O capítulo condenatório é
novo: nasceu depois do recurso e por isso não está impugnado nas razões originais.

A via é o **art. 1.024, § 4º, do CPC** (aplicável por força do art. 769 da CLT): o embargado que já
interpôs recurso tem o direito de **complementar ou alterar suas razões, nos exatos limites da
modificação**.

**Não é aditamento livre.** O que a decisão integrativa não modificou continua regido pelas razões
originais e não pode ser reaberto aqui. Se os embargos da parte adversa foram **rejeitados** ou não
alteraram a conclusão, não há complementação a fazer: o recurso já interposto é processado e julgado
independentemente de ratificação (art. 1.024, § 5º, do CPC).

Distingue-se de `contraminuta_ed__*`, que é a resposta aos embargos **antes** de julgados. Este modelo é o
que vem **depois**, quando a resposta não impediu a modificação.

## Estrutura padrão

Formatação: não repetir medidas aqui — o padrão visual vem da skill `formatar-minuta`.

```
── PETIÇÃO DE JUNTADA (à Vara do Trabalho) ──────────────────────
Endereçamento + autos + rótulos RECORRENTE / RECORRIDA
Preâmbulo — qualificação abreviada + art. 1.024, § 4º, do CPC + Id do RO já interposto
  — tempestividade (ver "Prazo" abaixo)
  — preparo: nada a recolher; a complementação não é recurso autônomo
  — pedido de juntada e remessa ao TRT24 com o recurso já interposto
Fecho + assinatura
── RAZÕES COMPLEMENTARES (ao TRT da 24ª Região) ─────────────────
[RETÂNGULO] DA DELIMITAÇÃO: OS EXATOS LIMITES DA MODIFICAÇÃO
[RETÂNGULO] DO MÉRITO
             1 – o capítulo novo (padrão de quatro movimentos do modelo de RO)
             1.1 – coerência interna da premissa, quando couber
             2 – subsidiariamente: base de cálculo do capítulo novo
             3 – consequência direta sobre a sucumbência já fixada
[RETÂNGULO] DO PREQUESTIONAMENTO EXPLÍCITO
[RETÂNGULO] DOS REQUERIMENTOS
Fecho + assinatura
```

## O tópico da delimitação — o que faz esta peça ser admissível

É o tópico que demonstra respeito ao limite legal, e por isso vem primeiro. Três movimentos:

1. **O que a decisão integrativa NÃO modificou** — dizer expressamente que, quanto a esses pontos, nada há
   a complementar. Se algum ponto foi negado à parte adversa, registrar: é resultado favorável que
   delimita o objeto.
2. **O que ela modificou** — identificar o capítulo novo e por que ele não podia estar nas razões
   originais (foi indeferido na sentença; passou a deferido depois do recurso).
3. **A reiteração** — "todos os demais capítulos permanecem impugnados nos exatos termos das razões
   originais, que aqui se reiteram integralmente".

## Prazo — a dúvida que o modelo carrega

`[REVISAR: conferir o entendimento do TRT da 24ª Região]` O art. 1.024, § 4º, do CPC fala em **15 dias**;
no processo do trabalho é discutível se prevalece o prazo do próprio recurso (**8 dias**, art. 895 da CLT,
em dobro pelo art. 1º, III, do DL 779/69). **Redigir a tempestividade cobrindo os dois critérios e
protocolar dentro do menor** — a peça do caso-fonte foi escrita assim.

## Linguagem / trechos-padrão reaproveitáveis

- **Fundamento de admissibilidade** (literal): *"com fundamento no art. 1.024, § 4º, do CPC, aplicável
  subsidiariamente por força do art. 769 da CLT, apresentar COMPLEMENTAÇÃO DAS RAZÕES DO RECURSO ORDINÁRIO
  já interposto (Id. [ID DO RO]), nos exatos limites da modificação promovida pela r. decisão de embargos
  de declaração de Id. [ID]"*.
- **Preparo** (literal): *"Não há preparo a recolher: além de a Recorrente ser isenta de custas e de
  depósito recursal (art. 1º, IV e VI, do Decreto-Lei nº 779/69), a complementação não constitui recurso
  autônomo."*
- **Reiteração das razões originais** (literal): ver o terceiro movimento do tópico da delimitação.
- **Capítulo de mérito**: mesmo padrão de quatro movimentos do
  [`recurso_ordinario__sentenca_primeiro_grau.md`](recurso_ordinario__sentenca_primeiro_grau.md) — o que a
  decisão decidiu (transcrever) → por que está errada → consequência concreta → pedido específico.

## A técnica que este modelo acrescenta: a premissa da decisão contra ela mesma

Decisão que acolhe embargos com efeito infringente costuma fundamentar-se em **poucas linhas**, e é aí que
se encontra a alavanca: uma premissa adotada para um efeito, que o julgado não aplica ao outro.

No caso-fonte, ao deferir a dobra de férias a decisão deslocou o termo final do período aquisitivo
justificando-o pela **suspensão do contrato** — reconhecendo, portanto, que a suspensão repercute na
disciplina das férias. Mas era a mesma suspensão que, pela norma interna, disparava a exclusão automática
da programação, fato que a decisão desconsiderou ao aferir a quem era imputável o atraso. Acolher o efeito
da suspensão para um lado e desconsiderá-lo para o outro é aplicar a mesma premissa em dois sentidos.

Como procurar: isolar cada premissa que a decisão **adotou** (não as que rejeitou) e perguntar se ela,
levada a sério, não decide também o ponto contrário.

## O capítulo que não se pode esquecer: a sucumbência

Modificação com efeito infringente **realoca a sucumbência**, e o efeito pode ser grande sem aparecer no
dispositivo. No caso-fonte, honorários já deferidos à ECT sobre "o valor do pedido indeferido" esvaziaram-se
quase por inteiro, porque o pedido depois deferido era a maior parcela indeferida.

Pedir a **readequação ao resultado final do julgamento** (art. 791-A, § 3º, da CLT), mantida a suspensão de
exigibilidade do § 4º quando houver justiça gratuita. Cabe nos "exatos limites", por ser consequência
direta da modificação — e é preciso pedir, porque a ECT não teve oportunidade de se manifestar sobre esse
efeito reflexo antes da decisão.

## Variações observadas

- **Embargos rejeitados** — modelo inaplicável; art. 1.024, § 5º, do CPC (nem ratificação é exigida).
- **Recurso ainda não interposto** quando sai a decisão integrativa — não é caso de complementação: o
  capítulo novo entra no próprio recurso ordinário, pelo modelo
  [`recurso_ordinario__sentenca_primeiro_grau.md`](recurso_ordinario__sentenca_primeiro_grau.md).
- **Modificação em mais de um capítulo** — repetir o padrão de quatro movimentos por capítulo, mantendo a
  numeração corrida e o tópico da delimitação nomeando todos.

## Ligação com a base de teses

- Tema do caso-fonte (dobra de férias após afastamento):
  [teses/trabalhista/afastamentos_auxilio_doenca.md](../../teses/trabalhista/afastamentos_auxilio_doenca.md)
- Prerrogativas e preparo:
  [teses/transversal/prerrogativas_processuais_ect.md](../../teses/transversal/prerrogativas_processuais_ect.md)
- Peça anterior do fluxo: [contraminuta_ed__honorarios_sucumbenciais.md](contraminuta_ed__honorarios_sucumbenciais.md)
- Padrão visual: skill `formatar-minuta`; nome do arquivo entregue: skill `nomear-minuta` (`Adit RO`).

## Par `.docx`

Não é necessário: o corpo não tem estrutura visual própria — dois blocos de qualificação e tópicos em
retângulo, tudo já coberto pela skill `formatar-minuta` a partir de `modelos/_FORMATO_BASE.docx`.
