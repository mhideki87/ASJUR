# Contexto permanente — Assessoria Jurídica ECT

> **Este é o único arquivo da base que deve ser lido em toda sessão, sempre por inteiro.** É curto de
> propósito. Ele não contém teses: teses ficam em `teses/<área>/<tema>.md` e são lidas **sob demanda**,
> a partir do roteamento de [INDICE.md](INDICE.md).
>
> No Projeto do claude.ai, é este arquivo (não a base inteira) que vai nas **instruções personalizadas**.

---

## 1. Quem sou eu (usuário)

- Advogado da **Assessoria Jurídica da Empresa Brasileira de Correios e Telégrafos (ECT)**.
- Assinatura das peças: **Marcos Hideki Kamibayashi — OAB/MS 14.580**.
  - Em peças cíveis também já apareceu **Marcos Henrique Boza — OAB/MS 13.041-B** `[REVISAR: confirmar se
    a área cível usa outra assinatura ou se foi caso isolado]`.
- Base: **Campo Grande/MS**.
- **Trabalhista:** jurisdição do **TRT da 24ª Região** e Varas do Trabalho de Campo Grande. Sistema **PJe**.
  Ritos **sumaríssimo (ATSum)** e ordinário.
- **Cível:** **Juizados Especiais Federais (JEF)** e **Justiça Federal comum (1º e 2º grau, TRF3)**
  `[REVISAR: confirmar se há também Justiça Estadual / Juizados Estaduais]`.
- Atuo **sempre no polo passivo** — a ECT é Reclamada/Ré. Toda peça é de defesa.
  - Exceção a confirmar em cível `[REVISAR: 3 petições iniciais catalogadas — verificar se há atuação
    no polo ativo, ex.: cobrança]`.

---

## 2. O que eu produzo

| Peça | Contexto típico |
|---|---|
| Contestação / Defesa | Resposta à inicial (trabalhista e cível) |
| Contrarrazões de recurso | Defesa da sentença favorável (TRT24 na trabalhista) |
| Recurso de revista | Sentença/acórdão desfavorável (trabalhista) |
| Quesitos para perícia | Médica (doença ocupacional) e técnica (insalubridade/periculosidade) |
| Manifestações | Documentos do INSS, laudos, cálculos, RPV, audiência |
| Embargos de declaração | Omissão/contradição + prequestionamento |
| Impugnação aos cálculos · Embargos à execução | Fase de execução (aparecem sobretudo em cível) |

Fluxo padrão na trabalhista: **petição de juntada à Vara → razões/contrarrazões ao TRT24**.

---

## 3. Padrão formal das peças

**Trabalhista** (validado, uso real):
- Formato: **.odt** (LibreOffice); conversão para .docx quando necessário.
- Fonte **Arial 11**, **entrelinha 1,5**, parágrafos **justificados** com recuo de primeira linha.
- Margens: esquerda 2 cm / direita ~1,25 cm.
- **Cabeçalho** com logotipo dos Correios + "Assessoria Jurídica"; **rodapé** com endereço e numeração.
- Citações de jurisprudência em bloco recuado (~3 cm).
- Fecho: "N. Termos / P. Deferimento. / Campo Grande/MS, data de assinatura eletrônica." + bloco de
  assinatura centralizado com nome e OAB.
- Estrutura usual das razões: síntese → preliminares/prejudiciais → mérito → *ad cautelam* →
  requerimentos com **prequestionamento**.

**Cível:** formato **.txt/.odt**; endereçamento a Juizado Especial Federal ou Vara Federal; mesmo fecho
("N. Termos / P. Deferimento. / Campo Grande/MS, [data]"). `[REVISAR: confirmar se cabeçalho, fonte,
espaçamento e demais regras da trabalhista também valem aqui, ou se cível tem modelo próprio]`.

O arquivo que materializa esse padrão é `modelos/_FORMATO_BASE.docx` — comece por ele em qualquer peça
nova (ver [modelos/README.md](modelos/README.md)).

---

## 4. Como eu quero que o Claude trabalhe

**Regras inegociáveis (valem para as duas áreas):**
1. **Não inventar nada** — jurisprudência, doutrina, número de processo, data, cláusula de ACT ou Id de
   documento. Se não tiver certeza, marcar `[REVISAR: ...]` ou `[INSERIR: ...]` no corpo do texto.
2. Só usar ementas que constem dos autos, do modelo anexado ou do próprio recurso adversário.
3. Sempre listar ao final, separadamente, **o que precisa de conferência humana**: datas de intimação e
   contagem de prazo, cômputo de tempo em função gratificada, Ids e cláusulas, e toda a jurisprudência citada.
4. Não presumir fatos ausentes dos documentos anexados; quando a defesa e a sentença divergirem,
   apoiar-se nos fatos da sentença e da capa do PJe.
5. Trabalhar em **duas etapas** na mesma conversa: análise estruturada primeiro, minuta depois.
6. Replicar **integralmente** a formatação da peça-modelo (ou de `modelos/_FORMATO_BASE.docx`).
7. Um processo por conversa — não misturar autos diferentes.
8. **Ler o índice, não a base inteira** — antes de analisar ou minutar, identificar o objeto da demanda e
   abrir só as fichas de tese que o [INDICE.md](INDICE.md) indicar. Ficha marcada `status: rascunho` é
   candidata a tese, não tese confirmada: validar contra o processo em mãos antes de usar.

---

## 5. Nomenclatura de arquivos que eu uso

`Tipo - Tema abreviado - Rito - NOME DA PARTE.odt`

Exemplos de padrão (parte real substituída por placeholder — **nenhum nome real neste repositório**):
`Cont_-_Inc_-_[NOME_DA_PARTE].odt` · `RR_-_Inc_Fun_-_Sumula_51_-_Rito_Sumarissimo_-_[NOME_DA_PARTE].odt` ·
`Quesitos_-_Pericia_Medica_-_[NOME_DA_PARTE].odt`

Abreviações: `Cont` = contestação · `RR` = recurso de revista · `Inc Fun` = incorporação de função ·
`Manifest` = manifestação.

---

## 6. Lacunas desta base (preencher com uso real)

Lacunas gerais, que não pertencem a nenhum tema específico:

- [ ] Estrutura da equipe e distribuição de processos
- [ ] Volume mensal e prazos internos de entrega
- [ ] Orientações da Consultoria Jurídica nacional da ECT que vinculam a defesa local
- [ ] Teses que a ECT decidiu *não* sustentar (trabalhista e cível)
- [ ] Outras matérias além de trabalhista e cível (consumidor? improbidade?)

Lacunas de um tema específico ficam na própria ficha, na seção "Lacunas".
