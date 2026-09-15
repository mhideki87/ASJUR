# Modelo: Contestação — reintegração pedida contra justa causa apurada em PAD

**Consolidado de:** 1 caso-fonte (Vara do Trabalho na área do TRT24, contestação minutada em 09/2026, ainda **não
julgada**; justa causa por assédio sexual contra jovem aprendiz, empregado em afastamento previdenciário).
**Última atualização:** 2026-09-15 — criação inicial.
**Formatação:** vem de `modelos/_FORMATO_BASE.docx`, pela skill `formatar-minuta`. Sem `.docx` próprio.

---

## Quando usar este modelo

A inicial pede **nulidade da dispensa e reintegração** atacando a apuração feita em processo administrativo
disciplinar, e deduz a nulidade por acumulação de fundamentos subsidiários — estabilidade, ônus da prova,
vícios procedimentais, desproporcionalidade, retaliação —, cada um com um capítulo próprio.

Tese e jurisprudência:
[`teses/trabalhista/justa_causa_pad_assedio.md`](../../teses/trabalhista/justa_causa_pad_assedio.md) e
[`teses/trabalhista/justa_causa_durante_suspensao_contratual.md`](../../teses/trabalhista/justa_causa_durante_suspensao_contratual.md).

## A decisão de arquitetura que este modelo registra

**Espelhar a inicial item a item, e dizer isso no resumo da lide.** A tentação é organizar a defesa pela
lógica da Reclamada — o que é mais elegante e é o que a primeira versão do caso-fonte fez, agrupando
"regularidade do procedimento" num só tópico. O usuário pediu o contrário, e tinha razão: quando a causa de
pedir vem fatiada em seis ou sete alegações de nulidade, **cada uma precisa de subtópico próprio**, porque
alegação sem resposta nominal é alegação que o juiz lê como incontroversa.

O recurso que fecha isso é um **quadro-síntese ao final do resumo da lide**, listando todos os fundamentos
de nulidade da inicial, cada um identificado pelo item da vestibular (II.1, II.2.3…) e remetido ao tópico do
mérito que o impugna. Efeito duplo: o juiz enxerga que nada ficou sem resposta, e a Reclamada se obriga a
não deixar nada sem resposta.

**Cuidado de execução:** o gerador da skill `formatar-minuta` **não monta tabela**. O quadro se faz com o
bloco `>>` (Arial 10, recuo de 4 cm, alinhado à esquerda), uma linha por fundamento.

**Segundo cuidado:** ler o título *e o conteúdo* de cada item da inicial antes de nomear o subtópico. No
caso-fonte, o item II.2.6 ("Da necessidade de produção de provas para apuração da verdade real") tratava de
prova a produzir **em juízo**, e a queixa sobre diligências não apreciadas no recurso administrativo estava
no II.2.5 — a primeira versão trocou os dois, e o subtópico respondia a uma alegação que não existia.

## Estrutura

**Abertura**

1. **Da equiparação à Fazenda Pública e da tempestividade** — art. 12 do DL 509/69, DL 779/69, RE 220.906/DF;
   pedir destacadamente prazo em dobro, dispensa de custas e de depósito recursal, precatório e EC 113/2021.
   Ver [`teses/transversal/prerrogativas_processuais_ect.md`](../../teses/transversal/prerrogativas_processuais_ect.md).
2. **Resumo da vestibular** — admissão, rescisão, objeto do PAD, síntese dos pedidos, estado atual da lide
   (liminar, mandado de segurança, agravo) e **o quadro-síntese** descrito acima.

**Preliminarmente**

3. Prevenção e conexão, se suscitadas.
4. Limitação da condenação aos valores indicados (art. 840, § 1º, da CLT; no TRT24, tese prevalecente nº 13
   do IUJ 0024122-54.2021.5.24.0000).
5. **Inépcia parcial — pedidos sem valor algum.** Não se confunde com a anterior: ali se discute se o valor
   limita; aqui **não há valor**. Fechar a conta do valor da causa declarado na inicial e mostrar que ele
   comporta apenas alguns pedidos; os demais entraram sem valor (art. 840, §§ 1º e 3º, da CLT).

**Mérito — os dois tópicos de base, antes de responder a qualquer alegação**

6. **Da validade da justa causa: o que o PAD apurou** — enquadramento, rito, colegialidade, unanimidade.
7. **Do teor do que foi dirigido à vítima** — transcrição dos trechos, quando o caso a comportar. É o tópico
   que sustenta os demais: a gravidade concreta é o que torna desproporcional a reintegração, não a pena.

**Mérito — um subtópico por alegação, na ordem da inicial**

8. a 18. Estabilidade acidentária · ônus da prova · comprovação específica dos fatos · imediatidade e perdão
    tácito · cadeia de custódia da prova digital · imagens de CFTV · habilitação tardia da assistência
    técnica · **recurso administrativo e seu processamento** · prova requerida em juízo ·
    desproporcionalidade · alocação funcional · motivação retaliatória · plano de saúde · dano moral ·
    honorários · juros e correção.

O tópico do **recurso administrativo** é o que costuma faltar, e é dos mais rendosos — item 7 do MANCOD 1/2,
detalhado na ficha. Responde de uma vez a "a rescisão foi precipitada" e a "as diligências nunca foram
analisadas", e ainda fornece munição ao tópico da imediatidade.

**Fechamento**

19. Impugnação aos documentos e ao valor da causa.
20. Requerimentos, com prequestionamento explícito.

## Texto reaproveitável

- **Abertura de subtópico que espelha a inicial:** *"Sustenta a inicial (item II.2.3) que …"* — nomear o item
  faz o juiz localizar a correspondência sem procurar.
- **Fecho do tópico de proporcionalidade**, quando a vítima é aprendiz: a dimensão que transcende o interesse
  patrimonial — o programa de aprendizagem, as famílias que confiam um adolescente a um orientador designado
  por portaria, e o que a reintegração comunicaria a quem denuncia. Usar uma vez, no fim do tópico, sem
  repetir o registro em outros.
- **Fecho de capítulo de nulidade:** prejuízo é requisito, não consequência (arts. 794 e 796 da CLT; art. 282,
  § 1º, do CPC). Exigir da inicial que diga **o que** teria produzido e **em que** o resultado seria outro.

## O que não fazer

- **Não afirmar fato da fase recursal sem o documento.** Ver o ponto sensível correspondente na ficha: a
  cópia do PAD se encerra na notificação do julgamento.
- **Não organizar o mérito pela lógica da defesa** quando a inicial fatiou a causa de pedir. Ver acima.
- **Não anexar o arquivo da peça a este repositório** — contém dado real de parte.
