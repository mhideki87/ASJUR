---
name: peca-ect
description: Gerar qualquer peça processual da Assessoria Jurídica ECT/MS em .docx com a formatação da casa — retângulo nos tópicos, subtópicos numerados, citações em bloco de 10 pt, alíneas dos requerimentos, cabeçalho com logotipo e bloco de assinatura. Use SEMPRE que for produzir contestação, recurso ordinário, recurso de revista, contrarrazões, contraminuta, embargos de declaração, manifestação ou quesitos de perícia para a ECT. Também use ao consolidar um novo modelo em modelos/ ou ao atualizar _FORMATO_BASE.docx.
---

# Peças da Assessoria Jurídica ECT/MS

## Regra que não se negocia

**Nunca descreva a formatação: execute-a.** A formatação vive em
`scripts/peca_fmt.py` e em `modelos/_FORMATO_BASE.docx`. Toda peça é montada por
esse módulo, e nunca recriada a partir de uma descrição em texto, de memória ou
de inspeção visual de um PDF.

Se você se pegar escrevendo XML de parágrafo à mão, ou escolhendo um recuo "que
parece certo", pare: o valor correto já está no módulo.

## Como produzir uma peça

```python
import sys; sys.path.insert(0, ".claude/skills/peca-ect/scripts")
from peca_fmt import hdr, p, box, sub, cit, alinea, travessao, vazio, quebra, fecho, montar

X = []
X.append(hdr([("EXCELENTÍSSIMO(A) ... VARA DO TRABALHO DE CAMPO GRANDE/MS.", "b")]))
X.append(p([("EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS", "b"), (", ...", "")]))
X.append(box("DO MÉRITO"))
X.append(sub("1 – DA PRESCRIÇÃO TOTAL"))
X.append(p("texto do parágrafo..."))
X.append(cit("Art. 11. ..."))
X.append(box("DOS REQUERIMENTOS"))
X.append(alinea("a)", "primeiro requerimento;"))
X.append(fecho())
montar(X, "Cont_-_Tema_-_NOME_DA_PARTE.docx")
```

Cada trecho é `(texto, estilo)`, com estilo `""`, `"b"` negrito, `"i"` itálico,
`"u"` sublinhado — combináveis (`"bu"`). Passar uma string simples equivale a
`[(texto, "")]`.

## Os sete papéis de parágrafo

| Função | Papel na peça | Geometria |
|---|---|---|
| `box()` | tópico principal | retângulo 0,75 pt, centralizado, **negrito, sem sublinhado** |
| `sub()` | subtópico `1 – TÍTULO` | bloco de 3 cm, **negrito + sublinhado** |
| `p()` | corpo | recuo de 1ª linha de 3 cm, justificado, 11 pt |
| `cit()` | citação em bloco | bloco de 3 cm, **10 pt, itálico**, entrelinha menor |
| `alinea()` | alínea dos requerimentos | bloco de 3 cm, rótulo `a)` em negrito |
| `travessao()` | item de lista | recuo 3,6 cm, pendente 0,6 cm |
| `hdr()` | endereçamento e qualificação | sem recuo, justificado |

`box()` só nas grandes divisões (PRELIMINARMENTE, DO MÉRITO, DO
PREQUESTIONAMENTO, DOS REQUERIMENTOS). Tudo o mais é `sub()`, numerado em
sequência dentro de cada tópico. Valores exatos em `reference/catalogo_estilos.md`.

## Verificação obrigatória antes de entregar

Rode `scripts/conferir.py <arquivo.docx>`. Ele confere que cabeçalho, rodapé,
estilos e logotipo continuam byte-idênticos ao `_FORMATO_BASE.docx`, lista os
papéis usados e acusa espaços duplos e vírgulas órfãs. Não entregue peça que
não passe.

Como o LibreOffice pode não estar disponível no ambiente, a conferência é feita
lendo o próprio .docx — não confie em conversão para PDF.

## Nome do arquivo

`Tipo - Tema abreviado - Rito - NOME DA PARTE.docx` — `Cont` contestação, `RO`
recurso ordinário, `RR` recurso de revista, `Manifest` manifestação.

## Quando a peça de referência divergir do template

Se o usuário anexar uma peça real cuja formatação não bate com
`_FORMATO_BASE.docx`, **a peça real vence** — ela é a fonte da verdade. Nesse
caso: extraia o catálogo dela, atualize `peca_fmt.py` e regere o
`_FORMATO_BASE.docx` com `scripts/gerar_formato_base.py`, e só então produza a
peça. Avise o usuário do que mudou.

## Conteúdo jurídico

Formatação é o que esta skill resolve; o conteúdo segue
`base_conhecimento_juridico_ECT.md` e `playbook_prompts_ECT.md`. Em especial:
nunca inventar jurisprudência, dispositivo, cláusula de ACT, data ou Id — marcar
`[REVISAR: ...]` em negrito no corpo e listar as pendências ao final da resposta.
