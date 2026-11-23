# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-22.** Fatias 4, 5, 6 e 10a do WP-10 mescladas em `feat/wp-08-layout-unico`; o #37 passou no CI em 0fe1b70.

## 1. Onde parei

- WP-10 `doing`, por fatias. Cada fatia vira PR para `feat/wp-08-layout-unico`, o usuário mescla, e o CI prova no #37 (`feat/wp-08-layout-unico -> develop`), que **não se mescla antes do deploy único** (D13). Mescladas hoje: fatia 4 (404), 5 (template e EclipseGo, D29), 6 (Home, D30; #52, 5161f02) e 10a (aceite parcial, D31, JSON-LD; #53, 0fe1b70). WP-10 e `decisoes.md` já refletem D29 a D31.
- Branch local: `feat/wp-10-fatia-10a-aceite-parcial`, já mesclada. Esta escrituração do handoff está **não commitada** nela. Quando o usuário pedir, vai para branch nova a partir de `origin/feat/wp-08-layout-unico`, com PR para ela.
- Bloqueadas pelo usuário: fatias 7 (TopoWalk) e 8 (Pole Position) esperam capturas (D26); a 9 (LottoExpert), capturas e copy (D25); a 10b (remover `legado.css`/`brand.*`, aceite final) vem por último. Nenhuma fatia começa sem essa entrada.
- Fora do WP-10: WP-26 a WP-28 esperam `TERMS_OF_SERVICE.md` nos repos dos apps; D3 decidida (2026-11-22: não medir; WP-13 `adiado` para futura análise, sem bloquear o deploy único); WP-20 é sessão do Claude Design. Também nesta sessão: a régua do `test:css` foi trocada (decisão do usuário) e o orçamento Lighthouse de `/eclipsego.html` foi atualizado. Tag `v1.0.1` do `eclipse-go` (leve, `f5c1d6b`, 2026-07-26) dá o `atualizadoEm` do EclipseGo; o §21 do `check_site.py` a confere. Deploy único **antes do fim de 2026**.

## 2. Quebrado ou pela metade agora

Nada quebrado. CI do #37 em 0fe1b70: `plano`, `site` e `lighthouse` passaram. Passaram no `/verify` local: `test:css`, `check_site.py` (raiz e `dist`), `contrato.sha256`, html-validate, `lighthouse.py` sem `--medir`, `gen_estado --check` e `check_plano`. `lychee` não está instalado localmente; o CI cobre.

**Cuidados:**
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com a própria linha de comando do laço, que não termina. Use `pgrep -f "^python3 tools/lighthouse.py"` ou espere pelo PID.
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- O `--medir` do `lighthouse.py` não confere o orçamento; use a execução sem a flag.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- `tools/sync_legal.py:51` aponta o Pole Position para `pole-position/pole-position-app`, caminho que não existe (`PP-ORIGEM-CAMINHO-01`, roteado ao WP-28).

## 3. O que só o navegador prova (pendente)

**Fatia 10a do WP-10 (aceite parcial):** `python3 -m http.server 8080 -d dist`. Conferir:
- FAQ do EclipseGo (`/eclipsego.html` e `/en/eclipsego.html`): "+" vira "−" ao abrir e volta ao fechar, a 360 e a 1280;
- Home: Sobre e Privacidade lado a lado a 1280 e empilhados a 360; o pouso de `/#sobre`;
- 404, Footer e Nav sem mudança visível;
- Rich Results Test em `/` e `/eclipsego.html` (JSON-LD novo).

**Fatia 6 do WP-10 (Home):** `python3 -m http.server 8080 -d dist`, em `/` e `/en/`, a 360, 768, 1024 e 1280. Conferir:
- sem rolagem horizontal;
- grade 2x2 a 1024, sem card órfão;
- alturas iguais por linha;
- clique em qualquer ponto do card abre a landing; o Play abre em outra aba;
- hover do card, do Play (borda) e dos links de privacidade, com mouse real;
- Tab passando por nome e Play de cada card;
- aspecto contra o export (`Home.dc.html`);
- Safari/iOS.

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

**Do agente:** nada começa sozinho. Com capturas da fatia 7 ou 8 (ou da 9, com a copy), abrir `/wp WP-10` na fatia correspondente. Se o usuário pedir, commitar este handoff em branch nova a partir de `origin/feat/wp-08-layout-unico`.

**Do usuário, em ordem de impacto no prazo:**
1. capturas do app (D26) e, para o LottoExpert, a copy (D25);
2. os `TERMS_OF_SERVICE.md` de TopoWalk, EclipseGo e Pole Position;
3. sessão do WP-20 no Claude Design;
4. checklists de navegador das fatias 3, 4, 5, 6 e 10a (seção 3), a 360/768/1280, pt e en;
5. Safari (pelo iPhone).

## 5. Decisões não registradas

Nenhuma. `BUILD-RELOGIO-NAO-REPRODUTIVEL-01` foi decidido (D31) e implementado na 10a. O primeiro corte real da D12 é o do EclipseGo, depois de 2027-07-26; o §20 avisa 30 dias antes.

## 6. Esperando publicação

`git log origin/master..origin/develop` (após `git fetch`): 4 commits só de documentação (04f8639, 400d254, 09967ab, 44e95af), **sem texto legal**, sem urgência. O que realmente espera é a modernização inteira (WP-08 a WP-10 e o resto), que está em `feat/wp-08-layout-unico` (#37) e só vai ao ar no deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a 10b.

## 7. Escrituração e branches

- Triagem: vazia. Os 11 achados da 10a e a `ROTULO-DATA-DUAS-FONTES-01` ("mantém duas fontes") estão resolvidos. Novos da 10a: fatia 10b (`LISTAAPPS-VARIANTES-01`, `FAVICON-LITERAL-LEGAIS-01`); WP-20 (`ORG-LOGO-NAO-QUADRADO-01`, `OG-IMAGE-QUADRADA-LANDINGS-01`, e `JSONLD-IMAGE-FAVICON-PEQUENO-01`, que pode ir à 10b); WP-28 (`SYNC-LEGAL-DOCSTRING-GIT-01`); nota (`SOFTWAREAPP-SEM-RATING-01`). Da fatia 6, seguem para a 10b `HOME-ICONES-ORFAOS-01`, `CSS-BUNDLE-NOME-FOOTER-01`, `HOME-VOCABULARIO-TECNICO-01`; para o WP-20 os 5 da Home; WP-18 `HOME-X-DEFAULT-EN-01`; WP-28 `CLAUDE-MD-POLE-CAMINHO-01`. `INDEX-LOTTO-DESC-DIVERGE-01` segue aberto para a fatia 9.
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-10-fatia-6-home` e `feat/wp-10-fatia-10a-aceite-parcial` (ambas mescladas) e `feat/wp-05-ci-no-pr` (não integrada).
