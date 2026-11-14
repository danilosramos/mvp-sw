# Fechou

Jogos com vaga para arenas esportivas. MVP do time no Startup Weekend Araranguá (novembro de 2026).

**Hipótese:** gente sem parceiro vira reserva num horário que a arena não vende.

A arena (ou a equipe, no papel de concierge) abre um horário vago ou um grupo incompleto. O app mostra quem da base combina: mesmo esporte, nível até 1 de diferença e horário que a pessoa marcou no formulário. A equipe convida pelo WhatsApp com a mensagem pronta, e o jogador confirma em um toque, sem conta e sem baixar app. Quando completa, aparece **Fechou! Reserva gerada: R$ X**.

- App: https://danilosramos.github.io/mvp-sw/
- Convite de um jogo: `https://danilosramos.github.io/mvp-sw/#convite-<id>`

## O que é real e o que fica de fora

| Funciona de verdade | Fica de fora no MVP |
|---|---|
| Abrir jogo (horário vago ou grupo incompleto) | Pagamento |
| Quem combina (esporte, nível e horário) | Envio automático de mensagens |
| Convite pelo WhatsApp com mensagem pronta | App nativo, chat e avaliação |
| Confirmação pelo link ou pelo concierge | Integração com o sistema da arena |
| Placar ao vivo e reserva gerada em R$ | |
| Painel só com jogos reais (teste fica fora) | |

## Configurar (uma vez, uns 15 minutos)

### 1. Firebase

1. Entre em https://console.firebase.google.com e crie um projeto (pode desligar o Google Analytics).
2. **Firestore Database** > Criar banco de dados > local `southamerica-east1 (São Paulo)` > modo de produção.
3. Na aba **Regras**, apague o que estiver lá, cole o conteúdo de [`firestore.rules`](firestore.rules) e clique em **Publicar**.
4. **Authentication** > Vamos começar > **E-mail/senha** > Ativar > Salvar. Na aba **Usuários**, clique em **Adicionar usuário** e crie a conta da equipe. Copie o **UID** que aparece na lista.
5. Volte ao **Firestore Database** > Iniciar coleção > ID da coleção `admins` > ID do documento = o UID copiado > um campo `nome` (string) com o seu nome > Salvar. Cada pessoa da equipe precisa de uma conta e de um documento desses.
6. Engrenagem > **Configurações do projeto** > Seus apps > ícone **</>** (Web) > registre o app > copie o objeto `firebaseConfig` e cole os valores em [`config.js`](config.js).

Se você entrar no app antes do passo 5, ele mostra o seu UID com um botão para copiar.

### 2. GitHub Pages

Settings > Pages > Source: **Deploy from a branch** > `main` / `(root)` > Save. Em 1 ou 2 minutos o app fica no ar.

### 3. Primeiro acesso

1. Abra o app e entre com a conta da equipe.
2. **Jogadores** > **Importar lista do formulário (.json)** > escolha o arquivo gerado das respostas do Tally.

O arquivo de jogadores tem nome e WhatsApp de pessoas reais: **nunca suba esse arquivo para este repositório**.

## Como usar

**Equipe (arena ou concierge)**

1. **Abrir jogo com vagas**: horário vago ou grupo incompleto, esporte, nível, dia e hora, vagas e preço da quadra.
2. **Quem combina**: toque em **Convidar** para abrir o WhatsApp com a mensagem pronta.
3. Quem tocar no link confirma sozinho. Quem responder "tô dentro" no WhatsApp, marque em **Confirmou**.
4. Quando completa: **Fechou!** e a reserva entra no painel.

Em demonstrações, marque **Jogo de teste**: ele aparece na lista, mas fica fora dos números do painel.

**Jogador**: abre o link do convite, escreve o nome e toca em **Tô dentro**. Sem conta e sem app.

## Roteiro da demo (40 segundos)

1. Antes: cadastre o colega da plateia em **Jogadores** com o WhatsApp dele (vôlei de praia, nível 3, sábado à tarde ou noite).
2. No palco, ligue **Ocultar nomes**: os nomes reais da base viram apelidos.
3. **Abrir jogo com vagas**: grupo incompleto, vôlei de praia, nível 3, próximo sábado às 18h, preço real, **Jogo de teste**.
4. Aparecem os jogadores reais que combinam. Toque em **Convidar** no colega.
5. Ele toca no link e em **Tô dentro**. No telão: **Fechou! Reserva gerada: R$ X**.

A data do jogo precisa ser futura: um jogo que já passou não aceita confirmação.

## Privacidade

- Só contas da equipe (coleção `admins`) leem os telefones dos jogadores. Quem abre um convite vê o jogo e o primeiro nome de quem confirmou.
- Os valores de `config.js` são públicos por natureza. Quem protege os dados são as regras de `firestore.rules`.

## Arquivos

- `index.html`: o app inteiro (telas, regra de quem combina e mensagens).
- `firebase.js`: liga o app ao Firestore e ao login da equipe.
- `config.js`: configuração do projeto Firebase.
- `firestore.rules`: quem pode ler e escrever o quê.
