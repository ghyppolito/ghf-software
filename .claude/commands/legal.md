---
description: Espelha política de privacidade e termos de uso de um app, do repositório do app para o site — docs/*.md e HTML pt/en
argument-hint: app (lottoexpert | topowalk | poleposition | eclipsego) e, opcionalmente, "só privacidade" ou "só termos"
---

App: **$ARGUMENTS**

Este é o ritual que se repete a cada versão de app. A origem é o repositório do app; o site
é cópia. O agente **não redige** texto legal.

| App | Origem | Site (md) | Site (html) |
|---|---|---|---|
| lottoexpert | `../lotto-expert/docs/PRIVACY_POLICY.md`, `TERMS_OF_SERVICE.md` | `docs/LOTTOEXPERT_PRIVACY_POLICY.md`, `docs/LOTTOEXPERT_TERMS_OF_SERVICE.md` | `lottoexpert-privacy.html`, `lottoexpert-terms.html` |
| topowalk | `../topo-walk/PRIVACY_POLICY.md` | `docs/TOPOWALK_PRIVACY_POLICY.md` | `topowalk-privacy.html` |
| poleposition | `../pole-position/pole-position-app/PRIVACY_POLICY.md` | `docs/POLEPOSITION_PRIVACY_POLICY.md` | `poleposition-privacy.html` |
| eclipsego | `../eclipse-go/docs/PRIVACY_POLICY.md` | `src/content/legal/eclipsego-privacy.pt.md` e `.en.md` (front-matter `lastUpdated`; espelho: `diff <(sed '1,/^---$/d' src/content/legal/eclipsego-privacy.pt.md) ../eclipse-go/docs/PRIVACY_POLICY.md`) | `src/pages/eclipsego-privacy.astro`, `src/pages/en/eclipsego-privacy.astro` |

(Caminhos conferidos em 2026-10-12. Se um não existir, procure por `**Última atualização` no repositório do app e corrija a tabela.)

1. **Há WP?** Texto legal é `risco: alto` e entra sempre por WP (`/novo-wp` se não houver).
   Sem WP aberto para este app, pare e proponha.
2. `diff ../<origem> docs/<destino>.md` — se vazio, não há o que fazer; diga e pare.
3. Invoque `site-legal` com o diff. Ele atualiza md, HTML pt, HTML en e a data, e relata
   seção a seção.
4. `/verify` — `check_site.py` (datas) e `diff -q` (espelho) verdes.
5. Diga ao usuário o que olhar no navegador: topo (data), seções alteradas, pt e en. A
   publicação é `/release`.
