---
title: "Decisions Log"
owner: "Product"
version: "2026.11.16.1"
status: "current"
last_updated: "2026-11-16"
next_review: "2026-12-01"
depends_on: ["01-prd-phase1-2.md"]
---

# Decisões do Projeto — Energia Boa

**Data:** 16/11/2026  
**Fonte:** PRD.md seção 11  
**Status:** Log de decisões — rastreamento de escolhas do projeto

---

## Resumo

O projeto tem **14 decisões principais** que moldam os requisitos. Cada decisão:
- Tem um **recomendação adotada** (usado neste projeto)
- Teve **opções consideradas** (alternativas rejeitadas)
- Afeta **requisitos específicos** (se mudar, esses reqs mudam)
- Pode ser **reaberta** após piloto/aprendizado

---

## Decisões — Rastreamento

| # | Decisão | Recomendação Adotada | Status | Fase | Afeta Reqs | Revisão |
|---|---------|----------------------|--------|------|-----------|---------|
| 1 | Preço pós-piloto | (a) Valor fixo/jogo | ✅ Decided | 1-2 | E7, J5, M1 | Pós-piloto |
| 2 | Servidor | (a) Sem servidor | ✅ Decided | 1-2 | Arquitetura | Fase 3? |
| 3 | Quem confirma | (b) Dono marca + time confirma | ✅ Decided | 2 | J4, N1 | Pós-piloto |
| 4 | Contato espera | (a) Visível a quem espera | ✅ Accepted risk | 1-2 | H6, N11 | Known limitation |
| 5 | Tela Premium | (a) Fora nav, como pergunta | ✅ Decided | 1 | E10, J8 | Pós-piloto |
| 6 | Endereço oficial | (c) Domínio próprio | ⏳ **OPEN** | 1 | C1, C4, E9 | **BLOCKER** |
| 7 | Perfil | (a) Opcional | ✅ Decided | 1 | D4, D5 | Confirmed |
| 8 | Conta público | (a) Exigida | ✅ Decided | 1 | D2, D3, J2, I1 | Confirmed |
| 9 | Jogo público painel | (b) Separado, sem valor | ✅ Decided | 2 | J4, J7 | Pós-piloto |
| 10 | Edição com confirmados | (a) Permitida + aviso | ✅ Decided | 1 | I4 | Confirmed |
| 11 | Teto de valor | R$ 1.000 | ✅ Decided | 1 | B3 | Confirmar com time |
| 12 | Login WhatsApp | (a) "Abrir no navegador" | ✅ Provisional | 1 | D2, D3 | Re-avaliar após D3 |
| 13 | Contador fechamento | (a) Calculado de confirmacoes | ✅ Decided | 1 | H5, J1 | Concorrência → Teste |
| 14 | Analytics | Serviço sem cookies | ⏳ **OPEN** | 1 | G2 | Termos/preço a conferir |

---

## Decisões Detalhadas

### Decisão 1: Preço pós-piloto para a arena

**Recomendação:** (a) Valor fixo por jogo fechado em horário vago

**Por que:** 
- Simplicidade operacional (não precisa de cálculos de percentual)
- Transparência (arena sabe exatamente quanto ganha por jogo)
- Alinhado com modelo de negócio testável

**Valor:** R$ XXX (a definir pelo time antes da primeira oferta)

**Impacto se mudar:**
- Com (b) percentual: J4 calcula sobre preço confirmado
- Com (c) mensalidade: J4 vira apenas relatório de apoio

**Status:** ✅ Decided  
**Requisitos afetados:** E7, J5, M1  
**Data decisão:** 2026-11-16  
**Revisar após:** Piloto com 3-5 arenas

---

### Decisão 2: Servidor nas fases 1 e 2

**Recomendação:** (a) Sem servidor — apenas Firestore

**Por que:**
- MVP rápido (sem infraestrutura)
- Custo baixo (Firebase free tier)
- Restrição técnica: "Hospedagem estática"

**Impacto se mudar:**
- Com (b) Cloud Functions: J1 e I5 ficam mais simples, aviso automático sobe para Fase 2

**Status:** ✅ Decided  
**Requisitos afetados:** Arquitetura geral  
**Data decisão:** 2026-11-16  
**Revisar após:** Piloto (se volume exigir)

---

### Decisão 3: Quem confirma que o jogo aconteceu

**Recomendação:** (b) Dono marca presença + time confirma "realizado"

**Por que:**
- Dono tem incentivo honesto (quer bom histórico)
- Time valida (pega valor_confirmado + presença)
- Reduz manipulação

**Impacto se mudar:**
- Com (a) só dono: J4 perde força como base de cobrança
- Com (c) arena: Surge acesso da arena (Fase 3)

**Status:** ✅ Decided  
**Requisitos afetados:** J4, N1  
**Data decisão:** 2026-11-16  
**Revisar após:** Piloto com arena

---

### Decisão 4: Contato de quem organiza para a lista de espera

**Recomendação:** (a) Visível a quem espera

**Por que:**
- Código é pequeno (sem servidor = sem verificação de posição)
- Espera pode combinar horário se abrir vaga

**Risco aceito:** Contato mais exposto (mitiga com H6 segurança)

**Impacto se mudar:**
- Com (b) só a quem tem vaga: Precisaria servidor ou toggle "mostrar depois de aceitar"

**Status:** ✅ Accepted risk  
**Requisitos afetados:** H6, N11  
**Data decisão:** 2026-11-16  
**Revisar após:** Fase 2 (pode ter servidor)

---

### Decisão 5: Tela do Premium

**Recomendação:** (a) Fora da navegação, como pergunta

**Por que:**
- MVP não tem Premium real
- Coleta feedback (J8) sem prometer
- Tira peso visual da navegação

**Impacto se mudar:**
- Com (b) remover: E10 vira remoção, J8 sai
- Com (c) manter: Promete recursos que não tem

**Status:** ✅ Decided  
**Requisitos afetados:** E10, J8  
**Data decisão:** 2026-11-16  
**Revisar após:** Pós-piloto

---

### Decisão 6: Endereço oficial do aplicativo ⏳ BLOCKER

**Recomendação:** (c) Domínio próprio

**Por que:**
- GitHub Pages URL muda com repo
- Todos os links enviados precisam de URL estável

**Impacto:**
- Afeta **todos** os links já enviados
- Deve ser decidido **antes de Fase 1 terminar**
- C1 (configuração chave), C4 (docs), E9 (prévia), D1 (links)

**Status:** ⏳ **ABERTO — BLOQUEADOR**  
**Requisitos afetados:** C1, C4, E9, D1  
**Data decisão:** Não decidido  
**Revisar:** HOJE (bloqueia divulgação)

**Opções:**
- (a) URL do README (muda = ruim)
- (b) URL remoto do repo (ainda GitHub Pages = ruim)
- **(c) Domínio próprio** ← Recomendado

---

### Decisão 7: Perfil

**Recomendação:** (a) Opcional

**Por que:**
- MVP testa se gente joga, não perfil completo
- Reduz atrito
- Pode preencher depois

**Impacto se mudar:**
- Com (b) obrigatório: D4 e D5 se invertem, precisa regra

**Status:** ✅ Decided  
**Requisitos afetados:** D4, D5  
**Data decisão:** 2026-11-16  
**Revisar após:** Métricas (quantos preenchem depois?)

---

### Decisão 8: Conta em jogo público

**Recomendação:** (a) Conta exigida

**Por why:**
- Google Sign-In já pronto
- Rastreamento de jogador (J2 — segundo jogo em 14 dias)
- Segurança (ataque S1 — WhatsApp)

**Impacto se mudar:**
- Com (b) só nome: D2, D3 saem, perde identidade do jogador (I1, J2 quebra)

**Status:** ✅ Decided  
**Requisitos afetados:** D2, D3, J2, I1  
**Data decisão:** 2026-11-16  
**Revisar após:** Métricas (taxa de criação conta?)

---

### Decisão 9: Jogo em quadra pública no painel

**Recomendação:** (b) Conta separadamente, sem valor

**Por why:**
- Quadra pública = sem receita
- Precisa aparecer para o time (saber que tá lotado)

**Impacto:**
- Só altera apresentação em J4, J7

**Status:** ✅ Decided  
**Requisitos afetados:** J4, J7  
**Data decisão:** 2026-11-16  
**Revisar após:** Padrão estabilizar

---

### Decisão 10: Edição do jogo com gente confirmada

**Recomendação:** (a) Permitida até o início, com aviso

**Por why:**
- Dono pode corrigir hora/local/total
- Confirmados recebem aviso (I4)
- Mais flexível

**Impacto se mudar:**
- Com (b) bloqueada: I4 precisa "sem confirmações"

**Status:** ✅ Decided  
**Requisitos afetados:** I4  
**Data decisão:** 2026-11-16  
**Revisar após:** Feedback piloto

---

### Decisão 11: Teto de valor do jogo na regra

**Recomendação:** R$ 1.000

**Por why:**
- Referências de mercado: R$ 60-220/hora
- R$ 1.000 tem margem
- Previne typos / manipulação

**Status:** ✅ Decided (com confirmação do time)  
**Requisitos afetados:** B3  
**Data decisão:** 2026-11-16  
**Confirmar com:** Time (antes da Fase 1 fim)

---

### Decisão 12: Saída para login em navegador embutido

**Recomendação:** (a) "Abrir no navegador" (D2)

**Por why:**
- Firebase Hosting redirect (b) falha quando domínios diferem
- Google bloqueia login em embedded browsers
- Simples (D2)

**Impacto se mudar:**
- Com (c) Firebase anon auth: Muda H4, precisa review segurança

**Status:** ✅ Provisional (reavalia após D3)  
**Requisitos afetados:** D2, D3  
**Data decisão:** 2026-11-16  
**Revisar após:** Teste D3 (WhatsApp Android/iPhone)

**Ação:** Se D3 falhar, reabre decisão 12

---

### Decisão 13: Contador de confirmados e momento de fechamento

**Recomendação:** (a) Calculado a partir das confirmacoes

**Por why:**
- Segurança: aparelho não pode atualizar jogo
- Escala do piloto: leitura N+1 é aceitável
- Mais seguro contra race conditions

**Impacto se mudar:**
- Com (b) gravado no jogo: H5 lê menos docs, mas regra delicada (precisa teste concorrência)

**Status:** ✅ Decided  
**Requisitos afetados:** H5, J1  
**Data decisão:** 2026-11-16  
**Revisar após:** Teste de concorrência (2+ confirmacoes última vaga)

---

### Decisão 14: Ferramenta do contador de páginas ⏳ ABERTA

**Recomendação:** Serviço sem cookies com chamada manual por rota

**Por why:**
- Sem rastreamento invasivo
- LGPD/GDPR compatível

**Falta:** Conferir termos e preço

**Status:** ⏳ **ABERTO — Precisa conferência**  
**Requisitos afetados:** G2  
**Data decisão:** Não decidido  
**Revisar:** Antes de Fase 2

**Opções:**
- Serviço sem cookies (recomendado — precisa validação)
- Firebase Analytics (default Google — mais fácil)
- Gravar em Firestore (simples — sem vendor lock)

---

## 📊 Resumo de Status

| Status | Decisões | Lista |
|--------|----------|-------|
| ✅ Decided | 11 | 1, 2, 3, 5, 7, 8, 9, 10, 11, 13 |
| ✅ Provisional | 1 | 12 (reavalia após D3) |
| ✅ Accepted risk | 1 | 4 (limitação conhecida) |
| ⏳ OPEN — BLOCKER | 1 | **6** (endereço oficial) |
| ⏳ OPEN — Precisa validação | 1 | **14** (analytics) |

---

## 🚨 Bloqueadores

### Decisão 6: Endereço Oficial
- **Por quê bloqueia:** Todos os links enviados precisam de URL estável
- **Que reqs afeta:** C1 (chave segura), C4 (documentação), E9 (preview), D1 (links compartilhados)
- **Ação:** Decidir hoje, registrar domínio

### Decisão 14: Analytics Tool
- **Por quê aberta:** Precisa conferir termos/preço
- **Que reqs afeta:** G2 (medição)
- **Ação:** Validar antes de Fase 2

---

## 🔄 Rastreabilidade com PRD

Cada decisão **cruza** com requisitos específicos:

| Decisão | Se muda, afeta | Requisitos |
|---------|---|---|
| **1 — Preço** | Faturamento | E7 (tela), J5 (oferta), M1 (hipótese) |
| **3 — Quem confirma** | Autorização | J4 (calculado), N1 (métrica) |
| **4 — Contato espera** | Privacidade | H6 (leitura), N11 (risco) |
| **5 — Premium** | Navegação | E10 (tela), J8 (pergunta) |
| **6 — Endereço** | TUDO | C1, C4, E9, D1 (todos os links) |
| **12 — Login WhatsApp** | Aquisição | D2, D3, D1 (fluxo) |

---

## 📅 Calendário de Revisão

| Decisão | Próxima revisão | Trigger |
|---------|---|---|
| 1 | Pós-piloto (3 arenas) | Feedback arena sobre preço |
| 2 | Fase 3 | Se volume exigir servidor |
| 3 | Pós-piloto | Dados de presença real |
| 4 | Fase 2 | Se server adicionado |
| 5 | Pós-piloto | Resposta pergunta Premium |
| **6** | **HOJE** | **Bloqueador** |
| 7 | Métricas | % que preenchem perfil |
| 8 | Métricas | Taxa conversão conta |
| 9 | Padrão | Dados acumulando |
| 10 | Feedback | Reclamações sobre edição |
| 11 | Pré-Fase 1 | Confirmar com time |
| 12 | Teste D3 | Resultado WhatsApp |
| **14** | **Pré-Fase 2** | **Validar termos/preço** |

---

## 🔗 Links

- **Fonte:** [PRD seção 11](01-prd-phase1-2.md#11-decisões-em-aberto)
- **Rastreabilidade:** [PRD seção 12](01-prd-phase1-2.md#12-rastreabilidade)
- **Requisitos:** [PRD seção 5-6](01-prd-phase1-2.md#5-requisitos-da-fase-1)
- **Blockers:** [docs/decisions/03-blockers-critical-path.md](../decisions/03-blockers-critical-path.md)

---

**Última atualização:** 2026-11-16  
**Próxima revisão:** 2026-12-01  
**Owner:** Product  

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
