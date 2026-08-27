# Especificação de formatação — padrão MS/DEJUR/SEJUR

Extraída de peça real aprovada pelo usuário. Unidades em **twips** (1 pt = 20 twips;
1 cm ≈ 567 twips). `w:sz` de fonte é em meios-pontos (`22` = 11 pt).

## Página e pacote

| Item | Valor |
|---|---|
| Papel | A4 — `w:w="11906" w:h="16838"` |
| Margens | esquerda `1701` · direita `1134` · superior `1701` · inferior `1134` |
| Cabeçalho / rodapé | `397` da borda |
| Fonte padrão | Arial, `w:sz="22"` (11 pt), `pt-BR` |
| Cabeçalho | `word/header1.xml` — logotipo (`word/media/image1.png`) + "EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS" + "Assessoria Jurídica MS/DEJUR/SEJUR" |
| Rodapé | `word/footer1.xml` — linha divisória + endereço + `PAGE` |

Tudo isso já vem pronto ao reaproveitar `modelos/_FORMATO_BASE.docx`: copie todas as entradas
do pacote ZIP e troque **apenas** `word/document.xml`.

## Tópico principal — RETÂNGULO

O elemento característico do padrão. Borda simples de `sz="6"` (0,75 pt) nos quatro lados,
`space="4"` de respiro interno, texto centralizado em negrito e caixa alta.

```xml
<w:pPr>
  <w:pStyle w:val="Normal"/>
  <w:pBdr>
    <w:top    w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:left   w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/>
    <w:right  w:val="single" w:sz="6" w:space="4" w:color="000000"/>
  </w:pBdr>
  <w:spacing w:lineRule="exact" w:line="240" w:before="320" w:after="260"/>
  <w:ind w:left="0" w:right="0" w:hanging="0"/>
  <w:jc w:val="center"/>
</w:pPr>
<w:r>
  <w:rPr><w:rFonts w:eastAsia="Arial" w:cs="Arial"/><w:b/><w:bCs/>
         <w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  <w:t>DO MÉRITO</w:t>
</w:r>
```

Exemplos reais de tópicos: `DA EQUIPARAÇÃO À FAZENDA PÚBLICA`, `RESUMO DA VESTIBULAR`,
`DO MÉRITO`, `DO PREQUESTIONAMENTO`, `DOS REQUERIMENTOS`.

## Demais parágrafos

Todos usam `<w:pStyle w:val="Normal"/>` e `<w:jc w:val="both"/>`, variando recuo e espaçamento.

| Tipo | `spacing` | `ind` | Run |
|---|---|---|---|
| Parágrafo de texto | `line=360 before=0 after=160` | `firstLine=1701` | Arial 11 |
| Subtópico | `line=360 before=200 after=120` | `left=1701 hanging=0` | negrito + `<w:u w:val="single"/>` |
| Citação / ementa | `line=260 before=0 after=160` | `left=1701 hanging=0` | itálico, `sz=20` |
| Alínea / requerimento | `line=360 before=0 after=160` | `left=1701 hanging=0` | Arial 11 (rótulo `a)` em negrito) |
| Marcador (travessão) | `line=360 before=0 after=160` | `left=2041 hanging=340` | Arial 11, texto iniciado por `– ` |
| Endereçamento / epígrafe | `line=360 before=0 after=160` | `left=0 hanging=0` | Arial 11 |
| Linha em branco | `before=0 after=200` | — | — |

## Bloco de fecho

Vem pronto do modelo, centralizado:

```
Nesses Termos,
Pede Deferimento.
Campo Grande/MS, data de assinatura eletrônica.

Marcos Hideki Kamibayashi
OAB/MS 14.580
```

## Bloco de qualificação — o que muda por tipo de peça

`modelos/_FORMATO_BASE.docx` traz placeholders. Dois dependem do tipo de peça:

| Peça | Endereçamento | `[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]` |
|---|---|---|
| Contestação | Vara do Trabalho | arts. 847 da CLT c/c 336 do CPC |
| Quesitos de perícia | Vara do Trabalho | art. 465, § 1º, II e III, do CPC c/c art. 769 da CLT |
| Recurso ordinário | TRT da 24ª Região | art. 895 da CLT |
| Contrarrazões | TRT da 24ª Região | art. 900 da CLT |
| Recurso de revista | TRT da 24ª Região | art. 896 da CLT |
| Embargos de declaração | juízo prolator | art. 897-A da CLT c/c art. 1.022 do CPC |

Os rótulos de polo também mudam: `RECLAMANTE`/`RECLAMADA` em 1º grau;
`RECORRENTE`/`RECORRIDO` em recurso; `EMBARGANTE`/`EMBARGADO` em embargos.

## Armadilha conhecida do ambiente cloud

O LibreOffice do contêiner cloud costuma falhar ao converter estes `.docx` para PDF
("source file could not be loaded") — **inclusive o próprio `_FORMATO_BASE.docx`**. É
limitação do ambiente, não defeito do arquivo. Valide a estrutura com
`scripts/conferir_peca.py` (usa `python-docx`) em vez de tentar renderizar.
