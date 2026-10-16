// Textos da landing do TopoWalk (topowalk.html), pt e en — transportados do dicionário JS da
// topowalk.html antiga (WP-08, fatia 3), sem retradução. Chaves `*Html` levam marcação e são
// renderizadas com set:html: `&` escrito `&amp;`.
//
// O pt é o do dicionário, não o do HTML: o JS da página antiga trocava todo `data-i18n` pelo
// dicionário ao carregar, então é o texto que o visitante via. Diferiam `hero_desc` e
// `features_title` (achado TOPO-PT-HTML-DIVERGE-01).
//
// A página antiga não tinha title/description/og em en: os do en abaixo reusam textos en que ela
// já publicava (achado TOPO-EN-META-01).

import type { Idioma } from './ui';

export const topowalk = {
  pt: {
    title: 'TopoWalk - Levantamento Topográfico de Bolso e RTK',
    description:
      'TopoWalk transforma seu Android em uma ferramenta topográfica avançada de campo. Receptores GNSS/RTK externos, áreas de exclusão e área líquida, importação KML/GeoJSON, locação, laudos PDF e exportação em DXF, CSV, GeoJSON, KML e GPX. GHF Software.',
    hero_badge: 'Levantamento Topográfico de Bolso & RTK',
    hero_titleHtml:
      'Precisão Profissional<br class="hidden md:block"> nas <span class="text-gradient-amber">Suas Mãos</span>',
    hero_desc:
      'O TopoWalk transforma seu smartphone em uma ferramenta topográfica avançada de campo. Suporta receptores GNSS/RTK externos via Bluetooth, altimetria barométrica, áreas de exclusão e área líquida, importação KML/GeoJSON, locação de pontos, fotos de campo e exportação para PDF, DXF, CSV, GeoJSON, KML e GPX.',
    btn_play: 'Baixar na Google Play',
    btn_learn: 'Como Funciona',
    features_badge: 'Poder no Terreno',
    features_title: 'Tecnologia Desenhada para a Área Externa',
    feat1_title: 'Receptor GNSS/RTK (Bluetooth)',
    feat1_desc:
      'Conecta-se a receptores RTK externos via Bluetooth (NMEA 0183) para precisão centimétrica, monitoramento de fix (RTK FIX/FLOAT) e offset de altura de bastão.',
    feat2_title: 'Áreas de Exclusão & Área Líquida',
    feat2_desc:
      'Meça o talhão e desconte açudes, APPs ou benfeitorias: cálculo automático de área bruta, descontada e líquida (Pro), propagado para PDF, GeoJSON, KML, DXF e CSV.',
    feat3_title: 'Importação de Camadas (KML/GeoJSON)',
    feat3_desc:
      'Carregue o KML do CAR, um KMZ do Google Earth, GeoJSON, GPX ou CSV para visualizar o perímetro no mapa e calcular a área líquida sem caminhar.',
    feat4_title: 'Locação de Pontos & Bússola (Pro)',
    feat4_desc:
      'Navegue de volta a qualquer ponto levantado com distância, azimute e seta com bússola orientada ao norte verdadeiro (corrigida por declinação magnética).',
    feat5_title: 'Fotos de Campo & Waypoints',
    feat5_desc:
      'Anexe até 5 fotos por levantamento e marque pontos de interesse (árvores, portões, erosões) com ícones e notas livres sem alterar a área.',
    feat6_title: 'Laudo PDF Personalizado (Pro)',
    feat6_desc:
      'Gere relatórios em PDF A4 com a marca da sua empresa: adicione seu logotipo, nome do responsável técnico, registro profissional (CREA/CAU) e nota de rodapé.',
    feat7_title: 'Exportação CAD & SIG Multi-Formato',
    feat7_desc:
      'Exporte em DXF (AutoCAD R12 ASCII em metros no plano local), CSV em dois arquivos (pontos/segmentos), GeoJSON, KML (Google Earth) e GPX (trilhas/waypoints).',
    feat8_title: 'Núcleo Gratuito + Pro sem Assinatura',
    feat8_desc:
      'Sem anúncios. Todo o núcleo do app é 100% gratuito e sem limite. O TopoWalk Pro é uma compra única sem assinatura nem mensalidades.',
    pro_badge: 'TopoWalk Pro',
    pro_title: 'Ferramentas Profissionais de Entrega ao Cliente',
    pro_subtitle: 'Compra única e definitiva · Sem assinaturas nem taxas recorrentes',
    pro1_title: 'Locação de Pontos',
    pro1_desc: 'Bússola orientada ao norte verdadeiro e indicação de tolerância do equipamento.',
    pro2_title: 'Áreas de Exclusão',
    pro2_desc: 'Desconto de furos no terreno (açudes, APPs) com cálculo de área líquida real.',
    pro3_title: 'PDF com Identidade Visual',
    pro3_desc: 'Relatórios A4 personalizados com logotipo, responsável técnico e CREA.',
    pro4_title: 'Exportação DXF & CSV',
    pro4_desc: 'Arquivos prontos para desenhos no AutoCAD e tabelas de cálculo em planilhas.',
    how_badge: 'Simples e Direto',
    how_title: 'O Fluxo de Uso Mais Rápido',
    how1_title: '1. Ponto Inicial & Receptor RTK',
    how1_desc:
      'Conecte seu receptor GNSS/RTK via Bluetooth ou use o GPS interno com o barômetro. Aguarde o fix de alta precisão e grave o primeiro ponto.',
    how2_title: '2. Capturar, Excluir & Fotografar',
    how2_desc:
      'Percorra o terreno capturando pontos, anexe fotos de campo, marque pontos de interesse e defina áreas de exclusão para obter a área líquida.',
    how3_title: '3. Importar & Locar',
    how3_desc:
      'Carregue camadas KML/GeoJSON enviadas pelo cliente como referência no mapa ou use a Locação Pro para encontrar marcos no terreno.',
    how4_title: '4. Laudos PDF & Exportação CAD/SIG',
    how4_desc:
      'Finalize para gerar relatórios PDF A4 com sua identidade visual ou exporte arquivos DXF, CSV, GeoJSON, KML e GPX para seu software de escolha.',
  },
  en: {
    title: 'TopoWalk - Pocket Topographic Survey & RTK',
    description:
      'TopoWalk turns your smartphone into an advanced fieldwork surveying tool. Supports external Bluetooth GNSS/RTK receivers, barometric altimetry, exclusion zones & net area, KML/GeoJSON import, point stakeout, field photos, and exports to PDF, DXF, CSV, GeoJSON, KML, and GPX.',
    hero_badge: 'Pocket Topographic Survey & RTK',
    hero_titleHtml:
      'Professional Precision<br class="hidden md:block"> in <span class="text-gradient-amber">Your Hands</span>',
    hero_desc:
      'TopoWalk turns your smartphone into an advanced fieldwork surveying tool. Supports external Bluetooth GNSS/RTK receivers, barometric altimetry, exclusion zones & net area, KML/GeoJSON import, point stakeout, field photos, and exports to PDF, DXF, CSV, GeoJSON, KML, and GPX.',
    btn_play: 'Get it on Google Play',
    btn_learn: 'How It Works',
    features_badge: 'Off-Road Power',
    features_title: 'Engineered specifically for the Great Outdoors',
    feat1_title: 'External GNSS/RTK (Bluetooth)',
    feat1_desc:
      'Connects to paired external RTK receivers via Bluetooth (NMEA 0183) for centimeter accuracy, real-time fix quality (RTK FIX/FLOAT), and rod height offset.',
    feat2_title: 'Exclusion Zones & Net Area',
    feat2_desc:
      'Survey land plots and deduct ponds, APPs, or structures: automatic calculation of gross, deducted, and net area (Pro), exported across PDF, GeoJSON, KML, DXF, and CSV.',
    feat3_title: 'Layer Import (KML/GeoJSON)',
    feat3_desc:
      'Load registry KMLs, Google Earth KMZ, GeoJSON, GPX, or CSV to overlay perimeters on the map and calculate net area instantly.',
    feat4_title: 'Point Stakeout & Compass (Pro)',
    feat4_desc:
      'Navigate back to any saved survey point with distance, azimuth, and true-north compass guidance (magnetic declination corrected).',
    feat5_title: 'Field Photos & Waypoints',
    feat5_desc:
      'Attach up to 5 photos per survey and mark points of interest (trees, gates, erosion) with custom icons and notes without affecting area calculations.',
    feat6_title: 'Custom Branded PDF Reports (Pro)',
    feat6_desc:
      'Generate A4 PDF reports featuring your company branding: add your logo, technical manager name, professional license (CREA/CAU), and custom footers.',
    feat7_title: 'Multi-Format CAD & GIS Export',
    feat7_desc:
      'Export to DXF (AutoCAD R12 ASCII in meters on local plane), dual CSV files (points/segments), GeoJSON, KML (Google Earth), and GPX (tracks/waypoints).',
    feat8_title: 'Free Core + One-Time Pro Upgrade',
    feat8_desc:
      'Ad-free. All core surveying tools are 100% free with no usage limits. TopoWalk Pro is a one-time purchase with zero recurring subscriptions.',
    pro_badge: 'TopoWalk Pro',
    pro_title: 'Professional Deliverables for Your Clients',
    pro_subtitle: 'One-time lifetime purchase · No subscriptions or recurring fees',
    pro1_title: 'Point Stakeout',
    pro1_desc: 'True-north compass navigation and hardware tolerance indicators.',
    pro2_title: 'Exclusion Zones',
    pro2_desc: 'Deduct land cutouts (ponds, APPs) with precise net area calculation.',
    pro3_title: 'Custom Branded PDFs',
    pro3_desc: 'Professional A4 reports featuring your company logo and engineer license.',
    pro4_title: 'DXF & CSV Export',
    pro4_desc: 'Production-ready files for AutoCAD drawings and spreadsheet calculations.',
    how_badge: 'Keep It Simple',
    how_title: 'Frictionless Workflow',
    how1_title: '1. Initial Point & RTK Receiver',
    how1_desc:
      'Connect your GNSS/RTK receiver via Bluetooth or use internal GPS with barometer. Wait for high-accuracy fix and capture your origin point.',
    how2_title: '2. Capture, Deduct & Photograph',
    how2_desc:
      'Traverse the terrain capturing points, attach field photos, mark waypoints, and outline exclusion areas for net area calculations.',
    how3_title: '3. Import & Stake Out',
    how3_desc:
      'Load client KML/GeoJSON layers as map references or use Pro Stakeout to navigate directly back to boundary markers in the field.',
    how4_title: '4. PDF Reports & CAD/GIS Export',
    how4_desc:
      'Finalize to generate branded A4 PDF reports or export DXF, CSV, GeoJSON, KML, and GPX files for your preferred software.',
  },
} satisfies Record<Idioma, Record<string, string>>;

export type ChaveTopo = keyof (typeof topowalk)['pt'];
