// /robots.txt (WP-11, ADR-005 §4). Gerado no build, não em public/: o `Sitemap:` sai de SITE, e a
// lista fechada de public/ (§13 do check_site.py) não muda. Sem nenhum `Disallow`: o crawler de
// preview do WhatsApp lê o og do convite, e o Android lê /.well-known/assetlinks.json.
import { SITE } from '../i18n/ui';

export function GET() {
  const corpo = `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`;
  return new Response(corpo, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
