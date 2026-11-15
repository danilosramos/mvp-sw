"""Mede o contraste WCAG das cores do design system (DESIGN.md). Uso: python3 tests/contraste.py"""
def lin(c):
    c=c/255; return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def L(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def cr(a,b):
    la,lb=L(a),L(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
pares = {
 "claro": [
  ("tinta #0E1B3D / branco", "#0E1B3D","#FFFFFF",4.5),
  ("tinta / fundo #F3F5FA", "#0E1B3D","#F3F5FA",4.5),
  ("apoio #4A5675 / branco", "#4A5675","#FFFFFF",4.5),
  ("apoio / fundo", "#4A5675","#F3F5FA",4.5),
  ("cobalto #1B4FE0 / branco (link)", "#1B4FE0","#FFFFFF",4.5),
  ("cobalto / fundo", "#1B4FE0","#F3F5FA",4.5),
  ("branco / cobalto (botão, cabeçalho)", "#FFFFFF","#1B4FE0",4.5),
  ("tinta / sol #FFC928 (botão principal)", "#0E1B3D","#FFC928",4.5),
  ("tinta / areia #F1DDAE", "#0E1B3D","#F1DDAE",4.5),
  ("apoio / areia", "#4A5675","#F1DDAE",4.5),
  ("cobalto / areia", "#1B4FE0","#F1DDAE",4.5),
  ("sol / placar #0E1B3D (números)", "#FFC928","#0E1B3D",3),
  ("branco / placar", "#FFFFFF","#0E1B3D",4.5),
  ("verde-claro #8CF5BE / placar", "#8CF5BE","#0E1B3D",4.5),
  ("branco / placar fechou #0B6B3A", "#FFFFFF","#0B6B3A",4.5),
  ("ok #0E7A44 / ok-bg #DDF6E8", "#0E7A44","#DDF6E8",4.5),
  ("warn #8A4B00 / warn-bg #FFF0C4", "#8A4B00","#FFF0C4",4.5),
  ("branco / zap #0F7A43", "#FFFFFF","#0F7A43",4.5),
  ("perigo #B42318 / branco", "#B42318","#FFFFFF",4.5),
  ("borda campo #7C88A8 / branco (3:1)", "#7C88A8","#FFFFFF",3),
  ("barra cobalto / trilho #E3E8F3 (3:1)", "#1B4FE0","#E3E8F3",3),
  ("foco cobalto / branco (3:1)", "#1B4FE0","#FFFFFF",3),
  ("foco sol / cobalto cabeçalho (3:1)", "#FFC928","#1B4FE0",3),
  ("tinta / cobalto-tint #E9EFFF", "#0E1B3D","#E9EFFF",4.5),
 ],
 "escuro": [
  ("tinta #EEF2FF / fundo #0A1330", "#EEF2FF","#0A1330",4.5),
  ("tinta / superfície #111C3F", "#EEF2FF","#111C3F",4.5),
  ("apoio #A8B3D6 / superfície", "#A8B3D6","#111C3F",4.5),
  ("apoio / fundo", "#A8B3D6","#0A1330",4.5),
  ("cobalto #8CAEFF / superfície (link)", "#8CAEFF","#111C3F",4.5),
  ("tinta-escura #0A1330 / cobalto #8CAEFF (chip)", "#0A1330","#8CAEFF",4.5),
  ("branco / cabeçalho #1A3FB8", "#FFFFFF","#1A3FB8",4.5),
  ("tinta-escura / sol", "#0E1B3D","#FFC928",4.5),
  ("areia-tinta #F5E6C4 / areia #3B3424", "#F5E6C4","#3B3424",4.5),
  ("sol / placar #050B22", "#FFC928","#050B22",3),
  ("ok #6FE0A6 / ok-bg #12392A", "#6FE0A6","#12392A",4.5),
  ("warn #F6C766 / warn-bg #3A2C0F", "#F6C766","#3A2C0F",4.5),
  ("zap-tinta #04140B / zap #36C877", "#04140B","#36C877",4.5),
  ("perigo #FF8A80 / superfície", "#FF8A80","#111C3F",4.5),
  ("borda campo #5A6894 / superfície (3:1)", "#5A6894","#111C3F",3),
  ("barra #8CAEFF / trilho #26335F (3:1)", "#8CAEFF","#26335F",3),
 ]}
for tema, ps in pares.items():
    print("==", tema)
    for nome,a,b,minimo in ps:
        v=cr(a,b); print(f"{'OK ' if v>=minimo else 'FALHA'} {v:5.2f} (mín {minimo})  {nome}")
