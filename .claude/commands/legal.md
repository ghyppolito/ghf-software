---
description: Espelha política de privacidade e termos de uso de um app, do repositório do app para o site — markdown pt/en em src/content/legal/
argument-hint: app (lottoexpert | topowalk | poleposition | eclipsego) e, opcionalmente, "só privacidade" ou "só termos"
---

App: **$ARGUMENTS**

Este é o ritual que se repete a cada versão de app. A origem é um **commit** do repositório do
app (ADR-004); o site é cópia. O agente **não redige** texto legal, e nunca escreve o corpo do
`.pt.md`: quem copia é `tools/sync_legal.py`.

**De onde vem cada documento:** a tabela `ORIGENS` de `tools/sync_legal.py` (doc → repositório,
caminho, ref padrão = branch principal do app, D14) é a verdade; esta página não a repete. Doc
novo entra em `ORIGENS` e em `LEGAL` do `check_site.py` no mesmo commit (o check exige as duas
iguais).

| App | Site (markdown) | Rota (Astro) |
|---|---|---|
| lottoexpert | `src/content/legal/lottoexpert-privacy.{pt,en}.md`, `lottoexpert-terms.{pt,en}.md` | `src/pages/lottoexpert-privacy.astro`, `src/pages/lottoexpert-terms.astro` e os pares em `src/pages/en/` |
| topowalk | `src/content/legal/topowalk-privacy.{pt,en}.md` | `src/pages/topowalk-privacy.astro`, `src/pages/en/topowalk-privacy.astro` |
| poleposition | `src/content/legal/poleposition-privacy.{pt,en}.md` | `src/pages/poleposition-privacy.astro`, `src/pages/en/poleposition-privacy.astro` |
| eclipsego | `src/content/legal/eclipsego-privacy.{pt,en}.md` | `src/pages/eclipsego-privacy.astro`, `src/pages/en/eclipsego-privacy.astro` |

O `.pt.md` é o corpo do `.md` do app no commit `origemCommit`, byte a byte, com o front-matter
`lastUpdated` / `origemCommit` / (`en: "pendente"` enquanto o en está atrás); o `.en.md` segue a
estrutura do `.pt.md` e só tem `lastUpdated`. Hero, `<title>` e description ficam em
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
3. `python3 tools/sync_legal.py <app> [--ref …]` — copia o pt, grava `lastUpdated`,
   `origemCommit` e `en: "pendente"`, e imprime a ref, o sha e as seções `##` alteradas. Invoque
   `site-legal` **só para o en**, com essa saída e o `git diff` do `.pt.md`.
4. `/verify` — `npm run build && python3 tools/check_site.py`: com o app presente, o §4 compara o
   corpo do pt com `git show <origemCommit>` e falha enquanto houver `en: "pendente"`.
   `sync_legal.py <app> --check` tem de dizer "nada a fazer".
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
5. `site-legal` traduz o en, com o en do HTML do hotfix como base.
6. `check_site` verde.

Depois do deploy único, `master` tem o layout novo e o hotfix vira um `sync_legal.py` numa
branch de `master`, sem conflito.
