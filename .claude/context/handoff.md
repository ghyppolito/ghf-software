# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** Branch `feat/wp-08-layout-unico` (integração D13, PR rascunho #37 contra `develop`, **não mesclar**), HEAD 816cb2f, árvore limpa, em dia com a origem.
CI completo verde em 1f1e96f (plano, site, lighthouse); o de 816cb2f (só docs) estava `in_progress` ao fechar a sessão (run 38976819842) — confira com `gh run list --branch feat/wp-08-layout-unico --limit 2`.

## 1. Onde parei

- WP-22 `done` (a11y e i18n sem redesign, com a regressão do WP-15 nos seletores das legais do LottoExpert corrigida e guardada em `check_site` §17 (e)); com WP-12, WP-14 e WP-15, está integrado na `feat/wp-08-layout-unico`. Nada publicado (D13).
- Nenhum WP desbloqueado sem o usuário: WP-16 (`PREVALENCIA-PT-NOS-APPS-01`), WP-10 (checklist do WP-19, D11, D12, copy), WP-20 (Claude Design), WP-13 (D3).

## 2. Quebrado ou pela metade agora

Nada quebrado: `npm run build` e `check_site.py` ("site consistente", 22 páginas, 553 links) passam. Avisos de proveniência legal, preexistentes:
- topowalk e eclipsego: `origemCommit` (7fc7870, 4668019) só existe na máquina local, em nenhum remoto do app.
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
- `CONVITE-TEMA-ESCURO-01` (nota): URL contratual; o usuário não pediu WP.

## 4. Próxima ação

**Do agente:** `/wp` sem número propõe o próximo; os restantes esperam o usuário.
- WP-16: depende de `PREVALENCIA-PT-NOS-APPS-01` (decisão do usuário).
- WP-10: checklist do WP-19, D11 (`--success`), D12 (limiares de destaque) e a copy abaixo.
- WP-20: sessão do usuário no Claude Design.
- WP-13: D3 (medição).

**Do usuário:** checklist do WP-19; D11, D12, D3; levar as branches dos apps (topo-walk, eclipse-go; Pole Position com `/legal poleposition` depois) para a main;
nos apps (D19), registrar o en do LottoExpert no `ASO_METADATA.md` e criar a ficha do EclipseGo; `PP-NAV-CONTRASTE-01` aguarda decisão.

**Copy pendente antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável (o export traz "Texto provisório");
confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; selo "Vantagem Competitiva" (`LOTTO-COPY-VANTAGEM-01`); qual descrição do LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões não registradas

Nenhuma que pertença a `decisoes.md`. As escolhas do usuário nesta sessão (posição do WP-22 na trilha C antes do WP-10, `primary-claro` na pílula do PP, rótulos
"Incluído/Não incluído", os 4 itens de UX sem referência no handoff, incluir a regressão no WP-22, rodapé 44 px e anel da tabela aceitos) são de escopo e UX de um WP, já
escritas no WP-22 e nos achados; não definem produto nem processo. Cota de CI dos repositórios privados: o usuário trata em versões próprias.

## 6. Esperando publicação

- `origin/master..origin/develop`: 4 commits; só `.claude/` e `tools/gen_estado.py`; **sem texto legal, `src/`, `public/` nem `docs/`** — nenhuma urgência.
- `origin/develop..origin/feat/wp-08-layout-unico`: 159 commits — a modernização inteira espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master` entra no passo 6, D22). Rollback por tag.

## 7. Escrituração e branches

- Triagem: só `INVITE-PAKO-CDNJS-01`, de propósito: o convite está congelado por D13 até o deploy único e não há WP aberto para rotear. O `check_plano.py` o conta
  como "1 achado aguardando triagem" (aviso; só falha com mais de 10). Destino previsto: `/novo-wp` depois do deploy único (pako e Inter locais, `contrato.sha256` novo, teste com `?d=` real).
- Branches restantes: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-19-rodada-3-claude-design` (integrada, mas o WP-19 segue `blocked`; o usuário não confirmou apagar)
  e `feat/wp-05-ci-no-pr` (não integrada). As demais e a `main` órfã foram apagadas (`BRANCH-MAIN-ORFA-01` resolvido, origin/HEAD em master).
