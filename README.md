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

## Como está configurado

- **Firebase:** projeto `fechou-sw`, Firestore em `southamerica-east1` (São Paulo), com as regras de [`firestore.rules`](firestore.rules) publicadas.
- **Login da equipe:** Google. O domínio `danilosramos.github.io` está nos domínios autorizados do Firebase.
- **[`config.js`](config.js)** já aponta para o projeto.

### Colocar alguém no time

1. No rodapé do painel, toque em **Copiar convite para o time** e mande no grupo. A mensagem tem o link e o código do time.
2. A pessoa abre o link, toca em **Entrar com Google** e digita o código.

Se o código vazar, toque em **Trocar código**: o antigo para de funcionar para novas entradas. Quem já entrou continua no time; para tirar alguém, apague o documento dela na coleção `admins` do Firestore.

### Primeiro acesso

**Jogadores** > **Importar lista do formulário (.json)** > arquivo gerado das respostas do Tally.

O arquivo de jogadores tem nome e WhatsApp de pessoas reais: **nunca suba esse arquivo para este repositório**.

### Recriar do zero, em outro projeto Firebase

1. Crie um projeto em https://console.firebase.google.com.
2. **Firestore Database** > Criar banco de dados > São Paulo > modo de produção. Na aba **Regras**, cole `firestore.rules` e publique.
3. **Authentication** > Método de login > **Google** > Ativar. Em Configurações > **Domínios autorizados**, adicione o domínio do GitHub Pages.
4. **Configurações do projeto** > Seus apps > **Web (</>)** > copie o `firebaseConfig` para `config.js`.
5. No GitHub: Settings > Pages > **Deploy from a branch** > `main` / `(root)`.

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
