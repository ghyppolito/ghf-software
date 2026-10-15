# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-15 (fim).** Fechamento do WP-08, na branch `feat/wp-08-layout-unico`.

## 1. Onde parei

- **WP-08 `done` na integração** (`feat/wp-08-layout-unico`): as 9 fatias integradas, CI do #37 verde, checklist de navegador reportado pelo usuário ("estao ok", 2026-10-15). O PR #37 segue aberto até o deploy único (D13); nada foi publicado.
- **Próximo: WP-09** (`sync_legal.py`), que o agente começa por `/wp`. Nada o bloqueia: depende só do WP-08 e de D7 (resolvida).
- **D13 em vigor:** deploy único depois de WP-08..WP-19; antes, tag `pre-modernizacao` em `master` e ensaio do rollback.
- **Repositórios dos apps, sem merge:** topo-walk `docs/politica-tres-observacoes` (7fc7870); eclipse-go `docs/email-suporte-politica`
  (7f349a2, 4668019); pole-position `item/PP-144-segunda-sessao-mesma-pista` (00968f5); `/legal poleposition` quando a PP-144 entrar no app. **WP-19** `blocked` (checklist da rodada 3).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar nem pela metade. Servidor antigo na porta 8081 (pid 686166), deixado por uma auditoria: o usuário decide se encerra.

## 3. O que só o navegador prova (usuário ainda não reportou)

- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota, sem WP): código só tema claro; hipótese de escurecimento
  forçado do navegador; o usuário testou e não pediu WP. Convite é URL contratual.

## 4. Próxima ação

**Do usuário:**
1. Levar as branches dos apps (seção 1) para a main de cada um (topo-walk e eclipse-go; o Pole Position com o `/legal poleposition` depois).
2. Checklist de navegador do WP-19; escrever o resultado no WP.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10; D3 (medição) bloqueia o WP-13. `PP-NAV-CONTRASTE-01` aguarda decisão.

**Do agente:** `/wp` para abrir o WP-09.

**Copy pendente do usuário antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade";
selo "Vantagem Competitiva" da LottoExpert (`LOTTO-COPY-VANTAGEM-01`). Decidir também qual descrição do LottoExpert fica na
home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões fora de `decisoes.md` e ADR

- **Opção (A) do texto do EclipseGo** (site segue o `.md` do app) e **check da raiz fora do CI** (veredito do arquiteto): no WP-08.
- **`lastUpdated` string `AAAA-MM[-DD]`** para as fatias 7 e 8: no WP-08 e em `WP09-NOME-ARQUIVO-01`.
- **Fatiamento em 9 fatias e deploy único (D13):** plano do arquiteto, no WP-08; D13 em `decisoes.md`.
- Decisões abertas em `decisoes.md`: D3, D11, D12. D10 resolvida.

## 6. Escrituração e branches

- Triagem de `achados-novos.md`: nenhuma linha em `triagem`; nenhum achado aberto aponta mais para o `WP-08` (`HOTFIX-LEGAL-POS-MIGRACAO-01` foi para o `WP-09`, `404-SEM-OG-CANONICAL-01` está resolvido).
- **Branches locais já integradas**, candidatas a apagar pelo usuário: `feat/wp-08-f2…`, `f3…`, `f4…`, `f5…`, `feat/wp-08-f6-legal-eclipsego`, `feat/wp-08-f7-legal-topowalk-poleposition` `feat/wp-08-f8-legal-lottoexpert` e `feat/wp-08-f9-public-limpeza` (fatias integradas;
  `f1-infra-e-home` idem, com a ressalva de que a integração ainda não está em `develop`), `docs/publicacao-wp-07`,
  `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`, `feat/wp-01-legal-lottoexpert-2-05-02`,
  `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`, `feature/invite-bolao`, `main` (órfã,
  `BRANCH-MAIN-ORFA-01`) e as `docs/…`/`hotfix/…` do Pole Position já mescladas (conferir com `git branch --merged`).
  `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
