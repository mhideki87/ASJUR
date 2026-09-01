---
name: formatar-minuta
description: >-
  Padrão único de formatação de TODA minuta da Assessoria Jurídica ECT — contestação, recurso ordinário,
  recurso de revista, contrarrazões, embargos, quesitos, manifestação, impugnação, petição simples: fonte
  Arial 11, entrelinha exata de 18 pt, margens 3/2/3/2 cm, cabeçalho com logotipo dos Correios, rodapé com
  endereço e numeração de página, tópico principal em CAIXA ALTA dentro de retângulo, subtópicos numerados em
  negrito sublinhado, citações em Arial 10 recuadas 4 cm, fecho e assinatura (Marcos Hideki
  Kamibayashi — OAB/MS 14.580). DISPARE sempre que for redigir, montar, converter, reformatar ou entregar
  qualquer peça em .docx/.odt, mesmo que o usuário não mencione formatação, e também quando ele pedir "põe no
  formato", "gera o docx", "formata a peça", "arruma o cabeçalho/rodapé/assinatura", "numera os tópicos",
  "põe o título na caixa". DISPARE também para reformatar peça antiga fora do padrão. NÃO dispare em sessão
  só de análise, de roteamento de tese ou de dúvida jurídica, sem entrega de arquivo.
---

# Formatação padrão das minutas (ASJUR/ECT)

## Regra de precedência

Esta skill é a **fonte única** da formatação de qualquer peça da assessoria — **trabalhista e cível, sem
distinção**: mesma fonte, mesmas margens, mesmo espaçamento, mesmo cabeçalho e rodapé, mesma assinatura.
Onde qualquer outro arquivo da base (playbook, `modelos/README.md`, prompt antigo, peça anexada pelo usuário)
descrever fonte, margem, espaçamento, numeração, cabeçalho, rodapé ou assinatura de forma diferente,
**vale esta skill**.

Peça-modelo anexada pelo usuário serve para **estrutura, tese e texto reaproveitável** — nunca para
formatação. A formatação vem sempre de `modelos/_FORMATO_BASE.docx` + a especificação desta skill.

## Como produzir o arquivo

`modelos/_FORMATO_BASE.docx` já contém, byte a byte, o cabeçalho (com o logotipo), o rodapé, os estilos e a
configuração de página do padrão. **Nunca recrie isso a partir da descrição em texto** — clone o arquivo.

O caminho normal é o script, que faz exatamente isso: copia todo o `.docx` base e regrava só o corpo.

```bash
python .claude/skills/formatar-minuta/scripts/gerar_minuta_docx.py <minuta.md> <saida.docx>
```

Só stdlib (`zipfile` + XML montado à mão) — roda em qualquer Python 3.8+, local ou cloud, sem instalar nada.

Você escreve a minuta num `.md` com a marcação abaixo; o script devolve o `.docx` com a formatação exata.
Referência completa da marcação e das medidas:
[`referencia/especificacao_formatacao.md`](referencia/especificacao_formatacao.md). Exemplo pronto de
entrada, com todos os tipos de bloco: [`referencia/exemplo_minuta.md`](referencia/exemplo_minuta.md).

Se, por qualquer motivo, o arquivo tiver de ser montado à mão (LibreOffice/Word), abra
`modelos/_FORMATO_BASE.docx`, escreva dentro dele e siga a especificação — não comece de documento em branco.

## Marcação da minuta (`.md` de entrada)

| Marca na linha | Vira |
|---|---|
| `@ENDERECAMENTO: EXCELENTÍSSIMO(A)...` | Endereçamento em negrito, caixa alta, sem recuo |
| `@AUTOS: 0000000-00.0000.5.24.0000` | `Autos nº. ...` em negrito |
| `@POLO: RECLAMANTE: [NOME]` | Linha de polo (rótulo em negrito, valor normal). Repita para cada polo |
| `@PREAMBULO: <qualificação da ECT>` | Parágrafo de qualificação, recuo de 1ª linha |
| `# DAS PRERROGATIVAS PROCESSUAIS` | **Tópico principal**: caixa alta, negrito, centralizado, dentro de retângulo |
| `## 1 – DA CARÊNCIA DE AÇÃO` | Subtópico: negrito + sublinhado, caixa alta, recuo 3 cm |
| `### 5.1 – DA BASE DE CÁLCULO` | Subsubtópico: mesma forma do subtópico |
| texto solto | Parágrafo do corpo: justificado, recuo de 1ª linha de 3 cm |
| `> "Ementa..."` | Citação: Arial 10, recuo 4 cm, justificado |
| `>> Salário R$ 0,00 ÷ 30 = ...` | Bloco de cálculo/enumeração: Arial 10, recuo 4 cm, alinhado à esquerda |
| `- (a) texto da alínea` | Alínea do corpo: recuo 3 cm, sem recuo de 1ª linha |
| `+ a) PRELIMINARMENTE, ...` | Alínea de requerimento: recuo 3 cm, espaçamento maior depois |
| `@QUEBRA` | Quebra de página — separa a petição de juntada das razões, em recurso e contrarrazões |
| `@ASSINATURA: Nome \| OAB/UF 00.000` | Troca a assinatura padrão — só quando o próprio usuário pedir, nunca por conta própria. Precisa vir **antes** do `@FECHO` |
| `@FECHO` | Fecho ("Nesses Termos, / Pede Deferimento. / Campo Grande/MS, data de assinatura eletrônica.") + assinatura |

Ênfase dentro da linha: `**negrito**`, `*itálico*`, `__sublinhado__`. Combinam entre si
(`**__assim__**` = negrito sublinhado).

`@FECHO` já emite os três parágrafos do fecho e a assinatura completa (nome + OAB) — não escreva o bloco de
assinatura à mão. Aceita local próprio: `@FECHO: Campo Grande/MS, [DATA].`

Espaçadores em branco (4 depois do endereçamento, 2 depois do bloco de polos, 2 antes da assinatura) são
emitidos automaticamente — não crie linhas em branco para isso.

Comentário `<!-- ... -->`, de uma ou mais linhas, é ignorado e não vai para o `.docx`.

## Regras de formatação que você precisa aplicar ao escrever (o script não adivinha)

1. **Tópico principal em retângulo e caixa alta** — só as divisões maiores da peça: `DA EQUIPARAÇÃO À
   FAZENDA PÚBLICA`, `RESUMO DA VESTIBULAR`, `PRELIMINARMENTE`, `DO MÉRITO`, `DOS REQUERIMENTOS` e
   equivalentes do tipo de peça (`DAS RAZÕES DO RECURSO`, `DO CABIMENTO`, `DA TEMPESTIVIDADE`). Escreva o
   texto já em caixa alta — não existe formatação automática de maiúsculas no padrão.
2. **Numeração dos subtópicos é manual e recomeça em 1 dentro de cada tópico principal.** Em
   `PRELIMINARMENTE`, `1 – ...`; ao entrar em `DO MÉRITO`, volta a `1 – ...`. Desdobramento vira `5.1 – `,
   `5.2 – `. Separador é sempre espaço + travessão + espaço (` – `, en dash), nunca `-` nem `.`.
   Não use lista automática do Word.
3. **Um pedido por subtópico**, na ordem da inicial/do recurso — casa com a regra 9 do `CONTEXTO.md`
   (nenhum pedido sem resposta).
4. **Citação só do que está nos autos** (regra 2 do `CONTEXTO.md`). Ementa, dispositivo de lei e trecho de
   documento vão em bloco `>`; conta de cálculo e enumeração de valores vão em `>>`.
5. **Nota de rodapé: o padrão não usa.** O rodapé da página é fixo (endereço + numeração) e vem do arquivo
   base. Referência a documento (SEI, Id do PJe, folha) vai **no corpo, entre parênteses** — nunca em nota
   de rodapé.
6. **Assinatura invariável, nas duas áreas:** `Marcos Hideki Kamibayashi` / `OAB/MS 14.580`, centralizado,
   em negrito — vale igual em trabalhista e em cível. Só troque se o próprio usuário pedir, na sessão.
7. **Marcações de conferência** (`[REVISAR: ...]`, `[INSERIR: ...]`) ficam no corpo, em texto normal, e são
   repetidas na lista de conferência humana ao final da resposta — não no arquivo.

## O que muda por tipo de peça (e o que nunca muda)

Nunca muda — em nenhum tipo de peça, em nenhuma das duas áreas: fonte, margens, espaçamento, cabeçalho,
rodapé, retângulo do tópico, numeração, fecho, assinatura.

Muda, no bloco de qualificação:

| Tipo de peça | Endereçamento | Rótulos de polo | Fundamento de admissibilidade |
|---|---|---|---|
| Contestação | Vara do Trabalho | RECLAMANTE / RECLAMADA | art. 847 da CLT c/c art. 336 do CPC |
| Recurso ordinário | Petição de juntada à Vara + razões ao TRT da 24ª Região | RECORRENTE / RECORRIDO | art. 895 da CLT |
| Contrarrazões de RO | Petição de juntada à Vara + razões ao TRT da 24ª Região | RECORRIDO / RECORRENTE | art. 900 da CLT |
| Recurso de revista | Presidência do TRT24 + razões ao TST | RECORRENTE / RECORRIDO | art. 896 da CLT |
| Embargos de declaração | Juízo/órgão que decidiu | EMBARGANTE / EMBARGADO | art. 897-A da CLT c/c art. 1.022 do CPC |
| Quesitos / manifestação | Juízo do processo | conforme os autos | — |
| Contestação cível | Juizado Especial Federal ou Vara Federal | AUTOR / RÉ | `[REVISAR: dispositivo]` |
| Recurso / contrarrazões em cível | Turma Recursal do JEF ou TRF3 | RECORRENTE / RECORRIDO | `[REVISAR: dispositivo]` |

Nas linhas de cível, o endereçamento e os rótulos de polo estão confirmados; o dispositivo de
admissibilidade de cada peça **ainda não** — confirme com o usuário na primeira peça cível da sessão e
registre aqui pela skill `atualizar-base-conhecimento`. Não preencha por dedução.

Recurso e contrarrazões são **dois blocos de qualificação no mesmo arquivo**: a petição de juntada (dirigida
à Vara) e as razões (dirigidas ao Tribunal), cada uma com seu `@ENDERECAMENTO`.

## Nome do arquivo entregue

**Não é desta skill.** O nome do arquivo é da skill **`nomear-minuta`** — invoque-a ao salvar ou citar o
arquivo, e não repita a regra de nome aqui.

Esta skill decide só o **formato**: a peça é gerada em `.docx`, porque o padrão visual vem de clonar
`modelos/_FORMATO_BASE.docx`. A extensão que chega ao usuário é a que a `nomear-minuta` fixar — sendo
`.odt`, salve o `.docx` como `.odt` no LibreOffice, que preserva tudo. Nunca monte a peça direto em
documento em branco.

## Antes de entregar, confira

- [ ] Cabeçalho com logotipo e rodapé com endereço + número de página aparecem em **todas** as páginas
      (vêm do arquivo base — se não aparecerem, o `.docx` não foi gerado a partir dele).
- [ ] Todo tópico principal está em caixa alta, centralizado e dentro do retângulo.
- [ ] Numeração dos subtópicos reinicia em cada tópico principal e não tem salto nem repetição.
- [ ] Nenhum pedido da inicial/do recurso ficou sem subtópico.
- [ ] Citações em Arial 10 recuadas 4 cm; nada de citação em corpo de texto normal. Itálico só em expressão
      latina no corpo (*ad argumentandum tantum*, *verbis*), nunca na citação inteira.
- [ ] Fecho e assinatura fecham a peça; nada depois deles.
- [ ] Nenhuma nota de rodapé no documento.
- [ ] O arquivo **não** foi copiado para dentro deste repositório (dado real de parte fica em
      `D:\Claude\00 caso_atual`).
- [ ] O nome do arquivo saiu da skill `nomear-minuta` — sem `_`, tópicos separados por ` - `, nome da parte
      por último em caixa alta.

## Nunca

- Recriar cabeçalho, rodapé ou logotipo a partir da descrição em texto, em vez de clonar
  `modelos/_FORMATO_BASE.docx`.
- Usar entrelinha 1,5 "múltipla" no lugar da entrelinha **exata de 18 pt**, ou margens diferentes de
  3/2/3/2 cm — são as duas divergências mais comuns em relação ao padrão real.
- Usar numeração automática, estilos de título do Word (`Título 1`, `Título 2`) ou nota de rodapé.
- Commitar neste repositório qualquer arquivo com nome de parte, número de processo ou CPF.
