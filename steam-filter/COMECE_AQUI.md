# Como abrir o app — passo a passo

Cinco minutos, uma vez só. Depois é sempre duplo clique no `run.bat`.

---

## 1. Traga o código para o seu PC

### Jeito A — sem git, só cliques (recomendado se você não mexe com git)

1. Abra <https://github.com/mhideki87/ASJUR> logado na sua conta.
2. Clique no botão cinza **Code** (fica acima da lista de arquivos, à direita) → **Download ZIP**.
   - Se ainda não mesclou o pull request #2: antes de clicar em *Code*, clique no seletor de branch
     (o botão à esquerda que escreve `main`) e escolha `claude/steam-game-filter-friends-rxo1an`.
     Só então **Code → Download ZIP**.
3. Na pasta Downloads, clique com o botão direito no arquivo `.zip` → **Extrair tudo…** → escolha um lugar
   simples, como `C:\SteamFilter` (evite o Desktop se ele for sincronizado pelo OneDrive).
4. Entre na pasta extraída (o nome é comprido, algo como `ASJUR-claude-steam-game-filter-friends-rxo1an`)
   e depois na pasta **`steam-filter`**. É lá que está o `run.bat`.

> Se ao rodar o `run.bat` o Windows mostrar "O Windows protegeu o seu computador", clique em
> **Mais informações** → **Executar assim mesmo**. Isso aparece porque o arquivo veio da internet.

### Jeito B — com git, mantendo o repositório atualizado

Se você já tem o repositório clonado (é a pasta onde você abre o Claude Code local — a que contém
`CLAUDE.md` e `README.md`), abra o **Prompt de Comando** nela: clique na barra de endereço do Explorador de
Arquivos, escreva `cmd` e aperte Enter. Então:

```bash
git checkout main
git pull
```

Isso traz a pasta `steam-filter` depois que o **pull request #2** estiver mesclado no GitHub. Para testar
antes de mesclar, use a branch direto:

```bash
git fetch origin
git checkout claude/steam-game-filter-friends-rxo1an
```

Mais simples ainda: abra o Claude Code local nessa pasta e peça *"atualize o repositório para a branch
claude/steam-game-filter-friends-rxo1an"*.

## 2. Pegue a sua chave da Steam

1. Abra <https://steamcommunity.com/dev/apikey> (logado na sua conta Steam).
2. Em *Nome de domínio*, escreva qualquer coisa — `localhost` serve.
3. Aceite os termos e clique em **Registrar**.
4. Copie a sequência de letras e números que aparece. **É isso que o app vai pedir.**

## 3. Deixe dois campos do seu perfil como públicos

Na Steam: clique no seu nome → **Perfil** → **Editar perfil** → aba **Privacidade**.

| Campo | Precisa estar |
|---|---|
| Detalhes do jogo | **Público** |
| Lista de amigos | **Público** |

Sem isso a própria Steam recusa a leitura, mesmo sendo a sua conta e a sua chave. Se quiser, depois de
sincronizar você pode voltar tudo para privado — os dados já ficam salvos no seu PC (é só lembrar de
liberar de novo quando for sincronizar outra vez).

## 4. Abra o app

Entre na pasta `steam-filter` no Explorador de Arquivos e dê **duplo clique em `run.bat`**.

- Vai abrir uma janela preta escrevendo "preparando o ambiente" — é normal, só na primeira vez, ~1 minuto.
- Em seguida o navegador abre sozinho em `http://127.0.0.1:8777`.
- **Deixe a janela preta aberta** enquanto estiver usando o app. Para fechar o app: clique nela e aperte
  `Ctrl+C`.

> Se aparecer "NAO ENCONTREI O PYTHON": instale de <https://www.python.org/downloads/> marcando a caixinha
> **"Add python.exe to PATH"** na primeira tela do instalador, e clique no `run.bat` de novo.

## 5. Configure e sincronize (só na primeira vez)

O app abre já pedindo a configuração:

1. **Chave da Steam Web API** → cole o que você copiou no passo 2.
2. **Seu SteamID64 ou URL do perfil** → pode colar a URL mesmo, ex.: `https://steamcommunity.com/id/seunome`.
3. **Salvar**.
4. Clique em **Sincronizar** (canto superior direito) e espere.

A sincronização baixa a sua biblioteca, sua lista de amigos e a biblioteca de cada amigo — é uma consulta
por amigo, então com 100 amigos leva alguns minutos. A barra de progresso mostra em que fase está e você
pode cancelar no meio; o que já veio fica salvo.

Depois disso, filtrar é instantâneo. Você só precisa sincronizar de novo quando quiser atualizar (uma vez
por semana já basta; jogos novos e amigos novos só aparecem depois de sincronizar).

---

## Como usar no dia a dia

### Aba "Minha biblioteca" — o que jogar agora

1. Duplo clique no `run.bat`.
2. Arraste **"Mínimo de amigos com o jogo"** para o número que quiser.
3. Marque **"Contar só amigos online agora"** se a ideia é jogar já.
4. Em **Modo de jogo**, escolha *Co-op online* ou *PvP* conforme a vontade.
5. Não conseguiu decidir? **🎲 Escolher**.
6. **Jogar** abre o jogo direto no cliente Steam.

### Aba "Descobrir na Steam" — o que comprar

1. Clique na aba **Descobrir na Steam**.
2. Monte o pedido na barra da esquerda. Exemplo de um roguelite em promoção para jogar com amigos:
   - *Estilo*: digite `Roguelite` e escolha na lista que aparece
   - *Modo de jogo*: `Co-op online`
   - *Preço*: arraste até `R$ 30` e marque **Só o que está em promoção**
   - *Avaliações*: mínimo de positivas `90%`, mínimo de análises `1.000`
   - *Ordenar por*: `Melhor avaliados (com peso)`
3. Clique em **🔎 Procurar no catálogo** e acompanhe a barrinha. Os resultados vão aparecendo aos poucos:
   o app pega a lista de jogos primeiro e depois busca preço e avaliação de um em um, no ritmo que a loja
   da Steam permite (~200 consultas a cada 5 minutos).
4. Cada card mostra o preço com desconto, o % de avaliações positivas **e quantos amigos seus já têm** —
   clique em **Quem tem** para ver quem.

Se o resultado for grande, o app avisa que alguns jogos ficaram sem preço/avaliação nesta rodada: é só
clicar em **Procurar no catálogo** de novo, que ele continua de onde parou. O que já veio fica em cache e
não é buscado outra vez.

> **Sobre "para X jogadores":** a Steam não publica o número máximo de jogadores em lugar nenhum da API.
> O que funciona é combinar *Modo de jogo* (co-op online, co-op local, PvP) com etiquetas — digite
> `4 Player` no campo *Estilo* para ver as que existem — e o mínimo de amigos que já têm o jogo.

Os filtros ficam salvos — na próxima vez o app abre do jeito que você deixou.

## Se algo der errado

| Sintoma | O que é |
|---|---|
| "Nao consegui ler a SUA biblioteca" | *Detalhes do jogo* ainda não está Público (passo 3). |
| "Sua lista de amigos esta privada" | *Lista de amigos* ainda não está Pública (passo 3). |
| Chave inválida / 403 | A chave foi copiada pela metade, ou você revogou ela na Steam. |
| Muitos jogos com a etiqueta `categoria ?` | Normal no começo: a loja da Steam limita ~200 consultas a cada 5 min. Clique em **continuar detalhes** no rodapé dos filtros, quantas vezes quiser. |
| Amigos aparecem como "biblioteca privada" | É a privacidade **deles**. Não existe jeito de contornar; o app mostra quantos amigos são legíveis para você saber o tamanho do ponto cego. |
| A busca no catálogo não traz nada | Rode o diagnóstico e me mande a saída: abra a pasta `steam-filter`, digite `cmd` na barra de endereço e rode `.venv\Scripts\python -m steam_filter doctor`. Ele testa cada endereço da Steam, um por um, e diz qual falhou. |
| O campo *Estilo* não sugere nada | O app baixa a lista de etiquetas da Steam na primeira vez que você digita. Sem internet no momento, ele avisa embaixo do campo; nesse caso use o campo *Nome contém*. |

Detalhes técnicos, opções avançadas e limitações estão no [README.md](README.md).
