# Instruções de projeto — ASJUR (Claude Code)

Este arquivo vale para **todas as sessões do Claude Code** — local (CLI/desktop) e **cloud/web** —, porque
é lido do próprio repositório. Cada seção indica onde se aplica:

| Seção | Claude Code local | Claude Code cloud/web | Project do claude.ai |
|---|---|---|---|
| Consulta à base de conhecimento (índice → fichas) | sim | sim | sim |
| Consolidação da base ao final da tarefa (skill `atualizar-base-conhecimento`) | sim | sim | sem skills nem escrita de arquivo — usar a seção 6.2 do playbook |
| Nome do arquivo da minuta (skill `nomear-minuta`) | sim | sim | sem skills — usar o padrão da seção 5.1 do playbook |
| Conversão de PDF/DOC da parte → `.md` | sim | **não** (sem acesso a `D:\Claude\00 caso_atual` nem ao Python local) | não |
| Título da sessão com o nome do Reclamante | sim | sim | sem ferramenta de renomear — usar o fallback da seção |

Para valer no cloud, qualquer alteração aqui precisa estar **commitada e enviada (push)** para a branch
usada na sessão cloud (por padrão, `main`): o cloud lê o repositório, não a máquina local.

## Consulta à base de conhecimento — ler o índice, não a base inteira

**Objetivo:** não gastar contexto lendo teses que não têm nada a ver com o processo da sessão.

A base é fatiada por tema em `teses/<área>/<tema>.md`, e o roteamento está em `INDICE.md`.

**Protocolo obrigatório, em toda sessão que envolva analisar peça ou minutar:**

1. Ler `CONTEXTO.md` por inteiro (é curto: perfil e regras inegociáveis).
2. Ler `INDICE.md` — só o protocolo do topo e a tabela de roteamento.
3. Ler os documentos do processo e **listar os pedidos**.
4. Para cada pedido, casar com um `gatilho` da tabela e abrir **somente** a ficha indicada. Abrir também as
   fichas da seção "Sempre aplicável" do índice (prerrogativas processuais; prescrição, na trabalhista).
5. Só então abrir o modelo estrutural (`modelos/<área>/…`) e a seção correspondente do
   `playbook_prompts_ECT.md`.

Regras:
- **Nunca** ler `teses/` por inteiro, nem abrir ficha "por precaução" — cada ficha aberta custa contexto.
- Nenhum gatilho bateu → dizer isso explicitamente e tratar como **tema novo**: analisar a partir dos
  autos, sem forçar o encaixe numa ficha existente, e ao final propor a criação de ficha nova a partir de
  `teses/_TEMPLATE_TESE.md`.
- Ficha com `status: rascunho` é **candidata a tese**, não tese confirmada — validar contra o processo em
  mãos e nunca citar como jurisprudência pronta.
- Depois de criar ou alterar qualquer ficha, rodar `python scripts/atualizar_indice.py` (regenera a tabela
  do `INDICE.md` e valida os metadados). Antes de commitar, conferir com
  `python scripts/atualizar_indice.py --check`. Esse script é só stdlib — roda em qualquer ambiente com
  Python 3, inclusive no cloud/web.
- Ficha nova ou alterada só entra no repositório depois de **aprovação explícita do usuário** (protocolo da
  seção 6.2 de `playbook_prompts_ECT.md`).

## Consolidação da base ao final da tarefa

**Objetivo:** o que a sessão descobriu não pode morrer com a sessão.

**Gatilho:** ao terminar a tarefa — peça analisada ou minutada, ficha/modelo criado ou alterado — e antes de
encerrar a resposta final.

**Ação:** invocar a skill **`atualizar-base-conhecimento`** (`.claude/skills/atualizar-base-conhecimento/`).
Ela levanta os achados da sessão, grava cada um no arquivo certo (`teses/<área>/`, `modelos/`, `CONTEXTO.md`,
playbook), regenera o `INDICE.md` e apresenta o diff.

Regras:
- Rodar **depois** de entregar a peça/resposta, nunca no meio do trabalho.
- Se nada de novo apareceu, dizer isso em uma linha e encerrar — não inventar achado para preencher.
- A skill **commita e faz push sozinha** na branch `claude/*` da sessão, depois de conferir branch, escopo
  do diff e ausência de dado identificável. A revisão do usuário é no diff do commit, não antes dele.
  Única exceção: `.docx` anonimizado, que espera aprovação (conferir texto oculto e metadados é
  verificação humana, e o repositório é público).

## Nome do arquivo da minuta entregue

**Objetivo:** o arquivo que chega ao usuário já vem com o nome que ele usaria — sem `_`, legível na pasta do
caso.

**Gatilho:** gerar, salvar, anexar, renomear ou citar o nome de qualquer arquivo de peça (contestação,
contrarrazões, RO, RR, quesitos, manifestação, embargos, impugnação, petição de juntada).

**Ação:** invocar a skill **`nomear-minuta`** (`.claude/skills/nomear-minuta/`) e nomear no padrão:

```
Tipo - Tema abreviado - NOME DA PARTE.odt
```

Espaço simples no lugar de `_`; tópicos separados por ` - `; nome da parte por último, em caixa alta.
Exemplo de formato: `RO - Resp Subs - NOME DA PARTE.odt`.

Regras:
- Vale para o nome escrito **na resposta** tanto quanto para o arquivo salvo — os dois têm de ser idênticos.
- Não se aplica aos arquivos internos do repositório (`teses/`, `modelos/`, `scripts/`), que seguem o
  snake_case de `modelos/README.md`.
- Nome de parte real nunca entra em arquivo deste repositório — nos exemplos, `NOME DA PARTE`.

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
