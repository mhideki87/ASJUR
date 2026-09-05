# Instruções de projeto — ASJUR (Claude Code)

Este arquivo vale para **todas as sessões do Claude Code** — local (CLI/desktop) e **cloud/web** —, porque
é lido do próprio repositório. Cada seção indica onde se aplica:

| Seção | Claude Code local | Claude Code cloud/web | Project do claude.ai |
|---|---|---|---|
| Consulta à base de conhecimento (índice → fichas) | sim | sim | sim |
| Formatação da minuta (skill `formatar-minuta`) | sim | sim | sem skills — seguir a especificação do arquivo da skill como texto |
| Consolidação da base ao final da tarefa (skill `atualizar-base-conhecimento`) | sim | sim | sem skills nem escrita de arquivo — usar a seção 6.2 do playbook |
| Nome do arquivo da minuta (skill `nomear-minuta`) | sim | sim | sem skills — usar o padrão da seção 5.1 do playbook |
| Conversão de PDF/DOC da parte → `.md` | sim | **não** (sem acesso a `D:\Claude\00 caso_atual` nem ao Python local) | não |
| Título da sessão com o nome do Reclamante | sim | sim | sem ferramenta de renomear — usar o fallback da seção |
| Conferência de texto legal na internet | sim | **não** (rede bloqueada — ver seção) | sim |
| Autonomia em PR e merge (sem perguntar, sem relatório longo) | sim | sim | não se aplica — não há Git |

Para valer no cloud, qualquer alteração aqui precisa estar **commitada e enviada (push)** para a branch
usada na sessão cloud (por padrão, `main`): o cloud lê o repositório, não a máquina local.

## Consulta à base de conhecimento — ler o índice, não a base inteira

**Objetivo:** não gastar contexto lendo teses que não têm nada a ver com o processo da sessão.

A base é fatiada por tema em `teses/<área>/<tema>.md`, e o roteamento está em `INDICE.md`.

### Passo 0 — confirmar que a branch está atualizada

**Por que existe:** a sessão cloud/web pode nascer de uma branch criada semanas antes, e as fichas lidas
ali são as **daquela** branch, não as do `main`. A base é justamente o que envelhece. Já aconteceu de uma
contestação ser minutada sobre a **Súmula 294** e a **Súmula 372, I** como se vigentes — as duas canceladas
pela Resolução 225/2025, com os cancelamentos já registrados nas fichas do `main` —, e a peça foi
protocolada assim.

```bash
git fetch origin main && git log --oneline HEAD..origin/main
```

Saiu commit na lista? A branch está atrás: rebasear (ou ler as fichas de `origin/main`) **antes** de usar a
base. Um sinal rápido do mesmo problema: se `git ls-files` ainda mostrar `base_conhecimento_juridico_*.md`,
a branch é anterior ao fatiamento em `teses/` e a base que ela carrega está superada.

**Branch atrasada também não tem as skills.** `.claude/skills/` é lido do repositório: numa branch anterior
à criação das skills, `formatar-minuta` e `nomear-minuta` simplesmente não existem na sessão — e o padrão
visual e o nome do arquivo passam a sair da peça-modelo que o usuário anexou, que é justamente o que a
regra proíbe. Já aconteceu: peça entregue em `.odt`, com underscores no nome e entrelinha 1,5 herdada do
modelo anexado, e a divergência só apareceu depois do rebase. Por isso o Passo 0 vem **antes** de minutar,
não depois: rebasear é o que faz as skills existirem na sessão.

**Protocolo obrigatório, em toda sessão que envolva analisar peça ou minutar:**

1. Ler `CONTEXTO.md` por inteiro (é curto: perfil e regras inegociáveis).
2. Ler os documentos do processo e **listar os pedidos**.
3. Rotear com o script, que faz a busca **fora** do contexto — nenhuma linha da tabela do índice entra na
   conversa:

   ```bash
   python scripts/rotear.py --por-pedido "<um pedido por linha>"
   ```

   Ele devolve só os caminhos das fichas que casaram, já com as de "Sempre aplicável". Aceita também
   `--arquivo <caminho>` (inclusive fora do repositório) e `--area trabalhista|civel`. Alimente-o com a
   **lista de pedidos**, não com a inicial inteira: a inicial menciona de passagem temas que não são
   pedido nenhum, e cada um vira ficha aberta à toa.
4. Abrir **somente** as fichas que o script apontou. Casamento marcado "fraco" (um gatilho só) é
   candidato, não resposta: conferir se o tema é mesmo aquele antes de abrir.
5. Só então abrir o modelo estrutural (`modelos/<área>/…`) e a seção correspondente do
   `playbook_prompts_ECT.md`.

Sem Python no ambiente, ou o script falhando: aí sim ler o `INDICE.md` (protocolo do topo + tabela) e casar
os gatilhos à mão. O índice continua sendo a fonte legível para humano e a rede de segurança — o script só
evita pagá-lo em contexto a cada sessão.

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

## Formatação de toda minuta — skill `formatar-minuta`

**Objetivo:** toda peça sai no mesmo padrão visual, sem depender de o usuário anexar peça-modelo antiga.

**Gatilho:** qualquer sessão em que uma peça vá ser redigida, montada, convertida, reformatada ou entregue
como arquivo — contestação, recurso ordinário, recurso de revista, contrarrazões, embargos, quesitos,
manifestação, impugnação, petição simples —, mesmo que o usuário não fale de formatação.

**Ação:** invocar a skill **`formatar-minuta`** (`.claude/skills/formatar-minuta/`) **antes** de começar a
escrever a peça, não depois. Ela traz a especificação completa (Arial 11, entrelinha exata de 18 pt, margens
3/2/3/2 cm, tópico principal em caixa alta dentro de retângulo, subtópicos numerados em negrito sublinhado,
citações em Arial 10 recuadas 4 cm, cabeçalho com logotipo, rodapé com endereço e numeração, fecho e
assinatura) e o gerador:

```bash
python .claude/skills/formatar-minuta/scripts/gerar_minuta_docx.py <minuta.md> <saida.docx>
```

Regras:
- Essa skill é a **fonte única** da formatação. Onde qualquer outro arquivo da base, prompt antigo ou peça
  anexada disser coisa diferente sobre fonte, margem, espaçamento, numeração, cabeçalho, rodapé ou
  assinatura, **vale a skill**.
- Peça-modelo anexada pelo usuário serve para **estrutura, tese e texto reaproveitável** — nunca para
  formatação.
- **Nunca** recriar cabeçalho, rodapé ou logotipo a partir de descrição em texto: clone
  `modelos/_FORMATO_BASE.docx`.
- O arquivo da peça, por conter dado real da parte, é gravado **fora deste repositório** (em
  `D:\Claude\00 caso_atual\<pasta da parte>`, ao lado dos documentos do processo). Nunca em `modelos/`.
- O padrão **não usa nota de rodapé**: referência a documento (SEI, Id do PJe, folha) vai no corpo, entre
  parênteses.

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
Tipo - Tema abreviado - NOME DA PARTE.docx
```

Espaço simples no lugar de `_`; tópicos separados por ` - `; nome da parte por último, em caixa alta;
extensão sempre `.docx`. Exemplo de formato: `RO - Resp Subs - NOME DA PARTE.docx`.

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

## Conferência de texto legal — o cloud/web não alcança as fontes oficiais

**Objetivo:** não repetir, a cada sessão, uma tentativa de conferência que o ambiente não permite concluir —
e, principalmente, não deixar que resultado de busca vire citação de norma.

**O que foi constatado (03/09/2026, sessão cloud/web):** a política de rede do ambiente bloqueia o acesso
externo do `WebFetch` e do `curl`. Ficaram inacessíveis, entre outros, `planalto.gov.br`, `in.gov.br`
(Diário Oficial), `bvsms.saude.gov.br`, `renastonline.ensp.fiocruz.br` e repositórios de universidades. O
`noProxy` do ambiente libera só registros de pacote (npm, PyPI, crates), as APIs da Anthropic e o acesso git
ao GitHub. O `WebSearch` funciona, porque não é egresso direto — mas devolve **resumo de terceiros, não o
texto da norma**.

**Regra:** resumo de busca **não** confere norma. Ele serve para descobrir que existe uma questão; nunca
para afirmar o conteúdo de artigo, anexo, lista, súmula ou portaria. Duas buscas que se contradizem são
sinal de que a questão é real e precisa de leitura humana — não de uma terceira busca.

**Como proceder ao esbarrar num `[REVISAR]` de texto legal em sessão cloud/web:**

1. Tentar o `WebFetch` **uma vez**. Bloqueou, não insistir com outro domínio atrás do mesmo texto.
2. Usar o `WebSearch` para mapear **o que está em jogo** — qual norma, qual dispositivo, se há divergência,
   qual o impacto na tese se a resposta for num sentido ou noutro.
3. Registrar na ficha como **não confirmado**, com as leituras concorrentes e a linha de resposta para cada
   uma — nunca como tese fechada.
4. Dizer ao usuário, na resposta, que a conferência ficou pendente, por quê, e **em que ordem** conferir.
5. Diagnóstico do bloqueio, se necessário: `curl -sS "$HTTPS_PROXY/__agentproxy/status"`.

A política de rede é escolhida na criação do ambiente e pode mudar; o que está acima é o comportamento
observado, não uma garantia permanente. Em sessão local (CLI/desktop), a conferência costuma ser possível —
é o caminho preferível para fechar pendência de texto legal.

## Autonomia em PR e merge — executar, não narrar

**Objetivo:** o usuário não quer ser consultado nem receber relatório detalhado a cada etapa de Git. Ele
quer o problema resolvido e uma confirmação curta no final.

**Gatilho:** qualquer sessão que envolva commit, push, abertura de pull request, resolução de conflito,
correção de CI ou merge neste repositório.

**Ação:** executar o ciclo inteiro por conta própria — commit, push, abrir o PR, corrigir o que estiver
vermelho e fazer o merge —, e só então responder, em **até três linhas**, o que ficou pronto e o link do PR.

Regras:
- **Não perguntar** se pode commitar, se pode abrir PR, se pode fazer merge, qual mensagem de commit usar,
  qual método de merge, se pode apagar a branch. É tudo autorizado por padrão nesta base.
- **Não explicar** passo a passo o que o Git fez: nada de listar arquivo por arquivo, colar diff, narrar
  tentativa de push, descrever a resolução de conflito ou o motivo de cada falha de CI. O diff do commit é o
  registro; quem quiser o detalhe abre o PR.
- **Falar apenas quando houver decisão jurídica em jogo** (duas teses possíveis, risco de perder argumento,
  dado do processo faltando) ou quando algo travar de fato e não houver caminho — aí sim, dizer em uma linha
  o que trava e o que falta.
- Problema no meio do caminho (push recusado, conflito, CI vermelho, lint) se **resolve na própria sessão**,
  sem avisar antes nem pedir permissão; a resposta final menciona no máximo que houve correção, sem o
  histórico.
- Continua valendo o que é proibido em qualquer sessão: nunca reescrever histórico de branch de outra
  pessoa, nunca desativar ou pular teste para ficar verde, nunca subir dado real de parte para o
  repositório.

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
