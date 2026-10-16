---
id: WP-22
titulo: Acessibilidade e i18n sem redesign (a11y AA, foco, `<main>`, headings, reduced-motion, contraste fora da paleta, rótulos pt na /en/)
area: landing
status: todo
depende_de: [WP-12, WP-15]
adr: [ADR-003, ADR-007]
spec: docs/AVALIACAO.md
decisoes: []
tamanho: M
risco: medio
visual: true
branch: feat/wp-22-a11y-sem-redesign
---

# WP-22 — Acessibilidade e i18n sem redesign

**Depende de:** WP-12 (ícones SVG, `Icon.astro`), WP-15 (`SeletorIdioma`, `idiomas.json`) — ambos `done`.
Branch nasce de `feat/wp-08-layout-unico` (integração D13) e vai ao ar no deploy único.

**Achados roteados** (`achados-novos.md`, varredura de 2026-10-16):

- **Inteiros (21) — destino passa a `WP-22`:** `LEGAL-CODE-LONGO-360-01` (**prioridade**),
  `HOME-EN-ROTULOS-PT-01`, `HERO-ROTATE-4-01`, `REDUCED-MOTION-01`, `LOTTO-REDUCED-MOTION-01`,
  `HOME-SEM-MAIN-01`, `LOTTO-TABELA-SEM-TEXTO-01`, `TOPO-PLAY-HL-PT-01`, `TOPO-PASSO-NUMERO-DUPLO-01`,
  `NAV-BOTAO-MENU-FOCO-01`, `NAV-FOCO-VISIVEL-01`, `I18N-CHAVE-DINAMICA-01`, `POLE-HEADING-ORDEM-01`,
  `FOOTER-H4-ORDEM-01`, `TROCA-IDIOMA-ROTULO-01`, `LEGAL-SELO-EN-PT-01`, `LEGAL-MAILTO-SEM-DESTAQUE-01`,
  `PP-NAV-CONTRASTE-01`, `TABELA-ROLAVEL-FOCO-01`, `NAV-MENU-ALVO-TOQUE-01`, `HOME-TECH-CURSOR-01`.
- **Parciais (5) — destino fica `WP-10`, com nota** "parte corrigível no WP-22: …" (o dono do resto é
  o WP-10; mesma convenção de `OG-MOCKUP-JPEG-PESADO-01`, que ficou no WP-20 com "a parte exibida
  saiu no WP-12"). Não há reroteamento ao fechar este WP: o site-docs só troca a nota para "saiu no
  WP-22 (commit)".
  - `404-FONTE-NAV-01` — aqui: Nav e Footer na 404. (Fonte já resolvida em fe286b7; nada fica no WP-10 —
    se o WP-22 fechar a parte de Nav/Footer, o achado é `resolvido`.)
  - `LANG-SWITCH-ALVO-01` — aqui: ícones sociais do Footer (`w-10 h-10` → 44 px), botão do menu, links
    do menu do celular e do rodapé com alvo ≥ 24 px (AA, 2.5.8). Fica no WP-10: alvo de 44 px como
    padrão de desenho (AAA), se o handoff pedir.
  - `LOTTO-CONTRASTE-AA-01` — aqui: rodapé (`text-gray-500/600` → `text-gray-400`, `#year`). Fica no
    WP-10: `brand-primary` #8B5CF6 (paleta, D4).
  - `POLE-EN-ROTULOS-PT-01` — aqui: o `?locale=pt_BR` do link do Facebook. Fica no WP-10: seções
    "Veja na prática" e "Para quem é" (copy de produto, não rótulo).
  - `LEGAL-LINK-CONTRASTE-01` — aqui: sublinhado nos links do corpo legal (`link-in-text-block`). Fica
    no WP-10: a cor (`color-contrast`, paleta D4).

**Objetivo:** as páginas do site passam o Lighthouse de acessibilidade sem `color-contrast` fora da
paleta, sem `heading-order`, `label-content-name-mismatch`, `target-size` nem `landmark-one-main`; a
360 px nenhuma página legal rola na horizontal; a `/en/` não mostra rótulo de interface em pt nem
manda para a Play/Facebook em pt.

**Contexto:** a varredura de 2026-10-16 (3 site-qa sobre `dist/` do HEAD a8c2c43) separou dos achados
roteados ao WP-10 os que não dependem do handoff, de D11/D12 nem de copy nova. O WP-10 espera D11,
D12 e o checklist do WP-19; estes 26 não precisam esperar. Evidência (detalhe em cada linha de
`achados-novos.md`):

- **Prioridade:** `/lottoexpert-privacy.html` e `/en/lottoexpert-privacy.html` a 360 px (Puppeteer):
  `innerWidth` 495, `scrollWidth` 494/489, botão do menu fora da tela — `<code>` com a URL do
  googleapis sem quebra. `.legal-corpo` não tem regra de quebra para `code`
  (`src/styles/global.css:337-460`; só o tema do PP estiliza `code`, `:445`).
- `<main>` ausente em 10 páginas de `dist/` (home e 4 landings, pt e en): o corpo vem de
  `src/components/paginas/Pagina{Home,LottoExpert,TopoWalk,PolePosition,EclipseGo}.astro:41-46`
  sem landmark. Legais já têm (`LegalLayout.astro:85`), 404 também (`pages/404.astro:14`). O convite
  também não tem e fica fora (D13, `CONVITE-SEM-MAIN-01`).
- Heading: `<h4>` depois de `<h2>` em `PolePosition.astro:170,231` e no rodapé (`Footer.astro:167,175,195`).
- Foco e alvo: `Nav.astro:133-138` (`#mobile-menu-btn`, `focus:outline-none`, ~17,5×28 px);
  `Footer.astro:76` (social `w-10 h-10`, 40 px).
- Rótulo acessível: `SeletorIdioma.astro:37` decide o nome por substring (`'ENGLISH'.includes('EN')`)
  e sai `aria-label="English"` com texto visível "EN" — axe compara por palavra e reprova.
- Contraste do rodapé: `Footer.astro:213,226,229` (`text-gray-500/600` sobre #111827: 3,66:1 e 2,34:1).
- `PP-NAV-CONTRASTE-01`: pílula Contato da política do PP, branco sobre lima, 1,98:1;
  `PaginaPolePositionPrivacy.astro:6` documenta `realce="primary"`; a landing do PP já usa
  `primary-claro`.
- i18n: `apps.ts:27` (`&hl=pt_BR` no TopoWalk, nos dois idiomas e no JSON-LD);
  `PaginaPolePosition.astro:56` (`?locale=pt_BR`); `legal.ts:30` (`en.selo: 'Documento Legal'`);
  `Home.astro:74-387` (rótulos de categoria e 16 `alt` literais em pt, nos dois idiomas).
- `txt()` com cast silencioso: `TopoWalk.astro:22`, `PolePosition.astro:29`, `EclipseGo.astro:27`,
  `LottoExpert.astro:45-46`.
- Movimento: `global.css:164-258` (`animate-float`, `fade-in-*`, `spin-slow`, `corona-glow`) e as do
  Tailwind (`animate-bounce` `Home.astro:138`, `animate-pulse` `LottoExpert.astro:186-192` e
  `EclipseGo.astro:54`, `animate-ping` `EclipseGo.astro:85`), sem `prefers-reduced-motion`.
- Tabela Free × Premium: `LottoExpert.astro:267-276`, célula só com ícone ou "—".
- Mortos: `-rotate-4`/`rotate-4` em `Home.astro:87,102` (fora da escala do Tailwind 3, nunca geraram
  CSS); `cursor-pointer` em ícones não interativos, `Home.astro:188-198`.
- Tabela legal rolável: `legal.mjs:39` envolve em `div.legal-tabela` sem `tabindex` nem nome.

**Decisões conferidas (nenhuma aberta):**
- `LOTTO-TABELA-SEM-TEXTO-01`: rótulos sr-only "Incluído"/"Não incluído", en "Included"/"Not included"
  — aprovados pelo usuário em 2026-10-16.
- `HOME-EN-ROTULOS-PT-01` e `LEGAL-SELO-EN-PT-01`: o en é tradução de rótulo de interface que já existe
  em pt ("Topografia", "Loterias", `alt` de imagem, "Documento Legal"). Não é copy de produto (não
  descreve o app nem promete nada) nem texto legal (o selo é cromo do `LegalLayout`, fora do `.md`).
  ADR-007 exige espelho completo das línguas listadas; a tradução de interface é do agente desde o
  WP-08 (as chaves en de `ui.ts`/`<pagina>.ts`). Cabe sem decisão; o usuário confere o en no roteiro
  de navegador. **Limite:** se algum `alt` da home descrever funcionalidade (copy) e não a imagem,
  ele fica como está em pt e vira linha em `achados-novos.md` → `WP-10`; não se reescreve aqui.
- `PP-NAV-CONTRASTE-01` dizia "trocar é decisão do usuário". Não é desenho novo: `primary-claro` é a
  variante que o mesmo app já usa na landing (`PaginaPolePosition.astro`); o WP alinha a política à
  landing. **Confirmado pelo usuário em 2026-10-16** ("pode seguir o recomendado"), junto com a posição
  do WP na trilha C, antes do WP-10.
- `TOPO-PLAY-HL-PT-01` e o `?locale=pt_BR`: tirar o parâmetro (a Play e o Facebook usam a língua da
  conta/navegador), igual aos outros três apps em `apps.ts:25,29,31`. Não é `hl` por língua: isso
  seria um mapa novo por idioma para um parâmetro que os outros apps não usam.
- Alvo de toque ≥ 44 px no botão do menu e nos sociais: 44 px é o mínimo que o próprio site já
  adotou (`404.astro`, `SeletorIdioma.astro:58` `min-h-11`), não escolha de desenho nova.

**Ler antes:** `docs/AVALIACAO.md` §1 (linha "Acessibilidade") e §3.3 (foco visível, contraste AA);
ADR-007 §5 e §7 (espelho completo, seletor); ADR-003 (Tailwind 3 até o redesign); a linha de cada
achado em `achados-novos.md`.

**Arquivos-alvo** (lista fechada):
- `src/components/Nav.astro`, `src/components/Footer.astro`, `src/components/SeletorIdioma.astro`
- `src/components/Home.astro`, `LottoExpert.astro`, `TopoWalk.astro`, `PolePosition.astro`, `EclipseGo.astro`
- `src/components/paginas/Pagina{Home,LottoExpert,TopoWalk,PolePosition,EclipseGo,PolePositionPrivacy}.astro`
- `src/pages/404.astro`
- `src/i18n/home.ts`, `lottoexpert.ts`, `legal.ts`, `apps.ts`, `ui.ts` (helper de chave, se usado)
- `src/styles/global.css` (regras gerais de `.legal-corpo` e `@media (prefers-reduced-motion)`; **não**
  muda token nem `--brand-*` de tema)
- `src/markdown/legal.mjs` (só o `wrapNode` da tabela)
- `tools/check_site.py` (guardas novas, passo 9)
- `tools/orcamento-lighthouse.json` (só a entrada `/404.html`, medida com `--medir`)

**Fora:** `src/content/legal/**` (o corpo legal não muda), `tailwind.config.mjs` e qualquer
`--brand-*`, `public/**` (o convite e o `assetlinks.json`, D13), ícones (D21-C), copy de produto,
`cursor-pointer` dos mockups do Pole Position (`PolePosition.astro:90,95` — não roteado; se o site-qa
quiser, é achado novo para o WP-10).

**Passos** (ordem = prioridade; cada item é um commit `WP-22: …`):
1. **360 px nas legais.** Em `global.css`, regra geral `.legal-corpo code { overflow-wrap: anywhere; }`
   (e `word-break: break-word` como reserva). Medir as 10 legais a 360 px antes de seguir.
2. **Landmarks e headings.** `<main>` em volta do corpo nas 5 `Pagina*.astro` de landing (Nav e
   Footer fora dele); Nav e Footer na 404, com `lang="pt"`, `caminho="404.html"` e hrefs absolutos
   (a 404 é servida em qualquer profundidade; `linguasDe('404.html')` dá só pt, então sem seletor).
   `<h4>` → `<h3>` em `PolePosition.astro:170,231` e `Footer.astro:167,175,195`, mesmas classes.
3. **Foco e alvo.** `#mobile-menu-btn`: tira `focus:outline-none`, ganha o `focus-visible` do
   `SeletorIdioma.astro:38` e `min-w-11 min-h-11 inline-flex items-center justify-center`. Social do
   Footer `w-11 h-11`. Links do menu do celular e do rodapé com altura de alvo ≥ 24 px (`py-*` ou
   `min-h-6`); Lighthouse `target-size` é o juiz.
4. **Rótulo do seletor.** `SeletorIdioma.astro:37`: código contido no nome **como palavra**, senão
   `Nome (CÓDIGO)` → `English (EN)`, `Português (PT)`.
5. **Contraste fora da paleta.** Rodapé `text-gray-500/600` → `text-gray-400` (`Footer.astro:213,226,229`);
   `realce="primary-claro"` na Nav de `PaginaPolePositionPrivacy.astro` (e o comentário da linha 6).
6. **Texto legal: marcação, não conteúdo.** `global.css`: `.legal-corpo a { text-decoration: underline; }`
   geral (mailto incluso; as regras de tema mantêm a cor). `legal.mjs:39`: `.legal-tabela` ganha
   `tabindex="0"`, `role="region"` e `aria-labelledby` com o `id` do último título antes da tabela
   (`secao-N-M`, igual em todas as línguas) — nenhuma string nova.
7. **i18n.** `apps.ts:27` sem `&hl=pt_BR` (e o comentário da `:17`); `PaginaPolePosition.astro:56` sem
   `?locale=pt_BR`; `legal.ts:30` `selo: 'Legal Document'`; rótulos de categoria e `alt` de
   `Home.astro:74-387` para chaves de `home.ts`, pt byte a byte igual ao de hoje, en traduzido;
   tabela do LottoExpert com `<span class="sr-only">` "Incluído"/"Não incluído" (en "Included"/
   "Not included") em `lottoexpert.ts`, ícone e "—" com `aria-hidden="true"`; círculo do número dos
   passos do TopoWalk (`TopoWalk.astro:152`) com `aria-hidden="true"`; `txt()` dos 4 componentes
   lança `Error` com o nome da chave quando `x[chave] === undefined` (falha o build).
8. **Movimento e mortos.** `global.css`: `@media (prefers-reduced-motion: reduce)` com
   `animation-duration: .01ms !important; animation-iteration-count: 1 !important;
   transition-duration: .01ms !important; scroll-behavior: auto !important` sobre `*, ::before, ::after`
   — **não** `animation: none`, porque `fade-in-*` parte de `opacity: 0` e o elemento sumiria. Remover
   `-rotate-4`/`rotate-4` (`Home.astro:87,102`) e `cursor-pointer` dos ícones (`Home.astro:188-198`).
9. **Guardas no `check_site.py`** (sobre todo `dist/`, fora `CONGELADAS`; o Lighthouse só cobre 9
   páginas): (a) exatamente um `<main>` por página; (b) heading sem salto (`h(n)` → `h(n+2)` é erro);
   (c) `a`/`button` com `aria-label` e texto visível não vazio: o texto visível, normalizado, aparece
   como palavra no `aria-label`; (d) nenhum `hl=pt_BR`/`locale=pt_BR` em `href` de página que não seja
   pt. Cada regra com mutação provada (quebrar de propósito, ver o erro, desfazer), como no WP-15.
10. Medir a 404 com `python3 tools/lighthouse.py --medir` e atualizar só a entrada `/404.html` do
    orçamento (cresce por Nav, Footer e logo); nenhuma outra entrada sobe.

**Critérios de aceite:**
- `npm run build` verde (inclui o `txt()` que lança: mutação — chave errada falha o build — provada e desfeita).
- `python3 tools/check_site.py` verde, com as guardas (a)–(d) do passo 9 e a mutação de cada uma relatada.
- `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` verde.
- `python3 tools/sync_legal.py --todos --check` sem nada "atrás"/"divergente" e `git diff --stat
  feat/wp-08-layout-unico -- src/content/legal/` vazio (o texto legal não mudou).
- `python3 -B -m unittest tools/test_regras_i18n.py`, `npx html-validate 'dist/**/*.html'` e lychee verdes.
- `python3 tools/lighthouse.py` verde (orçamento cumprido; só `/404.html` mudou no JSON).
- Lighthouse a11y das 9 páginas do orçamento **e** de `/en/`, `/en/poleposition.html`,
  `/en/lottoexpert-privacy.html`: `heading-order`, `label-content-name-mismatch`, `target-size`,
  `landmark-one-main`, `link-in-text-block` com score 1; `color-contrast` com score 1 fora das páginas do
  LottoExpert, e nelas só nós com `#8B5CF6`/`brand-primary` (o violeta, WP-10). Prova: JSON do
  Lighthouse filtrado por `jq '.audits["<id>"].details.items[].node.snippet'`, colado no relatório.
- 360 px (Puppeteer, `document.documentElement.scrollWidth`): 360 nas 10 páginas legais (pt e en) e
  em `/404.html`; o `#mobile-menu-btn` com `getBoundingClientRect().right ≤ 360` e ≥ 44×44.
- `grep -rlE 'hl=pt_BR|locale=pt_BR' dist/en/` vazio; `grep -c 'Documento Legal' dist/en/*-privacy.html
  dist/en/*-terms.html` = 0.
- `grep -rE '\b-?rotate-4\b' src/components/Home.astro` vazio; nenhum `focus:outline-none` sem
  `focus-visible:` no mesmo elemento em `src/components/`.
- Puppeteer com `emulateMediaFeatures([{name:'prefers-reduced-motion', value:'reduce'}])` na home, no
  LottoExpert e no EclipseGo: nenhum elemento com animação infinita (`getAnimations()` todas
  `finished`/ausentes após 100 ms) e nenhum elemento do hero com `opacity` computada 0.

**Só no navegador** (o usuário reporta; sem o relato o WP não fecha):
1. `/lottoexpert-privacy.html` e `/en/lottoexpert-privacy.html`, 360 px: sem rolagem lateral; o botão
   do menu visível e abre o menu; a URL do googleapis quebra dentro do bloco.
2. Uma legal de cada tema (`/topowalk-privacy.html`, `/poleposition-privacy.html`, `/eclipsego-privacy.html`,
   `/lottoexpert-terms.html`), 360 e 1280 px, pt: links do corpo e o e-mail do §Contato sublinhados;
   a tabela larga rola com Tab + setas (anel de foco visível).
3. `/poleposition-privacy.html`, 360 px, menu aberto: pílula Contato com texto escuro legível.
4. Toda a navegação por teclado (Tab) na home, 360 e 1280 px: o botão do menu mostra o anel de foco.
5. Rodapé em qualquer página, 1280 px: "© ano" e linha de baixo legíveis (cinza mais claro que hoje);
   ícones sociais um pouco maiores, ainda alinhados.
6. `/404.html` (e um caminho inexistente como `/x/y`), 360 e 1280 px: Nav e Footer presentes, links
   funcionam a partir de subpasta.
7. `/en/` e `/en/poleposition.html`, 1280 px: nenhum rótulo de interface em pt na home (categorias dos
   cards); hover nos ícones de tecnologia sem cursor de mão; o en dos rótulos lê bem.
8. `/en/topowalk.html`: botão da Play abre a ficha na língua da conta, não forçada em pt.
9. `/lottoexpert.html`, leitor de tela (TalkBack ou NVDA): a tabela Free × Premium anuncia
   "Incluído"/"Não incluído"; `/en/lottoexpert.html` anuncia "Included"/"Not included".
10. Sistema com "reduzir movimento" ligado: home, LottoExpert e EclipseGo sem flutuar, girar ou pulsar,
    e todo o conteúdo do hero visível.

**Irreversível:** nada. Nenhuma URL contratual, `public/` ou deploy muda; o texto legal (`src/content/legal/`)
não muda — só a marcação em volta (`legal.mjs`) e o estilo (`.legal-corpo`), que o `sync_legal --check`,
o §4 do `check_site.py` e o `diff` vazio provam.

**Risco:** médio, não alto. Não toca texto legal, URL nem deploy (os três gatilhos de alto), mas muda
Nav, Footer e o render das 10 legais — componentes de todas as 20 páginas. O que pode dar errado:
(1) `aria-labelledby` da tabela apontar para id inexistente quando a tabela vem antes de qualquer
título — cair para nenhum `aria-labelledby` e `aria-label` não entra (seria string nova); (2) a regra
de reduced-motion deixar o hero invisível (por isso `.01ms`, não `none`); (3) `<main>` em volta de
componente que já tenha `<main>` dentro (a guarda (a) pega); (4) a 404 com Nav estourar o orçamento
de LCP; (5) `overflow-wrap: anywhere` quebrar `code` curto em tabela larga de um jeito feio — conferir
no item 2 do roteiro.
