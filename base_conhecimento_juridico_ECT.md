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
- **Doença ocupacional** — ver a frente 0 da seção 3.4: o marco não é a extinção do contrato, mas a **ciência inequívoca da lesão e a sua consolidação**.

### 3.3 Prerrogativas processuais da ECT
- **Prazo em dobro** — art. 1º do Decreto-lei 779/69, combinado com a equiparação à Fazenda Pública do art. 12 do Decreto-lei 509/69, recepcionado pela CF/88 (STF, **RE 220.906/DF**).
- **Dispensa de preparo/custas**.

### 3.4 Doença ocupacional
**Frente 0 — prescrição (prejudicial, antes de qualquer discussão de mérito):**
- Marco inicial = **ciência inequívoca da lesão e efetiva consolidação** (princípio da *actio nata*, art. 189 do CC;
  **Súmulas 230 do STF e 278 do STJ**), e não a extinção do contrato nem o ajuizamento.
- Ciência inequívoca **posterior à EC 45/2004** → incide o prazo trabalhista do art. 7º, XXIX, da CF (e não o civil);
  fixado pela SBDI-1 do TST, em composição completa, no **E-RR-2700-23.2006.5.10.0005** (Rel. Min. Aloysio Corrêa da
  Veiga, sessão de 22/05/2014).
- **Tese mais forte quando houve reabilitação profissional do INSS:** a real extensão da doença só é conhecida em um de
  dois resultados excludentes — aposentadoria por invalidez, ou cessação do benefício com retorno/readaptação. Logo, a
  **data do certificado de reabilitação (ou da cessação do benefício com readaptação) é o marco prescricional**, e as
  pretensões ligadas ao **cargo anterior** ficam atingidas por **prescrição total** (art. 487, II, do CPC), ainda que o
  contrato siga em vigor. Pedir sempre, sucessivamente, a prescrição quinquenal das verbas anteriores ao quinquênio.
- Não afasta a prejudicial a alegação de quadro "crônico e progressivo": o que se protrai é o *tratamento*, não o
  nascimento da pretensão.
- Precedentes (todos verificados em peça real aprovada): **TRT24 – ROT 0024198-95.2023.5.24.0004** (1ª Turma, Des.
  Nicanor de Araujo Lima, j. 09/07/2024 — carteiro reabilitado; prescrição total reconhecida); **TST – E-ED-ED-RR-315-98.2011.5.06.0018**
  (SBDI-1, Red. Min. Cláudio Mascarenhas Brandão, DEJT 16/08/2019); **TST – AIRR-620-92.2013.5.04.0204** (2ª T., Min.
  José Roberto Freire Pimenta, j. 19/08/2015 — é dele o raciocínio dos "dois resultados excludentes"); **TST –
  RR-92000-78.2009.5.04.0030** (2ª T., mesmo relator, j. 12/11/2014); **TST – RR-10165-68.2015.5.03.0165** (2ª T., mesmo
  relator, j. 14/10/2015); **TST – RR-11817-09.2017.5.15.0039** (4ª T., Min. Caputo Bastos, DEJT 18/09/2020 — mera
  exposição a agente nocivo, sem doença caracterizada, não atrai a Súmula 278 do STJ).

Depois da prejudicial, três frentes de defesa, sempre nesta ordem:
1. **Inexistência de incapacidade total e permanente** — incapacidade parcial/temporária, reversibilidade (sobretudo em quadros psiquiátricos), natureza temporária dos benefícios do INSS (DCB).
2. **Inexistência de nexo causal** — etiologia multifatorial, fatores extralaborais e familiares, antecedentes, espécie 31 x 91, NTEP/CNAE **5310-5/01**, art. 20, §1º, da Lei 8.213/91; eventual concausa deve ser quantificada.
3. **Inexistência de culpa da empregadora** — exames admissional e periódicos, PCMSO e riscos psicossociais, ausência de comunicação prévia à empresa; exigir do perito a indicação da **norma específica** supostamente descumprida.
   - **Reabilitação profissional como prova de diligência:** quando a ECT encaminhou o empregado ao Programa de
     Reabilitação Profissional do INSS (art. 89 e ss. da Lei 8.213/91; art. 140 do Decreto 3.048/99), ministrou o
     curso/treinamento da nova função e o aproveitou em atividade compatível **sem redução salarial**, o certificado
     expedido pela autarquia é prova documental de conduta diligente — e desmonta a alegação de "manutenção do
     empregado em função incompatível". Serve simultaneamente à frente 0 (marco prescricional) e a esta.
   - Emissão de **CAT** pela empregadora é cumprimento do dever do art. 22 da Lei 8.213/91 — não confissão de culpa.
- Ver modelo completo em `modelos/trabalhista/contestacao__doenca_ocupacional.md` (formatação em `modelos/_FORMATO_BASE.docx`).

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

### 3.7 Impugnação ao pedido de justiça gratuita
- Base atual: **Súmula 463, I, do TST** (basta a declaração de hipossuficiência) e **Tema 21 do IRR do TST**
  (0000277-83.2020.5.09.0084): item I — concessão de ofício a quem percebe até 40% do teto do RGPS; item II — acima
  desse patamar, admite-se declaração particular (Lei 7.115/83); **item III — havendo impugnação da parte contrária
  acompanhada de prova, abre-se vista e decide-se o incidente**. É por esse item III que a defesa entra: impugnar
  sempre **com prova documental** (fichas financeiras e contracheques), nunca por simples negativa.
- **ADC 80 (STF)** — proposta pela **CONSIF**, relator o Min. **Edson Fachin**, tem por objeto a constitucionalidade
  dos **§§ 3º e 4º do art. 790 da CLT** (critérios da gratuidade na Justiça do Trabalho; suficiência ou não da simples
  autodeclaração). Estado do julgamento e teses em construção:
  - **Voto do relator:** constitucionalidade dos dispositivos, com interpretação conforme, admitindo a autodeclaração
    como meio de prova e reputando constitucional a Súmula 463 do TST; a presunção é **relativa** e **cede diante de
    impugnação fundamentada**; declaração falsa gera responsabilidade civil e penal.
  - **Divergência do Min. Gilmar Mendes:** presunção de hipossuficiência limitada a quem percebe até cerca de
    **R$ 5.000,00 mensais**; acima disso, incumbe ao interessado **comprovar concretamente** a insuficiência de
    recursos. Acompanhada, até a última assentada, pelos Ministros Zanin, Alexandre de Moraes, Flávio Dino e Dias
    Toffoli (placar de 5 x 1 antes do destaque).
  - **Andamento:** julgamento iniciado em plenário virtual em 28/11/2025; **destaque pedido pelo próprio relator em
    08/04/2026** (placar zerado); retomada em **sessão presencial de 21/05/2026**, com sustentações orais; **sem
    proclamação de resultado** até 25/08/2026.
  - **Uso na peça:** invocar como **reforço argumentativo** — as duas teses em disputa levam ao mesmo resultado quando
    a impugnação vem instruída com prova e o salário supera os patamares (40% do teto / R$ 5.000,00). Nunca tratar como
    precedente vinculante enquanto não houver trânsito.
  - `[REVISAR]` Dados de andamento coletados em 25/08/2026 a partir de **notícias e publicações especializadas** (o
    portal do STF não estava acessível na sessão). **Conferir o andamento no portal do STF antes de cada protocolo** —
    e atualizar esta seção quando o julgamento se encerrar.
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
