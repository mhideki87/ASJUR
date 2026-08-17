# ferramentas/

## `converter_documentos.py` — pré-processa a pasta do caso

Converte todos os documentos de uma pasta de caso (PDF, DOCX, planilha, e-mail, HTML…) em
Markdown enxuto. Você anexa o `.md` no lugar do arquivo original e a mesma informação chega ao
Claude gastando uma fração dos tokens — PDF e imagem anexados são processados página por página,
enquanto o texto extraído é só texto.

### Instalação (uma vez)

Com [Python 3.9+](https://www.python.org/downloads/) instalado (marque **"Add python.exe to
PATH"** no instalador):

```bat
pip install pdfplumber python-docx openpyxl python-pptx striprtf
```

Opcionais, conforme o que aparecer na sua pasta:

| Instale | Para |
|---|---|
| `pip install extract-msg` | e-mail `.msg` exportado do Outlook |
| `pip install odfpy` | `.odt` (LibreOffice) |
| `pip install pywin32` | `.doc` antigo (converte usando o Word instalado) |
| `pip install pymupdf pytesseract pillow` + [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) com o idioma `por` | PDF digitalizado e foto/print de documento (`--ocr`) |

O script não quebra se faltar alguma: ele lista no início o que está ausente, com a linha de
`pip install` pronta, e segue convertendo o que consegue.

### Uso

```bat
python converter_documentos.py "F:\Claude\00 caso_atual\Arionaldo Espinoza"
```

Varre também as subpastas e grava tudo em `<pasta do caso>\_convertido`:

| Arquivo gerado | Para que serve |
|---|---|
| `_INDICE.md` | tabela de todos os documentos com páginas, palavras e tokens estimados — abra primeiro para decidir o que anexar |
| um `.md` por documento | anexe só o documento que interessa (o mais econômico) |
| `_CASO_COMPLETO.md` | o caso inteiro em um arquivo, quando precisar do contexto todo |
| `_MANIFESTO.json` | controle interno: na segunda execução só converte o que mudou |

Cada página vira um marcador `[p.3]` no texto, então continua sendo possível citar a folha
correta na peça.

### Opções

| Opção | Efeito |
|---|---|
| `--ocr` | tenta OCR nas páginas de PDF sem texto e nas imagens (mais lento; exige Tesseract) |
| `--anonimizar` | mascara CPF, CNPJ e número de processo na saída |
| `--forcar` | reconverte tudo, ignorando o cache |
| `--sem-reflow` | preserva as quebras de linha originais (mantém o layout, gasta mais token) |
| `--sem-consolidado` | não gera o `_CASO_COMPLETO.md` |
| `--max-linhas-tabela N` | limite de linhas por tabela/planilha (padrão: 300) |
| `-s PASTA` | grava a saída em outro lugar |
| `--silencioso` | imprime menos |

### O que a limpeza remove

Só o que gasta token sem informar: cabeçalho e rodapé repetidos em toda página, número de página
e "Fls. N" isolados, tarja de assinatura eletrônica e hash de validação do PJe, linha de
separação, espaço em excesso, hifenização de fim de linha e quebra de linha no meio da frase.
O conteúdo jurídico não é resumido nem reescrito — nenhum trecho é interpretado pelo script.

### Conferência

Ao terminar, olhe a seção **"Revisar manualmente"** do `_INDICE.md`: ela lista os documentos de
que não saiu texto — normalmente PDF digitalizado (rode de novo com `--ocr`) ou `.doc` antigo
(abra e salve como `.docx`). Antes de usar a saída em uma peça, confira no original os trechos que
você for citar.

### Regra permanente

A saída contém nome de parte, CPF e número de autos. **Não comite `_convertido/` neste
repositório** — o `.gitignore` da raiz já bloqueia, mas a pasta do caso deve continuar fora do
repositório de todo modo.
