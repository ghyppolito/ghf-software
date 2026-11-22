# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-22.** WP-25 `done` (#47; CI do #37 verde no Node 22.23.5). Fatia 2 do WP-10 feita em `feat/wp-10-fatia-2` (criada de `origin/feat/wp-08-layout-unico`, 79e6703).

## 1. Onde parei

- WP-25 `done` (#47 integrado). Fatia 2 do WP-10 (casca) feita em 2026-11-22 na branch `feat/wp-10-fatia-2` (8999f11, 872c0ef, 0ee743c; não enviada); auditorias sem achado alto. WP-10 segue `doing`.
- Próxima: **fatia 3 (legal)**, `risco: alto` (5 URLs contratuais), passa pelo `site-legal`. Prova: `sync_legal.py --todos --check` mais o texto do corpo em `dist/` igual antes e depois.
- Usuário: abrir e mesclar um PR `feat/wp-10-fatia-2` -> `feat/wp-08-layout-unico`, como o #46 e o #47, e conferir o CI do #37. O #37 segue sem merge até o deploy único.
- O merge local é barrado pela permissão desta sessão: o agente abre o PR e o usuário mescla no GitHub.

## 2. Quebrado ou pela metade agora

Nada quebrado. Passaram no `/verify` da fatia 2: `test:css`, `check_site.py` (raiz e `dist`), `contrato.sha256`, html-validate, `lighthouse.py` sem `--medir`, `gen_estado --check` e `check_plano`. `lychee` não está instalado localmente e não rodou; o CI cobre.
**Cuidado:** o agente rodou `npm ci` num worktree com `node_modules` em symlink e isso esvaziou o `node_modules` principal; foi restaurado. Não rode `npm ci` em worktree que compartilhe `node_modules` por symlink.
`lychee` não rodou localmente na fatia 2 (CI cobre).

## 3. O que só o navegador prova (pendente)

`python3 -m http.server 8080 -d dist`. **Fatia 1**, a 1280 px, salvo onde indicado:
- h1 do hero mais alto (entrelinha 1,25) em `/`, `/en/`, lottoexpert, topowalk e poleposition; o hero do poleposition ganhou 55 px;
- paleta v4 (oklch) nos chips cyan, emerald e orange da home, nos ✓ verdes da tabela do lottoexpert e no lima do poleposition;
- `backdrop-blur-sm` mais forte nos chips;
- listas e destaques das páginas legais;
- vidro do nav ao rolar e menu móvel a 360 px;
- Safari 16.4.

**Fatia 2 (casca)**, `python3 -m http.server 8080 -d dist`:
- barra do nav a 360, 768 e 1280, pt e en (60/68 px; recorte do logo sem o texto "since 1996");
- menu: abrir e fechar, Esc, girar a tela;
- segmento PT/EN com anel;
- rodapé a 360, 768 e 1280: ordem marca -> apps -> contato, coluna vazia a 768, linha dupla a 360;
- "Pular para o conteúdo" e Enter, no Chrome e no Safari;
- faixa de idioma;
- páginas antigas com ~68 px a mais no topo; CTA da Play do LottoExpert e do EclipseGo abaixo da dobra a 1280x720 (aceito até as fatias 5 e 9).

**WP-25 (`visual: false`, checagem rápida):** em `/` com o navegador em inglês e sem `ghf_lang` no `localStorage`, a faixa de idioma aparece; em `/en/`, não.

**WP-19 (rodada 3):** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`; Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o resultado no WP-19 (segue `blocked`).

Herdados, sem mudança: seletor com 3+ línguas (WP-16); Search Console, preview no WhatsApp e cards de compartilhamento no deploy único (WP-11, WP-21); 404 em `/x/y` só no Pages; WP-23 depois do deploy (convite com `?d=` v1 e v2 sem terceiros).

## 4. Próxima ação

**Do agente:** `/wp WP-10` fatia 3 (legal; `site-legal`). As fatias 3 e 4 andam sem copy nova.

**Do usuário:**
- PR da fatia 2 (seção 1);
- checklists do WP-19, da fatia 1 e da fatia 2 (seção 3);
- capturas do app (D26): todas para LottoExpert e TopoWalk, 2 para Pole Position e 2 para EclipseGo;
- push de `feat/wp-10-redesign`;
- decidir o PR rascunho `feat/wp-10-redesign → develop`, título `[NÃO FAZER MERGE — D13]`, para o CI rodar a cada fatia;
- D3 (medição), que segura o WP-13;
- PR #37: não se mescla até o deploy único.

**Copy pendente (fatia 5):** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável; confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; `LOTTO-COPY-VANTAGEM-01`; `INDEX-LOTTO-DESC-DIVERGE-01`. Pendências dos apps (herdadas): `PREVALENCIA-PT-NOS-APPS-01` (WP-16), `PP-NAV-CONTRASTE-01`, branches de eclipse-go e Pole Position para a main.

## 5. Decisões não registradas

Nenhuma. D24-D27 e o ADR-008 (incluindo o §7, plugin `sem-polyfill`) estão registrados.

## 6. Esperando publicação

A modernização inteira (WP-08 a WP-10 e o resto) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a fatia 9, e o WP-19 segura o deploy.

## 7. Escrituração e branches

- Triagem: vazia. `RODAPE-ORDEM-M-T-01` roteado ao WP-19; `DATA-APP-E-TABULAR-01` resolvido na fatia 2.
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-10-fatia-2` (não enviada), `feat/wp-19-rodada-3-claude-design` (integrada; WP-19 segue `blocked`) e `feat/wp-05-ci-no-pr` (não integrada).
