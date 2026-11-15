"""Mede o contraste WCAG das cores do design system (DESIGN.md). Uso: python3 tests/contraste.py"""
def lin(c):
    c = c / 255; return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def L(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
def cr(a, b):
    la, lb = L(a), L(b); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)
PARES = [
  ("texto #FBF7FF / fundo #1F0733", "#FBF7FF", "#1F0733", 4.5),
  ("texto / superfície #2A0F45", "#FBF7FF", "#2A0F45", 4.5),
  ("apoio #CDB9EA / fundo", "#CDB9EA", "#1F0733", 4.5),
  ("apoio / superfície", "#CDB9EA", "#2A0F45", 4.5),
  ("link #DDB0FF / fundo", "#DDB0FF", "#1F0733", 4.5),
  ("link / superfície", "#DDB0FF", "#2A0F45", 4.5),
  ("branco / roxo #A925E6 (seleção, canhoto)", "#FFFFFF", "#A925E6", 4.5),
  ("noite #1F0733 / limão #A9F809 (botão principal)", "#1F0733", "#A9F809", 4.5),
  ("noite / branco (botão secundário)", "#1F0733", "#FFFFFF", 4.5),
  ("branco / roxo profundo #611098 (quadra do início)", "#FFFFFF", "#611098", 4.5),
  ("apoio da quadra #EBDCFF / roxo profundo", "#EBDCFF", "#611098", 4.5),
  ("limão / placar #12041F (números)", "#A9F809", "#12041F", 3),
  ("branco / placar", "#FFFFFF", "#12041F", 4.5),
  ("nível #F1DDFF / #3E1466", "#F1DDFF", "#3E1466", 4.5),
  ("ok #C8FF5E / #263B0B", "#C8FF5E", "#263B0B", 4.5),
  ("aviso #FFC857 / #3B2A0C", "#FFC857", "#3B2A0C", 4.5),
  ("verde-escuro #052E16 / WhatsApp #25D366", "#052E16", "#25D366", 4.5),
  ("perigo #FF8A8A / superfície", "#FF8A8A", "#2A0F45", 4.5),
  ("borda de campo #9A7CC4 / superfície (3:1)", "#9A7CC4", "#2A0F45", 3),
  ("borda de campo / fundo (3:1)", "#9A7CC4", "#1F0733", 3),
  ("barra limão / trilho #3C1D60 (3:1)", "#A9F809", "#3C1D60", 3),
  ("foco limão / fundo (3:1)", "#A9F809", "#1F0733", 3),
  ("foco limão / roxo profundo (3:1)", "#A9F809", "#611098", 3),
  ("apoio / trilho (placar passou)", "#CDB9EA", "#3C1D60", 4.5),
  ("limão / superfície (aba atual)", "#A9F809", "#2A0F45", 4.5),
]
if __name__ == "__main__":
    for nome, a, b, minimo in PARES:
        v = cr(a, b); print(f"{'OK ' if v >= minimo else 'FALHA'} {v:5.2f} (mín {minimo})  {nome}")
