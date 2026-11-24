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
//   O card usa só `tag` e `curta` (D30 (3)). Cada fatia de landing (7, 8, 9) move o objeto para o
//   `<app>.ts` e troca uma linha no Home.astro. O do EclipseGo já está em eclipsego.ts, e o do
//   LottoExpert em lottoexpert.ts (fatia 9, texto mantido por resposta do usuário em 2026-11-24).
// - WP-30, fatia 1 (respostas do usuário em 2026-11-24, D25 e D33): `hero_title` e `hero_desc`
//   novos (o h1 e o subtítulo aprovados; `title` e `description` do <head> não mudam aqui),
//   `apps_titulo` passa a "Produtos"/"Products", `areas_titulo` e `areas` (as três áreas de atuação,
//   com o ícone FA no componente), `cta_produtos` (o CTA primário do hero) e `contato_frase` (a
//   frase do CTA final). `about_leadHtml` + `about_restHtml` são o `about_p1Html` publicado dividido
//   na 1ª frase, verbatim (nenhuma palavra muda; a concatenação com um espaço é o texto antigo).
// Chaves `*Html` levam marcação e são renderizadas com set:html: `&` escrito `&amp;`.

import type { Idioma } from './ui';

type Resumo = { tag: string; descricao: string; curta: string };
type Area = { titulo: string; texto: string };

type TextosHome = {
  title: string;
  description: string;
  since_2004: string;
  hero_title: string;
  hero_desc: string;
  /** CTA primário do hero, para `#portfolio` */
  cta_produtos: string;
  areas_titulo: string;
  /** as três áreas de atuação, na ordem dos ícones de Home.astro */
  areas: readonly [Area, Area, Area];
  /** frase do CTA final (o título é `nav_contact` de ui.ts) */
  contato_frase: string;
  apps_titulo: string;
  selo_publicado: string;
  selo_indisponivel: string;
  play_curto: string;
  /** `aria-label` do Play: `{app}` vira o nome do app */
  play_rotulo: string;
  /** rótulo da data da release do app no card; não é o `rotuloData` de idiomas.json (revisão do documento legal, lido pelo §4) */
  atualizado: string;
  todos_apps: string;
  sobre_titulo: string;
  /** 1ª frase do texto do Sobre (lead) */
  about_leadHtml: string;
  /** o resto do texto do Sobre */
  about_restHtml: string;
  resumos: { topowalk: Resumo; poleposition: Resumo };
};

export const home = {
  pt: {
    // title = h1 e description = footer_desc (ui.ts), nos dois idiomas; o og e o twitter repetem
    // os dois (WP-21, D19).
    title: 'GHF Software — Construímos o futuro da Mobilidade e IoT',
    description:
      'Engenharia de software de ponta para aplicações Mobile e Internet das Coisas. Criando o futuro, com performance desde 2004.',
    since_2004: 'Desde 2004',
    hero_title: 'Engenharia de software, do celular à nuvem.',
    hero_desc:
      'Apps nativos, plataformas em nuvem e IA aplicada, projetados e mantidos pela GHF Software desde 2004.',
    cta_produtos: 'Ver produtos',
    areas_titulo: 'Áreas de atuação',
    areas: [
      { titulo: 'Apps mobile', texto: 'Android nativo com Kotlin e Jetpack Compose; multiplataforma com Flutter.' },
      { titulo: 'Nuvem e SaaS', texto: 'Back-end serverless no Google Cloud e Firebase; plataformas web.' },
      { titulo: 'IA aplicada', texto: 'Modelos Gemini e Claude, agentes, MCP e IA no aparelho, como OCR.' },
    ],
    contato_frase: 'Tem um projeto em mente? Escreva para a GHF Software.',
    apps_titulo: 'Produtos',
    selo_publicado: 'Publicado',
    selo_indisponivel: 'Indisponível',
    play_curto: 'Play',
    play_rotulo: '{app} na Google Play',
    atualizado: 'Última atualização',
    todos_apps: 'Todos os apps GHF',
    sobre_titulo: 'Sobre',
    about_leadHtml:
      'A <strong>GHF Software</strong> é impulsionada pela paixão por resolver problemas complexos com soluções elegantes.',
    about_restHtml:
      'Nossa empresa foi fundada por um <strong>Arquiteto de Sistemas</strong> com profunda bagagem técnica e experiência em desenvolvimento de software e soluções atuando ativamente <strong>desde 2004</strong>.',
    resumos: {
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
    hero_title: 'Software engineering, from the phone to the cloud.',
    hero_desc:
      'Native apps, cloud platforms and applied AI, designed and maintained by GHF Software since 2004.',
    cta_produtos: 'See products',
    areas_titulo: 'Areas of expertise',
    areas: [
      { titulo: 'Mobile apps', texto: 'Native Android with Kotlin and Jetpack Compose; cross-platform with Flutter.' },
      { titulo: 'Cloud and SaaS', texto: 'Serverless back-end on Google Cloud and Firebase; web platforms.' },
      { titulo: 'Applied AI', texto: 'Gemini and Claude models, agents, MCP and on-device AI, such as OCR.' },
    ],
    contato_frase: 'Have a project in mind? Write to GHF Software.',
    apps_titulo: 'Products',
    selo_publicado: 'Published',
    selo_indisponivel: 'Unavailable',
    play_curto: 'Play',
    play_rotulo: '{app} on Google Play',
    atualizado: 'Last updated',
    todos_apps: 'All GHF apps',
    sobre_titulo: 'About',
    about_leadHtml:
      '<strong>GHF Software</strong> is driven by a passion for solving complex mechanics into elegant solutions.',
    about_restHtml:
      'Founded by a <strong>Systems Architect</strong> with profound technical background actively operating <strong>since 2004</strong>.',
    resumos: {
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
