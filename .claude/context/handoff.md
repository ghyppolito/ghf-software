# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-21.** Branch `feat/wp-10-redesign` (integração da D13, nasceu de `feat/wp-08-layout-unico`), **não enviada ao GitHub**. Árvore limpa antes deste commit. WP-10 segue `doing`.

## 1. Onde parei

- Fatia 1 do WP-10 feita: Tailwind 4.3.5 pelo `@tailwindcss/vite` e tokens do handoff em `src/styles/tokens.css` (ADR-008). Commits c2e2de8, 837d483, ee0ea3e, eb52fbe, mais D24-D27, ADR-008 e WP-24 (7663b16).
- Auditoria (`site-qa`, `site-seo-perf`, `site-ux`): um achado alto, o orçamento do lighthouse estourava em `/eclipsego-privacy.html` (178 962 > 178 482) e o FCP de `/` foi de 1,50 para 1,65 s. O plugin `sem-polyfill` (ADR-008 §7, com teste e regra §18 no `check_site.py`) cortou o CSS de 95 962 para 80 683 B; FCP de volta a 1,50 s; LCP de `/` 2,55 s (aviso, igual ao Tailwind 3). O `orcamento-lighthouse.json` não foi remedido.
- Próxima: fatia 2 (casca: `Base`, `Nav`, `Footer`, `SeletorIdioma`, `SugestaoIdioma`, `Logo.astro`), com a prop `app`/`data-app` em `Base.astro` e o `tabular-nums` (`DATA-APP-E-TABULAR-01`).

## 2. Quebrado ou pela metade agora

Nada quebrado. Passaram no `/verify`: `check_site.py --raiz dist`, `contrato.sha256`, html-validate, `npm run test:css` (21 testes) e `check_plano`. `lychee` não está instalado localmente e não rodou; o CI cobre.
**Cuidado:** o agente rodou `npm ci` num worktree com `node_modules` em symlink e isso esvaziou o `node_modules` principal; foi restaurado. Não rode `npm ci` em worktree que compartilhe `node_modules` por symlink.
As utilidades `*-app-acc` ficam sem valor em toda página até a fatia 2 emitir `data-app`.

## 3. O que só o navegador prova (pendente)

`python3 -m http.server 8080 -d dist`. **Fatia 1**, a 1280 px, salvo onde indicado:
- h1 do hero mais alto (entrelinha 1,25) em `/`, `/en/`, lottoexpert, topowalk e poleposition; o hero do poleposition ganhou 55 px;
- paleta v4 (oklch) nos chips cyan, emerald e orange da home, nos ✓ verdes da tabela do lottoexpert e no lima do poleposition;
- `backdrop-blur-sm` mais forte nos chips;
- listas e destaques das páginas legais;
- vidro do nav ao rolar e menu móvel a 360 px;
- Safari 16.4.

**WP-19 (rodada 3):** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`; Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o resultado no WP-19 (segue `blocked`).

Herdados, sem mudança: seletor com 3+ línguas (WP-16); Search Console, preview no WhatsApp e cards de compartilhamento no deploy único (WP-11, WP-21); 404 em `/x/y` só no Pages; WP-23 depois do deploy (convite com `?d=` v1 e v2 sem terceiros).

## 4. Próxima ação

**Do agente:** `/wp WP-10` fatia 2 (a 1 a 4 andam sem copy nova).

**Do usuário:**
- checklist do WP-19 e o da fatia 1 (seção 3);
- capturas do app (D26): todas para LottoExpert e TopoWalk, 2 para Pole Position e 2 para EclipseGo;
- push de `feat/wp-10-redesign`;
- decidir o PR rascunho `feat/wp-10-redesign → develop`, título `[NÃO FAZER MERGE — D13]`, para o CI rodar a cada fatia;
- D3 (medição), que segura o WP-13;
- **pergunta:** o `ASTRO-UNDICI-AUDIT-01` (`astro` ≤ 7.4.6 e `undici` 8.0.0–8.12.1 no `npm audit`; conserto: Astro ≥ 7.4.13) vira `/novo-wp` ou um WP S de dependências? Está como `nota` até você responder.

**Copy pendente (fatia 5):** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável; confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; `LOTTO-COPY-VANTAGEM-01`; `INDEX-LOTTO-DESC-DIVERGE-01`. Pendências dos apps (herdadas): `PREVALENCIA-PT-NOS-APPS-01` (WP-16), `PP-NAV-CONTRASTE-01`, branches de eclipse-go e Pole Position para a main.

## 5. Decisões não registradas

Nenhuma. D24-D27 e o ADR-008 (incluindo o §7, plugin `sem-polyfill`) estão registrados.

## 6. Esperando publicação

A modernização inteira (WP-08 a WP-10 e o resto) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a fatia 9, e o WP-19 segura o deploy.

## 7. Escrituração e branches

- Triagem: vazia. O `ASTRO-UNDICI-AUDIT-01` virou `nota` com a pergunta acima; `DATA-APP-E-TABULAR-01` está roteado ao WP-10 (fatia 2).
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-19-rodada-3-claude-design` (integrada; WP-19 segue `blocked`) e `feat/wp-05-ci-no-pr` (não integrada).
