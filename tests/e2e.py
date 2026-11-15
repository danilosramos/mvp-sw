"""Testes de ponta a ponta do Fechou com um backend simulado (mock-backend.js),
que aplica as mesmas permissões de firestore.rules. Dados 100% fictícios.

Uso:  pip install playwright && playwright install chromium
      python3 tests/e2e.py
Variáveis opcionais: CHROME (caminho de um Chrome já instalado) e
FIREBASE_SDK_DIR (pasta node_modules/firebase, para testar o SDK real sem internet).
"""
import asyncio, json, urllib.parse, subprocess, time, os
from playwright.async_api import async_playwright

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
_src = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
_tag = '<script type="module" src="firebase.js"></script>'
assert _src.count(_tag) == 1
open(os.path.join(AQUI, "test.html"), "w", encoding="utf-8").write(_src.replace(_tag, '<script src="mock-backend.js"></script>'))
open(os.path.join(AQUI, "smoke.html"), "w", encoding="utf-8").write(_src.replace('<script src="config.js"></script>', '<script src="config-fake.js"></script>'))
open(os.path.join(AQUI, "firebase.js"), "w", encoding="utf-8").write(open(os.path.join(RAIZ, "firebase.js"), encoding="utf-8").read())
EXE = os.environ.get("CHROME")
SDK = os.environ.get("FIREBASE_SDK_DIR", "")

srv = subprocess.Popen(["python3", "-m", "http.server", "8765", "--bind", "127.0.0.1"], cwd=AQUI, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
BASE = "http://127.0.0.1:8765/"
erros = []
def txt(s): return " ".join(s.split())

async def main():
    async with async_playwright() as p:
        b = await (p.chromium.launch(executable_path=EXE, headless=True, args=["--no-sandbox"]) if EXE else p.chromium.launch())
        ctx = await b.new_context(viewport={"width": 390, "height": 844})

        # A. Time: login, importa base, marca jogo público em Araranguá, combina com formulário + app
        pg = await ctx.new_page(); pg.on("pageerror", lambda e: erros.append("A: " + str(e)))
        await pg.goto(BASE + "test.html?cancela&comperfil#painel")
        await pg.wait_for_selector("text=Falta gente pro seu jogo?", timeout=5000)
        await pg.click("#fl-google"); await pg.wait_for_selector("#fl-erro:not([hidden])")
        print("A login cancelado:", await pg.text_content("#fl-erro"))
        await pg.click("#fl-google")
        await pg.wait_for_selector("#t-base", timeout=5000); await pg.wait_for_timeout(300)
        print("A tiles:", json.dumps([txt(t) for t in await pg.eval_on_selector_all(".tile", "els => els.map(e => e.innerText)")], ensure_ascii=False))
        print("A código do time:", txt(await pg.text_content("#p-time .codigo")))
        await pg.evaluate("location.hash='jogadores'"); await pg.click("#jg-imp summary")
        await pg.set_input_files("#f-imp", os.path.join(AQUI, "jogadores-teste.json"))
        await pg.wait_for_function("(document.getElementById('imp-status')||{}).textContent.indexOf('importados') >= 0", timeout=8000)
        print("A base:", await pg.text_content("#jg-n"), "| chips app:", await pg.locator("#jg-lista .chip", has_text="app").count())
        await pg.evaluate("location.hash='novo'"); await pg.wait_for_selector("#f-novo")
        await pg.fill("#f-arena", "Arena Teste"); await pg.fill("#f-cidade", "Araranguá"); await pg.fill("#f-quando", "2026-11-21T18:00"); await pg.fill("#f-valor", "120")
        print("A faltam:", await pg.text_content("#f-faltam"))
        await pg.click("#f-enviar"); await pg.wait_for_selector("#j-match .prow", timeout=5000)
        print("A combina:", await pg.text_content("#j-nmatch"), "| topo:", txt(await pg.inner_text("#j-head-main .g-title")))
        nomes = await pg.eval_on_selector_all("#j-match .pname", "els => els.map(e => e.textContent.trim())")
        print("A nomes:", nomes)
        for i in range(3):
            await pg.click("#j-match button[data-acao=confirmou] >> nth=0"); await pg.wait_for_timeout(120)
        gid = (await pg.evaluate("location.hash")).replace("#jogo-", "")
        await pg.evaluate(f"location.hash='convite-{gid}'"); await pg.wait_for_selector("#fc-nome")
        print("A botão (jogo cheio após 3 + precisa 1):", await pg.text_content("#fc-btn"))
        await pg.fill("#fc-nome", "Jogador Teste"); await pg.click("#fc-btn")
        await pg.wait_for_selector("text=Você está no jogo!", timeout=5000)
        print("A check-in logado gravou com uid:", await pg.evaluate(f"window.__store.has('confirmacoes/{gid}_u_equipe') && window.__store.get('confirmacoes/{gid}_u_equipe').uid"))
        await pg.evaluate(f"location.hash='jogo-{gid}'"); await pg.wait_for_selector("#j-score .status")
        print("A final:", txt(await pg.text_content("#j-score .status")))
        await pg.evaluate("location.hash='jogos'"); await pg.wait_for_selector("#jg-res")
        await pg.wait_for_timeout(200)
        print("A jogos abertos (com vaga):", await pg.text_content("#jg-qtd"), "| teste fica fora? (é jogo real fechado)")
        await pg.click("#jg-filtros summary"); await pg.uncheck("#ff-vaga"); await pg.wait_for_timeout(200)
        print("A jogos abertos (inclui fechados):", await pg.text_content("#jg-qtd"))
        await pg.evaluate("location.hash='arenas'"); await pg.wait_for_selector("#f-arena-piloto")
        await pg.fill("#fa-arena", "Arena Exemplo"); await pg.fill("#fa-cidade", "Araranguá"); await pg.fill("#fa-contato", "Fulano"); await pg.fill("#fa-zap", "(48) 90000-0055")
        await pg.fill("#fa-vazios", "10"); await pg.fill("#fa-preco", "90"); await pg.check("input[name=famodelo][value=jogo]", force=True)
        await pg.click("#fa-enviar"); await pg.wait_for_selector("text=Pedido recebido!", timeout=5000)
        await pg.evaluate("location.hash='painel'"); await pg.wait_for_selector("#t-reais"); await pg.wait_for_selector("#p-arenas .prow", timeout=5000)
        print("A arenas no painel:", await pg.text_content("#t-arenas"), "|", txt(await pg.text_content("#t-arenas-sub")), "|", txt(await pg.inner_text("#p-arenas"))[:90])
        await pg.click("button[data-acao=sair-conta]")
        await pg.wait_for_selector("text=Falta gente pro seu jogo?", timeout=5000)
        print("A sair: página inicial | nav:", txt(await pg.inner_text("#nav")))

        # B. Visitante sem conta: check-in pelo link e lista pública
        pv = await ctx.new_page(); pv.on("pageerror", lambda e: erros.append("B: " + str(e)))
        await pv.goto(BASE + "test.html?comjogo#convite-g1")
        await pv.wait_for_selector("#fc-nome", timeout=5000)
        await pv.fill("#fc-nome", "Visitante"); await pv.click("#fc-btn")
        await pv.wait_for_selector("text=Você está no jogo!", timeout=5000); await pv.wait_for_timeout(200)
        print("B visitante:", txt(await pv.inner_text("#cv-score")))
        await pv.evaluate("location.hash='jogo-g1'"); await pv.wait_for_timeout(300)
        print("B sem conta abrindo #jogo vai para:", await pv.evaluate("location.hash"))
        await pv.evaluate("location.hash='jogos'"); await pv.wait_for_selector("#jg-res"); await pv.wait_for_timeout(200)
        print("B lista pública sem login:", await pv.text_content("#jg-qtd"), "| nav:", txt(await pv.inner_text("#nav")))
        await pv.evaluate("location.hash='arenas'"); await pv.wait_for_selector("#ar-box > *")
        if await pv.is_visible("button[data-acao=outra-arena]"):
            await pv.click("button[data-acao=outra-arena]")
        await pv.wait_for_selector("#f-arena-piloto")
        await pv.click("#fa-enviar"); await pv.wait_for_selector("#fa-erro:not([hidden])")
        print("B arena, validação:", await pv.text_content("#fa-erro"))
        await pv.fill("#fa-arena", "Arena Visitante"); await pv.fill("#fa-cidade", "Criciúma"); await pv.fill("#fa-contato", "Maria"); await pv.fill("#fa-zap", "48900000066")
        await pv.click("#fa-enviar"); await pv.wait_for_selector("text=Pedido recebido!", timeout=5000)
        print("B arena sem login: pedidos gravados:", await pv.evaluate("Array.from(window.__store.keys()).filter(k => k.startsWith('arenas_piloto/')).length"))
        print("B regra: visitante lendo a lista de arenas:", await pv.evaluate("new Promise(async ok => { const b = await window.backendPronto; b.db.collection('arenas_piloto').onSnapshot(() => ok('LEU'), e => ok(e.code)); })"))
        await pv.evaluate("location.hash='novo'"); await pv.wait_for_timeout(200)
        print("B visitante em #novo vê:", (await pv.inner_text("#app")).split("\n")[1])

        # C. Jogadora: cadastro, marca jogo público, filtros, Premium, entra no time
        pn = await ctx.new_page(); pn.on("pageerror", lambda e: erros.append("C: " + str(e)))
        await pn.goto(BASE + "test.html?naoadmin&codigo=K7MPQ2#painel")
        await pn.wait_for_selector("#fl-google"); await pn.click("#fl-google")
        await pn.wait_for_selector("#f-perfil", timeout=5000)
        print("C primeiro acesso cai no perfil:", (await pn.inner_text("#app")).split("\n")[1], "| nome:", await pn.input_value("#fp-nome"), "| pode pular:", await pn.is_visible("button[data-acao=pular-perfil]"))
        await pn.click("#fp-salvar"); await pn.wait_for_selector("#fp-erro:not([hidden])")
        print("C validação:", await pn.text_content("#fp-erro"))
        await pn.fill("#fp-cidade", "Araranguá")
        await pn.check("input[name=pesp][value='Vôlei de praia']", force=True)
        await pn.check("input[name=pniv][value='3']", force=True)
        await pn.check("input[name=phor][value='Sábado à tarde ou noite']", force=True)
        await pn.fill("#fp-zap", "(48) 99999-0000")
        await pn.click("#fp-salvar")
        await pn.wait_for_selector("#m-lista", timeout=5000)
        print("C depois do perfil:", txt(await pn.inner_text("#m-lista")), "| nav:", txt(await pn.inner_text("#nav")))
        await pn.click("a.btn[href='#novo']"); await pn.wait_for_selector("#f-novo")
        print("C marcar já vem com:", await pn.input_value("#f-esporte"), "|", await pn.input_value("#f-cidade"), "|", await pn.input_value("#f-zap"), "| faltam:", await pn.text_content("#f-faltam"))
        await pn.fill("#f-quando", "2026-11-21T18:00"); await pn.fill("#f-arena", "X7 Padel")
        await pn.click("#f-enviar"); await pn.wait_for_selector("#j-score .score", timeout=5000)
        print("C dono:", txt(await pn.inner_text("#j-head-main .g-title")), "| vê base?", await pn.is_visible("#j-match"))
        gidc = (await pn.evaluate("location.hash")).replace("#jogo-", "")
        print("C contato separado:", await pn.evaluate(f"[window.__store.get('jogos/{gidc}').donoZap, (window.__store.get('jogos/{gidc}/contato/dono')||{{}}).zap, window.__store.get('jogos/{gidc}').tipoLocal]"))
        # enche o jogo (3 vagas) e testa espera + desistência
        g2 = (await pn.evaluate("location.hash")).replace("#jogo-", "")
        for nm in ["Um", "Dois", "Tres"]:
            await pn.fill("#f-addconf-nome", nm); await pn.click("#f-addconf button"); await pn.wait_for_timeout(150)
        await pn.evaluate(f"location.hash='convite-{g2}'"); await pn.wait_for_selector("#fc-btn")
        print("C jogo cheio, botão:", await pn.text_content("#fc-btn"))
        await pn.click("#fc-btn"); await pn.wait_for_selector("text=Você está na lista de espera", timeout=5000)
        print("C espera:", txt(await pn.inner_text("#cv-acao"))[:70], "|", txt(await pn.inner_text("#cv-score"))[-40:])
        await pn.evaluate(f"location.hash='jogo-{g2}'"); await pn.wait_for_selector("#j-confs .prow")
        await pn.click("#j-confs button[data-acao=tirar] >> nth=0"); await pn.wait_for_timeout(300)
        await pn.evaluate(f"location.hash='convite-{g2}'"); await pn.wait_for_selector("text=Você está no jogo!", timeout=5000)
        print("C alguém saiu -> promovida: Você está no jogo!")
        await pn.click("button[data-acao=desistir]"); await pn.click("button[data-acao=desistir]")
        await pn.wait_for_selector("#fc-btn", timeout=5000)
        print("C desistiu, volta o botão:", await pn.text_content("#fc-btn"))
        await pn.evaluate("location.hash='jogos'"); await pn.wait_for_selector("#jg-res"); await pn.wait_for_timeout(200)
        print("C abertos (cidade dela por padrão):", await pn.input_value("#ff-cidade"), "|", await pn.text_content("#jg-qtd"))
        print("C resumo dos filtros:", await pn.text_content("#jg-resumo"))
        await pn.click("#jg-filtros summary"); await pn.select_option("#ff-esporte", "Padel"); await pn.wait_for_timeout(150)
        print("C filtro Padel:", await pn.text_content("#jg-qtd"))
        await pn.select_option("#ff-esporte", "Vôlei de praia"); await pn.select_option("#ff-nivel", "5"); await pn.wait_for_timeout(150)
        print("C filtro vôlei nível 5:", await pn.text_content("#jg-qtd"))
        await pn.select_option("#ff-nivel", "4"); await pn.select_option("#ff-data", "hoje"); await pn.wait_for_timeout(150)
        print("C filtro nível 4 + hoje:", await pn.text_content("#jg-qtd"))
        await pn.select_option("#ff-data", "todas"); await pn.wait_for_timeout(150)
        print("C filtro nível 4 + qualquer data:", await pn.text_content("#jg-qtd"))
        await pn.evaluate("location.hash='premium'"); await pn.wait_for_selector("#pr-acao button", timeout=5000)
        await pn.click("button[data-acao=quero-premium]")
        await pn.wait_for_selector("text=Você está na lista do Premium", timeout=5000)
        print("C premium: na lista")
        await pn.evaluate("location.hash='painel'"); await pn.wait_for_selector("#m-time")
        await pn.click("#m-time summary"); await pn.fill("#fc-codigo", "k7m pq2"); await pn.click("#fc-entrar")
        await pn.wait_for_selector("#t-premium", timeout=5000); await pn.wait_for_timeout(300)
        print("C virou time: Premium =", await pn.text_content("#t-premium"), "| base:", txt(await pn.text_content("#t-base-sub")))

        # P. Jogo público: visitante precisa de conta; depois vê o contato; aviso de jogo parecido; quadra pública
        pp = await ctx.new_page(); pp.on("pageerror", lambda e: erros.append("P: " + str(e)))
        await pp.goto(BASE + "test.html?compub&naoadmin#convite-pub1")
        await pp.wait_for_selector("#cv-google", timeout=5000)
        print("P visitante em jogo público:", txt(await pp.inner_text("#cv-acao"))[:60], "| form visível:", await pp.is_visible("#fc-nome"))
        print("P regra: check-in sem conta negado:", await pp.evaluate("window.claude, (async()=>{ try{ await (await window.backendPronto).db.doc('confirmacoes/x1').set({jogoId:'pub1',nome:'Zé',via:'link',criadoEm:1}); return 'ACEITOU'; }catch(e){ return e.code; } })()"))
        await pp.click("#cv-google"); await pp.wait_for_selector("#fc-nome", timeout=5000)
        print("P contato antes de entrar:", await pp.evaluate("(async()=>{ try{ var s = await (await window.backendPronto).db.doc('jogos/pub1/contato/dono').get(); return 'LEU ' + s.exists; }catch(e){ return e.code; } })()"))
        await pp.click("#fc-btn"); await pp.wait_for_selector("#cv-acao a.btn.zap", timeout=6000)
        print("P depois de entrar com conta:", urllib.parse.unquote(await pp.get_attribute("#cv-acao a.btn.zap", "href"))[:44])
        await pp.evaluate("location.hash='novo'"); await pp.wait_for_selector("#f-perfil, #f-novo")
        if await pp.is_visible("button[data-acao=pular-perfil]"):
            await pp.click("button[data-acao=pular-perfil]"); await pp.wait_for_selector("#f-novo")
        await pp.select_option("#f-esporte", "Vôlei de praia"); await pp.fill("#f-quando", "2026-11-21T18:30"); await pp.fill("#f-arena", "arena pública"); await pp.fill("#f-cidade", "Araranguá")
        await pp.click("#f-enviar"); await pp.wait_for_selector("#f-parecido:not([hidden])", timeout=4000)
        print("P jogo parecido:", txt(await pp.inner_text("#f-parecido"))[:95], "| botão:", await pp.text_content("#f-enviar"))
        await pp.check("input[name=tipo][value=publica]", force=True); await pp.fill("#f-arena", "Quadra da praça")
        print("P quadra pública: rótulo:", await pp.text_content("#f-arena-lbl"), "| preço escondido:", not await pp.is_visible("#f-valor"))
        await pp.click("#f-enviar"); await pp.wait_for_selector("#j-score .score", timeout=5000)
        print("P jogo em quadra pública:", txt(await pp.inner_text("#j-head-main .g-title")))
        await pp.evaluate("location.hash='jogos'"); await pp.wait_for_selector("#jg-res"); await pp.click("#jg-filtros summary"); await pp.select_option("#ff-tipo", "publica"); await pp.wait_for_timeout(200)
        print("P filtro quadra pública:", await pp.text_content("#jg-qtd"), "|", txt(await pp.inner_text("#jg-res"))[:70])
        await pp.evaluate("location.hash='privacidade'"); await pp.wait_for_selector("text=Quem vê o quê")
        print("P privacidade ok | nav:", txt(await pp.inner_text("#nav")))

        if SDK and os.path.isdir(SDK):
            # D. SDK real do Firebase (sem internet para o Google): carrega e mostra a página inicial
            ps = await ctx.new_page(); ps.on("pageerror", lambda e: erros.append("D: " + str(e)))
            async def rota(route):
                nome = route.request.url.rsplit("/", 1)[-1]
                caminho = os.path.join(SDK, nome)
                if os.path.exists(caminho): await route.fulfill(path=caminho, content_type="application/javascript")
                else: await route.abort()
            await ps.route("https://www.gstatic.com/firebasejs/**", rota)
            await ps.goto(BASE + "smoke.html#painel")
            await ps.wait_for_selector("text=Falta gente pro seu jogo?", timeout=12000)
            print("D SDK real: página inicial ok")
        await b.close()

try:
    asyncio.run(main())
finally:
    srv.terminate()
print("ERROS:", erros)
