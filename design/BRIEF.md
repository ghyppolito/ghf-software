# Brief de design — ghfsoftware.com

Brief para o Claude Design (claude.ai/design). Escrito pelo agente `site-ux` no WP-06; a decisão
visual é do humano (D4). O export da sessão entra em `design/handoff/<AAAA-MM-DD>/` e passa a
prevalecer sobre o HTML atual. Este documento descreve o que existe, o que precisa ser resolvido
e o que fica aberto. Não fixa estilo.

Fontes: `docs/AVALIACAO.md` §2 item 7 e §3.3; `index.html` e as landings; `docs/*_README.md`;
`../lotto-expert/docs/ASO_METADATA.md`; ADR-001 e ADR-002; decisões D4 e D8.

---

## 1. Marca e tom

**GHF Software** — soluções de engenharia, **privacy-first**. Software desde 2004, hoje quatro
apps Android. Os apps resolvem problemas técnicos de nicho (topografia, telemetria, loterias,
astronomia) e rodam, em geral, no próprio aparelho, sem conta nem rastreador.

Tom:
- **Técnico e direto.** Fala de números, método e o que o app faz. Sem superlativos, sem "revolucionário".
- **Honesto sobre limites.** Funciona offline? Diz. Tem versão paga? Diz o que muda.
- **Privacidade dita em uma frase, com link** para a política. Nunca em parágrafo de marketing.
- **Sem promessa.** No LottoExpert, jogo responsável: nada de "aumente suas chances", "maximize",
  "garantia de prêmio". O app garante só a matemática provada do fechamento. `tools/check_site.py` barra esses termos.
- Português é o idioma primário; inglês é espelho completo da página. O design não pode assumir que o inglês é mais curto.

O site é o lugar para onde a Play Store, o convite de bolão e o "Sobre" do app mandam as pessoas.
Quem chega quer o app certo, a política de privacidade ou o convite. Ninguém chega para conhecer a empresa.

## 2. Os quatro produtos

Cores abaixo são as que cada landing já usa como `brand.primary` — exceto o TopoWalk, que mantém o
esmeralda `#10B981` como primária e usa o terracota como `accent` (fundo `#0B1120` e superfície `#111827` iguais em todas).
O designer pode propor outra por app, mas precisa justificar a troca e garantir contraste.

| App | Público | Proposta em uma linha | Cor de identidade hoje |
|---|---|---|---|
| **TopoWalk** | Topógrafos, agrimensores, engenheiros e técnicos de campo; produtor rural | Levantamento topográfico no celular, com GPS e barômetro: área, declividade, desnível, exporta PDF, GeoJSON, KML e GPX | Terracota `#B5541C` como accent (400 `#D97736`, 600 `#8C3F11`, 900 `#4A2109`); primária esmeralda |
| **LottoExpert** | Apostadores de loterias da Caixa e organizadores de bolão | Scanner de bilhetes, fechamentos, gestão de bolão e resultados oficiais | Violeta `#8B5CF6` (hover `#7C3AED`) |
| **Pole Position** | Pilotos de kart e automobilismo amador | Telemetria e análise de sessão 100% offline, alternativa a hardwares como MyChron e Alfano | Lima `#84CC16` (hover `#65A30D`, accent `#A3E635`) |
| **EclipseGo** | Quem quer saber se um eclipse é visível de onde está | Mostra se um eclipse solar ou lunar é visível em um local, com horários de início, pico e fim; 100% offline | Dourado `#EAB308` (hover `#CA8A04`; secundária índigo `#6366F1`) |

Fatos de produto a respeitar (não reescrever):
- TopoWalk: sem anúncios; núcleo gratuito; **Pro** é compra única, sem assinatura. Landing e política em 7 línguas (pt, en, es, fr, it, de, ru).
- Pole Position: landing e política em 6 línguas (pt, en, es, fr, it, de).
- LottoExpert: freemium com planos Mensal, Anual e Vitalício; landing hoje tem ~17 funcionalidades, tabela de comparação e preços. LottoExpert e EclipseGo ficam em pt/en (D8).
- Os "públicos" de TopoWalk e EclipseGo acima são inferidos do README; confirme com o usuário se algo destoar.

A cor de cada app deve funcionar como **acento dentro do sistema do site**, não como quatro temas independentes.
Hoje o `primary` de cada landing troca e o resto do site é verde (`#10B981`), o que fragmenta a marca.
Os favicons e mockups em `assets/` são a referência da identidade de cada app (ver seção 6).

## 3. Hierarquia da home

Problema (AVALIACAO §3.3): o visitante chega **pelo app**, e a home hoje fala da empresa. Os quatro cards
têm o mesmo peso e o hero fala de "engenharia de ponta", não do que o visitante procura.

O que a home precisa fazer:
- **Em um toque, o visitante chega ao app certo.** Os quatro apps aparecem acima ou logo na dobra do hero, não depois de "Sobre Nós".
- Hero curto: marca em uma linha + a escolha entre os apps. Sem carrossel, sem vídeo que atrase o LCP.
- Card de app (componente único): ícone/favicon, nome, a linha de proposta, selo de estado (publicado / em breve), um alvo principal (a landing do app) e, secundário, o link da Play.
- Ordem dos apps: **decisão do humano** (ver seção 9). Hoje os cards aparecem na ordem Pole Position, TopoWalk, LottoExpert, EclipseGo; os quatro estão publicados na Play (o estado "em breve" serve a apps futuros).
- Depois dos apps: "Sobre" em um bloco curto, contato e privacidade. É conteúdo de apoio, não é o foco.
- Contato: `support@ghfsoftware.com`, YouTube e Instagram (já existem no footer).

## 4. Anatomia de landing de app (única, igual para os 4)

Hoje cada landing tem estrutura própria (a do LottoExpert é a maior, a do TopoWalk usa outro conjunto de cores).
Pedido: **um só esqueleto**, com a cor do app como acento.

Ordem das seções:
1. **Hero** — nome, proposta em uma linha, **um único botão primário** (Google Play), mockup do app. Nada compete com o botão acima da dobra.
2. **Funcionalidades** — 3 a 5 destaques com imagem real (screenshot, não ícone genérico). O restante (o LottoExpert tem ~17) vai para "ver todas", tabela ou página colapsável, não para um mural de 17 cards.
3. **Screenshots** — galeria ou carrossel sem JS de framework, com `alt` descritivo.
4. **Prova** — números, avaliações, nota na Play. Só entra o que for verdadeiro e atualizável; se não houver, a seção some em vez de inventar.
5. **Privacidade em uma frase + link** para a política do app.
6. **FAQ** — perguntas reais do app (offline? tem anúncio? o que o Pro acrescenta?).
7. **CTA final** — o mesmo botão da Play do hero.
8. **Links legais** no footer: política de privacidade (todos), termos de uso (LottoExpert).

Específico por app, dentro do mesmo esqueleto:
- **LottoExpert:** seção de planos/preços e tabela de comparação (Grátis, Mensal, Anual, Vitalício) como bloco opcional entre prova e privacidade. Aviso de jogo responsável visível no rodapé da landing e perto de qualquer CTA de preço. Nenhum elemento visual sugere prêmio ou sorte (trevo, moedas caindo, selo de "ganhe"): a imagem do app é de método e organização. Tem também a página do convite de bolão (`/lotto-expert/sweepstake-invite/lottoexpert-invite.html`), que deve usar o mesmo sistema.
- **TopoWalk:** bloco "grátis x Pro" (Pro: DXF/CSV, PDF com identidade da empresa, locação).
- **Pole Position e TopoWalk:** seletor com todas as línguas da página (6 e 7).
- **Estado "em breve"** (app futuro, sem URL da Play): variação do hero sem botão quebrado. Hoje os quatro apps estão publicados.

## 5. Página legal legível

Política de privacidade e termos são **espelho do app**. O texto legal não é redigido nem alterado pelo site; o design só apresenta.
O design define tipografia, largura de leitura, sumário e lugar da data — não define texto, ordem nem agrupamento de cláusulas.
Use o texto real (`docs/LOTTOEXPERT_PRIVACY_POLICY.md`) como amostra no mockup.
As páginas são longas (a política do LottoExpert tem ~27 KB; a do TopoWalk, ~37 KB) e hoje o texto está numa caixa "glass" com cabeçalhos numerados.

Pedido:
- **Tipografia de leitura longa:** largura de ~65–75 caracteres, entrelinha confortável, hierarquia h1 / h2 / h3 clara (as seções são numeradas: 1., 4.1, 4.2…).
- **Sumário** navegável (lateral no desktop; colapsável no topo no mobile) com âncoras para as seções.
- **Data de "Última atualização" e identificação do app** no topo, em destaque. A data é a mesma do `.md` de origem (conferida por `check_site.py`).
- **Troca de idioma sem perder a posição** na página; pt e en têm o mesmo conteúdo. TopoWalk e Pole Position terão mais línguas nas políticas (D8).
- Aviso de que, em divergência, **prevalece a versão em português** (cláusula que nasce no repositório do app, D8). O design reserva um lugar para esse aviso; não redige o texto.
- Links internos e para a Play legíveis; tabelas (se houver) com rolagem horizontal em 360 px.
- Impressão: a página tem de imprimir sem o nav e sem fundo escuro.

## 6. Tokens atuais, o que preservar e o que resolver

**Existe hoje** (`index.html:43–70`, replicado e alterado em cada página):
- Tema escuro único: `base #0B1120`, `surface #111827`, texto `#F3F4F6`.
- Marca: `primary #10B981` (esmeralda), `primaryHover #059669`, `secondary #3B82F6`, `accent #06B6D4`.
- Fonte **Inter** (300–800), via Google Fonts.
- Sombras de brilho (`glow` verde, `glow-blue`), painel "glass" com blur, texto em gradiente azul→verde, fundo "tech-grid" com grade de 40 px, animação flutuante.
- Ícones Font Awesome via CDN.

**Preservar** (salvo decisão contrária do humano):
- O **logo** `assets/GHFSoftware.png`.
- Os **mockups e screenshots** de cada app em `assets/` (`lottoexpert_app_mockup.png`, `poleposition_dashboard_mockup.png`, `poleposition_real_mockup.png`, `topowalk_screenshot.png`, `eclipsego_screenshot.png`, `eclipsego_phone_screen.png`, entre outros) e os **favicons** (`topowalk_favicon.png`, `lottoexpert_favicon_v3.png`, `poleposition_favicon.png`, `eclipse-go-favicon.png`). O designer pode propor o enquadramento (moldura de aparelho, sombra), mas não redesenha os apps.
- A família Inter, a menos que o designer justifique outra (ver seção 9).

**Resolver** (AVALIACAO §3.3, independente do estilo):
- Hierarquia da home (seção 3).
- Uma só anatomia de landing (seção 4).
- Página legal legível (seção 5).
- **Tokens semânticos:** fundo, superfície, texto (primário/secundário/mudo), borda, primária, cor por app, sucesso/erro/aviso; escala tipográfica; espaçamento em múltiplos de 4 pt; raio; sombra; **foco visível**. Hoje as classes são utilitárias soltas e `brand.primary` muda por página.
- **Contraste:** o texto cinza `text-gray-400` sobre `#0B1120`, o lima, o dourado e o violeta como texto ou botão (e o texto sobre botão colorido) precisam ser verificados em AA; o terracota `#B5541C` sobre fundo escuro provavelmente não passa e precisa de variante. O designer informa as razões.
- **Estados:** app "em breve" vs publicado, página en incompleta, imagem ausente.
- Muita decoração (glass, glow, gradiente, grade, flutuação) compete com o conteúdo; avalie o que fica.

## 7. Restrições

Técnicas (ADR-001, ADR-002, D8):
- **Site estático no GitHub Pages**, gerado com **Astro** sem framework JS (sem React/Vue/SPA). Todo componente é HTML + CSS; interação mínima (seletor de idioma, menu mobile, galeria, FAQ) com CSS ou JS leve, sem dependência. Tokens têm de ser expressáveis como variáveis CSS.
- **Sem rastreador** e sem cookie banner. Medição, se houver, é sem cookie (D3, em aberto). Nada de fonte ou ícone que dependa de CDN de terceiros no desenho final: o designer deve supor fontes e ícones **servidos pelo próprio site** (SVG inline/sprite).
- **URLs contratuais não mudam** (ADR-001): `/lottoexpert-privacy.html`, `/lottoexpert-terms.html`, `/topowalk-privacy.html`, `/poleposition-privacy.html`, `/eclipsego-privacy.html`, o convite do bolão e `/.well-known/assetlinks.json`. O design não renomeia, junta nem move essas páginas; navegação nova só aponta para caminhos que já existem.
- Peso: imagens otimizadas (WebP/AVIF); o design não pode exigir vídeo ou animação pesada.

Acessibilidade e responsividade:
- **WCAG AA:** contraste 4,5:1 (texto) e 3:1 (texto grande e componentes); foco visível em tudo que é interativo; **alvo de toque ≥ 44 px**; um `h1` por página, `h2` por seção; `alt` descritivo; `prefers-reduced-motion` respeitado.
- **Mobile primeiro**, verificado em **360, 768 e 1280 px**. O visitante quase sempre vem da Play, no celular.
- **i18n:** línguas de 2 a 7 por página. Alemão e russo podem ocupar **~35% mais** que o português; botões, nav, cards e tabelas não podem estourar nem truncar, nem ter largura fixa para o texto. A fonte escolhida precisa cobrir latin-ext e **cirílico** (russo no TopoWalk). Seletor de idioma deve comportar 7 línguas e uma faixa de sugestão por idioma do navegador (`navigator.languages`), sem redirecionamento (D8 c1).

**Em aberto, o brief não decide:**
- **Tema escuro.** O site hoje é só escuro. O designer pode manter só escuro, propor claro, ou claro + escuro. A escolha é do humano (seção 9). Páginas legais costumam ler melhor com fundo claro; avalie.

Copy:
- LottoExpert: **jogo responsável**. Sem "aumente suas chances", "maximize", "garantia de prêmio" nem equivalentes, em nenhum texto de exemplo do design. Se o designer escrever placeholder, use texto neutro ou o real dos `docs/*_README.md`.
- Use a copy real das fichas (`docs/*_README.md`, ASO) como conteúdo. Não invente números, avaliações ou depoimentos.
- **Todo texto do export é placeholder.** Na implementação (WP-10), a copy vem do README/ASO de cada app e o texto legal do repositório do app — nunca do export.

## 8. O que o export precisa conter

Lista de entregáveis para `design/handoff/<data>/`. Se algo não couber, diga o que ficou de fora.

1. **Tokens:** cor semântica (fundo, superfície, texto, borda, primária, por-app, estados), tipografia (família, escala, pesos, entrelinha), espaçamento (4 pt), raio, sombra, foco. Em formato que o `site-dev` consiga transcrever para CSS/Tailwind.
2. **Nav**, com o **seletor de idioma** (2 e 7 línguas), a faixa de sugestão de idioma e menu mobile.
3. **Footer** (marca, contato, links legais por app, redes).
4. **Hero da home**, com os 4 apps.
5. **Card de app** (publicado, em breve).
6. **Bloco de feature** (imagem + título + texto).
7. **Landing completa de um app** (sugestão: LottoExpert, a mais complexa) seguindo a seção 4, e como as variações dos outros três mudam só o acento.
8. **Página legal** completa, com sumário, data e troca de idioma.
9. **Página 404.**
10. **Estados** de botão e link: normal, hover, foco, ativo, desabilitado; mais estados de dados: em breve, imagem ausente, idioma incompleto.
11. **Variações mobile (360) e desktop (1280)**, e tablet (768) onde o layout mudar.
12. Opcional: o convite de bolão (`lottoexpert-invite.html`) como página pequena do mesmo sistema.

O export é versionado no repositório e, enquanto o Pages publicar em modo branch, fica público em
`ghfsoftware.com/design/...` — inclusive `uploads/`. Não envie ao Claude Design nada que não possa ser público.

## 9. Perguntas ao designer e decisões que ficam com o humano

Perguntas ao designer (responder no export):
- Qual escala de contraste cada acento de app atinge sobre o fundo escolhido (texto e botão)? Qual ajuste mantém AA?
- A cor do acento de cada app bate com o favicon e o ícone dele? Se não, qual muda?
- Como cada componente se comporta com texto ~35% maior (de/ru) em 360 px?
- Como o CTA da Play se apresenta para o app "em breve"?
- Que elementos decorativos do site atual (glass, glow, grade, flutuação) ficam, e por quê?
- Qual a regra de quando uma funcionalidade vai para o destaque e quando vai para "ver todas" (LottoExpert tem ~17)?

Decisões do humano (o designer propõe, o usuário decide) — **respondidas na seção 10**:
- **Ordem e peso dos 4 apps na home** (por data de publicação, por público ou todos iguais mas navegáveis em um toque).
- **Tema:** só escuro, só claro ou ambos.
- **Fonte:** manter Inter ou trocar.
- **Acento por app:** manter as cores atuais ou redefinir; e se o verde esmeralda continua como cor da marca GHF.
- **Prova:** quais números e avaliações podem aparecer (precisam ser reais e mantidos).
- **Medição** (D3): o design reserva ou não um aviso de privacidade sobre ela.
- Se o designer não puder resolver algo, devolva como "sem referência no handoff" e o humano decide. O `site-ux` não inventa o que o handoff não cobre.

## 10. Decisões do humano (2026-10-13, depois da rodada 1)

Respondem a seção 9. Prevalecem sobre o que as seções 1–8 deixavam em aberto; o handoff
`design/handoff/2026-10-13/` (rodada 1) é a base.

- **Direção:** A "Navy técnico" do export — fundo `#0B1120`, superfície `#111827`, botão em pílula.
- **Tema:** escuro; páginas legais em papel claro (tokens de papel da direção A).
- **Fonte:** Inter, servida pelo próprio site (latin-ext e cirílico), algarismos tabulares em números.
- **Marca GHF:** ciano dos nós do logo (`#3CC8D0` no export). O esmeralda `#10B981` sai do sistema.
- **Acentos por app** (paleta do export, exceto LottoExpert):
  - LottoExpert: **violeta**. `#A78BFA` sobre o escuro (6,9:1); `#6D28D9` sobre o papel (6,6:1). O
    ouro da rodada 1 sai: com o trevo do ícone, reforçaria a ideia de sorte e prêmio.
  - Pole Position `#5FD47E`, TopoWalk `#E38A57`, EclipseGo `#EE737D`, com as variantes para papel da rodada 1.
- **Ordem dos apps**, em toda lista (home, footer, menus): LottoExpert, TopoWalk, Pole Position,
  EclipseGo — mesmo peso visual, sem card de destaque.
- **Prova:** sem números de downloads nem nota por enquanto; fatos verificáveis do produto. O
  componente "nota na Google Play" fica desenhado como opcional.
- **Ano da empresa:** **desde 2004**. O logo atual diz "since 1996" e precisa de nova versão
  (também uma para fundo escuro) — achado `LOGO-ANO-E-FUNDO-ESCURO-01`.
- **Ícone do LottoExpert (trevo):** o site usa o ícone oficial como está (identidade do app na
  Play); nada além dele remete a sorte.
