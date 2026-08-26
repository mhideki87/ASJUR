# Instruções de projeto — ASJUR (Claude Code)

Este arquivo vale para **todas as sessões do Claude Code** — local (CLI/desktop) e **cloud/web** —, porque
é lido do próprio repositório. Cada seção indica onde se aplica:

| Seção | Claude Code local | Claude Code cloud/web | Project do claude.ai |
|---|---|---|---|
| Conversão de PDF/DOC da parte → `.md` | sim | **não** (sem acesso a `D:\Claude\00 caso_atual` nem ao Python local) | não |
| Título da sessão com o nome do Reclamante | sim | sim | sem ferramenta de renomear — usar o fallback da seção |
| Padrões de saída (nome de arquivo + formatação de tópicos) | sim | sim | sim |

Para valer no cloud, qualquer alteração aqui precisa estar **commitada e enviada (push)** para a branch
usada na sessão cloud (por padrão, `main`): o cloud lê o repositório, não a máquina local.

## Conversão automática de documentos da parte para Markdown

**Objetivo:** nunca ler um PDF/DOC/DOCX diretamente (parsing inline é mais caro em tokens e menos confiável)
quando já existir — ou puder existir — um `.md` equivalente.

**Gatilho — qualquer um dos dois:**
1. O usuário informa o nome da parte adversa (Reclamante/Autor) em qualquer mensagem da sessão.
2. O próprio Claude identifica esse nome ao ler um documento do processo já anexado/aberto na sessão
   (capa do PJe, petição inicial, sentença etc.).

**Ação, assim que o nome for conhecido e antes de ler qualquer PDF/DOC/DOCX daquela parte:**

```bash
python scripts/converter_parte_para_md.py "<NOME DA PARTE>"
```

Isso converte todo PDF/DOC/DOCX encontrado em `D:\Claude\00 caso_atual\<pasta da parte>` (busca por nome
parcial, sem diferenciar maiúsculas/acentos) para um `.md` irmão, na mesma pasta. Reconverte só o que for
novo ou tiver mudado desde a última conversão (comparação de data de modificação) — rodar de novo é barato.
Depois de rodar, **leia os `.md` gerados, não os originais**.

**Depois de converter com sucesso, sobre os arquivos originais (PDF/DOC/DOCX):** Claude nunca exclui
arquivo definitivamente — nem sozinho, nem se o usuário pedir/autorizar, nem como passo automático desta
rotina. A única opção existente é **mover o original para a Lixeira do Windows** (reversível), rodando o
script com `--mover-para-lixeira`, e só quando o usuário pedir isso explicitamente naquela sessão — nunca
por padrão/silenciosamente ao final da conversão. Fora isso, os originais ficam onde estão; cabe ao usuário
decidir se e quando excluí-los de fato.

Tratamento de erro do script (não insista sozinho — reporte ao usuário):
- **Nenhuma pasta encontrada** ou **mais de uma pasta corresponde ao nome** → o script lista as opções
  existentes; peça ao usuário para confirmar o nome/pasta exata antes de prosseguir.
- **Falha ao converter um `.doc` antigo** (formato binário do Word 97-2003) → avise o usuário; a solução é
  salvar o arquivo como `.docx` ou `.pdf` e rodar o script de novo.
- Pré-requisito de ambiente: Python 3.12+ com `markitdown[pdf,docx]` instalado
  (`pip install -r scripts/requirements.txt`). Se o comando falhar por lib ausente, avise antes de tentar
  qualquer alternativa manual de leitura do PDF.

**Nunca:**
- Copiar `.md`/PDF/DOC com dado real de parte para dentro deste repositório Git (`D:\Claude\00 caso_atual`
  é local, fora do repo — ver regra permanente no [README.md](README.md)).
- Presumir o nome da pasta da parte sem confirmação quando o script indicar ambiguidade.

## Título da sessão — identificação do caso na aba lateral

**Objetivo:** permitir que o usuário localize a sessão na aba lateral do Claude Code só lendo o título.

**Gatilho:** assim que começar a analisar qualquer peça do processo (petição inicial, contestação, sentença,
acórdão, recurso, laudo etc.) **e** o nome do Reclamante/Autor já for conhecido — informado pelo usuário ou
identificado por mim na leitura do documento.

**Ação (antes de produzir a análise, não depois):** renomear a sessão com a ferramenta de renomeação do
ambiente — no Claude Code local e cloud/web é `mcp__ccd_session_mgmt__set_session_title`, com
`session_id: "self"` — usando o formato:

```
<NOME DO RECLAMANTE> — <o que estou fazendo>
```

Exemplos: `João da Silva — Análise de petição inicial`, `Maria Souza — Análise de sentença`,
`Carlos Pereira — Análise de acórdão`.

Regras:
- Renomear **sem pedir confirmação** — é comportamento padrão pedido pelo usuário.
- Se a sessão mudar de foco (ex.: passar da inicial para a sentença do mesmo caso), **atualizar o título**
  para refletir a peça em análise no momento.
- Se o processo tiver mais de um Reclamante, usar o primeiro nome + `e outros`.
- Se o nome do Reclamante ainda não for conhecido, não inventar: analisar normalmente e renomear no momento
  em que o nome aparecer.
- **Vale em qualquer ambiente**, inclusive nas sessões cloud/web. Se ali não existir ferramenta de
  renomeação (ex.: Project do claude.ai), o fallback é abrir a resposta com a linha
  `**<NOME DO RECLAMANTE> — <o que estou fazendo>**`, para o assunto ficar visível no histórico.
- Não pedir que o usuário renomeie manualmente: havendo ferramenta, usar; não havendo, usar o fallback.

## Padrões de saída — nome de arquivo e formatação de tópicos

Valem em **qualquer sessão** (local, cloud/web, Project) e **sem pedir confirmação**, para todo arquivo que eu
gerar e toda peça que eu minutar.

### Nome de arquivo

Padrão: `Tipo - Tema abreviado - Rito - NOME DA PARTE.odt` (regra completa e abreviações na seção 6 de
[base_conhecimento_juridico_ECT.md](base_conhecimento_juridico_ECT.md)).

- As palavras de cada campo são separadas por **espaço** — **nunca** por `_`.
- Os campos (tópicos) do nome são separados por **` - `** (hífen entre espaços).
- `Rito` é omitido quando não for relevante ou não estiver confirmado nos autos.
- Underscore só é aceitável em arquivo baixado do PJe ou recebido de terceiro; arquivo que eu gerar, nunca.
- Exemplos: `ED - Reducao de Jornada - NOME DA PARTE.odt` · `Cont - Inc Fun - NOME DA PARTE.odt`.

### Formatação dos tópicos da peça

- **Tópico principal**: parágrafo próprio, em **caixa alta, negrito, centralizado e dentro de retângulo**
  (borda simples nos quatro lados), sem recuo. Ex.: `DA TEMPESTIVIDADE`, `DO MÉRITO`, `DOS REQUERIMENTOS`.
- **Subtópico**: numerado (`1 – ...`), caixa alta, **negrito e sublinhado**, justificado, **sem** retângulo.
- Não usar numeração romana (`I –`, `II –`) nos tópicos principais: o padrão das peças é o retângulo.
- Esse padrão **não** aparece em `modelos/_FORMATO_BASE.docx` (o corpo dele é placeholder). Antes de gerar
  qualquer peça, abrir também um `.docx` de tema em `modelos/<área>/` para conferir o corpo — a formatação
  geral (cabeçalho, rodapé, fonte, assinatura) continua vindo de `_FORMATO_BASE.docx`.
