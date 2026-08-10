# Checklist de formatação e conversão de peças — ECT / Contencioso Trabalhista

> Complemento da `base_conhecimento_juridico_ECT.md` (seção 4 — Padrão formal das peças).
> Use este arquivo em conjunto com os prompts 2.x (redação) e 3.3 (conversão) do
> `playbook_prompts_ECT.md`.

---

## 1. Limitação técnica importante

O Claude **não edita diretamente arquivos .odt** dentro de uma conversa comum —
.odt é um formato binário (ZIP + XML) que exige uma ferramenta específica. Na
prática, dois caminhos funcionam:

1. **Via skill de Word (.docx):** peça a minuta em **.docx** (o assistente tem uma
   skill dedicada para isso, com controle de fonte, espaçamento, cabeçalho,
   rodapé e numeração). Depois converta .docx → .odt no LibreOffice
   (`Arquivo → Salvar como → ODF Texto` ou, em lote, `soffice --headless
   --convert-to odt arquivo.docx`).
2. **Via texto estruturado:** peça a minuta em texto puro/Markdown já na ordem
   final das seções, e você mesmo cola no modelo .odt existente (mantém 100% da
   formatação original, mas exige colar manualmente).

Para peças novas, o caminho 1 é mais rápido; para reaproveitar um modelo com
formatação elaborada (logotipo, cabeçalho institucional), o caminho 2 é mais
seguro. **Nunca confie na formatação de um .odt/.docx gerado sem confirmar
visualmente** — abra o arquivo final antes de protocolar.

---

## 2. Especificação do padrão formal (referência rápida)

| Item | Padrão |
|---|---|
| Fonte | Arial 11 |
| Entrelinha | 1,5 |
| Parágrafos | Justificados, com recuo de primeira linha |
| Margem esquerda | 2 cm |
| Margem direita | ~1,25 cm |
| Cabeçalho | Logotipo dos Correios + "Assessoria Jurídica" |
| Rodapé | Endereço + numeração de páginas |
| Citação de jurisprudência | Bloco recuado (~3 cm) |
| Fecho | "N. Termos / P. Deferimento. / Campo Grande/MS, data de assinatura eletrônica." |
| Assinatura | Bloco centralizado — Marcos Hideki Kamibayashi, OAB/MS 14.580 |

---

## 3. Passo a passo para gerar uma peça nova replicando o modelo

1. Anexe o `<MODELO.odt>` (ou .docx) **junto** com os documentos do processo na
   mesma conversa — o Claude só replica com fidelidade o que consegue ler no
   próprio arquivo.
2. Peça primeiro a etapa de **análise** (prompts 1.x do playbook) — nunca pule
   direto para a redação.
3. Na etapa de redação (2.x), inclua explicitamente:
   > "Replique integralmente a formatação (cabeçalho, fonte, espaçamento,
   > margens, rodapé, bloco de assinatura) do arquivo `<MODELO.odt>` anexado."
4. Gere em .docx usando a skill de documentos.
5. Rode o **checklist de verificação pós-geração** (seção 4) antes de converter
   para .odt.
6. Converta para .odt (se for o formato final exigido) e rode o checklist de
   novo — a conversão pode alterar espaçamento ou quebras de página.

---

## 4. Checklist de verificação pós-geração/conversão

Antes de protocolar, confira manualmente (não delegue esta etapa):

- [ ] Fonte Arial 11 em todo o corpo (inclusive em blocos de citação)
- [ ] Entrelinha 1,5 mantida após a conversão
- [ ] Parágrafos justificados com recuo de primeira linha
- [ ] Margens conforme padrão (2 cm esq. / ~1,25 cm dir.)
- [ ] Cabeçalho com logotipo e "Assessoria Jurídica" presente em todas as páginas
- [ ] Rodapé com endereço e numeração de páginas correta (sem reiniciar contagem)
- [ ] Citações de jurisprudência em bloco recuado (~3 cm), destacadas do corpo
- [ ] Fecho padrão presente ("N. Termos / P. Deferimento...")
- [ ] Bloco de assinatura centralizado, com nome e OAB corretos
- [ ] Quebras de página não deixaram títulos "órfãos" (título sozinho no fim da página)
- [ ] Numeração de itens/seções contínua e sem duplicação após edições
- [ ] Nome do arquivo final segue a convenção da seção 6 da base de conhecimento

---

## 5. Prompt pronto de verificação de formatação

Use depois de gerar/converter, antes do protocolo:

```
Revise apenas a formatação do arquivo anexado (não o conteúdo jurídico):
- confirme fonte, tamanho e entrelinha em todo o documento;
- confirme margens;
- confirme presença e conteúdo de cabeçalho e rodapé em todas as páginas;
- confirme numeração de páginas contínua;
- confirme que blocos de citação de jurisprudência estão recuados e
  destacados do corpo do texto;
- aponte qualquer inconsistência de formatação entre seções.
Liste apenas os problemas encontrados, com a localização de cada um.
```

---

## 6. Nomenclatura final do arquivo

Confirme antes de salvar/enviar (ver seção 6 da base de conhecimento):

`Tipo - Tema abreviado - Rito - NOME DA PARTE.odt`

Abreviações usuais: `Cont` (contestação) · `RR` (recurso de revista) ·
`Inc Fun` (incorporação de função) · `Manifest` (manifestação).

---

## Lacunas deste checklist (preencher)

- [ ] Confirmar se há modelo .odt padrão único ou um por tipo de peça
- [ ] Definir se a conversão final para protocolo deve ser sempre .odt ou se o
      PJe aceita .docx/.pdf diretamente
- [ ] Registrar problemas recorrentes de conversão observados na prática, para
      alimentar este checklist
