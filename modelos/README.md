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

**Atenção — o que o placeholder do corpo não mostra:** os tópicos da peça são parágrafos em **retângulo**
(caixa alta, negrito, centralizado, borda simples nos quatro lados) e os subtópicos vêm numerados, em
negrito e sublinhado, sem retângulo. Isso **não** aparece em `_FORMATO_BASE.docx`, porque o corpo dele é
placeholder — conferir num `.docx` de tema (ex.: `trabalhista/contestacao__afastamentos.docx`) antes de
gerar a peça. Regra completa na seção 4 de `base_conhecimento_juridico_ECT.md`.

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
