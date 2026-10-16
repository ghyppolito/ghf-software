# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** Branch `feat/wp-08-layout-unico` (integração D13, PR rascunho #37 contra `develop`, **não mesclar**), HEAD be54dc8, árvore limpa, em dia com a origem.
CI completo verde em a2ae150 (plano, site, lighthouse); o de be54dc8 (só docs e `tools/gen_estado.py`) estava `in_progress` ao fechar (run 38981384613) — confira com `gh run list --branch feat/wp-08-layout-unico --limit 2`.

## 1. Onde parei

- WP-23 (convite sem terceiros) escrito pelo `/novo-wp`; o usuário aprovou a opção A em 2026-10-16 (pako e Inter locais ao lado do convite, `<main>`, `contrato.sha256` novo, teste com `?d=` real v1/v2). Risco alto, visual. **Só depois do deploy único (D13)**, branch de `develop`, `/release` próprio; último da trilha C. `INVITE-PAKO-CDNJS-01` e `CONVITE-SEM-MAIN-01` estão roteados a ele; fila de triagem vazia.
- WP-12, WP-14, WP-15 e WP-22 `done` e integrados na `feat/wp-08-layout-unico`. Nada publicado (D13).
- Nenhum WP desbloqueado sem o usuário: WP-16 (`PREVALENCIA-PT-NOS-APPS-01`), WP-10, WP-20, WP-13; WP-23 espera o deploy.

## 2. Quebrado ou pela metade agora

Nada quebrado: `npm run build` (21 páginas) e `check_site.py` ("site consistente") passam. Avisos de proveniência legal, preexistentes:
- topowalk e eclipsego: `origemCommit` (7fc7870, 4668019) só existe na máquina local, em nenhum remoto do app (o aviso do build de hoje cita o eclipsego).
- topowalk, poleposition e eclipsego: o texto da ref padrão do app (topo-walk@master 98f7c71, pole-position-app@master a22f957, eclipse-go@main 439454c) difere do `origemCommit` publicado.
  Pole Position: `sync_legal --check` diz "à frente/divergente"; copiar desfaria texto publicado.
  Causa: branches dos apps ainda não levadas à main de cada um. Resolve-se nos apps, não aqui.

## 3. O que só o navegador prova (pendente)

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

**Do usuário:** checklist do WP-19; D11, D12, D3; levar as branches dos apps (topo-walk, eclipse-go; Pole Position com `/legal poleposition` depois) para a main;
nos apps (D19), registrar o en do LottoExpert no `ASO_METADATA.md` e criar a ficha do EclipseGo; `PP-NAV-CONTRASTE-01` aguarda decisão.

**Copy pendente antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável (o export traz "Texto provisório");
confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; selo "Vantagem Competitiva" (`LOTTO-COPY-VANTAGEM-01`); qual descrição do LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões não registradas

A opção A do convite (WP-23) está escrita no próprio WP, com o veredito do `site-arquiteto`; não precisa de entrada nova em `decisoes.md`. Ela altera o congelamento do convite
pela D13, mas só depois do deploy único, e a D13 não cita o WP-23 (nenhuma menção hoje). Sugestão, a critério do usuário: uma linha na D13 apontando para o WP-23 como
a exceção posterior ao congelamento, para quem ler só a D13. Não editei `decisoes.md`. As demais escolhas desta e da sessão anterior (ordem na trilha C, rótulos, rodapé 44 px etc.)
são de escopo de WP e já estão nos WPs e nos achados. Cota de CI dos repositórios privados: o usuário trata em versões próprias.

## 6. Esperando publicação

- `origin/master..origin/develop`: 8 commits (inclui merges de PR); 9 arquivos, **só `.claude/` e `tools/gen_estado.py`** — **sem texto legal, `src/`, `public/` nem `docs/`**; nenhuma urgência.
  (O hotfix legal do Pole Position, PR #44, já está em `master`/`develop`.)
- `origin/develop..origin/feat/wp-08-layout-unico`: 161 commits, 298 arquivos (+15.496/-8.628) — a modernização inteira espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master` entra no passo 6, D22). Rollback por tag.

## 7. Escrituração e branches

- Triagem: vazia (nenhum achado em `triagem`).
- Branches restantes: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-19-rodada-3-claude-design` (integrada, mas o WP-19 segue `blocked`; o usuário não confirmou apagar)
  e `feat/wp-05-ci-no-pr` (não integrada). `origin/HEAD` aponta para `master`.
