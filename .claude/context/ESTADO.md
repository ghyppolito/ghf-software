# Estado da execução

> **Gerado por `tools/gen_estado.py`.** A fonte de verdade do status é o
> front-matter de cada WP em `wps/` — altere lá e regenere este arquivo.
> Status: `todo` · `doing` · `blocked` · `done` · `adiado`

**31 WPs** · 17 concluídos · 1 em andamento

## Sequência recomendada

Próximo WP = o primeiro da trilha A cujas dependências estejam `done`. Reordenar é decisão do usuário (`SEQUENCIA` em `tools/gen_estado.py`).

**A · LottoExpert 2.05.02 — publicar política, termos e landing antes de qualquer evolução do site**

| # | WP | Status | Nota |
|---|---|---|---|

**B · fundação — rede de segurança, build e fonte única, nesta ordem**

| # | WP | Status | Nota |
|---|---|---|---|

**C · evolução — design, SEO, performance e medição; WP-06 e WP-19 podem rodar a qualquer momento (são sessões do usuário no Claude Design)**

| # | WP | Status | Nota |
|---|---|---|---|
| 1 | [WP-30 — O site tem direção visual própria, aprovada no navegador, antes do deploy único](wps/WP-30-revisao-visual-antes-do-deploy-unico.md) | `doing` | revisão visual antes do deploy único (D33): direção + Home do estúdio → LottoExpert → propagação; pausa as fatias 7/8/9/10b do WP-10. L, visual |
| 2 | [WP-10 — A home e as landings de app seguem o sistema visual do handoff](wps/WP-10-redesign-com-o-handoff.md) | `blocked` | redesign da home e das landings de app com o handoff: hierarquia por app, anatomia única de landing, página legal legível. L, depois do WP-06 e WP-08 |
| 3 | [WP-27 — Os termos de uso do EclipseGo existem no site em pt e en, e a política aponta para o commit da main, espelhados do repositório do app](wps/WP-27-termos-de-uso-do-eclipsego-no-site.md) | `todo` | termos de uso do EclipseGo (UE, D28 B) e `origemCommit` da política apontando para a `main` do app. Pré-condição cumprida (`docs/TERMS_OF_USE.md`, app `5cd6b83`); EclipseGo ainda sem ficha na Play (D19 e). Legal, risco alto, URL nova |
| 4 | [WP-26 — Os termos de uso do TopoWalk existem no site em pt e en, espelhados do repositório do app](wps/WP-26-termos-de-uso-do-topowalk-no-site.md) | `todo` | termos de uso do TopoWalk (exigência da UE para comerciante, prazo 2027; D28 B: vai no deploy único). Pré-condição: `TERMS_OF_SERVICE.md` na `master` do app, escrito pelo humano. Legal, risco alto, URL nova |
| 5 | [WP-28 — Os termos de uso do Pole Position existem no site em pt e en, espelhados do repositório do app](wps/WP-28-termos-de-uso-do-poleposition-no-site.md) | `todo` | termos de uso do Pole Position (UE, D28 B). Pré-condição: texto na `master` do app; corrige a origem `../pole-position-app` (PP-ORIGEM-CAMINHO-01). Legal, risco alto, URL nova |
| 6 | [WP-20 — Imagens de compartilhamento 1200×630 por página e twitter:card coerente](wps/WP-20-imagens-de-compartilhamento-1200x630.md) | `todo` | imagens de compartilhamento 1200×630 (D16 A): marca para home e legais, uma por app; sessão do usuário no Claude Design, depois `twitter:card` e `og:image:alt`. M, `visual`, antes do deploy único (D13) |
| 7 | [WP-31 — O site tem páginas de conteúdo que trazem busca nova para os apps](wps/WP-31-conteudo-para-seo.md) | `todo` | conteúdo para SEO (D34): 2 páginas do LottoExpert em pt (fechamento da Lotofácil, bolão), rascunho do agente com origem e aprovação do usuário. M, visual · ⏳ depois do deploy único, `/release` próprio |
| 8 | [WP-16 — A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de](wps/WP-16-politica-do-poleposition-em-6-linguas.md) | `todo` | política do Pole Position em pt/en/es/fr/it/de, traduzida do pt de origem; pré-condição: cláusula de prevalência do pt no app (D8 b1, `PREVALENCIA-PT-NOS-APPS-01`); o espelho pt fica em dia no WP-04. Texto legal, risco alto — prova o processo na política menor |
| 9 | [WP-17 — A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru](wps/WP-17-politica-do-topowalk-em-7-linguas.md) | `todo` | política do TopoWalk em pt/en/es/fr/it/de/ru (5.842 palavras × 6 línguas além do pt); PR por língua. L, risco alto, depois do WP-16 · ⏳ aguarda WP-16 |
| 10 | [WP-18 — As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala](wps/WP-18-landings-topowalk-e-poleposition-nas-linguas-dos-apps.md) | `todo` | landings TopoWalk (7 línguas) e Pole Position (6) com copy das fichas da Play; só se D8 (a2/a3), depois do WP-10 para não traduzir duas vezes · ⏳ aguarda WP-10 |
| 11 | [WP-13 — O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade](wps/WP-13-medicao.md) | `adiado` | medição com consentimento ou sem cookie (D3: Plausible/Umami vs GA4 Consent Mode); evento de clique na Play por app. M, depois do WP-08 |
| 12 | [WP-23 — O convite do bolão abre sem terceiros (pako e Inter servidos pelo site, com `<main>`)](wps/WP-23-convite-sem-terceiros.md) | `todo` | convite sem terceiros: pako 2.1.0 (sha256 do tarball do npm) e Inter servidos ao lado do convite, `<main>`, `contrato.sha256` novo, convite entra no §15 (a)/(b) e §17 do check_site e no Lighthouse; teste com `?d=` real v1 e v2. M, risco alto (URL contratual), visual · ⏳ só depois do deploy único (D13), branch de `develop`, `/release` próprio |
| 13 | [WP-29 — A prévia do convite do bolão mostra o LottoExpert 2.06.00 em 1200×630](wps/WP-29-imagem-de-previa-do-convite-do-bolao.md) | `todo` | imagem da prévia do convite do bolão (D32: caminho novo, 1200×630, tela do bolão da 2.06.00, arte no Claude Design). M, risco alto (URL contratual), visual · ⏳ depois do deploy único e do WP-23, `/release` próprio |

## Todos os WPs

| WP | Título | Área | Tam | Risco | Visual | Depende de | ADR | Status |
|---|---|---|---|---|---|---|---|---|
| [WP-01](wps/WP-01-politica-e-termos-do-lottoexpert-2-05-02-no-site.md) | O site publica a política de privacidade e os termos de uso do LottoExpert 2.05.02 | legal | M | alto | 🖥️ | — | ADR-001 | `done` |
| [WP-02](wps/WP-02-landing-do-lottoexpert-reflete-a-2-05-02.md) | A landing do LottoExpert apresenta as funcionalidades da 2.05.02 | landing | M | medio | 🖥️ | WP-01 | — | `done` |
| [WP-03](wps/WP-03-publicar-develop-em-master.md) | O site no ar tem o LottoExpert 2.05.02 e as atualizações pendentes de TopoWalk e Pole Position | infra | S | alto | 🖥️ | WP-01, WP-02, WP-04 | ADR-001 | `done` |
| [WP-04](wps/WP-04-convite-com-og-image-e-data-do-pole-position.md) | O convite de bolão compartilha com imagem e a política do Pole Position no site é a do app | legal | S | alto | 🖥️ | — | ADR-001 | `done` |
| [WP-05](wps/WP-05-ci-no-pr.md) | Todo PR para develop roda check_site, check_plano e validação de HTML e links | infra | M | medio |  | WP-04 | — | `done` |
| [WP-06](wps/WP-06-brief-de-design-e-sessao-no-claude-design.md) | O sistema visual do site está decidido no Claude Design e exportado em design/handoff | design | M | baixo | 🖥️ | — | — | `done` |
| [WP-07](wps/WP-07-stack-com-build-spike.md) | O site tem build que preserva as URLs contratuais e publica no Pages por Actions | infra | L | alto | 🖥️ | WP-05 | ADR-001, ADR-002 | `done` |
| [WP-08](wps/WP-08-layout-e-componentes-unicos.md) | As 10 páginas usam um layout, componentes únicos e rota por idioma | landing | L | alto | 🖥️ | WP-07 | ADR-001, ADR-002, ADR-003 | `done` |
| [WP-09](wps/WP-09-legal-como-fonte-unica.md) | O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência | legal | M | alto |  | WP-08 | ADR-004 | `done` |
| [WP-10](wps/WP-10-redesign-com-o-handoff.md) | A home e as landings de app seguem o sistema visual do handoff | design | L | medio | 🖥️ | WP-06, WP-08 | ADR-001, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-009 | `blocked` |
| [WP-11](wps/WP-11-seo-tecnico.md) | Buscadores leem sitemap, canonical, hreflang e dados estruturados de cada página | seo | M | medio | 🖥️ | WP-08 | ADR-005 | `done` |
| [WP-12](wps/WP-12-performance.md) | Toda página pontua 90 ou mais nas quatro categorias do Lighthouse mobile | seo | L | medio | 🖥️ | WP-08 | ADR-006 | `done` |
| [WP-13](wps/WP-13-medicao.md) | O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade | infra | M | medio | 🖥️ | WP-08 | — | `adiado` |
| [WP-14](wps/WP-14-readme-e-arquitetura.md) | README e docs/ARQUITETURA.md descrevem a stack nova e como publicar | docs | S | baixo |  | WP-09 | — | `done` |
| [WP-15](wps/WP-15-i18n-n-linguas.md) | Cada página declara em que línguas existe e o site roteia, anuncia e verifica só essas | infra | L | alto | 🖥️ | WP-08, WP-09, WP-11 | ADR-001, ADR-002, ADR-004, ADR-005, ADR-007 | `done` |
| [WP-16](wps/WP-16-politica-do-poleposition-em-6-linguas.md) | A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de | legal | M | alto | 🖥️ | WP-15 | ADR-001 | `todo` |
| [WP-17](wps/WP-17-politica-do-topowalk-em-7-linguas.md) | A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru | legal | L | alto | 🖥️ | WP-16 | ADR-001 | `todo` |
| [WP-18](wps/WP-18-landings-topowalk-e-poleposition-nas-linguas-dos-apps.md) | As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala | landing | M | medio | 🖥️ | WP-10, WP-15 | ADR-001 | `todo` |
| [WP-19](wps/WP-19-rodada-3-do-claude-design.md) | A rodada 3 do Claude Design cobre as landings que faltam, o tablet e os defeitos da rodada 2 | design | S | baixo | 🖥️ | WP-06 | — | `done` |
| [WP-20](wps/WP-20-imagens-de-compartilhamento-1200x630.md) | Imagens de compartilhamento 1200×630 por página e twitter:card coerente | design | M | baixo | 🖥️ | WP-11 | ADR-005 | `todo` |
| [WP-21](wps/WP-21-copy-de-compartilhamento-da-ficha-da-play.md) | Title e description de compartilhamento vêm da ficha da Play | landing | M | baixo |  | WP-11 | — | `done` |
| [WP-22](wps/WP-22-acessibilidade-e-i18n-sem-redesign.md) | Acessibilidade e i18n sem redesign (a11y AA, foco, `<main>`, headings, reduced-motion, contraste fora da paleta, rótulos pt na /en/) | landing | M | medio | 🖥️ | WP-12, WP-15 | ADR-003, ADR-007 | `done` |
| [WP-23](wps/WP-23-convite-sem-terceiros.md) | O convite do bolão abre sem terceiros (pako e Inter servidos pelo site, com `<main>`) | infra | M | alto | 🖥️ | — | ADR-001, ADR-002, ADR-006 | `todo` |
| [WP-24](wps/WP-24-convite-com-o-sistema-visual-do-handoff.md) | O convite do bolão segue o sistema visual do handoff, com o parse de `?d=` intocado | design | M | alto | 🖥️ | WP-10, WP-23 | ADR-001, ADR-006, ADR-008 | `todo` |
| [WP-25](wps/WP-25-dependencias-sem-aviso-do-npm-audit.md) | O build sai do Astro 7.3.8 e o npm audit não acusa dependência vulnerável | infra | S | alto |  | WP-08 | ADR-001, ADR-002, ADR-008 | `done` |
| [WP-26](wps/WP-26-termos-de-uso-do-topowalk-no-site.md) | Os termos de uso do TopoWalk existem no site em pt e en, espelhados do repositório do app | legal | M | alto | 🖥️ | — | ADR-001, ADR-004, ADR-005, ADR-007 | `todo` |
| [WP-27](wps/WP-27-termos-de-uso-do-eclipsego-no-site.md) | Os termos de uso do EclipseGo existem no site em pt e en, e a política aponta para o commit da main, espelhados do repositório do app | legal | M | alto | 🖥️ | — | ADR-001, ADR-004, ADR-005, ADR-007 | `todo` |
| [WP-28](wps/WP-28-termos-de-uso-do-poleposition-no-site.md) | Os termos de uso do Pole Position existem no site em pt e en, espelhados do repositório do app | legal | M | alto | 🖥️ | — | ADR-001, ADR-004, ADR-005, ADR-007 | `todo` |
| [WP-29](wps/WP-29-imagem-de-previa-do-convite-do-bolao.md) | A prévia do convite do bolão mostra o LottoExpert 2.06.00 em 1200×630 | infra | M | alto | 🖥️ | — | ADR-001, ADR-002, ADR-006 | `todo` |
| [WP-30](wps/WP-30-revisao-visual-antes-do-deploy-unico.md) | O site tem direção visual própria, aprovada no navegador, antes do deploy único | design | L | medio | 🖥️ | — | ADR-001, ADR-006, ADR-007, ADR-008 | `doing` |
| [WP-31](wps/WP-31-conteudo-para-seo.md) | O site tem páginas de conteúdo que trazem busca nova para os apps | seo | M | medio | 🖥️ | — | ADR-001, ADR-005, ADR-007, ADR-009 | `todo` |

## Bloqueios ativos

| WP | Bloqueado por | Desde |
|---|---|---|
