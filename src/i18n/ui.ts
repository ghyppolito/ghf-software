// Textos de nav e footer, um bloco por língua de src/i18n/idiomas.json — transportados do dicionário
// JS de index.html (WP-08, fatia 1). `idioma`, `faixa_idioma`, `faixa_ir` e `fechar` (seletor e
// faixa de sugestão, WP-15) são `language`/`band`/`bandGo`/`close` do handoff `content/i18n.js`,
// sempre na língua do bloco: a faixa fala a língua que sugere. Toda chave nova entra em todas as
// línguas no mesmo commit.
// Casca do WP-10 (fatia 2): `menu`, `footer_app_page`, `footer_privacy` e `footer_terms` são
// `menu`/`appPage`/`privacy`/`terms` de `content/i18n.js`; `nav_principal` é o `aria-label` do
// `<nav>` de `Site Nav.dc.html:36` ("Principal"; en "Main"); `pular` é o link "Pular para o
// conteúdo" (WCAG 2.4.1), que o handoff não tem (resposta 8 do usuário, 2026-11-22).
// Landings do WP-10 (fatia 5): `nav_funcionalidades`, `nav_planos`, `nav_gratis_pro`, `nav_faq` e
// `nav_privacidade` são `features`/`plans`/`freepro`/`faq`/`privacy` de `content/i18n.js`.
// WP-30 (fatia 1, resposta do usuário em 2026-11-24): `nav_portfolio` passa de "Portfólio"/"Portfolio"
// a "Produtos"/"Products", o título da seção de apps da Home; a âncora continua `#portfolio`.
// WP-30 (fatia 2, copy aprovada pelo usuário em 2026-11-24): `footer_desc` = `hero_desc` de home.ts,
// verbatim. `EMAIL_SUPORTE`: o e-mail de contato, um lugar só (footer e CTA final da Home).
// `Idioma` vem do mapa (idiomas.ts); fica reexportado aqui para os dicionários de src/i18n/.
import type { Idioma } from './idiomas';

export type { Idioma };

export const SITE = 'https://ghfsoftware.com';
export const EMAIL_SUPORTE = 'support@ghfsoftware.com';

export const ui = {
  pt: {
    nav_about: 'Sobre Nós',
    nav_portfolio: 'Produtos',
    nav_contact: 'Contato',
    nav_principal: 'Principal',
    nav_funcionalidades: 'Funcionalidades',
    nav_planos: 'Planos',
    nav_gratis_pro: 'Grátis e Pro',
    nav_faq: 'FAQ',
    nav_privacidade: 'Privacidade',
    menu: 'Menu',
    pular: 'Pular para o conteúdo',
    footer_desc:
      'Apps nativos, plataformas em nuvem e IA aplicada, projetados e mantidos pela GHF Software desde 2004.',
    footer_app_page: 'Página do app',
    footer_privacy: 'Privacidade',
    footer_terms: 'Termos de uso',
    footer_rights: 'GHF Software. Todos os direitos reservados.',
    idioma: 'Idioma',
    faixa_idioma: 'Esta página também está disponível em português.',
    faixa_ir: 'Ver em português',
    fechar: 'Fechar',
  },
  en: {
    nav_about: 'About Us',
    nav_portfolio: 'Products',
    nav_contact: 'Contact',
    nav_principal: 'Main',
    nav_funcionalidades: 'Features',
    nav_planos: 'Plans',
    nav_gratis_pro: 'Free & Pro',
    nav_faq: 'FAQ',
    nav_privacidade: 'Privacy',
    menu: 'Menu',
    pular: 'Skip to content',
    footer_desc:
      'Native apps, cloud platforms and applied AI, designed and maintained by GHF Software since 2004.',
    footer_app_page: 'App page',
    footer_privacy: 'Privacy',
    footer_terms: 'Terms of use',
    footer_rights: 'GHF Software. All rights reserved.',
    idioma: 'Language',
    faixa_idioma: 'This page is also available in English.',
    faixa_ir: 'Switch to English',
    fechar: 'Close',
  },
} as const;

export type ChaveUi = keyof (typeof ui)['pt'];

/** Texto de chave montada em tempo de build (`feat${n}_title`): a chave fora do dicionário falha o
 *  build com o nome dela, em vez de sair vazia nas duas línguas (WP-22, `I18N-CHAVE-DINAMICA-01`).
 *  `onde` é o dicionário e a língua, para a mensagem (`topowalk.ts [en]`). */
export function textoDaChave(dicionario: object, chave: string, onde: string): string {
  const valor = (dicionario as Record<string, unknown>)[chave];
  if (valor === undefined) throw new Error(`${onde}: chave \`${chave}\` não existe`);
  return valor as string;
}

export function t(lang: Idioma, chave: ChaveUi): string {
  return ui[lang][chave];
}
