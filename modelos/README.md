# Modelos: estrutura + visual

## Formatação geral — `_FORMATO_BASE.docx`

Este arquivo é o template visual **de todas as peças**, qualquer tipo ou tema: fonte, margens, cabeçalho com
logotipo, rodapé com endereço/numeração, e o bloco de fecho + assinatura (Marcos Hideki Kamibayashi, OAB/MS
14.580). Foi extraído de uma peça real aprovada e anonimizada, mantendo cabeçalho/rodapé/estilos **byte-
idênticos** ao original — só o corpo foi trocado por um placeholder, porque a estrutura do corpo varia por
tipo de peça (contestação ≠ recurso ≠ quesitos) e por tema.

Ao gerar qualquer peça nova, comece por este arquivo. Dois pontos do bloco de qualificação **mudam conforme o
tipo de peça** e precisam ser ajustados a cada uso:
- Endereçamento (Vara do Trabalho para peças de 1º grau; TRT24 para recursos/contrarrazões e mandado de
  segurança) e os rótulos de polo (Reclamante/Reclamada; Recorrente/Recorrido; Impetrante/Autoridade
  Coatora/Litisconsorte, etc.).
- `[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]` — o dispositivo que autoriza a peça (ex.: art. 847 CLT c/c 336
  CPC para contestação; art. 895 CLT para recurso ordinário; art. 896 CLT para recurso de revista; art. 897-A
  CLT para embargos de declaração; art. 5º, LXIX, da CF e Lei 12.016/2009 para mandado de segurança).

### Padrão de parágrafos (obrigatório em qualquer peça)

O corpo do `_FORMATO_BASE.docx` traz **um exemplo de cada tipo de parágrafo**. Use exatamente esses formatos —
não invente variações. Página A4, margens 3,0 cm (esq.) × 2,0 cm (dir.) × 3,0 cm (sup.) × 2,0 cm (inf.),
Arial em todo o documento.

| Tipo | Uso | Formato |
|---|---|---|
| Endereçamento / rótulos | destinatário, nº dos autos, partes | Arial 11 **negrito**, justificado, sem recuo, entrelinha exata 18 pt |
| Tarja de urgência | `URGENTE…`, `SEGREDO DE JUSTIÇA` | igual ao anterior, **em vermelho** (`FF0000`) — só quando houver |
| Título da peça | `MANDADO DE SEGURANÇA…`, `CONTESTAÇÃO` | Arial 11 negrito, **centralizado**, sem recuo |
| **Título de seção** | seções principais | Arial 11 negrito, **CAIXA ALTA, centralizado, dentro de quadro** (borda simples 0,5 pt nos 4 lados, espaçamento 4 pt), entrelinha simples, 16 pt antes / 13 pt depois — **sem numeração romana** |
| **Subtítulo de item** | subdivisões da seção | Arial 11 negrito **e sublinhado**, CAIXA ALTA, numeração arábica (`1.`, `2.`…), **bloco recuado 3 cm à esquerda**, justificado |
| Texto corrido | regra geral | Arial 11, justificado, **recuo de primeira linha de 3 cm**, entrelinha exata 18 pt, 8 pt depois |
| Enumeração | `(i)…`, `a)…` quando destacados do texto | Arial 11, **bloco recuado 3 cm à esquerda**, sem recuo de primeira linha, justificado |
| Citação | lei, súmula, jurisprudência, doutrina | Arial **10, itálico**, bloco recuado 3 cm à esquerda, justificado, entrelinha simples |
| Fecho | `Nesses Termos,` / `Pede Deferimento.` / `Campo Grande/MS, data de assinatura eletrônica.` | mesmo formato do texto corrido |
| Assinatura | nome + OAB | Arial 11 negrito, centralizado |

Regras de estilística que acompanham o padrão:
- Destaques no texto em **negrito**; expressões latinas (*data venia*, *fumus boni iuris*) e títulos de obra em
  itálico. Sublinhado é reservado aos subtítulos de item.
- Cada título de seção é **um único parágrafo** — não quebrar o título em dois parágrafos, senão o quadro se
  parte em duas caixas.
- Marcações `[REVISAR: ...]` ficam no corpo do texto durante a minuta e **devem sair antes do protocolo**;
  vermelho é usado só na tarja de urgência.

### Receita OOXML (para gerar o `.docx` sem abrir o Word)

Ao montar a peça programaticamente, reaproveite **todas** as partes do pacote `_FORMATO_BASE.docx`
(`styles.xml`, `header*.xml`, `footer*.xml`, `theme/`, `settings.xml`, `fontTable.xml`, `media/`) e substitua
apenas o conteúdo de `<w:body>`, mantendo o `<w:sectPr>` final. Os `w:pPr` de cada tipo:

```
texto corrido : <w:spacing w:lineRule="exact" w:line="360" w:after="160"/><w:ind w:firstLine="1701"/><w:jc w:val="both"/>
título seção  : <w:pBdr>(single sz=6 space=4 nos 4 lados)</w:pBdr>
                <w:spacing w:lineRule="exact" w:line="240" w:before="320" w:after="260"/><w:ind w:start="0"/><w:jc w:val="center"/>
subtítulo     : <w:spacing w:lineRule="exact" w:line="360" w:after="160"/><w:ind w:start="1701" w:hanging="0"/><w:jc w:val="both"/>  + run <w:b/><w:u w:val="single"/>
enumeração    : idem subtítulo, run sem negrito/sublinhado
citação       : <w:spacing w:lineRule="exact" w:line="240" w:after="160"/><w:ind w:start="1701" w:hanging="0"/><w:jc w:val="both"/>  + run <w:i/> sz 20
cabeçalho/rótulo: <w:spacing w:lineRule="exact" w:line="360" w:after="160"/><w:ind w:hanging="0"/><w:jc w:val="both"/>  + run <w:b/>
centralizado  : <w:spacing w:after="60"/><w:jc w:val="center"/>  + run <w:b/>
linha em branco: <w:spacing w:after="200"/>
```

Runs: `<w:rFonts w:eastAsia="Arial" w:cs="Arial"/>` + `<w:sz w:val="22"/>` (11 pt) — ou `20` (10 pt) nas
citações. Tarja de urgência acrescenta `<w:color w:val="FF0000"/>`.

Um modelo específico de tipo de peça + tema (ver abaixo) só precisa de `.docx` próprio quando o **corpo**
tiver algo estruturalmente distinto que valha preservar (uma tabela, uma numeração especial de quesitos) —
fora isso, a formatação já vem de `_FORMATO_BASE.docx` e o `.md` do tema basta para descrever a estrutura.

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

> **Precedência:** em qualquer divergência de formatação entre um `.docx` de tema e o `_FORMATO_BASE.docx`,
> vale o `_FORMATO_BASE.docx`. Os `.docx` de tema salvos antes da revisão do padrão de parágrafos servem
> apenas como referência de **estrutura de corpo**; a aparência (títulos em quadro, subtítulos sublinhados,
> recuos, citações) sai sempre do formato base.

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
- Um modelo só é criado ou atualizado depois de **aprovação explícita do usuário**.
- Use `modelos/_TEMPLATE.md` como ponto de partida do arquivo de estrutura.

## Como isso é usado no dia a dia

Ver seção 6 de `playbook_prompts_ECT.md`. Resumo: antes de anexar peça antiga, o Claude verifica se já
existe o par `.md` + `.docx` para aquele tipo de peça + tema; se existir, usa direto. Se não existir (ou
estiver desatualizado), pede o anexo, minuta, e ao final propõe consolidar o par de arquivos aqui.
