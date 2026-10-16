---
id: WP-15
titulo: Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas
area: infra
status: doing
depende_de: [WP-08, WP-09, WP-11]
adr: [ADR-001, ADR-002, ADR-004, ADR-005, ADR-007]
spec: docs/AVALIACAO.md
decisoes: [D2, D8, D18, D23]
tamanho: L
risco: alto
visual: true
branch: feat/wp-15-i18n-n-linguas
---

# WP-15 — Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas

**Depende de:** WP-08 (rota `/en/`), WP-09 (front-matter legal e `sync_legal.py`), WP-11
(`Seo.astro` com `hreflang` pt/en) · **Achados roteados:** HOME-HREFLANG-XDEFAULT-01, LEGAL-SLUG-ACENTO-01, TROCA-IDIOMA-ATRIBUTO-SEM-CONSUMIDOR-01

**Objetivo:** uma configuração única (`src/i18n/idiomas.ts`) diz, por página, quais línguas
existem; o roteamento, o seletor de idioma, o `hreflang`/`x-default` e o `check_site.py` leem
dela. pt continua no caminho atual (raiz), en em `/en/`, as demais em `/<lang>/`. Este WP não
publica nenhuma página em língua nova — só a estrutura; conteúdo é WP-16/17/18.

**Contexto:** D8. Os apps TopoWalk e Pole Position falam de/es/fr/it(/ru) além de pt e en
(`../topo-walk/app/src/main/res/values-*`, `../pole-position/pole-position-app/app/src/main/res/values-*`),
e o site só tem pt/en por JS (`topowalk-privacy.html:1042` lê `ghf_lang` do `localStorage`,
25 `data-i18n` em cada política, 67 em `topowalk.html`, 103 em `poleposition.html`). O WP-08
planeja rota só para `/en/` e o WP-11 `hreflang` só pt-BR/en — generalizar aqui, depois deles,
evita fazer o roteamento duas vezes; generalizar dentro do WP-08 misturaria stack com escopo
de produto ainda em aberto (D8). `docs/AVALIACAO.md` §2 item 6 (i18n invisível para buscadores).

**Ler antes:** `docs/AVALIACAO.md` §2 item 6 e §3.2 (i18n por rota); ADR-001; ADR-002 (stack);
WP-08 (como `/en/` foi feito); WP-11 (`Seo.astro`); WP-09 (`sync_legal.py`, marcador `en: pendente`).

**Arquivos-alvo:** `src/i18n/idiomas.ts` (novo — lista de línguas do site e mapa
página → línguas), `src/i18n/ui.ts` (rótulos do seletor e da faixa nas línguas listadas),
`src/components/SeletorIdioma.astro` (novo), `src/components/SugestaoIdioma.astro` (novo, se
D8 (c1)), `src/components/Seo.astro`, `src/layouts/**`, `astro.config.mjs` (`i18n.locales`),
`tools/check_site.py`, `tools/sync_legal.py`, `tools/fixtures/i18n/**` (novo — `dist` sintético
para provar as regras do check), `CLAUDE.md` (seções "Produto e copy" e "Arquitetura").

**Passos:**
1. `idiomas.ts`: `IDIOMAS = ['pt','en','es','fr','it','de','ru']` com `hreflang` (`pt-BR`,
   `en`, `es`, …) e nome nativo; `PAGINAS = { 'topowalk-privacy': ['pt','en'], … }` — hoje
   todas `['pt','en']`. `x-default` aponta para **en** quando a página tem en (os apps têm o
   inglês como `values/` padrão), senão pt — registrar no ADR do passo 8.
2. Roteamento: pt na raiz com o caminho de hoje (ADR-001), demais em `/<lang>/<mesmo caminho>`.
   Página só é gerada nas línguas do mapa; sem fallback silencioso para pt dentro de `/es/`.
3. `SeletorIdioma`: lista só `PAGINAS[pagina]`; troca preserva a página; some quando a página
   tem uma língua só. Sem bandeira — nome nativo (`Español`, `Deutsch`, `Русский`).
4. `Seo.astro`: `hreflang` só das línguas existentes da página + `x-default`.
5. Chegada na língua conforme D8 (c): se (c1), `SugestaoIdioma` compara `navigator.languages`
   com `PAGINAS[pagina]` e mostra uma faixa com link; **nunca** `location.replace`/`href=` automático.
6. `check_site.py`, para cada página legal com mais de uma língua: (i) mesma data
   (`lastUpdated` do front-matter) em todas; (ii) mesmo número de `##`/`<h2>` e de `###`/`<h3>`;
   (iii) cada token em `` `código` `` da versão pt (permissões, `topowalk_pro`, eventos) aparece
   o mesmo número de vezes em cada tradução; (iv) cada nome de SDK de uma lista fixa (`Firebase
   Analytics`, `Firebase Crashlytics`, `Google Play Billing`, `Cloud Firestore`, `Google`) aparece
   em cada versão em que aparece no pt; (v) toda língua em `PAGINAS` gerou arquivo em `dist/`;
   (vi) nenhum arquivo em `dist/<lang>/` para língua fora do mapa. `--raiz dist` continua
   provando os contratuais.
7. `sync_legal.py`: o marcador `en: pendente` do WP-09 vira `pendente: [en, es, …]` — toda
   língua listada para a página fica pendente quando o pt muda; `check_site.py` falha com pendente.
8. ADR de i18n (`/adr`; o número é o próximo livre — o ADR-003 já é o Tailwind compilado, da branch do WP-08): "pt na raiz, demais línguas em `/<lang>/`, sem redirecionamento" — cita ADR-001.
9. `CLAUDE.md`: "inglês é espelho completo" vira "toda língua listada para uma página é espelho
   completo; língua não listada não aparece".

**Critérios de aceite:**
- Com o mapa só `['pt','en']`: `npm run build` e `diff -r` de `dist/` contra o build anterior
  ao WP mostram só o markup do seletor/`hreflang` — nenhuma página a mais nem a menos.
- `python3 tools/check_site.py --raiz dist` verde; os 7 caminhos de ADR-001 com `test -f`.
- `python3 tools/check_site.py --raiz tools/fixtures/i18n/<caso>` **falha** em cada caso
  sintético: data divergente, `h2` a menos, token `` `POST_NOTIFICATIONS` `` ausente, SDK ausente,
  língua no mapa sem arquivo, arquivo em `/ru/` fora do mapa, `pendente` no front-matter; e passa
  no caso correto. Saída colada no WP.
- `grep -rn "location.replace\|location.href *=" src/` vazio (sem redirect automático).
- `grep -c 'hreflang' dist/topowalk-privacy.html` = nº de línguas da página + 1 (`x-default`).

**Herdado do WP-08 (fatia 9):** a gravação de `ghf_lang` no `localStorage` foi removida por não ter leitor (`GHF-LANG-SEM-CONSUMIDOR-01`, privacy-first). A escolha de idioma (D8 c1) nasce aqui, gravação e leitor juntos. `data-troca-idioma` em `TrocaIdioma.astro` também ficou sem consumidor: usar ou remover (`TROCA-IDIOMA-ATRIBUTO-SEM-CONSUMIDOR-01`).

**Só no navegador:** com uma página de teste local mapeada para `['pt','en','es']` (não
publicada): 360 e 1280, seletor mostra 3 línguas e troca preservando a página; navegador em
`es` vê a faixa de sugestão na URL pt e **continua na URL pt**; página com `['pt']` sem
seletor. O usuário reporta.

**Irreversível:** nada sai do ar — pt continua no caminho atual. O que fica difícil de desfazer
é publicar `/<lang>/…`: depois que o Google indexa, mudar o esquema vira redirecionamento. Por
isso o esquema vai em ADR antes de qualquer língua nova ir para `master`.

**Risco:** alto — mexe no roteamento em volta das URLs contratuais. Específico: o i18n
routing do Astro com `prefixDefaultLocale: false` e `build.format: 'file'` gerar `/pt/…` ou
`index.html` em vez do caminho literal; mitigação: `check_site.py --raiz dist` no CI (WP-05).

---

## Veredito do arquiteto (2026-10-16)

**O WP-15 está aprovado com mudanças. Ele substitui os Passos, os Arquivos-alvo e os Critérios
acima onde houver conflito.** O texto acima foi escrito antes dos WP-08/09/11/21. O `Seo.astro` não
existe: o head é `src/layouts/Base.astro`. O formato do build é `'preserve'` (ADR-002 §2), e não
`'file'`. O marcador do WP-09 é `en: "pendente"`, em `src/content.config.ts:31`. O ADR deste WP é a
**ADR-007**. Agora o tamanho é **L**: são 20 páginas reescritas como cascas, mais o check e os
fixtures. O risco continua **alto**.

### Confronto com o código (o que já existe)
- A mesma lista de pares en está escrita à mão em quatro lugares: `COM_PAR_EN` (`src/i18n/ui.ts:61`),
  `EN_PENDENTE`/`COM_PAR` (`tools/check_site.py:130-132`), `INDEXAVEIS` (`:719`) e o sitemap
  (`src/pages/sitemap.xml.ts:9`). As línguas pt/en também aparecem fixas em
  `Base.astro:107-109,121`, `TrocaIdioma.astro:16-18`, no §4/§8/§9/§12/§14 do check e em
  `sync_legal.py:239`.
- O `x-default` → en já existe nas 20 páginas (D18, WP-11). Conferido em `dist/index.html`,
  `dist/en/index.html` e `dist/topowalk-privacy.html`, com `grep -c 'hreflang="x-default"'` = 1 em
  cada uma.
- O §12 do check já compara contagens de `##`, `###` e crases entre pt e en. O WP generaliza essa
  regra, e não a cria do zero.

### Achados roteados: destino
| Achado | Destino |
|---|---|
| `HOME-HREFLANG-XDEFAULT-01` | **resolvido** pelo WP-11 (D18). Ver a evidência acima. O WP-15 só generaliza a regra pelo mapa (ADR-007 §4). |
| `LEGAL-SLUG-ACENTO-01` | **WP-15, commit 5.** O `id` passa a vir da posição (`secao-2`, `secao-2-1`), igual em todas as línguas (ADR-007 §6). Esses `id`s nunca foram publicados, porque `origin/master` não tem `id` nos títulos legais. Trocar agora não custa nada. |
| `TROCA-IDIOMA-ATRIBUTO-SEM-CONSUMIDOR-01` | **WP-15, commit 4. A premissa do achado está errada:** o atributo é lido em `tools/check_site.py:559`, onde o §9 isenta o link de troca de idioma. O atributo fica, com o mesmo nome, em cada link do `SeletorIdioma`, e o §9 generalizado passa a ler o atributo. |

### Esquema e geração (ADR-007)
- O pt fica literal em `src/pages/<x>.astro`, sem mudança de caminho. As outras línguas saem de
  `src/pages/[lang]/<x>.astro`, onde `getStaticPaths()` devolve `linguasDe('<x>')` sem o `pt`. Os 10
  `src/pages/en/*.astro` literais são substituídos por essas 10 rotas dinâmicas. Com o mapa só
  pt/en, a saída é a mesma: `en/<x>.html` e `en/index.html`. O corpo de cada página vira um
  componente com a prop `lang`, e a casca pt e a casca `[lang]` só passam a prop. O 404 continua só
  em pt.
- O `i18n` do `astro.config.mjs` **não** é usado, e o `astro.config.mjs` sai dos Arquivos-alvo.
- **Medir antes de seguir (commit 3):** `[lang]/index.astro` com `lang=en` tem de gerar
  `dist/en/index.html` com `format: 'preserve'`. Se gerar `en.html`, o WP para e volta ao arquiteto.

### Fonte única
`src/i18n/idiomas.json` (ADR-007 §2) substitui o `idiomas.ts` como fonte. Nele, a lista `idiomas`
começa só com **pt e en**. es, fr, it, de e ru entram com os metadados e o bloco de `ui.ts` no WP
que publica cada língua (WP-16/17/18). O WP-15 não escreve rótulo de língua sem página. Os leitores
do JSON:
- `src/i18n/idiomas.ts`: valida e tipa. `Idioma` passa a ser derivado do JSON, e `rota()` e
  `COM_PAR_EN` saem de `ui.ts`.
- `Base.astro`, `sitemap.xml.ts`, `Footer`/`Nav`/`Home` (pelo `rota()`) e `legal.ts` (meses e
  rótulo, pelo JSON).
- `check_site.py` e `sync_legal.py`, pelo `json.load`. `PUBLICADAS` continua fixa como guarda: as
  chaves de `paginas` mais o convite têm de ser exatamente `PUBLICADAS`.

### Seletor e sugestão
- O `SeletorIdioma.astro` **substitui** o `TrocaIdioma.astro`, que é apagado.
  - Com 2 línguas, o markup gerado é **o de hoje** (um link para a outra língua, com `hreflang`,
    `lang`, `aria-label` e `data-troca-idioma`), para o `dist/` não mudar.
  - Com 3 ou mais, é uma lista de `<a hreflang lang>` com o nome nativo, e a língua atual leva
    `aria-current="true"`. É HTML sem JS, e o desenho vem do handoff `Site Nav.dc.html` (D4):
    `site-ux` DESENHAR antes do commit 4.
  - Com 1 língua, o seletor não aparece.
- A `SugestaoIdioma.astro` (D8 c1, ADR-007 §7) entra **nas 20 páginas pt/en já neste WP**. Um
  visitante com o navegador em en que abre a URL pt vê a faixa em inglês. É mudança visível,
  decidida na D8.
  - Copy da faixa: `band`/`bandGo` do handoff rodada 3, que é a fonte rastreável.
    - pt: "Esta página também está disponível em português." / "Ver em português"
    - en: "This page is also available in English." / "Switch to English"
  - O texto vai em `<template lang>`.
  - `localStorage.ghf_lang` é gravado só no clique do seletor ou da faixa, e lido só pela faixa.
  - `sessionStorage.ghf_faixa_idioma` guarda o fechamento.
  - Não há cookie nem rede.
  - Gravar a escolha em `localStorage` é **aceitável sob privacy-first**: guarda só o código da
    língua, sem identificador, não sai do navegador e é uma preferência pedida pelo próprio usuário.
    A D8 já decidiu isso.
  - A faixa é `position: fixed`. O Lighthouse do CI roda com `en-US`, então a faixa **aparece** nas
    páginas pt medidas, e o orçamento (D22) tem de continuar verde, com CLS 0.

### Regras novas do `check_site.py`
Elas valem para toda página com mais de uma língua no mapa, e os §4/§7/§8/§9/§12/§14 passam de
"pt e en" para "línguas do mapa".
- (i) Mesmo `lastUpdated` em todas as línguas.
- (ii) Mesma **sequência** de níveis `##`/`###`, e não só a mesma contagem: é a pré-condição das
  âncoras por posição.
- (iii) Cada `` `token` `` do pt aparece o mesmo número de vezes em cada tradução.
- (iv) A lista fixa de SDKs aparece onde aparece no pt.
- (v) Toda língua do mapa gerou o arquivo em `dist/`.
- (vi) Não existe `dist/<código>/` para língua fora do mapa da página, e nunca existe `dist/pt/`.
- (vii) Sem `pendente` no front-matter, e `.<código>.md` sem `origemCommit` nem `pendente`.
- (viii) `hreflang`: um por língua mais `x-default` (en se houver, senão pt), recíprocos. Uma página
  com uma língua só não tem `hreflang`.
- (ix) `og:locale:alternate` para cada outra língua.
- (x) Nenhum `location.replace`/`location.assign`/`location.href =`/`<meta http-equiv="refresh">` em
  `dist/`, fora do convite (CONGELADAS).
- (xi) Cada dicionário de `src/i18n/*.ts` tem as mesmas chaves em todos os blocos de língua, e
  `ui.ts` tem um bloco para cada língua de `idiomas.json`.
- (xii) As chaves de `paginas` mais o convite são `PUBLICADAS`.

**Fixtures:** um `dist/` sintético inteiro não serve, porque o check também lê `src/` da raiz e
cobra o §1/§11/§13. Por isso as regras (i)–(viii) e (xi) viram funções puras em
`tools/regras_i18n.py`, que recebem o mapa, os textos e a lista de arquivos. O `check_site.py` as
chama sobre o real. `tools/test_regras_i18n.py` (unittest, biblioteca padrão) as chama sobre
`tools/fixtures/i18n/<caso>/` (mapa JSON, `.md` e a lista de arquivos), com um caso correto e um caso
por regra. O teste entra como passo no job `site` do `pr.yml`, sem job novo e sem mexer no
`deploy.yml` (D9).

### `sync_legal.py`
`CHAVES` passa a ser `lastUpdated`, `origemCommit` e `pendente`. Ao copiar o pt, ele grava
`pendente: [<línguas do mapa, menos pt>]`, lidas do JSON. O schema de `content.config.ts` passa a
ser `pendente: z.array(z.enum(<códigos>)).nonempty().optional()`. `/legal` e `site-legal` passam a
tirar uma língua da lista por vez e a apagar a chave quando a lista esvazia.

### Arquivos-alvo (lista fechada, substitui a de cima)
- **i18n:** `src/i18n/idiomas.json` (novo), `src/i18n/idiomas.ts` (novo), `src/i18n/ui.ts`,
  `src/i18n/legal.ts`.
- **Páginas:** `src/pages/*.astro` (as 10 páginas pt viram cascas), `src/pages/en/**` (apagado),
  `src/pages/[lang]/*.astro` (novo, 10 arquivos) e `src/pages/sitemap.xml.ts`.
- **Componentes:** `src/components/` (o corpo de cada página como componente, além de `Nav`,
  `Footer`, `Home` e dos componentes de landing só no import de `rota`), `SeletorIdioma.astro`
  (novo), `SugestaoIdioma.astro` (novo) e `TrocaIdioma.astro` (apagado).
- **Layouts e conteúdo:** `src/layouts/Base.astro`, `src/layouts/LegalLayout.astro`,
  `src/markdown/legal.mjs` (só o `idDosTitulosLegais`) e `src/content.config.ts`.
- **Ferramentas:** `tools/check_site.py`, `tools/regras_i18n.py` (novo), `tools/test_regras_i18n.py`
  (novo), `tools/fixtures/i18n/**` (novo) e `tools/sync_legal.py`.
- **CI:** `.github/workflows/pr.yml`, só um passo no job `site`.
- **Instruções:** `.claude/commands/legal.md`, `.claude/agents/site-legal.md`,
  `.claude/commands/verify.md` (se citar `en: "pendente"`) e `CLAUDE.md` ("Produto e copy",
  "Arquitetura", "Comandos").
- **Fora:** `astro.config.mjs`, `public/**` e `deploy.yml`.

### Sequência de commits (cada um com `npm run build` + `check_site.py` verdes)
1. `WP-15: idiomas.json e idiomas.ts`. Liga o mapa, o `rota()` e o `Idioma` derivado do JSON.
   `ui.ts`, `sitemap.xml.ts` e `Base.astro` passam a ler o mapa, e `COM_PAR_EN` sai.
   `diff -r` do `dist/` contra a base: vazio.
2. `WP-15: check_site e sync_legal leem o mapa`. `regras_i18n.py`, a guarda (xii), o fim de
   `EN_PENDENTE`/`COM_PAR` à mão, `pendente: [...]` no `sync_legal.py` e no schema, e
   `legal.md`/`site-legal.md`. Junto entram os fixtures, o unittest e o passo no `pr.yml`.
3. `WP-15: [lang]/ no lugar de en/`. Cascas, componentes de página e a medição do
   `[lang]/index.astro`. `diff -r` do `dist/`: vazio.
4. `WP-15: SeletorIdioma`. Substitui o `TrocaIdioma`, com o §9 lendo o `data-troca-idioma` em
   qualquer língua. **Depende da D23** e do `site-ux` DESENHAR. `diff -r`: vazio com 2 línguas.
5. `WP-15: âncoras legais por posição` (`LEGAL-SLUG-ACENTO-01`) e a regra (ii) por sequência.
   `diff`: só `id="secao-…"` nas 10 legais.
6. `WP-15: SugestaoIdioma`. `diff`: só o `<template>`, o script da faixa e, eventualmente, o hash
   de `_astro/*.css` nas 20 páginas.
7. `WP-15: CLAUDE.md e ADR-007` (a ADR já está escrita; aqui ela só é citada) e a regra "toda
   língua listada é espelho completo; língua não listada não aparece".

### Critérios de aceite (substituem os de cima)
- **Lista de arquivos:** `diff <(cd base && find . -type f | sort) <(cd dist && find . -type f | sort)`
  é vazio, salvo o nome de `_astro/*.css`/`*.js` com hash. Nenhuma página a mais nem a menos.
- **Conteúdo:** `diff -r` do `dist/` contra o build de `0e6b666` mostra só os `id="secao-…"` das 10
  legais, a faixa (`<template>` e script) e o hash do CSS. Nenhuma linha de `<head>` muda: canonical,
  hreflang, og e JSON-LD iguais. A saída vai colada no WP.
- **Checks do site:**
  - `python3 tools/check_site.py --raiz dist` verde.
  - `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` verde.
  - Os 7 caminhos de ADR-001 passam no `test -f`.
  - `test ! -e dist/pt`.
- **Testes das regras:** `python3 -m unittest tools/test_regras_i18n.py` verde. Cada caso inválido
  (data divergente, `###` fora de ordem, `` `POST_NOTIFICATIONS` `` ausente, SDK ausente, língua
  do mapa sem arquivo, `dist/ru/` fora do mapa, `pendente` no front-matter, ui.ts sem bloco de
  língua do mapa) falha com a mensagem esperada, e o caso correto passa. A saída vai colada no WP.
- **Redirect:** `grep -rnE "location\.(replace|assign)|location\.href *=|http-equiv=\"refresh\"" src/ dist/ --exclude-dir=lotto-expert`
  vazio.
- **hreflang:** `grep -o '<link rel="alternate" hreflang=' dist/topowalk-privacy.html | wc -l`
  = nº de línguas da página + 1 (`x-default`) = 3. Medido hoje: `grep -o 'hreflang=' … | wc -l`
  = 5, que são os 3 do head mais os 2 links do seletor (desktop e celular). Esse total também não
  muda.
- **CI:** `npx html-validate 'dist/**/*.html'` e `lychee` verdes. O job `lighthouse` do PR verde
  (D22), com CLS ≤ 0,1 e a faixa visível nas páginas pt medidas.

### Só no navegador (substitui o de cima)
Primeiro, `python3 -m http.server 8080 -d dist`. Depois:
- Com o Chrome em **en**, a 360 e a 1280, em `/topowalk-privacy.html`: a faixa em inglês aparece,
  a URL continua pt e o conteúdo não pula.
- "Switch to English" leva a `/en/topowalk-privacy.html`.
- Ao recarregar `/topowalk-privacy.html` depois de escolher en: a faixa sugere en de novo, mas
  nada redireciona. Ao fechar a faixa: ela não volta na mesma aba.
- Com o Chrome em **pt-BR**, em `/`: nenhuma faixa.
- O seletor pt/en continua como hoje.
- O seletor com 3 ou mais línguas é provado no WP-16, a primeira página com 6.

O usuário reporta.

### Decisões
- **D23 (aberta, registrada em `decisoes.md`):** para onde vai o link quando o destino não tem a
  língua atual. Recomendada: (A) en se houver, senão pt. **Bloqueia só o commit 4** e o §9
  generalizado. Os commits 1–3 não dependem dela, porque com o mapa pt/en todas as opções dão o
  mesmo `dist/`.
- Nenhuma outra. D8 (c1) já decidiu o `localStorage`, e D18 já decidiu o `x-default`.

### Impacto nos WPs seguintes
- **WP-16, WP-17 e WP-18:** cada um passa a ter em Arquivos-alvo a entrada da língua em
  `idiomas.json` (`idiomas` e `paginas`), o bloco dela em `src/i18n/ui.ts` (copy da faixa e do
  seletor tirada do handoff) e o orçamento das páginas novas em `tools/orcamento-lighthouse.json`,
  se forem medidas.
- **`site-docs`:** ajustar esses três WPs no fechamento deste.

---

## Execução

Linha de base: `npm run build` em `fb68942` (veredito), copiado para o scratchpad da sessão.

### Commit 1 — `idiomas.json` e `idiomas.ts`
`diff -r <base> dist` (saída inteira):

```
(vazio)
```

### Commit 2 — `check_site` e `sync_legal` leem o mapa
`python3 -m unittest -v tools/test_regras_i18n.py`:

```
test_cada_caso_falha_pela_sua_regra (tools.test_regras_i18n.RegrasI18n.test_cada_caso_falha_pela_sua_regra) ... 
  [data-divergente] app-privacy.es.md: `lastUpdated` '2026-09-30' ≠ o do pt '2026-10-12' (regra i)
  [guarda] idiomas.json: app.html está em PUBLICADAS e falta em `paginas` (regra xii)
  [h3-fora-de-ordem] app-privacy.es.md: sequência de títulos `##`/`###` diverge do pt no título 3 (4 títulos, pt tem 4) — a âncora por posição sairia trocada (regra ii)
  [hreflang-sem-x-default] es/app-privacy.html: hreflang [('en', 'https://ghfsoftware.com/en/app-privacy.html'), ('es', 'https://ghfsoftware.com/es/app-privacy.html'), ('pt-BR', 'https://ghfsoftware.com/app-privacy.html')] ≠ esperado [('en', 'https://ghfsoftware.com/en/app-privacy.html'), ('es', 'https://ghfsoftware.com/es/app-privacy.html'), ('pt-BR', 'https://ghfsoftware.com/app-privacy.html'), ('x-default', 'https://ghfsoftware.com/en/app-privacy.html')] (x-default = en se houver, senão pt; regra viii)
  [lingua-sem-arquivo] es/app-privacy.html: ausente — app-privacy.html tem `es` no mapa (regra v)
  [linha-de-data-errada] app-privacy.es.md: linha de data ['12 de septiembre de 2026'] ≠ 2026-10-12
  [origem-na-traducao] app-privacy.en.md: `origemCommit` na tradução — proveniência e marcador ficam só no .pt.md (regra vii)
  [pendente] app-privacy.pt.md: `pendente: ['es']` — tradução atrás do pt; traduzir e tirar cada língua da lista (regra vii)
  [pt-na-pasta] pt/app-privacy.html: `pt/` não existe — o pt fica na raiz (ADR-007 §1, regra vi)
  [ru-fora-do-mapa] ru/app-privacy.html: `ru` fora do mapa de app-privacy.html — página sem a língua não é gerada (regra vi)
  [sdk-ausente] app-privacy.es.md: sem `Firebase Analytics`, que o pt cita (regra iv)
  [token-ausente] app-privacy.en.md: `POST_NOTIFICATIONS` 0× ≠ 1× no pt (regra iii)
  [ui-sem-bloco] ui.ts: sem bloco `es` — toda língua de idiomas.json tem o seu em ui.ts (regra xi)ok
test_correto_passa (tools.test_regras_i18n.RegrasI18n.test_correto_passa) ... ok
test_data_em_qualquer_lingua (tools.test_regras_i18n.RegrasI18n.test_data_em_qualquer_lingua) ... ok
test_hreflang_sem_en_aponta_para_pt (tools.test_regras_i18n.RegrasI18n.test_hreflang_sem_en_aponta_para_pt) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.011s

OK
```

`diff -r <base> dist`: vazio (o commit não muda o gerado). `check_site.py` verde; provado à mão sobre o real (revertido): `pendente` no `.pt.md`, `lastUpdated` divergente, `dist/ru/` e `dist/pt/`, `location.replace` em `dist/en/`, token, SDK, linha de data e `###` a menos no en — cada um reprovou pela sua regra.

---

### Commit 3 — `[lang]/` no lugar de `en/`
Medição (ADR-007 §3): `src/pages/[lang]/index.astro` com `lang=en` e `build.format: 'preserve'`
gera `dist/en/index.html`; `dist/en.html` não existe; `dist/pt` não existe.

`diff -r <base> dist` (saída inteira) e lista de arquivos:

```
(vazio)
$ diff <(cd base && find . -type f | sort) <(cd dist && find . -type f | sort)
(vazio)
```

Os 7 caminhos de ADR-001 com `test -f`: ok. `grep -o '<link rel="alternate" hreflang=' dist/topowalk-privacy.html | wc -l` = 3;
`grep -o 'hreflang=' … | wc -l` = 5 (igual à base). `grep -rnE "location\.(replace|assign)|location\.href *=|http-equiv=\"refresh\"" src/ dist/ --exclude-dir=lotto-expert`: vazio.

### Commit 4 — `SeletorIdioma` e `rota()` com a D23
`SeletorIdioma.astro` no lugar do `TrocaIdioma.astro` (apagado); `rota()` com a D23 (A) e
`link()`/`atributosLink()` em `idiomas.ts`, que acrescentam `hreflang`/`lang` do destino quando ele
está em outra língua. Nav, Footer, Home, as duas landings com link de política e o "voltar" do
`LegalLayout` passam a espalhar esses atributos (`<a {...link(lang, x)}>`), em vez de `href={rota(…)}`:
é o único jeito de o atributo sair do `rota()` e não de cada página (especificação, §1). §9 do
`check_site.py` vale para toda página do mapa (pt inclusive), pela `regras_i18n.regra_link`; a 404
(fora do mapa, bilíngue por desenho) fica de fora. Chave `idioma` nova em `ui.ts` (pt/en), usada só
com 3+ línguas.

`diff -r <base> dist`, com o nome `_astro/Base.<hash>.css` normalizado: **HTML idêntico**, mesma lista
de arquivos. O CSS muda (o Tailwind lê as classes do ramo `n ≥ 3` do componente, que nenhuma página
publicada renderiza): só regras novas, nenhuma removida.

```
== lista de arquivos (CSS normalizado)
== diff -r sem o CSS
== CSS: regras novas
> .top-full  .mt-2  .h-2.5  .h-px  .min-h-11  .w-2.5  .w-[220px]  .shrink-0  .list-none  .gap-0.5
> .overflow-y-auto  .break-words  .bg-gray-700  .p-1.5  .py-28  .text-[13px]  .text-[15px]
> .[justify-content:safe_center]  .hover:bg-white/5  .focus-visible:outline-offset-2
> .focus-visible:outline-white  .[&::-webkit-details-marker]:hidden
```

Mutação no `dist/` real (revertida): `en/topowalk.html` apontando para `/topowalk-privacy.html` e
`topowalk.html` para `/en/topowalk-privacy.html` — os dois reprovam no §9. `unittest`: 5 testes,
`test_link_d23` novo (mesma língua; fallback en com `hreflang`/`lang`; fallback errado; pt também
conferido; seletor isento; fora do mapa).

**Prova de 3 e de 1 língua (build descartável numa cópia do repositório, nada commitado):** mapa com
`topowalk.html: [pt, en, es]` (es = cópia do en, sem conteúdo real) e `eclipsego.html: [pt]`.
`check_site.py` na cópia: só a regra xi (o bloco `es` de `ui.ts` era um getter, que o check não lê —
esperado); §9 e hreflang verdes; html-validate verde.

- `es/topowalk.html`, barra (desktop): `<details data-seletor-idioma>` com `<summary>` (globo +
  `<span lang="es">Español</span>` + seta) e `<ul aria-label="Language">` com
  `<a href="/topowalk.html" hreflang="pt-BR" lang="pt-BR" data-troca-idioma="pt">Português</a>`,
  `…/en/topowalk.html … data-troca-idioma="en">English`,
  `…/es/topowalk.html … data-troca-idioma="es" aria-current="true">Español` + check; o script do
  `<details>` (Esc, clique fora, foco fora) só aparece nessa página.
- Barra do celular: vazia antes do botão do menu. Menu do celular: separador, "Language" e grade
  `grid-cols-2` com os 3 links (bolinha preenchida no atual, `aria-current`); overlay com
  `[justify-content:safe_center] py-28 overflow-y-auto`.
- `<head>`: hreflang pt-BR/en/es + x-default→en; `og:locale` es_ES + 2 `og:locale:alternate`.
- D23 no nav/footer de `es/topowalk.html`: `<a href="/en/" hreflang="en" lang="en">` (home sem es),
  `/en/lottoexpert-privacy.html … hreflang="en" lang="en"`, e `/eclipsego.html hreflang="pt-BR"
  lang="pt-BR"` (página só pt).
- `eclipsego.html` com `[pt]`: 0 `hreflang`, 0 `og:locale:alternate`, 0 `data-troca-idioma`, 0
  `<details>`; `en/eclipsego.html` não gerado; links de `en/index.html` para ela com `hreflang="pt-BR"`.

Verificação: `npm run build`, `check_site.py`, contrato sha256, html-validate, lychee (0 erros),
`unittest` OK, `gen_estado --check`, `check_plano` — verdes. Os 7 caminhos de ADR-001 com `test -f`;
`test ! -e dist/pt`; hreflang do head de `topowalk-privacy.html` = 3, total = 5; grep de redirect vazio.

### Commit 5 — âncoras legais por posição
`idDosTitulosLegais` (`src/markdown/legal.mjs`) dá o `id` pela posição: `secao-2`, `secao-2-1`. A
regra (ii) por sequência já estava no commit 2. **`LEGAL-SLUG-ACENTO-01` resolvido** (a linha em
`achados-novos.md` fica para o `site-docs`, que não está nos Arquivos-alvo deste WP).

`diff -r <base> dist` (CSS normalizado como no commit 4), com os `id="secao-…"` trocados por um
marcador: as 10 legais ficam iguais à base, e nenhum outro arquivo muda. Lista de arquivos idêntica.

```
arquivo                     igual sem os ids   ids base → ids novos   exemplo
eclipsego-privacy.html      sim                11 → 11   secao-21-localização-do-dispositivo-gps → secao-2-1
en/eclipsego-privacy.html   sim                11 → 11   secao-21-device-location-gps → secao-2-1
lottoexpert-privacy.html    sim                24 → 24   secao-1-princípio-geral-privacidade-por-padrão → secao-1
en/lottoexpert-privacy.html sim                24 → 24
lottoexpert-terms.html      sim                13 → 13   secao-2-isenção-de-responsabilidade → secao-2
en/lottoexpert-terms.html   sim                13 → 13
poleposition-privacy.html   sim                25 → 25   secao-resumo-de-segurança-dos-dados-google-play → secao-2
en/poleposition-privacy.html sim               25 → 25
topowalk-privacy.html       sim                44 → 44   secao-21-localização-gps → secao-2-1
en/topowalk-privacy.html    sim                44 → 44
```

Os `id`s do pt e do en são iguais nas 5 políticas (`grep -o 'id="secao-[^"]*"'`, pt = en), sem
repetição. Nenhum link interno para `#secao-…` em `dist/` (nada a atualizar). Verificação completa
verde (a mesma lista do commit 4).

### Commit 6 — `SugestaoIdioma`
`SugestaoIdioma.astro` montada pelo `Base.astro` no fim do `<body>` (depois do footer). Um
`<template data-faixa-idioma lang>` por outra língua da página, com `<section aria-label>` (landmark
`region`; o html-validate recusa `role="region"` em `<div>`), texto `band`, link `bandGo` e ✕
`close` do handoff, na língua sugerida. Script: preferência = `localStorage.ghf_lang` se está na
página, senão a primeira de `navigator.languages` que a página tem; faixa só se ≠ língua da página e
`sessionStorage.ghf_faixa_idioma ≠ "off"`; inserida no `load`, entra por `opacity`/`translate-y` em
200 ms (`motion-reduce:transition-none`); ✕ e Esc gravam `"off"` e removem. `ghf_lang` é gravado só
no clique de um `a[data-troca-idioma]` (seletor ou faixa), sem `preventDefault`: a navegação é a do
`<a href>`. Storage em `try/catch`. Chaves novas em `ui.ts` (pt/en): `faixa_idioma`, `faixa_ir`,
`fechar` (`idioma` veio no commit 4). 404 e página de uma língua: nada.

O link da faixa leva `data-troca-idioma` (isento no §9) e `lang` pelo `<section lang>`, mas **não**
`hreflang`: o critério "total de `hreflang=` em `topowalk-privacy.html` = 5" continua valendo (medido: 5).

`diff -r <base> dist` (CSS normalizado, `id="secao-…"` do commit 5 neutralizados): lista de arquivos
idêntica; 20 páginas mudam, e as 20 ficam iguais à base depois de tirar o `<template>` (1 por página)
e o `<script>` da faixa. O CSS ganha as classes da faixa (`inset-x-3`, `bottom-[calc(…env(safe-area-inset-bottom))]`,
`md:left-4`, `md:max-w-[560px]`, `translate-y-*`, `transition`, `duration-200`, `motion-reduce:transition-none`…).

Prova no Chromium headless (`--dump-dom` depois do `load`): com o navegador em en-US, a faixa é
inserida em `/lottoexpert-privacy.html` e não em `/en/`; em pt-BR, o contrário.

Lighthouse local, 1 run, navegador em en-US como no CI (`LANG=en_US.UTF-8`; a faixa aparece nas
páginas pt medidas):

```
/                            perf  98 · a11y  95 · bp 100 · seo 100 · LCP 2.33 s · CLS 0.000 · 294 KB (img 116 KB)
/lottoexpert.html            perf  95 · a11y  96 · bp 100 · seo 100 · LCP 2.25 s · CLS 0.000 · 254 KB (img 45 KB)
/topowalk.html               perf  99 · a11y  96 · bp 100 · seo 100 · LCP 2.03 s · CLS 0.000 · 177 KB (img 18 KB)
/poleposition.html           perf  99 · a11y  94 · bp 100 · seo 100 · LCP 2.10 s · CLS 0.000 · 218 KB (img 38 KB)
/eclipsego.html              perf  99 · a11y  94 · bp 100 · seo 100 · LCP 1.95 s · CLS 0.000 · 173 KB (img 22 KB)
/lottoexpert-privacy.html    perf  99 · a11y  90 · bp 100 · seo 100 · LCP 1.95 s · CLS 0.000 · 179 KB (img 9 KB)
/lottoexpert-terms.html      perf  99 · a11y  90 · bp 100 · seo 100 · LCP 1.80 s · CLS 0.000 · 158 KB (img 9 KB)
/eclipsego-privacy.html      perf  99 · a11y  94 · bp 100 · seo 100 · LCP 1.80 s · CLS 0.000 · 151 KB (img 9 KB)
/404.html                    perf 100 · a11y 100 · bp 100 · seo  66 · LCP 1.50 s · CLS 0.000 · 111 KB (img 0 KB)

✅ orçamento cumprido
```

Elemento LCP: o logo do nav em `/`, um `<p>` do corpo em `/lottoexpert-privacy.html` — não a faixa.
O a11y 90 das legais é o da base: mesmas auditorias reprovadas antes e depois (`color-contrast` e
`link-in-text-block` nos links externos do corpo, `heading-order` no `<h4>` do footer); a faixa não
acrescenta nenhuma.

Verificação completa verde (§16 inclusive). `grep -rnE "location\.(replace|assign)|location\.href *=|http-equiv=\"refresh\"" src/ dist/ --exclude-dir=lotto-expert`: vazio.

### Commit 7 — `CLAUDE.md` e ADR-007
"Produto e copy": "toda língua listada para uma página em `src/i18n/idiomas.json` é espelho
completo, nunca parcial; língua não listada não aparece", pt na raiz e as outras em `/<código>/`,
sem redirecionamento (ADR-007). "Arquitetura": `tools/` (regras_i18n.py, test_regras_i18n.py,
fixtures/i18n/), Base (hreflang pelo mapa, faixa no fim do `<body>`), components (SeletorIdioma,
SugestaoIdioma, `paginas/`), i18n (`idiomas.json` como fonte única, `idiomas.ts` com
`linguasDe`/`rota`/`link` e a D23), `pendente: [códigos]`, ids legais por posição, `pages/[lang]/`
(nunca `pt/`). "Comandos": `python3 -B -m unittest tools/test_regras_i18n.py` e o passo no job
`site`. `dist/` não muda. Verificação completa verde.

O achado `TOOLS-PYCACHE-GITIGNORE-01` **não** foi resolvido aqui: `.gitignore` não está nos
Arquivos-alvo. O `-B` nos comandos de teste evita o `tools/__pycache__` enquanto isso.

## Especificação do site-ux (2026-10-16)

Modo DESENHAR, para os commits 4 (`SeletorIdioma`) e 6 (`SugestaoIdioma`). D23 = (A): link para
página sem a língua atual vai para **en** se a página tiver en, senão **pt** (mesma regra do
`x-default`). Fonte visual: `design/handoff/2026-10-13-rodada-3/Site Nav.dc.html` (prevalece sobre o
HTML) e `content/i18n.js`. O handoff é um protótipo em estilo inline; aqui só se tiram **estrutura,
medidas e comportamento**. Cor, fonte e classes saem dos tokens atuais (`tailwind.config.mjs`,
`src/styles/global.css`). Nenhum token novo.

### 0. Onde o handoff e o site divergem (decisão já tomada ou do humano)

| Ponto | Handoff | Site hoje / WP | Resolução |
|---|---|---|---|
| 2 línguas | grupo segmentado `PT`/`EN` com `aria-pressed` (`Site Nav.dc.html:44-50`, `two: avail.length<=3`, linha 138) | link único com globo + código da outra língua | **Fica o de hoje** (critério `diff -r` vazio). Reconciliar com o segmentado é decisão de produto, fora do WP-15: vira linha em `achados-novos.md` (`SELETOR-2-LINGUAS-FORA-DO-HANDOFF-01`). |
| 3 línguas | ainda segmentado (≤3) | arquiteto: 3+ = lista | **Lista a partir de 3.** Divergência assumida; o segmentado com 3 códigos de 2 letras não tem nome nativo (WCAG 2.5.3 / 1.1). |
| Lista com 4+ | botão + `ul` de `<button>` com `aria-haspopup="true"` (`:53-65`) | links `<a hreflang>` | **Links, não botões** (ADR-007: é navegação para outra URL). `aria-haspopup` sai: promete `role=menu` com setas, que o handoff não implementa. Padrão adotado: botão de disclosure (`aria-expanded`). |
| Faixa de sugestão | no topo, **em fluxo**, empurra o nav (`:10-21`) | nav é `fixed` (`Nav.astro:88`) | **Sem referência no handoff para `position: fixed`.** Posição e overlay da faixa abaixo são proposta do site-ux; o usuário confirma no navegador. |
| Breakpoints do nav | 600 / 1024 (`:105`) | menu desktop em `md` (768) | Mantém o `md` do site. Sem referência no handoff para a quebra em 768. |

### 1. `SeletorIdioma.astro` (substitui `TrocaIdioma.astro`)

**Props:** `lang`, `caminho` (pt), `class` (como hoje) e `posicao: 'barra' | 'menu'`. As línguas vêm
de `linguasDe(pagina)` em `idiomas.ts`; o componente não conhece a lista.

**Regra por número de línguas `n` da página:**

- `n = 1`: não renderiza nada (nem wrapper, nem `<span>` vazio).
- `n = 2`: **idêntico ao `TrocaIdioma.astro` de hoje**, byte a byte: `<a href hreflang lang aria-label
  data-troca-idioma class><Icon globo/><span>EN|PT</span></a>`. A cópia das classes `trocaDesktop` /
  `trocaCelular` do `Nav.astro` não muda. `posicao` é ignorado.
- `n >= 3`: abaixo.

**`n >= 3`, `posicao='barra'` (>= md):** lugar do `TrocaIdioma` atual (depois dos itens, com a
mesma borda `border-l border-gray-700 pl-6 ml-2`).
- Gatilho: `<button type="button" aria-expanded="false" aria-controls="<id>">`, ícone `globe`
  + nome nativo da língua atual (`<span lang>`) + seta. Mín. 44 px de altura, `rounded-full`,
  borda `border-gray-500` (não `gray-700`: 3:1 contra `brand-base` para o limite do controle),
  texto `text-gray-300`, hover `text-white`. Sem rótulo extra: o nome visível já contém o
  rótulo acessível (WCAG 2.5.3). O painel é `<ul aria-label="{idioma}">` (chave `idioma`, §2).
- Painel: `<ul>` posicionado `absolute right-0 top-full mt-2`, largura 220 px (`w-[220px]`,
  `Site Nav.dc.html:57`), `bg-brand-surface border border-gray-600 rounded-xl shadow-xl`, `p-1.5`,
  `gap-0.5`. Máx. de altura = a lista toda (7 itens x 44 = 308 px + padding: cabe em 1280x720).
- Item: `<li><a href hreflang lang data-troca-idioma="<código>">Nome nativo</a></li>`, `min-h-11`
  (44 px), `px-3`, `rounded-lg`, texto 15 px. Língua atual: `aria-current="true"`, fundo
  `bg-white/5` e check à direita (o ícone `check`, se existir em `Icon.astro`; senão, um
  `border-r-2 border-b-2` rotacionado como em `:63`), cor `brand-primary`. **O atual não é
  apenas cor:** tem check e `aria-current`.
- Os nomes são sempre nativos e cada `<a>` leva `lang` próprio: `Português`, `English`, `Español`,
  `Français`, `Italiano`, `Deutsch`, `Русский` (fonte: `nome` em `idiomas.json`; handoff: `NAMES`,
  `Site Nav.dc.html:130`). Sem bandeira. O nome da língua atual no gatilho é o mesmo texto (não a sigla).

**Estados do painel (só n >= 3):** fechado (padrão) / aberto. Sem JS o painel precisa existir:
renderizar com `<details><summary>` como base (abre/fecha nativo, sem script) e o script de
~15 linhas só acrescenta o fechamento. Se o site-dev preferir o `<button aria-expanded>` do handoff,
o estado sem JS é "painel sempre visível dentro do menu mobile e escondido na barra"; a escolha
do site-dev tem de manter a lista **acessível sem JS**, porque é a única forma de achar a página
em outra língua. Recomendação do site-ux: `<details>`.
- Teclado: `Enter`/`Espaço` no gatilho abre; `Tab` percorre os links na ordem do DOM; `Esc` fecha
  e devolve o foco ao gatilho; `Tab` para fora do painel fecha. Clique fora fecha. **Sem setas**:
  não é `role=menu`, então sem armadilha de teclado (WCAG 2.1.1/2.1.2).
- Foco visível: `outline outline-2 outline-offset-2 outline-white` (`focus-visible:`). O site hoje
  não tem estilo de foco global (`grep focus src/styles/global.css` vazio) e o botão do menu usa
  `focus:outline-none` (`Nav.astro:129`): isso é **achado fora do diff**
  (`NAV-FOCO-VISIVEL-01`), não se corrige neste commit. O seletor novo já nasce com foco
  visível; o handoff usa 2 px em `--br` `#3CC8D0` (`:51`), e `white` evita o terracota
  `#B5541C` do TopoWalk (~3,2:1 sobre `#111827`, no limite).
- Movimento: sem animação de entrada (abre instantâneo). Não há nada a reduzir.

**`n >= 3`, `posicao='menu'` (< md, dentro de `#mobile-menu`):** sem reaproveitar o painel.
Referência: handoff `sheetLang` (`Site Nav.dc.html:88-99`, abaixo de 600 px).
- No overlay existente (`Nav.astro:140`), depois dos links e do separador `h-px bg-gray-700`:
  rótulo "Idioma" (13 px, `text-gray-400`, 600) e uma grade `grid grid-cols-2 gap-1` de
  `<a href hreflang lang data-troca-idioma>`, `min-h-11`, texto 15 px, `rounded-lg`. Atual:
  `aria-current="true"` + bolinha preenchida à esquerda (anel `border-brand-primary`), não só cor
  (`:94`).
- Na barra do celular, para `n >= 3`, **não** há atalho ao lado do botão do menu (some o
  `trocaCelular`): vale o que o handoff faz abaixo de 600 px (`barLang: bp!=='m'`, `:140`).
  Para `n = 2` o link da barra continua como hoje.
- O overlay é `justify-center` e sem scroll. Com a grade de 7 línguas (4 linhas x 44 + gaps)
  mais 4-5 links em 360x640 o conteúdo pode passar de 640 px. Pedido ao site-dev: `overflow-y-auto`
  e `justify-start`/`safe center` no overlay **só quando houver o bloco de idiomas** (com 2 línguas,
  o overlay não muda). Verificar a 360x640 e 360x568.
- Ao ativar um link de idioma, a página muda; não há estado do menu a fechar (navegação completa).
- Alemão/russo: o nome é o próprio nome (não "35% mais longo"), mas o painel tem `w-[220px]`
  e a grade `1fr 1fr` aceita `Русский`/`Français` a 360 px (cada coluna ~150 px). Sem truncar:
  `break-words`, nunca `truncate`.

**D23 no resto do nav (não é o seletor):** o seletor só lista línguas que existem para a
página atual, então seus links nunca caem em fallback. A regra (A) vale para `rota(lang, caminho)`
usado em Nav/Footer/Home/landings quando a página-destino não tem a língua atual (ex.: `/es/`
numa landing que linka a `lottoexpert-privacy.html`, só pt/en). Para o desenho:
- Esses links levam `hreflang` e `lang` do destino **quando a língua do destino difere da
  da página** (WCAG 3.1.2): leitor de tela lê em en/pt certo. O site-dev emite o atributo no
  `rota()`/componente de link, não em cada página.
- Sem indicação visual (sem selo "EN"): o brief não pede, e o texto do link já fica na língua da
  página. **Sem referência no handoff** para marcar visualmente o link que muda de língua; se o
  usuário quiser, é decisão dele (Claude Design). Registrado em `achados-novos.md` como
  `LINK-FALLBACK-IDIOMA-SEM-SINAL-01`.

**Uma coisa que o §9 do `check_site.py` precisa ler:** `data-troca-idioma="<código>"` em **todo**
`<a>` do seletor (barra e menu), com o código da língua de destino. Atributo do link, não do wrapper.

### 2. `SugestaoIdioma.astro` (D8 c1, ADR-007 §7)

**Copy (do handoff, nada de texto novo):**

| Chave | pt | en | Fonte |
|---|---|---|---|
| `band` | Esta página também está disponível em português. | This page is also available in English. | `content/i18n.js:4` (pt), `:6` (en) |
| `bandGo` | Ver em português | Switch to English | `content/i18n.js:4`, `:6` |
| `close` | Fechar | Close | `content/i18n.js:3`, `:5` |
| `language` | Idioma | Language | `content/i18n.js:3`, `:5` |

(es/fr/it/de/ru estão em `content/i18n.js:8,10,12,14,16` e entram com cada língua, WP-16/17/18.)
**A copy da faixa é sempre na língua sugerida**, não na da página atual. Por isso o `<template>`
carrega **um bloco por língua da página que não seja a atual**, cada um com `lang="<código>"`; o
script escolhe e clona o bloco certo (o handoff faz o mesmo: `T(sug,'band')`, `Site Nav.dc.html:141`).
Chaves novas em `ui.ts` por língua: `faixa`, `faixaIr`, `fechar`, `idioma` (nomes a critério do dev;
conteúdo = tabela).

**Quando aparece (todas as condições):**
1. A página tem 2+ línguas (`n >= 2`); com `n = 1` o componente nem entra no HTML.
2. Língua preferida = `localStorage.ghf_lang`, se existir e estiver em `linguasDe(pagina)`;
   senão a **primeira** entrada de `navigator.languages` (`navigator.language` se vazio) cujo
   prefixo de 2 letras (`pt-BR`, `pt-PT` → `pt`) esteja em `linguasDe(pagina)` (`Site Nav.dc.html:113-115`).
   Entrada que não existe na página é pulada (`["fr","en"]` numa página pt/en → `en`).
3. Preferida **diferente** da língua da página (`<html lang>` / prop `lang`).
4. `sessionStorage.ghf_faixa_idioma` ≠ `"off"` (o handoff usa `ghf-lang-band`, `:109`; o nome do
   ADR-007 prevalece).
5. O parâmetro `?suggest=<código>` do handoff (`Site Nav.dc.html:108`) é só de teste do protótipo: o site **não** o implementa.

Sem JS: não aparece (e o seletor continua lá). Falhas de `localStorage`/`sessionStorage`
(modo privado, bloqueio): `try/catch` e a faixa se comporta como sem preferência salva; fechar sem
`sessionStorage` só some até recarregar.

**Gravação (sem rastreador, sem rede):** `localStorage.ghf_lang = <código>` somente no **clique**
no botão da faixa ou em um link do seletor. Fechar com ✕ grava só `sessionStorage`
(`ghf_faixa_idioma = "off"`). Clique no botão **não** usa `location.href=`/`replace`: o botão é um
`<a href=<URL da língua>>` e a navegação é a do navegador; o script só grava antes (`click` listener
sem `preventDefault`). Assim `grep location.href` fica vazio e o link funciona com clique do meio e
copiar endereço. (O handoff usa `<button>`, `:16`, porque o protótipo não navega; o site navega, logo
é link: divergência intencional.)

**Posição e layout (sem referência no handoff para fixed; proposta):**
- `position: fixed`, **embaixo**, nunca no topo: o nav é `fixed top-0 z-50` com altura variável
  (logo `h-16 lg:h-20` + `py-5`, ~104-120 px) e a hero ocupa `min-h-screen` logo embaixo. Uma faixa
  no topo cobriria o menu ou a hero; no rodapé não cobre o nav nem o CTA da Play no hero.
- < md: `inset-x-3 bottom-3`; >= md: `bottom-4 left-4`, `max-w-[560px]` (canto, nada no centro da
  hero). Sem `inset-x-0` de ponta a ponta: não vira "barra de cookies".
- `bottom` soma `env(safe-area-inset-bottom)`. Sem `100vh`/`100dvh` no cálculo: não empurra
  nem redimensiona nada. **Nunca altera o fluxo:** nada de `padding-top` no `body`, nada de
  `position: sticky`, CLS 0.
- z-index **30**: abaixo do overlay do menu mobile (`z-40`) e do nav (`z-50`). Com o menu aberto
  a faixa fica por baixo e, como o overlay cobre a tela, não é alcançável (e o foco da faixa sai
  da ordem se o overlay tiver trap; hoje não tem, ver `NAV-FOCO-VISIVEL-01`).
- Cobre conteúdo enquanto estiver aberta: aceito porque se fecha com um toque e não volta na
  sessão. **Não pode cobrir o botão da Play do hero no carregamento** em 360x640 e 1280x720: a
  faixa vem depois do hero no DOM, mas fixed sobrepõe. Em 360x640 o CTA do hero fica acima de
  ~y=480, a faixa (110 px) ocupa ~y=520-628: conferir no navegador. Se cobrir, a saída é reduzir a faixa em < md a uma linha de texto curto (nunca subir para o topo). Decisão visual a confirmar pelo usuário.
- Estrutura: `<div role="region" aria-label="{idioma}" lang="{sug}">` (o handoff faz o mesmo, `:11`)
  contendo `<p>` com `band`, `<a>` com `bandGo` e `<button type="button" aria-label="{fechar}">`
  com ✕. Não é `role=alert`/`aria-live`: não interrompe leitor de tela; ele chega nela na ordem do DOM.
  Colocar o componente **no fim do `<body>`** (depois do footer), não no topo, para não ser o
  primeiro foco de Tab.
- Cores (tokens atuais): fundo `bg-brand-surface` (#111827), borda `border border-gray-600`,
  sombra `shadow-xl`, `rounded-xl`; texto `text-gray-200` 14/20 px (contraste ~12:1, AA); o link
  `bandGo` é botão contornado, `border-gray-500 text-white` 600, `min-h-11`, `px-4`, `rounded-full`,
  hover `bg-white/10`. **Não** usa `bg-brand-primary` sólido: a faixa não pode competir com o CTA da
  página (um primário acima da dobra). ✕: 44x44, `text-gray-300`, hover `text-white bg-white/10`.
  Cores independentes do tema da página (lottoexpert violeta, topowalk terracota), a faixa fica
  neutra de propósito.
- Foco: mesmo `focus-visible:outline-2 outline-offset-2 outline-white` do seletor.
- Teclado: `Esc` com foco dentro da faixa fecha. Fechar não move o foco para lugar nenhum se o foco
  estava fora; se estava dentro, devolve ao `<body>`/próximo ponto de Tab natural (o link anterior
  no DOM), sem foco perdido.
- Movimento: entrada com `opacity` + `translateY(8px)` em 200 ms. `@media (prefers-reduced-motion:
  reduce)`: sem transição, aparece direto. Só `opacity`/`transform` (sem CLS).
- Inserção: o script clona o bloco do `<template>` num `DOMContentLoaded`/`load`. Como o
  Lighthouse do CI roda em `en-US` e vê a faixa nas páginas pt, ela não pode virar o elemento LCP
  nem gerar CLS: `fixed` + `opacity` inicial 0 e inserção depois do `load`. Verificar o LCP das
  páginas pt medidas (D22).
- 360 px: texto em até 3 linhas, depois linha com `bandGo` + ✕ (`flex-wrap`, texto `flex: 1 1 220px`,
  igual ao handoff `:13`). Sem largura fixa em nenhum texto. 1280 px: uma linha, texto + `bandGo` + ✕.
- Idiomas longos (de/ru): `bandGo` "Auf Deutsch ansehen" / "Открыть на русском" quebra a linha em 360;
  `flex-wrap` e `whitespace-normal` resolvem. Não usar `truncate`.

### 3. Acessibilidade (checklist para o `site-dev` e a auditoria)

- Contraste AA: texto 4,5:1 (gray-200 em #111827 ~12:1; gray-400 do rótulo "Idioma" em #111827 ~7:1);
  bordas de controle `gray-500`/`gray-600` >= 3:1 contra o fundo do componente.
- Alvo de toque >= 44 px em tudo (links da lista, gatilho, ✕, `bandGo`).
- Um `h1` por página não muda; o seletor e a faixa **não** têm heading.
- `lang` nos nomes de língua e na faixa (WCAG 3.1.2); `aria-current="true"` na língua atual.
- Sem armadilha de foco; `Esc` fecha painel e faixa.
- `prefers-reduced-motion` respeitado na faixa; o seletor não anima.
- `alt`: o ícone do globo é decorativo (`aria-hidden`), o texto visível nomeia o controle.

### 4. Estados

| Estado | Seletor | Faixa |
|---|---|---|
| 1 língua | não renderiza | não renderiza |
| 2 línguas | link de hoje | pode aparecer |
| 3+ línguas | disclosure (barra) / grade (menu) | pode aparecer |
| JS desligado | `<details>` funciona; lista visível no menu mobile | não aparece |
| Idioma incompleto (`pendente`) | a língua **não** aparece em `PAGINAS` até estar completa (regra do WP); sem estado "em tradução" no seletor | n/a |
| Storage bloqueado | n/a | `try/catch`, comportamento sem preferência |

### 5. Componentes e referência

- Reaproveita: `Nav.astro` (lugar do `TrocaIdioma`, classes `trocaDesktop`/`trocaCelular` por
  `realce`), `Icon.astro` (`globe`), overlay `#mobile-menu`.
- **Componente novo: nenhum fora dos dois pedidos.** O painel de idioma (lista) e a faixa são
  novos, mas existem no handoff (`Site Nav.dc.html:10-21`, `:53-65`, `:88-99`), então não voltam ao
  Claude Design; as divergências da seção 0 sim, se o usuário quiser reabrir.
- **Sem referência no handoff:** faixa `position: fixed` e embaixo; seletor com 3 línguas em lista;
  breakpoint do menu em 768; marca visual de link que muda de língua (D23); foco em branco em vez
  de `--br`. O usuário decide se quer levar algum ao Claude Design; o site-dev implementa a
  proposta acima enquanto isso.

### 6. Para o `site-dev` (não decide, só implementa)

- Commit 4: n = 2 gera o **mesmo** HTML; `diff -r` vazio. A parte `n >= 3` não aparece em nenhuma
  página publicada (mapa só pt/en): prove com uma página de teste local mapeada com 3+ línguas (não
  publicada) e capturas a 360 e 1280 para o usuário. O §9 passa a ler `data-troca-idioma` em qualquer
  língua.
- Commit 6: `diff` só com `<template>`, script e CSS. Chaves novas em `ui.ts` (pt/en).
  `grep -rnE "location\.(replace|assign)|location\.href *=" src/` vazio.
- Auditoria (`site-ux` AUDITAR depois do commit): cobertura da faixa sobre o CTA da Play a 360x640 e
  1280x720, foco, `Esc`, `prefers-reduced-motion`, overlay do menu por cima da faixa, 7 línguas a 360.

### 7. Achados novos a registrar (destino sugerido)

- `NAV-FOCO-VISIVEL-01`: `Nav.astro:129` usa `focus:outline-none` no botão do menu e não há estilo de
  foco global (`global.css`). WCAG 2.4.7. Destino: WP de acessibilidade/QA (não WP-15).
- `SELETOR-2-LINGUAS-FORA-DO-HANDOFF-01`: seletor pt/en é link único com globo; handoff desenha
  grupo segmentado com `aria-pressed`. Destino: decisão do usuário/Claude Design.
- `LINK-FALLBACK-IDIOMA-SEM-SINAL-01`: D23 (A) leva a página em outra língua sem sinal visual.
  Destino: decisão do usuário, só se virar problema real (nasce com WP-16).

**Usuário (2026-10-16):** aceitou as três propostas sem referência no handoff:
- faixa de sugestão fixa embaixo, inserida depois do `load`;
- link único com 2 línguas e lista de nomes nativos a partir de 3;
- link de fallback da D23 sem sinal visual, só com `hreflang` e `lang`.

## Correções da auditoria (2026-10-16)

Um commit, `WP-15: correções da auditoria (…)`, só nos Arquivos-alvo do veredito.

- **§16 sem redirecionamento:** a expressão foi para `regras_i18n.RE_REDIRECT`/`redirecionamentos()`
  com fronteira de palavra (`\blocation…`). Ela cobre `location.replace/assign(`,
  `location[.href|.pathname|.search|.hash] =`, `location[`, `navigation.navigate(` e
  `<meta http-equiv="refresh">`. Cada forma tem um caso no `test_redirecionamento`, com os
  inocentes que devem passar (`geolocation=`, `==`/`===`, leitura de `location.pathname`).
  A regra antiga dava falso positivo em `allow="geolocation=self"` e deixava passar
  `location.pathname=` e `navigation.navigate(`. Mutação em `dist/index.html`:
  - com a regra antiga: `geolocation` vermelho, `pathname`/`navigate` verdes;
  - com a nova: `geolocation` verde, `pathname`/`navigate` vermelhos.
- **§9, link `data-troca-idioma="X"`:** deixou de ser isento. Agora tem de levar à mesma página na
  língua X (`destino == arquivo(X, origem)`), X tem de ser uma língua da página no mapa, e
  `hreflang`/`lang`, quando o link os tem, são os de X.
  - O link da faixa não tem nenhum dos dois: a língua vem do `<section lang>`/`<template lang>`.
    Por isso a ausência passa, e só a incoerência reprova.
  - Casos novos no `test_link_d23`.
  - Mutação: faixa apontando para `/en/topowalk.html` e seletor com `hreflang="pt-BR"`. As duas
    passavam com a regra antiga e reprovam com a nova.
- **§10:** `ui.ts` sem nenhum bloco lido é erro, porque a regra ficaria calada se o formato mudasse.
  Teste: `test_ui_sem_blocos_e_erro`.
- **§4, linha de data:** virou `regras_i18n.regra_linha_data()`, usada pelo `check_site.py` e pelo
  teste. Teste: `test_linha_de_data`.
- **CI:** `python3 -B -m unittest`.
- **`SugestaoIdioma`:**
  - **Foco ao fechar:** com ✕ ou Esc e o foco dentro da faixa, o foco vai ao último elemento
    focável e visível antes da faixa no DOM. Na prática é o último link do rodapé, porque a faixa é
    o fim do `<body>`. Com o foco fora da faixa, ele não se move.
  - **Abaixo de md, uma linha só (~62 px):**
    - o texto corta com reticências (`truncate`), e o texto inteiro fica no DOM;
    - o botão e o ✕ são `shrink-0`, e o botão tem `whitespace-nowrap`, por isso nunca são cortados;
    - os alvos continuam com 44 px.
    - De md para cima o desenho é o de antes, com `flex-wrap`.
- **`SeletorIdioma`:**
  - **Língua atual da lista da barra:** passou a `text-white`, com `brand-primary` só no check, como
    no ramo do menu.
  - **`focusout` sem `relatedTarget`:** não fecha o painel se o último `pointerdown` foi dentro dele.
    No Safari, o clique num link não o foca. Uma tecla zera a marca, e o clique fora continua
    fechando.

**Item 10, o Lighthouse en-US vê a faixa nas páginas pt?** Sim.
- Na rodada sobre `/` com `LANG=en_US.UTF-8`:
  - `configSettings.locale` é `en-US`, e o Chrome lançado herda o `LANG`: `navigator.languages`
    dá `["en-US"]`, conferido com `--dump-dom`.
  - `fullPageScreenshot.nodes` tem `page-24-SECTION` com `top` 6656 e altura 70, no fim da página.
  - A captura de página inteira mostra a faixa "This page is also available in English. / Switch
    to English".
- Ela **não** aparece no `final-screenshot`, que é tirado a ~2,4 s, antes de `load` mais dois
  quadros mais 200 ms de transição. Nenhuma auditoria lista o nó.
- CLS 0 e LCP 2,33 s: a faixa não é o LCP.
- `LANG=en_US.UTF-8 python3 tools/lighthouse.py --runs 1`: ✅ orçamento cumprido.
- As legais ficam em a11y 90 por `color-contrast`/`link-in-text-block` dos links do corpo e pelo
  `heading-order` do h4 do rodapé. São herdados e estão em `LOTTO-CONTRASTE-AA-01` e
  `FOOTER-H4-ORDEM-01` (WP-10), não na faixa.

**Aceito sem mudança:**
- **Um `<template>` por língua na faixa:** o HTML cresce linearmente com as línguas da página.
  Reavaliar no WP-16, com a terceira língua.
- **Script inline da faixa e do seletor:** não é cacheável entre páginas. Aceito pelo tamanho.
- **Landmark `aria-label="Idioma"`/`"Language"` na faixa:** igual ao handoff. Aceito.

**Só o navegador prova (usuário):**
- `/`, pt, a 360x568 e 360x640, com o navegador em en: a faixa numa linha, sem cobrir o botão da
  Play do hero, o botão "Switch to English" inteiro e o texto com reticências.
- A 1280x720: o desenho anterior.
- Tab até o ✕ e Enter, e depois Tab até "Switch to English" e Esc: o foco fica no último link do
  rodapé.
- Seletor com 3 línguas, só em página de teste local: no Safari, clicar numa língua da lista
  navega, sem fechar o painel antes.

**CI (2026-10-16):** `b0ee3df` entrou na `feat/wp-08-layout-unico` por fast-forward. O run 38920589727
do #37 deu verde em `plano`, `site` (`check_site` consistente, unittest com 8 testes OK, lychee) e
`lighthouse` (orçamento cumprido). Falta o checklist de navegador do usuário.
