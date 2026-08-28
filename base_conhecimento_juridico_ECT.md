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
| Contraminuta a embargos de declaração | Reclamante embarga alegando omissão na sentença (art. 897-A, § 2º, CLT) |

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

### 3.7 Honorários de sucumbência — defesa do *quantum* quando a sentença é omissa

Cenário: a ECT sucumbe, mas a sentença nada decide sobre os honorários pedidos pelo Reclamante, e este opõe
embargos de declaração para suprir a omissão. A omissão costuma ser real — negá-la em bloco desgasta a defesa
sem evitar a condenação. **A disputa útil é a do critério de cálculo, não a da existência da verba**: entre
15% sobre o valor da causa e 5% sobre o valor arbitrado à condenação há, tipicamente, duas ordens de grandeza.

**Regra estratégica anterior a tudo:** se a sentença é omissa quanto aos honorários do Reclamante, **a ECT não
deve suscitar essa omissão** — nem em embargos próprios, nem "para organizar o julgado". O silêncio é um ativo.
Suscitá-lo provoca a condenação que não existia. Espere os embargos da parte contrária, se vierem.

Argumentos, na ordem em que se sustentam:

1. **Norma de regência é o art. 791-A da CLT, não o art. 85 do CPC.** O art. 791-A é específico do processo do
   trabalho e posterior, e disciplina exaustivamente limites percentuais (5% a 15%), base de cálculo e critérios
   de arbitramento. Não havendo omissão a colmatar, não incide o processo comum (art. 769 da CLT e art. 15 do CPC).
2. **O capítulo de direito intertemporal da própria sentença.** As sentenças em geral abrem com um tópico
   fixando que a Lei 13.467/2017 rege honorários, custas e periciais, sendo a sentença o marco temporal. Esse
   capítulo costuma **não ser embargado** — logo, pedir a aplicação do art. 85 do CPC é pedir que o juízo
   contradiga parte não impugnada do próprio julgado que se quer apenas integrar. É o argumento mais forte,
   porque não depende de tese controvertida: depende do texto da decisão.
3. **Pinça sobre a Súmula 219 do TST.** O Reclamante invoca o verbete (Fazenda Pública → percentuais do CPC)
   para elevar o percentual. Responder que (a) o verbete nasceu em contexto de honorários assistenciais,
   anterior à sistematização da Lei 13.467/2017, e não prevalece sobre regra legal expressa e superveniente; e
   (b) **se o CPC vier, vem inteiro** — inclusive o art. 85, § 8º, que impõe arbitramento por apreciação
   equitativa quando o proveito econômico for inestimável ou irrisório. Não se invoca o Código só na parte que
   amplia percentual.
4. **Base de cálculo.** O art. 791-A, *caput*, ordena os critérios: liquidação da sentença → proveito econômico
   → *residualmente* valor atualizado da causa. Havendo **valor arbitrado à condenação** na própria sentença
   (comum em obrigação de fazer, ainda que arbitrado "para fins estatísticos"), é sobre ele que o percentual
   incide. O valor da causa costuma ser convencional (ex.: 12 salários-base) e não traduzir proveito algum.
   Cuidado: sustentar apenas "não há proveito mensurável" é contraproducente — a própria letra do *caput*
   remete, nessa hipótese, ao valor da causa, que é o que a parte contrária quer.
5. **Contradição do próprio pedido.** Quando o Reclamante pede percentual sobre o valor da causa "em razão de o
   direito pleiteado não ter efeito pecuniário", ele afirma e nega o proveito na mesma frase. Usar a afirmação
   dele para ancorar o arbitramento equitativo.
6. **Percentual mínimo de 5%, pelos critérios do art. 791-A, § 2º** (zelo, lugar, natureza e importância,
   trabalho realizado e tempo exigido): rito sumaríssimo, matéria exclusivamente de direito, tese já pacificada
   em precedente vinculante — o que reduz o trabalho do causídico —, ausência de dilação probatória relevante,
   tramitação célere, serviço prestado na comarca do domicílio dos patronos. Relevância social da causa não é
   critério legal de majoração.
7. **Repelir a majoração por "resistência" e por atos futuros.** É frequente o embargante sustentar que a ECT
   não se curvou ao comando judicial e esgotará as instâncias. Responder com: (a) o **próprio julgado** que
   reconhece o cumprimento da tutela e não aplica um dia de multa; (b) recorrer é exercício do art. 5º, LV, da
   CF, não conduta apenável; (c) honorários não se arbitram sobre trabalho hipotético de instância superior,
   que tem sede e momento próprios.
8. **Destinação da verba — assistência sindical.** Se a inicial declara o Reclamante assistido por sindicato
   nos termos da **Lei 5.584/70**, por advogada credenciada, a destinação de eventual verba segue o regime
   próprio dessa assistência. Confirmar a credencial nos autos antes de suscitar.
9. **Condicionalidade e art. 1.024, § 4º, do CPC.** Consignar que o arbitramento fica subordinado à manutenção
   do capítulo principal (provido o recurso, inverte-se a sucumbência) e requerer o prazo para complementar as
   razões do recurso já interposto, nos limites da modificação — art. 1.024, § 4º, do CPC c/c art. 769 da CLT.

Fundamento da própria manifestação: **art. 897-A, § 2º, da CLT** e **art. 1.023, § 2º, do CPC** — a oitiva da
parte contrária é obrigatória porque o acolhimento acrescenta capítulo condenatório, com efeito modificativo.

Ver modelo completo em `modelos/trabalhista/contraminuta_ed__honorarios_sucumbenciais.md`.

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
