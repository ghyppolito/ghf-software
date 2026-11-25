---
id: WP-09
titulo: O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência
area: legal
status: done
depende_de: [WP-08]
adr: [ADR-004]
spec: ""
decisoes: [D7, D14, D15]
tamanho: M
risco: alto
visual: false
branch: feat/wp-09-sync-legal
---

# WP-09 — O texto legal entra no site por um comando que copia do repositório do app e o CI acusa divergência

**Depende de:** WP-08 (legal em `.md` no site) · **Achados roteados:** `WP09-NOME-ARQUIVO-01`, `HOTFIX-LEGAL-POS-MIGRACAO-01`, `LOTTO-EN-ESPELHO-AUSENTE-01`

**Objetivo:** `tools/sync_legal.py <app>` copia `PRIVACY_POLICY.md`/`TERMS_OF_SERVICE.md` do
repositório do app para `src/content/legal/<app>.pt.md`, extrai a data para o front-matter e
deixa um marcador `en: pendente` quando o en está atrás; `check_site.py` falha se o pt do
site difere da origem (quando a origem está acessível) ou se o en está marcado pendente.

**Contexto:** D7; o `/legal` hoje é manual (WP-01 é o primeiro uso). Com 4 apps e releases
mensais, o ritual se repete; o erro recorrente é esquecer a data no en.

**Ler antes:** `.claude/commands/legal.md`; `.claude/agents/site-legal.md`; WP-08 (formato
do `.md` e do front-matter).

**Arquivos-alvo:** `tools/sync_legal.py`; `tools/check_site.py` (§4 passa a ler front-matter);
`.claude/commands/legal.md` (passa a chamar o script); `CLAUDE.md` "Comandos".

**Critérios de aceite:**
- `python3 tools/sync_legal.py lottoexpert` com origem igual: "nada a fazer"; com origem
  diferente: `.md` pt atualizado, `lastUpdated` certo, `en: pendente` no front-matter.
- `python3 tools/check_site.py` falha com `en: pendente` e passa depois da tradução.
- Script só biblioteca padrão; roda sem o repositório do app presente (aviso, não erro).

**Risco:** médio — automatizar cópia de texto legal. O script **nunca** toca o en nem altera
texto; só copia pt e marca.

---

## Veredito do arquiteto (site-arquiteto, 2026-10-15)

**Aprovado, com o desenho abaixo.** Os critérios originais ficam substituídos pelos desta seção.
Não toca URL contratual, deploy nem `pr.yml`. Mexe no front-matter dos 5 `.pt.md` (não no corpo).
Por isso o `risco` sobe para **alto**: `site-docs` troca o campo e regenera o `ESTADO.md` no mesmo
commit. Isso não foi feito aqui para não deixar `gen_estado.py --check` vermelho. O caminho
`src/content/legal/<app>.pt.md` do objetivo lê-se `<app>-<doc>.pt.md` (`WP09-NOME-ARQUIVO-01`).

### Fato medido que fixa o desenho (2026-10-15)

Corpo do `.pt.md` do site comparado com a origem, conferido com `cmp`:

| doc | site = | checkout do app | branch principal do app |
|---|---|---|---|
| lottoexpert-privacy/terms | `lotto-expert` master `363cb9f` | `develop`, igual | `master` igual |
| topowalk-privacy | `7fc7870` (`docs/politica-tres-observacoes`, **sem remoto**) | igual | `master` **difere** |
| eclipsego-privacy | `4668019` (`docs/email-suporte-politica`, **sem remoto**) | igual | `main` **difere** |
| poleposition-privacy | `00968f5` (PP-144) | `chore/release-2.2.0`, **difere** (§2 "Quatro marcos", §2 sem "quantidade total de circuitos") | `master` **difere** |

O working tree não serve de origem: hoje ele sobrescreveria o Pole Position com o texto de uma
release em andamento. A branch principal também não serve sozinha: ela desfaria três correções que
o site já publica. O que é estável é o **commit** de onde o texto foi copiado.

### Precisa de ADR: sim, ADR-004

Título: *"O espelho legal registra o commit do app de onde foi copiado"*. É o primeiro commit
do WP, e o `adr: [ADR-004]` entra no front-matter no mesmo commit, porque o `check_plano` exige que
o ADR exista. A ADR complementa a D7, sem repeti-la. Ela decide três coisas:
- a origem é sempre `git show <ref>:<caminho>`, nunca o disco;
- o `.pt.md` guarda o commit;
- a comparação de texto é local e determinística, contra esse commit. O CI cobra formato,
  proveniência e `en` pendente.

### `tools/sync_legal.py`: só biblioteca padrão, nunca abre `.en.md`

**Tabela única `ORIGENS`** (no script):

```
.pt.md → (repo, caminho, ref_padrão)
lottoexpert-privacy → (lotto-expert, docs/PRIVACY_POLICY.md, master)
lottoexpert-terms   → (lotto-expert, docs/TERMS_OF_SERVICE.md, master)
topowalk-privacy    → (topo-walk, PRIVACY_POLICY.md, master)
poleposition-privacy→ (pole-position/pole-position-app, PRIVACY_POLICY.md, master)
eclipsego-privacy   → (eclipse-go, docs/PRIVACY_POLICY.md, main)
```

O `check_site.py` importa `ORIGENS` (o `tools/` já está no `sys.path`) e falha se
`set(ORIGENS) != set(LEGAL.values())`. A tabela do `/legal` cita `ORIGENS` e não a duplica como
verdade. A `ref_padrão` depende da decisão **D14**, abaixo.

**CLI:**

```
python3 tools/sync_legal.py <app>|--todos [--doc privacy|terms] [--ref REF] [--apps-dir DIR] [--check] [--forca]
```

- `--apps-dir`: padrão `$GHF_APPS_DIR` ou `..` da raiz do repositório.
- `--ref`: aceita branch, tag ou sha. Sem ele, vale a `ref_padrão`.
- `--check`: não escreve. Para cada doc, diz um destes:
  - igual;
  - atrás (a ref tem texto novo);
  - **à frente/divergente** (o commit registrado não é ancestral da ref);
  - origem ausente.

  Sai com 1 se houver o que fazer. Substitui o `diff` manual do `/legal`.

**De onde lê:** só `git -C <repo> show <sha>:<caminho>`, com `sha = git rev-parse <ref>^{commit}`.
O texto que não está commitado no app não é origem (D7: nasce no repositório do app).

**O que escreve:** só o `.pt.md`, nesta forma exata:

```
---
lastUpdated: "AAAA-MM[-DD]"
origemCommit: "<sha de 40>"
en: "pendente"
---
<bytes da origem, sem nenhuma transformação: CRLF, BOM e newline final preservados>
```

Escrita em modo binário, por arquivo temporário e `os.replace`.

**Regras de escrita:**

| Caso | O que o script faz |
|---|---|
| Corpo igual | Escreve "nada a fazer (…@sha)" e sai com 0. Só escreve se faltar `origemCommit` (bootstrap), e então só no front-matter |
| Corpo diferente | Copia o corpo. `lastUpdated` sai da linha `**Última atualização:**` da origem: "12 de Outubro de 2026" → `2026-10-12`; "setembro de 2026" → `2026-09`. Grava `origemCommit` e `en: "pendente"` |
| Data da origem igual à do site, com o corpo mudado | Copia mesmo assim e avisa: "texto mudou sem data nova — achado para o repositório do app" |

**Recusa, sai com ≠0 e não escreve nada quando:**
- a origem não tem a linha de data, ou o mês é desconhecido;
- a ref não existe;
- o `.pt.md` tem modificação não commitada;
- o front-matter tem uma chave fora de `{lastUpdated, origemCommit, en}`;
- o `origemCommit` registrado não é ancestral da ref, porque a cópia desfaria texto publicado.
  `--forca` libera só este último caso.

**Origem ausente** (o diretório do app não existe): aviso, sai com 0, não escreve nada.

**Aviso de hotfix:** quando `origin/master` do site tem um commit fora de `HEAD` que toca
`src/content/legal/`, `docs/*POLICY*`, `docs/*TERMS*`, `*-privacy.html` ou `*-terms.html`, o script
avisa: "hotfix legal em master não integrado — `git merge origin/master` antes do sync".

Mais dois avisos:
- `origemCommit` que não está em nenhum remoto do app: "texto publicado de commit que só existe
  na sua máquina". É o caso hoje do TopoWalk e do EclipseGo.
- O script imprime a ref, o sha e as seções `##` alteradas, para o `site-legal` partir do diff.

**Schema de `src/content.config.ts`:**

```ts
z.object({
  lastUpdated: …regex atual…,
  origemCommit: z.string().regex(/^[0-9a-f]{40}$/).optional(),
  en: z.literal('pendente').optional(),
}).strict()
```

- `.strict()` faz o build falhar em chave errada.
- O build **não** falha com `en: "pendente"`, para que o pt continue visível no `dist/` local.
- Quem bloqueia é o `check_site`.
- `optional` porque o schema vale para pt e en. "Obrigatório no pt, proibido no en" é regra do
  `check_site`.

### `check_site.py` §4 (e a docstring)

**Sempre, inclusive no CI:**
- o `.pt.md` tem `origemCommit` de 40 hex;
- `en: "pendente"` no `.pt.md` é **erro**: "en atrás do pt — traduzir e tirar o marcador";
- `origemCommit` ou `en` num `.en.md` é erro;
- `set(ORIGENS) == set(LEGAL.values())`;
- o resto do §4 e do §12 fica como está. A data do en diferente da do pt já falha hoje.

**Com o repositório do app presente** (`<apps-dir>/<repo>/.git`):
- `git show <origemCommit>:<caminho>` tem de ser **igual byte a byte** ao corpo do `.pt.md`.
  Senão, erro: "pt ≠ <repo>@<sha7> — texto editado à mão? rode sync_legal".
- Commit inexistente no repositório local: erro ("`git fetch` no app ou origemCommit inventado").
- Commit fora de qualquer remoto: aviso.
- Ref padrão com texto diferente: **aviso**, não erro ("app avançou: `sync_legal.py <app> --check`").
  O site não fica vermelho por commit alheio, e a decisão de espelhar é do humano (D7).

**Sem o repositório:** um aviso por repositório ("origem ausente — comparação de texto pulada"),
sem erro. O CI fica nesse caso; ver **D15**.

### `/legal` e `site-legal`

**`/legal`:**
- **Passo 2:** `python3 tools/sync_legal.py <app> --check`. Se der "igual", para. Se der
  "à frente/divergente", para e pergunta ao usuário qual ref usar.
- **Passo 3:** `python3 tools/sync_legal.py <app> [--ref …]` e, em seguida, `site-legal` só
  para o en.
- **Passo 4:** `/verify`, com o `check_site` local, que agora compara contra o commit.
- **Seção nova, "Hotfix durante a integração":** ver abaixo.

**`site-legal`:**
- o passo 2 (pt à mão) **deixa de existir**: o agente nunca escreve o corpo do `.pt.md`;
- o passo 3 traduz o en a partir do diff que o script imprimiu e atualiza `lastUpdated` e
  `**Last updated:**` do en;
- por fim, o agente apaga só a linha `en: "pendente"` do `.pt.md`;
- critério de saída: `sync_legal.py <app> --check` "igual" e `check_site` verde;
- entra em "O que você nunca faz": editar o corpo do `.pt.md` ou o `origemCommit` à mão.

### `HOTFIX-LEGAL-POS-MIGRACAO-01`

Hoje não há pendência: `origin/master` (6655b71, #43) está integrada em conteúdo, e
`git diff HEAD...origin/master` sai vazio. Até o deploy único, `master` ainda tem o layout antigo
(`docs/*.md` e HTML na raiz).

O ritual entra no `/legal`:
1. O hotfix é feito em `master` como hoje: branch de `master`, PR e deploy (D13 (6)).
2. Na integração: `git merge origin/master`.
3. O conflito modificar/apagar se resolve **mantendo a remoção** (`git rm` dos caminhos antigos).
4. Rodar `sync_legal.py <app> --ref <sha do app usado no hotfix>`.
5. O en é traduzido pelo `site-legal`, com o en do HTML do hotfix como base.
6. `check_site` verde.

O aviso de hotfix do `sync_legal.py` lembra o passo 2. Depois do deploy único, `master` passa a ter
o layout novo, e o hotfix vira um `sync_legal.py` numa branch de `master`, sem conflito. **Destino:
`resolvido` no WP-09**, quando o `/legal` tiver essa seção.

`LOTTO-EN-ESPELHO-AUSENTE-01`: o en do LottoExpert existe (`lottoexpert-privacy.en.md`, `-terms.en.md`,
desde o WP-08). O export do Claude Design não é origem (D7). **Destino: `resolvido` no WP-09**, com
uma nota no WP-10: a página legal do redesign consome `src/content/legal/`, não o stub do export.

`WP09-NOME-ARQUIVO-01`: **`resolvido`** por esta seção.

### Arquivos-alvo (substitui a lista)

- `.claude/context/decisions/ADR-004-*.md`
- `tools/sync_legal.py`
- `tools/check_site.py` (§4 e docstring)
- `src/content.config.ts`
- `src/content/legal/*.pt.md`: só o front-matter (`origemCommit` do bootstrap)
- `.claude/commands/legal.md`
- `.claude/agents/site-legal.md`
- `.claude/context/invariantes.md` (guarda da linha "Texto legal é espelho")
- `CLAUDE.md` "Comandos" (o `sync_legal --check` substitui os 5 `diff`)
- `achados-novos.md` (três fechamentos)

Fora: `.github/workflows/*`, porque o CI já roda o `check_site` e um repositório de app no CI é a D15.
Também ficam fora os `.en.md` e o corpo dos `.pt.md`.

### Critérios de aceite (substituem os originais)

1. Bootstrap: `sync_legal.py <app> --ref <sha>` com os shas da tabela acima grava só
   `origemCommit` nos 5 `.pt.md`.
   - `git diff` mostra só linhas de front-matter.
   - `diff <(sed '1,/^---$/d' X.pt.md) <(git -C ../app show sha:caminho)` vazio nos 5.
2. Com corpo igual, sai "nada a fazer" e o `sha256sum` do arquivo não muda.
3. Com a origem diferente: o corpo fica igual byte a byte a `git show`, `lastUpdated` vem da linha
   da origem, `en: "pendente"` está presente e o `sha256sum` dos `.en.md` não muda.
   - Prova num worktree temporário com um repositório de app falso (`git init` + 2 commits), sem
     tocar nos apps reais.
4. `npm run build` passa com `en: "pendente"`. `check_site` falha com ele e passa depois da
   tradução e da remoção da linha.
5. Sem `../<app>`: o sync avisa e sai com 0, e o `check_site` avisa e não erra pelo texto. Com
   `--apps-dir /inexistente`, o mesmo resultado.
6. `sync_legal.py poleposition --check` (ref master) diz "à frente/divergente", e sem `--forca` não
   escreve nada.
7. `pr.yml` verde sem mudança no workflow.
8. Os scripts só importam da biblioteca padrão:
   `grep -E '^(import|from)' tools/sync_legal.py` lista só módulos dela.

### Mutações que têm de falhar

Cada uma é revertida depois de provada.

| # | Mutação | Quem pega |
|---|---|---|
| 1 | 1 byte no corpo de `topowalk-privacy.pt.md`, com o repositório presente | `check_site` (pt ≠ commit) |
| 2 | `en: "pendente"` no `.pt.md` | `check_site`, inclusive sem os apps |
| 3 | `en: "pendente"` ou `origemCommit` num `.en.md` | `check_site` |
| 4 | `origemCommit` ausente, de 39 hex ou em maiúsculas | `check_site`, e o build no formato |
| 5 | `origemCommit` de 40 hex que não existe no app | `check_site`, erro local |
| 6 | `en: "pronto"` ou uma chave `En:` | build (`literal` e `.strict()`) |
| 7 | Doc novo em `LEGAL` sem entrada em `ORIGENS` | `check_site` |
| 8 | Origem falsa sem a linha `**Última atualização:**` | sync sai com ≠0 e não escreve nada |
| 9 | `--ref nao-existe` | sync sai com ≠0 e não escreve nada |
| 10 | `.pt.md` com modificação não commitada | sync recusa |
| 11 | `origemCommit` que não é ancestral da ref | sync recusa sem `--forca` |
| 12 | Origem falsa com CRLF e sem newline final | o sync copia igual. O teste prova que essa mutação não é perdida |
| 13 | `lastUpdated` do pt alterado sem mudar o corpo | `check_site` §4 (já existe; não pode regredir) |
| 14 | Front-matter em CRLF + corpo mudado / + `en: "pendente"` / sem `origemCommit` (no `.pt.md` e no `.en.md`) | `check_site` (front-matter fora do formato em LF), inclusive sem os apps |

### Ordem dos commits

1. `WP-09: ADR-004 — espelho legal registra o commit do app`, com `adr: [ADR-004]` e `risco: alto`
   no WP e o `ESTADO.md` regenerado.
2. `WP-09: tools/sync_legal.py` (ORIGENS, `--check`, cópia e recusas). Não escreve no site ainda.
3. `WP-09: schema legal com origemCommit e en pendente` (`content.config.ts`).
4. `WP-09: bootstrap do origemCommit nos 5 .pt.md`, gerado pelo script. O diff mostra só o
   front-matter.
5. `WP-09: check_site §4 compara pt com o commit do app`, junto com o import de `ORIGENS`.
6. `WP-09: /legal e site-legal chamam o sync; ritual de hotfix`, com `CLAUDE.md` e `invariantes.md`.
7. `WP-09: achados roteados fechados`, depois da auditoria.

As mutações rodam entre o 5 e o 6, e a saída fica no "Estado" do WP.

### Decisões do usuário

Registrar com `/decisao` antes do commit 2. O WP não segue sem a D14.

**D14: qual ref é "a publicada" de cada app (a `ref_padrão` do sync).**
- **(A) A branch principal do app** (`master`; `main` no EclipseGo), com `--ref` para a exceção.
  **Recomendada.** É o que o app em produção mostra. O commit registrado e a recusa por
  ancestralidade impedem que um sync desfaça a correção que veio de branch. Consequência hoje:
  TopoWalk, EclipseGo e Pole Position ficam "à frente" até as branches entrarem na principal do
  app. É o sinal certo, e já está em `PP-POLITICA-BRANCH-APP-01`.
- (B) O `HEAD` do checkout do app. É cômodo, mas o resultado depende de onde a outra sessão parou:
  hoje copiaria a release 2.2.0 do Pole Position.
- (C) Sem padrão, com `--ref` obrigatório. É seguro, mas o `--check` em lote fica sem referência.

**D15: o CI do site compara o texto com o app?**
- **(A) Não.** O CI cobra formato, proveniência e `en` pendente, e a comparação byte a byte é
  local (`/verify` e `/legal`). **Recomendada.** Não exige segredo nem acesso aos repositórios
  privados.
- (B) Sim. O `pr.yml` faz checkout dos 4 apps no `origemCommit`, com uma deploy key ou um token
  por repositório. Prova a cópia em todo PR, mas põe credencial no CI e exige um WP próprio, com
  plano de reversão (item 4 do guarda: mudança de CI).

---

## Estado (fim da implementação, 2026-10-15)

**Fechamento (2026-10-15):** o usuário integrou (`git merge --no-ff feat/wp-09-sync-legal` na `feat/wp-08-layout-unico`); push e CI do #37 verde (run 38799499185: `plano` pass, `site` pass, sem mudança no `pr.yml`) — critério 7 provado. Status `done`. Integrado, não publicado: vai ao ar no deploy único (D13).

**Status: `doing`, de propósito.** Falta só o critério 7 (`pr.yml` verde sem mudança no workflow), que
só o CI prova. Depois do merge do usuário na integração (`feat/wp-08-layout-unico`) e do CI do #37
verde, o agente marca `done` e escreve "Publicado" só quando `master` tiver o commit (D13: deploy único).

**Decisões:** D14 = A (ref padrão é a branch principal do app) e D15 = A (o CI não compara com o app),
ambas em 2026-10-15 ("pode seguir o recomendado"). ADR-004.

**Commits:** f14b1f4 início · d44e042 veredito · bd4bc76 ADR-004 e D14/D15 · 8b17b09 `sync_legal.py` ·
49b497c schema · 5c0b13c bootstrap do `origemCommit` (TopoWalk 7fc7870, EclipseGo 4668019, Pole Position
00968f5, LottoExpert ffce885, que é a master atual do app; o veredito citava 363cb9f, de corpo idêntico
e ancestral) · 7e3e5fc `check_site` §4 · 6ee0b6d `/legal` e `site-legal` · 6e1ca1c achados · 41c77cf
`/verify` usa o §4 em vez do `diff` com o disco do app · c4d4c28 correções da auditoria.

**Provas:**
- `git diff` de `src/content/legal/` contra a integração: só as 5 linhas `+origemCommit` nos `.pt.md`;
  `.en.md` e texto legal intactos. `dist/` idêntico ao da integração (`diff -r`, site-qa).
- `/verify` verde no HEAD: build, `check_site.py` (22 páginas, 5 avisos esperados), contrato,
  html-validate e plano.
- 14 mutações da tabela, mais as das correções, falham como deviam; cada uma foi revertida.
- Critérios 1 a 6 e 8 provados. O 7 espera o CI.

**Avisos esperados (5):** o `origemCommit` de TopoWalk e EclipseGo não está em nenhum remoto; a ref
padrão difere em TopoWalk, Pole Position e EclipseGo (D14). Somem quando o usuário levar as branches dos
apps para a principal de cada um.

**Auditoria:** `site-qa` achou 1 alto (front-matter em CRLF desligava a proveniência, inclusive no CI),
1 médio (aviso "origem ausente" não contava como verificação não rodada) e 3 baixos (`--forca` liberava
demais, `--todos` não era atômico, mensagem "app avançou"); todos corrigidos em c4d4c28 e provados por
mutação. `site-seo-perf` não foi invocado (o HTML não muda); `site-ux` não se aplica (`visual: false`).

**Incidente:** um `sync_legal --todos --ref HEAD` que sobrou num comando escreveu
`poleposition-privacy.pt.md` no repositório principal. Foi restaurado antes de qualquer commit, sem dano.

**Nota para o WP-10:** a página legal do redesign consome `src/content/legal/`, não o stub do export
(`LOTTO-EN-ESPELHO-AUSENTE-01`).
