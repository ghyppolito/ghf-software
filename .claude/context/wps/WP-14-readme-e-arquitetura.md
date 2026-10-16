---
id: WP-14
titulo: README e docs/ARQUITETURA.md descrevem a stack nova e como publicar
area: docs
status: done
depende_de: [WP-09]
adr: []
spec: ""
decisoes: []
tamanho: S
risco: baixo
visual: false
branch: feat/wp-14-readme-e-arquitetura
---

# WP-14 — README e docs/ARQUITETURA.md descrevem a stack nova e como publicar

**Depende de:** WP-09 (fecha a trilha B) · **Achados roteados:** TOOLS-PYCACHE-GITIGNORE-01, AGENTES-PRE-ASTRO-01

**Objetivo:** `README.md` (estrutura do repositório, como rodar, como publicar) e
`docs/ARQUITETURA.md` (layouts, componentes, conteúdo, i18n, build, deploy, URLs contratuais,
ferramentas de verificação) refletem o que existe depois dos WP-07/08/09. `CLAUDE.md` seção
"Arquitetura" aponta para o `ARQUITETURA.md` em vez de descrever.

**Ler antes:** `README.md` atual; `CLAUDE.md`; ADR-001, ADR-002.

**Arquivos-alvo:** `README.md`, `docs/ARQUITETURA.md`, `CLAUDE.md` (só as seções
"Arquitetura" e "Comandos"), `.gitignore` (linha `__pycache__/`, TOOLS-PYCACHE-GITIGNORE-01), `.claude/agents/site-dev.md`,
`.claude/agents/site-arquiteto.md` e `.claude/agents/site-qa.md` (só os trechos da stack anterior ao
Astro, AGENTES-PRE-ASTRO-01).

**Critérios de aceite:**
- Todo caminho citado no README e no ARQUITETURA existe (`grep -oE '\`[a-zA-Z0-9_./-]+\`'` + `test -e`).
- `README.md` não cita `.html` da raiz que já não existe.
- `CLAUDE.md` ≤ 10 KB.
- `tools/__pycache__/` não aparece no `git status` depois do unittest.
- Os agentes não citam mais a stack anterior ao Astro ("10 páginas", `tailwind.config` inline,
  `translations`/`data-i18n`, "antes do WP-08").

**Risco:** baixo.

## Registro

Integrado em `feat/wp-08-layout-unico` (8da7714) em 2026-10-16; CI do #37 verde (run 38946009217: plano, site, lighthouse).

Publicado em: ainda não (D13: sobe com a modernização inteira).

Commits: 35650b3 (início; `AGENTES-PRE-ASTRO-01` entrou no escopo), 05d3f08 (`docs/ARQUITETURA.md` novo, `CLAUDE.md` 12909 → 9540 B com "Arquitetura" apontando para o ARQUITETURA e "Comandos" com os 3 jobs, README com estrutura/como rodar/como publicar, `__pycache__/` no `.gitignore`, agentes sem stack pré-Astro), dda4340 (auditoria do site-qa: 0 alta, 1 média, 5 baixas, todas corrigidas: regra "nenhum .html na raiz" via `check_site.py` §7, front-matter legal, `regras_i18n` chamadas pelo `check_site`, `design/`, pré-requisito do rollback da D13, README sobre a origem do texto legal).

Critérios: caminhos citados existem (sobras são só URLs do site, comandos e extensões soltas); README sem `.html` de raiz; `CLAUDE.md` 9540 B; unittest sem `-B` não suja o `git status`; grep nos agentes limpo; `check_plano` e `check_site` verdes. `visual: false`, nada para o navegador.
