# Índice do banco de peças — ECT / Contencioso Trabalhista

> Complemento da `base_conhecimento_juridico_ECT.md` e do
> `banco_teses_jurisprudencia.md`.
> Objetivo: permitir que o Claude use peças já produzidas como **modelo de
> formatação/estrutura** e como **fonte de busca primária** ("já existe algo
> parecido a isso?") antes de redigir do zero — sem que dado de parte ou
> processo entre neste repositório Git.

---

## 1. Por que os arquivos reais NÃO ficam neste repositório

Peças trabalhistas contêm nome de parte, número de processo e, em casos de
doença ocupacional, **dado sensível de saúde** (CID, diagnóstico) — dados
protegidos pela LGPD. Mesmo em repositório privado, versionamento em Git
mantém histórico permanente e amplia desnecessariamente a superfície de
exposição desses dados.

Por isso, a divisão de responsabilidade é:

| O quê | Onde fica |
|---|---|
| **Arquivos reais** (.odt/.docx das peças) | Fora do Git — acervo local do escritório e/ou "Conhecimento do Projeto" no claude.ai (ver seção 2) |
| **Índice/catálogo** (este arquivo) | Neste repositório — só metadados, sem nome completo de parte |
| **Peça anexada numa conversa** | Sempre feito manualmente por você, a partir do acervo local, nunca versionado aqui |

**Regra ao preencher a tabela da seção 4:** nunca coloque nome completo da
parte. Use apenas o número do processo (se a ação não tiver segredo de
justiça — trabalhista em regra é pública) ou, em caso de sigilo, apenas o
**ID interno** deste índice.

---

## 2. Estrutura sugerida do acervo real (fora do Git)

Organize os arquivos reais em pastas por tipo de peça, seguindo a
nomenclatura já definida na base de conhecimento (seção 6):

```
BancoDePecas/                        (pasta local, ou upload direto no Projeto Claude)
├── Contestacoes/
├── ContrarazoesRO/
├── RecursoDeRevista/
├── EmbargosDeclaracao/
├── Quesitos_PericiaMedica/
├── Quesitos_PericiaTecnica/
└── Manifestacoes/
```

Nome de arquivo dentro de cada pasta, conforme padrão já existente:
`Tipo - Tema abreviado - Rito - NOME DA PARTE.odt`

Se o volume crescer, subdivida por ano (`Contestacoes/2026/...`).

**Uso como Conhecimento do Projeto:** o claude.ai permite subir os arquivos
reais diretamente como "Conhecimento do projeto" (não passam pelo Git). Isso
é o mais prático para consulta rápida, mas fique atento ao limite de arquivos/
tamanho do Projeto — para acervos grandes, prefira manter localmente e anexar
a peça específica na conversa quando for usá-la como modelo.

---

## 3. Como isso vira "busca primária"

Fluxo ao iniciar uma peça nova (ver também `playbook_prompts_ECT.md`):

1. Antes de redigir do zero, **consulte a tabela da seção 4** (ou peça ao
   Claude para consultar, se este índice estiver subido como conhecimento do
   Projeto) filtrando por Tipo + Tema + Rito.
2. Se existir peça equivalente, localize o arquivo real no acervo (seção 2)
   pelo ID/nome e **anexe-o na conversa** como `<MODELO>` — reaproveita
   estrutura, formatação e, quando cabível, argumentação já validada.
3. Se não existir nada parecido, redija do zero (fluxo normal do playbook) e,
   depois de protocolada, **cadastre a peça nova** na tabela (seção 4) usando
   o prompt de catalogação (seção 5).

---

## 4. Índice de peças

| ID | Tipo | Tema/tese principal | Rito | Data | Sigiloso? | Nº do processo | Local do arquivo real | Teses/precedentes (ref.) | Resultado | Obs. |
|---|---|---|---|---|---|---|---|---|---|---|
| _(cadastrar ao importar o acervo)_ | | | | | | | | | | |

Colunas:
- **ID** — sequencial (P001, P002...), usado como referência quando o processo é sigiloso.
- **Tema/tese principal** — usar os nomes das seções de `banco_teses_jurisprudencia.md` quando possível, para cruzar os dois índices.
- **Local do arquivo real** — caminho da pasta local (seção 2) ou "Conhecimento do Projeto Claude".
- **Teses/precedentes (ref.)** — remeter à seção correspondente de `banco_teses_jurisprudencia.md`.

---

## 5. Prompt de catalogação (para importar peças antigas)

Use este prompt numa conversa com a peça real anexada — **a resposta do
Claude não deve reproduzir nome completo da parte**, apenas os metadados
necessários para colar na tabela da seção 4:

```
Leia a peça anexada e extraia os metadados para catalogação no banco de
peças. NÃO reproduza o nome completo da parte na sua resposta — se precisar
diferenciar, use apenas iniciais. Devolva uma linha pronta para colar na
tabela de banco_pecas_indice.md:

| Tipo | Tema/tese principal | Rito | Data | Sigiloso? (S/N) | Nº do processo (omitir se sigiloso) | Teses/precedentes usados | Resultado (se constar) | Obs. |

Também sugira o nome de arquivo para o acervo local, seguindo o padrão
"Tipo - Tema abreviado - Rito - NOME DA PARTE.odt" (o nome da parte você
mesmo preenche depois, fora desta conversa, direto no nome do arquivo local).
```

Depois de gerar a linha, você:
1. Atribui o próximo ID sequencial.
2. Cola a linha na tabela da seção 4 (removendo qualquer dado sensível residual).
3. Move/renomeia o arquivo real para a pasta correspondente do acervo (seção 2).

---

## Lacunas deste índice (preencher)

- [ ] Importar retroativamente o acervo existente (peças antigas indicadas por você)
- [ ] Decidir se o acervo real fica local ou como Conhecimento do Projeto Claude
- [ ] Confirmar quais processos antigos correm em segredo de justiça, para tratamento diferenciado no índice
