# -*- coding: utf-8 -*-
"""Regera modelos/_FORMATO_BASE.docx a partir de uma peça real aprovada.
O corpo vira um catálogo dos sete papéis de parágrafo, para que o template
carregue fisicamente todos os estilos — e não apenas um placeholder."""
import os, sys, zipfile, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from peca_fmt import hdr, p, box, sub, cit, alinea, travessao, vazio, fecho, montar

ORIGEM = os.environ.get("ASJUR_PECA_REFERENCIA", "peca_referencia.docx")  # peça real: doa cabeçalho, rodapé, estilos, logotipo
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "modelos", "_FORMATO_BASE.docx")

X = []
A = X.append

A(hdr([("EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DO TRABALHO DA [Nº]ª VARA DO "
        "TRABALHO DE [CIDADE]/MS.", "b")]))
A(vazio(2))
A(hdr([("Autos nº [Nº DO PROCESSO].", "b")]))
A(hdr([("RECLAMANTE: ", "b"), ("[NOME DA PARTE].", "")]))
A(hdr([("RECLAMADA: ", "b"), ("EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS.", "")]))
A(vazio(2))

A(p([("EMPRESA BRASILEIRA DE CORREIOS E TELÉGRAFOS – SUPERINTENDÊNCIA ESTADUAL DE MATO GROSSO DO SUL", "b"),
     (", Empresa Pública Federal, instituída pelo Decreto-Lei nº 509/69, com sede na Avenida Calógeras "
      "nº 2.309, centro, Campo Grande/MS, telefone (67) 2109-1004, nos autos da ", ""),
     ("RECLAMAÇÃO TRABALHISTA", "b"), (" em epígrafe, que lhe move ", ""),
     ("[NOME DA PARTE]", "b"),
     (", por meio do procurador que esta subscreve, vem, respeitosamente, à presença de Vossa Excelência, "
      "com fundamento em ", ""),
     ("[FUNDAMENTAÇÃO LEGAL DE ADMISSIBILIDADE]", "b"), (", apresentar ", ""),
     ("[TIPO DE PEÇA]", "b"), (", pelos motivos de fato e de direito que seguem.", "")]))

A(box("[TÍTULO DO TÓPICO PRINCIPAL]"))
A(p([("Tópico principal: retângulo de borda simples de 0,75 pt nos quatro lados, parágrafo "
      "centralizado, texto em negrito e sem sublinhado. Use-o apenas nas grandes divisões da peça — "
      "PRELIMINARMENTE, DO MÉRITO, DO PREQUESTIONAMENTO, DOS REQUERIMENTOS.", "")]))
A(p([("Corpo: recuo de primeira linha de 3 cm, justificado, Arial 11 e entrelinha exata de 1,5. É o "
      "parágrafo padrão da peça, e este mesmo é um exemplar dele.", "")]))

A(sub("1 – [TÍTULO DO SUBTÓPICO]"))
A(p([("Subtópico: numeração arábica seguida de travessão, recuo de bloco de 3 cm (sem recuo de primeira "
      "linha), em negrito e sublinhado. Numere na sequência dentro de cada tópico principal.", "")]))
A(p([("A citação de lei, súmula, ementa ou trecho de decisão vem em bloco recuado, ", ""),
     ("verbis", "i"), (":", "")]))
A(cit("Citação em bloco: recuo esquerdo de 3 cm, corpo reduzido para 10 pt, itálico e entrelinha "
      "menor que a do corpo. A referência do julgado vem ao final, entre parênteses e em negrito."))
A(p([("Listas dentro do corpo usam travessão, com recuo de 3,6 cm e pendente de 0,6 cm:", "")]))
A(travessao("primeiro item da lista;"))
A(travessao("segundo item da lista."))

A(box("DOS REQUERIMENTOS"))
A(p("Ante todo o exposto, requer a Reclamada:"))
A(alinea("a)", [("as alíneas do rol de requerimentos usam o mesmo bloco de 3 cm do subtópico, com a "
                 "letra em negrito e o texto em redondo;", "")]))
A(alinea("b)", [("uma alínea por requerimento, na ordem em que as teses foram desenvolvidas;", "")]))
A(alinea("c)", [("expressões de destaque, como ", ""), ("AD CAUTELAM", "b"),
                 (", ficam em negrito dentro da própria alínea.", "")]))
A(fecho())

montar(X, DESTINO, base=ORIGEM)

# limpa metadados residuais da peça de origem
z = zipfile.ZipFile(DESTINO); partes = {n: z.read(n) for n in z.namelist()}; z.close()
core = partes["docProps/core.xml"].decode()
core = re.sub(r"<cp:revision>\d+</cp:revision>", "<cp:revision>1</cp:revision>", core)
partes["docProps/core.xml"] = core.encode()
with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED) as zo:
    for n, d in partes.items():
        zo.writestr(n, d)
print("gerado:", DESTINO)
