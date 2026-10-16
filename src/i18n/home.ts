// Textos da home (index.html), pt e en — transportados do dicionário JS da index.html antiga
// (WP-08, fatia 1), sem retradução. Chaves `*Html` levam marcação e são renderizadas com
// set:html: `&` escrito `&amp;`.
//
// O pt é o do dicionário, não o do HTML: o JS da página antiga trocava todo `data-i18n` pelo
// dicionário ao carregar, então é o texto que o visitante via. Só `app_lotto_desc` diferia
// (achado INDEX-LOTTO-DESC-DIVERGE-01).
//
// Rótulos sem `data-i18n` na página antiga (Topografia, Telemetria GPS, Loterias, os selos dos
// cards e os `alt`) apareciam em pt também no modo en; continuam no markup, iguais nos dois
// idiomas (achado HOME-EN-ROTULOS-PT-01).

import type { Idioma } from './ui';

export const home = {
  pt: {
    // title = h1 (hero_titleHtml) e description = footer_desc (ui.ts), nos dois idiomas; o og e o
    // twitter repetem os dois (WP-21, D19).
    title: 'GHF Software — Construímos o futuro da Mobilidade e IoT',
    description:
      'Engenharia de software de ponta para aplicações Mobile e Internet das Coisas. Criando o futuro, com performance desde 2004.',
    hero_badge: 'Elevando o Padrão do Software',
    hero_titleHtml: 'Construímos o futuro da<br class="hidden md:block"> <span class="text-gradient">Mobilidade e IoT</span>',
    hero_desc:
      'Trazer soluções inovadoras com foco em Internet das Coisas e mobilidade para facilitar e empoderar o seu dia a dia.',
    btn_portfolio: 'Ver Portfólio',
    btn_about: 'Conheça a GHF',
    scroll: 'Rolar',
    solid_foundation: 'Fundação Sólida',
    since_2004: 'Desde 2004',
    arch_perf: 'Arquitetura de Alta Performance',
    extreme_scale: 'Escalabilidade Extrema',
    code_quality: 'Qualidade de Código',
    ai_solutions: 'Soluções com Inteligência Artificial',
    stack_title: 'Stack Tecnológico',
    about_badge: 'Nossa Essência',
    about_titleHtml: 'Excelência em <span class="text-gray-300">Engenharia</span>',
    about_p1Html:
      'A <strong>GHF Software</strong> é impulsionada pela paixão por resolver problemas complexos com soluções elegantes. Nossa empresa foi fundada por um <strong>Arquiteto de Sistemas</strong> com profunda bagagem técnica e experiência em desenvolvimento de software e soluções atuando ativamente <strong>desde 2004</strong>.',
    about_p2:
      'Não apenas escrevemos código; nós desenhamos ecossistemas. Nossas aplicações mobile e IoT são construídas sobre pilares rigorosos de engenharia moderna, garantindo que entreguemos performance impecável, tolerância a falhas e escalabilidade contínua.',
    about_quote:
      '"Acreditamos que a tecnologia deve ser invisível, proporcionando ferramentas robustas que elevam a experiência e a eficiência no dia a dia."',
    stat_years_titleHtml: '+22<span class="text-brand-primary"> Anos</span>',
    stat_years_desc: 'De Experiência',
    stat_focus_titleHtml: 'IoT <span class="text-brand-primary">&amp; Mobile</span>',
    stat_focus_desc: 'Foco Principal',
    port_badge: 'Nossos Projetos',
    port_title: 'Soluções no Mercado',
    port_desc:
      'Conheça os aplicativos desenhados e mantidos pela GHF Software, projetados para transformar áreas específicas da sua vida.',
    app_pole_desc:
      'Transforma seu smartphone numa interface de telemetria offline. Com GPS de alta frequência, Força G lateral em tempo real e detecção vetorial de parciais.',
    app_topo_desc:
      'Transforma seu smartphone numa ferramenta topográfica de campo com precisão barométrica. Calcule distâncias, inclinações e desníveis em tempo real, gerando relatórios em PDF 100% offline.',
    app_lotto_desc:
      'Engenharia estatística para loterias com motor combinatório offline, scanner de bilhetes via OCR, gestão de bolões e simulação de ROI histórico.',
    app_eclipse_tag: 'Astronomia & GPS',
    app_eclipse_desc:
      'Cálculo local de visibilidade e linha do tempo de eclipses solares e lunares. Totalmente offline com suporte a GPS e busca por cidades.',
    hero_topo_desc: 'Levantamento de campo barométrico de bolso.',
    hero_lotto_desc: 'Análise matemática e fechamentos offline.',
    hero_pole_desc: 'Telemetria de kart e automobilismo real-time.',
    hero_eclipse_desc: 'Previsão local de eclipses 100% offline.',
    btn_google_play: 'Ver na Google Play',
    btn_app_page: 'PÁGINA DO APP',
    btn_privacy: 'PRIVACIDADE',
    // Rótulos de interface e `alt` dos cards (WP-22): estavam literais em pt no componente e a /en/
    // os mostrava em pt. Os `alt` das capturas que descrevem funcionalidade em vez da imagem ficam
    // literais no Home.astro (achado para o WP-10).
    tag_hero_topo: 'Topografia',
    tag_hero_pole: 'Telemetria GPS',
    tag_hero_lotto: 'Loterias',
    tag_pole: 'Kart & Automobilismo',
    tag_topo: 'Topografia & SIG',
    tag_lotto: 'Estatística & OCR',
    alt_icone_topo: 'Ícone do app TopoWalk',
    alt_icone_eclipse: 'Ícone do app EclipseGo',
    alt_icone_pole: 'Ícone do app Pole Position',
    alt_icone_lotto: 'Ícone do app LottoExpert',
    alt_tela_eclipse: 'Tela do app EclipseGo',
    alt_tela_eclipse_previsao: 'Tela do app EclipseGo mostrando previsão de eclipse solar',
  },
  en: {
    title: 'GHF Software — Building the future of Mobility & IoT',
    description:
      'Cutting-edge software engineering for Mobile and IoT applications. Creating the future with performance since 2004.',
    hero_badge: 'Elevating Software Standards',
    hero_titleHtml: 'Building the future of<br class="hidden md:block"> <span class="text-gradient">Mobility &amp; IoT</span>',
    hero_desc:
      'Bringing innovative solutions focused on Internet of Things and mobility to empower and simplify your daily routines.',
    btn_portfolio: 'View Portfolio',
    btn_about: 'Discover GHF',
    scroll: 'Scroll',
    solid_foundation: 'Solid Foundation',
    since_2004: 'Since 2004',
    arch_perf: 'High-Performance Architecture',
    extreme_scale: 'Extreme Scalability',
    code_quality: 'Code Quality',
    ai_solutions: 'Artificial Intelligence Solutions',
    stack_title: 'Tech Stack',
    about_badge: 'Our Essence',
    about_titleHtml: 'Excellence in <span class="text-gray-300">Engineering</span>',
    about_p1Html:
      '<strong>GHF Software</strong> is driven by a passion for solving complex mechanics into elegant solutions. Founded by a <strong>Systems Architect</strong> with profound technical background actively operating <strong>since 2004</strong>.',
    about_p2:
      "We don't just write code; we design ecosystems. Our mobile and IoT applications are built upon rigorous modern engineering pillars, ensuring flawless performance, fault tolerance, and continuous scalability.",
    about_quote:
      '"We believe technology should be invisible, providing robust tools that elevate experience and daily efficiency."',
    stat_years_titleHtml: '+22<span class="text-brand-primary"> Years</span>',
    stat_years_desc: 'Of Experience',
    stat_focus_titleHtml: 'IoT <span class="text-brand-primary">&amp; Mobile</span>',
    stat_focus_desc: 'Main Focus',
    port_badge: 'Our Projects',
    port_title: 'Market Solutions',
    port_desc:
      'Discover applications designed and maintained by GHF Software, engineered to transform specific areas of your life.',
    app_pole_desc:
      'Transforms your smartphone into an offline telemetry dashboard. Featuring high-frequency GPS, real-time lateral G-force, and rigorous vector split detection.',
    app_topo_desc:
      'Transforms your smartphone into an advanced field topographic tool with barometric precision. Calculate distances, slopes, and elevation on the fly, generating 100% offline PDF reports.',
    app_lotto_desc:
      'Statistical engineering for lotteries featuring an offline combinatorial engine, OCR ticket scanner, sweepstakes management, and historical ROI simulation.',
    app_eclipse_tag: 'Astronomy & GPS',
    app_eclipse_desc:
      'Local calculations of solar and lunar eclipse visibility and timeline. Fully offline with GPS support and city database search.',
    hero_topo_desc: 'Pocket barometric field survey tool.',
    hero_lotto_desc: 'Mathematical analysis and offline lotto wheels.',
    hero_pole_desc: 'Real-time kart and motorsport telemetry.',
    hero_eclipse_desc: '100% offline local eclipse forecasting.',
    btn_google_play: 'Get it on Google Play',
    btn_app_page: 'APP PAGE',
    btn_privacy: 'PRIVACY POLICY',
    tag_hero_topo: 'Topography',
    tag_hero_pole: 'GPS Telemetry',
    tag_hero_lotto: 'Lotteries',
    tag_pole: 'Karting & Motorsport',
    tag_topo: 'Topography & GIS',
    tag_lotto: 'Statistics & OCR',
    alt_icone_topo: 'TopoWalk app icon',
    alt_icone_eclipse: 'EclipseGo app icon',
    alt_icone_pole: 'Pole Position app icon',
    alt_icone_lotto: 'LottoExpert app icon',
    alt_tela_eclipse: 'EclipseGo app screen',
    alt_tela_eclipse_previsao: 'EclipseGo app screen showing a solar eclipse forecast',
  },
} as const satisfies Record<Idioma, Record<string, string>>;
