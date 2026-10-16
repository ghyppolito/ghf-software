# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Sessão de 2026-10-16.** WP-12 (performance), branch `feat/wp-12-performance`, commits 399ce20..0830d4d.

## 1. Onde parei

- **WP-12 `doing`**: implementação, tabela antes/depois (perf 98–99 nas 20 indexáveis, LCP 1,8–2,3 s, CLS 0),
  job `lighthouse` em `pr.yml` e auditoria (`site-qa`, `site-seo-perf`, `site-ux`) concluídos e corrigidos. Detalhe no WP.
- Não é `done` por três coisas do usuário (seção 4). Nada publicado (D13).
- WP-21 e WP-11 `done`. Próximos depois do WP-12: WP-20 (sessão no Claude Design) ou WP-10.

## 2. Quebrado ou pela metade agora

Nada quebrado. Servidores `http.server` locais desta sessão nas portas 8094, 8095 e 8096 podem estar de pé; o usuário
decide se encerra. Capturas antes/depois em
`/tmp/claude-1000/-home-gustavo-hyppolito-GIT-codes-ghf-software/2a605719-7521-4725-bb47-f7ee945cd31f/scratchpad/capturas-wp12/`
são anteriores à correção da caixa dos ícones (0830d4d): nas "depois" os ícones aparecem 4–8 px menores, já corrigido.

## 3. O que só o navegador prova (usuário ainda não reportou)

- **WP-12** (`npm run build && python3 -m http.server 8080 -d dist`): menu do celular hambúrguer↔X a 360; nitidez 2× da logo e
  dos mockups; favicon a 48 px; ícones lado a lado com o antes; dica (tooltip) nos logos de tecnologia; card offline do
  EclipseGo sem ícone. Escrever o resultado no WP.
- **WP-19, rodada 3:** `python3 -m http.server 8080 -d design/handoff/2026-10-13-rodada-3`. `Landing App.dc.html?app=topo&lang=ru`
  a 360; `?app=topo`, `?app=pole`, `?app=eclipse` a 1280; `Home.dc.html`, `Landing App.dc.html` e `Legal LottoExpert.dc.html`
  a 768; troca pt/en na legal (en é stub); `?app=pole&suggest=de` (a faixa fecha e não volta na sessão); Tab com foco
  em "Ver todas" e nos sociais do footer; selo "Publicado" distinto do verde do Pole. Escrever o que viu no WP-19.
- **Convite em tema escuro** (`CONVITE-TEMA-ESCURO-01`, nota, sem WP): convite é URL contratual; o usuário testou e não pediu WP.

**Checklist do deploy único (D13), vindo do WP-11 e do WP-21:** Search Console com o `sitemap.xml` enviado e lido; preview no
WhatsApp de um convite real gerado pelo app e de uma landing, sobre o site no ar; card do WhatsApp/LinkedIn com título em
travessão e descrição curta em `/`, `/en/`, `/lottoexpert.html` e `/en/topowalk.html`.

## 4. Próxima ação

**Do usuário:**
1. WP-12: dar push; conferir o job `lighthouse` verde no PR e provocar o vermelho numa branch descartável (CI); decidir se
   `lighthouse` vira check obrigatório na proteção de branch; rodar o checklist de navegador da seção 3.
2. Levar as branches dos apps para a main de cada um (topo-walk e eclipse-go; o Pole Position com o `/legal poleposition` depois).
3. Checklist de navegador do WP-19.
4. Decidir D11 (`--success`) e D12 (limiares de destaque), só para o WP-10; D3 (medição) bloqueia o WP-13. `PP-NAV-CONTRASTE-01` aguarda decisão.
5. Nos apps (D19): registrar o en do LottoExpert no `ASO_METADATA.md` e criar a ficha do EclipseGo.

**Copy pendente do usuário antes do WP-10:** "chance matemática" -> "probabilidade exata"; texto final do aviso de jogo
responsável (o export traz "Texto provisório"); confirmar "Nada de cadastro, e-mail ou CPF" e "Nenhum SDK de publicidade";
selo "Vantagem Competitiva" da LottoExpert (`LOTTO-COPY-VANTAGEM-01`); qual descrição do LottoExpert fica na home
(`INDEX-LOTTO-DESC-DIVERGE-01`).

## 5. Escrituração e branches

- Triagem: `INVITE-PAKO-CDNJS-01` fica em `triagem` de propósito (convite congelado por D13); destino previsto: `/novo-wp`
  depois do deploy único. `CONVITE-FORA-DO-WP-12-01` vira `resolvido` no fechamento do WP-12.
- **Branches locais já integradas**, candidatas a apagar pelo usuário: `feat/wp-08-f1…` a `f9…` (conferir com
  `git branch --merged`), `docs/publicacao-wp-07`, `docs/publicacao-trilha-a`, `feat/wp-19-rodada-3-claude-design`,
  `feat/wp-01-legal-lottoexpert-2-05-02`, `feat/wp-02-landing-lottoexpert-2-05-02`, `feat/wp-04-og-do-convite-e-poleposition`,
  `feature/invite-bolao`, `main` (órfã, `BRANCH-MAIN-ORFA-01`) e as `docs/…`/`hotfix/…` do Pole Position já mescladas.
  `feat/wp-05-ci-no-pr` não aparece como integrada: conferir antes. Nada foi apagado.
