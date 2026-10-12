---
id: WP-03
titulo: O site no ar tem o LottoExpert 2.05.02 e as atualizações pendentes de TopoWalk e Pole Position
area: infra
status: done
depende_de: [WP-01, WP-02, WP-04]
adr: [ADR-001]
spec: ""
decisoes: [D5]
tamanho: S
risco: alto
visual: true
branch: develop
---

# WP-03 — O site no ar tem o LottoExpert 2.05.02 e as atualizações pendentes

**Depende de:** WP-01, WP-02, WP-04 · **Achados roteados:** `DEVELOP-NAO-PUBLICADO-01`

**Objetivo:** `master` (o que o Pages serve) contém `develop`: política e termos do LottoExpert
2.05.02, landing atualizada, correções do WP-04 e os 10 commits já pendentes (TopoWalk e Pole
Position).

**Contexto:** `git log --oneline master..develop` = 10 commits no setup (2026-10-12), com
texto legal de dois apps que está desatualizado no ar. O app LottoExpert 2.05.02 está indo
para produção e aponta para o site.

**Ler antes:** `.claude/commands/release.md`.

**Arquivos-alvo:** nenhum arquivo — é `/release`. Se o WP-02 estiver bloqueado por D1, o
usuário decide se publica WP-01 + WP-04 antes (recomendado: sim — texto legal não espera landing).

**Passos:** `/release`, passos 1–6.

**Critérios de aceite:**
- `git log --oneline master..develop` vazio após o merge.
- `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -o "Última atualização: [^<]*"` = `12 de Outubro de 2026`.
- `curl -sI https://ghfsoftware.com/lotto-expert/sweepstake-invite/lottoexpert-invite.html` 200;
  `curl -sI https://ghfsoftware.com/.well-known/assetlinks.json` 200.
- `python3 tools/check_site.py` verde na `develop` antes do merge.

**Só no navegador:** o checklist acumulado dos WP-01, 02 e 04, na `develop`, **antes** do
merge; depois do merge, as mesmas páginas no ar. Um convite de bolão real compartilhado no
WhatsApp mostra imagem (WP-04).

**Irreversível:** é deploy. Reverter = novo merge com `git revert` em `develop` e novo release.

**Risco:** alto por ser o que o app em produção aponta; baixo tecnicamente (Pages publica
estático). Erro típico: mesclar com `check_site.py` vermelho.

**Publicado em 2026-10-12** (PR #30 → `develop`, PR #31 → `master`, merges do usuário). Conferido
no ar: `git log origin/master..origin/develop` vazio; 200 em `lottoexpert-privacy.html`,
`lottoexpert-terms.html`, `lottoexpert.html`, `poleposition-privacy.html`,
`.well-known/assetlinks.json`, convite e `assets/lottoexpert_app_mockup.png`; privacidade do
LottoExpert com "12 de Outubro de 2026"; termos com `<title>` "Termos de Uso"; Pole Position com
"setembro de 2026"; landing com Teimosinha; convite com `og:image` do mockup
(servido como `image/png`, 555.466 bytes). Falta só o critério do WhatsApp (prévia com imagem).

**WhatsApp:** usuário colou um link de convite real e a prévia saiu com imagem (2026-10-12).
WP `done`.
