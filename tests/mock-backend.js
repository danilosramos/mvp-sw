// Backend simulado (mesma interface do firebase.js) com as mesmas permissões de firestore.rules.
(function(){
  var params = new URLSearchParams(location.search);
  var store = new Map(), listeners = [], docListeners = [], authCbs = [];
  var EQUIPE = { uid: "u_equipe", email: "equipe@teste.com", displayName: "Equipe Teste" };
  var JOGADORA = { uid: "u_outro", email: "ana@teste.com", displayName: "Ana Teste" };
  var usuario = params.has("logado") ? EQUIPE : null;
  function ehEquipe(){ return !!usuario && store.has("admins/" + usuario.uid); }
  function colOf(p){ return p.split("/").slice(0, -1).join("/"); }
  function negar(){ return Promise.reject({ code: "permission-denied", message: "Missing or insufficient permissions." }); }
  function wait(){ return new Promise(function(r){ setTimeout(r, 10); }); }
  function chaves(d){ return Object.keys(d || {}).sort().join(","); }
  function donoDoJogo(jogoId){ var g = store.get("jogos/" + jogoId); return !!usuario && !!g && g.donoUid === usuario.uid; }
  function podeLer(c){ return c === "jogos" || c === "confirmacoes" || ehEquipe(); }
  function podeLerDoc(p){
    var col = colOf(p), id = p.split("/").pop();
    var mc = /^jogos\/([^/]+)\/contato$/.exec(col);
    if (mc) return ehEquipe() || donoDoJogo(mc[1]) || (!!usuario && store.has("confirmacoes/" + mc[1] + "_" + usuario.uid));
    if (col === "perfis" || col === "interesse_premium") return ehEquipe() || (!!usuario && usuario.uid === id);
    if (col === "admins") return !!usuario && usuario.uid === id;
    return podeLer(col);
  }
  function podeEscrever(op, p, d){
    var col = colOf(p);
    if (col === "admins"){
      var cfg = store.get("config/equipe");
      return op === "set" && !!usuario && p === "admins/" + usuario.uid && !store.has(p) && chaves(d) === "codigo,criadoEm,nome" && !!cfg && d.codigo === cfg.codigo;
    }
    var mct = /^jogos\/([^/]+)\/contato$/.exec(col);
    if (mct){
      if (ehEquipe()) return true;
      if (!donoDoJogo(mct[1])) return false;
      return op === "delete" || (chaves(d) === "zap" && typeof d.zap === "string" && d.zap.length <= 15);
    }
    if (col === "perfis"){
      var idp = p.split("/").pop();
      if (!usuario || usuario.uid !== idp) return false;
      if (op === "delete") return true;
      var okp = "aceitaConvites,atualizadoEm,cidade,cidadeChave,criadoEm,esportes,horarios,nivel,nome,plano,whatsapp";
      return chaves(d) === okp && d.plano === "free" && Array.isArray(d.esportes) && Array.isArray(d.horarios) && typeof d.aceitaConvites === "boolean";
    }
    if (col === "interesse_premium"){
      var idi = p.split("/").pop();
      if (!usuario || usuario.uid !== idi) return false;
      return op === "delete" || (chaves(d) === "criadoEm,plano" && d.plano === "premium");
    }
    if (ehEquipe()) return true;
    if (col === "jogos"){
      if (op === "set" && !store.has(p)){
        var ok = ["arena","cidade","cidadeChave","criadoEm","donoNome","donoUid","donoZap","esporte","nivel","origem","quando","situacao","teste","tipoLocal","total","vagas","valor","visibilidade"].join(",");
        return !!usuario && chaves(d) === ok && d.donoUid === usuario.uid && d.origem === "jogador" && d.teste === false && d.vagas >= 1 && d.vagas <= d.total && d.total <= 30;
      }
      if (op === "delete"){ var g = store.get(p); return !!usuario && !!g && g.donoUid === usuario.uid; }
      return false;
    }
    if (col === "confirmacoes"){
      if (op === "set" && !store.has(p)){
        var kp = chaves(d);
        var jg = store.get("jogos/" + d.jogoId) || {};
        var comConta = kp === "criadoEm,jogoId,nome,uid,via" && !!usuario && d.uid === usuario.uid && p === "confirmacoes/" + d.jogoId + "_" + usuario.uid;
        var publica = ((kp === "criadoEm,jogoId,nome,via" && jg.visibilidade !== "publico") || comConta) && d.via === "link" && typeof d.nome === "string" && d.nome.length >= 2 && d.nome.length <= 40 && store.has("jogos/" + d.jogoId);
        var doDono = chaves(d) === "criadoEm,jogoId,nome,via" && d.via === "whatsapp" && typeof d.nome === "string" && d.nome.length >= 2 && donoDoJogo(d.jogoId);
        return publica || doDono;
      }
      if (op === "delete"){ var c = store.get(p); return !!c && (donoDoJogo(c.jogoId) || (!!usuario && c.uid === usuario.uid)); }
      return false;
    }
    return false;
  }
  function snap(c){
    var docs = Array.from(store.entries()).filter(function(e){ return colOf(e[0]) === c; }).sort(function(a, b){ return a[0] < b[0] ? -1 : 1; })
      .map(function(e){ var d = JSON.parse(JSON.stringify(e[1])); return { id: e[0].split("/").pop(), data: function(){ return d; } }; });
    return { docs: docs, metadata: { fromCache: false } };
  }
  function notify(c){ listeners.filter(function(l){ return l.col === c; }).forEach(function(l){ setTimeout(function(){ l.next(snap(c)); }, 0); }); }
  function docSnap(p){ var d = store.get(p); return { exists: !!d, data: function(){ return d ? JSON.parse(JSON.stringify(d)) : undefined; } }; }
  function notifyDoc(p){ docListeners.filter(function(l){ return l.path === p; }).forEach(function(l){ setTimeout(function(){ l.next(docSnap(p)); }, 0); }); }
  var db = {
    collection: function(c){ return { onSnapshot: function(next, err){
      if (!podeLer(c)){ setTimeout(function(){ if (err) err({ code: "permission-denied" }); }, 20); return function(){}; }
      var l = { col: c, next: next }; listeners.push(l); setTimeout(function(){ next(snap(c)); }, 30);
      return function(){ var i = listeners.indexOf(l); if (i >= 0) listeners.splice(i, 1); };
    } }; },
    doc: function(p){ return {
      set: function(d){ if (!podeEscrever("set", p, d)) return negar(); store.set(p, JSON.parse(JSON.stringify(d))); notify(colOf(p)); notifyDoc(p); return wait(); },
      update: function(d){ if (!ehEquipe()) return negar(); if (!store.has(p)) return Promise.reject({ code: "not-found" }); store.set(p, Object.assign({}, store.get(p), JSON.parse(JSON.stringify(d)))); notify(colOf(p)); notifyDoc(p); return wait(); },
      delete: function(){ if (!podeEscrever("delete", p)) return negar(); store.delete(p); notify(colOf(p)); notifyDoc(p); return wait(); },
      get: function(){ if (!podeLerDoc(p)) return negar(); return wait().then(function(){ return docSnap(p); }); },
      onSnapshot: function(next, err){
        if (!podeLerDoc(p)){ setTimeout(function(){ if (err) err({ code: "permission-denied" }); }, 20); return function(){}; }
        var l = { path: p, next: next }; docListeners.push(l); setTimeout(function(){ next(docSnap(p)); }, 30);
        return function(){ var i = docListeners.indexOf(l); if (i >= 0) docListeners.splice(i, 1); };
      }
    }; }
  };
  var conta = {
    aoMudar: function(cb){ authCbs.push(cb); setTimeout(function(){ cb(usuario); }, 20); return function(){}; },
    entrarGoogle: function(){ return new Promise(function(res, rej){ setTimeout(function(){
      if (params.has("cancela") && !window.__jaCancelou){ window.__jaCancelou = true; return rej({ code: "auth/popup-closed-by-user" }); }
      usuario = params.has("naoadmin") ? JOGADORA : EQUIPE;
      authCbs.forEach(function(cb){ cb(usuario); }); res({ user: usuario });
    }, 30); }); },
    sair: function(){ usuario = null; authCbs.forEach(function(cb){ cb(null); }); return Promise.resolve(); },
    ehAdmin: function(uid){ return new Promise(function(r){ setTimeout(function(){ r(store.has("admins/" + uid)); }, 20); }); }
  };
  store.set("admins/u_equipe", { nome: "Equipe" });
  if (params.get("codigo")) store.set("config/equipe", { codigo: params.get("codigo"), criadoEm: 1 });
  if (params.has("compub")){
    store.set("jogos/pub1", { arena: "Arena Publica", esporte: "Vôlei de praia", nivel: 3, quando: "2026-11-21T18:00", total: 4, vagas: 3, valor: 100, situacao: "vago", teste: false, criadoEm: 5, donoUid: "u_dono", donoNome: "Dani", donoZap: "", origem: "jogador", visibilidade: "publico", cidade: "Araranguá", cidadeChave: "ararangua", tipoLocal: "privada" });
    store.set("jogos/pub1/contato/dono", { zap: "5548900000077" });
  }
  if (params.has("comperfil")) store.set("perfis/u_app", { nome: "Zé App", esportes: ["Vôlei de praia"], nivel: 3, horarios: ["Sábado à tarde ou noite"], cidade: "Araranguá", cidadeChave: "ararangua", whatsapp: "5548900000099", aceitaConvites: true, plano: "free", criadoEm: 1, atualizadoEm: 1 });
  if (params.has("comjogo")){
    store.set("jogos/g1", { arena: "Arena Teste", esporte: "Vôlei de praia", nivel: 3, quando: "2026-11-21T18:00", total: 4, vagas: 2, valor: 100, situacao: "cancelar", teste: true, criadoEm: 9 });
    store.set("confirmacoes/c1", { jogoId: "g1", nome: "Hotel", via: "whatsapp", criadoEm: 10 });
  }
  window.__store = store;
  window.__resolverBackend({ db: db, conta: conta });
})();
