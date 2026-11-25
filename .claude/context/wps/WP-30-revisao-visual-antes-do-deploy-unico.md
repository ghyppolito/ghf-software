---
id: WP-30
titulo: O site tem direção visual própria, aprovada no navegador, antes do deploy único
area: design
status: doing
depende_de: []
adr: [ADR-001, ADR-006, ADR-007, ADR-008]
spec: design/REVISAO-VISUAL.md
decisoes: [D4, D25, D26, D29, D30, D33]
tamanho: L
risco: medio
visual: true
branch: feat/wp-30-revisao-visual
---

# WP-30 — O site tem direção visual própria, aprovada no navegador, antes do deploy único

**Depende de:** — (as fatias 1 a 6 e 10a do WP-10 estão feitas e a 9 está parcial; o WP-10 não
entra em `depende_de` porque ele só fecha depois deste WP, e o laço travaria o `ESTADO.md`) ·
**Achados roteados:** `FUNC-SEM-IMAGEM-METADE-VAZIA-01` e `HOME-GRADE-3-CARDS-01` (hoje no WP-20;
a fatia 1 diz se a direção nova os resolve e, se sim, o `site-docs` move o destino para cá) ·
`HOME-VOCABULARIO-TECNICO-01` (hoje na 10b do WP-10): a Home volta a citar as áreas de domínio
(correção do usuário abaixo), então o `site-docs` move este achado para cá

**Objetivo:** a Home e as landings passam nos 7 critérios de "página linda" de
`design/REVISAO-VISUAL.md` §2, com a direção visual proposta em código pelo `site-ux` e pelo
`site-dev` e aprovada pelo usuário no navegador (D33), sem perder nada do que o site já prova.

**Contexto:** ao ver a landing do LottoExpert da fatia 9 do WP-10, o usuário disse "achei que tá
ficando meio sem graça, queria uma página linda", e o mesmo sobre a Home
(`design/REVISAO-VISUAL.md:3-6`). O diagnóstico está em `design/REVISAO-VISUAL.md` §1. Ele aponta
monocromia (o acento por app só tinge botão e etiqueta, `src/styles/tokens.css:149-170`), ritmo
plano, captura crua sem moldura e a Home que acaba na primeira dobra. Também aponta a tabela de 20
linhas do LottoExpert (`src/i18n/lottoexpert.ts:163-184`, en `:346`) e o hero genérico da Home
(`src/i18n/home.ts:49`, D30 (1)). As respostas do usuário estão no §6 do mesmo arquivo e foram
registradas como D33.

**Correção do usuário (2026-11-24), que vale sobre o critério 5 de `design/REVISAO-VISUAL.md` §2
e sobre o `design/BRIEF.md` §3:** "Não queria relacionar a página principal com os apps pois eles
têm temas distintos e eu sigo com novos projetos que não necessariamente seguem a mesma linha.
Posso puxar um SaaS mais para frente por ex. É só ver a stack que tenho domínio". Logo, a Home
**não** é vitrine dos apps, e o h1 não fala deles. Ela apresenta a GHF Software como estúdio de
engenharia desde 2004 (`since_2004`, D30), com as áreas de domínio que o usuário listou:
- mobile nativo (Kotlin/Compose) e Flutter;
- nuvem serverless (GCP/Firebase);
- IA aplicada (Gemini/Claude, agentes e MCP);
- automação e entrega contínua (Docker, Terraform, GitHub Actions);
- processamento no aparelho (ex.: OCR com ML Kit).

**Escolhas do usuário (2026-11-24, questionário):**
- **h1:** "Engenharia de software, do celular à nuvem." **Subtítulo:** "Apps nativos, plataformas em
  nuvem e IA aplicada, projetados e mantidos pela GHF Software desde 2004." (texto aprovado pelo
  usuário: é a origem, D25; o en é tradução fiel).
- **Áreas na Home: três** — Apps mobile (Android nativo com Kotlin e Jetpack Compose; multiplataforma
  com Flutter), Nuvem e SaaS (back-end serverless no Google Cloud e Firebase; plataformas web) e IA
  aplicada (modelos Gemini e Claude, agentes, MCP, IA no aparelho como OCR). **Automação e entrega
  não entra.** O processamento no aparelho entra dentro de IA aplicada.
- **Apps:** seção "Produtos" abaixo das áreas, com espaço para um SaaS futuro.

Essa lista é a origem (D25) das áreas. A redação de cada uma é proposta pelo `site-ux` e aprovada
pelo usuário. Os apps entram numa seção de produtos/portfólio, abaixo, e não são o assunto
principal. A página não cita nome de repositório interno ou privado. Valem os números já medidos da fatia 9 em `/lottoexpert.html`: perf 98, a11y
100, LCP 2,25 s (WP-10, item 9). São o piso que este WP não pode perder.

**Ler antes:** `design/REVISAO-VISUAL.md` (inteiro, 133 linhas), `design/BRIEF.md` §1 (tom), §3
(home) e §7 (restrições: "JS leve, sem dependência", `prefers-reduced-motion`, 360/768/1280,
alemão e russo ~35% mais longos), a D33 em `decisoes.md`, o ADR-008 §5 e §7 (tokens e
sem-polyfill) e o ADR-006 §5 (nenhum terceiro no `<head>`).

**Arquivos-alvo:**
- `src/styles/tokens.css`: escala tipográfica, sombras, gradientes, tinta de faixa por app e
  duração e curva de movimento. Tudo é token, e `legado.css` não muda (sai na 10b).
- `src/components/landing/*`. Um componente novo de moldura de aparelho
  (`src/components/landing/Aparelho.astro`, nome a confirmar pelo `site-ux`) é o único lugar da
  moldura: o Hero, as Funcionalidades e a Home o consomem, sem copiar marcação.
- `src/components/Home.astro`, `src/components/ListaApps.astro` e `src/components/VerTodasApps.astro`
  (Home de estúdio, com os apps numa seção de portfólio). A partição D12 e a ordem de
  `ORDEM_APPS` ficam como estão: o §20 do `check_site.py` confere os `<article>` de `/` e `/en/`, e
  este WP não muda `tools/*.py`.
- `src/components/paginas/PaginaHome.astro`, `PaginaLottoExpert.astro` e `PaginaEclipseGo.astro`.
- `src/layouts/Base.astro`, só se o movimento precisar de um script inline (ver "Movimento").
- `src/i18n/home.ts`: `hero_title` e `hero_desc`, as áreas de domínio e o título da seção de
  portfólio, em pt e en, depois da escolha ou da aprovação do usuário.
- `src/i18n/lottoexpert.ts`: só a tabela de planos (quais linhas aparecem e o rótulo de "ver
  tabela completa"), pt e en.
- `src/i18n/landing.ts`: só o rótulo de interface de "ver tabela completa", se ele for do template.
- `src/assets/img/**`: só se a moldura pedir variante de tamanho da mesma captura. Nenhuma captura
  nova sai deste WP (D26).
- `tools/fixtures/sem-polyfill/*`, regenerada pelo ADR-008 §7 quando o CSS muda.
- `tools/orcamento-lighthouse.json`: só com autorização do usuário, registrada aqui, com o
  número medido.
- `design/REVISAO-VISUAL.md`: seção 7 nova, "Direção aprovada". Ela registra o que o usuário aprovou,
  com a data e a captura de referência, e passa a ser a referência do `site-ux` AUDITAR onde
  diverge do handoff (D33 (a)).
- `.claude/context/wps/WP-10-redesign-com-o-handoff.md`: só a nota de retomada das fatias.

Fora (até a fatia 4, que as inclui por pedido do usuário): as 10 legais e o `LegalLayout` (entram só se um token global mudar, e aí só para medir o
contraste de novo), o convite e tudo em `public/` (ADR-001, D13), `TopoWalk.astro` e
`PolePosition.astro` (são das fatias 7 e 8 do WP-10, que retomam com a direção nova), `tools/*.py`
e os workflows.

## Desenho (site-arquiteto, 2026-11-24)

**Branch.** O protótipo nasce de `feat/wp-10-fatia-9-lottoexpert`, a página que o usuário viu,
como `feat/wp-30-revisao-visual`. Cada fatia é um commit `WP-30: fatia N — …` e passa no `/verify`.
Depois da aprovação, a branch entra na integração (`feat/wp-08-layout-unico`) pelo fluxo de fatias
de sempre (PR do agente, merge do usuário). A fatia 9 do WP-10 fica nela, parcial, até as capturas
que faltam. Nada vai a `develop` nem a `master` por este WP. O deploy continua sendo o único da D13.

**Uma direção, um lugar.** A direção visual é token (`tokens.css`) e componente (`landing/*`,
`Home.astro`). Uma página não ganha cor, sombra nem gradiente próprio. A variação por app sai de
`data-app` (ADR-008), como hoje: template único com variações por app (D33 (d), mantém a D29). O
grep de cores literais do WP-10 continua sendo critério.

**Moldura de aparelho (D33 (b)).** Só CSS (borda, raio, sombra ou brilho com o acento), em volta
do `<Image>` do `astro:assets`. A moldura não recorta nem cobre o conteúdo da captura. A barra de
status pode ficar escondida atrás do recorte, o que é recorte de apresentação, não edição do
arquivo: ela continua na captura e o `alt` não muda. Nenhum PNG ou SVG de aparelho de terceiros.

**Movimento (D33 (f)).** Vale a ordem de preferência abaixo:
1. Só CSS (`transition` no hover e no foco).
2. Aparecer ao rolar com `animation-timeline: view()`, como melhoria progressiva. Abaixo do piso do
   ADR-008, que é o Safari 16.4, ou sem suporte, o conteúdo aparece parado.
3. Se a opção 2 não bastar, um script inline único em `Base.astro` (`IntersectionObserver`, sem
   biblioteca, ≤ 1 KB).

O conteúdo é visível sem JS: a classe que esconde só é posta pelo próprio script. Com
`prefers-reduced-motion: reduce`, não há animação. Nada anima a imagem do LCP, e o CLS segue ≤ 0,1.

**Hero da Home (D33 (c)).** O h1 apresenta a GHF Software como estúdio de engenharia e não fala
dos apps. Antes do `site-dev`, o `site-ux` traz de 3 a 5 opções de h1. Cada opção cita a fonte: a
correção do usuário acima, `since_2004`/`hero_desc`/`about_p1Html` em `src/i18n/home.ts`, ou
`footer_desc` em `src/i18n/ui.ts` (D25). O usuário escolhe ou reescreve, e a resposta vai para este
WP. O en é tradução fiel no mesmo commit (ADR-007). Sem resposta, o h1 atual fica e a fatia 1
fecha o resto. Faixa de logos de tecnologia não entra: a D30 (2) a tirou, e voltar com ela é
pedido do usuário, com o logo servido pelo site (ADR-006).

**Tabela do LottoExpert (D33 (e)).** O `site-ux` propõe de 6 a 8 linhas das 20 que existem
(`lottoexpert.ts:163-184`), e o usuário escolhe quais. Escolher o que destacar é decisão de produto.
O resto fica em `<details>` ("ver tabela completa"), sem JS. As 20 linhas continuam no HTML, pela
busca e pelo leitor de tela. O rótulo vem do `content/i18n.js` do export (D25). Se ele não tiver o
rótulo, o texto é pergunta ao usuário. Nenhuma linha muda de texto.

**i18n.** Todo texto novo nasce em pt e en no mesmo commit. O layout é provado com o en, o mais
longo dos dois hoje, e sem largura fixa para texto (`BRIEF.md` §7).

## Fatias

1. **Direção e Home.** O `site-ux` DESENHA: paleta ampliada (faixas tingidas por app, gradiente do
   hero), escala tipográfica com contraste entre h1, h2, h3 e corpo, ritmo de seções (fundo base,
   superfície e faixa tingida, alternados), a moldura e o movimento. Também traz as opções de h1 e a
   redação das áreas de domínio. O `site-dev` aplica a direção nos tokens, na moldura e na Home. A
   Home fica nesta ordem:
   - hero do estúdio, com a cor da marca GHF e sem acento de app;
   - áreas de domínio, com o "momento" da página;
   - seção de produtos/portfólio com os 4 apps (cor, frase de origem e, se houver captura real no
     repositório, a tela na moldura; sem captura, ícone e cor, sem inventar tela, D26);
   - Sobre e Privacidade.

   **Aprovação 1:** o usuário vê a Home em `localhost:8080` (`python3 -m http.server 8080 -d dist`).
2. **LottoExpert.** A direção vai para o template (`landing/*`), e o LottoExpert é a primeira
   página a mostrá-la. O hero ganha tinta do violeta, a moldura entra em volta da captura da Home
   do app e o destaque sem imagem deixa de ter metade vazia. "Como o app trabalha" ganha número ou
   ícone, e o CTA final ganha faixa própria. A tabela fica resumida. Pelo menos um "momento"
   (critério 3). **Aprovação 2:** o usuário vê `/lottoexpert.html` e `/en/lottoexpert.html`.
3. **Propagação.** O EclipseGo recebe a direção pelo template (só o que o template já entrega, sem
   ajuste próprio). A seção 7 de `design/REVISAO-VISUAL.md` registra a direção aprovada, e a nota
   de retomada vai para o WP-10. **Aprovação 3:** o usuário vê `/eclipsego.html` em pt e en.

   **Aprovações 2 e 3 (2026-11-24):** o usuário viu `/lottoexpert.html`, `/eclipsego.html` e a
   Home depois das correções da auditoria (commit `9cfec02`): "ok, agora ficou bom, aprovado".
4. **Páginas legais (acrescentada em 2026-11-24, pedido do usuário: "não vai ter ajuste no layout
   dos termos e política também?"; resposta ao questionário: "Topo escuro + corpo claro").** As 10
   legais (5 documentos × pt/en) ganham o cabeçalho escuro com o glow do acento do app (ícone,
   título, data), no padrão das landings; o corpo continua no papel claro, que é o melhor para
   texto longo; o sumário e os números das seções usam o acento do app. **O texto legal não muda
   em nada** (`check_site.py` §4 e `sync_legal.py --check` provam). Arquivos: `src/layouts/
   LegalLayout.astro`, `src/styles/tokens.css` (só se faltar token), `src/components/paginas/
   Pagina*Privacy.astro`/`*Terms.astro` (só se o cabeçalho morar nelas). URLs contratuais
   (ADR-001) intactas: só a apresentação muda. **Aprovação 4:** o usuário vê uma legal de cada app
   em pt e en.

Depois da fatia 4, este WP fica `done`. As fatias 7 (TopoWalk), 8 (Pole Position) e 9 (LottoExpert,
com as capturas que faltam) e a 10b do WP-10 retomam com a direção nova. A 10b é a primeira a
medir as legais se um token global tiver mudado.

**Prazo (D33 (g)):** se a aprovação 2 não sair em ~1 semana (até ~2026-12-01), o usuário revê o
prazo do deploy único (nota na D13). O agente não corta escopo por conta própria.

**Passos (por fatia):** `site-ux` DESENHAR → perguntas de copy ao usuário (fatias 1 e 2) →
`site-dev` → `/verify` → `python3 tools/lighthouse.py` → aprovação do usuário no navegador →
commit → auditoria em paralelo (`site-ux` AUDITAR, `site-qa`, `site-seo-perf`) → `site-docs`.

**Critérios de aceite:**
- `npm run build` e `python3 tools/check_site.py` verdes, e o §5 (jogo responsável) também sobre o
  `alt` e o texto novo.
- `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` verde: o convite, o `assetlinks`, o
  `og:image` do convite e o `CNAME` ficam iguais.
- `npx html-validate 'dist/**/*.html'`, `npm run test:css` e
  `python3 -B -m unittest tools/test_regras_i18n.py tools/test_regras_apps.py` verdes.
- Grep de cores literais vazio:
  `grep -rnE "#[0-9a-fA-F]{3,6}\b|rgb\(" src/ | grep -v -e src/styles/tokens.css -e src/styles/legado.css`.
- `tools/lighthouse.py` (mobile, mediana de 3) em `/`, `/en/`, `/lottoexpert.html` e
  `/eclipsego.html`: desempenho ≥ 95, acessibilidade 100 e LCP < 2,5 s (piso deste WP, mais
  alto que o `performance_erro` 0,85 do orçamento), CLS ≤ 0,1 e orçamento de bytes cumprido (ou
  aumentado com autorização registrada aqui).
- Tabela de contraste do `site-ux` (Chrome headless) com todo par novo (faixa tingida, gradiente,
  texto sobre o hero) ≥ 4,5 para texto e ≥ 3 para texto grande, controle e foco. Sobre gradiente,
  a medida é o pior ponto.
- Sem requisição a outra origem (a regra do `tools/lighthouse.py`). Nenhum pacote novo no
  `package.json`.
- `grep -o "<tr" dist/lottoexpert.html | wc -l` igual ao de antes da fatia 2 (21 em 2026-11-24:
  cabeçalho + 20 linhas; o mesmo em `dist/en/lottoexpert.html`): a tabela completa continua no HTML.
- Nenhuma frase nova sem origem: cada texto novo cita a fonte ou a resposta do usuário neste WP (D25).

**Só no navegador** (o usuário reporta; sem o relato a fatia não fecha):
- `/` e `/en/` a 360, 768 e 1280, e a 1280×720. Quem chega entende, sem rolar, que a GHF Software é
  um estúdio de engenharia, e o h1 não fala dos apps. As áreas de domínio aparecem como um
  "momento" da página. Os apps estão numa seção de portfólio, cada um com cor e frase, e não
  dominam a página. O hero tem impacto, e a página não acaba na primeira dobra.
- A Home não cita nome de repositório interno ou privado.
- `/lottoexpert.html` e `/en/lottoexpert.html` a 360, 768 e 1280: o violeta é reconhecível em 1
  segundo e reaparece em pelo menos 2 momentos. A captura aparece na moldura e o conteúdo dela está
  inteiro. O CTA da Play fica acima da dobra a 1280×720. "Ver tabela completa" abre e fecha pelo
  teclado.
- `/eclipsego.html` e `/en/eclipsego.html` a 360 e 1280: a direção chegou sem regressão no hero
  com foto.
- Com "reduzir movimento" ligado no sistema, nada anima. Com o JS desligado, todo o conteúdo
  aparece.
- Foco visível em tudo que é interativo, e nenhum texto en estourado ou truncado.

**Risco:** médio. Não toca URL contratual, deploy nem texto legal. Riscos específicos:
- Gradiente e sombra derrubam o contraste do texto sobre o hero.
- Moldura e movimento pesam no LCP ou no CLS e derrubam o desempenho abaixo de 95.
- O "aparecer ao rolar" esconde conteúdo sem JS ou do crawler.
- A frase nova do hero, as áreas de domínio ou o rótulo da tabela entram sem origem (D25).
- A Home volta a falar dos apps no hero, contra a correção do usuário.
- A aprovação demora e empurra o deploy único (D13, D33 (g)).
