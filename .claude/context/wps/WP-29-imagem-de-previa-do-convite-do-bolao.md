---
id: WP-29
titulo: A prévia do convite do bolão mostra o LottoExpert 2.06.00 em 1200×630
area: infra
status: todo
depende_de: []
adr: [ADR-001, ADR-002, ADR-006]
spec: ""
decisoes: [D13, D16, D26, D32]
tamanho: M
risco: alto
visual: true
branch: feat/wp-29-previa-do-convite
---

# WP-29 — A prévia do convite do bolão mostra o LottoExpert 2.06.00 em 1200×630

**Depende de:** o **deploy único** (D13), que não é WP — mesmo raciocínio do WP-23: `depende_de`
fica vazio e o pré-voo prova o fato com
`git fetch origin && git merge-base --is-ancestor origin/feat/wp-08-layout-unico origin/master`
(sai 0) **e** o relato do teste com link real do D13 (4). Antes disso o WP não começa.

**Decisão do usuário (2026-11-24), registrada como resposta:** "release própria depois do deploy
único (como o WP-23)". A D13 fica intacta: o deploy único sobe com `assets/lottoexpert_app_mockup.png`
e o convite iguais ao `master` (`tools/contrato.sha256`). Este WP roda **depois**, em branch de
`develop`, com `/release` próprio, sem outro WP no mesmo deploy. Nota na D13 em `decisoes.md`.

**Branch:** `feat/wp-29-previa-do-convite`, de `develop` atualizado **depois** do deploy único; PR
mira `develop`.

**Achados roteados:** nenhum novo. Toca a parte do convite de `OG-MOCKUP-JPEG-PESADO-01` (JPEG
com extensão `.png`, 542 KB), que segue no WP-20 para as landings.

**Objetivo:** o convite (`/lotto-expert/sweepstake-invite/lottoexpert-invite.html`, ADR-001)
aponta `og:image` para uma imagem 1200×630, ≤ 300 KB, feita a partir de captura real do
LottoExpert 2.06.00, com `og:image:width`/`height`/`type`/`alt` iguais ao arquivo — com o mesmo
caminho do convite, o mesmo parse de `?d=` e o mesmo comportamento de abrir o app.

**Contexto** (medido em 2026-11-24, branch `docs/d3-nao-medir-handoff`):

- Pedido do usuário (2026-11-24): "tem o link do bolão que usa uma imagem hoje, essa imagem também
  teria de ser atualizada." O LottoExpert fechou a 2.06.00 hoje (tag `v2.06.00` em
  `../lotto-expert`, commit `98bffa6`, 2026-11-24 14:44 -0300).
- `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html:13-15`: `og:image` =
  `https://ghfsoftware.com/assets/lottoexpert_app_mockup.png`, `og:image:width`/`height` 1024.
  Não há `og:image:type` nem `og:image:alt`. É a imagem da prévia no WhatsApp.
- `file public/assets/lottoexpert_app_mockup.png`: **JPEG** 1024×1024 com extensão `.png`, 542,4 KB
  (o Pages serve `image/png`). O achado `OG-MOCKUP-JPEG-PESADO-01` registra que o WhatsApp
  costuma omitir prévia acima de ~300 KB (no teste do WP-03 ela saiu mesmo assim).
- O mesmo arquivo é o `og:image` da landing do LottoExpert
  (`src/components/paginas/PaginaLottoExpert.astro:25`), e o `Base.astro:9,131-133` lê
  width/height do cabeçalho do arquivo. Trocar os bytes no mesmo caminho troca também a prévia da
  landing, que é do WP-20 (D16).
- **Contrato byte a byte.** `tools/contrato.sha256:1` (convite, `27925c02…0af1`) e `:3`
  (`assets/lottoexpert_app_mockup.png`, `b3583319…c550`). Conferido por
  `cd dist && sha256sum --quiet -c ../tools/contrato.sha256` no `pr.yml:85-89` e no
  `deploy.yml:57-59`: o deploy falha se divergir. A comparação é contra o arquivo
  `tools/contrato.sha256`, não contra `origin/master` por `git`: ele foi escrito com os bytes
  publicados, e a troca controlada é **editar `tools/contrato.sha256` no mesmo PR**, como diz o
  comentário de `pr.yml:87-88` ("Mudar um deles é decisão do usuário: atualiza
  tools/contrato.sha256 no mesmo PR, com teste de link real").
- `tools/check_site.py:866` `CONGELADAS` (o `.html` de `contrato.sha256`, conferido em `:876-880`)
  isenta o convite de todo o §14, inclusive da regra de `og:image:width`×`height` iguais ao
  arquivo (`:1038-1053`). Hoje nada confere as dimensões declaradas no convite. O §2 (`:349-357`)
  só confere que o arquivo do `og:image` existe.
- `tools/check_site.py:806-807`: `public/` tem o primeiro nível fechado e só o convite como `.html`;
  arquivo de imagem novo ao lado do convite não abre a lista (precedente: veredito do WP-23, §1).

**Veredito de arquitetura (site-arquiteto, 2026-11-24):**

1. **Caminho novo, ao lado do convite** (recomendado; a escolha é a D32 (1)):
   `public/lotto-expert/sweepstake-invite/og-convite-2-06-00.jpg`. Por quê:
   - o caminho antigo é compartilhado com a landing do LottoExpert
     (`PaginaLottoExpert.astro:25`): mesmo caminho = este WP muda a prévia da landing, fora do
     escopo e em colisão com o WP-20;
   - mesmo caminho mantém um JPEG servido como `image/png` (`OG-MOCKUP-JPEG-PESADO-01`), e
     `og:image:type` coerente fica impossível;
   - o WhatsApp e o Facebook guardam em cache a imagem pela URL da imagem; URL nova força a busca
     do arquivo novo; nome com a versão (`2-06-00`) deixa a próxima troca fazer o mesmo;
   - com 1200×630 o convite muda de qualquer jeito (`:14-15`), então "mesmo caminho para não tocar
     o HTML" só vale se a imagem continuar quadrada 1024×1024 — o que contraria a D16.

   Ao lado do convite, e não em `public/assets/`, pelo mesmo motivo do WP-23 §1: os arquivos de que
   o convite depende ficam juntos e no contrato. Prova de que a URL não é contratual nova: nenhum
   app nem a Play aponta para ela; só o `<meta>` do convite.
2. **`assets/lottoexpert_app_mockup.png` fica no ar, sem mudança de bytes**: a landing do LottoExpert
   ainda o usa até o WP-20, e mensagens antigas não dependem dele (ver "Irreversível"). Ele **sai** de
   `tools/contrato.sha256`, porque deixa de ser a imagem do convite; a linha da imagem nova entra no
   lugar. Assim o WP-20 pode trocar a imagem da landing sem tocar no contrato.
3. **O HTML do convite muda só no `<head>`, nas linhas de `og:image`** (`:13-15` e duas linhas
   novas, `og:image:type` e `og:image:alt`). O bloco `<script>` de `:289-429` (parse de `?d=`, v1 e
   v2, `pako.ungzip`, `window.location = appUrl`) não muda: prova por `diff` do bloco. O caminho do
   convite não muda; `assetlinks.json` e `CNAME` não mudam.
4. **Guarda nova no `check_site.py`**, porque o §14 pula o convite: para cada página de
   `CONGELADAS`, `og:image` é URL absoluta de arquivo do site, `og:image:width`×`height` iguais ao
   arquivo (usa `dimensoes()` de `:940`), `og:image:type` igual ao formato real (JPEG ou PNG pelo
   cabeçalho, não pela extensão), `og:image:alt` presente e arquivo ≤ 300 KB. É regra só de `og:*`;
   o resto do §14 continua isento (deep link, ADR-005).
5. **Sem ADR novo.** ADR-001 (caminho do convite e `?d=` intocados), ADR-002 §3 (`public/` byte a
   byte) e ADR-006 §2 (URL fixa em `public/`) cobrem. Formato, conteúdo e caminho são a D32.

**Formato** (D16 e D32 (2)): 1200×630 (1,91:1), JPEG com extensão `.jpg`, ≤ 300 KB.
`og:image:width` 1200, `og:image:height` 630, `og:image:type` `image/jpeg`, `og:image:alt` em pt
(o convite é só pt). Quadrado (1024×1024) o WhatsApp mostra como miniatura pequena ao lado do
texto; 1,91:1 ele mostra como prévia grande.

**Origem da imagem** (D26 e D32 (3)): captura real do LottoExpert 2.06.00, sem dado pessoal. O
agente pode capturar pelo emulador (`../lotto-expert/scripts/emulador.sh subir`, AVD sem conta nem
dado de ninguém) com bolão de exemplo; a tela é a da D32 (3). A captura é retrato; a arte
1200×630 (fundo, enquadramento, texto) é composta pelo usuário ou no Claude Design (WP-06, D4). O
agente **não gera mockup** nem edita o conteúdo da captura (D26); só converte e comprime o export
final para ≤ 300 KB. Texto dentro da imagem segue a régua de jogo responsável (o
`check_site.py` não lê imagem: conferência no navegador). O `og:image:alt` segue a D25 (texto com
origem: resposta do usuário registrada aqui).

**Relação com outros WPs:**

- **WP-23** (convite sem terceiros) e **este WP** mudam o convite e `tools/contrato.sha256` depois
  do deploy único, cada um com `/release` próprio. Não dependem um do outro; **não** vão no mesmo
  release. O que for segundo refaz os critérios de contrato dele sobre o `contrato.sha256` do
  primeiro (o WP-23 diz hoje "mockup igual"; se este WP for antes, a linha do mockup já terá
  saído). Ordem entre os dois: pergunta ao usuário.
- **WP-24** (redesign do convite) vem depois dos dois; ele preserva os `og:*` que estiverem no ar.
  O texto "Fora: … `og:image` (`assets/lottoexpert_app_mockup.png`, cujo hash não muda)" do WP-24
  fica velho com este WP: o `site-docs` atualiza na escrituração deste WP.
- **WP-20** (imagens 1200×630 das landings) vai no deploy único e não toca o convite. A imagem do
  LottoExpert do WP-20 pode servir de base para a arte deste WP (D32 (3), opção c), mas como
  **arquivo separado** ao lado do convite: compartilhar o arquivo amarraria a prévia da landing ao
  contrato.

**Ler antes:** ADR-001 inteiro; ADR-006 §2; D13, D16, D26, D32 em `decisoes.md`; WP-23 (veredito,
rollback, roteiro de navegador); o `<head>` do convite (`:1-20`); `tools/check_site.py` §2
(`:349-372`), §13 (`:801-835`), §14 (`:862-880`, `:1038-1053`), `dimensoes()` (`:940`).

**Arquivos-alvo:**

- `public/lotto-expert/sweepstake-invite/og-convite-2-06-00.jpg` (novo; nome final conforme D32 (1))
- `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html` (só `:13-15` e as linhas novas
  de `og:image:type` e `og:image:alt`)
- `tools/contrato.sha256` (linha do convite trocada; linha do mockup trocada pela da imagem nova)
- `tools/check_site.py` (guarda do passo 5 e docstring)
- `design/handoff/<data>/` (export da arte, se for do Claude Design)

**Passos:**

1. Pré-voo: deploy único em `master` (comando em "Depende de") e teste do D13 (4) relatado; D32
   decidida; ordem com o WP-23 decidida. Branch de `develop` atualizado.
2. Captura: `../lotto-expert/scripts/emulador.sh subir`, instalar o build da tag `v2.06.00`,
   montar o bolão de exemplo da D32 (3), capturar com `adb -s emulator-5580 exec-out screencap -p`.
   Conferir que não há dado pessoal. Entregar a captura ao usuário.
3. **Usuário:** compõe a arte 1200×630 (ou sessão no Claude Design) e entrega o export.
4. Agente: converter o export para JPEG ≤ 300 KB sem mudar o conteúdo; `file` mostra
   `JPEG … 1200x630`; copiar para o caminho da D32 (1).
5. `check_site.py`: guarda do veredito (4). Prova de mutação, cada uma acusa e depois reverte:
   width 1024; `og:image:type` `image/png`; `og:image:alt` removido; imagem de 400 KB; `og:image`
   para arquivo inexistente.
6. Convite: `:13` aponta para a URL nova; `:14-15` 1200 e 630; duas linhas novas
   `og:image:type` e `og:image:alt`. Nada mais muda.
7. `tools/contrato.sha256`: hash novo do convite; linha `assets/lottoexpert_app_mockup.png` trocada
   pela da imagem nova; `assetlinks.json` e `CNAME` iguais.
8. `/verify`; auditoria `site-qa` + `site-seo-perf`.
9. Rollback preparado antes do `/release`: tag `pre-wp-29` no `master` publicado e acrescentada à
   política do ambiente `github-pages` (mesmo comando do D13 (5), com `name=pre-wp-29`).

**Critérios de aceite:**

- `file dist/lotto-expert/sweepstake-invite/og-convite-2-06-00.jpg` mostra `JPEG` e `1200x630`;
  `stat -c %s` ≤ 307200.
- `grep -n 'og:image' dist/lotto-expert/sweepstake-invite/lottoexpert-invite.html`: `og:image` =
  `https://ghfsoftware.com/lotto-expert/sweepstake-invite/og-convite-2-06-00.jpg`, width 1200,
  height 630, type `image/jpeg`, `alt` não vazio.
- Bloco `<script>` (do `<script>` sem `src` ao `</script>`) do convite antes e depois: `diff` vazio.
  `git diff` do convite: só linhas `og:image*` no `<head>`.
- `git diff tools/contrato.sha256`: linha do convite trocada, linha do mockup trocada pela da
  imagem nova, `assetlinks.json` e `CNAME` iguais; `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` sai 0.
- `sha256sum public/assets/lottoexpert_app_mockup.png` = `b358331990e6c60d8900888b789f252665267edfa35d6471dd2347b9a6f1c550`
  (o arquivo antigo continua no ar, igual).
- `python3 tools/check_site.py --raiz dist` verde, URLs contratuais presentes, as 5 mutações do
  passo 5 acusam (saída no commit).
- `npx html-validate 'dist/**/*.html'` e `lychee --offline` sobre `dist/` sem erro.

**Só no navegador** — o usuário faz e reporta; sem o relato o WP não fecha.

*Antes do merge:*

1. A arte: sem dado pessoal, sem "aumenta suas chances", "maximize" ou "garantia de prêmio";
   legível a 360 px de largura de tela (tamanho da prévia no WhatsApp).
2. `dist/` local (`python3 -m http.server 8080 -d dist`): um convite real v1 e um v2 com
   `https://ghfsoftware.com` trocado por `http://<ip>:8080` abrem o card como hoje (PC 1280,
   Android 360).

*Depois do `/release` (produção):*

3. **Link novo:** gerar convite no app e mandar pelo WhatsApp: a prévia mostra a imagem nova,
   grande (1,91:1), com o título de sempre. Se vier a antiga ou nenhuma, anotar e testar no
   Sharing Debugger do Facebook (`https://developers.facebook.com/tools/debug/`) com a URL do
   convite.
4. **Link já compartilhado** (mensagem anterior ao release): a mensagem segue com a miniatura que
   já tinha, e tocar abre o convite.
5. Android **com** o app: tocar o link novo abre o app direto (App Links) e importa o bolão.
6. Android **sem** o app e PC em aba anônima: o card aparece, v1 e v2.

**Irreversível:** nada sai do site. O caminho do convite, o `?d=`, `assetlinks.json` e
`lottoexpert_app_mockup.png` ficam no ar. Prévia de mensagem já enviada no WhatsApp **não** muda:
a miniatura vai dentro da mensagem; é o esperado, não falha. App instalado: App Links depende do
`assetlinks.json` (hash inalterado) e do caminho — abre igual. O que não volta: o cache do
WhatsApp/Facebook da URL nova da imagem; se a arte sair errada, a correção é outro arquivo com
outro nome, não sobrescrever o mesmo.

**Rollback:** `gh workflow run deploy.yml --ref pre-wp-29` (republica o artefato anterior em
minutos); depois `git revert` do merge pelo fluxo normal. A tag sai da política quando o WP fechar.

**Risco:** alto (URL contratual e deploy). Específicos: (a) edição do convite fora do `<head>`
quebra o parse de `?d=` — o `diff` do bloco `<script>` fecha; (b) imagem > 300 KB e o WhatsApp
omite a prévia — guarda do passo 5; (c) dimensões declaradas diferentes do arquivo e a prévia sai
cortada — guarda do passo 5; (d) WhatsApp mostrando a imagem antiga por cache — caminho novo
(D32 (1)); (e) captura com dado pessoal ou copy barrada dentro da imagem — conferência do usuário.
