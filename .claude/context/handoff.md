# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** WP-12 fechado e integrado; WP-15 (i18n em N línguas) implementado e auditado, falta integrar e o navegador.

## 1. Onde parei

- **WP-12 `done`** e integrado na `feat/wp-08-layout-unico` (0640565). Performance 98–100, LCP máx 2,33 s, CLS 0.
- **WP-15 `doing`**, branch `feat/wp-15-i18n-n-linguas` (0e6b666..e31f059): 7 commits, auditoria (qa, seo-perf, ux) e correções feitas, `/verify` verde.
  Entrega: `idiomas.ts`, `SeletorIdioma`, `SugestaoIdioma` (faixa sem redirect), `rota()` com a D23 (A), âncoras legais por posição, regras i18n no `check_site.py` §9 e `tools/test_regras_i18n.py`. ADR-007.
- **Decisões:** D22 (lighthouse obrigatório em `develop`; em `master` entra no `/release`) e D23 (A).
- **Falta para fechar o WP-15:** (1) integração por fast-forward na `feat/wp-08-layout-unico`, push e CI do #37 verde (agora com o passo `unittest` no job `site`); (2) checklist de navegador (seção 3).

## 2. Quebrado ou pela metade agora

Nada quebrado. WP-15 integrado só na própria branch; nada publicado (D13).

## 3. O que só o navegador prova (usuário ainda não reportou)

- **WP-15** (`npm run build && python3 -m http.server 8080 -d dist`, Chrome em en): `/`, `/lottoexpert.html`, `/topowalk-privacy.html` a 360x568,
  360x640 e 1280x720. Faixa embaixo em uma linha abaixo de 768 px, URL continua pt, conteúdo não pula, não cobre CTA.
  "Switch to English" leva à mesma página em `/en/`; recarregar volta a faixa, sem redirect. ✕/Esc fecham; não volta na aba, volta em aba nova.
  Foco após fechar vai ao último link do rodapé. `prefers-reduced-motion` sem animação. Menu do celular por cima da faixa.
  Chrome em pt-BR: `/` sem faixa, `/en/` com "Ver em português". Seletor pt/en igual ao de antes. (Seletor 3+ línguas vai ao checklist do WP-16.)
- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`; Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota): URL contratual; o usuário não pediu WP.

**Checklist do deploy único (D13), do WP-11 e do WP-21:** Search Console com `sitemap.xml` enviado e lido; preview no WhatsApp de um convite
real e de uma landing, com o site no ar; card do WhatsApp/LinkedIn com título em travessão e descrição curta em `/`, `/en/`, `/lottoexpert.html` e `/en/topowalk.html`.

## 4. Próxima ação

**Do agente, depois do usuário:** integrar o WP-15 por fast-forward (o usuário roda
`! git checkout feat/wp-08-layout-unico && git merge --ff-only feat/wp-15-i18n-n-linguas`), push da integração, CI do #37, fechar o WP com o relato do navegador.

**Do usuário:**
1. Rodar o merge acima e o checklist do WP-15.
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
