---
id: WP-09
titulo: O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência
area: legal
status: todo
depende_de: [WP-08]
adr: []
spec: ""
decisoes: [D7]
tamanho: M
risco: medio
visual: false
branch: feat/wp-09-sync-legal
---

# WP-09 — O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência

**Depende de:** WP-08 (legal em `.md` no site) · **Achados roteados:** —

**Objetivo:** `tools/sync_legal.py <app>` copia `PRIVACY_POLICY.md`/`TERMS_OF_SERVICE.md` do
repositório do app para `src/content/legal/<app>.pt.md`, extrai a data para o front-matter e
deixa um marcador `en: pendente` quando o en está atrás; `check_site.py` falha se o pt do
site difere da origem (quando a origem está acessível) ou se o en está marcado pendente.

**Contexto:** D7; o `/legal` hoje é manual (WP-01 é o primeiro uso). Com 4 apps e releases
mensais, o ritual se repete; o erro recorrente é esquecer a data no en.

**Ler antes:** `.claude/commands/legal.md`; `.claude/agents/site-legal.md`; WP-08 (formato
do `.md` e do front-matter).

**Arquivos-alvo:** `tools/sync_legal.py`; `tools/check_site.py` (§4 passa a ler front-matter);
`.claude/commands/legal.md` (passa a chamar o script); `CLAUDE.md` "Comandos".

**Critérios de aceite:**
- `python3 tools/sync_legal.py lottoexpert` com origem igual: "nada a fazer"; com origem
  diferente: `.md` pt atualizado, `lastUpdated` certo, `en: pendente` no front-matter.
- `python3 tools/check_site.py` falha com `en: pendente` e passa depois da tradução.
- Script só biblioteca padrão; roda sem o repositório do app presente (aviso, não erro).

**Risco:** médio — automatizar cópia de texto legal. O script **nunca** toca o en nem altera
texto; só copia pt e marca.
