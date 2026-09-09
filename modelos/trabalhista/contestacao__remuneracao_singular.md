# Modelo: Contestação — Complemento de Remuneração Singular (mudança de função gratificada)

**Consolidado de:** 1 contestação real minutada nesta base (2026-08-31/09-01).
**Formatação:** vem da skill **`formatar-minuta`** — fonte única, para toda peça da assessoria. Escrever a
minuta no `.md` com a marcação da skill e rodar
`python .claude/skills/formatar-minuta/scripts/gerar_minuta_docx.py <minuta.md> <saida.docx>`.
Nome do arquivo entregue: skill **`nomear-minuta`**.
**Este arquivo descreve só estrutura, teses e texto reaproveitável** — nunca formatação. O `.docx` do tema
(`contestacao__incorporacao_funcao.docx`) serve para colher **blocos literais** (a tese e a ementa do Tema
23, o bloco de equiparação), não para definir fonte, margem ou espaçamento.
O `.docx` da peça real **não entra no repositório** (contém nome de parte).
**Última atualização:** 2026-09-08 — remete a formatação à skill, adota a titulação dela e registra o
mapeamento de blocos e o cancelamento da Súmula 372, I.

---

## Quando usar este modelo

Use **este** modelo, e não `contestacao__incorporacao_funcao.md`, quando o caso reunir estas três marcas:

1. o objeto do pedido é a rubrica **"Complemento Remun. Singular"** (regime de remuneração singular), e não
   FAT/FAO/ITF/GPTF;
2. **não houve reversão ao cargo efetivo** — o Reclamante passou de uma função gratificada para **outra**
   função gratificada, e segue recebendo parcela de função;
3. a inicial **não invoca norma interna revogada** (Módulos 55/36), fundando-se apenas na Súmula 372, I, e no
   direito adquirido pré-reforma.

Presentes as três, o modelo `contestacao__incorporacao_funcao.md` fica largo demais: seu bloco 2 (normas
internas, Súmula 51, três variantes) não tem objeto, e sua ordem de mérito não ataca o ponto central, que
aqui é **a natureza da parcela**, não o requisito temporal.

Fichas de tese: [`teses/trabalhista/remuneracao_singular.md`](../../teses/trabalhista/remuneracao_singular.md)
(eixo do mérito) + [`teses/trabalhista/incorporacao_gratificacao_funcao.md`](../../teses/trabalhista/incorporacao_gratificacao_funcao.md)
(Tema 23, distinção de precedentes) + [`teses/trabalhista/temas_acessorios.md`](../../teses/trabalhista/temas_acessorios.md).

## Como gerar a peça (ordem das operações)

1. Escrever a minuta num `.md` com a marcação da skill `formatar-minuta` (`# tópico`, `## subtópico`,
   `> citação`, `@ENDERECAMENTO`, `@AUTOS`, `@POLO`, `@PREAMBULO`, `@FECHO`).
2. Colher do `.docx` do tema os **blocos literais** que se aproveitam — a tese e a ementa integral do Tema
   23, o bloco de equiparação à Fazenda Pública — e transcrevê-los como citação.
3. Rodar o script da skill para gerar o `.docx`.
4. Nomear o arquivo pela skill `nomear-minuta`.

Não montar o arquivo à mão nem partir do `.docx` do tema: a formatação é da skill.

## A escolha estrutural que faz a peça funcionar

Esta contestação **não se defende no requisito temporal** — e essa é a decisão de arquitetura.

Quando o Reclamante exerceu função gratificada por mais de dez anos antes de 11/11/2017, e a própria ficha
cadastral da ECT o comprova, disputar o requisito temporal é perder tempo em terreno perdido. A peça abandona
esse campo de propósito e ataca em dois eixos onde a prova é da ECT e é aritmética:

- **não houve reversão ao cargo efetivo** — logo a Súmula 372 não tem pressuposto de incidência; e
- **a parcela nunca foi fixa** — logo não há supressão de parcela integrada, e não há valor nominal a
  incorporar.

O núcleo persuasivo é o **item 3 do mérito**: quatro demonstrações extraídas da folha de pagamento do próprio
Reclamante. Ele carrega a peça sozinho. Montá-lo bem vale mais que qualquer ementa.

## Estrutura padrão

**Nomes dos tópicos principais: usar os da skill `formatar-minuta`** — `DA EQUIPARAÇÃO À FAZENDA PÚBLICA`,
`RESUMO DA VESTIBULAR`, `PRELIMINARMENTE`, `PREJUDICIAL DE MÉRITO`, `DO MÉRITO`, `DOS REQUERIMENTOS`.
Atenção: o `.docx` antigo do tema usa `RESUMO DA DEMANDA` e `DOS PEDIDOS`, que **não** são os nomes do
padrão — ao colher blocos literais dele, não trazer a titulação junto.

Subtópicos numerados manualmente, **reiniciando em 1 dentro de cada tópico principal**, com ` – ` (en dash)
como separador. Impugnação aos documentos e honorários **não** são tópicos próprios: são itens do mérito.

Como cada bloco de conteúdo se traduz na marcação da skill (é decisão de conteúdo, e a primeira vez
engana):

| Conteúdo | Marca |
|---|---|
| Ementa, dispositivo de lei, trecho da ficha cadastral, transcrição do MANPES | `>` (citação) |
| Quadro das reduções mês a mês · períodos de soma constante · a fórmula da parcela | `>>` (enumeração de valores) |
| Critérios do *ad cautelam* · impugnação de cada reflexo · prova em sentido contrário | `- (a)` (alínea de corpo) |
| Alíneas dos requerimentos | `+ a)` |

Nada de forma neste arquivo: fonte, margens, espaçamento, retângulo e recuos são da skill.

```
DA EQUIPARAÇÃO À FAZENDA PÚBLICA                     (tópico principal)
    DL 509/69 art. 12 · DL 779/69 art. 1º · RE 220.906/DF · RE 220.699/SP · tempestividade
    [fechar já aqui a ponte para o mérito: a equiparação submete a ECT ao art. 37, caput, CF, que lhe veda
     conceder vantagem remuneratória sem norma]
RESUMO DA VESTIBULAR                                 (tópico principal)
    Enunciar as PREMISSAS DE FATO da inicial e anunciar, uma a uma, que os documentos dela as desmentem.
    No caso real foram três: (a) teria sido "revertido" ao cargo efetivo; (b) a parcela seria "mensal fixa";
    (c) a substituição de rubrica seria inédita e ilícita. É o roteiro de leitura da peça.
PRELIMINARMENTE                                      (tópico principal)
  1. AUSÊNCIA DE DIREITO ADQUIRIDO – JULGAMENTO PELO C. TST DO INCJULGRREMBREP – 528-80.2018.5.14.0004
       Bloco reaproveitável LITERALMENTE do .docx do modelo: art. 468, §2º, CLT + tese fixada + ementa
       integral do Tema 23. Somar: fato gerador posterior a 11/11/2017; expectativa de direito; art. 8º,
       §2º, CLT; DISTINÇÃO DOS PRECEDENTES DA INICIAL PELAS DATAS que as próprias ementas declaram.
       Usar o item 9 da ementa (irredutibilidade = montante nominal das parcelas PERMANENTES) como ponte
       para o mérito.
       Somar o CANCELAMENTO do item I da Súmula 372 (Resolução nº 225/2025 do Pleno do TST, por perda de
       eficácia desde 11/11/2017): a inicial se apoia em enunciado que não existe mais, e cuja perda de
       eficácia antecede o ato impugnado. Ressalvar que o item II NÃO foi cancelado, e por que não é a
       hipótese quando a função foi ALTERADA, e não mantida. Manter a ressalva de conferência da fonte
       oficial (a base registra o dado com essa mesma reserva).
  2. DA INÉPCIA DO PEDIDO DE INDENIZAÇÃO POR DANO MORAL   [SE HOUVER pedido sem causa de pedir]
       arts. 840, §1º, CLT e 330, §1º, I e III, CPC; incongruência entre pedido e fundamentação; vício
       aritmético do valor. Se a inicial deduzir mais de uma causa de pedir para o mesmo pedido, arguir a
       INDETERMINAÇÃO e reservar-se para contestar todas, por eventualidade (arts. 141, 329 e 341 CPC).
  3. DA IMPUGNAÇÃO AO PEDIDO DE JUSTIÇA GRATUITA
       art. 790, §§3º e 4º, CLT; remuneração da ficha cadastral; a CLT disciplina a matéria e afasta o
       art. 99, §3º, CPC (art. 769 CLT); descontos de livre opção
PREJUDICIAL DE MÉRITO – PRESCRIÇÃO                   (tópico principal)
    Só do que couber. Se a inicial não datar o fato, arguir de forma CONDICIONAL e atribuir ao autor o ônus
    da data (art. 818, I, CLT). Dizer expressamente que NÃO se argui prescrição do pedido de incorporação
    quando o ato impugnado é recente — arguição inútil sinaliza fraqueza.
MÉRITO                                               (tópico principal)
  1. DA INEXISTÊNCIA DE REVERSÃO AO CARGO EFETIVO – INAPLICABILIDADE DA SÚMULA 372 DO C. TST
       Transcrever o enunciado grifando "revertê-lo a seu cargo efetivo"; transcrever a seção FUNÇÕES da
       ficha cadastral; demonstrar a continuidade e a parcela de função que segue sendo paga; afastar também
       o item II (a função não foi mantida, foi alterada); apontar a qualificação errada ("gerencial" x
       "Técnica"). Fechar: esta razão, isoladamente, basta.
  2. DA NATUREZA DA PARCELA – REMUNERAÇÃO SINGULAR E COMPLEMENTO DE REMUNERAÇÃO SINGULAR
       Transcrever MANPES Mód. 1 Cap. 1, itens 2.80, 2.171 e 2.37; reduzir a norma à fórmula
       (complemento = valor de tabela − salário); extrair a consequência (residual, variável, decrescente)
  3. DA PROVA DOCUMENTAL PRODUZIDA PELO PRÓPRIO RECLAMANTE            <- núcleo da peça
       1ª demonstração: soma "salário + parcela de função" constante; blocos de N competências; identidade
                        ao centavo com o valor de tabela da Tabela de Funções
       2ª demonstração: quadro mês a mês das reduções do complemento contra os aumentos de salário
                        (competência · antes -> depois · variação · aumento do salário), em citação recuada
       3ª demonstração: rubrica 056106 — devoluções do complemento recebido a maior, por exercício
       4ª demonstração: rubrica 051003 no lugar da 051106 em competências anteriores, sem protesto, e o
                        retorno de ofício ao regime singular com recálculo retroativo (056312 + 052313)
  4. DA INEXISTÊNCIA DE REDUÇÃO SALARIAL – PAGAMENTO DO VALOR MAIS VANTAJOSO PARA A NOVA FUNÇÃO
       Calcular o complemento singular que resultaria na nova função e compará-lo ao convencional;
       quantificar em reais a vantagem; mostrar o rateio pro rata do mês da transição; apontar a confusão
       de códigos de rubrica cometida pela inicial
  5. DA INEXISTÊNCIA DE OFENSA À IRREDUTIBILIDADE SALARIAL – SALÁRIO-CONDIÇÃO
       arts. 450, 468 e 499 CLT + o próprio MANPES ("mensal ou temporariamente", "pelo desempenho de função")
  6. DA INAPLICABILIDADE DA SÚMULA 372, I, DO C. TST À RECLAMADA
       equiparação à Fazenda Pública; art. 37, caput, CF; efeito antinormativo (cumulação de duas parcelas
       de função)
  7. AD CAUTELAM – DA METODOLOGIA E DO LIMITE DO VALOR A INCORPORAR
       Os três resultados insustentáveis do congelamento e os quatro critérios requeridos (apuração mês a
       mês pela fórmula; compensação integral; extinção ao alcançar o valor de tabela; ausência de reajuste
       autônomo). FECHAR com o Ag-AIRR-24942-23.2019.5.24.0007 transcrito pela PRÓPRIA INICIAL, que manda a
       incorporação seguir a metodologia da norma interna da ECT.
  8. DA IMPOSSIBILIDADE DE REAJUSTE DA PARCELA E DOS REFLEXOS PRETENDIDOS
  9. DA IMPROCEDÊNCIA DO PEDIDO DE INDENIZAÇÃO POR DANO MORAL
       Um subitem por causa de pedir efetivamente deduzida. No caso real foram quatro:
       9.1 a causa de pedir do pedido (assalto): ausência de prova + PROVA EM SENTIDO CONTRÁRIO da ficha
           cadastral (área de atividade, ausência de CAT, avaliações e elogios)
       9.2 a causa de pedir da fundamentação (constrangimento pela redução salarial): falta o ato ilícito;
           mero inadimplemento contratual não gera dano moral; a própria inicial qualifica o prejuízo como
           patrimonial; bis in idem com o pedido de diferenças; desproporção do valor
       9.3 a causa de pedir residual (represália sindical)
       9.4 subsidiariamente, do valor (art. 223-G, §1º, CLT: são TETOS, não pisos)
  10. DO ÔNUS DA PROVA        11. DA CORREÇÃO MONETÁRIA
  12. DOS DESCONTOS PREVIDENCIÁRIOS E FISCAIS        13. DA AUDIÊNCIA DE CONCILIAÇÃO
  14. DA IMPUGNAÇÃO AOS DOCUMENTOS E AOS VALORES
       Documentos no que excedem o próprio conteúdo; ementa inverificável; valor do pedido sem
       demonstrativo; valor da causa; limitação da condenação aos valores atribuídos (art. 492 CPC)
  15. DOS HONORÁRIOS ADVOCATÍCIOS
       art. 791-A CLT; faixa de 5% a 15%; base = liquidação/proveito econômico; sucumbência recíproca
DOS REQUERIMENTOS                                    (tópico principal)
    Alíneas espelhando cada bloco, na ordem, + protesto por provas + PREQUESTIONAMENTO expresso
    (art. 896, §1º-A, CLT), listando artigo por artigo
Fecho "Nesses Termos, / Pede Deferimento." + bloco de assinatura   (vem do .docx do modelo)
```

## Linguagem / trechos-padrão reaproveitáveis

- **Bloco de equiparação** e **bloco do Tema 23**: reaproveitáveis literalmente de
  `contestacao__incorporacao_funcao.md`.
- **Fórmula da parcela em display**, isolada num parágrafo recuado
  (`complemento = valor de tabela da função − salário do empregado`): é o que faz o juízo entender o caso em
  cinco segundos. Não diluir em prosa.
- **Quadro das reduções** em citação recuada, uma competência por linha. Não resumir em "houve diversas
  reduções": a força está na repetição visual e na coincidência exata dos valores.
- **Cada demonstração do item 3 do mérito abre com uma frase-título** ("Primeira demonstração: ..."), para que
  o leitor apressado colha a tese só pelos títulos.
- **Fórmula de fechamento de bloco autossuficiente**: "Esta razão, isoladamente, é suficiente para a
  improcedência." Usar com parcimônia — no caso real, só no item 1 do mérito.
- **Distinção de precedente pela data declarada na própria ementa**: "todos eles cuidam de empregados
  dispensados da função antes ou logo após a vigência da Lei nº 13.467/2017 — é o que se lê no próprio texto
  colacionado: [datas]. Nenhum deles enfrenta hipótese de dispensa da função ocorrida em [ano]."
- **Virar o precedente do autor**: "Sublinhe-se que essa não é tese da Reclamada, mas o que decidiu o
  precedente transcrito pela própria inicial."

## Variações observadas

- **Se houver reversão efetiva ao cargo efetivo**, o item 1 do mérito cai e a peça perde seu bloco mais forte:
  aí o eixo passa a ser os itens 2 e 3 do mérito (natureza da parcela) e o item 7 (limitação do valor), e o requisito temporal
  volta a importar.
- **Se a inicial invocar norma interna** (Módulos 55/36) além da Súmula 372, acrescentar o bloco 2 de
  `contestacao__incorporacao_funcao.md` e a prejudicial de prescrição total (Súmula 294/TST).
- **Se o requisito temporal NÃO estiver cumprido antes de 11/11/2017**, inverter a ordem: a preliminar 1 (Tema 23)
  vira o eixo e o item 3 do mérito passa a reforço.
- **Se não houver pedido de dano moral**, suprimir a preliminar 2 e o item 9 do mérito.

## Lacuna deste modelo

- [ ] O `.docx` do tema está em Times New Roman 12 com margens 4/1,5/2,6/1,6, fora do padrão da skill
      `formatar-minuta` (Arial 11, margens 3/2/3/2). Ele segue útil pelos **blocos literais**; convém
      reformatá-lo ou marcá-lo como fonte só de texto, para não induzir erro de formatação de novo.
- [ ] Estrutura ainda **não testada em sentença**. Registrar aqui o que o juízo acolheu e o que rejeitou —
      em especial se o item 1 do mérito (ausência de reversão) foi enfrentado, e como o juízo tratou o pedido
      *ad cautelam* de metodologia do item 7 do mérito.
