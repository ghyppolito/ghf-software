# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-13/14.** Escrito na branch `feat/wp-19-rodada-3-claude-design` (pushada, sem PR; vai a
`develop` por PR). A branch `feat/wp-08-f1-infra-e-home` tem outra versão deste arquivo (commit 10d14a7):
**no conflito, vale a versão mais recente (esta).**

## 1. Onde parei

- **WP-19** `blocked`: rodada 3 exportada em `design/handoff/2026-10-13-rodada-3/` e auditada (`design/README.md`:
  cobertos 4, 5, 8; 6 escrito com decisão pendente; parciais 1, 2, 3, 7). Falta o checklist de navegador do usuário.
- **WP-08** `doing` (exceção de dependência decidida pelo usuário). Integração `feat/wp-08-layout-unico`
  (pushada; PR rascunho #37 "NÃO FAZER MERGE — aguarda WP-07 no ar"). Fatia 1 (home em `/` e `/en/`, Tailwind
  compilado, layout único) está em `feat/wp-08-f1-infra-e-home` (337c58f, 7dc7834, 10d14a7), **local, sem push,
  não integrada**. Auditada (qa, seo-perf, ux): nada alto no escopo.
- **WP-07** segue `blocked`. Deploy adiado pelo usuário para janela de pouco uso do bolão (o app LottoExpert está
  em atualização de versão).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar. Pela metade:
- **Fatia 1 não integrada.** O agente não tem permissão de `git merge`. Usuário roda:
  `git switch feat/wp-08-layout-unico && git merge --no-ff feat/wp-08-f1-infra-e-home -m "WP-08: fatia 1 — infra, layout único e home" && git push`
  e, na branch da fatia, `git push` (nada dela está no GitHub).
- **Push desta branch** (handoff + escrituração): é do usuário, ou peça ao agente.
- Publicação: `origin/develop` está 29 commits à frente de `origin/master`. Conferido com `git diff --name-only
  origin/master origin/develop`: nenhum HTML legal nem caminho contratual; só cópias em `design/` e `docs/AVALIACAO.md`.
- Lighthouse mobile da home (fatia 1): perf 63→66–67, a11y 80→94, BP 100, SEO 100. LCP ~16 s por PNGs
  (`ASSETS-PNG-LCP-01`, WP-12) — conhecido, não é regressão.
- Ainda não feito: tag `pre-wp-08` em `master` (só antes da R1); ajuste de uma linha no ADR-003 sobre `cssTarget`
  (seção 5); `README.md`/`CLAUDE.md` da fatia 1 já foram tocados na branch dela, não aqui.
- Branches locais antigas apagadas (`feat/wp-06-…`, `feat/wp-07-…`, `docs/handoff-2026-10-13`); conferir com `git branch`.
  Restam `feat/wp-01…02…04…05`, `docs/publicacao-trilha-a`, `feature/invite-bolao`, `main`, se também integradas, podem sair.

## 3. O que só o navegador prova (usuário ainda não viu)

- **WP-19:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **WP-08 fatia 1:** `/`, `/en/` e `/404.html`, a 360 e 1280, no Chrome e no Safari (checklist no WP-08). Não feito.
- **WP-07 inteiro** (build local, depois no ar): home, `lottoexpert.html`, legais pt/en, convite com `?d=` de link real
  (Android abre o app), `/404.html`, `/qualquer/coisa`, HTTPS.
- **Convite do bolão em tema escuro:** o usuário vê o card escuro. O código é só tema claro (sem `prefers-color-scheme`
  nem `color-scheme`; cabeçalho em degradê escuro de propósito). Hipótese: escurecimento forçado do navegador (Samsung
  Internet / Chrome auto-dark). Está testando no PC. **Não criar WP ainda** (achado `CONVITE-TEMA-ESCURO-01`, `nota`).
  Opções: `color-scheme: only light` ou tema escuro desenhado (recomendado; exige Claude Design). Convite é URL contratual.

## 4. Próxima ação

**Do usuário, nesta ordem:**
1. Integrar a fatia 1 (comando na seção 2) e fazer o checklist de navegador da home.
2. Checklist do WP-19; escrever o resultado no WP.
3. Decidir **D10** antes de qualquer `/release` (excluir `design/` do `_config.yml`: hoje o `/release` publicaria
   ~19 MB de `design/`, com cópias do texto legal em URLs alternativas). Depois D11 (`--success`, só WP-10) e D12
   (limiares de destaque, WP-10).
4. Quando a janela do bolão chegar, a lista do WP-07: `/release`; remover `main` da política do ambiente
   `github-pages` (`PAGES-ENV-MAIN-01`); conferir Play Console sem links `ghfsoftware.com/docs/...`; trocar o Pages
   para "GitHub Actions", `gh variable set PAGES_VIA_ACTIONS --body true`, `gh workflow run Deploy --ref master`;
   `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json` (200) e a checklist no domínio.
   Rollback: Source "Deploy from a branch" → master e `gh variable delete PAGES_VIA_ACTIONS`.

**Do agente:** fatia 2 do WP-08 (landing LottoExpert), incluindo `HOME-EN-SEM-LANG-01` (gravar `ghf_lang` ao abrir
`/en/`, sem redirect). Respostas do usuário ao plano do WP-08: R1 (fatias 1–5) só depois do WP-07 no ar, convite real
testado e alguns dias sem incidente; tag `pre-wp-08` em `master` antes da R1; 3 releases (R1 fatias 1–5, R2 legais 6–8,
R3 `public/` e convite 9); sem redirect para `/en/` até o WP-15. Tudo isso está no corpo do WP-08.

**Copy pendente do usuário antes do WP-10:** "chance matemática" → "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de
publicidade". Rodada 3 é pré-condição das landings TopoWalk, Pole Position e EclipseGo no WP-10, não da home.

## 5. Decisões fora de `decisoes.md` e ADR

- **Exceção de dependência do WP-08 e respostas ao plano** (releases, tag, sem redirect): registradas no WP-08, não em
  `decisoes.md`. Motivo: são decisões de execução e processo daquele WP, não escolhas de produto que bloqueiem outro WP.
- **`cssTarget` no `astro.config.mjs`** (`chrome87, edge88, firefox78, safari14`, evita `backdrop-filter` duplicado no
  CSS compilado): complementa o ADR-003 e **não está nele**. Merece uma linha lá (o próximo agente na branch da fatia 1
  faz; não dá para editar o ADR daqui, ele não existe nesta branch).
- **Texto pt da home vem do dicionário JS** (o que o visitante via, não o HTML estático antigo): `INDEX-LOTTO-DESC-DIVERGE-01`.
- Já em arquivo: `if: vars.PAGES_VIA_ACTIONS == 'true'` no `deploy.yml` (descrito no workflow e no WP-07; fora do ADR-002).
- O usuário não recusou nenhuma proposta.

## 6. Escrituração desta sessão

- **ADR de i18n do WP-15** citado como "ADR-003": renumerado no WP-15 (ADR-003 é o Tailwind, da branch do WP-08).
- **D11** passou a impactar só o WP-10; o achado `SUCCESS-DOIS-VALORES-01` foi roteado para `WP-10`.
- Novos achados: `INVITE-PAKO-CDNJS-01` (→ WP-12) e `CONVITE-TEMA-ESCURO-01` (`nota`).
- Os achados da fatia 1 (`INDEX-LOTTO-DESC-DIVERGE-01`, `HOME-*`, `ASSETS-PNG-LCP-01` etc.) vivem em
  `achados-novos.md` da branch `feat/wp-08-f1-infra-e-home`, com destino; **não estão aqui**. Ao integrar, o conflito
  em `achados-novos.md` se resolve mantendo as linhas das duas versões.
