// Service worker da Energia Boa.
// - Arquivos do app: rede primeiro, com cópia em cache para abrir sem internet. Assim versão antiga não fica presa.
// - SDK do Firebase (endereço com versão): cache primeiro. As fontes são do próprio app e entram na cópia do app.
// - Dados (Firestore, login) nunca passam por aqui: jogos e vagas só valem ao vivo.
// Para forçar todo mundo a atualizar, mude VERSAO.
const VERSAO = "v3";
const CACHE = "energiaboa-" + VERSAO;
const SHELL = [
  "./", "index.html", "config.js", "firebase.js", "manifest.webmanifest", "offline.html",
  "icons/favicon-48.png", "icons/marca.png", "icons/palavra.png", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png",
  "fonts/barlow-latin-400-normal.woff2", "fonts/barlow-latin-600-normal.woff2", "fonts/barlow-latin-700-normal.woff2",
  "fonts/montserrat-latin-700-normal.woff2", "fonts/montserrat-latin-800-normal.woff2"
];

self.addEventListener("install", (ev) => {
  ev.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL.map((u) => new Request(u, { cache: "reload" })))));
});

self.addEventListener("activate", (ev) => {
  ev.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => (k.startsWith("fechou-") || k.startsWith("energiaboa-")) && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// A página pede a troca quando a pessoa toca em "Atualizar".
self.addEventListener("message", (ev) => {
  if (ev.data && ev.data.type === "SKIP_WAITING") self.skipWaiting();
});

function comLimite(promessa, ms) {
  return new Promise((ok, falha) => {
    const t = setTimeout(() => falha(new Error("tempo esgotado")), ms);
    promessa.then((v) => { clearTimeout(t); ok(v); }, (e) => { clearTimeout(t); falha(e); });
  });
}

async function redePrimeiro(req) {
  const cache = await caches.open(CACHE);
  const navegacao = req.mode === "navigate";
  try {
    const res = await comLimite(fetch(req), navegacao ? 5000 : 8000);
    if (res && res.ok && res.type === "basic") cache.put(req, res.clone());
    return res;
  } catch (e) {
    const guardado = await cache.match(req, { ignoreSearch: navegacao });
    if (guardado) return guardado;
    if (navegacao) return (await cache.match("index.html")) || (await cache.match("offline.html")) || Response.error();
    return Response.error();
  }
}

async function cachePrimeiro(req) {
  const cache = await caches.open(CACHE);
  const guardado = await cache.match(req);
  if (guardado) return guardado;
  const res = await fetch(req);
  if (res && (res.ok || res.type === "opaque")) cache.put(req, res.clone());
  return res;
}

self.addEventListener("fetch", (ev) => {
  const req = ev.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === self.location.origin) {
    if (!url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
    ev.respondWith(redePrimeiro(req));
    return;
  }
  const sdk = url.hostname === "www.gstatic.com" && url.pathname.startsWith("/firebasejs/");
  if (sdk) ev.respondWith(cachePrimeiro(req));
});
