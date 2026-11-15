# Design system do Fechou

Regra geral: cada escolha se justifica por **função** (ação, confiança, legibilidade), não por "psicologia das cores". Os efeitos de cor e forma existem, mas são pequenos e dependem de contexto. Na banca, diga isso antes que perguntem.

## Cores (por função)

| Token | Hex | Onde | Por quê |
|---|---|---|---|
| `cta` Laranja | `#FF6B35` | Só o botão principal da tela, com texto grafite | Um único ponto de alta saliência por tela diz onde tocar. Texto branco sobre esse laranja não passa em contraste. |
| `accent` Azul-petróleo | `#0F5C6E` | Links, seleção, navegação, número do painel | Tom frio e escuro para tudo que não é a ação principal. Contraste alto sobre o fundo. |
| `ok` Verde | `#2BB673` (barra) e `#12733F` (texto) | Só quando o jogo fecha ou alguém confirma | Verde reservado para "deu certo" mantém o significado. |
| `warn` Âmbar | `#8A5300` sobre `#FFEFC2` | "Faltam 2" | Estado de atenção, separado da cor de ação. |
| `bg` Areia | `#FFF8F0` | Fundo | Branco quente; cartões brancos se destacam sem sombra pesada. |
| `ink` Grafite | `#1E2A32` | Texto | Contraste AAA sobre areia e branco. |

## Tipografia e forma

- Títulos e números: **Outfit** 700/800. Corpo: **Inter**, 16px, entrelinha 1,5.
- Escala: 13 / 14 / 16 / 20 / 24 / 32, e 68 só no placar.
- Cartões com raio de 20px, botões de 12px, área de toque mínima de 46px.
- Uma coluna de até 560px. Um botão laranja por tela.

## Os quatro mecanismos que o produto usa de verdade

1. **Progresso perto do fim:** "Falta 1" e a barra quase cheia. Pessoas se esforçam mais quanto mais perto da meta (efeito de gradiente de meta).
2. **Prova social com nome:** "Já confirmaram: Ana, Beto". Gente identificável convence mais que um número.
3. **Menos atrito:** entrar no jogo sem conta, só com o nome. Cada campo a mais derruba conversão.
4. **Recompensa no momento certo:** confete e "Fechou!" só quando o jogo completa, nunca antes.

## Voz

Informal e de convite: "Falta 1 pro seu jogo", "Bora jogar", "Você não joga sozinho". A palavra **solidão não aparece no app**: ela fica no pitch. Ninguém abre um app que o chama de solitário.

## Imagens (pitch e redes)

Rostos e grupos reais, de preferência a foto do jogo que vocês organizaram. Quadra vazia só no slide do problema.
