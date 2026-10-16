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

**Ler antes:** `docs/AVALIACAO.md` §2.4; `@astrojs/image`/`astro:assets`; `@lhci/cli` com
`lighthouserc.json`.

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
- Lighthouse no CI, conforme D20: (A) `package.json`, `package-lock.json`, `lighthouserc.json`;
  (B) `package.json`, `package-lock.json`, `tools/lighthouse.py`, `tools/orcamento-lighthouse.json`;
  as duas com `.github/workflows/pr.yml` (job `lighthouse`). (C) nenhum destes.

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
- Job `lighthouse` verde no PR (D20 A ou B); com D20 (C), o critério sai e a medição local fica.

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
de CDN. Os commits 1 a 5 não dependem de nenhuma decisão em aberto. O commit 6 espera a D20.
D21 não bloqueia: sem resposta, vale a opção (C).

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
- O que a página exibe passa a sair de uma cópia em `src/assets/img/`. As cópias somam ≈ 3,5 MB
  no git, e esse custo é aceito para que a URL externa não mude.
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
  `opsz` 14, faixa latina + U+2192: medido 24,9 KB. O único caractere fora da faixa latina em
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
- A ferramenta é a D20, porque a D2 deixou "Lighthouse CI" em aberto.
- Desenho para (A) ou (B): job `lighthouse` separado no `pr.yml`, com o próprio `npm ci` +
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

### 8. Decisões do usuário
- **D20**: ferramenta do Lighthouse no CI. Recomendada: (B).
- **D21**: o ícone que falta no card "offline" do EclipseGo. Recomendada: (C).

Opções, custos e motivos em `decisoes.md`.

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
6. `WP-12: job lighthouse no PR com orçamento` (só depois da D20). Prova: o job verde no PR, e um
   vermelho provocado e revertido (PNG grande de volta numa branch descartável) mostrando que a
   regra de bytes pega.

### Destino dos achados roteados
- `ASSETS-PESO-01`, `ASSETS-PNG-LCP-01`, `IMG-ATRIBUTOS-FONTES-01` → WP-12, commit 4.
- `TOPO-CLS-HERO-01` → commit 2.
- `POLE-JETBRAINS-SEM-USO-01` → commit 2.
- `OG-MOCKUP-JPEG-PESADO-01` → WP-20, na parte da og:image; o que é exibido sai no commit 4.
- `CONVITE-FORA-DO-WP-12-01` → resolvido pelo §5 deste veredito, ao fechar.
- `INVITE-PAKO-CDNJS-01` → `triagem`, para WP pós-deploy.

**Nota para o `site-docs`:** a árvore de Arquitetura do `CLAUDE.md` ("assets/ … PNG, sem
otimização"; "Base.astro … fontes") fica desatualizada no commit 4. A atualização é do
`site-docs`/usuário, no fechamento.
