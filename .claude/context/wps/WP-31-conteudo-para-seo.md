---
id: WP-31
titulo: O site tem páginas de conteúdo que trazem busca nova para os apps
area: seo
status: todo
depende_de: []
adr: [ADR-001, ADR-005, ADR-007, ADR-009]
spec: design/REVISAO-VISUAL.md
decisoes: [D25, D34]
tamanho: M
risco: medio
visual: true
branch: feat/wp-31-conteudo-para-seo
---

# WP-31 — O site tem páginas de conteúdo que trazem busca nova para os apps

**Depende de:** — A D34 e o texto correm em paralelo ao WP-30 (§6 item 8: não bloqueia a
revisão). A implementação da página entra depois da fatia 2 do WP-30, para nascer na direção
aprovada e não ser redesenhada. Se a D34 (e) puser este WP depois do deploy único, isso já vale. · **Achados roteados:** `HOME-VOCABULARIO-TECNICO-01` e
`HERO-H1-SEM-PALAVRA-CHAVE-01` ficam no WP-10 (10b). Este WP não os absorve: é sobre página nova,
não sobre o h1 de página existente.

**Objetivo:** de 2 a 4 páginas de conteúdo (ex.: "Fechamento da Lotofácil: como funciona" e "Como
organizar um bolão") publicadas no sitemap. Elas respondem uma busca que hoje não chega ao site e
levam à landing do app, com texto de origem rastreável e sob a régua de jogo responsável.

**Contexto:** o site hoje tem 5 páginas de produto e 10 legais (`src/i18n/idiomas.json`, 10
entradas). Nenhuma responde a uma pergunta de busca: quem não conhece o app não chega. O
`design/REVISAO-VISUAL.md:115-117` separa os dois trabalhos: "a beleza ajuda a converter quem
chega; o conteúdo traz quem ainda não conhece". O usuário confirmou o WP separado e sem bloquear a
revisão (§6 item 8). Já existe material de origem no repositório do app, como
`../lotto-expert/docs/LottoExpertContent.md` §2.2 (gerador e fechamento) e §2.8 (bolão) e
`../lotto-expert/docs/SPEC_desdobramento_fechamento_volante.md`. Esse material foi escrito para
atendimento e especificação, não para página pública. Logo, a adaptação é redação nova (D25), e
nenhum número de "busca nova" foi medido: sem medição (D3 (C)), o efeito só aparece no Search
Console, se o usuário o usar.

**Ler antes:** a D34 decidida, a D25 (alerta do §5 sobre a frase negativa "não aumenta suas
chances"), o ADR-007 §4 (página de língua única não tem `hreflang`), o ADR-005 (sitemap sai da lista
de rotas) e o ADR-009 (JSON-LD só com campo derivado do que a página publica).

**Arquivos-alvo** (fechados depois da D34; hoje são prováveis):
- `src/pages/<slug>.astro` (e `src/pages/[lang]/…` se a D34 (c) pedir en).
- `src/components/paginas/PaginaGuia*.astro` e um layout ou componente de artigo único em
  `src/components/` (ou `src/layouts/`), consumido por todas as páginas de conteúdo, sem copiar
  marcação.
- `src/content/guias/*.md` (se a D34 (b) escolher markdown) ou `src/i18n/guia-*.ts`.
- `src/i18n/idiomas.json`, uma entrada por página, com as línguas da D34 (c).
- Link de entrada: `src/i18n/lottoexpert.ts` (e equivalentes), só a linha que aponta para o guia.
- `tools/orcamento-lighthouse.json`, uma linha por página nova, medida.
- `tools/check_site.py`, só se a página nova precisar de regra (ex.: §5 já cobre a copy; nada
  novo previsto).

**Fora:** URL contratual (ADR-001), `public/` (página não vai para `public/`; o diretório
`/lotto-expert/` é do convite e fica fechado), o convite, texto legal, medição (D3).

**Passos:**
1. Pré-voo: a D34 está decidida? Sem ela, o WP não começa.
2. `site-arquiteto` fecha os arquivos-alvo e a forma da URL (D34 (d)) e confere com o
   `check_site.py` que nenhum caminho novo colide com URL contratual ou com `/lotto-expert/`.
3. Texto: chega do usuário ou é montado só com trechos da fonte, citando `arquivo:linha` (D34 (b)).
   Ele passa no §5 antes de entrar na página. Frase de jogo responsável cuja única fonte dispara o
   §5 é pergunta ao usuário (D25).
4. `site-ux` DESENHAR, se a página pedir componente novo (artigo, passo a passo, tabela de exemplo).
5. `site-dev` → `/verify` → `tools/lighthouse.py` → navegador → commit → auditoria (`site-qa`,
   `site-seo-perf`, `site-ux`).

**Critérios de aceite:**
- `python3 tools/check_site.py` verde, inclusive o §5 sobre o corpo, o `title`, a description e o
  `alt`.
- Cada página nova aparece em `dist/sitemap*.xml` e tem `title`, description, `canonical` e
  `og:*`. O `hreflang` só aparece se a página tiver mais de uma língua (ADR-007 §4).
- Para cada língua listada em `idiomas.json`, a página existe em `dist/`. Língua não listada não
  aparece. `python3 -B -m unittest tools/test_regras_i18n.py tools/test_regras_apps.py` verde.
- `(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)` verde, e as URLs contratuais
  continuam presentes.
- `tools/lighthouse.py` nas páginas novas: desempenho ≥ 95, acessibilidade 100, SEO 100 e LCP < 2,5 s.
- Cada parágrafo tem origem registrada neste WP (`arquivo:linha` da fonte ou "texto do usuário,
  AAAA-MM-DD").
- A página tem link para a landing do app e é alcançável a partir dela (`lychee --offline` verde).

**Só no navegador:** cada página nova a 360 e 1280, em cada língua listada: leitura confortável,
tabela de exemplo sem rolagem horizontal a 360, link para a landing e para a Play. O usuário lê o
texto inteiro e aprova a redação, porque é copy de produto.

**Risco:** médio. Não toca URL contratual nem deploy, mas a URL nova vira pública. Depois de
indexada, mudar a URL custa como mudar qualquer URL (ADR-007, "Voltar atrás tem custo"), e por
isso a forma da URL é decidida antes (D34 (d)). Riscos específicos:
- Copy de loteria que escapa do §5 por paráfrase ("melhore seus resultados").
- Conteúdo traduzido sem origem.
- Página de uma língua só que ganha `hreflang` por engano.
