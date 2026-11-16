# Modelo de Dados — Energia Boa

**Fonte de autoridade:** [`PRD.md` seção 8](../product/01-prd-phase1-2.md#8-modelo-de-dados-e-migração)

**Data:** 16/11/2026  
**Escopo:** Schema completo de Firestore (Fase 1 + Fase 2)

---

## Resumo

**8 coleções** em Fase 1, **+1 novo** em Fase 2.

| Coleção | Fase | Tipo | Proposito |
|---------|------|------|-----------|
| `config/` | 1+ | Root | Configuração do time e app |
| `jogos/{id}` | 1+ | Root → Raiz | Jogos (público/privado) |
| `confirmacoes/{cid}` | 1 | Root | Confirmações (move para subcol em Fase 2) |
| `perfis/{uid}` | 1+ | Root | Perfil do jogador |
| `admins/{uid}` | 1+ | Root | Membros do time |
| `arenas_piloto/{id}` | 1+ | Root | Ofertas de piloto |
| `interesse_premium/{uid}` | 1+ | Root | Respostas Premium |
| `arenas/{aid}` | 2 | Root | Arenas parceiras (novo) |
| `jogos/{id}/confirmacoes/{cid}` | 2 | Subcol | Confirmações (novo local) |
| `jogos/{id}/contatos/{cid}` | 2 | Subcol | Contatos (WhatsApp restrito) |
| `arenas/{aid}/privado/piloto` | 2 | Subcol | Dados comerciais arena |

**Total leitura Fase 1:** ~100-200 docs/mês (escala piloto)  
**Total leitura Fase 2:** Reduz com subcoleções filtradas

---

## Fase 1: Coleções Raiz

### config/equipe
Documento único para configuração do time.

```json
{
  "codigo": "ABC123",           // 6 chars, único
  "preco_pos_piloto": 100,      // R$, opcional
  "endereço_oficial": "..."     // URL app
}
```

**Acesso:**
- Leitura: Time, aplicação
- Escrita: Time (console Firebase)

---

### config/versao
Versionamento da app.

```json
{
  "versao": "2026.11.16",       // YYYY.MM.DD
  "minima": "2026.11.09",       // Força update (A4)
  "changelog": "..."            // Notas
}
```

**Acesso:**
- Leitura: Pública (service worker)
- Escrita: CI/CD (GitHub Actions)

---

### jogos/{id}
Um jogo de esporte em um horário.

**Campos principais:**

```json
{
  // ID & Timing
  "id": "[20 chars random]",
  "quando": "2026-11-21T18:30",           // Local, sem fuso
  "quandoTs": 1700604600000,              // Timestamp UTC
  "criadoEm": 1700600000000,              // Server time (Fase 1: número antigo)

  // Esporte & Local
  "esporte": "Vôlei de praia",
  "arena": "Reis D'arena",
  "tipoLocal": "privada",                 // ou "publica"
  "cidade": "São Paulo",
  "cidadeChave": "sao-paulo",             // Normalizado

  // Participantes
  "total": 4,
  "vagas": 2,
  "nivel": 3,                             // 1, 3 ou 5
  "valor": 120,                           // R$, ou null se quadra pública

  // Status
  "estado": "aberto",                     // Fase 2: "cancelado"
  "situacao": "vago",
  "teste": false,

  // Proprietário
  "donoUid": "user-123",
  "donoNome": "Ana",

  // Metadados
  "origem": "jogador",                    // ou "time"
  "origem_link": "grupo-volei",           // De qual grupo (G1)
  "visibilidade": "privado",              // Fase 2 apenas: "publico"

  // Fase 2: Estados
  "canceladoEm": null,
  "atualizadoEm": null,

  // Fase 2: Arena Integration
  "arenaId": "arena-123",                 // Ref arenas/
  "realizado": true,                      // Time apenas
  "valorConfirmado": true,                // Time apenas
  "horarioVazio": true,                   // Time apenas

  // Fase 2: Tracking
  "copiadoDe": "game-999"                 // "Marcar de novo"
}
```

**Índices necessários (Fase 2):**
- `(visibilidade ASC, estado ASC, quandoTs DESC)` — Para listar públicos
- `(donoUid ASC, quandoTs DESC)` — Para "Meus jogos"

**Regras de leitura:**
- Pública: visibilidade="publico" apenas
- Privada: Por link (jogoId) ou dono

---

### confirmacoes/{cid} [Fase 1 apenas]

**Movido para `jogos/{id}/confirmacoes/{cid}` em Fase 2**

```json
{
  "jogoId": "game-123",
  "nome": "Beto",                         // 2-40 chars
  "via": "link",                          // ou "whatsapp"
  "uid": "user-456",                      // Opcional se sem conta
  "criadoEm": 1700600000000,              // Server time (Fase 2)
  
  // Fase 2 apenas
  "estado": "confirmado",                 // "desistiu", "removido"
  "saiuEm": null,
  "presente": false,                      // Marked by dono após jogo
  "presencaEm": null,
  "origem": "grupo-volei"                 // Link origin
}
```

**Acesso:**
- Leitura: Pública por jogoId (nome de confirmados)
- Escrita: Visitante ou dono

---

### perfis/{uid}
Dados do jogador logado.

```json
{
  "nome": "Beto",
  "cidade": "São Paulo",
  "esportes": ["Vôlei de praia", "Futsal"],
  "nivel": 3,
  "horarios": {
    "inicio": 18,
    "fim": 23
  },
  "whatsapp": "5511987654321",            // Opcional
  "origem": "grupo-volei"                 // Fase 2 apenas
}
```

**Acesso:**
- Leitura: Dono apenas
- Escrita: Dono apenas

---

### admins/{uid}
Membro do time.

```json
{
  "nome": "Carlos",
  "codigo": "ABC123",                     // 6 chars = config/equipe.codigo
  "criadoEm": 1700600000000
}
```

**Regra:** Criar exigindo código correto.  
**Remoção:** Time remove via `delete` (B6)

---

### arenas_piloto/{id}
Ofertas de piloto.

```json
{
  "nomeArena": "Reis D'arena",
  "cidade": "São Paulo",
  "whatsapp": "5511987654321",
  
  // Dados comerciais (time apenas)
  "valorAceitavel": 100,                  // Arena propõe (optional)
  "oferta_resposta": "sim",               // "nao", null
  "oferta_respondidoEm": 1700600000000,
  "oferta_valor": 100,
  
  "criadoEm": 1700600000000,
  "origem": "formulario"
}
```

---

### interesse_premium/{uid}
O que o jogador pagaria por.

```json
{
  "respostas": [
    "Lembrete e aviso de vaga no WhatsApp",
    "Jogo garantido: quem fura paga"
  ]
}
```

---

## Fase 2: Novas Coleções & Subcoleções

### jogos/{id}/confirmacoes/{cid}

**Substitui `confirmacoes/` raiz**

Mesma estrutura que Fase 1 `confirmacoes`, mas:
- `cid` é `uid` se logado, 20 chars random se não
- Leitura restrita: Apenas confirmados, dono, time

```json
{
  "nome": "Beto",
  "via": "link",
  "uid": "user-456",                      // Ou null
  "criadoEm": 1700600000000,
  "estado": "confirmado",
  "saiuEm": null,
  "presente": true,
  "presencaEm": 1700604600000
}
```

**Índices:**
- Group collection query por uid (para "Meus jogos")

---

### jogos/{id}/contatos/{cid}

**Novo em Fase 2 — Separa WhatsApp de confirmações**

```json
{
  "whatsapp": "5511987654321",
  "consentiu": true,                      // Consentimento explícito
  "criadoEm": 1700600000000
}
```

**Regra:** Leitura restrita a dono e time  
**Propósito:** Avisar vaga (I5) sem expor WhatsApp na confirmação pública

---

### arenas/{aid}

**Novo em Fase 2 — Arenas parceiras**

```json
{
  "nome": "Reis D'arena",
  "cidade": "São Paulo",
  "cidadeChave": "sao-paulo",
  "ativa": true
}
```

**Acesso:**
- Leitura: Pública (dropdown em marcar jogo)
- Escrita: Time apenas

---

### arenas/{aid}/privado/piloto

**Novo em Fase 2 — Dados comerciais (time only)**

```json
{
  "inicio_data": 1700600000000,
  "preco_hora": 100,
  "preco_pos_piloto": 100,
  "aceite": "sim",                        // "nao", null
  "aceite_data": 1700600000000,
  
  "horarios_vazios": [
    { "dia": 6, "inicio": 10, "fim": 12 },
    { "dia": 6, "inicio": 14, "fim": 17 }
  ],
  
  "pedidoId": "request-123"                // Ref arenas_piloto/
}
```

**Acesso:**
- Leitura: Time apenas
- Escrita: Time apenas

---

## 📊 Comparação Fase 1 ↔ Fase 2

| Aspecto | Fase 1 | Fase 2 |
|---------|--------|--------|
| **Confirmações** | Root collection | Subcoleção `jogos/{id}/confirmacoes` |
| **Privacidade** | Mínima (nomes públicos) | Maior (subcoleção restrita) |
| **Contato** | Em `confirmacoes` (público) | Em `jogos/{id}/contatos` (restrito) |
| **Arenas** | Texto digitado | Ref `arenas/{aid}` |
| **Dados arena** | Em `arenas_piloto` | Em `arenas/{aid}/privado/piloto` |
| **Performance** | Lê colection inteira | Lê filtrado + subcoleções |
| **Indices** | Mínimos | Compostos (visibilidade, donoUid) |
| **Consultas** | Listeners globais | Listeners filtrados |

---

## 🔄 Fluxo de Migração (Fase 2)

1. **Pré-migração:** Publicar regras ampliadas (aceitam estrutura nova e antiga)
2. **Migração:** Copiar `confirmacoes/` → `jogos/{id}/confirmacoes/` com estado novo
3. **Pós-migração:** Bloquear criação em `confirmacoes/` raiz
4. **Limpeza:** Depois de 7 dias, apagar `confirmacoes/` raiz

---

## 🔐 Segurança por Coleção

| Coleção | Leitura | Escrita | Notas |
|---------|---------|---------|-------|
| `config/` | App | Time (console) | Pública URL, privado preço |
| `jogos/` | Pública (público) / Link (privado) | Dono / Time | B1-B7 rules |
| `confirmacoes/` (Fase 1) | Pública (nome) | Visitante / Dono | Move para subcol Fase 2 |
| `perfis/` | Dono / Time (WhatsApp) | Dono | H6 — time só lê WhatsApp |
| `admins/` | Dono / Time | Time (criar exigindo código) | B6 — remove membros |
| `arenas_piloto/` | Time | Arena / Time | Oferta comercial |
| `interesse_premium/` | Dono / Time | Dono | J8 — Pergunta Premium |
| `arenas/` | Pública (nome) | Time | Dropdown de arenas |

---

## 📏 Escala

**Fase 1 (piloto):** 10-100 games, 50-500 confirmations  
**Fase 2 (arena network):** 100-1K games, 1K-5K confirmations  
**Fase 3 (público):** 1K+ games — índices e subcoleções obrigatórias

**Free tier Firestore:**
- 50K reads/day → ~1.4K reads/hour → Fase 1 OK
- Fase 2 com subcoleções → Reduz a ~20% de leituras globais
- Fase 3 → Cloud Functions + upgrade pago

---

## 🔗 Referências

- **Regras:** [`docs/architecture/03-firestore-rules.md`](03-firestore-rules.md)
- **PRD autoridade:** [`docs/product/01-prd-phase1-2.md`](../product/01-prd-phase1-2.md)
- **Implementação:** [`docs/technical/01-technical-specs.md`](01-technical-specs.md)
- **Migração:** [`docs/product/01-prd-phase1-2.md#8-modelo-de-dados-e-migração`](../product/01-prd-phase1-2.md#8-modelo-de-dados-e-migração)

---

**Última atualização:** 2026-11-16  
**Próxima revisão:** 2026-12-01  
**Owner:** Engineering  

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
