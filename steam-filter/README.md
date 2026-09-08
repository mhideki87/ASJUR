# Steam Game Filter

App local que sincroniza com a sua conta Steam e responde a duas perguntas:

- **"o que a gente joga agora?"** — filtra a sua biblioteca pela quantidade de amigos que têm cada jogo,
  inclusive só os que estão **online agora**;
- **"o que eu compro?"** — procura no catálogo inteiro da Steam por estilo (etiqueta), modo de jogo,
  **preço, promoção e avaliação** — e mostra, em cada resultado, quantos amigos seus já têm aquele jogo.

![filtro por nº de amigos](docs/screenshot.png)

![busca no catálogo por etiqueta, preço e avaliação](docs/screenshot-descobrir.png)

## Por que essa arquitetura (a resposta curta)

| Decisão | Por quê |
|---|---|
| **Web app rodando na sua máquina** (`http://127.0.0.1:8777`), não site hospedado nem app de celular | A Steam Web API **não permite chamada direta do navegador** (sem CORS) e a chave de API **não pode ir para o front-end** — precisa de um servidor. Um servidor local resolve isso sem hospedagem, sem custo e sem sua chave sair do seu PC. |
| **Chave da Web API + SteamID**, sem "login com Steam" | Para uso pessoal, OpenID só adicionaria um fluxo de autenticação sem dar nenhum dado a mais: tudo que o app lê (biblioteca, amigos, jogos dos amigos) vem da Web API com a sua chave. |
| **Cache em SQLite** (`data/steam.db`) | Ler a biblioteca de N amigos é 1 requisição por amigo. Sem cache, cada filtro custaria minutos; com cache, filtrar é instantâneo e você só sincroniza quando quiser. |
| **Python + FastAPI**, front-end em HTML/JS puro | Zero build step: `pip install` e roda. Você já usa Python 3.12 neste repositório. |
| Categorias (co-op/PvP) vindas da **API pública da loja**, com cache permanente | É a única fonte que diz se o jogo é multiplayer. Ela limita ~200 consultas a cada 5 min, então o app busca em fila, prioriza os jogos com mais amigos e **nunca rebusca** o que já tem. |
| Descoberta = **busca da loja** para achar candidatos + **endpoints JSON oficiais** para os dados | Só a busca da loja sabe filtrar por etiqueta ("Roguelite") e promoção; ela devolve HTML, do qual o app extrai **apenas o identificador de cada jogo**. Preço, categorias e avaliações vêm depois de endpoints JSON oficiais. Assim uma mudança no visual da loja não quebra nada. |

> **Primeira vez? Siga o [COMECE_AQUI.md](COMECE_AQUI.md)** — passo a passo, sem jargão.

## Requisitos

- Python 3.10 ou superior
- Uma chave da Steam Web API: <https://steamcommunity.com/dev/apikey> (grátis, pede só um domínio qualquer)
- No **seu** perfil Steam → *Editar perfil* → *Privacidade*: **Lista de amigos** e **Detalhes do jogo** em
  **Público**. A chave de API respeita a privacidade, mesmo sendo a sua conta.

## Instalação e uso

### Windows (jeito rápido)

```bat
run.bat
```

Cria o ambiente virtual, instala as dependências, sobe o app e abre o navegador.

### Qualquer sistema

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt     # Windows: .venv\Scripts\pip
.venv/bin/python -m steam_filter               # sobe em http://127.0.0.1:8777
```

Na primeira execução, a tela de **Configurar** pede a chave da API e o seu SteamID64 (ou a URL do seu
perfil — o app resolve o vanity name). Depois é só clicar em **Sincronizar**.

Prefere não usar a tela? Copie `.env.example` para `.env` e preencha `STEAM_API_KEY` e `STEAM_ID`.

Sincronizar pelo terminal, sem abrir a interface:

```bash
.venv/bin/python -m steam_filter sync            # tudo
.venv/bin/python -m steam_filter sync --mode details   # só continua a fila de categorias da loja
```

## As duas abas

### Minha biblioteca

O que você (e seus amigos) já têm.

- **Nº de amigos que têm o jogo** e **nº de amigos online agora** que têm o jogo
- Biblioteca: só os meus · meus + dos amigos · que algum amigo tem · que eu não tenho
- Amigos que jogaram nas últimas 2 semanas · jogos que eu nunca joguei

### Descobrir na Steam

O catálogo inteiro da loja. Clique em **🔎 Procurar no catálogo** e o app traz os jogos que batem com os
critérios da barra lateral, já cruzados com a sua rede de amigos.

> Exemplo do que dá para pedir: *roguelite, co-op online, até R$ 30, em promoção, com pelo menos 90% de
> avaliações positivas e mais de mil análises, que pelo menos 2 amigos meus já tenham.*

### Filtros comuns às duas (é o mesmo painel — ele filtra o que você tem **e** guia a busca)

| Grupo | Filtros |
|---|---|
| Estilo | etiqueta da Steam com autocompletar (Roguelite, Soulslike, Deckbuilder…), gênero, nome |
| Modo de jogo | multiplayer, co-op, co-op online, co-op local/tela dividida, PvP, Remote Play Together |
| Amigos | mínimo de amigos com o jogo, só amigos online agora, quem jogou nas últimas 2 semanas |
| Preço | preço máximo, só em promoção, desconto mínimo, incluir ou não jogos gratuitos |
| Avaliações | % mínimo de positivas, número mínimo de análises |
| Ordenação | amigos · amigos online · **melhor avaliados (com peso)** · % positivas · maior desconto · mais baratos · lançamento · horas jogadas · Metacritic · nome |

**"Melhor avaliados (com peso)"** usa o limite inferior do intervalo de Wilson em vez do percentual cru:
um jogo com 100% de 3 análises não passa na frente de um com 95% de 200 mil. Ordenar por "% de avaliações
positivas" continua disponível, para quando você quiser justamente o percentual bruto.

**🎲 Escolher** sorteia entre os jogos que passaram no filtro. **Quem tem** lista os amigos donos do jogo,
quem está online e quantas horas cada um tem. Os filtros ficam salvos no navegador; **Jogar** abre o jogo
direto pelo cliente Steam (`steam://run/<id>`).

### Sobre "para X jogadores"

A API da Steam **não expõe o número máximo de jogadores** de um jogo — esse dado simplesmente não existe
nos endpoints públicos. O que dá para fazer, e o app faz:

- filtrar por **modo de jogo** (co-op online, co-op local/tela dividida, PvP), que vem das categorias
  oficiais e é exato;
- filtrar por **etiqueta**, incluindo as que a comunidade usa para isso — digite `4 Player` no campo
  *Estilo* e o autocompletar mostra o que a Steam realmente tem;
- exigir um **mínimo de amigos que já têm o jogo**, que na prática é a pergunta que importa quando o grupo
  tem N pessoas.

## Como funciona a sincronização

1. `ISteamUser/ResolveVanityURL` + `GetPlayerSummaries` → confirma quem é você
2. `IPlayerService/GetOwnedGames` → sua biblioteca
3. `ISteamUser/GetFriendList` → seus amigos
4. `GetOwnedGames` para **cada** amigo (em paralelo, com controle de taxa) → é isto que gera a contagem
5. `store.steampowered.com/api/appdetails` → categorias (multiplayer/co-op/PvP), em fila e com cache

Tudo é gravado em `data/steam.db`. Sincronizar de novo atualiza; não duplica. Dá para cancelar no meio —
o que já veio fica salvo.

## Como funciona a busca no catálogo

1. `store.steampowered.com/search/results` com etiqueta, preço e promoção → **quais** jogos batem
   (o app lê só o identificador de cada linha do resultado)
2. `api/appdetails` de cada jogo novo → preço, desconto, categorias, gêneros
3. `appreviews` de cada jogo novo → total de análises e quantas são positivas

Os passos 2 e 3 respeitam o limite da loja e só rodam para o que ainda não está em cache: repetir a mesma
busca depois é instantâneo. Cada busca enriquece até 60 jogos por vez (ajustável em *Configurar → Ajustes
avançados*); se o resultado for maior, o app avisa e basta rodar de novo para completar.

## Limitações (são da Steam, não do app)

- **Amigo com "Detalhes do jogo" privado não pode ser contado.** Não existe endpoint que contorne isso.
  A barra lateral e o painel **Amigos** mostram quantos amigos são legíveis, para você saber o tamanho do
  ponto cego.
- A API da loja limita ~200 consultas a cada 5 minutos. Por isso as categorias vêm aos poucos: os jogos
  ainda sem categoria aparecem marcados com `categoria ?` e continuam entrando nos filtros de modo de jogo
  (a menos que você desmarque *"Incluir jogos sem categoria baixada"*). Use **continuar detalhes** no
  rodapé dos filtros para seguir de onde parou.
- Amigos "online agora" é consultado ao vivo, com cache de 45 s. Se a Steam não responder, o app continua
  funcionando com os dados em cache — só não mostra o status online.

## Estrutura

```
steam-filter/
├── run.bat / run.ps1            atalho para Windows
├── requirements.txt
├── .env.example
├── steam_filter/
│   ├── __main__.py              CLI: serve | sync
│   ├── config.py                chave, SteamID e ajustes (env > .env > data/config.json)
│   ├── steam_api.py             cliente assíncrono: rate limit, retry, perfis privados
│   ├── db.py                    schema SQLite + classificação das categorias
│   ├── sync.py                  orquestração da sincronização, com progresso e cancelamento
│   ├── discover.py              busca no catálogo: etiqueta/preço/promoção + preço e avaliações
│   ├── doctor.py                diagnóstico de cada endpoint externo
│   ├── queries.py               as consultas que fazem a filtragem
│   ├── server.py                API HTTP (FastAPI)
│   └── web/                     interface (HTML/CSS/JS, sem build)
└── tests/test_smoke.py          teste ponta a ponta com a Steam falsificada
```

## Quando alguma coisa não funcionar

```bash
.venv/bin/python -m steam_filter doctor
```

Bate uma vez em cada endpoint externo — seu SteamID, sua biblioteca, sua lista de amigos, preço,
avaliações, catálogo de etiquetas e busca da loja — e diz qual falhou e por quê. Os endpoints da loja não
são documentados formalmente pela Valve; se a Valve mudar algum, é este comando que aponta qual.

## Testes

```bash
.venv/bin/python tests/test_smoke.py
```

Sobe uma Steam falsa (`httpx.MockTransport`) e confere, sem tocar a rede: a sincronização inteira, a
contagem de amigos, cada filtro (amigos, modo de jogo, preço, promoção, avaliação, etiqueta), o ranking
com peso, o cache da loja, a detecção de perfil privado, a migração de um banco da versão anterior e todos
os endpoints HTTP.

## Privacidade

A chave da API e o banco ficam só em `data/` (fora do Git, junto com `.env` e `.venv`). Nada é enviado
para lugar nenhum além da própria Steam.
