---
id: WP-06
titulo: O sistema visual do site está decidido no Claude Design e exportado em design/handoff
area: design
status: done
depende_de: []
adr: []
spec: docs/AVALIACAO.md
decisoes: [D4]
tamanho: M
risco: baixo
visual: true
branch: feat/wp-06-brief-de-design
---

# WP-06 — O sistema visual do site está decidido no Claude Design e exportado em design/handoff

**Depende de:** — (pode rodar em paralelo à trilha B) · **Achados roteados:** DESIGN-PUBLICO-JEKYLL-01 (WP-07), LOGO-ANO-E-FUNDO-ESCURO-01 e DESIGN-RODADA-3-01 (WP-10)

**Objetivo:** existe `design/BRIEF.md` escrito pelo agente e `design/handoff/<data>/` com o
export da sessão do usuário no Claude Design: tokens (cor semântica, tipografia, espaçamento,
raio), nav, footer, hero, card de app, bloco de feature, página legal, estados.

**Contexto:** `docs/AVALIACAO.md` §2 item 7 e §3.3. Hoje a paleta e a tipografia foram
decididas inline por geração de código; não há hierarquia entre os 4 produtos. O FORMA usou o
mesmo caminho (brief → Claude Design → handoff → `forma-ux` audita).

**Ler antes:** `docs/AVALIACAO.md` §3.3 inteiro; `index.html:43-70` (tokens atuais);
`../forma/docs/FORMA_Design_Brief.md` §3 e §5 como modelo de brief (só a estrutura).

**Arquivos-alvo:** `design/BRIEF.md`; `design/handoff/<data>/` (export, pelo usuário);
`design/README.md` (atualizar o caminho do handoff).

**Passos:**
1. `site-ux` escreve o brief: marca (GHF Software, "soluções de engenharia, privacy-first"),
   os 4 produtos com público e cor de identidade de cada (favicons/mockups em `assets/`),
   hierarquia da home (um toque até o app certo), anatomia única de landing, página legal
   legível, tokens que já existem e o que preservar (logo, mockups), restrições (Pages
   estático, sem JS de framework, AA).
2. **Usuário:** sessão no Claude Design com o brief; export para `design/handoff/<data>/`.
3. `site-ux` lê o export e escreve em `design/README.md` o mapa (onde está cada componente)
   e o que o export **não** cobre.

**Critérios de aceite:**
- `design/BRIEF.md` existe e cobre as 7 seções do passo 1 (`grep -c "^## " design/BRIEF.md` ≥ 7).
- `design/handoff/<data>/` existe, com pelo menos: tokens, nav, footer, hero, card de app, página legal.
- `design/README.md` aponta o handoff vigente e lista o que falta.

**Só no navegador:** a sessão no Claude Design é do usuário. O WP fica `blocked` entre os
passos 1 e 2 (motivo em `BLOQUEIOS`).

**Risco:** baixo. O custo é a sessão do usuário; sem ela, D4 (B) — redesign direto no código.

## Estado em 2026-10-13 (fechado)

- Passo 1 feito: `design/BRIEF.md` (9 seções `## `, critério >= 7 coberto), escrito pelo `site-ux` com as
  restrições do `site-arquiteto`; `design/README.md` com as regras (export congelado, handoff prevalece,
  texto do export é placeholder, `design/` é público no modo branch) e "Handoff vigente: nenhum ainda".
- Verificação: `check_site.py` na raiz e com `--raiz dist` verdes, `design/` fora de `dist`. Nenhuma página
  tocada; auditoria `site-qa`/`seo-perf`/`site-ux` dispensada (só markdown em `design/` e `.claude/context`).
- Critérios 2 e 3 abertos: dependem do export em `design/handoff/<data>/` (passo 2, do usuário) e do mapa
  do passo 3. `visual: true` fecha só depois que o usuário reportar o que viu.
- Achado `DESIGN-PUBLICO-JEKYLL-01` roteado ao WP-07.
- Passos 2 e 3 feitos. Sessão no Claude Design feita pelo usuário em duas rodadas: rodada 1 em
  `design/handoff/2026-10-13/` (histórico, commit 7c52237) e rodada 2 em `design/handoff/2026-10-13-rodada-2/`
  (vigente, commit b75892d: tokens `GHF Kit v2`, nav, footer, hero, card de app, página legal, landing
  LottoExpert, 404, convite). `site-ux` auditou cada rodada (rodada 2: "sim, com ressalvas").
- Critérios: (1) `grep -c "^## " design/BRIEF.md` = 10 (a §10 registra as decisões do usuário: direção A,
  tema escuro com legal em papel, Inter, marca ciano, LottoExpert violeta, ordem dos apps, prova sem
  números, desde 2004, trevo só como ícone); (2) o handoff vigente tem os componentes exigidos;
  (3) `design/README.md` nomeia o vigente e lista o que falta.
- Resíduos roteados ao WP-10: `LOGO-ANO-E-FUNDO-ESCURO-01` e `DESIGN-RODADA-3-01`.
- O item visual (a sessão no Claude Design) foi feito e visto pelo usuário.
- Publicado em: — (branch `feat/wp-06-brief-de-design`; PR para `develop` ainda não aberto, decisão do usuário).
