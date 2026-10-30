// /sitemap.xml (WP-11, ADR-005 §1–§3). Mesma lista e mesma URL do canonical e do hreflang do
// Base.astro: o mapa de src/i18n/idiomas.json (ADR-007 §2/§4). Uma `<url>` por página e língua, cada
// uma com o hreflang de todas as línguas da página e o x-default (→ en se a página tem en, senão pt;
// D8/D18). Página com uma língua só entra sem hreflang. Fora: a 404 (noindex) e o convite (sem ?d=
// só mostra o erro; com ?d= é bolão privado).
import { SITE } from '../i18n/ui';
import { PAGINAS, hreflang, rota, type Idioma } from '../i18n/idiomas';

export function GET() {
  const url = (l: Idioma, caminho: string) => SITE + rota(l, caminho);
  const urls = Object.entries(PAGINAS).flatMap(([caminho, linguas]) => {
    const padrao: Idioma = linguas.includes('en') ? 'en' : 'pt';
    const alternativas =
      linguas.length > 1
        ? [
            ...linguas.map((l) => `    <xhtml:link rel="alternate" hreflang="${hreflang(l)}" href="${url(l, caminho)}"/>\n`),
            `    <xhtml:link rel="alternate" hreflang="x-default" href="${url(padrao, caminho)}"/>\n`,
          ].join('')
        : '';
    return linguas.map((l) => `  <url>\n    <loc>${url(l, caminho)}</loc>\n` + alternativas + `  </url>`);
  });
  const corpo =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
    urls.join('\n') +
    '\n</urlset>\n';
  return new Response(corpo, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
