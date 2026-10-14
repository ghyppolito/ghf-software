# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-14.** Escrito na branch `docs/publicacao-wp-07` (de `origin/develop`, sem push; vai a `develop`
por PR). A branch `feat/wp-08-f1-infra-e-home` tem outra versão deste arquivo: **no conflito, vale esta.**

## 1. Onde parei

- **WP-07 `done`, publicado em 2026-10-14.** PR #39 (`develop → master`, merge 075469f); Pages em "GitHub Actions"
  (`build_type: workflow`), `PAGES_VIA_ACTIONS=true`, Deploy `success`. Provas e checklist de navegador (inclusive o
  bolão com link real: Android abre o app) estão no corpo do WP-07.
- **Relógio da R1 do WP-08 começa em 2026-10-14.** Pela regra do usuário, a R1 só sai depois de alguns dias sem
  incidente com o WP-07 no ar, com convite real testado (feito hoje) e a tag `pre-wp-08` em `master` antes.
- **WP-08** `doing`, integração `feat/wp-08-layout-unico` (PR rascunho #37, "NÃO FAZER MERGE" — o aviso do WP-07 já
  não vale; segue rascunho até a R1). Fatia 1 (home em `/` e `/en/`) está em `feat/wp-08-f1-infra-e-home`,
  **local, sem push, não integrada**. O arquivo do WP-08 não foi tocado aqui, para não conflitar.
- **WP-19** `blocked`: falta o checklist de navegador da rodada 3 (seção 3). Já está publicado (`design/` não vai ao ar).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar. Pela metade:
- **Fatia 1 não integrada.** O agente não tem permissão de `git merge`. Usuário roda:
  `git switch feat/wp-08-layout-unico && git merge --no-ff feat/wp-08-f1-infra-e-home -m "WP-08: fatia 1 — infra, layout único e home" && git push`
  e, na branch da fatia, `git push`.
- **Push desta branch** (escrituração do WP-07): é do usuário, ou peça ao agente.
- Tag `pre-wp-08` em `master`: ainda não criada (só antes da R1).
- `CONFIG-YML-ORFAO-01`: `_config.yml` já não é lido; sai no WP-08.
- Branches locais antigas (`feat/wp-01…02…04…05`, `docs/publicacao-trilha-a`, `feature/invite-bolao`, `main`): podem
  sair, se integradas. Conferir com `git branch`.

## 3. O que só o navegador prova (usuário ainda não viu)

- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **WP-08 fatia 1 (home):** `/`, `/en/` e `/404.html`, a 360 e 1280, no Chrome e no Safari (checklist no WP-08). Não feito.
- **Convite do bolão em tema escuro** (nota `CONVITE-TEMA-ESCURO-01`, sem WP): o código é só tema claro; hipótese de
  escurecimento forçado do navegador (Samsung Internet / Chrome auto-dark). Opções: `color-scheme: only light` ou tema
  escuro desenhado (recomendado; exige Claude Design). Convite é URL contratual.

## 4. Próxima ação

**Do usuário:**
1. Integrar a fatia 1 (comando na seção 2) e fazer o checklist da home.
2. Checklist do WP-19; escrever o resultado no WP.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10.
4. Acompanhar o site no ar nos próximos dias; sem incidente, autorizar a R1 do WP-08.

**Do agente:** fatia 2 do WP-08 (landing LottoExpert), incluindo `HOME-EN-SEM-LANG-01` (gravar `ghf_lang` ao abrir
`/en/`, sem redirect). Respostas do usuário ao plano do WP-08 (R1 das fatias 1–5, R2 legais 6–8, R3 `public/` e convite 9;
sem redirect para `/en/` até o WP-15) estão no corpo do WP-08.

**Copy pendente do usuário antes do WP-10:** "chance matemática" → "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de
publicidade". Rodada 3 é pré-condição das landings TopoWalk, Pole Position e EclipseGo no WP-10, não da home.

## 5. Decisões fora de `decisoes.md` e ADR

- **Exceção de dependência do WP-08 e respostas ao plano:** registradas no WP-08, são decisões de execução daquele WP.
- **`cssTarget` no `astro.config.mjs`** (`chrome87, edge88, firefox78, safari14`): complementa o ADR-003 e não está
  nele. O ADR-003 só existe na branch do WP-08: acrescentar a linha quando a fatia 1 integrar.
- **D10 resolvida sem mudar `_config.yml`:** o usuário fez `/release` e troca do Pages na mesma sessão; `design/` saiu
  do ar pela troca. Está em `decisoes.md`.
- O usuário não recusou nenhuma proposta.

## 6. Escrituração desta sessão

- Publicação: `git log --oneline origin/master..origin/develop` vazio; `origin/develop..origin/master` tem só o
  merge 075469f (#39). Nada espera publicação. Esta branch ainda não está em `develop`.
- Resolvidos e tachados: `PAGES-ENV-MAIN-01`, `DESIGN-PUBLICO-JEKYLL-01`, `DESIGN-NAO-EXCLUIDO-JEKYLL-02`.
- "Publicado em 2026-10-14" nos WP-05, WP-06, WP-07 e WP-19.
- Os achados da fatia 1 (`INDEX-LOTTO-DESC-DIVERGE-01`, `HOME-*`, `ASSETS-PNG-LCP-01` etc.) vivem em `achados-novos.md`
  da branch `feat/wp-08-f1-infra-e-home`. Ao integrar, o conflito em `achados-novos.md` e `handoff.md` se resolve
  mantendo as linhas das duas versões (handoff: vale esta).
