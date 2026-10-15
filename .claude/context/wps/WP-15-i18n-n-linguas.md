---
id: WP-15
titulo: Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas
area: infra
status: todo
depende_de: [WP-08, WP-09, WP-11]
adr: [ADR-001]
spec: docs/AVALIACAO.md
decisoes: [D2, D8]
tamanho: M
risco: alto
visual: true
branch: feat/wp-15-i18n-n-linguas
---

# WP-15 — Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas

**Depende de:** WP-08 (rota `/en/`), WP-09 (front-matter legal e `sync_legal.py`), WP-11
(`Seo.astro` com `hreflang` pt/en) · **Achados roteados:** —

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
