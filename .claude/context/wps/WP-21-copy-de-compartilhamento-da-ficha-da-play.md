---
id: WP-21
titulo: Title e description de compartilhamento vêm da ficha da Play
area: landing
status: doing
depende_de: [WP-11]
adr: []
spec: docs/AVALIACAO.md
decisoes: []
tamanho: M
risco: baixo
visual: false
branch: feat/wp-21-copy-de-compartilhamento
---

# WP-21 — Title e description de compartilhamento vêm da ficha da Play

**Depende de:** WP-11 · **Achados roteados:** `HOME-EN-META-01`, `LOTTO-EN-META-01`, `TOPO-EN-META-01`, `POLE-EN-META-01`, `ECLIPSE-EN-META-01`, `HOME-TITLE-LONGO-01`, `TITLE-HIFEN-TRAVESSAO-01`

**Objetivo:** `title`, `description` e og/twitter da home e das 4 landings, em pt e en, saem da copy oficial de cada app, e
não de texto herdado da página antiga.

**Contexto:** o veredito do WP-11 tirou estes achados do SEO técnico: são copy de produto. As páginas en reaproveitam textos
que a página antiga já publicava; o title pt da home tem 66 caracteres; o `<title>` usa hífen onde h1 usa travessão.

**Ler antes:** `../lotto-expert/docs/ASO_METADATA.md`, `../topo-walk/docs/store_listing_texts.md`,
`../pole-position/pole-position-app/docs/aso_plan.md`, `../eclipse-go/docs/EclipseGoContent.md`; `src/i18n/<pagina>.ts`.

**Arquivos-alvo:** `src/i18n/{home,lottoexpert,topowalk,poleposition,eclipsego}.ts`, `tools/check_site.py` (limite de title).

**Passos:**
1. Para cada página, escolher title (≤ 60) e description da ficha, em pt e en. Copy de produto é decisão do usuário: opções
   em `decisoes.md` se a ficha divergir da página.
2. Unificar o separador do `<title>` com o do h1.
3. `check_site.py`: erro para title > 60 caracteres.

**Critérios de aceite:**
- `python3 tools/check_site.py` verde, com a regra do title.
- Copy do LottoExpert sob o §5 (jogo responsável).
- Nenhum `title`/`description` en igual ao pt.

**Risco:** baixo. Copy de produto passa pelo usuário antes do commit.

## Veredito do arquiteto (site-arquiteto, 2026-10-15)

**Aprovado, com o desenho abaixo e a copy pendente da D19 (`/decisao`).** Nenhuma URL contratual
muda, nenhuma página nova, nada de deploy; o convite fica fora (congelado, D13). `risco: baixo` e
`visual: false` ficam: o que vai ao `<head>` o `check_site.py` prova; o card do WhatsApp entra no
checklist do `/release`. Os **Arquivos-alvo crescem** (fonte única do og e separador das legais).

### Fatos medidos (build de 4fdc621, `dist/`, `len()` de str Python após `html.unescape`)

| Página | `<title>` (nº) | description (nº) | og/twitter hoje |
|---|---|---|---|
| `index.html` | `GHF Software - Soluções Inovadoras em IoT e Engenharia de Software` (**66**) | 111 | og:title outro (43), og:description outra (127), twitter:description outra (73) |
| `en/index.html` | `GHF Software - Building the future of Mobility & IoT` (52) | 117 (= hero_desc) | og:title = title; og/twitter desc = `footer_desc` (115) |
| `lottoexpert.html` | `LottoExpert - GHF Software` (26) | 76 | og:title outro (44), og desc 98, twitter desc 65 |
| `en/lottoexpert.html` | **igual ao pt** (26) | **293** | og:title 51, og desc 293, twitter desc 62 ("manage your bets…") |
| `topowalk.html` | `TopoWalk - Levantamento Topográfico de Bolso e RTK` (50) | **248** | og:title 45, og desc 185, twitter desc 163 |
| `en/topowalk.html` | `TopoWalk - Pocket Topographic Survey & RTK` (42) | **274** | og = twitter = description (274) |
| `poleposition.html` | `Pole Position: Race Telemetry & Analytics - GHF Software` (56, em inglês) | 151 | og:title 52, og desc 104, twitter desc 61 |
| `en/poleposition.html` | **igual ao pt** (56) | **198** | og = twitter = description (198) |
| `eclipsego.html` | `EclipseGo - Previsão de Eclipses Offline - GHF Software` (55) | 146 | og:title 40; og = twitter desc 97 |
| `en/eclipsego.html` | `EclipseGo - Offline Eclipse Prediction - GHF Software` (53) | **182** | og = twitter = description (182) |

Origem: `src/pages/{,en/}<pagina>.astro:14–25` passam `x.title`, `x.description` e
`og={{ titulo: x.og_title, descricao: x.og_description, descricaoTwitter: x.twitter_description }}`
de `src/i18n/<pagina>.ts` (home.ts:17–23/74–81, lottoexpert.ts:20–25/153–159, topowalk.ts:16–23/84–91,
poleposition.ts:18–24/148–155, eclipsego.ts:18–23/73–78 — EclipseGo sem `twitter_description`).
`src/layouts/Base.astro`: `og:title = og.titulo ?? title`, `og:description = og.descricao ?? description`,
`twitter:title = og:title`, `twitter:description = og.descricaoTwitter ?? og:description`.
Legais: `src/i18n/legal.ts:13–47` (`*_title` com hífen, `*_h1` com travessão); 404: literal em
`src/pages/404.astro:7` (`·`). Hoje há **até 4 textos por página** para o mesmo cartão — 5 páginas
pt com og ≠ title, e a divergência não tem origem rastreável (fonte única, item 2: reprovado manter).

### Fontes da ficha (somente leitura)

| App | Arquivo, branch@commit | pt-BR título (30) / curta (80) | en título / curta |
|---|---|---|---|
| LottoExpert | `docs/ASO_METADATA.md:11–21`, `develop`@c7f11f0 (= master) | `LottoExpert: Loterias e Bolão` (sugestão 1) ou `LottoExpert Scanner e Matriz` (sugestão 2) / `Scanner de bilhetes, fechamentos, bolão e resultados oficiais da Caixa.` (71) | **não existe** (o app só tem `values/` pt) |
| TopoWalk | `docs/store_listing_texts.md:66–69,122–125`, `docs/politica-tres-observacoes`@b2ea76b (= develop = master) | `TopoWalk: Topo e Altimetria` (27) / `Topografia de campo: pontos, área, declividade, vista 3D e exportação PDF.` (74) | `TopoWalk: Survey & Altimeter` (28) / `Land surveying: points, area, slope %, 3D view, PDF export.` (59) |
| Pole Position | `docs/aso_plan.md:60–67,113–121`, `chore/release-2.2.0`@cd5b704 (= develop = master) | `Pole Position: Cronômetro GPS` (29; A/B: `Pole Position: Lap Timer GPS`) / `Lap timer GPS: cronômetro de voltas, parciais, velocidade e força G na pista` (76) | `Pole Position: GPS Lap Timer` (28) / `GPS lap timer with sector splits, speed and G-force telemetry for track days` (76) |
| EclipseGo | `docs/EclipseGoContent.md` existe, **não tem ficha** (base de suporte). Mais próximo: linha 14, "Resumo em uma frase", `docs/email-suporte-politica`@4668019 (main@439454c não diverge na linha) | `Descubra se e quando você vai poder ver o próximo eclipse solar ou lunar, sem precisar de internet.` (99) | **não existe** |
| GHF (home) | sem ficha. Publicado nos dois idiomas: `hero_titleHtml` (home.ts:25/83) e `footer_desc` (ui.ts:13/33) | — | — |

Régua do §5 (`COPY_PROIBIDA`) sobre a curta e o título do LottoExpert: **nada barrado**. Da descrição
longa, `Fechamento com Garantia Matemática` e `garanta uma premiação mínima` passam no regex
(`premiação` ≠ `prêmio`) mas não entram na proposta; `ferramenta definitiva` também não.

### Desenho

1. **Fonte única do cartão.** `og:title = twitter:title = <title>`; `og:description =
   twitter:description = description`. Saem de `Base.astro` os campos `titulo`, `descricao` e
   `descricaoTwitter` de `Og` (ficam `imagem` e `tipo`); saem de `src/i18n/<pagina>.ts` as chaves
   `og_title`, `og_description`, `twitter_description` (pt e en, §10 continua par a par); as 10
   páginas param de passá-las. O sufixo de marca no og:title fica: o WhatsApp mostra título e
   domínio, não `og:site_name`.
2. **Separador único: ` — ` (U+2014 entre espaços)**, o do h1. Landing: `<título da ficha> — GHF Software`
   (≤ 30 + 15 = ≤ 45, sem risco de estourar). Home: `GHF Software — <lema>`. Legal: `<h1> — GHF Software`
   (o mais longo: `Política de Privacidade — Pole Position — GHF Software`, 54), em `legal.ts`, só as 10
   chaves `*_title`; `*_description` e `*_h1` não mudam. Texto legal não é tocado (o corpo vem de
   `src/content/legal/`). A 404 (NOINDEX, bilíngue com `·`) fica fora — sem achado.
3. **Description = descrição curta da ficha, literal** (59–76 caracteres). Abaixo dos 110 sugeridos;
   aceito: é a copy oficial, sem composição do agente. Juntar curta + abertura da longa seria redação nova.
4. **`tools/check_site.py`, §14** (o `Cabeca` passa a ler o texto de `<title>`, com
   `convert_charrefs=True`; CONGELADAS já sai por `continue` antes — o convite fica isento, ADR-005 §5):
   - erro: `len(title) > 60`; erro: `len(description) > 160`;
   - erro: `og:title ≠ <title>`, `twitter:title ≠ og:title`, `og:description ≠ description`,
     `twitter:description ≠ og:description`;
   - erro: nas INDEXAVEIS, `<title>` com ` - ` ou sem `GHF Software` unido por ` — `;
   - erro: par en com `<title>` ou description igual ao pt (critério de aceite vira guarda).
   Docstring do §14 atualizada no mesmo commit.

### Proposta (contada; ★ = depende da D19)

| Página | Idioma | Campo | Valor | Nº | Fonte |
|---|---|---|---|---|---|
| home | pt | title ★ | `GHF Software — Construímos o futuro da Mobilidade e IoT` | 55 | home.ts:25 (h1) |
| home | en | title ★ | `GHF Software — Building the future of Mobility & IoT` | 52 | home.ts:83 (h1) |
| home | pt | description ★ | `Engenharia de software de ponta para aplicações Mobile e Internet das Coisas. Criando o futuro, com performance desde 2004.` | 123 | ui.ts:14 |
| home | en | description ★ | `Cutting-edge software engineering for Mobile and IoT applications. Creating the future with performance since 2004.` | 115 | ui.ts:34 |
| lottoexpert | pt | title ★ | `LottoExpert: Loterias e Bolão — GHF Software` | 44 | ASO_METADATA.md:11 |
| lottoexpert | en | title ★ | `LottoExpert: Lotteries & Sweepstakes — GHF Software` | 51 | tradução (vocabulário do site en) |
| lottoexpert | pt | description | `Scanner de bilhetes, fechamentos, bolão e resultados oficiais da Caixa.` | 71 | ASO_METADATA.md:20 |
| lottoexpert | en | description ★ | `Ticket scanner, wheels, sweepstakes and official Caixa lottery results.` | 71 | tradução |
| topowalk | pt | title | `TopoWalk: Topo e Altimetria — GHF Software` | 42 | store_listing_texts.md:67 |
| topowalk | en | title | `TopoWalk: Survey & Altimeter — GHF Software` | 43 | store_listing_texts.md:123 |
| topowalk | pt | description | `Topografia de campo: pontos, área, declividade, vista 3D e exportação PDF.` | 74 | store_listing_texts.md:70 |
| topowalk | en | description | `Land surveying: points, area, slope %, 3D view, PDF export.` | 59 | store_listing_texts.md:126 |
| poleposition | pt | title ★ | `Pole Position: Cronômetro GPS — GHF Software` | 44 | aso_plan.md:115 |
| poleposition | en | title | `Pole Position: GPS Lap Timer — GHF Software` | 43 | aso_plan.md:62 |
| poleposition | pt | description | `Lap timer GPS: cronômetro de voltas, parciais, velocidade e força G na pista` | 76 | aso_plan.md:121 |
| poleposition | en | description | `GPS lap timer with sector splits, speed and G-force telemetry for track days` | 76 | aso_plan.md:67 |
| eclipsego | pt | title ★ | `EclipseGo: Previsão de Eclipses Offline — GHF Software` | 54 | eclipsego.ts:25 (`hero_badge`) |
| eclipsego | en | title ★ | `EclipseGo: Offline Eclipse Prediction — GHF Software` | 52 | eclipsego.ts:80 (`hero_badge`) |
| eclipsego | pt | description ★ | `Descubra se e quando você vai poder ver o próximo eclipse solar ou lunar, sem precisar de internet.` | 99 | EclipseGoContent.md:14 |
| eclipsego | en | description ★ | `Find out if and when you will be able to see the next solar or lunar eclipse, no internet needed.` | 97 | tradução |

og:title/twitter:title = title; og:description/twitter:description = description, em todas.
Nenhum par en igual ao pt. Régua do §5 roda sobre os valores do LottoExpert e da home: verde.

### D19 — copy de compartilhamento (abrir com `/decisao`; o commit da copy espera)

- **(a) Ficha diverge da página** (TopoWalk perde "RTK"; Pole Position pt deixa de ser título em
  inglês): **(A) recomendada: a ficha vence** (é o objetivo do WP) · (B) manter o texto da página.
- **(b) Título do LottoExpert:** a ficha tem duas sugestões e não diz qual está no ar.
  **(A) recomendada: `LottoExpert: Loterias e Bolão`** (sugestão 1) · (B) `LottoExpert Scanner e Matriz`
  · (C) o que estiver no Play Console hoje, informado pelo usuário.
- **(c) LottoExpert en sem ficha:** **(A) recomendada: tradução fiel da ficha pt** (tabela acima) e
  registrar o en no `ASO_METADATA.md` do app depois (lá, pelo usuário) · (B) manter o en atual
  encurtado.
- **(d) Pole Position pt:** **(A) recomendada: `Cronômetro GPS`** (nome principal) · (B) `Lap Timer GPS` (variante A/B).
- **(e) EclipseGo sem ficha:** **(A) recomendada: title do `hero_badge` publicado + description do
  "Resumo em uma frase" e a tradução** · (B) manter a description atual da página (146 pt; en 182 > 160,
  teria de encurtar).
- **(f) Home:** **(A) recomendada: h1 + `footer_desc`** (já publicados nos dois idiomas) · (B) o
  og pt atual (`Soluções em IoT e Mobilidade` + `Aplicativos Android de engenharia para telemetria,
  topografia e loterias…`, 127) com tradução nova — omite o EclipseGo.

### Arquivos-alvo (substituem os do front-matter)

`src/i18n/{home,lottoexpert,topowalk,poleposition,eclipsego}.ts` · `src/i18n/legal.ts` (só `*_title`) ·
`src/layouts/Base.astro` (`Og` sem `titulo`/`descricao`/`descricaoTwitter`) ·
`src/pages/{index,lottoexpert,topowalk,poleposition,eclipsego}.astro` e os 5 de `src/pages/en/` (só o
objeto `og`) · `tools/check_site.py` (§14 e docstring). Fora: convite, `public/`, `src/content/legal/`,
`404.astro`, `ui.ts` (lido, não alterado).

### Commits

1. `WP-21: og e twitter iguais a title e description` — Base.astro, 10 páginas, remoção das chaves
   `og_*`/`twitter_description`; build + check verdes (o cartão passa a repetir o title atual).
2. `WP-21: separador — no <title> das legais` — legal.ts.
3. `WP-21: guardas de title e description no check_site.py` — fica **vermelho** até o commit 4
   (66 da home, 293/274/248/198/182 das descriptions, en = pt): não sobe sozinho; pode ir junto do 4.
4. `WP-21: title e description da ficha da Play` — só depois da D19 decidida; home e 4 landings.
5. `/verify`: build, `check_site.py`, `sha256sum -c ../tools/contrato.sha256`, html-validate, lychee.
   Achados roteados fecham no `site-docs`.
