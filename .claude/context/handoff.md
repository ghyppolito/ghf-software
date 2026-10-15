# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-14 (fim).** Escrito na branch `feat/wp-08-f4-landing-poleposition` (fatia 4 do WP-08, commit
b6e4f5c), ainda não integrada.

## 1. Onde parei

- **Site no ar:** WP-07 publicado em 2026-10-14 por GitHub Actions (Pages `build_type: workflow`,
  `PAGES_VIA_ACTIONS=true`, ambiente `github-pages` só `master`). Bolão testado pelo usuário com link real.
- **Esperando publicação** (`origin/master..origin/develop`): escrituração do WP-07 e os PRs #41 e #42 (mergeados em
  `develop`). Nenhum texto legal, nenhuma página nova. Sem urgência.
- **WP-08** `doing`: fatias 1 a 3 integradas (a 3 em 9b3a0c5, enviada; CI do #37 verde); **fatia 4 (landing
  Pole Position, pt e en) implementada e auditada** na branch acima; aguarda o usuário integrar e o checklist de navegador (seção 3).
- **D13 (deploy único):** nada do WP-08 vai ao ar até o backlog de evolução (WP-08..WP-19) terminar; as releases R1/R2/R3
  deixaram de existir. Antes do deploy: criar a tag `pre-modernizacao` em `master`, adicionar a tag à política do ambiente
  `github-pages` e ensaiar o rollback. Hotfix sai por `master`. `tools/contrato.sha256` roda no CI, no deploy e no `/verify`.
- **WP-19** `blocked`: falta o checklist de navegador da rodada 3 (seção 3).

## 2. Quebrado ou pela metade agora

Nada quebrado no ar. Pela metade:
- **Fatia 4 por integrar:** na integração, `git switch feat/wp-08-layout-unico && git merge --no-ff
  feat/wp-08-f4-landing-poleposition -m "WP-08: fatia 4 — landing Pole Position"`. O agente não tem `git merge`.
- `CONFIG-YML-ORFAO-01`: `_config.yml` já não é lido; sai no WP-08 (fatia 9).

## 3. O que só o navegador prova (usuário ainda não viu)

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
1. Integrar a fatia 4 (seção 2) e rodar os checklists das fatias 2, 3 e 4 (seção 3).
2. Checklist do WP-19; escrever o resultado no WP.
3. Decidir D11 (`--success`) e D12 (limiares de destaque), ambas só para o WP-10; D3 (medição) bloqueia o WP-13.

**Do agente:** fatia 5 do WP-08 (`eclipsego.html`, última landing — fecha o grupo das landings), depois de a fatia 4 estar integrada.

**Copy pendente do usuário antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de
publicidade"; selo "Vantagem Competitiva" da LottoExpert (`LOTTO-COPY-VANTAGEM-01`). Decidir também qual descrição do
LottoExpert fica na home (`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Decisões fora de `decisoes.md` e ADR

- **Exceção de dependência do WP-08 e respostas do usuário ao plano:** no corpo do WP-08 (decisões de execução daquele WP).
- **Fatiamento em 9 fatias e deploy único (D13):** plano do arquiteto, no WP-08; D13 em `decisoes.md`.
- **Texto pt da home vem do dicionário JS** (o que o visitante via, não o HTML estático): vira o achado
  `INDEX-LOTTO-DESC-DIVERGE-01`, roteado ao WP-10.
- `cssTarget` do `astro.config.mjs`: registrado no ADR-003.
- Decisões abertas em `decisoes.md`: D3, D11, D12. D10 resolvida.

## 6. Escrituração e branches

- Triagem de `achados-novos.md`: nenhuma linha em `triagem`; os achados das fatias 2, 3 e 4 têm destino (WP-10, WP-11, WP-12, `aceito`).
- **Branches locais integradas** (`git branch --merged feat/wp-08-layout-unico`), candidatas a apagar pelo usuário:
  `docs/publicacao-wp-07`, `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`,
  `feat/wp-08-f1-infra-e-home` (preservada pelo merge `--no-ff`; a integração ainda não está em `develop`, então vale
  esperar o deploy único se quiser rastro por nome), `feat/wp-01-legal-lottoexpert-2-05-02`,
  `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`, `feature/invite-bolao`, `main`
  (órfã, `BRANCH-MAIN-ORFA-01`). `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
