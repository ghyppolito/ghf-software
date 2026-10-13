# design/

Sistema visual do site — decisão do humano, no Claude Design (claude.ai/design), conforme D4.

- `BRIEF.md` — escrito pelo agente no WP-06: marca, os 4 produtos e a hierarquia entre eles,
  anatomia de landing, tokens que já existem, o que preservar, o que resolver. A seção 10 traz
  as decisões do humano depois da rodada 1.
- `handoff/<AAAA-MM-DD>/` — o export de cada sessão no Claude Design. É a referência que o
  `site-ux` audita e o `site-dev` implementa.

## Handoff vigente

**`handoff/2026-10-13-rodada-2/` — rodada 2.** Direção A "Navy técnico", com as decisões da
seção 10 do brief: LottoExpert em violeta (`#A78BFA` no escuro, `#6D28D9` no papel), ordem
LottoExpert, TopoWalk, Pole Position, EclipseGo, marca GHF em ciano, "desde 2004", Inter
servida pelo próprio site (OFL).

Cobre: tokens com contraste calculado (`GHF Kit v2`), nav, footer, home, landing completa do
LottoExpert, landing do TopoWalk (hero e Grátis × Pro), página legal com o texto real da
política do LottoExpert (e modo impressão), 404, convite do bolão (ok, fallback, erro),
estados de botão, link e dado.

**Sem referência no handoff** (o `site-ux` não inventa; pauta de uma rodada 3 antes das landings
que dependem dela): landing completa do TopoWalk (funcionalidades, telas, FAQ), landing do Pole
Position e do EclipseGo, tablet (768) — o footer desktop fica espremido nessa largura —, card
"em breve" completo, imagens reais dos blocos de feature e da galeria, troca de idioma da página
legal (só simulada), logo final para fundo escuro e com "desde 2004"
(`LOGO-ANO-E-FUNDO-ESCURO-01`), regra escrita de "destaque vs ver todas", aviso de jogo
responsável final.

Defeitos conhecidos do export (corrigir na implementação, não copiar): alvos abaixo de 44 px
(links do footer 32 px, alternador de idioma 38 px, sumário legal 36 px); `--border-strong` mede
2,93:1 sobre `--rs`; o ponto "Publicado" das cards é quase o verde do Pole Position; foco ausente
no `<details>` "Ver todas" e nos links sociais do footer; "Texto provisório" visível no aviso de
jogo responsável do LottoExpert; "chance matemática" na landing; "Como tratamos dados" no footer
do kit não tem página. A copy do export não é fonte: frases como "Nada de cadastro, e-mail ou
CPF" e "Nenhum SDK de publicidade" precisam de fonte no README/ASO do app antes de ir ao ar.

Para abrir: sirva a pasta por HTTP (`python3 -m http.server -d "design/handoff/2026-10-13-rodada-2"`).
Cada página tem um prop `w` (default `1280`) que escolhe o ramo de layout; aberta direto, só
mostra o desktop. Para ver 360 ou 768, monte um wrapper que passe `w` por `<dc-import>`.

### Mapa do export 2026-10-13-rodada-2

- `GHF Kit v2.dc.html` — tokens (cor, tipo, espaço, raio, sombra, foco), contrastes calculados
  ao vivo, estados semânticos, papel, estados de componente, proposta de logo, nav, footer.
  `GHF Kit.dc.html` e `GHF Design System.dc.html` são da rodada 1.
- `Site Nav.dc.html`, `Site Footer.dc.html` — componentes importados pelas páginas.
- `fonts/InterVariable.woff2` — Inter variável (SIL OFL 1.1, "The Inter Project Authors"),
  latin-ext, cirílico e `tnum`. Na implementação, acompanhar do `OFL.txt` e avaliar subset.
- `content/LOTTOEXPERT_PRIVACY_POLICY.md` — cópia de `docs/` usada na página legal.
- `support.js` — runtime do canvas, carrega React/Babel do unpkg; não é parte do site.
- `assets/`, `uploads/`, `github.md` — logo e favicons, o que foi enviado, nota de sincronização.

| Tela | Arquivo | Larguras |
|---|---|---|
| Home | `Home.dc.html` | 1280, 360 |
| Landing LottoExpert | `Landing LottoExpert.dc.html` | 1280, 360 (768 sem desenho próprio) |
| Landing TopoWalk (parcial) | `Landing TopoWalk.dc.html` | 1280, 360 |
| Página legal (política do LottoExpert) | `Legal LottoExpert.dc.html` | 1280, 360, impressão |
| 404 | `404.dc.html` | 1280, 360 |
| Convite do bolão | `Convite Bolao.dc.html` | 360, 1280 |
| Nav, footer | `Site Nav.dc.html`, `Site Footer.dc.html` | 1280, 360 |
| Tokens, estados | `GHF Kit v2.dc.html` | — |

### Rodada 1 (histórico) — `handoff/2026-10-13/`

Tokens e estados nas direções A, B e C, nav e footer. B e C ficam como registro do que foi
descartado. Substituída pela rodada 2.

## Regras

- **Cada export é congelado.** `handoff/<data>/` não se edita. Desenho novo é **pasta nova**
  (`handoff/<AAAA-MM-DD>-<tema>/`), e esta página passa a nomeá-la como vigente.
- **Onde o handoff e o brief divergem, o handoff prevalece** — a seção 10 do brief foi aplicada
  na rodada 2. `uploads/` dentro do export é a cópia que o Claude Design leu,
  não a fonte: a fonte é `BRIEF.md`.
- **Texto do export é placeholder.** A copy vem do README/ASO de cada app; o texto legal, do
  repositório do app.
- **Tudo aqui é público** enquanto o Pages publicar em modo branch (o Jekyll publica `design/`).
  Não versionar nada que não possa estar em `ghfsoftware.com/design/...`.

Quando houver biblioteca de componentes no código (depois do WP-08), `/design-sync` pode manter
o projeto de design-system sincronizado com ela, um componente por vez.
