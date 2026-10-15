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
- **Fatia 4** (2026-10-14): implementada (b6e4f5c), auditada (`site-qa`, `site-seo-perf`, `site-ux` — nenhum achado alto nem médio; nada a corrigir no escopo). `Base.astro` ganhou a prop `fontesExtras` (JetBrains Mono na mesma requisição da Inter, só nas duas páginas do Pole Position); `Nav` ganhou `realce="primary-claro"`; `Footer` ganhou `fundo="surface-sem-borda"` e `redes` com tiktok/facebook. `animate-fade-in-up` saiu do hero (a página antiga não declarava a keyframes; nada animava, nada anima). Home, lottoexpert, topowalk e 404 idênticas no `dist/` (fora o hash do CSS); en só com links en→en para o Pole Position. Texto visível idêntico em pt e en. Teste de mutação do `site-qa`: §9, §10, hreflang e og:image acusam. Lighthouse mobile antes→depois (pt): Performance 63→64, Accessibility 82→94, BP 100, SEO 100, LCP 9,6→9,2 s, CLS 0, HTML 66 KB→37 KB. Nenhum achado roteado ao WP-08 fechado nesta fatia. **Aguarda:** integração pelo usuário (`git merge --no-ff feat/wp-08-f4-landing-poleposition` na integração) e checklist de navegador. Status do WP continua `doing`.
- **Fatia 5** (2026-10-15): implementada (0fd8700), auditada (`site-qa`, `site-seo-perf`, `site-ux` — nenhum achado alto nem médio no escopo; nada a corrigir). `Nav` ganhou `realce="primary-texto-preto"`; `[data-tema='eclipsego'] .text-gradient` e `@keyframes corona-pulse`/`.corona-glow` foram para o CSS único (animava antes, anima agora); o blob do hero ficou sem `style="animation: float…"` (a antiga não declarava `float`; parado e centrado, como antes). Home, lottoexpert, topowalk, poleposition e 404 idênticas no `dist/` (fora o hash do CSS); en só com links en→en para o EclipseGo. Texto visível idêntico, exceto "Portfólio" → "Portfólio de Apps" no rodapé (`TOPO-FOOTER-PORTFOLIO-01`). Teste de mutação do `site-qa`: §10, `EN_PENDENTE` e link relativo em `en/` acusam. Lighthouse mobile antes→depois (pt): Performance 68→89, Accessibility 74→94, BP 100, SEO 100, LCP 5,5→3,2 s, FCP 4,6→2,6 s, CLS 0,033, HTML 39 KB→22 KB. **Com esta fatia as 5 landings estão no layout único** (fatias 1–5 = o grupo das landings); `EN_PENDENTE` fica só com as 5 legais. **Aguarda:** integração pelo usuário e checklist de navegador. Status do WP continua `doing`.
- **Fatia 6** (2026-10-15): implementada (3f26665 texto legal por `site-legal`, fb5fa66 layout/páginas/check/CI por `site-dev`, 372b097 correções da auditoria); piloto legal `eclipsego-privacy`. Content collection `src/content/legal/` (`eclipsego-privacy.pt.md` = `git mv` de `docs/ECLIPSE_GO_PRIVACY_POLICY.md` + front-matter `lastUpdated: "2026-07-13"`, corpo byte a byte o app, eclipse-go 7f349a2; `eclipsego-privacy.en.md`), `LegalLayout.astro`, plugins `src/markdown/legal.mjs`, páginas literais pt/en, `src/content.config.ts` (schema com `lastUpdated` string `AAAA-MM[-DD]`), `src/i18n/legal.ts` (`dataLegal()` sem `Date`), dependência `@astrojs/markdown-satteri` 0.4.3 (exata; `smartPunctuation: false`, porque `markdown.smartypants` está obsoleto no Astro 7.3.8), ids de título com prefixo `secao-` (html-validate `valid-id`), Nav/Footer com props `brilhoLogo` e `politicaAtual`. **Decisão do usuário (2026-10-15), opção (A):** o site segue o `.md` do app (D7). Diferenças de texto visível em relação ao publicado, aprovadas: intro sem "Ao utilizar o EclipseGo, você concorda com os termos descritos neste documento." e com `("o aplicativo", "nós")`/"dos usuários"; "dada" -> "dado"; tabela de 2 linhas -> 1 ("Localização (fina/aproximada)"); en com as mesmas correções. **Exceção registrada ao critério de aceite** "texto en renderizado igual ao en publicado hoje": para o EclipseGo o diff é exatamente essas correções. Antes, por autorização do usuário, o e-mail de contato do app foi trocado para `support@ghfsoftware.com` (eclipse-go 7f349a2 e 4668019, branch `docs/email-suporte-politica`, sem merge na main do app). **Check da raiz saiu do CI e do `/verify`:** uma URL contratual só existe em `dist/`; prova antes (data alterada em `topowalk-privacy.html` da raiz falha no `--raiz dist`) e 9 mutações do `site-qa` (datas, copy, assetlinks, contratual, link, og:image). Sem argumento, o check usa `dist/` e falha se `dist/` não existe ou está mais antigo que as fontes (§11, 372b097). §12: legal migrada em `dist/` com 1 h1, 1 data, sem aspas tipográficas que o `.md` não tenha, e pt/en com mesma contagem de `##`/`###`/linhas de tabela; mutações obrigatórias do veredito (4) e do `site-qa` (3) acusam. Auditoria: `site-qa` (2 médios no escopo, rede de verificação, corrigidos em 372b097; o commit intermediário 3f26665 isolado fica vermelho no `check_site.py`: aceito, o merge `--no-ff` leva a fatia inteira), `site-seo-perf` e `site-ux` sem alto/médio. Lighthouse mobile pt antes->depois: Performance 77->92, Accessibility 75->94, BP 100, SEO 100, LCP 4,1->2,7 s, HTML 33 KB->16 KB, corpo agora no HTML estático (antes montado por JS). Home, landings e 404 iguais fora o hash do CSS; en com links para `/en/eclipsego-privacy.html`. Fecha para `eclipsego-privacy`: `LEGAL-CORPO-SO-EM-JS-01`, `LEGAL-META-SEM-I18N-01` e as tags de `LEGAL-SEM-OG-01` (os três seguem para as outras 4 legais). **Aguarda:** integração pelo usuário e checklist de navegador. Status continua `doing`.
- **Fatia 7 — veredito** (`site-arquiteto`, 2026-10-15): **aprovado, com 4 decisões do usuário antes dos commits de texto legal** (abaixo). Branch `feat/wp-08-f7-legal-topowalk-poleposition` em 9fbf360; `topowalk-privacy.html` e `poleposition-privacy.html` da raiz iguais a `origin/master` (`git diff --stat origin/master` vazio); `docs/*.md` iguais ao app (`diff -q` vazio). Linha de base: `npm run build && python3 tools/check_site.py --raiz dist` verde (18 páginas, 432 links). URLs contratuais seguem como páginas literais (`src/pages/topowalk-privacy.astro`, `src/pages/poleposition-privacy.astro`), sem redirect; §1 prova.
  - **Diferenças em relação à fatia 6.** (a) Tamanho: TW 388 linhas, 13 `##`, 31 `###`, 2 tabelas, 2 `ol`, 1 lista aninhada, 4 links, 18 `code`, 14 `---`, 1 `*itálico*`; PP 238 linhas, 11 `##`, 14 `###`, 2 tabelas, 1 lista aninhada **com parágrafo de continuação dentro do item** (`POLEPOSITION_PRIVACY_POLICY.md:86-92` — a lista externa fica "loose" no CommonMark e todos os itens dela ganham `<p>`), 7 links, 14 `code`, 11 `---`. Sem HTML embutido, sem aspas tipográficas. O EclipseGo não tinha `---`, link, `ol`, lista aninhada nem `code` fora de tabela. (b) `---`: a página publicada só mostra 1 `<hr>` (TW, antes da nota LGPD) e 0 (PP); todo `---` dos dois `.md` precede um `## `, menos o último do TW. Regra: `hr` seguido de `h2` não aparece (plugin hast em `legal.mjs` ou CSS `hr:has(+ h2)`; escolha do `site-ux`), o resto com `border-gray-800 my-8`. (c) Links externos: publicados com `target="_blank"` (PP sem `rel` — `POLEPOSITION-NOOPENER-01`); markdown não tem `target`. Plugin hast em `legal.mjs`: `a[href^=http]` do texto legal ganha `target="_blank" rel="noopener noreferrer"` — mantém o comportamento e fecha o achado. Estilo do link por tema (TW `text-brand-primary underline hover:text-white`; PP `text-brand-primary hover:underline`). (d) Tabelas: a regra de hoje `.legal-corpo td:first-child` (mono + primary, por posição) só vale para o EclipseGo — escopar em `[data-tema='eclipsego-privacy']` e derivar dos dados nas outras: TW primeira coluna `**…**` → `font-semibold text-brand-primary`, `` `…` `` → `font-mono text-sm text-brand-primary`; PP tabelas inteiras em outro estilo (contêiner `my-6 border border-gray-800 rounded-xl`, `th py-4 px-5 text-sm font-semibold`, cabeçalho `bg-gray-800/30`, `tbody divide-y divide-gray-800/50`, 1ª coluna `text-gray-300`, demais `text-gray-400`). (e) `code` fora de tabela: TW sem classe (só a fonte mono do preflight); PP pílula `font-mono bg-gray-800 px-1.5 py-0.5 rounded text-gray-200 text-sm`. (f) Lista aninhada publicada sem marcador (`list-circle` não existe no Tailwind; preflight zera) com `pl-6 mt-1 space-y-1`; `li > p` da lista "loose" sem `mb-4`. (g) TW nota final `*…*` → `p` com `text-sm text-gray-500 italic`; PP `**Desenvolvido por Gustavo Hyppolito**` era `p.font-semibold.text-white.mt-6`. (h) Casca: nav `realce="primary"` com `brilhoLogo` (a classe `drop-shadow-[…rgba(181,84,28,0.5)]` sem espaço valia — diferente do EclipseGo), `classeBody` com `selection:text-white`, favicon `/assets/topo-walk.png` / `/assets/poleposition.png`, sem JetBrains Mono na política do PP, rodapé igual ao da fatia 6 (`fundo="surface"`, `redes={{}}`, `politicaAtual`). Selo: duas variantes novas em `LegalLayout` (TW `border-brand-primary/30 bg-brand-primary/20 text-brand-primary font-semibold`; PP `border-lime-500/20 bg-lime-900/10 text-lime-400 font-medium`). Botão: "Voltar para a GHF Software" / "Back to GHF Software" → home (`rota(lang,'index.html')`), chave nova em `legal.ts`. `title`/`description` en novos em `legal.ts` (casca, não texto legal). Todo CSS novo é bloco por `[data-tema='…-privacy']`; o `dist/` do EclipseGo pt/en fica igual fora o hash do CSS (prova). (i) O en a reproduzir sem retradução é o `content`/`intro`/`page_title`/`last_updated` do dicionário `en` (`topowalk-privacy.html:640-1037`, `poleposition-privacy.html:536-830`): mesma contagem de `h2`/`h3`/`li`/`ul`/`ol`/`tr`/`a`/`code` do pt nas duas páginas; o `.en.md` segue a **estrutura do `.pt.md`** (listas, tabelas, `---`, links, `code`) com as palavras do dicionário. A intro estática do PP (`poleposition-privacy.html:153`, "Ao utilizar o sistema…") é velha — o JS a trocava; some com a migração.
  - **Commits.** As duas páginas na mesma fatia, em commits separados por app (decisão do PP pode atrasar só o PP). 1) `site-legal`: TW — `git mv docs/TOPOWALK_PRIVACY_POLICY.md src/content/legal/topowalk-privacy.pt.md` + front-matter `lastUpdated: "2026-09"`, `topowalk-privacy.en.md`. 2) `site-legal`: PP — idem, `lastUpdated: "2026-10"`. 3) `site-dev`: infra comum — `legal.mjs` (links externos, `hr`), `LegalLayout` (selos, botão), `global.css` (blocos por tema; EclipseGo inalterado), `legal.ts`, `check_site.py`. 4) `site-dev`: TW — páginas pt/en, `topowalk-privacy.html` sai da raiz, de `COPIADOS_DA_RAIZ`, de `EN_PENDENTE`; `LEGAL` aponta para o `.pt.md`; `COM_PAR_EN`. 5) `site-dev`: PP — idem. 6) docs: `.claude/commands/legal.md:14-15` (destino passa a `src/content/legal/`), `README.md:17-20,37-48` (as 3 legais migradas — parte README de `DOCS-ECLIPSE-MOVIDO-01`), `CLAUDE.md:8` ("prova raiz e `dist/`") e linhas `diff` da tabela de comandos, e `CHECK-SEM-BUILD-INSTRUCOES-01` (5 linhas listadas no achado). WP-16 e WP-17 citam `docs/POLEPOSITION_…`/`docs/TOPOWALK_…` como origem — `site-docs` atualiza o caminho nos dois WPs. Commits 1–2 isolados ficam vermelhos (LEGAL aponta para `docs/`): aceito, como na fatia 6.
  - **Prova.** (1) Texto en renderizado contra o en publicado: de `dist/en/<x>.html`, hero (h1 + data) + intro + `.legal-corpo` sem tags, `html.unescape`, espaços colapsados, `**` removidos; do outro lado `page_title`, `last_updated`, `intro`, `content` do dicionário `en` de `git show origin/master:<x>.html`, mesma normalização; diff por palavra **vazio fora das decisões abaixo** (saída no relato). Idem pt contra o dicionário `pt`. (2) Mutações que têm de falhar: `lastUpdated: "2026-08"` no `topowalk-privacy.pt.md` (§4); `**Last updated:** September 2026` no `poleposition-privacy.en.md` (§4); um `### ` a menos no `topowalk-privacy.en.md` e uma linha de tabela a menos no `poleposition-privacy.en.md` (§12); um item de lista e um link a menos no `.en.md` (§12, regra nova); plugin de links desligado (regra nova de `noopener`); `topowalk-privacy.html` de volta em `COPIADOS_DA_RAIZ` com o arquivo antigo (§12 pelo rótulo de data duplicado, ou o build falha — os dois servem); `dist/en/poleposition-privacy.html` apagado (§4/§7). (3) `check_site.py` ganha: §12 paridade pt/en também de itens de lista (`^\s*([-*]|\d+\.) `), links (`](`), `code` (contagem de `` ` ``) e `^---$`; e, nas legais migradas, `target="_blank"` sem `noopener` no `rel` é erro (a régua geral é de `TARGET-BLANK-SEM-NOOPENER-01`, fatia 9). `html-validate`, `lychee` e `sha256sum -c` verdes. `site-ux` AUDITAR compara 360/1280 pt e en, com atenção a tabelas do PP, lista aninhada do PP e `hr`.
  - **Decisões do usuário (diferenças entre o `.md` do app e o publicado; o site segue o `.md` por D7 — não decidido aqui).** (D-a) TW, `docs/TOPOWALK_PRIVACY_POLICY.md:154` "Duas observações de precisão:" seguida de 3 itens (`:156-158`) ↔ publicado pt "Três observações de precisão:" (`topowalk-privacy.html:389`), en "Three notes for precision:". (D-b) PP, `docs/POLEPOSITION_PRIVACY_POLICY.md:236` "…ou pelo e-mail do desenvolvedor." ↔ publicado pt "…pelo e-mail do desenvolvedor em <strong>support@ghfsoftware.com</strong>.", en "…or the developer email at <strong>support@ghfsoftware.com</strong>." — seguir o `.md` tira o e-mail de contato da política. (D-c) PP, título `# Política de Privacidade — Pole Position: Race Analytics` (`:1`) ↔ h1 publicado "Política de Privacidade — Pole Position" / "Privacy Policy — Pole Position" (o h1 vem de `legal.ts`; o `#` do `.md` é omitido). (D-d) TW, `:383-384` "**GHF Software**" / "E-mail: **support@ghfsoftware.com**" em linhas seguidas sem quebra forçada (renderiza numa linha) ↔ publicado com `<br>` — só visual. Para D-a, D-b e D-d a correção, se o usuário quiser o publicado, é no repositório do app (como o e-mail do EclipseGo na fatia 6), espelhada depois; o agente não redige. Diferença só de marcação, sem decisão: TW `:367` `**…aplicativo**:` ↔ publicado `<strong>…aplicativo:</strong>`.
  - **Achados.** Fecha para TW e PP: `POLEPOSITION-NOOPENER-01`, `LEGAL-CORPO-SO-EM-JS-01`, `LEGAL-META-SEM-I18N-01` (as duas tinham `title` só em pt) e as tags de `LEGAL-SEM-OG-01`; os três últimos seguem abertos só para as 2 legais do LottoExpert (fatia 8). `CHECK-SEM-BUILD-INSTRUCOES-01` e a parte README/`CLAUDE.md:8` de `DOCS-ECLIPSE-MOVIDO-01` entram aqui (commit 6).
  - **Resolução das decisões** (usuário, 2026-10-15, "pode seguir o recomendado"): (D-a) "Duas" → "Três observações de precisão" e (D-d) quebra depois de `**GHF Software**\` corrigidas no app TopoWalk, commit 7fc7870 na branch `docs/politica-tres-observacoes` do `../topo-walk` (fora da master do app); (D-b) e-mail `support@ghfsoftware.com` na §10 no app Pole Position, commit 00968f5 na branch `item/PP-144-segunda-sessao-mesma-pista` (outra sessão do usuário, fora da main/develop do app); (D-c) h1 exibido "Política de Privacidade — Pole Position" / "Privacy Policy — Pole Position" via `legal.ts`, `#` do `.md` intacto. As datas das políticas não mudaram.
- **Fatia 7** (2026-10-15): implementada (af2a823, 7671f9e, 99e1881, 91b1bbf, cad6fa8, 5667f96, b40ba32); `topowalk-privacy` e `poleposition-privacy` no layout único. Entrou: plugin `linksExternosLegais` (`target="_blank" rel="noopener noreferrer"` nos links externos do texto legal), selos terracota/lima, CSS por tema com `:has` (hr antes de h2, tabelas, lista aninhada, `code`), §12 do `check_site.py` com paridade de listas, links, crases e `---` e `noopener` ausente como erro, páginas pt/en e `rota()` no botão da landing do Pole Position. Prova: diff por palavra do `dist/` contra o dicionário publicado, vazio em TW pt 5626, TW en 4600, PP pt 2697 e PP en 2458 palavras; 9 mutações do `site-dev` e as do `site-qa` acusam; b40ba32: regra de `noopener` com aspas simples, mutação conferida. `/verify` verde (build com cache limpo, `check_site.py` 20 páginas/468 links, contrato, html-validate 0 erros, plano; lychee só no CI). Auditoria: `site-qa` 0 alto, 2 médios de escrituração (este commit) e baixos corrigidos em b40ba32; `site-seo-perf` sem alto/médio, Lighthouse mobile pt antes→depois: TW Performance 70→77, Accessibility 77→94, LCP 4,9→4,2 s, HTML 125→56 KB; PP Performance 74→80, Accessibility 71→90, LCP 4,6→3,8 s, HTML 86→35 KB; `site-ux` 0 alto, alturas e posições de h2/h3 idênticas ao publicado a 1280/500/360, desvio aceito: `code` do PP com `px-1.5` em todos (2 eram `px-1`). Fecha `POLEPOSITION-NOOPENER-01` e, para TW/PP, `LEGAL-CORPO-SO-EM-JS-01`, `LEGAL-META-SEM-I18N-01` e as tags de `LEGAL-SEM-OG-01` (seguem abertos só para as 2 do LottoExpert, fatia 8); `CHECK-SEM-BUILD-INSTRUCOES-01` fechado; `DOCS-ECLIPSE-MOVIDO-01`: parte README/`CLAUDE.md` feita, resto na fatia 9; `ECLIPSE-COMENTARIO-PAR-EN-01` corrigido em b40ba32. **Aguarda:** integração pelo usuário e checklist de navegador. Status do WP continua `doing`.

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
