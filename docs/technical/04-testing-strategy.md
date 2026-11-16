# Testing Roadmap: Energia Boa

## Overview

This roadmap addresses six critical testing gaps identified in the security audit and product validation. Each gap blocks Fase 1 ship readiness or exposes the app to data loss, security breaches, or poor user experience in production.

**Prioritization**: P (Priority: blocks ship), M (Must-have), G (Good-to-have)
**Timeline**: Hours (P), Days (M), Weeks+ (G)

---

## GAP A1: Tests Break on 21/11/2026 (Hardcoded Dates)

### Current State

- **What's broken:** E2E test scenario A fails when system date reaches 2026-11-21 at 18:30 because the test hardcodes `2026-11-21T18:00` as the game date. When the current time passes this, the form rejects it as past.
- **Impact:** Test suite becomes unmaintainable; CI/CD will fail on and after Nov 21; deployed app still works but is untested after that date.
- **Evidence:** `tests/e2e.py:48, 123, 188` and `tests/mock-backend.js:114, 119` both use fixed dates.
- **Severity:** HIGH
- **Effort:** P (1 hour)

### Test Strategy

Replace all hardcoded dates in test files with relative dates calculated from "today". The `quando()` function in `mock-backend.js:124` already does this correctly; replicate the pattern in `e2e.py`.

**Steps:**
1. Create a `get_future_date()` helper in `e2e.py` that returns ISO8601 strings relative to current date.
2. Replace all `2026-11-21T18:00` and `2026-11-22T18:30` with calls to this helper (e.g., `+1 day at 18:00`).
3. Update mock-backend.js to use `quando()` consistently for all test fixtures.
4. Verify tests pass on any date, not just dates before Nov 21.

### Test Cases

1. **TC-A1-001: Test runs on date after hardcoded value**
   - Set system clock to 2026-11-30
   - Run `python3 tests/e2e.py`
   - Expected: All scenarios (A, B, C, P) pass, game dates are always in future

2. **TC-A1-002: Test generates dates relative to today**
   - Run `python3 tests/e2e.py` on three different dates: 2026-11-10, 2026-11-25, 2026-12-15
   - Expected: All tests pass on each date; game dates are always 1–7 days from "today"

3. **TC-A1-003: Date boundaries respected**
   - Create a game with `quando()` returning exactly "today at 18:00" (now)
   - Form rejects it as past
   - Create a game 1 second from now: rejected
   - Create a game 2 minutes from now: accepted
   - Expected: Form uses wall-clock time, not day boundary

4. **TC-A1-004: Mock-backend vitrine games are always visible**
   - Load `test.html?vitrine` on any date
   - Expected: v1 (1 day ahead), v2 (2 days), v3 (4 days), v4 (5 days) all show and have when > now

### Infrastructure Needed

- **Code changes:** `tests/e2e.py` (new `get_future_date()` function, ~15 lines)
- **Testing tools:** Python `datetime` module (already available)
- **Environment:** System clock must be adjustable or mocked (use `unittest.mock` on `datetime.now`)
- **No external infrastructure needed**

### Success Criteria

- [ ] `python3 tests/e2e.py` passes on any date, including dates after Nov 21, 2026
- [ ] All game dates in test fixtures are generated relative to "now" (no hardcoded years/months/days)
- [ ] Test runs in <15 seconds (same as today)
- [ ] CI workflow can run this test on any day without false failures

### Effort & Timeline

| Effort | Timeline | Owner |
|--------|----------|-------|
| **P** | 1 hour | Backend test engineer |

### CI/CD Integration

```yaml
# In .github/workflows/test.yml, add date test:
- name: Run E2E tests (verify date-agnostic)
  run: |
    # Run on today's date
    python3 tests/e2e.py
    # Verify tests would pass on future date (by checking code, not clock)
    grep -q "quando(nDias" tests/mock-backend.js || exit 1
    grep -q "get_future_date()" tests/e2e.py || exit 1
```

---

## GAP S4: No Relative Date Support in `quando()`

### Current State

- **What's broken:** The `quando()` helper function exists in `mock-backend.js` but is **not used** in `e2e.py`. Test dates are hardcoded in Python; mock-backend vitrine dates use `quando()` but other test fixtures don't.
- **Impact:** Inconsistency between test fixtures; some break in future, others don't; no documented pattern for adding relative dates to new tests.
- **Evidence:** `tests/mock-backend.js:124` defines `quando()` but it's only called for vitrine games, not for public games (line 114) or test games (line 119).
- **Severity:** HIGH (precursor to A1)
- **Effort:** M (1–2 days: needs Firebase Rules test harness)

### Test Strategy

1. Extend `quando()` to cover all date fields in test fixtures (not just vitrine).
2. Create a parallel `getDate()` utility in `e2e.py` that generates ISO8601 dates relative to "now".
3. Document the pattern: "All test dates must be relative to test execution time."
4. Add a linter rule to flag hardcoded dates in test files.

### Test Cases

1. **TC-S4-001: `quando()` generates valid ISO8601 for all offsets**
   - Call `quando(-7, 9)` (7 days ago at 9 AM)
   - Call `quando(0, 12)` (today at noon)
   - Call `quando(30, 23)` (30 days ahead at 11 PM)
   - Expected: All return valid ISO8601 strings; dates are past/future relative to call time

2. **TC-S4-002: Mock-backend public game uses `quando()`**
   - Remove hardcoded `2026-11-21T18:00` from `store.set("jogos/pub1"...)`
   - Replace with `quando(+1, 18)` (tomorrow at 6 PM)
   - Load test with `?compub` and inspect game date
   - Expected: Game date is always tomorrow at 6 PM, regardless of current date

3. **TC-S4-003: E2E test scenario A uses Python relative date**
   - Replace `await pg.fill("#f-quando", "2026-11-21T18:00")` with dynamic date
   - Expected: Form accepts the date; game is created with future date

4. **TC-S4-004: Date validation accepts relative dates near boundaries**
   - Test game 2 minutes in future (should accept)
   - Test game 1 minute in future (should accept)
   - Test game now (should reject)
   - Expected: Validation logic uses wall-clock time, not day boundary

### Infrastructure Needed

- **Code changes:**
  - `tests/mock-backend.js`: Refactor hardcoded dates to use `quando()` (line 114, 119)
  - `tests/e2e.py`: Add `get_future_date(ndays, hour)` utility (~10 lines)
- **Testing tools:** Python `datetime`, JavaScript `Date`
- **CI/CD:** No new infrastructure
- **Documentation:** Add comment in `tests/mock-backend.js` explaining `quando()` pattern

### Success Criteria

- [ ] All test fixture dates use relative date helpers (0 hardcoded dates)
- [ ] `quando(nDays, hour)` is documented and used consistently
- [ ] E2E tests pass on any date without modification
- [ ] New tests added after this uses relative dates by default
- [ ] Code review checklist includes "Date is relative (or explain why hardcoded)"

### Effort & Timeline

| Effort | Timeline | Owner |
|--------|----------|-------|
| **M** | 1–2 days | Backend test engineer |

### CI/CD Integration

```yaml
# Add lint rule to prevent hardcoded dates:
- name: Lint: Check test dates are relative
  run: |
    # Fail if test file contains hardcoded date in 2026
    if grep -rE '202[0-9]-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])' tests/*.py tests/*.js \
       | grep -v quando | grep -v '# hardcoded for' ; then
      echo "ERROR: Test contains hardcoded date"
      exit 1
    fi
```

---

## GAP S5: Firebase Rules Untested; Mock-Backend Diverges from Real Rules

### Current State

- **What's broken:** 
  - `firestore.rules` enforces security (e.g., only dono can delete game, only team reads WhatsApp), but **no test validates these rules**.
  - `mock-backend.js` reimplements the same logic by hand (`podeEscrever()`, `podeLer()`) but already diverges from real rules (see GAP S1, S2).
  - A bug in `firestore.rules` will pass all E2E tests (which use mock) and reach production undetected.
- **Impact:** Security vulnerabilities (S1–S3 in AUDITORIA-COMPLETA) go untested; mobile and security regressions have no test layer; Fase 1 ship is exposed.
- **Evidence:** `tests/mock-backend.js:35–38, 53–57`; zero tests in Firebase emulator; Firebase Rules validation never runs in CI.
- **Severity:** HIGH
- **Effort:** G (1 week: full Firestore emulator setup + test harness)

### Test Strategy

1. Stand up Firebase Emulator (Firestore + Auth) in CI and locally.
2. Write test suite that validates `firestore.rules` directly (not via mock-backend).
3. For each rule, write attack scenario + defense scenario (e.g., "unauthenticated user tries to read all profiles" should fail; "authenticated user reads own profile" should pass).
4. Migrate E2E tests to run against **both** mock-backend (fast feedback) **and** emulator (security validation).

### Test Cases

**Rule S1: Coleta de WhatsApp de organizadores (unauthorized read)**

5. **TC-S5-S1-001: Unauthenticated user reads all games and contato/dono**
   - Write as: query `jogos` collection (OK), query `jogos/g1/contato/dono` (should DENY)
   - Expected: Can read game, cannot read WhatsApp contact

6. **TC-S5-S1-002: Authenticated non-dono reads contato/dono of private game**
   - User A (uid=u_a) owns game g1, User B (uid=u_b) has no confirmacao
   - User B tries read `jogos/g1/contato/dono`
   - Expected: DENY, User B gets permission-denied

7. **TC-S5-S1-003: Authenticated non-dono WITH confirmacao reads contato**
   - User A owns game g1, User B has confirmacao for g1
   - User B reads `jogos/g1/contato/dono`
   - Expected: ALLOW, User B sees WhatsApp (because they're confirmed in game)

**Rule S2: Fila manipulável (server timestamp enforcement)**

8. **TC-S5-S2-001: User writes confirmacao with custom criadoEm timestamp**
   - Write: `confirmacoes/g1_u_b` with `criadoEm: 999999999` (attacker tries to jump queue)
   - Expected: DENY or ALLOW only if `criadoEm == request.time` (once Trecho 1 is applied)

9. **TC-S5-S2-002: User writes confirmacao with server timestamp**
   - Write: `confirmacoes/g1_u_b` with `criadoEm: request.time`
   - Expected: ALLOW, timestamp locks queue order

**Rule S3: Team entry gives access (code-based gating)**

10. **TC-S5-S3-001: User enters team with wrong code**
    - Existing user knows code is `abc123`, tries to write `admins/u_new` with code `wrongcode`
    - Expected: DENY, user not added to team

11. **TC-S5-S3-002: User enters team with correct code (first time only)**
    - Code is `abc123`, user writes `admins/u_new` with correct code
    - Expected: ALLOW, user added
    - User tries again: DENY (rule checks `!store.has(p)`)

**Rule S6: Game in past**

12. **TC-S5-S6-001: User creates game with past timestamp**
    - Write game with `quando: "2000-01-01T10:00"`
    - Expected: ALLOW (rule doesn't check date yet, Trecho 4 fixes this)

**General rules**

13. **TC-S5-GEN-001: Team member reads all profiles and WhatsApp**
    - User A is team (has doc in admins), queries `perfis` and reads `perfis/u_other/whatsapp`
    - Expected: ALLOW

14. **TC-S5-GEN-002: Non-team player reads own profile**
    - User B reads `perfis/u_b` (self)
    - Expected: ALLOW

15. **TC-S5-GEN-003: Non-team player reads another profile**
    - User B reads `perfis/u_other`
    - Expected: DENY

### Infrastructure Needed

- **Firebase Emulator Suite:**
  - Install: `npm install --save-dev firebase-tools@latest`
  - Configure: `firebase.json` with emulator settings
  - Start in CI: `firebase emulators:start --only firestore,auth`
  
- **Test harness:**
  - Language: Python (to match existing `e2e.py`)
  - SDK: `firebase-admin-python` (server SDK, can disable auth check)
  - File: `tests/firestore-rules.py` (~300 lines)
  
- **Environment:**
  - Service account key (CI-only, restricted permissions)
  - Or use emulator auth tokens (recommended for open source)

- **CI/CD:**
  - Run emulator on `localhost:8080` (Firestore) + `localhost:9099` (Auth)
  - After tests: collect coverage report

### Success Criteria

- [ ] Firebase Rules test suite exists and validates all 15 test cases above
- [ ] Suite runs in <2 minutes (emulator is fast)
- [ ] CI runs rules tests on every push to `main`
- [ ] No new merge to main until rules tests pass
- [ ] Rules test coverage >= 80% (all branches exercised)
- [ ] Mock-backend is updated to match real rules (or docs explain divergence)
- [ ] E2E tests now run twice: once with mock, once with emulator (nightly or on-demand)

### Effort & Timeline

| Effort | Timeline | Owner | Blockers |
|--------|----------|-------|----------|
| **G** | 1 week | Backend + DevOps | Firebase emulator setup; CI pipeline changes |

### CI/CD Integration

```yaml
# In .github/workflows/security-tests.yml
- name: Start Firebase Emulator
  run: |
    npm install -g firebase-tools
    firebase emulators:start --only firestore,auth --project test &
    sleep 3

- name: Run Firestore Rules tests
  run: |
    pip install firebase-admin
    python3 tests/firestore-rules.py

- name: Rules coverage report
  run: |
    firebase emulators:exec 'python3 tests/firestore-rules-coverage.py' --project test
```

---

## GAP D3: WhatsApp Embedded Browser Untested (Android/iPhone)

### Current State

- **What's broken:**
  - Convite link opens in WhatsApp's embedded browser (not Chrome/Safari), which **blocks popups by default**.
  - E2E tests run in headless Chromium, which allows popups—test passes, but real user sees broken login.
  - Game public access requires Google login (popup), and popup is blocked in WhatsApp browser. No fallback.
  - Form rejects login if popup fails; user cannot enter game via link.
- **Impact:** Users invited to public games cannot join (top funnel blocker); private games work (no login needed).
- **Evidence:** `firebase.js:49` (login popup), `index.html:1456–1463` (public game requires login); README demo assumes Privado.
- **Severity:** HIGH (affects public game hypothesis)
- **Effort:** G (2–3 days: mobile device lab or emulator, test harness)

### Test Strategy

1. Detect when app runs in WhatsApp browser (User-Agent contains `WhatsApp`).
2. Redirect popups to redirect flow (deep link to external browser) or inline iframe approach.
3. Test on Android and iOS with actual WhatsApp app (or emulator).
4. Add E2E test that simulates WhatsApp browser blocking popups.

### Test Cases

**Browser detection & fallback**

1. **TC-D3-001: Detect WhatsApp browser on Android**
   - Open app link in WhatsApp Android
   - Inspect `navigator.userAgent`
   - Expected: Contains `WhatsApp` or `Android`

2. **TC-D3-002: Detect WhatsApp browser on iOS**
   - Open app link in WhatsApp iOS
   - Inspect `navigator.userAgent`
   - Expected: Contains `WhatsApp` or `iPhone`

3. **TC-D3-003: Fallback login from popup failure**
   - Set User-Agent to simulate WhatsApp
   - Attempt Google login (popup will be blocked)
   - Expected: App shows "Open in browser" button instead of error; button opens external browser

**Public game join from WhatsApp**

4. **TC-D3-004: User opens public game invite link in WhatsApp Android**
   - Invite link: `https://app.com/#convite-g1` for public game
   - Open in WhatsApp Android
   - Expected: Can view game details and "Tô dentro" button (no login popup needed)

5. **TC-D3-005: User opens public game, tries to sign in from WhatsApp**
   - Invite link opens in WhatsApp browser
   - User taps "Entrar com Google"
   - Expected: Browser redirects to external Chrome/Safari; login succeeds; redirects back to app

6. **TC-D3-006: Private game invite link works in WhatsApp**
   - Invite link: `https://app.com/#convite-g1` for private game (no login required)
   - Open in WhatsApp Android and iOS
   - Expected: Can view game and confirm without login on both

**E2E with popup block simulation**

7. **TC-D3-007: E2E test simulates WhatsApp popup block**
   - Modify `e2e.py` to set User-Agent to WhatsApp
   - Block popups in Playwright context
   - Try to join public game
   - Expected: App handles blocked popup gracefully (not crash or hang)

8. **TC-D3-008: E2E test private game works in WhatsApp**
   - Set User-Agent to WhatsApp
   - Block popups
   - Try to confirm private game via invite link
   - Expected: Confirmation succeeds without popup

### Infrastructure Needed

- **Local testing:**
  - Android emulator (Android Studio) or real device (USB + adb)
  - iOS simulator (macOS Xcode) or real device
  - WhatsApp installed on simulator/device
  
- **Device lab (optional, for CI):**
  - BrowserStack, AWS Device Farm, or Sauce Labs ($ per month)
  - Or: GitHub Actions with Android emulator (free, but slow)
  
- **Code changes:**
  - `firebase.js`: Detect WhatsApp browser, add fallback login flow
  - `index.html`: Handle popup failures, show "Open in browser" button
  - `tests/e2e.py`: Add User-Agent simulation, disable popups
  
- **Testing tools:**
  - Playwright (already used)
  - `adb` for Android emulator
  - Xcode command-line tools for iOS

### Success Criteria

- [ ] User can join public game via WhatsApp link on Android (manual test on device or emulator)
- [ ] User can join public game via WhatsApp link on iOS (manual test on device or simulator)
- [ ] E2E test passes with User-Agent=WhatsApp and popups disabled
- [ ] No errors in console when popup is blocked
- [ ] "Open in external browser" button appears if login needed in WhatsApp
- [ ] Private game links work in WhatsApp without popup
- [ ] CI runs WhatsApp+popup-block scenario on every push (or nightly)

### Effort & Timeline

| Effort | Timeline | Owner | Blockers |
|--------|----------|-------|----------|
| **G** | 2–3 days (feature) | Frontend | Mobile device availability; device lab cost |
| **M** | 1 day (testing only) | QA | Same as above |

**Recommended approach for Fase 1:**
- Manual test on Android emulator (free) + iOS simulator (free if on Mac)
- Record video of join flow in WhatsApp
- E2E test with popup block (1 hour, Playwright already supports)
- Defer device lab to Fase 2

### CI/CD Integration

```yaml
# In .github/workflows/whatsapp-test.yml (run on PR, not push)
- name: Setup Android Emulator
  run: |
    npm install -g emu-runner
    emu-runner --start --avd Pixel_4_API_28 &
    sleep 10

- name: Test app in WhatsApp browser simulator
  run: |
    python3 tests/e2e-whatsapp.py

- name: Check no console errors
  run: |
    grep -i "popup\|blocked\|error" test-output.log && exit 1 || true
```

---

## GAP H2: Migration Not Validated for Data Corruption

### Current State

- **What's broken:**
  - App has no data migration logic (e.g., "if `v < 3`, update schema X").
  - If rules change and existing documents become invalid (e.g., adding required field), app crashes or corrupts state.
  - PWA cached data may be from old version; app + backend schema mismatch is not detected.
  - No validation on app load ("Does cached data match current schema?").
  - No rollback plan if Firestore data is corrupted.
- **Impact:** Upgrade to Fase 2 risks data loss; real users' games disappear or become unplayable; no recovery path.
- **Evidence:** No `migrate()` function in `index.html`; `sw.js` caches all collections without version tag; schema defined only in rules (not in code).
- **Severity:** HIGH
- **Effort:** G (1+ week: data model, migration framework, rollback)

### Test Strategy

1. Define schema (document shape) for each collection: `jogos`, `confirmacoes`, `perfis`, `arenas_piloto`.
2. Create migration framework: `migrate(oldVersion, newVersion, data)` function.
3. Write test that:
   - Loads old schema version into Firestore
   - Runs app upgrade
   - Validates data is migrated or error is recoverable
4. Test rollback: downgrade app, verify no crash.
5. Test cache invalidation: PWA cache stale, app detects and clears.

### Test Cases

**Schema validation on startup**

1. **TC-H2-001: App loads with valid schema**
   - Firestore has game: `{ arena, cidade, quando, esporte, nivel, ... }` (all required fields)
   - App loads, queries games
   - Expected: No errors, game displays correctly

2. **TC-H2-002: App loads with missing optional field (backward compatible)**
   - Firestore has game WITHOUT `visibilidade` field (added in later version)
   - App loads
   - Expected: App does not crash; uses default value (e.g., `visibilidade = "privado"`)

3. **TC-H2-003: App loads with missing required field (data corruption)**
   - Firestore has game WITHOUT `quando` field (required)
   - App loads
   - Expected: App detects corruption, shows error, offers recovery (e.g., "Reload" or "Contact support")

**Migration logic**

4. **TC-H2-004: Migrate v1 games to v2 (schema change)**
   - Firestore has old game schema (hypothetical): `{ jogo, horario }` (before "arena" and "cidade" were added)
   - App detects version mismatch (stored in `config/app-version`)
   - Migration runs: adds `arena=""`, `cidade=""`, maps `jogo` to `esporte`
   - Expected: Game is playable after migration; no data loss

5. **TC-H2-005: Migration fails and rolls back**
   - During migration, database is unreachable
   - Expected: App reverts to cached data, shows "Offline" state, no corruption

6. **TC-H2-006: Confirmacoes migrated with games**
   - Game is migrated, confirmacoes for that game are also checked for schema validity
   - Expected: Confirmacoes without required fields are marked as corrupt or deleted with user notification

**PWA cache invalidation**

7. **TC-H2-007: PWA cache stale, app detects**
   - Install PWA v1, cache data
   - Update app to v2 (bump `VERSAO` in `sw.js`)
   - User opens app (Service Worker updates)
   - Expected: Old cached data is cleared; fresh data loaded from Firestore

8. **TC-H2-008: PWA upgrade, offline fallback**
   - User is offline, app v1 cached
   - v2 deployed, Service Worker updates but data fetch fails (offline)
   - Expected: App shows "Offline" with cached data, no crash

**Rollback scenario**

9. **TC-H2-009: User downgrades app (PWA or mobile)**
   - v2 is deployed and cached
   - User downgrades to v1 (via install link or old app build)
   - Expected: App loads with v1 UI, no crash; users can still view existing data

10. **TC-H2-010: Firestore has v2 schema, app v1 tries to read**
    - Firestore documents have v2 fields that v1 doesn't expect
    - v1 app queries and renders
    - Expected: v1 app ignores unknown fields, renders correctly

### Infrastructure Needed

- **Code changes:**
  - `index.html`: Add `initSchema()` function to validate document structure
  - `index.html`: Add `migrate(oldVer, newVer, docs)` function
  - `sw.js`: Add version tag to cached collections (`jogos-v2`, `confirmacoes-v2`)
  - `config.js`: Add `APP_VERSION = 1` constant
  
- **Data model (new file: `SCHEMA.md`):**
  - Document required/optional fields for each collection
  - Version history (what changed in v2, v3, etc.)
  
- **Testing tools:**
  - Firestore emulator (already needed for S5)
  - Playwright for E2E (already used)
  - Python to seed Firestore with old schema
  
- **CI/CD:**
  - Migration test suite runs on every commit
  - Nightly: full rollback/upgrade scenario

### Success Criteria

- [ ] Schema defined in `SCHEMA.md` with version history
- [ ] `initSchema()` validates all documents on startup
- [ ] Migration function exists and handles v1→v2, v2→v3, etc.
- [ ] All 10 test cases pass
- [ ] Rollback from v2 to v1 is tested and documented
- [ ] PWA cache invalidation works (Service Worker detects version mismatch)
- [ ] No data loss in any migration scenario
- [ ] CI runs migration tests on every push

### Effort & Timeline

| Effort | Timeline | Owner | Blockers |
|--------|----------|-------|----------|
| **G** | 1–2 weeks | Backend + DevOps | Schema design review; Firestore emulator setup |

### CI/CD Integration

```yaml
# In .github/workflows/migration-tests.yml
- name: Start Firebase Emulator
  run: |
    firebase emulators:start --only firestore &
    sleep 3

- name: Seed old schema
  run: |
    python3 tests/seed-firestore-v1.py

- name: Run migration tests
  run: |
    python3 tests/migration.py

- name: Verify no data loss
  run: |
    python3 tests/validate-migration-data.py

- name: Test rollback
  run: |
    python3 tests/rollback-test.py
```

---

## GAP RC: Race Condition – 2 Users Confirm Last Vaga Simultaneously

### Current State

- **What's broken:**
  - When game has 1 vaga left, two users can confirm simultaneously (both see 1 vaga available, both write confirmacao).
  - App counts vagas client-side only (from `index.html:427`); no server validation.
  - Firestore allows duplicate confirmacoes for same user, but doesn't prevent 2nd user from joining full game.
  - Result: Game shows "Fechou" (closed), but 3rd person already in after 2 people joined in race.
- **Impact:** Revenue is miscalculated (shows 3 people when space is 2); trust is broken (user excluded despite confirming); SMS/WhatsApp says game is full but actually has slot.
- **Evidence:** No `Firestore.transaction()` in `firebase.js`; no server-side vaga counter; rule allows any confirmacao as long as game exists (`:61–71` checks format, not capacity).
- **Severity:** HIGH (business logic, not just UX bug)
- **Effort:** M (2–3 days: transaction logic, test harness)

### Test Strategy

1. Add server-side vaga counter to `confirmacoes` write (e.g., Firestore transaction: "if currentConfirmCount < vagas, write confirmacao, else reject").
2. Update rule (Trecho 3 in AUDITORIA-COMPLETA) to validate count at write time.
3. Update app to handle race (show "Game full" if race lost; offer next similar game).
4. Test race with simultaneous writes (Playwright + multiple browser contexts).

### Test Cases

**Single-threaded normal case (baseline)**

1. **TC-RC-001: User confirms last vaga (normal path)**
   - Game has 1 vaga, 3 of 4 confirmed
   - User confirms (write confirmacao/g1_u_new)
   - Expected: Confirmacao succeeds, vagas becomes 0, game shows "Fechou"

**Race condition: two users, one slot**

2. **TC-RC-002: Two users confirm last vaga simultaneously (race)**
   - Game has 1 vaga, 3 of 4 confirmed, U_A and U_B both see game
   - Both click "Confirmar" at same time
   - Expected (before fix): Both confirmacoes written, game shows 5 people confirmed (overflow)
   - Expected (after fix): One succeeds, one gets "Game is full" error

3. **TC-RC-003: Race with Firestore transaction (atomic check)**
   - Add transaction: `beginTransaction()` → check confirmCount → write confirmacao → check vagas match → commit
   - Two users try to confirm last vaga at same time (via Firestore write, not UI button)
   - Expected: One write succeeds, one fails with "Game full" before confirmacao is written

4. **TC-RC-004: User gets notified when race is lost**
   - User U_B loses race to U_A
   - U_B's confirmacao write fails
   - Expected: UI shows "Sorry, game filled up" with option to find similar game

**Edge cases**

5. **TC-RC-005: Exact number of vagas met**
   - Game created with 2 vagas, total 2 (1v1 game)
   - User 1 confirms: 1 vaga left
   - User 2 confirms: 0 vagas left, game is full
   - User 3 tries to confirm: should fail
   - Expected: User 3 sees "Game is full"

6. **TC-RC-006: Over-subscription prevented**
   - Game has 2 vagas, 10 users try to confirm at once (via backend load test)
   - Expected: Exactly 2 succeed, 8 get "Game full"

7. **TC-RC-007: Dono can override race (remove confirmacao)**
   - Game is full after race (overflow state before fix)
   - Dono removes one confirmacao manually
   - Expected: Game vagas updates to 1, app recalculates

**Server-side validation**

8. **TC-RC-008: Rule validates confirmacao count at write**
   - Game has 2 vagas; write 3rd confirmacao directly (via emulator or curl)
   - Expected: Firestore rule rejects write (Trecho 3: `count(confirmacoes) < vagas`)

9. **TC-RC-009: Migration: add vaga counter to game**
   - Existing games have no `vaga_counter` field
   - Migration runs, adds counter based on current confirmacoes
   - Expected: Counter matches reality; future writes use counter

### Infrastructure Needed

- **Code changes:**
  - `firebase.js`: Wrap confirmacao write in Firestore transaction
  - `index.html`: Handle race (show "Game full" error, offer alternatives)
  - `firestore.rules`: Add vaga count validation (Trecho 3 proposed in AUDITORIA)
  
- **Testing tools:**
  - Playwright multi-context (simulate 2 browsers confirming at once)
  - Firebase emulator (Firestore transactions support)
  - Load test tool (optional, for TC-RC-006)
  
- **CI/CD:**
  - Race test runs on emulator
  - Load test runs weekly (optional)

### Success Criteria

- [ ] Two simultaneous confirmacoes cannot exceed vagas (atomic at database level)
- [ ] Race loser gets clear error message
- [ ] Game never shows more confirmacoes than vagas
- [ ] E2E test demonstrates race condition is handled (TC-RC-002, RC-003)
- [ ] Server rule validates vaga count (no client-side bypass)
- [ ] Existing games have vaga counter migrated correctly
- [ ] CI test passes; race handling is deterministic (repeatable)

### Effort & Timeline

| Effort | Timeline | Owner | Blockers |
|--------|----------|-------|----------|
| **M** | 2–3 days | Backend | Firestore transaction support; rule testing (needs emulator) |

### CI/CD Integration

```yaml
# In .github/workflows/race-test.yml
- name: Start Firebase Emulator
  run: |
    firebase emulators:start --only firestore &
    sleep 3

- name: Run race condition tests
  run: |
    python3 tests/race-condition.py

- name: Verify no overflow (data integrity check)
  run: |
    firebase emulators:exec 'python3 tests/validate-vaga-count.py' --project test
```

---

## Prioritization Matrix & Shipping Checklist

### By Priority Level

| Gap | Type | Priority | Effort | Timeline | Blocker for Fase 1? |
|-----|------|----------|--------|----------|-------------------|
| **A1** | Tests break on 21/11 | P | P | 1 hour | YES (CI fails after date) |
| **S4** | Relative dates in quando() | P | M | 1–2 days | YES (precursor to A1) |
| **S5** | Firebase Rules untested | P | G | 1 week | YES (security unknown) |
| **D3** | WhatsApp browser untested | P | G | 2–3 days | YES (public game hypothesis) |
| **H2** | Migration not validated | M | G | 1–2 weeks | MAYBE (defer to Fase 1.5) |
| **RC** | Race condition on vaga | M | M | 2–3 days | YES (revenue integrity) |

### Recommended Phase-In for Fase 1 Ship

**Week 1 (Pre-launch, non-blocking hotfixes):**
- [ ] A1 & S4: Fix hardcoded dates (1–2 hours total)
- [ ] Add lint rule to prevent date regression

**Week 2 (Launch window, manual validation):**
- [ ] D3: Manual test on Android emulator (WhatsApp browser)
- [ ] Record demo video of public game join via link
- [ ] D3 fallback: If WhatsApp popup fails, disable public games for Fase 1; mark as "Team only"

**Post-launch (Fase 1 Ops):**
- [ ] RC: Implement race condition fix (2 days); deploy in hotfix
- [ ] S5: Set up Firebase Rules testing (1 week); run weekly
- [ ] H2: Plan migration framework (Fase 1.5); no customer data risk yet

### Shipping Gate: Fase 1 Readiness Checklist

```
MUST PASS (before launch):
  [ ] A1: Tests pass on any date (run dated 11-30-2026 to verify)
  [ ] S4: All test dates are relative (lint rule passes)
  [ ] D3: Manual test: invite link opens in WhatsApp Android emulator
  [ ] D3: If popup fails, app shows "Open in browser" button (manual check)
  [ ] RC: Race condition fixed OR documented as low-impact (< 1% of games, mitigated by team review)
  
SHOULD PASS (before launch, can defer 1 week):
  [ ] S5: Firestore Rules tested on emulator (5 key scenarios)
  [ ] CI: E2E tests run and pass in GitHub Actions
  
CAN DEFER (Fase 1.5):
  [ ] H2: Migration framework complete
  [ ] D3: Device lab testing (iOS real device)
  [ ] S5: 100% rule coverage (can start at 70%)
```

---

## Implementation Roadmap

### Week 1: Hotfixes (Before Soft Launch)

| Task | Owner | Days | Dependency | Gate |
|------|-------|------|------------|------|
| Fix A1 (hardcoded dates) | Test eng. | 0.5 | None | Tests pass |
| Fix S4 (relative dates) | Test eng. | 1 | A1 | Linter rule added |
| Manual D3 test on Android | QA | 1 | Emulator setup | Demo video recorded |
| **Subtotal** | | **2.5 days** | | **Ship gates cleared** |

### Week 2: Launch & Monitoring

| Task | Owner | Days | Dependency | Gate |
|------|-------|------|------------|------|
| Fix RC (race on vaga) | Backend | 2 | Firestore emulator | No game overflow in prod |
| Deploy race fix hotfix | DevOps | 0.5 | RC fix code | Hotfix tested |
| Monitor prod for S1/S2 exploits | Security | Daily | None | Incident response plan |
| **Subtotal** | | **2.5 days** | | **Launch healthy** |

### Weeks 3+: Hardening (Fase 1.5)

| Task | Owner | Days | Dependency | Gate |
|------|-------|------|------------|------|
| Set up Firebase Rules CI (S5) | Backend + DevOps | 5 | Emulator, rules harness | 70% coverage |
| Migration framework (H2) | Backend | 7 | Schema design review | Rollback plan approved |
| Device lab testing (D3 iOS) | QA | 3 | Device lab account | iOS demo recorded |
| **Subtotal** | | **15 days** | | **Fase 2 ready** |

---

## Effort Estimation Summary

| Category | Hours | Days | Owner |
|----------|-------|------|-------|
| **Hot fixes** (A1, S4) | 4 | 0.5 | Test engineer |
| **Manual testing** (D3 Android) | 8 | 1 | QA |
| **Race condition fix** (RC) | 16 | 2 | Backend |
| **Firebase Rules setup** (S5) | 40 | 5 | Backend + DevOps |
| **Migration framework** (H2) | 56 | 7 | Backend |
| **Device lab** (D3 iOS) | 24 | 3 | QA |
| **CI/CD integration** (all) | 24 | 3 | DevOps |
| **Documentation** (this roadmap) | 8 | 1 | QA Lead |
| **TOTAL (Fase 1 + 1.5)** | **180 hours** | **~23 days** | Cross-functional |

---

## Success Metrics & KPIs

### By Launch Date (Fase 1)

- [ ] Zero test failures due to hardcoded dates
- [ ] All public game invites open in WhatsApp browser (manual validation)
- [ ] No race condition game overflow (< 0.1% of games, monitored)
- [ ] 100% E2E test pass rate in CI/CD

### After Launch (Weeks 2–4)

- [ ] Zero data corruption incidents (migration non-issue)
- [ ] < 1% user report "Game full but I had spot"
- [ ] Security audit: zero S1/S2 exploits detected
- [ ] Firestore Rules test coverage >= 70%

### Fase 2 Readiness (Weeks 5+)

- [ ] Migration framework tested and approved
- [ ] Firebase Rules coverage >= 90%
- [ ] iOS device testing completed
- [ ] Rollback plan documented and rehearsed

---

## Appendix: Testing Infrastructure Setup Guide

### Local Development

**Prerequisites:**
```bash
pip install playwright firebase-admin pytest
playwright install chromium
npm install -g firebase-tools
```

**Run all tests locally:**
```bash
python3 tests/e2e.py              # E2E scenarios (uses mock-backend)
python3 tests/pwa.py              # PWA features
firebase emulators:start &        # Start Firestore + Auth emulator
python3 tests/firestore-rules.py  # Rules validation (against emulator)
python3 tests/migration.py        # Migration scenarios
```

### CI/CD Setup (GitHub Actions)

**New workflows to create:**
- `.github/workflows/e2e-tests.yml` – Run E2E tests on push to main
- `.github/workflows/security-tests.yml` – Firebase Rules tests (weekly or on-demand)
- `.github/workflows/migration-tests.yml` – Migration validation (on firestore.rules change)
- `.github/workflows/race-condition.yml` – Race tests (on index.html change to confirmacao logic)

**Shared: start emulator step**
```yaml
- name: Start Firebase Emulator
  run: |
    npm install -g firebase-tools
    firebase emulators:start --only firestore,auth &
    sleep 3
    echo "Emulator ready on localhost"
```

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| QA Lead | — | 2026-11-16 | DRAFT |
| Security | — | — | PENDING REVIEW |
| Backend | — | — | PENDING REVIEW |
| Product | — | — | PENDING REVIEW |

**Last updated:** 2026-11-16
**Next review:** After each gap is closed

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
