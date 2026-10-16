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
