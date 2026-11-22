// Teste do plugin src/styles/sem-polyfill.mjs (ADR-008 §7, SEM-POLYFILL-TESTE-01).
// `npm run test:css` (= node --test tools/test_sem_polyfill.mjs); só a biblioteca padrão do Node.
//
// Fixture em tools/fixtures/sem-polyfill/: `entrada.css` é o CSS cru do Tailwind 4.3.5 do build
// atual (o que o plugin recebe) e `saida.css` é o que ele devolve. Subiu o Tailwind ou mudou o CSS
// de src/? Regenere as duas e confira o diff da saída antes de aceitar:
//   GHF_SEM_POLYFILL_FIXTURE=tools/fixtures/sem-polyfill npm run build
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { declaracoes, tiraPolyfills } from '../src/styles/sem-polyfill.mjs';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const ler = (nome) => fs.readFileSync(path.join(aqui, 'fixtures', 'sem-polyfill', nome), 'utf8');
const entrada = ler('entrada.css');
const esperada = ler('saida.css');
const saida = tiraPolyfills(entrada);

const RE_COLOR_MIX = /@supports\s*\(\s*color\s*:\s*color-mix\(\s*in\s+lab/;
const RE_PROPERTIES = /@layer\s+properties\s*\{\s*@supports[^{]*margin-trim/;

// Seletores de regra de estilo (o prelúdio antes de cada `{` que não é at-rule), num CSS sem
// comentário nem chave dentro de string — o do Tailwind minificado.
function seletores(css) {
  const sem = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const achados = new Set();
  for (const m of sem.matchAll(/(?<=^|[{};])\s*([^\s{};@][^{};]*)\{/g)) achados.add(m[1].trim());
  return achados;
}

// O único seletor que sai: o do bloco 2 (valor inicial de `--tw-*`, abaixo do piso).
function seletoresDoPolyfillProperty(css) {
  const m = css.match(/@layer\s+properties\s*\{\s*@supports[^{]*margin-trim[^{]*\{([^{]+)\{/);
  return m ? [m[1].trim()] : [];
}

test('fixture: a saída é a esperada', () => {
  assert.equal(saida, esperada);
});

test('fixture: a entrada tem os dois polyfills (senão o teste não prova nada)', () => {
  assert.match(entrada, RE_COLOR_MIX);
  assert.match(entrada, RE_PROPERTIES);
});

test('fixture: nenhum @supports (color-mix) nem @layer properties com margin-trim resta', () => {
  assert.doesNotMatch(saida, RE_COLOR_MIX);
  assert.doesNotMatch(saida, RE_PROPERTIES);
  assert.doesNotMatch(saida, /margin-trim/);
});

test('fixture: os seletores da entrada são os da saída', () => {
  const removidos = seletoresDoPolyfillProperty(entrada);
  assert.equal(removidos.length, 1);
  const esperados = new Set([...seletores(entrada)].filter((s) => !removidos.includes(s)));
  assert.deepEqual([...seletores(saida)].sort(), [...esperados].sort());
});

test('fixture: as @property ficam, iguais', () => {
  const props = (css) => css.match(/@property\s+[^{]+\{[^}]*\}/g) ?? [];
  assert.ok(props(entrada).length > 0);
  assert.deepEqual(props(saida), props(entrada));
});

test('fixture: o CSS encolhe (plugin que vira no-op aparece aqui)', () => {
  assert.ok(saida.length < entrada.length * 0.9, `${saida.length} de ${entrada.length}`);
});

// ------------------------------------------------------------------ casos sintéticos
const CM = '@supports (color:color-mix(in lab, red, red))';

test('reserva com var(): fica o color-mix', () => {
  assert.equal(
    tiraPolyfills(`.a{color:rgb(var(--x))}${CM}{.a{color:color-mix(in oklab, rgb(var(--x)) 20%, transparent)}}`),
    '.a{color:color-mix(in oklab, rgb(var(--x)) 20%, transparent)}',
  );
});

test('reserva com currentcolor: fica o color-mix', () => {
  assert.equal(
    tiraPolyfills(`::placeholder{color:currentColor}${CM}{::placeholder{color:color-mix(in oklab, currentcolor 50%, transparent)}}`),
    '::placeholder{color:color-mix(in oklab, currentcolor 50%, transparent)}',
  );
});

test('reserva literal: fica a reserva, as outras declarações também', () => {
  assert.equal(
    tiraPolyfills(`.b{padding:0;background-color:#ffffff0d}${CM}{.b{background-color:color-mix(in oklab, var(--color-white) 5%, transparent)}}`),
    '.b{padding:0;background-color:#ffffff0d}',
  );
});

test('declaração que só existe dentro do bloco entra na regra', () => {
  assert.equal(
    tiraPolyfills(`.b{padding:0}${CM}{.b{color:color-mix(in oklab, red 5%, transparent)}}`),
    '.b{padding:0;color:color-mix(in oklab, red 5%, transparent)}',
  );
});

test('regra anterior de outro seletor: só sai o invólucro', () => {
  assert.equal(
    tiraPolyfills(`.a{color:#000}${CM}{.b{color:color-mix(in oklab, var(--x) 5%, transparent)}}`),
    '.a{color:#000}.b{color:color-mix(in oklab, var(--x) 5%, transparent)}',
  );
});

test('bloco aninhado em @media e em @layer', () => {
  assert.equal(
    tiraPolyfills(`@layer utilities{@media (hover:hover){.h:hover{color:rgb(var(--x))}${CM}{.h:hover{color:color-mix(in oklab, rgb(var(--x)) 50%, transparent)}}}}`),
    '@layer utilities{@media (hover:hover){.h:hover{color:color-mix(in oklab, rgb(var(--x)) 50%, transparent)}}}',
  );
});

test('@layer properties com margin-trim sai; outro @layer properties fica', () => {
  const poly = '@layer properties{@supports (((-webkit-hyphens:none)) and (not (margin-trim:block))) or ((-moz-orient:inline) and (not (color:rgb(from red r g b)))){*,:before,:after,::backdrop{--tw-x:0}}}';
  assert.equal(tiraPolyfills(`@layer properties;${poly}.a{color:red}`), '@layer properties;.a{color:red}');
  assert.equal(tiraPolyfills('@layer properties{.a{color:red}}'), '@layer properties{.a{color:red}}');
});

test('@property, @keyframes e @font-face ficam intactos', () => {
  const css = '@property --tw-x{syntax:"*";inherits:false;initial-value:0}@keyframes k{0%{opacity:0}to{opacity:1}}@font-face{font-family:x;src:url(a.woff2)}';
  assert.equal(tiraPolyfills(css), css);
});

test('string com chave e @ não confunde o leitor', () => {
  const css = `.s:after{content:"} @supports {"}.t{color:rgb(var(--x))}${CM}{.t{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}}`;
  assert.equal(
    tiraPolyfills(css),
    '.s:after{content:"} @supports {"}.t{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}',
  );
});

test('string com aspa escapada e chave', () => {
  const css = `.s:after{content:"a\\"}{"}${CM}{.u{color:red}}`;
  assert.equal(tiraPolyfills(css), '.s:after{content:"a\\"}{"}.u{color:red}');
});

test('comentário com chave e @ não confunde o leitor', () => {
  const css = `/* } @supports (color:color-mix(in lab, red, red)) { */.c{color:rgb(var(--x))}${CM}{.c{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}}`;
  assert.equal(
    tiraPolyfills(css),
    '/* } @supports (color:color-mix(in lab, red, red)) { */.c{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}',
  );
});

test('classe escapada com \\@ e \\{ não é at-rule', () => {
  const css = `.\\@md\\:p-4{padding:1rem}.x\\{y{color:rgb(var(--x))}${CM}{.z{color:red}}`;
  assert.equal(tiraPolyfills(css), '.\\@md\\:p-4{padding:1rem}.x\\{y{color:rgb(var(--x))}.z{color:red}');
});

test('chave escapada dentro de bloco aninhado (\\} no seletor)', () => {
  const css = `@media print{.p\\}{color:red}.r{color:rgb(var(--x))}${CM}{.r{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}}}.s{color:red}`;
  assert.equal(
    tiraPolyfills(css),
    '@media print{.p\\}{color:red}.r{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}}.s{color:red}',
  );
  // dentro do próprio bloco: sem pular o `\\}`, o invólucro fecharia no meio do seletor
  assert.equal(tiraPolyfills(`.a{color:red}${CM}{.p\\}{color:red}}`), '.a{color:red}.p\\}{color:red}');
});

test('url("data:…;base64,…") não parte a declaração na fusão', () => {
  const url = 'url("data:image/svg+xml;base64,PHN2Zz4=")';
  assert.deepEqual(declaracoes(`background-image:${url};color:rgb(var(--x))`), [
    ['background-image', url],
    ['color', 'rgb(var(--x))'],
  ]);
  assert.equal(
    tiraPolyfills(`.d{background-image:${url};color:rgb(var(--x))}${CM}{.d{color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}}`),
    `.d{background-image:${url};color:color-mix(in oklab, rgb(var(--x)) 5%, transparent)}`,
  );
});

test('chave sem par faz o build falhar', () => {
  assert.throws(() => tiraPolyfills(`${CM}{.a{color:red}`), /chave sem par/);
});
