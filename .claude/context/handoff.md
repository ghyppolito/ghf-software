# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-13.** Branch `docs/handoff-2026-10-13`, sobre `origin/develop`; sem push.

## 1. Onde parei

WP-05 e WP-06 `done`, integrados em `develop` (PR #33 e #35). WP-07 `blocked` (PR #34 integrado), mas
**nada dele está no ar**: depende de passos do usuário (seção 4). WP-19 (rodada 3 do Claude Design)
criado, `todo`, trilha C. Próximo WP depois do WP-07: WP-08 (depende só do WP-07).

## 2. Quebrado ou pela metade agora

Nada quebrado. Pela metade:
- Publicação: `origin/develop` está 27 commits à frente de `origin/master` (WP-03 escrituração, WP-05,
  D9, WP-07, WP-06, WP-19). Nenhum texto legal nem caminho contratual entre eles. Urgência baixa por
  conteúdo, média por deploy (o WP-07 só se prova no ar).
- WP-05: CI e proteção de branch (D9: `plano` e `site` obrigatórios em `develop` e `master`, strict off,
  admin pode ignorar, aplicada via `gh api` em 2026-10-12). O repositório é público, então Actions não
  consome a cota do plano free; o usuário decidiu manter o CI.
- Branch local `feat/wp-06-brief-de-design` já integrada: pode apagar. `feat/wp-07-stack-com-build` idem.

## 3. O que só o navegador prova (usuário ainda não viu)

WP-07 inteiro. Local (`npm ci && npm run build && python3 -m http.server 8080 -d dist`): home,
`lottoexpert.html`, `lottoexpert-privacy.html` e `-terms` (pt e en), convite com `?d=` de link real,
`/404.html` (Tab mostra contorno ciano; 360/768/1280). Depois, no ar: a mesma lista, `/qualquer/coisa`
mostra o 404 novo, link de bolão real no Android abre o app (App Links), HTTPS imposto.
As telas do handoff de design o usuário já viu no Claude Design (não é critério de página no ar).

## 4. Próxima ação

Do usuário, em ordem (recomendado: `/release` e a troca do Pages na mesma sessão, para encurtar a
janela em que o Jekyll publica `design/`, ~19 MB, e `docs/`):
1. Checklist local (seção 3).
2. `/release` (develop → master). Ainda em modo branch o run "pages build and deployment" do Jekyll tem
   de sair verde com o `exclude` novo; o `Deploy` só builda (job deploy pulado).
3. Remover `main` da política do ambiente `github-pages` (`PAGES-ENV-MAIN-01`).
4. Conferir o Play Console: nenhum link para `ghfsoftware.com/docs/...`.
5. Trocar o Pages para "GitHub Actions", `gh variable set PAGES_VIA_ACTIONS --body true`,
   `gh workflow run Deploy --ref master`; depois `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json`
   (200), `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -c "Última atualização"` (>= 1)
   e a checklist no domínio.
6. Rollback: Source "Deploy from a branch" → master e `gh variable delete PAGES_VIA_ACTIONS`.

**Copy pendente do usuário antes do WP-10** (não está em `decisoes.md`: é texto de produto, decidido
junto da implementação):
- "chance matemática" → "probabilidade exata".
- Texto final do aviso de jogo responsável (o export traz "Texto provisório").
- Confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade".

Rodada 3 do Claude Design (WP-19) é pré-condição das landings TopoWalk, Pole Position e EclipseGo no
WP-10, não da home, landing LottoExpert, legal, 404 e convite.

## 5. Decisões fora de `decisoes.md` e ADR

- Ordem dos apps (LottoExpert · TopoWalk · Pole Position · EclipseGo), tema escuro com legal em papel,
  Inter self-hosted, cores por app, prova sem números, "desde 2004", trevo só como ícone: estão em
  `design/BRIEF.md` §10. São decisões de design dentro da D4; o brief é a fonte, sem linha nova em
  `decisoes.md`.
- `if: vars.PAGES_VIA_ACTIONS == 'true'` no job `deploy` (evita deploy concorrente com o Jekyll em modo
  branch): descrito no `deploy.yml` e no WP-07, passo 5. **Não está no ADR-002** (conferido por grep).
- O usuário não recusou nenhuma proposta nesta sessão.

## 6. Esperando publicação

27 commits em `origin/develop` ainda fora de `master` (lista: `git log origin/master..origin/develop`).
Sem texto legal nem caminho contratual entre eles. Sem efeito no site até o `/release`.
