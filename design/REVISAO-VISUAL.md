# Revisão visual do site — briefing (2026-11-24)

**Por que existe.** Ao ver a landing do LottoExpert montada (WP-10, fatia 9) o usuário disse: "achei
que tá ficando meio sem graça, queria uma página linda" e, sobre a Home, "também está sem graça.
Acho que vale rever todas com o Claude Code". Este briefing para o avanço das fatias 7, 8, 9 e 10b
do WP-10 até a direção visual ser revista e aprovada.

O que **não** está em questão: a estrutura técnica entregue (Astro, Tailwind 4, tokens, template de
landing, i18n pt/en, legais, verificações). O problema é de expressão visual, não de arquitetura.

Capturas de referência (1280 e 390 px, `dist/` da branch `feat/wp-10-fatia-9-lottoexpert`):
`/tmp/claude-1000/-home-gustavo-hyppolito-GIT-codes-ghf-software/9d25ad29-bea8-45c6-ab42-b73c8deae001/scratchpad/shots/`
(temporárias; regenerar com Chrome headless sobre `python3 -m http.server 8080 -d dist`).

---

## 1. Diagnóstico

### 1.1 O que se repete em todas as páginas
1. **Monocromia.** Fundo `#0B1120` e superfícies quase iguais em tudo. O acento de cada app
   aparece só em botão, etiqueta e um título pequeno. Nada na página diz "este é o app violeta / o
   app dourado" à primeira vista.
2. **Ritmo plano.** As seções se separam por uma linha fina e têm o mesmo fundo, o mesmo tamanho de
   título e o mesmo espaçamento. A página vira uma lista longa, sem momentos de destaque.
3. **Capturas cruas.** O print do app entra solto, com barra de status e cantos retos, sem moldura,
   sombra ou contexto. Ao lado de texto pequeno, parece documentação, não vitrine.
4. **Tipografia sem contraste de escala.** O h1 é grande, mas h2, h3 e corpo ficam próximos entre si.
   Faltam números grandes, citações, destaques — os pontos onde o olho pousa.
5. **Pouco movimento e profundidade.** Sem gradiente, brilho, sombra ou transição. Correto e sóbrio,
   mas sem emoção.

### 1.2 Home (`/`)
- O hero "Construímos o futuro da Mobilidade e IoT" (D30) é genérico e não conversa com o visitante,
  que chega procurando um app (`BRIEF.md` §3). Copy é do usuário (D25).
- Os 4 cards de app são pequenos, de mesmo peso, com ícone de 28 px, e sem nenhuma tela dos apps.
  É o único lugar do site que mostra o portfólio, e ele cabe numa faixa de 120 px de altura.
- "Sobre" é um parágrafo em primeira pessoa institucional; "Privacidade" é só uma fila de 4 links.
- A página acaba na primeira dobra: não há nada que convide a ficar ou a descer.

### 1.3 Landings (template da fatia 5: EclipseGo e LottoExpert)
- O EclipseGo é a melhor página porque tem uma foto forte no hero. Fora o hero, sofre de tudo do 1.1.
- Destaque sem imagem (scanner e prestação de contas no LottoExpert) deixa metade da largura vazia.
- "Como o app trabalha" (3 fatos) é um bloco de texto pequeno, sem ícone nem número.
- Planos do LottoExpert: 3 cards corretos, mas a tabela de 20 linhas domina o fim da página.
- O CTA final repete o botão do hero sem nenhum apelo visual.
- TopoWalk e Pole Position ainda estão no visual antigo (fatias 7 e 8 não feitas), então o site
  hoje mistura dois sistemas.

### 1.4 Legais
Não revistas aqui; o leitor de política quer legibilidade e o `LegalLayout` já resolve isso.
Entram só se a revisão mudar tokens globais (cor, fonte).

---

## 2. O que é "página linda" aqui (critérios de aceite propostos)

1. **Identidade por app em 1 segundo.** O acento do app tinge o hero (gradiente, brilho ou fundo)
   e reaparece em pelo menos dois outros momentos da página.
2. **Capturas como vitrine.** Toda captura real aparece numa moldura de aparelho desenhada em CSS,
   com sombra/brilho do acento. O conteúdo da captura não muda (D26).
3. **Ritmo.** Seções alternam fundo (base, superfície, faixa tingida). Pelo menos um "momento" por
   página: número grande, faixa de destaque ou grade de telas.
4. **Hero com impacto** em 1280×720 e em 390 px: título, uma linha de valor, CTA e imagem fortes,
   sem depender de rolar.
~~5. **Home como vitrine dos 4 apps:** cada app com tela, cor e frase; o visitante escolhe pelo olhar.~~
   **Corrigido pelo usuário (2026-11-24, D33 (c)):** a Home apresenta a GHF Software como estúdio de
   engenharia desde 2004, com as áreas de domínio. O h1 não fala dos apps, e eles entram numa seção
   de produtos/portfólio. A página não cita nome de repositório interno ou privado.
6. **Movimento sutil** (aparecer ao rolar, hover), desligado com `prefers-reduced-motion`.
7. **Sem perder o que já está provado:** Lighthouse mobile ≥ 95 em desempenho e 100 em a11y, LCP
   < 2,5 s, contraste AA, sem terceiros, espelho pt/en, URLs contratuais intactas.

---

## 3. O que continua valendo (não negociável sem decisão nova)

- URLs contratuais e o convite do bolão (ADR-001, D13): fora desta revisão.
- Jogo responsável no LottoExpert (`check_site.py` §5): nenhuma promessa de ganho, nem em imagem.
- Copy com origem (D25): a revisão mexe em forma, não inventa frase. Frase nova vem do usuário.
- Captura real do app (D26): nada de tela inventada. Moldura em CSS ao redor da captura real é
  apresentação — **precisa de aceite do usuário** (pergunta 2).
- Sem fonte, script ou imagem de terceiros no `<head>` (ADR-006 §5); Inter servida pelo site.
- Tokens em `src/styles/tokens.css` (ADR-008); o acento por app continua via `data-app`.
- Orçamentos de Lighthouse (`tools/orcamento-lighthouse.json`): aumento só com autorização.

---

## 4. Perguntas ao usuário (recomendação primeiro)

1. **Quem desenha.** (a) **Recomendado, como você pediu:** o Claude Code (agente `site-ux` com o
   `site-dev`) propõe a direção visual em código, numa branch de protótipo, e você aprova no
   navegador, página a página. (b) Rodada 4 no Claude Design, com este briefing, e o código segue o
   export (caminho da D4). A (a) emenda a D4: o export do Claude Design deixa de ser a única origem
   do visual.
2. **Moldura de aparelho em CSS** ao redor das capturas reais. Recomendado: sim (emenda pequena na D26).
3. **Hero da Home.** Trocar "Construímos o futuro da Mobilidade e IoT" por uma frase que apresente os
   apps (você escreve ou escolhe entre opções tiradas das fichas da Play). Recomendado: trocar.
4. **Liberdade por app.** Manter um template único com variações de cor e imagem (recomendado: mais
   barato e coerente) ou permitir hero e seções próprias por app.
5. **Tabela de planos do LottoExpert.** Mostrar 6–8 linhas principais e "ver tabela completa".
   Recomendado: sim.
6. **Movimento.** Animações sutis ao rolar. Recomendado: sim, com `prefers-reduced-motion`.

---

## 5. Plano proposto

1. Você responde a seção 4. Decisões viram `/decisao` (emendas de D4, D26, D30).
2. `/novo-wp` "revisão visual": um WP próprio, que pausa as fatias 7, 8, 9 e 10b do WP-10.
3. **Protótipo:** `site-ux` define a direção (paleta ampliada, escala tipográfica, moldura, ritmo de
   seções) e o `site-dev` aplica na **Home** e na **landing do LottoExpert** primeiro. Você olha em
   `localhost:8080` e aprova ou pede ajuste.
4. **Propagação:** a direção aprovada vai para o template (EclipseGo junto), depois retomam as fatias
   7 (TopoWalk), 8 (Pole Position) e 9 (LottoExpert, com as capturas que faltam) e a 10b.
5. **Prazo:** o deploy único é para antes do fim de 2026 e agora espera também a 2.06.00 na Play.
   A revisão cabe se o protótipo for aprovado em até ~1 semana; senão o prazo precisa ser revisto.

Em paralelo, e independente do visual: um WP de **conteúdo para SEO** (páginas como "Fechamento da
Lotofácil: como funciona" e "Como organizar um bolão"), que é o que de fato traz busca nova. A
beleza ajuda a converter quem chega; o conteúdo traz quem ainda não conhece.

---

## 6. Respostas do usuário (2026-11-24, todas pela recomendada)

1. **Quem desenha:** o Claude Code, em protótipo numa branch, com aprovação do usuário no navegador.
   Emenda a D4.
2. **Moldura de aparelho em CSS** ao redor das capturas reais: sim. Emenda a D26.
3. **Hero da Home:** trocar; o agente traz opções montadas só com frases que já têm origem, e o
   usuário escolhe ou reescreve. Emenda a D30 (1).
4. **Template único com variações por app** (cor, imagens, destaques). Mantém a D29.
5. **Tabela de planos do LottoExpert:** 6 a 8 linhas principais e "ver tabela completa" recolhida.
6. **Movimento sutil:** sim, sem biblioteca externa, desligado com `prefers-reduced-motion`.
7. **Prazo:** a revisão entra **antes** do deploy único. As fatias 7, 8, 9 e 10b do WP-10 pausam até
   o protótipo da Home e do LottoExpert ser aprovado; se passar de ~1 semana, revê-se o prazo.
8. **SEO:** WP separado de conteúdo, sem bloquear a revisão.
