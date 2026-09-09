# Modelos: estrutura + visual

## Formatação geral — `_FORMATO_BASE.docx`

Este arquivo é o template visual **de todas as peças**, qualquer tipo ou tema: fonte, margens, cabeçalho com
logotipo, rodapé com endereço/numeração, e o bloco de fecho + assinatura (Marcos Hideki Kamibayashi, OAB/MS
14.580). Foi extraído de uma peça real aprovada e anonimizada, mantendo cabeçalho/rodapé/estilos **byte-
idênticos** ao original — só o corpo foi trocado por um placeholder, porque a estrutura do corpo varia por
tipo de peça (contestação ≠ recurso ≠ quesitos) e por tema.

Ao gerar qualquer peça nova, comece por este arquivo. Dois pontos do bloco de qualificação **mudam conforme o
tipo de peça** e precisam ser ajustados a cada uso:
- Endereçamento (Vara do Trabalho para peças de 1º grau; TRT24 para recursos/contrarrazões) e os rótulos de
  polo (Reclamante/Reclamada; Recorrente/Recorrido; Embargante/Embargado, etc.).
- `[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]` — o dispositivo que autoriza a peça (ex.: art. 847 CLT c/c 336
  CPC para contestação; art. 895 CLT para recurso ordinário; art. 896 CLT para recurso de revista).

Um modelo específico de tipo de peça + tema (ver abaixo) só precisa de `.docx` próprio quando o **corpo**
tiver algo estruturalmente distinto que valha preservar (uma tabela, uma numeração especial de quesitos) —
fora isso, a formatação já vem de `_FORMATO_BASE.docx` e o `.md` do tema basta para descrever a estrutura.

## Padrão formal, em texto

O `.docx` acima é a fonte da verdade — isto aqui é só a descrição, para conferência.

**Trabalhista** (validado, uso real): formato **.odt**, convertido para .docx quando necessário; fonte
**Arial 11**, entrelinha **1,5**, parágrafos justificados com recuo de primeira linha; margens esquerda
2 cm / direita ~1,25 cm; cabeçalho com logotipo dos Correios + "Assessoria Jurídica"; rodapé com endereço
e numeração; citações de jurisprudência em bloco recuado (~3 cm); fecho "N. Termos / P. Deferimento. /
Campo Grande/MS, data de assinatura eletrônica." + bloco de assinatura centralizado com nome e OAB.
Estrutura usual das razões: síntese → preliminares/prejudiciais → mérito → *ad cautelam* → requerimentos
com **prequestionamento**.

**Cível:** formato **.txt/.odt**; endereçamento a Juizado Especial Federal ou Vara Federal; mesmo fecho.
`[REVISAR: confirmar se cabeçalho, fonte, espaçamento e demais regras da trabalhista também valem aqui,
ou se cível tem modelo próprio]`

### Propriedades exatas dos parágrafos (trabalhista)

Extraídas do `word/document.xml` de peça real aprovada. Ao gerar `.docx` por script, usar estes valores —
descrever "entrelinha 1,5" em prosa não basta, e reconstruir de memória erra.

| Elemento | Propriedades |
|---|---|
| Corpo | `jc=both` · `lineRule="exact" line=360` · `before=0 after=120` · `ind firstLine=1701` · `sz=22` |
| Título de seção | **caixa com borda** (`pBdr` `single sz=6 space=4`) · `jc=center` · `exact 240` · `before=320 after=260` · `ind left=0` · negrito |
| Subtítulo numerado | `jc=both` · `exact 360` · `before=200 after=120` · `ind left=1701` · **negrito + sublinhado** |
| Sub-subtítulo | igual ao subtítulo, `before=160`, só negrito |
| Item recuado / requerimentos | `jc=both` · `exact 360` · `before=0 after=160` · `ind left=1701` · negrito |
| Citação | `jc=both` · `exact 240` · `before=100 after=160` · `ind left=2268` · **`sz=20` (10pt)** |

Cuidados que já custaram retrabalho:

- **`lineRule` é `exact`, não `auto`.** É o padrão real da casa; não "corrigir" para `auto`.
- Ordem exigida pelo schema em `<w:pPr>`: `pStyle` → `keepNext` → `widowControl` → `spacing` → `ind` → `jc`.
- Gerando a partir de `_FORMATO_BASE.docx`, substituir **só** o `word/document.xml`; ao final, conferir que
  os demais 12 componentes seguem byte-idênticos ao template.

### Conferência obrigatória antes de entregar

Peça em `.docx` **não se entrega sem renderizar e olhar** — validação por texto não pega erro de
formatação:

```bash
python <skill docx>/scripts/office/validate.py peca.docx --original modelos/_FORMATO_BASE.docx
python <skill docx>/scripts/office/soffice.py --headless --convert-to pdf --outdir out/ peca.docx
pdftoppm -jpeg -r 100 out/peca.pdf pg     # e então ler as imagens
```

Se o LibreOffice recusar **qualquer** arquivo com "source file could not be loaded", falta o módulo Writer
(`libswlo.so`): instalar `libreoffice-writer` — não é defeito do documento.

## Modelos por tipo de peça + tema

Cada peça-modelo consolidada aqui tem **dois arquivos de mesmo nome**, lado a lado:

```
modelos/<area>/<tipo_peca>__<tema>.md      → estrutura, teses, texto reaproveitável (o "o quê")
modelos/<area>/<tipo_peca>__<tema>.docx    → formatação real: fonte, margens, cabeçalho com
                                              logotipo, rodapé, bloco de assinatura (o "como fica")
```

O `.md` descreve em prosa para consulta rápida; o `.docx` é o arquivo literal que deve ser aberto e usado
como base ao gerar a peça final — **não tente recriar a formatação a partir da descrição em texto**, use o
arquivo binário como modelo.

## Por que isso existe

O objetivo é que, depois que um tipo de peça + tema já tiver um modelo salvo aqui, você **não precise mais
anexar** a peça antiga de novo — nem para saber a tese, nem para saber a formatação.

## Convenção de nomes

- `<area>` = `trabalhista` ou `civel`.
- `<tipo_peca>` = mesmo nome/abreviação da seção 6 de `playbook_prompts_ECT.md`.
- `<tema>` = mesmo tema da base de teses correspondente.

Exemplos: `modelos/trabalhista/contestacao__incorporacao_funcao.md` +
`modelos/trabalhista/contestacao__incorporacao_funcao.docx`.

## Como o `.docx` é criado (só a partir de um arquivo real seu, aprovado por você)

1. Você anexa uma peça sua real (um caso concreto, com nome de cliente/processo).
2. O Claude produz uma **cópia anonimizada**, preservando integralmente fonte, espaçamento, margens,
   cabeçalho/logotipo, rodapé, numeração de página e bloco de assinatura — só o conteúdo variável
   (nome da parte, nº do processo, datas, valores, fatos do caso) é substituído por placeholders
   (`[NOME DO RECLAMANTE]`, `[Nº PROCESSO]`, `[DATA]` etc.).
3. Você confere o resultado (inclusive que nenhum dado real ficou para trás em texto oculto,
   metadado do arquivo, ou propriedades do documento — nome de autor original, revisões, comentários).
4. Só depois de aprovado, o `.docx` anonimizado entra no repositório.

**Nunca** commitar um `.docx` com dado real de cliente — nem no corpo, nem nos metadados do arquivo.

## Regra de conteúdo (vale para `.md` e `.docx`)

- Nenhum nome de cliente, número de processo, CPF, ou dado que identifique uma parte real.
- O `.md` de estrutura é criado/atualizado e commitado pela skill `atualizar-base-conhecimento` na branch
  da sessão. O **`.docx`** só entra depois de **aprovação explícita do usuário** — ver o fluxo de
  anonimização acima.
- Use `modelos/_TEMPLATE.md` como ponto de partida do arquivo de estrutura.

## Como isso é usado no dia a dia

Ver seção 6 de `playbook_prompts_ECT.md`. Resumo: antes de anexar peça antiga, o Claude verifica se já
existe o par `.md` + `.docx` para aquele tipo de peça + tema; se existir, usa direto. Se não existir (ou
estiver desatualizado), pede o anexo, minuta, e ao final propõe consolidar o par de arquivos aqui.
