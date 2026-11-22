# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-22.** Fatia 5 do WP-10 (template de landing e EclipseGo, D29) feita em `feat/wp-10-fatia-5-eclipsego` (criada de `origin/feat/wp-08-layout-unico`; não enviada).

## 1. Onde parei

- Fatias 1 a 4 do WP-10 integradas (a 4 pelo #50, 551b846; o CI do #37 passou). A fatia 5 nova, template e EclipseGo, está feita na branch (f59a8c7, e8bad59, db8f931) e espera PR para `feat/wp-08-layout-unico`; quem mescla é o usuário. WP-10 segue `doing`.
- A D29 inverteu a ordem: a 5 é o EclipseGo e a 9 é o LottoExpert.
- Próxima: fatia 6, Home. Pode vir logo depois da 5 e passa a ler o `resumo` de cada app. Depois vêm a 7 (TopoWalk), a 8 (Pole Position) e a 9 (LottoExpert), cada uma esperando as capturas dos apps, que estão em evolução.
- WP-19 `done`: o usuário aprovou as landings; os itens 1, 3, 5 e 6 do checklist foram para a revisão final da fatia 10. WP-25 `done`.
- WP-26 a WP-28 criados (termos de uso de TopoWalk, EclipseGo e Pole Position), com a D28 (B): exigência da UE para comerciante, prazo 2027, o vão entra no deploy único.
- O usuário quer o deploy único **antes do fim de 2026**.

## 2. Quebrado ou pela metade agora

Nada quebrado. Passaram no `/verify` da fatia 5: `test:css`, `check_site.py` (raiz e `dist`), `contrato.sha256`, html-validate, `lighthouse.py` sem `--medir`, `gen_estado --check` e `check_plano`. `lychee` não está instalado localmente; o CI cobre.

**Cuidados:**
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com a própria linha de comando do laço, que não termina. Use `pgrep -f "^python3 tools/lighthouse.py"` ou espere pelo PID.
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- O `--medir` do `lighthouse.py` não confere o orçamento; use a execução sem a flag.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- `tools/sync_legal.py:51` aponta o Pole Position para `pole-position/pole-position-app`, caminho que não existe (`PP-ORIGEM-CAMINHO-01`, roteado ao WP-28).

## 3. O que só o navegador prova (pendente)

**Fatia 5 do WP-10 (template e EclipseGo):** `python3 -m http.server 8080 -d dist`, em `/eclipsego.html` e `/en/eclipsego.html`, a 360, 768 e 1280. Conferir:
- sem rolagem horizontal;
- hover do CTA e do `summary`;
- foco por Tab no CTA, no Nav, nos 4 `summary` e no link da privacidade;
- recorte da foto do hero a 768 (agora centrada);
- recorte 9:16 da captura da F1, com os horários visíveis;
- prova de 640 a 1023 px, com o 3º item na linha inteira;
- FAQ abrindo e fechando por teclado;
- âncoras do Nav;
- Safari/iOS: o `summary` sem o marcador nativo.

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

**Do agente:** PR `feat/wp-10-fatia-5-eclipsego` -> integração (o usuário mescla) e seguir para a **fatia 6 (Home)**. As fatias 7 a 9 precisam das capturas dos apps (D26).

**Do usuário, em ordem de impacto no prazo:**
1. capturas do app (D26);
2. os textos `TERMS_OF_SERVICE.md` nos repositórios de TopoWalk, EclipseGo e Pole Position;
3. D3 (medição);
4. sessão do WP-20 no Claude Design (imagens 1200x630, o logo, o callout `LEGAL-CALLOUT-SEM-HANDOFF-01`);
5. checklists de navegador das fatias 3, 4 e 5 (seção 3);
6. Safari (pelo iPhone).

## 5. Decisões não registradas

Nenhuma.

## 6. Esperando publicação

A modernização inteira (WP-08 a WP-10 e o resto) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a fatia 9; o PR #37 não se mescla até o deploy único.

## 7. Escrituração e branches

- Triagem: vazia. Achados novos da fatia 5 roteados: `LANDING-ESPELHO-SEM-TESTE-01` (fatia 7), `HERO-ASPECT-RETRATO-01` (fatias 7 e 8), `ECLIPSE-OG-IMAGE-442-01` e `FUNC-SEM-IMAGEM-METADE-VAZIA-01` (WP-20), `CORONA-GLOW-ORFAO-01`, `FAQ-SINAL-ABERTO-01`, `LANDING-JSONLD-CAMPOS-01`, `HERO-H1-SEM-PALAVRA-CHAVE-01` (fatia 10; o último é decisão de copy do usuário). Seguem: `PP-ORIGEM-CAMINHO-01` (WP-28), `APPS-LISTA-DUPLICADA-01` e `ORCAMENTO-404-FROUXO-01` (fatia 10).
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-10-fatia-4` (integrada pelo #50), `feat/wp-10-fatia-5-eclipsego` (não enviada) e `feat/wp-05-ci-no-pr` (não integrada).
