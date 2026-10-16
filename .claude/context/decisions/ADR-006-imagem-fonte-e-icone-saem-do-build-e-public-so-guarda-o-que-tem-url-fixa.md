# ADR-006 · Imagem, fonte e ícone saem do build do Astro; `public/assets/` só guarda o que tem URL fixa

**Data:** 2026-10-16 · **Estado:** aceita · **Origem:** WP-12 (veredito do arquiteto) ·
**Complementa:** ADR-001 (URLs contratuais), ADR-002 §3 (`public/` byte a byte), ADR-003 (o que
o WP-12 herdou do WP-08) · **Depende de:** D13 (convite congelado), D16 (og:image 1200×630 é do WP-20)

## Contexto

Linha de base do WP-12 (Lighthouse 13.5.0 mobile, 3 runs, mediana, `dist/` servido local sem
gzip): performance 65 na home e 70 no LottoExpert, LCP 16 s e 15 s. A home baixa 3,8 MB, quase
tudo PNG/JPEG de `public/assets/` exibido em tamanho menor (9 logos 500×500 de ~250 KB exibidos a
48 px); nenhuma `<img>` tem `width`/`height`/`loading`. Bloqueiam o render Google Fonts (Inter em
6 pesos, ~830 ms) e o Font Awesome 6.4.0 inteiro do cdnjs (~1 s, 253 KB de woff2 para 90 ícones).

## Decisão

1. **Imagem renderizada passa pelo `astro:assets`.** Toda `<img>` de página gerada é `<Image>`
   (ou `getImage()`) de `astro:assets` sobre um arquivo importado de `src/assets/img/`: o Astro
   emite WebP em `/_astro/<nome>.<hash>.webp`, com `width`/`height` do arquivo, `srcset` por
   densidade (`densities={[1, 2]}`, para o que tem tamanho fixo em CSS) ou por largura
   (`widths` + `sizes`, para o que é fluido), `loading="lazy"` e `decoding="async"` por padrão. O
   elemento LCP de cada página — medido, não suposto — leva `loading="eager"` e
   `fetchpriority="high"`; no máximo um por página. O favicon das páginas geradas também sai por
   `getImage()` (PNG 48 px), não do PNG de 296–516 KB. Só WebP: AVIF dobra o markup
   (`<Picture>`) e o tempo de build sem mudar a nota nesta escala. O codificador é o `sharp`
   0.35.5, dependência opcional do `astro` já no `package-lock.json`: nenhum pacote novo. Sem
   `sharp` instalado o build falha, não cai para imagem sem otimizar.
2. **`public/assets/` guarda só arquivo servido por URL fixa:** `og:image` (o `Base.astro` lê o
   tamanho do arquivo em `public/`), o `logo` do JSON-LD, e tudo o que o convite do bolão carrega
   (`lottoexpert_app_mockup.png`, `lottoexpert.png`, `lottoexpert_favicon_v3.png`,
   `lottoexpert/*.png`). Esses arquivos ficam no caminho e nos bytes de hoje; o
   `lottoexpert_app_mockup.png` está em `tools/contrato.sha256` (D13). Um arquivo pode existir nos
   dois lugares com papéis diferentes: a cópia de `src/assets/img/` é a que a página exibe; a de
   `public/assets/` é a que uma URL externa (app, WhatsApp, buscador) pede. Página gerada não tem
   `<img src="/assets/…">`; `check_site.py` passa a cobrar.
3. **Inter é servida pelo próprio site, pela API `fonts` do Astro** (`fontProviders.local()`,
   estável no Astro 7): um woff2 variável, eixo `wght` 400–800, `opsz` fixo em 14, subconjunto
   latino (o `unicode-range` "latin" do Google Fonts + U+2192 `→`, que as páginas usam), em
   `src/assets/fonts/`, com a licença OFL ao lado. Origem: `InterVariable.woff2` 4.001 (rsms/inter)
   do handoff (`design/handoff/2026-10-13-rodada-3/fonts/`). O comando do recorte (fontTools,
   fora do CI) fica no comentário do `astro.config.mjs`; medido em 2026-10-16: 24,9 KB. O
   `<Font preload>` no `<head>` do `Base.astro` faz o preload, e o fallback com métricas ajustadas
   (`size-adjust`) que o Astro gera é o que segura o CLS do swap. Pesos 300 e 900 ficam fora: o
   CSS compilado usa 400, 500, 600, 700 e 800 (`font-weight` em `dist/_astro/*.css`; nenhum
   `font-light` em `src/`). Nada em `public/fonts/`: a lista fechada de `public/` (§13) não muda.
4. **Ícone é SVG inline**, por `src/components/Icon.astro`, a partir de arquivos copiados de
   `@fortawesome/fontawesome-free@6.4.0/svgs/{solid,brands}/` (a mesma versão de hoje, ícones
   sob CC BY 4.0) para `src/icons/fa/`, com o comentário de licença que cada arquivo já traz. A
   cópia tem só os ícones usados; o pacote não entra no `package.json`. Nome inexistente em
   `src/icons/fa/` falha o build. O `<svg>` sai com `aria-hidden="true"`, `fill="currentColor"`,
   altura `1em` e o `viewBox` do arquivo, para herdar a cor e o tamanho de texto do pai como o
   glifo fazia. Os nomes são os canônicos do FA 6 (`clock-rotate-left`, não o apelido
   `history`).
5. **Terceiro no `<head>` de página gerada:** nenhum. O convite fica de fora (D13) até o WP que o
   mudar com teste de link real (ADR-001).

## O que isto fecha

Manter imagem renderizada em `public/` com variantes geradas por script próprio. `@fontsource/*`
ou Google Fonts. Font Awesome por CDN, por kit ou pelo pacote npm inteiro. AVIF neste WP. Voltar
atrás custa pouco por item: as imagens originais seguem no repositório, e a fonte e os ícones são
arquivos.

## O que isto mantém aberto

A família de ícones do redesign (WP-10, D4): o `Icon.astro` aceita outra pasta de SVG sem mudar
quem o chama. JetBrains Mono ou outra fonte de exibição, pela mesma API `fonts`, se o handoff
pedir. AVIF, se a medição pedir. A troca das og:image pelas 1200×630 (WP-20, D16); com ela, as
cópias em `public/assets/` que só existiam como og:image podem sair. O convite sem terceiros
(pako e Inter locais), num WP que aceite mudar `tools/contrato.sha256`.

## Onde olhar

`astro.config.mjs` (`fonts`), `src/layouts/Base.astro`, `src/components/Icon.astro`,
`src/assets/img/`, `src/assets/fonts/`, `src/icons/fa/`, `tools/check_site.py` (§15), `public/assets/`,
`tools/contrato.sha256`; WP-12, WP-10, WP-20.
