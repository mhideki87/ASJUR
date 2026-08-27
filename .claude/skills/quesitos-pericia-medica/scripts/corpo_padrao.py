# -*- coding: utf-8 -*-
"""Corpo padrão dos quesitos de perícia médica — versão aprovada pelo usuário.

Estrutura fixa (não reorganizar sem pedido expresso):
    preâmbulo (3 parágrafos) → quesitos corridos, numerados → DOS REQUERIMENTOS (retângulo)

Os textos entre [colchetes] são os pontos que mudam de caso a caso e PRECISAM ser
substituídos pelos fatos concretos dos autos. Quesitos cujos fatos não existirem no
processo devem ser removidos, não preenchidos com suposição.

Uso:
    from corpo_padrao import montar_corpo
    corpo = montar_corpo(sintese="...", quesitos_extra=[...], remover={7})
"""

# ------------------------------------------------------------------ preâmbulo

PREAMBULO = [
    ("P", "[SÍNTESE DA DEMANDA — função, data de admissão, eventos e patologias "
          "imputados, pedidos deduzidos.]"),
    ("P", "Requer-se, desde já, que o(a) Sr(a). Perito(a) indique expressamente, ao "
          "responder cada quesito, a fonte objetiva de sua conclusão – exame clínico, "
          "documento médico contemporâneo aos fatos, exame complementar ou prontuário –, "
          "discriminando o que decorre de constatação técnica e o que decorre do mero "
          "relato unilateral do periciando, cuja narrativa se encontra expressamente "
          "impugnada nestes autos."),
    ("P", "Requer, ainda, que as respostas sejam apresentadas de forma discriminada, uma "
          "a uma, sendo insuficiente a remissão genérica ao corpo do laudo, sob pena de "
          "nulidade por deficiência de fundamentação."),
]

# ------------------------------------------------------------------ quesitos
# (tipo, texto) — "Q" numera sozinho; "A" é alínea do quesito anterior.

QUESITOS = [
    # 1 — diagnóstico + metodologia embutida
    ("Q", "Queira o(a) Sr(a) Perito(a) esclarecer o diagnóstico atual, com a respectiva "
          "codificação na CID-10, de cada patologia constatada [SEGMENTOS ACOMETIDOS], "
          "dizendo se a conclusão decorre de achado clínico ou de imagem objetivamente "
          "verificado por V. Sa. ou apenas do relato subjetivo do periciando, apontando "
          "expressamente eventuais divergências entre o que foi relatado e o que foi "
          "constatado ao exame? Para cada uma delas, queira o(a) Sr(a). Perito(a) "
          "classificar, se for o caso, a natureza — traumática aguda, degenerativa, "
          "constitucional, inflamatória ou mista — e estimar o tempo mínimo de evolução "
          "compatível com os achados encontrados."),

    # 2 — achados degenerativos dos exames do próprio autor (alíneas por exame)
    ("Q", "A respeito dos achados degenerativos documentados nos exames juntados pelo "
          "próprio Reclamante, queira o(a) Sr(a). Perito(a) esclarecer:"),
    ("A", "a) [EXAME E DATA] descreve “[TRANSCRIÇÃO LITERAL DO ACHADO DEGENERATIVO]”. "
          "[PERGUNTA QUE OPÕE O ACHADO À TESE DE ORIGEM TRAUMÁTICA — p. ex.: é "
          "medicamente possível que essa alteração se instale em menos de 24 horas, ou "
          "traduz, necessariamente, condição preexistente ao sinistro?]"),
    ("A", "b) [EXAME E DATA] traz como dado clínico “[TRANSCRIÇÃO]” e conclui por "
          "“[TRANSCRIÇÃO]”. Tais achados são compatíveis com um evento traumático único "
          "ocorrido em [DATA DO EVENTO], ou correspondem a processo degenerativo crônico "
          "de instalação lenta e progressiva? Qual o tempo estimado de evolução desses "
          "achados?"),
    ("A", "c) [EXAME E DATA] aponta “[TRANSCRIÇÃO]”. Trata-se de achados de natureza "
          "degenerativa e condral, próprios da evolução articular natural, ou de lesão "
          "traumática?"),

    # 3 — incapacidade
    ("Q", "Existe, na data do exame pericial, incapacidade laborativa? Em caso "
          "afirmativo, queira classificá-la quanto à extensão (total ou parcial) e quanto "
          "à duração (temporária ou permanente), esclarecendo se a eventual incapacidade "
          "é específica para a função de [FUNÇÃO] ou se alcança toda e qualquer atividade "
          "laborativa; se parcial, indicar o percentual e o critério de aferição. "
          "Considerando que o Reclamante [SITUAÇÃO FUNCIONAL ATUAL — p. ex.: permanece em "
          "plena atividade, na mesma função, sem qualquer afastamento previdenciário "
          "desde DATA, percebendo remuneração integral e progressões de carreira], tal "
          "realidade é tecnicamente compatível com incapacidade laborativa permanente? As "
          "altas previdenciárias de [DATAS] traduzem recuperação da capacidade para o "
          "trabalho?"),

    # 4 — dano funcional sem repercussão laborativa
    ("Q", "Ainda que constatadas alterações anatômicas nos exames de imagem, elas "
          "repercutem efetivamente na capacidade laborativa do Reclamante, ou se está "
          "diante de dano funcional ou redução de capacidade funcional sem repercussão na "
          "capacidade de trabalho, na dicção do art. 104, § 4º, I, do Decreto nº "
          "3.048/99? Existe, hoje, restrição médica formal em vigor? Há necessidade "
          "técnica de readaptação funcional e, em caso positivo, desde quando e por qual "
          "fundamento clínico?"),

    # 5 — sucesso do tratamento e prova objetiva da sequela
    ("Q", "[EXAME MAIS RECENTE E DATA] descreve “[TRANSCRIÇÃO DOS ACHADOS FAVORÁVEIS]”. "
          "Queira o(a) Sr(a). Perito(a) informar se o tratamento [CIRÚRGICO/CONSERVADOR] a "
          "que se submeteu o Reclamante resultou em consolidação anatômica e funcional "
          "satisfatória e se remanesce sequela funcional objetivamente mensurável — "
          "indicando, em caso positivo, amplitude de movimento, força muscular, perimetria "
          "e os testes objetivos que a demonstrem, e não apenas a queixa referida."),

    # 6 — anamnese e fatores extralaborais
    ("Q", "Queira o(a) Sr(a). Perito(a) colher e registrar anamnese ocupacional e de vida "
          "pregressa completa, informando: idade, peso, altura e índice de massa corporal; "
          "tabagismo e etilismo; prática desportiva atual e pregressa; atividades "
          "domésticas, de lazer ou informais com sobrecarga de [SEGMENTOS EM LINGUAGEM "
          "CORRENTE]; [FATOR "
          "EXTRALABORAL ESPECÍFICO DA FUNÇÃO — p. ex.: condução habitual de motocicleta ou "
          "de veículo próprio fora da jornada]; antecedentes heredofamiliares de doença "
          "degenerativa osteoarticular; e a existência de vínculos empregatícios, "
          "atividades autônomas ou militares anteriores ou concomitantes à admissão em "
          "[DATA DE ADMISSÃO]. Qual a contribuição de cada um desses fatores extralaborais "
          "para o quadro clínico atual?"),

    # 7 — exclusão legal do art. 20, §1º, "a"
    ("Q", "As patologias diagnosticadas enquadram-se no conceito de doença degenerativa ou "
          "de doença inerente a grupo etário, expressamente excluídas do rol das doenças "
          "do trabalho pelo art. 20, § 1º, alínea “a”, da Lei nº 8.213/91? Elas constam "
          "das Listas A ou B do Anexo II do Decreto nº 3.048/99 como patologias associadas "
          "à atividade de [ATIVIDADE]? A literatura médico-científica reconhece que "
          "[PATOLOGIAS] têm etiologia multifatorial, com participação relevante de fatores "
          "constitucionais, etários e de hábitos de vida?"),

    # 8 — nexo individualizado por evento
    ("Q", "Queira o(a) Sr(a). Perito(a), individualizando os eventos, esclarecer, quanto a "
          "cada um dos [Nº] acidentes narrados — [LISTA: DATA (SEGMENTO)]: (i) qual lesão "
          "dele efetivamente decorreu; (ii) se essa lesão está consolidada e desde quando; "
          "e (iii) se a alteração hoje encontrada naquele segmento corresponde à sequela do "
          "trauma ou à evolução do processo degenerativo próprio identificado nos exames de "
          "imagem. Existe, no caso, doença ocupacional autônoma — de natureza osteomuscular "
          "relacionada ao trabalho, com quadro clínico próprio e evolução característica —, "
          "ou o que há são sequelas de eventos traumáticos isolados, sem caráter de doença "
          "profissional ou do trabalho? Do ponto de vista técnico, há elementos objetivos "
          "que demonstrem que o retorno ao trabalho após as altas previdenciárias tenha "
          "agravado as lesões, ou tal agravamento é mera conjectura?"),

    # 9 — prova previdenciária, NTEP e ciência inequívoca
    ("Q", "Considerando que a inicial não instrui os autos com extrato CNIS ou carta de "
          "concessão, queira o(a) Sr(a). Perito(a), à vista da documentação previdenciária "
          "que vier a ser juntada, informar a espécie dos benefícios concedidos nos "
          "períodos de [PERÍODOS DE AFASTAMENTO] — auxílio-doença comum (espécie 31) ou "
          "auxílio-doença acidentário (espécie 91). Havendo invocação de Nexo Técnico "
          "Epidemiológico, queira esclarecer se os elementos clínicos e de imagem "
          "concretamente constatados neste caso afastam a presunção relativa do art. 21-A "
          "da Lei nº 8.213/91. Por fim, queira indicar a data de início da incapacidade e a "
          "data em que o Reclamante teve ciência inequívoca da lesão e de sua extensão."),

    # 10 — tratamento futuro não coberto pelo plano
    ("Q", "Queira o(a) Sr(a). Perito(a) informar se há tratamento futuro necessário que não "
          "esteja coberto pelo plano de saúde mantido pela empregadora, discriminando-o e "
          "estimando seu custo."),

    # 11 — concausa quantificada e tabela objetiva
    ("Q", "Na hipótese de o(a) Sr(a). Perito(a) reconhecer alguma participação do trabalho "
          "no quadro clínico, queira esclarecer se o labor atuou como causa única ou como "
          "concausa e, nesta última hipótese, quantificar percentualmente a participação "
          "dos fatores laborais e dos fatores extralaborais (degenerativos, constitucionais, "
          "etários e de hábitos de vida) na gênese e no agravamento de cada patologia, "
          "explicitando o critério técnico adotado. Requer-se, ainda, que eventual perda "
          "funcional seja aferida por tabela objetiva de valoração do dano corporal, com "
          "indicação do percentual de comprometimento por segmento acometido — [SEGMENTOS] "
          "—, vedada a atribuição de percentual global de incapacidade sem discriminação de "
          "origem."),

    # 12 — capacidade residual
    ("Q", "Persistindo alguma limitação, queira o(a) Sr(a). Perito(a) descrever a capacidade "
          "laborativa residual do Reclamante: quais atividades ele pode exercer sem risco de "
          "agravamento; se pode permanecer na função de [FUNÇÃO], com ou sem restrição; se é "
          "apto a outras funções compatíveis existentes na estrutura da Reclamada; qual o "
          "tempo estimado de tratamento e o prognóstico de reversibilidade do quadro; e se "
          "as sequelas comprometem, e em que grau, a realização das atividades da vida "
          "diária e independente."),
]

# ------------------------------------------------------------------ requerimentos

REQUERIMENTOS = [
    ("T", "DOS REQUERIMENTOS"),
    ("P", "Ante o exposto, a Reclamada requer:"),
    ("A", "a) sejam os presentes quesitos deferidos e respondidos, um a um, de forma "
          "individualizada e tecnicamente fundamentada;"),
    ("A", "b) a juntada do laudo com a antecedência do art. 477 do CPC, abrindo-se prazo "
          "para manifestação e para eventual pedido de esclarecimentos;"),
    ("A", "c) a reserva do direito de apresentar quesitos suplementares no curso da "
          "diligência, na forma do art. 469 do CPC."),
]


def montar_corpo(sintese=None, dados=None, remover=(), quesitos_extra=()):
    """Devolve o corpo pronto para `montar_peca.montar`.

    sintese        — texto do 1º parágrafo do preâmbulo (substitui o placeholder).
    dados          — {"FUNÇÃO": "carteiro motorizado", ...}: cada chave substitui o
                     placeholder "[CHAVE]" em todos os quesitos. Aceita-se também a
                     chave já entre colchetes. Placeholder não preenchido sobrevive e
                     faz `montar_peca.montar` recusar a peça — é a rede de segurança
                     contra entregar quesito genérico.
    remover        — números de quesito (1-based, na ordem final) a suprimir por não
                     terem suporte fático nos autos; as alíneas do quesito saem junto.
    quesitos_extra — [(tipo, texto)] acrescentados ao fim dos quesitos.
    """
    def preencher(texto):
        for chave, valor in (dados or {}).items():
            k = chave if chave.startswith("[") else "[" + chave + "]"
            texto = texto.replace(k, str(valor))
        return texto

    corpo = [(t, preencher(x)) for t, x in PREAMBULO]
    if sintese:
        corpo[0] = ("P", sintese)

    n, pulado = 0, False
    for tipo, texto in QUESITOS:
        texto = preencher(texto)
        if tipo == "Q":
            n += 1
            pulado = n in remover
            if not pulado:
                corpo.append((tipo, texto))
        elif not pulado:           # alínea acompanha o quesito a que pertence
            corpo.append((tipo, texto))
    corpo.extend(quesitos_extra)
    corpo.extend(REQUERIMENTOS)
    return corpo
