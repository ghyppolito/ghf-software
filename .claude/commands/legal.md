---
description: Espelha política de privacidade e termos de uso de um app, do repositório do app para o site — markdown pt/en em src/content/legal/
argument-hint: app (lottoexpert | topowalk | poleposition | eclipsego) e, opcionalmente, "só privacidade" ou "só termos"
---

App: **$ARGUMENTS**

Este é o ritual que se repete a cada versão de app. A origem é um **commit** do repositório do
app (ADR-004); o site é cópia. O agente **não redige** texto legal, e nunca escreve o corpo do
`.pt.md`: quem copia é `tools/sync_legal.py`.

**De onde vem cada documento:** a tabela `ORIGENS` de `tools/sync_legal.py` (doc → repositório,
caminho **por língua**, ref padrão = branch principal do app, D14) é a verdade; esta página não a
repete. Doc novo entra em `ORIGENS` e em `LEGAL` do `check_site.py` no mesmo commit (o check exige
as duas iguais). Língua que o app publica (`<BASE>.en.md` ao lado do pt, hoje no TopoWalk) e
`ORIGENS` declara é **espelhada** pelo script, não traduzida (ADR-010); o `--check` avisa quando o
app publica um `.en.md` que `ORIGENS` não declara — achado, não mudança de passagem.

| App | Site (markdown) | Rota (Astro) |
|---|---|---|
| lottoexpert | `src/content/legal/lottoexpert-privacy.{pt,en}.md`, `lottoexpert-terms.{pt,en}.md` | `src/components/paginas/PaginaLottoExpertPrivacy.astro`, `PaginaLottoExpertTerms.astro` (cascas em `src/pages/` e `src/pages/[lang]/`) |
| topowalk | `src/content/legal/topowalk-privacy.{pt,en}.md`, `topowalk-terms.{pt,en}.md` (pt e en espelhados do app, ADR-010) | `src/components/paginas/PaginaTopoWalkPrivacy.astro`, `PaginaTopoWalkTerms.astro` (cascas em `src/pages/` e `src/pages/[lang]/`) |
| poleposition | `src/content/legal/poleposition-privacy.{pt,en}.md` | `src/components/paginas/PaginaPolePositionPrivacy.astro` (cascas em `src/pages/` e `src/pages/[lang]/`) |
| eclipsego | `src/content/legal/eclipsego-privacy.{pt,en}.md`, `eclipsego-terms.{pt,en}.md` | `src/components/paginas/PaginaEclipseGoPrivacy.astro`, `PaginaEclipseGoTerms.astro` (cascas em `src/pages/` e `src/pages/[lang]/`) |

O `.pt.md` é o corpo do `.md` do app no commit `origemCommit`, byte a byte, com o front-matter
`lastUpdated` / `origemCommit` / (`pendente: ["en", …]` enquanto alguma tradução está atrás — as
línguas da página em `src/i18n/idiomas.json` menos o pt e menos as espelhadas, ADR-007 §8); cada
tradução `.<código>.md` segue a estrutura do `.pt.md` e só tem `lastUpdated`. A língua espelhada
(ADR-010) é o corpo do `.<código>.md` do app no **mesmo** commit, byte a byte, com `lastUpdated` e o
mesmo `origemCommit` do pt. Link relativo do app para o par (`[Termos de Uso](TERMS_OF_USE.md)`,
`….en.md`) vira a página do mesmo app no build (`linksInternosLegais`, `src/markdown/legal.mjs`);
outro `.md` relativo reprova o §12. Hero, `<title>` e description ficam em
`src/i18n/legal.ts`. O HTML é gerado; não há HTML legal a editar.

1. **Há WP?** Texto legal é `risco: alto` e entra sempre por WP (`/novo-wp` se não houver).
   Sem WP aberto para este app, pare e proponha.
2. `python3 tools/sync_legal.py <app> --check` (`--doc privacy|terms` para um só).
   - **igual** ("nada a fazer"): não há o que fazer; diga e pare.
   - **atrás**: a ref tem texto novo; siga.
   - **à frente/divergente** (o `origemCommit` não é ancestral da ref): **pare e pergunte ao
     usuário** qual ref usar (`--ref <branch|tag|sha>`). Nunca `--forca` sem ele dizer.
   - **origem ausente**: o repositório do app não está em `..` (ou `$GHF_APPS_DIR`); diga e pare.
   - Aviso "hotfix legal em master não integrado": siga a seção abaixo antes.
3. `python3 tools/sync_legal.py <app> [--ref …]` — copia o pt e as línguas espelhadas do mesmo sha,
   grava `lastUpdated`, `origemCommit` e `pendente: [<línguas da página menos o pt e as
   espelhadas>]`, e imprime a ref, o sha e as seções `##` alteradas. **Recusa** (sai com 2, nada
   escrito) se a data do pt e a da língua espelhada diferem na origem: o en do app está atrás, e
   o problema volta ao app (ADR-010 §4). O aviso "pt mudou e en não" é achado para o app.
   Invoque `site-legal`: **para traduzir** cada língua de `pendente` (uma por vez), com essa saída
   e o `git diff` do `.pt.md`; **para só conferir** cada língua espelhada (estrutura, links, nome
   do documento, o que o §12 acusa), sem traduzir nem editar.
4. `/verify` — `npm run build && python3 tools/check_site.py`: com o app presente, o §4 compara o
   corpo do pt e de cada língua espelhada com `git show <origemCommit>` e falha enquanto houver
   `pendente`.
   `sync_legal.py <app> --check` tem de dizer "nada a fazer".
   Aviso "origem ausente" aqui = a comparação de texto não rodou, então não passou.
5. Diga ao usuário o que olhar no navegador: topo (data), seções alteradas, pt e en. A
   publicação é `/release`.

## Hotfix durante a integração

Enquanto `develop` não foi ao ar (deploy único, D13), `master` tem o layout antigo
(`docs/*.md` e HTML na raiz) e `develop` o novo (`src/content/legal/`). Um hotfix legal:

1. É feito em `master` como hoje: branch de `master`, PR e deploy (D13 (6)).
2. Na integração, na branch de trabalho: `git merge origin/master` (o `sync_legal.py` avisa
   "hotfix legal em master não integrado" enquanto isso não acontece).
3. O conflito modificar/apagar se resolve **mantendo a remoção**: `git rm` dos caminhos antigos
   (`docs/*POLICY*`, `docs/*TERMS*`, `*-privacy.html`, `*-terms.html` da raiz).
4. `python3 tools/sync_legal.py <app> --ref <sha do app usado no hotfix>`.
5. `site-legal` traduz o en, com o en do HTML do hotfix como base — só para doc sem en na origem;
   com en na origem, o passo 4 já o espelhou (ADR-010).
6. `check_site` verde.

Depois do deploy único, `master` tem o layout novo e o hotfix vira um `sync_legal.py` numa
branch de `master`, sem conflito.
