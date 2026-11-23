---
id: WP-13
titulo: O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade
area: infra
status: adiado
depende_de: [WP-08]
adr: []
spec: docs/AVALIACAO.md
decisoes: [D3]
tamanho: M
risco: medio
visual: true
branch: feat/wp-13-medicao
---

# WP-13 — O site mede visitas, origem e cliques na Play sem ferir a régua de privacidade

> **Congelado (2026-11-22, D3):** o usuário decidiu não medir — "não é previsto custos no site no momento" — e
> "deixa o item congelado para futura análise". O WP fica `adiado`, não cancelado; não sai do lugar sem o
> usuário reabrir a D3. Reabrir com (A) ou (B) exige revisar o ADR-006 §5 e a regra de terceiros de
> `tools/lighthouse.py`.

**Depende de:** WP-08 · **Achados roteados:** —

**Objetivo:** conforme D3: script de medição em `Base.astro`, evento `play_click` com o
`app` como parâmetro em todo botão da Play, e — se GA4 — banner de consentimento com Consent
Mode v2 e nada disparado antes do aceite. Política de privacidade **do site** publicada
(`/privacy.html`, pt e en) dizendo o que se mede.

**Contexto:** `docs/AVALIACAO.md` §2 item 8 e §3.4. Nada é medido hoje.

**Ler antes:** D3; `docs/AVALIACAO.md` §3.4; documentação da ferramenta escolhida (só a
página de instalação e a de eventos).

**Arquivos-alvo:** `src/layouts/Base.astro`, `src/components/PlayButton.astro`,
`src/components/Consent.astro` (se GA4), `src/pages/privacy.astro` e `en/privacy.astro`,
`tools/check_site.py` (`/privacy.html` entra nas páginas obrigatórias).

**Critérios de aceite:**
- Sem consentimento (se GA4): nenhuma requisição ao domínio do coletor (aba Rede, relato do usuário ou Claude in Chrome).
- Clique em qualquer botão da Play emite `play_click` com `app` ∈ {topowalk, lottoexpert, poleposition, eclipsego}
  — visto no painel da ferramenta (captura).
- `/privacy.html` existe em pt e en e é linkada no footer.
- `check_site.py` verde.

**Só no navegador:** banner (se houver) em 360 px; evento no painel.

**Risco:** médio — LGPD. Plausible/Umami sem cookie dispensa banner; GA4 não.
