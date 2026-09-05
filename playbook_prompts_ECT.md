# Playbook de prompts — Contencioso Trabalhista ECT

> Complemento de `CONTEXTO.md` + `INDICE.md` + fichas de `teses/`.
> Cole o `CONTEXTO.md` e o protocolo de leitura do `INDICE.md` nas instruções do Projeto; use os prompts
> abaixo no dia a dia. Este arquivo também é lido **por seção**, não inteiro: vá direto na seção do tipo
> de peça da sessão.
> Convenção: `<...>` = você preenche. `[REVISAR: ...]` = marcação que eu devo deixar no documento.

---

## 0. Regras que valem para todo prompt

Se o `CONTEXTO.md` já estiver nas instruções do Projeto, não precisa repetir. Fora do Projeto, cole este bloco no fim de qualquer pedido:

```
REGRAS FIXAS:
- Antes de responder: leia CONTEXTO.md e a tabela de roteamento de INDICE.md, e
  abra SÓ as fichas de teses/ cujo gatilho bater com os pedidos deste processo.
  Não leia a base inteira. Se nenhum gatilho bater, diga isso e trate como tema novo.
- Ficha com status: rascunho é candidata a tese, não tese confirmada — valide contra
  os autos antes de usar e não cite como jurisprudência pronta.
- Não invente jurisprudência, doutrina, número de processo, data, Id de documento
  ou cláusula de ACT. Use apenas o que consta dos autos anexados, da peça-modelo
  ou do recurso adversário.
- Onde faltar informação, escreva [REVISAR: o que precisa ser conferido] no corpo
  do texto — não preencha com conteúdo plausível.
- Ao final, liste separadamente tudo que exige conferência humana antes do protocolo.
- Se a defesa e a sentença divergirem quanto aos fatos, apoie-se na sentença e na
  capa do PJe.
- Formatação: use SEMPRE o padrão único da skill formatar-minuta (Arial 11,
  entrelinha exata de 18 pt, margens 3/2/3/2 cm, tópico principal em caixa alta
  dentro de retângulo, subtópicos numerados em negrito sublinhado, cabeçalho/rodapé
  e assinatura de modelos/_FORMATO_BASE.docx). Peça-modelo anexada serve para
  estrutura e tese, nunca para formatação. Sem nota de rodapé.
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
5. TESES DA ECT APLICÁVEIS — para cada pedido, indique qual ficha de teses/ se
   aplica (pelo gatilho do INDICE.md) e com que força. Liste também as fichas que
   você NÃO abriu e por quê, para eu conferir se faltou alguma.
6. PONTOS FRÁGEIS DA INICIAL — prescrição, ausência de prova, contradição de datas,
   pedido genérico, incompatibilidade com o rito.
7. RISCOS — onde a ECT tende a sucumbir e por quê.
8. O QUE FALTA NOS AUTOS para montar a defesa (documentos a requisitar à área).
9. PRAZOS AUTÔNOMOS que correm antes da contestação — em especial o pedido de
   adesão ao "Juízo 100% Digital": pela RA TRT24 nº 40/2021, art. 4º, §§ 2º e 3º,
   o silêncio da ECT por 5 dias úteis contados da primeira notificação vale como
   ANUÊNCIA TÁCITA. Se houver interesse em audiência de instrução presencial, a
   recusa é manifestação própria e não pode esperar o prazo da defesa.

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
   (é o que gera tópico de embargos de declaração).
5. PREQUESTIONAMENTO — dispositivos e súmulas expressamente enfrentados, e os que
   ficaram de fora (insumo do RECURSO, não dos embargos — ver 2.6).
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
Com base na análise acima, redija a contestação da ECT no padrão de formatação da
skill formatar-minuta (entrega em .docx gerado de modelos/_FORMATO_BASE.docx).

ESTRUTURA:
I    — Endereçamento, qualificação e tempestividade (prazo em dobro, DL 779/69)
II   — Síntese da inicial sob a ótica da defesa
III  — Preliminares e prejudiciais (prescrição total — art. 11, § 2º, da CLT; a Súmula 294 foi cancelada)
IV   — Mérito, pedido a pedido, na ordem da inicial
V    — Impugnação aos documentos e ao valor da causa
VI   — Requerimentos, provas e prequestionamento

Impugne especificamente cada fato e cada pedido. Não deixe pedido sem resposta.
```

### 2.2 Contrarrazões de Recurso Ordinário
```
Redija contrarrazões ao RO do Reclamante no padrão da skill formatar-minuta.

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
Redija recurso de revista contra o acórdão anexado, no padrão da skill
formatar-minuta.

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
Formule quesitos para perícia médica judicial, no padrão da skill formatar-minuta,
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
Redija embargos de declaração contra a decisão anexada, no padrão da skill
formatar-minuta.

Aponte, um a um: omissão / contradição / obscuridade / erro material, indicando
para cada vício o trecho exato da decisão e a tese ou dispositivo não enfrentado.
NÃO inclua seção de prequestionamento nem alínea de prequestionamento nos
requerimentos — isso vai no recurso, não nos embargos. A única exceção é o
pedido subsidiário DENTRO do tópico, quando a súmula ou o dispositivo é o
próprio eixo do vício (ex.: "...e, subsidiariamente, o pronunciamento explícito
sobre o verbete, para fins de prequestionamento").
Seja econômico: só vícios de alta convicção. Migre para o recurso tudo que
dependa de requalificar o que o juízo decidiu, que não tenha sido deduzido
especificamente na defesa, que seja erro material de baixo impacto econômico,
ou que seja objeção subsidiária de mérito.
Não use os embargos para rediscutir mérito — se não houver vício real, diga isso
em vez de redigir a peça.
```

Para sentença de 1º grau existe modelo consolidado:
`modelos/trabalhista/embargos_declaracao__sentenca_primeiro_grau.md` (+ `.docx`) — traz o padrão de cinco
movimentos de cada tópico, o bloco recorrente da ECT (honorários de sucumbência recíproca, prerrogativas da
Fazenda Pública, EC 113/2021, planilhas anexas), o registro de estilo e o checklist de leitura da sentença —
cujo item 0 manda **conferir na fonte oficial** toda súmula que for sustentar um tópico.

**Padrão confirmado (08/2026):** embargos **sem seção de prequestionamento** — ele é do recurso. E peça
**enxuta**: no caso-fonte a minuta foi de 15 para 7 tópicos, com numeração corrida, sem subdividir por espécie
de vício. Um ED com 15 tópicos lê-se como inconformismo; com 7, como apontamento técnico.

### 2.7 Recurso Ordinário
```
Redija recurso ordinário contra a sentença anexada, formatação do <MODELO.odt>.

ESTRUTURA (duas peças no mesmo arquivo, com quebra de página entre elas):
- Petição de juntada à <Nª> Vara do Trabalho de Campo Grande/MS — tempestividade
  (8 dias em dobro, dias úteis, contados da publicação da decisão de embargos, que
  interromperam o prazo) e preparo (isenção de custas e de depósito recursal)
- Razões endereçadas ao TRT da 24ª Região:
I   — Síntese da demanda e da decisão recorrida
II  — Preliminar de nulidade por negativa de prestação jurisdicional (SÓ se houve
      embargos apontando a omissão e a decisão integrativa não a sanou; sempre com
      pedido subsidiário de julgamento imediato — art. 1.013, §3º, IV, do CPC)
III — Mérito, capítulo a capítulo, do mais forte para o mais fraco
IV  — Prequestionamento explícito (aqui sim — só do que foi debatido no corpo)
V   — Requerimentos

Cada capítulo de mérito em quatro movimentos: o que a sentença decidiu (transcrever)
→ por que está errada (fato, prova e norma, nomeando o ônus da prova) → a
consequência concreta se subsistir → o pedido de reforma, específico.

Leia a decisão de embargos procurando material aproveitável CONTRA ela: prerrogativa
processual reconhecida (blinda o preparo), erro material admitido (reforça iliquidez),
contradição interna (sustenta a preliminar), qualificação branda do fato no dano moral.

NÃO recorra do que está perdido nem do que já se ganhou nos embargos — diga isso
expressamente em vez de incluir o capítulo.
```

Modelo consolidado: `modelos/trabalhista/recurso_ordinario__sentenca_primeiro_grau.md` (+ `.docx`).

---

## 3. Prompts de apoio

### 3.1 Revisão antes do protocolo
```
Revise a minuta anexada como se fosse conferi-la antes do protocolo. Verifique:
- algum pedido da inicial ficou sem impugnação específica?
- há contradição interna de datas, valores ou nomes?
- há citação de jurisprudência sem fonte nos autos?
- os requerimentos finais correspondem às teses desenvolvidas?
- se a peça for recurso: o prequestionamento cobre todos os dispositivos
  discutidos? (em embargos de declaração não se aplica — ver 2.6)
Liste apenas os problemas, com a localização de cada um. Não reescreva a peça.
```

### 3.2 Teste da tese adversa
```
Assuma a posição do Reclamante e ataque a minuta anexada: quais são os três
argumentos mais fortes contra ela e como o juízo provavelmente responderia?
Depois indique o que eu deveria reforçar na peça.
```

### 3.3 Reformatação de peça fora do padrão
```
Reformate o arquivo anexado no padrão da skill formatar-minuta, sem alterar o
texto. Confirme depois, item por item: margens 3/2/3/2 cm, Arial 11, entrelinha
exata de 18 pt, tópicos principais em caixa alta dentro de retângulo, numeração
dos subtópicos reiniciando em cada tópico, cabeçalho com logotipo, rodapé com
endereço e numeração, fecho e assinatura, ausência de nota de rodapé.
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
| Reaproveitar peça-modelo sem conferir as datas do caso | argumento de modulação temporal vira autofágico (ex.: ADI 5322, efeitos _ex nunc_ de 12/07/2023, invocada em contrato posterior) | "confira as datas do contrato contra o marco temporal antes de repetir o argumento; se não servir, diga e proponha outro" |
| Pedir honorários/impugnar honorários sem checar o dispositivo | a parte autora costuma pedir pelo art. 85, § 3º, do CPC "pela equiparação à Fazenda Pública"; no processo do trabalho é o art. 791-A da CLT | "confira o dispositivo dos honorários no pedido e impugne se vier pelo CPC" |
| Aceitar a formatação "parecida" | cabeçalho, rodapé e estilos precisam ser os do arquivo real | anexe o `.docx`/`.odt` e peça: "reconstrua a peça sobre o pacote deste arquivo, substituindo só o corpo" |

---

## 5. Checklist de anexos por tipo de peça

| Peça | Anexar |
|---|---|
| Contestação | inicial · documentos da ECT · peça-modelo · ACT vigente |
| Recurso ordinário | sentença · decisão dos embargos · contestação · peça-modelo |
| Contrarrazões | RO do Reclamante · sentença · contestação · peça-modelo |
| Recurso Ordinário | sentença · contestação · peça-modelo do mesmo tema · contrato administrativo e documentos de fiscalização (quando o tema for responsabilidade subsidiária) |
| Recurso de revista | acórdão · embargos e decisão dos embargos · peça-modelo |
| Quesitos | contestação · laudos e documentos do INSS · peça-modelo |
| Embargos | decisão embargada · peça em que a tese omitida foi deduzida |

---

## 5.1 Peças que eu produzo, e como nomeio o arquivo

| Peça | Contexto típico |
|---|---|
| Contestação / Defesa | Resposta à inicial (trabalhista e cível) |
| Contrarrazões de recurso | Defesa da sentença favorável (TRT24 na trabalhista) |
| Recurso Ordinário | Sentença desfavorável (trabalhista, ao TRT24) — petição de interposição à Vara + razões ao Tribunal |
| Recurso de revista | Sentença/acórdão desfavorável (trabalhista) |
| Quesitos para perícia | Médica (doença ocupacional) e técnica (insalubridade/periculosidade) |
| Manifestações | Documentos do INSS, laudos, cálculos, RPV, audiência |
| Embargos de declaração | Omissão/contradição + prequestionamento |
| Impugnação aos cálculos · Embargos à execução | Fase de execução (sobretudo em cível) |

Fluxo padrão na trabalhista: **petição de juntada à Vara → razões/contrarrazões ao TRT24**.

Nome do arquivo final: `Tipo - Tema abreviado - NOME DA PARTE.docx` — **sem `_`** (espaço simples no
lugar) e com os tópicos separados por ` - ` (espaço, hífen, espaço). O nome da parte vem por último, em
caixa alta. Cabe um bloco livre a mais entre o tema e a parte, quando o usuário indicar. Exemplo de padrão:
`RO - Resp Subs - NOME DA PARTE.docx` (nenhum nome real neste repositório).

Abreviações de tipo: `Cont` = contestação · `Contrarraz` = contrarrazões · `RO` = recurso ordinário ·
`RR` = recurso de revista · `Manifest` = manifestação · `ED` = embargos de declaração ·
`Quesitos` = quesitos de perícia. Abreviações de tema: `Inc Fun` = incorporação de função ·
`Resp Subs` = responsabilidade subsidiária · `Doença Ocup` = doença ocupacional ·
`Inc AAT reab` = incorporação do adicional de atividade de tratamento após reabilitação ·
`Inc AADC reab` = idem, adicional de distribuição e coleta · `Presc total` = prescrição total (bloco livre,
quando a prejudicial for o eixo da peça). Abreviação nova criada em sessão entra nesta lista.

A regra é aplicada pela skill `nomear-minuta` (`.claude/skills/nomear-minuta/`), que vale também para o nome
citado no corpo da resposta, não só para o arquivo salvo. Não confundir com o padrão **interno** do
repositório (`modelos/<área>/<tipo_peca>__<tema>.md`, em snake_case), que segue `modelos/README.md`.

A peça é gerada **e entregue** em `.docx`, pela skill `formatar-minuta`, a partir de `modelos/_FORMATO_BASE.docx` — nunca em documento em branco e nunca em `.odt`.

---

## 6. Protocolo de atualização da base (teses + modelos)

Objetivo: depois de algumas sessões sobre o mesmo tema, eu não deveria mais precisar anexar uma peça-modelo
antiga — o esqueleto da peça já deve estar salvo em `modelos/`, e a tese já deve estar numa ficha de
`teses/<área>/`, roteada pelo `INDICE.md`. Isso só acontece se dois passos forem seguidos: um **antes** de
anexar, e um **ao final** de cada sessão em que algo for minutado.

### 6.1 Antes de anexar uma peça-modelo antiga (passo novo)

```
Antes de eu anexar um modelo antigo: a formatação desta peça vem da skill formatar-minuta, que
clona modelos/_FORMATO_BASE.docx (fonte, cabeçalho, rodapé, fecho e assinatura), para qualquer tipo
de peça — não peça modelo antigo por causa de formatação. Siga também a tabela de parágrafos de
modelos/README.md (títulos de seção em quadro centralizado, subtítulos sublinhados recuados,
enumerações e citações em bloco de 3 cm). Ajuste o bloco de qualificação (endereçamento, rótulos de
polo, fundamentação legal de admissibilidade) conforme o tipo de peça desta sessão.
Além disso, verifique em modelos/<área>/ se já existe o par <tipo_peca>__<tema>.md (+ .docx, se
houver) para esta peça + tema. Se existir, use o .md como base de estrutura/tese — não peça o anexo
de uma peça-modelo antiga. Se não existir, ou se estiver desatualizado, me avise e eu anexo o modelo.
```

Isso evita reanexar o que já foi consolidado — a formatação vem sempre da skill `formatar-minuta`, sobre
`_FORMATO_BASE.docx`;
a tese/estrutura do tema vem do `.md` correspondente. Só volte a anexar uma peça antiga quando o tema for
novo, o modelo salvo estiver incompleto, ou o caso trouxer uma variação de estrutura que valha preservar
num `.docx` próprio do tema.

### 6.2 Ao final de qualquer sessão de minuta

```
Antes de encerrarmos: revise esta conversa e aponte, separadamente:
1. TESE NOVA — algum argumento usado aqui não está nas fichas de teses/ que eu abri?
   Se o tema não tem ficha, proponha uma nova a partir de teses/_TEMPLATE_TESE.md,
   com o bloco de metadados preenchido (area, tema, slug, status, gatilhos, pecas,
   modelos, ver_tambem, atualizado).
2. CORREÇÃO — alguma tese das fichas se mostrou errada, incompleta ou foi contestada
   com sucesso pela parte contrária neste processo? Se sim, proponha também mudar o
   status da ficha para "revisar" e registrar o ponto na seção Lacunas dela.
3. JURISPRUDÊNCIA NOVA — algum precedente citado aqui (dos autos ou anexado por mim)
   ainda não consta da ficha do tema?
3b. ROTEAMENTO — algum gatilho faltou? Se eu tive que dizer do que se tratava porque
   o índice não levou até a ficha certa, proponha os gatilhos a acrescentar.
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
   a gerar), pronto para eu revisar e commitar no GitHub. Se alguma ficha foi criada
   ou alterada, atualize o campo `atualizado` dela e lembre de rodar
   `python scripts/atualizar_indice.py` antes do commit.
Se nada for novo, diga isso explicitamente — não force um "achado" apenas para preencher a resposta.
```

Regras deste protocolo:
- Em sessão de Claude Code, a skill `atualizar-base-conhecimento` aplica as alterações de texto (fichas de
  `teses/`, modelos estruturais `.md`, CONTEXTO, playbook) e **commita sozinha** na branch `claude/*` da
  sessão — eu reviso no diff do commit ou no PR. Modelo visual (`.docx` anonimizado) continua entrando só
  depois da minha aprovação explícita, porque conferir texto oculto e metadados do arquivo é verificação
  minha e o repositório é público.
- Toda tese ou modelo novo entra como candidato — soma à ficha/arquivo correspondente, não substitui o que já
  existe, a menos que eu confirme que o anterior estava errado ou desatualizado.
- Ficha criada ou alterada exige regenerar a tabela do índice (`python scripts/atualizar_indice.py`); o
  commit não deve ir com `INDICE.md` fora de sincronia (`--check` confere isso).
- Modelo (estrutural ou .docx) nunca leva nome de cliente, nº de processo, CPF ou qualquer dado
  identificável — nem no corpo, nem em metadados do arquivo (ver `modelos/README.md`).
- Se o commit for feito por mim direto no GitHub (app ou site), não precisa repetir o protocolo na mesma
  conversa. Se for pedir para o Claude commitar via connector do GitHub, confirme o resultado primeiro —
  e verifique se esse connector consegue mesmo subir arquivo binário (.docx); se não conseguir, essa etapa
  precisa ser feita numa sessão com acesso a git (Claude Code).
