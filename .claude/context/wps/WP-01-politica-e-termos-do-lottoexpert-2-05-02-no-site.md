---
id: WP-01
titulo: O site publica a política de privacidade e os termos de uso do LottoExpert 2.05.02
area: legal
status: doing
depende_de: []
adr: [ADR-001]
spec: ""
decisoes: [D7]
tamanho: M
risco: alto
visual: true
branch: feat/wp-01-legal-lottoexpert-2-05-02
---

# WP-01 — O site publica a política de privacidade e os termos de uso do LottoExpert 2.05.02

**Depende de:** — · **Achados roteados:** —

**Objetivo:** `lottoexpert-privacy.html` e `lottoexpert-terms.html` (pt e en) e os `.md` em
`docs/` dizem o que `../lotto-expert/docs/PRIVACY_POLICY.md` e `TERMS_OF_SERVICE.md` dizem na
versão de 12 de outubro de 2026.

**Contexto:** o app 2.05.02 está em promoção para produção e aponta para
`ghfsoftware.com/lottoexpert-privacy.html`; o site está em 23/07/2026. O handoff do app
(`../lotto-expert/.claude/context/handoff.md` §2) registra que a cópia web "precisa ser
atualizada pelo usuário". Diff medido no setup (`diff ../lotto-expert/docs/… docs/…`):

| Documento | O que mudou |
|---|---|
| Privacidade | data; nota sobre nomes em bolões (imagem de prestação de contas); eventos novos de analytics (`contests_view_opened`, `performance_viewed`, `monthly_report_opened`, `content_shared`, `widget_added`, `review_prompt_shown`, `paywall_dismissed`, `premium_welcome_shown`); finalidade do compartilhamento inclui imagem; parágrafo **Prestação de contas** (§4.8); parágrafo **Restauração** (§4.9: não sobrescreve, não reativa analytics) |
| Termos | título e nome **"Termos de Uso"** (era "Termos de Serviço"; referências ao Google ficam); data; §1 inclui Teimosinha e prestação de contas; §4 espelho premium de **14 dias**; §6 prestação de contas é informativa e nomes exigem consentimento ou desligar; §7 inclui **Gson**; §9 e §12 renomeados |

**Ler antes:** só o diff acima (não os documentos inteiros); `CLAUDE.md` § "Fontes de verdade";
`.claude/agents/site-legal.md`.

**Arquivos-alvo:**
- `docs/LOTTOEXPERT_PRIVACY_POLICY.md`, `docs/LOTTOEXPERT_TERMS_OF_SERVICE.md` (cópia idêntica)
- `lottoexpert-privacy.html`, `lottoexpert-terms.html` (pt e en, inclusive dicionário i18n)
- Lista fechada (verificada pelo `site-arquiteto` com grep): **só os 4 arquivos acima**.
  - `lottoexpert-terms.html`: renomear "Termos de Serviço" → "Termos de Uso" em `<title>` (l.7),
    `<meta description>` (l.9), `<h1>` (l.137), `page_title` pt (l.240), §9 (l.350), contato
    (l.363); en "Terms of Service" → "Terms of Use" em `page_title` (l.370), §9 (l.480), contato
    (l.493). **Não mudam:** l.342 "Termos de Serviço do Google" e l.472 "Google Terms of Service".
  - `lottoexpert-privacy.html`: as 4 ocorrências pt (l.312/322/361/369) e 4 en (l.581/591/630/638)
    são termos do Google Play/Drive e **não mudam** (a origem também as mantém).
  - Footers das 10 páginas usam o rótulo neutro "Termos - LottoExpert" / "Terms - LottoExpert"
    (`footer_terms_lotto`) — **não mudam**; nenhuma outra página exibe "Termos de Serviço"
    apontando para `lottoexpert-terms.html`. `README.md` já diz "Termos de Uso".
  - `poleposition-privacy.html` e `topowalk-privacy.html` referem-se a termos do Google/Firebase
    e **não mudam**.

**Passos:**
1. `cp` dos dois `.md` da origem; `diff -q` vazio.
2. `site-legal`: HTML pt, seção a seção do diff; renomear "Termos de Serviço" → "Termos de Uso"
   em `<title>`, `<h1>`, nav, footer, dicionário i18n e links das páginas do LottoExpert.
3. `site-legal`: HTML en, tradução fiel dos mesmos trechos ("Terms of Use").
4. Data: "Última atualização: 12 de Outubro de 2026" / "Last updated: October 12, 2026" nos
   dois HTML (estático e dicionário).
5. `/verify`.

**Critérios de aceite:**
- `diff -q ../lotto-expert/docs/PRIVACY_POLICY.md docs/LOTTOEXPERT_PRIVACY_POLICY.md` e o dos
  termos sem saída.
- `python3 tools/check_site.py` sem erro de data nas duas páginas.
- `grep -c "12 de Outubro de 2026" lottoexpert-privacy.html lottoexpert-terms.html` ≥ 2 em cada;
  `grep -c "October 12, 2026"` ≥ 1 em cada; `grep -c "23 de Julho" lottoexpert-*.html` = 0.
- `grep -n "Termos de Serviço" lottoexpert-privacy.html lottoexpert-terms.html` só retorna
  linhas com "Google"; `grep -n "Terms of Service" lottoexpert-privacy.html lottoexpert-terms.html`
  idem; `grep -c "Termos de Uso" lottoexpert-terms.html` ≥ 5 e `grep -c "Terms of Use"` ≥ 3.
- `grep -c "Teimosinha" lottoexpert-terms.html` ≥ 2 (pt e en); `grep -ci "prestação de contas\|settlement" lottoexpert-privacy.html` ≥ 2;
  `grep -c "14 dias\|14 days" lottoexpert-terms.html` ≥ 2; `grep -c "Gson" lottoexpert-terms.html` ≥ 2.
- Nenhum arquivo fora de Arquivos-alvo no `git diff --stat develop...HEAD`, exceto a escrituração em `.claude/context/` (status do WP, `ESTADO.md`, achados).

**Só no navegador:** `python3 -m http.server 8080`; abrir as duas páginas em 360 px e 1280 px,
pt e en: data no topo, §4.8/§4.9 da privacidade, §1/§4/§6/§7 dos termos legíveis e sem
parágrafo cortado; troca de idioma mantém o conteúdo correspondente. O usuário reporta.

**Irreversível:** o texto vai ao ar no `/release` (WP-03) e é o que a Play e o app apontam.
Nada muda de caminho (ADR-001).

**Risco:** alto — texto legal. Erro típico: traduzir só parte, esquecer a data no dicionário
i18n, renomear "Termos de Serviço do Google". `check_site.py` e os `grep` acima são a rede.
