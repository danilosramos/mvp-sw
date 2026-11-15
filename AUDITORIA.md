# Auditoria do Fechou e o que mudou (15/11/2026)

## 1. Diagnóstico

### Técnico

| Item | Como está | Avaliação |
|---|---|---|
| Arquitetura | Página única (`index.html`, JavaScript puro) + `firebase.js` + `config.js`. Sem build. | Certa para 54 horas e para o GitHub Pages. Vira dívida quando passar de umas 2 mil linhas: separar em módulos depois do evento. |
| Dados | Firestore ao vivo, login Google, regras em `firestore.rules`. | Funciona. O app escuta as coleções `jogos` e `confirmacoes` inteiras: serve até centenas de jogos, não escala além disso. |
| Estado | Um objeto global e redesenho por tela. | Simples e previsível. |
| Deploy | Push na `main`, GitHub Pages serve a pasta. Caminhos relativos. | Funciona em subpasta (`/mvp-sw/`). |
| Console | Sem erros na página publicada. | Ok |
| Testes | Não havia nada no repositório. | **Corrigido:** `tests/e2e.py` e `tests/pwa.py`. |

### Problemas encontrados, por prioridade

| # | Problema | Impacto | Esforço | Situação |
|---|---|---|---|---|
| 1 | O WhatsApp de quem organiza ficava no documento público do jogo: qualquer pessoa podia ler todos os números pela API. | Alto (privacidade) | Médio | **Corrigido:** foi para `jogos/{id}/contato`, lido só por quem entrou com conta, pelo dono e pelo time. |
| 2 | Desconhecidos entravam em jogo público só com um nome. | Alto (segurança) | Baixo | **Corrigido:** jogo público pede conta; jogo privado por link continua só com o nome. |
| 3 | O app falava em "reserva gerada" sem reservar nada. | Alto (honestidade com a banca e com o usuário) | Baixo | **Corrigido:** o texto diz que o horário é combinado com a arena e que quadra pública não tem reserva. |
| 4 | Não diferenciava quadra pública de arena. | Alto (tese do produto) | Médio | **Corrigido:** tipo de local no jogo, na lista e no filtro. |
| 5 | Dois jogos do mesmo esporte, lugar e horário dividiam a demanda. | Médio (liquidez) | Baixo | **Corrigido:** o app avisa e oferece entrar no jogo que já existe. |
| 6 | Mesma conta podia confirmar duas vezes. | Médio | Baixo | **Corrigido** na regra: uma confirmação por conta e por jogo. |
| 7 | Não era instalável e não abria sem internet. | Médio | Médio | **Corrigido:** PWA. |
| 8 | Navegação no topo, longe do polegar. | Médio | Baixo | **Corrigido:** barra inferior com ícones no celular. |
| 9 | Filtros ocupavam a primeira tela de "Jogos abertos". | Médio | Baixo | **Corrigido:** recolhidos, com resumo do que está ativo. |
| 10 | Sem página de privacidade nem regra de idade. | Médio (LGPD) | Baixo | **Corrigido em parte:** página de privacidade e segurança, 18+. Falta o que está em Limitações. |
| 11 | Check-in sem conta pode ser inflado com nomes falsos. | Médio | Alto | **Aberto:** precisa de App Check ou backend. Quem organiza consegue tirar nomes. |
| 12 | Jogos privados e confirmações ainda são legíveis por quem conhecer a API. | Médio | Alto | **Aberto:** exige trocar as escutas por consultas e contadores. |

### Produto: o usuário entende em 5 segundos?

| Pergunta | Antes | Agora |
|---|---|---|
| O que é e que problema resolve | Sim | Sim |
| Como achar gente para jogar | Sim | Sim, com atalho por esporte na capa |
| Como achar partidas | Sim, com filtros na frente | Sim, resultados primeiro |
| Como marcar e entrar | Sim | Sim |
| Local, horário e participantes | Sim | Sim, com cidade e tipo de local |
| Como achar quadras | Não | **Não, de propósito** (ver seção 5) |

## 2. PWA

| Arquivo | Para quê |
|---|---|
| `manifest.webmanifest` | Nome, cores, modo tela cheia, `start_url` e `scope` relativos (funciona em subpasta), atalhos para Marcar e Jogos abertos. |
| `icons/` | 192, 512, 512 maskable, apple-touch 180 e favicon em SVG. |
| `sw.js` | Arquivos do app: rede primeiro, cache como reserva. SDK do Firebase e fontes: cache primeiro. Dados nunca passam pelo cache. |
| `offline.html` | Página de reserva se nem o app estiver em cache. |
| `404.html` | Endereço errado volta para o início do app. |

- **Atualização controlada:** versão nova do `sw.js` só assume quando a pessoa toca em "Atualizar". Para forçar, mude `VERSAO` no `sw.js`.
- **Sem versão velha presa:** os arquivos do app vêm sempre da rede quando há internet.
- **Sem dado velho como se fosse atual:** offline, o app mostra o aviso de sem internet, não mostra jogos e bloqueia gravações.
- **Instalação:** o botão "Instalar" só aparece quando o navegador oferece a instalação. No iPhone aparece a orientação de "Adicionar à Tela de Início". Dá para dispensar.

## 3. Testes executados

| Teste | Como | Resultado |
|---|---|---|
| Fluxos de ponta a ponta (time, visitante, jogadora, jogo público) | `tests/e2e.py`, Chrome sem interface, backend simulado com as mesmas permissões das regras | Passou, sem erros de página |
| Regras simuladas: check-in sem conta em jogo público | idem | Negado, como esperado |
| Regras simuladas: ler contato antes de entrar no jogo | idem | Negado; liberado depois de entrar |
| Tela de 390 px sem rolagem lateral | captura de tela | Passou |
| SDK real do Firebase carrega e mostra a capa | idem, sem acesso à internet do Google | Passou |
| Manifest válido e ícones respondendo | `tests/pwa.py`, app servido em subpasta | Passou |
| Service worker ativo, com escopo da subpasta | idem | Passou |
| Recarregar sem internet abre o app | idem | Passou |
| Atualização: versão nova, aviso, toque e troca de cache | idem | Passou |
| Botão Instalar chama o prompt do navegador | evento simulado | Passou |
| **No ar (GitHub Pages):** manifest, ícones, service worker ativo no escopo `/mvp-sw/`, cache com app, SDK e fontes, console sem erros, jogos carregando do Firestore | navegador real | Passou |
| Regras novas publicadas no Firebase | console do Firebase | Publicadas sem erro de sintaxe |

**Não testado:** login com Google, perfil e check-in no Firebase de verdade (precisa de uma pessoa logada); instalação em aparelho Android e iPhone reais; login dentro do app instalado no iPhone, onde janelas de login costumam dar problema.

## 4. Limitações: o que depende de backend, parceiro ou validação

| Tema | Limite hoje | O que resolve |
|---|---|---|
| Reserva de quadra | O Fechou não reserva. O horário é combinado com a arena. | Integração com o sistema da arena ou acordo direto. |
| Pagamento e sinal antifuro | Não existe. | Meio de pagamento (Pix) e servidor. |
| Avisos (vaga abriu, jogo fechou) | Só com o app aberto. | Notificações push ou WhatsApp, com servidor. |
| Check-ins falsos | Possíveis em jogo privado. | Firebase App Check e limite por servidor. |
| Jogos privados | Ocultos na interface, não na API. | Consultas por visibilidade e dono, com contador no jogo. |
| Chave do Firebase | Pública por natureza. | Restringir por domínio no Google Cloud (5 minutos, recomendado). |
| LGPD | Falta canal de contato do responsável pelos dados, termos de uso e política de retenção. | Definir um e-mail do time e escrever os termos. |
| Menores de idade | O app declara 18+, mas não verifica. | Verificação de idade se o público pedir. |
| Segurança do encontro | Dicas, conta em jogo público e arena como lugar padrão. | Denúncia, bloqueio e reputação depois do jogo. |
| Dados antigos | Jogos criados antes desta versão podem ter o WhatsApp no documento público. | Apagar ou recriar esses jogos. |

## 5. O que não foi feito, e por quê

| Pedido | Decisão | Motivo |
|---|---|---|
| Diretório de quadras, mapa e distância por GPS | Não agora | Exige base de quadras verificada, que não existe. Dado errado de quadra custa mais confiança do que a falta dele. A cidade já filtra. Sem GPS, também não há consentimento de localização para gerir. |
| Favoritos e avaliações de locais | Não agora | Não ajudam a fechar jogo, que é a única coisa a provar. |
| Histórico completo | Parcial | "Marquei" e "Vou jogar" já mostram os jogos da pessoa. |
| Reescrever em framework | Não | Sem ganho para o usuário hoje e com risco alto a horas do pitch. |
| Premium com prioridade e pontos | Lista de espera | Sem volume, prioridade atrasa o preenchimento. |

## 6. Roadmap

| Quando | O quê |
|---|---|
| **Imediato (MVP)** | Fechar jogos reais pelo app; testar com pessoas reais o que está em "Não testado"; restringir a chave do Firebase por domínio; apagar jogos de teste. |
| **Curto prazo (validação regional)** | Piloto pago com 3 a 5 arenas; avisos por WhatsApp; App Check; contador no jogo e consultas por cidade; termos de uso e canal de dados. |
| **Médio prazo (monetização)** | Sinal antifuro por Pix; Plano Arena; integração com um sistema de reserva; reputação e denúncia; diretório de quadras verificado. |
| **Longo prazo (escala)** | Novas regiões com o mesmo roteiro; app nas lojas se a retenção pedir; parcerias com universidades e prefeituras como canal. |

## 7. Decisão mais importante agora

**Quem paga nos próximos 90 dias.** A recomendação é testar a taxa por jogo fechado com 3 arenas da região, antes de construir qualquer coisa nova. Se nenhuma topar, o caminho passa a ser crescer a rede em quadra pública e buscar receita em patrocínio ou parceria institucional, que é um negócio diferente, mais lento. Vale saber antes de decidir: a pesquisa mostrou que Kourt e MatchPoint já fazem partidas abertas com reserva, então o que diferencia o Fechou é chegar primeiro com jogos cheios na região, não uma funcionalidade. O detalhe está em [`ESTRATEGIA.md`](ESTRATEGIA.md).
