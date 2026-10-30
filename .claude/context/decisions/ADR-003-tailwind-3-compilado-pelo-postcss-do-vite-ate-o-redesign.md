# ADR-003 · O Tailwind é a v3.4 compilada pelo PostCSS do Vite até o redesign, com a cor de cada página em variável CSS

**Data:** 2026-10-13 · **Estado:** aceita · **Origem:** D2 e ADR-002 deixaram versão e forma de
integração do Tailwind para o WP-08

## Contexto

As 10 páginas carregam `https://cdn.tailwindcss.com` (Play CDN, linha v3, JIT no navegador) com
um `tailwind.config` inline de sintaxe v3 em cada uma. Os mesmos nomes têm valores diferentes por
página: `brand.primary` é `#10B981` em `index.html`, `#8B5CF6` nas três do LottoExpert, `#84cc16`
nas duas do Pole Position, `#EAB308` nas duas do EclipseGo, `#10B981` em `topowalk.html` e
`#B5541C` em `topowalk-privacy.html`; `brand.accent` difere entre `poleposition.html` (`#a3e635`)
e `poleposition-privacy.html` (`#06B6D4`) — 7 configurações em 10 páginas (`NAV-FOOTER-DERIVA-01`).
O WP-08 exige "sem mudança visual intencional", provado por captura antes/depois.

## Decisão

1. **`tailwindcss` 3.4.19** (tag `v3-lts` no npm em 2026-10-13), `postcss` e `autoprefixer`
   fixados exatamente em `devDependencies`, compilados pelo PostCSS que o Vite do Astro já roda
   (`postcss.config.mjs` + `tailwind.config.mjs` na raiz). **Sem integração do Astro** — a
   `@astrojs/tailwind` está descontinuada. Medido em 2026-10-13 (spike fora do repositório,
   Astro 7.3.8, Vite 8.3.4): sai um único `/_astro/*.css` ligado em `index.html` e
   `en/index.html`; classe literal em `<script>` de `.astro` (`classList.add('opacity-0')`)
   entra no CSS.
2. **Uma configuração, cores por variável.** `brand.*` no `tailwind.config.mjs` é
   `rgb(var(--brand-<nome>) / <alpha-value>)`; os valores vivem em `src/styles/global.css`, um
   bloco por tema (`[data-tema="lottoexpert"] { --brand-primary: 139 92 246 }`), e o layout recebe
   `tema` e o põe no `<html>`. Os temas reproduzem as 7 configurações medidas, **inclusive as
   divergências** entre landing e política do mesmo app — unificá-las é design (WP-10, D4). Medido
   no spike: `bg-brand-primary/20` sai `rgb(var(--brand-primary) / .2)`.
3. `content` do Tailwind cobre `src/**/*.{astro,md,mdx,ts}`. Classe montada por concatenação
   de string não é detectada (a Play CDN detectava, porque observa o DOM): é proibida; o que não
   puder ser literal vai para `safelist`, com comentário do porquê.
4. O minificador de CSS do Vite 8 (lightningcss) reescreve a saída — no spike,
   `backdrop-filter` saiu sem `-webkit-` mesmo com `autoprefixer`. Paridade é provada por captura
   (360/1280, `site-ux`), não suposta; regressão em navegador antigo vira achado com o navegador
   nomeado. Na fatia 1 do WP-08, `vite.build.cssTarget` explícito em `astro.config.mjs`
   (`chrome87, edge88, firefox78, safari14`) faz o minificador manter `-webkit-backdrop-filter`
   ao lado de `backdrop-filter`; sem ele, o vidro do `.glass-panel` sumia em um dos motores.

## O que isto fecha

Tailwind v4 no WP-08: o piso de navegador sobe (Safari 16.4, Chrome 111, Firefox 128 — usa
`@property`, `color-mix()` e `@layer`) e os padrões mudam (cor de borda, largura do `ring`,
escalas de `shadow`/`rounded`/`blur` renomeadas), o que torna "sem mudança visual" improvável de
provar. A Play CDN em qualquer página gerada. Um `tailwind.config` por página. Voltar atrás custa
pouco: a configuração é um arquivo e as classes nas páginas são as mesmas.

## O que isto mantém aberto

Tailwind v4 (`@tailwindcss/vite`, tema em CSS com `@theme`) no WP-10, quando o markup é reescrito
com os tokens do handoff (D4) — ADR que substitui este. Fontes self-hosted e ícones no lugar do
Font Awesome continuam no WP-12; o CDN do Font Awesome e o Google Fonts saem do WP-08 só como
**uma** ocorrência no layout, não mais dez. O convite do bolão é copiado byte a byte e não usa
este CSS.

## Onde olhar

`tailwind.config.mjs`, `postcss.config.mjs`, `src/styles/global.css`, `src/layouts/Base.astro`
(prop `tema`), `package.json`; ADR-002 §3; WP-08 (fatia 1), WP-10, WP-12.
