// Plugin do Vite que tira do CSS do Tailwind 4 os polyfills de navegador abaixo do piso da D24
// (Safari 16.4, Chrome 111, Firefox 128; ADR-008 §4). O Tailwind 4.3 os emite sempre, sem opção
// no `@tailwindcss/vite`, e com eles o CSS cresceu ~20 KB e atrasou o FCP da home (WP-10 fatia 1,
// CSS-V4-FALLBACKS-01). Dois blocos, os dois só têm efeito abaixo do piso:
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

const SUPORTE_COLOR_MIX = /^@supports\s*\(\s*color\s*:\s*color-mix\(\s*in\s+lab\s*,\s*red\s*,\s*red\s*\)\s*\)$/;
const POLYFILL_PROPERTY = /^@supports\b.*margin-trim/s;
// Regra simples no fim do texto já emitido: `seletor{declarações}`, sem chave dentro.
const REGRA_FINAL = /([^{}@;]+)\{([^{}]*)\}$/;
const REGRA_UNICA = /^\s*([^{}@]+)\{([^{}]*)\}\s*$/;

// Índice da `}` que fecha a `{` em `abre`. Ignora chave dentro de string e de comentário.
function fecha(css, abre) {
  let nivel = 0;
  for (let i = abre; i < css.length; i++) {
    const c = css[i];
    if (c === '"' || c === "'") {
      i = css.indexOf(c, i + 1);
      if (i === -1) break;
    } else if (c === '/' && css[i + 1] === '*') {
      i = css.indexOf('*/', i + 2) + 1;
      if (i === 0) break;
    } else if (c === '{') {
      nivel++;
    } else if (c === '}' && --nivel === 0) {
      return i;
    }
  }
  throw new Error('sem-polyfill: chave sem par no CSS do Tailwind');
}

// `a:1;b:2` → [['a','1'],['b','2']]. Valor do Tailwind não tem `;` nem chave.
function declaracoes(texto) {
  return texto
    .split(';')
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
  if (!anterior || !dentro || anterior[1].trim() !== dentro[1].trim()) return saida + corpo;
  const decl = declaracoes(anterior[2]);
  for (const [prop, valor] of declaracoes(dentro[2])) {
    const atual = decl.find(([p]) => p === prop);
    if (!atual) decl.push([prop, valor]);
    else if (/var\(|currentcolor/i.test(atual[1])) atual[1] = valor;
  }
  const regra = `${anterior[1]}{${decl.map(([p, v]) => `${p}:${v}`).join(';')}}`;
  return saida.slice(0, saida.length - anterior[0].length) + regra;
}

export function tiraPolyfills(css) {
  let saida = '';
  let i = 0;
  while (i < css.length) {
    const at = css.indexOf('@', i);
    if (at === -1) break;
    const abre = css.indexOf('{', at);
    const pontoEVirgula = css.indexOf(';', at);
    if (abre === -1 || (pontoEVirgula !== -1 && pontoEVirgula < abre)) {
      // at-rule sem bloco (`@layer a, b;`, `@import`)
      saida += css.slice(i, at + 1);
      i = at + 1;
      continue;
    }
    const cabeca = css.slice(at, abre).trim();
    const fim = fecha(css, abre);
    const corpo = css.slice(abre + 1, fim);
    if (SUPORTE_COLOR_MIX.test(cabeca)) {
      saida = funde(saida + css.slice(i, at), tiraPolyfills(corpo));
    } else if (/^@layer\s+properties$/.test(cabeca) && POLYFILL_PROPERTY.test(corpo.trim())) {
      saida += css.slice(i, at);
    } else if (/^@(media|supports|layer|container)\b/.test(cabeca)) {
      // pode haver polyfill aninhado (variantes `md:` e `hover:`, camadas)
      saida += css.slice(i, abre + 1) + tiraPolyfills(corpo) + '}';
    } else {
      saida += css.slice(i, fim + 1);
    }
    i = fim + 1;
  }
  return saida + css.slice(i);
}

export default function semPolyfill() {
  return {
    name: 'ghf:tailwind-sem-polyfill-abaixo-do-piso',
    transform(codigo, id) {
      if (!/\/src\/styles\/global\.css(\?|$)/.test(id)) return null;
      return { code: tiraPolyfills(codigo), map: null };
    },
  };
}
