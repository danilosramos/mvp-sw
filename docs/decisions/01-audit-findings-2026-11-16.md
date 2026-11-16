# Auditoria completa: Energia Boa

Data: 16/11/2026. Complementa o `AUDITORIA.md` de 15/11, que foi escrito antes da marca nova e dos três níveis.

**Como foi feita.** Sete sub-agentes em duas rodadas: três de levantamento (stack, regras de negócio, design e crescimento) e quatro de avaliação (segurança com execução dos testes, regras de negócio, design com o app rodando, e crescimento com pesquisa de mercado). Todo achado de severidade crítica ou alta foi conferido de novo no código antes de entrar aqui.

**Marcação dos achados.** **E** = executado nesta máquina. **L** = lido no código ou no documento. **I** = inferência, não testada. **F** = dado externo com fonte.

**Esforço.** P = horas. M = um ou dois dias. G = uma semana ou mais, ou exige backend.

---

## 1. Resumo executivo

### Veredito

O MVP cumpre o que um fim de semana pede: o fluxo principal (marcar, convidar, confirmar, fechar) funciona, os três conjuntos de testes passam, a identidade visual é forte e o convite por link é enxuto. A stack (um arquivo estático, Firestore e login Google) é adequada para esta fase.

O que falta não é funcionalidade, é prova. O produto mostra que um jogo completou. Ainda não mostra que o jogo aconteceu, que a arena vendeu um horário que não venderia, nem que ela pagaria por isso. E as regras do banco confiam demais no aplicativo, o que expõe o WhatsApp de quem organiza.

### Os cinco riscos principais

| # | Risco | Onde | Severidade |
|---|---|---|---|
| 1 | Qualquer conta Google lista todos os jogos, inclusive os privados, cria a própria confirmação e lê o WhatsApp de quem organizou. Dá para repetir em massa. | `firestore.rules:170`, `:80-95`, `:178-179` | Alto |
| 2 | O piloto com arenas é anunciado como grátis e sem compromisso, sem dizer o preço seguinte. A hipótese "a arena paga" não está sendo testada. | `index.html:834`, `772`; `ESTRATEGIA.md:121`, `140` | Crítico para o negócio |
| 3 | O número mostrado à arena ("Receita de quadra gerada") soma o preço digitado por qualquer jogador, sem teto, em jogos sem registro de presença. Não serve de argumento nem de base de cobrança. | `index.html:473-488`; `firestore.rules:45` | Alto |
| 4 | Jogo público exige login Google por popup, e o convite é aberto quase sempre no navegador interno do WhatsApp, onde popup costuma ser bloqueado. Não foi testado em aparelho. | `firebase.js:49`; `index.html:706`, `1456-1463` | Alto |
| 5 | Nada traz o jogador de volta (sem lembrete, aviso de vaga, "marcar de novo" ou pós-jogo) e nada é medido (sem analytics, sem origem, sem presença, sem momento de fechamento). | seções 6 e 8 | Alto |

### As cinco ações de maior retorno

1. **Declarar o preço pós-piloto na oferta para arenas** e pedir aceite por escrito. Custa uma linha de texto e é o único teste real da receita.
2. **Fechar as regras do banco:** horário do servidor na fila, faixas de valor e nível, jogo privado só por link. Os trechos estão na seção 2.
3. **Tornar o jogo fechado verificável:** gravar quando fechou, marcar presença depois do horário e vincular o jogo à arena do piloto.
4. **Consertar as duas costuras do funil:** guardar o destino "Marcar jogo" depois do login, e testar o convite público dentro do WhatsApp em Android e iPhone.
5. **Trocar a data fixa dos testes por data relativa.** Eles quebram em 21/11/2026 às 18h30.

---

## 2. Stack e segurança

### Veredito

A stack serve ao MVP: não há servidor para manter e os testes passam hoje. O problema é que toda a segurança depende de `firestore.rules`, e as regras checam formato e dono, mas não data, lotação, ordem da fila nem faixas. Nada disso impede uma demonstração; os itens altos devem ser resolvidos antes de divulgar o app para mais gente.

### Retrato

- **Aplicação:** `index.html` com 1.900 linhas, CSS e JavaScript embutidos, sem framework e sem build. Rotas por fragmento (`#jogos`, `#convite-<id>`).
- **Dados:** Firestore (projeto `fechou-sw`, região `southamerica-east1`) e Firebase Auth com Google. SDK 12.19.0 carregado por CDN em `firebase.js`.
- **Hospedagem:** GitHub Pages a partir da `main`. Sem integração contínua, sem variáveis de ambiente, regras publicadas colando o texto no console.
- **PWA:** `sw.js` (versão manual, hoje `v3`), `manifest.webmanifest`, `offline.html`.
- **Papéis:** visitante, jogador logado e time (quem tem documento em `admins/{uid}`).
- **Integrações:** WhatsApp só por link `wa.me`; Tally só por link e importação manual. Pagamento, e-mail, push e mapas não existem.

### Resultado dos testes (E)

| Teste | Resultado | Observação |
|---|---|---|
| `tests/contraste.py` | Passou | 25 de 25 pares. O mais justo é branco sobre `#A925E6`, com 5,13. |
| `tests/e2e.py` | Passou | Cenários A, B, C e P. O cenário D (SDK real) não rodou: depende da variável `FIREBASE_SDK_DIR`. |
| `tests/pwa.py` | Passou | Manifest, ícones, service worker, abertura sem internet e atualização de `v3` para `v4`. |

**Data fixa.** Com o relógio do navegador adiantado para 22/11/2026, o cenário A falha (o formulário recusa o horário como passado) e o script aborta sem rodar os demais. Pela leitura do código, a quebra começa em 21/11 às 18h30 (`tests/e2e.py:48`, `123`, `188`; `tests/mock-backend.js:114`, `119`).

### Achados

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| S1 | Coleta do WhatsApp de organizadores. Qualquer conta Google lista todos os jogos, cria a própria confirmação, lê `contato/dono` e apaga a confirmação. Em jogo público isso é o fluxo previsto; o problema é valer para jogo privado sem ter o link. | `firestore.rules:170`, `:80-95`, `:178-179`, `:193` | Alto | M | Trechos 2 e 3 abaixo. Ligar o App Check. Avaliar liberar o contato só a quem tem vaga. | L |
| S2 | Fila manipulável. A ordem de quem joga e de quem espera usa `criadoEm` enviado pelo aparelho; a regra só exige que seja número. | `firestore.rules:89`; `index.html:427` | Alto | P/M | Trecho 1. | L |
| S3 | Entrar no time dá acesso a todos os perfis e à base com WhatsApp, e não tem volta pelo app: a regra proíbe apagar `admins`. O risco real é o código vazar num grupo, não a força bruta. | `firestore.rules:109-124`, `:161-167` | Alto | P | Trecho 5. Trocar o código depois de cada entrada. A médio prazo, lista de e-mails autorizados. | L |
| S4 | Os testes de ponta a ponta quebram em 21/11/2026. | ver acima | Alto | P | Gerar datas relativas a hoje, como a função `quando()` de `tests/mock-backend.js:124`. | E |
| S5 | Os testes validam um backend simulado que reescreve as permissões à mão e já diverge das regras reais. Uma regra errada pode passar em todos os testes. | `tests/mock-backend.js:35-38`, `53-57` | Alto | M | Testar `firestore.rules` no emulador do Firebase, incluindo os ataques de S1 e S2. | L |
| S6 | Regras que valem só no aplicativo: jogo no passado, confirmação em jogo encerrado, preço negativo, nível fora da faixa, valores absurdos no pedido de arena. | `firestore.rules:36-38`, `:45`, `:155-156` | Médio | P | Trecho 4. | L |
| S7 | Escrita anônima sem limite: confirmações sem conta em jogo privado e pedidos de arena. | `firestore.rules:90-94`, `:144` | Médio | P/M | App Check com reCAPTCHA. Ele dificulta scripts, mas não limita um navegador real. | L |
| S8 | O app escuta as coleções `jogos` e `confirmacoes` inteiras, inclusive o histórico. Somado ao S7, pode esgotar a cota gratuita de leituras e tirar o app do ar. | `index.html:1815-1819` | Médio | M | Consultas filtradas por data e visibilidade (necessárias também para o trecho 2). | L; esgotamento é I |
| S9 | Confirmações legíveis sem login: nome, `uid` e `jogoId` de todos. | `firestore.rules:188` | Médio | M | Trecho 3. | L |
| S10 | Chave do Firebase sem restrição de domínio (pendência já no roadmap antigo). O console não foi verificado. | `config.js:5` | Médio | P | Restringir a chave e revisar os domínios autorizados. | L |
| S11 | Endereço de produção ambíguo: o README aponta para `danilosramos.github.io/mvp-sw` e o repositório remoto é `joedio-borges/mvp-sw`. | `README.md:11` | Médio | P | Definir o endereço oficial antes de espalhar links. Trocar depois quebra convites enviados e instalações. | L |
| S12 | Sem integração contínua; os testes são quase só `print`. | ausência de `.github/` | Médio | P | GitHub Actions rodando os três scripts, com `assert` nos pontos principais. | L |
| S13 | Login por e-mail e senha exposto em `firebase.js` sem uso em nenhuma tela. | `firebase.js:8`, `50` | Baixo | P | Remover e conferir no console se o provedor está desligado. | L |
| S14 | Identificador de jogo previsível (relógio mais `Math.random`). Fica fraco quando o link virar a chave do jogo privado. | `index.html:374` | Baixo | P | Gerar com `crypto.getRandomValues`. | L |
| S15 | Sem política de segurança de conteúdo e SDK sem verificação de integridade. O escape com `esc()` é consistente e não foi encontrada injeção. | `index.html:371`; `firebase.js:3-9` | Baixo | M | Deixar para quando houver build. | L |

### Correções propostas para `firestore.rules`

Nenhum trecho foi aplicado nem executado. Devem passar pelo emulador antes de publicar.

**Trecho 1: horário do servidor na confirmação** (fecha S2).

```
// em confirmacaoPublicaValida e confirmacaoDoDonoValida, no lugar de "criadoEm is number":
&& request.resource.data.criadoEm == request.time
```

Custo: o aplicativo passa a enviar `serverTimestamp()` em vez de `Date.now()`, e precisa aceitar os dois formatos ao ler, para as confirmações antigas continuarem ordenáveis.

**Trecho 2: jogo privado só por link** (fecha a enumeração de S1).

```
match /jogos/{id} {
  allow get: if true;   // quem tem o link abre o convite
  allow list: if ehEquipe()
    || resource.data.visibilidade == 'publico'
    || (request.auth != null && resource.data.donoUid == request.auth.uid);
}
```

Custo: o Firestore só aceita a listagem se a consulta tiver o mesmo filtro. O adaptador de `firebase.js` precisa ganhar `where`; "Procurar" passa a consultar os públicos e "Meus jogos" os do dono. O convite sem conta continua funcionando. Jogos antigos sem o campo `visibilidade` somem das listas até serem atualizados.

**Trecho 3: confirmações como subcoleção do jogo** (fecha S9).

```
match /jogos/{id}/confirmacoes/{cid} {
  allow read: if true;   // só lista quem já conhece o id do jogo
  allow create: if ehEquipe() || confirmacaoPublicaValida(id, cid) || confirmacaoDoDonoValida(id);
  allow delete: if ehEquipe() || ehDonoDoJogo(id)
    || (request.auth != null && resource.data.get('uid', '') == request.auth.uid);
}
```

Custo: é a mudança mais cara. Exige migrar os documentos, trocar a escuta global por uma escuta por jogo e manter um contador de vagas no documento do jogo. Sem os trechos 2 e 3 juntos, "privado" continua significando apenas "não aparece na lista do app".

**Trecho 4: faixas e datas** (fecha a maior parte de S6).

```
// jogoDeJogadorValido
&& request.resource.data.nivel in [1, 3, 5]
&& request.resource.data.quando.matches('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$')
&& (request.resource.data.valor == null
    || (request.resource.data.valor >= 0 && request.resource.data.valor <= 5000))
&& request.resource.data.criadoEm == request.time

// arenas_piloto
&& (request.resource.data.vazios == null || (request.resource.data.vazios >= 0 && request.resource.data.vazios <= 200))
&& (request.resource.data.preco == null || (request.resource.data.preco >= 0 && request.resource.data.preco <= 5000))
```

Custo: nenhum para quem usa o app. Impedir jogo no passado e confirmação em jogo encerrado exige um campo novo de data em formato de timestamp, porque o texto `quando` não é comparável com o relógio do servidor.

**Trecho 5: sair do time** (parte de S3).

```
match /admins/{uid} {
  allow delete: if ehEquipe();
}
```

Custo: um botão "remover do time" no painel.

---

## 3. Regras de negócio

### Veredito

As regras cobrem bem o fluxo principal, mas a maior parte vale só na interface. Três consequências importam agora: o número mostrado à arena não se sustenta, não existe o estado "cancelado" nem aviso fora da tela, e os documentos se contradizem entre si e com o código.

### Matriz de consistência

| Regra | O que o documento diz | O que o aplicativo faz | O que `firestore.rules` impõe | Veredito |
|---|---|---|---|---|
| Perfil obrigatório | "sem perfil a pessoa não marca jogo" (`REQUISITOS.md:15`) | Leva ao perfil, mas "Preencher depois" libera tudo (`index.html:648`) | Criar jogo não consulta o perfil | Contradiz o documento |
| Data no passado | Não aceita horário que já passou | Bloqueia se for anterior a 30 minutos atrás (`index.html:1257`) | `quando` é só texto de até 20 caracteres | Só no aplicativo |
| Total e vagas | Total e "quantos já são" | Total de 2 a 30, sobra pelo menos 1 vaga | Total de 2 a 30, vagas de 1 até o total | Coerente |
| Faixa de nível | Três níveis guardados como 1, 3 e 5; `ARQUITETURA.md:60` diz 1 a 5 | Só gera 1, 3 ou 5 | `nivel is number`, sem faixa | Só no aplicativo |
| Preço | Opcional; quadra pública não tem preço | Maior ou igual a zero, ou vazio | Número ou nulo, sem mínimo nem teto | Só no aplicativo |
| Jogo público exige conta | R8 exige; R3 e o README ainda dizem "sem conta" | Pede login Google (`index.html:1456`) | Exige `uid` em jogo público | Coerente; documentos desatualizados |
| Uma confirmação por conta | Não está escrito | Com conta, identificador fixo; sem conta, aleatório | Em jogo privado, sem `uid`, cria quantas quiser | Parcial |
| Lotação e lista de espera | Só em `ARQUITETURA.md:117` | As primeiras confirmações jogam, as demais esperam (`index.html:427-431`) | Sem limite por jogo | Só no aplicativo |
| Ordem da fila | "na ordem da lista" | Ordena por `criadoEm` | `criadoEm is number`, vindo do aparelho | Só no aplicativo, e manipulável |
| Jogo que já passou | Não está escrito | "Passou" começa 2 horas depois do início (`index.html:440`) | Nada | Só no aplicativo |
| Contato de quem organiza | R9: só quem entrou com conta; `REQUISITOS.md:61` diz "quem tem o link" | Mostra a quem confirmou com conta, inclusive na lista de espera | Time, dono ou quem tem a confirmação | Coerente com R9 |
| Editar e apagar jogo | Pode apagar; edição não é citada | O dono só apaga | Atualizar só o time; apagar time ou dono | Coerente, mas o dono não corrige nada |
| Jogo parecido | Mesmo esporte, lugar e até 1 hora | Avisa uma vez; o segundo toque grava | Não se aplica | Coerente |
| Jogo de teste | Fica fora dos números | Só o time marca | Jogador só cria com `teste == false` | Coerente |
| Entrada no time | Código do time | Aceita a partir de 4 caracteres; o código tem 6 (`index.html:889`) | Código igual ao guardado; sem saída | Coerente; sem saída |
| Pedido de arena | Não existe requisito escrito | Valida os campos e limita horários vazios a 200 | Qualquer um cria; sem faixas | Regra sem documento |

### O número mostrado à arena

`metricas()` (`index.html:473-488`) soma o `valor` de todo jogo em arena que não é de teste e está fechado neste instante. Cinco fragilidades:

1. O preço é digitado por quem marca, sem teto. Uma conta qualquer cria um jogo privado de 2 pessoas com valor de um milhão, confirma um nome sem conta e infla o painel (I: lido nas regras, não executado).
2. Fechar não é acontecer. Não há presença, e jogos passados contam para sempre.
3. O número oscila: se alguém desiste, a receita some. Não existe registro de quando o jogo fechou.
4. A reserva não é confirmada pela arena.
5. Em "grupo incompleto" a quadra possivelmente já estava reservada; o valor cheio só é receita nova se o grupo fosse de fato cancelar.

Até haver presença e preço confirmado, o rótulo honesto é "valor de quadra dos jogos que completaram (informado por quem marcou)".

### Achados

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| N1 | "Receita de quadra gerada" pode ser inflada e não distingue jogo fechado de jogo realizado. | `index.html:473-488`; `firestore.rules:45` | Alto | M | Teto de valor na regra, registro de fechamento, marcação "aconteceu", preço confirmado pelo time. Renomear o indicador até lá. | I |
| N2 | Apagar o jogo é o único cancelamento e ninguém é avisado. Quem confirmou vê "Convite não encontrado". | `index.html:1516`; `firestore.rules:173` | Alto | M | Estado "cancelado" em vez de exclusão, com o convite visível e mensagem pronta para avisar o grupo. | L |
| N3 | Lista de espera sem aviso: a promoção só aparece com a tela aberta. | `index.html:1489` | Alto | M | Botão "avisar o próximo da fila" para quem organiza, com mensagem pronta. | L |
| N4 | Quem marcou não corrige hora, local, total nem preço: precisa apagar e recriar, perdendo as confirmações. | `firestore.rules:172` | Médio | M | Permitir ao dono atualizar um conjunto restrito de campos. | L |
| N5 | Quem entrou sem conta não consegue desistir, e ao trocar de aparelho pode confirmar de novo e ocupar duas vagas. | `index.html:1472`, `1497` | Médio | M | Oferecer "entrar com Google para poder desistir" depois da confirmação. | L; duplicidade é I |
| N6 | O jogo aceita confirmação até 2 horas depois de começar. | `index.html:440` | Médio | P | Encerrar a confirmação no horário de início; manter as 2 horas só para o histórico. | L |
| N7 | Um único nível vale para todos os esportes do perfil. | `index.html:461-465` | Médio | M | Nível por esporte, ou tratar os demais esportes como "quase". | L |
| N8 | Perfil pode ser pulado; quem pula marca jogo como intermediário por padrão. | `index.html:648`, `1285` | Médio | P | Decidir a regra e alinhar o documento. Se for opcional, exigir o nível ao marcar. | L |
| N9 | Dois cortes de período: o filtro corta às 18h; "Quem combina" corta entre 17h e 19h. | `index.html:456`, `416-425` | Baixo | P | Uma única função para as duas telas. | L |
| N10 | Jogadores importados do formulário não têm cidade e passam em qualquer filtro; a mesma pessoa pode aparecer duas vezes (formulário e perfil). | `index.html:491-501` | Baixo | P | Importar a cidade e deduplicar por WhatsApp. | L |
| N11 | A lista de espera também recebe o WhatsApp de quem organiza. | `firestore.rules:179` | Baixo | P | Aceitar como decisão e registrar, ou restringir a quem tem vaga. | L |
| N12 | Nada impede a mesma conta de confirmar em dois jogos no mesmo horário. | `index.html:1468-1481` | Baixo | P | Avisar na confirmação. | L |

### Documentos a corrigir

- **`REQUISITOS.md`:** linha 15 (perfil obrigatório), 28 (confirmação sem conta vale só para jogo privado), 30 e 51 ("Reserva gerada"), 35 ("botão amarelo"), 61 (contato para quem tem o link). Acrescentar o que só existe no código: pedido de piloto, lista de espera e desistência.
- **`README.md`:** linha 9 ("sem conta" como regra geral e "Reserva gerada: R$ X") e linha 11 (endereço do app).
- **`ARQUITETURA.md`:** linha 60 (`nivel 1..5`), 47 ("Reserva gerada"), 37 e 123 ("Bora jogar"), 158 ("Google Fonts").
- **`firestore.rules`:** linha 3 ("Regras do Fechou").
- **`AUDITORIA.md`:** linha 22 dá "reserva gerada" como corrigida, mas o texto continua nos três documentos acima.

---

## 4. Design, experiência de uso e acessibilidade

Avaliado com o app rodando sobre o backend simulado, em 31 capturas a 390×844 e duas a 1280 de largura. Não foi testado em aparelho real, no navegador do WhatsApp nem com leitor de tela.

### Veredito

Identidade forte, primeira dobra clara e convite privado enxuto. Nenhum achado é crítico. Os problemas estão nas costuras do fluxo e em acessibilidade de navegação; o contraste é bom. A dívida do design system é real, mas quase toda pode esperar.

### O que funciona bem

- A landing responde "o que é" e "o que faço" na primeira dobra, e o primeiro jogo com vaga aparece logo abaixo.
- O convite privado cabe em uma tela: data, local, preço por pessoa, vagas, quem já confirmou e o botão "Tô dentro".
- O cartão de jogo é lido de relance no celular e no desktop.
- Os estados vazios falam como gente e, na maioria, apontam o próximo passo.
- Os 25 pares de cor passam, o foco é visível e a redução de movimento é respeitada.

### Achados

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| D1 | Jogo público exige login por popup dentro do navegador do WhatsApp. O app já tem mensagem pedindo para abrir no Chrome ou Safari. | `firebase.js:49`; `index.html:706` | Alto | M | Testar em aparelho. Se falhar, detectar o navegador interno e oferecer "Abrir no navegador" antes do login, ou usar login por redirecionamento. | L + I |
| D2 | A intenção de "Marcar jogo" se perde no primeiro acesso: depois do login e do perfil a pessoa cai em "Meus jogos". | `index.html:648`, `964` | Alto | P | Guardar `#novo` como destino ao tocar em "Marcar jogo". | E (visto na tela) |
| D3 | Nos formulários de perfil e de marcar jogo, o erro aparece numa faixa única no fim, a mais de uma tela do campo errado, sem destaque nem foco. | `index.html:946`, `1254` | Alto | M | Erro junto do campo, foco no primeiro inválido, `aria-invalid`. O convite já faz certo. | E |
| D4 | A tela de jogo lotado se contradiz: o topo diz "Falta gente nesse jogo", o placar diz "Fechou!" com confete para quem ficou de fora, e "1 de 1 vagas" tem erro de concordância. | `index.html:586`, `1523` | Médio | P | Topo "Esse jogo já fechou", confete só para quem está no jogo, corrigir o singular. | E |
| D5 | A troca de tela não é anunciada: o título da aba é sempre "Energia Boa" e o foco volta ao corpo da página. | `index.html:656` | Médio | P | A cada rota, definir `document.title` e mover o foco para o título da tela. | E |
| D6 | O diálogo de cópia manual não fecha com Esc e não prende o foco. | `index.html:297-304` | Médio | P | Trocar por `<dialog>` nativo com `showModal()`. | E |
| D7 | Mensagens técnicas chegam ao usuário: instruções do console do Firebase, código de erro cru, nome de coleção, "o arquivo que o Claude gerou". | `index.html:704-708`, `539`, `1811`, `1607` | Médio | P | Mostrar "Não deu para entrar agora. Tente de novo." e mandar o detalhe para o console. | L |
| D8 | Na tela de quem organiza, "Enviar no WhatsApp" fica cerca de duas telas abaixo do placar. É a ação que faz o produto funcionar. | `index.html:1318-1323`, `1397` | Médio | P | Subir o botão para logo abaixo do placar enquanto o jogo não fechou. | E |
| D9 | O perfil no primeiro acesso é longo (cinco campos obrigatórios e uma chamada do Premium no meio) e a saída "Preencher depois" é um link de 19 px. | `index.html:919-969` | Médio | M | Pedir só cidade, esporte e nível; o resto depois do primeiro jogo. Tirar o Premium dessa tela. | E |
| D10 | Em "Procurar", os filtros ocupam quase toda a primeira dobra no celular. | captura `02-procurar-com-resultado.png` | Médio | M | Deixar só Esporte visível e recolher dia e período. | E |
| D11 | Nomes diferentes para a mesma coisa: "Procurar jogos" e "Jogos abertos"; "Marcar jogo", "Marcar meu jogo" e "Marcar o meu jogo"; "check-in" ao lado de "Tô dentro". | `index.html:915`, `1203`, `1502` | Médio | P | Um termo por conceito. | E |
| D12 | Na barra inferior, "Procurar" tem sempre a pílula limão, mesmo quando a tela atual é outra. | `index.html:669-685` | Médio | P | Reservar a pílula para a tela atual. | E |
| D13 | Um par de contraste fora do teste falha: branco a 85% sobre roxo, 4,06:1 em 13 px. | `index.html:254` | Médio | P | Branco cheio (5,13:1) e incluir o par em `tests/contraste.py`. | L |
| D14 | Alvos de toque abaixo de 44 px: links de texto com 18 a 26 px, "Voltar" com 24 px, botões pequenos com 40 px ("Tirar", "Apagar jogo"). | `index.html:118`, `124`, `235` | Médio | P | Altura mínima de 44 px. Prioridade para os destrutivos. | E |
| D15 | Menores: "Entrar" leva à landing e não a um login; o painel não tem título principal; sem `<noscript>`; falta `viewport-fit=cover`; o aviso temporário some em 2,8 s. | `index.html:5`, `569`, `639-650` | Baixo | P | Corrigir em uma passada. | L + E |

### Design system

- **Vale consertar agora:** unificar as quatro implementações de chip em uma com 44 px de altura; aplicar o token `--toque` nos botões pequenos e links; corrigir o par de contraste.
- **Pode esperar:** os seis tokens de espaçamento sem uso, os 17 tamanhos de fonte (basta atualizar `DESIGN.md` para a escala real), `.btn.ghost` sem regra própria, `offline.html` duplicando cores, tema claro.

---

## 5. Captação

### Veredito

O canal certo foi escolhido: link do jogo no WhatsApp, sem instalar nada. Mas é onde o funil mais vaza, e nenhum vazamento pode ser medido hoje. Busca orgânica é secundária nesta fase.

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| C1 | Login por popup no convite público (o mesmo de D1). | — | Alto | M | Ver D1. | L + I |
| C2 | O convidado sem conta em jogo privado deixa só o nome. A pessoa mais qualificada do funil não vira contato. | `index.html:1466-1467` | Alto | P | Depois do "Tô dentro", campo opcional de WhatsApp com consentimento. Exige ajuste em `firestore.rules:81`. | L |
| C3 | Sem analytics e sem registro de origem. Não se sabe quantos abrem o convite, quantos confirmam, nem de onde vieram. | `firebase.js:3-9` | Alto | P | Parâmetro de origem no link, gravado na confirmação e no perfil. Contador de páginas sem cookies, com a tela de privacidade atualizada. | L |
| C4 | A página de arenas capta o pedido, mas não diz o que acontece depois nem quanto custará. | `index.html:827-838` | Alto | P | Ver seção 7. | L |
| C5 | A prévia do link no WhatsApp é igual para todos os jogos e não tem imagem. | `index.html:15-16` | Médio | P | Adicionar `og:image` da marca, `og:url` e `og:type`. Prévia por jogo exige servidor. | L |
| C6 | Só quem organiza compartilha; o convidado que acabou de confirmar não tem botão. | `index.html:1524` | Médio | P | "Chamar mais gente" na tela de confirmado, com as vagas restantes no texto. | L |
| C7 | A prova social diz "28 de 36 jogadores", mas a base são respostas, não pessoas. | `index.html:803-806`; `ESTRATEGIA.md:14-17` | Médio | P | Escrever "28 de 36 respostas" e manter a ressalva visível para arenas. | L |
| C8 | Sem `canonical`, `robots.txt`, `sitemap.xml`; rotas por fragmento não são indexáveis. | `index.html:13-16` | Baixo | P | Só o básico. Não é o canal desta fase. | L |

**Força da evidência da pesquisa.** Ela sustenta "a dor existe entre quem já joga e respondeu", e só isso. A amostra é pequena e autoselecionada, as perguntas diferem entre os três canais, três pessoas foram retiradas do denominador e o total soma envios. Ela não mede se desconhecidos comparecem, se o jogador volta nem se a arena paga. Serve como motivo para testar, não como dado de mercado.

---

## 6. Ativação e fidelização

### Veredito

O caminho até a primeira ação é curto para quem entra por convite privado, mas perde quem quer marcar jogo. Depois do primeiro jogo, nada traz a pessoa de volta: a retenção depende de quem organiza e do time mandando mensagem à mão. Boa parte se resolve sem backend.

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| F1 | Intenção perdida depois do primeiro login (o mesmo de D2). | `index.html:648`, `964` | Alto | P | Ver D2. | E |
| F2 | Sem lembrete antes do jogo nem "adicionar ao calendário". | ausência no código | Alto | P | Botão que gera arquivo `.ics` e link do Google Agenda na tela "Você está no jogo". | L |
| F3 | Sem recorrência nem "marcar de novo". Jogo semanal é o padrão de uso na pesquisa. | `ESTRATEGIA.md:20` | Alto | P | "Marcar de novo na próxima semana", duplicando o jogo e oferecendo reenviar o convite. | L |
| F4 | Sem pós-jogo: presença, "rolou?", reputação. A hipótese "desconhecidos aparecem" não pode ser validada. | `index.html:1501-1502` | Alto | M | Depois do horário, quem organiza marca quem foi. Exige regra nova. | L |
| F5 | Lista de espera só avisa com a tela aberta (o mesmo de N3). | `index.html:1489` | Alto | M | Ver N3. | L |
| F6 | O cruzamento por nível e horário só aparece para o time; o jogador não recebe sugestão. | `index.html:1309-1313` | Médio | M | Usar a mesma função para ordenar "Tem vaga agora" pelo perfil de quem está logado. | L |
| F7 | "Meus jogos" mistura passados e futuros. | `index.html:900-916` | Baixo | P | Separar "Próximos" e "Já joguei". | L |
| F8 | "Agora não" na faixa de instalação vale para sempre. | `index.html:1700` | Baixo | P | Oferecer de novo depois da primeira confirmação. | L |
| F9 | Push, e-mail e WhatsApp automático não existem. | `sw.js` | Médio | G | Adiar até o piloto mostrar que os lembretes manuais funcionam. | L |

**Ordem sugerida sem backend:** destino pós-login, calendário, "marcar de novo", compartilhar pelo convidado, presença pós-jogo.

---

## 7. Monetização

### Veredito

Não há nada implementado, e isso está certo para a fase. A tese "a arena paga por jogo fechado em horário ocioso" é coerente e o percentual está dentro do que o mercado cobra. O problema é que o produto não a testa: o piloto é grátis e sem preço posterior, e o único item de preço que o usuário vê é o Premium do jogador, que a estratégia põe em último lugar.

### Comparação de mercado (F)

| Empresa | Quem paga | Valores publicados | Fonte |
|---|---|---|---|
| Arena App | Arena | Grátis com 5% de comissão por reserva paga, ou R$ 259,90 por mês sem comissão | https://arenaapp.app.br/ |
| Atacante | Arena | R$ 199 por mês até 3 quadras; R$ 399 a partir de 4 | https://atacante.app/ |
| Zap Quadra | Arena | A partir de R$ 99,90 por mês | https://zapquadra.com/ |
| Arena Online | Arena | R$ 197 por mês até 3 quadras; planos de R$ 297 e R$ 397 | https://arenaonline.app.br/ |
| BoraGame | Arena | R$ 299,90 por mês | https://boragame.app/funcionalidades/reservas |
| DUPLA | Arena | R$ 559 por mês; R$ 419 no anual | https://site.appdupla.com/ |
| Playtomic | Clube e jogador | Assinatura do jogador na loja brasileira: R$ 50,90 por mês ou R$ 299 por ano (lido no resumo da busca, página não aberta). Comissão do clube não encontrada. | https://apps.apple.com/br/app/id1242321076 |

**Preço da hora de quadra de areia:** R$ 82 a R$ 91 em Porto Alegre (https://www.pucrs.br/parqueesportivo/locacao-esportiva/valores-espacos-equipamentos/); R$ 110 avulsa e R$ 87,50 em plano mensal em Joinville (https://arenasilvas.com.br/); R$ 70 a R$ 220 nas arenas de futevôlei listadas em https://www.minhaquadra.com.br/esportes/futevolei/.

**Não encontrado:** preço de Criciúma ou Araranguá; qualquer dado público de ociosidade de quadras; fonte para "Playtomic cobra 4% mais mensalidade" (a página citada em `ESTRATEGIA.md:155` hoje não menciona o Playtomic).

### Premissas de `ESTRATEGIA.md:96-112`

| Premissa | Avaliação |
|---|---|
| Hora a R$ 100 | Sustenta-se como ordem de grandeza. Fora do pico, que é o horário ocioso, o preço tende a ser menor (estimativa). Medir o preço real do horário vazio. |
| Taxa de 10% ou R$ 10 por jogo | Plausível: acima dos 5% de quem só processa a reserva. Frágil no valor absoluto: R$ 10 não paga o trabalho de fechar um jogo à mão. |
| Plano Arena a R$ 149 por mês | Frágil. Fica na faixa dos sistemas completos de gestão (R$ 99,90 a R$ 199), que entregam reserva, pagamento e financeiro. |
| 15, 30 e 50 jogos fechados por arena por mês | A mais frágil. Trinta por mês é um por dia, por arena, só em horário ocioso. Não há nenhum jogo real para calibrar. |
| Cenário conservador com resultado de R$ 549 | Enganoso: não inclui a pessoa de operação, e o modelo é manual. |
| Ordem das receitas | Coerente. O sinal por Pix ataca o furo que os jogadores relatam, mas depende de pagamento. |

### Achados

| # | Achado | Evidência | Sev. | Esf. | Recomendação | Base |
|---|---|---|---|---|---|---|
| M1 | O piloto é grátis e sem compromisso; a estratégia prevê piloto com taxa. A hipótese "a arena paga" não é testada. | `index.html:834`, `772`; `ESTRATEGIA.md:121`, `140` | Crítico | P | Manter os 30 dias grátis, declarar o preço seguinte na oferta e pedir aceite por escrito. O critério já existe: menos de 2 "sim" em 10 derruba a hipótese. | L |
| M2 | "Jogo fechado" não é auditável: calculado no aparelho, aceita confirmação anônima sem limite, sem presença. | `index.html:427-431`; `firestore.rules:89` | Alto | M | Definir o evento faturável: jogo que aconteceu, em horário que a arena declarou vazio, com presença marcada. | L |
| M3 | O jogo não tem vínculo com a arena do piloto: "arena" é texto livre. Não dá para somar por arena parceira. | `index.html:1284-1292` | Alto | M | Identificador da arena parceira gravado no jogo, com os horários declarados vazios. | L |
| M4 | A tela do Premium promete prioridade de 15 minutos e pontos num ranking que não existe, e "avisamos quando abrir" sem canal de aviso. | `index.html:1099-1101` | Médio | P | Trocar a promessa por uma pergunta, ou tirar a tela do menu até a hipótese da arena estar testada. | L |
| M5 | O formulário de arena pergunta o modelo preferido, mas não o valor que a arena aceitaria. | `index.html:749-797` | Médio | P | Perguntar o valor na conversa do piloto e registrar. | L |

**O que o piloto com 3 a 5 arenas precisa medir:** o preço real do horário ocioso; quantos horários vazios são declarados e quantos preenchidos; presença; horas do time por jogo fechado; quantas arenas aceitam por escrito o preço seguinte; quantos jogadores fazem o segundo jogo em 14 dias.

---

## 8. Métricas

### Veredito

A estratégia define bem o que importa; o código mede quase nada disso de forma confiável. Três características destroem o histórico: desistir apaga a confirmação, apagar o jogo apaga tudo, e as datas vêm do relógio do aparelho.

| Métrica da estratégia | O que o código permite hoje | Lacuna |
|---|---|---|
| Jogos fechados por semana (a principal) | Total acumulado no painel | Sem recorte semanal; sem momento de fechamento; jogo apagado some |
| Taxa de preenchimento | O painel mostra percentual de vagas, que é outra métrica | Calcular por jogo |
| Tempo até fechar | Derivável das datas das confirmações | As datas vêm do aparelho, e a desistência apaga registros |
| Segundo jogo em 14 dias | Só para quem confirmou com conta | Convidado sem conta só tem o nome |
| Comparecimento | Nada | Sem registro de presença |
| Jogos em horário ocioso por arena | Nada | Arena é texto livre |
| Origem e conversão do convite | Nada | Sem analytics e sem origem |

**Instrumentação mínima para o piloto, em ordem:** hora do servidor nas datas; estado em vez de exclusão; momento de fechamento; presença; identificador da arena no jogo; origem no link; recorte semanal no painel.

---

## 9. Roadmap priorizado

### Agora (antes de sábado e de divulgar para mais gente)

| Ação | Achados | Esforço |
|---|---|---|
| Datas relativas nos testes | S4 | P |
| Guardar o destino "Marcar jogo" depois do login | D2, F1 | P |
| Testar o convite público dentro do WhatsApp, em Android e iPhone | D1, C1 | P |
| Faixas de valor, nível e pedido de arena nas regras; horário do servidor na fila | S2, S6, N1 | P/M |
| Permitir remover alguém do time e exigir 6 caracteres no código | S3 | P |
| Definir o endereço oficial e restringir a chave do Firebase | S10, S11 | P |
| Passada de texto e tela: mensagens técnicas, tela de jogo lotado, um termo por conceito, par de contraste, alvos de toque | D4, D7, D11, D13, D14 | P |
| Corrigir os documentos desatualizados | seção 3 | P |

### Para o piloto com arenas

| Ação | Achados | Esforço |
|---|---|---|
| Declarar o preço pós-piloto e pedir aceite por escrito | M1, C4 | P |
| Tornar o jogo fechado verificável: momento de fechamento, presença, identificador da arena | N1, M2, M3, F4 | M |
| Jogo privado só por link e confirmações em subcoleção, com consultas filtradas | S1, S8, S9 | M/G |
| Estado "cancelado" e "desistiu" em vez de exclusão | N2 | M |
| Origem no link e contador de aberturas | C3 | P |
| Calendário, "marcar de novo", compartilhar pelo convidado, contato opcional do convidado | F2, F3, C6, C2 | P cada |
| Testes das regras no emulador e integração contínua | S5, S12 | M |
| Erro junto do campo nos formulários; perfil mais curto | D3, D9 | M |
| Rever a tela do Premium | M4 | P |
| App Check | S7 | P/M |

### Depois

- Aviso de vaga e lembrete automáticos (push ou WhatsApp por servidor).
- Sinal por Pix contra furo.
- Prévia do link por jogo.
- Build, política de segurança de conteúdo e limpeza do design system.
- Nível por esporte e sugestão de jogos para o jogador.

---

## 10. Limites desta auditoria

- **Nada foi executado contra o Firebase real.** As falhas de regra foram confirmadas por leitura de `firestore.rules`. O estado do console (provedores de login, restrição da chave, domínios autorizados) não foi verificado.
- **Os trechos de regra propostos não foram executados.**
- **Nenhum aparelho real.** O login dentro do WhatsApp, o iPhone com o app instalado e leitor de tela não foram testados. O achado D1 é uma inferência forte, não uma medição.
- **O cenário D dos testes (SDK real) não rodou.**
- **Pesquisa de mercado:** só preços publicados em sites. Um valor (Playtomic) veio do resumo de uma busca, sem abrir a página. Não foi encontrado preço local nem dado de ociosidade.
- **Nada foi alterado no projeto** além deste arquivo. As capturas de tela ficaram em um diretório temporário da sessão e podem ser apagadas.
