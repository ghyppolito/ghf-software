---
id: WP-18
titulo: As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala
area: landing
status: todo
depende_de: [WP-10, WP-15]
adr: [ADR-001]
spec: ""
decisoes: [D8]
tamanho: M
risco: medio
visual: true
branch: feat/wp-18-landings-n-linguas
---

# WP-18 — As landings do TopoWalk e do Pole Position existem nas línguas que cada app fala

**Depende de:** WP-10 (redesign — senão traduz duas vezes), WP-15 · **Achados roteados:** —

**Objetivo:** `topowalk.html` em pt, en, es, fr, it, de, ru e `poleposition.html` em pt, en,
es, fr, it, de, com copy vinda da ficha da Play de cada língua; mapa de `idiomas.json` atualizado.
**Só existe se D8 (a) for (a2) ou (a3)** — com (a1), este WP vira `adiado`.

**Contexto:** D8. Fonte da copy, com origem rastreável por língua:
`../topo-walk/docs/store_listing_texts.md` (pt-BR `:64`, en `:120`, es `:176`, fr `:233`,
de `:290`, it `:349`, ru `:406`) e `../pole-position/pole-position-app/docs/aso_plan.md` §4
(4.2 en, 4.3 pt-BR, 4.4 es, …). Hoje as landings são pt/en por JS com 67
(`topowalk.html`) e 103 (`poleposition.html`) ocorrências de `data-i18n`.

**Ler antes:** D8; WP-10 (anatomia de landing); as seções acima das duas fichas; WP-15.

**Arquivos-alvo:** `src/pages/{es,fr,it,de,ru}/topowalk.astro` (ou a forma de conteúdo que o
WP-10 deixar), `src/pages/{es,fr,it,de}/poleposition.astro`, `src/content/landing/**` se o
WP-10 criar, `src/i18n/idiomas.json` (só as duas entradas), `src/i18n/ui.ts` (rótulos de seção
nas línguas novas), `public/assets/{topowalk,poleposition}/**` (capturas localizadas, se houver).

**Passos:**
1. Mapear cada seção da anatomia do WP-10 para o trecho da ficha da Play daquela língua;
   texto sem correspondente na ficha é traduzido do pt e marcado no WP (lista).
2. Capturas: usar as da ficha da Play da língua se existirem; senão as do en.
3. Link da Play com `&hl=<lang>`.

**Critérios de aceite:**
- `python3 tools/check_site.py --raiz dist` verde; `dist/<lang>/topowalk.html` para as 5 línguas
  novas e `dist/<lang>/poleposition.html` para as 4.
- Mesmo número de `<section` em todas as versões de uma landing (`grep -c "<section"`).
- Nenhuma página em `dist/{es,fr,it,de,ru}/` além das listadas (sem home, LottoExpert, EclipseGo).
- Lista no WP: cada frase sem origem na ficha da Play, com a língua.

**Só no navegador:** as 11 versões novas em 360/768/1280: textos sem estouro (de e ru são
mais longos), seletor, link da Play abre na língua. O usuário reporta.

**Risco:** médio — copy de produto, não legal. Específico: texto alemão/russo quebrando o
layout do redesign; claim da ficha da Play que o site não pode fazer sem a captura correspondente.
