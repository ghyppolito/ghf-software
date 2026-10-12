# Achados novos

Espaço para agentes registrarem o que encontrarem **fora do escopo do WP em execução**. Não
corrigir de passagem — registrar aqui e seguir.

**Todo achado tem destino.** A coluna `Destino` aceita: `WP-NN` (um WP que não esteja `done`
passa a ser o dono — o `/wp` lê esta tabela no pré-voo e puxa os achados roteados para ele),
`aceito` (risco conhecido, com a justificativa), `resolvido`, `nota` ou `triagem`. O
`check_plano.py` avisa quando há achado em `triagem` e falha com mais de 10. Triagem é feita
pelo `site-docs` ao fim de cada WP: achado que vira trabalho novo é `/novo-wp`; resolvido se
tacha data e texto.

| Data | WP em execução | Achado | Severidade sugerida | Destino |
|------|----------------|--------|---------------------|---------|
| 2026-10-12 | setup | **`INVITE-OG-IMAGE-01`** — `lotto-expert/sweepstake-invite/lottoexpert-invite.html:12` e `:246` apontam para `https://ghfsoftware.com/logo_transp.png`, que não existe no repositório; todo convite de bolão compartilhado sai sem imagem no WhatsApp. A página também não tem `meta description`. `check_site.py` acusa | Alta | `WP-04` |
| 2026-10-12 | setup | **`POLEPOSITION-DATA-01`** — `poleposition-privacy.html:142` diz "junho de 2026" no HTML estático e `:245` (dicionário i18n) diz "agosto de 2026"; o `.md` diz agosto. `check_site.py` acusa | Média | `WP-04` |
| 2026-10-12 | setup | **`DEVELOP-NAO-PUBLICADO-01`** — `develop` está 10 commits à frente de `master` (TopoWalk e Pole Position: política e landing atualizadas) e o Pages serve `master`. Texto legal de dois apps está desatualizado no ar | Alta | `WP-03` |
| 2026-10-12 | setup | **`BRANCH-MAIN-ORFA-01`** — a branch `main` (local e remota) tem só o commit inicial `4dde88c`; `origin/HEAD` local aponta para ela. Confunde ferramenta e gente. Apagar `main` e `git remote set-head origin master` é decisão do usuário | Baixa | `aceito` — usuário confirmou em 2026-10-12 que `master` é a principal e `main` está sem uso. Apagar (`git push origin --delete main`, `git branch -D main`, `git remote set-head origin master`) fica a critério dele; sem efeito no site |
| 2026-10-12 | setup | **`NAV-FOOTER-DERIVA-01`** — nav e footer das 5 landings têm conteúdo diferente entre si (hash distinto em todas), e há 7 variantes de `tailwind.config` nas 10 páginas. Sem build, a deriva volta a cada edição | Média | `WP-08` |
| 2026-10-12 | setup | **`LEGAL-SEM-OG-01`** — as 5 páginas legais não têm `og:image`; quando compartilhadas (suporte manda o link), saem sem imagem. `check_site.py` avisa, não falha | Baixa | `WP-11` |
| 2026-10-12 | setup | **`I18N-SEM-URL-01`** — o inglês não tem URL própria (`/en/`), só troca por JS com `localStorage`; buscador indexa só o português e não há `hreflang` | Média | `WP-08` |
| 2026-10-12 | setup | **`README-LOTTO-DESATUALIZADO-01`** — `docs/LOTTOEXPERT_README.md` é cópia antiga do README do app; não cita Teimosinha, prestação de contas nem o espelho premium. Não é texto legal; o `/legal` não o cobre | Baixa | `WP-02` |
| 2026-10-12 | setup | **`HEADROOM-ARTEFATOS-01`** — `.claude/.headroom_wrap_*` e `.claude/settings.local.json` estavam sem `.gitignore`; adicionado no setup. Confirmar que não entraram em commit anterior (`git log --all -- .claude/`) | Baixa | `resolvido` — `.gitignore` criado no setup; `git log` sem histórico desses arquivos |
