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
| Contrarrazões de Recurso Ordinário | Defesa da sentença favorável, endereçada ao TRT24 — formatação em `modelos/trabalhista/contrarrazoes_ro__FORMATO.docx` |
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

### 3.7 Multa do art. 477, §8º, da CLT — base de cálculo e limites do pedido

- **Base de cálculo — tese adversa, e vinculante.** O Pleno do TST, no **Tema 142** da Tabela de Incidência
  de Recursos Repetitivos (**RR-11070-70.2023.5.03.0043**, acórdão publicado no **DJEN em 22/05/2025**),
  fixou: *"A multa prevista no art. 477, § 8º, da CLT incide sobre todas as parcelas de natureza salarial,
  não se limitando ao salário-base"*. O TRT24 aplica a tese nas **duas Turmas**. Não há tese da ECT que
  negue frontalmente o Tema 142 — e **não convém tentar**: desqualificar a eficácia de IRR do TST
  contradiz o item 3.1 desta base, que depende do Tema 23 do Pleno.
- **O que sobra de defesa, em ordem de força:**
  1. **Limite do valor do pedido.** A multa do art. 477, §8º, é verba de valor **único, atual e
     integralmente determinável no ajuizamento** — o Reclamante dispõe do próprio contracheque e apura ao
     centavo. Valor atribuído ao pedido, portanto, **vincula** (arts. 141 e 492 do CPC; art. 840, §1º, da
     CLT). Confrontar sempre o valor pedido na inicial com o valor deferido: a diferença é o **teto**
     aritmético do recurso.
     - Contra-argumento previsível: valores da inicial como meras estimativas (**art. 12, §2º, da IN
       41/2018 do TST**). Responder que a orientação foi concebida para pedidos de quantificação futura
       (horas extras, reflexos, diferenças ao longo do contrato), não para verba líquida e atual. Verificar
       sempre se a inicial contém **ressalva expressa de estimativa** — a ausência reforça decisivamente.
  2. **Inovação recursal.** Reconstituir a **memória de cálculo da inicial** por aritmética: se o valor
     pedido equivale ao salário-base acrescido de um percentual identificável (ex.: anuênio), as demais
     verbas que o recurso pretende agregar **não integraram o pedido** — inovação (art. 1.014 do CPC;
     Súmula 393 do TST). Somar os pedidos e conferir contra o valor da causa confirma que o valor foi
     apurado, e não arbitrado.
  3. **A sentença já pode ter aplicado o critério certo.** Verificar se a decisão apurou a multa citando
     o **art. 457, §1º, da CLT** — que é o próprio conceito de remuneração adotado pelo Tema 142. Se sim,
     não há violação da tese: há divergência de *quantum*, que o recorrente tem o ônus de demonstrar.
  4. **Ônus de demonstração.** Recurso que não reproduz as rubricas do contracheque, não indica valores,
     não apresenta cálculo e não impugna a planilha da sentença líquida não demonstra o erro que alega. E
     provimento em termos genéricos converteria sentença líquida em ilíquida.
  5. **Natureza das verbas — subsidiário e frágil.** O Tema 142 dá o critério ("parcelas de natureza
     salarial"), não a lista. Anuênio é salarial por força do art. 457, §1º — **não vale brigar**.
     Gratificação de função é **salário-condição** (item 3.1); CIP exige conferir a cláusula do ACT.
     Cuidado duplo: (a) se a contestação não impugnou a base de cálculo, a tese é atacável por preclusão
     (art. 342 do CPC; art. 847 da CLT) e deve ser formulada como *ausência de demonstração pelo
     recorrente*; (b) conferir se o contracheque/GFIP registra incidência de FGTS e contribuição
     previdenciária sobre a verba — se registra, a natureza salarial é difícil de negar.
- **Exceção do próprio §8º** — a multa não incide "quando, comprovadamente, o trabalhador der causa à
  mora". Tese de fato, que exige prova robusta: alegação de alteração de conta bancária pelo empregado sem
  comunicação **não se sustenta** se os extratos mostrarem que os salários já eram creditados na conta
  "nova". Registrado como derrota real (ver item 8). Ainda que houvesse falha de comunicação, o juízo
  tende a exigir da empregadora o **depósito em consignação** dentro do prazo do art. 477, §6º.
- **Dano moral por atraso rescisório** — capítulo em que a ECT tende a vencer: a inadimplência de
  obrigação sujeita-se ao art. 389 e seguintes do CC, não ao art. 186, e o art. 403 do CC limita a
  reparação aos prejuízos diretos e imediatos (STF, **RE 130.764**, Rel. Min. Moreira Alves, DJ
  07/08/1992). Precedente do TRT24 no mesmo sentido: **0024820-42.2021.5.24.0006**, 1ª Turma, Rel. Julio
  Cesar Bebber, 28/11/2022 — sonegação de direito trabalhista, por si só, gera dano patrimonial, não
  extrapatrimonial. Atenção à divergência interna do Regional: a 2ª Turma reconhece dano moral *in re
  ipsa* em **inadimplemento salarial reiterado** (ROT 0024548-57.2024.5.24.0066, Rel. Des. Marco Antonio
  de Freitas, 17/04/2026) — hipótese distinta do atraso rescisório único.
- **Arestos do TRT24 sobre o Tema 142** (todos localizados em recurso adversário, conferir teor antes de
  usar): ROT 0024548-57.2024.5.24.0066 (2ª T., Marco Antonio de Freitas, 17/04/2026); RORSum
  0024741-54.2024.5.24.0072 (2ª T., João de Deus Gomes de Souza, 05/02/2025 — base ampliada por **horas
  extras habituais deferidas na condenação**, bom material de *distinguishing*); ROT
  0027436-37.2024.5.24.0021 (1ª T., André Luís Moraes de Oliveira, 17/12/2025); ROT
  0024631-73.2024.5.24.0066 (1ª T., Nicanor de Araújo Lima, 29/07/2025); ROT 0024544-20.2024.5.24.0066
  (1ª T., Marcio Vasques Thibau de Almeida, 29/07/2025).
- **Rescisão por acordo (art. 484-A da CLT)** não afasta o prazo do art. 477, §6º, nem a multa do §8º.
- **Licença para tratar de assuntos particulares (LTAP)** suspende o contrato sem remuneração — hipótese
  **distinta** do afastamento previdenciário do item 3.6. Consequência prática: no período de LTAP não há
  remuneração paga pela ECT, e o parâmetro do art. 477, §8º, é o último contracheque anterior à suspensão.
- Formatação e estilística das contrarrazões: `modelos/trabalhista/contrarrazoes_ro__FORMATO.md`
  (+ `.docx`).

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

---

## 8. Lições de peças anteriores (conferir antes de protocolar a próxima)

Registro de falhas reais detectadas em peças já protocoladas, para não se repetirem. Não são teses: são
itens de checklist.

- **Impugnar sempre o valor atribuído a cada pedido, e não só o do dano moral.** Numa contestação de multa
  do art. 477, §8º, a omissão custou caro: sem impugnação ao valor do pedido nem à base de cálculo, a
  defesa perdeu, em contrarrazões, a possibilidade de discutir a natureza das verbas sem incorrer em
  preclusão (art. 342 do CPC; art. 847 da CLT). Ver item 3.7.
- **Cuidado com a descrição do pedido alheio.** Descrever o pedido do autor como "multa no importe da
  **última remuneração**" equivale a admitir a base remuneratória. Descrever o pedido pelos termos em que
  a inicial o formulou, sem qualificá-lo.
- **Não pedir correção monetária pela TR / OJ 300 da SDI-1.** Critério superado (ADIs 4357 e 4425; RE
  870.947 – Tema 810; EC 113/2021 – SELIC). O pedido ainda aparece em contestações antigas e contradiz o
  próprio requerimento de aplicação da EC 113/2021 feito na mesma peça.
- **Incluir requerimento de prequestionamento na contestação**, e não só nos recursos (estrutura da seção
  2.1 do playbook, bloco VI).
- **Conferir endereçamento e data antes de assinar.** Já foram protocoladas peças com "Campo Grande/**SP**"
  no endereçamento e com data anterior aos próprios fatos discutidos — resíduo de reaproveitamento.
- **Varrer resíduo de peça reaproveitada.** Menções a "adicional", "descontos ilícitos" ou a temas de outro
  processo (ex.: aresto sobre AADC em caso de atraso rescisório) enfraquecem a peça e sinalizam ao juízo
  que ela não foi escrita para aqueles autos.
- **Numeração de tópicos sem saltos** (já ocorreu "2." seguido de "3.1", sem item 3).
