// Plugin do Vite que tira do CSS do Tailwind 4 os polyfills de navegador abaixo do piso da D24
// (Safari 16.4, Chrome 111, Firefox 128; ADR-008 §4 e §7). O Tailwind 4.3 os emite sempre, sem
// opção no `@tailwindcss/vite`, e com eles o CSS cresceu ~20 KB e atrasou o FCP da home (WP-10
// fatia 1, CSS-V4-FALLBACKS-01). Dois blocos, os dois só têm efeito abaixo do piso:
//
// 1. Cor com opacidade (`bg-white/5`, `bg-brand-primary/20`) ou de `var()` sai duas vezes: uma
//    reserva em sRGB na regra e a real (`color-mix`) repetida dentro de
//    `@supports (color: color-mix(in lab, red, red)) { mesmo seletor { … } }`. Todo navegador do
//    piso tem `color-mix` (Safari 16.2, Chrome 111, Firefox 113). O plugin funde as duas numa regra:
//    - reserva literal (`#ffffff0d`): o Tailwind já calculou a mesma cor; fica a reserva, que é
//      menor, e o bloco sai;
//    - reserva com `var()` ou `currentcolor` (as cores do legado, `rgb(var(--brand-primary))`, e
//      os aliases `--app-acc`): a reserva é a cor opaca, sem a opacidade; fica o `color-mix`.
//    Quando a regra anterior não é do mesmo seletor, o bloco só perde o invólucro.
// 2. `@layer properties { @supports (… margin-trim … rgb(from …)) { *, … { --tw-…: … } } }`: dá
//    valor inicial às variáveis `--tw-*` em navegador sem `@property` (Safari < 16.4, Firefox <
//    128). O piso tem `@property`, e as regras `@property` ficam.
//
// Roda entre o Tailwind (`enforce: 'pre'`) e o minificador de CSS do Vite (no `vite:css-post`),
// sobre o CSS de src/styles/global.css. Nenhuma classe sai. Abaixo do piso, cor de legado com
// opacidade fica sem cor e sombra/anel composto fica sem valor inicial, o que a D24 aceita.
//
// Teste: tools/test_sem_polyfill.mjs (`npm run test:css`), com a fixture de
// tools/fixtures/sem-polyfill/. Subiu o Tailwind? Regenere a fixture (ADR-008 §7):
//   GHF_SEM_POLYFILL_FIXTURE=tools/fixtures/sem-polyfill npm run build
// grava `entrada.css` (o CSS cru do Tailwind) e `saida.css` (o que este plugin devolve).

import fs from 'node:fs';
import path from 'node:path';

const SUPORTE_COLOR_MIX = /^@supports\s*\(\s*color\s*:\s*color-mix\(\s*in\s+lab\s*,\s*red\s*,\s*red\s*\)\s*\)$/;
const POLYFILL_PROPERTY = /^@supports\b.*margin-trim/s;
// Regra simples no fim do texto já emitido: `seletor{declarações}`, sem chave dentro. Seletor com
// aspas, `@` ou `;` (atributo com string, classe escapada) não casa: o bloco só perde o invólucro.
const REGRA_FINAL = /([^{}@;"']+)\{([^{}]*)\}$/;
const REGRA_UNICA = /^\s*([^{}@;"']+)\{([^{}]*)\}\s*$/;

// Índice da aspa que fecha a string aberta em `i` (aspa escapada com `\` não fecha).
function fimDaString(css, i) {
  const aspa = css[i];
  for (let j = i + 1; j < css.length; j++) {
    if (css[j] === '\\') j++;
    else if (css[j] === aspa) return j;
  }
  throw new Error('sem-polyfill: string sem fim no CSS do Tailwind');
}

// Índice do `*/` (a barra) do comentário aberto em `i`.
function fimDoComentario(css, i) {
  const j = css.indexOf('*/', i + 2);
  if (j === -1) throw new Error('sem-polyfill: comentário sem fim no CSS do Tailwind');
  return j + 1;
}

// Índice da `}` que fecha a `{` em `abre`. Pula string, comentário e caractere escapado (`\{`).
function fecha(css, abre) {
  let nivel = 0;
  for (let i = abre; i < css.length; i++) {
    const c = css[i];
    if (c === '\\') i++;
    else if (c === '"' || c === "'") i = fimDaString(css, i);
    else if (c === '/' && css[i + 1] === '*') i = fimDoComentario(css, i);
    else if (c === '{') nivel++;
    else if (c === '}' && --nivel === 0) return i;
  }
  throw new Error('sem-polyfill: chave sem par no CSS do Tailwind');
}

// Onde termina o prelúdio da at-rule em `at`: índice do primeiro `{`, `;` ou `}` fora de string,
// comentário e parênteses.
function fimDoPreludio(css, at) {
  let parenteses = 0;
  for (let i = at + 1; i < css.length; i++) {
    const c = css[i];
    if (c === '\\') i++;
    else if (c === '"' || c === "'") i = fimDaString(css, i);
    else if (c === '/' && css[i + 1] === '*') i = fimDoComentario(css, i);
    else if (c === '(') parenteses++;
    else if (c === ')') parenteses--;
    else if (parenteses <= 0 && (c === '{' || c === ';' || c === '}')) return i;
  }
  return css.length;
}

// `a:1;b:url("x;y")` → [['a','1'],['b','url("x;y")']]: `;` só separa fora de string e parênteses.
export function declaracoes(texto) {
  const partes = [];
  let parenteses = 0;
  let inicio = 0;
  for (let i = 0; i < texto.length; i++) {
    const c = texto[i];
    if (c === '\\') i++;
    else if (c === '"' || c === "'") i = fimDaString(texto, i);
    else if (c === '(') parenteses++;
    else if (c === ')') parenteses--;
    else if (c === ';' && parenteses === 0) {
      partes.push(texto.slice(inicio, i));
      inicio = i + 1;
    }
  }
  partes.push(texto.slice(inicio));
  return partes
    .map((d) => d.trim())
    .filter(Boolean)
    .map((d) => {
      const p = d.indexOf(':');
      return [d.slice(0, p).trim(), d.slice(p + 1).trim()];
    });
}

// Funde o conteúdo do `@supports (color-mix)` na regra anterior, se for do mesmo seletor.
function funde(saida, corpo) {
  const anterior = saida.match(REGRA_FINAL);
  const dentro = corpo.match(REGRA_UNICA);
  if (!anterior || !dentro) return saida + corpo;
  // Comentário logo antes da regra (`/* … */.a{…}`) não é seletor: fica como prefixo.
  const fimComentario = anterior[1].lastIndexOf('*/') + 2;
  const prefixo = fimComentario >= 2 ? anterior[1].slice(0, fimComentario) : '';
  const seletor = anterior[1].slice(prefixo.length);
  if (seletor.trim() !== dentro[1].trim()) return saida + corpo;
  const decl = declaracoes(anterior[2]);
  for (const [prop, valor] of declaracoes(dentro[2])) {
    const atual = decl.find(([p]) => p === prop);
    if (!atual) decl.push([prop, valor]);
    else if (/var\(|currentcolor/i.test(atual[1])) atual[1] = valor;
  }
  const regra = `${prefixo}${seletor}{${decl.map(([p, v]) => `${p}:${v}`).join(';')}}`;
  return saida.slice(0, saida.length - anterior[0].length) + regra;
}

export function tiraPolyfills(css) {
  let saida = '';
  let copiado = 0; // css[copiado..] ainda não foi para a saída
  for (let i = 0; i < css.length; i++) {
    const c = css[i];
    if (c === '\\') {
      i++; // `\@`, `\{` de classe escapada
      continue;
    }
    if (c === '"' || c === "'") {
      i = fimDaString(css, i);
      continue;
    }
    if (c === '/' && css[i + 1] === '*') {
      i = fimDoComentario(css, i);
      continue;
    }
    if (c !== '@') continue;
    const abre = fimDoPreludio(css, i);
    if (css[abre] !== '{') {
      i = abre; // at-rule sem bloco (`@layer a, b;`, `@import …;`)
      continue;
    }
    const cabeca = css.slice(i, abre).trim();
    const fim = fecha(css, abre);
    const corpo = css.slice(abre + 1, fim);
    const antes = css.slice(copiado, i);
    if (SUPORTE_COLOR_MIX.test(cabeca)) {
      saida = funde(saida + antes, tiraPolyfills(corpo));
    } else if (/^@layer\s+properties$/.test(cabeca) && POLYFILL_PROPERTY.test(corpo.trim())) {
      saida += antes;
    } else if (/^@(media|supports|layer|container)\b/.test(cabeca)) {
      // pode haver polyfill aninhado (variantes `md:` e `hover:`, camadas)
      saida += antes + css.slice(i, abre + 1) + tiraPolyfills(corpo) + '}';
    } else {
      saida += antes + css.slice(i, fim + 1); // @keyframes, @property, @font-face: intactos
    }
    copiado = fim + 1;
    i = fim;
  }
  return saida + css.slice(copiado);
}

export default function semPolyfill() {
  const fixture = process.env.GHF_SEM_POLYFILL_FIXTURE;
  return {
    name: 'ghf:tailwind-sem-polyfill-abaixo-do-piso',
    transform(codigo, id) {
      if (!/\/src\/styles\/global\.css(\?|$)/.test(id)) return null;
      const saida = tiraPolyfills(codigo);
      if (fixture) {
        fs.mkdirSync(fixture, { recursive: true });
        fs.writeFileSync(path.join(fixture, 'entrada.css'), codigo);
        fs.writeFileSync(path.join(fixture, 'saida.css'), saida);
      }
      return { code: saida, map: null };
    },
  };
}
