# Base de conhecimento — Assessoria Jurídica ECT / Contencioso Trabalhista

> Documento para colar nas **instruções personalizadas** de um Projeto do Claude, ou no início de uma conversa nova.
> Fonte: reconstruído a partir das conversas de 04 a 06/08/2026.

---

## 1. Quem sou eu (usuário)

- Advogado da **Assessoria Jurídica da Empresa Brasileira de Correios e Telégrafos (ECT)**.
- Assinatura das peças: **Marcos Hideki Kamibayashi — OAB/MS 14.580**.
- Base: **Campo Grande/MS**. Jurisdição: **TRT da 24ª Região** e Varas do Trabalho de Campo Grande (4ª e 7ª VT aparecem nos autos recentes).
- Atuo **sempre no polo passivo** — a ECT é a Reclamada. Toda peça é de defesa.
- Sistema: **PJe**. Ritos: **sumaríssimo (ATSum)** e ordinário.

---

## 2. O que eu produzo

| Peça | Contexto típico |
|---|---|
| Contestação | Resposta à inicial trabalhista |
| Contrarrazões de Recurso Ordinário | Defesa da sentença favorável, endereçada ao TRT24 |
| Recurso de Revista | Sentença/acórdão desfavorável |
| Quesitos para perícia médica | Ações de doença ocupacional |
| Manifestações | Sobre documentos do INSS, laudos, etc. |

Fluxo padrão: **petição de juntada à Vara → razões/contrarrazões ao TRT24**.

---

## 3. Teses recorrentes da ECT

### 3.1 Incorporação de gratificação de função (o tema mais frequente)
- Normas internas: **Módulo 55** (revogado em **01/05/2012**) e **Módulo 36** (revogado em **15/05/2014**); substituição FAT/FAO por ITF/GPTF.
- Tese central: **requisito temporal não implementado até a revogação** → havia mera *expectativa de direito*, não direito adquirido. Sem alteração contratual lesiva (art. 468, CLT).
- **Súmula 51, I, do TST** — afastada quando os requisitos do regulamento não foram preenchidos na vigência.
- **Súmula 372 do TST** — item I cancelado (conferir data/teor).
- **Tema 23 dos repetitivos do Pleno do TST** — tese vinculante (CPC, art. 927).
- Argumentos de apoio: art. 8º, §2º, CLT; *ratio decidendi* de precedentes do STF; **salário-condição**; legalidade administrativa.
- Precedentes do TST sobre a própria ECT e os mesmos normativos: RR-10652-45.2019.5.03.0182 (2ª T., Min. Liana Chaib, DEJT 23/02/2024); RR-10662-35.2018.5.03.0179 (6ª T., Min. Kátia Magalhães Arruda, DEJT 13/06/2023); RRAg-0010959-96.2017.5.03.0140 (3ª T., Min. Mauricio Godinho Delgado, DEJT 26/05/2023); E-RR-1561-30.2015.5.10.0002 (SBDI-1, 06/12/2018).
- Ver modelo completo em `modelos/trabalhista/contestacao__incorporacao_funcao.md` (+ `.docx` de
  formatação) — modelo modular, com blocos condicionais (Motorizado, quebra de caixa, substituição, CIP,
  POSTALIS etc.) a selecionar conforme o caso.

### 3.2 Prescrição
- **Prescrição total** — Súmula 294 do TST e art. 11, §2º, da CLT, para alteração do pactuado com prestação sucessiva não assegurada por lei.

### 3.3 Prerrogativas processuais da ECT
- **Prazo em dobro** — art. 1º do Decreto-lei 779/69, combinado com a equiparação à Fazenda Pública do art. 12 do Decreto-lei 509/69, recepcionado pela CF/88 (STF, **RE 220.906/DF**).
- **Dispensa de preparo/custas**.

### 3.4 Doença ocupacional
Três frentes de defesa, sempre nesta ordem:
1. **Inexistência de incapacidade total e permanente** — incapacidade parcial/temporária, reversibilidade (sobretudo em quadros psiquiátricos), natureza temporária dos benefícios do INSS (DCB).
2. **Inexistência de nexo causal** — etiologia multifatorial, fatores extralaborais e familiares, antecedentes, espécie 31 x 91, NTEP/CNAE **5310-5/01**, art. 20, §1º, da Lei 8.213/91; eventual concausa deve ser quantificada.
3. **Inexistência de culpa da empregadora** — exames admissional e periódicos, PCMSO e riscos psicossociais, ausência de comunicação prévia à empresa; exigir do perito a indicação da **norma específica** supostamente descumprida.

### 3.5 Temas acessórios que reapareceam *ad cautelam*
Quebra de caixa · substituições · aplicação integral dos normativos internos · reajustes de ACT · CIP · POSTALIS · honorários advocatícios.

### 3.6 Afastamentos (atestado médico / auxílio-doença) e limite de responsabilidade do empregador
- **Limite de 15 dias** — art. 60, §3º, da Lei 8.213/91: a partir do 16º dia de afastamento por doença/acidente,
  opera-se de pleno direito a **suspensão do contrato de trabalho** (art. 476 da CLT) e o encargo do pagamento
  passa à Previdência Social. Atestados médicos sucessivos e intercalados no intervalo de 60 dias, uma vez
  homologados pela Medicina do Trabalho da ECT, somam-se para fins de contagem desse limite.
- **FGTS não incide** durante a suspensão contratual quando o benefício é de natureza previdenciária comum
  (espécie 31) — a obrigação de recolhimento durante afastamento restringe-se a acidente de trabalho e
  serviço militar (art. 15, §5º, da Lei 8.036/90 c/c art. 28 do Decreto 99.684/90).
- **Lacuna previdenciária** (período entre o fim da responsabilidade da empregadora e a decisão do INSS): a
  tese de defesa atribui a pendência a ato/omissão da própria empregada (atraso em protocolar o requerimento
  do benefício, atraso em juntar a Comunicação de Decisão do INSS à empresa) — combinar com **vedação ao
  comportamento contraditório** (art. 422 do Código Civil) e o brocardo de que ninguém pode beneficiar-se da
  própria torpeza.
- **Reajuste de ACT já pago / bis in idem** — quando a inicial calcula o período do afastamento usando valores
  *já reajustados* de um Acordo Coletivo posterior, cabe demonstrar que o reajuste foi pago autonomamente,
  evitando duplicidade.
- **Férias**: o afastamento médico causa exclusão automática da programação de férias no sistema da ECT;
  se a própria empregada assinar posteriormente formulário de reprogramação para período já vencido, isso
  concorre para o deslocamento da data de início do gozo — reduz ou afasta a dobra do art. 137 da CLT.
- Ver modelo completo em `modelos/trabalhista/contestacao__afastamentos.md` (+ `.docx` de formatação).

### 3.7 Progressão horizontal por antiguidade — PCCS/2008
- Tema de **ajuizamento em massa**: a inicial alega que a Promoção Horizontal por Antiguidade (PHA) seria
  bienal e que a ECT a concede, "na prática", a cada 36 meses, qualificando a diferença como **ato
  potestativo** (arts. 122 e 129 do Código Civil).
- **Tese central — a norma se aplica inteira.** Os itens 5.2.3.3.2 e 5.2.3.3.3 do PCCS/2008 formam uma
  unidade: são 24 meses de efetivo exercício **aferidos em data de corte fixa (31 de agosto)**, com
  aplicação **no mês de outubro**. Como a concessão anterior também se dá em 1º de outubro, na data de corte
  seguinte o empregado tem apenas **22 meses e 30 dias** — falta um mês e um dia —, tornando-se elegível só
  na apuração do ano seguinte. O intervalo de 36 meses é **consequência aritmética da norma**, não prática
  paralela da Empresa. Demonstrar ciclo a ciclo, com a ficha cadastral que o próprio autor juntou.
- **A concessão não é automática**: o item 5.2.3.3.3 exige critérios propostos pela Diretoria de Gestão de
  Pessoas, em consonância com o item 5.4.4, e **aprovação prévia da Diretoria Colegiada**. O item 5.4.4
  submete a promoção ao planejamento orçamentário, limitado ao percentual definido pelos órgãos de controle
  — 1% da folha, na Resolução nº 9, de 03/10/96, do antigo CCE (atual DEST). Isso afasta a alegação de que
  "o único requisito é o decurso do tempo".
- **Limites do PCCS**: item 8.5.1 (vedada a extrapolação da faixa de referências salariais do cargo) e itens
  5.2.3.2.4 / 5.2.3.3.4 (**alternância** — antiguidade e mérito não podem ser concedidas ao mesmo empregado
  no mesmo ano). Este último costuma ser violado pela própria tabela "pleiteada" da inicial.
- **Inexistência de condição potestativa**: data de corte e mês de aplicação são critérios objetivos,
  prévios, públicos e uniformes, não evento sujeito ao arbítrio da Empresa (art. 121 do CC); e o art. 129 do
  CC exige implemento *maliciosamente* obstado — o que a ficha cadastral desmente, já que a primeira PHA
  costuma vir em 26 a 28 meses da admissão, e não em 36.
- **Prescrição**: deduzir a total (Súmula 294 do TST e art. 11, §2º, da CLT, aplicável às lesões posteriores
  a 11/11/2017), mas contar com o cenário de prescrição **parcial** — a **Súmula 452 do TST** é frontalmente
  contrária e específica para inobservância de critérios de promoção de PCS. Pedido sucessivo: quinquênio
  contado do ajuizamento. O art. 3º da Lei 14.010/2020, quando invocado, suspende prazos apenas da entrada
  em vigor da lei até 30/10/2020 — não permite recuo do marco para datas anteriores.
- **Correção monetária**: o Tema 810 do STF (art. 1º-F da Lei 9.494/97) não rege crédito trabalhista;
  sustentar a SELIC do art. 3º da EC 113/2021, dada a equiparação da ECT à Fazenda Pública. `[REVISAR: o
  critério atualmente adotado pelo TST, à vista das ADCs 58 e 59 e da Lei 14.905/2024.]`
- **Ausência de prejuízo (quando houver função gerencial com CRS)**: nas fichas financeiras, o Complemento
  de Remuneração Singular (rubrica 051106) é reduzido no mesmo centavo em que o salário-base sobe por
  promoção horizontal, mantendo constante a soma "salário-base + CRS" — base de cálculo do anuênio e da CIP.
  No período de exercício da função, o reenquadramento não gera diferença alguma. `[REVISAR: obter o
  normativo interno do CRS junto à área de Gestão de Pessoas.]`
- **Reflexos**: o adicional de férias de 70% foi **excluído** pelo acórdão da SDC no processo
  1001203-57.2020.5.00.0000 (cláusula 59 — gratificação de férias), tendo sido mantido antes disso na
  sentença coletiva DCG-1000662-58.2019.5.00.0000, vigente até julho/2020. O "reflexo em anuênio" é *bis in
  idem*, pois o anuênio já é percentual incidente sobre a base salarial.
- Precedentes do TRT da 24ª Região sobre o próprio PCCS/2008: **ACP 0024181-70.2020.5.24.0002** (Tribunal
  Pleno, Rel. Des. Marcio Vasques Thibau de Almeida, j. 26/11/2020) — o mais forte, e que também sustenta a
  preliminar do art. 104 do CDC; **RO 0025003-89.2016.5.24.0005** (2ª Turma, Rel. Des. Amaury Rodrigues
  Pinto Junior, j. 22/08/2018); **RO.1 001285/2001-001-24-00-0** (Rel. Juiz Nicanor de Araújo Lima), sobre
  discricionariedade na concessão de promoções.
- Ver modelo completo em `modelos/trabalhista/contestacao__progressao_horizontal_pccs2008.md`.

---

## 4. Padrão formal das peças

- Formato: **.odt** (LibreOffice); conversão para .docx quando necessário.
- Fonte **Arial 11**, **entrelinha 1,5**, parágrafos **justificados** com recuo de primeira linha.
- Margens: esquerda 2 cm / direita ~1,25 cm.
- **Cabeçalho** com logotipo dos Correios + "Assessoria Jurídica"; **rodapé** com endereço e numeração de páginas.
- Citações de jurisprudência em bloco recuado (~3 cm).
- Fecho: "N. Termos / P. Deferimento. / Campo Grande/MS, data de assinatura eletrônica." + bloco de assinatura centralizado com nome e OAB.
- Estrutura usual das razões: síntese → preliminares/prejudiciais → mérito → *ad cautelam* → requerimentos com **prequestionamento**.

---

## 5. Como eu quero que o Claude trabalhe

**Regras inegociáveis:**
1. **Não inventar nada** — jurisprudência, doutrina, número de processo, data, cláusula de ACT ou Id de documento. Se não tiver certeza, marcar `[REVISAR: ...]` ou `[INSERIR: ...]` no corpo do texto.
2. Só usar ementas que constem dos autos, do modelo anexado ou do próprio recurso adversário.
3. Sempre listar ao final, separadamente, **o que precisa de conferência humana**: datas de intimação e contagem de prazo, cômputo de tempo em função gratificada, Ids e cláusulas, e toda a jurisprudência citada.
4. Não presumir fatos ausentes dos documentos anexados; quando a defesa e a sentença divergirem, apoiar-se nos fatos da sentença e da capa do PJe.
5. Trabalhar em **duas etapas** na mesma conversa: análise estruturada primeiro, minuta depois.
6. Replicar **integralmente** a formatação da peça-modelo anexada.
7. Um processo por conversa — não misturar autos diferentes.

---

## 6. Nomenclatura de arquivos que eu uso

`Tipo - Tema abreviado - Rito - NOME DA PARTE.odt`

Exemplos reais: `Cont_-_Inc_-_RONALDO_PEREIRA_DE_SOUZA.odt` · `RR_-_Inc_Fun_-_Sumula_51_-_Rito_Sumarissimo_-_ANTONIA_RAQUEL_TELES_GOMES_MEDEIROS.odt` · `Quesitos_-_Pericia_Medica_-_MARCIO_ALVES_DAS_NEVES.odt`

Abreviações: `Cont` = contestação · `RR` = recurso de revista · `Inc Fun` = incorporação de função · `Manifest` = manifestação.

---

## 7. Lacunas desta base (preencher)

- [ ] Estrutura da equipe e distribuição de processos
- [ ] Volume mensal e prazos internos de entrega
- [ ] Outras áreas além da trabalhista (cível, consumidor?)
- [ ] Orientações da Consultoria Jurídica nacional da ECT que vinculam a defesa local
- [ ] Teses que a ECT decidiu *não* sustentar
