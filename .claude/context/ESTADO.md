# Estado da execução

> **Gerado por `tools/gen_estado.py`.** A fonte de verdade do status é o
> front-matter de cada WP em `wps/` — altere lá e regenere este arquivo.
> Status: `todo` · `doing` · `blocked` · `done` · `adiado`

**19 WPs** · 6 concluídos · 1 em andamento

## Sequência recomendada

Próximo WP = o primeiro da trilha A cujas dependências estejam `done`. Reordenar é decisão do usuário (`SEQUENCIA` em `tools/gen_estado.py`).

**A · LottoExpert 2.05.02 — publicar política, termos e landing antes de qualquer evolução do site**

| # | WP | Status | Nota |
|---|---|---|---|

**B · fundação — rede de segurança, build e fonte única, nesta ordem**

| # | WP | Status | Nota |
|---|---|---|---|
| 1 | [WP-07 — O site tem build que preserva as URLs contratuais e publica no Pages por Actions](wps/WP-07-stack-com-build-spike.md) | `blocked` | stack com build (D2, recomendada Astro): spike que prova URLs contratuais preservadas, `.well-known` e convite intactos, deploy do Pages por Actions; ADR-002. L, risco alto |
| 2 | [WP-08 — As 10 páginas usam um layout, componentes únicos e rota por idioma](wps/WP-08-layout-e-componentes-unicos.md) | `doing` | migração das 10 páginas para layout e componentes únicos (nav, footer, tema, i18n por rota `/en/`); conteúdo legal em markdown renderizado. L, depois do WP-07 · ⏳ aguarda WP-07 |
| 3 | [WP-09 — O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência](wps/WP-09-legal-como-fonte-unica.md) | `todo` | legal como fonte única: `tools/sync_legal.py` importa do repositório do app, data no front-matter, CI acusa divergência. M, depois do WP-08 · ⏳ aguarda WP-08 |
| 4 | [WP-14 — README e docs/ARQUITETURA.md descrevem a stack nova e como publicar](wps/WP-14-readme-e-arquitetura.md) | `todo` | README e `docs/ARQUITETURA.md` refletem a stack nova; `CLAUDE.md` seção Comandos atualizada. S, fecha a trilha B · ⏳ aguarda WP-09 |

**C · evolução — design, SEO, performance e medição; WP-06 e WP-19 podem rodar a qualquer momento (são sessões do usuário no Claude Design)**

| # | WP | Status | Nota |
|---|---|---|---|
| 1 | [WP-19 — A rodada 3 do Claude Design cobre as landings que faltam, o tablet e os defeitos da rodada 2](wps/WP-19-rodada-3-do-claude-design.md) | `todo` | rodada 3 do Claude Design: landings TopoWalk, Pole Position e EclipseGo, tablet 768, card em breve, troca de idioma na legal, defeitos da rodada 2. S, sessão do usuário; em paralelo à trilha B, antes do WP-10 |
| 2 | [WP-10 — A home e as landings de app seguem o sistema visual do handoff](wps/WP-10-redesign-com-o-handoff.md) | `todo` | redesign da home e das landings de app com o handoff: hierarquia por app, anatomia única de landing, página legal legível. L, depois do WP-06 e WP-08 · ⏳ aguarda WP-08 |
| 3 | [WP-11 — Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página](wps/WP-11-seo-tecnico.md) | `todo` | SEO técnico: sitemap, robots, canonical, hreflang pt/en, JSON-LD (Organization, MobileApplication), OG por página. M, depois do WP-08 · ⏳ aguarda WP-08 |
| 4 | [WP-15 — Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas](wps/WP-15-i18n-n-linguas.md) | `todo` | i18n N-línguas: mapa único página → línguas (`src/i18n/idiomas.ts`), pt na raiz e demais em `/<lang>/`, seletor só com as línguas da página, hreflang/x-default das existentes, check_site compara data, seções e tokens entre versões legais; não publica língua nova. D8, ADR-003. M, risco alto, depois do WP-11 · ⏳ aguarda WP-08, WP-09, WP-11 |
| 5 | [WP-16 — A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de](wps/WP-16-politica-do-poleposition-em-6-linguas.md) | `todo` | política do Pole Position em pt/en/es/fr/it/de, traduzida do pt de origem; pré-condição: cláusula de prevalência do pt no app (D8 b1, `PREVALENCIA-PT-NOS-APPS-01`); o espelho pt fica em dia no WP-04. Texto legal, risco alto — prova o processo na política menor · ⏳ aguarda WP-15 |
| 6 | [WP-17 — A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru](wps/WP-17-politica-do-topowalk-em-7-linguas.md) | `todo` | política do TopoWalk em pt/en/es/fr/it/de/ru (5.842 palavras × 6 línguas além do pt); PR por língua. L, risco alto, depois do WP-16 · ⏳ aguarda WP-16 |
| 7 | [WP-18 — As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala](wps/WP-18-landings-topowalk-e-poleposition-nas-linguas-dos-apps.md) | `todo` | landings TopoWalk (7 línguas) e Pole Position (6) com copy das fichas da Play; só se D8 (a2/a3), depois do WP-10 para não traduzir duas vezes · ⏳ aguarda WP-10, WP-15 |
| 8 | [WP-12 — Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile](wps/WP-12-performance.md) | `todo` | performance: fontes self-hosted, ícones SVG inline no lugar do Font Awesome, imagens WebP/AVIF com dimensões, Lighthouse ≥ 90 nas 4 categorias em todas as páginas. M, depois do WP-08 · ⏳ aguarda WP-08 |
| 9 | [WP-13 — O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade](wps/WP-13-medicao.md) | `todo` | medição com consentimento ou sem cookie (D3: Plausible/Umami vs GA4 Consent Mode); evento de clique na Play por app. M, depois do WP-08 · ⏳ aguarda WP-08 |

## Todos os WPs

| WP | Título | Área | Tam | Risco | Visual | Depende de | ADR | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-01](wps/WP-01-politica-e-termos-do-lottoexpert-2-05-02-no-site.md) | O site publica a política de privacidade e os termos de uso do LottoExpert 2.05.02 | legal | M | alto | 🖥️ | — | ADR-001 | `done` |
| [WP-02](wps/WP-02-landing-do-lottoexpert-reflete-a-2-05-02.md) | A landing do LottoExpert apresenta as funcionalidades da 2.05.02 | landing | M | medio | 🖥️ | WP-01 | — | `done` |
| [WP-03](wps/WP-03-publicar-develop-em-master.md) | O site no ar tem o LottoExpert 2.05.02 e as atualizações pendentes de TopoWalk e Pole Position | infra | S | alto | 🖥️ | WP-01, WP-02, WP-04 | ADR-001 | `done` |
| [WP-04](wps/WP-04-convite-com-og-image-e-data-do-pole-position.md) | O convite de bolão compartilha com imagem e a política do Pole Position no site é a do app | legal | S | alto | 🖥️ | — | ADR-001 | `done` |
| [WP-05](wps/WP-05-ci-no-pr.md) | Todo PR para develop roda check_site, check_plano e validação de HTML e links | infra | M | medio |  | WP-04 | — | `done` |
| [WP-06](wps/WP-06-brief-de-design-e-sessao-no-claude-design.md) | O sistema visual do site está decidido no Claude Design e exportado em design/handoff | design | M | baixo | 🖥️ | — | — | `done` |
| [WP-07](wps/WP-07-stack-com-build-spike.md) | O site tem build que preserva as URLs contratuais e publica no Pages por Actions | infra | L | alto | 🖥️ | WP-05 | ADR-001, ADR-002 | `blocked` |
| [WP-08](wps/WP-08-layout-e-componentes-unicos.md) | As 10 páginas usam um layout, componentes únicos e rota por idioma | landing | L | alto | 🖥️ | WP-07 | ADR-001, ADR-002, ADR-003 | `doing` |
| [WP-09](wps/WP-09-legal-como-fonte-unica.md) | O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência | legal | M | medio |  | WP-08 | — | `todo` |
| [WP-10](wps/WP-10-redesign-com-o-handoff.md) | A home e as landings de app seguem o sistema visual do handoff | design | L | medio | 🖥️ | WP-06, WP-08 | — | `todo` |
| [WP-11](wps/WP-11-seo-tecnico.md) | Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página | seo | M | baixo |  | WP-08 | — | `todo` |
| [WP-12](wps/WP-12-performance.md) | Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile | seo | M | baixo | 🖥️ | WP-08 | — | `todo` |
| [WP-13](wps/WP-13-medicao.md) | O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade | infra | M | medio | 🖥️ | WP-08 | — | `todo` |
| [WP-14](wps/WP-14-readme-e-arquitetura.md) | README e docs/ARQUITETURA.md descrevem a stack nova e como publicar | docs | S | baixo |  | WP-09 | — | `todo` |
| [WP-15](wps/WP-15-i18n-n-linguas.md) | Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas | infra | M | alto | 🖥️ | WP-08, WP-09, WP-11 | ADR-001 | `todo` |
| [WP-16](wps/WP-16-politica-do-poleposition-em-6-linguas.md) | A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de | legal | M | alto | 🖥️ | WP-15 | ADR-001 | `todo` |
| [WP-17](wps/WP-17-politica-do-topowalk-em-7-linguas.md) | A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru | legal | L | alto | 🖥️ | WP-16 | ADR-001 | `todo` |
| [WP-18](wps/WP-18-landings-topowalk-e-poleposition-nas-linguas-dos-apps.md) | As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala | landing | M | medio | 🖥️ | WP-10, WP-15 | ADR-001 | `todo` |
| [WP-19](wps/WP-19-rodada-3-do-claude-design.md) | A rodada 3 do Claude Design cobre as landings que faltam, o tablet e os defeitos da rodada 2 | design | S | baixo | 🖥️ | WP-06 | — | `todo` |

## Bloqueios ativos

| WP | Bloqueado por | Desde |
|---|---|---|
| WP-07 | implementado e auditado; falta o usuário: CI no PR, /release, trocar o Pages para Actions + variável PAGES_VIA_ACTIONS, curls e checklist de navegador | 2026-10-13 |
