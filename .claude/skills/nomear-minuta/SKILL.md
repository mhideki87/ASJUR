---
name: nomear-minuta
description: >-
  Define o nome do arquivo de toda minuta entregue ao usuário no padrão
  "Tipo - Tema - Marcador - NOME DA PARTE": espaço no lugar de "_" e " - " entre os tópicos.
  DISPARE sempre que você for gerar, salvar, anexar, renomear ou apenas citar o nome de um arquivo de peça
  (contestação, contrarrazões, recurso ordinário, recurso de revista, quesitos, manifestação, embargos,
  impugnação aos cálculos, petição de juntada) — em .odt, .docx, .md, .txt ou .pdf —, e também quando o
  usuário pedir para "renomear", "arrumar o nome", "salvar como", "tirar os underscores" ou reclamar do nome
  de um arquivo entregue. Vale igualmente para o nome escrito no corpo da resposta, não só para o arquivo em
  disco. NÃO dispare para arquivos internos do repositório (fichas de teses/, modelos/, scripts) — esses
  seguem o snake_case de modelos/README.md.
---

# Nome do arquivo de minuta (ASJUR)

## Padrão

```
Tipo - Tema abreviado - Marcador - NOME DA PARTE.ext
```

Exemplo do formato (nome de parte sempre fictício neste repositório, que é público):

```
RO - Resp Subs - PRINT - NOME DA PARTE.odt
```

Quatro regras, nessa ordem de prioridade:

1. **Nenhum `_` no nome.** Onde havia `_`, entra **espaço simples**. Isso vale para todos os blocos,
   inclusive o nome da parte (`ADEMAR_LOPES` → `ADEMAR LOPES`).
2. **Tópicos separados por ` - `** — espaço, hífen, espaço. Nunca `-` colado (`RO-Resp`), nunca `_-_`,
   nunca `–` (travessão) ou `—`.
3. **Nome da parte por último, em CAIXA ALTA**, como o usuário escreveu. Hífen interno de nome próprio ou
   de sigla fica como está (`SANTA HELENA-MS` não vira `SANTA HELENA - MS`) — a regra 2 só separa blocos.
4. **Extensão preservada**, sem espaço antes do ponto. Padrão da trabalhista: `.odt`.

## Os blocos

| Bloco | Obrigatório | Conteúdo |
|---|---|---|
| Tipo | sim | abreviação da peça — ver tabela abaixo |
| Tema abreviado | sim | do que trata (`Resp Subs`, `Inc Fun`, `Insalub`) — abreviado, não a ementa |
| Marcador | não | rito, fase ou destino da peça (`PRINT`, `Juntada`, `TRT24`) |
| NOME DA PARTE | sim | Reclamante/Autor; havendo mais de um, o primeiro + `e outros` |

Abreviações de tipo já em uso (`playbook_prompts_ECT.md`, seção 5.1): `Cont` = contestação ·
`Contrarraz` = contrarrazões · `RO` = recurso ordinário · `RR` = recurso de revista ·
`Manifest` = manifestação · `ED` = embargos de declaração · `Quesitos` = quesitos de perícia.
Abreviações de tema em uso: `Inc Fun` = incorporação de função · `Resp Subs` = responsabilidade
subsidiária. **Abreviação nova que você criar entra no playbook** — pela skill
`atualizar-base-conhecimento`, ao final da sessão.

## Como aplicar

Ao entregar a minuta, monte o nome pelos blocos acima e confira, antes de salvar ou citar:

- [ ] zero `_` no nome inteiro;
- [ ] todo separador é exatamente ` - ` (um espaço de cada lado);
- [ ] nenhum espaço duplo, nenhum espaço no começo/fim ou antes da extensão;
- [ ] nome da parte em caixa alta, no último bloco;
- [ ] o nome citado na resposta é **idêntico** ao do arquivo salvo.

Recebendo um nome antigo para corrigir, a conversão é mecânica: `_-_` → ` - `, depois `_` → ` `, depois
colapsar espaços repetidos. `Cont_-_Inc_Fun_-_NOME_DA_PARTE.odt` → `Cont - Inc Fun - NOME DA PARTE.odt`.

Só renomeie arquivo em disco quando o usuário pedir; a regra é sobre o nome que **você** dá ao que entrega.

## Fora do escopo

Arquivo interno do repositório continua no padrão de `modelos/README.md`
(`modelos/<área>/<tipo_peca>__<tema>.md`, em snake_case) — este padrão é só para a peça que vai para o
usuário e para o processo. E nome de parte real nunca é escrito em arquivo deste repositório: nos exemplos,
use sempre `NOME DA PARTE`.
