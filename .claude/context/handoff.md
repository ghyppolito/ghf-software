# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-22.** Fatia 4 do WP-10 (404) feita em `feat/wp-10-fatia-4` (criada de `origin/feat/wp-08-layout-unico`; não enviada).

## 1. Onde parei

- Fatias 1 a 4 do WP-10 feitas. A 1, 2 e 3 foram integradas (#46, #48, #49; o CI do #37 passou nos 3 jobs depois do #49). A 4 está em `feat/wp-10-fatia-4` (1f6c207, 27700db), esperando PR para `feat/wp-08-layout-unico`; quem mescla é o usuário. WP-10 segue `doing`.
- Próxima: fatia 5 (LottoExpert). Começa com a copy publicada e precisa das capturas D26 para fechar.
- WP-19 `done`: o usuário aprovou as landings; os itens 1, 3, 5 e 6 do checklist foram para a revisão final da fatia 10. WP-25 `done`.
- WP-26 a WP-28 criados (termos de uso de TopoWalk, EclipseGo e Pole Position), com a D28 (B): exigência da UE para comerciante, prazo 2027, o vão entra no deploy único.
- O usuário quer o deploy único **antes do fim de 2026**.

## 2. Quebrado ou pela metade agora

Nada quebrado. Passaram no `/verify` da fatia 4: `test:css`, `check_site.py` (raiz e `dist`), `contrato.sha256`, html-validate, `lighthouse.py` sem `--medir`, `gen_estado --check` e `check_plano`. `lychee` não está instalado localmente; o CI cobre.

**Cuidados:**
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com a própria linha de comando do laço, que não termina. Use `pgrep -f "^python3 tools/lighthouse.py"` ou espere pelo PID.
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- O `--medir` do `lighthouse.py` não confere o orçamento; use a execução sem a flag.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- `tools/sync_legal.py:51` aponta o Pole Position para `pole-position/pole-position-app`, caminho que não existe (`PP-ORIGEM-CAMINHO-01`, roteado ao WP-28).

## 3. O que só o navegador prova (pendente)

**Fatia 4 do WP-10 (404):** `python3 -m http.server 8080 -d dist`, abrir `/404.html` a 360, 768 e 1280. Conferir:
- uma coluna abaixo de 1024 e duas a partir de 1024;
- o rodapé no fim da tela;
- sem rolagem horizontal;
- o anel de foco visível em todos os links, sem corte dentro da lista;
- os 4 quadrados nas cores dos apps;
- os ícones nítidos a 2x;
- o hover do botão.

**Fatia 3 do WP-10** (`python3 -m http.server 8080 -d dist`), nas 10 legais:
- a 360, 768 e 1280, em pt e en: sumário recolhível e sumário lateral fixo;
- a tabela que rola, com o anel;
- as caixas de destaque (termos §3; privacidade do LottoExpert §2 e §9.2);
- a troca de idioma numa seção, que deve manter a seção;
- impressão (Ctrl+P);
- a faixa clara no overscroll acima do Nav e abaixo do Footer;
- o chevron do `summary`.

Resta também o Safari (pelo iPhone, `python3 -m http.server 8080 -d dist -b 0.0.0.0`). Herdados: seletor com 3+ línguas (WP-16); Search Console, preview no WhatsApp e cards de compartilhamento no deploy único (WP-11, WP-21); 404 em `/x/y` só no Pages; WP-23 depois do deploy.

## 4. Próxima ação

**Do agente:** PR `feat/wp-10-fatia-4` -> integração (o usuário mescla), conferir o CI do #37 e seguir para a **fatia 5 (LottoExpert)**, que precisa das capturas D26.

**Do usuário, em ordem de impacto no prazo:**
1. capturas do app (D26);
2. os textos `TERMS_OF_SERVICE.md` nos repositórios de TopoWalk, EclipseGo e Pole Position;
3. D3 (medição);
4. sessão do WP-20 no Claude Design (imagens 1200x630, o logo, o callout `LEGAL-CALLOUT-SEM-HANDOFF-01`);
5. checklists de navegador das fatias 3 e 4 (seção 3);
6. Safari (pelo iPhone).

## 5. Decisões não registradas

Nenhuma.

## 6. Esperando publicação

A modernização inteira (WP-08 a WP-10 e o resto) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a fatia 9; o PR #37 não se mescla até o deploy único.

## 7. Escrituração e branches

- Triagem: vazia. `PP-ORIGEM-CAMINHO-01` roteado ao WP-28; `APPS-LISTA-DUPLICADA-01` e `ORCAMENTO-404-FROUXO-01` roteados à fatia 10 do WP-10.
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-10-fatia-3` (já integrada pelo #49), `feat/wp-10-fatia-4` (não enviada) e `feat/wp-05-ci-no-pr` (não integrada).
