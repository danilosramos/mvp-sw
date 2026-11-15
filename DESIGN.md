# Design system da Energia Boa

**Ideia: a quadra de areia vista de cima.** A cor cobalto vem da fita que marca a quadra, o amarelo vem do sol e a areia vem da própria quadra. O placar mostra quantas vagas faltam. Tudo isso é do mundo de quem joga vôlei de praia, futevôlei e beach tennis na região de Araranguá. "Energia" está no contraste forte entre cobalto e sol; "Boa" está na areia, nos cantos suaves e na voz do texto.

O que evitamos de propósito, porque é o visual de qualquer app de "boa vibe": degradê de pôr do sol, fonte arredondada, sol sorrindo e fundo creme. Também evitamos o kit de cartões iguais com a mesma sombra e os rótulos em caixa-alta. Cada escolha se justifica por função; onde há pesquisa, a referência está no fim.

## 1. Princípios

1. **O placar é o elemento ousado.** Os números de vagas aparecem grandes, condensados e em itálico, amarelos sobre azul-noite. É o único lugar com esse tratamento; o resto da tela fica quieto.
2. **Amarelo (sol) só na ação principal e nos números do placar.** Um alvo que difere dos vizinhos em uma só característica é achado sem busca (Treisman e Gelade, 1980). Na tela inicial e em Meus jogos há duas intenções de mesmo peso: **Procurar jogo** (sol, a mais saliente) e **Marcar jogo** (cobalto).
3. **Cobalto é marca, navegação e seleção:** cabeçalho, links, filtros e opções marcadas.
4. **Areia só onde é quadra:** o bloco de abertura (com a linha branca da quadra) e o canhoto da data nos cartões de jogo.
5. **Verde só quando o jogo fecha.**
6. **Palavras simples, em frase.** Só a marca é escrita em caixa-alta.

## 2. Cores

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `ink` (noite) | `#0E1B3D` | `#EEF2FF` | Texto |
| `muted` | `#4A5675` | `#A8B3D6` | Texto de apoio |
| `bg` (nuvem) | `#F3F5FA` | `#0A1330` | Fundo da página |
| `surface` | `#FFFFFF` | `#111C3F` | Cartões, formulários, barra de navegação |
| `accent` (cobalto) | `#1B4FE0` | `#8CAEFF` | Links, seleção, botão secundário |
| `topo` | `#1B4FE0` | `#1A3FB8` | Cabeçalho, com a fita amarela de 4 px embaixo |
| `cta` (sol) | `#FFC928`, texto `#0E1B3D` | igual | Ação principal |
| `areia` | `#F1DDAE`, linha `#FFFFFF` | igual | Quadra de abertura, canhoto da data |
| `placar` | `#0E1B3D`, número `#FFC928` | `#050B22` | Placar, mini placar, números grandes do painel |
| `placar-ok` | `#0B6B3A` | igual | Placar quando o jogo fecha |
| `ok` | `#0E7A44` sobre `#DDF6E8` | `#6FE0A6` sobre `#12392A` | Confirmado, pedido recebido |
| `warn` | `#8A4B00` sobre `#FFF0C4` | `#F6C766` sobre `#3A2C0F` | Avisos |
| `zap` | `#0F7A43`, texto branco | `#36C877`, texto `#04140B` | Só botões que abrem o WhatsApp |
| `danger` | `#B42318` | `#FF8A80` | Apagar, erro |
| `coral` | `#FF5A36` | igual | Só decoração (confete). Nunca texto |

A areia fica clara também no tema escuro: a quadra acesa sobre o azul-noite. O tema escuro acompanha a preferência do aparelho.

### Contraste medido (WCAG 2.2: texto 4,5:1; bordas e gráficos 3:1)

| Par | Razão |
|---|---|
| Texto sobre branco / sobre o fundo | 16,9:1 / 15,5:1 |
| Apoio sobre branco / sobre areia | 7,3:1 / 5,5:1 |
| Link cobalto sobre branco / sobre areia | 6,5:1 / 4,8:1 |
| Branco sobre cobalto (cabeçalho, botão) | 6,5:1 |
| Texto sobre sol (botão principal) | 11,0:1 |
| Número amarelo sobre o placar | 11,0:1 |
| Branco sobre o placar verde | 6,6:1 |
| Verde sobre fundo de sucesso / âmbar sobre fundo de aviso | 4,7:1 / 6,0:1 |
| Branco sobre o verde do WhatsApp | 5,4:1 |
| Borda de campo sobre branco | 3,5:1 |
| Foco amarelo sobre o cabeçalho cobalto | 4,2:1 |
| Escuro: texto, apoio e link sobre a superfície | 14,9:1, 8,0:1 e 7,6:1 |
| Escuro: texto sobre o chip cobalto marcado | 8,4:1 |

Para medir de novo: `python3 tests/contraste.py`.

## 3. Tipografia

| Família | Onde | Por quê |
|---|---|---|
| **Barlow Condensed 700** | Títulos, canhoto da data, botões grandes de ação | Lembra placar e camisa de time; cabe "Procurar jogo" em letra grande no celular |
| **Barlow Condensed 800 itálico** | Marca e números do placar | O itálico dá movimento; só aparece em números grandes e na marca |
| **Barlow 400, 600 e 700** | Texto, campos e botões | Mesma família, largura normal, boa leitura em 17 px |

- Antes usamos Barlow Condensed e trocamos porque era estreita demais em texto pequeno. Agora a condensada só aparece a partir de 20 px, e o texto corre em Barlow de largura normal.
- As fontes são servidas pelo próprio app (licença SIL OFL, em `fonts/`), sem chamar o Google: menos dados de quem usa saindo para terceiros, e o app abre sem internet.
- Escala: 13 / 15 / 17 (corpo) / 21 / 24 / 30 / 36 / 44, e 88 no placar. Entrelinha 1,5 no corpo. Nada essencial abaixo de 13 px (Legge e Bigelow, 2011).
- Horários, preços e vagas usam algarismos tabulares.
- Coluna de até 600 px, linhas de no máximo 60 a 70 caracteres.

## 4. Tokens de forma

| Grupo | Valores |
|---|---|
| Espaço | `--s1` 4, `--s2` 8, `--s3` 12, `--s4` 16, `--s5` 24, `--s6` 32 |
| Raio | `--r-sm` 8 (campos, chips de dia), `--r-md` 12 (botões, cartões de jogo), `--r-lg` 18 (quadra, placar, painéis), `--r-full` (chips) |
| Sombra | Só a barra de navegação do celular. Cartões se separam por borda de 1 px, não por sombra |
| Toque | `--toque` 48 px; chips de filtro 44 px; navegação 56 px |
| Navegação | Abaixo de 720 px, desce para a base da tela; acima, fica no cabeçalho |

## 5. Componentes

| Componente | Regra |
|---|---|
| Cabeçalho | Cobalto com a marca em Barlow Condensed itálico e a fita amarela de 4 px embaixo |
| Navegação | **Procurar** é sempre o primeiro destino. No celular, o ícone fica numa pílula amarela; no computador, vira o botão amarelo "Procurar jogos". A aba atual ganha uma barra curta no topo |
| Quadra (abertura) | Areia com a linha branca da quadra. Título grande e as duas ações |
| Ação dupla | Dois blocos lado a lado: **Procurar jogo** (sol) e **Marcar jogo** (cobalto), ícone em cima e rótulo em duas linhas |
| Cartão de jogo | Canhoto de areia com dia, número e hora; no meio, esporte, nível, lugar e situação; à direita, o mini placar com as vagas |
| Mini placar | Azul-noite com o número amarelo de vagas. Verde com "Fechou" quando completa |
| Placar | Número de 88 px, barra amarela e o estado em palavras. Fica verde quando o jogo fecha, com confete |
| Filtros da busca | Esporte (fila que rola), dia da semana (7 botões), período do dia (manhã 5h–12h, tarde 12h–18h, noite a partir das 18h). O resto fica em "Mais filtros (N)". O que está filtrado aparece em uma frase, com "Limpar filtros" |
| Nível | Três opções com nome e descrição: Iniciante, Intermediário, Avançado. Uma por linha no celular |
| Chips | Cobalto quando marcados. O chip de nível tem fundo cobalto claro |
| Campos | Rótulo sempre visível acima, borda de 1,5 px com contraste 3,5:1, erro em texto no fim do formulário |
| Botão do WhatsApp | Verde próprio, só para abrir o WhatsApp |

Estados de todo botão: foco visível (3 px, amarelo no cabeçalho), pressionado (leve redução), processando (desabilitado com indicador girando), sucesso (aviso curto na base) e erro (o que houve e o que fazer).

## 6. Movimento

Só o que responde a uma ação: a barra de vagas que enche, o placar que pulsa e o confete quando o jogo fecha. Com "reduzir movimento" ligado, nada disso roda.

## 7. Marca

O símbolo é o sol nascendo atrás da fita da rede, com o reflexo no mar. Funciona em 16 px (sol amarelo e faixa branca sobre cobalto). Os ícones do app (192, 512, maskable e Apple) usam o mesmo desenho; o maskable mantém tudo dentro da área segura.

## 8. Princípios de cognição aplicados

| Decisão na interface | Princípio | Referência |
|---|---|---|
| Procurar e Marcar como blocos grandes no topo, e Procurar como primeiro destino da navegação | Alvos maiores e mais próximos são atingidos mais rápido | Fitts (1954) |
| Esporte, dia e período à vista; o resto em "Mais filtros" | O tempo de decisão cresce com o número de opções | Hick (1952); Hyman (1953) |
| Três níveis com nome em vez de números de 1 a 5 | Reconhecer custa menos que lembrar o que cada número significa | Nielsen (1994); Sweller (1988) |
| Mini placar com "1 vaga" e barra quase cheia | O esforço aumenta perto da meta | Kivetz, Urminsky e Zheng (2006) |
| "Já confirmaram: Ana, Beto" | Pessoas seguem o que outras parecidas fizeram | Cialdini (2009) |
| Amarelo só na ação principal | Um traço distinto é achado sem busca | Treisman e Gelade (1980) |
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
