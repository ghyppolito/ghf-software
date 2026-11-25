# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-11-24/25.** A integração `feat/wp-08-layout-unico` está em cd38d02 (merge do #59), CI verde. O PR #37 (integração → `develop`) segue aberto e **não se mescla antes do deploy único** (D13).

## 1. Onde parei

- Mesclados pelo usuário na integração: #54/#55 (WP-30 revisão visual, WP-10 fatia 9 parcial, WP-27/29/31/32 escritos), #58 (WP-10 fatias 7–8, WP-26, WP-27; reparo, porque #56/#57 tinham sido mesclados em branches empilhadas), #59 (WP-28).
- `done` nesta sessão: WP-30 (direção em `design/REVISAO-VISUAL.md` §7), WP-26 (termos e política do TopoWalk, ADR-010), WP-27 (termos do EclipseGo, `origemCommit` reancorado), WP-28 (termos do Pole Position, origem `../pole-position-app`). Escritos, `todo`: WP-29 (prévia do convite, D32), WP-31 (conteúdo SEO, D34), WP-32 (lab Lighthouse com gzip, emenda da D20).
- **WP-10 `blocked`.** Fatias 1–8 e 10a entregues; **fatia 9 (LottoExpert) parcial**; 10b não começou.
- **Próximo:** fila do `gen_estado.py`: WP-10 → WP-32 → …; WP-31 e WP-29 só depois do deploy único.

## 2. Quebrado ou pela metade agora

Fatia 9 do WP-10 sem duas capturas:
- **scanner:** o usuário, no celular, com bilhete real; o agente recorta só a barra de status.
- **prestação de contas:** o agente, no emulador do LottoExpert (`scripts/emulador.sh` em `../lotto-expert`, AVD `lotto-api34`, porta 5580). O bolão de exemplo "Turma do Trabalho" foi lacrado no concurso 3090 da Mega-Sena, já sorteado: abrir o app, deixar sincronizar o resultado e capturar o card.

Faltam também a 10b e o `apps.ts` com a 2.06.00 (o §21 avisa "tag v2.06.00 depois de v2.05.03"), quando a versão sair na Play. Ajuste futuro, sem WP: traçado do Pole com o contorno de Interlagos (`POLE-TRACADO-INTERLAGOS-01`; emulador `pole-play34`, imagem Google Play, porta 5584, criado e desligado).

Ambiente: nenhum emulador ligado; o servidor `python3 -m http.server 8080 -d dist` pode estar rodando; APKs debug da master em `scratchpad/apks` (temporários). `lychee` não está instalado localmente (o CI cobre).

**Cuidados:**
- O merge local é barrado pela permissão: o agente abre o PR e o usuário mescla no GitHub.
- Um PR por branch empilhada causou o #58 de reparo. Daqui em diante, PR direto para a integração.
- Não rode `npm ci` em worktree com `node_modules` em symlink: esvazia o `node_modules` principal.
- Num laço `until ! pgrep -f "tools/lighthouse.py"`, o `pgrep` casa com o próprio laço; use `^python3 tools/lighthouse.py`. O `--medir` não confere o orçamento.

## 3. O que só o navegador prova (pendente)

O usuário aprovou o visual de Home, landings e legais, mas **não reportou** o que segue. `python3 -m http.server 8080 -d dist`.

**WP-30:**
- foco por Tab nas 4 cores de acento (Home, landings, legais);
- Ctrl+P de uma legal;
- hover do sumário das legais;
- `prefers-reduced-motion`: nada anima;
- Safari e Firefox (sem `animation-timeline`): conteúdo parado, visível.

**Páginas novas (WP-26 a 28):** `/topowalk-terms.html`, `/eclipsego-terms.html`, `/poleposition-terms.html` (pt e `/en/`); `/topowalk-privacy.html` (16 seções); `/en/poleposition-privacy.html` seção 2. Landings `/topowalk.html` e `/poleposition.html` a 360, 768 e 1280.

**Fatia 9 (LottoExpert):** `/lottoexpert.html` e `/en/`, a 360/768/1280: recorte do hero, CTA da Play acima da dobra a 1280×720, destaques sem imagem onde faltam as capturas, tabela a 360 rolando com foco, selo 18, aviso de jogo responsável, FAQ, contraste do violeta.

**Fatias 3, 4, 5, 6 e 10a do WP-10:** os checklists continuam pendentes e estão nos blocos "Estado" de `wps/WP-10-*.md`. Resumo: legais (sumário, tabela, caixas, troca de idioma, impressão), 404, FAQ do EclipseGo ("+"/"−"), Home (grade 2x2 a 1024, card clicável, Tab) e Rich Results Test em `/` e `/eclipsego.html`. Safari pelo iPhone (`-b 0.0.0.0`).

Herdados: seletor com 3+ línguas (WP-16); Search Console, preview no WhatsApp e cards de compartilhamento no deploy único (WP-11, WP-21); 404 em `/x/y` só no Pages; WP-23 depois do deploy.

## 4. Próxima ação

**Do agente:** com o scanner entregue, recortar a barra de status; capturar a prestação de contas no `emulator-5580`; fechar a fatia 9 (também `CAPTURAS-BARRA-GESTOS-01`); depois a 10b e o WP-32. `apps.ts` com a 2.06.00 só quando a versão sair na Play.

**Do usuário, em ordem de impacto no prazo:**
1. captura do scanner no celular, com bilhete real;
2. 2.06.00 na produção da Play (libera o deploy único);
3. correções nos apps (achados `nota`): TopoWalk (furos de camada no mapa, nome da exclusão, PDF com título colado, strings `help_a1`/`help_a15`, termos sem data nova); Pole (Maps legacy http, rótulos mistos, pista aberta, título da análise, política sem data nova, nome "Hyppolito" sem acento nos termos: corrigido no app, roda-se `/legal poleposition` de novo);
4. checklists de navegador da seção 3;
5. sessão do WP-20 no Claude Design;
6. apagar as branches remotas já mescladas: `feat/wp-30-revisao-visual`, `feat/wp-26-termos-topowalk`, `feat/wp-27-termos-eclipsego`, `feat/wp-28-termos-poleposition`; locais: `feat/wp-10-fatia-9-lottoexpert`, `docs/wp-27-ampliado-wp-29-respostas-fatia-9`.

**Depois do deploy:** cadastrar as URLs dos termos (TopoWalk, EclipseGo, Pole Position) na ficha da Play (pergunta 8 dos WPs 26–28).

## 5. Decisões não registradas

- Ordem WP-10 antes do WP-32: está só na `SEQUENCIA` do `gen_estado.py`; nenhum registro em `decisoes.md`.
- PR direto para a integração, sem branches empilhadas (ver seção 2): regra de processo sem registro.
- O usuário prefere decisões em questionário com a recomendação primeiro.

Registradas nesta sessão: D32, D33, D34, nota na D13 (deploy único só depois da 2.06.00 do LottoExpert na Play), ADR-010.

## 6. Esperando publicação

`git log origin/master..origin/develop` (após `git fetch`): 4 commits (04f8639, 400d254, 09967ab, 44e95af), só documentação, **sem texto legal**, sem urgência. A integração tem 264 commits à frente de `develop`, e tudo isso espera o deploy único (D13, `/release`; `lighthouse` obrigatório em `master`, D22; rollback por tag). Ele espera: a 2.06.00 do LottoExpert na Play, a fatia 9 e a 10b do WP-10, e o WP-32 (ou decisão do usuário de subir sem ele). O WP-10 só fica `done` com a 10b.

## 7. Escrituração

Triagem de `achados-novos.md`: vazia, e nenhum achado está roteado a WP `done` (conferido por script em 2026-11-25). Novo da sessão: `POLE-TERMOS-NOME-ACENTO-01` (`nota`, usuário corrige no app). Os achados do TopoWalk e do Pole listados na seção 4 estão como `nota` em `achados-novos.md`.
