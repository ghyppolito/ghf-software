# ADR-007 · pt fica na raiz, as outras línguas ficam em `/<código>/`, e um mapa JSON único diz quais existem, sem redirecionamento

**Data:** 2026-10-16 · **Estado:** aceita · **Complementa:** ADR-001 (URLs contratuais), ADR-002 §2
(`build.format: 'preserve'`, página contratual literal), ADR-004 (espelho legal por commit), ADR-005
(sitemap e hreflang da mesma lista de rotas) · **Depende de:** D8, D18, D23

## Contexto

A D8 publica o TopoWalk em 7 línguas e o Pole Position em 6, e o resto do site em pt/en. Hoje, em
2026-10-16, a lista de páginas com par en vive em dois lugares. Um é `COM_PAR_EN`, em `src/i18n/ui.ts:61`.
O outro é `EN_PENDENTE`/`COM_PAR`/`INDEXAVEIS`, em `tools/check_site.py:130-132,719`. As duas são
mantidas à mão, cada uma espelhando a outra. O `tools/sync_legal.py:239` grava `en: "pendente"`.
Cada `en/<x>.astro` é um arquivo literal, 10 deles. Com 7 línguas, isso daria 4 cópias da mesma lista
e até 60 arquivos por cópia.

## Decisão

1. **Esquema de URL.** O pt fica no caminho de hoje, na raiz, e as URLs de ADR-001 não mudam. As
   outras línguas ficam em `/<código>/<mesmo caminho>`, com o código ISO 639-1 em minúsculas (`en`,
   `es`, `fr`, `it`, `de`, `ru`) e a home em `/<código>/`. **Nunca existe `/pt/`.** Também não há
   redirecionamento de nenhum tipo: nem servidor, nem `<meta refresh>`, nem `location.*` por script.
2. **Fonte única: `src/i18n/idiomas.json`.** É JSON, e não TS, porque três leitores precisam dele:
   o build (TS) e `check_site.py`/`sync_legal.py` (Python, só biblioteca padrão, sem parse de TS por
   regex). O arquivo tem duas partes:
   - `idiomas`: um objeto por língua com `hreflang` (`pt-BR`, `en`, `es`…), `ogLocale` (`pt_BR`,
     `en_US`, `es_ES`, `fr_FR`, `it_IT`, `de_DE`, `ru_RU`), nome nativo, rótulo de data legal e os 12
     meses. Uma língua só entra com todos esses campos, junto com o bloco dela em `src/i18n/ui.ts`,
     no WP que a publica pela primeira vez.
   - `paginas`: o caminho pt de cada página (`"topowalk-privacy.html"`, `"index.html"`) com a lista
     ordenada de línguas, sempre começando por `pt`.

   `src/i18n/idiomas.ts` importa o JSON, valida no build (língua desconhecida, `pt` fora da primeira
   posição ou página sem `.astro` falham) e exporta `Idioma`, `linguasDe()`, `rota()` e `hreflang()`.
   `COM_PAR_EN`, `EN_PENDENTE`, `COM_PAR` e o `INDEXAVEIS` montado à mão deixam de existir. No
   `check_site.py`, `PUBLICADAS` e `CONTRATUAIS` continuam como listas fixas. Elas não repetem o
   mapa, servem de guarda: as chaves de `paginas` mais o convite têm de ser exatamente `PUBLICADAS`.
   Assim, uma página não sai do ar sem nenhum aviso só porque alguém apagou a linha dela no JSON.
3. **Geração no Astro, sem o `i18n` do Astro.** A página pt continua literal em
   `src/pages/<x>.astro` (ADR-002 §2). As outras línguas saem de **uma** rota dinâmica por página,
   `src/pages/[lang]/<x>.astro`. O `getStaticPaths()` dessa rota devolve `linguasDe('<x>')` sem o
   `pt`. As duas cascas renderizam o mesmo componente de página com a prop `lang`. O bloco `i18n` do
   `astro.config.mjs` **não** é usado: o roteamento dele (`prefixDefaultLocale`, `fallback`,
   `redirectToDefaultLocale`) resolve um problema que o mapa já resolve, e o fallback dele gera
   página de outra língua ou redirect, as duas coisas que este ADR proíbe. Página sem a língua no
   mapa não é gerada, e não há fallback silencioso para o pt dentro de `/es/`.
4. **hreflang e x-default.** Página com mais de uma língua declara um `hreflang` por língua do mapa,
   mais `x-default`, recíprocos. O `x-default` aponta para o en quando a página tem en (D8 c1, D18);
   sem en, aponta para o pt. Página com uma língua só não tem `hreflang`, `og:locale:alternate` nem
   seletor. O sitemap (ADR-005) lê o mesmo mapa.
5. **Link para página que não existe na língua atual:** segue a D23.
6. **Âncora das seções legais.** O `id` dos títulos do texto legal vem da posição na hierarquia
   (`secao-2`, `secao-2-1`), não do texto, e é igual em todas as línguas. Pré-condição: a sequência
   de níveis `##`/`###` é idêntica entre o `.pt.md` e cada tradução, e o `check_site.py` cobra isso.
   Os `id`s antigos, como `secao-21-localização-gps`, só existem na integração e nunca foram
   publicados: em `origin/master` não há `id` nos títulos legais (D13). Por isso a troca é livre agora
   e cara depois do deploy único.
7. **Chegada (D8 c1), privacy-first.** Um seletor lista as línguas da página por nome nativo, sem
   bandeira, e cada uma é um `<a hreflang lang>` comum. Uma faixa de sugestão compara a escolha
   gravada, ou `navigator.languages`, com as línguas da página e oferece um link. Ela nunca navega
   sozinha. Os textos da faixa vão no HTML em `<template lang>`, um por língua da página: nada é
   buscado na rede, e sem JS nada aparece. A faixa é `position: fixed` (CLS 0). Duas chaves de
   armazenamento, nenhuma com identificador:
   - `localStorage.ghf_lang`: só o código da língua. É gravado só quando o usuário clica no seletor
     ou no link da faixa, e lido só pela faixa.
   - `sessionStorage.ghf_faixa_idioma = "off"`: a faixa foi fechada nesta sessão.

   Nada sai do navegador, e não há cookie. É uma preferência pedida pelo próprio usuário, e não pede
   consentimento.
8. **Texto legal traduzido** segue a ADR-004. O `.<código>.md` não tem `origemCommit`. No `.pt.md`,
   o marcador `en: "pendente"` vira `pendente: [<códigos>]`, gravado pelo `sync_legal.py` com todas
   as línguas do mapa para a página, menos o `pt`. O `site-legal` tira cada língua da lista quando
   atualiza a tradução dela. Qualquer `pendente` reprova o `check_site.py`.

## O que isto fecha

Ficam fora:
- `/pt/…` e qualquer prefixo para o pt.
- Subdomínio ou `?lang=` por língua.
- Redirecionamento por `Accept-Language` ou por script.
- O roteamento i18n do Astro e o fallback dele.
- Arquivo literal por língua em `src/pages/<código>/`.
- A lista de línguas duplicada em TS e em Python.
- `id` de seção derivado do texto do título.

Voltar atrás tem custo. Depois que uma língua é indexada, mudar o esquema de URL dela exige
redirecionamento, que o App Links não segue (só as URLs pt são contratuais, mas o Google cobra o
mesmo). Trocar o JSON por outra fonte exige mudar os três leitores no mesmo commit.

## O que isto mantém aberto

- Língua nova por página: uma linha em `paginas`, o conteúdo e o bloco em `ui.ts`, sem arquivo novo
  em `src/pages/`.
- LottoExpert e EclipseGo em mais línguas, quando ganharem `values-xx` (D8).
- O visual do seletor com mais de 3 línguas e o da faixa, que são do handoff (D4) e do WP-10.
- Variante regional (`pt-PT`, `es-419`), que exige um código novo no JSON e não muda o esquema.

## Onde olhar

- Mapa e funções: `src/i18n/idiomas.json`, `src/i18n/idiomas.ts`.
- Páginas: `src/pages/[lang]/*.astro`.
- Componentes: `src/components/SeletorIdioma.astro`, `src/components/SugestaoIdioma.astro`.
- Head: `src/layouts/Base.astro`.
- Plugin de títulos: `src/markdown/legal.mjs` (`idDosTitulosLegais`).
- Sitemap: `src/pages/sitemap.xml.ts`.
- Coleção legal: `src/content.config.ts`.
- Verificação: `tools/check_site.py` §4, §7–§10, §12, §14 e §16 (i18n), e `tools/sync_legal.py`.
- WPs: WP-15, WP-16, WP-17 e WP-18.
