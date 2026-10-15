---
id: WP-08
titulo: As 10 páginas usam um layout, componentes únicos e rota por idioma
area: landing
status: doing
depende_de: [WP-07]
adr: [ADR-001, ADR-002, ADR-003]
spec: docs/AVALIACAO.md
decisoes: [D2, D8, D9]
tamanho: L
risco: alto
visual: true
branch: feat/wp-08-layout-unico
---

# WP-08 — As 10 páginas usam um layout, componentes únicos e rota por idioma

**Depende de:** WP-07 · **Achados roteados:** `NAV-FOOTER-DERIVA-01`, `I18N-SEM-URL-01`,
`LEGAL-META-SEM-I18N-01`, `LEGAL-CORPO-SO-EM-JS-01`, `TARGET-BLANK-SEM-NOOPENER-01`,
`POLEPOSITION-NOOPENER-01`, `FEATURES-ARIA-HIDDEN-01`, `HTMLVALIDATE-*-01` (6),
`404-SEM-OG-CANONICAL-01`, `CONFIG-YML-ORFAO-01`

**Exceção de dependência (2026-10-13, usuário):** o WP-08 começa com o WP-07 `blocked` (só falta
o deploy, adiado para uma janela de pouco uso do bolão). A branch fica isolada: **sem merge em
`develop` até o WP-07 estar no ar**, para o `/release` publicar a troca de stack e a migração das
páginas separadas, cada uma com o seu rollback. **Superada por D13 (2026-10-14):** a integração
só vai para `develop` com o backlog de evolução inteiro (WP-08 a WP-19), num único deploy.

**Objetivo:** nav, footer, tema e `<head>` existem uma vez (`src/layouts/`, `src/components/`);
o conteúdo legal é um `.md` por idioma em `src/content/legal/` renderizado por um layout; o
inglês vive em `/en/...` com `hreflang`; o Tailwind é compilado no build (ADR-003). Sem mudança
visual intencional — o redesign é WP-10.

**Contexto:** `docs/AVALIACAO.md` §2 itens 5 e 6; hashes de nav/footer diferentes em todas as
landings; 7 `tailwind.config` diferentes nas 10 páginas, com `brand.primary` próprio por página
(ADR-003 §Contexto); dicionário i18n de até 126 chaves por página; texto legal em 3 cópias
(`docs/*.md`, HTML pt, dicionário JS en).

**Ler antes:** `docs/AVALIACAO.md` §3.2; ADR-001; ADR-002; ADR-003; D8 (c1); WP-07 passo 7
(rollback do modo branch).

**Arquivos-alvo:** `src/**`, `public/**`, `astro.config.mjs`, `tailwind.config.mjs`,
`postcss.config.mjs`, `package.json`, `package-lock.json`, `tools/check_site.py`,
`tools/contrato.sha256` e o passo que o confere em `pr.yml`/`deploy.yml` (D13),
`.htmlvalidate.json`, `.github/workflows/pr.yml` (só o passo do `check_site.py` na raiz — nomes
`plano` e `site` intactos, D9), `.claude/commands/verify.md`, `_config.yml` (remoção, fatia 9),
os 10 `*.html` da raiz (remoção), `docs/*_PRIVACY_POLICY.md` e `docs/*_TERMS_OF_SERVICE.md`
(`git mv` para `src/content/legal/`), `.well-known/`, `lotto-expert/`, `assets/`, `CNAME`
(`git mv` para `public/`, fatia 9), `CLAUDE.md` seções "Arquitetura", "Comandos" e "Referência
rápida", `README.md`.

**Respostas do usuário (2026-10-13), todas como recomendado:** (1) a R1 só sai depois do WP-07
no ar com um convite real testado e alguns dias sem incidente, e com a tag `pre-wp-08` em `master`
antes; (2) publicação em três releases (R1/R2/R3) — **(1) e (2) superadas por D13**; (3) sem redirect para `/en/` até o WP-15 —
quem escolheu inglês volta a abrir a URL pt em português; (4) push da integração e PR rascunho
para `develop` com o título de não fazer merge, só para o CI rodar.

## Como a branch é fatiada (site-arquiteto, 2026-10-13)

**Uma branch de integração, fatias como sub-branches.** `feat/wp-08-layout-unico` é a
integração. Cada fatia nasce dela (`feat/wp-08-fN-<slug>`), passa no `/verify` e volta por
`git merge --no-ff` com a mensagem `WP-08: fatia N — …` — cada fatia é um commit de merge
revertível (`git revert -m 1`). Sem branches empilhadas: o `pr.yml` só roda em PR contra
`develop`/`master`, e PR entre fatias não teria CI.

**CI desde a fatia 1:** abrir **agora** um PR rascunho `feat/wp-08-layout-unico → develop`,
título começando por `[NÃO FAZER MERGE — aguarda WP-07 no ar]`. Cada push roda `plano` e `site`
sem mexer em workflow. O `develop` que andar (WP-07 ajustado no deploy, WP-19) entra na integração
por `git merge origin/develop`, nunca rebase (preserva os merges de fatia).

**Publicação: um único deploy, com o backlog de evolução inteiro (D13, 2026-10-14).** As releases
R1/R2/R3 deixaram de existir. O WP-08 termina na integração (status `done` com as 9 fatias
integradas e auditadas); os WP-09 a WP-19 nascem da integração e voltam a ela; o merge em
`develop` e o `/release` acontecem uma vez, no fim. Antes desse deploy: tag `pre-modernizacao` em
`master` (adicionada à política do ambiente `github-pages`, que hoje só aceita `master`), ensaio
do rollback (`gh workflow run deploy.yml --ref pre-modernizacao`) e checklist completo de navegador
sobre `dist/` local. O deploy é numa janela de pouco uso do bolão, com teste de link real gerado
pelo app logo depois. Enquanto a integração não sobe, texto legal novo e incidente seguem por
hotfix a partir de `master`, e voltam para cá por `git merge origin/develop`.

O deploy único apaga páginas da raiz: a partir dele, voltar o Pages ao modo "branch" (rollback do
WP-07) deixa de servir essas páginas; o rollback é o `workflow_dispatch` sobre a tag.

### Fatias

1. **Infra + home.** ADR-003 aplicado: `tailwindcss` 3.4.19, `postcss`, `autoprefixer` exatos;
   `tailwind.config.mjs` (união das 7 configs, `brand.*` por variável), `postcss.config.mjs`,
   `src/styles/global.css` (temas e o CSS de `<style>` de `index.html`). `Base.astro`: props
   `title`, `description`, `og`, `lang` (`pt`|`en`), `caminho`, `tema`; `<head>` único com
   `og:*`, `canonical`, `hreflang` pt-BR/en recíprocos, e Google Fonts + Font Awesome **uma vez**
   (saem no WP-12). `Nav.astro`, `Footer.astro` (referência: `index.html`; itens por página são
   prop, não markup; diferença intencional entre páginas → achado), `TrocaIdioma.astro` (link para
   o par `/x.html` ↔ `/en/x.html`, `type`/`aria-label` corretos; ao clicar grava `ghf_lang`, para
   as páginas ainda copiadas abrirem no idioma escolhido). Textos de nav/footer em
   `src/i18n/ui.ts` (pt e en). `404.astro` no `Base` (fecha `404-SEM-OG-CANONICAL-01`).
   `check_site.py` (ver abaixo). `src/pages/index.astro` + `src/pages/en/index.astro`; `index.html`
   sai da raiz e de `COPIADOS_DA_RAIZ`.
2. `lottoexpert.html` (passa por `PAGINAS_LOTTO` em pt e en; fecha `FEATURES-ARIA-HIDDEN-01`).
3. `topowalk.html` (escala `terracota` do config dela entra no config único).
4. `poleposition.html` (JetBrains Mono entra no `<head>` só desta página, por prop).
5. `eclipsego.html`.
6. **Legal — piloto `eclipsego-privacy`** (a menor, 32 KB, menos tráfego). Content collection
   `src/content/legal/<app>-<doc>.<idioma>.md`; pt = `git mv` de `docs/<APP>_….md` com
   front-matter `lastUpdated` **acima** do corpo, corpo byte a byte o `.md` do app; en = texto do
   dicionário JS atual convertido para markdown, **sem retradução**. `LegalLayout.astro` reproduz
   o card e a tipografia atuais — sumário e largura de leitura são WP-10. `site-legal` participa.
   `pr.yml` e `/verify` deixam de rodar `check_site.py` na raiz (contratual sai dela).
7. `topowalk-privacy` e `poleposition-privacy` (fecha `POLEPOSITION-NOOPENER-01`).
8. `lottoexpert-privacy` e `lottoexpert-terms` (fecha `LEGAL-META-SEM-I18N-01`,
   `LEGAL-CORPO-SO-EM-JS-01`).
9. **`public/` e limpeza.** `git mv` de `lotto-expert/`, `.well-known/`, `assets/`, `CNAME` para
   `public/`; `copiaRaiz` sai do `astro.config.mjs`; `_config.yml` removido
   (`CONFIG-YML-ORFAO-01`); as 6 regras do `.htmlvalidate.json` voltam a `error`;
   `TARGET-BLANK-SEM-NOOPENER-01` conferido em todo `dist/`; `CLAUDE.md` e `README.md`.

### Andamento

- **Fatia 1** (2026-10-14): implementada (337c58f + 7dc7834), auditada (`site-qa`, `site-seo-perf`, `site-ux` — nenhum achado alto no escopo; a regra do §4 do `check_site.py` que tinha afrouxado foi corrigida). Integrada pelo usuário com merge `--no-ff` (24f8bee); CI do PR #37 verde. Checklist de navegador de `/`, `/en/` e `/404.html` reportado ok pelo usuário em 2026-10-14, servindo `dist/` local. Achados das auditorias em `achados-novos.md`.
- **Fatia 2** (2026-10-14): implementada (f99c1ac), auditada (`site-qa`, `site-seo-perf`, `site-ux` — nenhum achado alto no escopo; dois achados médios/baixos do `site-qa` no escopo corrigidos em 45d3aa9: regra §10 do `check_site.py` de paridade pt/en dos dicionários em `src/i18n/*.ts` e `aria-hidden` em 3 ícones decorativos). Lighthouse mobile antes→depois: Performance 63→64, Accessibility 85→96, BP 100, SEO 100, LCP 18,6→17,8 s, FCP 4,9→3,9 s, HTML 83 KB→45 KB. Fechou `FEATURES-ARIA-HIDDEN-01` e `HOME-EN-SEM-LANG-01` (o script grava `ghf_lang` com o idioma da página, pt também — consistente com D8 c1). **Aguarda:** integração pelo usuário (`git merge --no-ff feat/wp-08-f2-landing-lottoexpert` na integração) e checklist de navegador do usuário. Status do WP continua `doing`.
- **Fatia 3** (2026-10-14): implementada (04be113), auditada (`site-qa`, `site-seo-perf`, `site-ux` — nenhum achado alto; um médio no escopo, o blob do hero, corrigido em 8111fe3: o atributo `style="animation: float 8s…"` saiu, porque a página antiga não declarava `@keyframes float` e não animava, enquanto no CSS único a keyframes da home existe e o transform tirava o blob do centro). `Nav` ganhou a prop `realce` (`primary`|`accent`) e `Footer` ganhou `realce`, `fundo` (`base`|`surface`) e `redes` opcional. Home e lottoexpert pt idênticas no `dist/` (fora o hash do CSS); en só com links en→en para o TopoWalk. Lighthouse mobile antes→depois (pt): Performance 68→74, Accessibility 76→96, BP 100, SEO 100, LCP 5,3→4,6 s, FCP 4,7→3,9 s, CLS 0→0,045, HTML 47 KB→25 KB. Nenhum achado roteado ao WP-08 fechado nesta fatia. **Aguarda:** integração pelo usuário (`git merge --no-ff feat/wp-08-f3-landing-topowalk` na integração) e checklist de navegador. Status do WP continua `doing`.

### `check_site.py` (fatia 1, antes da primeira página sair da raiz)

- §7 deixa de derivar a lista do glob da raiz (que encolhe a cada fatia e deixaria página sumir
  calada): lista **fixa** `PUBLICADAS` com as 10 páginas pt e o convite; e `EN_PENDENTE`, as
  páginas ainda sem `/en/` — encolhe a cada fatia e termina vazia.
- `hreflang`: toda página com par en declara os dois, recíprocos, e o par existe em `dist/`.
- §4: `LEGAL` ganha os pares `en/<pagina>`; a data é procurada **depois de tirar as tags** (o
  markdown renderiza `<strong>Última atualização:</strong> 13 de …`, que a regex de hoje não
  casa — passaria só com aviso); página legal sem data pt (ou en, em `en/`) é **erro**; a fonte
  passa a ser o `lastUpdated` do front-matter, conferido contra a linha do corpo.
- §5: `PAGINAS_LOTTO` ganha `en/index.html`, `en/lottoexpert*.html`.
- Página em `en/` com link interno para página que tem par en aponta para o par.

### Prova byte a byte (desde 2026-10-14, D13)

`tools/contrato.sha256` guarda o `sha256sum` de `lotto-expert/sweepstake-invite/lottoexpert-invite.html`,
`.well-known/assetlinks.json`, `assets/lottoexpert_app_mockup.png` (`og:image` do convite) e
`CNAME`, tirados de `origin/master` em 2026-10-14. O `pr.yml`, o `deploy.yml` e o `/verify` rodam
`cd dist && sha256sum --quiet -c ../tools/contrato.sha256` — o deploy falha se divergir. O convite
não é migrado nem reformatado (lê `?d=`; formato é do app, invariante sem teste automático). Mudar
um desses arquivos é decisão do usuário: atualiza o `.sha256` no mesmo PR e testa com link real.

## Passos (por página)

1. componentes do layout; conteúdo pt e en separados (`src/pages/x.astro`, `src/pages/en/x.astro`);
   caminho de asset **absoluto** (`/assets/…`; relativo quebra em `/en/` — §3 do check acusa);
2. a página da raiz sai do repositório e de `COPIADOS_DA_RAIZ` no mesmo commit;
3. `/verify`; `site-ux` AUDITAR compara antes/depois em 360/1280, pt e en (o "antes" en é a
   página atual com `ghf_lang=en`).

## Critérios de aceite

- `python3 tools/check_site.py --raiz dist` verde com `EN_PENDENTE` vazio; `dist/en/` com as
  mesmas 10 páginas de `dist/`.
- `grep -rl "tailwind.config = " src/ | wc -l` = 0; `grep -rlc "cdn.tailwindcss" dist | wc -l` = 0.
  Google Fonts e Font Awesome: uma ocorrência, no layout (`grep -rl "font-awesome" src | wc -l` = 1)
  — saem no WP-12.
- `grep -c "<nav" src/components/Nav.astro` = 1 e nenhuma outra `<nav` em `src/pages/`.
- Para cada página legal: um só `.md` por idioma, `lastUpdated` no front-matter igual à do
  repositório do app (`check_site.py`); texto en renderizado igual ao en publicado hoje
  (texto normalizado, sem tags — diff vazio, saída no relato da fatia).
- Convite, `assetlinks.json`, `assets/lottoexpert_app_mockup.png` e `CNAME`: `sha256sum -c
  tools/contrato.sha256` verde sobre `dist/` (CI e deploy).
- `npx html-validate 'dist/**/*.html'` sem nenhum aviso das 6 regras rebaixadas no WP-05.
- Capturas antes/depois (360 e 1280) por página, pt e en, sem diferença visual não intencional —
  relato do `site-ux`.

**Só no navegador:** cada página pt e en; a troca de idioma leva ao par da mesma página; quem
tinha `ghf_lang=en` abre a URL pt em português (D8 c1: sem redirect; a faixa de sugestão é WP-15);
convite com link real gerado pelo app, logo depois do deploy único (D13).

**Irreversível:** páginas `.html` da raiz removidas do repositório (ficam no git); rollback por
troca de modo do Pages deixa de existir a partir do deploy único (D13). URLs não mudam.

**Risco:** alto por volume e pelas URLs; médio por página.
