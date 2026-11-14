// Liga o app ao Firebase: Firestore (dados ao vivo) e login da equipe.
// A configuração do projeto fica em config.js. As permissões ficam em firestore.rules.
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";
import {
  getFirestore, collection, doc, onSnapshot, setDoc, updateDoc, deleteDoc, getDoc
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-firestore.js";
import {
  getAuth, onAuthStateChanged, signInWithEmailAndPassword, signOut, GoogleAuthProvider, signInWithPopup
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js";

const resolver = window.__resolverBackend || function () {};
const cfg = window.FIREBASE_CONFIG || {};

if (!cfg.apiKey || cfg.apiKey === "COLE_AQUI" || !cfg.projectId) {
  resolver({ erro: "config" });
} else {
  try {
    const app = initializeApp(cfg);
    const fs = getFirestore(app);
    const auth = getAuth(app);

    // Mesma interface que o app usa: collection(c).onSnapshot e doc(caminho).set/update/delete/onSnapshot
    const db = {
      collection(caminho) {
        return {
          onSnapshot(next, erro) { return onSnapshot(collection(fs, caminho), next, erro); }
        };
      },
      doc(caminho) {
        const ref = doc(fs, caminho);
        return {
          set(dados) { return setDoc(ref, dados); },
          update(dados) { return updateDoc(ref, dados); },
          delete() { return deleteDoc(ref); },
          onSnapshot(next, erro) {
            return onSnapshot(ref, (s) => next({ exists: s.exists(), data: () => s.data() }), erro);
          }
        };
      }
    };

    const google = new GoogleAuthProvider();
    google.setCustomParameters({ prompt: "select_account" });

    // Equipe = conta com um documento em admins/{uid}
    const conta = {
      aoMudar(cb) { return onAuthStateChanged(auth, cb); },
      entrarGoogle() { return signInWithPopup(auth, google); },
      entrar(email, senha) { return signInWithEmailAndPassword(auth, email, senha); },
      sair() { return signOut(auth); },
      async ehAdmin(uid) {
        try { return (await getDoc(doc(fs, "admins", uid))).exists(); }
        catch (e) { console.warn("admins", e); return false; }
      }
    };

    resolver({ db, conta });
  } catch (e) {
    console.error(e);
    resolver({ erro: "firebase" });
  }
}
