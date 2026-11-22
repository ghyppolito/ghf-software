---
id: WP-10
titulo: A home e as landings de app seguem o sistema visual do handoff
area: design
status: doing
depende_de: [WP-06, WP-08]
adr: [ADR-001, ADR-004, ADR-006, ADR-007, ADR-008]
spec: docs/AVALIACAO.md
decisoes: [D4, D11, D12, D24, D25, D26, D27, D29, D30]
tamanho: L
risco: medio
visual: true
branch: feat/wp-10-fatia-6-home
---

# WP-10 — A home e as landings de app seguem o sistema visual do handoff

**Depende de:** WP-06 (handoff), WP-08 (componentes únicos) · **Achados roteados:** ECLIPSE-ICONE-OFFLINE-01 (ícone do card "offline" do EclipseGo, D21), POLE-PRINTS-2X-01 (do WP-12) · o WP-19 (rodada 3) está `done` e não segura mais as landings

**Objetivo:** tokens do handoff em `src/styles/tokens.css` (`@theme`, ADR-008); home com hierarquia por app (um
toque até o app certo); as 4 landings com a mesma anatomia (hero + CTA → 3–5 funcionalidades
com imagem real → prova → privacidade em uma frase → FAQ → CTA); página legal legível (largura
de leitura, sumário, data no topo).

**Contexto:** `docs/AVALIACAO.md` §2 item 7 e §3.3.

**Ler antes:** `design/README.md` (mapa do handoff) e só os componentes do handoff que a
página usa; `docs/AVALIACAO.md` §3.3.

**Arquivos-alvo:** fatia 1: `package.json`, `package-lock.json`, `astro.config.mjs`,
`postcss.config.mjs` e `tailwind.config.mjs` (removidos), `src/styles/**`,
`tools/orcamento-lighthouse.json`, e as linhas que citam `tailwind.config.mjs` como origem do tema
(`CLAUDE.md:142`, `docs/ARQUITETURA.md:19`). Todas as fatias: `src/components/**`, `src/layouts/**`,
`src/pages/**` (pt e en), `src/assets/img/**` (imagens novas, pelo `astro:assets`; ADR-006 e
`check_site.py` §13 proíbem imagem exibida em `public/`), `src/i18n/**`, `src/styles/tokens.css` e
`tools/fixtures/sem-polyfill/*` (regenerada pelo ADR-008 §7 quando o CSS muda). Fatia 2:
`tools/check_site.py` (§19, o rodapé com as 5 URLs legais). Fatia 3: `tools/check_site.py` §12. O convite fica de fora (ver "Plano").

**Passos:** por página: `site-ux` DESENHAR (referência no handoff, estados) → `site-dev` →
`/verify` → auditoria (`site-ux` AUDITAR + `site-qa` + `site-seo-perf`). Home depois do template
de landing (fatia 5, com o EclipseGo; D29), sem esperar as outras landings: os cards de TopoWalk,
Pole Position e LottoExpert leem o resumo de cada app da mesma fonte que a landing dele (hoje
`src/i18n/home.ts`), e mudam sozinhos quando as fatias 7 a 9 entrarem (ver "Plano"). Depois da
Home vem a 10a; as landings em evolução (7 a 9) vão para o fim, antes só da 10b (D29, complemento
de 2026-11-22).

**Critérios de aceite:**
- Tokens: nenhuma cor literal (`#…`, `rgb(`) em `src/` fora do arquivo único de tokens
  (`grep -rnE "#[0-9a-fA-F]{3,6}\b|rgb\(" src/ | grep -v src/styles/tokens.css` vazio). O
  critério antigo excluía `tailwind.config.mjs`, que fica fora de `src/`, e reprovaria os valores
  de tema que hoje vivem em `src/styles/global.css`.
- Cada landing tem exatamente as seções da anatomia, na ordem (`site-ux` AUDITAR confere
  contra o handoff e lista desvios com justificativa).
- Contraste AA em todo texto (relato do `site-ux` com os pares cor/fundo medidos).
- `check_site.py` verde; Lighthouse Accessibility ≥ 95 em todas as páginas.

**Nota do WP-09 (2026-10-15, `LOTTO-EN-ESPELHO-AUSENTE-01`):** a página legal do redesign consome
`src/content/legal/` (pt copiado do commit do app por `tools/sync_legal.py`, en traduzido; ADR-004),
não o stub legal do export do Claude Design — o export não é origem de texto legal (D7).

**Só no navegador:** todas as páginas, 360/768/1280, pt e en, contra o handoff.

**Risco:** médio — visual. Sem handoff (WP-06 não feito), D4 (B) muda o WP: a referência passa
a ser `docs/AVALIACAO.md` §3.3 e o `site-ux` decide mais do que deveria — registrar.

## Plano (site-arquiteto, 2026-11-21)

**Branch.** `feat/wp-10-redesign` é a integração do WP-10. Ela nasceu de `feat/wp-08-layout-unico`
e volta para ela. Cada fatia nasce dela (`feat/wp-10-fN-<slug>`), passa no `/verify` e volta por
`git merge --no-ff` com a mensagem `WP-10: fatia N — …`, igual ao WP-08. Assim cada fatia é um
merge revertível (`git revert -m 1`). O CI roda pelo PR rascunho #37 da integração (D13), depois
que a integração recebe o merge de `feat/wp-10-redesign`. Para ter CI a cada fatia, abra um PR
rascunho `feat/wp-10-redesign → develop` com o título `[NÃO FAZER MERGE — D13]`.

**Fora do WP-10: o convite** (`CONVITE-REDESIGN-CONTRATO-01`, agora no WP-24). O WP-10 entra no deploy único, e a
D13 congela os bytes do convite até esse deploy (`tools/contrato.sha256`, conferido no `pr.yml` e
no `deploy.yml`). Um convite redesenhado aqui reprova o próprio deploy. O redesenho é o WP-24
(resposta 6, 2026-11-21), que depende do WP-23 e sai num `/release` próprio depois do deploy único,
com o parse de `?d=` intocado, os `og:*` preservados e o teste com link real.

**Fora do WP-10 também:** o card "em breve" (`GHF Kit v3` §5), porque nenhum app está em breve. E o
sinal visual do link de fallback de língua (`LINK-FALLBACK-IDIOMA-SEM-SINAL-01`), porque hoje toda
página tem pt e en e nenhum link cai na D23. O achado foi para o WP-16, o primeiro que publica uma
língua a mais.

**Regra de copy em todas as fatias (D25, resposta 2).** A copy do export é placeholder. Cada frase vem do
dicionário publicado (`src/i18n/*.ts`), do README/ASO do app ou de uma resposta do usuário. Frase
sem origem fica fora da página. Quando a página e a ficha da Play divergem, vale a ficha (D19 a).
Rótulo de interface (sumário, "ver todas", seletor) vem de `content/i18n.js` do export. O en de
cada frase nova é tradução fiel, na mesma fatia (ADR-007). Uma fatia sem en não fecha.
**Alerta:** o §5 do `check_site.py` (`tools/check_site.py:195`) reprova também a negação. "ele não
aumenta suas chances reais de ganhar" (`../lotto-expert/docs/LottoExpertContent.md:389`) tem origem e
reprova a página se copiado literal; o mesmo vale para "doesn't increase your chances" (`:198`). O
padrão não se afrouxa. Se a única fonte da frase dispara o §5, a redação é pergunta ao usuário.
**Imagens (D26, resposta 3):** uma captura real do app por funcionalidade em destaque, 3 a 5 por
landing, fornecida pelo usuário, em `src/assets/img/<app>/`. Sem mockup e sem ilustração do export.
**768 (D27, resposta 4):** home e landing usam o fluido do export; nav e footer, o ramo `t`. A
prova é o checklist de navegador.

### Fatias

1. **Stack e tokens** — **feita em 2026-11-21** (commits c2e2de8, 837d483, ee0ea3e, eb52fbe; o `/verify` e a auditoria de `site-qa`, `site-seo-perf` e `site-ux` passaram; resta o checklist de navegador, que é do usuário). (D24 A, ADR-008, que substitui o ADR-003). O Tailwind 4 entra pelo
   `@tailwindcss/vite`, e os tokens ficam em `@theme`. Os tokens vêm do `GHF Kit v3` (inclusive
   `--border-strong` #66738D) e da D11 (`--success` e `--success-surface`). Também entram
   `--app-acc`, `--app-acc-edge` e `--app-acc-light` por app e os tokens de papel da legal. Tudo
   fica num arquivo só, `src/styles/tokens.css`. Os temas antigos (`[data-tema=…]` em `global.css`)
   ficam como camada de legado até a fatia 10b, para que as páginas ainda não redesenhadas
   continuem montando. O `cssTarget` vai ao piso novo (Safari 16.4, Chrome 111, Firefox 128) e o
   `orcamento-lighthouse.json` é remedido. A paridade das páginas ainda não redesenhadas não é
   critério (ADR-008 §5); o build, o `check_site.py --raiz dist` e o html-validate são.
   **Achados:** `TAILWIND3-NPM-AUDIT-01` (`npm audit` sem os 7 avisos), `SUCCESS-DOIS-VALORES-01`,
   `HOME-BOTAO-EMERALD-CONTRASTE-01` (o esmeralda sai do sistema, brief §10).
   **Bloqueio:** nenhum. **Copy:** nenhuma.
2. **Casca: `Base`, `Nav`, `Footer`, `SeletorIdioma`, `SugestaoIdioma` e um `Logo.astro` novo.** **Feita em 2026-11-22** (commits 8999f11, 872c0ef, 0ee743c; branch `feat/wp-10-fatia-2`). Auditorias de `site-qa`, `site-seo-perf` e `site-ux`: nenhum achado alto; os médios (ordem do foco no rodapé, WCAG 2.4.3; "Pular" saltando o `<h1>` das legais) foram corrigidos. Medidas: rodapé a 360 de 1432 para 871 px, a 768 de 1108 para 687 px (contato em linha própria e coluna ao lado da marca vazia: `RODAPE-ORDEM-M-T-01`, WP-19); LCP de `/` de 2,56 para 2,33 s (o elemento mudou de `<img>` para `<span>`; remedir na fatia 6); orçamento cumprido sem `--medir`; axe sem nó da casca. `/verify` passou (`lychee` só no CI). **Checklist de navegador das fatias 1 e 2 aprovado pelo usuário em 2026-11-22** ("gostei bastante do resultado, passei pelas telas todas", Chrome, pt e en, 360/768/1280): coluna vazia do rodapé a 768 aceita ("pode ficar"); faixa de idioma conferida em inglês. Safari não testado (Linux).
   Ramos 360, 768 e 1280 de `Site Nav` e `Site Footer`. Seletor segmentado PT/EN. Foco visível e
   alvos de 44 px. O logo fica num componente só. Até existir a arte, ele usa o PNG atual. Pela
   WCAG 1.4.3, logotipo não tem exigência de contraste. A troca da arte depois é um arquivo. O
   rodapé não leva "Este site não usa rastreadores nem cookies" (depende da D3) nem "Como tratamos
   dados" (não há página para esse link).
   **Achados:** `SELETOR-2-LINGUAS-FORA-DO-HANDOFF-01`, `LANG-SWITCH-ALVO-01` (resto),
   `ALVOS-DESKTOP-ABAIXO-44-01`, `FOOTER-HOVER-BOLD-01`, `LOTTO-NAV-CONTATO-CONTRASTE-01`,
   `RODAPE-360-ALTO-01` (revisitar), a parte do rodapé de `LOTTO-CONTRASTE-AA-01` e de
   `A11Y-LH-BASELINE-WP12-01` (o `h4` do rodapé).
   **Bloqueio:** nenhum. O 768 de nav e footer está no checklist do WP-19. Se esse checklist achar
   defeito, ele é corrigido nesta fatia. **Copy:** nenhuma.
   **Respostas do usuário (2026-11-22, "segue o recomendado"): as oito perguntas da especificação do
   `site-ux` (DESENHAR) ficam na opção (A).**
   1. Pílula "Contato" do nav: sai (`GHF Kit v3` "Nav sem CTA: o botão da Play é do hero"). "Contato"
      vira link comum. Fecha `LOTTO-NAV-CONTATO-CONTRASTE-01` por remoção.
   2. Segmento da língua atual: fundo `raised` mais `ring-1 ring-inset ring-border-strong` (3,30:1).
      Só o fundo dá 1,20:1 e reprova o 1.4.11.
   3. Seletor de 2 línguas: segmentado em `<a>` (troca de língua é navegação; funciona sem JS e é o
      que o §9 do `check_site.py` conhece), não `<button aria-pressed>` como no handoff.
   4. Faixa de sugestão de idioma: fica fixa embaixo (desenho do WP-15, CLS 0), com os tokens novos.
      Não vai para o topo em fluxo como no handoff.
   5. Acento sem app: só `--app-acc: var(--color-brand)` no `:root` de `tokens.css`. `-light` e
      `-edge` sem app ficam indefinidos até uma fatia ter consumidor.
   6. Ativo do botão primário: `color-mix(in oklab, acento 88%, black)` em `tokens.css` (4,98 / 5,21 /
      7,16 / 4,80 com texto `--bg`). O Claude Design confirma na próxima rodada. Fecha
      `BOTAO-ATIVO-CONTRASTE-01`.
   7. Rodapé segue o handoff: saem "Desenvolvido com ♥ por especialistas.", as colunas
      "Institucional" e "Transparência & Políticas" (as 5 URLs legais ficam na coluna de cada app) e
      os ícones circulares (redes viram texto com seta). A linha de baixo fica só com o ©.
   8. "Pular para o conteúdo": entra como componente novo (`PularConteudo.astro`, chave `pular`, pt e
      en), para o `<main id="conteudo">` de cada página. Não está no handoff: é candidato a voltar ao
      Claude Design.
   **Fixture do `sem-polyfill` regenerada (ADR-008 §7, 2026-11-22).** As classes da casca mudaram o
   CSS de `src/`; `GHF_SEM_POLYFILL_FIXTURE=tools/fixtures/sem-polyfill npm run build` regravou
   `entrada.css` (95 580 → 101 216 bytes) e `saida.css` (81 494 → 87 440). As três conferências: o
   `npm run test:css` passa (21 de 21); o CSS publicado não tem nenhum dos dois marcadores (§18 do
   `check_site.py` verde); o plugin continua tirando o mesmo tanto (14 086 → 13 776 bytes, 14,7% →
   13,6% da entrada). No diff dos seletores da saída, saem 39 (o Nav, o Footer e o seletor antigos)
   e entram os da casca; nenhum seletor some sem motivo.
   **Correções da auditoria (2026-11-22, sobre 872c0ef).**
   - **Ordem do rodapé em m e t (desvio do `Site Footer`).** O handoff mostra marca → contato →
     apps em m e t, e o DOM único (marca → apps → contato, para os apps virarem colunas em d) só
     reproduzia isso com `order-last`, o que punha o Tab fora da ordem visual (WCAG 2.4.3). O
     `order-last` saiu: a ordem visual é a do DOM em toda largura. Medido em Chrome headless:
     blocos na ordem marca → LottoExpert → TopoWalk → Pole Position → EclipseGo → contato a 360,
     768 e 1280, e o Tab a 360 percorre o rodapé nessa ordem. A 360 a altura não muda (871 px na
     home pt, 829 en, 915 Pole Position, 827 política do LottoExpert); a 768 sobe de 519 para 687
     px, porque o contato deixa a coluna ao lado da marca e vai para uma linha própria. Para o
     Claude Design: `RODAPE-ORDEM-M-T-01`.
   - **Hero legal dentro do `<main id="conteudo">`.** O "Pular para o conteúdo" saltava o `<h1>` e a
     data das 10 legais, e o axe acusava `region`. Só estrutura: o texto visível do `<main>` de cada
     legal é o de antes mais o do hero (comparado nas 10 páginas, pt e en); o `<h1>` está dentro do
     `<main>` nas 10; axe 4 (`region`, `landmark-one-main`, `bypass`, `skip-link`) sem violação a 360
     e 1280.
   - `<main id="conteudo" tabindex="-1">` nas 11 páginas (o Safari só move o foco para destino
     focável), com `focus-visible:outline-none` para o contorno não cobrir a página inteira. Medido:
     Tab + Enter no "Pular" deixa o foco no `<main>`.
   - A prop `prefixoAncora` saiu do `Footer.astro` e das 11 chamadas.
   - Fixture do `sem-polyfill` regenerada de novo (ADR-008 §7): `entrada.css` 101 216 → 101 279 e
     `saida.css` 87 440 → 87 503 bytes (sai `order-last`, entra `focus-visible:outline-none`); o
     `test:css` passa, o §18 fica verde e o plugin tira o mesmo tanto (13 776 bytes, 13,6%).
   - `check_site.py` §19: todo `<footer>` de `dist/` tem link para as 5 URLs legais na língua da
     página. Provado com mutação numa cópia de `dist/` (link do termos tirado de `index.html` e da
     política do EclipseGo tirado de `en/topowalk.html`): ❌ 2 erros, um por página; a cópia foi
     apagada.
   - **LCP de `/`.** Caiu de 2,56 para 2,33 s (mediana do `lighthouse.py`) porque o elemento LCP mudou do `<img>` do logo para o
     `<span>` "GHF Software", não por otimização: o observado sem throttle não melhorou. Remedir na
     fatia 6.
3. **Legal: `LegalLayout`, 10 páginas.** **Feita em 2026-11-22** (commits 1dfe3bf e 6f5bf3e; branch `feat/wp-10-fatia-3`, não enviada; o `risco` do WP segue `medio`, a fatia é alta). Auditorias de `site-qa`, `site-seo-perf` e `site-ux`: nenhum achado alto; os médios foram corrigidos (ênfase restaurada, decisão (A); troca de idioma mantém `#secao-N`; §12 do `check_site.py` confere âncoras e caixas; parágrafo quebrado do item 10 do plano consertado). Medidas: acessibilidade das legais de 96 para 100 (LottoExpert e TopoWalk); LCP das legais +~80 ms (1,73-1,88 para 1,80-1,95 s; o elemento é um `<p>` do corpo); +2 a 5 KB por página (sumário duplicado); CSS 86,7 para 81,9 KB (antes das caixas); `<head>`, `sitemap` e `id` das seções idênticos; `.legal-corpo` idêntico byte a byte nas 10 páginas; `src/content/legal/` intocado; `sync_legal --check` igual ao de antes. `/verify` passou (`lychee` só no CI). Resta o checklist de navegador, que é do usuário. Safari não testado.
   Papel claro, largura de leitura, sumário (recolhível
   abaixo de 1024 px, lateral a partir de 1024 px) e data no topo. A troca de idioma mantém
   `#secao-N`. O texto vem de `src/content/legal/` e não é tocado. A prova é `sync_legal.py
   --todos --check` igual antes e depois, mais o texto extraído do corpo de cada página legal em
   `dist/` igual antes e depois. A fatia tem `risco: alto`, porque toca 5 URLs contratuais e texto
   legal, e o `site-legal` participa.
   **Achados:** `LEGAL-TABELA-MONO-01`, `TW-CONTRASTE-01`, `LEGAL-LINK-CONTRASTE-01`,
   `LEGAL-LE-SLOGAN-CONTRASTE-01`, `TABELA-LEGAL-ANEL-DISCRETO-01` (revisitar) e a parte legal de
   `A11Y-LH-BASELINE-WP12-01`.
   **Bloqueio:** nenhum. **Copy:** nenhuma. Os rótulos de interface vêm de `content/i18n.js`.
   **Respostas do usuário (2026-11-22, "pode seguir com as recomendações"): as perguntas da
   especificação do `site-ux` (DESENHAR) ficam na opção (A).**
   1. Selo "Documento Legal" do hero: sai (o handoff não o tem; o título e o app já dizem que é
      legal). A chave `selo` sai de `legal.ts`.
   2. Aviso "em divergência, prevalece a versão em português" no en: omitido. A cláusula nasce no
      repositório do app (D8 b1): `PREVALENCIA-PT-EN-MD-01`.
   3. Seletor pt/en no hero: omitido; o do Nav (fatia 2) basta.
   4. Sumário estático, sem JS (sem realce da seção atual).
   5. Sumário sempre visível, a mesma anatomia nas 5 páginas (inclusive o EclipseGo, com 8 seções).
   6. Nenhum acento por app no corpo nem no hero, como o handoff; o `data-app` dá o acento da casca.
   7. Impressão: CSS mínimo — sem Nav, Footer, sumário e voltar; fundo branco; sem a faixa de URL.
   8. Literais: `--color-paper-chip` (#ECEBE7) e `--color-paper-raised` (#FFFFFF) entram em
      `tokens.css`; raio `--radius-ctl` (8) no lugar de 10 px, `h2` em `text-h2` (24/32) no lugar
      de 26/34, tabela em `text-small` (14/22) no lugar de 15/23. O Claude Design confirma na
      próxima rodada (`LITERAIS-SEM-TOKEN-LEGAL-01`).
   A edição do §12 do `check_site.py` (o corpo legal termina em `data-legal-voltar`, não mais no
   `<div class="max-w-4xl …">` que saiu) foi autorizada nesta fatia, sem afrouxar a regra.
   **Fixture do `sem-polyfill` regenerada (ADR-008 §7, 2026-11-22).** O bloco "Texto legal por tema"
   e os temas `[data-tema='*-privacy']`/`lottoexpert-terms` saíram do CSS; `entrada.css` 101 279 →
   94 648 e `saida.css` 87 503 → 82 424 bytes. O `npm run test:css` passa (21 de 21), o §18 fica
   verde, e o plugin tira 12 224 bytes (12,9%) em vez de 13 776 (13,6%): saem com os temas as
   reservas de opacidade (`bg-gray-800/50`, `bg-lime-900/10`, `hover:bg-gray-800/50`) que só as
   legais usavam. No diff dos seletores da saída, saem 59 (os temas e o texto legal antigos) e entram
   67 (o layout novo e o `.legal-corpo` de papel); nenhum seletor de outra página sai.
   **Correções da auditoria (2026-11-22, sobre 1dfe3bf).** Nenhum achado alto.
   - Ênfase restaurada (opção (A) do usuário), só por CSS e com tokens de papel: o `.legal-corpo`
     leva `data-doc` (do caminho da página), e o bloco "Texto legal" de `global.css` põe caixa
     (`bg-paper-chip`, barra `border-paper-link`) nas 3 notas de §2 e no "Dado local" de §9.2 (sem
     barra) da privacidade do LottoExpert, e no item do CVV 188 de §3 dos termos. O §12 do
     `check_site.py` ganhou `CAIXAS_LEGAIS`: cada alvo tem de começar por "Nota sobre"/"Note on" ou
     "Dado local"/"Local data", e o de §3 conter "188". Provado com mutação numa cópia de `dist/`
     (nota trocada, 188 tirado, `data-doc` tirado, parágrafo a mais): ❌ um erro por mutação. A
     caixa não tem referência no handoff: `LEGAL-CALLOUT-SEM-HANDOFF-01` (WP-20).
   - A troca de idioma mantém `#secao-N` (`Legal LottoExpert.dc.html:151`): o script da faixa de
     idioma copia o `location.hash` para o link `data-troca-idioma` no clique. Sem JS, vai ao topo.
   - §12: todo `href="#x"` da página legal tem `id="x"` nela (provado com um `id` tirado: ❌).
   - Espaço entre o rótulo e a data no chip (o texto extraído saía "atualização:13").
   - A sombra do "Pular para o conteúdo" só com o foco: fora da tela, ela vazava no canto de cima,
     visível sobre o papel.
   - Fixture do `sem-polyfill` regenerada de novo (ADR-008 §7): `entrada.css` 94 648 → 96 042 e
     `saida.css` 82 424 → 83 818 bytes; entram os 3 seletores das caixas e o `focus:shadow-pop`, nada
     sai; o plugin tira o mesmo tanto (12 224 bytes); `test:css` 21 de 21.
4. **404.** `404.dc.html`, só pt, com o texto atual. **Feita em 2026-11-22** (commits 1f6c207 e 27700db; branch `feat/wp-10-fatia-4`, não enviada). `404.astro` segue `404.dc.html` da rodada 3: duas colunas a partir de 1024; lista dos 4 apps com ícone por `astro:assets`, quadradinho `bg-app-*`, link da landing e link "Privacidade" com `sr-only` do nome. Tokens no lugar de `brand.*`. A copy atual fica; o eyebrow, o h1 e os parágrafos do export ficam fora (D25). `tema="ghf"` segue porque o `Base` ainda exige a prop. Desvios do export aceitos pelo `site-ux`: `anel-foco-interno` em vez de offset +2 (a `ul` tem `overflow-hidden`), sem `scale(1.06)` no ícone, colunas em `lg` em vez de `auto-fit minmax(420px)`, `first:border-t-0` (o export tem linha dupla no topo), `loading="eager"`. Auditorias de `site-qa`, `site-ux` e `site-seo-perf`: nenhum achado alto nem médio. Medidas na 404 (Lighthouse mobile, mediana de 3): Performance 99, Acessibilidade 100, Boas práticas 100, LCP 1,80 s, CLS 0, 148 KB no total e 14 KB de imagem (os ícones somam 3,1 KB no 1x e 6,4 KB no 2x). Orçamento cumprido em todas as páginas. Fixture do sem-polyfill regenerada. `/verify` passou (`lychee` só no CI). Resta o checklist de navegador, que é do usuário.
   **Achados:** `APPS-LISTA-DUPLICADA-01`, `ORCAMENTO-404-FROUXO-01` (ambos na fatia 10a). **Bloqueio:** nenhum. **Copy:** nenhuma.
5. **Template de landing e EclipseGo** (D29: o template nasce no EclipseGo, não no LottoExpert). **Feita em 2026-11-22** (commits f59a8c7, e8bad59 e db8f931; branch `feat/wp-10-fatia-5-eclipsego`, não enviada). Nenhuma auditoria trouxe achado alto.
   Os componentes `src/components/landing/*` são os de `Landing App.dc.html` (rodada 3, `?app=eclipse`):
   hero, funcionalidades, "ver todas" (D12), prova, planos, privacidade, FAQ e CTA. O conteúdo de cada
   app tem um formato só, em `src/i18n/<app>.ts`. O link da Play vem de `src/i18n/apps.ts`. O formato e
   os componentes admitem blocos opcionais (o aviso de jogo responsável e os blocos da D1), mas esses
   blocos só entram na fatia 9; aqui nenhum app os consome. Seção sem conteúdo com origem (D25) não
   aparece, sem placeholder. `EclipseGo.astro` e `PaginaEclipseGo.astro` passam a montar o template.
   **Achados:** `ECLIPSE-ICONE-OFFLINE-01` e `ECLIPSE-ICONE-WIFI-SLASH-01` (o ícone
   de `Landing App?app=eclipse`; ícone de fora do FA entra com a licença ao lado),
   `ECLIPSE-EN-ROTULOS-PT-01`, a parte EclipseGo de `EXPORT-COPY-SEM-ORIGEM-01` ("Sem backend" e
   "Nenhuma chamada de rede" só entram se o README do app disser), a parte EclipseGo de
   `LANDINGS-URL-E-PLAY-01`, `BOTAO-ATIVO-CONTRASTE-01` (medir o 88% no navegador).
   **Topo:** recalcular o topo e recolocar o CTA da Play acima da dobra a 1280×720; com o nav em
   fluxo desde a fatia 2, o CTA do EclipseGo sai da dobra.
   **URL e deploy:** nenhuma URL contratual muda. `/eclipsego.html` não é contratual;
   `/eclipsego-privacy.html` é, e a fatia não toca nela nem no `LegalLayout`. Sem mudança de deploy
   nem de stack. **Copy:** a publicada em `src/i18n/eclipsego.ts`, o `docs/ECLIPSE_GO_README.md` e o
   `../eclipse-go/README.md` (o app não tem ASO); frase sem origem fica fora (D25).
   **Imagens (D26):** `src/assets/img/eclipsego_screenshot.png` é a imagem do hero e
   `src/assets/img/eclipsego_phone_screen.png` é a captura de funcionalidade (resposta do usuário em
   2026-11-22: "servem pois o eclipse go não teve nem tem mudança prevista, as telas são as mesmas";
   D29).
   **Entregue (2026-11-22).**
   - **Template:** `src/components/landing/*` (Landing, Secao, CtaPlay, Hero, Funcionalidades,
     VerTodas, Prova, Planos, PlanosNiveis, PlanosGratisPro, NotaPlanos, Privacidade, Faq, CtaFinal,
     Aviso). **Formato único:** `ConteudoApp` em `src/i18n/landing.ts`, com `exigeEspelho` (pt é a
     base) e `itensNav`.
   - **EclipseGo:** `eclipsego.ts` migrou para o formato. O `resumo` é cópia de `home.ts` até a
     fatia 6. Saíram "Como funciona" e a stack.
   - **Copy (D25 e respostas do usuário na D29):** 3 destaques, só o primeiro com captura
     (`eclipsego_phone_screen.png`); o `eclipsego_screenshot.png` fica só no hero. A `meta` é "100%
     offline · Android 8.0 ou superior · Grátis". O FAQ tem 4 perguntas (anos de 2017 a 2047; 139
     eclipses em `eclipses.json`).
   - **Achados resolvidos:** `ECLIPSE-ICONE-OFFLINE-01` e `ECLIPSE-ICONE-WIFI-SLASH-01` (o template
     não tem card com ícone: saem por remoção); `ECLIPSE-EN-ROTULOS-PT-01` (os `alt` estão em inglês
     e avisam que a interface é em português); as partes EclipseGo de `EXPORT-COPY-SEM-ORIGEM-01` e
     de `LANDINGS-URL-E-PLAY-01`; `BOTAO-ATIVO-CONTRASTE-01` no EclipseGo (o ativo dá 4,80:1, medido
     no Chrome headless pelo `site-ux`; os outros apps medem nas fatias 7 a 9).
   - **Desvios aceitos pelo `site-ux`:** `Landing` recebe `Record<Idioma, ConteudoApp>`;
     `exigeEspelho` tem um 3º parâmetro; `nav_planos` e `nav_gratis_pro` existem em `ui.ts`; a
     tabela de planos fica em `<section tabindex=0 aria-label>`, exigência do html-validate;
     `NotaPlanos` foi criado e a `Secao` ganhou props; o hero usa `wrap-break-word`, widths
     360/560/720/1024 e `mx-auto` com `max-w-[560px]`.
   - **Desvio de escopo (autorizado pelo usuário nesta sessão):** `tools/orcamento-lighthouse.json`
     foi remedido para `/eclipsego.html`: 248 687 B no total e 59 262 B de imagem (o medido + 20%,
     regra do WP-12). O arquivo está fora dos alvos da fatia, mas a doc do `lighthouse.py` manda o
     novo número entrar no mesmo PR.
   - **Medidas em `/eclipsego.html`:** perf 99, a11y 100, bp 100, seo 100, LCP 2,10 s, CLS 0; 202 KB
     no total, 48 KB de imagem. A 1280x720 o CTA do hero termina em y=591 (pt) e y=576 (en) e a
     faixa de idioma começa em 634: o CTA fica acima da dobra.
   - **Verificação:** o `/verify` passou, menos o `lychee` (não instalado; o CI roda). A fixture do
     sem-polyfill foi regenerada.
   - **Achados novos:** `LANDING-ESPELHO-SEM-TESTE-01` (fatia 7), `CORONA-GLOW-ORFAO-01` (fatia 10a),
     `HERO-ASPECT-RETRATO-01` (fatias 7 e 8), `FUNC-SEM-IMAGEM-METADE-VAZIA-01` e
     `ECLIPSE-OG-IMAGE-442-01` (WP-20), `FAQ-SINAL-ABERTO-01` e `LANDING-JSONLD-CAMPOS-01` (fatia
     10a), `HERO-H1-SEM-PALAVRA-CHAVE-01` (fatia 10b; decisão de copy do usuário).
   **Checklist de navegador (usuário):** ver `handoff.md`, seção 3.
   **Bloqueio:** nenhum. O EclipseGo é o único app estável; os outros três estão em evolução.
6. **Home.** **Feita em 2026-11-22** (commits 20649c6, a4d30b4 e 1f69780; branch `feat/wp-10-fatia-6-home`, não enviada). Nenhuma auditoria trouxe achado alto. Os cards seguem a ordem do brief §10 e a regra da D12. A lista "ver todas" fica vazia
   enquanto os 4 apps forem destaque. Cada app em `apps.ts` ganha um campo de data da última
   atualização, com comentário de origem (tag de release no repositório do app).
   **Fonte do card (D29, complemento de 2026-11-22):** o card do EclipseGo lê o `resumo` de
   `src/i18n/eclipsego.ts` (`ConteudoApp`), e as chaves do EclipseGo saem de `home.ts`; os cards de
   TopoWalk, Pole Position e LottoExpert leem `src/i18n/home.ts` até a landing de cada um migrar
   para `ConteudoApp` (fatias 7 a 9), que move o texto do card para o `resumo` do app.
   **Achados:** `INDEX-LOTTO-DESC-DIVERGE-01`, `HOME-ALT-DESCREVE-FUNCIONALIDADE-01`,
   `HOME-STACK-SELOS-CONTRASTE-01`, `DESTAQUE-LIMIARES-INVENTADOS-01`.
   **Bloqueio:** o texto do card do LottoExpert, se a fonte não tiver (D25). O 768 está decidido
   (D27). Quem desbloqueia: o usuário. O WP-19 não bloqueia a home.
   **Entregue (2026-11-22; copy pela D30).**
   - **Home:** `Home.astro` reescrita contra `Home.dc.html`: hero só com texto, grade `#portfolio` com
     4 cards na ordem do brief §10, e as seções Sobre e Privacidade. `VerTodasApps.astro` (sem desenho
     no handoff; não aparece hoje) e `src/assets/icones-apps.ts`. `home.ts` tipado, com os textos dos
     cards em `resumos.<app>`; a lista das chaves removidas está no commit a4d30b4.
   - **`apps.ts`:** campos `pagina`, `privacidade`, `atualizadoEm` (tag de release de cada app:
     LottoExpert v2.05.03 2026-10-12, TopoWalk v4.4.0 2026-10-29, Pole Position v2.2.0 2026-10-16 em
     `../pole-position-app`, EclipseGo v1.0.1 2026-07-26) e `indisponivel?`. Mais `ORDEM_APPS`,
     `particionarApps(hoje)` (D12 no build), `hojeDoBuild()` (`GHF_HOJE`, só para teste: validado e
     barrado com `CI`/`GITHUB_ACTIONS`) e `dataCurta` (locale do `idiomas.json`).
   - **Tag no app:** a v1.0.1 do EclipseGo é leve. O agente a criou e enviou em 2026-11-22, com
     autorização do usuário, sobre `f5c1d6b` (ponta da main, sem mudança de código desde o
     `versionName` 1.0.1).
   - **Desvios de escopo (autorizados):** `tools/test_sem_polyfill.mjs`, teste 6: a régua "saída <
     90% da entrada", que dependia do CSS do site, virou "a entrada tem os dois polyfills e a saída é
     menor" (decisão do usuário; o `site-qa` confirmou que não é mais fraca: plugin no-op derruba 3
     testes). `tools/orcamento-lighthouse.json`: o teto de `"/"` só baixou, para o medido + 20% (184
     844 / 18 234 B).
   - **Medidas em `/`:** perf 99, a11y 100, bp 100, seo 100, LCP 1,80 s (elemento `<h1>`; era 2,33 s
     no logo), CLS 0, 150 KB (15 KB de imagem). CSS publicado 87,7 -> 73,2 KB. Pelo `site-ux` em Chrome
     headless: grade 1/2/2/4 colunas (360/768/1024/1280), sem card órfão, h1 em 2 linhas, alvos >= 44
     px, menor contraste 5,97. Regra D12 exercitada com `GHF_HOJE`.
   - **Achados resolvidos:** `HOME-ALT-DESCREVE-FUNCIONALIDADE-01` (capturas saíram),
     `ALVOS-DESKTOP-ABAIXO-44-01` (o Play tem 44 px), `HOME-BOTAO-EMERALD-CONTRASTE-01`,
     `HOME-STACK-SELOS-CONTRASTE-01` (por remoção, D30 (2)), `DESTAQUE-LIMIARES-INVENTADOS-01`
     (regra D12 implementada), a parte da home de `A11Y-LH-BASELINE-WP12-01` e
     `INDEX-LOTTO-DESC-DIVERGE-01` na home (D30 (3)); o texto longo do LottoExpert fica para a fatia 9.
   - **Achados novos:** `LITERAIS-SEM-TOKEN-HOME-01`, `HOME-VER-TODAS-SEM-DESENHO-01`,
     `HOME-GRADE-3-CARDS-01`, `PRIV-NOME-ACESSIVEL-ORDEM-01`, `HOME-OG-IMAGE-677-01` (WP-20);
     `APPS-ATUALIZADO-EM-SEM-CHECK-01`, `HOME-ORDEM-SEM-CHECK-01`, `ICONES-APPS-DUPLICADOS-01`,
     `BUILD-RELOGIO-NAO-REPRODUTIVEL-01`, `SOBRE-REGIAO-ENGLOBA-PRIVACIDADE-01`,
     `ROTULO-DATA-DUAS-FONTES-01`, `ORGANIZATION-JSONLD-MINIMO-01` (fatia 10a);
     `HOME-ICONES-ORFAOS-01`, `CSS-BUNDLE-NOME-FOOTER-01`, `HOME-VOCABULARIO-TECNICO-01` (fatia 10b);
     `HOME-X-DEFAULT-EN-01` (WP-18); `CLAUDE-MD-POLE-CAMINHO-01` (WP-28).
   **Checklist de navegador (usuário):** ver `handoff.md`, seção 3.
7. **TopoWalk** (pt e en; as outras línguas são do WP-18). **Achados:** `TOPO-PT-HTML-DIVERGE-01`,
   `TOPO-CONTRASTE-AA-01`, a parte TopoWalk de `LANDINGS-URL-E-PLAY-01`. **Topo:** recalcular o
   topo e recolocar o CTA da Play acima da dobra a 1280×720 (nav em fluxo desde a fatia 2).
   **Bloqueio:** as 4 capturas (D26; o app está em evolução). Quem desbloqueia: o usuário.
8. **Pole Position.** **Achados:** `POLE-PT-HTML-DIVERGE-01` (vale o que a política do app diz
   sobre o Firebase), `POLE-EN-ROTULOS-PT-01`, `POLE-PRINTS-2X-01`, `POLE-MOCKUP-CURSOR-01`.
   **Topo:** recalcular o topo e recolocar o CTA da Play acima da dobra a 1280×720 (nav em fluxo
   desde a fatia 2).
   **Bloqueio:** 2 capturas (D26; o app está em evolução) e as capturas em 2× para `POLE-PRINTS-2X-01`. Quem desbloqueia:
   o usuário. O preço e a faixa etária vêm da ficha pública da Play, lidos como na D17, e não
   bloqueiam.
9. **LottoExpert** (D29: consome o template da fatia 5). Entram os blocos opcionais do template: o
   aviso de jogo responsável e os blocos da D1 (Teimosinha e prestação de contas do bolão).
   **Achados:** `FEATURES-SELO-PREMIUM-01`, `TEIMOSINHA-FORA-DA-TABELA-01` (o limite vem de
   `FreemiumConfig.kt`), `LOTTO-CONTRASTE-AA-01` (violeta), `LOTTO-EN-ROTULOS-PT-01`,
   `LOTTO-COPY-VANTAGEM-01`, `LOTTO-PT-HTML-DIVERGE-01`, `LANDINGS-RESIDUO-RODADA-2-01`, a parte
   LottoExpert de `EXPORT-COPY-SEM-ORIGEM-01` e de `LANDINGS-URL-E-PLAY-01`.
   **Topo:** recalcular o topo e recolocar o CTA da Play acima da dobra a 1280×720. Com o nav em
   fluxo desde a fatia 2, o CTA do LottoExpert sai da dobra.
   **Bloqueio para fechar (não para começar):** a copy que falte na fonte (D25) e as capturas
   das funcionalidades destacadas (D26). O repositório só tem o mockup do hero e os logos das loterias.
   Quem desbloqueia: o usuário.
10. A fatia 10 se divide em 10a e 10b (D29, complemento de 2026-11-22). As duas ficam numa
    posição diferente da ordem: a 10a vem logo depois da 6, a 10b é a última.

    **10a. Aceite parcial** (logo depois da 6, antes das landings em evolução). Só o que não depende
    das fatias 7 a 9.
    **Achados:** `ORCAMENTO-404-FROUXO-01` (reapertar o teto da 404), `APPS-LISTA-DUPLICADA-01`
    (fonte única da lista de apps em `src/i18n/apps.ts`, consumida pela 404 e pelo `Footer`),
    `FAQ-SINAL-ABERTO-01`, `LANDING-JSONLD-CAMPOS-01` e `CORONA-GLOW-ORFAO-01` (apaga só o
    `.corona-glow` de `legado.css`; a camada de legado fica até a 10b).
    Da fatia 6: `BUILD-RELOGIO-NAO-REPRODUTIVEL-01` (decisão do usuário), `APPS-ATUALIZADO-EM-SEM-CHECK-01`,
    `HOME-ORDEM-SEM-CHECK-01`, `ICONES-APPS-DUPLICADOS-01` e `ROTULO-DATA-DUAS-FONTES-01` (junto de
    `APPS-LISTA-DUPLICADA-01`), `SOBRE-REGIAO-ENGLOBA-PRIVACIDADE-01`, `ORGANIZATION-JSONLD-MINIMO-01`
    (junto de `LANDING-JSONLD-CAMPOS-01`).
    **Aceite parcial:** a tabela de contraste do `site-ux` (pares cor/fundo medidos) e o Lighthouse de
    acessibilidade ≥ 95 nas páginas já redesenhadas: as 10 legais, a 404, a Home e o EclipseGo, pt e
    en. As landings de TopoWalk, Pole Position e LottoExpert ficam de fora, porque ainda não
    migraram; entram na 10b.
    **Bloqueio:** nenhum. **Copy:** nenhuma.

    **10b. Limpeza e aceite final** (a última fatia, depois da 9). Saem a camada de legado
    (`src/styles/legado.css`, os nomes `brand.*` e os temas `[data-tema]`). O grep de tokens fica
    vazio. A tabela de contraste e o Lighthouse de acessibilidade ≥ 95 passam a valer para todas as
    páginas. Entra o checklist de navegador completo (todas as páginas, 360/768/1280, pt e en).
    **Achados:** `CSS-ORCAMENTO-BYTES-01` (teto de CSS medido depois de sair o legado),
    `HOME-ICONES-ORFAOS-01`, `CSS-BUNDLE-NOME-FOOTER-01`, `HOME-VOCABULARIO-TECNICO-01` (decisão de copy do usuário),
    `HERO-H1-SEM-PALAVRA-CHAVE-01` (decisão de copy do usuário; sem ela o h1 fica como está) e
    `FUNC-SEM-IMAGEM-METADE-VAZIA-01` se o WP-20 não o cobrir.
    **Revisão final no site real (do WP-19, decisão do usuário em 2026-11-22):** TopoWalk em russo a 360 (se a língua existir no site até lá); home, landing e legal a 768; faixa de sugestão de idioma (fecha e não volta na sessão); foco visível em "Ver todas" e nos sociais do rodapé; selo "Publicado" distinto do verde do Pole Position.

**Ordem** (replanejada pela D29 e pelo complemento dela de 2026-11-22): 1 → 2 → 3 → 4 → 5 → **6 →
10a → 7 → 8 → 9 → 10b**. As fatias 1 a 5 estão feitas. A 6 (Home) não tem bloqueio de captura: os
cards de TopoWalk, Pole Position e LottoExpert leem `home.ts` e mudam quando as landings deles
migrarem; o bloqueio dela continua sendo o texto do card do LottoExpert, se a fonte não tiver (D25).
A 10a vem logo depois da 6 e fecha o que não depende das landings em evolução. As fatias 7 a 9 usam
o template e cada uma entra quando as capturas dela chegarem (D26; os apps estão em evolução); a 9
(LottoExpert) é a última landing, porque depende também de copy (D25) e leva os blocos opcionais. A
10b é a última fatia. O WP-10 só fica `done` com a 10b, e o deploy único (D13) espera o WP-10. Logo,
o que segura o deploy único são as capturas e a copy que o usuário fornece. A numeração fica: a D29
trocou a 5 e a 9 de lugar e dividiu a 10 em 10a e 10b, para as referências a "fatia 6", "7" e "8"
continuarem válidas; referência antiga a "fatia 10" (ADR-008 §5, `CLAUDE.md`, `docs/ARQUITETURA.md`,
WP-19, WP-26 a WP-28) vale como 10b.

**Logo** (resposta 5 do usuário, 2026-11-21; decisão de execução, sem linha D). O PNG atual
(`GHFSoftware.png`) fica no `Logo.astro` da fatia 2; o agente não faz arte nova. A arte nova clara e escura, com "desde 2004", vai para a sessão do usuário no Claude Design
do WP-20 (D16); `LOGO-ANO-E-FUNDO-ESCURO-01` foi para o WP-20 e não bloqueia o WP-10.

**Respostas do usuário (2026-11-21, "Segue o recomendado").** As seis perguntas do veredito ficam na
opção (A): 1 D24, 2 D25, 3 D26, 4 D27, 5 logo (acima), 6 convite no WP-24.
