# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Fim da sessão de 2026-10-12.** Branch `feat/wp-05-ci-no-pr` (commits 025793e, 6081b1b e a escrituração).

## 1. Onde parei

Trilha A publicada (WP-01 a 04 `done`). WP-05 (CI no PR) implementado e verde localmente, `blocked`
só porque o critério "`gh pr checks` mostra `plano` e `site` verdes" precisa de push e PR do usuário.
Depois do WP-05: WP-07 bloqueado por D2 (stack); WP-06 pode começar quando o usuário quiser (D4).

## 2. Quebrado ou pela metade agora

Nada. `check_site.py`, `gen_estado.py --check`, `check_plano.py`, html-validate (0 erros, 202 avisos)
e lychee `--offline` saem 0.

## 3. O que só o navegador prova

Nada. O que falta é ver o CI verde no Actions (ver 4).

## 4. Próxima ação

1. Usuário: `git push -u origin feat/wp-05-ci-no-pr`, abrir PR para `develop`, conferir
   `gh pr checks`, e voltar para marcar o WP-05 `done`.
2. WP-05 não muda o site publicado: não precisa de `/release` para efeito no ar (o workflow só
   chega à `master` na próxima release).
3. Opção ao usuário, sem decisão registrada: proteger `develop`/`master` exigindo os checks
   `plano` e `site`. Se quiser, vira entrada em `decisoes.md`.
4. Em seguida: WP-06 (brief do Claude Design, D4) quando quiser; WP-07 espera D2.

## 5. Decisões fora de `decisoes.md` e ADR

- `check_plano.py` é cópia do lotto-expert com `AREAS` e `visual` adaptados (D6).
- `og:image` ausente é aviso em `check_site.py`; apontando para arquivo inexistente é erro.
- lychee sem `--include-fragments`: âncoras de i18n/JS dão falso positivo.

## 6. Esperando publicação

Branch do WP-05 ainda não foi enviada ao remoto. Sem efeito no site.
