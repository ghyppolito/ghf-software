---
id: WP-32
titulo: O Lighthouse do CI mede o site com gzip, como o GitHub Pages entrega
area: infra
status: todo
depende_de: []
adr: []
spec: ""
decisoes: [D20]
tamanho: S
risco: medio
visual: false
branch: feat/wp-32-lighthouse-com-gzip
---

# WP-32 — O Lighthouse do CI mede o site com gzip, como o GitHub Pages entrega

**Depende de:** — · **Achados roteados:** `ORCAMENTO-LH-FOLGA-01` (a recalibração resolve; vinha da fatia 10b do WP-10)

**Base:** a branch sai de `feat/wp-08-layout-unico` (integração do deploy único, D13), não de `develop`: o Pages hoje serve o site antigo, e o orçamento só faz sentido medido sobre as páginas novas. PR mira `feat/wp-08-layout-unico` (usuário, 2026-11-24).

**Objetivo:** `tools/lighthouse.py` serve `dist/` com `Content-Encoding: gzip` nos tipos de texto
quando o cliente manda `Accept-Encoding: gzip`, como o Pages, e o orçamento de bytes de
`tools/orcamento-lighthouse.json` passa a ser calibrado sobre o que o Pages transfere.

**Contexto:** pedido do usuário (questionário de 2026-11-24), a partir da auditoria `site-seo-perf`
da fatia 2 do WP-30.
- `tools/lighthouse.py:60-62` serve `dist/` com `ThreadingHTTPServer` e `SimpleHTTPRequestHandler`,
  sem compressão; a docstring (`tools/lighthouse.py:4-5`) diz "sem gzip" de propósito. A D20
  (`decisoes.md:32`) fixou "serve `dist/` sem gzip" para manter as condições da linha de base do
  WP-12. **Este WP emenda essa cláusula da D20** (emenda confirmada pelo usuário em 2026-11-24 e
  registrada na linha da D20); o resto dela (versão 13.5.0, 3 runs, mediana, regras do §7 do WP-12) fica.
- O Pages comprime. Medido em 2026-11-24 contra `https://ghfsoftware.com` (site antigo, `master`):
  `/` e `/lotto-expert/sweepstake-invite/lottoexpert-invite.html` saem com `content-encoding: gzip`;
  `/.well-known/assetlinks.json` também (`application/json`); `/assets/GHFSoftware.png` sai sem
  codificação. Com `Accept-Encoding: br` sozinho, nenhuma codificação: **o Pages não serve brotli**.
  O lab, portanto, simula só gzip. CSS, JS e SVG não existem no `master` atual para medir; o passo 1
  confere no primeiro ambiente onde existirem, ou assume o comportamento do HTML/JSON (mesmo
  servidor, varnish do GitHub, `vary: Accept-Encoding`).
- Efeito no lab (auditoria `site-seo-perf`, Lighthouse 13.5.0 mobile, throttling simulado, que
  estima tempo a partir do `transferSize`): `/lottoexpert.html` LCP 2476 ms sem gzip contra 1728 ms
  com gzip (FCP 1351 → 903); `/eclipsego.html` LCP 2027 → 1427 ms. CSS compartilhado 77 KB cru,
  ≈ 14,6 KB gzip; HTML de 53 KB, ≈ 11,8 KB. O CSS bloqueante pesa 451 ms no lab. O lab hoje
  superestima o tempo e aperta a página por um custo que o usuário real não paga.
- Os `bytes_total` de `tools/orcamento-lighthouse.json` são medido + 20% **sem gzip**
  (`tools/lighthouse.py:96-98` soma `transferSize`, que sem compressão é o tamanho cru). Com gzip
  o total cai, e o orçamento fica frouxo até ser recalibrado. `bytes_imagem` não muda (imagem não
  é comprimida pelo Pages nem pelo lab).

**Ler antes:** `tools/lighthouse.py` inteiro; D20 em `.claude/context/decisoes.md:32`; a seção
"Regras" do veredito do WP-12 (`wps/WP-12-performance.md`, §7). Nada além disso.

**Arquivos-alvo:**
- `tools/lighthouse.py`
- `tools/orcamento-lighthouse.json`
- `docs/ARQUITETURA.md` (linha da tabela de `tools/`, hoje `:128`, e o parágrafo do CI se citar o servidor)

Fora da lista, de propósito: `.github/workflows/pr.yml` (o job `lighthouse` continua chamando o
mesmo script com os mesmos argumentos; nenhuma mudança necessária), `src/`, `public/`, `design/`.
Se o workflow precisar mudar, parar e reportar.

**Passos:**
1. Conferir os tipos que o Pages comprime: `curl -sI -H 'Accept-Encoding: gzip, br' <url>` em HTML,
   JSON, CSS, JS, SVG, `.webmanifest`, `.woff2` e WebP do ambiente publicado que os tiver. Registrar
   a saída no fechamento do WP. Onde não houver como medir, registrar como suposição.
2. Em `tools/lighthouse.py`, trocar `Silencioso` por um handler que, quando o pedido tem `gzip` em
   `Accept-Encoding` e o arquivo é de tipo de texto (`text/*`, `application/json`,
   `application/javascript`, `image/svg+xml`, `application/manifest+json`, `application/xml`),
   comprime o corpo com `gzip` nível 6 (biblioteca padrão), envia `Content-Encoding: gzip`,
   `Vary: Accept-Encoding` e o `Content-Length` comprimido; `HEAD` responde os mesmos cabeçalhos.
   Imagem, fonte e qualquer outro tipo saem como hoje. Sem brotli (o Pages não serve). Continua só
   biblioteca padrão.
3. Guarda contra regressão do próprio lab: em cada relatório, recurso `Document`, `Stylesheet` ou
   `Script` da origem local com `resourceSize` > 1024 e `transferSize` ≥ `resourceSize` é **erro**
   ("lab sem compressão"). Sem isso, um handler em no-op volta a medir cru sem nenhum sinal.
4. Docstring: trocar "sem gzip" por "com gzip nos tipos de texto, como o Pages (sem brotli)", e a
   frase do orçamento ("medido no fechamento do WP-12 + 20%") pela recalibração deste WP.
5. Medir antes/depois, na mesma máquina e no mesmo commit: `python3 tools/lighthouse.py --raiz dist --medir`
   sem e com o handler. Tabela no fechamento: por página, LCP, FCP, performance, `bytes_total`,
   `bytes_imagem`.
6. **Unidade (usuário, 2026-11-24):** todo teto de bytes conta o transferido comprimido
   (`transferSize`), tanto o `bytes_total` da página quanto o futuro teto de CSS
   (`CSS-ORCAMENTO-BYTES-01`, fatia 10b do WP-10). **Recalibrar só com autorização do usuário:** apresentar a tabela; com o "ok", `bytes_total` de
   cada página = medido com gzip + 20%; `bytes_imagem` mantido (deve ser igual ao medido antes; se
   não for, parar e reportar). `regras` (LCP, performance, CLS) não mudam neste WP.
7. `docs/ARQUITETURA.md`: a linha de `tools/lighthouse.py` diz que o lab serve com gzip como o Pages.
8. Escrituração: a emenda da D20 já está em `decisoes.md` (2026-11-24); no fechamento, só citar o
   commit. A linha de base do WP-12 fica como está, histórica. Fechar `ORCAMENTO-LH-FOLGA-01` com a tabela do passo 5.

**Critérios de aceite:**
- `python3 tools/lighthouse.py --raiz dist` sai 0 com o orçamento recalibrado.
- No relatório JSON da mediana de `/lottoexpert.html`, o documento e o CSS de `/_astro/` têm
  `transferSize` < `resourceSize` (o passo 3 transforma isso em regra; a run passa).
- Mutação: com o handler revertido para `SimpleHTTPRequestHandler`, o script sai 1 com o erro
  "lab sem compressão" (rodar com `--runs 1` e anotar a saída).
- `bytes_imagem` medido com gzip igual ao medido sem gzip em todas as 9 páginas.
- Nenhum arquivo de `dist/` muda: `npm run build` antes e depois dá a mesma árvore
  (`find dist -type f -exec sha256sum {} + | sort` igual), e `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` passa.
- `python3 tools/check_site.py --raiz dist` passa (nenhuma URL contratual tocada).
- Job `lighthouse` do `pr.yml` verde no PR, sem mudança no workflow.

**Risco:** médio — é gate de CI.
- Orçamento frouxo: se o handler entra e a recalibração não, o `bytes_total` fica 4–5× acima do
  transferido em texto e uma regressão grande passa. Por isso handler e recalibração vão no mesmo
  commit.
- Lab otimista demais: gzip nível 6 do Python pode não ser igual ao do Pages (nível e
  implementação desconhecidos); a diferença esperada é pequena, mas o número do lab não é o do
  campo. Registrar a diferença no passo 1 se der para medir o tamanho transferido do Pages
  (`curl --compressed -w '%{size_download}'`).
- Comparação histórica quebra: LCP e bytes do WP-12 e das fatias do WP-10 foram medidos sem gzip e
  deixam de ser comparáveis com os novos. A tabela do passo 5 é a nova linha de base.
- Não esconde problema real: o CSS bloqueante continua bloqueante; o que muda é o custo estimado.
  Os achados de CSS (`CSS-ORCAMENTO-BYTES-01`) seguem com o WP-10.
