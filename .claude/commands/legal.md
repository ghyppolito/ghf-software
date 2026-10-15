---
description: Espelha política de privacidade e termos de uso de um app, do repositório do app para o site — markdown pt/en em src/content/legal/
argument-hint: app (lottoexpert | topowalk | poleposition | eclipsego) e, opcionalmente, "só privacidade" ou "só termos"
---

App: **$ARGUMENTS**

Este é o ritual que se repete a cada versão de app. A origem é o repositório do app; o site
é cópia. O agente **não redige** texto legal.

| App | Origem | Site (markdown) | Rota (Astro) |
|---|---|---|---|
| lottoexpert | `../lotto-expert/docs/PRIVACY_POLICY.md`, `TERMS_OF_SERVICE.md` | `src/content/legal/lottoexpert-privacy.pt.md` e `.en.md`, `src/content/legal/lottoexpert-terms.pt.md` e `.en.md` | `src/pages/lottoexpert-privacy.astro`, `src/pages/lottoexpert-terms.astro` e os pares em `src/pages/en/` |
| topowalk | `../topo-walk/PRIVACY_POLICY.md` | `src/content/legal/topowalk-privacy.pt.md` e `.en.md` | `src/pages/topowalk-privacy.astro`, `src/pages/en/topowalk-privacy.astro` |
| poleposition | `../pole-position/pole-position-app/PRIVACY_POLICY.md` | `src/content/legal/poleposition-privacy.pt.md` e `.en.md` | `src/pages/poleposition-privacy.astro`, `src/pages/en/poleposition-privacy.astro` |
| eclipsego | `../eclipse-go/docs/PRIVACY_POLICY.md` | `src/content/legal/eclipsego-privacy.pt.md` e `.en.md` | `src/pages/eclipsego-privacy.astro`, `src/pages/en/eclipsego-privacy.astro` |

O `.pt.md` é o `.md` do app byte a byte com um front-matter
`lastUpdated: "AAAA-MM[-DD]"` na frente; o `.en.md` segue a estrutura do `.pt.md`. Hero, `<title>`
e description ficam em `src/i18n/legal.ts`. O HTML é gerado; não há HTML legal a editar.

(Caminhos conferidos em 2026-10-15. Se um não existir, procure por `**Última atualização` no repositório do app e corrija a tabela.)

1. **Há WP?** Texto legal é `risco: alto` e entra sempre por WP (`/novo-wp` se não houver).
   Sem WP aberto para este app, pare e proponha.
2. `diff <(sed '1,/^---$/d' src/content/legal/<app>-<doc>.pt.md) ../<origem>` (o `sed` tira o
   front-matter) — se vazio, não há o que fazer; diga e pare.
3. Invoque `site-legal` com o diff. Ele atualiza o markdown pt e en e a data, e relata seção a seção.
4. `/verify` — `npm run build && python3 tools/check_site.py` (datas, estrutura pt/en) e o `diff`
   do passo 2 (espelho) verdes.
5. Diga ao usuário o que olhar no navegador: topo (data), seções alteradas, pt e en. A
   publicação é `/release`.
