# Fichas de tese — como funcionam

Cada arquivo `teses/<área>/<slug>.md` é uma **ficha de tese**: um tema autocontido, pequeno, pensado para
ser lido isoladamente. A base não é mais um documento único — é um conjunto de fichas mais o
[INDICE.md](../INDICE.md) que roteia até elas.

Áreas: `trabalhista/` · `civel/` · `transversal/` (vale nas duas áreas).

## Regra de ouro

Uma ficha por tema, e o tema é a **unidade de leitura**: se para responder a um pedido da inicial é preciso
abrir duas fichas, ou uma ficha grande da qual só 20% interessa, o recorte está errado. Ficha que passou de
~150 linhas ou que virou "tema + apêndices" deve ser dividida.

## Bloco de metadados (obrigatório no topo)

```yaml
---
area: trabalhista            # trabalhista | civel | transversal — igual ao nome da pasta
tema: Prescrição total       # como eu falaria do tema em voz alta
slug: prescricao             # igual ao nome do arquivo, sem .md
status: validada             # validada | rascunho | revisar
gatilhos: [prescrição, Súmula 294, art. 11 CLT]
pecas: [contestação, contrarrazões]
modelos: [modelos/trabalhista/contestacao__incorporacao_funcao.md]
ver_tambem: [teses/trabalhista/incorporacao_gratificacao_funcao.md]
atualizado: 2026-08-27
---
```

Formato de propósito restrito: uma chave por linha, listas em `[a, b, c]`. Não é YAML completo — é para ser
óbvio de escrever à mão e trivial de conferir por script.

**Os `gatilhos` são a parte que mais importa.** São as palavras procuradas no objeto da demanda
(por `scripts/rotear.py`, ou à mão pela tabela do `INDICE.md`) para decidir se a ficha é aberta: termos que aparecem literalmente na inicial, sinônimos, números de
norma e de súmula, nomes de parcela. Gatilho ruim = ficha invisível na hora certa, ou ficha aberta à toa.

### Gatilho é chave de busca, não resumo

Gatilho existe para uma coisa só: casar com o que aparece no **objeto da demanda** e levar à ficha certa.
Não é ementa, não é lista de tudo que a ficha discute. Cada gatilho é lido em toda sessão, de todo
processo — inclusive nos que não têm nada a ver com aquele tema.

O que **mantém**:
- o termo que o autor usa na inicial (`incorporação de gratificação`, `extravio`, `readaptação`);
- número de norma, súmula ou tema que identifica o assunto (`Súmula 51`, `Módulo 55`, `Tema 138`);
- nome da parcela ou do instituto (`FAT`, `ITF`, `quebra de caixa`, `NTEP`);
- o sinônimo que muda a palavra de verdade, não a flexão (`doença ocupacional` / `acidente de trabalho`).

O que **corta primeiro**, quando o pedágio apertar:
- flexão ou quase-repetição do vizinho (`prescrição` + `prescrição total`; `afastamento` + `afastamentos`)
  — o `rotear.py` já casa o plural sozinho, inclusive `postal`/`postais` e `indenização`/`indenizações`;
- termo já contido no campo `tema`, que o roteamento lê junto (a ficha "Prescrição total" não precisa do
  gatilho `prescrição total`);
- palavra genérica demais para discriminar (`dano moral`, `honorários`, `desconto em folha` aparecem em
  metade dos processos e não apontam para ficha nenhuma);
- detalhe interno da tese, que só faz sentido depois de a ficha estar aberta (`art. 476 CLT`,
  `divisor mensal`) — isso é conteúdo, e o lugar dele é o corpo.

Alvo de **6 a 10 gatilhos** por ficha. Acima de 12 quase sempre há redundância.

**Cortar gatilho custa recall.** Um termo a menos é um caminho a menos até a ficha; se o roteamento
deixar de achá-la, a tese não entra na peça — prejuízo muito maior que o do pedágio. Na dúvida sobre um
termo específico, mantenha. Corte o que é claramente redundante, não o que é apenas raro.

**Quando enxugar:** `python scripts/atualizar_indice.py` mede o pedágio a cada execução e avisa ao passar
de 40% da sessão típica, listando as fichas com mais gatilhos. Não corte por antecipação — enquanto o
script não reclamar, gatilho a mais é barato.

**`status`** indica o quanto se pode confiar na ficha:
- `validada` — usada em peça real, conferida.
- `rascunho` — candidata a tese (ex.: inferida de levantamento estatístico do acervo); validar contra o
  processo antes de usar, nunca citar como jurisprudência pronta.
- `revisar` — havia tese aqui e algo se mostrou errado/desatualizado; ler a seção "Lacunas" antes de usar.

Independentemente do `status`, itens pontuais incertos ficam marcados com `[REVISAR: ...]` no corpo da ficha.

## Seções do corpo

Na ordem, conforme [`_TEMPLATE_TESE.md`](_TEMPLATE_TESE.md): **Quando esta ficha se aplica** ·
**Tese central** · **Fundamentos** · **Jurisprudência (só o que já está confirmado)** ·
**Pontos sensíveis / variações** · **Ligações** · **Lacunas**.

"Quando esta ficha se aplica" é a primeira coisa lida depois do índice — precisa deixar claro, em duas ou
três linhas, se a ficha serve para o caso em mãos.

## Criar ou alterar uma ficha

1. Copiar `_TEMPLATE_TESE.md` para `teses/<área>/<slug>.md` (ou editar a ficha existente).
2. Atualizar o campo `atualizado`.
3. Regenerar a tabela do índice e validar os metadados:

```bash
python scripts/atualizar_indice.py           # reescreve a tabela do INDICE.md
python scripts/atualizar_indice.py --check    # só confere (útil antes de commitar)
```

O script recusa ficha com metadado faltando, `slug` diferente do nome do arquivo, `area` diferente da pasta,
`status` inválido, data fora do formato `AAAA-MM-DD` ou referência (`modelos`/`ver_tambem`) para arquivo
inexistente. Arquivos que começam com `_` e os `README.md` são ignorados.

## Regras de conteúdo

- **Nenhum dado que identifique parte real** — nome, nº de processo, CPF, Id de documento de caso concreto.
  Este repositório é **público**.
- Nada inventado: norma, súmula e aresto só entram com a fonte exata; na dúvida, `[REVISAR: ...]`.
- Ficha nova ou alterada é consolidada e **commitada** pela skill `atualizar-base-conhecimento` na branch
  `claude/*` da sessão; a revisão do usuário é no diff do commit (protocolo da seção 6.2 de
  [`playbook_prompts_ECT.md`](../playbook_prompts_ECT.md)). Tese nova **soma** à ficha, não substitui o que
  já está lá, a menos que o usuário confirme que o anterior estava errado.
