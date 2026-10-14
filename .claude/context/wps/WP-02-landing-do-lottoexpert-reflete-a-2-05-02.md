---
id: WP-02
titulo: A landing do LottoExpert apresenta as funcionalidades da 2.05.02
area: landing
status: done
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
`README-LOTTO-DESATUALIZADO-01`, `README-LOTTO-TERMOS-ROTULO-01`

**Objetivo:** `lottoexpert.html` (pt e en) apresenta o que a 2.05.02 entrega e que hoje não
aparece: Teimosinha, prestação de contas do bolão e backup com restauração segura — conforme D1.

**Contexto:** `grep -ci teimosinha lottoexpert.html` = 0; `grep -ci "prestação de contas"` = 0.
A copy de produto está em `../lotto-expert/docs/ASO_METADATA.md` e no README do app; o README
copiado em `docs/LOTTOEXPERT_README.md` está desatualizado (achado roteado). Régua de jogo
responsável: `check_site.py` §5.

**Origem da copy (fonte única).** Nem o `ASO_METADATA.md` nem o `README.md` do app citam
Teimosinha ou prestação de contas (`grep -ci` = 0 nos dois). A origem rastreável no repositório
do app é: Teimosinha — `../lotto-expert/docs/TERMS_OF_SERVICE.md:11` ("registro do mesmo jogo em
vários concursos seguidos"); prestação de contas — `TERMS_OF_SERVICE.md:11` e `:72`,
`PRIVACY_POLICY.md:121` (imagem gerada no aparelho, divisão do prêmio por participante);
restauração segura — `../lotto-expert/docs/LottoExpertContent.md:144` ("faz merge sem apagar
dados criados depois do backup") e `:551`. As duas funcionalidades estão na tag `v2.05.02`
(`SweepstakeSettlement.kt`, `FreemiumConfig.kt:37`). O bloco parafraseia essas linhas — não cria
promessa que elas não sustentem — e o en é tradução fiel do pt (o app não tem `values-en`).
Copiar o README do app **não** traz Teimosinha nem prestação de contas para
`docs/LOTTOEXPERT_README.md`: a lacuna é do README do app (ver triagem abaixo).

**Formato (D1).** D1 decidiu *o que* destacar; as "2 capturas" eram custo estimado, não
requisito. Não há capturas dessas telas no repositório do app e a grade `#features` (`:173`)
usa só ícone Font Awesome. Os 2 blocos seguem o padrão ícone dos 15 cards existentes, sem
imagem nova; capturas, se vierem, ficam para o redesign (WP-10).

**Ler antes:** D1 em `decisoes.md`; `../lotto-expert/docs/ASO_METADATA.md` §1 (descrição
longa) e as seções "Bolão" e "Jogos por Concurso" do `../lotto-expert/README.md`;
`docs/AVALIACAO.md` §3.3 (anatomia de landing — só para não contrariar; o redesign é WP-10).

**Arquivos-alvo:** `lottoexpert.html`; `docs/LOTTOEXPERT_README.md` (cópia do README do app).
Sem `assets/` — nenhuma imagem nova. Nav, footer e `tailwind.config` não mudam: não replica
nas outras páginas.

**Passos:**
1. `site-ux` DESENHAR: onde entram os 2 cards na grade `#features` (`:173`, hoje 15 cards em
   3 colunas — 17 deixa a última linha com 2) e onde entra a linha de backup na seção de
   privacidade/premium; mesmo componente, ícone Font Awesome.
2. `site-dev`: blocos pt e en (`data-i18n` + dicionário), copy a partir das linhas citadas em
   "Origem da copy".
3. `cp ../lotto-expert/README.md docs/LOTTOEXPERT_README.md`.
4. `/verify`.

**Critérios de aceite:**
- `grep -c "Teimosinha" lottoexpert.html` ≥ 2; `grep -ci "prestação de contas" lottoexpert.html` ≥ 1 e
  `grep -ci "settlement" lottoexpert.html` ≥ 1 (conforme D1).
- Toda chave `data-i18n` nova tem entrada pt e en: `site-qa` AUDITAR lista as chaves e as entradas.
- `python3 tools/check_site.py` sem erro em `lottoexpert.html` (copy e links).
- Linha de backup: `grep -ci "sobrescrev" lottoexpert.html` ≥ 1 e `grep -ci "overwrit"` ≥ 1
  (hoje 0 e 0).
- Nenhuma imagem nova: `git diff --stat develop -- assets/` sem saída; nenhum `<img` novo no
  diff de `lottoexpert.html`.
- Achados: `README-LOTTO-DESATUALIZADO-01` tachado como resolvido (cópia em dia) e
  `README-LOTTO-TERMOS-ROTULO-01` com destino `nota`, apontando o repositório do app.
- `diff -q ../lotto-expert/README.md docs/LOTTOEXPERT_README.md` sem saída.

**Só no navegador:** 360 px e 1280 px, pt e en: blocos novos alinhados aos existentes (última
linha da grade em `lg`); nenhum texto em inglês no modo pt e vice-versa.

**Triagem dos achados (site-docs, ao fechar):** o README do app tem o mesmo rótulo
"Termos de Serviço" (`../lotto-expert/README.md:361`) e não cita Teimosinha nem prestação de
contas. As duas coisas são do repositório do app: registrar uma linha no
`../lotto-expert/.claude/context/achados-novos.md` só com pedido do usuário (outro repositório);
aqui o destino é `nota` — "corrigir no README do app; o site recopia no próximo WP que tocar a
landing". O site não edita a cópia à mão (diverge da origem).

**Risco:** médio — copy pública de app de loteria. Se D1 = B (reescrever a seção), o WP vira L
e é melhor quebrar: B agora só com data/links, resto no WP-10.

**Verificação visual:** usuário revisou `lottoexpert.html` (cards novos e textos en) e reportou ok
em 2026-10-12. WP `done`; vai ao ar no `/release` (WP-03).

**Publicado em 2026-10-12** (PR #31 → `master`).
