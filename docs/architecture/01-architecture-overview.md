# Arquitetura da Energia Boa

> 📝 **Atualizado em 16/11/2026** após rebranding e alinhamento com schema Fase 2.
> Campos corrigidos: `donoZap` → `jogos/{id}/contato`, "Reserva gerada" → "Valor de quadra confirmado"

App de página única no GitHub Pages (`index.html`), com Firebase: login Google e Firestore ao vivo. Sem servidor próprio. As permissões ficam em `firestore.rules`.

## Casos de uso

```mermaid
flowchart LR
  V([Convidado sem conta])
  J([Jogador logado])
  T([Time da arena])
  V --> C1[Ver convite e fazer check-in]
  V --> C2[Entrar na lista de espera]
  V --> C3[Ver jogos abertos e filtrar]
  J --> C1
  J --> C3
  J --> C4[Criar perfil]
  J --> C5[Marcar jogo público ou privado]
  J --> C6[Compartilhar link]
  J --> C7[Desistir e liberar a vaga]
  J --> C8[Gerenciar confirmados do próprio jogo]
  T --> C5
  T --> C9[Ver quem combina e convidar no WhatsApp]
  T --> C10[Painel: valor de quadra confirmado]
  T --> C11[Importar base do formulário]
```

## Jornada principal (a da demo)

```mermaid
sequenceDiagram
  actor Ana as Ana (sozinha)
  participant App as Energia Boa
  participant DB as Firestore
  actor Beto as Beto (convidado)
  actor Time as Time da arena
  Ana->>App: Bora jogar (login Google)
  Ana->>App: Marcar jogo: vôlei, nível 3, sáb 18h, já é 1 de 4
  App->>DB: cria jogos/{id}
  App-->>Ana: link do convite
  Ana->>Beto: link pelo WhatsApp
  Time->>App: Quem combina → Convidar
  Beto->>App: abre o link, "Tô dentro" (sem conta)
  App->>DB: cria confirmacoes/{id}
  DB-->>App: placar ao vivo 3/3
  App-->>Ana: Fechou!
  App-->>Time: Valor de quadra confirmado
  Note over Beto,App: Jogo cheio → lista de espera. Se alguém sai, o próximo entra.
```

## Dados (coleções do Firestore)

```mermaid
classDiagram
  class Perfil {
    uid
    nome
    cidade
    esportes[]
    nivel 1..5
    horarios[]
    whatsapp
    aceitaConvites
    plano
  }
  class Jogo {
    id
    esporte
    nivel
    quando
    arena
    cidade
    total
    vagas
    valor
    visibilidade publico|privado
    donoUid
    donoNome
    contato (subcoleção: WhatsApp sob acesso restrito)
    origem jogador|equipe
    teste
  }
  class Confirmacao {
    id
    jogoId
    nome
    via link|whatsapp
    uid opcional
    criadoEm
  }
  class Jogador {
    id
    nome
    whatsapp
    esportes[]
    nivel
    horarios[]
    origem tally|manual
  }
  class Convite {
    jogoId
    jogadorId
    em
  }
  class Admin {
    uid
    nome
  }
  Perfil "1" --> "*" Jogo : marca
  Jogo "1" --> "*" Confirmacao : check-ins (ordem = fila)
  Jogo "1" --> "*" Convite
  Jogador "1" --> "*" Convite
  Admin ..> Jogador : só o time lê
  Admin ..> Perfil : só o time e o dono leem
```

As primeiras `vagas` confirmações, por ordem de chegada, estão no jogo. As seguintes formam a lista de espera.

## Telas

```mermaid
flowchart TD
  I[Início: Bora jogar] -->|login| P[Perfil, pode pular]
  P --> M[Meus jogos]
  I --> A[Jogos abertos + filtros]
  M --> N[Marcar jogo]
  N --> G[Meu jogo: placar, confirmados, divulgar]
  G -->|link| CV[Convite: Tô dentro / lista de espera]
  A --> CV
  M -->|código do time| PA[Painel do time]
  PA --> GT[Jogo: Quem combina + Convidar]
  PA --> JB[Jogadores: base e importação]
```

## Quem pode o quê

| Dado | Qualquer um | Jogador logado | Time |
|---|---|---|---|
| Jogos e confirmações | lê | marca o próprio jogo, apaga o próprio | tudo |
| Check-in | cria com o nome | cria, e desiste do próprio | tudo |
| Perfis e base (WhatsApp) | nada | só o próprio perfil | lê tudo |
| Código do time | nada | usa para entrar | lê e troca |

## Atualização de 15/11/2026

- **Jogo** ganhou `tipoLocal` (`privada` ou `publica`). O campo `donoZap` ficou vazio: o WhatsApp de quem organiza mora em `jogos/{id}/contato/dono`.
- **Contato:** lido só pelo dono, pelo time e por quem tem a confirmação `confirmacoes/{jogoId}_{uid}`.
- **Confirmação com conta** tem id fixo `{jogoId}_{uid}`: uma por pessoa e por jogo. Jogo público só aceita confirmação com conta.
- **PWA:** `manifest.webmanifest`, `sw.js` (rede primeiro para o app, cache primeiro para SDK e fontes; dados nunca em cache), `offline.html`, `icons/`.
- **Nova tela:** Privacidade e segurança. A navegação fica na base da tela no celular.

```mermaid
flowchart LR
  P[Página] -->|arquivos do app| SW[Service worker]
  SW -->|rede primeiro| GH[GitHub Pages]
  SW -->|sem rede| C[(Cache do app)]
  P -->|SDK e fontes| SW
  SW -->|cache primeiro| G[gstatic e Google Fonts]
  P -->|dados e login, direto| FB[(Firestore e Auth)]
```
