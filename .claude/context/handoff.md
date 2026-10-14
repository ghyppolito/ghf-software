# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-13.** Handoff da sessão anterior; "Onde parei" atualizado ao fechar o WP-19 (branch `feat/wp-19-rodada-3-claude-design`, local, sem push, sobre `origin/develop`).

## 1. Onde parei

WP-19: rodada 3 exportada (`design/handoff/2026-10-13-rodada-3/`) e auditada (`design/README.md`: 4 itens
cobertos, 1, 2, 3 e 7 parciais, nenhum ausente). `blocked`, falta o **checklist de navegador** do usuário
(`visual: true`, lista no WP). Branch local, sem push. WP-07 segue `blocked` (passos do usuário, seção 4);
o deploy está adiado até a janela de pouco uso do bolão (o app está em atualização de versão). WP-08 pode
andar em branch isolada, sem merge em `develop` até o WP-07 estar no ar (proposta feita, sem resposta).

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

**Antes de tudo, do usuário (WP-19):**
(a) Checklist de navegador da rodada 3: `python3 -m http.server 8080 -d "design/handoff/2026-10-13-rodada-3"`;
`Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`,
`Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768; troca pt/en na legal (en é stub, esperado);
`?app=pole&suggest=de`: a faixa fecha e não volta na sessão; Tab mostra foco em "Ver todas" e nos sociais
do footer; selo "Publicado" distinto do verde do Pole no footer. Escrever o que viu no WP-19.
(b) Decisões novas em `decisoes.md`: D10 (**`design/` no Jekyll: excluir antes do `/release`** — hoje o
`/release` publicaria ~19 MB de `design/`, inclusive cópias do texto legal em URLs alternativas), D11
(`--success`) e D12 (limiares de destaque vs ver todas).


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
