---
id: WP-14
titulo: README e docs/ARQUITETURA.md descrevem a stack nova e como publicar
area: docs
status: todo
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

**Depende de:** WP-09 (fecha a trilha B) · **Achados roteados:** TOOLS-PYCACHE-GITIGNORE-01

**Objetivo:** `README.md` (estrutura do repositório, como rodar, como publicar) e
`docs/ARQUITETURA.md` (layouts, componentes, conteúdo, i18n, build, deploy, URLs contratuais,
ferramentas de verificação) refletem o que existe depois dos WP-07/08/09. `CLAUDE.md` seção
"Arquitetura" aponta para o `ARQUITETURA.md` em vez de descrever.

**Ler antes:** `README.md` atual; `CLAUDE.md`; ADR-001, ADR-002.

**Arquivos-alvo:** `README.md`, `docs/ARQUITETURA.md`, `CLAUDE.md` (só as seções
"Arquitetura" e "Comandos"), `.gitignore` (linha `__pycache__/`, TOOLS-PYCACHE-GITIGNORE-01).

**Critérios de aceite:**
- Todo caminho citado no README e no ARQUITETURA existe (`grep -oE '\`[a-zA-Z0-9_./-]+\`'` + `test -e`).
- `README.md` não cita `.html` da raiz que já não existe.
- `CLAUDE.md` ≤ 10 KB.

**Risco:** baixo.
