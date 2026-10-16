# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** Branch `feat/wp-08-layout-unico` (integração D13, PR rascunho #37 contra `develop`, **não mesclar**), HEAD 9d308d1, em dia com a origem; CI do #37 verde (run 38946879566: plano, site, lighthouse).

## 1. Onde parei

- WP-22 `done` em 2026-10-16: integrado (41e3b56), CI do #37 verde, usuário rodou o checklist de navegador ("testei, pode fechar"). Nada publicado (D13). Branch `feat/wp-22-a11y-sem-redesign` integrada (local; pode apagar).
- Nenhum WP desbloqueado sem o usuário: WP-16 (`PREVALENCIA-PT-NOS-APPS-01`), WP-10 (checklist do WP-19, D11, D12, copy; agora com menos achados), WP-20 (Claude Design), WP-13 (D3).

## 2. Quebrado ou pela metade agora

Nada quebrado: `npm run build` (21 páginas) e `check_site.py` ("site consistente", 22 páginas, 542 links) passam. Avisos de proveniência legal, preexistentes:
- topowalk e eclipsego: `origemCommit` (7fc7870, 4668019) só existe na máquina local, em nenhum remoto do app.
- topowalk, poleposition e eclipsego: o texto da ref padrão do app difere do `origemCommit` publicado. Pole Position: `sync_legal --check` diz "à frente/divergente"
  (00968f5 não é ancestral de master a22f957); copiar desfaria texto publicado.
  Causa: branches dos apps ainda não levadas à main de cada um. Resolve-se nos apps, não aqui.

## 3. O que só o navegador prova (pendente)

- **WP-19 (rodada 3):** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru` a 360; `?app=topo`, `?app=pole`,
  `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html` a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de`;
  Tab em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o resultado no WP-19 (segue `blocked` por isso).
- **WP-16:** seletor com 3+ línguas (lista, não link).
- **Deploy único (D13), WP-11 e WP-21:** Search Console com `sitemap.xml` enviado e lido; preview no WhatsApp de um convite real e de uma landing, com o site no ar;
  card do WhatsApp/LinkedIn com título em travessão e descrição curta em `/`, `/en/`, `/lottoexpert.html` e `/en/topowalk.html`.
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

Nenhuma: D22, D23 e ADR-007 estão escritos. Cota de CI dos repositórios privados: o usuário trata em versões próprias, nada a fazer aqui.

## 6. Esperando publicação

- `origin/master..origin/develop`: 8 commits só de documentação (`.claude/context`, `tools/gen_estado.py`); **sem texto legal, `src/`, `public/` nem `docs/`** — nenhuma urgência.
- `origin/develop..feat/wp-08-layout-unico`: 139 commits — a modernização inteira espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master` entra no passo 6, D22). Rollback por tag.

## 7. Escrituração e branches

- Triagem: só `INVITE-PAKO-CDNJS-01`, de propósito. O convite está congelado por D13 até o deploy único e ainda não há WP aberto para rotear; o `check_plano.py` o conta
  como "1 achado aguardando triagem" (aviso; só falha com mais de 10). Destino previsto: `/novo-wp` depois do deploy único (pako e Inter locais, `contrato.sha256` novo, teste com `?d=` real).
- Branches integradas na `feat/wp-08-layout-unico` que o usuário pode apagar (`git branch -a --merged feat/wp-08-layout-unico`; nada foi apagado): `feat/wp-15-i18n-n-linguas`,
  `feat/wp-14-readme-e-arquitetura` (local, nunca teve push), `feat/wp-08-f1…` a `f9…`, `feat/wp-09-sync-legal`, `feat/wp-11-seo-tecnico`, `feat/wp-21-copy-de-compartilhamento`,
  `docs/publicacao-wp-07`, `docs/publicacao-trilha-a`, `docs/achados-convite-bolao`, `hotfix/legal-poleposition-outubro`, `feat/wp-01…`, `feat/wp-02…`, `feat/wp-04…`, `feature/invite-bolao`,
  `main` (órfã, `BRANCH-MAIN-ORFA-01`). `feat/wp-19-rodada-3-claude-design` também consta como integrada, mas o WP-19 segue `blocked`; confira antes.
