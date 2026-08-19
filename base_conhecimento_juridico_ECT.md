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

---

### 3.7 Responsabilidade subsidiária em terceirização (ECT como **tomadora**, 2ª Reclamada)

Cenário: o Reclamante é empregado de prestadora de serviços (limpeza, conservação, vigilância etc.) que
executa contrato administrativo em unidade da ECT; pede-se a condenação da prestadora e, subsidiariamente,
da ECT. **Não é caso de defesa de empregadora** — nenhuma das obrigações discutidas é da ECT.

- **Eixo legal (o mais forte):** **art. 77, §1º, da Lei 13.303/16** (Lei das Estatais) — reprodução integral
  do art. 71, §1º, da Lei 8.666/93: a inadimplência do contratado quanto aos encargos trabalhistas não
  transfere à empresa pública a responsabilidade pelo pagamento. Para a ECT é este o dispositivo aplicável,
  e não o art. 121 da Lei 14.133/2021.
- **Constitucionalidade e ônus da prova:** **ADC 16** (STF, Pleno, 24/11/2010) — constitucionalidade do
  art. 71, §1º, sem ressalvas; **Tema 246 da repercussão geral** — vedada a transferência automática;
  **Rcl 17.402/SP** (Min. Gilmar Mendes, 18/03/2014, envolvendo a própria ECT) e **Rcl 19.871**
  (Min. Dias Toffoli, DJE 63, 31/03/2015) — fundamentação genérica sobre culpa *in vigilando* contraria
  a ADC 16.
- **Tema 1.118 da repercussão geral** (STF, Pleno, Rel. Min. Nunes Marques, julgamento iniciado em
  13/02/2025): o voto do Relator, acompanhado pela maioria formada **até a suspensão do julgamento**,
  propõe que (1) não há responsabilidade subsidiária amparada em inversão do ônus da prova, sendo
  imprescindível a comprovação, pela parte autora, de comportamento negligente ou nexo causal; e (2) o
  comportamento negligente se caracteriza quando a Administração permanece inerte **após notificação
  formal** (do trabalhador, sindicato, MTE, MPT, Defensoria ou outro meio idôneo). Citar sempre como
  julgamento em curso — **não** como tese fixada; conferir o andamento antes de cada protocolo.
  - ⚠️ **Cautela ao transcrever:** o **item 3** da tese proposta atribui à Administração a
    responsabilidade por garantir segurança, higiene e salubridade quando o trabalho se dá em suas
    dependências (art. 5º-A, §3º, da Lei 6.019/74). Em casos de **insalubridade / SST**, transcrever a
    tese integral entrega ao Juízo o melhor argumento do autor — transcrever apenas os itens 1 e 2, com
    reticências. Em casos só de verbas contratuais, a transcrição integral é inofensiva.
- **Ônus probatório:** art. 373, I, do CPC e art. 818, I, da CLT — cabe ao Reclamante descrever e provar a
  falha concreta de fiscalização (quem era o gestor/fiscal, qual notificação foi desatendida, qual
  irregularidade foi comunicada e não sanada). Não se exige da ECT prova de fato negativo absoluto (art. 5º,
  LV, da CF).
- **Culpa *in eligendo*:** inexistente — a contratação decorre de licitação regular (art. 37, XXI, da CF);
  a escolha é ato vinculado, não discricionário.
- **Culpa *in vigilando*:** Súmula 331, V, do TST é aplicada de forma indistinta na prática; sustentar que
  isso equivale a responsabilidade objetiva pela teoria do risco integral, incompatível com o art. 37, §6º,
  da CF e com a ADC 16. Somar: (i) ausência de poder de polícia da ECT sobre normas trabalhistas;
  (ii) limite intrínseco da fiscalização, sob pena de configurar intermediação de mão de obra e burla ao
  concurso público; (iii) juntada dos documentos de fiscalização efetivamente existentes.
- **Vedação de vínculo direto:** art. 37, II e §2º, da CF; **Súmula 331, II** e **Súmula 363** do TST —
  pedido de reconhecimento de vínculo "com as reclamadas" é juridicamente impossível quanto à ECT.
- **Ilegitimidade passiva:** arguir como preliminar (art. 330, II, c/c art. 485, VI, do CPC), reforçada pelo
  fato de todas as obrigações discutidas serem legalmente do empregador — CTPS (arts. 29 e 41 da CLT),
  salário (art. 457), FGTS (art. 15 da Lei 8.036/90), verbas rescisórias e guias (art. 477), EPI (arts. 157,
  158 e 166), PGR/PCMSO (arts. 157 e 168) e PPP (art. 58, §4º, da Lei 8.213/91).
- **Base de execução da ECT:** DL 509/69, art. 12, e DL 779/69, art. 1º — prazo em dobro, isenção de custas
  e depósito recursal, execução por precatório (STF, RE 220.906/DF e RE 220.699/SP), juros e correção pelo
  art. 3º da EC 113/2021.
- **Ponto processual que não pode ser esquecido:** havendo pluralidade de réus, a contestação de um deles
  afasta os efeitos da revelia (**art. 345, I, do CPC**). Se a prestadora for revel, é a defesa da ECT que
  segura toda a matéria de fato — por isso a peça deve impugnar **especificamente todos os fatos**, inclusive
  os "exclusivos" da empregadora, e requerer ofício à 1ª Reclamada para juntada da documentação funcional.
- **Ad cautelam, para eventual condenação:** benefício de ordem com esgotamento prévio contra a prestadora e
  seus sócios; limitação ao período da efetiva prestação em favor da ECT (**Súmula 331, VI**); exclusão de
  parcelas sancionatórias/personalíssimas (multas dos arts. 467 e 477 da CLT) e das obrigações de fazer
  (anotação de CTPS, PPP, guias); compensação (art. 767 da CLT); limitação aos valores dos pedidos
  (art. 840, §1º, da CLT).
- Ver modelo completo em `modelos/trabalhista/contestacao__responsabilidade_subsidiaria_terceirizacao.md`
  (+ `.docx`).

### 3.8 Adicional de insalubridade — limpeza e higienização de sanitários

Tema que aparece acoplado ao 3.7 (empregada de prestadora de limpeza que higieniza os banheiros da agência).

- **Tese do autor:** NR-15, **Anexo 14** (agentes biológicos) e **Súmula 448, II, do TST** — a higienização
  de instalações sanitárias de uso público ou coletivo **de grande circulação**, e a respectiva coleta de
  lixo, rende adicional em **grau máximo (40%)**.
- **Defesa:** o enquadramento não é automático — "uso público ou coletivo **de grande circulação**" é
  requisito qualificado e é questão de fato. Fora dessa hipótese incide a **OJ 4, II, da SBDI-1 do TST**
  (limpeza de residências e escritórios e respectiva coleta de lixo não são atividades insalubres).
  Levantar com a área gestora, para o *distinguishing*: porte da unidade, número e destinação de cada
  sanitário (uso restrito a empregados × aberto ao público) e média de atendimentos diários/mensais.
- **Prova técnica é indispensável:** art. 195, §2º, da CLT; no rito sumaríssimo, art. 852-H, §4º, da CLT.
  Requerer perícia, reservar quesitos e assistente técnico (usar os blocos do playbook, item 2.5).
- **EPI:** **Súmula 289 do TST** — o simples fornecimento não exime; exige-se prova de entrega, CA,
  substituição periódica, treinamento e fiscalização do uso. A documentação é da empregadora: requerer
  ofício à 1ª Reclamada, não assumir o encargo.
- **Base de cálculo:** salário mínimo (art. 192 da CLT), pois a **Súmula 228 do TST** teve a aplicação
  suspensa pelo STF e a **Súmula Vinculante 4** não autoriza a substituição da base por decisão judicial.
  Conferir se a CCT/ACT da categoria de asseio e conservação fixa base distinta.
- **Reflexos:** o adicional **integra a base de cálculo** das horas extras, e não o contrário — pedido de
  "reflexo em horas extras" é teratológico. Para mensalista, não há reflexo em RSR.
- **Precedente que a parte autora costuma invocar** (tese adversa, registrar para *distinguishing*):
  TST-RR 269-75.2011.5.04.0015, 3ª T., Rel. Min. Alberto Luiz Bresciani de Fontan Pereira, DEJT 24/05/2013 —
  limpeza de banheiros **em agência dos Correios**, com enquadramento no Anexo 14 da NR-15 e afastamento da
  OJ 4, II. A distinção se faz na moldura fática (grande circulação e ausência de registro de EPI foram
  premissas fixadas em perícia naquele caso).

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
