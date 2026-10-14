# design/

Sistema visual do site — decisão do humano, no Claude Design (claude.ai/design), conforme D4.

- `BRIEF.md` — escrito pelo agente no WP-06: marca, os 4 produtos e a hierarquia entre eles,
  anatomia de landing, tokens que já existem, o que preservar, o que resolver. A seção 10 traz
  as decisões do humano depois da rodada 1.
- `handoff/<AAAA-MM-DD>/` — o export de cada sessão no Claude Design. É a referência que o
  `site-ux` audita e o `site-dev` implementa.

## Handoff vigente

**`handoff/2026-10-13-rodada-3/` — rodada 3.** Mantém a direção A "Navy técnico" e os tokens da
rodada 2 (violeta do LottoExpert, ordem LottoExpert, TopoWalk, Pole Position, EclipseGo, marca em
ciano, "desde 2004", Inter local). Acrescenta um template único de landing (`Landing App`) que
serve os 4 apps — entre eles mudam só `--app-acc`, `--app-acc-edge`, `--app-acc-light` e o objeto
de `content/landings.js` —, o tablet 768 de nav e footer, o estado "em breve", a regra escrita de
"destaque vs ver todas", a troca de idioma da política e a faixa de sugestão de idioma. Corrige os
alvos de toque, o foco e dois tokens (`--border-strong`, `--success`).

**Referência para o WP-10:** landings dos 4 apps → `Landing App.dc.html` (`?app=lotto|topo|pole|eclipse`,
`?lang=`). `Landing LottoExpert.dc.html` e `Landing TopoWalk.dc.html` ficaram da rodada 2 (só
trocaram o valor de `--border-strong`): são resíduo, não referência. Home, legal, nav, footer, 404
e convite: os arquivos de mesmo nome da rodada 3.

### Cobertura do pedido da rodada 3 (WP-19)

| # | Item | Arquivo no export | Veredito |
|---|---|---|---|
| 1 | Landing TopoWalk completa, 7 línguas, russo a 360 | `Landing App.dc.html?app=topo`; conteúdo em `content/landings.js` (`topo`); russo a 360 em `GHF Design System.dc.html` #3b | **Parcial.** Anatomia completa (hero, 4 funcionalidades, "ver todas", prova, Grátis × Pro, privacidade, FAQ, CTA) e seletor com 7 línguas. As 4 funcionalidades não têm imagem (placeholder `[imagem ausente]`); fora do pt, só os rótulos de interface existem — o resto é `[copy: ru · …]` com faixa de aviso |
| 2 | Pole Position (6 línguas) e EclipseGo (pt/en), mesma anatomia | `Landing App.dc.html?app=pole` e `?app=eclipse`; tokens `--app-*` em `landings.js`; regra escrita em `GHF Kit v3.dc.html` §6 | **Coberto.** Pole com 2 de 4 imagens de funcionalidade e galeria; EclipseGo com 1 de 3. Play = `#` nos dois |
| 3 | Tablet 768: home, landing, legal, nav, footer | `Site Nav` e `Site Footer` (ramo `t`, 600–1023 px); `GHF Design System.dc.html` #3e (landing) e #3f (home, legal, footer) | **Coberto, a verificar no navegador.** Nav: marca, idioma e "Menu" (menu em 2 colunas). Footer: marca e contato em cima, 4 apps em 4 colunas embaixo (≈ 158 px por coluna). Legal a 768 usa o sumário recolhível (índice lateral só ≥ 1024). Home e landing são fluidas, sem ramo próprio |
| 4 | Alvos 44 px e foco | `Site Footer` (links, títulos e sociais 44), `Site Nav` (alternador, menu, faixa 44), `Legal` (sumário 44/52), `GHF Kit v3` (alternador e footer do kit 44) | **Coberto.** Foco no `<summary>` "Ver todas as funcionalidades" (`Landing App`, contorno 3 px interno) e nos links sociais (contorno 2 px interno). O chip "Atualizado" da política mede 36 px, mas não é interativo |
| 5 | Card "em breve" e variante do hero | `GHF Kit v3.dc.html` §5 | **Coberto** como componente (borda e faixa tracejadas, selo "Em breve" com anel vazio, sem botão Play, CTA vira `role="status"`). Não aplicado numa landing real: `Landing App` não tem estado "em breve" |
| 6 | Regra "destaque vs ver todas" | `GHF Kit v3.dc.html` §6 | **Coberto, com decisão pendente.** Os limiares (publicado, landing e política, atualização nos últimos 12 meses, 4 posições) são do Claude Design, não do usuário — ver "Defeitos conhecidos" |
| 7 | Troca de idioma da legal real e faixa de sugestão | Legal: `Legal LottoExpert.dc.html` (`?lang=`, `#seção`, mantém a posição). Faixa: `Site Nav.dc.html` (`navigator.languages`, sem redirect, `sessionStorage`); aplicada em `GHF Design System.dc.html` #3c (`Landing App?app=pole&suggest=de`) | **Parcial.** A faixa é real e funciona numa página de verdade. A troca da legal carrega `content/LOTTOEXPERT_PRIVACY_POLICY.en.md`, que **não está no export**: o inglês cai no stub `[copy: en · …]` com o aviso de prevalência do pt |
| 8 | `--border-strong` ≥ 3:1 sobre `--rs`; `--success` distinto do Pole Position | `GHF Kit v3.dc.html` ("Rodada 3 · tokens alterados"); valores aplicados em `Home`, `Legal`, `Landing App`, `Site Nav` | **Coberto** (números abaixo). `--success` tem dois valores no mesmo export — ver defeitos |

### Contraste dos tokens novos ou alterados (WCAG 2.x, calculado pelo `site-ux`)

| Token | Valor | Sobre `--rs` #1A2335 | Sobre `--sf` #111827 | Sobre `--bg` #0B1120 |
|---|---|---|---|---|
| `--border-strong` rodada 2 | #5E6B85 | 2,93 (falha) | 3,31 | 3,51 |
| `--border-strong` rodada 3 | #66738D | **3,30** (meta ≥ 3) | 3,72 | 3,95 |
| `--success` (selo "Publicado") | #C5E86C | 11,33 | 12,78 | 13,57 |
| `--app-pole` (identidade) | #5FD47E | 8,39 | 9,47 | 10,05 |
| ponto "Publicado" da rodada 2 | #6FCF97 | 8,27 | 9,33 | 9,91 |

Distinção `--success` × Pole Position: matiz 77° contra 136° (59° de distância; o ponto antigo
ficava a 9°, ΔE 17); ΔE76 = 33,4 (antes 17,2); razão de luminância entre os dois verdes 1,35:1, ou
seja, a distinção é de matiz, não de brilho — por isso o selo é glifo `✓` + palavra, nunca só cor.
Sobre o fundo da card (`--sf`), os dois passam de 9:1 e o texto "Publicado" é `--tx2` (11,3:1 sobre
`--bg`). Veredito: distinto o bastante para quem enxerga cor; para daltonismo verde-vermelho a
diferença é fraca, e quem a sustenta é o glifo. O `--success` semântico do kit (mensagem
"Backup concluído") usa outro valor: #DDF3A8 (14,75 sobre `--sf`), tinta #1E2710, borda #5F7A24
(3,18:1 sobre a tinta).

Tokens `--app-*` presentes no template (a `--app-acc-edge` é nova):

| App | `--app-acc` sobre `--bg` | `--app-acc-light` sobre papel #F7F7F5 | `--app-acc-edge` sobre `--bg` |
|---|---|---|---|
| LottoExpert | 6,92 | 6,62 | 3,31 |
| TopoWalk | 7,21 | 5,65 | 2,99 |
| Pole Position | 10,05 | 5,13 | 2,98 |
| EclipseGo | 6,62 | 5,73 | 2,48 |

Texto de acento e `--app-acc-light` passam AA em todos. `--app-acc-edge` (borda da etiqueta Pro e
do plano destacado) fica abaixo de 3:1 em TopoWalk, Pole Position e EclipseGo; é contorno
decorativo — a informação está no texto da etiqueta —, mas na implementação vale usar
`--border-strong` ou clarear a borda do plano destacado.

### Defeitos conhecidos do export (corrigir na implementação, não copiar)

- `--success` com dois valores: #C5E86C no bloco "tokens alterados", em `Home` e na nota 8 do
  Design System; #DDF3A8 na tabela de estados semânticos do `GHF Kit v3`. Escolher um (ou dois
  nomes) antes do WP-08.
- Regra "destaque vs ver todas" (`GHF Kit v3` §6) fixa critérios de produto — 12 meses sem
  atualização, 4 posições, selo "Indisponível" — que ninguém decidiu. É proposta, não regra: decisão
  do usuário (`decisoes.md`) antes de virar código. A lista "ver todas" da home não é renderizada
  (hoje fica vazia).
- Texto legal: o arquivo em inglês da política não veio; o inglês da página legal é stub.
- "Texto provisório" continua em `Landing LottoExpert.dc.html` (resíduo da rodada 2); "Como
  tratamos dados" continua no footer do kit sem página correspondente.
- Copy sem origem em README/ASO (a copy do export não é fonte): "Nenhum SDK de publicidade" e "Nada
  de cadastro, e-mail ou CPF" (prova do LottoExpert; o README não diz isso — "CPF" só aparece na
  política, como dado não coletado); "Sem backend / Nenhum servidor próprio" e "Nenhuma chamada de
  rede" (EclipseGo); "Este site não usa rastreadores nem cookies" (rodapé, depende da D3);
  "equivale a R$ 2,91 por mês" (conta derivada dos R$ 34,90); "chance matemática" na
  funcionalidade do gerador (o README usa a expressão, mas é o termo que a régua de jogo
  responsável do LottoExpert vigia; revisar com o `check_site.py` antes de ir ao ar). Os preços dos planos do LottoExpert e as listas do TopoWalk, Pole Position e
  EclipseGo vêm dos READMEs.
- Links da Play dos 3 apps novos são `#`; `Home`/`Footer` apontam para `Landing App.dc.html?app=…`,
  que não existe no site (as URLs reais são decisão do WP-10/08, respeitando o ADR-001).
- `support.js` carrega React/Babel do unpkg; não entra no site. `screenshots/` só tem `kitv2.jpg`
  (desatualizado).

### O que ainda falta

- Copy e imagens: es, fr, it, de, ru (e en do LottoExpert e do EclipseGo) só existem como
  `[copy: …]`; falta ficha de loja por língua (D8). Imagens ausentes: 4 de 4 funcionalidades do
  TopoWalk, 4 de 4 do LottoExpert, 2 de 4 do Pole Position, 2 de 3 do EclipseGo. Faltam "grátis ou
  pago", faixa de anos e preço do Pole Position e do EclipseGo (`[copy: …]`).
- Arquivo `LOTTOEXPERT_PRIVACY_POLICY.en.md` no export (item 7) e, no repositório, o espelho em inglês
  vem do texto legal do app — não do Claude Design.
- Estado "em breve" aplicado numa landing (item 5); aviso final de jogo responsável do LottoExpert
  (`[copy: redação final do aviso…]`); logo final para fundo escuro e com "desde 2004"
  (`LOGO-ANO-E-FUNDO-ESCURO-01`) — a proposta de logo do `GHF Kit v3` é a da v2.
- Decisão do usuário sobre os limiares do item 6 e sobre o `--success` (dois valores).
- Conferência no navegador (checklist do WP-19): TopoWalk em russo a 360, as 3 landings novas a
  1280, home, landing e legal a 768, troca de idioma da legal e foco.

Para abrir: sirva a pasta por HTTP (`python3 -m http.server -d "design/handoff/2026-10-13-rodada-3"`).
`GHF Design System.dc.html` é o índice da rodada (cada item com iframe). As páginas aceitam
`?app=`, `?lang=` e `?suggest=` (forçar a faixa de sugestão); `w` (360, 768, 1280) escolhe o ramo
de layout quando a página é importada.

### Mapa do export 2026-10-13-rodada-3

- `Landing App.dc.html` — template único das 4 landings; lê `content/landings.js` e
  `content/i18n.js`. Seções opcionais (ver todas, telas, prova, planos em 4 níveis ou Grátis × Pro,
  aviso +18) aparecem só quando há conteúdo.
- `content/landings.js` — conteúdo por app (hero, funcionalidades, grupos, galeria, prova, planos,
  privacidade, FAQ) e tokens `--app-*`; só o pt tem texto. `content/i18n.js` — rótulos de interface
  nas 7 línguas (não é copy de produto).
- `GHF Kit v3.dc.html` — kit da rodada 2 com alvos de 44 px, tokens alterados, card e hero "em
  breve" e regras escritas. `GHF Design System.dc.html` — índice da rodada 3 e das anteriores.
- `Site Nav.dc.html`, `Site Footer.dc.html` — com ramos 360 / 768 / 1280, seletor por número de
  línguas (≤ 3 alternador, ≥ 4 lista) e faixa de sugestão.
- `Home`, `Legal LottoExpert`, `404`, `Convite Bolao` — como na rodada 2, com os tokens novos;
  `Legal` com troca de idioma real. `Landing LottoExpert` e `Landing TopoWalk`: resíduo da rodada 2.
- `assets/` (novos: capturas do Pole Position e do EclipseGo), `uploads/` (inclui os READMEs dos 4
  apps que o Claude Design leu — cópia, não fonte), `fonts/`, `support.js`, `github.md`.

| Tela | Arquivo | Larguras |
|---|---|---|
| Home | `Home.dc.html` | 360, 768, 1280 |
| Landing dos 4 apps | `Landing App.dc.html?app=…` | 360, 768, 1280 |
| Página legal (LottoExpert) | `Legal LottoExpert.dc.html` | 360, 768, 1280, impressão |
| 404, convite do bolão | `404.dc.html`, `Convite Bolao.dc.html` | 360, 1280 |
| Nav, footer | `Site Nav.dc.html`, `Site Footer.dc.html` | 360, 768, 1280 |
| Tokens, estados, em breve, regras | `GHF Kit v3.dc.html` | — |

### Rodada 2 (histórico) — `handoff/2026-10-13-rodada-2/`

Direção A "Navy técnico", com as decisões da seção 10 do brief. Cobriu tokens (`GHF Kit v2`), nav,
footer, home, landing do LottoExpert, hero e Grátis × Pro do TopoWalk, página legal (e impressão),
404 e convite do bolão. Lacunas que a rodada 3 fechou: landings do TopoWalk, Pole Position e
EclipseGo, tablet, card "em breve", faixa de idioma, regra de destaque; e defeitos: alvos de 32/36/38
px, `--border-strong` 2,93:1, ponto "Publicado" parecido com o verde do Pole Position, foco no
`<details>` e nos links sociais. Mapa: `GHF Kit v2`, `Site Nav`, `Site Footer`, `Home`,
`Landing LottoExpert`, `Landing TopoWalk` (parcial), `Legal LottoExpert`, `404`, `Convite Bolao`,
`content/LOTTOEXPERT_PRIVACY_POLICY.md`, `fonts/InterVariable.woff2` (Inter variável, SIL OFL 1.1;
acompanhar o `OFL.txt` e avaliar subset). Substituída pela rodada 3.

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
