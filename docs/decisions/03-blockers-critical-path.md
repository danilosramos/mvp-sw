# BLOCKERS-TASK-LIST: Phase 1 Critical Blockers

**Project:** Energia Boa MVP  
**Phase:** Phase 1 (MVP readiness before public release)  
**Date:** 2026-11-16  
**Status:** 0/8 complete, 0% to Phase 1 ready

---

## Executive Summary

Eight critical blockers must be resolved before Phase 1 is complete. These blockers span business alignment, product testing, testing infrastructure, backend transitions, security implementation, feature completeness, frontend stability, and configuration. All blockers have dependencies and must be resolved in priority order.

**Progress:** 0/8 complete | **Completion Rate:** 0% | **Phase 1 Readiness:** 0%

---

## Critical Blockers Tracking Table

| ID | Priority | Title | Owner | Status | Due Date | Effort | Dependencies |
|---|---|---|---|---|---|---|---|
| BLOCK-001 | 1 | Arena revenue model alignment (M1) | PM/Business | TODO | 2026-11-23 | M (2d) | None |
| BLOCK-002 | 2 | Relative dates in e2e tests (A1+S4) | QA/Testing | TODO | 2026-11-23 | P (4h) | None |
| BLOCK-003 | 3 | WhatsApp embedded browser test (D3) | Product/QA | TODO | 2026-11-30 | M (2d) | BLOCK-002 |
| BLOCK-004 | 4 | Server-time transition window (S2+B1) | Backend/Eng | TODO | 2026-11-30 | M (2d) | BLOCK-001, BLOCK-002 |
| BLOCK-005 | 5 | Emulator Firestore Rules tests (S5) | QA/Security | TODO | 2026-11-30 | M (2d) | BLOCK-004 |
| BLOCK-006 | 6 | Cancelation + waitlist + metric rename (N1–N3) | Eng/Frontend | TODO | 2026-12-07 | G (5d+) | BLOCK-001, BLOCK-004, BLOCK-005 |
| BLOCK-007 | 7 | Login destination + form errors (D1+K1) | Frontend/Eng | TODO | 2026-11-30 | P (6h) | BLOCK-002 |
| BLOCK-008 | 8 | Security config + docs alignment (C1+C2+C3) | Arch/Security | TODO | 2026-11-23 | P (4h) | None |

---

## Detailed Blocker Specifications

### BLOCK-001: Arena Revenue Model Alignment (Priority 1)

**Title:** Declare post-pilot price in arena offer and secure written acceptance  
**Owner:** PM / Business Lead  
**Status:** TODO  
**Due Date:** 2026-11-23  
**Effort:** M (1-2 days)  
**Dependencies:** None  
**Risk Level:** Critical (business viability)  

**Description:**  
The pilot is announced as "30 days free, no commitment" without declaring the price that will follow. This prevents testing whether arenas accept payment. Arena revenue hypothesis cannot be validated without explicit price declaration and written acceptance in the offer.

**Acceptance Criteria:**
- [ ] Arena offer template includes post-pilot price field (minimum 3 price points: R$50, R$100, R$200)
- [ ] Acceptance mechanism defined (checkbox + name capture in offer document)
- [ ] At least 2 of 10 arena pilots have written price acceptance before next phase
- [ ] Price terms appear in `config/equipe` document structure
- [ ] `index.html` arena panel displays accepted price alongside offer
- [ ] Documentation updated in ESTRATEGIA.md with pricing scenarios
- [ ] Team alignment confirmed: PM, Sales, Eng, Arenas (minimum 3 stakeholders)

**Verification:**
- Offer template deployed with price field
- At least 2 arena signatures in Firestore with explicit price acceptance
- Arena dashboard shows accepted price values
- Zero regressions in existing offer flow

**Tech References:**
- `index.html:834, 772` (current offer display)
- `ESTRATEGIA.md:121, 140` (strategy assumptions)
- `config/equipe` document schema

---

### BLOCK-002: Relative Dates in E2E Tests (Priority 2)

**Title:** Replace fixed test dates with relative date generation matching execution date  
**Owner:** QA / Testing Lead  
**Status:** TODO  
**Due Date:** 2026-11-23  
**Effort:** P (3-4 hours)  
**Dependencies:** None  
**Risk Level:** High (tests fail 2026-11-21 18:30)  

**Description:**  
E2E tests use hardcoded dates that cause test failure after 2026-11-21 18:30 UTC. The form rejects past dates and test suite aborts. This blocks all CI/CD validation after the cutoff date. Must implement relative date generation using server-side `quando()` function logic.

**Acceptance Criteria:**
- [ ] Remove all hardcoded date literals from `tests/e2e.py`
- [ ] Implement relative date generator: today, +30 days, +1 year
- [ ] All scenario dates computed at runtime from execution date
- [ ] `tests/mock-backend.js:124` logic ported to Python test suite
- [ ] Test suite passes with system clock set to: today, +30 days, +365 days
- [ ] No date constants remain in `tests/` directory
- [ ] GitHub Actions CI uses dynamic date generation
- [ ] Documentation updated with date generation approach

**Verification:**
- Run test suite with mock clock at: 2026-11-16, 2026-12-16, 2027-11-16 → all pass
- Code review confirms zero hardcoded dates in test files
- Grep `-r '202[67]-[0-1][0-9]-[0-3][0-9]' tests/` returns empty result
- CI/CD logs show date dynamically computed

**Tech References:**
- `tests/e2e.py:48, 123, 188` (hardcoded dates)
- `tests/mock-backend.js:114, 119, 124` (reference implementation)
- `firebase.js` date conversion logic

---

### BLOCK-003: WhatsApp Embedded Browser Test (Priority 3)

**Title:** Test public game invite in WhatsApp embedded browser on Android and iPhone  
**Owner:** Product / QA Lead  
**Status:** TODO  
**Due Date:** 2026-11-30  
**Effort:** M (1-2 days)  
**Dependencies:** BLOCK-002 (test infrastructure stable)  
**Risk Level:** High (user acquisition funnel)  

**Description:**  
Public game invites are shared via WhatsApp links but have never been tested in the embedded browser where most users open them. Login popup is blocked by embedded browser security policy, preventing user conversion. Must validate redirect flow "Open in browser" and confirm acceptance before Fase 1.

**Acceptance Criteria:**
- [ ] "Open in browser" UI element added before login attempt detection
- [ ] Invite opens in WhatsApp embedded browser without error
- [ ] Redirect to system browser triggered automatically or via button
- [ ] Login flow completes in system browser
- [ ] User redirected back to game after login confirmation
- [ ] Tested on: Android Chrome (WhatsApp), iOS Safari (WhatsApp) - both latest versions
- [ ] Screenshot evidence from both platforms attached to acceptance
- [ ] No popup blocking, auth errors, or loop conditions
- [ ] UX flow documented in DESIGN.md

**Verification:**
- WhatsApp conversation with test invite link
- Devices: 1x Android (SDK 14+), 1x iPhone (iOS 17+)
- Screen recording showing: tap link → see "Open in browser" → login → return to game
- Acceptance logged in GitHub issue

**Tech References:**
- `firebase.js:49` (login popup handling)
- `index.html:706, 1456-1463` (invite flow)
- WhatsApp embedded browser behavior (non-standard popup handling)

---

### BLOCK-004: Server-Time Transition Window (Priority 4)

**Title:** Implement server timestamp in confirmations and ensure backwards compatibility  
**Owner:** Backend / Engineering Lead  
**Status:** TODO  
**Due Date:** 2026-11-30  
**Effort:** M (1-2 days)  
**Dependencies:** BLOCK-001, BLOCK-002  
**Risk Level:** High (security, waitlist manipulation)  

**Description:**  
Current implementation uses client-side `Date.now()` for confirmation ordering. This allows queue manipulation (S2 finding). Must transition to `request.time` (server timestamp) in Firestore Rules. Backend must accept both old (client) and new (server) timestamps during transition for 7-day window to avoid breaking old app versions in circulation.

**Acceptance Criteria:**
- [ ] Firestore Rules updated: `confirmacaoPublicaValida` uses `request.time` for `criadoEm`
- [ ] Firestore Rules updated: `confirmacaoDoDonoValida` uses `request.time` for `criadoEm`
- [ ] JavaScript SDK sends `firebase.firestore.FieldValue.serverTimestamp()` for new confirmations
- [ ] Application accepts both timestamp formats when reading confirmations
- [ ] Existing confirmations with `Date.now()` remain ordered correctly
- [ ] Service Worker versioned: `v3` (old) → `v4` (new, accepts both)
- [ ] 7-day transition window implemented: publish rules (permissive), publish app (server TS), restrict rules
- [ ] Rules rollout: Day 1 (permissive), Day 2 (app deploy), Day 8 (restrict)
- [ ] Zero data loss in transition window

**Verification:**
- Firestore Rules emulator test: old and new timestamps both accepted
- E2E test confirms: new confirmation ordered before old confirmation (same minute)
- Transition timeline in GitHub issue with dates
- Monitoring: check for timestamp-related errors during 7-day window

**Tech References:**
- `firestore.rules:89` (queue manipulation vulnerability S2)
- `index.html:427` (confirmation creation)
- Firestore Rules trecho 1 (security audit recommendation)
- Firebase SDK serverTimestamp() API

---

### BLOCK-005: Emulator Firestore Rules Tests (Priority 5)

**Title:** Implement Firestore Rules validation in Firebase emulator with security scenarios  
**Owner:** QA / Security Lead  
**Status:** TODO  
**Due Date:** 2026-11-30  
**Effort:** M (1-2 days)  
**Dependencies:** BLOCK-004  
**Risk Level:** High (security validation)  

**Description:**  
Current tests validate a mock backend that diverges from real Firestore Rules. Invalid rules can pass all tests. Must migrate Firestore Rules validation to Firebase emulator, including attack scenarios (S1: private game enumeration, S2: queue manipulation, S6: invalid dates/values). Real rules must be tested before production publish.

**Acceptance Criteria:**
- [ ] Firebase emulator integration added to test suite
- [ ] `tests/firestore-rules.js` or `.py` created with emulator-based tests
- [ ] Test suite validates: rule acceptance for valid scenarios
- [ ] Test suite validates: rule rejection for attack scenarios
- [ ] Attack scenarios from S1 test: list private games, create own confirmation
- [ ] Attack scenarios from S2 test: manipulate queue order with old timestamps
- [ ] Attack scenarios from S6 test: past date, invalid level, out-of-range price
- [ ] Mock backend tests removed or refactored to emulator tests
- [ ] CI/CD runs emulator tests before production deploy
- [ ] 100% of audit security findings covered by tests

**Verification:**
- Emulator test run output shows: N pass, 0 fail for valid scenarios
- Emulator test run output shows: N attack scenarios rejected (expected failures pass)
- Code coverage: all security.related rules >=80%
- Pre-commit hook prevents Firestore Rules deploy without passing tests

**Tech References:**
- `tests/mock-backend.js:35-38, 53-57` (divergence from real rules)
- `firestore.rules:170, 80-95, 178-179` (private game access S1)
- `firestore.rules:89` (queue manipulation S2)
- Firebase Rules Emulator Suite documentation

---

### BLOCK-006: Cancelation + Waitlist + Metric Rename (Priority 6)

**Title:** Implement game state management, waitlist functionality, and metric definition alignment  
**Owner:** Engineering / Frontend Lead  
**Status:** TODO  
**Due Date:** 2026-12-07  
**Effort:** G (5+ days)  
**Dependencies:** BLOCK-001, BLOCK-004, BLOCK-005  
**Risk Level:** High (feature completeness, revenue metrics)  

**Description:**  
Games currently use binary delete instead of state tracking. Players disappear instead of canceling with notification. No waitlist exists; next player unaware of opening. Metrics tracked lack definition: "revenue" sums any price without confirmation or presence. Must implement: game states (open/canceled), cancelation with notification templates, automatic waitlist advancement, presence tracking, and defensible revenue metric.

**Acceptance Criteria:**
- [ ] Game state machine implemented: 'aberto' → 'cancelado' (N1 feature)
- [ ] `canceladoEm` timestamp added to `jogos/{id}` schema
- [ ] UI: "Cancelar jogo" button shows pre-filled WhatsApp message template
- [ ] Canceled game invitation continues to load, displays "Jogo cancelado em [data]"
- [ ] Waitlist implemented: confirmations with `situacao: 'espera'` ordered by `criadoEm`
- [ ] Waitlist UI: organizer sees next in line with "Avisar" button
- [ ] "Avisar" button pre-fills WhatsApp: "Abriu vaga! [link]"
- [ ] After-game: organizer marks attendance (`presenca: ['uid1', 'uid2', ...]`)
- [ ] Revenue metric renamed: "Jogos Realizados" (confirmed + attended, priced)
- [ ] Dashboard shows: realized games per week, per arena, with revenue
- [ ] Firestore Rules validate: cancelation only by organizer, presence only after game time
- [ ] Zero unintended deletions on existing games during migration

**Verification:**
- E2E test: organizer cancels game → notification sent → invitee sees status
- E2E test: participant joins waitlist → vaga opens → organizer advises → participant joins
- E2E test: post-game → organizer marks attendance → game counted in revenue
- Dashboard shows only "Jogos Realizados" with confirmation + presence + price
- Firestore Rules emulator confirms authorization constraints
- Zero game records deleted (all marked canceled)

**Tech References:**
- `firestore.rules:45` (presence requirement for revenue)
- `index.html:473-488` (current revenue calculation, flawed)
- `SPECS.md:76` (game state enum)
- N1–N3 audit findings

---

### BLOCK-007: Login Destination + Form Errors (Priority 7)

**Title:** Preserve "mark game" intent after login and add inline form field validation  
**Owner:** Frontend / Engineering Lead  
**Status:** TODO  
**Due Date:** 2026-11-30  
**Effort:** P (5-6 hours)  
**Dependencies:** BLOCK-002  
**Risk Level:** Medium (conversion funnel)  

**Description:**  
User clicks "Marcar Jogo", login popup appears, redirects to home after login → user loses intent and closes app. Players also receive generic error on form submit without field-specific feedback. Must preserve navigation destination across login and implement inline validation errors.

**Acceptance Criteria:**
- [ ] Login flow stores return destination before redirect
- [ ] After Google Sign-In, user returns to: game form (if from home), game details (if from invite)
- [ ] Return destination preserved in: sessionStorage or URL fragment
- [ ] No redirect loop if user cancels login
- [ ] Form validation: each field displays error inline (below or beside input)
- [ ] Error messages: specific per field (e.g., "Data deve ser futura", "Preço máximo R$5000")
- [ ] Validation runs: on blur, before submit
- [ ] Submit button disabled until form valid
- [ ] Re-open game form: pre-fills previous session data
- [ ] UX tested on mobile and desktop viewports

**Verification:**
- E2E test: click "Marcar Jogo" → login → return to form with pre-fill
- E2E test: enter invalid date → see inline error message → cannot submit
- E2E test: fix date → error clears, submit enabled
- Mobile responsiveness check: error messages visible, form readable
- Zero form abandonment regression vs. baseline

**Tech References:**
- `index.html:706` (login flow entry)
- `firebase.js:49` (login popup handler)
- Form validation best practices (mobile-first)

---

### BLOCK-008: Security Config + Docs Alignment (Priority 8)

**Title:** Restrict Firebase key to domain, define official URL, and align documentation  
**Owner:** Architecture / Security Lead  
**Status:** TODO  
**Due Date:** 2026-11-23  
**Effort:** P (3-4 hours)  
**Dependencies:** None  
**Risk Level:** High (abuse potential, link stability)  

**Description:**  
Firebase API key has no domain restriction and can be used from anywhere. Official app URL ambiguous (README vs. repo). Missing Content Security Policy and SDK integrity checks. Documentation diverges from code (Fase 1 vs. Fase 2 mislabeling). Must lock down config and align docs.

**Acceptance Criteria:**
- [ ] Firebase Console: API key restricted to authorized domains only
- [ ] Authorized domains: official app URL + localhost (dev) only
- [ ] Official URL decided: single source of truth (e.g., `energia-boa.app`, not GitHub Pages URL)
- [ ] README.md updated with single official URL
- [ ] `S11` finding resolved: no ambiguity in deployment URL
- [ ] Documentation audit complete: SPECS.md, PRD.md, ARQUITETURA.md labels accurate
- [ ] All "Fase 1" vs "Fase 2" labels match requirements
- [ ] Minimum Content Security Policy added to `index.html` (meta tag or header)
- [ ] Firebase SDK integrity check documented (or deferred to build phase)
- [ ] Security findings S10–S13 documented in BLOCKERS-TASK-LIST

**Verification:**
- Firebase Console screenshot: key restriction visible
- Test unauthorized domain: API calls rejected
- README, STRATEGY, SPECS docs reviewed for consistency
- CSP meta tag present in `index.html`
- Official URL published across all channels (GitHub, links, README)

**Tech References:**
- `config.js:5` (unrestricted Firebase key)
- `README.md:11` (ambiguous URL)
- Audit findings: S10 (key restriction), S11 (official URL), S12 (CI/CD)
- Firestore security best practices

---

## Priority Sequencing & Dependencies

### Critical Path

```
BLOCK-001 (Arena revenue)
    ↓
BLOCK-008 (Security + docs)
    ↓
BLOCK-002 (Relative dates)
    ├→ BLOCK-003 (WhatsApp test)
    └→ BLOCK-007 (Login + errors)
    ↓
BLOCK-004 (Server timestamp)
    ↓
BLOCK-005 (Emulator tests)
    ↓
BLOCK-006 (Cancelation + waitlist)
```

### Must Complete Before Phase 1 Release

All 8 blockers must reach "DONE" status.

---

## Owner Role Definitions

| Role | Responsibilities | Blockers |
|---|---|---|
| **PM/Business** | Arena alignment, revenue model validation, stakeholder sign-off | BLOCK-001 |
| **Product Lead** | WhatsApp UX, feature completeness, user funnel validation | BLOCK-003 |
| **QA/Testing** | Test infrastructure, e2e automation, Firestore Rules validation | BLOCK-002, BLOCK-005 |
| **Backend/Eng** | Firestore Rules, server timestamp transition, schema evolution | BLOCK-004, BLOCK-006 |
| **Frontend/Eng** | UI forms, login flow, inline validation, navigation preservation | BLOCK-007, BLOCK-006 |
| **Architecture/Security** | Key restrictions, official URL, security audit alignment | BLOCK-008 |

---

## Sprint Planning Timeline

| Sprint | Dates | Focus Blockers | Expected Completion |
|---|---|---|---|
| Sprint 1 | 2026-11-17 to 2026-11-23 | BLOCK-001, BLOCK-002, BLOCK-008 | Decisions, infrastructure |
| Sprint 2 | 2026-11-24 to 2026-11-30 | BLOCK-003, BLOCK-004, BLOCK-007 | Features, security transition |
| Sprint 3 | 2026-12-01 to 2026-12-07 | BLOCK-005, BLOCK-006 | Validation, waitlist |

---

## Completion Checklist

```
Phase 1 Blockers Status:

□ BLOCK-001: Arena revenue model alignment ........... [  ] DONE
□ BLOCK-002: Relative dates in e2e tests ............ [  ] DONE
□ BLOCK-003: WhatsApp embedded browser test ......... [  ] DONE
□ BLOCK-004: Server-time transition window .......... [  ] DONE
□ BLOCK-005: Emulator Firestore Rules tests ......... [  ] DONE
□ BLOCK-006: Cancelation + waitlist + metrics ....... [  ] DONE
□ BLOCK-007: Login destination + form errors ........ [  ] DONE
□ BLOCK-008: Security config + docs alignment ....... [  ] DONE

Completion Rate: ___ / 8  (___%)
Phase 1 Ready: [ ] YES  [ ] NO

Approval Sign-Off:
- Product: _________________ Date: _______
- Engineering: _____________ Date: _______
- Security: ________________ Date: _______
- Business: ________________ Date: _______
```

---

## Success Metrics Post-Phase 1

Once all blockers are complete, Phase 1 readiness validation:

1. **Business:** 2+ arena pilots signed with explicit post-pilot pricing
2. **Testing:** 100% e2e + Firestore Rules tests passing with dynamic dates
3. **Security:** 100% audit findings addressed; zero high/critical severity open
4. **Funnel:** WhatsApp invite → login → game confirmed without dropout
5. **Features:** Cancelation, waitlist, presence tracking, defensible revenue metric operational
6. **Deployment:** GitHub Actions CI/CD with all test gates passing

---

## Review & Tracking

- **Last Updated:** 2026-11-16
- **Next Review:** 2026-11-23 (Sprint 1 close)
- **Owner:** Project Coordinator
- **Tracked In:** GitHub Issues (one per blocker tag: `BLOCK-001`, etc.)
- **Dependencies:** Jira/Linear (optional, for resource planning)

---

## Document Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-11-16 | Initial creation; 8 critical blockers identified from AUDITORIA-COMPLETA and PRD |

