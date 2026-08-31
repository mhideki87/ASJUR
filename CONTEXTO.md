# Contexto permanente — Assessoria Jurídica ECT

> Único arquivo lido por inteiro em toda sessão. Curto de propósito: só o que muda a peça.
> Teses ficam em `teses/<área>/`, lidas sob demanda pelo roteamento do [INDICE.md](INDICE.md).
> No Projeto do claude.ai, é este arquivo que vai nas instruções personalizadas.

## Quem sou eu

- Advogado da **Assessoria Jurídica dos Correios (ECT)**, sempre no **polo passivo** — toda peça é de defesa.
- Assinatura: **Marcos Hideki Kamibayashi — OAB/MS 14.580**, nas duas áreas (trabalhista e cível). Base:
  Campo Grande/MS.
- **Trabalhista:** TRT da 24ª Região e Varas do Trabalho de Campo Grande; **PJe**; ritos sumaríssimo
  (ATSum) e ordinário.
- **Cível:** Juizados Especiais Federais e Justiça Federal comum (1º e 2º grau, TRF3). Mesma formatação e
  mesma assinatura da trabalhista.
  `[REVISAR: confirmar se há Justiça Estadual e se há atuação no polo ativo em cível]`

## Regras inegociáveis

1. **Não inventar nada** — jurisprudência, doutrina, número de processo, data, cláusula de ACT ou Id de
   documento. Sem certeza, marcar `[REVISAR: ...]` ou `[INSERIR: ...]` no corpo do texto.
2. Só usar ementas que constem dos autos, do modelo anexado ou do recurso adversário.
3. Listar ao final, separadamente, **o que precisa de conferência humana**: datas de intimação e contagem
   de prazo, cômputo de tempo em função gratificada, Ids e cláusulas, e toda a jurisprudência citada.
4. Não presumir fato ausente dos documentos; divergindo defesa e sentença, apoiar-se na sentença e na capa
   do PJe.
5. **Duas etapas** na mesma conversa: análise estruturada primeiro, minuta depois.
6. **Formatação de qualquer peça: só a da skill `formatar-minuta`** — Arial 11, entrelinha exata de 18 pt,
   margens 3/2/3/2 cm, tópico principal em caixa alta dentro de retângulo, subtópicos numerados em negrito
   sublinhado, cabeçalho/rodapé e assinatura clonados de `modelos/_FORMATO_BASE.docx`. Peça-modelo anexada
   serve para estrutura e tese, **nunca** para formatação.
7. Um processo por conversa.
8. **Ler o índice, não a base inteira** — identificar os pedidos, abrir só as fichas que o
   [INDICE.md](INDICE.md) indicar. Ficha `status: rascunho` é candidata a tese, não tese confirmada.
9. Impugnar especificamente cada fato e cada pedido; nenhum pedido fica sem resposta.

## Onde está o resto

| Preciso de | Vou em |
|---|---|
| Tese de um tema | [INDICE.md](INDICE.md) → `teses/<área>/` |
| Formatação da peça (fonte, margens, tópicos, cabeçalho, rodapé, assinatura) | skill `formatar-minuta` |
| Estrutura da peça por tipo + tema | [modelos/README.md](modelos/README.md) |
| Prompt de análise/redação, nomenclatura do arquivo final | [playbook_prompts_ECT.md](playbook_prompts_ECT.md) |
| Rotinas da sessão (conversão de PDF, título, consolidação) | [CLAUDE.md](CLAUDE.md) |
| O que ainda falta validar na base | [LACUNAS.md](LACUNAS.md) |
