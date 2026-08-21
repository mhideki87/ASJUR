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
| Embargos à execução / impugnação aos cálculos | Liquidação de sentença — individual ou de título coletivo |
| Contraminuta de agravo de petição | Resposta ao agravo do exequente na fase de execução |

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
- **Delimitação de matérias e valores no agravo de petição** — art. 897, §1º, da CLT. O TRT24 tem
  reconhecido o requisito atendido considerando que a ECT goza das prerrogativas da Fazenda Pública e do
  regime constitucional de pagamento por precatório. O exequente, quando agravante, é dispensado da
  delimitação de valores.

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

### 3.7 Honorários advocatícios em execução individual de sentença coletiva (tese vencedora — TRT24)

Cenário: ação coletiva com o sindicato como substituto processual, em que o título já fixou **honorários
assistenciais de 15% sobre o valor da condenação** (Lei 5.584/70 c/c **Súmula 219, V, do TST**). Depois,
nas execuções individuais, os **mesmos advogados** pedem nova verba **sucumbencial autônoma** para a fase
executiva, invocando o art. 85, §1º, do CPC e, por analogia, a **Súmula 345 do STJ**.

Argumentos da ECT (contraminuta ao agravo de petição dos exequentes), acolhidos em 1º grau e mantidos pelo TRT24:
- **Art. 791-A da CLT é regramento específico e exaustivo** — prevê a verba honorária apenas na fase de
  conhecimento; o silêncio quanto à execução é **escolha legislativa (silêncio eloquente)**, não lacuna a ser
  suprida pelo art. 85, §1º, do CPC.
- A execução trabalhista **não é processo autônomo**, e sim fase de satisfação do crédito → a aplicação
  subsidiária do CPC não é automática.
- Fixar nova verba honorária **inova o título executivo** e configura ***bis in idem***.

Fundamentos que o TRT24 adotou — roteiro a reproduzir em caso análogo:
1. Os honorários arbitrados na **ação matriz remuneram o labor advocatício em todas as fases**, da fase de
   conhecimento à liquidação/execução individual, até a satisfação final do crédito.
2. A base de cálculo — "valor da condenação" — **só se materializa líquida e certa após a liquidação
   individual**; logo, os 15% do título incidem exatamente sobre o proveito econômico que se liquida na
   execução. Não há trabalho advocatício sem remuneração.
3. **Identidade de patronos** entre a fase coletiva e a execução individual é o fato decisivo — comprová-la
   nos autos (procurações e substabelecimentos) é o passo prático mais importante da defesa.
4. **Os próprios exequentes já lançam a verba assistencial da ação coletiva nas planilhas de cálculo da
   execução** — apontar isso na contraminuta demonstra materialmente o `bis in idem`.
5. ***Distinguishing*** dos precedentes do TST invocados pelo exequente: eles partem da premissa de que
   (a) não houve fixação anterior de honorários abrangendo a totalidade do trabalho, ou (b) o patrocínio na
   execução é completamente independente do da ação coletiva. Onde há honorários da Súmula 219 do TST em favor
   do sindicato **e** os mesmos patronos, a hipótese é distinta e o precedente não se aplica.

Precedentes do próprio TRT24 (2ª Turma, Rel. Des. João de Deus Gomes de Souza), mesma reclamada e mesmo título
coletivo — checar se seguem válidos antes de citar:
- AP 0025022-77.2025.5.24.0006, j. 08/07/2026 (https://link.jt.jus.br/RbdesH) — precedente-líder da tese.
- AP 0025655-03.2025.5.24.0002, j. 12/08/2026 — reafirma o entendimento e desenvolve o *distinguishing* acima.

### 3.8 Liquidação e execução: teses da ECT já rejeitadas pelo TRT24 (usar com cautela)

Registro dos capítulos em que o agravo de petição da ECT foi **integralmente desprovido** no mesmo julgamento
citado na seção 3.7 (TRT24, 2ª Turma, AP, j. 12/08/2026). Serve para calibrar risco e não repetir tese perdida
sem argumento novo.

**(a) Compensação do AADC com o adicional de periculosidade pago a carteiro motorizado.**
Tese da ECT: a decisão do **TRF da 1ª Região** que suspendeu os efeitos da **Portaria MTE nº 1.565/2014**
(tutela antecipada recursal na Ação Declaratória de Nulidade nº 1012413-52.2017.4.01.3400) seria fato
superveniente a tornar indevido o adicional de periculosidade, autorizando a compensação (arts. 525, §1º, VII,
e 535, VI, do CPC) e o sobrestamento da execução, sob pena de enriquecimento sem causa. Por que caiu:
- **Coisa julgada** — o título declarou expressamente que o adicional de periculosidade e o AADC têm naturezas
  diversas, que a cumulação não configura `bis in idem` e que não há falar em compensação; matéria imutável em
  execução (art. 5º, XXXVI, da CF; art. 879, §1º, da CLT). A via adequada seria **ação rescisória**, não
  embargos/impugnação à execução.
- **Decisão precária não desconstitui título definitivo** — tutela antecipada de juízo diverso não tem esse efeito.
- **A cronologia mata o "fato superveniente"** — a decisão do TRF1 era de 22/01/2024 e o trânsito em julgado do
  título trabalhista, de 14/03/2024: sendo anterior ao trânsito, não é fato novo. *Lição prática: antes de
  sustentar fato superveniente, conferir se a data é posterior ao trânsito em julgado.*
- **Art. 193, §4º, da CLT é autoaplicável** — a suspensão da Portaria não retira o substrato legal do adicional
  (TST, Ag-RRAg 0000061-45.2022.5.05.0511, 5ª T., Rel. Min. Breno Medeiros, j. 17/09/2025, DEJT 23/09/2025).
  Sem "pagamento indevido" não há dívida recíproca a compensar.
- **STF, SL 1574 MC-Ref** (Rel. Min. Rosa Weber, Tribunal Pleno, j. 04/09/2023) — o pedido de suspensão foi
  formulado **pela própria ECT** e *denegado*, ratificando o **Tema Repetitivo nº 15 do TST**
  (IRR/RR-1757-68.2015.5.06.0371, Rel. Min. Alberto Bresciani, j. 14/10/2021): o AADC é adicional de
  **penosidade** (PCCS/2008, item 4.8), e o adicional do art. 193, §4º, da CLT remunera o **risco** em
  motocicleta (Lei 12.997/2014) — fatos geradores distintos, cumulação possível, sem `bis in idem`, cuja vedação
  só existe entre insalubridade e periculosidade (art. 193, §2º, da CLT).
- A cláusula de supressão do AADC "em caso de concessão legal de qualquer mecanismo sob o mesmo título ou
  idêntico fundamento/natureza" (PCCS/2008, itens 4.8.2 e 8.9.1; acordo homologado no DC
  TST-1956566-24.2008.5.00.0000) **não** foi aceita como suporte da substituição do AADC pelo adicional de
  periculosidade a partir de outubro/2014 — o TST viu nisso ofensa à isonomia frente aos carteiros não
  motorizados. Tese praticamente encerrada em desfavor da ECT; sustentar apenas para prequestionamento.

**(b) Exclusão dos reflexos do AADC em horas extras (base de cálculo restrita ao salário-base, Cláusula 31 dos ACTs).**
Rejeitada: o título determinou o cálculo "somente sobre o salário-base, com reflexos em horas extras, férias
acrescidas do terço constitucional, gratificação natalina e FGTS". Norma coletiva e **teoria do conglobamento**
(art. 7º, XXVI, da CF) não relativizam a coisa julgada em execução — a discussão devia ter sido exaurida na fase
de conhecimento. O acórdão registrou ainda **inobservância da dialeticidade recursal**: reiterar argumentos sem
atacar os fundamentos da decisão agravada foi expressamente usado contra a ECT.

**(c) Exclusão de "reflexos sobre reflexos" (FGTS e 13º/férias sobre horas extras).**
Rejeitada: o **FGTS** incide sobre parcelas de natureza salarial por imperativo legal (art. 15 da Lei
8.036/1990), independendo de menção expressa no título; **13º salário e férias sobre horas extras** são
decorrência lógica da natureza salarial das verbas deferidas (art. 142, §5º, da CLT; art. 77 do Decreto
10.854/2021). Não é inovação do título, é sua aplicação.

**(d) Juros e correção monetária pelo art. 1º-F da Lei 9.494/1997.**
Rejeitada porque **o próprio título** (acórdão do TST de 13/12/2023) já havia fixado os critérios: **IPCA-E mais
juros legais do art. 39, `caput`, da Lei 8.177/1991 na fase pré-judicial** e **SELIC a partir do ajuizamento**
(ADCs 58 e 59 do STF; EC 113/2021; Tema 1191 do STF). Pedir poupança até 08/12/2021 com SELIC depois, ou afastar
os juros da fase pré-judicial (art. 883 da CLT), é rediscutir o título. *Lição prática: em liquidação, conferir
primeiro o que o título fixou sobre atualização — se fixou, a tese de índice mais favorável está barrada.*

**Leitura de conjunto.** Nos quatro capítulos a razão de decidir foi a mesma: **art. 879, §1º, da CLT**. Em
liquidação e execução, a defesa da ECT rende quando ataca *cálculo* (critério, período, base, duplicidade)
dentro dos limites do título, e não quando tenta reabrir *tese* de mérito já decidida.
[REVISAR: definir se a tese de compensação AADC × periculosidade se mantém apenas para prequestionamento, dado
o desprovimento reiterado no TRT24, ou se passa a ser sustentada só em ações ainda na fase de conhecimento.]

**Estratégia recursal em execução:** recurso de revista contra acórdão em agravo de petição só cabe por **ofensa
direta e literal à Constituição** (art. 896, §2º, da CLT; Súmula 266 do TST) — alegações de coisa julgada tendem
a ser enquadradas como ofensa reflexa. [REVISAR: confirmar viabilidade caso a caso.]

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
- [ ] Teses que a ECT decidiu *não* sustentar — iniciado na seção 3.8 (teses de execução já
      rejeitadas pelo TRT24); falta o levantamento das demais áreas e da fase de conhecimento
