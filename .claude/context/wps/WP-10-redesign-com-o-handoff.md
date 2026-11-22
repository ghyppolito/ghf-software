---
id: WP-10
titulo: A home e as landings de app seguem o sistema visual do handoff
area: design
status: blocked
depende_de: [WP-06, WP-08]
adr: [ADR-001, ADR-004, ADR-006, ADR-007, ADR-008]
spec: docs/AVALIACAO.md
decisoes: [D4, D11, D12, D24, D25, D26, D27]
tamanho: L
risco: medio
visual: true
branch: feat/wp-10-redesign
---

# WP-10 — A home e as landings de app seguem o sistema visual do handoff

**Depende de:** WP-06 (handoff), WP-08 (componentes únicos) · **Achados roteados:** ECLIPSE-ICONE-OFFLINE-01 (ícone do card "offline" do EclipseGo, D21), NAV-MENU-ALVO-TOQUE-01, HOME-TECH-CURSOR-01, POLE-PRINTS-2X-01 (do WP-12) · landings TopoWalk, Pole Position e EclipseGo esperam o WP-19 (rodada 3)

**Objetivo:** tokens do handoff em `src/styles/tokens.css` (`@theme`, ADR-008); home com hierarquia por app (um
toque até o app certo); as 4 landings com a mesma anatomia (hero + CTA → 3–5 funcionalidades
com imagem real → prova → privacidade em uma frase → FAQ → CTA); página legal legível (largura
de leitura, sumário, data no topo).

**Contexto:** `docs/AVALIACAO.md` §2 item 7 e §3.3.

**Ler antes:** `design/README.md` (mapa do handoff) e só os componentes do handoff que a
página usa; `docs/AVALIACAO.md` §3.3.

**Arquivos-alvo:** fatia 1: `package.json`, `package-lock.json`, `astro.config.mjs`,
`postcss.config.mjs` e `tailwind.config.mjs` (removidos), `src/styles/**`,
`tools/orcamento-lighthouse.json`, e as linhas que citam `tailwind.config.mjs` como origem do tema
(`CLAUDE.md:142`, `docs/ARQUITETURA.md:19`). Todas as fatias: `src/components/**`, `src/layouts/**`,
`src/pages/**` (pt e en), `src/assets/img/**` (imagens novas, pelo `astro:assets`; ADR-006 e
`check_site.py` §13 proíbem imagem exibida em `public/`). O convite fica de fora (ver "Plano").

**Passos:** por página: `site-ux` DESENHAR (referência no handoff, estados) → `site-dev` →
`/verify` → auditoria (`site-ux` AUDITAR + `site-qa` + `site-seo-perf`). Home por último, com
o componente de landing pronto (fatia 5), não depois do WP-19: os cards de TopoWalk, Pole Position
e EclipseGo leem o resumo de cada app da mesma fonte que a landing dele, e mudam sozinhos quando
as fatias 7 a 9 entrarem (ver "Plano").

**Critérios de aceite:**
- Tokens: nenhuma cor literal (`#…`, `rgb(`) em `src/` fora do arquivo único de tokens
  (`grep -rnE "#[0-9a-fA-F]{3,6}\b|rgb\(" src/ | grep -v src/styles/tokens.css` vazio). O
  critério antigo excluía `tailwind.config.mjs`, que fica fora de `src/`, e reprovaria os valores
  de tema que hoje vivem em `src/styles/global.css`.
- Cada landing tem exatamente as seções da anatomia, na ordem (`site-ux` AUDITAR confere
  contra o handoff e lista desvios com justificativa).
- Contraste AA em todo texto (relato do `site-ux` com os pares cor/fundo medidos).
- `check_site.py` verde; Lighthouse Accessibility ≥ 95 em todas as páginas.

**Nota do WP-09 (2026-10-15, `LOTTO-EN-ESPELHO-AUSENTE-01`):** a página legal do redesign consome
`src/content/legal/` (pt copiado do commit do app por `tools/sync_legal.py`, en traduzido; ADR-004),
não o stub legal do export do Claude Design — o export não é origem de texto legal (D7).

**Só no navegador:** todas as páginas, 360/768/1280, pt e en, contra o handoff.

**Risco:** médio — visual. Sem handoff (WP-06 não feito), D4 (B) muda o WP: a referência passa
a ser `docs/AVALIACAO.md` §3.3 e o `site-ux` decide mais do que deveria — registrar.

## Plano (site-arquiteto, 2026-11-21)

**Branch.** `feat/wp-10-redesign` é a integração do WP-10. Ela nasceu de `feat/wp-08-layout-unico`
e volta para ela. Cada fatia nasce dela (`feat/wp-10-fN-<slug>`), passa no `/verify` e volta por
`git merge --no-ff` com a mensagem `WP-10: fatia N — …`, igual ao WP-08. Assim cada fatia é um
merge revertível (`git revert -m 1`). O CI roda pelo PR rascunho #37 da integração (D13), depois
que a integração recebe o merge de `feat/wp-10-redesign`. Para ter CI a cada fatia, abra um PR
rascunho `feat/wp-10-redesign → develop` com o título `[NÃO FAZER MERGE — D13]`.

**Fora do WP-10: o convite** (`CONVITE-REDESIGN-CONTRATO-01`, agora no WP-24). O WP-10 entra no deploy único, e a
D13 congela os bytes do convite até esse deploy (`tools/contrato.sha256`, conferido no `pr.yml` e
no `deploy.yml`). Um convite redesenhado aqui reprova o próprio deploy. O redesenho é o WP-24
(resposta 6, 2026-11-21), que depende do WP-23 e sai num `/release` próprio depois do deploy único,
com o parse de `?d=` intocado, os `og:*` preservados e o teste com link real.

**Fora do WP-10 também:** o card "em breve" (`GHF Kit v3` §5), porque nenhum app está em breve. E o
sinal visual do link de fallback de língua (`LINK-FALLBACK-IDIOMA-SEM-SINAL-01`), porque hoje toda
página tem pt e en e nenhum link cai na D23. O achado foi para o WP-16, o primeiro que publica uma
língua a mais.

**Regra de copy em todas as fatias (D25, resposta 2).** A copy do export é placeholder. Cada frase vem do
dicionário publicado (`src/i18n/*.ts`), do README/ASO do app ou de uma resposta do usuário. Frase
sem origem fica fora da página. Quando a página e a ficha da Play divergem, vale a ficha (D19 a).
Rótulo de interface (sumário, "ver todas", seletor) vem de `content/i18n.js` do export. O en de
cada frase nova é tradução fiel, na mesma fatia (ADR-007). Uma fatia sem en não fecha.
**Alerta:** o §5 do `check_site.py` (`tools/check_site.py:195`) reprova também a negação. "ele não
aumenta suas chances reais de ganhar" (`../lotto-expert/docs/LottoExpertContent.md:389`) tem origem e
reprova a página se copiado literal; o mesmo vale para "doesn't increase your chances" (`:198`). O
padrão não se afrouxa. Se a única fonte da frase dispara o §5, a redação é pergunta ao usuário.
**Imagens (D26, resposta 3):** uma captura real do app por funcionalidade em destaque, 3 a 5 por
landing, fornecida pelo usuário, em `src/assets/img/<app>/`. Sem mockup e sem ilustração do export.
**768 (D27, resposta 4):** home e landing usam o fluido do export; nav e footer, o ramo `t`. A
prova é o checklist de navegador.

### Fatias

1. **Stack e tokens** — **feita em 2026-11-21** (commits c2e2de8, 837d483, ee0ea3e, eb52fbe; o `/verify` e a auditoria de `site-qa`, `site-seo-perf` e `site-ux` passaram; resta o checklist de navegador, que é do usuário). (D24 A, ADR-008, que substitui o ADR-003). O Tailwind 4 entra pelo
   `@tailwindcss/vite`, e os tokens ficam em `@theme`. Os tokens vêm do `GHF Kit v3` (inclusive
   `--border-strong` #66738D) e da D11 (`--success` e `--success-surface`). Também entram
   `--app-acc`, `--app-acc-edge` e `--app-acc-light` por app e os tokens de papel da legal. Tudo
   fica num arquivo só, `src/styles/tokens.css`. Os temas antigos (`[data-tema=…]` em `global.css`)
   ficam como camada de legado até a fatia 10, para que as páginas ainda não redesenhadas
   continuem montando. O `cssTarget` vai ao piso novo (Safari 16.4, Chrome 111, Firefox 128) e o
   `orcamento-lighthouse.json` é remedido. A paridade das páginas ainda não redesenhadas não é
   critério (ADR-008 §5); o build, o `check_site.py --raiz dist` e o html-validate são.
   **Achados:** `TAILWIND3-NPM-AUDIT-01` (`npm audit` sem os 7 avisos), `SUCCESS-DOIS-VALORES-01`,
   `HOME-BOTAO-EMERALD-CONTRASTE-01` (o esmeralda sai do sistema, brief §10).
   **Bloqueio:** nenhum. **Copy:** nenhuma.
2. **Casca: `Base`, `Nav`, `Footer`, `SeletorIdioma`, `SugestaoIdioma` e um `Logo.astro` novo.**
   Ramos 360, 768 e 1280 de `Site Nav` e `Site Footer`. Seletor segmentado PT/EN. Foco visível e
   alvos de 44 px. O logo fica num componente só. Até existir a arte, ele usa o PNG atual. Pela
   WCAG 1.4.3, logotipo não tem exigência de contraste. A troca da arte depois é um arquivo. O
   rodapé não leva "Este site não usa rastreadores nem cookies" (depende da D3) nem "Como tratamos
   dados" (não há página para esse link).
   **Achados:** `SELETOR-2-LINGUAS-FORA-DO-HANDOFF-01`, `LANG-SWITCH-ALVO-01` (resto),
   `ALVOS-DESKTOP-ABAIXO-44-01`, `FOOTER-HOVER-BOLD-01`, `LOTTO-NAV-CONTATO-CONTRASTE-01`,
   `RODAPE-360-ALTO-01` (revisitar), a parte do rodapé de `LOTTO-CONTRASTE-AA-01` e de
   `A11Y-LH-BASELINE-WP12-01` (o `h4` do rodapé).
   **Bloqueio:** nenhum. O 768 de nav e footer está no checklist do WP-19. Se esse checklist achar
   defeito, ele é corrigido nesta fatia. **Copy:** nenhuma.
3. **Legal: `LegalLayout`, 10 páginas.** Papel claro, largura de leitura, sumário (recolhível
   abaixo de 1024 px, lateral a partir de 1024 px) e data no topo. A troca de idioma mantém
   `#secao-N`. O texto vem de `src/content/legal/` e não é tocado. A prova é `sync_legal.py
   --todos --check` igual antes e depois, mais o texto extraído do corpo de cada página legal em
   `dist/` igual antes e depois. A fatia tem `risco: alto`, porque toca 5 URLs contratuais e texto
   legal, e o `site-legal` participa.
   **Achados:** `LEGAL-TABELA-MONO-01`, `TW-CONTRASTE-01`, `LEGAL-LINK-CONTRASTE-01`,
   `LEGAL-LE-SLOGAN-CONTRASTE-01`, `TABELA-LEGAL-ANEL-DISCRETO-01` (revisitar) e a parte legal de
   `A11Y-LH-BASELINE-WP12-01`.
   **Bloqueio:** nenhum. **Copy:** nenhuma. Os rótulos de interface vêm de `content/i18n.js`.
4. **404.** `404.dc.html`, só pt, com o texto atual. **Bloqueio:** nenhum. **Copy:** nenhuma.
5. **Template de landing e LottoExpert.** Os componentes `src/components/landing/*` são os de
   `Landing App.dc.html`: hero, funcionalidades, "ver todas" (D12), prova, planos, privacidade,
   FAQ, CTA e aviso de jogo responsável. O conteúdo de cada app tem um formato só, em
   `src/i18n/<app>.ts`. O link da Play vem de `src/i18n/apps.ts`. Os blocos da D1 (Teimosinha e
   prestação de contas do bolão) ficam.
   **Achados:** `FEATURES-SELO-PREMIUM-01`, `TEIMOSINHA-FORA-DA-TABELA-01` (o limite vem de
   `FreemiumConfig.kt`), `LOTTO-CONTRASTE-AA-01` (violeta), `LOTTO-EN-ROTULOS-PT-01`,
   `LOTTO-COPY-VANTAGEM-01`, `LOTTO-PT-HTML-DIVERGE-01`, `LANDINGS-RESIDUO-RODADA-2-01`, a parte
   LottoExpert de `EXPORT-COPY-SEM-ORIGEM-01` e de `LANDINGS-URL-E-PLAY-01`.
   **Bloqueio para fechar (não para começar):** a copy que falte na fonte (D25) e as capturas
   das funcionalidades destacadas (D26). O repositório só tem o mockup do hero e os logos das loterias.
   Quem desbloqueia: o usuário.
6. **Home.** Os cards seguem a ordem do brief §10 e a regra da D12. A lista "ver todas" fica vazia
   enquanto os 4 apps forem destaque. Cada app em `apps.ts` ganha um campo de data da última
   atualização, com comentário de origem (tag de release no repositório do app).
   **Achados:** `INDEX-LOTTO-DESC-DIVERGE-01`, `HOME-ALT-DESCREVE-FUNCIONALIDADE-01`,
   `HOME-STACK-SELOS-CONTRASTE-01`, `DESTAQUE-LIMIARES-INVENTADOS-01`.
   **Bloqueio:** o texto do card do LottoExpert, se a fonte não tiver (D25). O 768 está decidido
   (D27). Quem desbloqueia: o usuário. O WP-19 não bloqueia a home.
7. **TopoWalk** (pt e en; as outras línguas são do WP-18). **Achados:** `TOPO-PT-HTML-DIVERGE-01`,
   `TOPO-CONTRASTE-AA-01`, a parte TopoWalk de `LANDINGS-URL-E-PLAY-01`. **Bloqueio:** WP-19
   (checklist) e as 4 capturas (D26). Quem desbloqueia: o usuário.
8. **Pole Position.** **Achados:** `POLE-PT-HTML-DIVERGE-01` (vale o que a política do app diz
   sobre o Firebase), `POLE-EN-ROTULOS-PT-01`, `POLE-PRINTS-2X-01`, `POLE-MOCKUP-CURSOR-01`.
   **Bloqueio:** WP-19, 2 capturas (D26) e as capturas em 2× para `POLE-PRINTS-2X-01`. Quem desbloqueia:
   o usuário. O preço e a faixa etária vêm da ficha pública da Play, lidos como na D17, e não
   bloqueiam.
9. **EclipseGo.** **Achados:** `ECLIPSE-ICONE-OFFLINE-01` e `ECLIPSE-ICONE-WIFI-SLASH-01` (o ícone
   de `Landing App?app=eclipse`; ícone de fora do FA entra com a licença ao lado),
   `ECLIPSE-EN-ROTULOS-PT-01`, a parte EclipseGo de `EXPORT-COPY-SEM-ORIGEM-01` ("Sem backend" e
   "Nenhuma chamada de rede" só entram se o README do app disser). **Bloqueio:** WP-19 e 2
   capturas (D26). Quem desbloqueia: o usuário.
10. **Limpeza e aceite.** Saem a camada de legado de `global.css` e os temas `[data-tema]`. O grep
    de tokens fica vazio. Entram a tabela de contraste do `site-ux`, o Lighthouse de
    acessibilidade ≥ 95 e o checklist de navegador (todas as páginas, 360/768/1280, pt e en).

**Ordem.** As fatias 1 a 4 andam sem nenhuma copy nova. A fatia 5 começa com a copy publicada e só
fecha com as respostas. A 6 vem depois da 5. As fatias 7 a 9 esperam o WP-19. A 10 é a última. O
WP-10 só fica `done` com a 9, e o deploy único (D13) espera o WP-10. Logo, o WP-19 segura o deploy
único.

**Logo** (resposta 5 do usuário, 2026-11-21; decisão de execução, sem linha D). O PNG atual
(`GHFSoftware.png`) fica no `Logo.astro` da fatia 2; o agente não faz arte nova. A arte nova clara e escura, com "desde 2004", vai para a sessão do usuário no Claude Design
do WP-20 (D16); `LOGO-ANO-E-FUNDO-ESCURO-01` foi para o WP-20 e não bloqueia o WP-10.

**Respostas do usuário (2026-11-21, "Segue o recomendado").** As seis perguntas do veredito ficam na
opção (A): 1 D24, 2 D25, 3 D26, 4 D27, 5 logo (acima), 6 convite no WP-24.
