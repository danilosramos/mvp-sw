# PRD: alterações indicadas na auditoria do Energia Boa

Data: 16/11/2026. Origem: `AUDITORIA-COMPLETA.md`. Os códigos entre parênteses (S1, N2, D3, C4, F5, M1) são os achados daquela auditoria.

**Como foi feito.** Quatro especialistas (produto e negócio, segurança, engenharia, design e crescimento) escreveram os requisitos da sua área; este documento junta os quatro, resolve os conflitos entre eles e ordena as entregas. Um revisor independente conferiu o resultado contra o código.

**O que este documento não é.** Nada aqui foi implementado. Os trechos de regra do apêndice B não foram executados.

---

## 1. Resumo

O MVP prova que um jogo completa. Não prova que o jogo aconteceu, que a arena vendeu um horário que não venderia, nem que ela pagaria por isso. E as regras do banco confiam demais no aplicativo. Este PRD fecha essas distâncias sem acrescentar servidor.

O que muda:

- **As regras do banco passam a mandar.** Data do servidor, faixas de valor e nível, jogo privado acessível só por link, confirmações dentro do jogo.
- **O jogo passa a ter história.** Cancelar e desistir viram estados com data, em vez de exclusão. Quem organiza marca quem compareceu.
- **O número mostrado à arena passa a ser defensável.** Conta só jogos realizados, com preço confirmado pelo time, em arena parceira identificada.
- **O piloto passa a testar a receita.** A oferta declara o preço seguinte aos 30 dias grátis e registra o aceite.
- **Quem organiza ganha controle.** Corrige o jogo, cancela com aviso, chama o próximo da lista de espera.
- **As costuras do funil são consertadas.** O destino "Marcar jogo" sobrevive ao login, o convite aberto dentro do WhatsApp ganha saída, e o erro aparece junto do campo.
- **O produto para de prometer o que não tem.** Premium, prova social e documentos são alinhados ao que existe.

São 71 requisitos em duas fases, mais o escopo da Fase 3. A **Fase 1** é o que precisa estar pronto antes de divulgar para mais gente e não exige migração de dados. A **Fase 2** é o que o piloto com arenas exige e inclui uma migração.

---

## 2. Objetivos, métricas e o que não é objetivo

### Objetivos

1. Fechar as falhas de autorização que expõem o WhatsApp de quem organiza e permitem furar a fila.
2. Tornar verificável o evento "jogo fechado e realizado em horário que a arena declarou vazio".
3. Testar, no piloto, se a arena aceita pagar por esse evento.
4. Preservar o histórico necessário para medir preenchimento, presença e retorno do jogador.
5. Dar a quem organiza os meios de corrigir, cancelar e repor vaga sem depender do time.
6. Alinhar o que o produto promete ao que ele faz.

### Métricas de sucesso

| Métrica | Alvo | Origem do alvo | Requisitos que a tornam mensurável |
|---|---|---|---|
| Arenas que aceitam por escrito o preço pós-piloto | Pelo menos 2 "sim" em 10 ofertas | `ESTRATEGIA.md:140` | E7, J5 |
| Comparecimento dos confirmados | No máximo 1 falta a cada 4 | `ESTRATEGIA.md:141` | J2 |
| Jogadores com segundo jogo em 14 dias | Pelo menos 1 em 4 | `ESTRATEGIA.md:143` | I1, I3, J7 |
| Jogos fechados por semana (a principal) | A definir pelo time | `ESTRATEGIA.md:129`, sem alvo | J1, J7 |
| Taxa de preenchimento (fechados sobre marcados) | A definir pelo time | sem alvo | I1, J1, J7 |
| Tempo entre marcar e fechar | A definir pelo time | sem alvo | B1, J1 |
| Horários vazios preenchidos, por arena | A definir pelo time | sem alvo | J3, J4 |
| Conversão do convite (abertura até confirmação), por origem | A definir pelo time | sem alvo | G1, G2 |
| Casos de ataque negados pelos testes das regras | 100% dos casos do apêndice B | este PRD | A5 |

### O que não é objetivo nas fases 1 e 2

- Cobrar dentro do aplicativo (pagamento, Pix, assinatura).
- Reservar quadra ou integrar com o sistema da arena.
- Aviso automático (push, e-mail ou WhatsApp por servidor).
- Lançar o Premium do jogador, ranking ou pontos.
- Verificar identidade ou idade.
- Aumentar o volume de usuários antes de a Fase 1 estar concluída.

---

## 3. Usuários e cenários

| Usuário | Antes | Depois |
|---|---|---|
| **Jogador convidado** | Abre o convite público dentro do WhatsApp e o login pode falhar. Se o jogo é apagado, vê "Convite não encontrado". Na lista de espera, só descobre a vaga com a tela aberta. | Vê "Abrir no navegador" antes do login. Se o jogo é cancelado, o convite continua abrindo e diz isso. Se abrir vaga, quem organiza o chama com mensagem pronta. Adiciona o jogo ao calendário. |
| **Quem organiza** | Errou a hora e precisa apagar e recriar, perdendo as confirmações. Não tem como avisar o cancelamento nem chamar o próximo da fila. | Corrige hora, local, total e preço. Cancela com mensagem pronta para o grupo. Vê o próximo da fila com o botão de avisar. Depois do horário, marca quem foi. Marca de novo para a semana seguinte em um toque. |
| **Time** | O painel mostra um total que qualquer conta pode inflar, com jogos que talvez não tenham acontecido. Não sabe de onde vêm os usuários. | O painel mostra, por semana e por arena parceira, jogos realizados com preço confirmado. Vê a origem de cada confirmação. Exporta os números. Remove alguém do time pelo app. |
| **Arena** | Recebe "piloto de 30 dias, grátis", sem saber quanto custará depois nem o que será contado. | Recebe a oferta com o preço seguinte e a definição do que conta. Declara os horários vazios e recebe um número que consegue conferir. |

---

## 4. Restrições e premissas

- **Hospedagem estática.** O aplicativo continua sendo arquivos estáticos, sem servidor próprio, sem Cloud Functions e sem etapa de build obrigatória.
- **Ferramentas de desenvolvimento são permitidas.** `package.json`, emulador do Firebase e GitHub Actions entram só para testar e publicar.
- **Toda garantia fica em `firestore.rules`.** O que a regra não impõe é só conveniência de tela.
- **Não há trabalho agendado.** Todo campo é gravado por um aparelho em uso.
- **Fuso.** O texto `quando` é horário local sem fuso (`index.html:396`). A conversão para data assume o fuso de Brasília.
- **Versões antigas em circulação.** O service worker busca a rede primeiro, então a versão antiga só sobrevive em aba aberta ou sem internet. Mesmo assim, toda mudança de regra segue o padrão "ampliar a regra, publicar o aplicativo, restringir a regra".
- **Escala do piloto.** Dezenas a poucas centenas de jogos, no plano gratuito do Firestore.
- **Endereço oficial.** Precisa estar decidido antes de C1, E9 e da Fase 2 (decisão 6).

---

## 5. Requisitos da Fase 1

Antes de divulgar para mais gente. Não exige migração de documentos. Esforço: P = horas, M = um ou dois dias, G = uma semana ou mais.

### A. Testes e publicação confiáveis

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| A1 | Os testes de ponta a ponta usam datas relativas ao dia da execução, reaproveitando a função `quando()` do backend simulado. | `tests/e2e.py` passa com o relógio do navegador em hoje, daqui a 30 dias e daqui a um ano. Nenhuma data literal resta em `tests/`. | `tests/e2e.py:48`, `123`, `188`; `tests/mock-backend.js:114`, `119`, `124` | S4 | P |
| A2 | Os três scripts de teste terminam com código de saída diferente de zero quando algo falha, com verificações explícitas no lugar de impressões. | Quebrar de propósito um seletor em `index.html` faz `e2e.py` sair com código 1. | `tests/` | S12 | P |
| A3 | Um fluxo do GitHub Actions roda contraste, ponta a ponta, PWA e testes das regras a cada envio. A publicação no GitHub Pages passa a ser feita por esse fluxo, só depois de os testes passarem, e publica apenas os arquivos do aplicativo. | Um envio com teste quebrado não é publicado. Os arquivos `.md`, `tests/` e `firestore.rules` não ficam acessíveis no endereço do app. | novo `.github/workflows/` | S12 | P |
| A4 | O aplicativo sabe a própria versão e a compara com um `versao.json` buscado na rede ao abrir e ao voltar para a aba. Abaixo da versão mínima, mostra o aviso de atualização que já existe e bloqueia gravações. | Com `versao.json` indicando mínima acima da atual, o app mostra "Atualizar" e não grava. Um envio que altera `index.html` sem alterar `VERSAO` falha na integração contínua. | `sw.js:6`; `index.html:1856` | pré-requisito de B1 e H2 | P |
| A5 | As regras têm testes automatizados no emulador do Firebase. O repositório ganha `firebase.json`, arquivo de índices e um `package.json` só de desenvolvimento. Regras e índices passam a ser publicados pela linha de comando. | Existe um teste para cada caso "negado" e "permitido" do apêndice B. Cada caso negado falha contra as regras atuais e passa contra as novas. | novos `firebase.json`, `firestore.indexes.json`, `tests/regras/` | S5 | M |

**Atenção sobre A3.** Hoje o GitHub Pages publica a raiz inteira da `main`. Se `AUDITORIA-COMPLETA.md` e este `PRD.md` forem commitados antes de A3, ficam públicos no endereço do app, com o passo a passo das falhas ainda abertas.

### B. Regras do banco sem migração

Os trechos estão no apêndice B.

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| B1 | A data de criação de jogo, confirmação, pedido de arena e entrada no time é a hora do servidor. A troca é feita em três passos: regra de transição que aceita número ou hora do servidor; aplicativo novo; regra estrita depois de sete dias. | Negado: confirmação com `criadoEm: 0` ou com qualquer número. Permitido: confirmação com a hora do servidor. | `firestore.rules:89`; gravações em `index.html:791`, `892`, `1295`, `1424`, `1475` | S2, N1 | M |
| B2 | O adaptador expõe a hora do servidor para gravação e converte, na leitura, qualquer campo de data para milissegundos: número antigo, data nova e data ainda pendente (com estimativa local). | Com uma confirmação antiga e uma nova no mesmo jogo, a ordem da fila é a cronológica. A confirmação recém-enviada aparece na posição certa antes da resposta do servidor. O backend simulado acompanha. | `firebase.js:23-41`; `index.html:427`; `tests/mock-backend.js` | S2 | P |
| B3 | Jogo, perfil e pedido de arena têm faixas e formatos nas regras: nível 1, 3 ou 5; valor de 0 até o teto (decisão 11); valor nulo em quadra pública; formato do texto `quando`; horários vazios de 0 a 200. | Negado: `valor: -1`, valor acima do teto, `nivel: 9`, valor preenchido em quadra pública. Permitido: jogo de amanhã às 18h, valor 120, nível 3. | `firestore.rules:25-57`, `59-77`, `142-159` | S6, N1 | P |
| B4 | Todo jogo novo grava também `quandoTs`, a data do jogo em formato comparável. A regra recusa jogo novo com `quandoTs` mais de 30 minutos no passado e recusa confirmação depois do início em jogos que têm o campo. | Negado: jogo com `quandoTs` de ontem; confirmação um minuto depois do início. Permitido: confirmação antes do início; confirmação em jogo antigo sem o campo. | `index.html:1284-1292`; `firestore.rules` | S6, N6 | P |
| B5 | A confirmação é aceita só até o horário de início. O prazo de 2 horas depois do início vale apenas para manter o jogo visível em "Meus jogos". | Um minuto depois do início, o convite mostra "Esse jogo já começou" (apêndice A) sem o botão de entrar, e o jogo não aparece em "Procurar". | `index.html:440`, `1056`, `1551` | N6 | P |
| B6 | O time remove membros pelo app. O código do time tem exatamente 6 caracteres, na tela e na regra. | Negado: não membro apagando um documento de `admins`; entrada com código de 4 caracteres. Permitido: membro remove outro; entrada com o código certo. O painel lista os membros com o botão "Remover do time". | `firestore.rules:109-124`; `index.html:889` | S3 | P |
| B7 | Identificadores de jogo, confirmação e pedido de arena têm 20 caracteres gerados com `crypto.getRandomValues`, e a regra recusa outro formato em jogo criado por jogador. | `novoId()` não usa `Math.random` nem o relógio. Negado: jogador cria `jogos/abc`. Convites antigos continuam abrindo. | `index.html:374`; `firestore.rules:171` | S14 | P |

### C. Configuração e limpeza

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| C1 | A chave da Web é restrita por referenciador ao domínio oficial e a `localhost`, e por API às que o app usa. Os domínios autorizados do Authentication ficam só com o oficial e o do projeto. | Uma página em outro domínio usando a mesma configuração recebe erro de chave. Login e leitura funcionam no endereço oficial. Conferência manual no console, registrada no `README.md`. | console; `config.js:5` | S10, S11 | P |
| C2 | O login por e-mail e senha sai do código e fica desligado no console. | A busca por `signInWithEmailAndPassword` no repositório não retorna nada. O console mostra só o provedor Google. | `firebase.js:8`, `50` | S13 | P |
| C3 | O App Check é registrado e inicializado em modo de monitoramento, sem exigência. | O console mostra a proporção de requisições verificadas. Nenhum fluxo muda, inclusive dentro do navegador do WhatsApp. | `firebase.js`; console | S7 | P |
| C4 | Os documentos são alinhados ao código: `REQUISITOS.md` (linhas 15, 28, 30, 35, 51, 61 e os requisitos que só existem no código), `README.md` (linhas 9 e 11), `ARQUITETURA.md` (37, 47, 60, 123, 158), o comentário de `firestore.rules:3` e a nota de `AUDITORIA.md:22`. | Busca sem ocorrência de "Reserva gerada", "nivel 1..5", "Bora jogar", "botão amarelo", "Regras do Fechou" e "Google Fonts". O endereço do app no README é o oficial. | arquivos citados | seção 3 da auditoria, S11 | P |

### D. Entrada no produto

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| D1 | Ao tocar em "Marcar jogo" sem estar logado, o app guarda `#novo` como destino e leva a pessoa ao formulário depois do login e do perfil, inclusive quando ela toca em "Preencher depois". | Partindo da landing sem conta: tocar em "Marcar jogo", concluir o login e salvar o perfil termina em `#novo`. O mesmo vale para "Preencher depois". O destino sobrevive a um recarregamento durante o login. | `index.html:648`, `714`, `964`, `1718-1721` | D2, F1 | P |
| D2 | O convite aceita também o identificador por parâmetro (`?c=<id>`), convertido para a rota atual. Quando o convite de jogo público é aberto em navegador embutido (WhatsApp, Instagram, Facebook) ou quando o popup falha, a tela mostra "Abrir no navegador" como ação principal e "Copiar link" como segunda, com "Entrar com Google" abaixo. | Abrir `…/?c=<id>` mostra o mesmo convite que `…/#convite-<id>`. Com agente de usuário contendo `WhatsApp`, `Instagram` ou `FBAN`, a tela mostra os textos do apêndice A. Fora desses navegadores a tela é a atual. | `index.html:632`, `700-714`, `1456-1463` | D1, C1 | M |
| D3 | Teste manual do convite público aberto dentro do WhatsApp, em um Android e um iPhone, com o resultado anotado no repositório. O resultado decide se D2 basta ou se a decisão 12 precisa ser reaberta. | Existe o registro do teste nos dois aparelhos, dizendo se o login funcionou e por qual caminho. | — | D1 | P |
| D4 | O perfil passa a ser opcional de forma declarada. No primeiro acesso pede só nome, cidade, esporte e nível, sem a chamada do Premium. "Preencher depois" vira botão. Horários e WhatsApp ficam na edição do perfil. | A tela do primeiro acesso tem 4 campos, nenhum link para `#premium` e cabe em duas alturas de tela a 390×844. "Preencher depois" tem pelo menos 48 px de altura. `REQUISITOS.md` deixa de dizer que o perfil é obrigatório. | `index.html:919-969`, `934`, `939` | D9, N8 | M |
| D5 | Quem marca jogo sem perfil escolhe o nível no formulário; o campo não vem marcado em "Intermediário". | Sem perfil, nenhum nível vem marcado, e salvar sem escolher mostra "Escolha o nível do jogo." | `index.html:1207`, `1285` | N8 | P |
| D6 | "Entrar", na barra de quem não está logado, abre o login com Google direto. | Tocar em "Entrar" chama o login sem trocar de tela; em caso de erro, a mensagem aparece na própria tela. | `index.html:674-677` | D15 | P |

### E. Telas e texto

Os textos finais estão no apêndice A.

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| E1 | Os erros de login deixam de mostrar instruções do console, código de erro ou nome de coleção. O detalhe técnico vai para `console.warn`. A mensagem de falta de permissão muda conforme o papel. | Nenhum texto visível contém "Firebase", "Authentication", "admins", nome de coleção, código entre parênteses ou "Claude". | `index.html:539`, `704-708`, `1607`, `1811` | D7 | P |
| E2 | A tela do convite de jogo lotado não se contradiz. | Visitante sem confirmação em jogo lotado: nenhum confete, cabeçalho "Esse jogo já fechou", placar "Time completo". Com 1 vaga, o texto é "1 de 1 vaga preenchida". Quem está no jogo vê o confete uma vez. | `index.html:586`, `1523`, `1545` | D4 | P |
| E3 | Na tela de quem organiza, enquanto o jogo não fechou, "Enviar no WhatsApp" fica logo abaixo do placar. A linha de local mostra a cidade, como no convite. | A 390×844, com o jogo aberto, o botão aparece sem rolar a tela. A linha de local é igual nas duas telas. | `index.html:1306-1323`, `1351-1368` | D8 | P |
| E4 | A barra inferior tem um só indicador de tela atual. | Fora de "Procurar", nenhum item além do atual tem fundo limão. | `index.html:673` | D12 | P |
| E5 | Estados vazios: a landing sem jogos mostra mensagem e botão em vez de esconder a seção; o filtro sem resultado oferece marcar um jogo em vez de repetir "Limpar filtros". | Sem jogos públicos, a seção "Tem vaga agora" aparece com o texto do apêndice A. Com filtro de esporte sem resultado, há um único "Limpar filtros" e um botão "Marcar jogo de <esporte>". | `index.html:729`, `743-746`, `1090-1093` | D15 | P |
| E6 | Um termo por conceito, conforme o glossário do apêndice A. No convite, o erro de nome vazio aparece junto do campo. | Busca em `index.html` e `manifest.webmanifest` sem "check-in", "Jogos abertos", "Marcar o meu jogo" nem "Marcar meu jogo" em texto visível. | `index.html:915`, `1203`, `1471`, `1502`, `1524` | D11 | P |
| E7 | A página para arenas declara, junto de "30 dias grátis", o que acontece depois: o preço por jogo fechado em horário vago, lido de uma configuração que o time preenche, e o que conta como jogo fechado. Sem preço configurado, diz que o valor é combinado por escrito antes do início do piloto. | Leitura da tela nos dois estados, com os textos do apêndice A. O texto distingue o pedido (sem cobrança) do período posterior. | `index.html:738`, `772`, `829-834` | M1, C4 | P |
| E8 | A prova social diz "respostas" em vez de "jogadores", e a página de arenas traz a ressalva visível. | A landing diz "28 de 36 respostas". A ressalva aparece na página de arenas sem precisar abrir nada. | `index.html:803-825` | C7 | P |
| E9 | A prévia do link tem imagem e endereço: `og:image` (PNG de 1200×630, até 300 KB), dimensões, texto alternativo, `og:url`, `og:type`, `og:locale` e `twitter:card`. | Colar o endereço em uma conversa do WhatsApp mostra a imagem. | `index.html:13-16`; `icons/` | C5 | P |
| E10 | A tela do Premium deixa de prometer prioridade de 15 minutos, pontos em ranking e aviso de abertura, e sai da navegação principal. O contador de interesse continua. | Nenhuma menção a "15 minutos", "ranking", "Pontos" ou "Avisamos quando abrir". O contador do painel continua funcionando. | `index.html:1096-1117` | M4 | P |
| E11 | O indicador principal do painel é renomeado para "Valor de quadra dos jogos que completaram (informado por quem marcou)". | Nenhuma ocorrência de "Receita de quadra gerada" nem de "Reserva gerada" em telas e documentos. | `index.html:1135`, `1367` | N1 | P |

### F. Acessibilidade

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| F1 | A cada troca de tela, o título da aba muda e o foco vai para o título principal da tela. | Depois de qualquer navegação, `document.title` é o da tabela do apêndice A e o elemento com foco é o `h1` da tela. | `index.html:13`, `656` | D5 | P |
| F2 | O diálogo de cópia manual usa `<dialog>` com `showModal()`. | Esc fecha; Tab não sai do diálogo; ao fechar, o foco volta ao botão que o abriu. | `index.html:297-304`, `580` | D6 | P |
| F3 | Todo controle tocável tem pelo menos 44 px de altura, por um token único de toque. | A 390 px de largura, nenhum botão, link de ação, "Voltar" ou chip tem menos de 44 px. "Tirar" e "Cancelar jogo" ficam a pelo menos 8 px de outro botão. Nenhum `min-height` literal de 40, 42 ou 44 px resta no CSS. | CSS em `index.html:28-50`, `118`, `124`, `235` | D14 | P |
| F4 | O texto de faixa de horário dos períodos usa branco cheio quando marcado, e o par entra no teste de contraste. | `tests/contraste.py` inclui o par e passa com 5,13:1. | `index.html:254`; `tests/contraste.py` | D13 | P |
| F5 | Pontos menores: título principal no painel; `<noscript>`; `viewport-fit=cover`; aviso temporário de 5 segundos; `aria-busy` em botão processando. | Existe um `h1` "Painel". Sem JavaScript aparece o texto do apêndice A. Em um iPhone com o app instalado, a barra inferior não encosta no indicador de início. | `index.html:5`, `121`, `569`, `1132` | D15 | P |

---

## 6. Requisitos da Fase 2

Para o piloto com arenas. Inclui a migração descrita na seção 8.

### G. Medição e retenção sem migração

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| G1 | Todo link aceita um parâmetro de origem (`?o=`), guardado na primeira visita e gravado na confirmação, no perfil e no jogo marcado. Quem organiza pode dar nome à origem antes de copiar o link. | Abrir `…/?o=grupo-volei#convite-<id>` e confirmar grava `grupo-volei` na confirmação. O valor aceita só letras minúsculas, números e hífen, até 40 caracteres; fora disso é descartado. | `index.html:515-533`, `958-961`, `1472-1475`; `firestore.rules:81` | C3 | M |
| G2 | Contador de páginas sem cookies, com um registro por troca de rota e os eventos da tabela do apêndice A. O caminho enviado é o nome da tela, nunca o identificador do jogo. A tela de privacidade diz o que é medido. | Navegar por cinco telas gera cinco registros com nomes de tela. Nenhum pedido ao contador contém identificador de jogo, nome, telefone ou `uid`. | `index.html:639-656`, `851-869` | C3 | P |
| G3 | "Adicionar ao calendário" na tela "Você está no jogo!" e na tela de quem organiza: arquivo `.ics` gerado no aparelho e link do Google Agenda. Duração padrão de uma hora, lembrete 2 horas antes, link do convite na descrição. | O arquivo importa sem erro no Google Agenda e no Calendário da Apple, com data, hora e local corretos, inclusive com vírgula no nome do local. | `index.html:1483-1499` | F2 | P |
| G4 | Quem acabou de confirmar vê "Chamar mais gente" enquanto o jogo tem vaga. Usa o compartilhamento do sistema quando existe e cai para o WhatsApp quando não existe. | Com vagas, o botão aparece e a mensagem leva o número de vagas e o link com `o=convidado`. Com o jogo fechado, não aparece. Cancelar a folha de compartilhamento não mostra erro. | `index.html:570`, `1397`, `1483-1499` | C6 | P |
| G5 | A oferta de instalação volta a aparecer uma vez depois da primeira confirmação, mesmo para quem tocou em "Agora não". | Quem dispensou a faixa e depois confirma vê a faixa de novo. Dispensar de novo esconde para sempre. | `index.html:609-617`, `1700` | F8 | P |

### H. Migração e privacidade do jogo

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| H1 | O adaptador ganha consulta filtrada (filtro, ordem e limite), consulta de grupo de coleções, leitura única e escrita em lote. | Cada operação nova tem teste no backend simulado e no emulador. | `firebase.js:23-41` | S1, S8 | M |
| H2 | Página de migração no próprio repositório, aberta por alguém do time, com modo de simulação, cópia de segurança em JSON e execução repetível, conforme a seção 8. | Rodar duas vezes seguidas no emulador com dados antigos produz o mesmo resultado. O número de confirmações por jogo é igual antes e depois. | nova página em `ferramentas/` | S1, S9 | M |
| H3 | Jogo privado só abre por link: qualquer um lê um jogo pelo identificador, mas só lista os públicos, os próprios, ou tudo se for do time. | Negado: listar `jogos` sem filtro; listar privados de outra pessoa. Permitido: abrir jogo privado pelo identificador sem conta; listar públicos; dono listar os seus. | `firestore.rules:169-174` | S1 | M |
| H4 | As confirmações passam a `jogos/{id}/confirmacoes/{cid}`. Com conta, `cid` é o `uid`. Sem conta, `cid` tem 20 caracteres aleatórios. A consulta entre jogos só devolve as do próprio usuário, ou tudo para o time. | Negado: consulta de grupo sem filtro; consulta com `uid` de outra pessoa; visitante criando `cid` igual ao `uid` de alguém. Permitido: listar confirmações de um jogo cujo identificador se conhece; "Meus jogos" com o próprio `uid`. | `firestore.rules:187-194`; `index.html:1424`, `1475`, `1669` | S9, S1 | G |
| H5 | Fim da escuta de coleções inteiras. "Procurar" e a landing consultam jogos públicos futuros, com limite de 50, e escutam as confirmações só dos jogos exibidos. "Meus jogos" consulta os jogos do dono e as confirmações do próprio `uid`. As telas de jogo e de convite escutam um jogo e as confirmações dele. | Com 500 jogos antigos no emulador, abrir a landing lê no máximo 60 documentos de jogo. Um jogo privado não aparece em nenhuma consulta de quem não é dono nem do time. | `index.html:1797-1842` | S8, S1 | G |
| H6 | O contato de quem organiza é lido pelo time, pelo dono e por quem tem confirmação própria em estado "confirmado" (decisão 4). | Negado: conta sem confirmação; conta com confirmação em "desistiu" ou "removido"; visitante. Permitido: conta confirmada. | `firestore.rules:177-185` | S1, N11 | P |
| H7 | Não existe contador de confirmados gravado pelo aparelho (decisão 13). As vagas dos cartões vêm da escuta das confirmações dos jogos exibidos. | Nenhuma regra permite a um jogador atualizar campo numérico de lotação no jogo. | `firestore.rules` | S8, N1 | — |
| H8 | O App Check passa a ser exigido no Firestore depois de uma semana de monitoramento com mais de 95% das requisições verificadas. | Negado: requisição por script sem token. Permitido: app no endereço oficial, inclusive no navegador do WhatsApp. Se a taxa não chegar a 95%, não exigir e registrar o motivo. | console | S7 | P |

### I. Estados e controle de quem organiza

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| I1 | Cancelar um jogo muda o estado para "cancelado", com data, em vez de apagar. "Apagar jogo" vira "Cancelar jogo". O convite de jogo cancelado continua abrindo e informa o cancelamento; o jogo sai de "Procurar" e dos indicadores, e o contato de quem organiza é apagado no mesmo passo. Só o time apaga de vez. | Quem organiza cancela um jogo com uma confirmação: o convite abre com "Esse jogo foi cancelado", o jogo não aparece em "Procurar" e as confirmações continuam gravadas. Negado: dono apagando o jogo; dono reabrindo jogo cancelado. | `index.html:1516`, `1743-1752`; `firestore.rules:173` | N2 | M |
| I2 | Antes de cancelar, quem organiza vê a mensagem pronta de aviso e o botão "Avisar o grupo no WhatsApp". | O cancelamento só acontece no segundo toque, em "Cancelar o jogo". Com zero confirmados, o diálogo não oferece o aviso. | `index.html:1324-1325` | N2 | P |
| I3 | Desistir e ser retirado são mudanças de estado na confirmação ("desistiu", "removido"), com data. Voltar depois de desistir reinicia a data e manda a pessoa para o fim da fila. Só o time apaga. | Negado: jogador apagando a própria confirmação; voltando com a data antiga; mudando o estado de outra pessoa. Permitido: desistir; voltar em jogo aberto e não iniciado; dono retirar alguém. | `index.html:1673`, `1709`; `firestore.rules:190-193` | N2, S1 | M |
| I4 | Quem marcou o jogo corrige horário, local, cidade, total, vagas, nível e preço enquanto o jogo está aberto e não começou. Esporte, visibilidade, dono e a marca de teste não mudam. Com confirmados, a tela oferece a mensagem pronta de mudança. | A dona altera a hora e o total, e as confirmações permanecem. Reduzir o total abaixo dos confirmados é recusado com o texto do apêndice A. Negado: dono mudando `donoUid`, `teste` ou os campos só do time. | `index.html:1194-1303`, `1360`; `firestore.rules:172` | N4 | M |
| I5 | Quando abre vaga e há lista de espera, quem organiza vê quem entrou e o botão "Avisar <nome> que abriu vaga", com mensagem pronta. A tela de quem espera deixa de prometer que "esta tela avisa". | Com uma desistência e alguém na espera, o primeiro da fila aparece com a etiqueta "entrou agora" e o botão de aviso. O botão abre o WhatsApp para quem deixou contato e copia a mensagem para quem não deixou. | `index.html:1388-1393`, `1489` | N3, F5 | M |
| I6 | O convidado sem conta pode deixar o WhatsApp depois de confirmar, com consentimento explícito e desmarcado por padrão. O telefone fica em documento separado da confirmação, legível só por quem organiza e pelo time. | Sem marcar o consentimento, nada é gravado. Negado: leitura do contato por outro jogador ou visitante; gravação sem consentimento; gravação sem confirmação correspondente. | `index.html:1466-1467`, `1498` | C2, N3 | M |
| I7 | No convite de jogo privado, a tela oferece "Entrar com Google" como alternativa ao nome, explicando que assim a pessoa consegue sair do jogo sozinha. Quem entrou só com o nome vê a explicação de que só quem organiza pode tirar. | A opção aparece abaixo do campo de nome. Quem entra com conta consegue desistir de qualquer aparelho. | `index.html:1466-1467`, `1497` | N5 | P |
| I8 | "Meus jogos" separa "Próximos" e "Já joguei". O cartão indica "Você marcou" ou "Você vai". | Com jogos futuros e passados, "Próximos" lista os futuros em ordem de data e "Já joguei" aparece recolhida com a contagem. | `index.html:877-878`, `900-916` | F7 | P |
| I9 | "Marcar de novo na próxima semana" em jogos passados e na tela do jogo fechado, para quem marcou. Abre o formulário preenchido com a data 7 dias depois e grava o jogo de origem. Não copia confirmações. Depois de marcar, oferece "Chamar quem jogou". | O jogo novo tem identificador próprio e o campo `copiadoDe` correto. | `index.html:1194-1303` | F3 | P |
| I10 | Mensagens prontas de WhatsApp para aviso de vaga, cancelamento, mudança de jogo, "marcar de novo" e "chamar mais gente", montadas ao lado de `msgConvite` e `msgGrupo`. | As mensagens são as do apêndice A. | `index.html:515-533` | N2, N3, F3 | P |

### J. Prova para a arena

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| J1 | O momento de fechamento do jogo é calculado, não gravado: é a data de servidor da confirmação ativa que preencheu a última vaga (decisão 13). O painel usa esse valor para "jogos fechados por semana" e "tempo até fechar". | Com um jogo de 2 vagas e confirmações às 10h e às 11h, o fechamento é 11h. Se a segunda desiste e outra entra às 12h, o fechamento passa a ser 12h. | `index.html:427-431`, `473-488` | N1, M2 | P |
| J2 | Depois do horário do jogo e por até 7 dias, quem organiza marca, entre os confirmados, quem compareceu. Em "Meus jogos", jogos passados sem marcação pedem a resposta. | Antes do horário o bloco "Quem foi?" não aparece. Depois, a dona marca 2 de 3 e o painel mostra 1 falta em 3. Negado: marcar presença antes do horário; jogador marcando presença em jogo alheio. | `index.html:1306-1325`, `1388-1393`, `1501-1502` | F4, N1, M2 | M |
| J3 | O time promove um pedido de piloto a "arena parceira", com identificador, nome e cidade públicos, e a parte comercial (início do piloto, preço confirmado da hora, preço pós-piloto, aceite, horários declarados vazios) em documento só do time. Ao marcar jogo, escolher uma parceira da lista grava o identificador dela. | Um jogo marcado com a arena parceira guarda o identificador; um jogo com o mesmo nome digitado à mão não guarda. Negado: visitante lendo o documento comercial; jogador criando jogo com identificador de arena inexistente. | `index.html:349`, `1284-1292` | M3 | M |
| J4 | Só o time grava, no jogo, "realizado", "valor confirmado" e "horário vazio". O evento faturável é calculado: jogo de arena parceira, realizado, com todas as vagas preenchidas, em horário declarado vazio, fora dos jogos de teste e fora de quadra pública. | Com quatro jogos: um que atende a tudo conta; um fora do horário declarado, um não realizado e um de teste não contam. Negado: jogador gravando qualquer um dos três campos. | `index.html:473-488`; `firestore.rules:172` | M2, N1 | M |
| J5 | O pedido de piloto registra o valor que a arena aceitaria pagar (opcional) e, no painel do time, o aceite da oferta: sem resposta, sim ou não, com data e valor. O painel mostra quantas ofertas e quantos "sim". | O time marca "sim" com valor em um pedido e o painel mostra "1 sim em 1 oferta". | `index.html:749-797`, `839`, `1164-1171`; `firestore.rules:144` | M1, M5 | P |
| J6 | O indicador principal do painel passa a contar só jogos realizados com valor confirmado, em dois números: receita nova em horário vago e reserva preservada. | Um jogo fechado sem "realizado" não soma. Um jogo realizado com situação "grupo incompleto" soma só em "reserva preservada". | `index.html:473-488`, `1135` | N1 | M |
| J7 | O painel lê os jogos de uma janela padrão de oito semanas, com o histórico completo sob demanda, mostra "esta semana" e "semana passada" para jogos marcados, fechados e realizados, lista os jogos por arena parceira e exporta em CSV. | Os números batem com uma contagem manual sobre os dados de teste. O CSV abre em planilha com acentos corretos, uma linha por jogo, sem jogos de teste. | `index.html:1132-1191` | S8, métricas | M |
| J8 | A tela do Premium vira a pergunta "O que valeria pagar?", com as opções do apêndice A, e grava a resposta. | A tela mostra as opções e a resposta aparece agregada no painel. | `index.html:1096-1117`; `firestore.rules:133-139` | M4 | P |

### K. Qualidade de tela e de regra

| Id | Requisito | Critério de aceite | Onde | Resolve | Esf. |
|---|---|---|---|---|---|
| K1 | Nos formulários de perfil, marcar jogo, arenas e base de jogadores, o erro aparece logo abaixo do campo errado, com `aria-invalid` e `aria-describedby`, e o foco vai para o primeiro campo inválido. As quatro cópias de `falha()` viram uma função. | Enviar o formulário de marcar jogo sem cidade: "Escreva a cidade." aparece a no máximo 8 px abaixo do campo, e o foco está nele. Todos os erros de um envio aparecem de uma vez. | `index.html:777`, `946`, `1254`, `1624` | D3 | M |
| K2 | Em "Procurar", no celular, só Esporte fica visível; dia da semana e período entram em "Mais filtros", que mostra quantos estão ativos. | A 390×844, sem filtros, o primeiro cartão aparece inteiro acima da barra inferior. A partir de 720 px o desenho atual é mantido. | `index.html:1020-1030` | D10 | M |
| K3 | As quatro implementações de chip selecionável compartilham uma regra base, com 44 px de altura mínima e o mesmo estado marcado. | Os chips do perfil, dos filtros e do formulário têm a mesma altura e o mesmo estado marcado. `DESIGN.md` descreve um componente só. | CSS em `index.html:131`, `221`, `235`, `248` | D14 | M |
| K4 | "Tem vaga agora" ordena os jogos pelo perfil de quem está logado, e cada cartão diz por que foi sugerido. | Com perfil de vôlei de praia intermediário, um jogo de vôlei intermediário aparece antes de um de padel mais próximo na data, com "Combina com você". Sem perfil, a ordem atual é mantida. | `index.html:461-471`, `907-912` | F6 | M |
| K5 | O filtro de "Procurar" e "Quem combina" usam a mesma função de período do dia. | Jogos às 3h, 12h, 17h30 e 19h recebem o mesmo período nas duas telas. | `index.html:416-425`, `456` | N9 | P |
| K6 | A importação da base grava a cidade, e "Quem combina" mostra uma linha por pessoa quando o mesmo WhatsApp existe no formulário e no perfil. | A mesma pessoa nas duas fontes aparece uma vez. Jogador importado sem cidade aparece com "cidade não informada". | `index.html:491-501`, `1565-1574` | N10 | P |
| K7 | Ao confirmar, o sistema avisa quando a mesma conta já tem confirmação em outro jogo no mesmo horário, sem impedir. | Uma conta confirmada às 18h recebe o aviso ao entrar em outro jogo às 18h30 e consegue seguir. | `index.html:1468-1481` | N12 | P |

---

## 7. Escopo da Fase 3

Sem critério de aceite detalhado. Entra depois que o piloto responder se a arena paga.

- Aviso de vaga e lembrete automáticos (push ou WhatsApp por servidor).
- Sinal por Pix contra furo.
- Prévia do link por jogo (esporte, dia e vagas), que exige servidor.
- Acesso da arena para conferir e confirmar os próprios jogos.
- Nível por esporte no perfil (achado N7).
- Etapa de build, política de segurança de conteúdo e SDK hospedado junto do app (achado S15).
- Limpeza do design system: tokens de espaçamento, escala de fontes, tema claro.
- Lista de e-mails autorizados no lugar do código compartilhado do time.

---

## 8. Modelo de dados e migração

### Campos, estados e coleções

| Onde | Campo ou coleção | Tipo | Quem grava | Compatibilidade | Fase |
|---|---|---|---|---|---|
| `jogos`, `confirmacoes`, `arenas_piloto`, `admins` | `criadoEm` | Passa de número do aparelho para hora do servidor | Quem cria | Documentos antigos ficam como número; a leitura aceita os dois (B2) | 1 |
| `jogos/{id}` | `quandoTs` | Data, derivada de `quando` no fuso de Brasília | Quem marca | Ausente nos antigos; a migração preenche. `quando` continua sendo o que a tela mostra | 1 (novos), 2 (antigos) |
| `jogos/{id}` | `estado` | `aberto` ou `cancelado` | Dono ou time | A migração grava `aberto`. "Fechado" e "passou" continuam calculados | 2 |
| `jogos/{id}` | `canceladoEm`, `atualizadoEm` | Hora do servidor | Dono ou time | Só existem depois de cancelar ou editar | 2 |
| `jogos/{id}` | `visibilidade` | `publico` ou `privado` | Quem marca | Ausente hoje vale privado; a migração torna explícito | 2 |
| `jogos/{id}` | `arenaId` | Identificador em `arenas/` | Quem marca, ao escolher uma parceira | Ausente vale "não parceira". O texto `arena` continua | 2 |
| `jogos/{id}` | `realizado`, `valorConfirmado`, `horarioVazio` | Booleanos | Só o time | Ausentes valem "não informado" | 2 |
| `jogos/{id}` | `copiadoDe`, `origem` | Textos | Quem marca | Opcionais | 2 |
| `jogos/{id}/confirmacoes/{cid}` (substitui `confirmacoes/`) | `nome`, `via`, `criadoEm`, `uid` opcional | Como hoje | Como hoje | A migração copia os documentos antigos | 2 |
| idem | `estado`, `saiuEm` | `confirmado`, `desistiu` ou `removido`; hora do servidor | Quem confirmou, dono ou time | Substitui a exclusão | 2 |
| idem | `presente`, `presencaEm` | Booleano; hora do servidor | Dono ou time, depois do horário | Ausente vale "não marcado" | 2 |
| idem | `origem` | Texto de até 40 caracteres | Quem confirma | Opcional | 2 |
| `jogos/{id}/contatos/{cid}` (nova) | `whatsapp`, `consentiu`, `criadoEm` | Texto, booleano, hora do servidor | Convidado sem conta que aceitar | Leitura só do dono e do time | 2 |
| `arenas/{aid}` (nova) | `nome`, `cidade`, `cidadeChave`, `ativa` | Textos e booleano | Só o time | Leitura pública, para a lista do formulário | 2 |
| `arenas/{aid}/privado/piloto` (nova) | início, preços, aceite, horários vazios, `pedidoId` | Vários | Só o time | Leitura só do time | 2 |
| `arenas_piloto/{id}` | `valorAceitavel`; situação e data da oferta | Número; texto e data | Arena (valor); time (oferta) | Opcionais | 2 |
| `interesse_premium/{uid}` | `respostas` | Lista de textos | A própria pessoa | Opcional | 2 |
| `perfis/{uid}` | `origem` | Texto | A própria pessoa, na criação | Opcional | 2 |

### Migração

**Fase 1, sem migração de documentos:**

1. Publicar a regra de transição, que aceita `criadoEm` como número ou como hora do servidor.
2. Publicar o aplicativo que envia a hora do servidor e lê os dois formatos, com a versão trocada.
3. Depois de sete dias, publicar a regra estrita. Aparelhos na versão antiga recebem o aviso de atualização (A4).

A ordem não pode ser invertida: a regra atual exige número, então o aplicativo novo seria recusado se fosse publicado antes do passo 1.

**Fase 2, em horário de pouco uso:**

1. Criar os índices: `jogos` por `visibilidade` e `quandoTs`; grupo de coleções `confirmacoes` por `uid`.
2. Publicar regras ampliadas: as novas ao lado das antigas.
3. Rodar a página de migração (H2). Para cada jogo: preencher `quandoTs`, `estado` e `visibilidade`. Para cada confirmação: copiar para a subcoleção com `estado: confirmado`.
4. Publicar o aplicativo novo, com a versão mínima trocada.
5. Publicar a regra que bloqueia criação na coleção antiga `confirmacoes`.
6. Rodar a migração de novo, para pegar o que foi gravado entre os passos 3 e 5.
7. Depois de sete dias, fechar a leitura da coleção antiga e apagar seus documentos pela mesma página.

**Convites já enviados continuam valendo:** o identificador do jogo não muda, e abrir um jogo pelo identificador segue liberado.

---

## 9. Segurança

### Modelo de ameaça

**Quem ataca.** Um curioso com conta Google e o console do navegador; um script com uma ou várias contas; um ex-membro do time ou alguém que recebeu o código repassado. Não se considera atacante com acesso ao console do Firebase.

**O que quer.** Coletar o WhatsApp de quem organiza; passar à frente na fila; inflar o número mostrado à arena; encher jogos e pedidos de lixo ou esgotar a cota de leituras; entrar no time para ler perfis e a base.

### Risco aceito nestas fases

- Em jogo público, qualquer conta entra e vê o contato: é o fluxo do produto. A mitigação é o rastro permanente (I3: a confirmação não é mais apagável pelo jogador) e o App Check.
- Quem está na lista de espera também vê o contato, porque as regras não sabem a posição na fila sem servidor.
- Nome dos confirmados fica legível para quem tem o identificador do jogo: é o que o convite mostra.
- Quem organiza pode marcar presença falsa no próprio jogo. Por isso o número da arena depende de "realizado", que só o time grava.
- O texto `quando` e a data `quandoTs` são gravados juntos pelo aparelho, e a regra não prova que dizem a mesma hora. Só afeta o jogo de quem mentiu.
- Qualquer membro do time remove outro, e o código continua compartilhado.
- O App Check não barra um navegador real operado à mão.

Os trechos de regra e os casos de teste estão no apêndice B.

---

## 10. Ordem de entrega e plano de testes

Cada entrega vai ao ar sozinha.

| Entrega | Requisitos | Depende de |
|---|---|---|
| 1. Testes confiáveis | A1, A2, A3, A4 | — |
| 2. Limpeza sem risco | C2, C4, B7, E1 a E11, F1 a F5 | pode ir junto com a 1 |
| 3. Regras testáveis | A5 | — |
| 4. Hora do servidor e faixas | B1, B2, B3, B4, B5, B6 | 1 e 3 |
| 5. Entrada no produto | D1 a D6 | — |
| 6. Configuração | C1, C3 | endereço oficial decidido |
| **Fim da Fase 1** | | |
| 7. Medição e retenção | G1 a G5 | 6 |
| 8. Adaptador novo | H1 | 3 |
| 9. Migração | H2, H3, H4, H5, H6, H7 | 8; é a única entrega grande |
| 10. Estados e controle | I1 a I10 | 9 |
| 11. Prova para a arena | J1 a J8 | 9 e 10 |
| 12. Qualidade | K1 a K7, H8 | independente, exceto H8 (uma semana de C3) |

**Por que a migração é uma entrega só.** Jogo privado por link, confirmações em subcoleção e consultas filtradas mexem nos mesmos documentos e nas mesmas telas. Separar obrigaria a migrar duas vezes.

**Plano de testes.**

- **Regras:** todo caso "negado" e "permitido" deste PRD vira teste no emulador (A5). Nenhuma regra é publicada sem passar.
- **Ponta a ponta:** os cenários atuais continuam, com datas relativas (A1), e ganham os fluxos novos: cancelar, desistir e voltar, editar, presença, "marcar de novo".
- **Manual em aparelho:** convite público dentro do WhatsApp em Android e iPhone (D3); barra inferior em iPhone com o app instalado (F5); prévia do link (E9).
- **Migração:** ensaio completo no emulador com uma cópia dos dados reais antes de rodar em produção (H2).

---

## 11. Decisões em aberto

Cada uma traz a recomendação adotada neste PRD. Mudar a escolha muda os requisitos indicados.

| # | Decisão | Opções | Recomendação | O que muda |
|---|---|---|---|---|
| 1 | Preço pós-piloto para a arena | (a) Valor fixo por jogo fechado em horário vago. (b) Percentual do preço da hora. (c) Mensalidade. | (a), com o valor definido pelo time antes da primeira oferta. Este PRD não define o valor. | E7 mostra o valor ou "combinado antes do início". Com (b), J4 calcula sobre o preço confirmado. Com (c), J4 vira relatório de apoio. |
| 2 | Servidor nas fases 1 e 2 | (a) Sem servidor. (b) Funções em nuvem. | (a). | Com (b), J1 e I5 ficam mais simples e o aviso automático sobe para a Fase 2. |
| 3 | Quem confirma que o jogo aconteceu | (a) Só quem organiza. (b) Quem organiza marca presença e o time confirma "realizado". (c) A arena. | (b). | Com (a), J4 perde força como base de cobrança. Com (c), surge o acesso da arena, que é Fase 3. |
| 4 | Contato de quem organiza para a lista de espera | (a) Visível a quem espera. (b) Só a quem tem vaga. | (a). Produto preferia (b), mas as regras não verificam a posição na fila sem servidor. | Com (b), é preciso servidor ou a opção "mostrar meu WhatsApp só depois que eu aceitar". |
| 5 | Tela do Premium | (a) Fora da navegação, como pergunta. (b) Remover. (c) Manter. | (a). | Com (b), E10 vira remoção e J8 sai. |
| 6 | Endereço oficial do aplicativo | (a) O do README. (b) O do repositório remoto. (c) Domínio próprio. | (c), antes de a Fase 1 terminar. | Afeta C1, C4, E9 e todos os links já enviados. |
| 7 | Perfil | (a) Opcional. (b) Obrigatório antes de marcar. | (a). | Com (b), D4 e D5 se invertem e a exigência passa a precisar de regra. |
| 8 | Conta em jogo público | (a) Continua exigida. (b) Entrada só com o nome. | (a). | Com (b), D2 e D3 saem, mas J2 e o segundo jogo em 14 dias perdem a identidade do jogador. |
| 9 | Jogo em quadra pública no painel | (a) Nunca conta. (b) Conta em indicador separado, sem valor. | (b) no painel, fora do evento faturável. | Só altera a apresentação em J4 e J7. |
| 10 | Edição do jogo com gente confirmada | (a) Permitida até o início, com mensagem pronta de aviso. (b) Bloqueada depois da primeira confirmação. | (a). | Com (b), I4 ganha a condição "sem confirmações". |
| 11 | Teto de valor do jogo na regra | Um valor em reais. | R$ 1.000, porque as referências de mercado vão de R$ 60 a R$ 220 por hora. A confirmar pelo time. | Só o número em B3. |
| 12 | Saída para o login em navegador embutido | (a) "Abrir no navegador" (D2). (b) Mudar a hospedagem para o Firebase Hosting e usar login por redirecionamento. (c) Login anônimo do Firebase para a confirmação. | (a), e reavaliar depois de D3. A documentação do Firebase diz que o redirecionamento falha quando o domínio do app difere do domínio de autenticação, e o Google bloqueia o próprio login em visualização embutida, o que (b) não resolve. | Com (c), a confirmação funciona em qualquer navegador, mas muda as regras de H4 e exige nova revisão de segurança. |
| 13 | Contador de confirmados e momento de fechamento | (a) Calculados a partir das confirmações. (b) Gravados no jogo, em transação, pelo aparelho que confirma. | (a). Engenharia preferia (b), para listar jogos sem ler confirmações. Segurança mostrou que um contador gravado pelo aparelho exigiria dar a qualquer visitante permissão de atualizar o jogo. Na escala do piloto, o custo de leitura de (a) é aceitável. | Com (b), H5 lê menos documentos, mas a regra do contador é a parte mais delicada e precisa de teste de concorrência. |
| 14 | Ferramenta do contador de páginas | Serviço sem cookies com chamada manual por rota; Firebase Analytics; gravar no próprio Firestore. | Serviço sem cookies. Termos e preço não foram conferidos e precisam ser antes de adotar. | Só G2. |

---

## 12. Rastreabilidade

Todo achado crítico ou alto da auditoria tem requisito. Os médios e baixos sem requisito estão justificados.

| Achado | Severidade | Requisitos |
|---|---|---|
| S1 WhatsApp de organizadores coletável | Alto | H3, H4, H6, I3, C3, H8 |
| S2 Fila manipulável | Alto | B1, B2 |
| S3 Time sem saída | Alto | B6 |
| S4 Testes quebram em 21/11 | Alto | A1 |
| S5 Testes não validam as regras | Alto | A5 |
| S6 Regras só no aplicativo | Médio | B3, B4 |
| S7 Escrita anônima sem limite | Médio | C3, H8 |
| S8 Escuta de coleções inteiras | Médio | H5, J7 |
| S9 Confirmações legíveis sem login | Médio | H4 |
| S10 Chave sem restrição | Médio | C1 |
| S11 Endereço ambíguo | Médio | C1, C4, decisão 6 |
| S12 Sem integração contínua | Médio | A2, A3 |
| S13 Login por e-mail exposto | Baixo | C2 |
| S14 Identificador previsível | Baixo | B7 |
| S15 Sem política de conteúdo | Baixo | Fase 3 (depende de build) |
| N1 Número da arena inflável | Alto | B3, E11, J1, J2, J4, J6 |
| N2 Cancelamento só por exclusão | Alto | I1, I2, I3 |
| N3 Lista de espera sem aviso | Alto | I5, I6 |
| N4 Dono não corrige o jogo | Médio | I4 |
| N5 Sem conta não desiste | Médio | I7 |
| N6 Confirmação até 2 horas depois | Médio | B4, B5 |
| N7 Um nível para todos os esportes | Médio | Fase 3 (muda perfil, importação e cruzamento) |
| N8 Perfil pulável | Médio | D4, D5 |
| N9 Dois cortes de período | Baixo | K5 |
| N10 Base sem cidade e duplicada | Baixo | K6 |
| N11 Contato para a lista de espera | Baixo | H6, decisão 4 |
| N12 Dois jogos no mesmo horário | Baixo | K7 |
| D1 Login por popup no WhatsApp | Alto | D2, D3, decisão 12 |
| D2 Intenção perdida | Alto | D1 |
| D3 Erro longe do campo | Alto | K1; E6 para o convite |
| D4 Tela de jogo lotado | Médio | E2 |
| D5 Troca de tela não anunciada | Médio | F1 |
| D6 Diálogo sem Esc | Médio | F2 |
| D7 Mensagens técnicas | Médio | E1 |
| D8 Botão de enviar longe | Médio | E3 |
| D9 Perfil longo | Médio | D4 |
| D10 Filtros ocupam a dobra | Médio | K2 |
| D11 Nomes diferentes | Médio | E6 |
| D12 Dois indicadores na barra | Médio | E4 |
| D13 Par de contraste | Médio | F4 |
| D14 Alvos de toque | Médio | F3, K3 |
| D15 Pontos menores | Baixo | D6, E5, F5 |
| C1 Login no convite público | Alto | D2, D3 |
| C2 Convidado não vira contato | Alto | I6 |
| C3 Sem analytics nem origem | Alto | G1, G2 |
| C4 Página de arenas sem o depois | Alto | E7 |
| C5 Prévia do link | Médio | E9 |
| C6 Convidado não compartilha | Médio | G4 |
| C7 Prova social | Médio | E8 |
| C8 SEO básico | Baixo | Sem requisito: não é o canal desta fase |
| F1 Intenção perdida | Alto | D1 |
| F2 Sem calendário | Alto | G3 |
| F3 Sem "marcar de novo" | Alto | I9 |
| F4 Sem pós-jogo | Alto | J2 |
| F5 Espera sem aviso | Alto | I5 |
| F6 Sugestão só para o time | Médio | K4 |
| F7 "Meus jogos" misturado | Baixo | I8 |
| F8 "Agora não" para sempre | Baixo | G5 |
| F9 Sem push nem e-mail | Médio | Fase 3 |
| M1 Piloto não testa a receita | Crítico | E7, J5 |
| M2 Jogo fechado não auditável | Alto | B1, J1, J2, J4 |
| M3 Jogo sem vínculo com a arena | Alto | J3 |
| M4 Premium promete o que não existe | Médio | E10, J8 |
| M5 Falta o valor aceitável | Médio | J5 |

---

## Apêndice A. Textos finais

Voz do produto conforme `DESIGN.md`: informal, segunda pessoa, frases curtas.

### Glossário (E6)

| Conceito | Termo único | Trocar |
|---|---|---|
| Tela de busca | **Procurar** | "Jogos abertos"; "Ver jogos abertos" vira "Procurar outro jogo" |
| Criar um jogo | **Marcar jogo** | "Marcar o meu jogo", "Marcar meu jogo" |
| Confirmar presença | **entrar no jogo** (botão "Tô dentro") | "check-in" |
| Quem criou o jogo | **quem organiza** | "dono", "quem marcou" em texto visível |
| Fila | **lista de espera** | "na espera" isolado |
| Equipe | **time** | "equipe" |
| Encerrar antes da hora | **cancelar** | "Apagar jogo" |

### Landing

- Prova social: "Perguntamos em 3 canais: **28 de 36 respostas dizem que a pessoa perdeu jogo por falta de gente** nas últimas 4 semanas. Formulário e 2 grupos de WhatsApp, nov/2026."
- "Tem vaga agora", vazio: "Ainda não tem jogo aberto. Marque o primeiro e chame a galera." Botão: "Marcar jogo".
- Chamada para arenas: "A Energia Boa leva jogadores para os horários que não enchem. 30 dias grátis para testar."

### Procurar

- Sem resultado: "Nenhum jogo com esses filtros." Botões: "Marcar jogo de Tênis" e "Limpar filtros".
- Filtros recolhidos: "Mais filtros (2)".
- Sugestão: "Combina com você", "Quase: outro horário", "Quase: nível vizinho".

### Convite

- Navegador embutido, título: "Abra no navegador para entrar". Texto: "O WhatsApp não deixa entrar com o Google por aqui. Abra este convite no Chrome ou no Safari: é um toque." Botões: "Abrir no navegador" e "Copiar link". Apoio: "No iPhone: toque nos três pontinhos e em “Abrir no navegador”." Abaixo: "Já está no navegador? Entrar com Google".
- Nome vazio: "Escreva seu nome para entrar no jogo."
- Jogo privado, alternativa ao nome: "Ou entre com Google para poder sair do jogo sozinho depois."
- Jogo lotado, cabeçalho: "Esse jogo já fechou". Placar: "Time completo". Texto: "Dá para entrar na lista de espera. Se alguém desistir, quem organiza te chama, na ordem da lista." Botão: "Entrar na lista de espera".
- Na lista de espera: "Você está na lista de espera" e "Posição 1. Se abrir vaga, quem organiza te avisa. Vale deixar seu WhatsApp para ele te achar."
- Contato opcional, rótulo: "Seu WhatsApp (opcional)". Consentimento: "Quem organiza este jogo e o time da Energia Boa podem me chamar no WhatsApp sobre este e os próximos jogos. Posso pedir para sair quando quiser." Botão: "Salvar". Depois: "Pronto. A gente te chama."
- Chamar mais gente: "Faltam 2 pra fechar. Chama alguém?" Botão: "Chamar mais gente".
- Calendário: "Adicionar ao calendário" e "Abrir no Google Agenda".
- Cancelado, título: "Esse jogo foi cancelado". Texto: "Quem organizou cancelou este jogo. Quer achar outro do seu nível?" Botão: "Procurar outro jogo".
- Já começou: "Esse jogo já começou". Texto: "Não dá mais para entrar por aqui. Fale com quem te convidou." Botão: "Procurar outro jogo".

### Jogo de quem organiza

- Abaixo do placar: "Faltam 2. Mande o link nos seus grupos." Botão: "Enviar no WhatsApp".
- Origem do link: "De qual grupo é este link? (opcional)".
- Aviso de vaga: "Bia entrou agora" e botão "Avisar Bia que abriu vaga".
- Presença, título: "Quem foi?" Texto: "Marque quem apareceu. Isso ajuda a montar jogos melhores." Botão: "Salvar presença". Depois: "Presença salva" e "3 de 4 foram".
- Editar: botão "Editar jogo". Com confirmados: "Já tem 3 pessoas no jogo. Avise a mudança." Botão: "Avisar no WhatsApp". Erro: "Já tem 3 pessoas no jogo. O total não pode ser menor."
- Cancelar, botão: "Cancelar jogo". Diálogo: "Cancelar este jogo?" e "3 pessoas confirmaram. Avise antes de cancelar: o link continua aberto e mostra que o jogo foi cancelado." Botões: "Avisar o grupo no WhatsApp", "Cancelar o jogo" e "Voltar". Aviso: "Jogo cancelado".
- Marcar de novo: "Marcar de novo na próxima semana". Depois: "Chamar quem jogou".

### Perfil (primeiro acesso)

- Título: "Só o básico pra começar". Texto: "Nome, cidade, esporte e nível. O resto você completa depois."
- Botões: "Salvar e continuar" e "Preencher depois".
- Erros: "Escreva seu nome." / "Escreva sua cidade." / "Escolha pelo menos um esporte." / "Escolha seu nível."

### Marcar jogo

- Erros: "Escolha o dia e a hora." / "Esse horário já passou. Escolha um que ainda vai acontecer." / "Escreva o nome do local." / "Escreva a cidade." / "Escolha o nível do jogo." / "O total vai de 2 a 30 pessoas." / "Tem que sobrar pelo menos 1 vaga." / "O preço é só número. Deixe vazio se não souber."

### Erros (E1)

| Situação | Texto |
|---|---|
| Login cancelado | "Login cancelado. Toque de novo para entrar." |
| Popup bloqueado | "O navegador bloqueou a janela do Google. Abra este link no Chrome ou no Safari e tente de novo." |
| Domínio não autorizado, login desligado ou erro desconhecido | "Não deu para entrar agora. Tente de novo daqui a pouco." |
| Sem internet | "Sem internet. Tente de novo." |
| Sem permissão, jogador | "Você não pode fazer isso neste jogo." |
| Sem permissão, time | "Sua conta não tem acesso a isso. Fale com quem cuida do time." |
| Falha ao carregar uma lista do time | "Não consegui carregar essa lista. Recarregue a página." |
| Importação da base | "Use o arquivo .json gerado a partir das respostas do formulário. Quem já está na base é atualizado, sem duplicar." |

### Arenas (E7)

- Oferta com preço: "30 dias grátis para testar. Depois, **{{PRECO_POS_PILOTO}}** por jogo fechado em horário que você marcou como vazio. Sem jogo fechado, você não paga nada. Você não troca de sistema, e a Energia Boa não mexe na sua agenda."
- Oferta sem preço configurado: "30 dias grátis para testar. O valor depois do piloto é combinado por escrito antes de começar. Você não troca de sistema, e a Energia Boa não mexe na sua agenda."
- Nota do formulário: "Só o time da Energia Boa vê esses dados. Pedir o piloto não gera cobrança: a gente combina tudo por escrito antes de qualquer valor."
- Depois de enviar: "Pedido recebido! A gente te chama no WhatsApp para combinar os horários." O prazo de resposta é do time; não prometer um sem confirmar.
- Ressalva da pesquisa: "São respostas de um formulário e de 2 grupos de WhatsApp, com perguntas parecidas mas não iguais. A mesma pessoa pode ter respondido em mais de um lugar."

### Premium (J8)

- Selo: "Queremos saber". Título: "O que valeria pagar?"
- Texto: "Hoje a Energia Boa é grátis. Antes de criar um plano pago, a gente quer ouvir você."
- Opções (uma ou mais): "Lembrete e aviso de vaga no WhatsApp" / "Jogo garantido: quem fura paga" / "Achar gente do meu nível mais rápido" / "Nada, prefiro grátis".
- Botão: "Enviar resposta". Depois: "Valeu! Sua resposta ajuda a decidir o que vem." Nota: "Ninguém é cobrado. Não é uma lista de compra."

### Mensagens de WhatsApp (I10)

Datas e horas no formato de `quandoTexto()`, que já existe.

- Aviso de vaga: "Oi, Bia! Abriu vaga no jogo de vôlei de praia de sábado, 21/11, às 18h, na Reis D'arena. A vaga é sua. Confirma aqui: <link>. Se não der, me avisa que eu chamo o próximo."
- Cancelamento: "Pessoal, o jogo de vôlei de praia de sábado, 21/11, às 18h, na Reis D'arena foi cancelado. Desculpa o transtorno! Quando eu marcar outro, mando o link."
- Mudança: "Pessoal, mudou o jogo de vôlei de praia: agora é sábado, 21/11, às 19h, na Reis D'arena. Quem não puder mais, me avisa. Detalhes: <link>."
- Marcar de novo: "Bora de novo? Marquei vôlei de praia para sábado, 28/11, às 18h, na Reis D'arena. Confirma aqui: <link>."
- Chamar mais gente: "Vou jogar vôlei de praia sábado, 21/11, às 18h, na Reis D'arena. Faltam 2 pra fechar. Bora? <link>"

### Prévia do link, sistema e privacidade

- `og:description`: "Falta gente pro seu jogo? Veja o jogo e entre em um toque." `og:image:alt`: "Energia Boa: falta gente pro seu jogo?"
- `<noscript>`: "A Energia Boa precisa de JavaScript para funcionar. Ative o JavaScript no navegador e recarregue a página."
- Instalação depois da primeira confirmação: "Seus jogos a um toque: instale a Energia Boa na tela inicial."
- Privacidade: "Contamos quantas vezes cada tela é aberta e de qual link a visita veio, para saber o que funciona. Não usamos cookies de propaganda e não ligamos essa contagem ao seu nome nem ao seu WhatsApp."

### Títulos por tela (F1)

| Rota | Título da aba |
|---|---|
| início | "Energia Boa: falta gente pro seu jogo?" |
| `#jogos` | "Procurar jogos · Energia Boa" |
| `#convite-<id>` | "<Esporte>, <dia e hora> · Energia Boa" |
| `#jogo-<id>` | "Seu jogo de <esporte> · Energia Boa" |
| `#novo` | "Marcar jogo · Energia Boa" |
| meus jogos | "Meus jogos · Energia Boa" |
| `#perfil` | "Perfil · Energia Boa" |
| painel | "Painel · Energia Boa" |
| `#jogadores` | "Jogadores · Energia Boa" |
| `#arenas` | "Para arenas · Energia Boa" |
| `#premium` | "O que valeria pagar? · Energia Boa" |
| `#privacidade` | "Privacidade e segurança · Energia Boa" |

### Eventos (G2)

Nenhum evento carrega nome, telefone, e-mail ou identificador de conta.

| Evento | Quando dispara | Propriedades |
|---|---|---|
| `convite_aberto` | O convite termina de carregar | origem, visibilidade, estado, navegador embutido |
| `login_iniciado`, `login_concluido`, `login_falhou` | Em cada tentativa | tela de origem, navegador embutido, motivo resumido |
| `confirmacao_feita` | A confirmação é gravada | origem, com ou sem conta, no jogo ou na espera |
| `desistencia_feita` | A pessoa sai do jogo | horas até o jogo |
| `jogo_marcado` | Um jogo é criado | origem, esporte, visibilidade, tipo de local, se veio de "marcar de novo" |
| `jogo_fechado` | A última vaga é preenchida | horas desde a criação |
| `compartilhamento_feito` | Toque em enviar ou copiar | quem, meio |
| `calendario_adicionado` | Toque em calendário | tipo |
| `presenca_salva` | Quem organiza salva a presença | confirmados, presentes |
| `piloto_pedido` | Envio do formulário de arena | origem, modelo escolhido |

---

## Apêndice B. Regras propostas e casos de teste

**Nenhum trecho foi executado.** A sintaxe não foi conferida contra a documentação. Quatro pontos precisam ser confirmados no emulador (A5) antes de qualquer publicação:

- comparação de `request.time` com um campo de data somado a `duration.value(...)`;
- regra de `list` que depende de `resource.data` (a consulta precisa ter o mesmo filtro);
- consulta de grupo de coleções autorizada pela regra `{path=**}`;
- `let` e o operador ternário dentro de função, junto com `diff().affectedKeys()`.

Os casos "negado" e "permitido" de cada requisito estão nas tabelas das seções 5 e 6.

### Fase 1 (a coleção `confirmacoes` continua na raiz)

**B1: hora do servidor.** Na regra de transição, cada linha abaixo vem com `|| request.resource.data.criadoEm is number`; na regra estrita, sem.

```
// confirmacaoPublicaValida: no lugar de "criadoEm is number"
&& request.resource.data.criadoEm == request.time

// confirmacaoDoDonoValida: acrescentar
&& request.resource.data.keys().hasAll(['jogoId', 'nome', 'via', 'criadoEm'])
&& request.resource.data.criadoEm == request.time

// jogoDeJogadorValido e arenas_piloto: acrescentar
&& request.resource.data.criadoEm == request.time
```

**B3 e B4: faixas, formatos e data do jogo.**

```
function camposDoJogoValidos() {
  let d = request.resource.data;
  return d.arena is string && d.arena.size() >= 2 && d.arena.size() <= 80
    && d.nivel in [1, 3, 5]
    && d.quando is string
    && d.quando.matches('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$')
    && d.quandoTs is timestamp
    && d.quandoTs > request.time - duration.value(30, 'm')
    && d.quandoTs < request.time + duration.value(365, 'd')
    && d.total is int && d.total >= 2 && d.total <= 30
    && d.vagas is int && d.vagas >= 1 && d.vagas <= d.total
    && d.get('tipoLocal', 'privada') in ['publica', 'privada']
    && (d.valor == null || (d.valor is number && d.valor >= 0 && d.valor <= 1000))
    && (d.get('tipoLocal', 'privada') != 'publica' || d.valor == null);
}
// jogoDeJogadorValido: incluir 'quandoTs' na lista de chaves e chamar camposDoJogoValidos()

// confirmacaoPublicaValida: só até o início (jogos antigos sem quandoTs continuam aceitando)
&& (!('quandoTs' in get(/databases/$(database)/documents/jogos/$(request.resource.data.jogoId)).data)
    || request.time < get(/databases/$(database)/documents/jogos/$(request.resource.data.jogoId)).data.quandoTs)

// perfilValido: acrescentar
&& request.resource.data.nivel in [1, 3, 5]

// arenas_piloto: no lugar das duas linhas de vazios e preco
&& (request.resource.data.vazios == null
    || (request.resource.data.vazios is number && request.resource.data.vazios >= 0 && request.resource.data.vazios <= 200))
&& (request.resource.data.preco == null
    || (request.resource.data.preco is number && request.resource.data.preco >= 0 && request.resource.data.preco <= 1000))
```

**B6: time.**

```
match /admins/{uid} {
  allow read: if request.auth != null && (request.auth.uid == uid || ehEquipe());
  allow create: if request.auth != null && request.auth.uid == uid
    && request.resource.data.keys().hasOnly(['nome', 'codigo', 'criadoEm'])
    && request.resource.data.nome is string && request.resource.data.nome.size() <= 60
    && request.resource.data.codigo is string && request.resource.data.codigo.size() == 6
    && request.resource.data.criadoEm == request.time
    && exists(/databases/$(database)/documents/config/equipe)
    && request.resource.data.codigo == get(/databases/$(database)/documents/config/equipe).data.codigo;
  allow update: if false;
  allow delete: if ehEquipe();
}
```

**B7: identificador.**

```
// em match /jogos/{id}
allow create: if ehEquipe() || (jogoDeJogadorValido() && id.matches('^[A-Za-z0-9]{20}$'));
```

### Fase 2 (substitui os blocos de `jogos`, `contato` e `confirmacoes`)

**H3, I1, I4, J3, J4: jogo.**

```
function jogoDeJogadorValido() {
  let d = request.resource.data;
  return request.auth != null
    && d.keys().hasOnly(['arena', 'esporte', 'nivel', 'quando', 'quandoTs', 'total', 'vagas', 'valor',
         'situacao', 'teste', 'criadoEm', 'donoUid', 'donoNome', 'origem', 'visibilidade',
         'cidade', 'cidadeChave', 'tipoLocal', 'estado', 'arenaId', 'copiadoDe', 'origemLink'])
    && d.donoUid == request.auth.uid && d.origem == 'jogador' && d.teste == false
    && d.estado == 'aberto' && d.criadoEm == request.time
    && d.visibilidade in ['publico', 'privado']
    && d.situacao in ['vago', 'cancelar']
    && d.esporte is string && d.esporte.size() <= 40
    && d.donoNome is string && d.donoNome.size() <= 60
    && (!('arenaId' in d) || exists(/databases/$(database)/documents/arenas/$(d.arenaId)))
    && camposDoJogoValidos();
}

function donoAtualizaJogo() {
  let muda = request.resource.data.diff(resource.data).affectedKeys();
  return request.auth != null && resource.data.donoUid == request.auth.uid
    && resource.data.estado == 'aberto'
    && muda.hasOnly(['arena', 'cidade', 'cidadeChave', 'quando', 'quandoTs', 'total', 'vagas',
         'valor', 'nivel', 'tipoLocal', 'estado', 'canceladoEm', 'atualizadoEm'])
    && request.resource.data.atualizadoEm == request.time
    && (!muda.hasAny(['valor']) || resource.data.get('valorConfirmado', false) == false)
    && (request.resource.data.estado == 'cancelado'
        ? request.resource.data.canceladoEm == request.time
        : (request.resource.data.estado == 'aberto'
           && request.time < resource.data.quandoTs
           && camposDoJogoValidos()));
}

match /jogos/{id} {
  allow get: if true;
  allow list: if ehEquipe()
    || resource.data.visibilidade == 'publico'
    || (request.auth != null && resource.data.donoUid == request.auth.uid);
  allow create: if ehEquipe() || (jogoDeJogadorValido() && id.matches('^[A-Za-z0-9]{20}$'));
  allow update: if ehEquipe() || donoAtualizaJogo();
  allow delete: if ehEquipe();
}

match /arenas/{aid} {
  allow read: if true;            // só nome, cidade e se está ativa
  allow write: if ehEquipe();
  match /privado/{doc} {
    allow read, write: if ehEquipe();
  }
}
```

No trecho acima, o campo `origemLink` guarda a origem do link (G1); o campo `origem` já existe e distingue jogo marcado por jogador de jogo marcado pelo time. Os campos `realizado`, `valorConfirmado`, `horarioVazio` e `teste` não estão na lista do dono: só o time os grava.

**H4, I3, J2, G1: confirmações.**

```
function jogoAbertoEAntesDoInicio(id) {
  let j = get(/databases/$(database)/documents/jogos/$(id)).data;
  return j.estado == 'aberto' && request.time < j.quandoTs;
}

function confirmacaoPorLink(id, cid) {
  let d = request.resource.data;
  let j = get(/databases/$(database)/documents/jogos/$(id)).data;
  return d.keys().hasOnly(['nome', 'via', 'criadoEm', 'estado', 'uid', 'origem'])
    && d.keys().hasAll(['nome', 'via', 'criadoEm', 'estado'])
    && d.via == 'link' && d.estado == 'confirmado'
    && d.nome is string && d.nome.size() >= 2 && d.nome.size() <= 40
    && d.criadoEm == request.time
    && (!('origem' in d) || (d.origem is string && d.origem.matches('^[a-z0-9-]{1,40}$')))
    && ('uid' in d
        ? (request.auth != null && d.uid == request.auth.uid && cid == request.auth.uid)
        : (j.visibilidade != 'publico' && cid.matches('^[A-Za-z0-9]{20}$')))
    && j.estado == 'aberto' && request.time < j.quandoTs;
}

function confirmacaoDoDono(id) {
  let d = request.resource.data;
  return ehDonoDoJogo(id)
    && d.keys().hasOnly(['nome', 'via', 'criadoEm', 'estado'])
    && d.keys().hasAll(['nome', 'via', 'criadoEm', 'estado'])
    && d.via == 'whatsapp' && d.estado == 'confirmado'
    && d.nome is string && d.nome.size() >= 2 && d.nome.size() <= 40
    && d.criadoEm == request.time;
}

function desiste() {
  let muda = request.resource.data.diff(resource.data).affectedKeys();
  return request.auth != null && resource.data.get('uid', '') == request.auth.uid
    && resource.data.estado == 'confirmado'
    && muda.hasOnly(['estado', 'saiuEm'])
    && request.resource.data.estado == 'desistiu'
    && request.resource.data.saiuEm == request.time;
}

function volta(id) {
  let muda = request.resource.data.diff(resource.data).affectedKeys();
  return request.auth != null && resource.data.get('uid', '') == request.auth.uid
    && resource.data.estado == 'desistiu'
    && muda.hasOnly(['estado', 'criadoEm'])
    && request.resource.data.estado == 'confirmado'
    && request.resource.data.criadoEm == request.time
    && jogoAbertoEAntesDoInicio(id);
}

function donoRetira(id) {
  let muda = request.resource.data.diff(resource.data).affectedKeys();
  return ehDonoDoJogo(id)
    && muda.hasOnly(['estado', 'saiuEm'])
    && request.resource.data.estado == 'removido'
    && request.resource.data.saiuEm == request.time;
}

function donoMarcaPresenca(id) {
  let muda = request.resource.data.diff(resource.data).affectedKeys();
  let j = get(/databases/$(database)/documents/jogos/$(id)).data;
  return request.auth != null && j.donoUid == request.auth.uid
    && resource.data.estado == 'confirmado'
    && muda.hasOnly(['presente', 'presencaEm'])
    && request.resource.data.presente is bool
    && request.resource.data.presencaEm == request.time
    && request.time > j.quandoTs
    && request.time < j.quandoTs + duration.value(7, 'd');
}

match /jogos/{id}/confirmacoes/{cid} {
  allow read: if true;                       // só alcança quem já conhece o id do jogo
  allow create: if ehEquipe() || confirmacaoPorLink(id, cid) || confirmacaoDoDono(id);
  allow update: if ehEquipe() || desiste() || volta(id) || donoRetira(id) || donoMarcaPresenca(id);
  allow delete: if ehEquipe();
}

// Consulta entre jogos ("Meus jogos" e painel do time)
match /{path=**}/confirmacoes/{cid} {
  allow list: if ehEquipe()
    || (request.auth != null && resource.data.uid == request.auth.uid);
}
```

**H6: contato de quem organiza.**

```
match /jogos/{id}/contato/{doc} {
  allow read: if ehEquipe() || ehDonoDoJogo(id)
    || (request.auth != null
        && exists(/databases/$(database)/documents/jogos/$(id)/confirmacoes/$(request.auth.uid))
        && get(/databases/$(database)/documents/jogos/$(id)/confirmacoes/$(request.auth.uid)).data.estado == 'confirmado');
  allow create, update: if ehEquipe() || (ehDonoDoJogo(id)
    && request.resource.data.keys().hasOnly(['zap'])
    && request.resource.data.zap is string
    && request.resource.data.zap.matches('^(55[0-9]{10,11})?$'));
  allow delete: if ehEquipe() || ehDonoDoJogo(id);
}
```

**I6: contato opcional do convidado.** Este trecho foi escrito na síntese, para conciliar o pedido de design (quem organiza precisa do contato para avisar a vaga) com o de segurança (o telefone não pode ficar na confirmação, que é legível por quem tem o link). Precisa da mesma revisão no emulador.

```
match /jogos/{id}/contatos/{cid} {
  allow read: if ehEquipe() || ehDonoDoJogo(id);
  allow create: if request.resource.data.keys().hasOnly(['whatsapp', 'consentiu', 'criadoEm'])
    && request.resource.data.whatsapp.matches('^55[0-9]{10,11}$')
    && request.resource.data.consentiu == true
    && request.resource.data.criadoEm == request.time
    && exists(/databases/$(database)/documents/jogos/$(id)/confirmacoes/$(cid));
  allow update: if false;
  allow delete: if ehEquipe() || ehDonoDoJogo(id);
}
```

Limite conhecido deste trecho: quem conhece o identificador de uma confirmação sem conta consegue gravar um telefone para ela. O dano é um número errado na lista de quem organiza; não há leitura indevida.

**J5 e J8: chaves novas.** `arenas_piloto` passa a aceitar `valorAceitavel` (número de 0 a 1.000, opcional) na criação; a situação da oferta é gravada pelo time, que já pode atualizar o documento. `interesse_premium` passa a aceitar `respostas` (lista de até 4 textos).

**C1, C2, C3 e H8** não têm regra: são configuração do console e código do cliente.
