// Textos da landing do Pole Position (poleposition.html), pt e en — transportados do dicionário JS
// da poleposition.html antiga (WP-08, fatia 4), sem retradução.
//
// O pt é o do dicionário, não o do HTML: o JS da página antiga trocava todo `data-i18n` pelo
// dicionário ao carregar, então é o texto que o visitante via. Diferiam `feat9_desc`,
// `step4_desc` e `set1_desc` (achado POLE-PT-HTML-DIVERGE-01).
//
// As seções "Veja na prática" e "Para quem é" e os `alt` das imagens não tinham `data-i18n`: o
// visitante via pt nos dois idiomas, e o en abaixo repete o pt (achado POLE-EN-ROTULOS-PT-01).
//
// A página antiga não tinha title/description/og em en: os do en abaixo reusam textos en que ela
// já publicava (o `<title>` pt já era em inglês) (achado POLE-EN-META-01).

import type { Idioma } from './ui';

export const poleposition = {
  pt: {
    title: 'Pole Position: Race Telemetry & Analytics - GHF Software',
    description:
      'Telemetria Automotiva profissional e offline direto no seu dispositivo Android. Desenvolvido para kart e trackdays com GPS 10Hz e intersecção vetorial.',

    hero_badge: 'Telemetria Automotiva Profissional',
    hero_title_1: 'Pole Position',
    hero_title_2: 'Telemetria de Alta Performance no Cockpit',
    hero_desc:
      'O Pole Position transforma seu smartphone num sistema completo de telemetria offline para kart e trackdays. GPS de alta frequência, intersecção de gates por vetor e áudio TTS integrados.',
    btn_download: 'Baixar na Google Play',
    btn_privacy: 'Privacidade',
    alt_session:
      'Tela de análise de sessão do Pole Position com comparativo de voltas e exportação CSV',
    alt_live: 'Painel ao vivo do Pole Position com velocidade, Força G e parciais em tempo real',

    features_badge: 'Recursos de Pista',
    features_title: 'Engenharia de Telemetria no Bolso',
    features_subtitle:
      'Tecnologias avançadas desenvolvidas para extrair cada milissegundo de performance em pista.',
    feat1_title: 'Telemetria em Tempo Real',
    feat1_desc:
      'GPS de 10 Hz com suporte a antenas externas Bluetooth. Algoritmo de intersecção por vetores (raio zero) com interpolação de milissegundos.',
    feat2_title: 'Painel do Piloto (Live Dash)',
    feat2_desc:
      'Design de alto contraste F1 otimizado para sol direto. Dígitos tabelados, congelamento pós-volta de 3s, deltas e parciais coloridas.',
    feat3_title: 'Voz do Engenheiro (TTS)',
    feat3_desc:
      'Feedback em áudio em tempo real por sintetizador de voz (TTS) das suas parciais e tempos ao fechar setores e voltas.',
    feat4_title: 'Modo Pista Aberta',
    feat4_desc:
      'Cronometragem baseada apenas na linha de início. Ideal para sessões de circuito aberto, trackdays e trajetos livres.',
    feat5_title: 'Configuração de Circuito',
    feat5_desc:
      'Mira interativa com ajuste de ângulo do gate (passos de 1° e 15°). Suporta até 2 setores customizados por circuito.',
    feat6_title: 'Análise de Sessão & CSV',
    feat6_desc:
      'Históricos organizados por pista, com velocidade máxima, velocidades mínimas, Força G e exportação estruturada para arquivos CSV.',
    feat7_title: 'Análise de Traçado (Lap Trace)',
    feat7_desc:
      'Visualização gráfica do traçado GPS da melhor volta com gráficos de velocidade e força G para comparar desempenho entre sessões.',
    feat8_title: 'Card de Compartilhamento',
    feat8_desc:
      'Geração de card em imagem (PNG) com o traçado da pista, dados de performance e QR code para compartilhar suas conquistas.',
    feat9_title: '100% Offline & Seguro',
    feat9_desc:
      'Processamento local seguro no dispositivo. Dados de pilotagem 100% offline, com envio exclusivo de métricas anônimas de uso e diagnósticos de falhas (Firebase Analytics & Crashlytics).',

    mockup_title: 'Veja na prática',
    mockup_desc: 'Interface desenhada para leitura sob luz solar direta.',
    alt_mockup: 'Painel de telemetria do Pole Position com volta atual, Força G e mapa de pista',

    audience_title: 'Para quem é',
    audience1_title: 'Pilotos de kart amador',
    audience1_desc: 'Identifique onde está perdendo tempo sem investir em equipamentos caros.',
    audience2_title: 'Instrutores de pilotagem',
    audience2_desc: 'Compare voltas de diferentes alunos com dados reais de GPS e G lateral.',
    audience3_title: 'Equipes de automobilismo regional',
    audience3_desc: 'Telemetria profissional no bolso, sem custo de hardware dedicado.',

    workflow_badge: 'Fluxo de Trabalho',
    workflow_title: 'Como Utilizar no Cockpit',
    step1_title: 'Traçar a Linha',
    step1_desc: 'Ajuste o gate da linha de chegada no mapa de satélite e adicione os setores desejados.',
    step2_title: 'Configurar',
    step2_desc:
      'Fixe o celular firmemente no cockpit, calibre os acelerômetros de Força G e conecte seus fones de ouvido.',
    step3_title: 'Acelerar',
    step3_desc:
      'Inicie a sessão e pilote. A primeira passagem cruza a linha iniciando a telemetria automaticamente.',
    step4_title: 'Analisar',
    step4_desc:
      'Finalize a sessão, exporte em CSV, gere o card de análise em imagem ou confira os gráficos de traçado de volta (GPS).',

    compare_badge: 'Comparativo',
    compare_title: 'Pole Position vs. Alternativas',
    compare_subtitle:
      'Veja como nos comparamos com cronômetros de hardware caros e aplicativos convencionais.',
    th_feature: 'Recurso',
    th_hardware: 'Telemetria dedicada (MyChron/Alfano)',
    th_common_app: 'Aplicativos de GPS comuns',
    th_pole: 'Pole Position App',
    row1_name: 'Frequência GPS',
    row1_hardware: 'Alta (10 Hz — 20 Hz)',
    row1_common: 'Baixa (1 Hz típica)',
    row1_pole: 'Alta (Até 10 Hz com antena externa)',
    row2_name: 'Custo',
    row2_hardware: 'Elevado (R$ 3.000+)',
    row2_common: 'Grátis / Assinatura',
    row2_pole: 'Gratuito (100% livre de custos)',
    row3_name: 'Detecção de Linha',
    row3_hardware: 'Sensor Magnético ou GPS',
    row3_common: 'Raio de Proximidade (Inexato)',
    row3_pole: 'Intersecção Vetorial Rigorosa',
    row4_name: 'Feedback de Áudio',
    row4_hardware: 'Não possui',
    row4_common: 'Simples ou Inexistente',
    row4_pole: 'Voz do Engenheiro (TTS volta e setores)',
    row5_name: 'Exportação de Dados',
    row5_hardware: 'Software proprietário / Cabo',
    row5_common: 'Limitada ou Paga',
    row5_pole: 'CSV Aberto com colunas alinhadas',
    row6_name: 'Processamento',
    row6_hardware: '100% Local',
    row6_common: 'Geralmente em Nuvem',
    row6_pole: '100% Offline no Dispositivo',

    settings_badge: 'Configurações Inteligentes',
    settings_title: 'Controle Total do Cockpit',
    settings_desc:
      'Ajustes criados para quem está dentro do cockpit pilotando, não apenas olhando para a tela.',
    set1_title: 'Modo de Localização Inteligente',
    set1_desc:
      'Ativação inteligente do GPS de alta precisão (em primeiro e segundo plano) apenas durante sessões ativas para garantir telemetria contínua e economizar bateria.',
    set2_title: 'Bloqueio de Notificações',
    set2_desc:
      'Desativa notificações de outros aplicativos enquanto a sessão estiver rodando para manter o foco total.',
    set3_title: 'Brilho e Orientação Travados',
    set3_desc:
      'Controle de intensidade de luz independente e travamento de orientação para visualização estável no suporte.',

    tech_badge: 'Stack de Tecnologia',
    tech_title: 'Arquitetura Nativa e Confiável',
    tech_subtitle:
      'Desenvolvido com tecnologias modernas do ecossistema Android para máxima eficiência.',
  },
  en: {
    title: 'Pole Position: Race Telemetry & Analytics - GHF Software',
    description:
      'Pole Position transforms your smartphone into a complete offline telemetry system for karting and trackdays. Featuring high-frequency GPS support, vector gate intersection, and integrated TTS audio.',

    hero_badge: 'Professional Motorsports Telemetry',
    hero_title_1: 'Pole Position',
    hero_title_2: 'High Performance Cockpit Telemetry',
    hero_desc:
      'Pole Position transforms your smartphone into a complete offline telemetry system for karting and trackdays. Featuring high-frequency GPS support, vector gate intersection, and integrated TTS audio.',
    btn_download: 'Get it on Google Play',
    btn_privacy: 'Privacy Policy',
    alt_session:
      'Tela de análise de sessão do Pole Position com comparativo de voltas e exportação CSV',
    alt_live: 'Painel ao vivo do Pole Position com velocidade, Força G e parciais em tempo real',

    features_badge: 'Track Features',
    features_title: 'Telemetry Engineering in your Pocket',
    features_subtitle:
      'Advanced features developed to extract every millisecond of performance on track.',
    feat1_title: 'Real-time Telemetry',
    feat1_desc:
      '10 Hz GPS support for external Bluetooth antennas. Vector gate intersection algorithm (zero radius) with millisecond interpolation.',
    feat2_title: 'Pilot Panel (Live Dash)',
    feat2_desc:
      'F1-style high contrast design optimized for direct sunlight. Monospace table digits, 3s post-lap freeze, deltas, and color-coded sectors.',
    feat3_title: 'Engineer Voice (TTS)',
    feat3_desc:
      'Real-time text-to-speech audio feedback for lap times and split sector updates while keeping your eyes on the track.',
    feat4_title: 'Open Track Mode',
    feat4_desc:
      'Timing based strictly on a single start line gate. Designed for open trackdays, custom routes, and open-circuit timing.',
    feat5_title: 'Circuit Configuration',
    feat5_desc:
      'Interactive map targeting with fine-grained gate rotation adjustments (1° and 15° steps). Set up to 2 splits per track.',
    feat6_title: 'Session Analytics & CSV',
    feat6_desc:
      'Track-grouped logs with detailed analysis: top speeds, minimum speeds, maximum G-forces, split delta comparison, and CSV export.',
    feat7_title: 'Lap Trace Analysis',
    feat7_desc:
      "Graphic visualization of the best lap's GPS trace with speed and G-force charts to compare performance between sessions.",
    feat8_title: 'Analysis Share Card',
    feat8_desc:
      'Generate an analysis card as a PNG image with track outline, performance metrics, and a Play Store QR code to share achievements.',
    feat9_title: '100% Offline & Secure',
    feat9_desc:
      'Secure on-device local processing. Driving data remains 100% offline, with only anonymous usage metrics and crash diagnostics sent (Firebase Analytics & Crashlytics).',

    mockup_title: 'Veja na prática',
    mockup_desc: 'Interface desenhada para leitura sob luz solar direta.',
    alt_mockup: 'Painel de telemetria do Pole Position com volta atual, Força G e mapa de pista',

    audience_title: 'Para quem é',
    audience1_title: 'Pilotos de kart amador',
    audience1_desc: 'Identifique onde está perdendo tempo sem investir em equipamentos caros.',
    audience2_title: 'Instrutores de pilotagem',
    audience2_desc: 'Compare voltas de diferentes alunos com dados reais de GPS e G lateral.',
    audience3_title: 'Equipes de automobilismo regional',
    audience3_desc: 'Telemetria profissional no bolso, sem custo de hardware dedicado.',

    workflow_badge: 'Workflow',
    workflow_title: 'How to Use in the Cockpit',
    step1_title: 'Draw the Line',
    step1_desc:
      'Set the finish line and optional sector gates using the interactive satellite view and gate rotation controls.',
    step2_title: 'Mount & Setup',
    step2_desc:
      'Securely mount the smartphone inside the cockpit, calibrate the G-force sensors, and connect your headsets.',
    step3_title: 'Drive',
    step3_desc:
      'Start monitoring and drive out. The timer starts automatically upon your first crossing of the finish line gate.',
    step4_title: 'Analyze & Share',
    step4_desc:
      'Finish your session, export data as CSV, generate image analysis cards, or review interactive lap trace charts.',

    compare_badge: 'Comparison',
    compare_title: 'Pole Position vs. Alternatives',
    compare_subtitle: 'See how we compare against expensive hardware timers and conventional apps.',
    th_feature: 'Feature',
    th_hardware: 'Dedicated Telemetry (MyChron/Alfano)',
    th_common_app: 'Standard GPS Apps',
    th_pole: 'Pole Position App',
    row1_name: 'GPS Update Rate',
    row1_hardware: 'High (10 Hz — 20 Hz)',
    row1_common: 'Low (1 Hz typical)',
    row1_pole: 'High (Up to 10 Hz with external antenna)',
    row2_name: 'Cost',
    row2_hardware: 'Very High ($500+)',
    row2_common: 'Free / Subscription',
    row2_pole: 'Free (100% free of charge)',
    row3_name: 'Line Detection',
    row3_hardware: 'Magnetic Loop or GPS Gate',
    row3_common: 'Radial Proximity (Inaccurate)',
    row3_pole: 'Strict Vector Intersection',
    row4_name: 'Audio Feedback',
    row4_hardware: 'None',
    row4_common: 'Simple or None',
    row4_pole: 'Engineer Voice (TTS lap and sectors)',
    row5_name: 'Data Export',
    row5_hardware: 'Proprietary software / Cable',
    row5_common: 'Limited or Paid',
    row5_pole: 'Open CSV format with aligned headers',
    row6_name: 'Processing',
    row6_hardware: '100% Offline/Local',
    row6_common: 'Cloud-dependent',
    row6_pole: '100% Offline on Device',

    settings_badge: 'Smart Settings',
    settings_title: 'Total Cockpit Control',
    settings_desc:
      'Telemetry settings designed for drivers inside the cockpit, not just spectators looking at a screen.',
    set1_title: 'Smart Location Service',
    set1_desc:
      'Automatically toggles high-accuracy telemetry GPS (foreground and background) only when a tracking session is active for continuous capture and battery efficiency.',
    set2_title: 'Suppress Alerts',
    set2_desc: 'Mutes incoming notifications and alerts during sessions to maintain total concentration.',
    set3_title: 'Brightness & Screen Lock',
    set3_desc: 'Independent screen brightness controls and rotation locking for stable dashboard mounting.',

    tech_badge: 'Technology Stack',
    tech_title: 'Native and Reliable Architecture',
    tech_subtitle:
      'Built with the modern Android software development ecosystem for performance and reliability.',
  },
} satisfies Record<Idioma, Record<string, string>>;

export type ChavePole = keyof (typeof poleposition)['pt'];

// Nomes de tecnologia da seção "Stack de Tecnologia": iguais nos dois idiomas (a página antiga
// não os traduzia).
export const tecnologias = [
  'Kotlin',
  'Jetpack Compose (Material 3)',
  'MVVM + StateFlow',
  'Hilt Injection',
  'Room Database (Room v7)',
  'Google Play Services Location (10Hz)',
  'SensorManager (Accelerometer & Gyroscope)',
  'Foreground Service (TelemetryService)',
  'Google Maps Compose API',
  'Android TextToSpeech (TTS)',
  'Firebase Analytics & Crashlytics',
];
