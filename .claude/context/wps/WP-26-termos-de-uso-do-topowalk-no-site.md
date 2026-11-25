---
id: WP-26
titulo: Os termos de uso do TopoWalk existem no site em pt e en, espelhados do repositório do app
area: legal
status: doing
depende_de: []
adr: [ADR-001, ADR-004, ADR-005, ADR-007]
spec: ""
decisoes: [D7, D13, D23, D28]
tamanho: M
risco: alto
visual: true
branch: feat/wp-26-termos-topowalk
---

# WP-26 — Os termos de uso do TopoWalk existem no site em pt e en, espelhados do repositório do app

**Depende de:** pré-condição fora do site: `../topo-walk/TERMS_OF_SERVICE.md` (ou `docs/`) commitado
na branch principal do app (`master`, D14). Pelo caminho (B) abaixo, depende também da fatia 3 do
WP-10 (`LegalLayout`) estar na integração; não está em `depende_de` porque o WP-10 inteiro só fecha
na fatia 10. · **Achados roteados:** —

**Pedido do usuário (2026-11-22, `/novo-wp`):** "isso está sendo exigido pela EEUU". **Esclarecido no
mesmo dia:** a exigência é da **União Europeia** — ao se declarar comerciante (*trader*) nas lojas,
os termos de uso passam a ser obrigatórios na UE. Prazo verificado pelo usuário: **até 2027**. Publicação
pela D28 (B): junto com o deploy único da modernização (D13), que o usuário quer subir **antes do fim
de 2026**.

**Objetivo:** `/topowalk-terms.html` (pt) e `/en/topowalk-terms.html` publicam, byte a byte no pt, o
`TERMS_OF_SERVICE.md` do repositório do TopoWalk, com a mesma data, e o rodapé de toda página leva
o link para eles.

**Contexto:**
- Hoje não há termos de uso do TopoWalk em lugar nenhum. `git -C ../topo-walk ls-files | grep -i term`
  não acha nada (2026-11-22). Só o LottoExpert tem termos no site (`/lottoexpert-terms.html`, origem
  `../lotto-expert/docs/TERMS_OF_SERVICE.md`, `tools/sync_legal.py:49`).
- O TopoWalk usa Play Billing (`../topo-walk/gradle/libs.versions.toml:27`, `billing = "9.1.0"`).
  É o único dos três com venda no app, o que torna o pedido de termos mais plausível nele.
- Nenhum dos três apps cita URL do site no código (`grep -rn "ghfsoftware.com/" app/src` só acha
  `support@`). A URL nova vira contrato pela ficha da Play, como as políticas (ADR-001 § Contexto).
- **Texto legal o agente não redige** (`CLAUDE.md` § Fontes de verdade). Se a origem não existir no
  app, o WP para no passo 1.
- O site hoje espelha 5 documentos: `ORIGENS` em `tools/sync_legal.py:47-53`, `LEGAL` em
  `tools/check_site.py:188-194`. O §19 (`tools/check_site.py:1339-1359`) percorre `LEGAL`, então
  passa a exigir uma URL a mais (6, 7 ou 8, conforme a ordem dos WP-26, WP-27 e WP-28) no rodapé sem mudar a lógica; só o texto "5 URLs" (`:105`, `:1339`,
  `:1352`, `:1358`) fica errado.

**URL contratual (ADR-001).** Não pede ADR novo nem emenda: o ADR-001 § Decisão já diz "Caminho
novo que um app passe a citar entra na lista no mesmo WP que o app o adota". `/topowalk-terms.html`
entra em `CONTRATUAIS` e no `CLAUDE.md` § "URLs que são contrato" **neste WP**, antes de a ficha
apontar para ela. `/en/topowalk-terms.html` só vira contrato se a ficha en citar esse caminho; o
ADR-001 § "O que isto mantém aberto" já cobre a versão en noutro caminho. Nome no padrão
`<app>-terms.html`, igual ao do LottoExpert, e não rota limpa: o par com `lottoexpert-terms.html`
mantém o `rota()` e o §9 sem caso novo.

**Ler antes:** `.claude/commands/legal.md`; `.claude/agents/site-legal.md`; ADR-001; ADR-004; ADR-007
§2–§5; D7, D13 (6), D14, D23 em `decisoes.md`; o `TERMS_OF_SERVICE.md` do TopoWalk inteiro;
`src/components/paginas/PaginaLottoExpertTerms.astro` (o modelo).

**Arquivos-alvo:**
- `tools/sync_legal.py` (só uma entrada `topowalk-terms` em `ORIGENS`)
- `tools/check_site.py` (`CONTRATUAIS`, `PUBLICADAS`, `LEGAL`; o texto "5 URLs" do §19 passa a
  dizer o número de `LEGAL`, sem mudar a regra)
- `src/content/legal/topowalk-terms.pt.md` (gerado pelo `sync_legal.py`) e `topowalk-terms.en.md`
- `src/components/paginas/PaginaTopoWalkTerms.astro`, `src/pages/topowalk-terms.astro`,
  `src/pages/[lang]/topowalk-terms.astro`
- `src/i18n/legal.ts` (só `topowalk_terms_h1/_title/_description`, pt e en)
- `src/i18n/idiomas.json` (só a entrada `topowalk-terms.html: ["pt", "en"]`)
- `src/components/Footer.astro` (só o link `topowalk-terms.html` com `footer_terms` na coluna do TopoWalk)
- `.claude/commands/legal.md` (linha do TopoWalk na tabela)
- `CLAUDE.md` (§ Fontes de verdade e § "URLs que são contrato")

Fora do site, e do usuário: `.claude/settings.json` (permissão de leitura da origem nova, se o
`/legal` pedir) e a ficha da Play.

**Passos:**
1. Pré-condição: o `TERMS_OF_SERVICE.md` existe num commit da `master` do TopoWalk que está em
   `origin`, com linha `**Última atualização:**`. Se não existe, **parar** e devolver ao usuário.
   O agente não redige, não completa e não adapta os termos do LottoExpert.
2. `ORIGENS["topowalk-terms"] = ("topo-walk", "<caminho do .md>", "master")`. `LEGAL`,
   `CONTRATUAIS` e `PUBLICADAS` ganham `topowalk-terms.html`.
3. `python3 tools/sync_legal.py topowalk --doc terms` grava `topowalk-terms.pt.md` com
   `origemCommit` e `pendente: ["en"]`.
4. `site-legal` traduz para `topowalk-terms.en.md`, cláusula por cláusula (D7), e tira `en` de
   `pendente`. Nomes próprios, e-mail, valores e prazos ficam literais.
5. Página: `PaginaTopoWalkTerms.astro` sobre o `LegalLayout` da fatia 3 do WP-10, copiando a
   estrutura de `PaginaLottoExpertTerms.astro`; cascas pt e `[lang]`; chaves em `legal.ts`;
   `idiomas.json`. Sitemap, canonical e `hreflang` saem do mapa (ADR-005, `src/pages/sitemap.xml.ts`)
   e não pedem código.
6. Rodapé: `footer_terms` na coluna do TopoWalk. Links para a página em língua sem versão seguem a D23.
7. `python3 tools/gen_estado.py && python3 tools/check_plano.py`; `/verify`.
8. Usuário: aponta a ficha da Play (e onde mais a exigência pedir) para a URL publicada, **só depois**
   de ela estar no ar. Registra no WP qual campo e qual URL (pt ou `/en/`).

**Critérios de aceite:**
- `python3 tools/sync_legal.py topowalk --doc terms --check` diz "igual".
- `diff <(sed '1,/^---$/d' src/content/legal/topowalk-terms.pt.md) <(git -C ../topo-walk show <origemCommit>:<caminho>)` vazio.
- `python3 tools/check_site.py` e `python3 tools/check_site.py --raiz dist` verdes. Isso inclui a
  data do `.pt.md` igual à da origem e à do `.en.md`, as mesmas seções nas duas línguas,
  `ORIGENS` = `LEGAL`, `/topowalk-terms.html` em `CONTRATUAIS` e o §19 com o link novo em todo `<footer>`.
- `test -f dist/topowalk-terms.html && test -f dist/en/topowalk-terms.html`.
- `grep -o '<link rel="alternate" hreflang="[^"]*"' dist/topowalk-terms.html | wc -l` = 3 (pt-BR, en, x-default → en), igual a `dist/topowalk-privacy.html` hoje; `grep -c '<loc>https://ghfsoftware.com/\(en/\)\?topowalk-terms.html</loc>' dist/sitemap.xml` = 2.
- `.en.md` sem `pendente`.
- `npx html-validate 'dist/**/*.html'` sem erro.

**Só no navegador:** `/topowalk-terms.html` e `/en/topowalk-terms.html` a 360 e 1280: título, data
no topo, sumário, troca de idioma mantendo `#secao-N`, link do rodapé na coluna do TopoWalk em
uma página qualquer, pt e en. Depois do deploy: a URL do ar abre sem login, e a ficha da Play leva
a ela. O usuário reporta.

**Irreversível:** a URL pt entra em `CONTRATUAIS` e não sai mais (ADR-001). Termos publicados são
o que o usuário do app aceitou naquela data. Tradução en errada vale como declaração da GHF em
inglês até ser corrigida, e importa mais aqui se a exigência vem dos Estados Unidos.

**Risco:** alto (texto legal, URL contratual nova). Específico: o §19 reprova as 22 páginas de `dist/` de uma
vez se o link do rodapé faltar numa língua; termos publicados antes da ficha estar pronta não fazem
mal, ficha apontando antes da página existir dá 404 ao revisor da loja.

**Caminho de publicação (D13 (6)) — decisão do usuário, proposta como D28:**
- **(A) Hotfix no `master`, stack antiga, e depois a integração.** Em `master` as páginas são HTML na
  raiz, copiadas por uma lista fechada (`origin/master:astro.config.mjs:10-19`), com o inglês num
  dicionário JS que abre em pt (`origin/master:lottoexpert-terms.html:504`,
  `localStorage.getItem('ghf_lang') || 'pt'`). Custo: a página é feita duas vezes; o rodapé muda nas
  10 páginas da raiz à mão; `CONTRATUAIS`/datas no `check_site.py` de `master`, que é outro;
  **não há `/en/topowalk-terms.html`**, e quem abre a URL vê português primeiro. No merge de volta, o
  HTML da raiz é apagado e a página nasce de novo pelo passo 5. Prazo: um PR pequeno.
- **(B) Entra na integração e sobe no deploy único.** Custo: a página só vai ao ar quando o deploy
  único subir, e ele espera o WP-10 até a fatia 10, D11 e D12. Sem trabalho duplicado, com
  `/en/` desde o primeiro dia. Serve se não houver prazo de loja ou de lei.
- **(C) Hotfix mínimo no `master` só com as URLs finais.** `topowalk-terms.html` e
  `en/topowalk-terms.html` como HTML estático, uma língua por arquivo, sem dicionário JS e sem link
  no rodapé de `master`; entram na lista de cópia de `astro.config.mjs` de `master` e no
  `CONTRATUAIS` dele. Custo: duas páginas fora do sistema até o deploy único, e uma linha a mais na
  lista de cópia do build de `master` (é deploy, risco alto); o rodapé de `master` não leva o link.
  Ganho sobre (A): as URLs pt e en já são as finais, e o revisor dos Estados Unidos abre o inglês.
  No deploy único, o build novo gera as mesmas URLs, e os arquivos estáticos saem.
- Fora: antecipar o deploy único só para isto reabre a D13 (condições (1)–(5)).

**Perguntas ao usuário (respondidas em 2026-11-22):**
1. Origem: União Europeia, status de comerciante nas lojas torna os termos obrigatórios.
2. Prazo: até 2027; sem urgência antes do deploy único.
3. Onde a URL será citada: em aberto — responder antes do passo 8 (ficha da Play / campo do Play Console).
4. Inglês: o `/en/` nasce junto (caminho B); a ficha en cita `/en/...` se o Play pedir.
5. Quem escreve o `TERMS_OF_SERVICE.md` e quando chega à branch principal do app: em aberto — pré-condição do passo 1.
6. Publicação: D28 (B), integração e deploy único.
