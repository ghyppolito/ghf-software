// Textos da landing do LottoExpert (lottoexpert.html), pt e en — transportados do dicionário JS
// da lottoexpert.html antiga (WP-08, fatia 2), sem retradução. Chaves `*Html` levam marcação e
// são renderizadas com set:html: `&` escrito `&amp;`.
//
// O pt é o do dicionário, não o do HTML: o JS da página antiga trocava todo `data-i18n` pelo
// dicionário ao carregar, então é o texto que o visitante via. Diferiam `hero_desc` e
// `plan_annual_title` (achado LOTTO-PT-HTML-DIVERGE-01).
//
// Rótulos sem `data-i18n` na página antiga (nomes das loterias, "LottoExpert Engine", os `alt`)
// apareciam iguais no modo en; continuam no markup, iguais nos dois idiomas (achado
// LOTTO-EN-ROTULOS-PT-01). A página antiga não tinha title/description/og em en: os do en abaixo
// reusam textos en que ela já publicava (achado LOTTO-EN-META-01).
//
// Jogo responsável: tools/check_site.py §5 (COPY_PROIBIDA) lê este arquivo também na raiz.

import type { Idioma } from './ui';

export const lottoexpert = {
  pt: {
    title: 'LottoExpert - GHF Software',
    description: 'LottoExpert - O motor matemático definitivo para desdobramentos de loterias.',
    og_title: 'LottoExpert — Motor Matemático para Loterias',
    og_description:
      'Fechamentos combinatórios, OCR de bilhetes e backtesting offline para Mega-Sena, Lotofácil e mais.',
    twitter_description: 'Fechamentos combinatórios, OCR de bilhetes e backtesting offline.',
    hero_badge: 'Engenharia Estatística para Loterias',
    hero_titleHtml: 'Jogue de forma<br class="hidden md:block"> <span class="text-gradient-purple">Inteligente</span>',
    hero_desc:
      'LottoExpert é uma solução de engenharia estatística para apostadores das Loterias da Caixa. Com processamento 100% local e privacidade, gera fechamentos, realiza conferência de bilhetes e reconhecimento OCR no próprio dispositivo, sincronizando resultados com infraestrutura própria no GCP.',
    hero_img_alt: 'Tela principal do app LottoExpert com gerador de fechamentos e estatísticas',
    btn_play: 'Baixar na Google Play',
    btn_learn: 'Ver Funcionalidades',
    features_badge: 'Vantagem Competitiva',
    features_title: 'Projetado por Especialistas',
    features_subtitle: 'Tudo o que você precisa para gerenciar suas apostas com rigor científico.',
    feat1_title: 'Motor Combinatório',
    feat1_desc:
      'Geração de fechamentos C(n,k) otimizada para dispositivos móveis, sem risco de estouro de memória.',
    feat2_title: 'Desdobramentos com Garantia',
    feat2_desc:
      'Matrizes com garantia matemática provada via solver de programação inteira (ILP) para Lotomania, Lotofácil e Timemania.',
    feat3_title: 'Dashboard Meu Desempenho',
    feat3_desc:
      'Gestão financeira completa com apuração de saldo real, ROI por período, evolução mensal e relatórios automatizados.',
    feat4_title: 'Jogos por Concurso',
    feat4_desc:
      'Vínculo de participação com custo congelado, apuração automática pós-sorteio e alertas de prêmios reais.',
    feat5_title: 'Scanner OCR com Consensus',
    feat5_desc:
      'Reconhecimento multi-captura por votação (ML Kit) e leitor matricial customizado para bilhetes da Lotomania.',
    feat6_title: 'Estratégias & Bolão Recorrente',
    feat6_desc:
      'Presets de fechamento salvos para geração em 1 toque e renovação automática de bolões a cada concurso.',
    feat7_title: 'Alertas Inteligentes',
    feat7_desc:
      'Notificações por limiar de acumulado, dezenas monitoradas em ciclo de atraso e lembretes de apostas.',
    feat8_title: 'Gestão de Bolões',
    feat8_desc:
      'Gerencie participantes e cotas com recálculo automático e copie estruturas de bolões com um toque.',
    feat9_title: 'Links Mágicos & QR Code',
    feat9_desc:
      'Convites presenciais via QR Code local e digitais via Link Mágico (GZIP + Base64) para importação instantânea.',
    feat10_title: 'Simulação de ROI',
    feat10_desc:
      'Backtesting de estratégias contra todo o histórico oficial local para projeção realista do retorno financeiro.',
    feat11_title: 'Sync Otimizado & GCP',
    feat11_desc:
      'Sincronização delta otimizada via Cloud Functions Gen 2 e GCS, com atestação de segurança do Firebase App Check.',
    feat12_title: 'Backup no Google Drive',
    feat12_desc:
      'Backup manual e automático (diário) na pasta oculta do app em sua conta Google Drive. A restauração não sobrescreve jogos nem bolões existentes.',
    feat13_title: 'Widget Glance & Resiliente',
    feat13_desc:
      'Widget gratuito na tela inicial via Jetpack Glance e notificações resilientes reagendadas pós-reboot.',
    feat14_title: 'Exportação em PDF',
    feat14_desc:
      "Gere relatórios profissionais em formato A4 para seus jogos e bolões, com cores oficiais e marca d'água por tier.",
    feat15_title: 'Privacidade Total On-Device',
    feat15_desc:
      'Processamento 100% no próprio dispositivo. Seus jogos, fotos de bilhetes e cálculos nunca saem do seu aparelho.',
    feat16_title: 'Teimosinha',
    feat16_desc:
      'Registre o mesmo jogo em vários concursos seguidos e acompanhe a conferência de cada participação. No Premium, até 12 concursos de uma vez.',
    feat17_title: 'Prestação de Contas',
    feat17_desc:
      'Após o sorteio, o organizador gera uma imagem com o resultado do bolão e a divisão informativa do prêmio por participante. Nomes podem ser ocultados.',
    lotteries_title: 'Todas as Loterias em um só lugar',
    lotteries_desc: 'Todas as modalidades oficiais da Caixa Econômica Federal suportadas nativamente.',
    lot_mega_details: '1–60 • Sel: 6–20 • R$ 6,00',
    lot_lotofacil_details: '1–25 • Sel: 15–20 • R$ 3,50',
    lot_quina_details: '1–80 • Sel: 5–15 • R$ 3,00',
    lot_lotomania_details: '1–100 • Sel: 50 • R$ 3,00',
    lot_timemania_details: '1–80 • Sel: 10 • R$ 3,50',
    lot_diadesorte_details: '1–31 • Sel: 7–15 • R$ 2,50',
    lot_duplasena_details: '1–50 • Sel: 6–15 • R$ 3,00',
    lot_mais_milionaria_details: '1–50 + trv • Sel: 6 • R$ 6,00',
    lot_supersete_details: '0–9 (7 col) • Sel: 7 • R$ 3,00',
    pricing_title: 'Grátis ou PRO? Você escolhe.',
    pricing_subtitle: 'Planos flexíveis para se adequar ao seu estilo de aposta. Cancele quando quiser.',
    plan_monthly_title: 'Mensal',
    plan_monthly_priceHtml: 'R$ 7,90<span class="text-sm text-gray-400 font-normal">/mês</span>',
    plan_monthly_desc: 'Experimente todos os recursos Premium com flexibilidade.',
    plan_annual_title: 'Anual ⭐',
    plan_annual_priceHtml: 'R$ 34,90<span class="text-sm text-gray-300 font-normal">/ano</span>',
    plan_annual_desc: 'O melhor custo-benefício para sua estratégia. Equivale a R$ 2,90/mês.',
    plan_lifetime_title: 'Vitalício',
    plan_lifetime_priceHtml: 'R$ 69,90<span class="text-sm text-gray-400 font-normal"> pago uma vez</span>',
    plan_lifetime_desc: 'Acesso permanente e livre de qualquer assinatura futura.',
    plan_badge_popular: 'Recomendado',
    plan_purchase_in_app: 'Disponível para compra no app',
    table_title: 'Comparação Detalhada',
    table_subtitle: 'Veja como a versão Free se compara ao plano Premium',
    pricing_th_features: 'Funcionalidade',
    pricing_th_free: 'Free',
    pricing_th_premium: 'Premium',
    price_feat1: 'Loterias Básicas (Mega-Sena/Lotofácil)',
    price_feat2: 'Todas as Loterias (9 modalidades)',
    price_feat_garantidos: 'Desdobramentos com Garantia (ILP)',
    price_feat3: 'Scanner de Bilhetes (OCR)',
    price_val_free_ocr: '3 capturas de teste',
    price_val_premium_ocr: 'Ilimitado',
    price_feat_conferencia: 'Conferência das Participações',
    price_val_free_conf: 'Manual',
    price_val_premium_conf: 'Automática pós-sorteio',
    price_feat_desempenho: 'Dashboard "Meu Desempenho" (ROI & Saldo)',
    price_val_free_desempenho: 'Amostra desfocada',
    price_val_premium_desempenho: 'Análise Completa',
    price_feat_presets: 'Estratégias Salvas (Presets)',
    price_val_free_preset: '1 Preset',
    price_val_premium_preset: 'Ilimitados',
    price_feat_alertas: 'Alertas Inteligentes (Limiar & Dezenas)',
    price_feat4: 'Backtesting Histórico',
    price_feat5: 'Filtros Pro no Gerador',
    price_feat6: 'Jogos Salvos (Carteira)',
    price_val_free_jogos: 'Até 10',
    price_val_premium_jogos: 'Ilimitado',
    price_feat_concurso: 'Jogos por Concurso',
    price_val_free_concurso: 'Até 5 por concurso',
    price_val_premium_concurso: 'Ilimitado',
    price_feat7: "PDF Limpo (Sem marca d'água)",
    price_feat8: 'Bolões Simultâneos',
    price_val_free_bolao: '1 Ativo',
    price_val_premium_bolao: 'Ilimitado',
    price_feat9: 'Participantes por Bolão',
    price_val_free_part: 'Até 10',
    price_val_premium_part: 'Ilimitado',
    price_feat10: 'Compartilhar Link Mágico + QR Code',
    price_feat11: 'Copiar Bolão & Bolão Recorrente',
    price_feat12: 'Backup no Google Drive',
    price_feat13: 'Widget de Tela Inicial',
  },
  en: {
    title: 'LottoExpert - GHF Software',
    description:
      'LottoExpert is a statistical engineering solution for Brazilian Caixa Lotteries. Designed with a strict focus on local processing and privacy, it handles wheel generation, ticket scanning (OCR), and result checking entirely on your device, syncing results via secure custom GCP infrastructure.',
    og_title: 'LottoExpert — Statistical Engineering For Lotteries',
    og_description:
      'LottoExpert is a statistical engineering solution for Brazilian Caixa Lotteries. Designed with a strict focus on local processing and privacy, it handles wheel generation, ticket scanning (OCR), and result checking entirely on your device, syncing results via secure custom GCP infrastructure.',
    twitter_description: 'Everything you need to manage your bets with scientific rigor.',
    hero_badge: 'Statistical Engineering For Lotteries',
    hero_titleHtml: 'Play Extremely<br class="hidden md:block"> <span class="text-gradient-purple">Smart</span>',
    hero_desc:
      'LottoExpert is a statistical engineering solution for Brazilian Caixa Lotteries. Designed with a strict focus on local processing and privacy, it handles wheel generation, ticket scanning (OCR), and result checking entirely on your device, syncing results via secure custom GCP infrastructure.',
    // sem par en na página antiga (o alt não tinha data-i18n): continua em pt — LOTTO-EN-ROTULOS-PT-01
    hero_img_alt: 'Tela principal do app LottoExpert com gerador de fechamentos e estatísticas',
    btn_play: 'Get it on Google Play',
    btn_learn: 'View Features',
    features_badge: 'Competitive Edge',
    features_title: 'Engineered By Experts',
    features_subtitle: 'Everything you need to manage your bets with scientific rigor.',
    feat1_title: 'Combinatorial Engine',
    feat1_desc:
      'Mobile-optimized C(n,k) matrix generation using lazy Sequences to prevent memory overflow in large wheels.',
    feat2_title: 'Guaranteed Wheelings',
    feat2_desc:
      'Proven mathematical guarantee matrices built via Integer Linear Programming (ILP) solvers for Lotomania, Lotofácil, and Timemania.',
    feat3_title: 'My Performance Dashboard',
    feat3_desc:
      'Comprehensive financial tracking with real balance, ROI analysis per period, monthly charts, and automated reports.',
    feat4_title: 'Draw-Based Tickets',
    feat4_desc:
      'Tickets linked to specific draws with frozen bet costs, automated post-draw verification, and real prize notifications.',
    feat5_title: 'Consensus OCR Scanner',
    feat5_desc: 'Multi-capture consensus reading (ML Kit) and a custom matrix reader for physical Lotomania cards.',
    feat6_title: 'Saved Strategies & Recurrent Sweepstakes',
    feat6_desc: 'One-touch wheeling presets and automatic sweepstake duplication for every upcoming draw.',
    feat7_title: 'Smart Alerts',
    feat7_desc:
      'Notifications for custom jackpot thresholds, monitored numbers on long delay cycles, and betting reminders.',
    feat8_title: 'Sweepstake Management',
    feat8_desc:
      'Manage participants and shares with automated cost calculations and single-tap sweepstake copying.',
    feat9_title: 'Magic Links & QR Codes',
    feat9_desc:
      'In-person sharing with local QR Codes and compressed Magic Links (GZIP + Base64) for instant import.',
    feat10_title: 'ROI Simulation',
    feat10_desc:
      'Historical strategy backtesting against all local official draws for realistic financial projections.',
    feat11_title: 'Optimized Sync & GCP',
    feat11_desc:
      'Optimized delta synchronization via Cloud Functions Gen 2 and GCS, secured with Firebase App Check attestation.',
    feat12_title: 'Google Drive Backup',
    feat12_desc:
      "Manual and automatic daily backups to the app's hidden folder in your Google Drive. Restoring never overwrites existing tickets or sweepstakes.",
    feat13_title: 'Glance Widget & Resilient Notifications',
    feat13_desc: 'Free home screen widget via Jetpack Glance and post-reboot rescheduled notification alarms.',
    feat14_title: 'PDF Export',
    feat14_desc:
      'Generate professional A4 PDF reports for tickets and sweepstakes with official lottery color schemes.',
    feat15_title: 'Total On-Device Privacy',
    feat15_desc:
      '100% on-device processing. Your games, ticket photos, and strategy data never leave your smartphone.',
    feat16_title: 'Repeat Entries (Teimosinha)',
    feat16_desc:
      'Register the same ticket across several consecutive draws and follow the result check for each entry. On Premium, up to 12 draws at once.',
    feat17_title: 'Sweepstake Settlement',
    feat17_desc:
      'After the draw, organizers generate an image with the sweepstake result and an informational prize split per participant. Names can be hidden.',
    lotteries_title: 'All Lotteries in One Place',
    lotteries_desc: 'All official Caixa Econômica Federal modalities supported natively.',
    lot_mega_details: '1–60 • Sel: 6–20 • R$ 6.00',
    lot_lotofacil_details: '1–25 • Sel: 15–20 • R$ 3.50',
    lot_quina_details: '1–80 • Sel: 5–15 • R$ 3.00',
    lot_lotomania_details: '1–100 • Sel: 50 • R$ 3.00',
    lot_timemania_details: '1–80 • Sel: 10 • R$ 3.50',
    lot_diadesorte_details: '1–31 • Sel: 7–15 • R$ 2.50',
    lot_duplasena_details: '1–50 • Sel: 6–15 • R$ 3.00',
    lot_mais_milionaria_details: '1–50 + clv • Sel: 6 • R$ 6.00',
    lot_supersete_details: '0–9 (7 col) • Sel: 7 • R$ 3.00',
    pricing_title: 'Free or PRO? Your Choice.',
    pricing_subtitle: 'Flexible plans to fit your betting style. Cancel anytime.',
    plan_monthly_title: 'Monthly',
    plan_monthly_priceHtml: 'R$ 7.90<span class="text-sm text-gray-400 font-normal">/month</span>',
    plan_monthly_desc: 'Try all Premium features with flexibility.',
    plan_annual_title: 'Annual ⭐',
    plan_annual_priceHtml: 'R$ 34.90<span class="text-sm text-gray-300 font-normal">/year</span>',
    plan_annual_desc: 'The best value for your strategy. Equivalent to R$ 2.90/month.',
    plan_lifetime_title: 'Lifetime',
    plan_lifetime_priceHtml: 'R$ 69.90<span class="text-sm text-gray-400 font-normal"> paid once</span>',
    plan_lifetime_desc: 'Permanent access, free from any future subscriptions.',
    plan_badge_popular: 'Recommended',
    plan_purchase_in_app: 'Available for purchase in-app',
    table_title: 'Detailed Comparison',
    table_subtitle: 'See how the Free version compares to the Premium plan',
    pricing_th_features: 'Features',
    pricing_th_free: 'Free',
    pricing_th_premium: 'Premium',
    price_feat1: 'Basic Lotteries (Mega-Sena/Lotofácil)',
    price_feat2: 'All Lotteries (9 modalities)',
    price_feat_garantidos: 'Guaranteed Wheelings (ILP)',
    price_feat3: 'Ticket Scanner (OCR)',
    price_val_free_ocr: '3 test captures',
    price_val_premium_ocr: 'Unlimited',
    price_feat_conferencia: 'Participation Verification',
    price_val_free_conf: 'Manual',
    price_val_premium_conf: 'Automatic post-draw',
    price_feat_desempenho: '"My Performance" Dashboard (ROI & Balance)',
    price_val_free_desempenho: 'Blurred sample',
    price_val_premium_desempenho: 'Full Analysis',
    price_feat_presets: 'Saved Strategies (Presets)',
    price_val_free_preset: '1 Preset',
    price_val_premium_preset: 'Unlimited',
    price_feat_alertas: 'Smart Alerts (Jackpots & Numbers)',
    price_feat4: 'Historical Backtesting',
    price_feat5: 'Pro Filters in Generator',
    price_feat6: 'Saved Games (Wallet)',
    price_val_free_jogos: 'Up to 10',
    price_val_premium_jogos: 'Unlimited',
    price_feat_concurso: 'Draw-Based Tickets',
    price_val_free_concurso: 'Up to 5 per draw',
    price_val_premium_concurso: 'Unlimited',
    price_feat7: 'Clean PDF (No watermark)',
    price_feat8: 'Simultaneous Sweepstakes',
    price_val_free_bolao: '1 Active',
    price_val_premium_bolao: 'Unlimited',
    price_feat9: 'Participants per Sweepstake',
    price_val_free_part: 'Up to 10',
    price_val_premium_part: 'Unlimited',
    price_feat10: 'Share Magic Link + QR Code',
    price_feat11: 'Copy Sweepstake & Recurrent Sweepstakes',
    price_feat12: 'Google Drive Backup',
    price_feat13: 'Home Screen Widget',
  },
} satisfies Record<Idioma, Record<string, string>>;

export type ChaveLotto = keyof (typeof lottoexpert)['pt'];
