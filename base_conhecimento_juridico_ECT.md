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
| Embargos de declaração | Sentença de 1º grau com omissão, contradição, obscuridade ou erro material |
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
- **Dispensa de preparo/custas** e de **depósito recursal**.
- **Atualização monetária e juros — art. 3º da EC 113/2021**: nas discussões e condenações que envolvam a
  Fazenda Pública incide, uma única vez e até o efetivo pagamento, o índice da **SELIC** acumulado
  mensalmente. É norma constitucional específica e superveniente; opor-se ao critério geral aplicado de
  ofício pelo juízo (nos autos recentes, a decisão vinculante TST-E-ED-RR-713-03.2010.5.04.0029
  `[REVISAR: conferir teor e se ressalva a Fazenda Pública]`) exige demonstrar por que o especial prevalece
  sobre o geral.
- **Pedir o pronunciamento é ato de admissibilidade, não formalidade.** A contestação deve consignar
  expressamente que o pronunciamento sobre custas e depósito recursal "se faz necessário para o
  preenchimento de todos os pressupostos extrínsecos para viabilização da admissibilidade de eventual
  recurso". Se a sentença silenciar — o que ocorreu no caso-fonte de 08/2026, que dispensou apenas as custas
  —, **cabem embargos de declaração**: a falta de pronunciamento sobre a isenção do depósito recursal é capaz
  de comprometer a admissibilidade do recurso ordinário.

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
- **[CORREÇÃO — 08/2026, validada por sentença desfavorável]** A tese da *lacuna previdenciária imputável à
  própria empregada* **não prevalece** quando a permanência em casa, no período controvertido, decorreu de
  **ordem da própria chefia** — ainda que baseada em informação equivocada sobre a situação previdenciária. No
  caso-fonte o juízo reconheceu correto o encaminhamento ao INSS e a superação dos 15 dias, mas condenou a ECT
  a "responder pelo dano acarretado à autora ao prestar informação incorreta", com prova testemunhal do fato.
  Consequência prática: antes de sustentar essa tese, **apurar com a área se houve dispensa do labor
  determinada por gestor** no interregno pleiteado; havendo, a defesa deve migrar para a delimitação do
  período e dos consectários, não para a negativa da obrigação.
- **[CORREÇÃO — 08/2026]** A tese do **FGTS/espécie 31** (art. 15, §5º, da Lei 8.036/90) pressupõe que o
  período seja reconhecido como de **suspensão contratual**. Se o juízo requalifica a parcela como
  indenização por ato ilícito do empregador, a tese perde objeto — e o ponto a explorar passa a ser a
  **contradição** entre a natureza indenizatória atribuída à verba e os consectários de natureza salarial
  deferidos (FGTS, vale-alimentação, previdência complementar, retificação de CNIS, contribuição
  previdenciária), que não podem coexistir sobre a mesma parcela.
- **Retificação do CNIS**: o cadastro é mantido pelo INSS; ao empregador cabe apenas prestar informações pelos
  sistemas de escrituração digital. Obrigação de fazer imposta sem indicação de *qual* informação, *por qual
  via* e com que exigibilidade é obrigação de objeto indeterminado — impugnar por iliquidez (art. 492 do CPC).
- Ver modelo completo em `modelos/trabalhista/contestacao__afastamentos.md` (+ `.docx` de formatação).

### 3.7 Dano moral (art. 223-G da CLT) — dois pontos que as sentenças costumam errar
- **Gradação obrigatória** — o art. 223-G, §1º, da CLT instituiu sistema de **tarifação legal**: o valor
  decorre do enquadramento da ofensa em um dos graus (leve, média, grave, gravíssima) e da aplicação do
  multiplicador do salário contratual. Sentença que invoca o art. 223-G e, na mesma frase, arbitra "em juízo
  de equidade" **sem declarar o grau** incorre em contradição, e impede a ECT de aferir o teto legal. Alegar
  também, quando for o caso, que **a própria inicial não indicou o grau** — requisito legal de formulação do
  pedido.
- **[TESE ERRADA — NÃO USAR] Súmula 439 do TST: CANCELADA.** O verbete — que mandava corrigir o dano moral
  da data do arbitramento — foi **cancelado pela Resolução nº 225, de 30/06/2025, do Pleno do TST**, que
  revogou 36 enunciados por perda de eficácia diante das ADIs 5.867 e 6.021 e das ADCs 58 e 59 do STF, com
  efeitos retroagindo a 09/12/2021. Esta base chegou a registrar a tese como válida em 08/2026, e ela foi
  levada a embargos de declaração num caso real: **o juízo rejeitou apontando o cancelamento**. Fica o
  registro do erro para que não se repita.
  **O que vale hoje:** os critérios de juros e correção seguem a legislação vigente na liquidação — ADC 58,
  Lei nº 14.905/2024 e, para a ECT, o art. 3º da EC nº 113/2021 (seção 3.3). Como a SELIC incide desde o
  ajuizamento, **sentença que manda corrigir o dano moral do ajuizamento tende a estar correta** — não há
  aqui capítulo recursal a explorar. `[REVISAR: há doutrina sustentando que a Lei nº 14.905/2024 reabilitaria
  o critério cindido para o dano moral trabalhista (ConJur, 01/05/2026); é tese doutrinária, não vinculante —
  conferir antes de eventual uso]`
- **Lição de método:** verbete marcado `[REVISAR]` **não vai para peça sem conferência na fonte oficial**. O
  custo aqui foi um tópico de embargos rejeitado e a credibilidade da peça.
- **Mérito**: mero inadimplemento contratual ou divergência sobre extensão de verbas não configura lesão a
  direito da personalidade; existe um piso de inconvenientes tolerável sem dano moral autêntico.

### 3.8 Honorários advocatícios — sucumbência recíproca em favor da ECT
- Toda contestação deve requerer, em alínea própria, a condenação da parte autora em honorários de
  sucumbência (**art. 791-A, §3º, da CLT**). Havendo **procedência parcial**, o juízo deve arbitrar
  honorários recíprocos, **vedada a compensação** entre eles.
- É pedido que as sentenças com frequência **deixam de apreciar**, tratando apenas dos honorários devidos
  pela ECT — omissão a sanar por embargos de declaração.
- O deferimento de **justiça gratuita** à parte autora **não afasta** a condenação: apenas **suspende a
  exigibilidade** (art. 791-A, §4º, da CLT; STF-ADI 5766; Tema Repetitivo nº 21 do TST). Argumento reforçado
  quando a própria sentença já cita esses precedentes ao deferir a gratuidade.
- Ao dimensionar o pedido, medir a sucumbência da parte autora em valor: pedidos indeferidos + parcelas
  reduzidas, contra o valor da causa.

---

## 4. Padrão formal das peças

- Formato: **.odt** (LibreOffice); conversão para .docx quando necessário.
- Fonte **Arial 11**, **entrelinha 1,5**, parágrafos **justificados** com recuo de primeira linha.
- Margens: esquerda 2 cm / direita ~1,25 cm.
- **Cabeçalho** com logotipo dos Correios + "Assessoria Jurídica"; **rodapé** com endereço e numeração de páginas.
- Citações de jurisprudência em bloco recuado (~3 cm).
- Fecho: "N. Termos / P. Deferimento. / Campo Grande/MS, data de assinatura eletrônica." + bloco de assinatura centralizado com nome e OAB.
- Estrutura usual das razões: síntese → preliminares/prejudiciais → mérito → *ad cautelam* → requerimentos com **prequestionamento**.
- **Peças incidentais (embargos de declaração, manifestações)**: o bloco de qualificação é **abreviado** —
  "já qualificada nos autos da RECLAMAÇÃO TRABALHISTA em epígrafe" —, dispensando endereço, Decreto-Lei de
  instituição e telefone, que só se repetem na peça inaugural de defesa. Os rótulos de polo mudam
  (Embargante/Embargada) e a fundamentação legal de admissibilidade passa a ser o art. 897-A da CLT c/c os
  arts. 1.022 e ss. do CPC.
- **Registro de estilo** (validado na revisão final do usuário em 08/2026): abertura com *captatio
  benevolentiae* ("Em que pese os usuais brilhantismo e clareza ínsitos às decisões proferidas por este d.
  Juízo…"); uso de *data venia* / *data maxima venia* nos pontos de divergência frontal; "Aclaratórios" como
  sinônimo de embargos; cada tópico fechado por "**Respeitosamente requer-se, pois,** …". Preferência por
  peça **enxuta**: numeração corrida dos vícios, sem subdividir por espécie (omissão/contradição/erro
  material), e descarte dos vícios de baixa convicção, que migram para o recurso.

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
