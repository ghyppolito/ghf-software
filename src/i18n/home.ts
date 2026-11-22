// Textos da home (index.html), pt e en (WP-10, fatia 6; D30). Origem de cada frase (D25):
// - `title`, `description`, `since_2004`, `hero_desc` e `about_p1Html`: o dicionário já publicado,
//   transportado da index.html antiga no WP-08 (fatia 1), sem retradução.
// - `hero_title`: o `hero_titleHtml` publicado sem a marcação (sem o `text-gradient` e o `<br>`; D30 (1)).
// - `apps_titulo`, `atualizado`, `todos_apps` e `sobre_titulo`: `apps`, `updated`, `allApps` e
//   `about` de `content/i18n.js` do handoff (rótulos de interface).
// - `selo_publicado`, `play_curto` e `play_rotulo`: rótulos de `Home.dc.html:30,32,87` ("Publicado",
//   "Play ↗", `{app} na Google Play`); `selo_indisponivel`: o selo do `GHF Kit v3` §6. O export só
//   traz o pt destes quatro: o en ("Published", "Unavailable", "{app} on Google Play") é tradução.
// - `resumos`: tag, texto longo e texto curto de cada app, no formato `ConteudoApp['resumo']`
//   (landing.ts), movidos sem edição das chaves antigas (`tag_*`, `app_*_desc`, `hero_*_desc`).
//   O card usa só `tag` e `curta` (D30 (3)); o `descricao` do LottoExpert é o do dicionário antigo
//   (INDEX-LOTTO-DESC-DIVERGE-01) e a escolha dele fica para a fatia 9. Cada fatia de landing
//   (7, 8, 9) move o objeto para o `<app>.ts` e troca uma linha no Home.astro. O do EclipseGo já
//   está em eclipsego.ts.
// Chaves `*Html` levam marcação e são renderizadas com set:html: `&` escrito `&amp;`.

import type { Idioma } from './ui';

type Resumo = { tag: string; descricao: string; curta: string };

type TextosHome = {
  title: string;
  description: string;
  since_2004: string;
  hero_title: string;
  hero_desc: string;
  apps_titulo: string;
  selo_publicado: string;
  selo_indisponivel: string;
  play_curto: string;
  /** `aria-label` do Play: `{app}` vira o nome do app */
  play_rotulo: string;
  atualizado: string;
  todos_apps: string;
  sobre_titulo: string;
  about_p1Html: string;
  resumos: { lottoexpert: Resumo; topowalk: Resumo; poleposition: Resumo };
};

export const home = {
  pt: {
    // title = h1 e description = footer_desc (ui.ts), nos dois idiomas; o og e o twitter repetem
    // os dois (WP-21, D19).
    title: 'GHF Software — Construímos o futuro da Mobilidade e IoT',
    description:
      'Engenharia de software de ponta para aplicações Mobile e Internet das Coisas. Criando o futuro, com performance desde 2004.',
    since_2004: 'Desde 2004',
    hero_title: 'Construímos o futuro da Mobilidade e IoT',
    hero_desc:
      'Trazer soluções inovadoras com foco em Internet das Coisas e mobilidade para facilitar e empoderar o seu dia a dia.',
    apps_titulo: 'Apps',
    selo_publicado: 'Publicado',
    selo_indisponivel: 'Indisponível',
    play_curto: 'Play',
    play_rotulo: '{app} na Google Play',
    atualizado: 'Última atualização',
    todos_apps: 'Todos os apps GHF',
    sobre_titulo: 'Sobre',
    about_p1Html:
      'A <strong>GHF Software</strong> é impulsionada pela paixão por resolver problemas complexos com soluções elegantes. Nossa empresa foi fundada por um <strong>Arquiteto de Sistemas</strong> com profunda bagagem técnica e experiência em desenvolvimento de software e soluções atuando ativamente <strong>desde 2004</strong>.',
    resumos: {
      lottoexpert: {
        tag: 'Estatística & OCR',
        descricao:
          'Engenharia estatística para loterias com motor combinatório offline, scanner de bilhetes via OCR, gestão de bolões e simulação de ROI histórico.',
        curta: 'Análise matemática e fechamentos offline.',
      },
      topowalk: {
        tag: 'Topografia & SIG',
        descricao:
          'Transforma seu smartphone numa ferramenta topográfica de campo com precisão barométrica. Calcule distâncias, inclinações e desníveis em tempo real, gerando relatórios em PDF 100% offline.',
        curta: 'Levantamento de campo barométrico de bolso.',
      },
      poleposition: {
        tag: 'Kart & Automobilismo',
        descricao:
          'Transforma seu smartphone numa interface de telemetria offline. Com GPS de alta frequência, Força G lateral em tempo real e detecção vetorial de parciais.',
        curta: 'Telemetria de kart e automobilismo real-time.',
      },
    },
  },
  en: {
    title: 'GHF Software — Building the future of Mobility & IoT',
    description:
      'Cutting-edge software engineering for Mobile and IoT applications. Creating the future with performance since 2004.',
    since_2004: 'Since 2004',
    hero_title: 'Building the future of Mobility & IoT',
    hero_desc:
      'Bringing innovative solutions focused on Internet of Things and mobility to empower and simplify your daily routines.',
    apps_titulo: 'Apps',
    selo_publicado: 'Published',
    selo_indisponivel: 'Unavailable',
    play_curto: 'Play',
    play_rotulo: '{app} on Google Play',
    atualizado: 'Last updated',
    todos_apps: 'All GHF apps',
    sobre_titulo: 'About',
    about_p1Html:
      '<strong>GHF Software</strong> is driven by a passion for solving complex mechanics into elegant solutions. Founded by a <strong>Systems Architect</strong> with profound technical background actively operating <strong>since 2004</strong>.',
    resumos: {
      lottoexpert: {
        tag: 'Statistics & OCR',
        descricao:
          'Statistical engineering for lotteries featuring an offline combinatorial engine, OCR ticket scanner, sweepstakes management, and historical ROI simulation.',
        curta: 'Mathematical analysis and offline lotto wheels.',
      },
      topowalk: {
        tag: 'Topography & GIS',
        descricao:
          'Transforms your smartphone into an advanced field topographic tool with barometric precision. Calculate distances, slopes, and elevation on the fly, generating 100% offline PDF reports.',
        curta: 'Pocket barometric field survey tool.',
      },
      poleposition: {
        tag: 'Karting & Motorsport',
        descricao:
          'Transforms your smartphone into an offline telemetry dashboard. Featuring high-frequency GPS, real-time lateral G-force, and rigorous vector split detection.',
        curta: 'Real-time kart and motorsport telemetry.',
      },
    },
  },
} as const satisfies Record<Idioma, TextosHome>;
