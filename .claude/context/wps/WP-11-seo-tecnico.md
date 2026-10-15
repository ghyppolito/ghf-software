---
id: WP-11
titulo: Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página
area: seo
status: doing
depende_de: [WP-08]
adr: [ADR-005]
spec: docs/AVALIACAO.md
decisoes: [D16, D17, D18]
tamanho: M
risco: medio
visual: true
branch: feat/wp-11-seo-tecnico
---

# WP-11 — Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página

**Depende de:** WP-08 · **Achados roteados:** `LEGAL-SEM-OG-01`

**Objetivo:** `sitemap-index.xml` e `robots.txt` gerados no build; `<link rel="canonical">` e
`hreflang` pt-BR/en/x-default em toda página; JSON-LD `Organization` na home e
`MobileApplication` (nome, `operatingSystem: Android`, `applicationCategory`, link da Play,
`offers`) em cada landing; `og:*`/Twitter completos em todas as páginas, inclusive legais.

**Contexto:** `docs/AVALIACAO.md` §1 (SEO) e §2 item 6.

**Ler antes:** `docs/AVALIACAO.md` §1; integração `@astrojs/sitemap`; schema.org
`MobileApplication` (só as propriedades acima).

**Arquivos-alvo:** `astro.config.mjs`, `src/layouts/Base.astro` (`<head>`),
`src/components/Seo.astro`, `src/components/JsonLd.astro`, `public/robots.txt`,
`tools/check_site.py` (§2 passa a exigir canonical/hreflang).

**Critérios de aceite:**
- `test -f dist/sitemap-index.xml` e `robots.txt` com `Sitemap:`.
- `grep -L 'rel="canonical"' dist/**/*.html` vazio; idem `hreflang`.
- JSON-LD válido: `python3 -c` que extrai cada `<script type="application/ld+json">` e faz `json.loads` sem erro;
  `@type` esperado por página.
- `check_site.py` passa a exigir `og:image` em **todas** as páginas (regra promovida de aviso a erro neste WP).
- Validação no Rich Results Test do Google para a home e uma landing: captura no WP (usuário).

**Risco:** médio (ver o veredito).

## Veredito do arquiteto (site-arquiteto, 2026-10-15)

**Aprovado, com o desenho abaixo.** Os critérios originais ficam substituídos pelos desta seção.
Nenhum caminho contratual muda e nenhuma página nova é publicada. O `robots.txt`, porém, controla
quem lê o convite e o `assetlinks.json`, e o WP fecha o `x-default`, que o WP-15 previa. Por isso
o front-matter passou a `risco: medio`, `visual: true` e `adr: [ADR-005]` no commit do ADR,
com o `ESTADO.md` regenerado.

### Fatos medidos (worktree de 9405cc2, Node 22.22.1, Astro 7.3.8)

- **`@astrojs/sitemap` 3.7.4** (`npm install --save-exact`) acrescenta 5 pacotes ao lockfile
  (`@astrojs/sitemap`, `sitemap`, `@types/node`, `@types/sax`, `undici-types`; +50 linhas). Com
  `build.format: 'preserve'`, ele emite `https://ghfsoftware.com/eclipsego` e
  `https://ghfsoftware.com/en`, sem `.html` e sem a barra final, enquanto o canonical é
  `/eclipsego.html` e `/en/`. O sitemap discordaria do canonical, e `/en` sofre redirect no Pages.
  O integration ignora `public/`, então o convite fica de fora sem configuração.
- **Endpoint à mão** (`src/pages/sitemap.xml.ts`, ~15 linhas, usa `SITE`, `rota` e `COM_PAR_EN`
  de `src/i18n/ui.ts`). Gera 20 `<loc>` iguais aos canonicals, com `xhtml:link` pt-BR, en e
  x-default. O XML faz parse e o `check_site.py` fica verde, sem nenhuma dependência nova.
  `src/pages/robots.txt.ts` também gera, e o §13 continua intacto.
- **Imagens de og:**

  | Arquivo | Formato e tamanho real | Onde é og:image | O que a página declara |
  |---|---|---|---|
  | `GHFSoftware.png` | PNG 677×369 | home e as 10 legais | home: 1200×630; legais: nada |
  | `topowalk_screenshot.png` | JPEG 1024×1024 | landing do TopoWalk | 1200×630 |
  | `poleposition_real_mockup.png` | JPEG 1024×1024 | landing do Pole Position | 1200×630 |
  | `lottoexpert_app_mockup.png` | JPEG 1024×1024 | landing do LottoExpert e convite | landing: 1200×630; convite: 1024×1024, que é o real |
  | `eclipse-go.png` | PNG 442×442 | landing do EclipseGo | 1200×630 |

  Hoje 5 páginas declaram 1200×630 e nenhuma imagem tem esse tamanho.
- **Dados de cada app (fontes):**
  - O link da Play já está em `src/components/{LottoExpert,TopoWalk,PolePosition,EclipseGo}.astro`
    e `Home.astro:264,302,342,380`.
  - A categoria da Play não aparece em nenhuma fonte. `../lotto-expert/docs/ASO_METADATA.md:100`
    só *recomenda* "Ferramentas ou Entretenimento".
  - Há fonte para "gratuito" no LottoExpert (`ASO_METADATA.md:67`) e no TopoWalk
    (`docs/TOPOWALK_README.md:5`). Não há para o Pole Position nem para o EclipseGo.

### ADR: sim, ADR-005 (primeiro commit)

Título: *"Sitemap, robots e hreflang saem da mesma lista de rotas, por endpoint do Astro"*.
- Diverge de `docs/AVALIACAO.md` §3.2, que dizia "sitemap por integração". O motivo é o fato medido acima.
- Fixa a forma canônica das URLs: `.html`, `/` e `/en/`, como no ADR-001 e no ADR-002 §2.
- Fixa que o convite e o `assetlinks.json` ficam fora de toda regra de SEO e de todo `Disallow`.
- Para o `x-default` = en, cita a D8 e o WP-15 passo 1, sem redecidir.
- Não repete o ADR-001.

### `@astrojs/sitemap`: não

Cumprir o critério com ele exigiria um `serialize` que reescreve cada URL, ou seja, a mesma lógica
do endpoint, mais 5 pacotes. O endpoint usa a lista que já gera o hreflang (fonte única). O WP-15,
quando generalizar os idiomas, troca `COM_PAR_EN` pelo mapa de `idiomas.ts` num só lugar. O
critério passa a ser `dist/sitemap.xml`, sem índice: são 20 URLs.

### Canonical, hreflang e indexação por página

| Página | canonical | hreflang | robots | sitemap | JSON-LD |
|---|---|---|---|---|---|
| 10 pt (`/`, `/x.html`) | a própria URL (= og:url) | pt-BR → pt, en → `/en/…`, x-default → `/en/…` | indexável | sim | home: `Organization`; landing: `MobileApplication`; legal: nenhum |
| 10 en (`/en/`, `/en/x.html`) | a própria URL | as mesmas três, recíprocas | indexável | sim | idem ao par pt |
| `404.html` | `/404.html` (como hoje; o Pages responde com status 404 em caminho inexistente) | nenhum | `noindex` | não | nenhum |
| convite | **nada muda** (sha256, D13): sem canonical, hreflang nem JSON-LD | — | sem meta, sem Disallow | **não** | nenhum |
| `/.well-known/assetlinks.json` | — | — | sem Disallow | não | — |

- **O convite fica fora do sitemap.** Sem `?d=`, a URL mostra só o estado de erro: não há conteúdo
  para indexar e o Google trataria a página como soft 404. Cada `?d=` é um bolão privado e não deve
  ser indexado.
- O crawler de preview do WhatsApp lê o og direto do HTML. A garantia é não haver nenhum `Disallow`.
- **`robots.txt`** sai do endpoint `src/pages/robots.txt.ts`, e não de `public/robots.txt`, por
  dois motivos: o `Sitemap:` sai de `site`, e a lista fechada `PUBLIC` do §13 não muda. Conteúdo
  literal: `User-agent: *` / `Allow: /` / linha vazia / `Sitemap: https://ghfsoftware.com/sitemap.xml`.
- **Somente a 404 tem `noindex`.**

### JSON-LD (`src/components/JsonLd.astro`)

- **Saída.** Um `<script type="application/ld+json">` com `JSON.stringify`, trocando todo `<`
  pela sequência de escape `\u003c` (barra invertida, u, 003c). Os dados ficam num só módulo, `src/i18n/apps.ts` (novo), e o botão "Google Play" da
  landing e da home passa a ler o link de lá. Assim o JSON-LD e o botão não têm como divergir.
- **`Organization` (home pt e en):** só `@context`, `@type`, `name` ("GHF Software"),
  `url` (`https://ghfsoftware.com/`) e `logo` (`/assets/GHFSoftware.png`, absoluto).
  Sem `sameAs`, `contactPoint` e `foundingDate`: não estão no WP.
- **`MobileApplication` (4 landings, pt e en):** exatamente `@context`, `@type`, `name`,
  `operatingSystem: "Android"`, `applicationCategory`, `installUrl` e `offers`.
  - `installUrl` é o link da Play de `apps.ts`, sem `&hl=pt_BR` (mesmo `id`).
  - `applicationCategory` é um valor da lista do Google (`UtilitiesApplication`, …), mapeado da
    categoria real da Play, **que o usuário informa** (decisão abaixo).
  - `offers` = `{"@type":"Offer","price":"0","priceCurrency":"BRL"}`, só para app com fonte de
    "gratuito".
  - Preço do Premium ou do Pro nunca entra: o preço vem da Play e do Remote Config, nunca de um
    literal (`docs/TOPOWALK_README.md:305`). Sem `aggregateRating` e sem `review`: nota inventada
    ou copiada da Play fere a política do Google.
- **Consequência para o critério de Rich Results.** Sem `aggregateRating`/`review`, o Google não
  dá rich result a `SoftwareApplication`. O Rich Results Test acusa a landing como inelegível, e
  isso é esperado. O critério passa a ser:
  - home no **Rich Results Test**: `Organization` detectado, 0 erro;
  - landing no **Schema Markup Validator** (validator.schema.org): `MobileApplication`, 0 erro e
    0 aviso.

### og:image

- **Neste WP, sem decisão:**
  - O §2 promove "sem og:image" de aviso a **erro** em todas as páginas de `dist/`. Hoje todas têm.
  - Novo erro: `og:image:width`/`height` declarados diferentes do tamanho real do arquivo (lido do
    cabeçalho PNG ou JPEG, só com a stdlib).
  - O `Base.astro` passa a declarar o tamanho real ou a omitir os dois atributos. Isso fecha a
    "mentira" de `OG-IMAGE-DIMENSAO-01` sem criar imagem.
  - O convite já declara o tamanho real.
- **A imagem 1200×630 é design** e fica para a decisão abaixo.
- **Fica fora de qualquer opção:** mudar `assets/lottoexpert_app_mockup.png` (sha256, D13) e o
  og:image do convite.

### Achados

| Achado | Destino |
|---|---|
| `ROBOTS-SITEMAP-AUSENTES-01` | **entra**, resolvido por este WP |
| `CONVITE-FORA-DO-WP-11-01` | **entra**: lista `CONGELADAS` no `check_site.py` (só o convite, a mesma de `contrato.sha256`), isenta das regras de canonical, hreflang, og completo e JSON-LD; `robots.txt` sem `Disallow`; o convite fora do sitemap é provado no check |
| `HOME-HREFLANG-XDEFAULT-01` | **entra** (sai do WP-15): o objetivo deste WP já pede `x-default`; a regra é a da D8 e do WP-15 passo 1 (en) |
| `LEGAL-SEM-OG-01` | **entra** a parte das tags (og:image vira erro). A parte da imagem se junta a `OG-IMAGE-DIMENSAO-01` |
| `OG-IMAGE-DIMENSAO-01`, `LEGAL-OG-IMAGE-DIMENSAO-01` | **entra** a declaração verdadeira e a guarda. A imagem 1200×630 depende da **D16**: se for (A) ou (B), vira um WP novo pelo `/novo-wp`, antes do deploy único; se for (C), resolve aqui |
| `HOME-EN-META-01`, `LOTTO-EN-META-01`, `TOPO-EN-META-01`, `POLE-EN-META-01`, `ECLIPSE-EN-META-01`, `HOME-TITLE-LONGO-01`, `TITLE-HIFEN-TRAVESSAO-01` | **saem**: são copy de produto, não SEO técnico. Vão para um WP novo, pelo `/novo-wp`: "title e description de compartilhamento vêm da ficha da Play", com fonte `ASO_METADATA.md`, `../topo-walk/docs/store_listing_texts.md`, `../pole-position/pole-position-app/docs/aso_plan.md` e `../eclipse-go/docs/EclipseGoContent.md`, em pt e en, antes do deploy único |
| `LEGAL-SLUG-ACENTO-01` | **sai** para o WP-15: âncora entre idiomas é estrutura de i18n. Os ids ainda não estão no ar (D13), então mudar antes do deploy custa zero |
| `OG-MOCKUP-JPEG-PESADO-01`, `ASSETS-PNG-LCP-01`, `CONVITE-FORA-DO-WP-12-01` | continuam no WP-12 |

### Arquivos-alvo (substitui a lista)

- `.claude/context/decisions/ADR-005-*.md` (novo).
- `astro.config.mjs`: só comentário, sem integração.
- `src/pages/sitemap.xml.ts` e `src/pages/robots.txt.ts`, ambos novos.
- `src/layouts/Base.astro`: x-default, og dimensões e o slot de JSON-LD.
- `src/components/JsonLd.astro` (novo).
- `src/i18n/apps.ts` (novo).
- `src/components/{Home,LottoExpert,TopoWalk,PolePosition,EclipseGo}.astro`: link da Play lido de
  `apps.ts`.
- As 10 páginas de `src/pages/` e de `src/pages/en/` que passam o JSON-LD: home e as 4 landings,
  nos dois idiomas.
- `tools/check_site.py`.
- `CLAUDE.md`: a seção "Arquitetura" ganha `sitemap.xml`, `robots.txt` e `apps.ts`.
- Fora da lista: `Seo.astro` não é criado, porque o `<head>` já é único no `Base.astro` (WP-08).
  O WP-15 passa a ler `Base.astro` onde hoje cita `Seo.astro`.

### Ordem de commits

1. `WP-11: ADR-005` (e `adr: [ADR-005]` no front-matter).
2. `check_site.py` §14 (SEO) e as listas `CONGELADAS`/`INDEXAVEIS`. Este commit fica **vermelho**
   de propósito: mostra o que falta. Se o CI exigir verde por commit, juntar com o 3.
3. `Base.astro`: x-default e dimensões verdadeiras de og.
4. `robots.txt.ts` e `sitemap.xml.ts`.
5. `apps.ts`, `JsonLd.astro`, os botões da Play lendo `apps.ts` e as 10 páginas com JSON-LD.
   `offers` e `applicationCategory` só depois da D17. Sem ela, o commit sai sem esses dois campos e
   o §14 marca a falta como erro.
6. `CLAUDE.md` e a escrituração.

### Critérios de aceite (substituem os originais)

- `npm run build`, `check_site.py`, `sha256sum -c tools/contrato.sha256`, html-validate e lychee
  todos verdes.
- `dist/sitemap.xml` faz parse. O conjunto de `<loc>` é igual ao conjunto dos canonicals das 20
  páginas indexáveis, e cada `<loc>` existe em `dist/`.
- `dist/robots.txt` é igual ao literal acima.
- Em toda página fora de `CONGELADAS`:
  - exatamente um canonical, igual ao og:url e à URL da própria página;
  - nas 20 páginas: pt-BR, en e x-default (= en) recíprocos;
  - `noindex` só na 404;
  - og:image presente, e width/height, quando declarados, iguais aos reais.
- JSON-LD: cada `<script type="application/ld+json">` passa por `json.loads`.
  - `@type` por página: `Organization` só nas duas home; `MobileApplication` só nas 8 landings;
    zero nas demais.
  - As chaves do `MobileApplication` são exatamente o conjunto permitido.
  - `installUrl` tem o mesmo `id` do botão da Play da página.
  - O §5 (`COPY_PROIBIDA`) roda também sobre o conteúdo do JSON-LD.
- Usuário (`visual: true`):
  - Rich Results Test da home (`Organization`, 0 erro);
  - Schema Markup Validator de uma landing (0 erro, 0 aviso);
  - Search Console: sitemap enviado e lido (depois do deploy único);
  - preview no WhatsApp de um link de convite real gerado pelo app e de uma landing, sobre o site
    no ar (deploy único, D13 condição 4);
  - captura de tela no WP.

### Mutações que têm de falhar (o `site-qa` roda cada uma)

1. `Disallow: /lotto-expert/`, `Disallow: /.well-known/`, `Disallow: /assets/` ou `Disallow: /` no `robots.txt`.
2. Apagar `robots.txt.ts` ou `sitemap.xml.ts`.
3. Convite ou 404 no sitemap. `<loc>` em `/eclipsego` ou `/en`, sem `.html` e sem a barra.
4. Canonical no convite, por edição em `public/` (pega no sha256 e no §14).
5. Tirar o `x-default` do `Base.astro`. `x-default` apontando para o pt. Canonical do en apontando para o pt.
6. og:url diferente do canonical.
7. `noindex` numa landing ou numa legal.
8. og:image removido de uma legal.
9. `og:image:width="1200"` sobre `GHFSoftware.png`.
10. JSON-LD com vírgula sobrando. `Organization` numa legal. `MobileApplication` ausente numa landing.
11. `aggregateRating` acrescentado. `offers.price: "7.90"`. `installUrl` com outro `id` que não o do botão.
12. "maximize" no JSON-LD do LottoExpert (§5).

### Decisões do usuário (registrar com `/decisao`; não bloqueiam os commits 1–4)

- **D16. Imagem de compartilhamento 1200×630.**
  - **(A) recomendada:** uma imagem da marca GHF, 1200×630, ≤ 300 KB, para a home e as 10 legais,
    e uma por app para as landings. Feitas no Claude Design (WP-10/WP-19), a partir do handoff.
  - **(B)** só a imagem da marca para todas as páginas, sem imagem por app.
  - **(C)** manter as imagens atuais com o tamanho real declarado. O WhatsApp e o LinkedIn
    cortam ou mostram miniatura; nenhum trabalho de design.
  - Em todas: o convite e `lottoexpert_app_mockup.png` ficam como estão (D13).
- **D17. Dados do `MobileApplication`.**
  - **(A) recomendada:** o usuário informa a categoria da Play de cada app (4 valores) e se o
    Pole Position e o EclipseGo são gratuitos para baixar. O agente mapeia para o enum do Google
    numa tabela no WP, com a fonte "Play Console, informado em <data>". `offers` só com preço 0 BRL.
  - **(B)** `offers` só onde há fonte escrita hoje (LottoExpert e TopoWalk); Pole Position e
    EclipseGo ficam sem `offers` até o README do app registrar o modelo.
  - **(C)** tirar `applicationCategory` e `offers` do WP. O JSON-LD fica com `name`,
    `operatingSystem` e `installUrl`, e o WP-11 muda o próprio objetivo.
- **D18. `x-default` nas páginas que a D8 não cobre** (home, LottoExpert e EclipseGo).
  - **(A) recomendada:** en, a mesma regra do WP-15 passo 1. Efeito colateral: quem lê pt-PT cai
    no en, porque o hreflang é `pt-BR`.
  - **(B)** pt nessas três, e en só no TopoWalk e no Pole Position.
  - Se a resposta não vier antes do commit 3, ele usa (A) e o usuário pode reverter numa linha.

## Decisões D16, D17 e D18 (usuário, 2026-10-15: "pode seguir o recomendado")

As três foram decididas na opção (A) e registradas em `decisoes.md`. A ADR-005 consolida o
desenho. O que muda no veredito acima:

- **D16 (A).** As imagens 1200×630 (marca para home e legais, uma por app) não são deste WP. Aqui
  só se declara o tamanho real e o `check_site.py` barra declaração falsa. A produção vai para um
  WP novo pelo `/novo-wp`, e não para o WP-19, cujo export da rodada 3 está congelado e auditado
  (achado `OG-IMAGE-1200-PRODUCAO-01`, em `triagem` até o `/novo-wp`). Convite e mockup intactos (D13).
- **D17 (A).** Fonte: o JSON-LD público da ficha de cada app na Play
  (`play.google.com/store/apps/details?id=…&hl=en&gl=BR`), lido pelo orquestrador em 2026-10-15.

  | App (`id` da Play) | Categoria na Play | `applicationCategory` no site | `offers` |
  |---|---|---|---|
  | `br.com.ghfsoftware.lottoexpert` | TOOLS | `UtilitiesApplication` | `{"@type":"Offer","price":"0","priceCurrency":"BRL"}` |
  | `br.com.ghfsoftware.topowalk` | TOOLS | `UtilitiesApplication` | idem |
  | `br.com.ghfsoftware.polepositionapp` | SPORTS | `SportsApplication` | idem |
  | `br.com.ghfsoftware.eclipsego` | LIFESTYLE | `LifestyleApplication` | idem |

  **Escolha técnica: o enum do schema.org/Google, e não o valor cru da Play.** O Google documenta
  `applicationCategory` com os valores `*Application`. `TOOLS` é o identificador interno da Play,
  e o Google não o reconhece no `SoftwareApplication`. O mapeamento fica numa tabela de
  `src/i18n/apps.ts`, com a categoria da Play ao lado como comentário, para quem conferir a ficha.
  `offers` vale para os 4 apps; preço do Premium/Pro, `aggregateRating` e `review` nunca entram.
  Com isso, o commit 5 sai com os dois campos, e o §14 os exige.
- **D18 (A).** O `x-default` → en nas 20 páginas com par, inclusive home, LottoExpert e EclipseGo.
  O critério "x-default (= en)" fica como está.

## Estado (fim da implementação, 2026-10-15)

**Status: `doing`, de propósito.** Falta o relato do usuário nos dois validadores (`visual: true`). Depois do merge dele na
integração (`feat/wp-08-layout-unico`) e do CI do #37 verde, o agente marca `done`. "Publicado" só com o deploy único (D13).

**Commits:** 9405cc2 início · 6838d10 veredito · 3b9b3d4 ADR-005, D16/D17/D18 · f6188d1 §14, x-default, dimensões de og ·
97fb75d `robots.txt` e `sitemap.xml` · 8a41c21 `apps.ts`, JSON-LD, botões da Play · a88e881 docs · 262d330 §14 barra SEO no
convite · 547c29c correções da auditoria.

**Provas de máquina (547c29c):** `/verify` verde. `<body>` das 21 páginas idêntico ao build de 3b9b3d4, botões da Play byte
a byte iguais, convite intacto. 14 mutações do veredito e 6 das correções falham como deviam. lychee só no CI.

**Auditoria.** `site-qa`: 0 alto, 1 médio (`content="none"`) e 6 baixos, todos corrigidos em 547c29c. `site-seo-perf`: 0
bloqueante; sitemap e hreflang recíprocos nas 20 páginas; HTML +0,9 %. `site-ux` não invocado (nada visível mudou).

**Achados roteados:** imagens (`OG-IMAGE-1200-PRODUCAO-01`, `TWITTER-CARD-IMAGEM-QUADRADA-01`, `OG-IMAGE-ALT-TYPE-01`,
`ORG-LOGO-NAO-QUADRADO-01`) para o WP-20; copy (`*-EN-META-01`, `HOME-TITLE-LONGO-01`, `TITLE-HIFEN-TRAVESSAO-01`) para o WP-21.

**Falta, do usuário (`visual: true`), já possível sem o site no ar:** colar o HTML na aba "Código" de cada ferramenta.
1. Rich Results Test com `dist/index.html`: `Organization` detectado, 0 erro.
2. Schema Markup Validator (validator.schema.org) com `dist/lottoexpert.html`: `MobileApplication`, 0 erro e 0 aviso.
(`python3 -m http.server` não é necessário. Escreva o resultado aqui.)

**Movido para o checklist do deploy único (D13), `handoff.md` §3, e não prende o `done`:** Search Console (sitemap enviado e
lido) e preview no WhatsApp de um convite real e de uma landing, sobre o site no ar.
