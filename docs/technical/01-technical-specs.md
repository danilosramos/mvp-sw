# SPECS: Especificações Técnicas do Energia Boa

Data: 16/11/2026. Baseado em: [`PRD.md`](01-prd-phase1-2.md).

**Este é um documento de implementação técnica.** Para requisitos, consulte [PRD.md](01-prd-phase1-2.md).

Este documento descreve especificações técnicas necessárias para implementar os requisitos do PRD em duas fases:
- **Seção 1:** Stack e premissas arquiteturais
- **Seção 2:** Dados — referência para schema Firestore (veja [PRD seção 8](01-prd-phase1-2.md#8-modelo-de-dados-e-migração))
- **Seção 3-15:** Implementação, padrões, checklist

---

## 1. Visão Geral Técnica

### Stack Tecnológico
- **Frontend:** HTML5, CSS3, JavaScript ES2020+
- **Backend:** Firestore (database) + Firestore Rules (authorization)
- **Autenticação:** Google Sign-In
- **Hospedagem:** GitHub Pages (estática)
- **Testing:** Python para e2e, JavaScript para regras
- **Utilitários:** Firebase CLI, GitHub Actions

### Premissas Arquiteturais
1. Sem servidor próprio – toda lógica de negócio nas Firestore Rules
2. Service Worker para cache e offline (versão semanal)
3. Datas convertidas para timestamp UTC (Brasília: UTC-3)
4. Versão do app comparada com versão.json na rede
5. App Check em modo monitoramento (Fase 1) → exigido (Fase 2)
6. Sem etapa de build obrigatória (apenas para teste)

---

## 2. Estrutura de Dados

> **Referência técnica de:**  [`PRD.md` seção 8 — Modelo de Dados e Migração](01-prd-phase1-2.md#8-modelo-de-dados-e-migração)
> 
> Este é o esquema Firestore da autoridade. Para decisões sobre design e campos, consulte PRD.

### 2.1 Coleções Raiz (Fase 1)

#### `config/`
Documento único para configuração de times e ofertas.

```
config/equipe {
  codigo: string (6 caracteres, único por time)
  preco_pos_piloto?: number (0-1000, em reais)
  endereço_oficial?: string (URL do app)
}

config/versao {
  versao: string ("YYYY.MM.DD")
  minima: string (força atualização)
}
```

#### `jogos/{id}`
Jogos públicos ou privados (criados por jogadores ou time).

```
jogos/{id} {
  // Identifiers
  id: string (20 chars, crypto.getRandomValues)
  
  // Timing
  quando: string ("YYYY-MM-DDTHH:mm" - local, sem timezone)
  quandoTs: timestamp (derivado de quando em fuso Brasília)
  criadoEm: number (Fase 1 apenas) → timestamp (Fase 2)
  
  // Location & Sport
  esporte: string (40 chars max)
  arena: string (2-80 chars, nome do local)
  tipoLocal: enum ('publica' | 'privada') = 'privada'
  cidade: string
  cidadeChave: string (minúsculas, acentos normalizados, para busca)
  
  // Participants
  total: int (2-30)
  vagas: int (1 até total)
  nivel: int (1 | 3 | 5)
  valor?: number (0-1000, null em quadra pública)
  
  // Status
  estado: enum ('aberto' | 'cancelado') = 'aberto' (Fase 2)
  situacao: enum ('vago' | 'cancelar') = 'vago'
  teste: boolean = false
  
  // Owner
  donoUid: string
  donoNome: string (60 chars max)
  
  // Meta
  origem: enum ('jogador' | 'time') = 'jogador'
  origem_link?: string (40 chars, opcional)
  visibilidade: enum ('publico' | 'privado') = 'privado' (Fase 2)
  
  // Timestamps (Fase 2)
  canceladoEm?: timestamp
  atualizadoEm?: timestamp
  
  // Arena Integration (Fase 2)
  arenaId?: string (referência a arenas/{aid})
  realizado?: boolean (apenas time)
  valorConfirmado?: boolean (apenas time)
  horarioVazio?: boolean (apenas time)
  
  // Tracking (Fase 2)
  copiadoDe?: string (ID do jogo original)
}
```

#### `confirmacoes/{cid}`
Confirmações de presença em jogos (Fase 1). Movem para `jogos/{id}/confirmacoes/{cid}` em Fase 2.

```
confirmacoes/{cid} {
  jogoId: string
  nome: string (2-40 chars)
  via: enum ('link' | 'whatsapp')
  uid?: string (presente se logado)
  criadoEm: number (Fase 1) → timestamp (Fase 2)
  
  // Fase 2 apenas
  estado: enum ('confirmado' | 'desistiu' | 'removido') = 'confirmado'
  saiuEm?: timestamp
  presente?: boolean
  presencaEm?: timestamp
  origem?: string (1-40 chars)
}
```

#### `perfis/{uid}`
Dados do jogador.

```
perfis/{uid} {
  nome: string (60 chars max)
  cidade: string
  esportes: array[string] (mínimo 1)
  nivel: int (1 | 3 | 5)
  
  // Opcional
  horarios?: object { inicio: int, fim: int } (hora do dia 0-23)
  whatsapp?: string (formato 55 + DDD + 8-9 dígitos)
  origem?: string (1-40 chars) [Fase 2]
}
```

#### `admins/{uid}`
Membros do time (apenas escrita controlada).

```
admins/{uid} {
  nome: string (60 chars max)
  codigo: string (6 caracteres, matches config/equipe)
  criadoEm: timestamp
}
```

#### `arenas_piloto/{id}`
Ofertas de piloto de arenas.

```
arenas_piloto/{id} {
  arenaId?: string (referência a arenas/{aid}, Fase 2)
  nomeArena: string
  cidade: string
  whatsapp: string
  vizualizacoes?: int
  
  // Dados comerciais
  valorAceitavel?: number (0-1000, opcional) [Fase 2]
  
  // Situação da oferta (apenas time, Fase 2)
  oferta_resposta?: enum ('sim' | 'nao' | null)
  oferta_respondidoEm?: timestamp
  oferta_valor?: number
  
  // Metadata
  criadoEm: timestamp
  origem?: string (1-40 chars) [Fase 2]
}
```

#### `interesse_premium/{uid}`
Respostas sobre features que valeriam pagar.

```
interesse_premium/{uid} {
  respostas: array[string] (até 4)
  // Opções: "Lembrete e aviso de vaga no WhatsApp", 
  //         "Jogo garantido: quem fura paga",
  //         "Achar gente do meu nível mais rápido",
  //         "Nada, prefiro grátis"
}
```

### 2.2 Subcoleções (Fase 2)

#### `jogos/{id}/confirmacoes/{cid}`
Confirmações de presença movem da raiz para subcoleção.

```
jogos/{id}/confirmacoes/{cid} {
  nome: string (2-40 chars)
  via: enum ('link' | 'whatsapp')
  uid?: string (apenas se logado)
  criadoEm: timestamp
  
  estado: enum ('confirmado' | 'desistiu' | 'removido')
  saiuEm?: timestamp
  presente?: boolean
  presencaEm?: timestamp
  origem?: string (1-40 chars)
  
  // Para cid = uid quando logado
  // Para cid = 20 chars random quando sem conta
}
```

#### `jogos/{id}/contatos/{cid}` [Fase 2]
Contatos de convidados sem conta (apenas dono e time leem).

```
jogos/{id}/contatos/{cid} {
  whatsapp: string (formato 55 + DDD + 8-9 dígitos)
  consentiu: boolean
  criadoEm: timestamp
  
  // Mesmo cid da confirmação correspondente
}
```

#### `arenas/{aid}/privado/piloto` [Fase 2]
Dados comerciais de piloto da arena (apenas time acessa).

```
arenas/{aid}/privado/piloto {
  inicio_data: timestamp
  preco_hora: number (0-1000)
  preco_pos_piloto: number (0-1000)
  aceite: enum ('sim' | 'nao' | null)
  aceite_data?: timestamp
  
  horarios_vazios: array[object] {
    dia: int (0-6, segunda=1)
    inicio: int (0-23)
    fim: int (0-23)
  }
  
  pedidoId: string (referência a arenas_piloto/{id})
}
```

#### `arenas/{aid}` [Fase 2]
Arenas parceiras (criadas pelo time, leitura pública).

```
arenas/{aid} {
  nome: string
  cidade: string
  cidadeChave: string (normalizado para busca)
  ativa: boolean = true
  
  // Privado em /privado/piloto
}
```

---

## 3. Firestore Rules – Especificação de Autorização

### 3.1 Funções Base (Fase 1)

```javascript
function ehEquipe() {
  return request.auth != null
    && exists(/databases/$(database)/documents/admins/$(request.auth.uid));
}

function ehDonoDoJogo(id) {
  return request.auth != null
    && get(/databases/$(database)/documents/jogos/$(id)).data.donoUid == request.auth.uid;
}

function jogoDeJogadorValido() {
  let d = request.resource.data;
  return request.auth != null
    && d.donoUid == request.auth.uid
    && d.origem == 'jogador'
    && d.teste == false
    && d.estado == 'aberto'
    && d.criadoEm == request.time
    && camposDoJogoValidos();
}

function camposDoJogoValidos() {
  let d = request.resource.data;
  return d.arena is string && d.arena.size() >= 2 && d.arena.size() <= 80
    && d.nivel in [1, 3, 5]
    && d.quando is string
    && d.quando.matches('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$')
    && d.quandoTs is timestamp
    && d.quandoTs > request.time - duration.value(30, 'm')
    && d.quandoTs < request.time + duration.value(365, 'd')
    && d.total is int && d.total >= 2 && d.total <= 30
    && d.vagas is int && d.vagas >= 1 && d.vagas <= d.total
    && d.get('tipoLocal', 'privada') in ['publica', 'privada']
    && (d.valor == null || (d.valor is number && d.valor >= 0 && d.valor <= 1000))
    && (d.get('tipoLocal', 'privada') != 'publica' || d.valor == null);
}
```

### 3.2 Regra de Transição (Fase 1) → Regra Estrita (Dia 7 Fase 1)

Fase 1 aceita `criadoEm` como número OU timestamp:
```javascript
&& (request.resource.data.criadoEm == request.time 
    || request.resource.data.criadoEm is number)
```

Fase 1 Dia 7+ (estrita): aceita só timestamp
```javascript
&& request.resource.data.criadoEm == request.time
```

### 3.3 Leitura de Confirmações (Fase 2)

Sem conta: acessa confirmação por ID público (20 chars)
Com conta: acessa confirmação com seu UID

---

## 4. Adaptadores Firebase

### 4.1 `firebase.js` – Interface com Firestore

```javascript
// Inicialização
initializeApp(config);
setupAppCheck();
setupVersionCheck();

// Leitura de Hora do Servidor
function getServerTime() {
  return firebase.firestore.Timestamp.now();
}

// Conversão de Datas
function parseDateToTimestamp(dataStr, horaStr) {
  // Recebe "YYYY-MM-DD" e "HH:mm"
  // Converte para UTC assumindo fuso Brasília (UTC-3)
  // Retorna timestamp de Firestore
}

function formatTimestamp(ts) {
  // Retorna "YYYY-MM-DD" e "HH:mm" em fuso Brasília
}

// Operações Firestore
async function writeGame(gameData) {
  gameData.criadoEm = getServerTime();
  gameData.quandoTs = parseDateToTimestamp(gameData.quando.split('T')[0], gameData.quando.split('T')[1]);
  return db.collection('jogos').doc(novoId()).set(gameData);
}

async function queryPublicGames(limit = 50) {
  // Busca jogos públicos, futuros, limitado
  // Escuta confirmações apenas dos jogos exibidos
  return db.collection('jogos')
    .where('visibilidade', '==', 'publico')
    .where('quandoTs', '>', new Date())
    .orderBy('quandoTs')
    .limit(limit)
    .onSnapshot();
}

async function listUserGames(uid) {
  // Fase 2: busca jogos do usuário
  return db.collection('jogos')
    .where('donoUid', '==', uid)
    .orderBy('quandoTs')
    .onSnapshot();
}

async function saveConfirmation(jogoId, confirmacaoData) {
  confirmacaoData.criadoEm = getServerTime();
  confirmacaoData.estado = 'confirmado';
  
  // Fase 2: subcoleção
  return db.collection('jogos').doc(jogoId)
    .collection('confirmacoes').doc(cid).set(confirmacaoData);
}

async function batchWrite(operations) {
  // Escrita em lote (Fase 2: migração)
}

async function queryByGroup() {
  // Consulta entre jogos (Fase 2: grupo de coleções)
}
```

### 4.2 `mock-backend.js` – Simulação para Testes

```javascript
class MockFirestore {
  static getServerTime() {
    return new Date().getTime();
  }
  
  static quandoToTs(quando) {
    // Converte "YYYY-MM-DDTHH:mm" para timestamp
    // Assume fuso Brasília
  }
  
  // Implementar todas as operações de firebase.js
}
```

---

## 5. Controle de Versão do App

### 5.1 Arquivo `versao.json`

```json
{
  "versao": "2026.11.16",
  "minima": "2026.11.09",
  "changelog": "Quebra de regras: hora do servidor"
}
```

### 5.2 Service Worker

```javascript
// sw.js
const VERSAO_ATUAL = "2026.11.16";

async function checkVersionOnStart() {
  const remoteVersion = await fetch('versao.json').then(r => r.json());
  
  if (remoteVersion.minima > VERSAO_ATUAL) {
    showUpdateRequired();
    blockWrites();
  }
  return remoteVersion;
}

async function checkVersionOnReturn() {
  // Roda ao voltar para a aba
}
```

---

## 6. Autenticação e Autorização

### 6.1 Google Sign-In (Fase 1)

```javascript
function loginWithGoogle() {
  const provider = new GoogleAuthProvider();
  provider.addScope('profile');
  
  return signInWithPopup(auth, provider)
    .catch(handleLoginError);
}

function handleLoginError(error) {
  switch(error.code) {
    case 'auth/popup-blocked':
      return "O navegador bloqueou a janela do Google...";
    case 'auth/cancelled-popup-request':
      return "Login cancelado. Toque de novo para entrar.";
    case 'auth/unauthorized-domain':
      return "Não deu para entrar agora...";
    default:
      return "Não deu para entrar agora. Tente de novo daqui a pouco.";
  }
}
```

### 6.2 Configuração da Chave Web (C1)

Restringir em console do Firebase:
- **HTTP referrer:** domínio oficial + localhost
- **APIs ativadas:** Firestore, Authentication, App Check
- **Domínios de Auth:** domínio oficial + projeto.firebaseapp.com

### 6.3 Desabilitar Email/Senha (C2)

Remover de `firebase.js` qualquer uso de `signInWithEmailAndPassword()`.
Desabilitar no console do Firebase → Authentication → Sign-in method.

---

## 7. App Check (C3)

### 7.1 Inicialização

```javascript
import { initializeAppCheck, getBrowserReCaptchaProvider } from 'firebase/app-check';

if (!self.FIREBASE_APPCHECK_DEBUG_TOKEN) {
  initializeAppCheck(app, {
    provider: getBrowserReCaptchaProvider(),
    isTokenAutoRefreshEnabled: true,
    forceRefresh: false
  });
}
```

### 7.2 Monitoramento (Fase 1) → Exigência (Fase 2)

Fase 1: Modo monitoramento (nenhuma exigência em Firestore)
Fase 2 Dia 7+: Exigência em regras (após validar >95% das requisições)

---

## 8. Identificadores

### 8.1 ID de Jogo e Confirmação (B7)

```javascript
function novoId() {
  const array = new Uint8Array(15);
  crypto.getRandomValues(array);
  return Array.from(array, byte => 
    byte.toString(16).padStart(2, '0')
  ).join('').substring(0, 20).toUpperCase();
  // Resultado: 20 chars alfanuméricos [A-Za-z0-9]
}
```

Nunca usar `Math.random()` nem `Date.now()`.

---

## 9. Dados de Hora e Fuso

### 9.1 Campo `quando`

Formato no banco: `"YYYY-MM-DDTHH:mm"` (horário local sem timezone)
Exemplo: `"2026-11-21T18:30"` (18:30 do horário local do jogador)

### 9.2 Derivação `quandoTs`

```javascript
function quandoToTimestamp(quando) {
  // Entrada: "2026-11-21T18:30"
  // Estratégia: fazer parse como hora de Brasília (UTC-3)
  
  const [data, hora] = quando.split('T');
  const [ano, mes, dia] = data.split('-').map(Number);
  const [h, m] = hora.split(':').map(Number);
  
  // Criar Date em fuso Brasília
  const dateUTC = new Date(ano, mes - 1, dia, h + 3, m, 0);
  // Ajustar para UTC: adicionar 3 horas
  
  return Timestamp.fromDate(dateUTC);
}
```

**Regra:** Confirmações não são aceitas após `quandoTs` (nem durante Fase 1).

---

## 10. Fases de Implementação

### Fase 1 – 71 Requisitos em 12 Entregas

#### Entrega 1: Testes Confiáveis (A1-A4)
- Testes e2e com datas relativas (via `quando()` mock)
- Validação de saída de código em scripts de teste
- GitHub Actions com teste + contraste + PWA + regras
- Versionamento do app com `versao.json`

#### Entrega 2: Limpeza (C2, C4, E1-E11, F1-F5)
- Remover login por email/senha
- Aligner documentação ao código
- Corrigir textos e mensagens de erro
- Implementar acessibilidade (títulos, alturas, contraste)

#### Entrega 3: Regras Testáveis (A5)
- `firebase.json` com testes para cada regra
- `firestore.indexes.json` com índices necessários
- `package.json` só de desenvolvimento

#### Entrega 4: Hora do Servidor + Faixas (B1-B5, B6)
- Aceitar `criadoEm` como hora do servidor (regra de transição)
- Converter `quando` em `quandoTs`
- Validar faixas de nível, valor, horário
- Recusar confirmação após início do jogo
- Time remove membros pelo app

#### Entrega 5: Entrada no Produto (D1-D6)
- Destino `#novo` sobrevive ao login
- Suporte a parâmetro `?c=<id>` para convites
- Tela "Abrir no navegador" em WhatsApp
- Perfil 4 campos, opcional, "Preencher depois"
- Botão "Entrar" direto no login

#### Entrega 6: Configuração (C1, C3)
- Chave Web restrita por referenciador
- App Check em modo monitoramento

**Fim Fase 1**

#### Entrega 7: Medição + Retenção (G1-G5)
- Parâmetro `?o=` para origem
- Contador sem cookies (rota + eventos)
- "Adicionar ao calendário" (`.ics` + Google Agenda)
- Oferecimento de instalação

#### Entrega 8: Adaptador Novo (H1)
- Consultas filtradas, limitadas
- Leitura única
- Escrita em lote

#### Entrega 9: Migração (H2-H7) ⭐ Grande
- Página de migração com simulação
- Preencher `quandoTs`, `estado`, `visibilidade`
- Mover confirmações para subcoleção
- Implementar contatos em `jogos/{id}/contatos`
- Implementar jogo privado por link

#### Entrega 10: Estados + Controle (I1-I10)
- Cancelamento com estado, não exclusão
- Desistir e ser removido com estado
- Edição de jogo com aviso
- Presença pós-jogo
- "Marcar de novo" para a semana seguinte

#### Entrega 11: Prova para Arena (J1-J8)
- Fechamento calculado (data da confirmação final)
- Presença: quem organiza marca
- Arena parceira com identificador
- "Realizado" + "Valor confirmado" + "Horário vazio" (apenas time)
- Painel com agregação 8 semanas
- Premium como pergunta "O que valeria pagar?"

#### Entrega 12: Qualidade (K1-K7, H8)
- Erros junto do campo com `aria-invalid`
- Filtros recolhidos no mobile
- Chips com altura mínima 44px
- App Check exigido (após semana em monitoramento)

### Fase 2 – Escopo Pós-Piloto

Decisão condicional ao "sim" das arenas em J5.

---

## 11. Especificações de Telas

### 11.1 Landing

**Componentes:**
- Prova social: "28 de 36 respostas"
- Seção "Tem vaga agora" com limite 50 jogos
- Chamada para arenas
- Prévia do link (og:image, og:url, etc)

**Estados:**
- Sem jogos: mensagem + botão "Marcar jogo"
- Com jogos: lista com sugestões

### 11.2 Procurar

**Filtros (mobile: "Mais filtros"):**
- Esporte (chips multichoice)
- Dia da semana (recolhido mobile)
- Período do dia (manhã/tarde/noite) [recolhido mobile]

**Ordem:** sugestões personalizadas (Combinado com você > Quase)

**Estados vazios:**
- "Nenhum jogo com esses filtros"
- Botões "Marcar jogo de [esporte]" e "Limpar filtros"

### 11.3 Convite (Jogo Público)

**Se navegador embutido (WhatsApp/Instagram/Facebook):**
- Título: "Abra no navegador para entrar"
- Botão primário: "Abrir no navegador"
- Botão secundário: "Copiar link"
- Link alternativo: "Já está no navegador? Entrar com Google"

**Se navegador normal:**
- Botão "Tô dentro" com Google Sign-In

**Estados do jogo:**
- Aberto: botão "Tô dentro", placar das vagas
- Lotado: "Esse jogo já fechou", "Entrar na lista de espera"
- Cancelado: "Esse jogo foi cancelado", botão "Procurar outro jogo"
- Já começou: "Esse jogo já começou"

**Contato opcional:**
- Rótulo: "Seu WhatsApp (opcional)"
- Consentimento checkbox
- Salvo em `jogos/{id}/contatos/{cid}`

**Integração:**
- "Adicionar ao calendário" (`.ics` + Google)
- "Chamar mais gente" (share nativo + WhatsApp fallback)

### 11.4 Jogo de Quem Organiza

**Se ainda aberto:**
- "Enviar no WhatsApp" (compartilhamento)
- Botão "Editar jogo"
- Botão "Cancelar jogo"

**Se próximo de fechar:**
- "Faltam N pra fechar"
- "Avisar [nome] que abriu vaga" (se na espera)

**Depois do horário:**
- Bloco "Quem foi?" com checkboxes
- Botão "Marcar de novo na próxima semana"

### 11.5 Marcar Jogo

**Formulário:**
- Data e hora (`quando`)
- Local (nome, cidade, tipo=pública/privada)
- Esporte
- Nível (1/3/5)
- Total de pessoas (2-30)
- Vagas (1 até total)
- Preço (opcional, 0-1000)
- **Fase 2:** Escolher arena parceira

**Validações:**
- Hora não no passado
- Horário não mais de 30 min no passado (B4)
- Total ≥ 2 e ≤ 30
- Vagas ≥ 1
- Preço número ou vazio
- Se reduzir total abaixo de confirmados: recusar
- Erros junto do campo (`aria-invalid`, `aria-describedby`)

### 11.6 Perfil (Primeiro Acesso)

**Campos:**
1. Nome (obrigatório)
2. Cidade (obrigatório)
3. Esporte (multichoice, mínimo 1)
4. Nível (1/3/5)

**Altura:** Cabe em 2 telas a 390×844
**Botões:** "Salvar e continuar" + "Preencher depois"

### 11.7 Meus Jogos

**Separação:**
- Aba "Próximos" (futuros, ordem por data)
- Aba "Já joguei" (passados, recolhida com contagem)

**Cartão indica:** "Você marcou" vs "Você vai"

### 11.8 Painel (Time)

**Período:** últimas 8 semanas (com histórico completo sob demanda)
**Indicadores:**
- Esta semana / semana passada
- Jogos marcados, fechados, realizados
- Valor de quadra dos jogos que completaram

**Por Arena Parceira:**
- Lista de arenas
- Número de jogos fechados com valor confirmado
- Ofertas: "N sim em M ofertas"

**Export:** CSV com acentos corretos, sem jogos de teste

### 11.9 Arenas (Página Pública)

**Se sem preço configurado:**
- "30 dias grátis para testar. O valor depois do piloto é combinado por escrito antes de começar."

**Se com preço:**
- "30 dias grátis para testar. Depois, R$ XXX por jogo fechado em horário que você marcou como vazio."

**Formulário de Piloto:**
- Nome, cidade, WhatsApp
- Horários vazios (seleção por dia/hora)
- Resposta: "Quanto valeria pagar?"

---

## 12. Fluxos Técnicos Críticos

### 12.1 Confirmação de Jogo

```
1. Usuário clica "Tô dentro"
2. Se sem conta: redireionar para login Google (D6)
3. Depois do login: buscar/criar perfil (D1)
4. Preencher nome (pré-preenchido se logado, obrigatório se não)
5. Enviar confirmação:
   a. Regra valida: estado=confirmado, criadoEm=now, antes do início
   b. Preparar confirmação:
      - Com conta: uid = auth.uid, cid = auth.uid
      - Sem conta: uid = null, cid = 20 chars random
   c. Salvar em confirmacoes/ (Fase 1) ou jogos/{id}/confirmacoes/ (Fase 2)
   d. Atualizar vagas (calculado de confirmacoes)
6. Mostrar "Você está no jogo!" com confete
7. Oferecer "Adicionar ao calendário" + "Chamar mais gente"
```

**Validações:**
- Jogo não pode estar cancelado
- Hora do servidor < quandoTs
- Mesmo uid não pode confirmar 2x no mesmo jogo

### 12.2 Cancelamento de Jogo

```
1. Dono clica "Cancelar jogo"
2. Diálogo: "Cancelar este jogo? N pessoas confirmaram."
3. Opção: "Avisar o grupo no WhatsApp"
4. Ao confirmar:
   a. Regra: estado='cancelado', canceladoEm=now, contato do dono apagado
   b. Confirmacoes permanecem com estado 'confirmado'
   c. Jogo sai de buscas (visibilidade=publico && estado!=cancelado)
5. Exibir "Jogo cancelado" no convite existente
6. Oferecer "Procurar outro jogo"
```

### 12.3 Presença Pós-Jogo

```
1. Depois de quandoTs, bloco "Quem foi?" aparece
2. Dono marca checkboxes de quem compareceu (presente=true)
3. Validação: antes de quandoTs + 7 dias
4. Painel agrega: "X de Y foram"
5. Se realizado=true (apenas time): contar para faturamento
```

### 12.4 Marcar de Novo

```
1. Depois de quandoTs, botão "Marcar de novo na próxima semana"
2. Abre formulário preenchido com quando = hoje + 7 dias
3. Novo jogo tem copiadoDe = ID do jogo original
4. Não copia confirmações
5. Depois de salvar: oferecer "Chamar quem jogou"
```

### 12.5 Migração (Fase 2)

```
Pré-migração:
1. Publicar regras ampliadas (aceitam estrutura nova e antiga)
2. Publicar app novo com versao.minima alterada

Migração (página em /ferramentas/):
1. Modo simulação: ler dados antigos no emulador
2. Para cada jogo antigo:
   a. Preencher quandoTs derivado de quando
   b. Gravar estado='aberto'
   c. Gravar visibilidade='privado' (padrão antigo)
3. Para cada confirmação antiga:
   a. Copiar para jogos/{id}/confirmacoes/{cid}
   b. Gravar estado='confirmado'
4. Criar índices em Firestore

Pós-migração:
1. Bloquear criação em confirmacoes/ (regra estrita)
2. Executar migração novamente para confirmar dados 3-5
3. Depois de 7 dias: apagar confirmacoes/ antiga
```

---

## 13. Padrões de Código

### 13.1 Nomes de Variáveis

- `jogoId`, `confirmacaoId`, `cid` para IDs
- `uid` para user ID do Firebase Auth
- `quandoTs` para timestamp do jogo
- `quando` para texto local `YYYY-MM-DDTHH:mm`
- `estado` para estado atual (aberto, cancelado, confirmado, desistiu, removido)

### 13.2 Funções de Data

```javascript
// Sempre usar para conversão
function quandoToTimestamp(quando) { ... }
function timestampToQuando(ts) { ... }

// Nunca usar Date.getTime() diretamente em Firestore
// Sempre usar firebase.firestore.Timestamp.now()
```

### 13.3 Tratamento de Erros

Erros de permissão devem ser mensagens ao usuário, não técnicas:

```javascript
catch (error) {
  if (error.code === 'permission-denied') {
    return showError("Você não pode fazer isso neste jogo.");
  }
  console.warn(error); // Log técnico
  return showError("Não deu para entrar agora. Tente de novo daqui a pouco.");
}
```

---

## 14. Checklist de Implementação

### Fase 1 – Antes de Divulgar

- [ ] A1: Testes com datas relativas
- [ ] A2: Testes com exit codes válidos
- [ ] A3: GitHub Actions publicando só app
- [ ] A4: Versionamento com `versao.json`
- [ ] A5: Testes das regras no emulador
- [ ] B1: `criadoEm` = timestamp (transição dia 1, estrita dia 7)
- [ ] B2: Leitura aceita número e timestamp
- [ ] B3: Faixas validadas (nível, valor, horário)
- [ ] B4: `quandoTs` derivado de `quando`
- [ ] B5: Sem confirmação após início
- [ ] B6: Time remove membros
- [ ] B7: IDs com 20 chars random
- [ ] C1: Chave restrita por referenciador
- [ ] C2: Email/senha removido
- [ ] C3: App Check monitoramento
- [ ] C4: Documentação alinhada
- [ ] D1: Destino `#novo` persiste
- [ ] D2: Suporte a `?c=<id>`
- [ ] D3: Teste manual WhatsApp (Android + iPhone)
- [ ] D4: Perfil 4 campos, opcional
- [ ] D5: Nível não vem marcado
- [ ] D6: "Entrar" abre login direto
- [ ] E1-E11: Textos e acessibilidade
- [ ] F1-F5: Acessibilidade completa
- [ ] G1-G5: Medição (Fase 2 início)
- [ ] H1-H8: Preparação para migração

### Fase 2 – Piloto com Arenas

- [ ] H2-H7: Migração completa
- [ ] I1-I10: Estados e controle de dono
- [ ] J1-J8: Faturamento para arena
- [ ] K1-K7: Qualidade de telas

---

## 15. Referências Externas

- Firestore Rules: https://firebase.google.com/docs/firestore/security/start
- Google Sign-In: https://developers.google.com/identity/sign-in/web
- App Check: https://firebase.google.com/docs/app-check
- Calendário iCal: https://tools.ietf.org/html/rfc5545
- CSV Export: Formato CSV com UTF-8 e acentos

---

## 16. Decisões Técnicas em Aberto

1. **Teto de preço (B3):** R$ 1.000 por hora (a confirmar)
2. **Endereço oficial (C1, E9):** A definir antes de Fase 1 terminar
3. **Ferramenta de analytics (G2):** Serviço sem cookies (termos/preço a conferir)
4. **Teste em WhatsApp (D3):** Decide se D2 basta ou se abre decisão 12
5. **App Check exigência (H8):** Depois de 7 dias com >95% de requisições verificadas

---

## Notas

- Este documento é vivo: atualizar com cada entrega
- Referências a seções do PRD.md facilitam rastreabilidade
- Decisões em aberto bloqueiam alguns requisitos (C1, E9)
- Testes de regras são pré-requisito para qualquer publicação de regra

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
