// Textos de nav e footer, um bloco por língua de src/i18n/idiomas.json — transportados do dicionário
// JS de index.html (WP-08, fatia 1). `idioma`, `faixa_idioma`, `faixa_ir` e `fechar` (seletor e
// faixa de sugestão, WP-15) são `language`/`band`/`bandGo`/`close` do handoff `content/i18n.js`,
// sempre na língua do bloco: a faixa fala a língua que sugere. Toda chave nova entra em todas as
// línguas no mesmo commit.
// `Idioma` vem do mapa (idiomas.ts); fica reexportado aqui para os dicionários de src/i18n/.
import type { Idioma } from './idiomas';

export type { Idioma };

export const SITE = 'https://ghfsoftware.com';

/** Anel de foco do teclado (WP-15, WP-22): branco, offset 2, em todos os temas; só `focus-visible:`.
 *  Usado no SeletorIdioma, na Nav e no Footer — classe literal para o Tailwind detectar. */
export const FOCO = 'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white';

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
    idioma: 'Idioma',
    faixa_idioma: 'Esta página também está disponível em português.',
    faixa_ir: 'Ver em português',
    fechar: 'Fechar',
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
