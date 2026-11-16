# Requisitos da Energia Boa (MVP do Startup Weekend)

O app se chamava Fechou até 15/11/2026. "Fechou!" continua sendo o estado do jogo completo.

Hipótese que o MVP testa: **gente sem parceiro vira reserva num horário que a arena não vende.**
Cada requisito abaixo existe para gerar essa evidência. O resto fica no roadmap, com o motivo.

## Agora no MVP

### R1. Perfil de jogador

- Entrar com Google. No primeiro acesso, a pessoa preenche nome, cidade, esportes que pratica, nível no esporte principal (Iniciante, Intermediário ou Avançado, sem números), quando pode jogar (7 faixas) e WhatsApp (opcional).
- "Quero ser chamado para jogos que combinam comigo" só vale com WhatsApp, e só o time vê o número.
- Editável em **Perfil**, onde aparece o plano atual (Free).
- **Aceite:** sem perfil a pessoa não marca jogo; outro jogador não consegue ler o perfil de ninguém (regra do banco).

### R2. Marcar jogo (evento)

- Campos: esporte, nível, dia e hora, arena, cidade, jogadores no total e quantos já são, preço da quadra (opcional) e WhatsApp de quem organiza (opcional).
- "Quantos já são" cobre os dois casos: **1** é quem está sozinho procurando gente; **2 ou mais** é grupo incompleto. O app mostra quantos faltam.
- Visibilidade: **Público no app** (aparece em Jogos abertos) ou **Privado** (só quem tem o link, para os grupos da pessoa).
- O formulário já vem com o esporte, o nível, a cidade e o WhatsApp do perfil.
- **Aceite:** não aceita horário que já passou nem jogo sem vaga; o link sai pronto para o WhatsApp.

### R3. Compartilhar e fazer check-in

- Cada jogo tem um link. Quem abre vê esporte, nível, dia, local, quem organiza, quantas vagas faltam e o primeiro nome de quem já confirmou.
- Check-in (**Tô dentro**) sem conta, só com o nome. Logado, o nome vem do perfil e o jogo aparece em **Vou jogar**.
- Depois do check-in, um botão abre o WhatsApp de quem organizou, se informado.
- Quem marcou vê os confirmados ao vivo, adiciona quem respondeu no WhatsApp e pode apagar o jogo. Quando completa: **Fechou! Reserva gerada**.

### R4. Procurar jogos, com filtros

- Lista de jogos públicos e futuros. Jogos de teste não aparecem.
- **Procurar** é o primeiro destino da navegação e o botão amarelo no início e em Meus jogos (uma mentora não achou o antigo "Abertos").
- À vista: esporte, **dia da semana** (seg a dom, mais de um) e **período do dia** (manhã 5h–12h, tarde 12h–18h, noite a partir das 18h).
- Em "Mais filtros": quando (qualquer data, hoje, amanhã, próximos 7 ou 30 dias), cidade, nível (mesmo nível) e local (arena ou quadra pública), e só com vaga. A cidade do perfil vem marcada.
- O que está filtrado aparece numa frase, com "Limpar filtros".
- Abre sem login, para quem recebeu um convite conhecer outros jogos.

### R4b. Níveis

- Três níveis com nome: **Iniciante** (começou agora ou joga por diversão), **Intermediário** (joga toda semana) e **Avançado** (joga torneio ou dá aula).
- O banco guarda número (1, 3 e 5), então as regras do Firestore não mudaram. Respostas antigas de 1 a 5 continuam valendo: 1 e 2 contam como iniciante, 3 como intermediário, 4 e 5 como avançado.
- **Quem combina:** mesmo nível e horário que a pessoa marcou. Nível vizinho ou outro horário aparece como "quase". Iniciante e avançado não se cruzam.

### R5. Time da arena (concierge)

- Entra com o código do time. Vê todos os jogos, públicos e privados, com quem marcou.
- **Quem combina** junta a base do formulário e os perfis do app que aceitaram convite, por esporte, nível (regra em R4b), horário e cidade. O convite sai pronto no WhatsApp.
- Painel: reservas geradas (R$), jogos que fecharam, vagas preenchidas, jogadores na base, jogos abertos e lista de espera do Premium. Jogo de teste fica fora dos números.

### R6. Premium como lista de espera

- Página **Energia Boa Premium (em breve)** com os benefícios planejados e o botão **Quero o Premium**. Ninguém é cobrado.
- O painel do time mostra quantos pediram: é a evidência de interesse em pagar.

## Requisitos não funcionais

- Celular primeiro: abre em qualquer navegador, sem instalar nada.
- Privacidade: telefones da base e dos perfis só para o time. O WhatsApp de quem organiza aparece para quem tem o link do jogo, com aviso no formulário.
- Dados ao vivo: placar e listas atualizam sozinhos.
- Números honestos: só dados reais; jogo de teste fica fora da conta.

## Roadmap: fora do MVP, e por quê

| Item | Por que espera |
|---|---|
| Prioridade de 15 minutos para Premium | Com poucos usuários, segurar o jogo 15 minutos atrasa o preenchimento, justamente a dor que a Energia Boa resolve. Ligar quando houver volume de jogos por cidade. |
| Pontuação 1,2x para Premium | Depende de um sistema de pontos e ranking que ainda não existe. |
| Cobrança do Premium e pagamento da quadra | Primeiro validar interesse (lista de espera) e preço. |
| Chat, avaliação depois do jogo, perfil de professor, notificação, app nativo | Não ajudam a provar a hipótese neste fim de semana. |

## Requisitos acrescentados em 15/11/2026

- **R7. Tipo de local.** Todo jogo é em arena ou em quadra pública. Quadra pública não tem preço nem reserva, e o app diz isso. "Jogos abertos" filtra por tipo.
- **R8. Conta em jogo público.** Para entrar em jogo público é preciso estar logado. Jogo privado por link aceita só o nome.
- **R9. Contato protegido.** O WhatsApp de quem organiza só aparece para quem entrou no jogo com conta.
- **R10. Jogo parecido.** Ao marcar no mesmo esporte, lugar e horário (até 1 hora) de um jogo aberto, o app oferece entrar nele.
- **R11. App instalável.** Instala na tela inicial, abre sem internet com aviso, e atualiza quando a pessoa aceita.
- **R12. Privacidade e segurança.** Página com o que é guardado, quem vê o quê, direitos, regra de 18+ e dicas para jogar com desconhecidos. O app não usa GPS.
- **Honestidade:** a Energia Boa não reserva quadra nem cobra. Nenhuma tela diz o contrário.
