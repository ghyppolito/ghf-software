---
id: WP-20
titulo: Imagens de compartilhamento 1200×630 por página e twitter:card coerente
area: design
status: todo
depende_de: [WP-11]
adr: [ADR-005]
spec: docs/AVALIACAO.md
decisoes: [D16]
tamanho: M
risco: baixo
visual: true
branch: feat/wp-20-imagens-de-compartilhamento
---

# WP-20 — Imagens de compartilhamento 1200×630 por página e twitter:card coerente

**Depende de:** WP-11 · **Achados roteados:** `OG-IMAGE-1200-PRODUCAO-01`, `TWITTER-CARD-IMAGEM-QUADRADA-01`, `OG-IMAGE-ALT-TYPE-01`, `ORG-LOGO-NAO-QUADRADO-01`, `OG-MOCKUP-JPEG-PESADO-01` (og:image; a parte exibida saiu no WP-12)

**Objetivo:** a home, as 10 legais e as 4 landings (pt e en) compartilham uma imagem 1200×630 de verdade, e as tags
`og:image:*`/`twitter:*` descrevem exatamente essa imagem.

**Contexto:** D16 (A). O WP-11 só declarou o tamanho real das imagens atuais (nenhuma é 1200×630) e o `check_site.py` §14
barra declaração falsa. As landings usam imagem quadrada (1024×1024) com `twitter:card: summary_large_image`, que o X corta
para 2:1. O `logo` do `Organization` (`src/i18n/apps.ts`) é `GHFSoftware.png`, 677×369, e o Google prefere logo quadrado.

**Ler antes:** ADR-005; D16 em `decisoes.md`; `src/layouts/Base.astro` (og e twitter); `src/i18n/apps.ts`.

**Arquivos-alvo:** `assets/` (5 imagens novas + logo quadrado), `src/layouts/Base.astro`, `src/i18n/apps.ts`,
`src/i18n/*.ts` (alt por página), `tools/check_site.py`. Fora: `assets/lottoexpert_app_mockup.png` e o og do convite (D13).

**Passos:**
1. **Usuário:** sessão no Claude Design com o handoff: 1 imagem da marca GHF (home e legais) e 1 por app, 1200×630, ≤ 300 KB,
   mais um logo quadrado. Export em `design/handoff/<data>/`.
2. Agente: copiar para `assets/`, apontar `Base.astro` e `apps.ts`, declarar width/height reais e `og:image:type`.
3. Agente: `og:image:alt` e `twitter:image:alt` por página, pt e en; `twitter:card` coerente com a proporção da imagem.
4. Agente: `check_site.py` passa a exigir 1200×630, ≤ 300 KB e `alt` presente.

**Critérios de aceite:**
- `python3 tools/check_site.py` verde, com a regra nova de 1200×630 e peso.
- `sha256sum -c tools/contrato.sha256` verde (convite e mockup intactos).
- `og:image:alt` e `og:image:type` em toda página fora de `CONGELADAS`.
- Preview no navegador e no WhatsApp: ver abaixo.

**Só no navegador:** a arte (sessão do usuário) e o preview de um link de landing no WhatsApp/X, depois do deploy único (D13).

**Risco:** baixo. Nenhuma URL contratual muda.
