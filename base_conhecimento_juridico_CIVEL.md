# Base de conhecimento — Assessoria Jurídica ECT / Contencioso Cível

> Documento para colar como **Project knowledge** (ou nas instruções personalizadas) de um Projeto do Claude.
> **STATUS: RASCUNHO NÃO VALIDADO.** Gerado a partir de estatística determinística (regex/contagem de pastas)
> sobre os metadados de `3_acervo_com_fichas/_indice/metadados.jsonl` — **nenhum arquivo foi lido/analisado por
> LLM** para produzir este documento. Tudo aqui é candidato a confirmação, não fato estabelecido.
> Antes de usar qualquer item abaixo como tese em uma peça real, valide contra o processo em mãos.

---

## 1. Quem sou eu (usuário)

- Advogado da **Assessoria Jurídica da Empresa Brasileira de Correios e Telégrafos (ECT)**.
- Assinatura das peças: **Marcos Hideki Kamibayashi — OAB/MS 14.580** (confirmar se todas as peças cíveis usam
  a mesma assinatura — nos exemplos vistos também aparece "Marcos Henrique Boza — OAB/MS 13.041-B" [REVISAR]).
- Base: **Campo Grande/MS**. Também aparecem processos de outras comarcas/varas federais de MS.
- Atuo predominantemente no **polo passivo** (a ECT como Ré), em ações de indenização por falha no serviço postal.
- Sistemas identificados nos autos: **Juizados Especiais Federais (JEF)** e **Justiça Federal comum (1º e 2º grau,
  TRF3)** [REVISAR — confirmar se há também Justiça Estadual/Juizados Estaduais].

---

## 2. O que eu produzo (frequência observada nos 461 arquivos catalogados como "Cível")

| Peça | Ocorrências no catálogo |
|---|---|
| Contestação / Defesa | ~127 |
| Sentença (anexada como modelo/precedente) | 24 |
| Manifestação (diversas: cálculo, RPV, audiência) | 22 |
| Acórdão (anexado como precedente) | 19 |
| Petição (avulsa) | 14 |
| Contrarrazões (recurso) | 12 |
| Petição Inicial (raramente — polo ativo?) | 3 |
| Impugnação aos Cálculos | 3 |
| Embargos à Execução | 1 |

`[REVISAR]`: 236 dos 461 arquivos não tiveram o tipo de peça identificado automaticamente (nomes de pasta,
documentos de apoio, jurisprudência solta, etc.) — não incluídos na tabela.

---

## 3. Tema dominante: Ações Indenizatórias — Serviço Postal

A imensa maioria dos casos cíveis está na pasta `AÇÕES INDENIZATÓRIAS SERVIÇO POSTAL`, com um padrão fático
recorrente (inferido dos **nomes das pastas de cliente**, não do conteúdo lido):

### 3.1 Fatos-tipo que se repetem (candidatos a tese — cada um precisa de confirmação no processo real)
- Extravio de encomenda/correspondência **sem declaração de valor** → tese provável: limitação de responsabilidade
  ao valor declarado / ausência de prova do conteúdo e valor.
- Atraso na entrega (SEDEX, PAC) → tese provável: ausência de prazo contratual de entrega vinculante /
  caso fortuito ou força maior.
- Objeto internacional retido/devolvido pela Receita Federal ou por tributo não recolhido → tese provável:
  legalidade da cobrança de despacho postal e do tributo (ver Súmula 7/STJ quanto a reexame de prova nesses casos).
- Fraude em venda pela internet, com alegação de ilegitimidade ativa do autor (quem vendeu x quem comprou).
- Avaria/violação de objeto após entrega, sem prova de nexo com a ECT.
- Cobrança do "despacho postal" em importações — citado explicitamente como tema com pasta própria de
  "SUBSÍDIOS PARA AÇÕES OBJ TRIBUTADO" e normativos internos (NJ-416/2014, Convenção Postal UPU, MANCAT/MANINT).

`[REVISAR]`: estes são padrões extraídos de **nomes de pastas de clientes** (ex.: "EXTRAVIO SEDEX SEM DECL VALOR",
"ATRASO PAC DANO MORAL"), não de leitura do inteiro teor. Servem para orientar qual pasta abrir, não para citar
como jurisprudência ou tese pronta.

### 3.2 Legislação e normativos que aparecem com frequência (contagem de menções detectadas por regex,
variantes de grafia agrupadas)
- **Decreto-lei nº 509/69** (equiparação da ECT à Fazenda Pública) — ~190 menções somando variantes de grafia.
- **Lei nº 6.538/78** (Código Postal — monopólio e regime jurídico dos serviços postais) — ~104 menções.
- **Lei nº 9.099/95** e **Lei nº 10.259/01** (rito dos Juizados Especiais / Federais) — ~112 menções.
- **CDC, art. 14** (responsabilidade objetiva do fornecedor de serviços) e **Lei nº 8.078/90** — usado tanto
  a favor (regime do CDC) quanto contra (discussão se a ECT, em serviço postal monopolizado, submete-se ao CDC).
- **Lei nº 9.494/97** (restrições a tutela antecipada contra a Fazenda Pública).
- **Lei nº 11.960/2009** (índices de juros/correção monetária contra a Fazenda Pública).
- **Súmula 7/STJ** (incompetência do STJ para reexame de prova — aparece em acórdãos anexados como precedente).
- Normativos internos da ECT citados: **MANCAT** (módulos 07 e 12), **MANINT** (módulo 05), **NJ-416/2014**
  (legalidade da cobrança do despacho postal), **Convenção Postal Universal (UPU)**.

`[REVISAR]`: contagem bruta de strings, sem verificar se a citação era favorável, contrária ou apenas mencionada
en passant no texto (ex.: pode aparecer no argumento do autor, não da defesa).

---

## 4. Padrão formal das peças

- Formato: **.txt/.odt**, endereçamento observado tanto a **Juizado Especial Federal** quanto a **Vara Federal**.
- Fecho recorrente: "N. Termos / P. Deferimento. / Campo Grande/MS, [data]." — mesmo padrão da base trabalhista.
- `[REVISAR]`: confirmar se cabeçalho, fonte, espaçamento e demais regras formais da base trabalhista
  (seção 4 de `base_conhecimento_juridico_ECT.md`) também se aplicam aqui, ou se a área cível tem modelo próprio.

---

## 5. Como eu quero que o Claude trabalhe

Mesmas **regras inegociáveis** da base trabalhista (seção 5 de `base_conhecimento_juridico_ECT.md`) — em
especial: não inventar jurisprudência/legislação/dados do processo; marcar `[REVISAR]` onde faltar informação;
listar ao final o que precisa de conferência humana; um processo por conversa.

Regra adicional específica desta base: **todo item das seções 3.1 e 3.2 acima é candidato, não tese confirmada**
— antes de usá-lo numa peça real, confirme contra os documentos do processo em mãos.

---

## 6. Lacunas desta base (preencher com uso real)

- [ ] Confirmar/corrigir cada "fato-tipo" da seção 3.1 com casos reais (qual realmente vira tese vencedora e qual não).
- [ ] Confirmar se a ECT é sempre polo passivo em cível, ou há também ações no polo ativo (ex.: cobrança).
- [ ] Padrão formal completo da peça cível (a base trabalhista não deve ser presumida idêntica).
- [ ] Existência de outras matérias cíveis além de indenização por serviço postal (ex.: embargos à execução,
  ações de improbidade administrativa aparecem citadas — volume e relevância desconhecidos).
- [ ] Teses que a ECT decidiu *não* sustentar em cível.
