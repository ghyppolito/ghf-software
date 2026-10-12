---
id: WP-07
titulo: O site tem build que preserva as URLs contratuais e publica no Pages por Actions
area: infra
status: todo
depende_de: [WP-05]
adr: [ADR-001]
spec: docs/AVALIACAO.md
decisoes: [D2, D5]
tamanho: L
risco: alto
visual: true
branch: feat/wp-07-stack-com-build
---

# WP-07 — O site tem build que preserva as URLs contratuais e publica no Pages por Actions

**Depende de:** WP-05 (gate) · **Achados roteados:** —

**Objetivo:** o repositório tem um projeto Astro (ou o que D2 decidir) cujo `npm run build`
gera `dist/` com **todas** as páginas atuais nos mesmos caminhos, `check_site.py --raiz dist`
verde, e o Pages passa a publicar `dist/` por GitHub Actions a partir de `master`. Esta é a
prova de conceito; a migração página a página é o WP-08.

**Contexto:** `docs/AVALIACAO.md` §2 item 4 (Tailwind CDN) e §3.2. Risco central: ADR-001 —
`/lottoexpert-privacy.html`, `/.well-known/assetlinks.json` e o convite precisam existir como
arquivo no resultado. Astro: `build.format: 'file'` + `public/` resolvem; provar, não supor.

**Ler antes:** `docs/AVALIACAO.md` §3.2; ADR-001; documentação do Astro sobre `build.format`,
`public/` e a action oficial `withastro/action` para Pages.

**Arquivos-alvo:** `package.json`, `astro.config.mjs`, `tailwind.config.mjs`, `src/` (um
layout mínimo + uma página de prova), `public/` (`.well-known/`, `CNAME`, convite, assets),
`.github/workflows/deploy.yml`, `.gitignore`, `CLAUDE.md` (seção "Comandos" e "Arquitetura"),
ADR-002.

**Passos:**
1. ADR-002 (stack escolhida em D2, por quê, o que fecha).
2. Projeto mínimo: as 10 páginas atuais copiadas para `src/pages/` **como estão** (HTML
   bruto dentro de `.astro`), sem refatorar — o objetivo é provar o pipeline, não migrar.
3. `npm run build`; `python3 tools/check_site.py --raiz dist` verde; `diff -r` entre `dist/`
   e a raiz atual para as páginas e assets: diferenças só de formatação.
4. `deploy.yml`: build em push para `master`, publica `dist/` (`actions/deploy-pages`).
   Pages muda de "branch" para "GitHub Actions" — **usuário** muda nas configurações, depois
   do merge, com rollback = voltar para "branch master".
5. `CLAUDE.md` e `/verify` ganham `npm run build`.

**Critérios de aceite:**
- `python3 tools/check_site.py --raiz dist` verde.
- `for p in <7 contratuais>; do test -f dist/$p; done` sem falha.
- `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json` 200 depois do deploy, e
  `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -c "Última atualização"` ≥ 1.
- Nenhum `cdn.tailwindcss.com` em `dist/` (`grep -rc cdn.tailwindcss dist | grep -v ":0"` vazio)
  — ou, se as páginas ainda forem HTML bruto, registrar que o CDN sai no WP-08.
- Lighthouse mobile da home, antes e depois: tabela no WP (`site-seo-perf`).

**Só no navegador:** home, uma landing, uma página legal e o convite com `?d=` de um link real,
em `dist/` servido local e depois no ar.

**Irreversível:** a troca do modo de publicação do Pages. Rollback descrito no passo 4.

**Risco:** alto — URL contratual e deploy. Mitigação: `check_site.py --raiz dist` no CI
antes do merge, e o Pages só muda de modo depois de `dist/` provado.
