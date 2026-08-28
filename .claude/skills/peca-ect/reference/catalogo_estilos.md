# Catálogo de estilos — peças ECT/MS

Extraído de peça real aprovada (contestação, 08/2026). Valores em twips
(1 cm = 567 twips; 3 cm = 1701) e meio-pontos (`sz="22"` = 11 pt).

## Página e fontes

- A4 (11906 × 16838), margens: esquerda 1701, direita 1134, superior 1701, inferior 1134
- Cabeçalho a 397, rodapé a 397
- Fonte padrão Arial 11 pt; cabeçalho e rodapé em Arial Narrow
- Entrelinha exata de 360 (1,5) no corpo

## Parágrafos

| Papel | `w:ind` | `w:spacing` | `w:jc` | Runs |
|---|---|---|---|---|
| endereçamento | left 0, hanging 0 | line 360, after 160 | both | negrito |
| corpo | left 0, firstLine 1701 | line 360, after 160 | both | normal |
| tópico (retângulo) | left 0, hanging 0 | line 240, before 320, after 260 | center | negrito |
| subtópico | left 1701, hanging 0 | line 360, before 200, after 120 | both | negrito + sublinhado |
| citação | left 1701, hanging 0 | line 260, after 160 | both | itálico, `sz=20` |
| alínea | left 1701, hanging 0 | line 360, after 160 | both | rótulo em negrito |
| travessão | left 2041, hanging 340 | line 360, after 160 | both | normal |
| assinatura | — | after 60 / 200 | center | negrito |

## Retângulo do tópico principal

```xml
<w:pBdr>
  <w:top    w:val="single" w:sz="6" w:space="4" w:color="000000"/>
  <w:left   w:val="single" w:sz="6" w:space="4" w:color="000000"/>
  <w:bottom w:val="single" w:sz="6" w:space="4" w:color="000000"/>
  <w:right  w:val="single" w:sz="6" w:space="4" w:color="000000"/>
</w:pBdr>
```

`w:sz="6"` = 0,75 pt (oitavos de ponto). `w:space="4"` = 4 pt de respiro interno.

## Armadilhas já observadas

- O sublinhado é do **subtópico**, não do retângulo. Inverter os dois é o erro
  mais fácil de cometer.
- Citação usa `sz=20` (10 pt) **e** itálico **e** entrelinha 260 — os três juntos.
- Subtópico e alínea usam `w:left="1701"`, e **não** `w:firstLine="1701"`: a
  diferença só aparece quando o texto quebra para a segunda linha.
- Peças antigas em .odt usam Arial Narrow no corpo. Está defasado: o corpo atual
  é Arial.
