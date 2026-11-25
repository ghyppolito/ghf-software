// Conteúdo da landing do LottoExpert (lottoexpert.html), pt e en, no formato único de landing.ts
// (WP-10, fatia 9; D29). Origem de cada frase (D25), com as respostas do usuário de 2026-11-24
// registradas no WP-10 (fatia 9). Siglas: ASO = ../lotto-expert/docs/ASO_METADATA.md na tag
// v2.06.00; LC = ../lotto-expert/docs/LottoExpertContent.md; FC = FreemiumConfig.kt do app na tag
// v2.06.00; LT = este arquivo antes da fatia 9 (dicionário transportado da página antiga, WP-08);
// TERMOS = src/content/legal/lottoexpert-terms.{pt,en}.md. O en é tradução fiel do pt (ADR-007).
// - `meta`: `title` e `description` já publicados (ficha da Play: ASO:11 e ASO:20; WP-21, D19).
// - `resumo`: o texto do card da Home, movido de home.ts sem edição (o card lê `tag` e `curta`).
// - `hero`: título da ficha (ASO:11; en D19 c), lead = descrição curta (ASO:20) + a frase de ASO:31
//   sem a abertura ("A ferramenta definitiva…", "Chega de…"); sem kicker nem o selo "Vantagem
//   Competitiva" (LOTTO-COPY-VANTAGEM-01). A `meta` é texto do usuário. O `alt` descreve a Home sem
//   valores e sem falar em ganho.
// - `funcionalidades` (ordem: fechamento, bolão, scanner, prestação de contas — decisão do usuário em
//   2026-11-24, WP-30 fatia 2; as duas com captura abrem o zigzag e as duas sem captura fecham em cartões):
//   ASO:35 (mais o limite do plano gratuito de FC/LT e LC:49: o teste vale na Lotofácil e na Mega-Sena), ASO:37 (8 modalidades; a frase X/Y é LC:15 e "a garantia é sobre pontos, não sobre lucro" é
//   ../lotto-expert/docs/SPEC_desdobramento_fechamento_volante.md:91 — a ASO:37 diz "garanta uma
//   premiação mínima", que a landing não usa), ASO:41 (mais os
//   limites de FC/LT) e LT `feat17_*`. O plano pago se chama Pro na landing (o texto legal não muda).
//   Scanner e prestação de contas ainda sem captura (D26): só texto, sem placeholder.
// - `todas`: LT `feat16_*` e FC:43-44 (Teimosinha), LC:82-87 e ASO:43 (conferência), ASO:45
//   (resultados), ASO:47 e LC:88-93 (Meu Desempenho), LT `feat12_*` (backup).
// - `prova`: ASO:62 e LC:36; LC:47; ASO:63 e ASO:72.
// - `planos`: LT `pricing_subtitle` + `plan_purchase_in_app`; preços e textos de ASO:68-72; a nota
//   de idade de TERMOS (pt:34, en:33); a tabela é a `price_*` de LT, "Premium" trocado por "Pro",
//   com a linha do fechamento (8 modalidades) e a da Teimosinha (FC:43-44; TEIMOSINHA-FORA-DA-TABELA-01).
// - `privacidade`: LC:35, "Premium" trocado por "Pro".
// - `faq`: LC §12 (LC:558, :561, :567, :570, :579), respostas literais com "Premium" trocado por "Pro".
// - `aviso`: ASO:74.
//
// Jogo responsável: tools/check_site.py §5 (COPY_PROIBIDA) lê este arquivo (FONTES_LOTTO). A regra
// é por linha: frase com "garant"/"guarantee" fica numa linha só.
import type { Idioma } from './idiomas';
import type { ConteudoApp } from './landing';

export const lottoexpert = {
  pt: {
    meta: {
      title: 'LottoExpert: Loterias e Bolão — GHF Software',
      description: 'Scanner de bilhetes, fechamentos, bolão e resultados oficiais da Caixa.',
    },
    resumo: {
      tag: 'Estatística & OCR',
      descricao:
        'Engenharia estatística para loterias com motor combinatório offline, scanner de bilhetes via OCR, gestão de bolões e simulação de ROI histórico.',
      curta: 'Análise matemática e fechamentos offline.',
    },
    hero: {
      titulo: 'LottoExpert: Loterias e Bolão',
      lead: 'Scanner de bilhetes, fechamentos, bolão e resultados oficiais da Caixa. Com análise estatística avançada, conferência automática e processamento local no seu celular, você tem o controle total das suas apostas — do jogo ao resultado.',
      meta: 'Grátis, com plano Pro opcional · Android 8.0 ou superior',
      alt: 'Tela inicial do LottoExpert: as loterias da Caixa, cada uma com a data do próximo sorteio e a estimativa de prêmio.',
    },
    funcionalidades: [
      {
        titulo: 'Fechamento com garantia matemática',
        descricao:
          'Matrizes provadas matematicamente para as 8 modalidades de dezenas: Lotofácil, Mega-Sena, Quina, Lotomania, Timemania, Dupla Sena, Dia de Sorte e +Milionária. Se X das suas dezenas saírem, algum jogo faz ao menos Y pontos. A garantia é sobre pontos, não sobre lucro.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'fechamento',
        alt: 'Tela de fechamento da Lotofácil no LottoExpert: a explicação da garantia de pontos e as matrizes para escolher, cada uma com o número de dezenas, os pontos garantidos, a quantidade de jogos e o custo.',
      },
      {
        titulo: 'Gerador de bolões',
        descricao:
          'Organize grupos de apostas, importe jogos via link direto, compartilhe o PDF profissional com os participantes e configure renovação automática para o próximo concurso (Pro). O plano gratuito tem 1 bolão ativo, com até 10 participantes.',
        imagem: 'bolao',
        alt: 'Tela de um bolão lacrado no LottoExpert: valor da cota, total arrecadado, botão de compartilhar, opção de bolão recorrente e a lista de participantes com a situação do pagamento.',
      },
      {
        titulo: 'Scanner de bilhetes',
        icone: 'camera',
        descricao:
          'Aponte a câmera e confira seus jogos na hora. O app identifica números, concursos e calcula seus prêmios automaticamente, tudo no seu celular, sem enviar foto para nenhum servidor. O plano gratuito tem 3 capturas de teste, na Lotofácil e na Mega-Sena; no Pro, ilimitado.',
      },
      {
        titulo: 'Prestação de contas do bolão',
        icone: 'receipt',
        descricao:
          'Após o sorteio, o organizador gera uma imagem com o resultado do bolão e a divisão informativa do prêmio por participante. Nomes podem ser ocultados.',
      },
    ],
    todas: [
      {
        titulo: 'Acompanhar seus jogos',
        itens: [
          {
            nome: 'Teimosinha',
            descricao:
              'Registre o mesmo jogo em vários concursos seguidos e acompanhe a conferência de cada um. No plano gratuito, um concurso por vez; no Pro, até 12 de uma vez.',
          },
          {
            nome: 'Conferência dos jogos',
            descricao:
              'Vincule cada jogo a um concurso. No plano gratuito você confere manualmente; no Pro, a conferência é automática após o sorteio, com notificação do resultado.',
          },
          {
            nome: 'Resultados oficiais',
            descricao:
              'Mega-Sena, Lotofácil, Quina, Lotomania, Timemania, Dupla Sena, Dia de Sorte, +Milionária e Super Sete, sincronizados automaticamente a cada sorteio, com widget na tela inicial.',
          },
        ],
      },
      {
        titulo: 'Desempenho e dados',
        itens: [
          {
            nome: 'Meu Desempenho',
            descricao:
              'Painel financeiro com total apostado, prêmios, saldo real e ROI, inclusive dos seus bolões. O plano gratuito mostra uma amostra desfocada.',
            etiqueta: { texto: 'Pro', pro: true },
          },
          {
            nome: 'Backup no Google Drive',
            descricao:
              'Backup manual e automático (diário) na pasta oculta do app em sua conta Google Drive. A restauração não sobrescreve jogos nem bolões existentes.',
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
    ],
    prova: [
      {
        titulo: 'Funciona sem internet',
        texto:
          'Consulte jogos salvos e gere matrizes mesmo sem internet. Os resultados ficam armazenados localmente após a sincronização.',
      },
      {
        titulo: 'Leitura no aparelho',
        texto: 'No scanner, toda a análise acontece no dispositivo e nenhuma imagem é enviada para servidores.',
      },
      {
        titulo: 'Sem anúncios',
        texto: 'Experiência limpa e focada no que importa: sua análise. Sem anúncios em nenhum plano.',
      },
    ],
    planos: {
      tipo: 'niveis',
      lead: 'Planos flexíveis para se adequar ao seu estilo de aposta. Cancele quando quiser. Disponível para compra no app.',
      niveis: [
        { nome: 'Mensal', preco: 'R$ 7,90', periodo: '/mês', descricao: 'Acesso completo. Cancele quando quiser.' },
        {
          nome: 'Anual',
          preco: 'R$ 34,90',
          periodo: '/ano',
          descricao: 'Menos de R$ 3 por mês. Acesso completo por um ano inteiro. (~R$ 2,91/mês)',
          destaque: true,
        },
        {
          nome: 'Vitalício',
          preco: 'R$ 69,90',
          periodo: 'pago uma vez',
          descricao: 'Pague uma vez. Use para sempre. Sem renovação automática.',
        },
      ],
      nota: {
        texto:
          'O LottoExpert é destinado a usuários maiores de 18 anos, dada a natureza do conteúdo (loterias e jogos de azar regulamentados pela legislação brasileira).',
        selo: '18',
        termos: 'lottoexpert-terms.html',
      },
      comparacao: {
        colRecurso: 'Funcionalidade',
        colGratis: 'Grátis',
        colPago: 'Pro',
        colPagoSub: 'Mensal · Anual · Vitalício',
        principais: [0, 1, 2, 3, 4, 5, 14, 18],
        linhas: [
          ['Loterias Básicas (Mega-Sena/Lotofácil)', 'Incluído', 'Incluído'],
          ['Gerador para todas as loterias (9 modalidades)', 'Não incluído', 'Incluído'],
          ['Fechamento com garantia (8 modalidades)', 'Não incluído', 'Incluído'],
          ['Scanner de Bilhetes (OCR)', '3 capturas de teste', 'Ilimitado'],
          ['Conferência das Participações', 'Manual', 'Automática pós-sorteio'],
          ['Dashboard "Meu Desempenho" (ROI & Saldo)', 'Amostra desfocada', 'Análise Completa'],
          ['Estratégias Salvas (Presets)', '1 Preset', 'Ilimitados'],
          ['Alertas Inteligentes (Limiar & Dezenas)', 'Não incluído', 'Incluído'],
          ['Backtesting Histórico', 'Não incluído', 'Incluído'],
          ['Filtros Pro no Gerador', 'Não incluído', 'Incluído'],
          ['Jogos Salvos (Carteira)', 'Até 10', 'Ilimitado'],
          ['Jogos por Concurso', 'Até 5 por concurso', 'Ilimitado'],
          ['Teimosinha (mesmo jogo em vários concursos)', '1 concurso por vez', 'Até 12 concursos'],
          ["PDF Limpo (Sem marca d'água)", 'Não incluído', 'Incluído'],
          ['Bolões Simultâneos', '1 Ativo', 'Ilimitado'],
          ['Participantes por Bolão', 'Até 10', 'Ilimitado'],
          ['Compartilhar Link Mágico + QR Code', 'Incluído', 'Incluído'],
          ['Copiar Bolão & Bolão Recorrente', 'Não incluído', 'Incluído'],
          ['Backup no Google Drive', 'Não incluído', 'Incluído'],
          ['Widget de Tela Inicial', 'Incluído', 'Incluído'],
        ],
      },
    },
    privacidade:
      'Seus jogos, estratégias e histórico de apostas ficam no seu celular (ou no Google Drive da sua própria conta, se você ativar o backup Pro) e nunca são enviados para servidores do desenvolvedor.',
    faq: [
      {
        pergunta: 'O app garante ganhos na loteria?',
        resposta:
          'Não. O LottoExpert é uma ferramenta de organização matemática e análise estatística para entretenimento. As loterias são jogos de azar — nenhuma ferramenta pode garantir resultados, nem mesmo o Fechamento com garantia (que garante pontuação condicionada, não o prêmio máximo).',
      },
      {
        pergunta: 'Meus jogos ficam seguros no app?',
        resposta:
          'Sim. Tickets, bolões e histórico de apostas ficam no seu celular (ou na sua própria conta do Google Drive, se você ativar o backup Pro). O app nunca envia esses dados para servidores do desenvolvedor.',
      },
      {
        pergunta: 'Posso usar o app sem internet?',
        resposta:
          'Sim, para a maioria das funcionalidades. Consulta de jogos salvos, geração de fechamentos e backtesting funcionam offline. A sincronização de novos sorteios e o backup no Drive requerem conexão.',
      },
      {
        pergunta: 'O app funciona no iPhone?',
        resposta: 'Não. O LottoExpert é exclusivo para Android (Android 8.0 ou superior).',
      },
      {
        pergunta: 'O plano vitalício é realmente para sempre?',
        resposta:
          'Sim. É uma compra única sem renovação automática. Após a compra, o acesso Pro é permanente naquele dispositivo (e em qualquer dispositivo associado à mesma conta Google Play, conforme política do Google).',
      },
    ],
    aviso:
      'O LottoExpert é uma ferramenta de análise estatística e entretenimento. Não realiza apostas, não garante ganhos e não tem vínculo com a Caixa Econômica Federal. As análises são baseadas em dados históricos. Jogue com responsabilidade.',
  },
  en: {
    meta: {
      title: 'LottoExpert: Lotteries & Sweepstakes — GHF Software',
      description: 'Ticket scanner, wheels, sweepstakes and official Caixa lottery results.',
    },
    resumo: {
      tag: 'Statistics & OCR',
      descricao:
        'Statistical engineering for lotteries featuring an offline combinatorial engine, OCR ticket scanner, sweepstakes management, and historical ROI simulation.',
      curta: 'Mathematical analysis and offline lotto wheels.',
    },
    hero: {
      titulo: 'LottoExpert: Lotteries & Sweepstakes',
      lead: 'Ticket scanner, wheels, sweepstakes and official Caixa lottery results. With advanced statistical analysis, automatic result checking and processing on your own phone, you stay in full control of your bets — from the game to the result.',
      meta: 'Free, with an optional Pro plan · Android 8.0 or later',
      alt: 'LottoExpert home screen: the Caixa lotteries, each with the next draw date and its prize estimate (app interface in Portuguese).',
    },
    funcionalidades: [
      {
        titulo: 'Wheeling with a mathematical guarantee',
        descricao:
          'Mathematically proven matrices for the 8 number-based modalities: Lotofácil, Mega-Sena, Quina, Lotomania, Timemania, Dupla Sena, Dia de Sorte and +Milionária. If X of your numbers are drawn, at least one ticket scores at least Y points. The guarantee is about points, not profit.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'fechamento',
        alt: 'LottoExpert Lotofácil wheeling screen: the explanation of the points guarantee and the matrices to choose from, each showing the number of numbers, the guaranteed points, the number of tickets and the cost (app interface in Portuguese).',
      },
      {
        titulo: 'Sweepstake generator',
        descricao:
          'Organize betting groups, import tickets from a direct link, share the professional PDF with participants and set up automatic renewal for the next draw (Pro). The free plan includes 1 active sweepstake with up to 10 participants.',
        imagem: 'bolao',
        alt: 'LottoExpert screen of a sealed sweepstake: share value, amount collected, share button, recurring sweepstake option and the participant list with payment status (app interface in Portuguese).',
      },
      {
        titulo: 'Ticket scanner',
        icone: 'camera',
        descricao:
          'Point the camera and check your tickets on the spot. The app reads the numbers and draws and calculates your prizes automatically, all on your phone, without sending any photo to a server. The free plan includes 3 test captures, for Lotofácil and Mega-Sena; Pro is unlimited.',
      },
      {
        titulo: 'Sweepstake settlement',
        icone: 'receipt',
        descricao:
          'After the draw, organizers generate an image with the sweepstake result and an informational prize split per participant. Names can be hidden.',
      },
    ],
    todas: [
      {
        titulo: 'Following your games',
        itens: [
          {
            nome: 'Repeat entries (Teimosinha)',
            descricao:
              'Register the same ticket across several consecutive draws and follow the result check for each one. On the free plan, one draw at a time; on Pro, up to 12 at once.',
          },
          {
            nome: 'Ticket checking',
            descricao:
              'Link each ticket to a draw. On the free plan you check manually; on Pro, checking is automatic after the draw, with a result notification.',
          },
          {
            nome: 'Official results',
            descricao:
              'Mega-Sena, Lotofácil, Quina, Lotomania, Timemania, Dupla Sena, Dia de Sorte, +Milionária and Super Sete, synced automatically after each draw, with a home screen widget.',
          },
        ],
      },
      {
        titulo: 'Performance and data',
        itens: [
          {
            nome: 'My Performance',
            descricao:
              'Financial dashboard with total wagered, prizes, real balance and ROI, including your sweepstakes. The free plan shows a blurred sample.',
            etiqueta: { texto: 'Pro', pro: true },
          },
          {
            nome: 'Google Drive backup',
            descricao:
              "Manual and automatic daily backups to the app's hidden folder in your Google Drive. Restoring never overwrites existing tickets or sweepstakes.",
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
    ],
    prova: [
      {
        titulo: 'Works offline',
        texto:
          'Browse saved tickets and generate matrices even without internet. Results stay stored on the device after syncing.',
      },
      {
        titulo: 'Reading on the device',
        texto: 'In the scanner, all analysis happens on the device and no image is sent to any server.',
      },
      {
        titulo: 'No ads',
        texto: 'A clean experience focused on what matters: your analysis. No ads on any plan.',
      },
    ],
    planos: {
      tipo: 'niveis',
      lead: 'Flexible plans to fit your betting style. Cancel anytime. Available for purchase in-app.',
      niveis: [
        { nome: 'Monthly', preco: 'R$ 7.90', periodo: '/month', descricao: 'Full access. Cancel anytime.' },
        {
          nome: 'Annual',
          preco: 'R$ 34.90',
          periodo: '/year',
          descricao: 'Under R$ 3 per month. Full access for a whole year. (~R$ 2.91/month)',
          destaque: true,
        },
        {
          nome: 'Lifetime',
          preco: 'R$ 69.90',
          periodo: 'paid once',
          descricao: 'Pay once. Use forever. No automatic renewal.',
        },
      ],
      nota: {
        texto:
          'LottoExpert is intended for users over 18 years of age, given the nature of the content (lotteries and gambling regulated by Brazilian legislation).',
        selo: '18',
        termos: 'lottoexpert-terms.html',
      },
      comparacao: {
        colRecurso: 'Feature',
        colGratis: 'Free',
        colPago: 'Pro',
        colPagoSub: 'Monthly · Annual · Lifetime',
        principais: [0, 1, 2, 3, 4, 5, 14, 18],
        linhas: [
          ['Basic Lotteries (Mega-Sena/Lotofácil)', 'Included', 'Included'],
          ['Generator for all lotteries (9 modalities)', 'Not included', 'Included'],
          ['Wheeling with guarantee (8 modalities)', 'Not included', 'Included'],
          ['Ticket Scanner (OCR)', '3 test captures', 'Unlimited'],
          ['Participation Verification', 'Manual', 'Automatic post-draw'],
          ['"My Performance" Dashboard (ROI & Balance)', 'Blurred sample', 'Full Analysis'],
          ['Saved Strategies (Presets)', '1 Preset', 'Unlimited'],
          ['Smart Alerts (Threshold & Numbers)', 'Not included', 'Included'],
          ['Historical Backtesting', 'Not included', 'Included'],
          ['Pro Filters in Generator', 'Not included', 'Included'],
          ['Saved Games (Wallet)', 'Up to 10', 'Unlimited'],
          ['Draw-Based Tickets', 'Up to 5 per draw', 'Unlimited'],
          ['Repeat entries (Teimosinha)', '1 draw at a time', 'Up to 12 draws'],
          ['Clean PDF (No watermark)', 'Not included', 'Included'],
          ['Simultaneous Sweepstakes', '1 Active', 'Unlimited'],
          ['Participants per Sweepstake', 'Up to 10', 'Unlimited'],
          ['Share Magic Link + QR Code', 'Included', 'Included'],
          ['Copy Sweepstake & Recurrent Sweepstakes', 'Not included', 'Included'],
          ['Google Drive Backup', 'Not included', 'Included'],
          ['Home Screen Widget', 'Included', 'Included'],
        ],
      },
    },
    privacidade:
      "Your tickets, strategies and bet history stay on your phone (or in your own Google Drive account, if you turn on Pro backup) and are never sent to the developer's servers.",
    faq: [
      {
        pergunta: 'Does the app guarantee gains?',
        resposta:
          'No. LottoExpert is a mathematical organization and statistical analysis tool for entertainment. Lotteries are games of chance: no tool can guarantee results, not even the guaranteed wheeling (which guarantees a conditional score, not the top prize).',
      },
      {
        pergunta: 'Are my tickets safe in the app?',
        resposta:
          "Yes. Tickets, sweepstakes and bet history stay on your phone (or in your own Google Drive account, if you turn on Pro backup). The app never sends this data to the developer's servers.",
      },
      {
        pergunta: 'Can I use the app without internet?',
        resposta:
          'Yes, for most features. Browsing saved tickets, generating wheels and backtesting work offline. Syncing new draws and the Drive backup require a connection.',
      },
      {
        pergunta: 'Does the app work on iPhone?',
        resposta: 'No. LottoExpert is Android-only (Android 8.0 or later).',
      },
      {
        pergunta: 'Is the lifetime plan really forever?',
        resposta:
          "Yes. It is a one-time purchase with no automatic renewal. After purchase, Pro access is permanent on that device (and on any device linked to the same Google Play account, according to Google's policy).",
      },
    ],
    aviso:
      'LottoExpert is a statistical analysis and entertainment tool. It does not place bets, does not guarantee gains, and is not affiliated with Caixa Econômica Federal. The analyses are based on historical data. Play responsibly.',
  },
} satisfies Record<Idioma, ConteudoApp>;
