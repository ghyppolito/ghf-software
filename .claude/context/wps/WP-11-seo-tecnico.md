---
id: WP-11
titulo: Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página
area: seo
status: todo
depende_de: [WP-08]
adr: []
spec: docs/AVALIACAO.md
decisoes: []
tamanho: M
risco: baixo
visual: false
branch: feat/wp-11-seo-tecnico
---

# WP-11 — Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página

**Depende de:** WP-08 · **Achados roteados:** `LEGAL-SEM-OG-01`

**Objetivo:** `sitemap-index.xml` e `robots.txt` gerados no build; `<link rel="canonical">` e
`hreflang` pt-BR/en/x-default em toda página; JSON-LD `Organization` na home e
`MobileApplication` (nome, `operatingSystem: Android`, `applicationCategory`, link da Play,
`offers`) em cada landing; `og:*`/Twitter completos em todas as páginas, inclusive legais.

**Contexto:** `docs/AVALIACAO.md` §1 (SEO) e §2 item 6.

**Ler antes:** `docs/AVALIACAO.md` §1; integração `@astrojs/sitemap`; schema.org
`MobileApplication` (só as propriedades acima).

**Arquivos-alvo:** `astro.config.mjs`, `src/layouts/Base.astro` (`<head>`),
`src/components/Seo.astro`, `src/components/JsonLd.astro`, `public/robots.txt`,
`tools/check_site.py` (§2 passa a exigir canonical/hreflang).

**Critérios de aceite:**
- `test -f dist/sitemap-index.xml` e `robots.txt` com `Sitemap:`.
- `grep -L 'rel="canonical"' dist/**/*.html` vazio; idem `hreflang`.
- JSON-LD válido: `python3 -c` que extrai cada `<script type="application/ld+json">` e faz `json.loads` sem erro;
  `@type` esperado por página.
- `check_site.py` passa a exigir `og:image` em **todas** as páginas (regra promovida de aviso a erro neste WP).
- Validação no Rich Results Test do Google para a home e uma landing: captura no WP (usuário).

**Risco:** baixo.
