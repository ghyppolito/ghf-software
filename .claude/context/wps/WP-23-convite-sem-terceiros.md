---
id: WP-23
titulo: O convite do bolão abre sem terceiros (pako e Inter servidos pelo site, com `<main>`)
area: infra
status: todo
depende_de: []
adr: [ADR-001, ADR-002, ADR-006]
spec: ""
decisoes: []
tamanho: M
risco: alto
visual: true
branch: feat/wp-23-convite-sem-terceiros
---

# WP-23 — O convite do bolão abre sem terceiros

**Depende de:** o **deploy único** (D13), que não é WP: é o `/release` da integração
`feat/wp-08-layout-unico` → `develop` → `master`. Por isso `depende_de` fica vazio: listar os WPs
que ainda faltam no escopo do D13 (WP-10, 13, 16 a 20) seria um substituto que envelhece se o
usuário tirar um deles do escopo, e "WP `done`" não é "no ar". O pré-voo prova o fato:
`git fetch origin && git merge-base --is-ancestor origin/feat/wp-08-layout-unico origin/master`
sai 0, **e** o teste com link real do D13 (4) foi relatado. Antes disso o WP não começa.

**Branch:** `feat/wp-23-convite-sem-terceiros`, criada de `develop` **depois** do deploy único
(D5); PR mira `develop`. **Não** nasce da integração `feat/wp-08-layout-unico`: a integração já
foi ao ar e o convite deixa de estar congelado pelo D13 só quando o publicado é o da integração.
Vai ao ar num `/release` próprio, depois do merge.

**Achados roteados:** `INVITE-PAKO-CDNJS-01`, `CONVITE-SEM-MAIN-01`. **Não entra:**
`CONVITE-TEMA-ESCURO-01` (o usuário pediu para não criar WP ainda; segue `nota`).

**Objetivo:** o convite (`/lotto-expert/sweepstake-invite/lottoexpert-invite.html`, ADR-001)
carrega só arquivos do próprio site — `pako` 2.1.0 e a Inter servidos de `dist/`, com hash em
`tools/contrato.sha256` —, tem um `<main>`, passa no html-validate sem ignore e entra nas guardas
de desempenho (§15 (a)/(b)) e de acessibilidade (§17) do `check_site.py`, que hoje o pulam.

**Contexto** (medido em 2026-10-16, branch `feat/wp-08-layout-unico`):

- `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html:20` carrega
  `https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js` sem `integrity`. É o único
  descompactador do `?d=`: `pako.ungzip` em `:311` (v1) e `:323` (v2, prefixo `2.`). Cloudflare
  fora do ar ou arquivo trocado = convite não decodifica (cai em `:388-399`, "Não conseguimos
  exibir o resumo…") ou roda código de terceiro numa página que lê o link do bolão.
- `:19` carrega a Inter de `fonts.googleapis.com`: IP do visitante para o Google, contra a régua
  privacy-first; o WP-12 já tirou o Google Fonts do resto do site (ADR-006 §3).
- Sem `<main>` (`:233-235`, o card está em `<div class="container">`).
- `npx html-validate` sobre o convite: 2 erros `no-trailing-whitespace` (`:9`, `:256`) — por isso
  ele está em `.htmlvalidateignore` (check_site §13 (d)).
- `tools/check_site.py:716` `CONGELADAS` isenta o convite de §14 (SEO), §15 (desempenho, `:1132`),
  §16 (redirecionamento, `:1185`) e §17 (acessibilidade, `:1266`); o comentário de `:1068` já diz
  que é por causa do pako e da Inter.
- **Origem do pako, conferida em 2026-10-16:** o arquivo do cdnjs e o `package/dist/pako.min.js`
  do tarball oficial `https://registry.npmjs.org/pako/-/pako-2.1.0.tgz` são o mesmo byte a byte —
  46.859 bytes, sha256 `ede2693a4a6a5126b9d35669062b358ecab6ae7b9b86a1cf302feb45a8514907`. O
  tarball confere com o `dist` do registro: `integrity`
  `sha512-w+eufiZ1WuJYgPXbV/PO3NCMEc3xqylkKHzp8bxp1uW4qaSNQUkwmLLEc3kKsfz8lpV1F8Ht3U1Cm+9Srog2ug==`,
  `shasum` (sha1) `266cc37f98c7d883545d11335c00fbd4062c9a86`. Cabeçalho do arquivo:
  `/*! pako 2.1.0 https://github.com/nodeca/pako @license (MIT AND Zlib) */` (a licença vai junto).
  Como o arquivo local é o mesmo que a página já executa, o comportamento de decodificação não muda.
- **Formato do link é do app** (`../lotto-expert/app/src/main/java/br/com/ghfsoftware/lottoexpert/domain/model/SweepstakeCoder.kt`):
  `encode` (`:75-82`) emite **v1** enquanto o total de dezenas do bolão for ≤
  `LEGACY_MAX_TOTAL_NUMBERS = 100` (`:61`) e **v2** (`"2."` + binário) acima disso; o link é
  montado em `SweepstakeViewModel.kt:910`. Ou seja: um bolão de Mega-Sena com até 16 jogos sai em
  v1; um de Lotomania com 3 jogos ou mais (50 dezenas cada) sai em v2.

**Veredito de arquitetura (site-arquiteto, 2026-10-16) — decide onde ficam os arquivos:**

1. **Ao lado do convite, em `public/lotto-expert/sweepstake-invite/`:** `pako-2.1.0.min.js` (nome
   com a versão) e `inter-latin-wght.woff2`. O primeiro nível de `public/` (§13 (a), `PUBLIC`) não
   muda — `lotto-expert/` já está na lista —, e §13 (b) só barra `.html`. **Nenhum caminho novo na
   lista fechada.** Fecha: `public/fonts/` ou `public/js/` (abririam a lista), apontar para
   `/_astro/…woff2` (nome com hash, muda a cada build e quebraria o convite em silêncio) e
   transformar o convite em página gerada (outro WP, se um dia; aqui o arquivo continua em
   `public/`, byte a byte).
2. **A Inter é uma cópia fixa de `src/assets/fonts/inter-latin-wght.woff2`** (sha256
   `100505487f9771ddb23d8b9cbb4c1a0b1b7dc5610801e2185ecaf41fac512f83`; recorte do
   `InterVariable.woff2` 4.001 do handoff, OFL, `astro.config.mjs:24-31`). Eixo `wght` 400–800
   cobre os pesos do convite (400, 600, 700, 800); a faixa latina cobre os acentos e o `—` do texto
   fixo. Dois arquivos iguais com papéis diferentes é o que o ADR-006 §2 já aceita (a cópia de
   `src/` alimenta o build; a de `public/` é URL fixa). **Sem guarda de igualdade** entre os dois:
   se o redesign (WP-10) recortar outra fonte, o convite não deve mudar junto — o
   `contrato.sha256` é quem prende a cópia do convite. Licença: mesmo tratamento do WP-12 (OFL no
   repositório, `src/assets/fonts/OFL.txt`).
3. **URLs a partir da raiz** (`/lotto-expert/sweepstake-invite/…`) no `<script src>`, no
   `@font-face` e no `<link rel="preload" as="font" type="font/woff2" crossorigin>` — a mesma
   string nos dois últimos, senão a fonte baixa duas vezes; o §15 (a) exige preload com caminho
   começando por `/`.
4. **`<main>` troca o `<div class="container">`** (mesma classe, CSS intocado). Embrulhar o
   container num `<main>` novo mudaria o layout: o `<main>` viraria o filho flex do `body` e o
   `width: 100%` do `.container` passaria a ser relativo a ele.
5. **Guardas.** `CONGELADAS` continua sendo "o `.html` de `tools/contrato.sha256`" e segue isentando
   o convite de **§14** (é deep link com `?d=`, uma língua, sem canonical/hreflang/JSON-LD por
   desenho — ADR-005) e de **§16** (o `window.location = appUrl` de `:398` e `:424` abre o app pelo
   esquema `lottoexpert://`; não é troca de língua). Sai de **§15 (a) e (b)** (fonte do site,
   nenhum recurso de outra origem, nenhuma menção a `cdnjs`) e de **§17** inteiro. Fica isento só
   de **§15 (c)**: o convite exibe as PNG de `public/assets/` por URL fixa e troca o ícone por JS
   (ADR-006 §2 diz isso) — lista própria, não `CONGELADAS`. `.htmlvalidateignore` deixa de
   existir e o §13 (d) passa a exigir que **não** exista (glob de ignore esconderia página).
6. **Os dois arquivos novos entram em `tools/contrato.sha256`**: o convite depende deles para
   decodificar e para renderizar; trocar o pako é mudar o contrato.

Sem ADR novo: ADR-006 deixou "o convite sem terceiros (pako e Inter locais), num WP que aceite
mudar `tools/contrato.sha256`" em aberto, e este WP o fecha dentro do §2/§3 dele. O `site-docs`
anota no ADR-006 ("O que isto mantém aberto") que o WP-23 fechou o item.

**Ler antes:** ADR-001 inteiro; ADR-006 §2, §3 e §5; `tools/check_site.py` §13 (`:651-710`), §15
(`:1067-1177`), §16 (`:1179-1188`), §17 (`:1190-1290`); o convite inteiro (431 linhas);
`SweepstakeCoder.kt:30-82`.

**Arquivos-alvo:**

- `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html` (`:19`, `:20`, `@font-face` no
  `<style>`, preload, `<main>`, espaços de `:9` e `:256`)
- `public/lotto-expert/sweepstake-invite/pako-2.1.0.min.js` (novo, cópia do tarball do npm)
- `public/lotto-expert/sweepstake-invite/inter-latin-wght.woff2` (novo, cópia de `src/assets/fonts/`)
- `tools/contrato.sha256`
- `tools/check_site.py` (docstring §13–§17, §13 (d), §15, §17, comentários `:1068`, `:1181`, `:1191`)
- `.htmlvalidateignore` (removido)
- `tools/orcamento-lighthouse.json` (o convite entra como página medida)
- `CLAUDE.md` (bloco "Arquitetura": linha do `lotto-expert/sweepstake-invite/`), `docs/ARQUITETURA.md:35`,
  `.claude/context/invariantes.md:14` (sem `.htmlvalidateignore`)

**Passos:**

1. Pré-voo: o deploy único está em `master` (comando em "Depende de") e o teste do D13 (4) foi
   relatado. Branch de `develop` atualizado.
2. Baixar o tarball `pako-2.1.0.tgz` do registro do npm para diretório vazio no scratchpad,
   conferir `sha512` com o `integrity` acima, extrair e conferir o sha256 de
   `package/dist/pako.min.js` = `ede2693a…4907`. Copiar como `pako-2.1.0.min.js`. Conferir que é
   igual ao arquivo que o cdnjs serve hoje (mesmo sha256). Saída dos três comandos no commit.
3. Copiar `src/assets/fonts/inter-latin-wght.woff2` para o lado do convite; sha256 = `100505…2f83`.
4. Convite: `:20` vira `<script src="/lotto-expert/sweepstake-invite/pako-2.1.0.min.js"></script>`;
   `:19` vira o preload da fonte; `@font-face { font-family: 'Inter'; src: url('/lotto-expert/sweepstake-invite/inter-latin-wght.woff2') format('woff2'); font-weight: 400 800; font-style: normal; font-display: swap; }`
   no início do `<style>`; `<div class="container">` → `<main class="container">` e o `</div>`
   correspondente → `</main>`; tirar os espaços de fim de linha de `:9` e `:256`. Comentário de
   origem no `<head>`, **sem a palavra `cdnjs`** (o §15 (b) a barra): versão, registro do npm,
   sha256. Nada mais muda — JS, CSS, textos, og:image.
5. `check_site.py`: §15 e §17 sem o `continue` de `CONGELADAS`; §15 (c) pula uma lista nova
   (`IMAGEM_DE_PUBLIC`, o convite, com ADR-006 §2 no comentário); §13 (d) erro se
   `.htmlvalidateignore` existir; docstring e comentários de §13–§17 atualizados. Prova de mutação
   (cada uma acusa, depois reverte): `<script src` do cdnjs de volta; `<link>` do Google Fonts de
   volta; preload removido; `<main>` → `<div>`; segundo `<main>`; `.htmlvalidateignore` recriado.
6. `.htmlvalidateignore` removido.
7. `tools/contrato.sha256`: hash novo do convite e duas linhas novas (pako, woff2); as do
   `assetlinks.json`, `lottoexpert_app_mockup.png` e `CNAME` **não mudam**.
8. `tools/lighthouse.py --medir` com o convite acrescentado a `tools/orcamento-lighthouse.json`
   (chave `/lotto-expert/sweepstake-invite/lottoexpert-invite.html`, sem `?d=`: a página cai na
   mensagem de erro, mas carrega pako e fonte do mesmo jeito; `"seo": false`, porque é deep link e
   não página de busca). Orçamento = medido + 20%, como as outras. Se acessibilidade ou boas
   práticas ficarem < 0,90, **parar e reportar**: corrigir é mudar o convite além do escopo, e o
   usuário decide (achado novo).
9. Docs dos Arquivos-alvo.

**Critérios de aceite:**

- `grep -nE 'cdnjs|googleapis|gstatic' dist/lotto-expert/sweepstake-invite/lottoexpert-invite.html` vazio.
- `grep -nE '<(script|link)[^>]+(src|href)="(https?:)?//' dist/lotto-expert/sweepstake-invite/lottoexpert-invite.html`
  vazio (nenhum script, estilo ou fonte de outra origem; o `og:image` é `<meta>` do próprio
  domínio e o link da Play é `<a>`, fora do critério).
- `sha256sum dist/lotto-expert/sweepstake-invite/pako-2.1.0.min.js` =
  `ede2693a4a6a5126b9d35669062b358ecab6ae7b9b86a1cf302feb45a8514907` (o do `package/dist/pako.min.js`
  do tarball oficial, cujo sha512 confere com o `integrity` do registro).
- `sha256sum dist/lotto-expert/sweepstake-invite/inter-latin-wght.woff2` = `100505…2f83`.
- `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` sai 0 com 6 linhas, a do convite
  diferente da de hoje (`27925c02…0af1`) e as de `assetlinks.json`, `lottoexpert_app_mockup.png` e
  `CNAME` iguais (`git diff tools/contrato.sha256` mostra só a linha do convite trocada e 2 linhas
  novas).
- `python3 tools/check_site.py --raiz dist` verde, com o convite verificado por §15 (a)/(b) e §17
  (as 6 mutações do passo 5 acusam, saída no commit) e as URLs contratuais presentes.
- `.htmlvalidateignore` ausente e `npx html-validate 'dist/**/*.html'` sai 0 (convite incluído).
- `lychee --offline` sobre `dist/` sem erro (os dois arquivos novos resolvem).
- `python3 tools/lighthouse.py` verde com o convite no orçamento: **nenhuma requisição a outra
  origem** em nenhuma run.
- `git diff` do convite: só as linhas do passo 4 (conferir com `git diff --stat` e leitura do
  diff no PR; nenhuma linha de JS muda).

**Só no navegador** — o usuário faz e reporta; sem o relato o WP não fecha. Dois momentos.

*Antes do merge (`dist/` local: `npm run build && python3 -m http.server 8080 -d dist`, celular na
mesma rede pelo IP do PC):*

1. Gerar no app **dois** convites reais e copiar os links: um **v1** (Mega-Sena, até 16 jogos —
   o `?d=` não começa com `2.`) e um **v2** (Lotomania com 3 jogos ou mais — o `?d=` começa com
   `2.`, o caminho de `:323`). Trocar `https://ghfsoftware.com` por `http://<ip>:8080`.
2. PC, aba anônima, 1280 px: os dois abrem o card com loteria, nome, concurso, cotas, total de
   jogos e custo iguais aos do app; fonte Inter (não a do sistema). DevTools → Network: **todas** as
   requisições para `<ip>:8080`; nenhuma para `cdnjs.cloudflare.com` nem `fonts.googleapis.com`/`gstatic`.
3. Android, Chrome, 360 px: mesmos dois links, mesmo resultado; card sem salto de layout.
4. Sem `?d=`: mensagem de erro. `?d=abc`: mensagem "Não conseguimos exibir o resumo…" e botão.

*Depois do `/release` (produção):*

5. Gerar um convite novo no app e mandar pelo WhatsApp: a prévia mostra título e
   `lottoexpert_app_mockup.png` como antes.
6. Android **com** o app: tocar o link abre o app direto (App Links) e importa o bolão.
7. Android **sem** o app (ou outro aparelho) e PC em aba anônima: o link abre a página e o card
   aparece, v1 e v2; Network sem outra origem.

**Irreversível:** nada sai do site. O caminho do convite, o `?d=`, o `assetlinks.json` e a
`og:image` ficam iguais; links já compartilhados continuam abrindo. O que muda são os bytes do
convite e dois arquivos novos ao lado dele. App instalado: App Links depende só do
`assetlinks.json` (hash inalterado) e do caminho — o app abre igual. Se a página quebrar, o
sintoma é o card não aparecer no navegador (quem tem o app não passa pela página).

**Rollback:** republicar o artefato anterior. Antes do `/release` deste WP, criar a tag
`pre-wp-23` no `master` publicado e acrescentá-la à política do ambiente `github-pages` (mesmo
comando do D13 (5), com `name=pre-wp-23`); se o teste de produção falhar,
`gh workflow run deploy.yml --ref pre-wp-23` (minutos, sem reverter merge). Depois, `git revert`
do merge em `develop` → `master` pelo fluxo normal. A tag sai da política quando o WP fechar.

**Risco:** alto (URL contratual). Específicos: (a) caminho errado do pako (`src` relativo vs. raiz)
→ `pako is not defined` → todo convite cai na mensagem de erro — o card não aparece; o passo 2 do
navegador e o lychee pegam; (b) arquivo do pako diferente do que roda hoje → decodificação muda — o
sha256 contra o tarball fecha; (c) `<main>` muda o layout se embrulhar em vez de trocar o
`<div>` — passo 3 do navegador a 360 px; (d) nome do bolão com caractere fora da faixa latina (o
Google servia latin-ext e outras faixas) cai na fonte do sistema só naquele glifo — aceito, é texto
digitado pelo usuário e continua legível; (e) Lighthouse do convite reprovar acessibilidade e
forçar mudança fora do escopo — o passo 8 para e reporta, não corrige de passagem.
