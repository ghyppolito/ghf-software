# GHF Software — site (ghfsoftware.com) — regras do projeto

Site estático da GHF Software: landing corporativa, uma landing por app (TopoWalk, LottoExpert,
Pole Position, EclipseGo), políticas de privacidade, termos de uso e a página do convite de bolão
do LottoExpert. **Em produção**, servido pelo GitHub Pages (por Actions) a partir da branch `master`.

As páginas são geradas pelo Astro a partir de `src/` (Tailwind compilado) em `dist/`, com `public/`
copiado byte a byte; o CI do PR (`check_site.py`, html-validate, lychee) prova `dist/`. A
evolução dessa stack é o backlog (ver `docs/AVALIACAO.md`). Este arquivo é curto de propósito — leia inteiro. O detalhe
está em `.claude/context/` e é lido **sob demanda**:

| Arquivo | O que tem |
|---|---|
| `.claude/context/handoff.md` | onde a última sessão parou — **leia ao começar** |
| `.claude/context/ESTADO.md` | **backlog** — status e sequência recomendada, gerado de `wps/` |
| `.claude/context/wps/WP-NN-*.md` | um arquivo por Work Package: objetivo, arquivos-alvo, critérios, o que só o navegador prova |
| `.claude/context/achados-novos.md` | o que foi achado fora de escopo, com destino |
| `.claude/context/decisoes.md` | decisões de produto e processo — em aberto bloqueiam o WP |
| `.claude/context/invariantes.md` | regras com a mesma autoridade deste arquivo, em detalhe |
| `.claude/context/decisions/ADR-NNN-*.md` | o **porquê** de cada decisão de arquitetura |
| `docs/AVALIACAO.md` | diagnóstico do site (2026-10-12) e a direção recomendada — origem do backlog |

---

## Fontes de verdade

| Documento | Autoridade |
|---|---|
| Repositório de cada app (`../lotto-expert/docs/PRIVACY_POLICY.md` e `TERMS_OF_SERVICE.md`; `../topo-walk/PRIVACY_POLICY.md`; `../pole-position/pole-position-app/PRIVACY_POLICY.md`; `../eclipse-go/docs/PRIVACY_POLICY.md`) | **texto legal** — o site publica cópia; nunca é a origem |
| `../lotto-expert/docs/ASO_METADATA.md`, `LottoExpertContent.md` (e equivalentes) | copy de produto e funcionalidades de cada app |
| `design/handoff/<data>/` (quando existir, D4) | sistema visual — prevalece sobre o que está no HTML |
| `docs/AVALIACAO.md` | direção técnica e de design do site |

**Texto legal o agente não redige.** Política e termos nascem no repositório do app; aqui o
agente espelha (`/legal <app>`), traduz para o inglês com fidelidade e atualiza a data. Mudar o
sentido de uma cláusula é decisão do humano, no repositório do app.

---

## URLs que são contrato (ADR-001)

Os apps instalados e a Play Store apontam para estes caminhos. **Nunca mudam, nem ganham
redirecionamento como substituto** — o Android App Links não segue redirect:

```
/.well-known/assetlinks.json
/lottoexpert-privacy.html          /lottoexpert-terms.html
/topowalk-privacy.html             /poleposition-privacy.html         /eclipsego-privacy.html
/lotto-expert/sweepstake-invite/lottoexpert-invite.html   (deep link do bolão; lê ?d= do link)
```

Toda mudança de stack (WP-07/08) prova com `tools/check_site.py` que esses caminhos continuam
existindo no resultado publicado.

## Produto e copy

- **Jogo responsável** nas páginas do LottoExpert: nada de "aumenta suas chances", "maximize",
  "garantia de prêmio". O app garante matemática provada (fechamento) e diz só isso.
  `tools/check_site.py` barra os termos — mesma régua do `PaywallCopyComplianceTest` do app.
- Marca **privacy-first** em todos os apps: o site segue a mesma régua (sem rastreador sem
  consentimento; D3 decide a medição).
- Português é o idioma primário. **Toda língua listada para uma página em `src/i18n/idiomas.json`
  é espelho completo, nunca parcial; língua não listada não aparece** (nem página, nem seletor,
  nem `hreflang`). pt fica na raiz e as outras em `/<código>/`, sem redirecionamento (ADR-007).
  Texto de interface e comentários em português.
- Data de "Última atualização" de uma página legal é o `lastUpdated` do `.pt.md` em
  `src/content/legal/`, igual à linha do corpo e ao repositório do app. `check_site.py` confere.

## Arquitetura

```
public/                     copiado byte a byte para dist/ pelo Astro (ADR-002 §3); lista fechada,
                            sem página — check_site.py §13 prova:
  assets/                     só URL fixa: og:image, favicons do convite, convite (PNG, sem otimização);
                              imagem exibida na página sai de src/assets/img/ (ADR-006)
  lotto-expert/sweepstake-invite/   página do convite de bolão (pako + Base64, lê o link)
  .well-known/assetlinks.json       App Links do LottoExpert
  CNAME                       domínio do Pages
docs/*.md                   README de cada app (o texto legal está em src/content/legal/)
tools/                      gen_estado.py · check_plano.py · check_site.py · regras_i18n.py (regras de
                            i18n como funções puras, que o check_site chama) + test_regras_i18n.py sobre
                            fixtures/i18n/ · sync_legal.py · lighthouse.py
design/                     brief e handoff do Claude Design (WP-06)
astro.config.mjs            Astro (ADR-002): build.format 'preserve', Sätteri com os plugins legais
tailwind.config.mjs         Tailwind 3.4.19 compilado pelo PostCSS (ADR-003); brand.* por variável CSS
src/                        assets/img/ (imagens exibidas, pelo astro:assets: WebP, width/height, lazy) ·
                            icons/fa + components/Icon.astro (SVG inline, sem Font Awesome por CDN) ·
                            layouts/ (Base.astro: head único, Inter local pela API fonts, og com width/height lidos do arquivo,
                            canonical, hreflang por língua da página + x-default (en se houver, senão pt),
                            slot jsonld, tema, faixa SugestaoIdioma no fim do <body>;
                            LegalLayout.astro: hero e card das páginas legais) · components/ (Nav,
                            Footer, SeletorIdioma: só as línguas da página, link com 2, lista com 3+;
                            SugestaoIdioma: faixa que sugere a língua do navegador, nunca navega
                            sozinha; JsonLd, uma por landing; paginas/: a página inteira com a prop
                            `lang`) · i18n/ (idiomas.json: línguas do site e de cada página — fonte
                            única, lida pelo build, check_site e sync_legal (ADR-007); idiomas.ts:
                            valida e exporta linguasDe/rota/link, com a D23 para destino sem a
                            língua; ui.ts, <pagina>.ts,
                            legal.ts, apps.ts: id, categoria e link da Play de cada app — botão e
                            JSON-LD leem dali) ·
                            content.config.ts + content/legal/<app>-<doc>.<idioma>.md (texto legal;
                            front-matter `lastUpdated: "AAAA-MM[-DD]"`, pt = .md do app byte a byte;
                            `pendente: [códigos]` no .pt.md enquanto uma tradução está atrás) ·
                            markdown/legal.mjs (plugins do Sätteri: título e data saem do corpo,
                            link do próprio site vira caminho a partir da raiz, /en/ no inglês,
                            id dos títulos pela posição — secao-2-1, igual em todas as línguas) ·
                            styles/global.css (temas por página, tipografia do texto legal) ·
                            pages/ (cascas: pt literal na raiz; [lang]/ as outras línguas do mapa
                            por getStaticPaths, nunca pt/; 404 só em pt; robots.txt.ts e
                            sitemap.xml.ts, endpoints da mesma lista de rotas do canonical — ADR-005)
dist/                       saída do build (não versionada) — é o que vai ao ar
.github/workflows/          pr.yml (checks `plano` e `site`) · deploy.yml (master → Pages por Actions)
```

Desde a fatia 8 do WP-08 nenhuma página vem da raiz: nav, footer e config mudam só no componente
(`src/components/`, `src/layouts/`), e a rede é o `check_site.py` sobre `dist/`.

---

## Ciclo de trabalho

Um item = um Work Package. Comando: **`/wp WP-NN`** (sem número, propõe o próximo da sequência).

1. pré-voo — status, dependências, decisões em aberto, achados roteados, o que só o navegador prova
2. `site-arquiteto` valida estrutura, URLs contratuais e impacto; ADR se houver decisão nova
3. `site-ux` (DESENHAR) quando o WP toca aparência: estados, componentes, referência no handoff
4. `site-dev` implementa; `site-legal` quando o WP é texto legal
5. `/verify`
6. commit; auditoria **em paralelo** sobre o diff: `site-qa` (AUDITAR) + `site-seo-perf` + `site-ux` (AUDITAR, se tocou tela)
7. `site-docs` atualiza status, `ESTADO.md`, triagem de achados e o "Onde parei" do `handoff.md`

WP `tamanho: S` + `risco: baixo` pula 2–3 — nunca em texto legal, URL contratual ou deploy.
Outros comandos: `/novo-wp <ideia>` (única entrada de trabalho novo) · `/legal <app>` (espelhar
política/termos do repositório do app) · `/decisao <texto>` · `/adr <texto>` · `/release`
(publicar `develop → master`) · `/handoff` (**toda sessão termina com ele**).

- **Escopo é contrato.** Achou problema fora do WP: linha em `achados-novos.md`, não corrige de
  passagem. Todo achado tem destino — `check_plano.py` cobra.
- **Decisão de produto não é do agente** — o que destacar na landing, stack, analytics, design.
  Opções em `decisoes.md`, e para.
- **Verificação que não rodou não passou.** O que só o navegador prova (layout, idioma, link
  de loja, compartilhamento no WhatsApp) vira checklist para o usuário; `visual: true` no WP.
- Commit `WP-NN: …`. Sem merge, push ou PR sem o usuário pedir.
- **Fluxo git `feat → develop → master`** (D5). Branch do WP nasce de `develop`; PR mira
  `develop`. `develop → master` **é deploy** — só pelo usuário, via `/release`. `main` é
  órfã (só o commit inicial) e não é usada.

## Comandos

```bash
npm ci && npm run build                                       # Astro → dist/ (Node 22.22)
python3 tools/check_site.py                                   # sobre dist/ (= --raiz dist; sem dist/, pede o build): URLs contratuais,
                                                              # links, assets, metadados, datas legais contra src/content/legal/, copy
(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)    # convite, assetlinks, og:image do convite e CNAME iguais ao publicado (D13)
python3 -B -m unittest tools/test_regras_i18n.py              # regras de i18n (ADR-007) sobre tools/fixtures/i18n/
python3 tools/gen_estado.py && python3 tools/check_plano.py   # backlog: regenerar e verificar
python3 -m http.server 8080 -d dist                           # servir dist/ para inspeção (Claude in Chrome ou usuário)
python3 tools/sync_legal.py --todos --check                    # o site está atrás do app? igual / atrás / à frente-divergente / origem ausente
python3 tools/sync_legal.py <app> [--ref REF]                 # copia o pt de um commit do app (ADR-004; nunca o en); só pelo /legal
npx html-validate 'dist/**/*.html'                            # HTML (versão do lockfile; regras em .htmlvalidate.json)
lychee --offline --no-progress --root-dir "$PWD/dist" 'dist/**/*.html'  # links internos (binário 0.24.2 do release lycheeverse/lychee)
python3 tools/lighthouse.py                                   # orçamento de bytes e Lighthouse mobile (3 runs, 9 páginas); serve dist/, precisa de Chrome
```

`.github/workflows/pr.yml` roda em todo PR e push para `develop`/`master`: job `plano`
(`gen_estado.py --check`, `check_plano.py`), job `site` (`npm ci`, `npm run build`,
`check_site.py --raiz dist`, contrato byte a byte, unittest das regras de i18n, html-validate e
lychee sobre `dist/`) e job
`lighthouse` (`tools/lighthouse.py` contra `tools/orcamento-lighthouse.json`).
`.github/workflows/deploy.yml` roda em push para `master` (e à mão): build, `check_site.py --raiz
dist` e publicação de `dist/` no Pages — só tem efeito com o Pages em modo "GitHub Actions".

## Referência rápida

| O que preciso | Onde olhar |
|---|---|
| Diagnóstico e direção | `docs/AVALIACAO.md` |
| Texto legal de um app | repositório do app, `docs/PRIVACY_POLICY.md` / `TERMS_OF_SERVICE.md` |
| Copy de produto | `../lotto-expert/docs/ASO_METADATA.md`, `docs/<APP>_README.md` |
| Dicionário i18n de uma página | `src/i18n/` (`ui.ts` nav/footer, `<pagina>.ts`, `legal.ts` hero e `<head>` das legais) |
| Cores e fonte da marca | `tailwind.config.mjs` (brand.base/surface/primary/secondary/accent, Inter) com os valores por tema em `src/styles/global.css` |
| Deep link do bolão | `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html`; formato é do app (ADR-006 lá) |
