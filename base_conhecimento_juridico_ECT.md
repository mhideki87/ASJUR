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

### 3.7 AADC — Adicional de Atividade de Distribuição e/ou Coleta Externa (carteiro motorizado)

**Norma interna:** PCCS/2008, item **4.8** — 4.8.1 (atribuição), 4.8.1.1 (30% do salário-base), 4.8.1.2 (valor
fixo), 4.8.1.3 (25% do valor fixo) e **4.8.2** (supressão); regulamentado pelo **Capítulo 6 do Módulo 8 do
MANPES**. O item 8.9.1 do próprio PCCS/2008 registra que a parcela nasceu do Termo de Compromisso ECT/FENTECT.

**Origem da parcela** (documentação: *histórico* — Termo de Compromisso, ata de reunião e petição de
homologação): PL 82/2003 e PL 7362/2006, que criariam adicional de periculosidade para carteiros →
**veto presidencial** (Mensagem nº 863, de 19/11/2007) → **Termo de Compromisso ECT/FENTECT de 20/11/2007**
(abono emergencial de 30% do salário-base, a título de adicional de risco) → greve de 1º/7/2008 →
**ata de 19/7/2008** (pagamento definitivo de 30%, com as hipóteses de supressão do subitem 2.1) →
homologação no **TST-DC-195.656/2008-000-00-00.5**, em 21/7/2008. Daí a natureza de **adicional de risco**.

**Tese 1 — impossibilidade de cumulação com o adicional de periculosidade do art. 193, §4º, da CLT**
(incluído pela Lei 12.997/2014, regulamentado pelo **Anexo 5 da NR 16**, Portaria MTE 1.565/2014):
- AADC e adicional legal têm **idêntica natureza, fundamento, base de cálculo e alíquota** (30% do salário-base,
  art. 193, §1º, da CLT) — ambos remuneram a exposição a risco em via pública.
- Autorizam a supressão: **item 4.8.2 do PCCS/2008**; **item 4.5 do Cap. 6 do Mód. 8 do MANPES**; **alínea "a"
  do subitem 2.1 da ata de 19/7/2008**, homologada pelo TST; e a cláusula de **acumulação de vantagens** dos
  ACTs (renumerada a cada acordo — conferir o número no ACT do período).
- **Item 3.1.2 do Cap. 6 do Mód. 8 do MANPES**: é vedada a percepção simultânea dos adicionais.
- Argumento *a fortiori*: se a lei veda cumular insalubridade com periculosidade (art. 193, §2º, da CLT), com
  muito mais razão veda dois adicionais de periculosidade.

**Tese 2 — o AADC é salário-condição** (serve mesmo quando a supressão não decorreu da periculosidade):
- **Item 4.8.1 do PCCS/2008**: parcela atribuída "exclusivamente aos empregados que atuarem no **exercício
  efetivo** da atividade postal externa de Distribuição e/ou Coleta em vias públicas".
- **MANPES, Cap. 6 do Mód. 8**: item 4.2/4.2.1 (pagamento **proporcional aos dias em efetivo exercício**),
  item 4.4 (desconto de **1/30 por dia de ausência** não equiparada a efetivo exercício, cf. Anexo 1) e
  item 4.5 (**supressão** quando o empregado não mais desempenha a atividade).
- **Alínea "b" do subitem 2.1 da ata de 19/7/2008**: supressão "quando o referido empregado não mais exercer a
  atividade de distribuição e/ou coleta em vias públicas".
- Consequência: cessada a condição, cessa a parcela — sem alteração contratual lesiva (art. 468 da CLT) nem
  ofensa à irredutibilidade salarial (art. 7º, VI, da CF). O fato constitutivo (exercício efetivo no período)
  é ônus do autor (art. 818, I, da CLT; art. 373, I, do CPC).

**Prova técnica:** **Laudo Técnico Pericial do DESAU**, elaborado por Engenheiro de Segurança do Trabalho na
forma do art. 195 da CLT e do item 16.3 da NR 16, que (i) enquadra as funções motorizadas "M" e "MV" no Anexo 5
da NR 16 e (ii) conclui pela **substituição** do AADC pelo adicional de periculosidade, e não pela soma.

**Contra-argumento de isonomia:** o carteiro motorizado percebe, além do adicional legal, a **gratificação de
função convencional motorizada** ("M", "MV", "V"), não suprimida — critérios de acesso no **item 9 do
Capítulo 2 do Módulo 1 do MANTRA**. Some-se a **Súmula 361 do TST**: o adicional de periculosidade não comporta
proporcionalidade nem graduação por tipo de atividade.

**Prescrição:** sendo a supressão **ato único** e a parcela decorrente de **norma interna** (não assegurada por
preceito de lei), aplica-se a **prescrição total** — Súmula 294 do TST e art. 11, §2º, da CLT (ver seção 3.2).

**Precedentes** (conferir a íntegra antes de transcrever): TST **RR-1254-27.2015.5.06.0313** (8ª Turma, Min.
Dora Maria da Costa, julgado em 07/12/2016, DEJT 12/12/2016) — impossibilidade de cumulação, caso da própria
ECT; TST **RR-122900-58.2008.5.02.0087** (7ª Turma, Min. Vieira de Mello Filho, 01/06/2016) — vedação de dois
adicionais de periculosidade; TRT 1ª Região **RO 0010998-96.2015.5.01.0018** e **RO 0010294-22.2014.5.01.0082**;
TRT 13ª Região **RO 0131247-94.2015.5.13.0001** e **RO 0131182-90.2015.5.13.0004**.

**Documentos que instruem a defesa:** histórico da parcela (Termo de Compromisso, ata de 19/7/2008 e petição de
homologação no TST), Laudo Técnico do DESAU, PCCS/2008, MANPES (Mód. 8, Cap. 6) e MANTRA (Mód. 1, Cap. 2),
ACTs do período, ficha cadastral/funcional e ficha financeira.

**Conferir sempre, antes de fechar a tese:**
- O **motivo formal** da supressão na ficha cadastral/financeira — periculosidade, afastamento, restrição médica
  ou remanejamento para atividade interna mudam qual das duas teses é a principal.
- O enquadramento no item **4.8.1.1 (30% do salário-base)** ou **4.8.1.2 (valor fixo)**, conforme cargo e função.
- Se houve pagamento simultâneo das duas parcelas no período (fundamenta compensação / *bis in idem*).
- Existência de **ação coletiva do sindicato** sobre a mesma matéria — art. 104 do CDC.

---

## 4. Padrão formal das peças

> Fonte da verdade da formatação: **`modelos/_FORMATO_BASE.docx`**. A lista abaixo descreve o que o arquivo
> contém — em caso de divergência, vale o arquivo. Toda peça nova, de qualquer tipo, começa por ele.

- Formato: **.odt** (LibreOffice); conversão para .docx quando necessário.
- Fonte **Arial 11**, **entrelinha 1,5 exata**, parágrafos **justificados** com recuo de primeira linha de **3 cm**.
- Margens: esquerda **3 cm** / direita **2 cm** / superior **3 cm** / inferior **2 cm**.
- **Cabeçalho** com logotipo dos Correios + "Assessoria Jurídica MS/DEJUR/SEJUR"; **rodapé** com endereço e numeração de páginas. Ambos a **0,7 cm** da borda da página.
- **Títulos de seção** — vale para **todas as peças**, não só contestação: **CAIXA ALTA**, **negrito**,
  **centralizados** e **dentro de um quadro** (borda simples nos quatro lados), sem numeração romana.
  São só os blocos maiores: `DA EQUIPARAÇÃO À FAZENDA PÚBLICA`, `SÍNTESE DA DEMANDA`, `PRELIMINARMENTE`,
  `PREJUDICIAL DE MÉRITO`, `DO MÉRITO`, `DOS PEDIDOS` — e os equivalentes de cada tipo de peça.
- **Subtítulos** (dentro de uma seção): **CAIXA ALTA**, **negrito e sublinhado**, numerados (`1.`, `1.1.`),
  justificados, com recuo de 3 cm à esquerda e sem recuo de primeira linha.
- Citações de lei, norma interna e jurisprudência em bloco recuado de **3 cm**, sem recuo de primeira linha.
- Fecho: "Nesses Termos, / Pede Deferimento. / Campo Grande/MS, data de assinatura eletrônica." + bloco de assinatura centralizado com nome e OAB.
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
