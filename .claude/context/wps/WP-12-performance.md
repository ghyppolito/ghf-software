---
id: WP-12
titulo: Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile
area: seo
status: todo
depende_de: [WP-08]
adr: []
spec: docs/AVALIACAO.md
decisoes: []
tamanho: M
risco: baixo
visual: true
branch: feat/wp-12-performance
---

# WP-12 — Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile

**Depende de:** WP-08 (o CDN do Tailwind já saiu lá) · **Achados roteados:** —

**Objetivo:** fontes self-hosted (Inter, subset latin, `font-display: swap`), ícones SVG
inline no lugar do Font Awesome, imagens em WebP/AVIF com `width/height` e `srcset` via
`<Image>` do Astro, hero com `fetchpriority="high"`, e Lighthouse CI no PR com orçamento.

**Contexto:** `docs/AVALIACAO.md` §2 item 4; baseline a medir no passo 0 (`site-seo-perf`),
antes de qualquer mudança — sem número de partida o WP não começa.

**Ler antes:** `docs/AVALIACAO.md` §2.4; `@astrojs/image`/`astro:assets`; `@lhci/cli` com
`lighthouserc.json`.

**Arquivos-alvo:** `src/layouts/Base.astro`, `src/components/Icon.astro`, `public/fonts/`,
`src/assets/**` (imagens movidas para serem processadas), `lighthouserc.json`,
`.github/workflows/pr.yml` (job `lighthouse`).

**Critérios de aceite:**
- Tabela antes/depois por página (4 notas + LCP/CLS/TBT), mobile, no WP.
- ≥ 90 nas 4 categorias em todas as páginas; CLS ≤ 0,1; LCP ≤ 2,5 s em `dist/` servido local.
- `grep -rc "fonts.googleapis\|font-awesome\|cdnjs" dist | grep -v ":0"` vazio.
- `lighthouserc.json` com `assertions` de orçamento e o job verde no PR.

**Só no navegador:** ícones e fontes iguais aos de antes (comparação de captura).

**Risco:** baixo.
