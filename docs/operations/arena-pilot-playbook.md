# ARENA-KICKOFF.md

**Data:** 16/11/2026  
**Criticidade:** M1 – Piloto não testa a receita (bloqueador de Fase 2)  
**Proprietário:** Time de operações  
**Referência:** PRD.md (seção 2, decisão 1 e 11); AUDITORIA.md (seção 7, achado M1)

---

## Resumo executivo

O piloto com arenas é o único teste real da hipótese "arena paga por jogo fechado em horário ocioso". Sem definição de preço pós-30 dias e sem aceite por escrito **antes do início**, o modelo fica validado apenas por intenção, não por compromisso.

Este documento padroniza a conversa, registra o acordo em escrito e cria checkpoints para decidir se continuamos para Fase 2.

**Decisão crítica:** Manter os 30 dias grátis e declarar **hoje** o preço que a arena pagará depois. Sem isso, o piloto não mede receita.

---

## 1. Arena Conversation Checklist

### Objetivo
Transformar uma oferta verbal em acordo documentado que prova a aceitação de pagar por um evento verificável.

### Antes da chamada (time)

- [ ] Definir o preço pós-piloto em reais (padrão: **R$ [A DEFINIR]** por jogo fechado em horário vago)
- [ ] Listar as 3-5 arenas prioritárias (cidade, contato, histórico de resposta)
- [ ] Preparar exemplos de horários vazios (segunda 10h, quarta 14h, sexta 20h)
- [ ] Ter pronto o link de demanda: `Energia Boa para arenas`
- [ ] Nomear responsável da conversa (ops, founder, BD)

### Na chamada com a arena

#### 1. Abertura (2 min)
- Apresentar a Energia Boa em 30 segundos: "levamos jogadores para seus horários vazios"
- **NÃO começar com preço.** Começar com dor: "Sua quadra está vaga às 14h de quarta?"

#### 2. Problema (3 min)
- Ouvir: "Qual horário mais sofre com ociosidade?"
- Ouvir: "Quantas pessoas vocês perdem por falta de gente?"
- **Documentar na conversa.** Essa informação entra no contrato.

#### 3. Solução (3 min)
- "A gente leva gente confirmada. Você marca as horas vazias, a gente enche, vocês cobram normalmente da galera."
- "Não mexemos no seu sistema. Vocês conferem se o jogo aconteceu, a gente paga."
- Mostrar a tela do convite (simples, privado, sem instalar app)

#### 4. Piloto (3 min)
- "Começamos com 30 dias grátis para vocês testarem, sem risco."
- **AQUI ENTRA O PREÇO:** "Depois do piloto, a gente paga **R$ [X]** por jogo fechado que cair em horário que vocês marcaram como vazio."

#### 5. Definir "jogo fechado" (5 min) ⭐ **CRÍTICO**

A arena precisa entender exatamente o que a gente conta. Usar esta frase:

> "Contamos um jogo como **'fechado e realizado em horário vago'** quando:
> 1. **Realizado:** vocês confirmam que o jogo aconteceu (checkinha em um link ou formulário)
> 2. **Horário vago:** o horário do jogo estava no calendário de vazios que vocês marcaram
> 3. **Valor confirmado:** o valor por pessoa foi confirmado pela gente antecipadamente (pra evitar surpresa)
> 
> Exemplo: sexta 20h é horário vago, 8 pessoas confirmadas pelo link, jogo acontece → **conta 1 jogo.**
> 
> Se uma pessoa não comparece, mesmo assim **conta.** Se o valor muda (arena cobra mais), a gente renegocia antes.

- Entregar a tabela `O que conta` em PDF/WhatsApp

#### 6. Aceitação (2 min)
- "Faz sentido pra vocês?"
- Se sim: "Então a gente manda por escrito e vocês assinam."
- Se não: Ir para Fallback Plan (seção 5)

#### 7. Horários vazios (5 min)
- Usar a tela "Declare seus horários vazios" (campo no formulário de arena)
- Pedir: **dias da semana, faixa horária, número de quadras**
- Exemplo: "segundas e quartas 10h-12h, sextas 19h-22h" (2 quadras)
- **Isso entra no contrato.** A gente só paga se o jogo cair nesses horários.

#### 8. Próximos passos (1 min)
- "Vocês recebem um documento (anexado) com tudo que conversamos"
- "Assinam e devolvem até [data]"
- "Na semana seguinte, a gente ativa o link de demanda aqui na região"

**Total da chamada:** 25 min | **Documentação:** Contrato assinado em até 48h

### Depois da chamada (time)

- [ ] Enviar contrato por escrito (template na seção 2) **no mesmo dia**
- [ ] Se não responder em 3 dias: ligar de novo
- [ ] Se recusar: aplicar Fallback Plan
- [ ] Se aceitar: adicionar ao painel, marcar início do piloto, configurar preço no app (E7)

---

## 2. Pilot Agreement Template

Use este modelo em um documento assinável (Google Docs, PDF com assinatura eletrônica, ou WhatsApp confirmado por texto).

```
ACORDO DE PILOTO – ENERGIA BOA

Data: ___/___/_______
Arena: _________________________________________________________
Cidade: _________________________________________________________
Contato: _________________________ Telefone: __________________

---

1. OBJETIVO
A Energia Boa compromete-se a levar jogadores confirmados para os horários 
que a Arena declarar como vazios, durante 30 dias de teste gratuito.

---

2. PERÍODO DO PILOTO
Início: ___/___/_______ (segunda-feira recomendada)
Fim: ___/___/_______ (30 dias depois)
Prorrogação: Decidida conjuntamente na semana 4

---

3. O QUE CONTA COMO "JOGO FECHADO"
Um jogo é contabilizado para cobrança quando **todos** os itens abaixo são verdadeiros:

a) REALIZADO
   ✓ Arena confirma que o jogo aconteceu (formulário/link que a gente manda)
   
b) HORÁRIO VAGO
   ✓ O horário do jogo foi marcado pela Arena como vazio (nesta lista)
   
c) VALOR CONFIRMADO
   ✓ Número de pessoas e preço por pessoa eram os esperados
   ✓ Arena e Energia Boa concordam antes do jogo

d) ARENA PARCEIRA
   ✓ O jogo foi criado pela Energia Boa apontando esta Arena

e) FORA DE TESTES
   ✓ Jogo não foi marcado como "teste" no sistema

---

4. HORÁRIOS VAZIOS DECLARADOS PELA ARENA

[Arena marca com um X os horários e dias]

| Dia | Horário Início | Horário Fim | Quadras |
|-----|---|---|---|
| Segunda | ___ h | ___ h | __ |
| Terça | ___ h | ___ h | __ |
| Quarta | ___ h | ___ h | __ |
| Quinta | ___ h | ___ h | __ |
| Sexta | ___ h | ___ h | __ |
| Sábado | ___ h | ___ h | __ |
| Domingo | ___ h | ___ h | __ |

Arena pode atualizar esta lista enviando mensagem ao time até 48h antes do jogo.

---

5. PREÇO PÓS-PILOTO

Após os 30 dias grátis, a Energia Boa pagará:

**R$ _____________ por jogo fechado**

(Baseado em: horário ocioso, evento realizado, confirmação de presença)

Este valor pode ser renegociado a cada 60 dias se a volume ou custos da Arena mudarem.

---

6. CONFIRMAÇÃO DE PRESENÇA

Para cada jogo que fecha, a Arena recebe um link simples onde marca:
- Que o jogo aconteceu (sim/não)
- Quantas pessoas compareceram (número)
- Qualquer observação

A Energia Boa usa isso para validar o evento antes de processar pagamento.

---

7. FATURAMENTO

- Contagem: Segunda-feira (semana 1 até 4, depois semanal)
- Formato: Relatório CSV com lista de jogos
- Pagamento: [A DEFINIR - sugestão: PIX em até 5 dias úteis]
- Período mínimo: Sem mínimo (paga por jogo)

---

8. DURANTE O PILOTO

A Energia Boa:
✓ Envia jogadores confirmados pelo link privado
✓ Respeita os horários e quantidade de quadras declaradas
✓ Não mexe no sistema da Arena
✓ Fornece relatório semanal de jogos criados

A Arena:
✓ Confirma presença dos jogadores
✓ Avisa mudanças de horários com 48h de antecedência
✓ Devolve feedback semanal (qual horário encheu, qual não)

---

9. RESCISÃO

Qualquer lado pode sair do piloto com 7 dias de aviso.

Se a Arena sair antes do fim:
- Jogos já realizados na semana são faturados normalmente
- Próximas semanas canceladas (sem débito, sem crédito)

Se a Energia Boa sair:
- Reembolsa proporcional do período não realizado
- Transfere toda documentação de jogos para a Arena

---

10. DECISÃO PÓS-PILOTO (fim do mês 1)

Na semana 4 (1 mês depois), a Energia Boa e Arena decidem:

□ Sim → Contrato mensal com os mesmos termos
□ Sim, mas com ajustes → Renegociar preço ou horários
□ Não → Encerrar relacionamento; não há débitos

---

11. DADOS PESSOAIS

A Energia Boa coleta nome e WhatsApp dos jogadores APENAS para confirmar presença.
Arena não recebe dados dos jogadores sem consentimento deles.

---

Assinado em: ___/___/_______

Arena: _________________________ Data: ___/___/_______
  
Energia Boa: _________________________ Data: ___/___/_______

---

ANEXO: O que conta / O que não conta

CONTA:
✓ 8 pessoas, 2 não aparecem, 6 comparecem → paga normalmente (6 jogam)
✓ Valor muda (arena cobra mais) → renegocia antes do próximo jogo
✓ Uma pessoa confirma mas o jogo não sai do chão → arena marca "não realizado", não paga

NÃO CONTA:
✗ Jogo cancelado pela Arena (não realizado)
✗ Jogo em horário que não estava marcado como vago
✗ Jogo criado fora do link da Energia Boa (manual no papel/WhatsApp)
✗ Jogo marcado como "teste" no sistema
✗ Jogo em quadra pública (sem renda para a Arena)
```

---

## 3. Communication Timeline

### Semana 1: Pitch com preço

**Responsável:** BD ou Founder  
**Meios:** Ligação + WhatsApp  
**Duração:** 25 min de conversa + 24h para resposta

| Dia | Ação | Quem | Resultado esperado |
|---|---|---|---|
| Seg | Ligar 3-5 arenas prioritárias | BD | 100% das ligações feitas |
| Seg-Ter | Executar checklist (seção 1) | BD | Áudio com consenso ou objeção registrada |
| Ter | Enviar contrato no mesmo dia | Ops | Contrato recebido pela Arena |
| Qua-Qui | Seguimento: "Recebeu? Dúvidas?" | BD | Arena marcando próxima chamada OU recusa |

**Vitória:** 1-2 arenas a enviar contrato assinado até sexta

### Semana 2: Assinatura e ativação

**Responsável:** Ops  
**Meios:** E-mail + WhatsApp  
**Dependências:** Código postal de preço definido; página de arenas com preço visível (E7)

| Dia | Ação | Quem | Resultado esperado |
|---|---|---|---|
| Seg | Cobrar assinatura: "Faltam 3 dias!" | Ops | 70% das arenas assinando |
| Ter | Registrar arenas no painel (time) | Dev | Arena aparece em dropdown ao marcar jogo |
| Ter | Testar link de demanda (Android + iPhone) | QA | Convite privado funciona sem erros |
| Qua | Treinar time com primeiras arenas | Ops | Time sabe quais são arenas piloto + horários vazios |
| Qui | Soft launch: chamar 20 jogadores pelo WhatsApp | BD | Primeira onda de convites saindo |
| Sex | Ligar arenas: "Começamos segunda!" | Ops | Arena preparada; relatório pronto |

**Vitória:** Primeira semana com pelo menos 1 jogo confirmado

### Semana 3-4: Soft launch e métricas

**Responsável:** Ops + Dev  
**Meios:** Painel em tempo real + relatório semanal  
**Cadência:** Reunião com arena toda semana (mesma hora, mesmo dia)

| Período | Ação | Quem | Check |
|---|---|---|---|
| Diariamente | Monitorar painel: jogos por arena | Dev | Link em dashboard |
| 2x por semana | Ligar arena para feedback | Ops | Qual horário encheu? Qual vazio? |
| Sexta | Enviar relatório semanal | Ops | CSV de jogos + presença + receita simulada |
| Sexta | Reunião com arena (30 min) | Ops + BD | Arena sente-se acompanhada |

**Métricas semana 3:**
- Jogos criados: target ≥ 5
- Jogos realizados: target ≥ 2
- Taxa de comparecimento: target ≤ 1 falta em 4
- Feedback da arena: "positivo", "neutro" ou "negativo"

**Se abaixo do target:** Ligar arena e revisar horários / aumentar demanda

### Semana 5+: Decisão pós-piloto

**Responsável:** Founder + Ops  
**Meios:** Reunião com arena + painel final  
**Critério:** Contagem de "sim" em aceitar preço

| Decisão da Arena | Ação | Próximo passo |
|---|---|---|
| Sim → Continua com preço | Contrato mensal | Escalar para 10 arenas até fim de ano |
| Sim, mas menor preço | Renegociar | Se ≤ 10% redução: aceitar; se > 10%: ir pro fallback |
| Não → Sem receita confirmada | Encerrar educadamente | Fallback: modelo de custeio alternativo |

**Critério de sucesso Fase 2:** Mínimo **2 "sim" em 10 ofertas** (do PRD, métrica E7)

---

## 4. Success Metrics for Arena

### Por Arena (semanal)

| Métrica | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Target final |
|---|---|---|---|---|---|
| Jogos criados | 0-2 | 2-4 | 4-8 | 6-10 | ≥ 8 |
| Jogos realizados (confirmado arena) | 0 | 0-1 | 1-2 | 2-4 | ≥ 2 |
| Taxa de comparecimento | — | — | 60-80% | 75%+ | ≤ 1 falta em 4 (75%+) |
| Horários vazios preenchidos | 20% | 30% | 50% | 70% | ≥ 70% |
| Receita simulada (R$) | 0 | 0-100 | 100-400 | 300-800 | Trend positivo |

### Painel do time (agregado, 4 arenas)

| Métrica | Alvo | Como medir |
|---|---|---|
| Ofertas entregues | 10 arenas | Contagem em painel |
| Aceites por escrito | 2-4 "sim" | Contratos assinados |
| Taxa de aceitação | 20-40% | % de "sim" / total ofertas |
| Jogos fechados em 4 semanas | ≥ 20 | Query `realizado=true` no painel |
| Presença média | ≤ 1 falta em 4 | (presentes / confirmados) por jogo |
| Receita anual projetada | ≥ R$ 2.400 | 20 jogos × R$ [PREÇO] × 12 meses / 4 arenas |

### Qualitativo (entrevista com arena ao fim)

- Facilidade de uso do link: 1-10
- Qualidade dos jogadores: 1-10
- Disposição de continuar: Sim / Sim com ajustes / Não
- Obs: "Qual horário mais encheu? Qual não decolou?"

---

## 5. Fallback Plan

### Se arena diz "não" ao preço

**Cenário:** Arena recusa R$ [X] por jogo fechado.

**3 opções de resposta (nessa ordem):**

#### Opção A: Negociar o valor
- Perguntar: "Qual valor faz sentido pra vocês?"
- Se delta ≤ 10%: aceitar no piloto, revisitar no mês 2
- Se delta > 10%: Ir para Opção B

#### Opção B: Mudar o modelo
- "E se a gente cobra comissão de 5% da receita do horário?"
  - Exemplo: Horário a R$ 100, 8 pessoas → receita R$ 800 → Energia Boa R$ 40
  - **Vantagem:** Arena vê receita extra gerada direto
  - **Risco:** Precisa integração com caixa da Arena (não está em Fase 1)
  - **Status:** Esperar resultado de 2-3 arenas com modelo fixo antes de usar

- "E se a gente cobra R$ [preço reduzido] os primeiros 3 meses, depois revisita?"
  - **Vantagem:** Arena testa com risco reduzido
  - **Status:** Viável; entra no contrato como "revisão em 90 dias"

#### Opção C: Encerrar educadamente
- "Entendo. Que tal a gente conversa de novo em 2 meses quando tivermos mais dados?"
- Manter contato mensal (1 mensagem)
- **Próxima tentativa:** Com histórico de 2-3 arenas já pagando

### Se arena aceita preço mas desempenho não sai do chão

**Cenário:** Semana 3, Arena autorizada mas só 1 jogo criado, 0 realizados.

**Diagnóstico (reunião urgente com arena):**
- Horários vazios reais não bateram com o declarado?
- Arena não comunicou internamente que o link chegaria?
- Jogadores não aparecem na região?
- Link não funciona (testar em aparelho real)?

**Planos de ação:**
1. **Revisar horários:** Pode ser que a arena tenha subestimado ociosidade. Pedir nova lista.
2. **Aumentar demanda:** Time manda 50 convites na região (vs. 10 da semana 1)
3. **Ajuste de comunicação:** Arena avisa seus clientes recorrentes "tem jogo toda quarta 14h"
4. **Estender prazo:** "Vamos contar 6 semanas em vez de 4" (mantém contrato igual)
5. **Cancelar:** Se nada funcionar até semana 4, encerrar e aplicar aprendizado

### Se time não conseguir atingir 10 ofertas

**Cenário:** Fim de dezembro, só 4 arenas em piloto.

**Decisão:** Validar M1 com o que temos.
- Se ≥ 1 "sim" em 4: Continua para Fase 2 (escopo reduzido a 2-5 arenas)
- Se 0 "sim": Resetar estratégia → Fallback: modelo de custeio (time como jogador organizador, subsídio temporário)

**Relatório:** Documento "Por que M1 falhou: análise por arena" para Founder

---

## 6. Checklist de Lançamento

### Pré-lançamento (semana 1 anterior)

- [ ] PRD.md confirma preço pós-piloto (ou "A DEFINIR" com data-limite)
- [ ] E7 (tela de arenas) mostra o preço; página atualizada no ar
- [ ] Contrato template revisado por lawyer (se houver)
- [ ] Lista de 10 arenas prioritárias + contatos confirmados
- [ ] Responsável nomeado para cada fase (BD, Ops, Dev, Founder)
- [ ] Painel tem coluna "Arena parceira" e aceita arenas em dropdown

### Lançamento (semana 1)

- [ ] Checklist conversa treinado com time
- [ ] Primeira ligação feita (segunda, 10h)
- [ ] Contrato enviado ao mesmo dia (segunda, 16h)
- [ ] Dashboard de métricas no ar (Dev)
- [ ] Relatório semanal template pronto (Ops)

### Semana 2 (assinatura)

- [ ] 100% dos contratos recebidos (assinados ou com dúvidas claras)
- [ ] Arenas cadastradas no painel de time
- [ ] Soft launch com primeiros 20 convites selecionados (segunda, 10h)
- [ ] Teste em aparelho real (Android + iPhone) passando

### Semana 3-4 (operação)

- [ ] Relatório semanal sendo enviado toda sexta
- [ ] Reunião com cada arena toda semana (mesma hora)
- [ ] Painel atualizado em tempo real
- [ ] Presença sendo marcada pela arena (≥ 50% dos jogos)

### Semana 5 (decisão)

- [ ] Resultado consolidado: X arenas aceitam pagar
- [ ] Relatório "Piloto M1: Validado" ou "Piloto M1: Não validado"
- [ ] Decisão sobre Fase 2 tomada

---

## Referências

| Documento | Seção | Uso |
|---|---|---|
| PRD.md | Seção 2: "Resumo" | Frase de abertura da ligação |
| PRD.md | Decisão 1 | Preço pós-piloto (valor fixo em reais) |
| PRD.md | Decisão 11 | Teto de preço (R$ 1.000 máx) |
| PRD.md | Apêndice A: Arenas | Textos exatos para E7 |
| PRD.md | Requisito E7, J5 | Aceite escrito da oferta |
| SPECS.md | Seção 2.1: `arenas_piloto` | Campos de contrato |
| AUDITORIA.md | Seção 7: M1, M2, M3 | Fragilidades a evitar |

---

## Versão

v1.0 | 16/11/2026 | Kickoff operacional para M1

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
