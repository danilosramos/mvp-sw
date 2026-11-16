# SECURITY-HOTFIXES.md

**Status:** CRITICAL  
**Date:** 2026-11-16  
**Severity:** 3 Critical Issues Requiring Immediate Action  
**Audience:** Security Team, Backend Leads, Product Management  

---

## Executive Summary

Three critical security vulnerabilities have been identified in the Energia Boa MVP that expose private game data, organizer contact information, and enable unrestricted write access. These issues require immediate mitigation before the arena pilot expands. This document provides day-1 mitigations and proper fixes with rollback strategies.

**Impact:**
- **Privacy:** Any Google account can enumerate and access all private games
- **Data Exposure:** Organizer WhatsApp numbers readable by unauthenticated users
- **Abuse:** Automated attacks bypass security controls; Firestore rules lack real validation

**Risk Timeline:** Medium (pilot phase with limited users, but discoverable and repeatable)

---

## ISSUE 1: S1 + S5 - Private Games Enumerable & Rules Unvalidated

### Threat Model & Attack Scenario

**Attack Vector:** Unauthenticated enumeration of private games combined with unvalidated Firestore rules

**Scenario:**
1. Attacker opens browser console and calls Firestore SDK directly
2. Query: `db.collection('jogos').where('visibilidade', '==', 'privado').get()`
3. Returns all private games created by any user (documents include game ID, location, time, organizer name)
4. Attacker obtains private game links and accesses restricted information
5. Can create fake confirmations, manipulate queues (since `criadoEm` is client-controlled)

**Current Gaps:**
- Firestore rules at line 170: `allow read: if true;` permits anyone to read any game
- No validation that private games are only accessible via direct link lookup
- Test suite (S5) uses mock backend that diverges from actual `firestore.rules`, creating false confidence
- `criadoEm` timestamps are client-generated (vulnerable to manipulation)

**Proof of Concept (Browser Console):**
```javascript
// Attacker can run this directly
db.collection('jogos')
  .where('visibilidade', '==', 'privado')
  .get()
  .then(snap => snap.docs.forEach(doc => console.log(doc.id, doc.data().donoZap)))
```

### Immediate Mitigation (Day 1 - 2 Hours)

**Option A: Disable Firestore Read Temporarily**
```
match /jogos/{id} {
  allow read: if false;  // Emergency: Breaks app completely
  allow create: if ehEquipe() || jogoDeJogadorValido();
  allow update: if ehEquipe();
  allow delete: if ehEquipe() || (request.auth != null && resource.data.donoUid == request.auth.uid);
}
```
**Consequence:** App becomes unusable. Only viable for <= 1 hour emergency.

**Option B: Restrict Private Game Reads (RECOMMENDED)**
```
match /jogos/{id} {
  allow read: if resource.data.visibilidade == 'publico' 
              || (request.auth != null && resource.data.donoUid == request.auth.uid)
              || ehEquipe();
  allow create: if ehEquipe() || jogoDeJogadorValido();
  allow update: if ehEquipe();
  allow delete: if ehEquipe() || (request.auth != null && resource.data.donoUid == request.auth.uid);
}
```
**Impact:** 
- Private games still readable by direct ID (links work)
- Prevents enumeration of private games
- Public games remain discoverable
- **Requires app change:** Add `visibilidade` field to all existing games (1-hour deploy + migration)

**Steps to Deploy:**
1. Run database migration to add `visibilidade: 'privado'` to all existing games
2. Update `firestore.rules` with Option B rules
3. Publish rules (Firebase Console, 2 minutes)
4. Clear browser cache
5. Test: Try querying `where('visibilidade', '==', 'privado')` in console → should return "PERMISSION_DENIED"

### Proper Fix (3-5 Days - Requires Code Changes)

**Implement Firestore Security Layers:**

1. **Enforce Server-Side Timestamps**
```firestore.rules
// Replace client-generated criadoEm with server timestamp
function jogoDeJogadorValido() {
  return request.auth != null
    && request.resource.data.criadoEm == request.time  // Server time only
    && ... (rest of validation)
}
```
App change: Use `serverTimestamp()` instead of `Date.now()`
```javascript
// BEFORE (vulnerable)
await db.doc(`jogos/${jogoId}`).set({
  ...jogoData,
  criadoEm: Date.now()  // Client time - manipulable
});

// AFTER (secure)
await db.doc(`jogos/${jogoId}`).set({
  ...jogoData,
  criadoEm: firebase.firestore.FieldValue.serverTimestamp()
});
```

2. **Move Confirmations to Subcollection** (Closes both S1 and S9)
```firestore.rules
match /jogos/{id}/confirmacoes/{cid} {
  allow read: if true;  // Can read only if you know jogoId
  allow create: if ehEquipe() 
                || confirmacaoPublicaValida(id, cid) 
                || confirmacaoDoDonoValida(id);
  allow delete: if ehEquipe() 
                || ehDonoDoJogo(id)
                || (request.auth != null && resource.data.get('uid', '') == request.auth.uid);
}
```
App changes:
- Write confirmations to `jogos/{jogoId}/confirmacoes/{confId}` instead of `confirmacoes/{confId}`
- Change read listeners from global `confirmacoes` to `jogos/{jogoId}/confirmacoes`
- Requires data migration (2-day backend task)

3. **Add Query-Time Validation** (Prevents enumeration)
App must use filtered queries matching Firestore rule requirements:
```javascript
// Valid queries only
db.collection('jogos')
  .where('visibilidade', '==', 'publico')
  .where('cidadeChave', '==', userCity)
  .get();

db.collection('jogos')
  .where('donoUid', '==', currentUserId)
  .get();
```

### Test Cases to Validate

**Test 1: Private Game Enumeration Prevention (CRITICAL)**
```javascript
// Setup: Create game with visibilidade: 'privado'
const jogoId = 'game-123';
const privadoJogo = {
  visibilidade: 'privado',
  donoUid: 'attacker-uid',
  donoZap: '5511999887766'
};

// Attempt enumeration as unauthenticated user
test('should DENY unauthenticated query for private games', async () => {
  const snap = await db.collection('jogos')
    .where('visibilidade', '==', 'privado')
    .get();
  expect(snap.empty).toBe(true);
  // OR expect error: 'PERMISSION_DENIED'
});

// Allow direct access with link
test('should ALLOW direct read of private game by ID', async () => {
  const snap = await db.collection('jogos').doc(jogoId).get();
  expect(snap.exists).toBe(true);
});
```

**Test 2: Queue Manipulation Prevention**
```javascript
test('should DENY client-generated criadoEm timestamps', async () => {
  const malformed = {
    ...validGame,
    criadoEm: Date.now()  // Client-generated
  };
  await expect(
    db.collection('jogos').add(malformed)
  ).rejects.toThrow('PERMISSION_DENIED');
});

test('should ACCEPT serverTimestamp for criadoEm', async () => {
  const valid = {
    ...validGame,
    criadoEm: firebase.firestore.FieldValue.serverTimestamp()
  };
  await expect(
    db.collection('jogos').add(valid)
  ).resolves.toBeDefined();
});
```

**Test 3: Firestore Rules Validation (Not Mock Backend)**
- Use Firebase Emulator Suite for all security tests
- Test against real `firestore.rules` file, not mock
- Include: enumeration attacks, timestamp manipulation, queue reordering, unauthorized reads

### Timeline & Effort

| Phase | Action | Effort | Timeline |
|-------|--------|--------|----------|
| **Day 1** | Deploy Option B (restrict private reads) + migration | M | 2 hours |
| **Day 2** | Add serverTimestamp() to app | P | 1-2 hours |
| **Days 3-5** | Migrate confirmations to subcollection | G | 3 days |
| **Testing** | Full rule validation with emulator | M | 1 day (parallel) |

**Critical Path:** Deploy Day 1 mitigation immediately. Full fix can proceed in parallel with arena pilot.

### Rollback Plan

**Rollback for Day 1 Mitigation (Option B):**
```firestore.rules
// Restore to original (vulnerable) state
match /jogos/{id} {
  allow read: if true;
  ...
}
```
- Publish via Firebase Console (2 minutes)
- Clear browser cache
- **Cost:** Private games become enumerable again (only during rollback window)
- **Detection:** Monitor Firestore read patterns for spike in `where()` queries

**Rollback for Proper Fix (Server Timestamps):**
- Keep both formats during transition period (accept `criadoEm` as number OR timestamp)
- Revert app to send `Date.now()` if needed
- **Data:** No data deletion needed; old confirmations remain readable

---

## ISSUE 2: H6 - Organizer WhatsApp in Public-Readable Game Document

### Threat Model & Attack Scenario

**Attack Vector:** Sensitive data stored in publicly-readable location

**Current Exposure:**
- Field: `donoZap` (organizer WhatsApp) stored directly in `/jogos/{id}` document
- Current Rule (line 170): `allow read: if true;`
- Result: Anyone with a game ID can read the organizer's WhatsApp number

**Scenario:**
1. Attacker discovers game ID (via enumeration, URL sharing, or brute force)
2. Fetches document: `db.collection('jogos').doc(gameId).get()`
3. Extracts `donoZap` field containing organizer's WhatsApp
4. Potential uses: Spam, impersonation, social engineering targeting organizers
5. Violation of LGPD (Brazilian data protection law) - unauthorized PII exposure

**Proof of Concept:**
```javascript
// Known game ID from URL or enumeration
const gameId = 'jogo_xyz123';
const gameData = await db.collection('jogos').doc(gameId).get();
const attackerHasWhatsApp = gameData.data().donoZap;  // Returns "5511987654321"
```

**Compliance Impact:**
- LGPD Article 5: Personal data processing requires consent
- LGPD Article 6: Unlawful processing liability
- **Fine exposure:** Up to 2% of annual revenue (or R$ 50 million)

### Immediate Mitigation (Day 1 - 1 Hour)

**Option A: Remove `donoZap` from Game Document (IMMEDIATE)**
```javascript
// 1. Update all existing games to delete donoZap
db.collection('jogos').get().then(snap => {
  snap.docs.forEach(doc => {
    doc.ref.update({ donoZap: firebase.firestore.FieldValue.delete() });
  });
});

// 2. Update firestore.rules to forbid new donoZap in games
function jogoDeJogadorValido() {
  return request.auth != null
    && request.resource.data.keys().hasOnly([
      'arena', 'esporte', 'nivel', 'quando', 'total', 'vagas', 'valor', 
      'situacao', 'teste', 'criadoEm', 'donoUid', 'donoNome', 
      // REMOVED: 'donoZap'
      'origem', 'visibilidade', 'cidade', 'cidadeChave', 'tipoLocal'
    ])
    && ...
}
```

**Store WhatsApp Securely Instead:**
- Use existing `/jogos/{id}/contato/{doc}` subcollection (line 177-185)
- Already protected: `allow read: if ehEquipe() || ehDonoDoJogo(id) || (has confirmation with uid)`
- App change: Move `donoZap` write from game creation to separate secure document

```javascript
// BEFORE (vulnerable)
await db.collection('jogos').doc(jogoId).set({
  donoZap: organzerWhatsApp,  // Public read!
  // ... other fields
});

// AFTER (secure)
await db.collection('jogos').doc(jogoId).set({
  // No donoZap here
  // ... other fields
});

// Store WhatsApp in protected subcollection
await db.collection('jogos').doc(jogoId)
  .collection('contato').doc('principal').set({
  zap: organizerWhatsApp
});
```

**Steps:**
1. Create migration script to remove `donoZap` from all games (5 minutes)
2. Update `firestore.rules` to remove `donoZap` from validation (5 minutes)
3. Test: Try reading `donoZap` field → should not exist
4. Update app to read from `/jogos/{id}/contato/principal` instead (requires auth)

### Proper Fix (2 Days - Backend Refactor)

**Implement Secure WhatsApp Storage Architecture:**

1. **Separate Contact from Game Metadata**
```firestore.rules
// Game document: public data only
match /jogos/{id} {
  allow read: if resource.data.visibilidade == 'publico' 
              || (request.auth != null && resource.data.donoUid == request.auth.uid)
              || ehEquipe();
  // donoZap NEVER stored here
}

// WhatsApp stored in protected subcollection
match /jogos/{id}/contato/{doc} {
  allow read: if ehEquipe() 
              || ehDonoDoJogo(id)
              || (request.auth != null && exists(/databases/$(database)/documents/confirmacoes/$(id + '_' + request.auth.uid)));
  allow write: if ehEquipe() || ehDonoDoJogo(id);
}
```

2. **App-Level Changes**
- Read WhatsApp only when needed (after confirmation or auth check)
- Display fallback: "Organizer contact not available" for unauthenticated users
- Lazy-load: Fetch contact info only when user clicks "Ligar/Chamar"

```javascript
// Load game metadata (public)
const gameRef = db.collection('jogos').doc(gameId);
const gameData = (await gameRef.get()).data();

// Load contact info only if user is authorized
let organizerContact = null;
try {
  const contactRef = db.collection('jogos').doc(gameId)
    .collection('contato').doc('principal');
  const contactData = (await contactRef.get()).data();
  organizerContact = contactData?.zap;  // Only if read permitted
} catch (e) {
  // User not authorized to read contact
  organizerContact = null;
}
```

3. **Data Audit**
- Query which games have `donoZap` exposed: `SELECT COUNT(*) FROM jogos WHERE donoZap IS NOT NULL`
- Identify how many organizers were exposed
- Document in security incident report
- Consider proactive notification to affected organizers

### Test Cases to Validate

**Test 1: Organizer WhatsApp Not in Public Game Document (CRITICAL)**
```javascript
test('should NOT expose donoZap in public game read', async () => {
  const jogoId = 'game-123';
  const gameData = await db.collection('jogos').doc(jogoId).get();
  
  expect(gameData.data()).not.toHaveProperty('donoZap');
});

test('should DENY game write with donoZap field', async () => {
  const malformedGame = {
    ...validGame,
    donoZap: '5511987654321'  // Attempt to include
  };
  
  await expect(
    db.collection('jogos').add(malformedGame)
  ).rejects.toThrow('PERMISSION_DENIED');
});
```

**Test 2: WhatsApp Only in Secure Subcollection**
```javascript
test('should ALLOW owner to read own contact info', async () => {
  const contactRef = db.collection('jogos').doc(ownGameId)
    .collection('contato').doc('principal');
  const contactData = await contactRef.get();
  
  expect(contactData.exists).toBe(true);
  expect(contactData.data().zap).toBeDefined();
});

test('should DENY unauthorized access to contact info', async () => {
  // Switch to different user (no confirmation in game)
  await switchUser('attacker-uid');
  
  const contactRef = db.collection('jogos').doc(someoneElsesGameId)
    .collection('contato').doc('principal');
  
  await expect(contactRef.get()).rejects.toThrow('PERMISSION_DENIED');
});
```

**Test 3: Enumeration of donoZap Values**
```javascript
test('should prevent scraping all WhatsApp numbers', async () => {
  // Attempt to query games to extract WhatsApp numbers
  const snap = await db.collection('jogos')
    .where('visibilidade', '==', 'publico')
    .get();
  
  snap.docs.forEach(doc => {
    expect(doc.data()).not.toHaveProperty('donoZap');
  });
});
```

### Timeline & Effort

| Phase | Action | Effort | Timeline |
|-------|--------|--------|----------|
| **Day 1** | Remove donoZap from rules + migrate data | P | 30 minutes |
| **Day 2** | Update app to read from `/contato` subcollection | P | 2 hours |
| **Testing** | Validate no public exposure of contact info | P | 1 hour |
| **Audit** | Identify and notify exposed organizers | M | 2 hours |

### Rollback Plan

**Immediate Rollback:**
```firestore.rules
// Add donoZap back to allowed fields
function jogoDeJogadorValido() {
  return request.auth != null
    && request.resource.data.keys().hasOnly([
      ..., 'donoZap', ...
    ])
}
```
- **Data restoration:** Backfill `donoZap` from contact subcollection
- **Cost:** PII exposure returns (only during rollback window)
- **Detection:** Difficult to detect exposure after the fact

**Recommended:** Keep fix in place. No rollback should be needed once migrated.

---

## ISSUE 3: App Check Insufficient - Doesn't Stop Real-Browser Attacks

### Threat Model & Attack Scenario

**Attack Vector:** Authenticated API abuse via real browser bypassing App Check

**Current State:**
- No App Check implementation (Firebase Console check: `config/equipe` has no token requirement)
- No rate limiting on API calls
- Rules don't validate App Check tokens in `Fase 1` (arena request phase)

**Attack Scenarios:**

**Scenario A: Automated Game Creation Loop**
```javascript
// Attacker with compromised/created Google account
for (let i = 0; i < 10000; i++) {
  await db.collection('jogos').add({
    arena: 'Arena' + i,
    esporte: 'Futebol',
    donoUid: attackerUid,
    // ... rest of game data
    criadoEm: firebase.firestore.FieldValue.serverTimestamp()
  });
}
// Result: Firestore quota exhausted, app goes offline
// Cost: ~100 reads/writes = ~$0.06 per 100K ops, but app becomes unusable
```

**Scenario B: Arena Pilot Data Poisoning**
```javascript
// 1. Create hundreds of fake arena requests
for (let i = 0; i < 500; i++) {
  await db.collection('arenas_piloto').add({
    arena: 'Fake Arena ' + i,
    whatsapp: '5511999999999' + i,
    modelo: 'jogo',
    // ... other fields
  });
}
// 2. Team sees 500 arena requests instead of real ~10
// 3. Can't distinguish signal from noise
// 4. Pilot metrics become unreliable
```

**Scenario C: Real Browser Abuse via Stolen Account**
```javascript
// Attacker owns or has access to real Google account
// Uses real browser → Passes all client checks
// Logs in to app → passes Firebase Auth
// But App Check token not required in rules → all operations succeed

// Can manipulate game queues (even with server timestamps):
await db.collection('jogos').doc(realGameId).set({
  status: 'cancelado',  // Cancel legitimate game
  vagas: 0  // Block all entries
});
```

**Current Gaps:**
1. No App Check integration in `firebase.js`
2. Firestore rules don't enforce App Check tokens for sensitive operations
3. No rate limiting (Firestore quotas are only circuit breaker)
4. Test endpoint (`arenas_piloto`) is wide-open to any authenticated user
5. No monitoring/alerting for unusual write patterns

### Immediate Mitigation (Day 1 - 4 Hours)

**Option A: Enable Firebase App Check** (Recommended for now)

1. **Enable in Firebase Console:**
   - Go to: Firestore Database → Rules → Security → App Check
   - Choose reCAPTCHA (doesn't require app rebuild)
   - Enable enforcement mode (optional: start with monitoring)

2. **Update Firestore Rules to Require App Check Token:**
```firestore.rules
function hasValidAppCheck() {
  return request.auth.token.firebase.sign_in_provider == 'anonymous'
      || request.auth.token.firebase.app_check_token != null;
}

match /jogos/{id} {
  allow read: if resource.data.visibilidade == 'publico' 
              || (request.auth != null && resource.data.donoUid == request.auth.uid)
              || ehEquipe();
  allow create: if (ehEquipe() || jogoDeJogadorValido()) 
                && hasValidAppCheck();  // NEW
  allow update: if ehEquipe() && hasValidAppCheck();  // NEW
  allow delete: if (ehEquipe() || (request.auth != null && resource.data.donoUid == request.auth.uid))
                && hasValidAppCheck();  // NEW
}

match /arenas_piloto/{id} {
  allow read, update, delete: if ehEquipe();
  allow create: if hasValidAppCheck();  // NEW - requires token for public submissions
}
```

3. **Update App to Initialize App Check:**
```javascript
// firebase.js - add after initializeApp
import { initializeAppCheck, ReCaptchaV3Provider } 
  from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app-check.js";

const app = initializeApp(cfg);
initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('YOUR_RECAPTCHA_PUBLIC_KEY'),
  isTokenAutoRefreshEnabled: true
});
```

**Benefits:**
- Stops most automated scripts (not all)
- Real browsers (legitimate + stolen accounts) can still use app
- Low user friction (invisible reCAPTCHA)
- **Important limitation:** Logged-in attackers with real accounts still bypass this

**Steps:**
1. Create reCAPTCHA v3 key pair in Google Cloud Console (5 minutes)
2. Add public key to `config.js` (1 minute)
3. Update `firebase.js` to initialize App Check (10 minutes)
4. Update `firestore.rules` with `hasValidAppCheck()` checks (10 minutes)
5. Deploy rules (2 minutes)
6. Test: Automated scripts should fail; browser-based usage should work

**Option B: Add Write Rate Limiting** (Medium-term, supplementary)

Firestore doesn't have built-in rate limiting. Use Cloud Functions:

```javascript
// Firebase Cloud Function (requires backend setup)
exports.enforceRateLimit = functions.firestore
  .document('jogos/{jogoId}')
  .onCreate(async (snap, context) => {
    const uid = snap.data().donoUid;
    const limiterRef = db.collection('_rate_limits').doc(uid);
    const limiter = await limiterRef.get();
    
    const now = Date.now();
    const windowStart = now - 3600000; // 1 hour
    
    if (limiter.exists) {
      const writes = limiter.data().writes.filter(t => t > windowStart);
      if (writes.length >= 10) {  // Max 10 games per hour
        // Delete the game or flag for review
        await snap.ref.delete();
        console.warn(`Rate limit exceeded for ${uid}`);
      }
    }
  });
```

**Cost:** Requires Firebase paid plan + backend development

### Proper Fix (1 Week - Backend + Architecture)

**Implement Defense-in-Depth:**

1. **Mandatory App Check + Persistent Tokens**
```firestore.rules
match /jogos/{id} {
  allow read: if resource.data.visibilidade == 'publico' 
              || (request.auth != null && resource.data.donoUid == request.auth.uid)
              || ehEquipe();
  allow create: if (ehEquipe() || jogoDeJogadorValido())
                && request.auth != null
                && request.auth.token.firebase.app_check_token != null
                && request.auth.token.firebase.sign_in_provider != null;
  allow update, delete: if (ehEquipe() || ehDonoDoJogo(id))
                        && request.auth.token.firebase.app_check_token != null;
}
```

2. **Backend Rate Limiting (Cloud Function)**
   - Track writes per user/hour
   - Block users exceeding threshold (10 games/hour, 50 arenas/day)
   - Log to Cloud Logging for monitoring

3. **Anomaly Detection**
   - Monitor for:
     - Spike in `arenas_piloto` creates (baseline: 2-3/day → alert at 50+/day)
     - Spike in failed authentication attempts
     - Multiple games with same contact info
   - Use Google Cloud Monitoring

4. **User-Level Monitoring**
   - Add `activity` collection to track sensitive operations
   - Log: `{ userId, action, timestamp, success/failure }`
   - Query before allowing sensitive operations

### Test Cases to Validate

**Test 1: Automated Script Blocked by App Check (CRITICAL)**
```javascript
test('should DENY game creation without App Check token', async () => {
  // Simulate no App Check (strip token from headers)
  const malformedRequest = {
    auth: {
      token: {
        firebase: {
          sign_in_provider: 'google.com'
          // Missing: app_check_token
        }
      }
    }
  };
  
  // This would be tested in emulator with rule validation
  await expect(
    db.collection('jogos').add(validGame)
  ).rejects.toThrow('PERMISSION_DENIED');
});
```

**Test 2: Legitimate Browser Usage Still Works**
```javascript
test('should ALLOW game creation with valid App Check token', async () => {
  // Real browser → has App Check token
  const gameRef = db.collection('jogos').doc();
  
  await expect(
    gameRef.set(validGame)
  ).resolves.toBeDefined();
});

test('should ALLOW authenticated user with App Check', async () => {
  await switchUser('valid-user-uid');
  const gameRef = db.collection('jogos').doc();
  
  await expect(
    gameRef.set(validGame)
  ).resolves.toBeDefined();
});
```

**Test 3: Rate Limiting Prevents Spam**
```javascript
test('should DENY excessive arena requests (>50/day)', async () => {
  for (let i = 0; i < 51; i++) {
    const result = await db.collection('arenas_piloto').add({
      arena: 'Spam Arena ' + i,
      whatsapp: '5511999999999',
      modelo: 'jogo'
    });
    
    if (i > 50) {
      expect(result).toBeUndefined();  // Should fail after limit
    }
  }
});
```

### Timeline & Effort

| Phase | Action | Effort | Timeline |
|-------|--------|--------|----------|
| **Day 1** | Enable App Check + update rules | P | 30 minutes |
| **Day 1** | Update firebase.js with reCAPTCHA | P | 30 minutes |
| **Day 2** | Test App Check enforcement | P | 2 hours |
| **Days 3-7** | Implement Cloud Functions rate limiting | G | 3 days |
| **Testing** | Monitor production for anomalies | M | 2 hours (setup only) |

### Rollback Plan

**Rollback for App Check Enforcement:**
```firestore.rules
// Remove hasValidAppCheck() requirement
match /jogos/{id} {
  allow create: if (ehEquipe() || jogoDeJogadorValido());
  // Revert: remove App Check token check
}
```
- Publish rules (2 minutes)
- **Cost:** App becomes vulnerable to automated attacks again
- **Detection:** Sudden spike in `arenas_piloto` creates or game writes

**Rollback App Check Integration:**
- Remove reCAPTCHA code from `firebase.js` and redeploy

---

## Implementation Priority & Sequence

### Critical Path (Must do first)

| Priority | Issue | Action | Timeline | Blocker |
|----------|-------|--------|----------|---------|
| **P0** | H6 | Remove `donoZap` from public games | 30 min | None |
| **P0** | S1 | Deploy Option B (restrict private reads) | 1 hour | None |
| **P1** | S5 | Add Firestore Emulator tests | 1 day | Rule validation |
| **P1** | App Check | Enable reCAPTCHA + rules | 1 hour | Arena pilot integrity |

### Full Implementation (Next sprint)

| Priority | Issue | Action | Timeline | Dependency |
|----------|-------|--------|----------|-----------|
| **P2** | S1 | Implement server timestamps | 2 days | P0 S1 complete |
| **P2** | S1 | Move confirmations to subcollection | 3 days | Server timestamps |
| **P2** | H6 | Audit affected organizers | 2 hours | P0 H6 complete |
| **P2** | App Check | Implement rate limiting (Cloud Functions) | 3 days | P1 App Check done |

---

## Validation & Sign-Off

### Pre-Deployment Checklist

- [ ] Database backup created (automated via Firebase)
- [ ] Firestore rules tested in emulator against all attack vectors
- [ ] App tested against updated rules (browser + mobile)
- [ ] Rollback procedure documented and tested
- [ ] Team trained on new validation rules
- [ ] Security lead sign-off obtained
- [ ] Arena pilot stakeholders notified of changes

### Post-Deployment Monitoring

**Metrics to Watch (First 24 hours):**
- Firestore write success rate (should remain >99%)
- Failed authentication attempts (baseline: <1/min → alert at >10/min)
- API error rates by error code (look for PERMISSION_DENIED spike)
- Arena pilot submissions (baseline: ~2-3/day → alert at >50/day)

**Logs to Review:**
```bash
# Check Firestore rule denials
gcloud firestore logs read --filter="severity=ERROR AND protoPayload.methodName=~'Create|Update|Delete'"

# Monitor authentication patterns
gcloud auth application-default logs read --filter="authenticationMethod != 'GOOGLE_SIGN_IN'"
```

---

## Communication Plan

### Internal (Day 0, Before Deployment)

- [ ] Notify backend team of rule changes
- [ ] Alert arena pilot organizers (non-technical: "Security improvements")
- [ ] Prepare incident response team

### External (Post-Fix Validation)

- [ ] Document security improvements in AUDITORIA.md
- [ ] Update README with security best practices for extensions
- [ ] File LGPD incident response if needed (contact legal)

---

## References

- **AUDITORIA-COMPLETA.md:** Full security audit findings (Sections 2.3: S1, S5, H6)
- **firestore.rules:** Current Firestore access control rules
- **firebase.js:** Firebase SDK initialization (requires App Check integration)
- **LGPD Compliance:** Lei Geral de Proteção de Dados Pessoais (Articles 5, 6)
- **Firebase Security Best Practices:** https://firebase.google.com/docs/database/security/start

---

## Appendix: Testing Commands

### Manual Testing (Browser Console)

**Test 1: Enumeration Prevention**
```javascript
// Should return PERMISSION_DENIED or empty
db.collection('jogos')
  .where('visibilidade', '==', 'privado')
  .get()
  .then(snap => console.log('Found:', snap.size, 'games'))
  .catch(e => console.log('Error (expected):', e.code));
```

**Test 2: Direct Link Still Works**
```javascript
// Should return game data (private or public)
db.collection('jogos').doc('game-id-from-link').get()
  .then(doc => console.log('Game:', doc.data()))
  .catch(e => console.log('Error:', e.code));
```

**Test 3: No donoZap Exposure**
```javascript
// Should NOT have donoZap field
db.collection('jogos').doc('any-game-id').get()
  .then(doc => {
    console.log('Has donoZap?', 'donoZap' in doc.data());
  });
```

**Test 4: App Check Status**
```javascript
// Check if App Check is initialized
console.log('App Check initialized:', firebase.appCheck() !== undefined);
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-11-16  
**Next Review:** 2026-11-23 (post-deployment validation)
