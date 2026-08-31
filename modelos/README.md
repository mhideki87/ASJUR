# Modelos: estrutura + visual

## Formatação geral — `_FORMATO_BASE.docx`

Este arquivo é o template visual **de todas as peças**, qualquer tipo ou tema: fonte, margens, cabeçalho com
logotipo, rodapé com endereço/numeração, e o bloco de fecho + assinatura (Marcos Hideki Kamibayashi, OAB/MS
14.580). Foi extraído de uma peça real aprovada e anonimizada, mantendo cabeçalho/rodapé/estilos **byte-
idênticos** ao original — só o corpo foi trocado por um placeholder, porque a estrutura do corpo varia por
tipo de peça (contestação ≠ recurso ≠ quesitos) e por tema.

Ao gerar qualquer peça nova, comece por este arquivo — o caminho normal é a skill **`formatar-minuta`**, que
clona este `.docx` e regrava só o corpo:

```bash
python .claude/skills/formatar-minuta/scripts/gerar_minuta_docx.py <minuta.md> <saida.docx>
```

Dois pontos do bloco de qualificação **mudam conforme o
tipo de peça** e precisam ser ajustados a cada uso:
- Endereçamento (Vara do Trabalho para peças de 1º grau; TRT24 para recursos/contrarrazões) e os rótulos de
  polo (Reclamante/Reclamada; Recorrente/Recorrido; Embargante/Embargado, etc.).
- `[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]` — o dispositivo que autoriza a peça (ex.: art. 847 CLT c/c 336
  CPC para contestação; art. 895 CLT para recurso ordinário; art. 896 CLT para recurso de revista).

Um modelo específico de tipo de peça + tema (ver abaixo) só precisa de `.docx` próprio quando o **corpo**
tiver algo estruturalmente distinto que valha preservar (uma tabela, uma numeração especial de quesitos) —
fora isso, a formatação já vem de `_FORMATO_BASE.docx` e o `.md` do tema basta para descrever a estrutura.

## Padrão formal — onde está a especificação

A especificação da formatação **não fica mais aqui**: está na skill `formatar-minuta`
([SKILL.md](../.claude/skills/formatar-minuta/SKILL.md) +
[especificação com as medidas](../.claude/skills/formatar-minuta/referencia/especificacao_formatacao.md)),
que é a fonte única para qualquer tipo de peça, trabalhista ou cível. Resumo do que vale:

- Arial 11 no corpo; Arial 10 nas citações e blocos de cálculo (recuo de 4 cm).
- Entrelinha **exata de 18 pt** (não é "1,5 linha" múltipla), espaço de 6 pt depois do parágrafo.
- Margens **3 cm** esquerda e superior, **2 cm** direita e inferior; A4.
- Recuo de primeira linha de 3 cm no corpo; alíneas recuadas 3 cm sem recuo de primeira linha.
- Tópico principal: caixa alta, negrito, centralizado, **dentro de retângulo**.
- Subtópicos numerados à mão (`1 – `, `5.1 – `), negrito + sublinhado, caixa alta, recuo de 3 cm;
  a numeração reinicia em cada tópico principal.
- Cabeçalho com logotipo dos Correios; rodapé com endereço e numeração de página. **Sem nota de rodapé.**
- Fecho "Nesses Termos, / Pede Deferimento. / Campo Grande/MS, data de assinatura eletrônica." + assinatura
  centralizada (Marcos Hideki Kamibayashi — OAB/MS 14.580).

Entrega em **.docx** gerado a partir de `_FORMATO_BASE.docx` — pelo script da skill, ou escrevendo dentro do
próprio arquivo base. Se o usuário precisar de `.odt`, salve o `.docx` como `.odt` no LibreOffice; não monte
a peça em documento em branco.

`[REVISAR: confirmar se a área cível usa este mesmo padrão visual e a mesma assinatura — ver LACUNAS.md]`

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
