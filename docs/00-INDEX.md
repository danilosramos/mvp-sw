# Energia Boa — Documentação

**Bem-vindo!** Escolha seu papel abaixo para encontrar o que precisa.

---

## 👥 Por Papel

### 👔 Product Manager / Negócio
1. [Estratégia & Modelo de Negócio](strategy/01-business-model.md)
2. [PRD: 71 Requisitos](product/01-prd-phase1-2.md) ← **Autoridade**
3. [Decisões do Projeto](product/02-decisions-log.md)
4. [Blockers & Tracking](decisions/03-blockers-critical-path.md)
5. [Arena Kickoff](operations/arena-pilot-playbook.md)

### 🔧 Engenheiro / Arquiteto
1. [Arquitetura & Design](architecture/01-architecture-overview.md)
2. [Modelo de Dados](architecture/02-data-model.md)
3. [Especificações Técnicas](technical/01-technical-specs.md)
4. [Firestore Rules & Segurança](architecture/03-firestore-rules.md)
5. [Plano de Testes](technical/04-testing-strategy.md)

### 🎨 Designer / UX
1. [Design System](design/01-design-system.md) ← Cores, tipografia, tokens
2. [Modelo de Dados (referência)](architecture/02-data-model.md)
3. [PRD: Requisitos de UI](product/01-prd-phase1-2.md#5-requisitos-da-fase-1) → Seção E (Telas)

### 🏟️ Arena Partner
1. [Arena Kickoff Playbook](operations/arena-pilot-playbook.md) ← **Comece aqui**
2. [PRD: Fase 2 (você)](product/01-prd-phase1-2.md#6-requisitos-da-fase-2) → Seção J (Prova para arena)
3. [O que é "jogo fechado"?](product/04-glossary.md)

### 👁️ Auditor / Revisor
1. [Achados da Auditoria](decisions/01-audit-findings-2026-11-16.md) ← Consolidado
2. [Vulnerabilidades de Segurança](decisions/02-security-issues-remediation.md)
3. [Blockers Críticos](decisions/03-blockers-critical-path.md)
4. [Deep-dive: S1, S5, Migration](decisions/04-deep-dive-s1-s5.md)

---

## 🚨 Por Urgência

### 🔴 CRÍTICO — Bloqueia Phase 1
- [3 Vulnerabilidades de Segurança](decisions/02-security-issues-remediation.md)
- [8 Tarefas Bloqueadoras](decisions/03-blockers-critical-path.md)
- **Status:** 4.5/10 shippable (precisa de 8 fixes)

### 🟠 ALTO — Fix Antes de Launch
- [Testes: 6 Gaps](technical/04-testing-strategy.md)
- [Prova de Receita (M1)](operations/arena-pilot-playbook.md)

### 🟡 PRÓXIMO — Próxima Sprint
- [71 Requisitos](product/01-prd-phase1-2.md)
- [Decisões Abertas](product/02-decisions-log.md)

---

## 📂 Por Categoria

### 📊 Estratégia & Negócio
- [Business Model Canvas](strategy/01-business-model.md)
- [Pesquisa de Mercado](strategy/01-business-model.md#mercado)
- [Go-to-Market Strategy](operations/arena-pilot-playbook.md)

### 📋 Requisitos & Produto
- [PRD — 71 Requisitos (Fase 1 + 2)](product/01-prd-phase1-2.md) ← **Autoridade**
- [Decisões do Projeto](product/02-decisions-log.md)
- [Checklist de Requisitos](product/03-requirements-checklist.md)
- [Glossário de Termos](product/04-glossary.md)

### 🎨 Design & Marca
- [Design System](design/01-design-system.md) — Cores, tipografia, componentes
- [Brand Guidelines](design/01-design-system.md#marca)
- [Rebranding 2026](design/02-brand-guidelines.md)

### 🏗️ Arquitetura & Dados
- [Arquitetura Geral](architecture/01-architecture-overview.md)
- [Modelo de Dados Firestore](architecture/02-data-model.md) ← Referência completa
- [Firestore Rules & Segurança](architecture/03-firestore-rules.md)
- [Fluxos de Autenticação](architecture/04-auth-flow.md)

### ⚙️ Implementação Técnica
- [Especificações Técnicas](technical/01-technical-specs.md)
- [Fases de Implementação (12 Deliverables)](technical/02-implementation-phases.md)
- [Padrões de Código](technical/03-code-patterns.md)
- [Plano de Testes Completo](technical/04-testing-strategy.md)

### 🎯 Decisões & Issues
- [Auditoria Completa 2026-11-16](decisions/01-audit-findings-2026-11-16.md)
- [Vulnerabilidades de Segurança](decisions/02-security-issues-remediation.md)
- [Blockers Críticos (8 itens)](decisions/03-blockers-critical-path.md)
- [Deep-dive: S1 (Rules), S5 (Tests), Migration](decisions/04-deep-dive-s1-s5.md)

### 🏢 Operações
- [Arena Pilot Playbook](operations/arena-pilot-playbook.md) ← M1 (revenue validation)
- [Deployment Checklist](operations/deployment-checklist.md)
- [Support Handbook](operations/support-handbook.md)

---

## 🔗 Links Rápidos

| Necessidade | Leitura |
|---|---|
| "Qual é a autoridade de requisitos?" | [PRD.md](product/01-prd-phase1-2.md) (71 reqs) + [Glossário](product/04-glossary.md) |
| "Qual é a schema do Firestore?" | [Data Model](architecture/02-data-model.md) |
| "Como são as Firestore Rules?" | [Rules & Security](architecture/03-firestore-rules.md) |
| "Qual é o design system?" | [Design System](design/01-design-system.md) |
| "Quais são os 8 blockers?" | [Blockers](decisions/03-blockers-critical-path.md) |
| "Qual é o plano de testes?" | [Testing Roadmap](technical/04-testing-strategy.md) |
| "Como convencer a arena?" | [Arena Kickoff](operations/arena-pilot-playbook.md) |
| "O que é 'jogo fechado'?" | [Glossário](product/04-glossary.md) + [PRD J4](product/01-prd-phase1-2.md#j-prova-para-a-arena) |
| "Por que 4.5/10 shippability?" | [Blockers](decisions/03-blockers-critical-path.md) |

---

## 📖 Leitura Recomendada (Ordem)

**Novo membro no projeto (30 minutos):**
1. Este arquivo (5 min)
2. [PRD — Resumo seção 1-2](product/01-prd-phase1-2.md#1-resumo) (10 min)
3. [Arquitetura — Casos de uso](architecture/01-architecture-overview.md#casos-de-uso) (5 min)
4. [Design System — Paleta de cores](design/01-design-system.md) (5 min)
5. [Blockers — O que falta](decisions/03-blockers-critical-path.md) (5 min)

**Implementação de feature (2 horas):**
1. [PRD — Requisito específico](product/01-prd-phase1-2.md)
2. [Data Model — Schema afetado](architecture/02-data-model.md)
3. [Specs — Implementação técnica](technical/01-technical-specs.md)
4. [Testing Roadmap — Testes necessários](technical/04-testing-strategy.md)

**Review de segurança (1 hora):**
1. [Achados da auditoria](decisions/01-audit-findings-2026-11-16.md)
2. [Vulnerabilidades críticas](decisions/02-security-issues-remediation.md)
3. [Firestore Rules](architecture/03-firestore-rules.md)
4. [Deep-dive S1 & S5](decisions/04-deep-dive-s1-s5.md)

---

## 📚 Documentos Arquivados (Obsoletos)

Esses documentos foram substituídos. Consultar apenas para referência histórica:
- `docs/archive/AUDITORIA.md` ← Substituído por `decisions/01-audit-findings-2026-11-16.md`
- `docs/archive/REQUISITOS.md` ← Substituído por `product/01-prd-phase1-2.md`

---

## 🔄 Versionamento de Docs

Cada documento tem:
- **Data de criação** (quando foi criado)
- **Última atualização** (quando foi revisado)
- **Status**: current | draft | archive
- **Owner**: Quem mantém
- **Review programado**: Quando revisar novamente

Exemplo metadata (topo de cada doc):
```
---
title: "PRD: Product Requirements"
owner: "Product"
version: "2026-11-16.1"
status: "current"
last_updated: "2026-11-16"
next_review: "2026-12-01"
---
```

---

## 📞 Dúvidas Frequentes

**P: Qual documento é a "fonte de verdade"?**  
R: **PRD.md** (71 requisitos). Tudo mais referencia PRD.

**P: Qual é o escopo da Fase 1?**  
R: [PRD seção 5](product/01-prd-phase1-2.md#5-requisitos-da-fase-1) + [Blockers](decisions/03-blockers-critical-path.md)

**P: Por que o app não é shippable (4.5/10)?**  
R: [8 Blockers](decisions/03-blockers-critical-path.md) + [3 Vulnerabilidades](decisions/02-security-issues-remediation.md)

**P: Como convencer a arena?**  
R: [Arena Kickoff Playbook](operations/arena-pilot-playbook.md)

**P: Qual é o design system?**  
R: [Design System](design/01-design-system.md) — Use os tokens antes de custom CSS

**P: Como rodar os testes?**  
R: [Testing Roadmap seção 5](technical/04-testing-strategy.md)

---

**Última atualização:** 2026-11-16  
**Próxima revisão:** 2026-12-01

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
