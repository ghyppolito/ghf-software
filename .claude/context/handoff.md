# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** WP-12 e WP-15 (i18n em N línguas) fechados e integrados na `feat/wp-08-layout-unico`.

## 1. Onde parei

- **WP-15 `done`** (2026-10-16): código integrado na `feat/wp-08-layout-unico` (0e6b666..e31f059), CI do #37 verde (run 38920589727) e checklist de navegador reportado pelo usuário ("ficou ok"). Nada publicado (D13).
- **WP-12 `done`**, também integrado. Decisões D22 e D23 (A) registradas.
- **Próximos:** WP-14 (docs, S); WP-16 (depende de `PREVALENCIA-PT-NOS-APPS-01`); WP-10 (espera checklist do WP-19, D11, D12 e copy); WP-20 (sessão do usuário no Claude Design); WP-13 (D3).

## 2. Quebrado ou pela metade agora

Nada quebrado. WP-15 integrado só na própria branch; nada publicado (D13).

## 3. O que só o navegador prova (pendente)

- **WP-15:** reportado como ok em 2026-10-16; o seletor com 3+ línguas segue no checklist do WP-16.
- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`; Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota): URL contratual; o usuário não pediu WP.

**Checklist do deploy único (D13), do WP-11 e do WP-21:** Search Console com `sitemap.xml` enviado e lido; preview no WhatsApp de um convite
real e de uma landing, com o site no ar; card do WhatsApp/LinkedIn com título em travessão e descrição curta em `/`, `/en/`, `/lottoexpert.html` e `/en/topowalk.html`.

## 4. Próxima ação

**Do agente:** `/wp` sem número propõe o próximo (WP-14 é o desbloqueado e pequeno).

**Do usuário:**
1. Se quiser, apagar a `feat/wp-15-i18n-n-linguas` (já integrada).
2. Em `master`, `lighthouse` entra no `/release` do deploy único (D22). Deploy único (D13): modernização inteira num só, rollback por tag.
3. Levar as branches dos apps para a main de cada um (topo-walk e eclipse-go; Pole Position com o `/legal poleposition` depois).
4. Checklist de navegador do WP-19.
5. Decidir D11 (`--success`) e D12 (limiares de destaque), só para o WP-10; D3 (medição) bloqueia o WP-13. `PP-NAV-CONTRASTE-01` aguarda decisão.
6. Nos apps (D19): registrar o en do LottoExpert no `ASO_METADATA.md` e criar a ficha do EclipseGo.

**Copy pendente antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo responsável (o export traz
"Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade"; selo "Vantagem Competitiva" (`LOTTO-COPY-VANTAGEM-01`);
qual descrição do LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Escrituração e branches

- Triagem: só `INVITE-PAKO-CDNJS-01`, de propósito (convite congelado por D13); destino previsto: `/novo-wp` depois do deploy único.
  `TOOLS-PYCACHE-GITIGNORE-01` foi para o WP-14.
- **Branches locais candidatas a apagar pelo usuário** (`feat/wp-12-performance` já foi apagada, local e remota): `feat/wp-08-f1…` a `f9…` (conferir com
  `git branch --merged`), `docs/publicacao-wp-07`, `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`,
  `feat/wp-01-legal-lottoexpert-2-05-02`, `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`,
  `feature/invite-bolao`, `main` (órfã, `BRANCH-MAIN-ORFA-01`) e as `docs/…`/`hotfix/…` do Pole Position já mescladas.
  `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
