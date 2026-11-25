// Conteúdo da landing do Pole Position (poleposition.html), pt e en, no formato único de landing.ts
// (WP-10, fatia 8; D29), na direção visual do WP-30. Origem de cada frase (D25), com as respostas do
// usuário de 2026-11-24 registradas no WP-10 (fatia 8). Base: a master do app (v2.2.0, `0f65baa`),
// lida só por `git show origin/master:`. Siglas: PP-README = README.md; PP-ficha = docs/aso_plan.md
// §4.3 (pt-BR) e §4.2 (en-US); PP-str = app/src/main/res/values-pt-rBR/strings.xml (pt) e
// values/strings.xml (en); LT = este arquivo antes da fatia 8 (dicionário transportado da página
// antiga, WP-08); POL = a política publicada, src/content/legal/poleposition-privacy.{pt,en}.md. O en
// é tradução fiel do pt (ADR-007); onde o app tem a string en, é ela.
// Fora, por resposta do usuário (sem origem na master): "100% offline" (há Google Maps e Firebase),
// "GPS de 10 Hz", "antenas externas Bluetooth" e a tabela comparativa (MyChron/Alfano, preços).
// - `meta`: `title` e `description` já publicados (nome e descrição curta da PP-ficha; WP-21, D19).
// - `resumo` (decisão do usuário, 2026-11-24): `descricao` = descrição curta da ficha da Play
//   (`docs/aso_plan.md` §4.3, pt e en, origin/master); `curta` resume a mesma frase sem "offline",
//   "alta frequência" nem "real-time" (sem origem na master). Título do destaque 01: "Painel ao vivo" /
//   "Live dashboard" (ficha: "Painel ao vivo… legível em movimento"), aprovado pelo usuário.
// - `resumo` (histórico): o texto do card da Home, movido de home.ts sem edição (o card lê `tag` e `curta`).
//   Ainda diz "offline"/"real-time" sem origem: achado da fatia, não redigido aqui.
// - `hero`: o nome da PP-ficha (o ": " divide o h1); `lead` = 1ª frase e 2º parágrafo da descrição
//   completa da PP-ficha, verbatim. `meta`: PP-ficha ("sem anúncios", "GRATUITO") e PP-README
//   "Requisitos" (Android 8.0, API 26). O `alt` descreve o painel sem os números.
// - `funcionalidades` (ordem da especificação da fatia; o app é todo grátis, sem etiqueta):
//   1. LT `feat2_*` (Painel do Piloto), sem imagem: o hero já é o painel (cartão com `gauge-high`);
//   2. LT `feat6_title` + PP-ficha ("Análise da sessão", "Volta ideal", "Exportação CSV");
//   3. PP-ficha ("Traçado GPS", "Gráficos de velocidade e força G") + LT `feat7_desc` (comparar
//      sessões);
//   4. LT `feat8_*` (o pt ganha "da Play Store", como o en e o PP-README); a imagem é o card PNG
//      gerado pelo app, que sai na figura de documento, variante escura (`imagemTipo: 'imagem'`),
//      não como tela.
// - `todas`: LT `feat5_*` (configuração de circuito); PP-README "Interpolação de Milissegundo";
//   PP-ficha ("Modo pista aberta", "Ignorar out-lap", "Histórico" e "FEITO PARA A PISTA");
//   LT `feat3_*` (Voz do Engenheiro); PP-README "Configurações" (bloquear notificações). A exportação
//   CSV está no destaque 2. A detecção por vetor está na `prova` (não se repete aqui).
// - `prova`: PP-README "Localização" (o GPS só liga na sessão); PP-README "Detecção de Linha por
//   Vetor"; PP-ficha "SEUS DADOS SÃO SEUS" (não nega o Firebase: a política é a referência); PP-str
//   `help_a11` (traçado opt-in por pista, até 3 sessões).
// - `privacidade`: LT `feat9_desc` ajustado para não contradizer POL ("Resumo de Segurança dos
//   Dados"): sem "100% offline"; "métricas anônimas de uso" é do PP-README "Privacidade".
// - `faq`: PP-str `help_q3`, `help_q4`, `help_q6`, `help_q7` e `help_q10`, literais (pt e en do
//   app); "É gratuito?" com a resposta da PP-ficha ("GRATUITO").
import type { Idioma } from './idiomas';
import type { ConteudoApp } from './landing';

export const poleposition = {
  pt: {
    meta: {
      title: 'Pole Position: Cronômetro GPS — GHF Software',
      description: 'Lap timer GPS: cronômetro de voltas, parciais, velocidade e força G na pista',
    },
    resumo: {
      tag: 'Kart & Automobilismo',
      descricao:
        'Lap timer GPS: cronômetro de voltas, parciais, velocidade e força G na pista.',
      curta: 'Cronômetro GPS de voltas para track day.',
    },
    hero: {
      titulo: 'Pole Position: Cronômetro GPS',
      lead: 'Transforme o celular em um data logger de track day. Defina sua linha de chegada uma vez, toque em IR e cada volta é cronometrada automaticamente por GPS — sem transponder, sem hardware extra, sem assinatura.',
      meta: 'Sem anúncios · Android 8.0 ou superior · Grátis',
      alt: 'Painel ao vivo do Pole Position durante uma volta: cronômetro da volta atual, parciais dos setores em cores, velocidade, delta em relação à melhor volta, barra de força G lateral, última volta e melhor volta.',
    },
    funcionalidades: [
      {
        titulo: 'Painel ao vivo',
        descricao:
          'Design de alto contraste F1 otimizado para sol direto. Dígitos tabelados, congelamento pós-volta de 3s, deltas e parciais coloridas.',
        icone: 'gauge-high',
      },
      {
        titulo: 'Análise de Sessão & CSV',
        descricao:
          'Melhor volta, média, consistência, tempo total e delta volta a volta, mais a volta ideal: sua melhor volta teórica, montada com os seus melhores setores. Exportação CSV para levar os dados para a planilha ou para o seu preparador.',
        imagem: 'analise',
        alt: 'Tela de análise de sessão do Pole Position: a melhor volta, a volta ideal, a média, a consistência e o tempo total, e a lista das cinco voltas com o tempo e o delta de cada uma.',
      },
      {
        titulo: 'Traçado GPS e Gráficos',
        descricao:
          'Sua melhor volta desenhada no mapa, colorida por velocidade, com gráficos de velocidade e força G (lateral e longitudinal, mais o diagrama G-G) para comparar desempenho entre sessões.',
        imagem: 'tracado',
        alt: 'Tela de traçado GPS do Pole Position: a melhor volta desenhada sobre o mapa de satélite, colorida por velocidade e com os tempos dos setores, e abaixo o gráfico de velocidade da volta.',
      },
      {
        titulo: 'Card de Compartilhamento',
        descricao:
          'Geração de card em imagem (PNG) com o traçado da pista, dados de performance e QR code da Play Store para compartilhar suas conquistas.',
        imagem: 'card',
        imagemTipo: 'imagem',
        alt: 'Card de compartilhamento gerado pelo Pole Position: a melhor volta num circuito de exemplo, o traçado sobre o mapa de satélite com os tempos dos setores, a velocidade máxima, a força G máxima, as três parciais e um QR code para baixar o app.',
      },
    ],
    todas: [
      {
        titulo: 'Cronometragem',
        itens: [
          {
            nome: 'Configuração de Circuito',
            descricao:
              'Mira interativa com ajuste de ângulo do gate (passos de 1° e 15°). Suporta até 2 setores customizados por circuito.',
          },
          {
            nome: 'Interpolação de milissegundo',
            descricao: 'Cálculo preciso do instante exato de cruzamento da linha, independentemente da frequência do GPS.',
          },
          { nome: 'Modo pista aberta', descricao: 'Para subidas de montanha, arrancadas e percursos ponto a ponto.' },
          { nome: 'Ignorar out-lap', descricao: 'A primeira volta não distorce suas estatísticas.' },
        ],
      },
      {
        titulo: 'No cockpit e depois',
        itens: [
          {
            nome: 'Voz do Engenheiro (TTS)',
            descricao:
              'Feedback em áudio em tempo real por sintetizador de voz (TTS) das suas parciais e tempos ao fechar setores e voltas.',
          },
          {
            nome: 'Gravação em segundo plano',
            descricao: 'Continua gravando com a tela desligada, e o botão de parar fica na própria notificação.',
          },
          {
            nome: 'Tela e notificações',
            descricao:
              'Modo diurno e noturno, controle de brilho e de orientação da tela, e bloqueio das notificações de outros apps durante a sessão.',
          },
          { nome: 'Histórico', descricao: 'Cada circuito e cada sessão salvos, para acompanhar sua evolução.' },
        ],
      },
    ],
    prova: [
      {
        titulo: 'O GPS só liga durante a sessão',
        texto: 'Fora da sessão não há rastreio nem notificação.',
      },
      {
        titulo: 'Detecção de linha por vetor',
        texto: 'Algoritmo de intersecção de segmentos de reta: não depende de raio de distância e elimina detecções falsas.',
      },
      {
        titulo: 'Seus dados são seus',
        texto:
          'Sem conta, sem cadastro, sem anúncios. Tempos de volta, traçado GPS e dados de sensores são processados e guardados no seu aparelho.',
      },
      {
        titulo: 'Traçado GPS opcional',
        texto:
          'O app pergunta na primeira sessão de cada pista. Até 3 sessões são armazenadas por pista; quando o limite é atingido, o traçado mais antigo é removido (os tempos de volta são sempre mantidos).',
      },
    ],
    privacidade:
      'Localização precisa, traçado da volta e dados de pilotagem ficam no seu aparelho; saem dele apenas métricas anônimas de uso e diagnósticos de falhas (Firebase Analytics e Crashlytics).',
    faq: [
      {
        pergunta: 'Por que as voltas não são registradas?',
        resposta:
          "Verifique se o seu GPS está com alta precisão (em local aberto sem teto, idealmente). Ao iniciar a sessão, o indicador na tela da sessão mostrará 'GPS OK'. Certifique-se também de estar passando exatamente pelas coordenadas estipuladas ao criar a pista, considerando a 'largura' do portão (Gate Width).",
      },
      {
        pergunta: 'O que significa Out-lap?',
        resposta:
          'É a volta inicial de saída dos boxes até o primeiro cruzamento da linha de chegada. Você pode pedir para o app ignorá-la marcando a opção antes de iniciar a sessão.',
      },
      {
        pergunta: 'Posso rodar em segundo plano?',
        resposta:
          'Sim. Depois que a sessão começa no painel, a gravação continua com a tela apagada ou o app minimizado. Se as notificações estiverem permitidas, uma notificação mostra a gravação e tem um botão para pará-la.',
      },
      {
        pergunta: 'O que é o modo Pista Aberta?',
        resposta:
          'O modo Pista Aberta registra a telemetria em qualquer percurso sem precisar de um circuito predefinido. O app registra uma única corrida cronometrada do início ao fim, e a sessão é encerrada automaticamente ao cruzar a linha de chegada. Ideal para subidas, trechos de rally ou qualquer rota em que você não retorna ao mesmo ponto. Basta selecionar uma pista marcada como Pista Aberta e tocar em IR.',
      },
      {
        pergunta: 'Posso exportar os dados da sessão?',
        resposta:
          'Sim. Na tela de resultados da sessão, toque no ícone de compartilhar para exportar um arquivo CSV com uma linha por volta: tempo de volta, velocidade máxima e mínima, G-Force máximo e tempos de cada setor. O arquivo pode ser aberto no Excel, Google Planilhas ou qualquer aplicativo de planilhas.',
      },
      {
        pergunta: 'É gratuito?',
        resposta: 'O Pole Position é gratuito e sem anúncios.',
      },
    ],
  },
  en: {
    meta: {
      title: 'Pole Position: GPS Lap Timer — GHF Software',
      description: 'GPS lap timer with sector splits, speed and G-force telemetry for track days',
    },
    resumo: {
      tag: 'Karting & Motorsport',
      descricao:
        'GPS lap timer with sector splits, speed and G-force telemetry for track days.',
      curta: 'GPS lap timer for track days.',
    },
    hero: {
      titulo: 'Pole Position: GPS Lap Timer',
      lead: 'Turn your phone into a track day data logger. Set your finish line once, tap GO, and every lap is timed automatically by GPS — no transponder, no extra hardware, no subscription.',
      meta: 'No ads · Android 8.0 or later · Free',
      alt: 'Pole Position live dashboard during a lap: current lap timer, color-coded sector splits, speed, delta to the best lap, lateral G-force bar, last lap and best lap (app interface in Portuguese).',
    },
    funcionalidades: [
      {
        titulo: 'Live dashboard',
        descricao:
          'F1-style high contrast design optimized for direct sunlight. Monospace table digits, 3s post-lap freeze, deltas, and color-coded sectors.',
        icone: 'gauge-high',
      },
      {
        titulo: 'Session Analytics & CSV',
        descricao:
          'Best lap, average, consistency, total time and lap-by-lap deltas, plus the ideal lap: your theoretical best lap, built from your fastest sectors. CSV export to take your data to a spreadsheet or to your engineer.',
        imagem: 'analise',
        alt: 'Pole Position session analysis screen: the best lap, the ideal lap, the average, the consistency and the total time, and the list of the five laps with the time and delta of each (app interface in Portuguese).',
      },
      {
        titulo: 'GPS Trace and Graphs',
        descricao:
          'Your best lap drawn on the map, colored by speed, with speed and G-force graphs (lateral and longitudinal G, plus a G-G diagram) to compare performance between sessions.',
        imagem: 'tracado',
        alt: 'Pole Position GPS trace screen: the best lap drawn over the satellite map, colored by speed and with the sector times, and below it the speed graph of the lap (app interface in Portuguese).',
      },
      {
        titulo: 'Analysis Share Card',
        descricao:
          'Generate an analysis card as a PNG image with track outline, performance metrics, and a Play Store QR code to share achievements.',
        imagem: 'card',
        imagemTipo: 'imagem',
        alt: 'Share card generated by Pole Position: the best lap on a sample circuit, the trace over the satellite map with the sector times, the top speed, the maximum G-force, the three splits and a QR code to download the app (card in Portuguese).',
      },
    ],
    todas: [
      {
        titulo: 'Timing',
        itens: [
          {
            nome: 'Circuit Configuration',
            descricao:
              'Interactive map targeting with fine-grained gate rotation adjustments (1° and 15° steps). Set up to 2 splits per track.',
          },
          {
            nome: 'Millisecond interpolation',
            descricao: 'Precise calculation of the exact moment the line is crossed, regardless of the GPS update rate.',
          },
          { nome: 'Open track mode', descricao: 'For hillclimbs, sprints and point-to-point runs.' },
          { nome: 'Out-lap toggle', descricao: "Ignore the first lap so it doesn't skew your stats." },
        ],
      },
      {
        titulo: 'In the cockpit and after',
        itens: [
          {
            nome: 'Engineer Voice (TTS)',
            descricao:
              'Real-time text-to-speech audio feedback for lap times and split sector updates while keeping your eyes on the track.',
          },
          {
            nome: 'Background recording',
            descricao: 'Recording continues with the screen off, and a stop button sits right in the notification.',
          },
          {
            nome: 'Screen and notifications',
            descricao:
              "Day and night themes, brightness and screen orientation control, and muting of other apps' notifications during a session.",
          },
          { nome: 'History', descricao: 'Every track and every session saved, so you can watch yourself improve.' },
        ],
      },
    ],
    prova: [
      {
        titulo: 'GPS is on only during a session',
        texto: 'Outside a session there is no tracking and no notification.',
      },
      {
        titulo: 'Vector line detection',
        texto: "Line-segment intersection algorithm: it doesn't rely on a distance radius and rules out false detections.",
      },
      {
        titulo: 'Your data stays yours',
        texto:
          'No account, no sign-up, no ads. Lap times, GPS traces and sensor data are processed and stored on your device.',
      },
      {
        titulo: 'Opt-in GPS trace',
        texto:
          'The app asks the first time you start a session on a track. Up to 3 sessions are stored per track; when the limit is reached, the oldest trace is removed (lap times are always kept).',
      },
    ],
    privacidade:
      'Precise location, lap traces and driving data stay on your device; only anonymous usage metrics and crash diagnostics leave it (Firebase Analytics and Crashlytics).',
    faq: [
      {
        pergunta: 'Why are my laps not being recorded?',
        resposta:
          "Check that your GPS has high precision (ideally in the open, with no roof). Once the session starts, the indicator on the session screen shows 'GPS OK'. Also make sure you pass exactly through the coordinates set when creating the track, considering the gate width (Gate Width).",
      },
      {
        pergunta: 'What does Out-lap mean?',
        resposta:
          'It is the initial exit lap from the pits until the first crossing of the finish line. You can request the app to ignore it by checking the option before starting the session.',
      },
      {
        pergunta: 'Can it run in the background?',
        resposta:
          'Yes. Once the session starts on the dashboard, recording continues with the screen off or the app minimized. If notifications are allowed, a notification shows the recording and has a button to stop it.',
      },
      {
        pergunta: 'What is Open Track mode?',
        resposta:
          "Open Track mode records telemetry on any open route — no predefined circuit needed. The app records a single timed run from start to finish, and the session stops automatically when the finish line is crossed. Ideal for hill climbs, rally stages, or any route where you don't return to the same point. Just select a track marked as Open Track and tap GO.",
      },
      {
        pergunta: 'Can I export my session data?',
        resposta:
          'Yes. In the session results screen, tap the share icon to export a CSV file with one row per lap: lap time, maximum and minimum speed, maximum G-Force, and individual sector times. The file can be opened in Excel, Google Sheets, or any spreadsheet app.',
      },
      {
        pergunta: 'Is it free?',
        resposta: 'Pole Position is free and ad-free.',
      },
    ],
  },
} satisfies Record<Idioma, ConteudoApp>;
