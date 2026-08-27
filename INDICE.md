# Índice da base de conhecimento — roteamento por tema

> **Objetivo:** não ler a base inteira. Ler este índice (curto), descobrir o objeto da demanda, e abrir
> **somente** as fichas de tese correspondentes.

## Como usar (protocolo de leitura)

1. **Sempre:** ler [CONTEXTO.md](CONTEXTO.md) — perfil, padrão formal e regras inegociáveis. É o único
   arquivo lido por inteiro em toda sessão.
2. **Identificar o objeto:** ler a inicial/sentença/recurso do processo e listar os **pedidos**.
3. **Rotear:** para cada pedido, procurar o gatilho na tabela abaixo e abrir a **ficha** indicada.
   Nenhum gatilho bateu → dizer isso explicitamente e tratar como **tema novo** (ver "Tema novo" abaixo);
   não forçar o encaixe numa ficha existente.
4. **Só então** abrir o `modelo de peça` da linha, se houver, e o
   [playbook_prompts_ECT.md](playbook_prompts_ECT.md) na seção do tipo de peça.
5. Fichas com status **rascunho** são **candidatas a tese**, não teses confirmadas: validar contra o
   processo em mãos antes de usar, e nunca citar como jurisprudência pronta.

Não abrir ficha "por precaução": cada ficha aberta é custo de contexto. Em caso de dúvida entre duas,
abrir a mais específica primeiro.

## Tabela de roteamento

<!-- TABELA-GERADA:INICIO -->

<!-- Gerado por scripts/atualizar_indice.py a partir dos metadados das fichas. Não editar à mão: edite a ficha e rode o script. -->

| Área | Tema | Gatilhos (o que procurar no objeto da demanda) | Ficha | Modelo de peça | Status |
|---|---|---|---|---|---|
| Trabalhista | **Afastamentos (atestado médico / auxílio-doença)** | afastamento · atestado médico · auxílio-doença · suspensão do contrato · 15 dias · art. 476 CLT · FGTS em afastamento · lacuna previdenciária · CNIS · vale-alimentação descontado · dobra de férias · art. 137 CLT · Medicina do Trabalho · desconto em folha | [`afastamentos_auxilio_doenca.md`](teses/trabalhista/afastamentos_auxilio_doenca.md) | [`contestacao__afastamentos.md`](modelos/trabalhista/contestacao__afastamentos.md) | validada |
| Trabalhista | **Doença ocupacional** | doença ocupacional · acidente de trabalho · nexo causal · concausa · incapacidade · perícia médica · NTEP · CNAE · espécie 91 · espécie 31 · PCMSO · riscos psicossociais · danos morais por doença · pensionamento · LER · DORT · transtorno psiquiátrico | [`doenca_ocupacional.md`](teses/trabalhista/doenca_ocupacional.md) | — | validada |
| Trabalhista | **Incorporação de gratificação de função** | incorporação de gratificação · gratificação de função · FAT · FAO · ITF · GPTF · Módulo 55 · Módulo 36 · MANPES · Súmula 372 · Súmula 51 · reversão ao cargo efetivo · destituição de função · direito adquirido · Tema 23 | [`incorporacao_gratificacao_funcao.md`](teses/trabalhista/incorporacao_gratificacao_funcao.md) | [`contestacao__incorporacao_funcao.md`](modelos/trabalhista/contestacao__incorporacao_funcao.md) | validada |
| Trabalhista | **Prescrição total** | prescrição · prescrição total · Súmula 294 · art. 11 CLT · prejudicial de mérito · alteração do pactuado · prestação sucessiva | [`prescricao.md`](teses/trabalhista/prescricao.md) | [`contestacao__incorporacao_funcao.md`](modelos/trabalhista/contestacao__incorporacao_funcao.md) | validada |
| Trabalhista | **Temas acessórios (ad cautelam)** | quebra de caixa · substituição · reajuste de ACT · acordo coletivo · CIP · POSTALIS · previdência privada · honorários advocatícios · art. 791-A · normativos internos · PLR | [`temas_acessorios.md`](teses/trabalhista/temas_acessorios.md) | [`contestacao__incorporacao_funcao.md`](modelos/trabalhista/contestacao__incorporacao_funcao.md) | validada |
| Cível | **Ações indenizatórias — falha no serviço postal** | extravio · encomenda · SEDEX · PAC · atraso na entrega · dano moral · declaração de valor · avaria · violação de objeto · fraude em venda pela internet · ilegitimidade ativa · CDC art. 14 · Lei 6.538/78 · Juizado Especial Federal | [`indenizatoria_servico_postal.md`](teses/civel/indenizatoria_servico_postal.md) | — | **rascunho** |
| Cível | **Despacho postal e objeto tributado (importação)** | despacho postal · objeto tributado · importação · tributo aduaneiro · Receita Federal · NJ-416/2014 · MANCAT · MANINT · Convenção Postal Universal · UPU · retenção de objeto internacional | [`despacho_postal_objeto_tributado.md`](teses/civel/despacho_postal_objeto_tributado.md) | — | **rascunho** |
| Cível | **Panorama do acervo cível (levantamento estatístico)** | panorama cível · volume de processos cível · tipos de peça cível · acervo · estatística do acervo | [`panorama_acervo_civel.md`](teses/civel/panorama_acervo_civel.md) | — | **rascunho** |
| Transversal | **Prerrogativas processuais da ECT (equiparação à Fazenda Pública)** | prazo em dobro · Decreto-lei 779/69 · Decreto-lei 509/69 · equiparação à Fazenda Pública · dispensa de preparo · dispensa de custas · tempestividade · empresa pública · juros e correção contra a Fazenda · tutela antecipada contra a Fazenda | [`prerrogativas_processuais_ect.md`](teses/transversal/prerrogativas_processuais_ect.md) | [`contestacao__incorporacao_funcao.md`](modelos/trabalhista/contestacao__incorporacao_funcao.md)<br>[`contestacao__afastamentos.md`](modelos/trabalhista/contestacao__afastamentos.md) | validada |

<!-- TABELA-GERADA:FIM -->

## Sempre aplicável, independentemente do objeto

- **Prerrogativas processuais da ECT** (prazo em dobro, dispensa de preparo, equiparação à Fazenda
  Pública): [teses/transversal/prerrogativas_processuais_ect.md](teses/transversal/prerrogativas_processuais_ect.md)
  — entra em praticamente toda peça; conferir a tempestividade antes de qualquer coisa.
- **Prescrição** na trabalhista, sempre que houver parcela de norma interna revogada:
  [teses/trabalhista/prescricao.md](teses/trabalhista/prescricao.md)

## Formatação e estrutura da peça (não são teses)

| Preciso de | Vou em |
|---|---|
| Formatação visual de qualquer peça (fonte, cabeçalho, rodapé, assinatura) | [modelos/_FORMATO_BASE.docx](modelos/) — ver [modelos/README.md](modelos/README.md) |
| Esqueleto/estrutura de um tipo de peça + tema | `modelos/<área>/<tipo_peca>__<tema>.md` (coluna "Modelo de peça" da tabela) |
| Prompt pronto para análise ou redação | [playbook_prompts_ECT.md](playbook_prompts_ECT.md) |
| Regra de conversão de PDF/DOC do processo para `.md` | [CLAUDE.md](CLAUDE.md) |

## Tema novo (nenhum gatilho bateu)

1. Analisar e minutar normalmente, a partir dos autos — sem inventar tese para preencher o vazio.
2. Ao final da sessão, rodar o protocolo da seção 6.2 do [playbook](playbook_prompts_ECT.md): a proposta
   deve incluir a **criação de uma ficha nova** a partir de [teses/_TEMPLATE_TESE.md](teses/_TEMPLATE_TESE.md).
3. Depois de criar ou editar qualquer ficha, regenerar esta tabela:

```bash
python scripts/atualizar_indice.py           # reescreve a tabela acima
python scripts/atualizar_indice.py --check   # só confere se está em sincronia
```

Como manter as fichas (formato dos metadados, o que vai em cada seção): [teses/README.md](teses/README.md).
