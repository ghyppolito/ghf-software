// /sitemap.xml (WP-11, ADR-005 §1–§3). Mesma lista e mesma URL do canonical e do hreflang do
// Base.astro (SITE, rota, COM_PAR_EN): as 20 páginas com par, cada uma com pt-BR, en e x-default
// (→ en, D8/D18). Fora: a 404 (noindex) e o convite (sem ?d= só mostra o erro; com ?d= é bolão
// privado). O WP-15 troca COM_PAR_EN pelo mapa de idiomas aqui e no Base.astro.
import { COM_PAR_EN, SITE, rota, type Idioma } from '../i18n/ui';

export function GET() {
  const url = (l: Idioma, caminho: string) => SITE + rota(l, caminho);
  const urls = [...COM_PAR_EN].flatMap((caminho) =>
    (['pt', 'en'] as const).map(
      (l) =>
        `  <url>\n    <loc>${url(l, caminho)}</loc>\n` +
        `    <xhtml:link rel="alternate" hreflang="pt-BR" href="${url('pt', caminho)}"/>\n` +
        `    <xhtml:link rel="alternate" hreflang="en" href="${url('en', caminho)}"/>\n` +
        `    <xhtml:link rel="alternate" hreflang="x-default" href="${url('en', caminho)}"/>\n  </url>`,
    ),
  );
  const corpo =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
    urls.join('\n') +
    '\n</urlset>\n';
  return new Response(corpo, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
