# ADR-008 · O Tailwind é a v4 pelo plugin do Vite, com os tokens do handoff num único arquivo CSS

**Data:** 2026-11-21 · **Estado:** aceita · **Substitui:** ADR-003 · **Origem:** D24 (A)

## Contexto

O ADR-003 fixou o Tailwind 3.4.19 pelo PostCSS para o WP-08 provar "sem mudança visual", e deixou
o v4 para o redesign. O WP-10 reescreve o markup de todas as páginas com os tokens do handoff
(`GHF Kit v3`, D11). O lock do v3 traz 7 avisos do `npm audit` (`TAILWIND3-NPM-AUDIT-01`). Hoje a
cor vive em dois lugares: `tailwind.config.mjs` (`brand.*`) e `src/styles/global.css` (`[data-tema]`).

## Decisão

1. **`tailwindcss` e `@tailwindcss/vite` na v4, versão exata em `devDependencies`**, ligados em
   `astro.config.mjs` (`vite.plugins`). Saem `postcss.config.mjs`, `tailwind.config.mjs`,
   `autoprefixer` e o `postcss` direto: o v4 faz prefixo e minificação pelo Lightning CSS.
2. **Os tokens ficam em `src/styles/tokens.css`, em `@theme`**, e é o único arquivo de `src/` com
   cor literal (critério do WP-10). Entram os tokens do `GHF Kit v3` (inclusive `--border-strong`
   `#66738D`), `--success` e `--success-surface` (D11), `--app-acc`, `--app-acc-edge` e
   `--app-acc-light` por app e os tokens de papel da página legal. A cor de cada app continua por
   atributo no `<html>` (prop do layout, como no ADR-003 §2); o nome do token, não o valor, é o
   que o componente usa.
3. **Fonte das classes explícita.** O CSS importa o Tailwind com `source(none)` e declara
   `@source` só para `src/`. A detecção automática do v4 varre o projeto e leria
   `design/handoff/**/*.html` e o convite em `public/`, e as classes do export entrariam no CSS
   publicado. Continua valendo o ADR-003 §3: classe montada por concatenação de string é proibida;
   o que não puder ser literal vai para `@source inline(...)`, com comentário do porquê.
4. **Piso de navegador: Safari 16.4, Chrome 111, Firefox 128** (D24). `vite.build.cssTarget` em
   `astro.config.mjs` passa a `['chrome111', 'edge111', 'firefox128', 'safari16.4']`. O Safari
   16.4 a 17 ainda exige `-webkit-backdrop-filter`; o alvo explícito mantém o prefixo (mesmo
   motivo do ADR-003 §4). Regressão abaixo do piso não é defeito; acima dele, é achado com o
   navegador nomeado.
5. **Camada de legado até a fatia 10 do WP-10.** Os temas `[data-tema]` e os nomes `brand.*`
   continuam, mapeados em `@theme inline` para as variáveis antigas, para que as páginas ainda não
   redesenhadas montem. A paridade visual dessas páginas **não** é critério: os padrões do v4 mudam
   (cor de borda, largura do `ring`, escalas de `shadow`/`rounded`/`blur`), e nenhuma delas vai
   ao ar antes de ser redesenhada, porque o WP-10 inteiro sai no deploy único (D13). A fatia 10
   remove a camada; o grep de cor literal fica vazio fora de `tokens.css`.
6. **O que não muda.** O convite do bolão tem CSS próprio inline e é copiado byte a byte
   (`tools/contrato.sha256`, D13); não usa este CSS nem este piso. Hotfix de texto legal sai de
   `master`, que segue no Tailwind 3 até o deploy único.

7. **Os polyfills do Tailwind para navegador abaixo do piso saem por um plugin do Vite próprio**
   (`src/styles/sem-polyfill.mjs`, ligado depois do `tailwindcss()` em `vite.plugins`; adendo de
   2026-11-21, fatia 1, `CSS-V4-FALLBACKS-01`).
   - **O que faz:** sobre o CSS de `src/styles/global.css`, antes do minificador, funde cada
     `@supports (color: color-mix(in lab, red, red))` na regra anterior do mesmo seletor e tira o
     `@layer properties { @supports (… margin-trim …) }`. As regras `@property` ficam; nenhuma
     classe sai.
   - **Por quê:** o Tailwind 4.3.5 emite os dois polyfills sempre. O `@tailwindcss/vite` não tem
     opção, e o `@tailwindcss/postcss` fixa `polyfills` em `All` (ou `All ^ AtProperty` para CSS
     module), sem opção do usuário. O Lightning CSS, com `targets` ou `exclude`, transpila para
     baixo e não remove `@supports`. Os polyfills custavam 15 KB de CSS bloqueante e 0,15 s de
     FCP na home. Aceitar e remedir o orçamento troca uma peça de build por desempenho
     permanente, e o piso da D24 já dispensa os dois blocos.
   - **Sinal de quebra:** chave sem par faz o build falhar (`sem-polyfill: chave sem par`). Formato
     novo que o plugin não reconhece vira no-op e o CSS volta a crescer. O orçamento do
     `lighthouse` só pega isso se o FCP passar do limite, então não é guarda suficiente. Fusão
     errada de declarações não quebra o build nem o HTML: só o teste do plugin pega
     (`SEM-POLYFILL-TESTE-01`).
   - **Regra para upgrade do Tailwind:** a versão continua exata (§1). Quem sobe o Tailwind
     regenera a fixture do teste com o CSS cru da versão nova (sem o plugin) e confirma três
     coisas: o teste passa, o CSS publicado não tem nenhum dos dois marcadores, e o tamanho do CSS
     cai como antes. Se o Tailwind passar a oferecer opção para desligar os polyfills, o plugin
     sai no mesmo WP.

## O que isto fecha

O Tailwind 3.4 e a Play CDN. Um `tailwind.config.mjs` como fonte de tema. Cor literal em
componente, página ou `global.css` depois da fatia 10. Navegador abaixo do piso com estilo
completo. Voltar ao v3 custa reescrever as classes renomeadas e o tema em JS, e o piso desce de
novo só por decisão do usuário.

## O que isto mantém aberto

A medição de quantos visitantes ficam abaixo do piso (D3). Plugin ou utilitário próprio em CSS
(`@utility`), se o redesign precisar. Transformar o convite em página gerada com estes tokens, que
é decisão do WP-24 e exige trocar o `contrato.sha256` num `/release` próprio.

## Onde olhar

`src/styles/tokens.css`, `src/styles/global.css`, `astro.config.mjs` (`vite.plugins`,
`cssTarget`), `package.json`, `package-lock.json`, `src/layouts/Base.astro`; D11, D13, D24; WP-10
(fatias 1 e 10); `tools/check_site.py` §15 (desempenho); `tools/orcamento-lighthouse.json`. O
`CLAUDE.md` e o `docs/ARQUITETURA.md` citam `tailwind.config.mjs` como origem do tema e mudam na
fatia 1.
