# Instruções de projeto — ASJUR (Claude Code)

Este arquivo vale para **todas as sessões do Claude Code** — local (CLI/desktop) e **cloud/web** —, porque
é lido do próprio repositório. Cada seção indica onde se aplica:

| Seção | Claude Code local | Claude Code cloud/web | Project do claude.ai |
|---|---|---|---|
| Conversão de PDF/DOC da parte → `.md` | sim | **não** (sem acesso a `D:\Claude\00 caso_atual` nem ao Python local) | não |
| Título da sessão com o nome do Reclamante | sim | sim | sem ferramenta de renomear — usar o fallback da seção |
| Formato `.docx`, nome do arquivo e formatação da minuta (skill `minuta-peca`) | sim | sim | descrever o padrão manualmente |

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

## Formato, nome do arquivo e formatação de toda minuta — skill `minuta-peca`

**Três diretrizes permanentes, já registradas, que valem para toda peça gerada (contestação,
contrarrazões, recurso, quesitos, embargos, manifestação, parecer):**

1. **Formato: sempre `.docx`.** Nunca entregar minuta como `.md`, `.txt`, `.pdf`, `.odt`,
   artefato HTML ou texto colado no chat. O texto da resposta explica a peça; não a substitui.
   `.md` só serve para o esqueleto anonimizado em `modelos/`.
2. **Nome do arquivo** com espaços simples nas separações internas — **nunca `_`** — e ` - `
   (espaço, hífen, espaço) entre as designações, com o **nome da parte em CAIXA ALTA**:
   `Quesitos - Perícia Médica - JOÃO DA SILVA SANTOS.docx`. A caixa alta vale também dentro da
   peça, na epígrafe e no bloco de qualificação.
3. **Formatação** de `modelos/_FORMATO_BASE.docx`, com os **tópicos principais dentro de
   retângulos** (borda simples nos quatro lados, centralizado, negrito), além do cabeçalho com
   logotipo, rodapé, fonte Arial 11 e espaçamento do padrão MS/DEJUR/SEJUR.

Antes de gerar ou entregar qualquer peça, **carregue a skill `minuta-peca`**
(`.claude/skills/minuta-peca/SKILL.md`) e use o gerador
`.claude/skills/minuta-peca/scripts/montar_peca.py`, que já aplica as três diretrizes.
Antes de entregar, rode o validador — ele reprova a peça fora do padrão:

```bash
python3 .claude/skills/minuta-peca/scripts/conferir_peca.py "<arquivo>.docx"
```

Nunca recrie a formatação a partir de descrição em texto e nunca entregue peça sem passar pelo
validador.

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
