---
id: WP-08
titulo: As 10 páginas usam um layout, componentes únicos e rota por idioma
area: landing
status: doing
depende_de: [WP-07]
adr: [ADR-001]
spec: docs/AVALIACAO.md
decisoes: [D2, D9]
tamanho: L
risco: alto
visual: true
branch: feat/wp-08-layout-unico
---

# WP-08 — As 10 páginas usam um layout, componentes únicos e rota por idioma

**Depende de:** WP-07 · **Achados roteados:** `NAV-FOOTER-DERIVA-01`, `I18N-SEM-URL-01`

**Exceção de dependência (2026-10-13, usuário):** o WP-08 começa com o WP-07 `blocked` (só falta
o deploy, adiado para uma janela de pouco uso do bolão). A branch fica isolada: **sem merge em
`develop` até o WP-07 estar no ar**, para o `/release` publicar a troca de stack e a migração das
páginas separadas, cada uma com o seu rollback.

**Objetivo:** nav, footer, tema e `<head>` existem uma vez (`src/layouts/`, `src/components/`);
o conteúdo legal é um `.md` por idioma em `src/content/legal/` renderizado por um layout; o
inglês vive em `/en/...` com `hreflang`; o Tailwind é compilado no build. Sem mudança visual
intencional — o redesign é WP-10.

**Contexto:** `docs/AVALIACAO.md` §2 itens 5 e 6; hashes de nav/footer diferentes em todas as
landings; dicionário i18n de até 126 chaves por página; texto legal em 3 cópias.

**Ler antes:** `docs/AVALIACAO.md` §3.2; ADR-001; ADR-002; WP-07 (o que ficou em `public/`).

**Arquivos-alvo:** `src/**`, `public/**`, `astro.config.mjs`, `tailwind.config.mjs`,
`tools/check_site.py` (passa a entender `en/`), `CLAUDE.md` seção "Arquitetura", `README.md`.
As páginas `.html` da raiz **saem** do repositório quando a equivalente em `src/` gera o mesmo
caminho em `dist/`.

**Passos:** por página, na ordem home → landings → legais → convite (que fica em `public/`):
1. extrair nav/footer para componentes (a versão de referência é a de `index.html`; as
   diferenças entre páginas viram achado se forem intencionais);
2. conteúdo pt e en separados (`src/pages/x.astro` e `src/pages/en/x.astro`, ou i18n routing
   do Astro), `hreflang` nos dois;
3. legal: `.md` em `src/content/legal/<app>.<idioma>.md` com `lastUpdated` no front-matter,
   layout de documento (sumário, largura de leitura);
4. `/verify` por página; `site-ux` AUDITAR compara antes/depois em 360/1280.

**Critérios de aceite:**
- `python3 tools/check_site.py --raiz dist` verde; `dist/en/` com as mesmas páginas de `dist/`.
- `grep -rl "tailwind.config = " src/ | wc -l` = 0; `grep -rc "cdn.tailwindcss\|font-awesome" dist | grep -v ":0"` vazio.
- `grep -c "<nav" src/components/Nav.astro` = 1 e nenhuma outra `<nav` em `src/pages/`.
- Para cada página legal: um só `.md` por idioma, data no front-matter, igual à do repositório do app (`check_site.py`).
- Capturas antes/depois (360 e 1280) por página sem diferença visual não intencional — relato do `site-ux`.

**Só no navegador:** cada página pt e en, troca de idioma preserva a página; convite com link real.

**Irreversível:** páginas `.html` da raiz removidas do repositório (ficam no git). URLs não mudam.

**Risco:** alto por volume e pelas URLs; médio por página. Quebrar em PRs por página.
