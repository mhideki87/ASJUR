---
name: minuta-peca
description: Padrão obrigatório de nome de arquivo e de formatação visual de toda minuta/petição gerada neste repositório (contestação, contrarrazões, recurso, quesitos de perícia, embargos, manifestação, parecer). Use SEMPRE que for produzir, editar ou entregar um arquivo de peça jurídica — inclusive quando o usuário só disser "faça a contestação", "elabore os quesitos", "minute o recurso" ou anexar uma peça para adaptar. Garante entrega sempre em .docx, nome de arquivo com espaços e hífen (nunca "_") e tópicos em retângulo com o cabeçalho, fonte e espaçamento da Assessoria Jurídica MS/DEJUR/SEJUR.
---

# Minuta de peça jurídica — formato, nome do arquivo e formatação

Três diretrizes **permanentes** do usuário. Valem para **toda** peça, de qualquer tema e
em qualquer ambiente (local e cloud/web). Não são sugestões e não precisam ser reconfirmadas
a cada sessão.

## Diretriz 1 — formato do arquivo: sempre `.docx`

**Toda minuta é entregue como arquivo `.docx`.** Sem exceção por tipo de peça, por tamanho ou
por pressa. Não entregue peça como `.md`, `.txt`, `.pdf`, `.odt`, artefato HTML, nem como texto
colado na resposta do chat — o usuário protocola e edita a peça no Word, e qualquer outro
formato quebra o fluxo.

- O texto no chat serve para **explicar** a peça e destacar pontos a revisar, nunca para
  substituir o arquivo.
- Se o usuário anexar um `.odt`, `.pdf` ou `.doc` como modelo ou como peça a adaptar, leia dele
  o que precisar, mas **entregue em `.docx`**.
- `.md` só é usado para o esqueleto anonimizado em `modelos/` — que é material de reúso
  interno, não é minuta.
- Só use outro formato se o usuário pedir explicitamente naquela sessão.

O gerador e o validador recusam qualquer extensão diferente de `.docx`.

## Diretriz 2 — nome do arquivo

- **Separação interna de palavras: espaço simples.** Nunca `_`, nunca `-` no lugar de espaço.
- **Separação entre designações: ` - ` (espaço, hífen, espaço).**
- Ordem: `<Tipo de peça> - <Tema> - <NOME DA PARTE ADVERSA>.docx`
- O nome da parte vai em **caixa alta**, como consta dos autos.

```
✅ Quesitos - Perícia Médica - JOÃO DA SILVA SANTOS.docx
✅ Contestação - Doença Ocupacional - MARIA SOUZA LIMA.docx
✅ Recurso Ordinário - Adicional de Periculosidade - MARIA SOUZA.docx

❌ Quesitos_Pericia_Medica_JOAO_DA_SILVA_SANTOS.docx
❌ Quesitos-Pericia-Medica-JOÃO DA SILVA SANTOS.docx
❌ quesitos pericia medica joão da silva.docx
```

Acentuação é preservada (`Perícia`, `Contestação`). Caracteres proibidos em nome de arquivo
(`< > : " / \ | ? *`) viram espaço.

Use sempre o helper, em vez de montar a string à mão:

```python
from montar_peca import nome_arquivo
nome_arquivo("Quesitos", "Perícia Médica", "JOÃO DA SILVA SANTOS")
# 'Quesitos - Perícia Médica - JOÃO DA SILVA SANTOS.docx'
```

## Diretriz 3 — formatação padrão

Base visual: `modelos/_FORMATO_BASE.docx` (cabeçalho com logotipo dos Correios e
"Assessoria Jurídica MS/DEJUR/SEJUR", rodapé com endereço e numeração, margens, bloco de
assinatura). **Nunca recrie a formatação do zero** — abra o `.docx` e reaproveite o pacote.

O ponto que mais se erra: **todo tópico principal vai dentro de um RETÂNGULO** — parágrafo
centralizado, em negrito, com borda simples fina nos quatro lados. Peça sem os retângulos
está fora do padrão, ainda que o texto esteja correto.

| Elemento | Aparência |
|---|---|
| Tópico principal | **RETÂNGULO**: borda nos 4 lados, centralizado, negrito, caixa alta |
| Subtópico | negrito + sublinhado, recuado, numerado (`1 – DA ...`) |
| Parágrafo | justificado, recuo de 1ª linha, entrelinha 18pt |
| Citação/ementa | bloco recuado, itálico, corpo 10, entrelinha 13pt |
| Alínea/requerimento | bloco recuado, sem recuo de 1ª linha (`a) ...`) |
| Marcador | travessão com recuo deslocado |

Fonte **Arial 11** em todo o corpo (Arial 10 nas citações). Os valores exatos em twips
estão em `reference/formatacao.md` — consulte antes de escrever XML na mão.

## Como gerar a peça

Use o gerador; ele já aplica as três diretrizes.

```python
import sys; sys.path.insert(0, ".claude/skills/minuta-peca/scripts")
from montar_peca import montar, nome_arquivo

montar(
    saida=nome_arquivo("Quesitos", "Perícia Médica", "JOÃO DA SILVA SANTOS"),
    vara="5ª VARA DO TRABALHO DE CAMPO GRANDE/MS",
    autos="0000000-00.2026.5.24.0000",
    reclamante="JOÃO DA SILVA SANTOS",
    tipo_peca="QUESITOS PARA A PERÍCIA MÉDICA",
    admissibilidade="fundamento no art. 465, § 1º, II e III, do CPC, c/c art. 769 da CLT",
    corpo=[
        ("T", "DO MÉRITO"),
        ("S", "1 – DA INEXISTÊNCIA DE NEXO CAUSAL"),
        ("P", "Texto com **negrito** e *itálico* onde couber."),
        ("C", "“Ementa transcrita.” (TST — RR 000-00)"),
        ("A", "a) requerimento;"),
        ("M", "item de lista;"),
        ("Q", "Texto do quesito — numera sozinho."),
    ],
)
```

A saída **tem de terminar em `.docx`** — `montar()` recusa outra extensão.

Tipos de parágrafo: `T` tópico em retângulo · `S` subtópico · `P` parágrafo · `C` citação ·
`A` alínea · `M` marcador · `Q` quesito numerado · `B` linha em branco.
Marcação inline: `**negrito**`, `*itálico*`, `***ambos***`.

O gerador **falha de propósito** se algum placeholder do modelo (`[Nº DO PROCESSO]`,
`[TIPO DE PEÇA]` etc.) ficar por substituir. Placeholders marcados `[REVISAR]` são
permitidos — são os campos que o usuário preenche depois (ex.: nome do assistente técnico).

## Conferência antes de entregar

1. A entrega é um arquivo **`.docx`** — não `.md`, `.pdf`, `.odt` nem texto no chat.
2. O nome do arquivo tem espaços e ` - `, e **nenhum** `_`.
3. Todos os tópicos principais estão em retângulo.
4. Cabeçalho com logotipo, rodapé e bloco de assinatura vieram do modelo.
5. Sobrou algum `[...]` que não seja `[REVISAR]`? Então falta preencher.

Validação rápida:

```bash
python3 .claude/skills/minuta-peca/scripts/conferir_peca.py "<arquivo>.docx"
```

## Onde a peça pronta pode ficar

A peça com dados reais da parte **não entra no repositório Git** (ver `CLAUDE.md` e
`README.md`): gere-a no diretório de trabalho da sessão e entregue ao usuário como arquivo.
Ao repositório só vai o esqueleto anonimizado em `modelos/<área>/<tipo_peça>__<tema>.md`.
