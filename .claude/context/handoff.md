# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-30.** Branch `feat/wp-08-layout-unico` (integração D13, PR rascunho #37 contra `develop`, **não mesclar**), HEAD 9059243 antes deste commit de handoff, árvore limpa.
CI do PR #37 verde nos dois últimos runs (41055905066, 41055169787). Localmente `lychee` não está instalado e não rodou (o CI cobre).

## 1. Onde parei

- Política do TopoWalk 4.4.0 (em teste interno) espelhada. Texto novo: data "outubro de 2026"; §8.2 item 3 e §8.3 dizem que arquivos de exportação com mais de 24 h são apagados pelo app na exportação seguinte (TD-18).
- No app, o 7fc7870 nunca tinha chegado à master; foi levado por cherry-pick (PR topo-walk #49) e o usuário fez develop→master: topo-walk@master = 7d69108 (no remoto).
- Hotfix D13 (6): PR #45 `hotfix/legal-topowalk-outubro` → master, mesclado em 2026-10-30 12:28; deploy 41055592320 success; no ar conferido por curl (pt e en, data e as duas frases de 24 h).
- Integração: 8ce7368 (`sync_legal topowalk --ref 7d69108 --forca`, porque o 7fc7870 não é ancestral pelo cherry-pick; en traduzido com o mesmo texto do hotfix; pendente removido). O usuário fez `git merge origin/master`; conflito modify/delete em `topowalk-privacy.html` resolvido mantendo a remoção; merge 9059243 enviado.
- Backlog parado: WP-16 (`PREVALENCIA-PT-NOS-APPS-01`), WP-10, WP-20, WP-13 esperam o usuário; WP-23 espera o deploy único. Fila de triagem vazia.

## 2. Quebrado ou pela metade agora

Nada quebrado: `npm run build` e `check_site.py --raiz dist` ("site consistente") passam; `sync_legal topowalk --check --ref origin/master` diz "nada a fazer". Avisos de proveniência legal:
- topowalk: o aviso de `origemCommit` só local acabou (7d69108 está no remoto). `sync_legal --todos --check` sem `--ref` ainda diz "à frente/divergente" porque o master **local** do clone topo-walk está parado em 9bde1ff; atualizar esse clone resolve.
- poleposition e eclipsego: branches dos apps ainda não levadas à main; texto da ref padrão difere do `origemCommit` publicado (copiar desfaria texto publicado em Pole Position). O `origemCommit` 4668019 do eclipsego só existe na máquina local.

## 3. O que só o navegador prova (pendente)

- **TopoWalk (novo):** `/topowalk-privacy.html` no ar (pt e `/en/`): data, §8.2 item 3, §8.3. Repetir em `dist/` da integração (`python3 -m http.server 8080 -d dist`: `/topowalk-privacy.html` e `/en/topowalk-privacy.html`).
- **WP-19 (rodada 3):** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`,
  `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`;
  Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o resultado no WP-19 (segue `blocked` por isso).
- **WP-16:** seletor com 3+ línguas (lista, não link).
- **Deploy único (D13), WP-11 e WP-21:** Search Console com `sitemap.xml` enviado e lido; preview no WhatsApp de um convite real e de uma landing, com o site no ar;
  card do WhatsApp/LinkedIn com título em travessão e descrição curta em `/`, `/en/`, `/lottoexpert.html` e `/en/topowalk.html`.
- **404 em `/x/y`:** só se prova no Pages (o servidor local não reproduz o fallback de subcaminho).
- **WP-23, depois do deploy:** convite aberto com link real (`?d=` v1 e v2) sem requisição a cdnjs nem a fonte de terceiros, e preview no WhatsApp.
- `CONVITE-TEMA-ESCURO-01` (nota): URL contratual; o usuário não pediu WP.

## 4. Próxima ação

**Do agente:** `/wp` sem número propõe o próximo; os restantes esperam o usuário.
- WP-16: depende de `PREVALENCIA-PT-NOS-APPS-01` (decisão do usuário).
- WP-10: checklist do WP-19, D11 (`--success`), D12 (limiares de destaque) e a copy abaixo.
- WP-20: sessão do usuário no Claude Design.
- WP-13: D3 (medição).
- WP-23: depois do `/release` do deploy único (pré-voo: `git merge-base --is-ancestor origin/feat/wp-08-layout-unico origin/master` sai 0).

**Do usuário:** checklist do WP-19 e o do TopoWalk acima; D11, D12, D3; atualizar o master local do clone topo-walk (9bde1ff → origin/master);
levar as branches dos apps (eclipse-go; Pole Position com `/legal poleposition` depois) para a main;
nos apps (D19), registrar o en do LottoExpert no `ASO_METADATA.md` e criar a ficha do EclipseGo; `PP-NAV-CONTRASTE-01` aguarda decisão.

**Copy pendente antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável (o export traz "Texto provisório");
confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; selo "Vantagem Competitiva" (`LOTTO-COPY-VANTAGEM-01`); qual descrição do LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões não registradas

Nenhuma nova. O pedido de que mudança legal de app em teste interno vá por hotfix e também componha a integração é a aplicação literal da D13 (6). O `--forca` no `sync_legal` foi autorizado
implicitamente pelo pedido de fix e se justifica porque o texto do 7fc7870 está contido no 7d69108. `decisoes.md` não foi editado.

## 6. Esperando publicação

- `origin/master..origin/develop`: 8 commits, **só `.claude/` e `tools/gen_estado.py`**, sem texto legal, `src/`, `public/` nem `docs/`; nenhuma urgência.
- `origin/develop..origin/feat/wp-08-layout-unico`: a modernização inteira (incluindo o espelho do TopoWalk de 8ce7368) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master` entra no passo 6, D22). Rollback por tag.

## 7. Escrituração e branches

- Triagem: vazia (nenhum achado em `triagem`; nesta sessão não houve achado novo).
- Branches restantes: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-19-rodada-3-claude-design` (integrada, mas o WP-19 segue `blocked`; o usuário não confirmou apagar)
  e `feat/wp-05-ci-no-pr` (não integrada). `origin/HEAD` aponta para `master`.
