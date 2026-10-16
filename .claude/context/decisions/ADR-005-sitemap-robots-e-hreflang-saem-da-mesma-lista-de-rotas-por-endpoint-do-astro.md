# ADR-005 · Sitemap, robots e hreflang saem da mesma lista de rotas, por endpoint do Astro

**Data:** 2026-10-15 · **Estado:** aceita · **Complementa:** ADR-001 (URLs contratuais) e
ADR-002 §2 (saída com caminho literal `.html`) · **Diverge de:** `docs/AVALIACAO.md` §3.2
("sitemap por integração") · **Depende de:** D8, D13, D16, D17, D18

## Contexto

Medido em 2026-10-15 (worktree de 9405cc2, Astro 7.3.8): com `build.format: 'preserve'`, o
`@astrojs/sitemap` 3.7.4 emite `/eclipsego` e `/en`, sem `.html` e sem barra, mas o canonical é
`/eclipsego.html` e `/en/`, e `/en` leva redirect no Pages. Ele também acrescenta 5 pacotes. O
hreflang já sai de `SITE`, `rota` e `COM_PAR_EN` (`src/i18n/ui.ts`). Um sitemap com outra lista
divergiria do canonical.

## Decisão

1. **Uma lista de rotas.** `src/pages/sitemap.xml.ts` e `src/pages/robots.txt.ts` são endpoints
   do Astro que leem `SITE`, `rota` e `COM_PAR_EN`, a mesma fonte do canonical e do hreflang do
   `Base.astro`. Não se usa `@astrojs/sitemap` nem `public/robots.txt`. A lista `PUBLIC` do §13
   do `check_site.py` não muda.
2. **Forma canônica da URL** (ADR-001, ADR-002 §2): `https://ghfsoftware.com` + caminho literal,
   ou seja, `/x.html`, `/` e `/en/`. O `<loc>` do sitemap, o canonical, o `og:url` e o `href` de
   todo hreflang são a mesma string.
3. **hreflang:** as 20 páginas com par têm `pt-BR`, `en` e `x-default` → en, recíprocos. Vale a
   D8 (c1) para TopoWalk e Pole Position e a D18 para home, LottoExpert e EclipseGo; o WP-15 passo
   1 generaliza pelo mapa de `idiomas.ts` sem mudar o valor.
4. **Indexação:** as 20 páginas são indexáveis e entram no sitemap. A 404 leva `noindex` e fica
   fora. O `robots.txt` é o literal `User-agent: *` / `Allow: /` / linha vazia /
   `Sitemap: https://ghfsoftware.com/sitemap.xml`, sem nenhum `Disallow`.
5. **Fora de toda regra de SEO:** o convite (`/lotto-expert/sweepstake-invite/lottoexpert-invite.html`)
   e `/.well-known/assetlinks.json`. Ficam fora do sitemap e sem `Disallow`, e o convite não ganha
   canonical, hreflang nem JSON-LD. O sha256 de `tools/contrato.sha256` não muda (D13). O
   `check_site.py` lista o convite em `CONGELADAS`, a mesma lista do contrato.
6. **JSON-LD** sai de um único módulo de dados (`src/i18n/apps.ts`), o mesmo que alimenta o botão
   da Play. `Organization` na home; `MobileApplication` nas landings, só com `name`,
   `operatingSystem`, `applicationCategory`, `installUrl` e `offers`. A `applicationCategory` é o
   enum do schema.org/Google, mapeado da categoria da ficha da Play (D17): TOOLS →
   `UtilitiesApplication`, SPORTS → `SportsApplication`, LIFESTYLE → `LifestyleApplication`.
   `offers` só com preço 0 BRL; nunca preço do Premium nem `aggregateRating`/`review`.
7. **og:image** declara o tamanho real do arquivo, ou omite `width`/`height`, até as imagens
   1200×630 da D16 existirem. O `check_site.py` barra declaração diferente do arquivo.

## O que isto fecha

`@astrojs/sitemap` e qualquer `serialize` que reescreva URL; `public/robots.txt`; URL sem `.html`
ou `/en` sem barra em qualquer metadado; `Disallow` de qualquer caminho; convite ou
`assetlinks.json` no sitemap; `x-default` → pt; `applicationCategory` com o texto cru da Play
(`TOOLS`). Voltar ao integration custa trocar 2 endpoints por config, mais 5 pacotes e um
`serialize` que repete a lógica do `rota`.

## O que isto mantém aberto

As línguas além do en (WP-15..18): os endpoints trocam `COM_PAR_EN` pelo mapa de `idiomas.ts`
num só lugar. Um sitemap-índice, se o site passar de algumas centenas de URLs. Novos campos do
JSON-LD (`sameAs`, `screenshot`) em WP próprio, com fonte. As imagens 1200×630 (D16), em WP
próprio. Um app que mude de categoria ou deixe de ser gratuito muda uma linha de `apps.ts`.

## Onde olhar

`src/pages/sitemap.xml.ts`, `src/pages/robots.txt.ts`, `src/layouts/Base.astro`,
`src/components/JsonLd.astro`, `src/i18n/ui.ts` (`SITE`, `rota`, `COM_PAR_EN`),
`src/i18n/apps.ts`, `tools/check_site.py` §14 (`CONGELADAS`, `INDEXAVEIS`),
`tools/contrato.sha256`; `decisoes.md` D8, D13, D16, D17, D18; ADR-001, ADR-002; WP-11, WP-15.
