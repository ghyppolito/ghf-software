---
id: WP-25
titulo: O build sai do Astro 7.3.8 e o npm audit não acusa dependência vulnerável
area: infra
status: todo
depende_de: [WP-08]
adr: [ADR-001, ADR-002, ADR-008]
spec: ""
decisoes: [D13]
tamanho: S
risco: alto
visual: false
branch: feat/wp-25-dependencias
---

# WP-25 — O build sai do Astro 7.3.8 e o npm audit não acusa dependência vulnerável

**Depende de:** WP-08 (integração `feat/wp-08-layout-unico`, D13) e a **fatia 1 do WP-10
integrada nela**. Essa fatia trocou o Tailwind 3 pelo 4 e reescreveu `package.json` e
`package-lock.json`. Isso não entra em `depende_de`: o WP-10 só fecha no fim do redesign, e a
dependência é do commit, não do WP. O pré-voo prova:
`git merge-base --is-ancestor e3430b7 feat/wp-08-layout-unico` sai 0. Antes disso o WP não
começa: os dois mexeriam no mesmo lockfile. · **Achados roteados:** `ASTRO-UNDICI-AUDIT-01`

**Branch:** `feat/wp-25-dependencias`, criada de `feat/wp-08-layout-unico` depois da fatia 1.
Volta para a integração por merge do usuário e vai ao ar no deploy único (D13). Não é hotfix
de `master`: os avisos só valem no build, como mostra o Contexto.

**Um `doing` por vez:** o WP-10 está `doing`. Este WP roda **entre a fatia 1 e a fatia 2** do
WP-10. Enquanto ele roda, o WP-10 fica `blocked` (motivo: "aguarda WP-25", em `BLOQUEIOS`).
Ele volta a `doing` quando o WP-25 fecha. Por quê: assim as fatias 2 em diante do WP-10, e o
checklist de navegador delas, já rodam no Astro novo, e o upgrade não fica para o fim. A
alternativa é rodar este WP depois do WP-10 `done`. Ela custa refazer a prova visual do
redesign inteiro sobre outro Astro. **Decidido pelo usuário em 2026-11-21: entre as fatias 1 e 2** ("Pode registrar as recomendações").

**Objetivo:** o `npm audit` sobre a integração sai com 0 avisos. Cada versão nova é exata e foi
publicada há mais de 14 dias. O `dist/` sai igual ao de antes, ou cada diferença tem motivo.

**Contexto:** `npm audit` em e3430b7 (2026-11-21): 3 avisos (2 moderate, 1 high).

| Pacote | Instalado | Quem traz | Prod/dev | Avisos (GHSA) | 1.ª versão corrigida |
|---|---|---|---|---|---|
| `astro` | 7.3.8 (`package.json:16`) | direto | prod | mh32-jxcr-mh9f (≤ 7.4.4, XSS por nome de tag dinâmico); r3h5-4585-7x3w (≥ 5.14.3 ≤ 7.4.6; só tem efeito com `@astrojs/node`, que o site não usa) | 7.4.7 |
| `undici` | 8.11.2 | `astro` → `unifont@0.7.5` | prod | 8 avisos: 4w7w, 2m5v, qrxm, 9fm3, 55wc, xjj6, 4qv8, f72v (DoS, TLS, SRI, redirect) | 8.12.2 |
| `fast-uri` | 3.1.8 | `html-validate@11.16.2` → `ajv@8.20.0` (`^3.0.1`) | **dev** | 4 avisos: w74x, xhq7, wjr9, 333x (publicados em 2026-10-23) | 3.1.9 |

- **`fast-uri` não saiu com o Tailwind 3.** Ele vem do `html-validate` e já estava no lockfile
  da integração antes da fatia 1 (`git show feat/wp-08-layout-unico:package-lock.json`, entrada
  `node_modules/fast-uri`, 3.1.8). `npm ls --omit=dev fast-uri` sai vazio. Só o lint do CI o
  executa, e ele não entra em `dist/`.
- **Nenhum dos três chega ao visitante.** O `dist/` é HTML, CSS e fonte estáticos.
  - O `undici` roda no build: é o cliente HTTP do `unifont`, o resolvedor de fontes do Astro.
  - O XSS da mh32 exige que um nome de tag dinâmico venha de entrada do usuário. No site estático
    não há essa entrada, e `src/` não tem componente de tag dinâmica (grep por `<Tag`, `as=`).
  - Por isso o conserto vai no deploy único, sem hotfix.
- **O `npm audit` sugere `astro@7.4.13`, mas essa versão não serve.** Ela saiu em 2026-11-18,
  menos de 14 dias atrás. A 7.4.7 (2026-11-05) já corrige as duas GHSA do Astro (API
  `/advisories` do GitHub, campo `first_patched_version`).
- **A 7.4.7 puxa três mudanças a mais:**
  - **Node.** `engines.node` passa a `>=22.23.4` (a 7.3.8 pede `>=22.12.0`; o piso subiu na
    7.4.5). O CI usa `node-version: '22.22'` em `.github/workflows/pr.yml:62` e `:135` e em
    `.github/workflows/deploy.yml:38`. O `package.json:6` declara `"node": "^22.22.0"`. Node
    22.23.4 saiu em 2026-10-21; o 22.23.5 (2026-11-11) ainda não tem 14 dias. Por isso o CI
    fixa `22.23.4` exato, não `22.23`. `html-validate` (`^22.22.0 || >= 24.8.0`) e `lighthouse`
    (`>=22.19`) aceitam esse Node.
  - **Markdown.** `@astrojs/markdown-satteri` vai de 0.4.3 para 0.4.7. O Astro 7.4.7 depende da
    0.4.7, e o site declara a 0.4.3 direto (`package.json:15`). A versão direta sobe junto para
    não duplicar o pacote. Essa é a etapa que gera o HTML das páginas legais.
  - **Fontes e Vite.** `unifont` vai de `~0.7.5` para `^1.0.3`, e `vite` de `^8.3.1` para `^8.3.5`.
- **Versões transitivas.** `undici` (`^8.0.0` no `unifont@1.0.3`) e `fast-uri` resolvem para a
  versão mais nova do range. Hoje essa versão é o `undici` 8.13.1, de 2026-11-20. O
  `npm install --before=2026-11-07` limita a resolução a versões de antes de 2026-11-07: dá
  `undici` 8.12.4, `fast-uri` 3.1.9 e `vite` ≤ 8.3.6. Assim não é preciso `overrides`.

**Ler antes:** ADR-002 §1 (Astro e Node fixados, lockfile versionado); ADR-008 §7 (plugin
`sem-polyfill`, fixture do Tailwind 4.3.5); ADR-001 (caminhos contratuais);
`tools/contrato.sha256`.

**Arquivos-alvo:** `package.json`, `package-lock.json`, `.github/workflows/pr.yml` (só as duas
linhas `node-version` e o comentário de `:61`), `.github/workflows/deploy.yml` (só
`node-version`), `README.md:63` e `CLAUDE.md:112` (versão do Node), ADR-002 (nota de rodapé:
Astro 7.4.7 e Node 22.23.4, mesma política de versão exata — não muda a decisão).

**Passos:**
1. Pré-voo: rodar `git merge-base --is-ancestor e3430b7 feat/wp-08-layout-unico`, que deve sair
   0. Depois `node -v` deve dar `v22.23.4`. Em seguida `npm ci && npm run build`, copiar `dist/`
   para `<scratchpad>/dist-antes` e salvar `npm audit --json` como linha de base.
2. `npm install --save-exact --before=2026-11-07 astro@7.4.7 @astrojs/markdown-satteri@0.4.7`.
3. Rodar `npm audit`. Se sobrar `undici` < 8.12.2 ou `fast-uri` < 3.1.9, rodar
   `npm update undici fast-uri --before=2026-11-07`. Não usar `npm audit fix --force`.
4. `engines.node` passa a `"^22.23.4"`. `node-version: '22.23.4'` nos três pontos dos workflows.
   README, `CLAUDE.md` e a nota do ADR-002 recebem a versão nova.
5. `npm ci && npm run build`, copiar o resultado para `<scratchpad>/dist-depois`, e comparar com
   os hashes normalizados:
   `diff -r <(cd dist-antes && find . -type f | sed -E 's/\.[A-Za-z0-9_-]{8}\./.HASH./' | sort) <(… dist-depois …)`
   e, por arquivo, `diff` do conteúdo com a mesma troca de hash aplicada.
6. Cada diferença vai para o WP: o arquivo, a linha, e o pacote e a versão que a causaram.

**Critérios de aceite:**
- `npm audit` sai com `found 0 vulnerabilities`. Se sobrar aviso, o WP registra a GHSA, por que
  não tem conserto com 14 dias e por que não chega a `dist/`.
- `package.json` sem `^` nem `~` em `dependencies` e `devDependencies`: `astro` `7.4.7`,
  `@astrojs/markdown-satteri` `0.4.7`.
- Cada pacote que mudou no `package-lock.json` tem `time[versão]` anterior a 2026-11-07.
  Conferir com `npm view <pacote> time --json` sobre a lista de `git diff` do lockfile.
- `npm ls --omit=dev undici` mostra ≥ 8.12.2. `npm ls fast-uri` mostra ≥ 3.1.9.
- O diff entre `dist-antes` e `dist-depois`, com hashes normalizados, sai vazio, ou cada
  diferença está explicada no WP (passo 6). Diferença no HTML das legais não pode mudar o texto.
  O texto visível de cada legal antes e depois tem de ser igual: comparar `<main>` sem tags.
- `cd dist && sha256sum --quiet -c ../tools/contrato.sha256` sai 0.
- `python3 tools/check_site.py` e `python3 tools/check_site.py --raiz dist` saem 0.
- `npx html-validate 'dist/**/*.html'` sai 0.
- `lychee --offline --no-progress --root-dir "$PWD/dist" 'dist/**/*.html'` sai 0.
- `npm run test:css` passa (21 testes). A fixture `tools/fixtures/sem-polyfill/` não muda: o
  Tailwind continua 4.3.5.
- `python3 tools/lighthouse.py --raiz dist` (sem `--medir`) cumpre o orçamento de
  `tools/orcamento-lighthouse.json`.
- No PR para a integração, os jobs `plano`, `site` e `lighthouse` passam no Node 22.23.4.

**Irreversível:** nada sai do site neste WP. Ele não publica: entra na integração e só vai ao
ar no deploy único (D13). O risco está no build que o `deploy.yml` faz nesse dia, pelos motivos
abaixo:
- Astro, Node e o renderizador de markdown das legais trocam juntos.
- Um caminho contratual pode deixar de sair em `dist/`. O `contrato.sha256` (convite,
  `assetlinks.json`, mockup, `CNAME`) e o §15 do `check_site.py` barram isso no PR e no deploy.

**Reversão:** antes do deploy único, `git revert` do commit do WP na integração. O lockfile
antigo volta e o `node-version` volta para `22.22`. Depois do deploy, vale o rollback da D13 (5):
`gh workflow run deploy.yml --ref pre-modernizacao`.

**Risco:** alto. O WP toca o deploy: o `node-version` do `deploy.yml` e o build que ele executa.
Também troca o renderizador do HTML das páginas legais. O que pode dar errado:
- O `unifont` 1.x muda o nome ou o recorte do `.woff2` publicado. Aí as fontes mudam de bytes e
  o `lighthouse` acusa.
- O satteri 0.4.7 muda âncoras ou tipografia (smartypants) do markdown legal. Aí o §9 e o §17
  do `check_site.py` acusam, e o diff de `dist/` mostra.
- O Vite 8.3.6 reordena o CSS. Aí o `test:css` passa, mas o CSS de `dist/` muda.
- O setup-node não acha `22.23.4` no cache do runner e baixa a versão (só fica mais lento).
