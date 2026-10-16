// Textos da landing do EclipseGo (eclipsego.html), pt e en — transportados do dicionário JS da
// eclipsego.html antiga (WP-08, fatia 5), sem retradução.
//
// O pt é o do dicionário: o JS da página antiga trocava todo `data-i18n` pelo dicionário ao
// carregar, então é o texto que o visitante via. Nesta página o HTML estático e o dicionário pt
// coincidiam.
//
// O `alt` do print do app não tinha `data-i18n`: o visitante via pt nos dois idiomas, e o en abaixo
// repete o pt (achado ECLIPSE-EN-ROTULOS-PT-01).
//
// O EclipseGo não tem ficha da Play no repositório do app: o `title` (que o og e o twitter
// repetem) é o `hero_badge` publicado, e a `description` é o "Resumo em uma frase" de
// ../eclipse-go/docs/EclipseGoContent.md, com tradução para o en (WP-21, D19).

import type { Idioma } from './ui';

export const eclipsego = {
  pt: {
    title: 'EclipseGo: Previsão de Eclipses Offline — GHF Software',
    description:
      'Descubra se e quando você vai poder ver o próximo eclipse solar ou lunar, sem precisar de internet.',

    hero_badge: 'Previsão de Eclipses Offline',
    hero_title_1: 'EclipseGo',
    hero_title_2: 'Sombra & Luz no seu Bolso',
    hero_desc:
      'Saiba exatamente se um eclipse solar ou lunar é visível de onde você está. Um aplicativo totalmente offline que calcula horários locais de início, pico e fim sem fazer qualquer chamada de rede.',
    btn_play: 'Baixar na Google Play',
    badge_available: 'Disponível na Google Play',
    btn_privacy: 'Privacidade',
    alt_screen: 'Tela real do aplicativo EclipseGo',

    features_badge: 'Recursos Offline',
    features_title: 'Astronomia de Bolso Sem Conexão',
    features_subtitle:
      'Tecnologia de ponta e matemática astronômica local para prever eclipses a qualquer momento.',
    feat1_title: '100% Offline',
    feat1_desc:
      'Todos os cálculos e a base de dados de mais de 34 mil cidades estão embutidos. Funciona perfeitamente no meio do deserto ou em alto mar.',
    feat2_title: 'Modos de Localização',
    feat2_desc:
      'Minha localização (GPS), busca por cidade ou a ferramenta exclusiva que localiza o ponto de melhor visibilidade mais próximo de você.',
    feat3_title: 'Linha do Tempo do Evento',
    feat3_desc:
      'Gráfico interativo e slider que demonstram o progresso exato da cobertura (início → pico → fim) no fuso horário local.',
    feat4_title: 'Calendário Completo',
    feat4_desc:
      'Acesse o histórico e as datas futuras de eclipses solares e lunares com mecanismos rápidos de busca e filtragem.',

    workflow_badge: 'Fluxo de Uso',
    workflow_title: 'Como Funciona o EclipseGo',
    step1_title: 'Selecionar Localização',
    step1_desc:
      'Use o GPS atual, busque uma cidade na base de dados Room offline ou peça para encontrar a melhor visibilidade próxima.',
    step2_title: 'Calcular Visibilidade',
    step2_desc:
      'O motor matemático avalia as circunstâncias locais de visibilidade do eclipse selecionado para as coordenadas.',
    step3_title: 'Simular Linha do Tempo',
    step3_desc:
      'Use o slider interativo para ver a cobertura em cada horário e planeje sua observação com antecedência.',
    step4_title: 'Acompanhar Offline',
    step4_desc:
      'Consulte todos os dados de início, pico e fim em campo, sem precisar de internet ou sinal de celular.',

    tech_badge: 'Stack de Tecnologia',
    tech_title: 'Arquitetura Nativa e Livre de Rede',
    tech_subtitle:
      'Desenvolvido com tecnologias modernas do ecossistema Android para máxima eficiência.',
  },
  en: {
    title: 'EclipseGo: Offline Eclipse Prediction — GHF Software',
    description:
      'Find out if and when you will be able to see the next solar or lunar eclipse, no internet needed.',

    hero_badge: 'Offline Eclipse Prediction',
    hero_title_1: 'EclipseGo',
    hero_title_2: 'Shadow & Light in Your Pocket',
    hero_desc:
      'Know exactly if a solar or lunar eclipse is visible from your location. A fully offline application that calculates local start, peak, and end times without making any network calls.',
    btn_play: 'Get it on Google Play',
    badge_available: 'Available on Google Play',
    btn_privacy: 'Privacy Policy',
    alt_screen: 'Tela real do aplicativo EclipseGo',

    features_badge: 'Offline Features',
    features_title: 'Pocket Astronomy Without Connection',
    features_subtitle:
      'State-of-the-art technology and local astronomical mathematics to predict eclipses anytime, anywhere.',
    feat1_title: '100% Offline',
    feat1_desc:
      'All calculations and a database of over 34,000 cities are built-in. Works perfectly in the middle of a desert or in the high seas.',
    feat2_title: 'Location Modes',
    feat2_desc:
      'My location (GPS), city search, or the exclusive tool that finds the nearest location with the best visibility.',
    feat3_title: 'Event Timeline',
    feat3_desc:
      'Interactive graphic and slider showing the exact progress of coverage (start → peak → end) in your local timezone.',
    feat4_title: 'Full Calendar',
    feat4_desc:
      'Access past and future dates of solar and lunar eclipses with fast searching and filtering mechanisms.',

    workflow_badge: 'Usage Flow',
    workflow_title: 'How EclipseGo Works',
    step1_title: 'Select Location',
    step1_desc:
      'Use current GPS, search for a city in the offline Room database, or ask to find the nearest best visibility.',
    step2_title: 'Calculate Visibility',
    step2_desc:
      'The mathematical engine calculates the local circumstances of visibility of the selected eclipse for the coordinates.',
    step3_title: 'Simulate Timeline',
    step3_desc:
      'Use the interactive slider to see the coverage at each hour and plan your observation in advance.',
    step4_title: 'Track Offline',
    step4_desc:
      'Consult all start, peak, and end data in the field, without needing internet or cellular signal.',

    tech_badge: 'Tech Stack',
    tech_title: 'Native Architecture and Network-Free',
    tech_subtitle: 'Built upon the most modern pillars of native Android development.',
  },
} satisfies Record<Idioma, Record<string, string>>;

export type ChaveEclipse = keyof (typeof eclipsego)['pt'];

// Nomes de tecnologia da seção "Stack de Tecnologia": iguais nos dois idiomas (a página antiga
// não os traduzia).
export const tecnologias = [
  'Kotlin',
  'Jetpack Compose',
  'MVVM Architecture',
  'StateFlow & Coroutines',
  'Room Database (City Caching)',
  'Device Location Provider (GPS)',
  '100% Offline calculations',
  'Mathematical Visibility Algorithms',
];
