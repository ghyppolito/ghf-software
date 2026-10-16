# Arquitetura do site ghfsoftware.com

Como o site é feito, de onde sai cada página e o que prova que ela está certa. O **porquê** de
cada escolha está nos ADRs em `.claude/context/decisions/`; as regras de projeto, no `CLAUDE.md`.

Em uma frase: o Astro gera `dist/` a partir de `src/` (páginas, layouts, componentes, dicionários,
texto legal) e copia `public/` byte a byte; `dist/` é o que vai ao ar, e a rede de segurança é o
`tools/check_site.py` rodando sobre `dist/`. Nenhum `.html` mora na raiz do repositório: página só
sai de `src/pages/` (`tools/check_site.py` §7). Nav, footer e config mudam só no componente.

---

## 1. Build (ADR-002, ADR-003)

| Arquivo | Papel |
|---|---|
| `package.json` / `package-lock.json` | Astro, `@astrojs/markdown-satteri`, Tailwind 3.4.19, html-validate, lighthouse; Node 22.22 |
| `astro.config.mjs` | `build.format: 'preserve'` (cada rota sai como `x.html`, igual às URLs contratuais), fonte Inter local pela API `fonts`, Sätteri com os plugins de `src/markdown/legal.mjs` |
| `tailwind.config.mjs` | tokens `brand.*` (base, surface, primary, secondary, accent) por variável CSS, Inter |
| `postcss.config.mjs` | Tailwind compilado pelo PostCSS do Vite (ADR-003) |
| `src/styles/global.css` | valores dos tokens por tema (um tema por página), tipografia do texto legal |

`npm run build` = `astro build --force`. A saída é `dist/`, que não é versionada.

`design/` guarda o brief e o handoff do Claude Design (WP-06); quando houver handoff, ele prevalece
sobre o sistema visual que está no código.

## 2. `public/` — o que passa sem build (ADR-002 §3, ADR-006)

Copiado byte a byte para `dist/`. Lista fechada; nenhuma página mora aqui (`tools/check_site.py` §13):

| Caminho | O que é |
|---|---|
| `public/assets/` | só arquivo de URL fixa: `og:image`, favicons e imagens do convite (PNG, sem otimização) |
| `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html` | página do convite de bolão (pako + Base64, lê o `?d=` do link) |
| `public/.well-known/assetlinks.json` | App Links do LottoExpert |
| `public/CNAME` | domínio do GitHub Pages |

Imagem **exibida** na página não fica em `public/`: sai de `src/assets/img/` pelo `astro:assets`
(WebP, `width`/`height`, `loading="lazy"` fora do hero — ADR-006). Ícones são SVG inline de
`src/icons/fa/` pelo `src/components/Icon.astro`, sem Font Awesome por CDN. A fonte é
`src/assets/fonts/inter-latin-wght.woff2` (OFL em `src/assets/fonts/OFL.txt`).

O convite, o `public/.well-known/assetlinks.json`, a `og:image` do convite e o `CNAME` têm hash fixo em
`tools/contrato.sha256` (D13): mudam só de propósito.

## 3. Rotas (`src/pages/`)

| Caminho | O que gera |
|---|---|
| `src/pages/index.astro`, `src/pages/lottoexpert.astro`, … | a página em pt, literal, no caminho de sempre (`/lottoexpert.html`) |
| `src/pages/[lang]/` | as outras línguas de cada página por `getStaticPaths`, lidas de `src/i18n/idiomas.json` (`/en/lottoexpert.html`); nunca gera `pt/` |
| `src/pages/404.astro` | 404, só em pt |
| `src/pages/robots.txt.ts`, `src/pages/sitemap.xml.ts` | endpoints da mesma lista de rotas do `canonical` (ADR-005) |

As rotas são cascas: a página inteira é um componente de `src/components/paginas/` que recebe a
prop `lang`.

## 4. Layouts e componentes

| Caminho | Papel |
|---|---|
| `src/layouts/Base.astro` | `<head>` único: título, descrição, `canonical`, `hreflang` por língua da página + `x-default` (en se houver, senão pt), `og:*` com `width`/`height` lidos do arquivo, Inter local, slot de JSON-LD, tema da página; faixa `SugestaoIdioma` no fim do `<body>` |
| `src/layouts/LegalLayout.astro` | hero e card das páginas legais |
| `src/components/Nav.astro`, `src/components/Footer.astro` | nav e footer, iguais em todas as páginas — mudam só aqui |
| `src/components/SeletorIdioma.astro` | só as línguas da página: link com 2, lista com 3+ |
| `src/components/SugestaoIdioma.astro` | faixa que sugere a língua do navegador; nunca navega sozinha |
| `src/components/JsonLd.astro` | um bloco JSON-LD por landing |
| `src/components/Home.astro`, `src/components/LottoExpert.astro`, `src/components/TopoWalk.astro`, `src/components/PolePosition.astro`, `src/components/EclipseGo.astro` | corpo de cada landing |
| `src/components/paginas/` | uma `Pagina<Nome>.astro` por página: layout + corpo, com a prop `lang` |

## 5. Conteúdo legal (`src/content/legal/`, ADR-004)

Um arquivo por app, documento e língua (`src/content/legal/lottoexpert-privacy.pt.md`,
`src/content/legal/lottoexpert-privacy.en.md`, …), declarados em `src/content.config.ts`.
Front-matter: `lastUpdated: "AAAA-MM[-DD]"` em todos. Só o `.pt.md` tem o commit de origem no app
(`origemCommit`, 40 hex) e, enquanto uma tradução está atrás, `pendente: [códigos]` — o
`tools/check_site.py` reprova enquanto o `pendente` existir. A tradução só tem `lastUpdated`.

- O `.pt.md` é o `.md` do repositório do app **byte a byte**, copiado de um commit por
  `tools/sync_legal.py` (só pelo `/legal`). O inglês é tradução fiel, feita aqui.
- `src/markdown/legal.mjs` (plugins do Sätteri): título e data saem do corpo; link do próprio
  site vira caminho a partir da raiz, com o prefixo da língua; id dos títulos pela posição
  (`secao-2-1`), igual em todas as línguas.
- Hero e textos de `<head>` das legais: `src/i18n/legal.ts`.

## 6. i18n (ADR-007, D23)

- `src/i18n/idiomas.json` é a **fonte única** das línguas do site (rótulos, `hreflang`,
  `og:locale`, meses) e das línguas de cada página. O build, o `tools/check_site.py` e o
  `tools/sync_legal.py` leem dali.
- pt fica na raiz; as outras línguas em `/<código>/`. Sem redirecionamento.
- Língua listada para uma página é espelho completo; língua não listada não aparece (nem
  página, nem seletor, nem `hreflang`).
- `src/i18n/idiomas.ts` valida o mapa e exporta `linguasDe`, `rota` e os atributos de link.
  **D23:** link para uma página que não existe na língua atual vai para o en, se o destino tem
  en, senão para o pt, e leva `hreflang`/`lang` da língua de destino.
- Dicionários: `src/i18n/ui.ts` (nav, footer, textos comuns), um por página
  (`src/i18n/home.ts`, `src/i18n/lottoexpert.ts`, `src/i18n/topowalk.ts`,
  `src/i18n/poleposition.ts`, `src/i18n/eclipsego.ts`), `src/i18n/legal.ts` e
  `src/i18n/apps.ts` (id, categoria e link da Play de cada app — botão e JSON-LD leem dali).

## 7. URLs contratuais (ADR-001)

Os apps instalados e a Play Store apontam para estes caminhos; eles nunca mudam nem viram
redirecionamento (o Android App Links não segue redirect):

```
/.well-known/assetlinks.json
/lottoexpert-privacy.html   /lottoexpert-terms.html
/topowalk-privacy.html      /poleposition-privacy.html   /eclipsego-privacy.html
/lotto-expert/sweepstake-invite/lottoexpert-invite.html
```

`tools/check_site.py` §1 prova que cada um existe em `dist/`; o §16 barra redirecionamento (script ou
`<meta refresh>`) em qualquer página.

## 8. Verificação

| Ferramenta | O que prova |
|---|---|
| `tools/check_site.py` | sobre `dist/` (sem `dist/`, pede o build): URLs contratuais, links e assets, metadados, datas legais contra `src/content/legal/` e o commit do app, copy do LottoExpert (jogo responsável), `public/.well-known/assetlinks.json`, `hreflang`, língua dos links, `public/` fechado, SEO técnico, desempenho (sem fonte do Google, imagem pelo build), nenhum redirecionamento |
| `tools/regras_i18n.py` + `tools/test_regras_i18n.py` | regras de i18n como funções puras, que o `tools/check_site.py` chama; testadas sobre `tools/fixtures/i18n/` |
| `tools/contrato.sha256` | convite, `public/.well-known/assetlinks.json`, `og:image` do convite e `CNAME` iguais ao publicado |
| `tools/sync_legal.py` | o espelho legal está igual, atrás ou divergente do app (`--todos --check`) |
| `tools/lighthouse.py` | orçamento de bytes e Lighthouse mobile contra `tools/orcamento-lighthouse.json` |
| `tools/gen_estado.py`, `tools/check_plano.py` | backlog (`.claude/context/ESTADO.md` gerado dos WPs) e consistência do plano |
| html-validate (`.htmlvalidate.json`), lychee | HTML válido e links internos de `dist/` |

## 9. CI e deploy (ADR-002 §4, D5, D13)

- `.github/workflows/pr.yml`, em todo PR e push para `develop`/`master`, três jobs:
  - `plano`: `gen_estado.py --check` e `tools/check_plano.py`;
  - `site`: `npm ci`, `npm run build`, `tools/check_site.py --raiz dist`, unittest das regras de
    i18n, contrato byte a byte, html-validate e lychee sobre `dist/`;
  - `lighthouse`: build e `tools/lighthouse.py --raiz dist`.
- `.github/workflows/deploy.yml`, em push para `master` (e à mão): build, `tools/check_site.py`,
  conferência do `public/.well-known/assetlinks.json` e do contrato byte a byte, e publicação de `dist/` no
  GitHub Pages em modo "GitHub Actions" (variável `PAGES_VIA_ACTIONS`).
- Fluxo git `feat → develop → master` (D5): o PR do WP mira `develop`; `develop → master` é
  deploy, feito só pelo usuário pelo `/release` (`.claude/commands/release.md`).
- Rollback é por tag (D13): rodar o `Deploy` sobre a tag `pre-modernizacao` (marcada em `master`
  antes do deploy único), sem reverter merge. Pré-requisito: a tag na `deployment-branch-policies`
  do ambiente `github-pages` e um ensaio — D13 em `.claude/context/decisoes.md`.
