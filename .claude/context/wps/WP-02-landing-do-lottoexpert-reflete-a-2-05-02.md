---
id: WP-02
titulo: A landing do LottoExpert apresenta as funcionalidades da 2.05.02
area: landing
status: todo
depende_de: [WP-01]
adr: []
spec: docs/AVALIACAO.md
decisoes: [D1]
tamanho: M
risco: medio
visual: true
branch: feat/wp-02-landing-lottoexpert-2-05-02
---

# WP-02 — A landing do LottoExpert apresenta as funcionalidades da 2.05.02

**Depende de:** WP-01 (o link "Termos de Uso" no footer já renomeado) · **Achados roteados:**
`README-LOTTO-DESATUALIZADO-01`

**Objetivo:** `lottoexpert.html` (pt e en) apresenta o que a 2.05.02 entrega e que hoje não
aparece: Teimosinha, prestação de contas do bolão e backup com restauração segura — conforme D1.

**Contexto:** `grep -ci teimosinha lottoexpert.html` = 0; `grep -ci "prestação de contas"` = 0.
A copy de produto está em `../lotto-expert/docs/ASO_METADATA.md` e no README do app; o README
copiado em `docs/LOTTOEXPERT_README.md` está desatualizado (achado roteado). Régua de jogo
responsável: `check_site.py` §5.

**Ler antes:** D1 em `decisoes.md`; `../lotto-expert/docs/ASO_METADATA.md` §1 (descrição
longa) e as seções "Bolão" e "Jogos por Concurso" do `../lotto-expert/README.md`;
`docs/AVALIACAO.md` §3.3 (anatomia de landing — só para não contrariar; o redesign é WP-10).

**Arquivos-alvo:** `lottoexpert.html`; `assets/lottoexpert/` (capturas novas, se D1 = A ou B);
`docs/LOTTOEXPERT_README.md` (cópia do README do app).

**Passos:**
1. `site-ux` DESENHAR: onde entram os blocos novos na estrutura existente (seção
   "features", `:173`), sem novo componente; estado sem imagem se a captura não vier.
2. `site-dev`: blocos pt e en (`data-i18n` + dicionário), imagens com `width/height`/`alt`/`lazy`.
3. `cp ../lotto-expert/README.md docs/LOTTOEXPERT_README.md`.
4. `/verify`.

**Critérios de aceite:**
- `grep -c "Teimosinha" lottoexpert.html` ≥ 2; `grep -ci "prestação de contas" lottoexpert.html` ≥ 1 e
  `grep -ci "settlement" lottoexpert.html` ≥ 1 (conforme D1).
- Toda chave `data-i18n` nova tem entrada pt e en: `site-qa` AUDITAR lista as chaves e as entradas.
- `python3 tools/check_site.py` sem erro em `lottoexpert.html` (copy e links).
- Imagem nova: `<img` com `width`, `height`, `alt` não vazio e `loading="lazy"`.
- `diff -q ../lotto-expert/README.md docs/LOTTOEXPERT_README.md` sem saída.

**Só no navegador:** 360 px e 1280 px, pt e en: blocos novos alinhados aos existentes; imagem
não estoura; nenhum texto em inglês no modo pt e vice-versa.

**Risco:** médio — copy pública de app de loteria. Se D1 = B (reescrever a seção), o WP vira L
e é melhor quebrar: B agora só com data/links, resto no WP-10.
