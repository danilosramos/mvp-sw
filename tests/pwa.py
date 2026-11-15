"""Teste do PWA: manifest, ícones, service worker, cache, abertura sem internet e atualização.
Uso: python3 tests/pwa.py  (CHROME opcional)"""
import asyncio, subprocess, time, os, shutil, json
from playwright.async_api import async_playwright
ORIGEM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = "/tmp/pwa_site/mvp-sw"  # servido numa subpasta, como no GitHub Pages
shutil.rmtree("/tmp/pwa_site", ignore_errors=True); os.makedirs("/tmp/pwa_site")
shutil.copytree(ORIGEM, RAIZ, ignore=shutil.ignore_patterns(".git", "tests"))
srv = subprocess.Popen(["python3", "-m", "http.server", "8770", "--bind", "127.0.0.1"], cwd="/tmp/pwa_site", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
URL = "http://127.0.0.1:8770/mvp-sw/"
erros = []
async def main():
    async with async_playwright() as p:
        EXE = os.environ.get("CHROME")
        b = await (p.chromium.launch(executable_path=EXE, headless=True, args=["--no-sandbox"]) if EXE else p.chromium.launch())
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, service_workers="allow")
        pg = await ctx.new_page(); pg.on("pageerror", lambda e: erros.append(str(e)))
        await pg.goto(URL)
        man = await pg.evaluate("fetch(document.querySelector('link[rel=manifest]').href).then(r => r.json())")
        print("manifest:", man["short_name"], man["display"], man["start_url"], man["scope"], [i["sizes"] + "/" + i.get("purpose", "") for i in man["icons"]])
        icones = await pg.evaluate("Promise.all(['icons/icon-192.png','icons/icon-512.png','icons/icon-maskable-512.png','icons/apple-touch-icon.png','icons/favicon.svg','offline.html'].map(u => fetch(u).then(r => r.status)))")
        print("ícones e offline.html (status):", icones)
        await pg.wait_for_function("navigator.serviceWorker.controller !== null", timeout=15000)
        info = await pg.evaluate("navigator.serviceWorker.getRegistration().then(r => ({scope: r.scope, ativo: r.active && r.active.state}))")
        print("service worker:", info)
        chaves = await pg.evaluate("caches.keys().then(async ks => ({caches: ks, itens: (await (await caches.open(ks[0])).keys()).map(r => new URL(r.url).pathname.replace('/mvp-sw/', '') || './')}))")
        print("cache:", chaves["caches"], sorted(chaves["itens"]))
        # sem internet: recarrega e o app abre
        await ctx.set_offline(True)
        await pg.reload()
        await pg.wait_for_selector("text=Você está sem internet", timeout=10000)
        print("offline, recarregou:", " | ".join((await pg.inner_text("#app")).split("\n")[:1]), "| título:", await pg.title())
        print("offline, aviso no topo:", (await pg.inner_text("#aviso"))[:40])
        r2 = await pg.evaluate("fetch('nao-existe-' + Date.now()).then(r => r.status, e => 'falhou')")
        print("offline, arquivo fora do cache:", r2)
        await ctx.set_offline(False)
        # atualização controlada: muda a versão do sw.js, pede update, aparece o aviso, toca em Atualizar
        await pg.goto(URL); await pg.wait_for_function("navigator.serviceWorker.controller !== null")
        s = open(RAIZ + "/sw.js").read().replace('const VERSAO = "v1";', 'const VERSAO = "v2";'); open(RAIZ + "/sw.js", "w").write(s)
        await pg.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update())")
        await pg.wait_for_selector("button[data-acao=atualizar-app]", timeout=15000)
        print("atualização: aviso apareceu:", (await pg.inner_text("#aviso")).replace("\n", " ")[:50])
        async with pg.expect_navigation(timeout=15000):
            await pg.click("button[data-acao=atualizar-app]")
        await pg.wait_for_function("navigator.serviceWorker.controller !== null")
        await pg.wait_for_timeout(800)
        print("atualização: caches depois:", await pg.evaluate("caches.keys()"), "| aviso sumiu:", not await pg.is_visible("button[data-acao=atualizar-app]"))
        # instalação: simula o evento do navegador
        await pg.evaluate("(() => { const e = new Event('beforeinstallprompt', {cancelable: true}); e.prompt = () => { window.__pediu = true; }; e.userChoice = Promise.resolve({outcome: 'dismissed'}); window.dispatchEvent(e); })()")
        await pg.wait_for_timeout(300)
        visivel = await pg.is_visible("button[data-acao=instalar]")
        print("instalar: faixa aparece na tela atual:", visivel, "| view:", await pg.evaluate("document.body.getAttribute('data-view')"))
        await b.close()
try: asyncio.run(main())
finally: srv.terminate()
print("ERROS:", erros)
