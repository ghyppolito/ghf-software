---
id: WP-05
titulo: Todo PR para develop roda check_site, check_plano e validação de HTML e links
area: infra
status: todo
depende_de: [WP-04]
adr: []
spec: docs/AVALIACAO.md
decisoes: [D5]
tamanho: M
risco: medio
visual: false
branch: feat/wp-05-ci-no-pr
---

# WP-05 — Todo PR para develop roda check_site, check_plano e validação de HTML e links

**Depende de:** WP-04 (o `check_site.py` precisa estar verde para o CI nascer verde) ·
**Achados roteados:** —

**Objetivo:** existe `.github/workflows/pr.yml` que, em PR para `develop` e `master`, roda
`tools/check_site.py`, `tools/gen_estado.py --check`, `tools/check_plano.py`, validação de
HTML (`html-validate`) e de links (`lychee`, só internos). Não muda o deploy.

**Contexto:** `docs/AVALIACAO.md` §2 item 3 — não há rede nenhuma hoje. O WP-07 (migração de
stack) não pode começar sem gate. Cota do Actions: o lotto-expert registra estouro (D7 lá);
este repositório é público e estático — minutos grátis, jobs de segundos.

**Ler antes:** `docs/AVALIACAO.md` §2.3 e §3.2; `.github/workflows/pr.yml` do lotto-expert
(job `plano`) como modelo de estrutura.

**Arquivos-alvo:** `.github/workflows/pr.yml`; `.htmlvalidate.json` (regras: `no-inline-style`
desligada — Tailwind é inline até o WP-08); `CLAUDE.md` seção "Comandos" (uma linha).

**Passos:**
1. `pr.yml`: jobs `plano` (python) e `site` (python + `npx html-validate *.html` +
   `lychee --offline`). `concurrency` por branch; `on: pull_request` para `develop` e `master`.
2. Rodar os validadores localmente antes, e corrigir o que for **erro** de HTML nas páginas
   atuais só se for trivial (tag não fechada); o resto vira achado roteado ao WP-08.
3. `/verify`; abrir PR de teste e ver o CI verde (usuário faz push).

**Critérios de aceite:**
- `gh pr checks <PR>` mostra `plano` e `site` verdes num PR da branch deste WP.
- `pr.yml` não tem `deploy`, `pages` nem `permissions: contents: write`.
- `npx html-validate *.html` sem erro (avisos permitidos); erros restantes listados em
  `achados-novos.md` com destino.

**Risco:** médio — proteção de branch com CI obrigatório é decisão do usuário (registrar em
`decisoes.md` se ele quiser).
