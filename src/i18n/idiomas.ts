// Línguas do site e em quais delas cada página existe (WP-15, ADR-007). A fonte é
// src/i18n/idiomas.json, lida também por tools/check_site.py e tools/sync_legal.py: aqui ela só é
// validada e tipada. O pt fica na raiz (URLs de ADR-001); as outras línguas, em `/<código>/`.
// Nunca existe `/pt/`, e nada redireciona.
import { existsSync } from 'node:fs';
import path from 'node:path';
import dados from './idiomas.json';

export type Idioma = keyof typeof dados.idiomas;

export interface DadosIdioma {
  /** valor de `hreflang` e de `<html lang>` (`pt-BR`, `en`, `es`…) */
  hreflang: string;
  /** `og:locale` (`pt_BR`, `en_US`…) */
  ogLocale: string;
  /** nome da língua nela mesma (`Português`, `English`) */
  nome: string;
  /** rótulo da data das páginas legais, com a pontuação da língua */
  rotuloData: string;
  /** os 12 meses, de janeiro a dezembro, como escritos na data legal */
  meses: string[];
}

export const IDIOMAS: Record<Idioma, DadosIdioma> = dados.idiomas;
export const CODIGOS = Object.keys(IDIOMAS) as Idioma[];
/** caminho pt da página (`index.html`, `topowalk-privacy.html`) → línguas, a primeira é sempre `pt` */
export const PAGINAS: Record<string, Idioma[]> = dados.paginas as Record<string, Idioma[]>;

// Validação no build: erro aqui para o `npm run build` antes de gerar página errada.
for (const [codigo, d] of Object.entries(IDIOMAS)) {
  for (const campo of ['hreflang', 'ogLocale', 'nome', 'rotuloData'] as const) {
    if (typeof d[campo] !== 'string' || !d[campo]) throw new Error(`idiomas.json: ${codigo} sem \`${campo}\``);
  }
  if (!Array.isArray(d.meses) || d.meses.length !== 12) throw new Error(`idiomas.json: ${codigo} sem os 12 \`meses\``);
}
if (CODIGOS[0] !== 'pt') throw new Error('idiomas.json: `pt` tem de ser a primeira língua de `idiomas`');
for (const [pagina, linguas] of Object.entries(PAGINAS)) {
  if (linguas[0] !== 'pt') throw new Error(`idiomas.json: ${pagina} não começa por \`pt\` (${linguas.join(', ')})`);
  if (new Set(linguas).size !== linguas.length) throw new Error(`idiomas.json: ${pagina} com língua repetida`);
  for (const l of linguas) {
    if (!Object.hasOwn(IDIOMAS, l)) throw new Error(`idiomas.json: ${pagina} com língua desconhecida \`${l}\``);
  }
  // Premissa do Base.astro: o build roda na raiz do repositório (npm run build).
  const fonte = path.resolve(process.cwd(), 'src/pages', pagina.replace(/\.html$/, '.astro'));
  if (!pagina.endsWith('.html') || !existsSync(fonte)) {
    throw new Error(`idiomas.json: ${pagina} sem src/pages/${pagina.replace(/\.html$/, '.astro')}`);
  }
}

/** Línguas em que a página existe; página fora do mapa (a 404) só existe em pt. */
export function linguasDe(caminho: string): Idioma[] {
  return Object.hasOwn(PAGINAS, caminho) ? PAGINAS[caminho] : ['pt'];
}

/** `hreflang` (e `<html lang>`) da língua. */
export function hreflang(lang: Idioma): string {
  return IDIOMAS[lang].hreflang;
}

// Caminho público de uma página do site na língua pedida: pt na raiz, as outras em `/<código>/`.
// `index.html` vira a pasta (`/`, `/en/`), como o og:url que a home já declarava. Página sem a
// língua continua em pt (D23 decide o destino quando houver mais de duas línguas).
export function rota(lang: Idioma, caminho: string): string {
  const destino = linguasDe(caminho).includes(lang) ? lang : 'pt';
  const prefixo = destino === 'pt' ? '/' : `/${destino}/`;
  return caminho === 'index.html' ? prefixo : prefixo + caminho;
}

/** `getStaticPaths()` de `src/pages/[lang]/<x>.astro`: uma rota por língua da página, menos o pt
 *  (que é a página literal na raiz). */
export function rotasDeLingua(caminho: string): { params: { lang: Idioma } }[] {
  return linguasDe(caminho)
    .filter((l) => l !== 'pt')
    .map((lang) => ({ params: { lang } }));
}
