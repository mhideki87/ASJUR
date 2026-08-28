---
name: formatar-peca
description: Gera o arquivo final de qualquer peça da ASJUR (.docx) com a formatação oficial do escritório — cabeçalho com logotipo dos Correios, rodapé, Arial 11, entrelinha 1,5, recuo de 3 cm, marcadores de seção em caixa, títulos numerados sublinhados, citações em bloco recuado — e com o nome de arquivo na convenção correta. DISPARE sempre que for produzir o arquivo de uma contestação, contrarrazões, recurso, manifestação, quesitos ou embargos, e também quando o usuário disser que "a formatação está errada", pedir a peça "em .docx", "no formato certo", "no modelo", ou reclamar do nome do arquivo. NÃO dispare para analisar peça, para responder dúvida jurídica, nem para redigir o texto — esta skill cuida da forma, não do conteúdo.
---

# Formatar peça (ASJUR)

## O que esta skill resolve

Duas falhas que se repetiam: (a) a peça saía com formatação inventada a partir da descrição em texto,
em vez da formatação real do escritório; (b) o nome do arquivo saía com `_` no lugar de espaço.

A regra é simples: **a formatação nunca é redigida à mão em XML nem "no olho".** O corpo da peça vai num
arquivo de texto com marcas, e `scripts/gerar_peca_docx.py` aplica a formatação a partir do `.docx` modelo,
preservando cabeçalho, logotipo, rodapé e estilos byte a byte.

## Passo 1 — Escrever o conteúdo em arquivo de texto

Grave o corpo da peça num `.txt` (fora do repositório — ver Passo 4), uma marca por parágrafo:

```
@vara            2ª VARA DO TRABALHO DE CAMPO GRANDE/MS      (caixa alta, sem "ª Vara" duplicado)
@autos           0000000-00.0000.5.24.0000
@reclamante      NOME DA PARTE
@admissibilidade fundamento nos arts. 847 da CLT c/c 336 do CPC
@tipo            CONTESTAÇÃO

@caixa    MARCADOR DE SEÇÃO           → centralizado, negrito, dentro de uma caixa com borda
@titulo   1 – TÍTULO DO TÓPICO        → negrito + sublinhado, recuo esquerdo 3 cm, numerado
@p        parágrafo de corpo          → justificado, recuo de 1ª linha 3 cm, Arial 11, entrelinha 1,5
@cit      citação                     → itálico Arial 10, bloco recuado 3 cm (jurisprudência, normas)
@lista    – item                      → recuo 3,6 cm com pendente
@centro   texto centralizado
@vazio                                → linha em branco
```

Linha iniciada por `#` é comentário; linha sem marca continua o parágrafo anterior.

**Estrutura padrão da contestação** (ordem validada em peça real):

```
@caixa DA EQUIPARAÇÃO À FAZENDA PÚBLICA        (bloco padrão; fecha com a tempestividade — prazo em dobro)
@caixa DA TRAMITAÇÃO PELO “JUÍZO 100% DIGITAL”  (se a inicial aderiu — ver "Prazos" abaixo)
@caixa RESUMO DA VESTIBULAR                     (é "VESTIBULAR", não "DEMANDA")
@caixa DAS PRELIMINARES E DA PREJUDICIAL DE MÉRITO
@caixa DO MÉRITO                                (tópicos numerados 1..N, em @titulo)
@caixa DO PREQUESTIONAMENTO
@caixa DOS REQUERIMENTOS                        (alíneas a), b), c)... com os AD CAUTELAM)
```

O fecho — protesto por provas, declaração de autenticidade das fotocópias, "Nesses Termos / Pede
Deferimento / Campo Grande/MS, data de assinatura eletrônica" e o bloco de assinatura — **já vem do `.docx`
modelo**. Não repetir no conteúdo.

## Passo 2 — Gerar o arquivo

```bash
python scripts/gerar_peca_docx.py <conteudo.txt> -o "<nome do arquivo>.docx"
```

O script usa `modelos/_FORMATO_BASE.docx` por padrão; `--base` aponta outro modelo. Ele avisa quando sobra
placeholder do template sem preencher e quantas marcações `[REVISAR]`/`[INSERIR]` ficaram no corpo.

Só stdlib — roda em qualquer ambiente com Python 3, inclusive no cloud/web.

## Passo 3 — Nome do arquivo (convenção obrigatória)

```
<Tipo> - <Tema abreviado> - <Rito> - <NOME DA PARTE>.docx
```

- **Espaço simples entre as palavras.** Nunca `_` como separador de palavras.
- **` - ` (espaço-hífen-espaço) para separar os tópicos** do nome.
- Abreviações: `Cont` = contestação · `Contrarraz` = contrarrazões · `RR` = recurso de revista ·
  `ED` = embargos de declaração · `Manifest` = manifestação · `Quesitos` = quesitos de perícia ·
  `Inc Fun` = incorporação de função · `Afast` = afastamentos · `ATSum` = rito sumaríssimo ·
  `Ord` = rito ordinário.

Exemplo: `Cont - Inc Fun - ATSum - NOME DA PARTE.docx`

Errado: `Cont_-_Inc_Fun_-_ATSum_-_NOME_DA_PARTE.docx`

## Passo 4 — Onde o arquivo pode ficar

**A peça com dado real de parte nunca entra no repositório** — nem o `.txt` de conteúdo. Grave no diretório
de trabalho da sessão (scratchpad) e entregue o arquivo ao usuário. O repositório é público; ver a regra
permanente no [README.md](../../../README.md).

## Prazos que a forma não resolve, mas a peça precisa respeitar

- **Juízo 100% Digital:** havendo interesse em se opor, o prazo é **autônomo — 5 dias úteis do recebimento
  da primeira notificação** (art. 3º, §1º, da Res. CNJ 345/2020, red. Res. 378/2021), e a oposição vai em
  **petição avulsa**, não na contestação. A prática registrada da ECT é **não se opor**; confirmar no caso.
- **Tempestividade:** conferir a data de notificação e a contagem em dobro (art. 1º do Decreto-lei 779/69)
  antes de fechar o arquivo — vai sempre na lista de conferência humana.

## Quando o modelo visual precisar mudar

`modelos/_FORMATO_BASE.docx` é a fonte da verdade da formatação. Trocá-lo exige uma peça real aprovada pelo
usuário, anonimizada, e **commit só depois de aprovação explícita dele** — conferir texto oculto, metadados
e propriedades do documento é verificação humana. Ver o fluxo em [modelos/README.md](../../../modelos/README.md).
O `.docx` base precisa conter o parágrafo marcador `[CORPO DA PEÇA ...]`, que é onde o script injeta o corpo.
