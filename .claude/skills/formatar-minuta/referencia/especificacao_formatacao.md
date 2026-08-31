# Especificação de formatação — padrão ASJUR/ECT

Medidas extraídas do XML de uma peça real aprovada (a mesma de onde saiu `modelos/_FORMATO_BASE.docx`).
Unidade nativa do Word é o **twip** (1/20 de ponto; 1 cm = 566,93 twips; 1 pt = 20 twips). A coluna "twips"
é a que vale — as demais são conversão de conferência.

## 1. Página (`w:sectPr`)

| Item | Valor XML | Equivalente |
|---|---|---|
| Tamanho | `w:pgSz w:w="11906" w:h="16838"` | A4 — 21,0 × 29,7 cm |
| Margem esquerda | `w:left="1701"` | 3,0 cm |
| Margem direita | `w:right="1134"` | 2,0 cm |
| Margem superior | `w:top="1701"` | 3,0 cm |
| Margem inferior | `w:bottom="1134"` | 2,0 cm |
| Distância do cabeçalho | `w:header="397"` | 0,7 cm |
| Distância do rodapé | `w:footer="397"` | 0,7 cm |
| Medianiz | `w:gutter="0"` | 0 |
| Numeração de página | `w:pgNumType w:fmt="decimal"` | 1, 2, 3… |

Largura útil da linha: 11906 − 1701 − 1134 = **9071 twips (16,0 cm)** — é essa a largura da tabela do
cabeçalho e a posição da tabulação direita do rodapé.

## 2. Fonte e padrões do documento

| Item | Valor XML | Equivalente |
|---|---|---|
| Fonte padrão | `w:rFonts ascii/hAnsi/eastAsia/cs="Arial"` | Arial |
| Corpo do texto | `w:sz w:val="22"` | **11 pt** |
| Citação / cálculo | `w:sz w:val="20"` | 10 pt |
| Cabeçalho da página | Arial Narrow, `w:sz w:val="24"` | 12 pt |
| Rodapé da página | Arial Narrow, `w:sz w:val="14"` | 7 pt |
| Idioma | `w:lang w:val="pt-BR"` | Português (Brasil) |
| Hifenização | `w:suppressAutoHyphens w:val="true"` | desligada |
| Controle de linhas órfãs/viúvas | `w:widowControl` (ligado no estilo `Normal`) | ligado |

Todo parágrafo usa o estilo `Normal` — o padrão **não** usa `Título 1..6`, nem `Corpo do texto`, nem lista
numerada automática (`w:numPr` não aparece uma única vez no documento de referência).

## 3. Espaçamento — a regra que mais se erra

O padrão usa **entrelinha exata**, não múltipla:

```xml
<w:spacing w:lineRule="exact" w:line="360" w:before="0" w:after="120"/>
```

- `lineRule="exact"` + `line="360"` = **exatamente 18 pt** entre linhas (no Word: Espaçamento entre linhas →
  *Exatamente* → 18 pt). Não é "1,5 linha", que é `lineRule="auto" line="360"` e dá resultado diferente.
- `line="240"` = exatamente 12 pt (citações e tópico em retângulo).
- `before`/`after` em twips: `120` = 6 pt · `160` = 8 pt · `200` = 10 pt · `260` = 13 pt · `320` = 16 pt ·
  `40` = 2 pt · `60` = 3 pt · `100` = 5 pt.

## 4. Blocos, um a um

Recuos em twips: `1701` = 3,0 cm · `2268` = 4,0 cm.

### 4.1 Endereçamento
`jc=both` · `spacing exact 360, before 0, after 160` · `ind hanging=0` (sem recuo de 1ª linha) ·
Arial 11 **negrito**, caixa alta.
Depois dele, **4 parágrafos vazios** com `spacing after=200`.

### 4.2 Autos e polos
Três parágrafos, `jc=both` · `spacing exact 360, before 0, after 160` · `ind hanging=0`:
`Autos nº. <número>.` inteiro em negrito; `RECLAMANTE: ` (rótulo em negrito) + nome em texto normal;
`RECLAMADA: ` + `EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS.`
Depois deles, **2 parágrafos vazios** com `spacing after=200`.

### 4.3 Preâmbulo (qualificação da ECT)
`jc=both` · `spacing exact 360, before 0, after 120` · `ind firstLine=1701` · Arial 11.
Em negrito: a razão social + superintendência, o nome da parte adversa, o tipo de ação e o nome da peça.

### 4.4 Tópico principal — retângulo + caixa alta
```xml
<w:pPr><w:pStyle w:val="Normal"/><w:jc w:val="center"/>
  <w:spacing w:lineRule="exact" w:line="240" w:before="320" w:after="260"/>
  <w:ind w:left="0" w:right="0" w:hanging="0"/>
  <w:pBdr>
    <w:top    w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:left   w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:right  w:val="single" w:sz="6" w:space="4" w:color="000000"/>
  </w:pBdr>
</w:pPr>
```
Borda simples de `sz=6` (0,75 pt) nos quatro lados, `space=4` (4 pt de folga interna), preta.
Texto: Arial 11 **negrito**, **caixa alta digitada** (não há `w:caps`), centralizado.

### 4.5 Subtópico numerado (e desdobramento `N.M`)
`jc=both` · `spacing exact 360, before 200, after 120` · `ind left=1701, hanging=0` ·
Arial 11 **negrito + sublinhado simples** (`w:u w:val="single"`), caixa alta.
Texto no formato `1 – TÍTULO DO TÓPICO` / `5.1 – TÍTULO DO DESDOBRAMENTO`. Numeração digitada, reiniciando
em 1 a cada tópico principal.

### 4.6 Corpo do texto
`jc=both` · `spacing exact 360, before 0, after 120` · `ind firstLine=1701` · Arial 11.

### 4.7 Citação (ementa, lei, trecho de documento)
`jc=both` · `spacing exact 240, before 100, after 160` · `ind left=2268, hanging=0` ·
Arial 10, **sem itálico** — a peça de referência desliga o itálico explicitamente
(`<w:i w:val="false"/><w:iCs w:val="false"/>`): o destaque da citação vem do corpo menor e do recuo de 4 cm,
não do itálico. Itálico fica reservado a expressão latina no corpo do texto (*ad argumentandum tantum*,
*verbis*), em Arial 11. Cada parágrafo da citação leva `before=100 after=160`.

### 4.8 Bloco de cálculo / enumeração de valores
`jc=left` · `spacing exact 240` · `ind left=2268, hanging=0` · Arial 10, sem itálico (igual à citação).
Espaçamento na sequência: primeira linha `before=100 after=40`; intermediárias `before=0 after=40`;
última `before=0 after=160`.

### 4.9 Alínea do corpo — `(a)`, `(b)`
`jc=both` · `spacing exact 360, before 0, after 120` · `ind left=1701, right=0, hanging=0` · Arial 11.
Nesses parágrafos (e nos do fecho) a referência traz também `<w:widowControl/><w:bidi w:val="0"/>` antes do
`spacing` — sem efeito visual (o estilo `Normal` já liga o controle de linhas e o texto já é LTR), mantido
para o arquivo gerado ficar idêntico ao de referência.

### 4.10 Alínea de requerimento — `a)`, `b)`
Igual à anterior, com `after=160`. Marcador (`a)`, `b)`) e o núcleo do pedido em negrito.

### 4.11 Fecho e assinatura
Três parágrafos `jc=both` · `spacing exact 360, before 0, after 160` · `ind left=0, right=0, firstLine=1701`:

```
Nesses Termos,
Pede Deferimento.
Campo Grande/MS, data de assinatura eletrônica.
```

Depois: **2 parágrafos vazios** (`after=200`), e a assinatura centralizada em negrito, Arial 11:
`Marcos Hideki Kamibayashi` (`jc=center`, `after=60`) e `OAB/MS 14.580` (`jc=center`, `after=200`).

## 5. Cabeçalho da página (`word/header1.xml`)

Tabela de **2 colunas sem borda**, largura `9071`, layout fixo, margens de célula zeradas:

- Coluna 1 (`2850` twips): logotipo dos Correios (`word/media/image1.png`), imagem inline de
  `1714500 × 361950` EMU = **4,76 × 1,01 cm**.
- Coluna 2 (`6220` twips), dois parágrafos centralizados, `spacing exact 240`:
  1. `EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS` — Arial Narrow 12 pt **negrito**.
  2. `Assessoria Jurídica MS/DEJUR/SEJUR` — Arial Narrow 12 pt, com borda inferior
     (`w:bottom single sz=6 space=2`) fazendo o traço sob o texto.

Depois da tabela, um parágrafo vazio (`spacing after=0`).

## 6. Rodapé da página (`word/footer1.xml`)

Dois parágrafos, ambos `spacing exact 200` (10 pt), Arial Narrow 7 pt negrito:

1. Linha de sublinhados (`_` repetido) centralizada, fazendo o filete sobre o rodapé.
2. `Avenida Calógeras nº 2309 – 2º andar – Centro – Campo Grande – MS – Fone 2109-1004.` +
   tabulação direita em `9071` + campo `PAGE` (número da página).

**Não existe nota de rodapé** (`w:footnoteReference` não aparece no documento de referência, e não há
`word/footnotes.xml`). "Rodapé" no padrão é este bloco de página. Referência a documento vai no corpo, entre
parênteses.

## 7. Ordem dos elementos no XML (não é opcional)

O schema OOXML impõe a ordem dos filhos. Fora de ordem, o Word acusa arquivo corrompido e "repara" o
documento, desmanchando a formatação. A ordem usada na peça de referência — e a que o gerador emite:

- `w:pPr` → `pStyle`, [`widowControl`, `bidi`], [`pBdr`], `spacing`, `ind`, `jc`, `rPr` (marca de parágrafo).
- `w:rPr` → `rFonts`, `b`, `bCs`, `i`, `iCs`, `sz`, `szCs`, `u`.

Atenção a dois pontos contraintuitivos: `jc` (alinhamento) vem **depois** de `spacing` e `ind`; e `u`
(sublinhado) vem **depois** de `sz`. No subtópico, a marca de parágrafo também carrega o sublinhado
(`<w:rPr><w:u w:val="single"/></w:rPr>` dentro do `w:pPr`). Todo run traz
`<w:rFonts w:eastAsia="Arial" w:cs="Arial"/>`, e o parágrafo vazio de espaçamento traz um run vazio
(`<w:r><w:rPr></w:rPr></w:r>`).

## 8. Como o `.docx` é montado

`modelos/_FORMATO_BASE.docx` traz `header1.xml`, `footer1.xml`, `styles.xml`, `media/image1.png` e o
`sectPr` exatos. O gerador
[`../scripts/gerar_minuta_docx.py`](../scripts/gerar_minuta_docx.py) copia **todas** as entradas do zip
base e regrava apenas `word/document.xml`, preservando o `sectPr` original. Assim cabeçalho, rodapé,
logotipo, estilos e página nunca se degradam de uma geração para a outra.

Conferência rápida de um arquivo gerado:

```bash
python - <<'PY'
import zipfile, re
d = zipfile.ZipFile('saida.docx').read('word/document.xml').decode()
print('parágrafos:', d.count('<w:p>') + d.count('<w:p '))
print('retângulos de tópico:', d.count('<w:pBdr>'))
print('entrelinha exata 18pt:', d.count('w:lineRule="exact" w:line="360"'))
print('notas de rodapé (deve ser 0):', d.count('footnoteReference'))
PY
```
