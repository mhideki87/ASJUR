# Playbook de prompts — Contencioso Trabalhista ECT

> Complemento da `base_conhecimento_juridico_ECT.md`.
> Cole a base no Projeto; use os prompts abaixo no dia a dia.
> Convenção: `<...>` = você preenche. `[REVISAR: ...]` = marcação que eu devo deixar no documento.

---

## 0. Regras que valem para todo prompt

Se a base já estiver nas instruções do Projeto, não precisa repetir. Fora do Projeto, cole este bloco no fim de qualquer pedido:

```
REGRAS FIXAS:
- Não invente jurisprudência, doutrina, número de processo, data, Id de documento
  ou cláusula de ACT. Use apenas o que consta dos autos anexados, da peça-modelo
  ou do recurso adversário.
- Onde faltar informação, escreva [REVISAR: o que precisa ser conferido] no corpo
  do texto — não preencha com conteúdo plausível.
- Ao final, liste separadamente tudo que exige conferência humana antes do protocolo.
- Se a defesa e a sentença divergirem quanto aos fatos, apoie-se na sentença e na
  capa do PJe.
```

---

## 1. Etapa de análise (sempre antes da minuta)

### 1.1 Análise de petição inicial
```
Analise a petição inicial anexada (ECT no polo passivo) e estruture assim:

1. IDENTIFICAÇÃO — processo, vara, rito, valor da causa, data de ajuizamento,
   período contratual, cargo/função do Reclamante.
2. PEDIDOS — liste um a um, com o valor atribuído a cada um.
3. CAUSA DE PEDIR — fatos e fundamentos por pedido.
4. DOCUMENTOS JUNTADOS — quais são e o que provam de fato (não o que a inicial
   diz que provam).
5. TESES DA ECT APLICÁVEIS — para cada pedido, indique qual das teses recorrentes
   da base se aplica e com que força.
6. PONTOS FRÁGEIS DA INICIAL — prescrição, ausência de prova, contradição de datas,
   pedido genérico, incompatibilidade com o rito.
7. RISCOS — onde a ECT tende a sucumbir e por quê.
8. O QUE FALTA NOS AUTOS para montar a defesa (documentos a requisitar à área).

Ainda não redija a contestação.
```

### 1.2 Análise de sentença (antes de recorrer ou contrarrazoar)
```
Analise a sentença anexada e estruture:

1. DISPOSITIVO — o que foi deferido e indeferido, pedido a pedido.
2. FUNDAMENTOS DE CADA CAPÍTULO — resumo fiel, com a referência do item da sentença.
3. CAPÍTULOS FAVORÁVEIS À ECT — e quais fundamentos sustentam cada um (servirão
   para contrarrazões).
4. CAPÍTULOS DESFAVORÁVEIS — e se há tese da ECT que a sentença deixou de enfrentar
   (relevante para embargos de declaração / prequestionamento).
5. PREQUESTIONAMENTO — dispositivos e súmulas expressamente enfrentados, e os que
   ficaram de fora.
6. RECOMENDAÇÃO — embargos, recurso ordinário, ou aguardar. Justifique.
```

### 1.3 Análise de Recurso Ordinário do Reclamante
```
Analise o Recurso Ordinário anexado e estruture:

1. CAPÍTULOS IMPUGNADOS e o que o Recorrente pede em cada um.
2. ARGUMENTOS NOVOS — o que não estava na inicial (possível inovação recursal).
3. JURISPRUDÊNCIA INVOCADA — para cada aresto, aponte se é aplicável ao caso ou se
   cabe *distinguishing* (diferença de fato ou de norma interna).
4. PONTOS EM QUE A SENTENÇA JÁ RESPONDE ao recurso — cite o item.
5. TESES DA CONTESTAÇÃO a reiterar *ad cautelam*, caso a sentença seja reformada.
6. TEMPESTIVIDADE — verifique e sinalize [REVISAR] nas datas que não constarem.
```

---

## 2. Etapa de redação

### 2.1 Contestação
```
Com base na análise acima, redija a contestação da ECT em .odt, replicando
integralmente a formatação (cabeçalho, fonte, espaçamento, rodapé, bloco de
assinatura) do arquivo <MODELO.odt> anexado.

ESTRUTURA:
I    — Endereçamento, qualificação e tempestividade (prazo em dobro, DL 779/69)
II   — Síntese da inicial sob a ótica da defesa
III  — Preliminares e prejudiciais (prescrição total — Súmula 294/TST)
IV   — Mérito, pedido a pedido, na ordem da inicial
V    — Impugnação aos documentos e ao valor da causa
VI   — Requerimentos, provas e prequestionamento

Impugne especificamente cada fato e cada pedido. Não deixe pedido sem resposta.
```

### 2.2 Contrarrazões de Recurso Ordinário
```
Redija contrarrazões ao RO do Reclamante em .odt, com a formatação do
<MODELO.odt> anexado.

Conteúdo: defenda o acerto da sentença usando (a) os próprios fundamentos da
decisão, (b) os argumentos da contestação anexada, (c) fundamentos jurídicos
adicionais que você identificar com segurança.

ESTRUTURA:
- Petição de juntada à <Nª> Vara do Trabalho de Campo Grande/MS
- Razões endereçadas ao TRT da 24ª Região
I    — Síntese
II   — Tempestividade (prazo em dobro; dispensa de preparo)
III  — Prejudicial de prescrição, se aplicável
IV   — Mérito, capítulo a capítulo, com *distinguishing* dos arestos do recurso
V    — Ad cautelam: reiteração das teses da contestação para o caso de reforma
VI   — Requerimentos com prequestionamento expresso
```

### 2.3 Recurso de Revista
```
Redija recurso de revista contra o acórdão anexado, formatação do <MODELO.odt>.

Para cada tema, obedeça à estrutura de admissibilidade:
- transcrição do trecho do acórdão que consubstancia o prequestionamento
  (art. 896, §1º-A, I, da CLT)
- indicação expressa do dispositivo violado / súmula contrariada / divergência
- demonstração analítica do conflito (art. 896, §1º-A, III)
- no rito sumaríssimo, apenas ofensa direta à CF ou contrariedade a súmula do
  TST / súmula vinculante (art. 896, §9º, CLT)

Se algum requisito não estiver satisfeito pelos autos, sinalize [REVISAR] em vez
de forçar o enquadramento.
```

### 2.4 Quesitos de perícia médica
```
Formule quesitos para perícia médica judicial, com a formatação do <MODELO.odt>,
organizados em blocos que sustentem as teses da ECT:

I   — Metodologia e fontes (separar achado clínico objetivo de relato do periciando)
II  — Diagnóstico e capacidade (parcial/temporária, reversibilidade, DCB do INSS)
III — Nexo causal (etiologia multifatorial, fatores extralaborais, espécie 31 x 91,
      NTEP/CNAE, art. 20, §1º, Lei 8.213/91; quantificação de eventual concausa)
IV  — Culpa (exames admissional e periódicos, PCMSO, riscos psicossociais, ausência
      de comunicação prévia; exigir do perito a norma específica supostamente violada)
V   — Ad cautelam (percentuais por tabela objetiva, capacidade residual)
VI  — Requerimentos finais (impugnação, quesitos complementares, assistente técnico)

Extraia os fatos da contestação anexada. CIDs e datas devem vir dos laudos —
se não constarem, marque [REVISAR].
```

### 2.5 Quesitos de perícia técnica (insalubridade/periculosidade)
```
Mesmo padrão do item anterior, com blocos:
I — atividades efetivamente exercidas e tempo de exposição
II — agente insalubre alegado, enquadramento na NR-15 e limite de tolerância
III — EPIs fornecidos, CA, treinamento e fiscalização do uso (Súmula 289/TST)
IV — periculosidade: enquadramento na NR-16, habitualidade e área de risco
V — ad cautelam: grau e base de cálculo
```

### 2.6 Embargos de declaração
```
Redija embargos de declaração contra a decisão anexada, formatação do <MODELO.odt>.

Aponte, um a um: omissão / contradição / obscuridade / erro material, indicando
para cada vício o trecho exato da decisão e a tese ou dispositivo não enfrentado.
Requeira o prequestionamento explícito (Súmula 297/TST).
Não use os embargos para rediscutir mérito — se não houver vício real, diga isso
em vez de redigir a peça.
```

### 2.7 Contraminuta a embargos de declaração do Reclamante
```
Redija contraminuta aos embargos de declaração anexados, com a formatação da skill peca-ect.

Antes de redigir, decida e me diga: o vício alegado existe? Se existir, NÃO gaste a peça
negando-o — concentre a defesa no que ainda está em disputa (critério de cálculo, alcance
do suprimento, condicionalidade). Se não existir, diga isso e sustente a inexistência.

ESTRUTURA:
- Endereçamento com o fundamento da oitiva (art. 897-A, §2º, CLT; art. 1.023, §2º, CPC)
I   — Delimitação do objeto dos embargos e limites do suprimento
II  — Mérito, tópico a tópico
III — Requerimentos, com prequestionamento

Aponte também se o acolhimento abre prazo para complementar recurso já interposto
(art. 1.024, §4º, CPC).
```

---

## 3. Prompts de apoio

### 3.1 Revisão antes do protocolo
```
Revise a minuta anexada como se fosse conferi-la antes do protocolo. Verifique:
- algum pedido da inicial ficou sem impugnação específica?
- há contradição interna de datas, valores ou nomes?
- há citação de jurisprudência sem fonte nos autos?
- os requerimentos finais correspondem às teses desenvolvidas?
- o prequestionamento cobre todos os dispositivos discutidos?
Liste apenas os problemas, com a localização de cada um. Não reescreva a peça.
```

### 3.2 Teste da tese adversa
```
Assuma a posição do Reclamante e ataque a minuta anexada: quais são os três
argumentos mais fortes contra ela e como o juízo provavelmente responderia?
Depois indique o que eu deveria reforçar na peça.
```

### 3.3 Conversão de formato
```
Converta o arquivo anexado para .docx (ou .odt) mantendo integralmente a
formatação. Confirme depois: paginação, margens, fontes, cabeçalho com logotipo,
rodapé e numeração.
```

### 3.4 Reaproveitamento de peça
```
Adapte a peça anexada (processo <X>) para o processo <Y>, cujos documentos seguem.
Substitua partes, número do processo, vara e datas. Marque [REVISAR] em toda
informação do processo antigo que eu preciso conferir se procede no novo — em
especial períodos contratuais, funções exercidas e Ids de documentos.
Aponte quais teses da peça original NÃO se aplicam ao novo caso.
```

---

## 4. Erros a evitar nos pedidos

| Pedido ruim | Por quê | Versão melhor |
|---|---|---|
| "Faça a contestação" (sem análise antes) | a minuta sai genérica | peça a análise primeiro, na mesma conversa |
| "Cite jurisprudência favorável" | convite à invenção | "use apenas ementas dos autos; se faltar, marque [REVISAR]" |
| Dois processos na mesma conversa | contamina fatos e datas | uma conversa por processo |
| Anexar só a inicial | defesa sem lastro | anexe também os documentos da ECT e a peça-modelo |
| "Melhore isso" | vago | diga o que está errado ou peça a revisão do item 3.1 |

---

## 5. Checklist de anexos por tipo de peça

| Peça | Anexar |
|---|---|
| Contestação | inicial · documentos da ECT · peça-modelo · ACT vigente |
| Contrarrazões | RO do Reclamante · sentença · contestação · peça-modelo |
| Recurso de revista | acórdão · embargos e decisão dos embargos · peça-modelo |
| Quesitos | contestação · laudos e documentos do INSS · peça-modelo |
| Embargos | decisão embargada · peça em que a tese omitida foi deduzida |
| Contraminuta a embargos | embargos do Reclamante · decisão embargada · inicial (para o pedido tido por omitido) |

---

## 6. Protocolo de atualização da base (teses + modelos)

Objetivo: depois de algumas sessões sobre o mesmo tema, eu não deveria mais precisar anexar uma peça-modelo
antiga — o esqueleto da peça já deve estar salvo em `modelos/`, e a tese já deve estar em
`base_conhecimento_juridico_*.md`. Isso só acontece se dois passos forem seguidos: um **antes** de anexar, e
um **ao final** de cada sessão em que algo for minutado.

### 6.1 Antes de anexar uma peça-modelo antiga (passo novo)

```
Antes de eu anexar um modelo antigo: use modelos/_FORMATO_BASE.docx (via GitHub) como formatação
geral desta peça — fonte, cabeçalho, rodapé, fecho e assinatura já vêm dali, para qualquer tipo de
peça. Ajuste o bloco de qualificação (endereçamento, rótulos de polo, fundamentação legal de
admissibilidade) conforme o tipo de peça desta sessão.
Além disso, verifique em modelos/<área>/ se já existe o par <tipo_peca>__<tema>.md (+ .docx, se
houver) para esta peça + tema. Se existir, use o .md como base de estrutura/tese — não peça o anexo
de uma peça-modelo antiga. Se não existir, ou se estiver desatualizado, me avise e eu anexo o modelo.
```

Isso evita reanexar o que já foi consolidado — a formatação geral vem sempre de `_FORMATO_BASE.docx`;
a tese/estrutura do tema vem do `.md` correspondente. Só volte a anexar uma peça antiga quando o tema for
novo, o modelo salvo estiver incompleto, ou o caso trouxer uma variação de estrutura que valha preservar
num `.docx` próprio do tema.

### 6.2 Ao final de qualquer sessão de minuta

```
Antes de encerrarmos: revise esta conversa e aponte, separadamente:
1. TESE NOVA — algum argumento usado aqui não está na base de conhecimento anexada?
2. CORREÇÃO — alguma tese da base se mostrou errada, incompleta ou foi contestada
   com sucesso pela parte contrária neste processo?
3. JURISPRUDÊNCIA NOVA — algum precedente citado aqui (dos autos ou anexado por mim)
   ainda não consta da base?
4. MODELO (estrutura) — o modelo estrutural usado nesta sessão já está salvo em modelos/*.md? Se não
   estiver, ou se este caso revelou uma variação relevante, proponha a criação/atualização do arquivo
   em modelos/<área>/<tipo_peca>__<tema>.md (a partir de modelos/_TEMPLATE.md), sem nenhum dado que
   identifique o cliente ou o processo.
5. MODELO (visual, .docx) — se eu anexei uma peça-modelo real nesta sessão e ainda não existe o
   .docx correspondente em modelos/<área>/, produza uma cópia anonimizada preservando integralmente
   fonte, margens, cabeçalho/logotipo, rodapé, numeração e bloco de assinatura, substituindo todo dado
   identificável por placeholder. Aponte também se algum metadado do arquivo (autor, revisões,
   comentários) precisa ser limpo antes do commit.
6. Para cada item acima, escreva o trecho EXATO a acrescentar/alterar (ou o arquivo .docx anonimizado
   a gerar), pronto para eu revisar e commitar no GitHub.
Se nada for novo, diga isso explicitamente — não force um "achado" apenas para preencher a resposta.
```

Regras deste protocolo:
- Claude nunca commita sozinho sem eu revisar o resultado — teses, modelos estruturais e modelos
  visuais (.docx) entram só depois da minha aprovação explícita.
- Toda tese ou modelo novo entra como candidato — soma à seção/arquivo correspondente, não substitui o que já
  existe, a menos que eu confirme que o anterior estava errado ou desatualizado.
- Modelo (estrutural ou .docx) nunca leva nome de cliente, nº de processo, CPF ou qualquer dado
  identificável — nem no corpo, nem em metadados do arquivo (ver `modelos/README.md`).
- Se o commit for feito por mim direto no GitHub (app ou site), não precisa repetir o protocolo na mesma
  conversa. Se for pedir para o Claude commitar via connector do GitHub, confirme o resultado primeiro —
  e verifique se esse connector consegue mesmo subir arquivo binário (.docx); se não conseguir, essa etapa
  precisa ser feita numa sessão com acesso a git (Claude Code).
