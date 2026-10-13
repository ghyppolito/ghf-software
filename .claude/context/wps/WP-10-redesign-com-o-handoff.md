---
id: WP-10
titulo: A home e as landings de app seguem o sistema visual do handoff
area: design
status: todo
depende_de: [WP-06, WP-08]
adr: []
spec: docs/AVALIACAO.md
decisoes: [D4]
tamanho: L
risco: medio
visual: true
branch: feat/wp-10-redesign
---

# WP-10 — A home e as landings de app seguem o sistema visual do handoff

**Depende de:** WP-06 (handoff), WP-08 (componentes únicos) · **Achados roteados:** LOGO-ANO-E-FUNDO-ESCURO-01, DESIGN-RODADA-3-01

**Objetivo:** tokens do handoff em `tailwind.config.mjs`; home com hierarquia por app (um
toque até o app certo); as 4 landings com a mesma anatomia (hero + CTA → 3–5 funcionalidades
com imagem real → prova → privacidade em uma frase → FAQ → CTA); página legal legível (largura
de leitura, sumário, data no topo).

**Contexto:** `docs/AVALIACAO.md` §2 item 7 e §3.3.

**Ler antes:** `design/README.md` (mapa do handoff) e só os componentes do handoff que a
página usa; `docs/AVALIACAO.md` §3.3.

**Arquivos-alvo:** `tailwind.config.mjs`, `src/components/**`, `src/layouts/**`,
`src/pages/**` (pt e en), `public/assets/**` (imagens novas, otimizadas se o WP-12 já passou).

**Passos:** por página: `site-ux` DESENHAR (referência no handoff, estados) → `site-dev` →
`/verify` → auditoria (`site-ux` AUDITAR + `site-qa` + `site-seo-perf`). Home por último, com
as landings prontas.

**Critérios de aceite:**
- Tokens: nenhuma cor literal (`#…`, `rgb(`) em `src/` fora de `tailwind.config.mjs`
  (`grep -rnE "#[0-9a-fA-F]{3,6}\b|rgb\(" src/ | grep -v tailwind.config` vazio).
- Cada landing tem exatamente as seções da anatomia, na ordem (`site-ux` AUDITAR confere
  contra o handoff e lista desvios com justificativa).
- Contraste AA em todo texto (relato do `site-ux` com os pares cor/fundo medidos).
- `check_site.py` verde; Lighthouse Accessibility ≥ 95 em todas as páginas.

**Só no navegador:** todas as páginas, 360/768/1280, pt e en, contra o handoff.

**Risco:** médio — visual. Sem handoff (WP-06 não feito), D4 (B) muda o WP: a referência passa
a ser `docs/AVALIACAO.md` §3.3 e o `site-ux` decide mais do que deveria — registrar.
