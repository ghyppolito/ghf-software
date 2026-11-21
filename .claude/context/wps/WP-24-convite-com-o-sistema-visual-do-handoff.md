---
id: WP-24
titulo: O convite do bolão segue o sistema visual do handoff, com o parse de `?d=` intocado
area: design
status: todo
depende_de: [WP-10, WP-23]
adr: [ADR-001, ADR-006, ADR-008]
spec: docs/AVALIACAO.md
decisoes: [D4, D13, D25]
tamanho: M
risco: alto
visual: true
branch: feat/wp-24-convite-redesign
---

# WP-24 — O convite do bolão segue o sistema visual do handoff

**Depende de:** WP-10 (tokens e sistema visual no ar pelo deploy único, D13) e WP-23 (convite sem
terceiros, com `<main>`, já publicado). O WP-23 só começa depois do deploy único, então este WP
também. Pré-voo: `git fetch origin && git merge-base --is-ancestor <commit do WP-23 em develop> origin/master`
sai 0, ou seja, o `/release` do WP-23 já foi ao ar e o teste de produção dele foi relatado.

**Branch:** `feat/wp-24-convite-redesign`, de `develop`, depois do `/release` do WP-23. PR mira
`develop`. Vai ao ar num `/release` **próprio** (resposta 6 do veredito do WP-10, 2026-11-21),
sem outro WP no mesmo deploy, numa janela de pouco uso do bolão escolhida pelo usuário.

**Achados roteados:** `CONVITE-REDESIGN-CONTRATO-01`. **Não entra:** `CONVITE-TEMA-ESCURO-01`
(segue `nota`; o usuário pediu para não criar WP ainda — tema escuro desenhado é D nova).

**Objetivo:** o convite (`/lotto-expert/sweepstake-invite/lottoexpert-invite.html`, ADR-001) tem a
aparência de `design/handoff/2026-10-13-rodada-3/Convite Bolao.dc.html`, com o mesmo caminho, o
mesmo parse de `?d=` (v1 e v2), os mesmos `og:*` e o mesmo comportamento de abrir o app.

**Contexto:**

- O WP-10 tirou o convite do redesign: a D13 congela os bytes dele até o deploy único
  (`tools/contrato.sha256:1`, conferido no `pr.yml` e no `deploy.yml`), e um convite redesenhado
  reprovaria o próprio deploy (WP-10, "Plano").
- O export tem `Convite Bolao.dc.html` (71 linhas) a 360 e 1280 (`design/README.md:137`). A página
  publicada tem 431 linhas: o JS de decodificação (`pako.ungzip`, v1 e v2), a mensagem de erro e o
  `window.location = appUrl` são do app (`SweepstakeCoder.kt`, ADR-006 do app) e não são desenho.
- A copy do export é placeholder (D25). O rodapé do export (`Convite Bolao.dc.html:58`) traz
  frases sem origem ("nenhum servidor guarda este convite").

**Decisão de arquitetura no pré-voo (`site-arquiteto`).** O convite fica em `public/`, copiado
byte a byte, e não lê `src/styles/tokens.css`. Copiar valores de token para o `<style>` inline
duplica o tema (reprovado pela regra "um lugar só"). Gerar o convite pelo Astro no mesmo caminho
liga o hash do `.html` ao hash do CSS, que muda a cada build, e o `contrato.sha256` deixa de ser
estável. O arquiteto escolhe entre (a) página gerada com o CSS do convite inline no build e hash
reprodutível, (b) cópia em `public/` com um passo de build que injeta os tokens, ou (c) outra
proposta, e escreve o ADR antes do `site-dev`. Sem ADR, o WP não passa do passo 2.

**Ler antes:** ADR-001 inteiro; ADR-006 §2 e §5; ADR-008; WP-23 (veredito e roteiro de navegador);
`Convite Bolao.dc.html`; o convite publicado inteiro; `SweepstakeCoder.kt:30-82`.

**Arquivos-alvo:** `public/lotto-expert/sweepstake-invite/lottoexpert-invite.html` (só o CSS e o
markup do card), `tools/contrato.sha256` (só a linha do convite), e o que o ADR do pré-voo listar
(nenhum caminho novo em `public/` sem ele). **Fora:** o JS de `?d=`, os `og:*`, o `og:image`
(`assets/lottoexpert_app_mockup.png`, cujo hash não muda), `.well-known/assetlinks.json`, `CNAME`.

**Passos:**

1. Pré-voo: `/release` do WP-23 no ar e relatado; ADR do convite (ver acima).
2. `site-ux` DESENHAR: estados do card (carregando, v1, v2, erro sem `?d=`, erro de decodificação),
   360 e 1280, contra o export; texto de cada estado com origem (D25).
3. `site-dev`: troca CSS e markup do card. O bloco `<script>` de decodificação sai igual,
   conferido por diff do bloco antes e depois (vazio).
4. `tools/contrato.sha256`: hash novo do convite; as outras linhas iguais.
5. `/verify`; auditoria `site-qa` + `site-seo-perf` + `site-ux` AUDITAR.

**Critérios de aceite:**

- O bloco `<script>` de decodificação é idêntico ao publicado: extrair o bloco das duas versões e
  `diff` vazio.
- `grep -n 'og:' ` do convite antes e depois: `diff` vazio.
- `git diff tools/contrato.sha256` mostra só a linha do convite trocada.
- `python3 tools/check_site.py --raiz dist` verde, com as URLs contratuais presentes e o convite
  nas guardas §15 (a)/(b) e §17 (do WP-23).
- `npx html-validate 'dist/**/*.html'` e `lychee --offline` sobre `dist/` sem erro.
- `python3 tools/lighthouse.py` verde no orçamento do convite (WP-23); nenhuma requisição a outra
  origem.
- Contraste AA de todo texto do card (relato do `site-ux` com os pares medidos).

**Só no navegador** — o usuário faz e reporta; sem o relato o WP não fecha. Mesmo roteiro do
WP-23, nos dois momentos: antes do merge, com `dist/` local, dois convites reais gerados no app no
mesmo dia (um **v1** e um **v2**), PC 1280 e Android 360, sem `?d=` e com `?d=abc`; depois do
`/release`, convite novo pelo WhatsApp (prévia com título e mockup como antes), Android com o app
(abre o app pelo App Links e importa o bolão), Android sem o app e PC (card aparece, v1 e v2).
Comparar cada estado com `Convite Bolao.dc.html` a 360 e 1280.

**Irreversível:** nada sai do site; caminho, `?d=`, `assetlinks.json` e `og:image` ficam. O risco
é o convite deixar de decodificar um link já enviado: links antigos no WhatsApp continuam
apontando para a mesma página. Reversão: `git revert` do merge e `/release`; o hash anterior volta
com ele.

**Risco:** alto — URL contratual aberta por usuários do app a partir do WhatsApp. O que pode dar
errado: CSS novo esconder o card em navegador antigo (o convite não segue o piso da D24; o ADR do
pré-voo diz qual piso vale aqui), JS tocado por engano, prévia do WhatsApp sem imagem.
