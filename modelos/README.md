# Modelos: estrutura + visual

## Formatação geral — `_FORMATO_BASE.docx`

Template visual **de todas as peças**, qualquer tipo ou tema: página, fonte, cabeçalho com logotipo, rodapé
com endereço/numeração, bloco de fecho + assinatura — e, desde 08/2026, o **catálogo completo dos sete papéis
de parágrafo**. Foi regerado a partir de uma peça real aprovada, mantendo cabeçalho, rodapé, estilos,
logotipo e configuração de página **byte-idênticos** ao original.

O corpo do arquivo não é mais um placeholder solto: cada papel de parágrafo aparece uma vez, com texto que
descreve a si mesmo. Isso existe por um motivo — enquanto o corpo era um placeholder, quem gerasse uma peça
a partir dele não tinha como saber que existiam retângulo, citação de 10 pt ou alínea, e acabava inventando
formatação.

| Papel | Onde se usa | Geometria |
|---|---|---|
| Tópico principal | grandes divisões: PRELIMINARMENTE, DO MÉRITO, DOS REQUERIMENTOS | retângulo de 0,75 pt, centralizado, negrito, **sem** sublinhado |
| Subtópico | `1 – TÍTULO` dentro de cada tópico | bloco de 3 cm, negrito **e sublinhado** |
| Corpo | parágrafo padrão | recuo de 1ª linha de 3 cm, justificado, Arial 11 |
| Citação em bloco | lei, súmula, ementa, trecho de decisão | bloco de 3 cm, **10 pt**, itálico, entrelinha menor |
| Alínea | rol de requerimentos | bloco de 3 cm, rótulo `a)` em negrito |
| Travessão | listas dentro do corpo | recuo 3,6 cm, pendente 0,6 cm |
| Endereçamento | juízo, autos, rótulos de polo | sem recuo, justificado |

Valores exatos em `.claude/skills/peca-ect/reference/catalogo_estilos.md`.

**Não recrie essa formatação a partir da descrição acima.** Gere a peça com
`.claude/skills/peca-ect/scripts/peca_fmt.py`, que é a fonte executável do padrão, e confira o resultado com
`scripts/conferir.py`. A tabela serve para você entender o padrão, não para reimplementá-lo.

Dois pontos do bloco de qualificação **mudam conforme o tipo de peça**:
- Endereçamento (Vara para 1º grau; TRT24 para recursos/contrarrazões) e rótulos de polo
  (Reclamante/Reclamada; Recorrente/Recorrido; Embargante/Embargada).
- `[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]` — o dispositivo que autoriza a peça (art. 847 CLT c/c 336 CPC
  para contestação; art. 895 CLT para recurso ordinário; art. 896 CLT para recurso de revista; art. 897-A,
  § 2º, CLT c/c art. 1.023, § 2º, CPC para contraminuta de embargos).

### Quando a peça real divergir do template

A peça real vence. Extraia o catálogo dela, atualize `peca_fmt.py`, regere o `_FORMATO_BASE.docx` com
`scripts/gerar_formato_base.py` e só então produza a peça nova — avisando o que mudou.

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
