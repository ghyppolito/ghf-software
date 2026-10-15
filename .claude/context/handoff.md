# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-15 (fim).** Escrito na branch `feat/wp-08-f8-legal-lottoexpert` (fatia 8 do WP-08), ainda não integrada.

## 1. Onde parei

- **Integração** `feat/wp-08-layout-unico` em 6cff4e6: fatias 1 a 7 mais `origin/develop`, CI verde; #37 fica aberto até o
  deploy único (D13).
- **Fatia 8 pronta** na branch `feat/wp-08-f8-legal-lottoexpert` (1d7d6ba a a917ccb + escrituração), aguarda o usuário
  (seção 2). Política e termos do LottoExpert migrados; raiz sem `*.html`. WP-08 segue `doing`; D-a, D-b, D-c resolvidas no WP-08.
- **D13 em vigor:** deploy único depois de WP-08..WP-19. Antes: tag `pre-modernizacao` em `master`, a tag na política do ambiente
  `github-pages` e ensaio do rollback. `tools/contrato.sha256` roda no CI, no deploy e no `/verify`.
- **Repositórios dos apps, sem merge:** topo-walk `docs/politica-tres-observacoes` (7fc7870); eclipse-go
  `docs/email-suporte-politica` (7f349a2, 4668019; `ECLIPSE-ORIGEM-NAO-MESCLADA-01`, `ECLIPSE-DATA-APOS-EMAIL-01`); pole-position:
  e-mail no commit 00968f5 da `item/PP-144-segunda-sessao-mesma-pista` (outra sessão do usuário); `/legal poleposition` quando a
  PP-144 entrar na main do app (`PP-POLITICA-BRANCH-APP-01`). A branch vazia `docs/politica-email-contato` do pole-position-app
  pode ser apagada. Texto do app PP a decidir lá: 2.1 "o pedido de localização precisa venha junto"; "descrita acima" aponta para a 2.4.
- **WP-19** `blocked`: falta o checklist de navegador da rodada 3 (seção 3).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar. Pela metade:
- **Fatia 8 por integrar:** `git switch feat/wp-08-layout-unico && git merge --no-ff feat/wp-08-f8-legal-lottoexpert -m "WP-08: fatia 8 — política e termos do LottoExpert; fim das páginas copiadas"`.
  O agente não tem `git merge`. Conflito em `achados-novos.md`/`handoff.md`/`ESTADO.md`: manter as linhas dos dois lados.
- `CONFIG-YML-ORFAO-01`: `_config.yml` já não é lido; sai no WP-08 (fatia 9).
- Servidor antigo na porta 8081 (pid 686166), deixado por uma auditoria: o usuário decide se encerra.

## 3. O que só o navegador prova (usuário ainda não reportou)

- **Fatia 8 do WP-08** (`npm run build && python3 -m http.server 8080 -d dist`): `/lottoexpert-privacy.html`, `/lottoexpert-terms.html`
  e as `/en/` a 360, 768 e 1280: política com §2 em destaque de barra violeta e §9.2 sem barra; §4.1 a 4.10 sem marcador; §4.7
  aninhada com bolinha; §5 1ª coluna mono violeta, §9.1 com texto menor; termos §3 em três blocos, o último em destaque com
  Jogadores Anônimos e CVV 188; termos §4 1ª coluna negrito violeta e 2ª branca; §8 com link na mesma aba (en leva a `/en/`);
  slogan em itálico centralizado nas duas; selo escudo/contrato; TopoWalk inalterado; troca de idioma; rodapé en levando a
  `/en/lottoexpert-*`. Escrever o resultado no WP-08.
- **Fatia 7 do WP-08** (`npm run build && python3 -m http.server 8080 -d dist`): `/topowalk-privacy.html`, `/en/topowalk-privacy.html`,
  `/poleposition-privacy.html` e `/en/poleposition-privacy.html` a 360, 768 e 1280: tabelas do Pole Position em cartão e rolagem a
  360; lista aninhada da 2.4 do PP sem marcador e "São durações…" com respiro; "Desenvolvido por" branco semibold; TW com um só
  filete antes da nota LGPD em itálico pequeno; 1ª coluna das tabelas do TW terracota semibold / mono; quebra depois de
  "GHF Software"; links externos em nova aba; selos terracota/lima; Contato no menu mobile; troca pt↔en; "Voltar para a GHF
  Software" leva a `/` ou `/en/`; rodapé en com `/en/…-privacy.html`. Escrever o resultado no WP-08.

- **Fatia 6 do WP-08** (`npm run build && python3 -m http.server 8080 -d dist`): `/eclipsego-privacy.html` e
  `/en/eclipsego-privacy.html` a 360, 768 e 1280: hero (selo, h1 e data uma vez; selo em pt também no en, conhecido), intro com
  filete, tabela de 1 linha com 1ª coluna mono dourada e rolagem a 360, e-mail do §8 clicável sem cor de link, logo que só cresce
  no hover (sem brilho, como antes), pílula Contato dourada com texto preto, rodapé `surface` com "Privacidade - EclipseGo"
  destacada e só o e-mail, troca PT↔EN leva ao par, botão voltar para `/eclipsego.html` / `/en/eclipsego.html`; no en, os links
  do rodapé para as outras 4 políticas abrem em pt (esperado). Escrever o resultado no WP-08.

- **Fatia 5 do WP-08** (`npm run build && python3 -m http.server 8080 -d dist`): `/eclipsego.html` e `/en/eclipsego.html` a 360 e
  1280: moldura do celular pulsando brilho dourado/índigo a cada 4 s; blob dourado parado e centrado; lua do selo pulsando e
  ponto do selo da Play com ping; "Sombra & Luz no seu Bolso" com gradiente dourado→índigo; pílula Contato do menu mobile com
  texto preto e hover dourado mais escuro; troca de idioma leva ao par; "Privacidade" abre a política pt nos dois idiomas;
  card "100% Offline" sem ícone (herdado, `ECLIPSE-ICONE-WIFI-SLASH-01`); a 360, botões empilhados e cards em coluna única sem
  estouro. Escrever o resultado no WP-08.
- **Fatia 4 do WP-08** (`npm run build && python3 -m http.server 8080 -d dist`): `/poleposition.html` e `/en/poleposition.html`
  a 360 e 1280: mockups do hero sobrepostos com moldura e entalhe, hover trazendo cada um à frente; moldura 260×520 a 360
  sem estouro e 320×640 a 768; título com gradiente branco→lima; hero sem animação de entrada (como antes); pílula Contato
  do menu mobile lima com texto preto, hover lima mais claro; rodapé sem filete no topo, 5 ícones (e-mail, YouTube,
  Instagram, TikTok, Facebook) abrindo os destinos certos, Pole Position destacado em lima; tabela comparativa a 360
  (espreme ou rola como na página antiga — comparar com `https://ghfsoftware.com/poleposition.html`, que ainda é a antiga);
  seleção de texto lima com letra preta; troca PT↔EN leva ao par; links en→en na home e nas outras landings en. Escrever
  o resultado no WP-08.
- **Fatia 3 do WP-08** (ainda não reportada; `npm run build && python3 -m http.server 8080 -d dist`): `/topowalk.html` e `/en/topowalk.html` a 360 e
  1280: brilho terracota do hero centrado e parado atrás do conteúdo (como na página antiga); nav com hover terracota,
  pílula Contato e pílula terracota no menu mobile; glow terracota do logo na nav e no rodapé; rodapé em `surface`, TopoWalk
  destacado em terracota com chevron, coração terracota, só o ícone de e-mail; título do hero com "Suas Mãos"/"Your Hands" em
  gradiente âmbar e quebra de linha no desktop; 8 cards, banner Pro e 4 passos; troca de idioma leva ao par; na home `/en/`,
  os links do TopoWalk levam a `/en/topowalk.html`. Escrever o resultado no WP-08.
- **Fatia 2 do WP-08** (ainda não reportada): `npm run build && python3 -m http.server 8080 -d dist`. `/lottoexpert.html` e `/en/lottoexpert.html`
  a 360 e a 1280: hero (gradiente violeta, mockup), 17 cards, cubo girando, hover colorido das 9 loterias, 3 planos com
  "Anual ⭐", tabela de 19 linhas a 360, footer com LottoExpert destacado e favicon; menu mobile; EN/PT leva ao par.
  `ghf_lang`: abrir `/en/lottoexpert.html` direto e depois `/topowalk.html` -> abre em en; abrir `/lottoexpert.html` -> volta
  a pt; `/404.html` não altera. Escrever o resultado no WP-08.
- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota, sem WP): código só tema claro; hipótese de escurecimento
  forçado do navegador; o usuário testou e não pediu WP. Convite é URL contratual.

## 4. Próxima ação

**Do usuário:**
1. Integrar a fatia 8 (seção 2); levar as branches dos apps (seção 1) para a main de cada um.
2. Checklists de navegador das fatias 2 a 8 e do WP-19; escrever o resultado nos WPs.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10; D3 (medição) bloqueia o WP-13.

**Do agente:** push e CI após o merge; **fatia 9**: `public/`, `copiaRaiz` fora, `_config.yml`, as 6 regras do html-validate a `error`,
`TARGET-BLANK-SEM-NOOPENER-01`, docs restantes e os achados de limpeza (`GHF-LANG-SEM-CONSUMIDOR-01`, `CHECK-SITE-RAMOS-DOCS-01`,
`FONTES-LOTTO-SEM-DIST-01`). Mexe em `assets/`/`.well-known/`/convite: contrato byte a byte e `site-arquiteto` obrigatórios.

**Copy pendente do usuário antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade";
selo "Vantagem Competitiva" da LottoExpert (`LOTTO-COPY-VANTAGEM-01`). Decidir também qual descrição do LottoExpert fica na
home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões fora de `decisoes.md` e ADR

- **Opção (A) do texto do EclipseGo** (site segue o `.md` do app) e **check da raiz fora do CI** (veredito do arquiteto): no WP-08.
- **`lastUpdated` string `AAAA-MM[-DD]`** para as fatias 7 e 8: no WP-08 e em `WP09-NOME-ARQUIVO-01`.
- **Fatiamento em 9 fatias e deploy único (D13):** plano do arquiteto, no WP-08; D13 em `decisoes.md`.
- Decisões abertas em `decisoes.md`: D3, D11, D12. D10 resolvida.

## 6. Escrituração e branches

- Triagem de `achados-novos.md`: nenhuma linha em `triagem`; os achados das fatias 6 a 8 têm destino (`WP-08`, `WP-09`, `WP-10`, `WP-11`, `nota`).
- **Branches locais já integradas**, candidatas a apagar pelo usuário: `feat/wp-08-f2…`, `f3…`, `f4…`, `f5…`, `feat/wp-08-f6-legal-eclipsego`, `feat/wp-08-f7-legal-topowalk-poleposition` e, depois do merge, `feat/wp-08-f8-legal-lottoexpert` (fatias integradas;
  `f1-infra-e-home` idem, com a ressalva de que a integração ainda não está em `develop`), `docs/publicacao-wp-07`,
  `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`, `feat/wp-01-legal-lottoexpert-2-05-02`,
  `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`, `feature/invite-bolao`, `main` (órfã,
  `BRANCH-MAIN-ORFA-01`) e as `docs/…`/`hotfix/…` do Pole Position já mescladas (conferir com `git branch --merged`).
  `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
