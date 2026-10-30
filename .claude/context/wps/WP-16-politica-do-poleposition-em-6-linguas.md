---
id: WP-16
titulo: A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de
area: legal
status: todo
depende_de: [WP-15]
adr: [ADR-001]
spec: ""
decisoes: [D7, D8]
tamanho: M
risco: alto
visual: true
branch: feat/wp-16-legal-poleposition-6-linguas
---

# WP-16 — A política de privacidade do Pole Position existe no site em pt, en, es, fr, it e de

**Depende de:** WP-15 (rota e check N-línguas) · **Achados roteados:** `PREVALENCIA-PT-NOS-APPS-01` (o `POLEPOSITION-ATRAS-01` foi para o WP-04, que espelha o pt antes)

**Objetivo:** `/poleposition-privacy.html` (pt, URL contratual intocada), `/en/`, `/es/`,
`/fr/`, `/it/` e `/de/poleposition-privacy.html` com o mesmo texto, a mesma data e as mesmas
seções, espelhando o `PRIVACY_POLICY.md` do repositório do app; o mapa de `idiomas.json` passa a
listar as 6 línguas para esta página. Vem antes do TopoWalk por ser 2,5× menor (2.352 vs 5.842
palavras) — prova o processo.

**Contexto:** D8. O app fala `values-{pt-rBR,de,es,fr,it}` com inglês padrão
(`../pole-position/pole-position-app/app/src/main/res/values/strings.xml:2`); a ficha da Play
nas 6 línguas está em `docs/aso_plan.md` §4. A origem legal só existe em pt
(`../pole-position/pole-position-app/PRIVACY_POLICY.md`, 10 seções `##` numeradas + "Resumo de
Segurança dos Dados", 14 `###`). **O site está atrás da origem hoje:**
`diff <(sed '1,/^---$/d' src/content/legal/poleposition-privacy.pt.md) ../pole-position/pole-position-app/PRIVACY_POLICY.md`
→ data "setembro de 2026" vs "agosto de 2026" e a linha `POST_NOTIFICATIONS` (`:140`) ausente no
site. Traduzir de uma cópia atrasada propaga o atraso para 6 línguas.

**Ler antes:** `.claude/commands/legal.md`; `.claude/agents/site-legal.md`; D7 e D8 em
`decisoes.md`; `../pole-position/pole-position-app/PRIVACY_POLICY.md` inteiro; WP-15 (formato
do `.md` por língua e regras do check).

**Arquivos-alvo:** `src/content/legal/poleposition.{pt,en,es,fr,it,de}.md`,
`src/content/legal/poleposition-privacy.pt.md`, `src/i18n/idiomas.json` (só a entrada `poleposition-privacy`).
Fora do site, **antes** deste WP e feito pelo usuário (ou por WP no repositório do app):
cláusula de prevalência do pt no `PRIVACY_POLICY.md` do app, se D8 (b1).

**Passos:**
1. Pré-condição: `diff` (sem o front-matter) entre a origem e `src/content/legal/poleposition-privacy.pt.md` vazio
   (`python3 tools/sync_legal.py poleposition`). Se a cláusula de prevalência (D8 b1) ainda não
   está na origem, **parar** — o agente não a redige aqui.
2. en: conferir o en existente contra o pt atualizado (D7).
3. es, fr, it, de: traduzir do **pt** (não do en), cláusula por cláusula, sem reorganizar;
   nomes próprios, SDKs, permissões e e-mail literais; tabela do "Resumo de Segurança dos Dados"
   com os rótulos que a Play usa naquela língua.
4. `lastUpdated` igual em todas; mapa de `idiomas.json` com as 6.
5. `site-legal` confere; usuário revisa es/fr/it (e de, se puder) — o relato entra no WP.

**Critérios de aceite:**
- `diff <(sed '1,/^---$/d' src/content/legal/poleposition-privacy.pt.md) ../pole-position/pole-position-app/PRIVACY_POLICY.md` vazio.
- `python3 tools/check_site.py --raiz dist` verde — inclui as regras do WP-15: mesma data nas 6,
  mesmo número de `##` (11) e `###` (14) em todas, cada `` `PERMISSÃO` `` da origem com a mesma
  contagem em cada língua, `Firebase Analytics`/`Firebase Crashlytics` presentes em todas.
- `for l in en es fr it de; do test -f dist/$l/poleposition-privacy.html; done` sem falha;
  `test -f dist/poleposition-privacy.html` e o conteúdo é pt (`grep -c "Última atualização" ≥ 1`).
- `grep -c 'hreflang' dist/poleposition-privacy.html` = 7.
- Nenhum `pendente` no front-matter dos 6 `.md`.

**Do WP-15 (ADR-007):** a faixa de sugestão traz um `<template lang>` por língua da página; ao publicar as línguas novas, reavaliar se o template por língua escala (6 línguas na política) ou se a faixa passa a ler o texto de `ui.ts`. O seletor com 3+ línguas só existe a partir daqui: o visual dele (e dele com a faixa) entra neste checklist, não no do WP-15.

**Só no navegador:** as 6 versões em 360 e 1280: título, data no topo, sumário com 11 entradas,
tabela do resumo legível (sem estouro horizontal em 360), seletor com as 6 línguas e troca
preservando a página. Navegador em `de`: abre a URL pt, vê a faixa (se D8 c1) e fica no pt. O
usuário reporta, e registra quais línguas revisou.

**Irreversível:** texto legal publicado é o que o usuário aceitou naquela data; tradução
errada publicada vale como declaração da GHF naquela língua até ser corrigida. A cláusula de
prevalência (D8 b1) é a mitigação. A URL pt que a Play cita não muda.

**Risco:** alto — texto legal em 4 línguas novas, revisão humana parcial. Específico: tradução
que muda o sentido de "não coletamos"/"anônimo"/"opcional"; tabela da Play com rótulo que não
corresponde ao formulário de segurança de dados.
