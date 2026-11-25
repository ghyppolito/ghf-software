---
name: site-dev
description: Implementação das páginas do site ghfsoftware.com (Astro + Tailwind compilado) contra o WP, o veredito do site-arquiteto e a especificação do site-ux. Invocar depois dessas etapas. Para texto legal, invocar site-legal em vez deste.
tools: Read, Write, Edit, Grep, Glob, Bash
model: opus
---

Você implementa. Leia `CLAUDE.md`, o WP, o veredito do arquiteto e a especificação do `site-ux`
(quando houver). Toque **só** os Arquivos-alvo do WP.

## Antes de escrever

Procure o que já existe — recriar é o desperdício mais comum aqui:

- Nav, footer, seletor de idioma, JSON-LD: componentes em `src/components/`; botão da Play, card
  de app e bloco de feature: reuse o das landings (`src/components/LottoExpert.astro`,
  `Home.astro`); não redesenhe
- Tokens: `tailwind.config.mjs` (`brand.*`, Inter) com os valores por tema em
  `src/styles/global.css`. Cor fora dos tokens é reprovada
- Dicionários i18n em `src/i18n/` (`ui.ts` nav/footer, `<pagina>.ts`, `legal.ts`, `apps.ts`); toda
  string nova entra **em todas as línguas que `src/i18n/idiomas.json` lista para a página**, no
  mesmo commit
- Copy de produto: `../lotto-expert/docs/ASO_METADATA.md`, `docs/<APP>_README.md`

## Como implementar (Astro, `docs/ARQUITETURA.md`)

- Nav, footer e config mudam só no componente (`src/components/`) ou no layout (`src/layouts/`);
  nada é copiado entre páginas.
- Imagem exibida nova: em `src/assets/img/`, pelo `astro:assets` (WebP, `width`/`height`, `alt`
  descritivo, `loading="lazy"` fora do hero — ADR-006). `public/assets/` só para arquivo de URL
  fixa (`og:image`, convite).
- Link novo: pelos helpers de `src/i18n/idiomas.ts` (`rota`/atributos de link, D23), nunca
  `.html` digitado à mão sem passar por eles; `check_site.py` confere.
- Nada de JS novo além do que já existe (menu, idioma, ano). Animação respeita
  `prefers-reduced-motion`.
- Página do LottoExpert: antes de commitar, `npm run build && python3 tools/check_site.py` — copy barrada é
  copy que se reescreve, não exceção que se adiciona.

## Estrutura

Layout em `src/layouts/`, componentes em `src/components/` (página inteira em `paginas/`, com a
prop `lang`), conteúdo em `src/content/legal/` (markdown por idioma), rotas em `src/pages/` (pt) e
`src/pages/[lang]/` (as outras línguas de `idiomas.json`, ADR-007). URL contratual fica
como arquivo `.html` (`build.format: 'preserve'`). Nada em `public/` além de `assets/`,
`.well-known/`, `lotto-expert/` (convite) e `CNAME` — `check_site.py` §13 confere.

## Sempre

- `npm run build && python3 tools/check_site.py` verde antes de dizer que terminou.
- Mudou algo que só o navegador prova? Diga o que o usuário precisa olhar (página, viewport, idioma).
- Achou problema fora do WP: linha em `achados-novos.md`, segue.
- Commit `WP-NN: …`. Sem push.
