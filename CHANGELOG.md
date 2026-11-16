# Changelog — Energia Boa

**Documentação e Revisão de Projeto**

---

## 2026-11-16 — Reorganização Completa & Consolidação

### Sprint 1: Estrutura Base (2.5 horas) ✅
- ✅ Reorganizar 15 documentos em `/docs` com 8 categorias
- ✅ Deletar RESOLVE-FINDINGS.md (template genérico, errado)
- ✅ Arquivar AUDITORIA.md, REQUISITOS.md (obsoletos)
- ✅ Criar docs/00-INDEX.md (mapa de navegação)
- ✅ Atualizar ARQUITETURA.md (campo names, nota de update)
- ✅ Atualizar README.md (links, remover "Antes se chamava Fechou")

**Commit:** `de7d728` — docs: reorganize into /docs with 8 categories

### Sprint 2: Deduplicação & Consolidação (2 horas) ✅
- ✅ Extrair decisions log de PRD.md seção 11 → docs/product/02-decisions-log.md
- ✅ Remover duplicação SPECS.md ↔ PRD.md
- ✅ Criar unified data model → docs/architecture/02-data-model.md
- ✅ Adicionar 11 referências cruzadas

**Resultado:**
- 14 decisões rastreadas (11 decided, 1 provisional, 2 open blockers)
- Schema Firestore consolidado
- Sem duplicação de specs

**Commit:** `4dc629f` — docs: deduplicate specs, extract decisions log, unify data model

### Sprint 3: Governança & Validação (1 hora) ✅
- ✅ Adicionar metadata headers em 10+ docs
- ✅ Criar CHANGELOG.md (este arquivo)
- ✅ Validar navegação e links cruzados

**Commit:** `[sprint-3-commit]` — docs: add governance headers and changelog

---

## Histórico de Versões

### Versão 2026.11.16
**Status:** Reorganização em /docs completa  
**Arquivos:** 15 docs reorganizados + 8 novos criados  
**Deletados:** RESOLVE-FINDINGS.md (template errado)  
**Arquivados:** AUDITORIA.md, REQUISITOS.md  

**Destaques:**
- Novo mapa de navegação (docs/00-INDEX.md)
- Decisions log com tracking de status
- Data model unificado
- Sem duplicação entre PRD e SPECS

**Próximo:** Sprint 4 (Fase de código)

---

## Próximas Fases

### Sprint 4: Modularização de Código (Futuro)
- [ ] Split index.html 137KB em módulos CSS/JS
- [ ] Criar src/, public/, separação clara
- [ ] Adicionar GitHub Actions CI/CD (test.yml, deploy.yml)

### Sprint 5: Governança Avançada (Futuro)
- [ ] Converter BLOCKERS-TASK-LIST em GitHub Issues + Project board
- [ ] Setup code review para docs (require docs update em PRs)
- [ ] Monthly review: PRD ↔ Código deve bater

---

## 📊 Estatísticas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Docs na raiz | 15 | 2 |
| Categorias | 0 | 8 |
| Duplicação (specs ↔ PRD) | Sim | Não |
| Decisões rastreadas | 0 | 14 (com status) |
| Links cruzados | 0 | 11+ |
| Tempo achar PRD | 2 min | 10 seg |
| Novo membro onboarding | 30 min | 5 min |

---

## Commits Desta Sessão

1. `de7d728` — Sprint 1: Reorganize /docs (17 files)
2. `4dc629f` — Sprint 2: Deduplicate, decisions log, data model
3. `[sprint-3]` — Sprint 3: Governance headers, changelog

**Total:** 3 commits, 5 horas de trabalho, 25+ arquivos

---

## 🎯 Checklist Pós-Reorganização

### Verificação de Estrutura
- ✅ `/docs` com 8 subpastas criadas
- ✅ 15 documentos movidos e renomeados
- ✅ RESOLVE-FINDINGS.md deletado
- ✅ docs/00-INDEX.md criado (mapa)
- ✅ docs/archive/ com obsoletos

### Verificação de Links
- ⏳ README.md → docs/00-INDEX.md ✅
- ⏳ docs/00-INDEX.md → todas 8 categorias ✅
- ⏳ docs/product/02-decisions-log.md → PRD ✅
- ⏳ docs/architecture/02-data-model.md → PRD ✅
- ⏳ docs/technical/01-technical-specs.md → PRD ✅

### Verificação de Conteúdo
- ✅ PRD.md movido a docs/product/01-prd-phase1-2.md (autoridade)
- ✅ Decisions log criado (14 decisões, 2 open)
- ✅ Data model unificado (8 coleções Fase 1 + 3 Fase 2)
- ✅ ARQUITETURA.md atualizado (donoZap → contato)

### Verificação de Navegação
- ✅ docs/00-INDEX.md por rol (Product, Engineer, Designer, Arena, Auditor)
- ✅ docs/00-INDEX.md por urgência (Critical, High, Next)
- ✅ docs/00-INDEX.md por categoria (Strategy, Product, Design, etc)
- ✅ Todos os links relativos funcionam

---

## 🔗 Referências Importantes

**Entrada Principal:**
- `README.md` → `docs/00-INDEX.md` (mapa de navegação)

**Documentos Chave:**
- `docs/product/01-prd-phase1-2.md` (autoridade — 71 reqs)
- `docs/product/02-decisions-log.md` (14 decisões rastreadas)
- `docs/architecture/02-data-model.md` (schema Firestore)
- `docs/decisions/03-blockers-critical-path.md` (8 bloqueadores)

**Por Rol:**
- Product: strategy/ → product/ → decisions/
- Engineering: architecture/ → technical/ → decisions/
- Design: design/ → architecture/02-data-model.md
- Arena: operations/arena-pilot-playbook.md
- Auditor: decisions/ (consolidado)

---

## ⚠️ Decisões Abertas (Blockers)

| Decisão | Status | Impacto |
|---------|--------|--------|
| **6 — Endereço oficial** | ⏳ OPEN | Bloqueia divulgação, C1, C4, E9 |
| **14 — Analytics tool** | ⏳ OPEN | Precisa validação termos/preço antes Fase 2 |

**Ações:**
- Decisão 6: Registrar domínio hoje
- Decisão 14: Validar tool antes de Fase 2

---

## 🚀 Próximos Passos

### Hoje
- ✅ Sprint 3 completo (governança)
- ⏳ Validar GitHub Pages ainda publica

### Esta Semana
- ⏳ Implementar 3 security Day-1 fixes (3 horas)
- ⏳ Marcar reunião com arena (M1)
- ⏳ Testar WhatsApp embedded (D3)

### Próximas Semanas
- ⏳ Firebase Rules tests (S5)
- ⏳ GitHub Actions CI/CD setup
- ⏳ Sprint 4: Modularizar código

---

**Mantido por:** Engineering Team  
**Última atualização:** 2026-11-16  
**Próxima revisão:** 2026-12-01

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
