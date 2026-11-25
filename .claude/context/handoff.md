# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-24.** Fatia 9 do WP-10 parcial, em branch própria. Fatias 4, 5, 6 e 10a já mescladas em `feat/wp-08-layout-unico` (#37 verde em 0fe1b70).

## 1. Onde parei

- WP-26 e WP-27 `done` (escrituração de 2026-11-25); WP-10 fatias 7 (TopoWalk) e 8 (Pole) entregues, WP-10 `blocked` nas capturas do scanner. Branches empilhadas e locais: `feat/wp-30-revisao-visual` (PR #55 para `feat/wp-08-layout-unico`) → `feat/wp-26-termos-topowalk` → `feat/wp-27-termos-eclipsego`; nenhuma com PR além do #55.
- **Próximo:** usuário mescla o #55; depois PRs do WP-26 e do WP-27 (rebase na integração). Então WP-10 fatia 9 (prestação de contas no emulador do LottoExpert; scanner é do usuário), WP-28 (termos do Pole: o usuário escreve no app), WP-32, e o deploy único (espera a 2.06.00 na Play).
- Emuladores: `emulator-5582` (topowalk-api34), `emulator-5584` (pole-play34), `emulator-5580` (lotto); confira com `adb devices`, sem desligar. Servidor local :8080.

## 2. Quebrado ou pela metade agora

Pela metade: a fatia 9 (acima). Nas verificações locais da fatia: build, `check_site.py` (raiz e `dist`), contrato, html-validate, unittest 42 OK, `test:css` 21 pass, Lighthouse de `/lottoexpert.html` (perf 98, a11y 100, bp 100, seo 100, LCP 2,25 s) dentro do orçamento. `lychee` não está instalado; o CI cobre. O CI ainda não viu esta branch.

**Cuidados:**
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com a própria linha de comando do laço, que não termina. Use `pgrep -f "^python3 tools/lighthouse.py"` ou espere pelo PID.
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- O `--medir` do `lighthouse.py` não confere o orçamento; use a execução sem a flag.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- `tools/sync_legal.py:51` aponta o Pole Position para `pole-position/pole-position-app`, caminho que não existe (`PP-ORIGEM-CAMINHO-01`, roteado ao WP-28).

## 3. O que só o navegador prova (pendente)

**WP-30 (direção visual):** `python3 -m http.server 8080 -d dist`. O visual foi aprovado; falta reportar:
- foco por Tab nas 4 cores de acento (Home, landings, legais);
- impressão real (Ctrl+P) de uma legal;
- hover do sumário das legais;
- `prefers-reduced-motion` ligado: nada anima;
- Safari e Firefox (sem `animation-timeline`): o conteúdo deve aparecer parado.

**Fatia 9 do WP-10 (LottoExpert):** `python3 -m http.server 8080 -d dist`, em `/lottoexpert.html` e `/en/lottoexpert.html`, a 360, 768 e 1280. Conferir:
- recorte do hero (nome inteiro, cards Quina/Lotomania cortados na borda);
- CTA da Play acima da dobra a 1280×720;
- destaques sem imagem onde faltam as capturas (scanner e prestação de contas);
- tabela a 360 rolando, com foco por teclado; Anual em destaque; "R$ 69,90 pago uma vez";
- selo 18 e link dos termos; aviso de jogo responsável no fim; FAQ;
- contraste do violeta; Nav e âncoras;
- Home sem mudança visível.

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

**Do agente:** com o scanner entregue, recortar a barra de status; com a Mega-Sena 3090 apurada, capturar a prestação de contas no `emulator-5580`; depois fechar a fatia 9 (também `CAPTURAS-BARRA-GESTOS-01` e `apps.ts`). Nada de PR sem o usuário pedir.

**Do usuário, em ordem de impacto no prazo:**
1. captura do scanner no celular, com bilhete real (Lotofácil ou Mega-Sena);
2. capturas do TopoWalk e do Pole Position (D26) e os `TERMS_OF_SERVICE.md` dos três apps;
3. 2.06.00 na produção da Play (libera o deploy único);
4. sessão do WP-20 no Claude Design;
5. checklists de navegador das fatias 3, 4, 5, 6, 9 e 10a (seção 3); Safari pelo iPhone.

## 5. Decisões não registradas

Nenhuma. `BUILD-RELOGIO-NAO-REPRODUTIVEL-01` foi decidido (D31) e implementado na 10a. O primeiro corte real da D12 é o do EclipseGo, depois de 2027-07-26; o §20 avisa 30 dias antes.

## 6. Esperando publicação

`git log origin/master..origin/develop` (após `git fetch`): 4 commits só de documentação (04f8639, 400d254, 09967ab, 44e95af), **sem texto legal**, sem urgência. O que realmente espera é a modernização inteira (WP-08 a WP-10 e o resto), que está em `feat/wp-08-layout-unico` (#37) e só vai ao ar no deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a 10b.

## 7. Escrituração e branches

- Triagem: vazia. Fechados pela fatia 9: `LOTTO-COPY-VANTAGEM-01`, `LOTTO-EN-ROTULOS-PT-01`, `LOTTO-PT-HTML-DIVERGE-01`, `FEATURES-SELO-PREMIUM-01`, `TEIMOSINHA-FORA-DA-TABELA-01`, `LOTTO-CONTRASTE-AA-01`, `INDEX-LOTTO-DESC-DIVERGE-01`; só a parte LottoExpert de `LANDINGS-RESIDUO-RODADA-2-01`, `EXPORT-COPY-SEM-ORIGEM-01` e `LANDINGS-URL-E-PLAY-01`. Novos: 10b (`LEGADO-TEMA-LOTTOEXPERT-ORFAO-01`, `FONTES-LOTTO-SEM-LANDING-01`), WP-20 (`OG-LOTTO-MOCKUP-IPHONE-01`), 10b (`ORCAMENTO-LH-FOLGA-01`), fatia 9 (`CAPTURAS-BARRA-GESTOS-01`, `APPS-LOTTO-2060-TAG-01`), aceito (`LOTTO-LEAD-CONFERENCIA-PRO-01`). `HERO-ASPECT-RETRATO-01` agora vale também para o LottoExpert. Os da 10a e da fatia 6 seguem roteados à 10b, WP-20, WP-18 e WP-28 como registrados em `achados-novos.md`.
- Branches: `develop`, `master`, `feat/wp-08-layout-unico` (#37), `docs/wp-27-ampliado-wp-29-respostas-fatia-9` e `feat/wp-10-fatia-9-lottoexpert` (locais, não enviadas), mais as já mescladas `feat/wp-10-redesign`, `feat/wp-10-fatia-6-home`, `feat/wp-10-fatia-10a-aceite-parcial`, e `feat/wp-05-ci-no-pr` (não integrada).
