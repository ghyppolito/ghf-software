---
id: WP-12
titulo: Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile
area: seo
status: doing
depende_de: [WP-08]
adr: [ADR-006]
spec: docs/AVALIACAO.md
decisoes: [D20]
tamanho: L
risco: medio
visual: true
branch: feat/wp-12-performance
---

# WP-12 — Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile

**Depende de:** WP-08 (o CDN do Tailwind já saiu lá) · **Achados roteados:** OG-MOCKUP-JPEG-PESADO-01, ASSETS-PESO-01, INVITE-PAKO-CDNJS-01, ASSETS-PNG-LCP-01, IMG-ATRIBUTOS-FONTES-01, TOPO-CLS-HERO-01, POLE-JETBRAINS-SEM-USO-01, CONVITE-FORA-DO-WP-12-01 (destino de cada um no veredito)

**Objetivo:** fontes self-hosted (Inter, subset latin, `font-display: swap`), ícones SVG
inline no lugar do Font Awesome, imagens em WebP/AVIF com `width/height` e `srcset` via
`<Image>` do Astro, hero com `fetchpriority="high"`, e Lighthouse CI no PR com orçamento.

**Contexto:** `docs/AVALIACAO.md` §2 item 4; baseline a medir no passo 0 (`site-seo-perf`),
antes de qualquer mudança — sem número de partida o WP não começa.

**Ler antes:** `docs/AVALIACAO.md` §2.4; `@astrojs/image`/`astro:assets`; CLI do `lighthouse`
13.5.0 (D20 B).

**Arquivos-alvo:** (fechados pelo veredito do arquiteto, 2026-10-16; ADR-006)
- remoção: `public/assets/lottoexpert_favicon_v2.png`, `public/assets/poleposition_dashboard_mockup.png`,
  `public/assets/poleposition_favicon.png`, `public/assets/topowalk_favicon.png`
- fontes: `src/assets/fonts/inter-latin-wght.woff2`, `src/assets/fonts/OFL.txt`,
  `astro.config.mjs` (`fonts`), `tailwind.config.mjs` (`fontFamily.sans`)
- ícones: `src/icons/fa/{solid,brands}/*.svg`, `src/icons/fa/LICENSE.txt`, `src/components/Icon.astro`
- imagens: `src/assets/img/**` (cópias das imagens exibidas por `<img>`; os originais de
  `public/assets/` ficam)
- markup: `src/layouts/Base.astro`, `src/layouts/LegalLayout.astro`, `src/components/{Nav,Footer,
  Home,LottoExpert,TopoWalk,PolePosition,EclipseGo,TrocaIdioma}.astro`, `src/styles/global.css`,
  `src/pages/poleposition.astro`, `src/pages/en/poleposition.astro` (`fontesExtras`),
  `src/pages/lottoexpert-terms.astro`, `src/pages/en/lottoexpert-terms.astro` (`iconeSelo`)
- guarda: `tools/check_site.py` (§15 novo)
- Lighthouse no CI (D20 decidida: B): `package.json` e `package-lock.json` (`lighthouse` 13.5.0
  exato em `devDependencies`), `tools/lighthouse.py`, `tools/orcamento-lighthouse.json`,
  `.github/workflows/pr.yml` (job `lighthouse`).

Fora da lista, de propósito: `public/lotto-expert/**`, `public/.well-known/**`, `public/CNAME`,
`tools/contrato.sha256`, `.github/workflows/deploy.yml`, `.htmlvalidate.json`, `public/fonts/`.

**Critérios de aceite:** (régua fixada no veredito)
- Tabela antes/depois no WP, das 21 páginas (20 indexáveis + 404): 4 notas + LCP/CLS/TBT/FCP +
  KB, Lighthouse 13.5.0 mobile, 3 runs, mediana pela nota de performance, `dist/` servido por
  `python3 -m http.server -d dist` (sem gzip, o mesmo servidor da linha de base).
- 20 indexáveis: performance, acessibilidade, boas práticas e SEO ≥ 90 na mediana; LCP ≤ 2,5 s;
  CLS ≤ 0,1. 404: performance, acessibilidade e boas práticas ≥ 90; SEO isenta, e a única
  auditoria de SEO reprovada é `is-crawlable` (`noindex` de propósito, ADR-005 §4). O convite
  fica fora da medição (D13).
- `grep -rlE "fonts\.googleapis|fonts\.gstatic|font-awesome|cdnjs" dist | grep -vx 'dist/lotto-expert/sweepstake-invite/lottoexpert-invite.html'`
  vazio.
- `check_site.py` §15 verde: nenhum `<link>`/`<script>` de outra origem nas páginas geradas,
  toda `<img>` com `width` e `height`, nenhuma `<img src="/assets/…">` nem `class="fa-` fora do
  convite.
- `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` verde; `public/assets/` sem os 4
  órfãos e com todo o resto byte a byte.
- Job `lighthouse` verde no PR (D20 B).

**Só no navegador:** capturas antes/depois (360 e 1280, pt) da home, das 4 landings, de uma
legal e da 404, nos commits de fonte, ícones e imagens: ícones no mesmo lugar, tamanho e cor;
texto sem salto de linha a mais; imagens nítidas em tela 2×. O menu do celular abre e fecha com o
ícone trocando. O usuário confere as capturas.

**Risco:** médio. Muda o `<body>` das 21 páginas (ícones e imagens) e a fonte de todas. O que
pode dar errado: ícone com alinhamento vertical diferente do glifo; quebra de linha nova pela
métrica da fonte recortada; imagem LCP com `loading="lazy"`; o recorte sem um glifo usado.

## Veredito do arquiteto (2026-10-16)

**Aprovado com mudanças**, já aplicadas no cabeçalho e nas seções acima: ADR-006, `tamanho: L`,
`risco: medio`, Arquivos-alvo fechados, régua da 404 explícita e exceção do convite no critério
de CDN. Os commits 1 a 5 não dependem de nenhuma decisão em aberto. D20 e D21 foram decididas
em 2026-10-16 ("pode seguir o recomendado"): D20 (B) e D21 (C). Ver §8.

**Guarda.** (1) URL contratual: nenhuma muda. O convite, o `assetlinks.json`, o
`lottoexpert_app_mockup.png` e o `CNAME` ficam fora da lista, e o `contrato.sha256` roda em todo
commit. (2) Fonte única: a Inter vem do handoff (D4), e os ícones vêm do FA Free 6.4.0, que é a
versão publicada hoje. Nada é digitado à mão. (3) Réplica: não há. Nav, footer e head só mudam no
componente. (4) Deploy: `deploy.yml` e `CNAME` ficam intocados, e `pr.yml` ganha um job que não
publica nada. (5) i18n: nenhum texto novo. (6) Nenhum rastreador; D3 não se aplica.

### 1. Imagens: `astro:assets`, com `public/assets/` só para URL fixa (ADR-006 §1–2)
- `sharp` 0.35.5 já está no lockfile, como `optionalDependencies` do `astro` 7.3.8
  (`package-lock.json`, `node_modules/astro`), e `require('sharp')` funciona. Sem ele, o build
  para com `MissingSharp` (`node_modules/astro/dist/assets/services/sharp.js:57`). O
  `package.json` não muda.
- Ficam em `public/assets/`, nos mesmos bytes:
  - as og:image atuais: `GHFSoftware`, `eclipse-go`, `lottoexpert_app_mockup`,
    `poleposition_real_mockup` e `topowalk_screenshot`;
  - os favicons apontados hoje;
  - tudo o que o convite carrega (`lottoexpert_app_mockup`, `lottoexpert`,
    `lottoexpert_favicon_v3` e as 9 de `lottoexpert/`).
- O que a página exibe passa a sair de uma cópia em `src/assets/img/`. As cópias somam 6,2 MB
  no git (medido; o veredito estimou ≈ 3,5 MB, ver §10), e esse custo é aceito para que a URL externa não mude.
- Formato WebP. `densities={[1, 2]}` para o que tem tamanho fixo (logos de 48 px, ícone da nav).
  `widths` + `sizes` para mockup fluido. `fetchpriority="high"` + `loading="eager"` só no
  elemento LCP medido de cada página; a logo da nav é sempre `eager`.
- Favicon das páginas geradas por `getImage()`, em PNG de 48 px. Hoje o
  `lottoexpert_favicon_v3.png` de 296 KB está entre os 3 maiores recursos de toda legal do
  LottoExpert.
- A og:image continua de `public/` e é do WP-20 (D16). O `.png` que é JPEG, nas og:image das
  landings, vai junto (`OG-MOCKUP-JPEG-PESADO-01` → WP-20; no convite, congelado por D13).

### 2. Fontes: Inter local pela API `fonts` do Astro; a JetBrains sai (ADR-006 §3)
- Os pesos que o CSS compilado usa são 400, 500, 600, 700 e 800: há `font-weight` 400, 500, 600,
  700 e 800 em `dist/_astro/Base.poFuGAu4.css`, e nenhum `font-light` em `src/`. O 300 sai.
- O arquivo é o `InterVariable.woff2` 4.001 do handoff (OFL), recortado em `wght` 400–800,
  `opsz` 14, faixa latina + U+2192: 33,7 KB com as features padrão (o veredito mediu 24,9 KB; ver §10). O único caractere fora da faixa latina em
  `dist/` é o `⭐` do LottoExpert, que vem da fonte de emoji.
- Não entra `@fontsource`: seria pacote novo, decisão de stack, para fazer o que a API `fonts`
  do Astro 7 já faz. Também não entra `public/fonts/`: abriria a lista fechada do §13 e exigiria
  `@font-face` e métricas de fallback escritos à mão.
- `<Font cssVariable="--fonte-inter" preload />` no `Base.astro`. O fallback com `size-adjust` é
  gerado pelo Astro (`optimizedFallbacks`, padrão) e resolve `TOPO-CLS-HERO-01`.
- A JetBrains Mono sai: nenhum elemento das duas páginas do Pole Position usa `font-mono`
  (`grep -c font-mono dist/poleposition.html` = 0). Saem com ela a prop `fontesExtras` do `Base`
  e a linha `--fonte-mono` do tema `poleposition` em `global.css:69`. Não muda nada visível, então
  não é decisão de design (`POLE-JETBRAINS-SEM-USO-01`).

### 3. Ícones: `Icon.astro` com SVG inline, copiado do FA Free 6.4.0 (ADR-006 §4)
- São 91 nomes em `src/`, não ~10: 77 `solid` e 14 `brands`. Três são apelidos e viram o nome
  canônico: `history` → `clock-rotate-left`, `sync` → `arrows-rotate`, `drafting-compass` →
  `compass-drafting`.
- `fa-wifi-slash` (`EclipseGo.astro:28`) **não existe no FA Free 6.4.0**: o card 1 do EclipseGo
  sai hoje sem ícone. Isso vira a D21.
- Os SVG são cópia (`npm pack @fortawesome/fontawesome-free@6.4.0` fora do repositório, copiando
  só os usados), sem pacote. O comentário de licença CC BY 4.0 de cada arquivo vai junto, e
  `LICENSE.txt` fica em `src/icons/fa/`.
- Os ícones montados em dicionário (`fundo`/`icone` em LottoExpert, PolePosition, TopoWalk,
  EclipseGo, Footer, `iconeSelo` do LegalLayout) passam a `{ conjunto, nome }`.
- O menu do `Nav.astro:179-183` troca `classList` `fa-bars`/`fa-xmark`. Passa a renderizar os
  dois SVG e alternar `hidden`.
- O SVG inline precisa passar no html-validate com as regras de hoje. Se não passar, parar e
  reportar: `.htmlvalidate.json` não está na lista, e o §13 trava as regras.

### 4. Órfãos: apagar os 4
- `lottoexpert_favicon_v2`, `poleposition_dashboard_mockup`, `poleposition_favicon` e
  `topowalk_favicon` (1,98 MB) não são referenciados por:
  - nenhuma página de `dist/`, nem pelo convite (`uso.txt` do site-seo-perf);
  - nenhum arquivo de `origin/master` (`git grep`);
  - os repositórios dos 4 apps. A única URL do site neles é `ghfsoftware.com/logo_transp.png`,
    em `../lotto-expert/lottoexpert-invite.html`, que é uma cópia antiga do convite.
- A loja não aponta para arquivo de `assets/`.
- O handoff cita `pole_dashboard_mockup` (`design/handoff/2026-10-13-rodada-3/content/landings.js:89`),
  mas tem cópia própria com o mesmo sha256, assim como os dois favicons.
- Risco: a URL some na publicação, e quem a abrir recebe 404. Não é contrato (ADR-001), e o git
  guarda os arquivos. Aceito.

### 5. Convite
- Fica congelado até o deploy único (D13 condição 1). O critério de CDN o exclui pelo caminho
  exato, e o §15 o trata como CONGELADAS, como o §14.
- `CONVITE-FORA-DO-WP-12-01` se cumpre com essa exclusão e com o mockup no caminho fixo; vira
  `resolvido` ao fechar este WP.
- `INVITE-PAKO-CDNJS-01` (pako sem SRI, Inter do Google) **não cabe aqui**: muda os bytes do
  convite. Destino `triagem`, para `/novo-wp` depois do deploy único: "convite sem terceiros",
  com pako local, Inter local, novo `contrato.sha256` e teste com `?d=` real gerado pelo app.

### 6. Régua
- Mediana de 3 runs, local, para as 20 indexáveis e a 404, como nos Critérios. A 404 é isenta só
  de SEO.
- Acessibilidade já está ≥ 90 em todas (mínimo 90, nas legais) e o valor é determinístico (não
  oscila entre runs). `color-contrast` e `link-in-text-block` mexem em cor e sublinhado, que é
  design (D4). `heading-order` está em markup que o WP-10 reescreve. Os três vão para o WP-10,
  que já exige AA e acessibilidade ≥ 95 (achado `A11Y-LH-BASELINE-WP12-01`). Não entram aqui.
- Página que oscila entre 82 e 92 (as legais): a oscilação vem dos ~2,5 s de CSS bloqueante de
  terceiros sob throttling simulado. Com eles fora, a margem esperada passa de 5 pontos. Se a
  mediana local ficar abaixo de 90, o WP não fecha: não há arredondamento nem "melhor de N".
  Repete-se com 5 runs só para relatar a dispersão.

### 7. Lighthouse no CI
- A ferramenta é a D20 (B): `lighthouse` 13.5.0 + `tools/lighthouse.py` + `tools/orcamento-lighthouse.json`.
- Desenho: job `lighthouse` separado no `pr.yml`, com o próprio `npm ci` +
  build, `timeout-minutes: 15`, sem `paths:`.
- 9 páginas, uma por template, mais as que medem diferente: `/`, `lottoexpert`, `topowalk`,
  `poleposition`, `eclipsego`, `lottoexpert-privacy`, `lottoexpert-terms`, `eclipsego-privacy` e
  `404`. São 3 runs cada, ≈ 27 execuções. O par en usa o mesmo template e os mesmos recursos; a
  medição das 21 é a do WP.
- Assertions:
  - erro: acessibilidade, boas práticas e SEO ≥ 0,90 (SEO desligada na 404); CLS ≤ 0,1; nenhuma
    requisição a outra origem; bytes totais e bytes de imagem por página ≤ medido depois + 20%
    (o número entra no arquivo de orçamento);
  - performance: erro < 0,85 e aviso < 0,90;
  - LCP: erro > 3,0 s e aviso > 2,5 s.
- A folga entre erro e aviso existe porque o runner varia até 10 pontos nas páginas leves (linha
  de base). O orçamento em bytes e a proibição de terceiros não variam, e são eles que pegam a
  regressão de verdade (PNG de 700 KB, CDN de volta).
- Tornar o check obrigatório na proteção de branch é decisão do usuário.

### 8. Decisões do usuário (decididas em 2026-10-16)
- **D20 → (B)**: `lighthouse` 13.5.0 exato em `devDependencies`, `tools/lighthouse.py` (biblioteca
  padrão) e `tools/orcamento-lighthouse.json`; job `lighthouse` no `pr.yml`. (A) e (C) fechadas.
- **D21 → (C)**: o card "offline" do EclipseGo fica sem ícone, como no ar. A escolha vai ao WP-10
  pelo achado `ECLIPSE-ICONE-OFFLINE-01` (destino `WP-10`, listado nos achados roteados de lá).

Motivos e o que fica aberto em `decisoes.md`.

### 9. Sequência de commits

Cada um passa pelo `/verify` completo: build, `check_site.py`, `contrato.sha256`,
html-validate e lychee. As capturas antes/depois do `site-ux` são dos commits 2, 3 e 4.

1. `WP-12: remove os 4 arquivos órfãos de public/assets`. Prova: `check_site.py` §3/§13 verde;
   `grep -rl` dos 4 nomes em `dist/` vazio. Sem captura.
2. `WP-12: Inter servida pelo site; JetBrains sai`. Inclui `src/assets/fonts/`, `astro.config.mjs`,
   `tailwind.config.mjs`, `Base.astro`, `global.css` e as 2 páginas do Pole Position, além do §15
   (a) do `check_site.py`: nenhum `fonts.googleapis`/`fonts.gstatic` em página gerada. Prova: o
   grep de fontes vazio fora do convite; `<link rel="preload" as="font">` em toda página.
   **Captura antes/depois.**
3. `WP-12: ícones em SVG inline (Icon.astro); Font Awesome sai`. Inclui `src/icons/fa/**`,
   `Icon.astro`, os 8 componentes, `LegalLayout`, as 2 páginas de termos, `Base.astro` (sai o
   `<link>` do cdnjs) e o §15 (b): nenhum `class="fa-`/`cdnjs` fora do convite. Prova: o grep do
   critério vazio. **Captura antes/depois**, com o menu do celular aberto.
4. `WP-12: imagens pelo astro:assets (WebP, width/height, lazy, LCP com fetchpriority)`. Inclui
   `src/assets/img/**`, os componentes, `Base.astro` (favicon por `getImage`) e o §15 (c): toda
   `<img>` com `width`/`height`, nenhuma com `src="/assets/`, no máximo um `fetchpriority="high"`
   por página. Prova: `contrato.sha256` verde, `public/assets/` intacto (§13). **Captura
   antes/depois em 1280 e 360**, com nitidez em 2×.
5. `WP-12: tabela antes/depois`. Medição das 21 pelo `site-seo-perf` nas condições da linha de
   base, colada no WP. Se alguma ficar abaixo da régua, o conserto é feito aqui e medido de novo,
   antes do CI.
6. `WP-12: job lighthouse no PR com orçamento` (D20 B). Prova: o job verde no PR, e um
   vermelho provocado e revertido (PNG grande de volta numa branch descartável) mostrando que a
   regra de bytes pega.

### Destino dos achados roteados
- `ASSETS-PESO-01`, `ASSETS-PNG-LCP-01`, `IMG-ATRIBUTOS-FONTES-01` → WP-12, commit 4.
- `TOPO-CLS-HERO-01` → commit 2.
- `POLE-JETBRAINS-SEM-USO-01` → commit 2.
- `OG-MOCKUP-JPEG-PESADO-01` → WP-20, na parte da og:image; o que é exibido sai no commit 4.
- `CONVITE-FORA-DO-WP-12-01` → resolvido pelo §5 deste veredito, ao fechar.
- `INVITE-PAKO-CDNJS-01` → `triagem`, para WP pós-deploy.

### 10. Desvios da implementação (commits c7d5683..1856a27), julgados em 2026-10-16
- **Fonte com 33,7 KB, não 24,9 KB: aceito.** Refeito o comando do `astro.config.mjs:29-31`
  (fontTools 4.61.1, `InterVariable.woff2` da rodada 3): 33.492 bytes com as features padrão do
  `pyftsubset` (o arquivo commitado tem 33.740; a diferença é de versão do fontTools); 28.812 com `--layout-features=kern,liga,calt`; 25.312 só com `kern`. O 24,9 KB do
  veredito e do ADR-006 §3 não se reproduz com as features padrão; o mais perto é o recorte só com
  `kern`. Cortar
  `ccmp`, `locl`, `mark`/`mkmk` e `calt` muda o desenho de texto que hoje sai certo (acento
  combinado, `→` contextual da Inter), e o WP promete paridade. São ~8 KB num único arquivo com
  preload, sem efeito mensurável na nota. Nada a cortar. O número do ADR-006 §3 foi corrigido
  com uma nota no próprio ADR.
- **§14 do `check_site.py` ignora `<title>` dentro de `<svg>`: aceito.** O `<title>` de um `<svg>`
  é o nome acessível do gráfico, não o título do documento. Contá-lo faria o §14 acusar título
  duplicado em toda página com logo de tecnologia. O recorte é estreito: só o que está entre
  `<svg>` e `</svg>`, e `<svg/>` vazio não abre nível (`tools/check_site.py:746-779`). A falha é
  segura: um `<svg>` mal fechado esconderia o `<title>` real, e o §14 reprovaria por falta de
  título. Está fora da letra "§15 novo" dos Arquivos-alvo, mas é o mesmo arquivo e é consequência
  direta do commit de ícones. Não é escopo novo.
- **`src/assets/img/` com 6,2 MB, não ≈ 3,5 MB: aceito, e o número do §1 está corrigido.** Medido:
  6.425.245 bytes. Desses, 2.369.902 são as 9 loterias de `lottoexpert/`, exibidas na landing por
  `<img>` e por isso cópia pela regra do §1 (o original fica em `public/` porque o convite o
  carrega). Mais 309 KB são origens de favicon para o `getImage()`. O custo é só no git, uma vez:
  `dist/` recebe o WebP. O que o veredito errou foi a conta, não a regra.

**Nota para o `site-docs`:** a árvore de Arquitetura do `CLAUDE.md` ("assets/ … PNG, sem
otimização"; "Base.astro … fontes") fica desatualizada no commit 4. A atualização é do
`site-docs`/usuário, no fechamento.

## Tabela antes/depois (commit 5, 2026-10-16)

Lighthouse 13.5.0 mobile (throttling simulado), 3 runs por página, mediana pela nota de
performance, `dist/` servido por `python3 -m http.server -d dist`, sem gzip. "Antes" é a linha de
base do `site-seo-perf`, medida antes do commit 1; "depois" é o `dist/` deste commit. Cada
célula mostra `antes → depois`; KB é o `total-byte-weight`.

| página | perf | a11y | BP | SEO | LCP s | CLS | TBT ms | FCP s | KB |
|---|---|---|---|---|---|---|---|---|---|
| `/en/` | 65 → 98 | 94 → 95 | 100 → 100 | 100 → 100 | 16.1 → 2.3 | 0.000 → 0.000 | 0 → 0 | 4.0 → 1.4 | 3838 → 288 |
| `/` | 65 → 98 | 94 → 95 | 100 → 100 | 100 → 100 | 16.1 → 2.3 | 0.000 → 0.000 | 0 → 0 | 4.0 → 1.4 | 3838 → 288 |
| `/eclipsego.html` | 88 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 3.3 → 1.9 | 0.033 → 0.000 | 0 → 0 | 2.7 → 1.2 | 625 → 167 |
| `/en/eclipsego.html` | 88 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 3.3 → 1.9 | 0.002 → 0.000 | 0 → 0 | 2.7 → 1.2 | 625 → 167 |
| `/eclipsego-privacy.html` | 92 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 2.7 → 1.8 | 0.000 → 0.000 | 0 → 0 | 2.7 → 1.2 | 385 → 145 |
| `/en/eclipsego-privacy.html` | 83 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 3.6 → 1.8 | 0.051 → 0.000 | 0 → 0 | 3.3 → 1.2 | 384 → 145 |
| `/lottoexpert.html` | 70 → 98 | 96 → 96 | 100 → 100 | 100 → 100 | 15.1 → 2.2 | 0.001 → 0.000 | 0 → 0 | 2.8 → 1.5 | 4179 → 249 |
| `/en/lottoexpert.html` | 70 → 98 | 96 → 96 | 100 → 100 | 100 → 100 | 14.9 → 2.2 | 0.001 → 0.000 | 0 → 0 | 2.8 → 1.5 | 4178 → 248 |
| `/lottoexpert-privacy.html` | 82 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 3.8 → 2.0 | 0.002 → 0.000 | 0 → 0 | 3.4 → 1.4 | 704 → 174 |
| `/en/lottoexpert-privacy.html` | 90 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 2.8 → 2.0 | 0.075 → 0.000 | 0 → 0 | 2.7 → 1.4 | 701 → 171 |
| `/lottoexpert-terms.html` | 91 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 2.7 → 1.8 | 0.069 → 0.000 | 0 → 0 | 2.7 → 1.2 | 682 → 153 |
| `/en/lottoexpert-terms.html` | 92 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 2.6 → 1.8 | 0.002 → 0.000 | 0 → 0 | 2.6 → 1.2 | 682 → 152 |
| `/poleposition.html` | 66 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 8.9 → 2.1 | 0.024 → 0.000 | 0 → 0 | 4.0 → 1.4 | 1423 → 212 |
| `/en/poleposition.html` | 72 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 7.1 → 2.1 | 0.001 → 0.000 | 0 → 0 | 2.7 → 1.4 | 1423 → 212 |
| `/poleposition-privacy.html` | 83 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 3.6 → 2.0 | 0.004 → 0.000 | 0 → 0 | 3.3 → 1.4 | 451 → 161 |
| `/en/poleposition-privacy.html` | 92 → 99 | 90 → 90 | 100 → 100 | 100 → 100 | 2.7 → 1.8 | 0.000 → 0.000 | 0 → 0 | 2.7 → 1.2 | 448 → 159 |
| `/topowalk.html` | 80 → 99 | 96 → 96 | 100 → 100 | 100 → 100 | 4.0 → 2.0 | 0.047 → 0.000 | 0 → 0 | 3.4 → 1.4 | 586 → 171 |
| `/en/topowalk.html` | 90 → 99 | 96 → 96 | 100 → 100 | 100 → 100 | 3.1 → 2.0 | 0.002 → 0.000 | 0 → 0 | 2.7 → 1.4 | 586 → 171 |
| `/topowalk-privacy.html` | 91 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 2.8 → 2.0 | 0.003 → 0.000 | 0 → 0 | 2.8 → 1.4 | 510 → 183 |
| `/en/topowalk-privacy.html` | 91 → 99 | 94 → 94 | 100 → 100 | 100 → 100 | 2.8 → 2.0 | 0.002 → 0.000 | 0 → 0 | 2.8 → 1.4 | 504 → 177 |
| `/404.html` | 99 → 100 | 100 → 100 | 100 → 100 | 66 → 66 | 1.7 → 1.5 | 0.000 → 0.000 | 0 → 0 | 1.7 → 1.1 | 219 → 108 |

**Resultado:** as 20 indexáveis cumprem a régua: performance de 98 a 99, boas práticas e SEO
100, acessibilidade de 90 a 96, LCP de 1,8 a 2,3 s e CLS 0. A 404 tem 100/100/100. O único item de
SEO reprovado nela é `is-crawlable`, como previsto. A oscilação entre as 3 runs ficou em no máximo
1 ponto, contra até 9 pontos na linha de base.

**Conserto feito aqui:** a primeira medição pós-commit 4 deu LCP de 2,6 s na `/en/` (2 das 3
runs) e de 2,3 s na `/`. O LCP das duas homes é a logo da nav. As 17 imagens `lazy` dos cards
estão perto da dobra no viewport do celular, então o navegador as busca antes de pintar a logo, e
elas disputavam banda com ela. Sem essas imagens, o LCP caiu para 1,8–1,95 s, o que prova a
causa. A solução foi `fetchpriority="low"` em toda `<Image>` de `Home.astro`, e o LCP ficou em
2,33 s estável nas duas homes. As imagens continuam `lazy`, e nada muda na tela.

**Acessibilidade**, para registro: o que reprova é `color-contrast`, `heading-order` e, nas legais,
`link-in-text-block`. Os três foram roteados ao WP-10 (`A11Y-LH-BASELINE-WP12-01`), conforme o §6.

## Job `lighthouse` (commit 6, 2026-10-16)

`tools/lighthouse.py` usa só a biblioteca padrão. Ele serve `dist/` num `http.server` de porta livre e
roda o `lighthouse` 13.5.0 do lockfile 3× em cada uma das 9 páginas de `tools/orcamento-lighthouse.json`.
Confere a mediana pela performance contra as regras do §7. O orçamento em bytes é o medido no
commit 5 + 20%. `--medir` imprime os bytes para atualizar o orçamento de propósito.

- **Verde local** sobre o `dist/` do commit 5: as 9 páginas cumprem as regras (perf 98–100, LCP de 1,50 a
  2,33 s, CLS 0).
- **Vermelho provocado local** numa cópia de `dist/` com o `lottoexpert_app_mockup.png` (555 KB) e
  o CSS do Google Fonts injetados na home. Deu `exit=1` com 3 erros: requisição a
  `fonts.googleapis.com`, 852.264 bytes > 354.427 no total e 674.549 > 142.673 em imagem. O LCP
  só gerou aviso (2,63 s). Isso confirma o §7: são os bytes e os terceiros que pegam a regressão.
  Boas práticas ficou em 100 mesmo com o terceiro.
- **Pendente:** o job verde no PR e o vermelho provocado numa branch descartável no CI. Os dois
  dependem de push, e push é do usuário. Tornar o check obrigatório na proteção de branch também
  é decisão do usuário.

## Auditoria (2026-10-16) e correções

`site-qa`, `site-seo-perf` e `site-ux` rodaram em paralelo sobre `ad62095..8d16a5f`. Nenhum achado alto.

**Corrigido no commit de correções:**
- **Caixa dos ícones (`site-ux`, médio).** O `<i>` do FA ocupava a própria altura de linha, que é 1 no
  `.fa-solid` e 28 px num `text-xl`. O SVG tinha `height: 1em`. Por isso o botão da Play encolhia
  4 px e a faixa de tecnologia da home 8 px. Agora o `.icone` (`global.css`) tem `line-height: 1`,
  `padding-block` com a meia-entrelinha (`(1lh - 1em) / 2`) e o `vertical-align` compensado.
  Medido em 10 páginas × 3 larguras contra os DOMs "antes":
  - alturas de página iguais (±1 px de arredondamento), exceto `eclipsego` en a 768;
  - altura e centro de todos os ícones iguais.
- **Reflow em `/en/eclipsego.html` a 768 px: aceito.** Um parágrafo passa de 4 para 3 linhas e a
  página fica 23 px menor, por métrica da Inter servida pelo site contra a do Google. Não há quebra
  nova; o texto ficou mais curto.
- **§15 do `check_site.py` (`site-qa`)** agora pega:
  - `<img>`/`<source>` de `assets/` também por caminho relativo à página;
  - `srcset` de `<source>`;
  - terceiro em `img`, `source`, `iframe`, `video`, `audio`, `embed` e `url()` de `style`;
  - ícone de qualquer `rel` com `icon`;
  - `fetchpriority="high"` junto de `loading="lazy"`;
  - `<svg>` sem `aria-hidden` nem `role="img"` com nome.

  Prova: 10 mutações numa cópia de `dist/`, 9 vermelhas e o SVG correto verde.
- **`tools/lighthouse.py` (`site-qa`):**
  - um arquivo por run, para não ler o relatório de outra página;
  - `timeout` de 120 s por run, com a URL na mensagem;
  - na 404, falha se reprovar qualquer auditoria de SEO além de `is-crawlable`;
  - terceiros somados de todas as runs;
  - `--runs` precisa ser 1 ou mais.

**Aceito sem mudança:**
- **Orçamento só em pt e em 9 páginas.** É o desenho do §7: uma página por template, e o par en
  usa os mesmos recursos.
- **Folga de 135 bytes entre o orçamento e o +20% de hoje.** É variação entre runs.
- **`fetchpriority="low"` nas imagens do hero da home.** É de propósito (commit 5). O LCP é a logo.
- **Mockup do LottoExpert `lazy`.** O LCP medido da landing é a logo, com 2,18 s.
- **Margem de 0,17 s no LCP da home**, a menor do conjunto. O aviso do CI pega primeiro.

**Roteado ao WP-10** (`achados-novos.md`):
- `NAV-MENU-ALVO-TOQUE-01`: alvo de toque do menu com ~17,5×28 px. Já era assim antes.
- `HOME-TECH-CURSOR-01`: `cursor-pointer` sem interação.
- `POLE-PRINTS-2X-01`: as capturas do Pole Position têm só 460 px na origem.

**Ainda aberto:** o job verde no PR e o vermelho provocado no CI dependem de push, que é do usuário.
O checklist de navegador também está aberto: menu do celular, nitidez em 2×, favicon e paridade dos ícones.
