# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-15 (fim).** Fechamento do WP-08, na branch `feat/wp-08-layout-unico`.

## 1. Onde parei

- **WP-11 `done`** (2026-10-15): integrado na `feat/wp-08-layout-unico` (be43372), CI do #37 verde (run 38838938355),
  os 2 validadores com 0 erro pelo usuário. Não publicado (D13).
- **Próximos:** WP-20 (imagens 1200×630, sessão no Claude Design) e WP-21 (copy da ficha da Play), ambos antes do deploy único (D13); depois WP-10.

## 2. Quebrado ou pela metade agora

Nada quebrado no ar nem pela metade. Servidor antigo na porta 8081 (pid 686166), deixado por uma auditoria: o usuário decide se encerra.

## 3. O que só o navegador prova (usuário ainda não reportou)

- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota, sem WP): código só tema claro; hipótese de escurecimento
  forçado do navegador; o usuário testou e não pediu WP. Convite é URL contratual.

**Checklist do deploy único (D13), vindo do WP-11:** Search Console com o `sitemap.xml` enviado e lido; preview no WhatsApp
de um convite real gerado pelo app e de uma landing, sobre o site no ar.

## 4. Próxima ação

**Do usuário:**
1. Levar as branches dos apps (seção 1) para a main de cada um (topo-walk e eclipse-go; o Pole Position com o `/legal poleposition` depois).
2. Checklist de navegador do WP-19; escrever o resultado no WP.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10; D3 (medição) bloqueia o WP-13. `PP-NAV-CONTRASTE-01` aguarda decisão.

**Do agente:** `/wp` para o WP-21 (copy da ficha da Play) ou o WP-20 quando as imagens existirem; depois o WP-10 (branch a partir da integração, D13).

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

- Triagem de `achados-novos.md`: nenhuma linha em `triagem`; os três achados do WP-09 e `VERIFY-DIFF-LEGAL-WORKTREE-01` estão `resolvido`.
- **Branches locais já integradas**, candidatas a apagar pelo usuário: `feat/wp-08-f2…`, `f3…`, `f4…`, `f5…`, `feat/wp-08-f6-legal-eclipsego`, `feat/wp-08-f7-legal-topowalk-poleposition` `feat/wp-08-f8-legal-lottoexpert` e `feat/wp-08-f9-public-limpeza` (fatias integradas;
  `f1-infra-e-home` idem, com a ressalva de que a integração ainda não está em `develop`), `docs/publicacao-wp-07`,
  `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`, `feat/wp-01-legal-lottoexpert-2-05-02`,
  `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`, `feature/invite-bolao`, `main` (órfã,
  `BRANCH-MAIN-ORFA-01`) e as `docs/…`/`hotfix/…` do Pole Position já mescladas (conferir com `git branch --merged`).
  `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
