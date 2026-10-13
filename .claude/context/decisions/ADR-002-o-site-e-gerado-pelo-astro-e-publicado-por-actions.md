# ADR-002 · O site é gerado pelo Astro e o Pages publica `dist/` por GitHub Actions

**Data:** 2026-10-12 · **Estado:** aceita · **Decisão de produto:** D2 (A), usuário, 2026-10-12

## Contexto

Dez páginas com nav, footer, `tailwind.config` e dicionário i18n copiados em cada uma já
derivaram (`NAV-FOOTER-DERIVA-01`); o Tailwind vem do CDN de desenvolvimento; o texto legal é
HTML de ~100 KB por página, mantido à mão (`docs/AVALIACAO.md` §2 e §3.2). Hoje o Pages publica
a raiz de `master` pelo Jekyll, e **tudo** o que está na raiz vai ao ar (`/CLAUDE.md`,
`/tools/check_site.py` e `/docs/AVALIACAO.md` respondem 200 em 2026-10-12).

## Decisão

1. **Astro** (7.3.8 em 2026-10-12, fixado exatamente em `package.json`) com Node `22.22`
   (`engines` e `actions/setup-node`), `package-lock.json` versionado e `npm ci` no CI. Saída
   estática; telemetria desligada no CI (`ASTRO_TELEMETRY_DISABLED=1`, a mesma régua privacy-first).
2. **URLs contratuais (ADR-001) saem como arquivo literal** em `dist/`. Página contratual
   gerada por rota usa um arquivo `src/pages/<nome-contratual>.astro` com `build.format:
   'preserve'`: `x.astro` → `x.html`, `en/index.astro` → `en/index.html`. `'file'` não serve —
   transforma `en/index.astro` em `en.html` (medido em 2026-10-12, Astro 7.3.8), o que quebra a
   rota `/en/` do WP-08. Arquivo que não pode ser reescrito (convite do bolão, `assetlinks.json`,
   `CNAME`) é copiado **byte a byte**, nunca gerado.
3. **HTML legado não passa pelo compilador do Astro.** Um `.astro` com HTML bruto é reescrito:
   `<script>` vira módulo empacotado em `/_astro/`, `<style>` é escopado e minificado
   (`backdrop-filter` sem prefixo some), `{` no texto é expressão. Enquanto uma página não é
   migrada (WP-08), ela é copiada sem alteração para `dist/`; migrar é reescrever, não colar.
4. **Publicação por Actions** (`.github/workflows/deploy.yml`), só em push para `master`
   (D5) e `workflow_dispatch`. O job de build roda `npm ci`, `npm run build` e
   `python3 tools/check_site.py --raiz dist` **antes** do upload: o artefato que vai ao ar é o
   artefato provado. `actions/upload-pages-artifact` com `include-hidden-files: true` —
   desde a v4 ele exclui dotfiles por padrão, e sem isso `/.well-known/assetlinks.json` some do
   site com o build verde. Permissões: `contents: read` no workflow; `pages: write` e
   `id-token: write` só no job de deploy, no ambiente `github-pages` (que já só aceita `master`
   e `main`). `concurrency: pages`, sem cancelar deploy em andamento.
5. **Actions fixadas por SHA de commit**, com a tag em comentário, em todos os workflows
   (`CI-ACTIONS-POR-TAG-01`).
6. **Os nomes dos checks `plano` e `site` não mudam** (D9). O build e as checagens sobre `dist/`
   entram como passos do job `site` de `pr.yml`; o deploy é outro workflow e não é check
   obrigatório.
7. **`check_site.py --raiz dist` prova o publicado**, e as fontes (`docs/*.md`) continuam
   lidas da raiz do repositório — a checagem de datas legais não pode depender de `docs/`
   estar em `dist/`.

## O que isto fecha

Eleventy e HTML + Tailwind CLI (D2 B/C); Next.js/React; o Pages em modo "branch" depois da
troca; `build.format: 'directory'` ou `'file'`; página contratual gerada por rota dinâmica ou
por redirect; colar HTML legado num `.astro` como forma de migração; actions por tag móvel.
Voltar ao modo "branch" depois que a raiz deixar de ter as páginas (WP-08) exige reverter o
WP-08 inteiro.

## O que isto mantém aberto

Tailwind (v4 por plugin do Vite, ou outro) e a saída do CDN — WP-08. Content collections para o
legal — WP-09. Lighthouse CI — WP-12. Integrações (sitemap, imagens) entram quando um WP as
pedir. O que deixa de ser publicado (`/docs/*.md`, `/CLAUDE.md`, `/tools/`, `/design/`) pode
voltar a ser, por WP, se algum app ou ficha passar a citá-lo — hoje nenhum cita (busca nos
quatro repositórios em 2026-10-12: só `lottoexpert-privacy.html` e o convite).

## Onde olhar

`astro.config.mjs`, `package.json`, `.github/workflows/deploy.yml` e `pr.yml`,
`tools/check_site.py` (`CONTRATUAIS`, §4), ADR-001, D2, D5, D9, WP-07 e WP-08.
