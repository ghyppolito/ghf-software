# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-22.** Fatia 6 do WP-10 (Home, D30) feita em `feat/wp-10-fatia-6-home` (criada de `origin/feat/wp-08-layout-unico`; não enviada).

## 1. Onde parei

- Fatias 1 a 5 do WP-10 integradas (a 5 pelo #51, 723ad46; o CI do #37 passou nos 3 jobs). A fatia 6 (Home) está feita na branch (20649c6, a4d30b4, 1f69780 e a escrituração) e espera PR para `feat/wp-08-layout-unico`; quem mescla é o usuário. WP-10 segue `doing`.
- Próxima: **fatia 10a (aceite parcial)**: `BUILD-RELOGIO-NAO-REPRODUTIVEL-01` (depende de decisão, abaixo), `APPS-LISTA-DUPLICADA-01` com `ICONES-APPS-DUPLICADOS-01` e `ROTULO-DATA-DUAS-FONTES-01`, `APPS-ATUALIZADO-EM-SEM-CHECK-01`, `HOME-ORDEM-SEM-CHECK-01`, `ORCAMENTO-404-FROUXO-01`, `FAQ-SINAL-ABERTO-01`, `LANDING-JSONLD-CAMPOS-01` com `ORGANIZATION-JSONLD-MINIMO-01`, `CORONA-GLOW-ORFAO-01`, `SOBRE-REGIAO-ENGLOBA-PRIVACIDADE-01`; mais a tabela de contraste e o Lighthouse a11y >= 95 nas páginas redesenhadas.
- Depois vêm 7 (TopoWalk), 8 (Pole Position) e 9 (LottoExpert), cada uma esperando as capturas dos apps (em evolução, D26), e a 10b.
- Tag `v1.0.1` criada e enviada no repositório `eclipse-go` (leve, sobre `f5c1d6b`, com autorização do usuário); é a origem de `atualizadoEm` do EclipseGo em `apps.ts`.
- WP-19 e WP-25 `done`. WP-26 a WP-28 (termos de uso, D28 B). O usuário quer o deploy único **antes do fim de 2026**.

## 2. Quebrado ou pela metade agora

Nada quebrado. Passaram no `/verify` da fatia 5: `test:css`, `check_site.py` (raiz e `dist`), `contrato.sha256`, html-validate, `lighthouse.py` sem `--medir`, `gen_estado --check` e `check_plano`. `lychee` não está instalado localmente; o CI cobre.

**Cuidados:**
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com a própria linha de comando do laço, que não termina. Use `pgrep -f "^python3 tools/lighthouse.py"` ou espere pelo PID.
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- O `--medir` do `lighthouse.py` não confere o orçamento; use a execução sem a flag.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- `tools/sync_legal.py:51` aponta o Pole Position para `pole-position/pole-position-app`, caminho que não existe (`PP-ORIGEM-CAMINHO-01`, roteado ao WP-28).

## 3. O que só o navegador prova (pendente)

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

**Do agente:** PR `feat/wp-10-fatia-6-home` -> integração (o usuário mescla) e seguir para a **fatia 10a**. As fatias 7 a 9 precisam das capturas dos apps (D26).

**Do usuário, em ordem de impacto no prazo:**
1. capturas do app (D26);
2. os textos `TERMS_OF_SERVICE.md` nos repositórios de TopoWalk, EclipseGo e Pole Position;
3. D3 (medição);
4. sessão do WP-20 no Claude Design (imagens 1200x630, o logo, o callout `LEGAL-CALLOUT-SEM-HANDOFF-01`);
5. checklists de navegador das fatias 3, 4, 5 e 6 (seção 3);
6. Safari (pelo iPhone).

## 5. Decisões não registradas

Nenhuma. **Pergunta em aberto ao usuário (`BUILD-RELOGIO-NAO-REPRODUTIVEL-01`, fatia 10a):** a partição D12 usa a data do build; o `dist/` do PR pode diferir do `dist/` do deploy se um corte de 12 meses cair entre os dois. Qual caminho? (b) regra no `check_site.py` que recalcula a partição, confere os `<article>` na ordem e avisa 30 dias antes do corte; (c) build de teste no CI com data fixa (`GHF_HOJE`); ou usar a data do commit em HEAD como "hoje", o que torna o build reprodutível. O primeiro corte real é o do EclipseGo, depois de 2027-07-26.

## 6. Esperando publicação

A modernização inteira (WP-08 a WP-10 e o resto) espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22). Rollback por tag. O WP-10 só fica `done` com a fatia 9; o PR #37 não se mescla até o deploy único.

## 7. Escrituração e branches

- Triagem: vazia. Achados novos da fatia 6 roteados: fatia 10a (`BUILD-RELOGIO-NAO-REPRODUTIVEL-01`, `APPS-ATUALIZADO-EM-SEM-CHECK-01`, `HOME-ORDEM-SEM-CHECK-01`, `ICONES-APPS-DUPLICADOS-01`, `ROTULO-DATA-DUAS-FONTES-01`, `SOBRE-REGIAO-ENGLOBA-PRIVACIDADE-01`, `ORGANIZATION-JSONLD-MINIMO-01`); fatia 10b (`HOME-ICONES-ORFAOS-01`, `CSS-BUNDLE-NOME-FOOTER-01`, `HOME-VOCABULARIO-TECNICO-01`); WP-20 (`LITERAIS-SEM-TOKEN-HOME-01`, `HOME-VER-TODAS-SEM-DESENHO-01`, `HOME-GRADE-3-CARDS-01`, `PRIV-NOME-ACESSIVEL-ORDEM-01`, `HOME-OG-IMAGE-677-01`); WP-18 (`HOME-X-DEFAULT-EN-01`); WP-28 (`CLAUDE-MD-POLE-CAMINHO-01`). `INDEX-LOTTO-DESC-DIVERGE-01` segue aberto para a fatia 9.
- Branches: `develop`, `master`, `feat/wp-08-layout-unico`, `feat/wp-10-redesign`, `feat/wp-10-fatia-5-eclipsego` (integrada pelo #51), `feat/wp-10-fatia-6-home` (não enviada) e `feat/wp-05-ci-no-pr` (não integrada).
