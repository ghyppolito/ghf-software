# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-13.** Branch `feat/wp-07-stack-com-build`, sobre `origin/develop`; sem push.

## 1. Onde parei

WP-07 implementado e auditado, `blocked` (2026-10-13): o que falta é do usuário. Build Astro copia a
raiz para `dist/`, `check_site.py --raiz dist` verde, deploy por Actions pronto e travado atrás da
variável `PAGES_VIA_ACTIONS`. Lighthouse sem regressão (tabela no WP). Ainda em modo branch, o Jekyll
segue publicando. Depois do WP-07 `done`: WP-08.

## 2. Quebrado ou pela metade agora

Nada quebrado. Pela metade: a publicação (itens 1 a 6 abaixo) e o critério dos dois `curl` no ar.

## 3. O que só o navegador prova

Local (`npm ci && npm run build && python3 -m http.server 8080 -d dist`): home, `lottoexpert.html`,
`lottoexpert-privacy.html` e `-terms` (data em pt e en), convite com `?d=` de link real, `/404.html`
(Tab mostra contorno ciano; 360/768/1280). No ar: a mesma lista, `/qualquer/coisa` mostra o 404 novo,
link de bolão real no Android abre o app (App Links), HTTPS imposto.

## 4. Próxima ação

Do usuário, em ordem:
1. PR `feat/wp-07-stack-com-build → develop` (o agente abre se pedir), CI verde, merge.
2. Checklist local (seção 3).
3. `/release` (develop → master). Ainda em modo branch: o run "pages build and deployment" do Jekyll
   tem de sair verde com o `exclude` novo; o `Deploy` só builda (job deploy pulado).
4. Conferir o Play Console: nada aponta para `ghfsoftware.com/docs/...`.
5. Remover `main` da política do ambiente `github-pages` (`PAGES-ENV-MAIN-01`).
6. Trocar o Pages para "GitHub Actions", `gh variable set PAGES_VIA_ACTIONS --body true`,
   `gh workflow run Deploy --ref master`; depois `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json`
   (200), `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -c "Última atualização"` (>= 1)
   e a checklist no domínio.
7. Rollback: Source "Deploy from a branch" → master e `gh variable delete PAGES_VIA_ACTIONS`.

## 5. Decisões fora de `decisoes.md` e ADR

- `if: vars.PAGES_VIA_ACTIONS == 'true'` no job `deploy`: evita deploy concorrente com o Jekyll em
  modo legacy (achado alto do `site-qa`); descrito no WP-07, passo 5.

## 6. Esperando publicação

Cinco commits na branch do WP-07 (6670de1 D9, e503dca D2 + ADR-002, c2e6a31, 6a2a06e, 2c6d854) mais
a escrituração; nada no remoto. Sem efeito no site até o `/release`.
