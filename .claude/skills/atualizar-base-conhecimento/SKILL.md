---
name: atualizar-base-conhecimento
description: >-
  Consolida na base de conhecimento do repositório ASJUR o que uma sessão produziu de novo — tese, correção
  de tese, jurisprudência confirmada, gatilho de roteamento que faltou, estrutura de peça — gravando cada
  achado na ficha/arquivo certo (teses/<área>/, modelos/, CONTEXTO.md, playbook, CLAUDE.md) e regenerando o
  INDICE.md com scripts/atualizar_indice.py. Use ao FINAL de qualquer sessão em que uma peça foi analisada ou
  minutada (contestação, contrarrazões, recurso, quesitos, manifestação, embargos), ou em que uma ficha,
  modelo ou regra da base foi criada/alterada — mesmo que o usuário não peça: a consolidação é o passo que
  faz a base crescer, e é justamente o que se perde quando a sessão termina. Use também quando o usuário
  disser "atualize a base", "consolide isso", "o que aprendemos aqui", "pode encerrar", "rode o protocolo",
  ou pedir para revisar o índice/os gatilhos. NÃO use no meio da análise ou da minuta: primeiro entrega a
  peça, depois consolida.
---

# Atualizar a base de conhecimento (ASJUR)

## O que esta skill resolve

A base cresce **por demanda**: só aprende o que for consolidado ao fim de uma sessão real. O risco é duplo e
simétrico — perder o que foi descoberto, ou inventar achado para parecer produtivo. As duas falhas custam
caro: a primeira faz a base estagnar; a segunda a envenena, porque tese não conferida vira citação errada em
peça protocolada.

Então o critério é: **consolidar só o que apareceu de fato nesta sessão, e dizer com clareza quando nada
apareceu.** "Nada novo" é resultado legítimo e frequente — a maioria das sessões repete tese conhecida.

## Passo 1 — Levantar os achados

Reveja a conversa (não a base) e responda, separadamente, cada pergunta abaixo. Se a resposta for "nada",
escreva "nada" e siga:

1. **Tese nova** — algum argumento usado aqui não está nas fichas que você abriu?
2. **Correção** — alguma tese da base se mostrou errada, incompleta, ou foi rebatida com sucesso pela parte
   contrária neste processo?
3. **Jurisprudência nova** — algum precedente **dos autos ou anexado pelo usuário** ainda não consta da ficha
   do tema? (Aresto que você "lembra" não conta — só entra o que está nos documentos da sessão.)
4. **Roteamento** — o índice levou você até a ficha certa sozinho? Se o usuário teve que dizer do que se
   tratava, ou se você abriu ficha que não servia, faltou ou sobrou gatilho.
5. **Modelo de peça** — a estrutura usada já está em `modelos/`? O caso revelou variação que valha preservar?
6. **Regra de trabalho** — o usuário corrigiu *como* você trabalha (formato, ordem das etapas, o que nunca
   fazer)? Isso não é tese, é `CONTEXTO.md`.

## Passo 2 — Mandar cada achado para o arquivo certo

| Achado | Destino |
|---|---|
| Tese nova, tema **já tem** ficha | seção correspondente da ficha (`Tese central`, `Fundamentos`, `Pontos sensíveis`) |
| Tese nova, tema **sem** ficha | ficha nova em `teses/<área>/<slug>.md`, a partir de `teses/_TEMPLATE_TESE.md` |
| Jurisprudência confirmada | seção `Jurisprudência` da ficha do tema |
| Tese que se mostrou errada | corrige o corpo da ficha, muda `status` para `revisar` e registra o motivo em `Lacunas` |
| Gatilho que faltou / sobrou | metadado `gatilhos:` da ficha (é o que faz o roteamento funcionar na próxima vez) |
| Estrutura de peça nova ou variação | `modelos/<área>/<tipo_peca>__<tema>.md` (+ `.docx` anonimizado, se houver peça real anexada) — e acrescente o caminho no metadado `modelos:` da ficha |
| Regra de trabalho, padrão formal, perfil, nomenclatura | `CONTEXTO.md` |
| Prompt que funcionou bem / erro de pedido a evitar | `playbook_prompts_ECT.md` |
| Rotina de sessão do Claude Code (automação, título, conversão) | `CLAUDE.md` |
| Protocolo de leitura do índice (a prosa, não a tabela) | `INDICE.md` — a tabela é gerada, não se edita à mão |

Área é `trabalhista`, `civel` ou `transversal` (vale nas duas). Convenções de ficha, metadados e seções:
`teses/README.md`.

Uma ficha é a **unidade de leitura**: se o achado não cabe na ficha existente sem inflá-la, ou se o tema tem
gatilho próprio na inicial, é ficha nova — não apêndice de uma ficha alheia.

## Passo 3 — Aplicar as edições

- **Somar, não substituir.** Tese nova entra ao lado do que já existe. Só reescreva ou apague o que estava
  lá se o usuário confirmar que estava errado ou desatualizado.
- Atualize o campo `atualizado:` (formato `AAAA-MM-DD`) de toda ficha que você tocar.
- `status:` da ficha: `validada` (usada em peça real, conferida) · `rascunho` (candidata a tese) ·
  `revisar` (algo se mostrou errado). Ficha nova nascida de uma sessão real de minuta é `validada`;
  nascida de hipótese ou de levantamento é `rascunho`.
- **Nada inventado.** Norma, súmula e aresto só entram com a fonte exata. Faltando informação, deixe
  `[REVISAR: o que conferir]` no corpo — não preencha com conteúdo plausível.
- **Nenhum dado que identifique parte real** — nome, nº de processo, CPF, Id de documento de caso concreto.
  O repositório é **público**. Vale para o corpo do `.md`, para o `.docx` e para os **metadados** do `.docx`
  (autor, revisões, comentários).

## Passo 4 — Regenerar o índice

Toda vez que uma ficha for criada, renomeada, ou tiver metadado alterado:

```bash
python scripts/atualizar_indice.py           # revalida os metadados e reescreve a tabela do INDICE.md
python scripts/atualizar_indice.py --check   # confere sincronia — rode antes de propor o commit
```

O script recusa metadado faltando, `slug` diferente do nome do arquivo, `area` diferente da pasta, `status`
inválido, data fora do formato e referência para arquivo inexistente. Se ele reclamar, corrija a ficha — não
edite a tabela do `INDICE.md` à mão, ela é sobrescrita.

## Passo 5 — Apresentar e esperar aprovação

Aplique as edições nos arquivos, rode o script, e então mostre ao usuário:

1. o resumo por achado (o que entrou, em qual arquivo, e por quê);
2. o `git diff` (é o que ele revisa de fato);
3. o que ficou marcado `[REVISAR: ...]` e precisa de conferência humana.

**Não commite nem faça push sem aprovação explícita nesta sessão** — a regra da casa é que nada entra no
repositório sem o usuário ver. Aplicar no diretório de trabalho é seguro e reversível; commitar não é a
mesma coisa. Se ele aprovar, commite na branch da sessão com mensagem que diga o **tema** consolidado, não
"atualiza base".

## Tarefa que não é minuta

Se a sessão foi de manutenção do repositório (criou ficha, mexeu em modelo, mudou estrutura), o Passo 1 não
se aplica — vá direto ao Passo 4 e ao Passo 5: garanta que o índice está em sincronia, que os metadados
`modelos:`/`ver_tambem:` apontam para arquivos existentes, e que nenhum arquivo ficou órfão do roteamento.

## Quando não há nada a consolidar

Diga isso em uma linha ("nada novo nesta sessão — tese X já estava na ficha Y") e encerre. Não crie ficha
para tema que já tem uma, não acrescente gatilho redundante, não promova a "achado" o que era apenas a base
funcionando como devia. Uma base pequena e confiável vale mais que uma grande e duvidosa.

## Fora do Claude Code

No Project do claude.ai não há como gravar arquivo nem rodar o script. Ali o equivalente é o protocolo da
seção 6.2 de `playbook_prompts_ECT.md`: escrever o **trecho exato** a acrescentar em cada arquivo, incluindo
o bloco de metadados completo da ficha, para o usuário colar e commitar — e lembrar que ele precisa rodar
`python scripts/atualizar_indice.py` depois.
