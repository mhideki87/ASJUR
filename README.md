# ASJUR — Sistema de automação para a Assessoria Jurídica

Sistema de apoio à redação, formatação e organização jurisprudencial para o
contencioso trabalhista da Assessoria Jurídica da ECT, construído como um
**Projeto Claude**: um conjunto de arquivos de conhecimento + prompts padronizados
que você usa dentro do claude.ai (ou app Claude), sem necessidade de código ou
infraestrutura própria.

## Mapa dos arquivos

| Arquivo | Para que serve |
|---|---|
| `base_conhecimento_juridico_ECT.md` | Quem você é, o que produz, teses recorrentes da ECT, padrão formal das peças e regras de trabalho. É a espinha dorsal do sistema. |
| `playbook_prompts_ECT.md` | Prompts prontos: análise de inicial/sentença/RO, redação de cada tipo de peça, revisão pré-protocolo, teste da tese adversa, checklist de anexos. |
| `banco_teses_jurisprudencia.md` | Registro vivo dos precedentes e súmulas já usados e verificados, com status de vigência — evita repetir jurisprudência desatualizada ou já superada. |
| `checklist_formatacao_pecas.md` | Especificação do padrão formal (fonte, margens, cabeçalho etc.) e passo a passo para gerar/converter peças em .docx/.odt sem perder a formatação do modelo. |
| `banco_pecas_indice.md` | Catálogo de peças já produzidas (só metadados — tipo, tema, rito, local do arquivo real) para localizar rapidamente uma peça-modelo equivalente antes de redigir do zero. **Os arquivos reais ficam fora deste repositório** (ver seção "Banco de peças" abaixo). |
| `instrucoes_personalizadas_projeto.md` | Texto pronto para colar no campo "Instruções personalizadas" do Projeto Claude — amarra todos os arquivos acima em regras de comportamento. |

## Como montar o Projeto (uma vez)

1. Crie um Projeto no claude.ai (ou app), por exemplo **"Contencioso Trabalhista ECT"**.
2. Cole o conteúdo de `instrucoes_personalizadas_projeto.md` no campo
   **"Instruções personalizadas"** do Projeto.
3. Suba como **"Conhecimento do projeto"**:
   - `base_conhecimento_juridico_ECT.md`
   - `playbook_prompts_ECT.md`
   - `banco_teses_jurisprudencia.md`
   - `checklist_formatacao_pecas.md`
   - `banco_pecas_indice.md`
4. Pronto — toda conversa nova dentro do Projeto já herda essas regras e essa base.

## Banco de peças (modelos e busca primária)

Além da base de conhecimento e do banco de teses, o sistema mantém um
**catálogo de peças já produzidas**, para servir de modelo de formatação e de
busca primária ("já fiz algo parecido com isso?") antes de redigir do zero.

Por conter dado de parte, número de processo e, em doença ocupacional, dado
de saúde (LGPD), **os arquivos reais das peças não entram neste repositório
Git** — só o índice de metadados (`banco_pecas_indice.md`) fica aqui. Os
arquivos reais ficam:

- no acervo local do escritório, organizado por tipo de peça (estrutura de
  pastas sugerida na seção 2 de `banco_pecas_indice.md`); e/ou
- subidos diretamente como "Conhecimento do Projeto" no claude.ai (fora do
  Git, mas dentro do ambiente do Projeto).

Fluxo: antes de redigir, você (ou o Claude, se o índice estiver subido)
consulta o catálogo por tipo/tema/rito; se existir peça equivalente, você
localiza o arquivo real no acervo e anexa na conversa como modelo. Peças
antigas são importadas aos poucos com o **prompt de catalogação** (seção 5 de
`banco_pecas_indice.md`), que extrai só os metadados sem expor dado sensível.

## Fluxo de trabalho por processo (repita a cada caso)

1. Abra uma **conversa nova dentro do Projeto** (um processo por conversa — nunca misture autos).
2. Rode a **busca de peça-modelo equivalente** (prompt 0.1 do playbook) no `banco_pecas_indice.md` — se existir peça parecida, localize-a no acervo.
3. Anexe os documentos do processo conforme o checklist de anexos (seção 5 do playbook): inicial, sentença, contestação anterior, laudos, peça-modelo (a localizada no passo 2, ou outra), ACT vigente, conforme o tipo de peça.
4. Rode o prompt de **análise** correspondente (1.1, 1.2 ou 1.3 do playbook). Não pule esta etapa.
5. Rode o prompt de **redação** (2.1 a 2.6), citando o `<MODELO.odt/.docx>` anexado.
6. Rode a **revisão pré-protocolo** (prompt 3.1) e, se quiser, o **teste da tese adversa** (3.2).
7. Rode o **checklist de formatação** (`checklist_formatacao_pecas.md`, seções 4 e 5) antes de converter/salvar o arquivo final.
8. Confira manualmente **tudo que foi listado como `[REVISAR]`** — isso nunca é opcional.
9. Se usou jurisprudência nova, **atualize `banco_teses_jurisprudencia.md`**; cadastre a peça no `banco_pecas_indice.md` usando o prompt de catalogação — ambos depois de protocolar.

## O que este sistema não faz (por enquanto)

- Não integra com o PJe (sem robô de peticionamento nem leitura automática de intimações).
- Não controla prazos automaticamente — é preciso um sistema de agenda/prazos à parte.
- Não gera .odt diretamente a partir de uma conversa comum — ver a limitação técnica descrita em `checklist_formatacao_pecas.md` (seção 1) e o caminho de contorno (gerar em .docx e converter).
- Depende de você anexar os documentos certos em cada conversa — não há leitura automática de processo.

## Possíveis evoluções futuras

- Automação real (script/serviço) para monitorar publicações/intimações e alertar prazos.
- Extração automática de dados estruturados de PDFs de inicial/sentença.
- Geração de minutas em lote via API, para processos com o mesmo padrão fático (ex.: mesma tese, múltiplos reclamantes).

## Lacunas a preencher (ver também a seção 7 da base de conhecimento)

- [ ] Estrutura da equipe e distribuição de processos
- [ ] Volume mensal e prazos internos de entrega
- [ ] Outras áreas além da trabalhista (cível, consumidor?)
- [ ] Orientações da Consultoria Jurídica nacional da ECT que vinculam a defesa local
- [ ] Teses que a ECT decidiu *não* sustentar
- [ ] Importar retroativamente o acervo de peças antigas para `banco_pecas_indice.md` (ver seção "Banco de peças" acima)
