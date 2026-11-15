# Design system do Fechou

Regra geral: cada escolha se justifica por **função** (o que a pessoa precisa ver e tocar), não por "psicologia das cores". A revisão de Elliot e Maier (2014) mostra que os efeitos de cor sobre comportamento existem, mas são pequenos e dependem de contexto e cultura. Onde uma decisão abaixo se apoia em pesquisa, a referência está no fim. Onde é só convenção ou bom senso, está dito.

## 1. Tipografia

| Opção | Prós | Contras | Decisão |
|---|---|---|---|
| **Inter** (corpo) | Altura-x grande, feita para tela, algarismos tabulares, boa distinção entre I, l e 1 | Muito usada, pouca personalidade | **Corpo e interface** |
| Roboto | Legível, padrão do Android | Algarismos e formas mais estreitos em tamanho pequeno | Não |
| Atkinson Hyperlegible | Máxima distinção entre letras | Poucos pesos, aparência menos neutra | Não agora |
| Fonte do sistema | Zero download | Muda de um aparelho para outro | Reserva (fallback) |
| **Outfit** (títulos e números grandes) | Geométrica, pesos fortes, lê bem em placar | Ruim para texto longo | **Só títulos e placar** |
| Barlow Condensed (anterior) | Cabe muito número | Estreita demais em celular | Substituída |

- Corpo em 16 px com entrelinha 1,5. Tamanho pequeno demais reduz a velocidade de leitura (Legge e Bigelow, 2011); por isso nada essencial fica abaixo de 14 px.
- Escala: 12 (rótulo da barra) / 14 / 16 / 20 / 24 / 32, e 68 só no placar.
- Horários, preços e contagens usam algarismos tabulares, para alinhar e comparar.
- Coluna de até 560 px: linhas de cerca de 60 caracteres.

## 2. Cores, por função

| Token | Hex | Onde |
|---|---|---|
| `cta` | `#FF6B35` | Só a ação principal da tela, com texto grafite |
| `accent` | `#0F5C6E` | Links, seleção, navegação ativa, número principal do painel |
| `bg` | `#FFF8F0` | Fundo |
| `surface` | `#FFFFFF` | Cartões, barra de navegação |
| `ink` | `#1E2A32` | Texto |
| `muted` | `#55646D` | Texto secundário |
| `line` | `#EADFD2` | Bordas |
| `ok` | `#12733F` sobre `#DDF5E8`, barra `#2BB673` | Jogo fechou, pessoa confirmada |
| `warn` | `#8A5300` sobre `#FFEFC2` | "Faltam 2", avisos |
| `danger` | `#B42318` | Erro e ações destrutivas |
| desabilitado | opacidade 60% | Botão em processamento |

Uma única cor de alta saliência por tela aponta a ação: um alvo que difere dos vizinhos em uma só característica é achado sem esforço de busca (Treisman e Gelade, 1980). Por isso o laranja nunca aparece em dois botões da mesma tela, e verde e âmbar ficam reservados para estado.

### Contraste medido (WCAG 2.2, critério 1.4.3: mínimo 4,5:1)

| Par | Razão |
|---|---|
| Texto sobre areia | 13,9:1 |
| Texto secundário sobre areia | 5,8:1 |
| Link sobre areia | 7,2:1 |
| Branco sobre petróleo | 7,6:1 |
| Grafite sobre laranja (botão principal) | 5,2:1 |
| Branco sobre laranja | 2,8:1, **reprovado**: por isso o texto do botão é grafite |
| Verde sobre fundo de sucesso | 5,2:1 |
| Âmbar sobre fundo de atenção | 5,5:1 |
| Erro sobre branco | 6,6:1 |
| Tema escuro: texto, secundário e link | 16,0:1, 7,0:1 e 8,6:1 |

O tema escuro acompanha a preferência do aparelho, com os mesmos papéis de cor.

## 3. Tokens

Ficam todos no bloco `:root` do `index.html`.

| Grupo | Valores |
|---|---|
| Espaço | `--s1` 4, `--s2` 8, `--s3` 12, `--s4` 16, `--s5` 24, `--s6` 32 |
| Raio | `--r-sm` 10, `--r-md` 14, `--r-lg` 20, `--r-full` |
| Elevação | `--e1` cartão, `--e2` camada flutuante |
| Toque | `--toque` 48 px |
| Largura | Uma coluna de até 560 px. Abaixo de 720 px, a navegação desce para a base da tela. |
| Ícones | Traço de 2 px, 24 px, sempre com rótulo |

## 4. Componentes e estados

| Componente | Regra |
|---|---|
| Botão principal | Laranja, texto grafite, 48 px ou 58 px de altura, largura total no celular |
| Botão secundário | Borda, fundo branco |
| Botão do WhatsApp | Verde próprio, só para abrir o WhatsApp |
| Navegação inferior | 2 a 4 destinos, ícone com rótulo, alvo de 52 px |
| Chips de esporte e filtros | Alvos de 44 px; filtros recolhidos com o resumo do que está ativo |
| Campo | Rótulo sempre visível acima, 48 px, erro em texto no fim do formulário |
| Cartão de jogo | Esporte e nível, quando e onde, situação, e a pílula "Faltam N" |
| Placar | Número grande, barra de progresso, estado em palavras |

Estados em todos os botões: foco visível (contorno de 3 px), pressionado (leve redução), processando (desabilitado com indicador girando), sucesso (aviso curto na base da tela) e erro (mensagem dizendo o que houve e o que fazer).

## 5. Princípios de cognição aplicados

| Decisão na interface | Princípio | Referência |
|---|---|---|
| Botões grandes, na largura da tela e navegação na base, perto do polegar | Alvos maiores e mais próximos são atingidos mais rápido | Fitts (1954) |
| No máximo 4 destinos na navegação; filtros recolhidos; uma ação principal por tela | O tempo de decisão cresce com o número de opções | Hick (1952); Hyman (1953) |
| Formulário de jogo já vem preenchido com o perfil; escolher em vez de digitar | Reconhecer custa menos que lembrar; menos carga de trabalho | Nielsen (1994); Sweller (1988) |
| "Falta 1" e barra quase cheia | O esforço aumenta perto da meta | Kivetz, Urminsky e Zheng (2006) |
| "Já confirmaram: Ana, Beto" | Pessoas seguem o que outras parecidas fizeram | Cialdini (2009) |
| Cantos arredondados | Preferência por contornos curvos (efeito de preferência, não de segurança) | Bar e Neta (2006) |
| Rótulo, valor e ajuda sempre juntos; cartões separam grupos | Proximidade e região comum agrupam | Princípios da Gestalt |
| Confirmar antes de apagar ("toque de novo") e validar antes de salvar | Prevenção de erro | Nielsen (1994) |
| Placar e listas mudam na hora; avisos de sem internet | Visibilidade do estado do sistema | Nielsen (1994) |
| Alvos de pelo menos 44 px (mínimo da norma: 24 px) | Tamanho de alvo | WCAG 2.2, critério 2.5.8 |

O que **não** afirmamos: que alguma cor "gera confiança" ou "libera dopamina". Não há base para isso.

## 6. Voz

Informal e de convite: "Falta 1 pro seu jogo", "Tô dentro", "Você não joga sozinho". O botão diz o que acontece ("Marcar um jogo", "Entrar na lista de espera"). A palavra solidão não aparece no app: fica no pitch.

## 7. Referências

- Bar, M., e Neta, M. (2006). Humans prefer curved visual objects. *Psychological Science*, 17(8).
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
