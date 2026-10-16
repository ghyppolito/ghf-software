// Textos de nav e footer, um bloco por língua de src/i18n/idiomas.json — transportados do dicionário
// JS de index.html (WP-08, fatia 1). Toda chave nova entra em todas as línguas no mesmo commit.
// `Idioma` vem do mapa (idiomas.ts); fica reexportado aqui para os dicionários de src/i18n/.
import type { Idioma } from './idiomas';

export type { Idioma };

export const SITE = 'https://ghfsoftware.com';

export const ui = {
  pt: {
    nav_about: 'Sobre Nós',
    nav_portfolio: 'Portfólio',
    nav_contact: 'Contato',
    footer_desc:
      'Engenharia de software de ponta para aplicações Mobile e Internet das Coisas. Criando o futuro, com performance desde 2004.',
    footer_inst: 'Institucional',
    footer_port: 'Portfólio de Apps',
    footer_cont: 'Contato Profissional',
    footer_apps: 'Aplicativos',
    footer_transp: 'Transparência & Políticas',
    footer_priv_lotto: 'Privacidade - LottoExpert',
    footer_terms_lotto: 'Termos - LottoExpert',
    footer_priv_pole: 'Privacidade - Pole Position',
    footer_priv_topo: 'Privacidade - TopoWalk',
    footer_priv_eclipse: 'Privacidade - EclipseGo',
    footer_rights: 'GHF Software. Todos os direitos reservados.',
    footer_dev: 'Desenvolvido com',
    footer_dev2: 'por especialistas.',
  },
  en: {
    nav_about: 'About Us',
    nav_portfolio: 'Portfolio',
    nav_contact: 'Contact',
    footer_desc:
      'Cutting-edge software engineering for Mobile and IoT applications. Creating the future with performance since 2004.',
    footer_inst: 'Institutional',
    footer_port: 'App Portfolio',
    footer_cont: 'Professional Contact',
    footer_apps: 'Applications',
    footer_transp: 'Transparency & Policies',
    footer_priv_lotto: 'Privacy - LottoExpert',
    footer_terms_lotto: 'Terms - LottoExpert',
    footer_priv_pole: 'Privacy - Pole Position',
    footer_priv_topo: 'Privacy - TopoWalk',
    footer_priv_eclipse: 'Privacy - EclipseGo',
    footer_rights: 'GHF Software. All rights reserved.',
    footer_dev: 'Developed with',
    footer_dev2: 'by experts.',
  },
} as const;

export type ChaveUi = keyof (typeof ui)['pt'];

export function t(lang: Idioma, chave: ChaveUi): string {
  return ui[lang][chave];
}
