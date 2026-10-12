# GHF Software — site (ghfsoftware.com) — regras do projeto

Site estático da GHF Software: landing corporativa, uma landing por app (TopoWalk, LottoExpert,
Pole Position, EclipseGo), políticas de privacidade, termos de uso e a página do convite de bolão
do LottoExpert. **Em produção**, servido pelo GitHub Pages a partir da branch `master`.

Hoje é HTML puro com Tailwind via CDN, sem build, sem teste e sem CI. A evolução dessa stack é
o backlog (ver `docs/AVALIACAO.md`). Este arquivo é curto de propósito — leia inteiro. O detalhe
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
- Português é o idioma primário; inglês é espelho completo, nunca parcial. Texto de interface
  e comentários em português.
- Data de "Última atualização" de uma página legal é a mesma do `.md` em `docs/` e do
  repositório do app. `check_site.py` confere.

## Arquitetura (estado atual — muda no WP-07/08)

```
*.html                      uma página por arquivo; nav, footer, tailwind.config e dicionário
                            i18n (data-i18n + JS) duplicados em cada uma — deriva conhecida
assets/                     imagens, favicons, mockups (PNG, sem otimização)
docs/*.md                   cópia markdown das políticas/termos e README de cada app
lotto-expert/sweepstake-invite/   página do convite de bolão (pako + Base64, lê o link)
.well-known/assetlinks.json       App Links do LottoExpert (Jekyll inclui via _config.yml)
tools/                      gen_estado.py · check_plano.py · check_site.py
design/                     brief e handoff do Claude Design (WP-06)
```

Enquanto não há build: alteração em nav/footer/config **se replica nas 10 páginas** no mesmo
WP, e o `check_site.py` é a única rede. Depois do WP-08, há um layout único.

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
python3 tools/check_site.py                                   # links, assets, metadados, datas legais, copy — roda sempre
python3 tools/gen_estado.py && python3 tools/check_plano.py   # backlog: regenerar e verificar
python3 -m http.server 8080                                   # servir local para inspeção (Claude in Chrome ou usuário)
diff ../lotto-expert/docs/PRIVACY_POLICY.md docs/LOTTOEXPERT_PRIVACY_POLICY.md   # o site está atrás do app?
```

Depois do WP-05 há CI no PR; depois do WP-07 há `npm run build` — atualize esta seção no WP.

## Referência rápida

| O que preciso | Onde olhar |
|---|---|
| Diagnóstico e direção | `docs/AVALIACAO.md` |
| Texto legal de um app | repositório do app, `docs/PRIVACY_POLICY.md` / `TERMS_OF_SERVICE.md` |
| Copy de produto | `../lotto-expert/docs/ASO_METADATA.md`, `docs/<APP>_README.md` |
| Dicionário i18n de uma página | bloco `<script>` no fim do próprio HTML (`translations`/`data-i18n`) |
| Cores e fonte da marca | `tailwind.config` inline em `index.html` (brand.base/surface/primary/secondary/accent, Inter) |
| Deep link do bolão | `lotto-expert/sweepstake-invite/lottoexpert-invite.html`; formato é do app (ADR-006 lá) |
