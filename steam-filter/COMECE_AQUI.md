# Como abrir o app — passo a passo

Cinco minutos, uma vez só. Depois é sempre duplo clique no `run.bat`.

---

## 1. Traga o código para o seu PC

No Claude Code local (ou no terminal, dentro da pasta do repositório):

```bash
git checkout main
git pull
```

Isso só funciona depois que o **pull request #2** estiver aprovado e mesclado no GitHub. Se preferir testar
antes de mesclar, use a branch direto:

```bash
git fetch origin
git checkout claude/steam-game-filter-friends-rxo1an
```

Você vai passar a ter a pasta `steam-filter` dentro do repositório.

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

1. Duplo clique no `run.bat`.
2. Arraste **"Mínimo de amigos com o jogo"** para o número que quiser.
3. Marque **"Contar só amigos online agora"** se a ideia é jogar já.
4. Em **Modo de jogo**, escolha *Co-op online* ou *PvP* conforme a vontade.
5. Não conseguiu decidir? **🎲 Escolher por mim**.
6. **Jogar** abre o jogo direto no cliente Steam.

Os filtros ficam salvos — na próxima vez o app abre do jeito que você deixou.

## Se algo der errado

| Sintoma | O que é |
|---|---|
| "Nao consegui ler a SUA biblioteca" | *Detalhes do jogo* ainda não está Público (passo 3). |
| "Sua lista de amigos esta privada" | *Lista de amigos* ainda não está Pública (passo 3). |
| Chave inválida / 403 | A chave foi copiada pela metade, ou você revogou ela na Steam. |
| Muitos jogos com a etiqueta `categoria ?` | Normal no começo: a loja da Steam limita ~200 consultas a cada 5 min. Clique em **continuar detalhes** no rodapé dos filtros, quantas vezes quiser. |
| Amigos aparecem como "biblioteca privada" | É a privacidade **deles**. Não existe jeito de contornar; o app mostra quantos amigos são legíveis para você saber o tamanho do ponto cego. |

Detalhes técnicos, opções avançadas e limitações estão no [README.md](README.md).
