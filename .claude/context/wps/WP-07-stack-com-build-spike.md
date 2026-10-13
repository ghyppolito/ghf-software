---
id: WP-07
titulo: O site tem build que preserva as URLs contratuais e publica no Pages por Actions
area: infra
status: doing
depende_de: [WP-05]
adr: [ADR-001, ADR-002]
spec: docs/AVALIACAO.md
decisoes: [D2, D5, D9]
tamanho: L
risco: alto
visual: true
branch: feat/wp-07-stack-com-build
---

# WP-07 — O site tem build que preserva as URLs contratuais e publica no Pages por Actions

**Depende de:** WP-05 (gate) · **Achados roteados:** `ASSETLINKS-PUBLICACAO-NAO-PROVADA-01`,
`CI-ACTIONS-POR-TAG-01`

**Objetivo:** o repositório tem um projeto Astro (D2, ADR-002) cujo `npm run build`
gera `dist/` com **todas** as páginas atuais nos mesmos caminhos, `check_site.py --raiz dist`
verde, e o Pages passa a publicar `dist/` por GitHub Actions a partir de `master`. Esta é a
prova de conceito; a migração página a página é o WP-08.

**Contexto:** `docs/AVALIACAO.md` §2 item 4 (Tailwind CDN) e §3.2. Risco central: ADR-001 —
`/lottoexpert-privacy.html`, `/.well-known/assetlinks.json` e o convite precisam existir como
arquivo no resultado. Astro com `build.format: 'preserve'` (ADR-002; `'file'` transformaria `en/index` em
`en.html`). As páginas atuais ficam na raiz, fonte única até o WP-08: uma integração local copia
para `dist/` uma lista fechada, byte a byte. HTML bruto em `src/pages/*.astro` foi testado e
quebra as páginas (scripts empacotados, texto en some) — descartado.

**Ler antes:** `docs/AVALIACAO.md` §3.2; ADR-001; documentação do Astro sobre `build.format`,
`public/` e a action oficial `withastro/action` para Pages.

**Arquivos-alvo:** `package.json`, `package-lock.json`, `astro.config.mjs`, `src/layouts/`
(layout mínimo), `src/pages/404.astro` (página de prova), `.github/workflows/deploy.yml`,
`.github/workflows/pr.yml`, `tools/check_site.py`, `_config.yml` (`exclude`), `.gitignore`,
`CLAUDE.md` (seção "Comandos" e "Arquitetura"), ADR-002. Sem `public/` e sem Tailwind (o CDN
sai no WP-08).

**Passos:**
1. ADR-002 (stack escolhida em D2, por quê, o que fecha).
2. Projeto mínimo: `astro` 7.3.8 exato, Node 22.22, lockfile versionado. Integração local
   (`astro:build:done`) copia da raiz para `dist/`: os 10 `*.html`, `assets/`, `.well-known/`,
   `lotto-expert/` e `CNAME` — `fs.cp` com `errorOnExist`; colisão com página gerada falha o
   build. Página de prova `src/pages/404.astro` (pt e en, sem JS, sem copy de produto).
3. `check_site.py`: as fontes legais (`docs/*.md`) são lidas da raiz do repositório mesmo com
   `--raiz dist`, e fonte ausente é erro (hoje pula calado).
4. `pr.yml` (nomes `plano` e `site` intactos, D9): mantém `check_site.py` na raiz e acrescenta
   `npm ci`, `npm run build`, `check_site.py --raiz dist`, html-validate (do lockfile) e lychee
   sobre `dist/`. Actions fixadas por SHA de commit, com a tag em comentário.
5. `deploy.yml`: `push` em `master` e `workflow_dispatch`; build, `check_site.py --raiz dist`,
   `test -f dist/.well-known/assetlinks.json`, upload com `include-hidden-files: true`, deploy
   com `environment: github-pages`; `pages: write` e `id-token: write` só no job de deploy. O job
   de deploy só roda com a variável de repositório `PAGES_VIA_ACTIONS` = `true` (ausente = não
   publica): enquanto o Pages está em modo branch, o Jekyll publica e o `deploy.yml` só builda.
6. `_config.yml`: `exclude` de `src`, `node_modules`, `package*.json`, `astro.config.mjs` —
   enquanto o Pages está em modo branch, o Jekyll não pode publicar o projeto Astro.
7. Sequência de publicação: PR para `develop` com CI verde → `/release` (ainda em modo branch;
   o run "pages build and deployment" precisa sair verde) → **usuário** troca o Pages para
   "GitHub Actions", cria a variável `PAGES_VIA_ACTIONS=true` (Settings → Secrets and variables →
   Actions → Variables, ou `gh variable set PAGES_VIA_ACTIONS --body true`) e dispara `deploy.yml`
   por `workflow_dispatch` → `curl` dos critérios e checklist do navegador. Rollback: voltar o
   modo para "branch master" **e** apagar a variável ou trocá-la para `false` (a raiz segue
   intacta até o WP-08, que só apaga páginas da raiz depois do modo Actions confirmado no ar).
8. `CLAUDE.md` e `/verify` ganham `npm run build`.

**Critérios de aceite:**
- `python3 tools/check_site.py --raiz dist` verde; com a data de "Última atualização" de uma
  página legal adulterada em `dist/`, vermelho.
- `cmp` sem diferença entre cada arquivo copiado da raiz e o seu par em `dist/`.
- `for p in <7 contratuais>; do test -f dist/$p; done` sem falha.
- `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json` 200 depois do deploy, e
  `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -c "Última atualização"` ≥ 1.
- Nenhum `cdn.tailwindcss.com` em `dist/` (`grep -rc cdn.tailwindcss dist | grep -v ":0"` vazio)
  — ou, se as páginas ainda forem HTML bruto, registrar que o CDN sai no WP-08.
- Lighthouse mobile da home, antes e depois: tabela no WP (`site-seo-perf`).

**Só no navegador:** home, uma landing, uma página legal e o convite com `?d=` de um link real,
em `dist/` servido local e depois no ar.

**Deixa de ser publicado:** `docs/`, `CLAUDE.md`, `README.md`, `tools/`, `design/` — o Jekyll
publica hoje (200); nenhum app aponta para eles (busca nos 4 repositórios). Não são URLs
contratuais. **Passa a responder 200** no modo Actions: `/404.html` (a página de prova) e
`/CNAME` — inofensivos.

**Irreversível:** a troca do modo de publicação do Pages. Rollback descrito no passo 7.

**Risco:** alto — URL contratual e deploy. Mitigação: `check_site.py --raiz dist` no CI
antes do merge, e o Pages só muda de modo depois de `dist/` provado.
