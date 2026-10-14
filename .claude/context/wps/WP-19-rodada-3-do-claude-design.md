---
id: WP-19
titulo: A rodada 3 do Claude Design cobre as landings que faltam, o tablet e os defeitos da rodada 2
area: design
status: blocked
depende_de: [WP-06]
adr: []
spec: docs/AVALIACAO.md
decisoes: [D4, D8]
tamanho: S
risco: baixo
visual: true
branch: feat/wp-19-rodada-3-claude-design
---

# WP-19 — A rodada 3 do Claude Design cobre as landings que faltam, o tablet e os defeitos da rodada 2

**Depende de:** WP-06 (handoff da rodada 2 vigente) · **Achados roteados:** DESIGN-RODADA-3-01

**Objetivo:** existe `design/handoff/<AAAA-MM-DD>-rodada-3/`, exportado pelo usuário do Claude
Design, que cobre os 8 itens do pedido abaixo, e `design/README.md` o nomeia como handoff vigente.

**Contexto:** `design/README.md:18-37` (seção "Handoff vigente"): a rodada 2
(`design/handoff/2026-10-13-rodada-2/`) não tem landing completa do TopoWalk, landings do Pole
Position e do EclipseGo, tablet 768 (o footer de 6 colunas fica espremido), card "em breve"
completo, troca de idioma real na página legal, faixa de sugestão de idioma numa página real, nem
a regra escrita de "destaque vs ver todas". Defeitos medidos pelo `site-ux` no export: alvos
abaixo de 44 px (links do footer 32 px, alternador PT/EN 38 px, sumário legal 36 px),
`--border-strong` 2,93:1 sobre `--rs`, ponto "Publicado" quase igual ao verde do Pole Position,
foco ausente no `<details>` "Ver todas" e nos links sociais do footer. O seletor de línguas e a
faixa de sugestão vêm de D8 (c1); TopoWalk fala 7 línguas e Pole Position 6 (D8 a2).

Relação com outros WPs: é pré-condição das landings TopoWalk, Pole Position e EclipseGo no WP-10
e do WP-18; **não** bloqueia home, landing LottoExpert, legal, 404 e convite no WP-10, que já têm
referência na rodada 2. O template não tem campo para dependência parcial; o WP-10 não muda —
o pré-voo dele lê este WP pela linha do achado.

**Ler antes:** `design/README.md` seção "Handoff vigente" e o mapa da rodada 2; `design/BRIEF.md`
§10 (decisões do usuário); `docs/AVALIACAO.md` §3.3; D8 em `decisoes.md` (escopo de línguas e
chegada c1). Copy: `docs/TOPOWALK_README.md`, `docs/POLEPOSITION_README.md`,
`docs/ECLIPSE_GO_README.md` e a ficha ASO de cada app no repositório dele.

**Arquivos-alvo:** `design/handoff/<AAAA-MM-DD>-rodada-3/` (export, pelo usuário — pasta nova,
congelada; a rodada 2 não é editada); `design/README.md` (handoff vigente, mapa da rodada 3,
tabela de cobertura dos 8 itens, o que ainda falta). `design/BRIEF.md` só se a sessão trouxer
decisão nova do usuário (seção 10).

**Passos:**
1. Agente: entrega ao usuário o texto da seção "Pedido para o Claude Design" abaixo, com o
   handoff da rodada 2 como contexto da sessão. WP vai a `blocked` (motivo em `BLOQUEIOS`).
2. **Usuário:** sessão no Claude Design e export para `design/handoff/<AAAA-MM-DD>-rodada-3/`.
3. `site-ux` (AUDITAR) lê o export: confere item a item contra o pedido, calcula o contraste dos
   tokens novos ou alterados, e escreve em `design/README.md` o mapa da rodada 3, a tabela de
   cobertura (item → arquivo do export → coberto/parcial/ausente) e o que ainda falta. A rodada 2
   passa a histórico.

## Pedido para o Claude Design

> Rodada 3 do site da GHF Software, a partir do handoff da rodada 2 (`GHF Kit v2`). Mantenha a
> direção, os tokens e as decisões já tomadas; mude só o que este pedido cita.
>
> **Copy:** use o texto real dos READMEs e das fichas de loja de cada app. Onde não houver texto
> de origem, deixe placeholder marcado como tal (ex.: `[copy: …]`) — não invente frase de produto.
>
> 1. **Landing do TopoWalk completa**, na mesma anatomia da landing do LottoExpert (hero + CTA →
>    funcionalidades com imagem → prova → privacidade em uma frase → FAQ → CTA). Seletor com as
>    7 línguas do app (pt, en, es, fr, it, de, ru). Mostre a página em russo a 360 px.
> 2. **Landings do Pole Position (6 línguas: pt, en, es, fr, it, de) e do EclipseGo (pt/en)**, na
>    mesma anatomia. Deixe explícito que, entre as landings, só mudam os tokens `--app-*` e o
>    conteúdo.
> 3. **Tablet (768 px)** de home, landing, página legal, nav e footer. O footer de 6 colunas da
>    rodada 2 fica espremido nessa largura — redesenhe a quebra.
> 4. **Alvos de toque e foco:** alvo mínimo de 44 px nos links do footer (hoje 32), no alternador
>    de idioma (hoje 38) e no sumário da página legal (hoje 36); foco visível no `<details>` "Ver
>    todas" e nos links sociais do footer.
> 5. **Card "em breve" completo** (para app futuro) e a variante do hero para esse estado.
> 6. **Regra escrita de "destaque vs ver todas"** na home: o que decide um app ir para destaque e
>    o que fica em "ver todas".
> 7. **Troca de idioma da página legal funcionando** (não simulada) e a **faixa de sugestão de
>    idioma** (por `navigator.languages`, sem redirect) aplicada numa página real.
> 8. **Tokens:** `--border-strong` com pelo menos 3:1 sobre `--rs` (hoje 2,93:1), e um token
>    `--success` distinto do verde do Pole Position para o ponto "Publicado" das cards.

**Critérios de aceite:**
- `design/handoff/<AAAA-MM-DD>-rodada-3/` existe (`ls -d design/handoff/*-rodada-3/`) e a
  rodada 2 não mudou (`git diff --stat develop -- design/handoff/2026-10-13-rodada-2/` vazio).
- `design/README.md` tem a tabela de cobertura com os 8 itens do pedido, cada um com o arquivo do
  export onde está, escrita pelo `site-ux`; item ausente ou parcial fica listado em "o que ainda
  falta".
- `design/README.md` nomeia a rodada 3 como handoff vigente
  (`grep -n "rodada-3" design/README.md` na seção "Handoff vigente").
- Contraste de todo token novo ou alterado calculado pelo `site-ux` e registrado em
  `design/README.md`, com `--border-strong` ≥ 3:1 sobre `--rs` e `--success` distinto do token
  de identidade do Pole Position.
- `python3 tools/check_site.py` verde (nenhuma página tocada).

**Só no navegador:** a sessão no Claude Design é do usuário. O WP fica `blocked` entre os passos
1 e 2. Depois do export, o usuário abre a rodada 3 servida por HTTP e confirma: landing do
TopoWalk em russo a 360, as três landings novas a 1280, home/landing/legal a 768, e a troca de
idioma da página legal funcionando.

**Risco:** baixo. Nenhuma página publicada muda. O custo é a sessão do usuário; o que ela não
cobrir fica em "o que ainda falta" e as landings dependentes no WP-10 continuam sem referência.
Copy do export não é fonte — sem origem no README/ASO, não vai ao ar.

## Estado (2026-10-13)

Passos 1–3 feitos: export em `design/handoff/2026-10-13-rodada-3/` (89eaaf6), auditoria do `site-ux` e
do `site-qa` em `design/README.md` (b9a720f). Cobertura: 4 itens cobertos (4, 5, 8 e o 6, com decisão
pendente), parciais 1, 2, 3 e 7, nenhum ausente; o que falta está em "o que ainda falta" do README.
Critérios de comando passaram (`check_site.py` na raiz e em `dist/`, `gen_estado.py --check`,
`check_plano.py`, build, html-validate sem erros; lychee não instalado, não verificado). O critério 1
usa `git diff --stat develop`, mas o `develop` local fica atrás: comparar com `origin/develop`
(`WP-19-DIFF-ORIGEM-01`). **Pendente, do usuário:** checklist de navegador (`visual: true`), que deve
ser escrito aqui com o que ele viu antes de o WP ir a `done`.

Checklist (`python3 -m http.server 8080 -d "design/handoff/2026-10-13-rodada-3"`):
- `Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280.
- `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768.
- Troca pt/en na legal (o en é stub, esperado).
- `Landing App.dc.html?app=pole&suggest=de`: a faixa fecha e não volta na sessão.
- Tab mostra foco em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole no footer.
