---
id: WP-17
titulo: A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru
area: legal
status: todo
depende_de: [WP-16]
adr: [ADR-001]
spec: ""
decisoes: [D7, D8]
tamanho: L
risco: alto
visual: true
branch: feat/wp-17-legal-topowalk-7-linguas
---

# WP-17 — A política de privacidade do TopoWalk existe no site em pt, en, es, fr, it, de e ru

**Depende de:** WP-16 (processo provado na política menor) · **Achados roteados:** —

**Objetivo:** `/topowalk-privacy.html` (pt, URL contratual intocada) e `/en/`, `/es/`,
`/fr/`, `/it/`, `/de/`, `/ru/topowalk-privacy.html` com o mesmo texto, data e seções,
espelhando `../topo-walk/PRIVACY_POLICY.md`; o mapa de `idiomas.json` lista as 7.

**Contexto:** D8. O app fala `values-{pt-rBR,de,es,fr,it,ru}` com inglês padrão
(`../topo-walk/app/src/main/res/values/strings.xml:5`); a ficha da Play nas 7 línguas está em
`../topo-walk/docs/store_listing_texts.md:64–406`. Origem só em pt: 5.842 palavras, 13 `##`,
31 `###` (`../topo-walk/PRIVACY_POLICY.md:9–379`). Hoje o espelho está em dia:
`diff <(sed '1,/^---$/d' src/content/legal/topowalk-privacy.pt.md) ../topo-walk/PRIVACY_POLICY.md` vazio (2026-10-12).
Tamanho L pelo volume (~29 mil palavras traduzidas); se passar de uma sessão, PR por língua —
cada PR só entra no mapa de `idiomas.json` a língua que está completa.

**Ler antes:** `.claude/commands/legal.md`; `.claude/agents/site-legal.md`; D7 e D8; o relato
de revisão do WP-16 (o que o usuário corrigiu vira regra aqui); `../topo-walk/PRIVACY_POLICY.md` inteiro.

**Arquivos-alvo:** `src/content/legal/topowalk.{pt,en,es,fr,it,de,ru}.md`,
`src/content/legal/topowalk-privacy.pt.md`, `src/i18n/idiomas.json` (só a entrada `topowalk-privacy`).
Fora do site, antes: cláusula de prevalência no `PRIVACY_POLICY.md` do TopoWalk, se D8 (b1).

**Passos:** os do WP-16, com ru a mais. ru: nomes de SDK e de produto em latim, sem transliterar
(`Firebase`, `Google Play`, `TopoWalk Pro`, `topowalk_pro`).

**Critérios de aceite:**
- `diff <(sed '1,/^---$/d' src/content/legal/topowalk-privacy.pt.md) ../topo-walk/PRIVACY_POLICY.md` vazio.
- `python3 tools/check_site.py --raiz dist` verde — mesma data nas 7, 13 `##` e 31 `###` em
  todas, `` `topowalk_pro` `` e cada permissão com a mesma contagem do pt, `Firebase Analytics`,
  `Firebase Crashlytics`, `Google Play Billing` presentes em todas.
- `for l in en es fr it de ru; do test -f dist/$l/topowalk-privacy.html; done` sem falha;
  `dist/topowalk-privacy.html` em pt.
- `grep -c 'hreflang' dist/topowalk-privacy.html` = 8.
- `grep -c "[А-Яа-я]" dist/ru/topowalk-privacy.html` > 0 e `grep -c "[А-Яа-я]"` nas outras 6 = 0
  (cirílico só no ru; pega cópia trocada).

**Só no navegador:** as 7 versões em 360 e 1280: data, sumário com 13 entradas, tabelas e
blocos de permissão legíveis, cirílico renderizado com a fonte da marca (Inter tem cirílico —
conferir que não cai em fallback), seletor com as 7. O usuário reporta e registra o que revisou.

**Irreversível:** o mesmo do WP-16. ru e de dificilmente terão revisão humana do usuário — a
cláusula de prevalência é o que limita o dano.

**Risco:** alto — volume e duas línguas sem revisor. Específico: seção 2 (`:17–144`, 127
linhas de dados acessados) traduzida com omissão; o check de `###` e de tokens pega omissão de
bloco, não de frase.
