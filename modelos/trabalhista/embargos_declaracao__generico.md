# Modelo: Embargos de Declaração — estrutura geral (qualquer tema)

**Consolidado de:** 1 caso-fonte — embargos contra acórdão de Turma do TRT24 em tema de redução de jornada de
empregado público (caso identificado só pelo tema; nenhum dado de parte ou processo neste arquivo).
**Última atualização:** 26/08/2026 — criação do modelo.

---

## Quando usar este modelo

Embargos de declaração contra **sentença ou acórdão** (art. 897-A da CLT), em qualquer tema. A estrutura
abaixo é independente do tema: o que muda é o conteúdo dos subtópicos do bloco de vícios.

Antes de redigir, aplicar o filtro dos embargos de declaração do `playbook_prompts_ECT.md`: **se não houver vício real, dizer
isso em vez de redigir a peça**. Embargos que rediscutem mérito são protelatórios e custam credibilidade —
e, no caso-fonte, o próprio acórdão havia enfrentado, um a um, todos os argumentos do recurso.

Situações que **justificam** a peça:
- pedido recursal (ainda que sucessivo) que a decisão não apreciou;
- obrigação criada pela própria decisão sem prazo, forma ou consequência definidos — vício que torna
  inexequível justamente o capítulo em que a ECT venceu;
- questão jurídica que precisa de tese explícita para viabilizar recurso de revista (Súmula 297 do TST;
  art. 896, § 1º-A, I, da CLT; art. 1.025 do CPC).

## Estrutura padrão

Formatação: não repetir medidas aqui — o padrão visual (tópico em retângulo, subtópico numerado em negrito
e sublinhado, corpo, citação recuada) vem da skill `formatar-minuta`
(`.claude/skills/formatar-minuta/referencia/especificacao_formatacao.md`).

```
Endereçamento — Relator/Turma do TRT24 (acórdão) ou Juízo da Vara (sentença)
Autos nº / EMBARGANTE / EMBARGADO(A)
Preâmbulo — qualificação da ECT + art. 897-A da CLT c/c arts. 1.022 e 1.025 do CPC

[RETÂNGULO] DA TEMPESTIVIDADE
[RETÂNGULO] DA SÍNTESE DO JULGADO E DA DELIMITAÇÃO DESTES EMBARGOS
[RETÂNGULO] DAS OMISSÕES E OBSCURIDADES
             1 – <um subtópico por vício, na ordem: omissões, depois obscuridades>
             2 – ...
             n – [BLOCO CONDICIONAL] <vício que depende de conferência nos autos>
[RETÂNGULO] DO PREQUESTIONAMENTO
[RETÂNGULO] DOS REQUERIMENTOS
Fecho + assinatura (vêm de modelos/_FORMATO_BASE.docx, clonado pela skill formatar-minuta)
```

- **Tempestividade** — prazo de 5 dias (art. 897-A da CLT), em dias úteis (art. 775 da CLT) e **em dobro**
  (art. 1º, III, do DL 779/69 c/c art. 12 do DL 509/69; STF, RE 220.906/DF). Registrar a dispensa de preparo.
- **Síntese e delimitação** — resumir o decidido e **declarar expressamente o que a peça não faz**: não
  rediscute mérito nem tese vinculante aplicada. É o parágrafo que separa embargos úteis de protelatórios.
- **Omissões e obscuridades** — um subtópico por vício. Ordem sugerida: primeiro os pedidos não apreciados
  (omissão pura, a mais forte), depois o conteúdo indefinido de obrigações criadas na decisão, por fim as
  questões deduzidas para prequestionamento.
- **Prequestionamento** — lista fechada dos dispositivos e teses sobre os quais se pede pronunciamento.
- **Requerimentos** — conhecimento e provimento; efeito modificativo **com pedido expresso** e delimitado;
  prequestionamento pelo art. 1.025 do CPC; registro da interrupção do prazo recursal.

## Linguagem / trechos-padrão reaproveitáveis

- Fórmula de cada vício, em três movimentos: (i) transcrever o trecho exato da decisão (ou registrar o
  silêncio dela); (ii) apontar o que faltou decidir; (iii) enquadrar no dispositivo — art. 1.022, I
  (obscuridade/contradição) ou II (omissão), do CPC, e art. 489, § 1º, IV, do CPC quando a decisão deixou de
  enfrentar argumento capaz de infirmar a conclusão.
- Delimitação: *"A embargante não pretende, por esta via, rediscutir o mérito do julgado nem a tese
  vinculante adotada no voto condutor. Os vícios a seguir apontados dizem respeito, exclusivamente, a ..."*
- Obrigação criada sem consequência: pedir esclarecimento sobre **prazo**, **forma**, **iniciativa** e
  **efeito do descumprimento** — sem os quatro, a obrigação não se cumpre nem se executa.
- Efeito modificativo: art. 897-A, **caput** e § 2º, da CLT — só é possível **com pedido expresso** do
  embargante; formular o pedido delimitado ao que se quer alterar, nunca ao capítulo inteiro.
- Erro material pode ser corrigido de ofício ou a requerimento (art. 897-A, § 1º, da CLT).
- Interrupção do prazo para outros recursos: art. 897-A, § 3º, da CLT.
- Prequestionamento: Súmula 297 do TST; art. 896, § 1º-A, I e III, da CLT; art. 1.025 do CPC.

## Variações observadas

- **Contra sentença** (1º grau): endereçar ao Juízo da Vara, rótulos Reclamante/Reclamada, e a peça
  normalmente acompanha petição de juntada — ver fluxo padrão na seção 2 da base.
- **Contra acórdão**: endereçar ao Relator/Turma, rótulos Embargante/Embargado(a), protocolo direto no 2º grau.
- **Bloco condicional**: quando o vício depende de conferência que só o usuário pode fazer (se determinado
  pedido foi de fato formulado no recurso, se a sentença fixou honorários etc.), manter o subtópico com
  `[REVISAR: ...]` e instrução explícita de **suprimir** o item se a conferência for negativa. Alegar omissão
  sobre pedido que não foi feito é o caminho mais curto para a multa por embargos protelatórios.
- **Decisão que aplica tese vinculante** (IRR/repetitivo): não embargar contra a tese. Embargar apenas o que
  a tese não cobre e o que a decisão deixou indefinido — é o que preserva a transcendência do recurso
  posterior (art. 896-A da CLT).
- **Rito sumaríssimo**: conferir antes o valor da causa (art. 896, § 9º, da CLT limita o recurso de revista a
  ofensa direta à CF ou contrariedade a súmula do TST/vinculante). Isso muda o que vale prequestionar.

## Ligação com a base de teses

- Prerrogativas de prazo e preparo, usadas na tempestividade de qualquer embargo:
  [teses/transversal/prerrogativas_processuais_ect.md](../../teses/transversal/prerrogativas_processuais_ect.md)
- Tema em que este modelo nasceu, e de onde saíram os quatro vícios-padrão:
  [teses/trabalhista/reducao_jornada_dependente_deficiencia.md](../../teses/trabalhista/reducao_jornada_dependente_deficiencia.md)
- Padrão visual: skill `formatar-minuta`; nome do arquivo entregue: skill `nomear-minuta`.

## Par `.docx`

`embargos_declaracao__generico.docx`, ao lado deste arquivo. Gerado a partir de uma peça real aprovada e
**anonimizado**: nome da parte, nº do processo, datas, fls. e todos os fatos do caso foram substituídos por
placeholders entre `[...]`. Preserva integralmente a formatação padrão — a especificada, com as medidas
exatas, na skill `formatar-minuta`
(`.claude/skills/formatar-minuta/referencia/especificacao_formatacao.md`). Não redescreva as medidas aqui:
elas vivem num lugar só, para não divergir.

Como usar: abrir o `.docx`, substituir o texto entre `[...]` e replicar os blocos do tópico
**DAS OMISSÕES E OBSCURIDADES** — um subtópico por vício. Os três parágrafos do item 1 estão marcados como
`[1º movimento]`, `[2º movimento]` e `[3º movimento]` justamente para reproduzir a fórmula em cada vício
novo; apagar essas marcações ao redigir.

O que **não** deve ser apagado: o parágrafo de delimitação (tópico da síntese), o item condicional 4 enquanto
a conferência nos autos não estiver feita, e a advertência do art. 1.026, § 2º, do CPC que o acompanha.
