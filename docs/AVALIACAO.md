# Avaliação do site ghfsoftware.com — 2026-10-12

Diagnóstico do estado atual e direção recomendada. É a origem do backlog em
`.claude/context/ESTADO.md`; cada recomendação aponta o WP que a executa. Decisões que não são
do agente estão em `.claude/context/decisoes.md`.

## 1. O que existe

| Item | Estado |
|---|---|
| Páginas | 10 HTML na raiz (home, 4 landings, 5 legais) + convite de bolão + `assetlinks.json` |
| Stack | HTML + Tailwind **via CDN** (`cdn.tailwindcss.com`, JIT no navegador) + Font Awesome CDN + Google Fonts |
| Build / teste / CI | nenhum. Jekyll só para incluir `.well-known` |
| Deploy | GitHub Pages da branch `master`; `develop` está **10 commits à frente** (TopoWalk e Pole Position atualizados, não publicados) |
| i18n | pt/en no mesmo HTML, troca por JS (`data-i18n` + `localStorage`); dicionário duplicado por página (26 a 126 chaves) |
| Reuso | nav, footer e `tailwind.config` copiados em cada página — **os 5 navs e os 5 footers das landings já divergem entre si** (hash diferente em todos); 7 variantes de `tailwind.config` |
| Legal | markdown em `docs/` + HTML pt/en; a cópia do LottoExpert está em **23/07/2026**, o app está em **12/10/2026** |
| Acessibilidade | todas as `<img>` têm `alt`; um `<h1>` por página; nada mais verificado |
| SEO | title/description/OG/Twitter presentes; **sem** sitemap, robots, canonical, hreflang, JSON-LD; en sem URL própria |
| Medição | nenhuma |

## 2. Problemas, por impacto

1. **Publicação atrasada.** A política de privacidade e os termos do LottoExpert 2.05.02 (Teimosinha,
   prestação de contas do bolão, espelho premium de 14 dias, restauração sem sobrescrever, Gson,
   "Termos de Uso" no lugar de "Termos de Serviço") não estão no site, e o app em produção aponta
   para `lottoexpert-privacy.html`. Além disso, `develop` tem atualizações de TopoWalk e Pole
   Position que `master` (o que o Pages serve) não tem. → **WP-01, WP-02, WP-03**
2. **OG image do convite de bolão quebrada.** `lottoexpert-invite.html` aponta para
   `https://ghfsoftware.com/logo_transp.png`, que não existe no repositório. Todo convite
   compartilhado no WhatsApp sai sem imagem — é o canal viral do app. → **WP-04**
3. **Sem rede de segurança.** Nada impede link quebrado, data legal divergente, nav diferente
   entre páginas ou copy que viole jogo responsável. → **`tools/check_site.py` (neste setup) + WP-05**
4. **Tailwind pelo CDN em produção.** O próprio Tailwind documenta que o CDN é para
   desenvolvimento: ~300 KB de JS, compila CSS no cliente a cada carga, FOUC, sem purge. É o
   maior custo de performance do site e o motivo de não haver build. → **WP-07**
5. **Duplicação sem fonte única.** Toda mudança de nav/footer/tema é feita 10 vezes à mão e já
   divergiu. O texto legal existe em 3 lugares (repositório do app, `docs/*.md`, HTML pt + en
   inline) e diverge. → **WP-08, WP-09**
6. **i18n invisível para buscadores.** `/en/` não existe como URL; o Google indexa só o
   português e o inglês não tem `hreflang`. → **WP-07 (rotas por idioma), WP-11**
7. **Design sem sistema.** Paleta e tipografia foram decididas inline por geração de código; não
   há tokens, grade, escala de espaçamento ou estados definidos; a home é um "dark tech"
   genérico (emerald/blue/cyan sobre `#0B1120`) sem hierarquia clara entre os 4 produtos.
   → **WP-06 (Claude Design), WP-10**
8. **Sem medição** de visitas, cliques no botão da Play nem origem do tráfego — não dá para
   saber se a landing converte. → **WP-13 (decisão D3)**

## 3. Direção recomendada

### 3.1 Primeiro: publicar o que está pronto (trilha A)

Nada do redesign deve atrasar o LottoExpert 2.05.02. A trilha A roda **na stack atual**, sem
build, com `check_site.py` como única rede: espelhar política e termos, atualizar a landing com
as funcionalidades novas, corrigir a OG do convite e publicar `develop → master`.

### 3.2 Depois: fundação (trilha B)

**Stack com build — recomendação: Astro** (decisão D2). Motivos, em ordem:

- É o padrão de mercado atual para site de conteúdo e landing: zero JS por padrão, HTML
  estático na saída, Lighthouse 100 sem esforço.
- **Markdown nativo** (content collections): o texto legal passa a ser **um** arquivo `.md` por
  idioma, renderizado num layout — some a cópia HTML de 95 KB e o dicionário i18n de 600 linhas.
- **i18n por rota** embutido (`/` e `/en/`), com `hreflang` gerado.
- **Preserva URLs**: `build.format: 'file'` mantém `/lottoexpert-privacy.html` como está, e
  `public/` carrega `.well-known/` e o convite intactos. Isso é o que torna a migração segura.
  *(Revisto no ADR-002, 2026-10-12: `build.format: 'preserve'`, e as páginas atuais são
  copiadas da raiz para `dist/` por integração até o WP-08, em vez de irem para `public/`.)*
- Tailwind como plugin com purge, imagens otimizadas (`<Image>`), sitemap por integração.
- Deploy por GitHub Actions para o Pages (action oficial), com build + `check_site.py` +
  Lighthouse CI no PR.

Alternativas: **Eleventy** (mais simples, menos convenção, i18n e imagens à mão) e **manter
HTML + Tailwind CLI** (resolve só o CDN; não resolve duplicação nem i18n). Next.js/React é
excesso para um site sem interação.

**Legal como fonte única:** o repositório do app é a origem; `tools/sync_legal.py` copia e o CI
acusa divergência. A tradução para o inglês é feita pelo agente e revisada pelo usuário.

### 3.3 Em paralelo: sistema visual no Claude Design (trilha C)

O Claude Design (claude.ai/design) faz sentido aqui pelo mesmo motivo que fez no FORMA: a
decisão visual é do humano, e o export vira a referência que o `site-ux` audita e o `site-dev`
implementa. O agente escreve o **brief** (`design/BRIEF.md`: marca, 4 produtos, hierarquia,
tokens que já existem, o que preservar) e o usuário faz a sessão; o export entra em
`design/handoff/<data>/`. Quando houver uma biblioteca de componentes no código (após o WP-08),
o `/design-sync` pode manter o projeto de design-system sincronizado com ela, um componente de
cada vez.

O que o redesign deve resolver, independente do estilo escolhido:

- **Hierarquia da home:** o visitante chega pelo app (link na Play, no convite, no "Sobre").
  A home precisa levar em um toque ao app certo; hoje os 4 cards têm o mesmo peso e o hero
  fala da empresa, não do que o visitante procura.
- **Uma só anatomia de landing de app:** hero com mockup + botão da Play, 3–5 funcionalidades
  com imagem real, prova (números, avaliações), privacidade em uma frase com link, FAQ, CTA
  final. Hoje cada landing tem estrutura própria.
- **Página legal legível:** largura de leitura (~70 caracteres), sumário lateral, data e
  versão no topo, troca de idioma sem perder a posição.
- **Tokens:** cor semântica (fundo, superfície, texto, primária, por-app), escala tipográfica,
  espaçamento em 4 pt, raio, sombra, foco visível. Contraste AA mínimo.
- **Estados:** app "em breve" vs publicado, página en incompleta, imagem ausente.

### 3.4 Medição

Marca privacy-first pede medição sem cookie: **Plausible ou Umami** (self-host grátis ou ~€9/mês)
não exige banner de consentimento sob LGPD e mede o que importa (visita, origem, clique na
Play). GA4 com Consent Mode é a alternativa se a atribuição com os anúncios dos apps importar
mais que a simplicidade. Decisão D3.

## 4. O que não fazer

- Não migrar a stack antes de publicar a trilha A — o atraso legal é risco de política da Play.
- Não trocar URLs contratuais "porque o framework prefere" — redirect não vale para App Links.
- Não introduzir React/SPA para um site sem estado.
- Não reescrever o texto legal no site — a origem é o repositório do app.
