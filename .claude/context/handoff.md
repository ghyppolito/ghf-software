# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-14 (fim).** Escrito na branch de integração `feat/wp-08-layout-unico` (PR rascunho #37,
"NÃO FAZER MERGE — PR de CI da integração"), em dia com `origin/develop`.

## 1. Onde parei

- **Site no ar:** WP-07 publicado em 2026-10-14 por GitHub Actions (Pages `build_type: workflow`,
  `PAGES_VIA_ACTIONS=true`, ambiente `github-pages` só `master`). Bolão testado pelo usuário com link real.
- **Esperando publicação** (`origin/master..origin/develop`): só escrituração do WP-07 (44e95af, 09967ab e o merge do
  #40). Nenhum texto legal, nenhuma página. Sem urgência; vai no próximo `/release`.
- **WP-08** `doing`: fatia 1 (Tailwind 3 compilado/ADR-003, layout `Base`, Nav/Footer/TrocaIdioma, home em `/` e `/en/`,
  404 no layout, regras novas do `check_site.py`) integrada, CI do #37 verde, `/`, `/en/` e `/404.html` conferidos pelo
  usuário (b88d5e0). **Fatia 2 (landing LottoExpert) não começou.**
- **WP-19** `blocked`: falta o checklist de navegador da rodada 3 (seção 3).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar. Pela metade:
- **Relógio da R1 do WP-08:** alguns dias sem incidente a partir de 2026-10-14. A tag `pre-wp-08` em `master` **não foi
  criada** (só antes da R1). Publicação em 3 releases via `release/wp-08-rN` (R1 fatias 1–5, R2 legais 6–8, R3 `public/` e
  convite 9; sem redirect para `/en/` até o WP-15).
- **Rollback da troca do Pages:** Source -> "Deploy from a branch" `master` + `gh variable delete PAGES_VIA_ACTIONS`.
  Vale só até a R1 tirar páginas da raiz.
- **Merges são do usuário:** o agente não tem `git merge` (settings). Fatia volta à integração por
  `git merge --no-ff feat/wp-08-fN-<slug>`; a integração recebe `origin/develop` por `git merge origin/develop`. Conflito
  de `ESTADO.md`/`handoff.md`/`achados-novos.md`: manter as linhas dos dois lados e regenerar `ESTADO.md`; o agente
  conclui com `git commit` depois que o usuário inicia o merge.
- `CONFIG-YML-ORFAO-01`: `_config.yml` já não é lido; sai no WP-08.

## 3. O que só o navegador prova (usuário ainda não viu)

- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota, sem WP): código só tema claro; hipótese de escurecimento
  forçado do navegador; o usuário testou e não pediu WP. Convite é URL contratual.
- Home, `/en/` e `/404.html` (fatia 1): já conferidos em 2026-10-14.

## 4. Próxima ação

**Do usuário:**
1. Acompanhar o site no ar; sem incidente, autorizar a R1 do WP-08 (criar `pre-wp-08` antes).
2. Checklist do WP-19; escrever o resultado no WP.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10; D3 (medição) bloqueia o WP-13.
4. Quando quiser, `/release` das escriturações do WP-07 (ou esperar a R1).

**Do agente:** fatia 2 do WP-08 (landing LottoExpert), incluindo `HOME-EN-SEM-LANG-01` (gravar `ghf_lang` ao abrir
página em `/en/`, sem redirect). Respostas do usuário ao plano estão no corpo do WP-08.

**Copy pendente do usuário antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de
publicidade". Decidir também qual descrição do LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões fora de `decisoes.md` e ADR

- **Exceção de dependência do WP-08 e respostas do usuário ao plano:** no corpo do WP-08 (decisões de execução daquele WP).
- **Fatiamento e 3 releases:** plano do arquiteto, no WP-08.
- **Texto pt da home vem do dicionário JS** (o que o visitante via, não o HTML estático): vira o achado
  `INDEX-LOTTO-DESC-DIVERGE-01`, roteado ao WP-10.
- `cssTarget` do `astro.config.mjs`: registrado no ADR-003.
- Decisões abertas em `decisoes.md`: D3, D11, D12. D10 resolvida.

## 6. Escrituração e branches

- Triagem de `achados-novos.md`: nenhuma linha em `triagem`; todos os achados do WP-08 têm destino.
- **Branches locais integradas** (`git branch --merged feat/wp-08-layout-unico`), candidatas a apagar pelo usuário:
  `docs/publicacao-wp-07`, `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`,
  `feat/wp-08-f1-infra-e-home` (preservada pelo merge `--no-ff`; a integração ainda não está em `develop`, então vale
  esperar a R1 se quiser rastro por nome), `feat/wp-01-legal-lottoexpert-2-05-02`,
  `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`, `feature/invite-bolao`, `main`
  (órfã, `BRANCH-MAIN-ORFA-01`). `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
