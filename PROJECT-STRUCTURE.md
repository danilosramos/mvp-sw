# Proposta de Reorganização de Estrutura do Projeto

**Data:** 16/11/2026  
**Status:** Recomendação para review  
**Padrão Aplicado:** Firestore + PWA (Firebase Hosting compatible)

---

## 1. Situação Atual

```
mvp-sw/
├── [14 markdown docs] (na raiz)
├── [5 arquivos de código] (index.html, firebase.js, config.js, sw.js, etc)
├── fonts/
├── icons/
├── tests/
└── .git/

PROBLEMA:
- Docs na raiz: difícil navegar, sem prioridade
- Código monolítico: index.html 137KB em um arquivo
- Sem separação entre production, staging, tools
- Sem ci/cd, build, publishment
- Docs e código misturados
```

---

## 2. Estrutura Proposta

```
mvp-sw/
├── README.md                          ← Landing do projeto
├── package.json                        ← Dev tools (testes, linting)
├── firebase.json                       ← Firebase config
├── .github/
│   └── workflows/
│       ├── test.yml                   ← CI: contraste + e2e + PWA + rules
│       └── deploy.yml                 ← Deploy automático a Pages
├── docs/                               ← DOCUMENTAÇÃO ORGANIZADA
│   ├── _index.md                      ← Mapa e índice de docs
│   ├── strategy/                      ← Visão, negócio, roadmap
│   │   ├── vision.md                  ← Hipótese, caso de uso
│   │   ├── market.md                  ← Mercado, concorrentes (ex ESTRATEGIA)
│   │   ├── roadmap.md                 ← Fases 1, 2, 3, timeframe
│   │   └── business-model.md          ← Canvas, receita, métricas
│   ├── design/                        ← Design system, tokens, UI
│   │   ├── design-system.md           ← Cores, tipografia, tokens (ex DESIGN)
│   │   ├── components.md              ← Componentes reutilizáveis
│   │   └── accessibility.md           ← WCAG, contrast, aria
│   ├── technical/                     ← Especificação técnica
│   │   ├── architecture.md            ← Casos de uso, sequência (ex ARQUITETURA)
│   │   ├── specs.md                   ← Requisitos técnicos (ex SPECS)
│   │   ├── data-model.md              ← Firestore collections schema
│   │   ├── firebase-rules.md          ← Autorização, security model
│   │   ├── api-endpoints.md           ← Se houver backend (Fase 3)
│   │   └── deployment.md              ← Ambientes, CI/CD (novo)
│   ├── product/                       ← Requirements, features
│   │   ├── requirements.md            ← User stories (ex REQUISITOS)
│   │   ├── prd.md                     ← Product Requirements Doc (ex PRD)
│   │   ├── features/                  ← Features por versão
│   │   │   ├── 2026-11-phase-1.md
│   │   │   ├── 2026-12-phase-2.md
│   │   │   └── 2027-phase-3.md
│   │   └── user-flows.md              ← Fluxos de usuário
│   ├── operations/                    ← Go-to-market, arena, suporte
│   │   ├── arena-kickoff.md           ← Arena onboarding (ex ARENA-KICKOFF)
│   │   ├── support-handbook.md        ← FAQ, troubleshooting
│   │   └── metrics-dashboard.md       ← KPIs, tracking
│   ├── decisions/                     ← Decisions & ADRs
│   │   ├── audit-2026-11.md           ← Auditoria consolidada (ex AUDITORIA + AUDITORIA-COMPLETA)
│   │   ├── findings-2026-11.md        ← Critical findings (ex RESOLVE-FINDINGS)
│   │   ├── security-review.md         ← Security assessment (ex SECURITY-HOTFIXES)
│   │   └── migration-plan.md          ← Fase 2 migration strategy
│   ├── testing/                       ← Testing strategy & plans
│   │   ├── testing-roadmap.md         ← Test gaps & roadmap (ex TESTING-ROADMAP)
│   │   ├── test-plan-phase-1.md       ← Phase 1 test cases
│   │   ├── test-plan-phase-2.md       ← Phase 2 test cases
│   │   └── manual-testing.md          ← Device tests, edge cases
│   └── blockers/                      ← Critical blockers & tracking
│       └── phase-1-blockers.md        ← 8 blockers to resolve (ex BLOCKERS-TASK-LIST + CRITICAL-ISSUES-DEEP-DIVE)
├── src/                                ← SOURCE CODE
│   ├── index.html                     ← Split from monolithic (140KB → modular)
│   ├── styles/
│   │   ├── variables.css              ← Tokens de design
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── accessibility.css
│   ├── scripts/
│   │   ├── app.js                     ← Lógica principal
│   │   ├── firebase-adapter.js        ← Firebase integration
│   │   ├── ui-controller.js           ← Telas, eventos
│   │   ├── utils.js                   ← Helpers
│   │   └── offline.js                 ← Suporte offline
│   ├── config.js                      ← Firebase config (referenciado)
│   ├── sw.js                          ← Service Worker
│   └── manifest.webmanifest           ← PWA metadata
├── public/                             ← ASSETS & STATIC
│   ├── icons/
│   │   ├── logo.svg
│   │   ├── logo-192.png
│   │   └── favicon.ico
│   ├── fonts/
│   │   └── [...fonts]
│   ├── 404.html                       ← GitHub Pages 404
│   └── offline.html                   ← Offline fallback
├── tests/                              ← TESTING
│   ├── unit/
│   │   └── firebase-adapter.test.js
│   ├── integration/
│   │   └── firestore-rules.test.js    ← Firebase emulator tests
│   ├── e2e/
│   │   ├── e2e.py                     ← Playwright tests
│   │   ├── mock-backend.js
│   │   └── test-data.json
│   ├── performance/
│   │   └── lighthouse.test.js
│   └── security/
│       └── contrast.py                ← A11y testing
├── .firebaserc                        ← Firebase project config
├── firestore.rules                    ← Firestore security rules
├── firestore.indexes.json             ← Firestore indices
├── CHANGELOG.md                       ← Version history
└── .claude/                           ← Claude Code config
    └── CLAUDE.md                      ← Project guidelines for AI
```

---

## 3. Reorganização de Documentos

### 3.1 O que fazer com cada documento

| Documento Atual | Ação | Novo Local | Motivo |
|---|---|---|---|
| **ESTRATEGIA.md** | Move | `docs/strategy/market.md` | Negócio/mercado |
| **DESIGN.md** | Move | `docs/design/design-system.md` | Design tokens |
| **ARQUITETURA.md** | Move + Update | `docs/technical/architecture.md` | Remover "Reserva gerada", adicionar diagramas atualizados |
| **REQUISITOS.md** | Move | `docs/product/requirements.md` | Product requirements |
| **PRD.md** | Move | `docs/product/prd.md` | Manter, adicionar links internos |
| **SPECS.md** | Move | `docs/technical/specs.md` | Manter como referência |
| **DESIGN.md** | Rename | `docs/design/design-system.md` | Mais claro |
| **AUDITORIA.md** | Consolidate | `docs/decisions/audit-2026-11.md` | Juntar com AUDITORIA-COMPLETA |
| **AUDITORIA-COMPLETA.md** | Consolidate | `docs/decisions/audit-2026-11.md` | Junta com AUDITORIA |
| **RESOLVE-FINDINGS.md** | Move | `docs/decisions/findings-2026-11.md` | Tracking de issues |
| **SECURITY-HOTFIXES.md** | Move | `docs/decisions/security-review.md` | Security decisions |
| **TESTING-ROADMAP.md** | Move | `docs/testing/testing-roadmap.md` | Testing strategy |
| **ARENA-KICKOFF.md** | Move | `docs/operations/arena-kickoff.md` | Go-to-market |
| **BLOCKERS-TASK-LIST.md** | Move | `docs/blockers/phase-1-blockers.md` | Tracking |
| **CRITICAL-ISSUES-DEEP-DIVE.md** | Merge | `docs/blockers/phase-1-blockers.md` | Detalhe dos 3 críticos |

### 3.2 Documentos novos a criar

| Documento | Local | Propósito |
|---|---|---|
| **_index.md** | `docs/` | Mapa de documentação (central landing) |
| **vision.md** | `docs/strategy/` | Hipótese, casos de uso, north star |
| **roadmap.md** | `docs/strategy/` | Fases 1, 2, 3, timeline |
| **business-model.md** | `docs/strategy/` | Canvas, unit economics |
| **data-model.md** | `docs/technical/` | Firestore schema detalhado |
| **firebase-rules.md** | `docs/technical/` | Autorização e segurança |
| **deployment.md** | `docs/technical/` | Ambientes, CI/CD, publishment |
| **user-flows.md** | `docs/product/` | Fluxos de usuário por role |
| **features/*.md** | `docs/product/features/` | Features por release |
| **support-handbook.md** | `docs/operations/` | FAQ, troubleshooting |
| **metrics-dashboard.md** | `docs/operations/` | KPIs, tracking, alerts |
| **migration-plan.md** | `docs/decisions/` | Fase 2 migration strategy |
| **test-plan-phase-1.md** | `docs/testing/` | Casos de teste Fase 1 |
| **test-plan-phase-2.md** | `docs/testing/` | Casos de teste Fase 2 |
| **manual-testing.md** | `docs/testing/` | Device tests (D3, F5) |
| **CLAUDE.md** | `.claude/` | Diretrizes para Claude Code |

---

## 4. Reorganização de Código

### 4.1 Quebrar index.html monolítico

**Atual:** 1 arquivo de 137KB

**Proposto:**
```
src/
├── index.html              ← Container + loader
├── styles/
│   ├── variables.css       ← Tokens (cores, fontes, espaçamento)
│   ├── layout.css
│   ├── components.css
│   └── accessibility.css
└── scripts/
    ├── app.js              ← State, routing
    ├── firebase-adapter.js ← Firestore + Auth
    ├── ui-controller.js    ← Renderização de telas
    ├── utils.js            ← Helpers (data, format, validation)
    └── offline.js          ← Offline support
```

**Benefícios:**
- Reutilização de CSS/JS
- Testável
- Versionamento mais claro
- Build tools para minification (Fase 3)

### 4.2 Service Worker e PWA assets

```
src/
├── sw.js                   ← Service Worker
├── manifest.webmanifest    ← PWA metadata
└── offline.html            ← Fallback offline

public/
├── icons/                  ← Logos, favicons
├── fonts/                  ← Tipografia
└── 404.html                ← GitHub Pages 404
```

---

## 5. CI/CD & Build

### 5.1 GitHub Actions workflows

```
.github/workflows/
├── test.yml
│   - Contraste (Python)
│   - E2E (Playwright)
│   - PWA (validation)
│   - Firebase Rules (emulator)
│   → Falha na CI se algum teste falha
├── deploy.yml
│   - Roda APÓS test.yml passar
│   - Publica para GitHub Pages
│   - Atualiza versão em versionamento
│   → Só arquivos em src/ e public/
│       (exclui tests/, docs/, .github/)
└── security-scan.yml (novo)
    - SonarQube ou OWASP
    - Detecta vulnerabilidades
    → Recomendação antes de Fase 2
```

### 5.2 Package.json (dev tools)

```json
{
  "name": "energia-boa",
  "version": "2026.11.16",
  "scripts": {
    "test": "npm run test:contrast && npm run test:e2e && npm run test:pwa && npm run test:rules",
    "test:contrast": "python3 tests/security/contrast.py",
    "test:e2e": "python3 tests/e2e/e2e.py",
    "test:pwa": "npm run test:manifest && npm run test:sw",
    "test:rules": "firebase emulators:exec 'jest tests/integration/firestore-rules.test.js'",
    "dev": "firebase emulators:start",
    "build": "echo 'No build step (static files)'",
    "deploy": "firebase deploy --only hosting"
  },
  "devDependencies": {
    "firebase-tools": "^latest",
    "jest": "^latest",
    "playwright": "^latest"
  }
}
```

---

## 6. Exemplo: Navegação de Docs

**Novo leitor quer entender o projeto:**
1. Ler `README.md` (landing)
2. Consultar `docs/_index.md` (mapa)
3. Ir a `docs/strategy/vision.md` (o quê, por quê)
4. Consultar `docs/product/prd.md` (requisitos)
5. Explorar `docs/technical/specs.md` (como)

**Arquiteto quer revisar segurança:**
1. Ir a `docs/decisions/security-review.md`
2. Ver referência em `docs/technical/firebase-rules.md`
3. Executar testes: `npm run test:rules`

**QA quer testar:**
1. Consultar `docs/testing/testing-roadmap.md`
2. Executar: `npm run test`
3. Se falhar, consultar `docs/decisions/findings-2026-11.md`

---

## 7. Prioridade de Implementação

### Sprint 1 (Nov 23-28): Reorganização base
- [ ] Criar diretórios: `docs/`, `src/`, `public/`
- [ ] Mover documentos para novo local
- [ ] Criar `docs/_index.md` (mapa)
- [ ] Atualizar `README.md` (landing)
- [ ] Criar `.github/workflows/test.yml`

### Sprint 2 (Dec 2-6): Código modular
- [ ] Split `index.html` em módulos CSS/JS
- [ ] Validar que funciona (nenhuma quebra)
- [ ] Atualizar testes

### Sprint 3 (Dec 9+): Polimento
- [ ] Criar documentos novos (vision, deployment, etc)
- [ ] `CLAUDE.md` (diretrizes para AI)
- [ ] Validar navegação (todos os links funcionam)

---

## 8. Checklist de Implementação

- [ ] Criar estrutura de diretórios
- [ ] Mover docs (rsync ou manual)
- [ ] Atualizar todos os links internos (relativos)
- [ ] Atualizar `README.md` com nova estrutura
- [ ] Criar `.github/workflows/` com CI/CD
- [ ] Validar que GitHub Pages ainda publica (após CI)
- [ ] Testar localmente: `npm run test`
- [ ] Documento novo: `docs/_index.md`
- [ ] Documento novo: `.claude/CLAUDE.md`
- [ ] Validar que convites públicos ainda funcionam
- [ ] Commit: "Reorganize project structure (docs, src, ci-cd)"

---

## 9. Padrão Aplicado

Este projeto segue o padrão **Firestore + PWA** com inspiração em:

- **Firebase/Google:** `firebase.json`, `.firebaserc`, `firestore.rules`, hospedagem GitHub Pages
- **Static Site Generators (Hugo, Jekyll):** `docs/` com markdown hierárquico
- **Node.js/npm:** `package.json` para dev tools
- **12-Factor App:** Separação clara entre docs, código, testes, build
- **GitHub:** `.github/workflows/` para CI/CD

**Vantagens:**
- Escalonável sem servidor
- Docs e código próximos
- CI/CD automático
- Testável
- Pronto para Fase 2 (backend opcional)

---

## 10. Notas & Ressalvas

**Deve ser feito:**
- Atualizar `firestore.rules` comentários com link a `docs/technical/firebase-rules.md`
- Adicionar `docs/_index.md` como primeira leitura
- Testar todos os links com ferramenta de validação

**Nice-to-have (Fase 3):**
- Build tool (Webpack/Vite) para bundling
- Linting (ESLint)
- Formatter (Prettier)
- Type checking (TypeScript, JSDoc)

---

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
