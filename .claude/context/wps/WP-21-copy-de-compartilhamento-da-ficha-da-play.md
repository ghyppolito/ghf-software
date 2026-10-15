---
id: WP-21
titulo: Title e description de compartilhamento vêm da ficha da Play
area: landing
status: todo
depende_de: [WP-11]
adr: []
spec: docs/AVALIACAO.md
decisoes: []
tamanho: M
risco: baixo
visual: false
branch: feat/wp-21-copy-de-compartilhamento
---

# WP-21 — Title e description de compartilhamento vêm da ficha da Play

**Depende de:** WP-11 · **Achados roteados:** `HOME-EN-META-01`, `LOTTO-EN-META-01`, `TOPO-EN-META-01`, `POLE-EN-META-01`, `ECLIPSE-EN-META-01`, `HOME-TITLE-LONGO-01`, `TITLE-HIFEN-TRAVESSAO-01`

**Objetivo:** `title`, `description` e og/twitter da home e das 4 landings, em pt e en, saem da copy oficial de cada app, e
não de texto herdado da página antiga.

**Contexto:** o veredito do WP-11 tirou estes achados do SEO técnico: são copy de produto. As páginas en reaproveitam textos
que a página antiga já publicava; o title pt da home tem 66 caracteres; o `<title>` usa hífen onde h1 usa travessão.

**Ler antes:** `../lotto-expert/docs/ASO_METADATA.md`, `../topo-walk/docs/store_listing_texts.md`,
`../pole-position/pole-position-app/docs/aso_plan.md`, `../eclipse-go/docs/EclipseGoContent.md`; `src/i18n/<pagina>.ts`.

**Arquivos-alvo:** `src/i18n/{home,lottoexpert,topowalk,poleposition,eclipsego}.ts`, `tools/check_site.py` (limite de title).

**Passos:**
1. Para cada página, escolher title (≤ 60) e description da ficha, em pt e en. Copy de produto é decisão do usuário: opções
   em `decisoes.md` se a ficha divergir da página.
2. Unificar o separador do `<title>` com o do h1.
3. `check_site.py`: erro para title > 60 caracteres.

**Critérios de aceite:**
- `python3 tools/check_site.py` verde, com a regra do title.
- Copy do LottoExpert sob o §5 (jogo responsável).
- Nenhum `title`/`description` en igual ao pt.

**Risco:** baixo. Copy de produto passa pelo usuário antes do commit.
