# design/

Sistema visual do site — decisão do humano, no Claude Design (claude.ai/design), conforme D4.

- `BRIEF.md` — escrito pelo agente no WP-06: marca, os 4 produtos e a hierarquia entre eles,
  anatomia de landing, tokens que já existem, o que preservar, o que resolver. A seção 10 traz
  as decisões do humano depois da rodada 1.
- `handoff/<AAAA-MM-DD>/` — o export de cada sessão no Claude Design. É a referência que o
  `site-ux` audita e o `site-dev` implementa.

## Handoff vigente

**`handoff/2026-10-13/` — rodada 1 (incompleta).** Direção escolhida: **A "Navy técnico"**, com
as trocas da seção 10 do brief (LottoExpert em violeta; ordem dos apps).

Cobre: tokens, estados, nav com seletor de idioma, faixa de sugestão, menu mobile e footer, nas
três direções (A navy técnico, B grafite instrumento, C ardósia do logo — B e C ficam como
registro do que foi descartado).

Não cobre: home, card de app completo, bloco de feature, landing completa, página legal (só os
tokens de papel), 404, convite do bolão, tablet (768), foco e acento sobre o papel claro, versão
do logo para fundo escuro. Para esses itens vale "sem referência no handoff": o `site-ux` não
inventa — é a pauta da rodada 2.

Divergências do export que a seção 10 do brief corrige: acento do LottoExpert (ouro → violeta),
ordem dos apps no footer, `uploads/BRIEF.md` antigo (EclipseGo "em breve"). Defeitos do mock:
dropdown de 7 línguas cortado; `--border-strong` rotulado "3:1" mede ~2:1; foco ciano sobre o
papel claro mede 1,7–1,9:1.

Para abrir: sirva a pasta por HTTP (`python3 -m http.server -d "design/handoff/2026-10-13"`) e
abra `GHF Design System.dc.html` — por `file://` o canvas não carrega (usa `fetch`).

### Mapa do export 2026-10-13

- `GHF Design System.dc.html` — canvas com as 3 direções lado a lado; importa o `GHF Kit.dc.html`.
- `GHF Kit.dc.html` — o componente. Tokens em `THEMES` (A, B, C) e `APPS` no `<script>` do fim do
  arquivo; contrastes calculados ao vivo.
- `support.js` — runtime do canvas, não é parte do site.
- `assets/` — logo e favicons usados; `uploads/` — o que foi enviado (inclui uma versão antiga do brief).
- `github.md` — nota de sincronização gerada pelo Claude Design.

| Componente | Onde no `GHF Kit.dc.html` | Larguras |
|---|---|---|
| Tokens (cor, tipo, espaçamento, raio, sombra, foco) | "1 · Tokens"; dados em `THEMES`/`APPS` | — |
| Papel claro (páginas legais) | cartão "Tema claro" | — |
| Botão primário e secundário, link (5 estados) | "2 · Estados" | — |
| CTA da Play publicado vs em breve, selo, imagem ausente, idioma incompleto | "2 · Estados" | — |
| Prova: fatos, nota da Play (opcional), seção ausente | "2 · Estados" | — |
| Nav da home, seletor de 7 línguas, faixa de sugestão | "3 · Nav e seletor de idioma" | 1280, 360 |
| Nav de landing com alternador PT/EN; menu mobile; TopoWalk em russo | "3 · Nav e seletor de idioma" | 1280, 360 |
| Footer | "4 · Footer" | 1280, 360 |

## Regras

- **Cada export é congelado.** `handoff/<data>/` não se edita. Desenho novo é **pasta nova**
  (`handoff/<AAAA-MM-DD>-<tema>/`), e esta página passa a nomeá-la como vigente.
- **Onde o handoff e o brief divergem, o handoff prevalece** — exceto as decisões da seção 10 do
  brief, posteriores à rodada 1. `uploads/` dentro do export é a cópia que o Claude Design leu,
  não a fonte: a fonte é `BRIEF.md`.
- **Texto do export é placeholder.** A copy vem do README/ASO de cada app; o texto legal, do
  repositório do app.
- **Tudo aqui é público** enquanto o Pages publicar em modo branch (o Jekyll publica `design/`).
  Não versionar nada que não possa estar em `ghfsoftware.com/design/...`.

Quando houver biblioteca de componentes no código (depois do WP-08), `/design-sync` pode manter
o projeto de design-system sincronizado com ela, um componente por vez.
