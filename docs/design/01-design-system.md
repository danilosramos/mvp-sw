# Design system da Energia Boa

**Base: a logo do time** (cavalo e raio, feita pelo designer da equipe). Todas as cores saem dela, medidas nos pixels da arte: fundo roxo-noite, roxo elétrico, limão e branco. O app usa tema escuro único porque a logo foi desenhada para fundo escuro, e o limão e o roxo só acendem sobre ele.

A arte original está em `icons/logo-energia-boa.png`. No app ela aparece recortada, sem o fundo, em duas peças: a marca (`icons/marca.png`) e o nome (`icons/palavra.png`). O cabeçalho junta as duas na horizontal, sobre o mesmo roxo-noite da logo.

## 1. Princípios

1. **A logo manda.** Cores, peso da fonte e tom vêm dela. Não redesenhamos a marca: só tiramos o fundo e montamos a versão horizontal.
2. **Limão é energia e ação:** botão principal, números do placar, foco do teclado e a linha embaixo do cabeçalho. Um alvo que difere dos vizinhos em uma só característica é achado sem busca (Treisman e Gelade, 1980).
3. **Roxo elétrico é seleção e marca:** filtros marcados, opção escolhida e o canhoto da data nos cartões.
4. **O placar é o elemento ousado:** números grandes em limão sobre o roxo mais escuro. Quando o jogo fecha, o placar inteiro vira limão.
5. **Branco para o segundo botão** (Marcar jogo), para não competir com o limão.
6. **Palavras simples, em frase.** Só a marca é escrita em caixa-alta.

## 2. Cores

| Token | Hex | Uso |
|---|---|---|
| `bg` (roxo-noite, fundo da logo) | `#1F0733` | Fundo da página, cabeçalho, fundo dos campos |
| `surface` | `#2A0F45` | Cartões, barra de navegação |
| `ink` | `#FBF7FF` | Texto |
| `muted` | `#CDB9EA` | Texto de apoio |
| `link` | `#DDB0FF` | Links e rótulos curtos |
| `roxo` (elétrico, da logo) | `#A925E6`, texto branco | Seleção, canhoto da data |
| `roxo-profundo` (da logo) | `#611098` | Quadra do início, avatar |
| `roxo-medio` (da logo) | `#891BC9` | Confete |
| `cta` (limão, do raio) | `#A9F809`, texto `#1F0733` | Ação principal, placar, foco, barras de progresso |
| `limao-claro` (da logo) | `#D2FC88` | Confete |
| `sec` | `#FFFFFF`, texto `#1F0733` | Segundo botão |
| `placar` | `#12041F` | Placar, mini placar, números grandes do painel |
| `line` / `line-forte` | `#46256B` / `#9A7CC4` | Divisórias / bordas de campos e chips |
| `ok` | `#C8FF5E` sobre `#263B0B` | Confirmado, pedido recebido |
| `warn` | `#FFC857` sobre `#3B2A0C` | Avisos |
| `zap` | `#25D366`, texto `#052E16` | Só botões que abrem o WhatsApp |
| `danger` | `#FF8A8A` | Apagar, erro |

### Contraste medido (WCAG 2.2: texto 4,5:1; bordas e gráficos 3:1)

Para medir de novo: `python3 tests/contraste.py`.

| Par | Razão |
|---|---|
| Texto sobre o fundo / sobre a superfície | 17,5:1 / 15,9:1 |
| Apoio e link sobre a superfície | 9,4:1 |
| Branco sobre roxo elétrico (seleção, canhoto) | 5,1:1 |
| Roxo-noite sobre limão (botão principal, placar fechado) | 14,2:1 |
| Roxo-noite sobre branco (segundo botão) | 18,5:1 |
| Branco sobre roxo profundo (quadra do início) | 10,3:1 |
| Limão sobre o placar | 15,2:1 |
| Chip de nível | 11,0:1 |
| Verde sobre fundo de sucesso / âmbar sobre fundo de aviso | 10,5:1 / 9,0:1 |
| Texto escuro sobre o verde do WhatsApp | 7,5:1 |
| Borda de campo sobre a superfície | 4,8:1 |
| Barra limão sobre o trilho | 10,5:1 |
| Foco limão sobre o fundo | 14,2:1 |

## 3. Tipografia

| Família | Onde | Por quê |
|---|---|---|
| **Montserrat 800** | Títulos, números do placar, canhoto da data, rótulos dos botões grandes | Geométrica e pesada como o nome na logo |
| **Barlow 400, 600 e 700** | Texto, campos e botões | Lê bem em 17 px no celular e não briga com a Montserrat |

- As fontes são servidas pelo próprio app (licença SIL OFL, em `fonts/`), sem chamar o Google: menos dados de quem usa saindo para terceiros, e o app abre sem internet.
- Escala: 12,5 / 15 / 17 (corpo) / 20 / 21 / 26 / 30 / 34, e 76 no placar. Entrelinha 1,5 no corpo. Nada essencial abaixo de 12,5 px (Legge e Bigelow, 2011).
- Horários, preços e vagas usam algarismos tabulares.
- Coluna de até 600 px.

## 4. Tokens de forma

| Grupo | Valores |
|---|---|
| Espaço | `--s1` 4, `--s2` 8, `--s3` 12, `--s4` 16, `--s5` 24, `--s6` 32 |
| Raio | `--r-sm` 8 (campos, chips de dia), `--r-md` 12 (botões, cartões de jogo), `--r-lg` 18 (quadra, placar, cartões), `--r-full` (chips) |
| Sombra | Só a barra de navegação do celular. Cartões se separam por borda de 1 px |
| Toque | `--toque` 48 px; chips de filtro 44 px; navegação 56 px |
| Navegação | Abaixo de 720 px, desce para a base da tela; acima, fica no cabeçalho |

## 5. Componentes

| Componente | Regra |
|---|---|
| Cabeçalho | Logo horizontal (marca e nome) sobre o roxo-noite, com a linha limão de 3 px embaixo |
| Navegação | **Procurar** é sempre o primeiro destino. No celular, o ícone fica numa pílula limão; no computador, vira o botão limão "Procurar jogos". A aba atual fica limão, com uma barra curta no topo |
| Quadra (abertura) | Roxo profundo com a linha limão da quadra. Título grande e as duas ações |
| Ação dupla | **Procurar jogo** (limão) e **Marcar jogo** (branco), ícone em cima e rótulo em duas linhas |
| Cartão de jogo | Canhoto roxo com dia, número e hora; no meio, esporte, nível, lugar e situação; à direita, o mini placar com as vagas |
| Mini placar | Roxo mais escuro com o número em limão. Fica limão com "Fechou" quando completa |
| Placar | Número de 76 px em limão, barra limão e o estado em palavras. Vira limão por inteiro quando o jogo fecha, com confete nas cores da logo |
| Filtros da busca | Esporte, dia da semana (7 botões) e período do dia (manhã 5h–12h, tarde 12h–18h, noite a partir das 18h) à vista. O resto em "Mais filtros (N)". O que está filtrado aparece em uma frase, com "Limpar filtros" |
| Nível | Três opções com nome e descrição: Iniciante, Intermediário, Avançado. Uma por linha no celular |
| Campos | Fundo roxo-noite, rótulo visível acima, borda de 1,5 px que fica limão no foco, erro em texto no fim do formulário |
| Botão do WhatsApp | Verde próprio, só para abrir o WhatsApp |

Estados de todo botão: foco visível (contorno limão de 3 px), pressionado (leve redução), processando (desabilitado com indicador girando), sucesso (aviso curto na base) e erro (o que houve e o que fazer).

## 6. Movimento

Só o que responde a uma ação: a barra de vagas que enche, o placar que pulsa e o confete quando o jogo fecha. Com "reduzir movimento" ligado, nada disso roda.

## 7. Marca e ícones

- A logo é usada como o designer entregou. O fundo foi removido por cor (a cor do fundo foi medida na arte), com borda suave, para a marca ficar limpa sobre qualquer roxo escuro do app. Sobre fundo claro ela não deve ser usada: os contornos brancos somem.
- Ícones do app (192, 512, maskable e Apple) e favicon: a marca sobre o roxo-noite. No maskable, a marca fica dentro da área segura.

## 8. Princípios de cognição aplicados

| Decisão na interface | Princípio | Referência |
|---|---|---|
| Procurar e Marcar como blocos grandes no topo, e Procurar como primeiro destino da navegação | Alvos maiores e mais próximos são atingidos mais rápido | Fitts (1954) |
| Esporte, dia e período à vista; o resto em "Mais filtros" | O tempo de decisão cresce com o número de opções | Hick (1952); Hyman (1953) |
| Três níveis com nome em vez de números de 1 a 5 | Reconhecer custa menos que lembrar o que cada número significa | Nielsen (1994); Sweller (1988) |
| Mini placar com "1 vaga" e barra quase cheia | O esforço aumenta perto da meta | Kivetz, Urminsky e Zheng (2006) |
| "Já confirmaram: Ana, Beto" | Pessoas seguem o que outras parecidas fizeram | Cialdini (2009) |
| Limão só na ação principal e no placar | Um traço distinto é achado sem busca | Treisman e Gelade (1980) |
| Frase "Filtrando por…" e "Limpar filtros" | Visibilidade do estado do sistema | Nielsen (1994) |
| Confirmar antes de apagar ("toque de novo") | Prevenção de erro | Nielsen (1994) |
| Alvos de pelo menos 44 px | Tamanho de alvo | WCAG 2.2, critério 2.5.8 |

O que **não** afirmamos: que alguma cor "gera confiança" ou "libera dopamina". Os efeitos de cor existem, mas são pequenos e dependem de contexto (Elliot e Maier, 2014).

## 9. Voz

Informal e de convite: "Falta 1 pro seu jogo", "Tô dentro", "Você não joga sozinho". O botão diz o que acontece ("Procurar jogo", "Marcar e pegar o link", "Entrar na lista de espera"). "Fechou!" é o estado do jogo completo, não o nome do app. A palavra solidão não aparece no app: fica no pitch.

## 10. Referências

- Cialdini, R. (2009). *Influence: Science and Practice*.
- Elliot, A. J., e Maier, M. A. (2014). Color psychology: effects of perceiving color on psychological functioning in humans. *Annual Review of Psychology*, 65.
- Fitts, P. M. (1954). The information capacity of the human motor system in controlling the amplitude of movement. *Journal of Experimental Psychology*, 47(6).
- Hick, W. E. (1952). On the rate of gain of information. *Quarterly Journal of Experimental Psychology*, 4(1).
- Hyman, R. (1953). Stimulus information as a determinant of reaction time. *Journal of Experimental Psychology*, 45(3).
- Kivetz, R., Urminsky, O., e Zheng, Y. (2006). The goal-gradient hypothesis resurrected. *Journal of Marketing Research*, 43(1).
- Legge, G. E., e Bigelow, C. A. (2011). Does print size matter for reading? *Journal of Vision*, 11(5).
- Nielsen, J. (1994). 10 usability heuristics for user interface design. Nielsen Norman Group.
- Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*, 12(2).
- Treisman, A., e Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, 12(1).
- W3C (2023). Web Content Accessibility Guidelines 2.2.
