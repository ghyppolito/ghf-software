// Conteúdo da landing do TopoWalk (topowalk.html), pt e en, no formato único de landing.ts (WP-10,
// fatia 7; D29), na direção visual do WP-30. Origem de cada frase (D25), com as respostas do
// usuário de 2026-11-24 registradas no WP-10 (fatia 7). Base: a master do app (v4.4.0, `cfbff63`),
// lida só por `git show origin/master:` (as versões em andamento saem depois do site). Siglas:
// TW-README = README.md; TW-ficha = docs/store_listing_texts.md (pt-BR e English); TW-str =
// app/src/main/res/values-pt-rBR/strings.xml (pt) e values/strings.xml (en); LT = este arquivo antes
// da fatia 7 (dicionário transportado da página antiga, WP-08); POL = a política publicada,
// src/content/legal/topowalk-privacy.{pt,en}.md. O en é tradução fiel do pt (ADR-007); onde o app
// tem a string en, é ela.
// - `meta`: `title` e `description` já publicados (título e descrição curta da TW-ficha; WP-21, D19).
// - `resumo`: o texto do card da Home, movido de home.ts sem edição (o card lê `tag` e `curta`).
// - `hero`: o `title` publicado (TW-ficha, título) no lugar do "Precisão Profissional nas Suas Mãos"
//   e sem o selo "de Bolso & RTK" (resposta do usuário: o RTK sai de destaque); `lead` = descrição
//   curta + a 2ª frase da descrição longa da TW-ficha (sem superlativo); sem kicker (repetiria o
//   começo do lead). `meta`: TW-README:5 ("Sem anúncios", "núcleo gratuito") e "Requisitos"
//   (Android 7.0, API 24). O `alt` descreve a tela sem os números.
// - `funcionalidades` (ordem da especificação da fatia): LT `feat3_*` (importação; grátis por
//   TW-README "Importação"), LT `feat2_*` (exclusão; "APPs" do en trocado pelo "protected strip" da
//   TW-ficha en), LT `feat6_*` (laudo; a imagem é a página do PDF gerado pelo app, resposta do
//   usuário) e LT `feat5_*` + TW-str `photos_in_pdf_pro` (fotos e pontos de interesse; título com os
//   nomes do TW-README). "(Pro)" saiu dos títulos: a etiqueta diz. O en de `feat3` foi alinhado ao
//   pt ("sem caminhar"; o publicado dizia "instantly").
// - `todas`: TW-str `help_q5`/`help_a5` (receptor, com "(Beta)" e sem "centimétrica"), `help_a2`
//   (barômetro), `capture_mode_high_detail` (captura Alta, Pro por `capture_mode_high_pro`);
//   TW-README "Visualizações" e "Exportação" (DXF e CSV são Pro, os outros grátis); LT `feat4_*`
//   (locação); TW-README "Histórico" e TW-str `help_a7` (histórico e backup).
// - `prova`: TW-README "Altitude"; TW-README "Importação" e "Fotos de campo" (não diz "nada sai do
//   aparelho": há Firebase Analytics e Crashlytics, POL §4); TW-str `capture_mode_honest` e
//   `help_a18` ("precisão inventada"); TW-str `help_a9` (rascunho).
// - `planos` (`gratis-pro`, sem preço: o preço fica na Play, resposta do usuário): TW-README:5 e
//   "TopoWalk Pro"; TW-ficha ("O essencial é grátis, sempre" e o bullet do Pro). Sem `nota` (o
//   TopoWalk ainda não tem página de termos no site, WP-26).
// - `privacidade`: a landing antiga não tinha frase de privacidade; é a de POL §1 (pt:17, en:17), sem
//   a exceção da migração do Pro, que não toca no levantamento.
// - `faq`: TW-str `help_q1`, `help_q7`, `help_q8`, `help_q15`, `help_q16` e `help_q9`, literais (pt e
//   en do app). Dois desvios do literal, por decisão do usuário (2026-11-24): "seqüencialmente" →
//   "sequencialmente" em `help_a1`, e "(Pro)" depois da tela de locação em `help_a15` (pt e en), porque
//   a locação é Pro; a correção da string no app fica como achado (TOPO-APP-STRINGS-FAQ-01).
import type { Idioma } from './idiomas';
import type { ConteudoApp } from './landing';

export const topowalk = {
  pt: {
    meta: {
      title: 'TopoWalk: Topo e Altimetria — GHF Software',
      description: 'Topografia de campo: pontos, área, declividade, vista 3D e exportação PDF.',
    },
    resumo: {
      tag: 'Topografia & SIG',
      descricao:
        'Transforma seu smartphone numa ferramenta topográfica de campo com precisão barométrica. Calcule distâncias, inclinações e desníveis em tempo real, gerando relatórios em PDF 100% offline.',
      curta: 'Levantamento de campo barométrico de bolso.',
    },
    hero: {
      titulo: 'TopoWalk: Topo e Altimetria',
      lead: 'Topografia de campo: pontos, área, declividade, vista 3D e exportação PDF. Caminhe pelo perímetro, capture os pontos e receba a área, o perímetro, a declividade e o relatório pronto para impressão, tudo no bolso.',
      meta: 'Sem anúncios · Android 7.0 ou superior · Núcleo grátis',
      alt: 'Tela de resultados do TopoWalk: a área do polígono em hectares e, na aba Mapa, o polígono levantado desenhado sobre o mapa.',
    },
    funcionalidades: [
      {
        titulo: 'Importação de Camadas (KML/GeoJSON)',
        descricao:
          'Carregue o KML do CAR, um KMZ do Google Earth, GeoJSON, GPX ou CSV para visualizar o perímetro no mapa e calcular a área líquida sem caminhar.',
        etiqueta: { texto: 'Grátis' },
        imagem: 'camadas',
        alt: 'Detalhe de uma camada importada de um arquivo KML no TopoWalk: área líquida, área bruta e área descontada calculadas a partir do arquivo, e o perímetro da camada desenhado no mapa.',
      },
      {
        titulo: 'Áreas de Exclusão & Área Líquida',
        descricao:
          'Meça o talhão e desconte açudes, APPs ou benfeitorias: cálculo automático de área bruta, descontada e líquida, propagado para PDF, GeoJSON, KML, DXF e CSV.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'exclusao',
        alt: 'Resultados de um levantamento no TopoWalk: distâncias, desnível, declividade, a área líquida em destaque, a área bruta e a área descontada, e as fotos de campo anexadas.',
      },
      {
        titulo: 'Laudo PDF Personalizado',
        descricao:
          'Gere relatórios em PDF A4 com a marca da sua empresa: adicione seu logotipo, nome do responsável técnico, registro profissional (CREA/CAU) e nota de rodapé.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'laudo',
        imagemTipo: 'documento',
        alt: 'Primeira página de um laudo em PDF gerado pelo TopoWalk: cabeçalho com o logotipo e o nome da empresa, o responsável técnico e o registro profissional, e a lista dos pontos medidos com latitude, longitude e altitude.',
      },
      {
        titulo: 'Fotos de Campo & Pontos de Interesse',
        descricao:
          'Anexe até 5 fotos por levantamento e marque pontos de interesse (árvores, portões, erosões) com ícones e notas livres sem alterar a área. Fotos no laudo em PDF fazem parte do TopoWalk Pro.',
        etiqueta: { texto: 'Grátis' },
        imagem: 'pontosFotos',
        alt: 'Resultados de um levantamento no TopoWalk: duas fotos de campo anexadas e, no mapa, o polígono com uma área de exclusão vazada e um ponto de interesse marcado.',
      },
    ],
    todas: [
      {
        titulo: 'Captura',
        itens: [
          {
            nome: 'Receptor GNSS/RTK externo (Beta)',
            descricao:
              'Pareie o receptor nas configurações de Bluetooth do Android e ative o recurso. Com o receptor ligado, os pontos só são capturados com fix válido.',
            etiqueta: { texto: 'Beta' },
          },
          {
            nome: 'Altitude barométrica',
            descricao:
              'Se o aparelho tem barômetro, o TopoWalk o prioriza para o desnível, com calibração manual por uma altitude conhecida. Sem ele, usa a altitude do GPS.',
          },
          {
            nome: 'Captura Alta',
            descricao: 'Média de 10 leituras. Para marco de divisa — cerca de 10 segundos parado.',
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
      {
        titulo: 'Visualização e exportação',
        itens: [
          { nome: 'Perfil 2D, vista 3D e mapa', descricao: 'Perfil de elevação, vista isométrica do polígono e o mapa OpenStreetMap.' },
          {
            nome: 'GeoJSON, KML e GPX',
            descricao: 'Para QGIS e ArcGIS, para o Google Earth e para OsmAnd, Wikiloc e Garmin.',
          },
          {
            nome: 'DXF e CSV',
            descricao: 'DXF (AutoCAD R12 ASCII, em metros num plano local) e CSV em dois arquivos: pontos e segmentos.',
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
      {
        titulo: 'Campo e histórico',
        itens: [
          {
            nome: 'Locação de Pontos & Bússola',
            descricao:
              'Navegue de volta a qualquer ponto levantado com distância, azimute e seta com bússola orientada ao norte verdadeiro (corrigida por declinação magnética).',
            etiqueta: { texto: 'Pro', pro: true },
          },
          {
            nome: 'Histórico e backup',
            descricao:
              'Reabra um levantamento salvo para acrescentar, remover ou inserir pontos, e exporte todo o histórico para um único arquivo.',
          },
        ],
      },
    ],
    prova: [
      {
        titulo: 'De onde vem a altitude',
        texto: 'Do receptor externo, do barômetro ou do GPS do aparelho, nessa ordem de prioridade.',
      },
      {
        titulo: 'O levantamento fica no aparelho',
        texto:
          'Camadas importadas e fotos são copiadas para dentro do app e não são enviadas a lugar nenhum; a foto é gravada sem EXIF.',
      },
      {
        titulo: 'Sem precisão inventada',
        texto:
          'A média deixa o ponto mais estável, não mais preciso: o número mostrado nunca promete melhor do que o seu aparelho informa.',
      },
      {
        titulo: 'Rascunho protegido',
        texto:
          'Cada ponto é gravado no instante em que você o captura. Se o app fechar, a bateria acabar ou o Android encerrar o app, o TopoWalk oferece continuar de onde você parou.',
      },
    ],
    planos: {
      tipo: 'gratis-pro',
      lead: 'Sem anúncios. O núcleo do app é gratuito e sem limite de uso; o TopoWalk Pro é uma compra única, sem assinatura.',
      gratis: {
        titulo: 'Grátis',
        sub: 'Sem anúncios e sem limite de uso',
        itens: [
          'Captura de pontos e todos os cálculos',
          'Altitude barométrica',
          'Receptor GNSS/RTK externo (Beta)',
          'Relatório em PDF',
          'Exportação GeoJSON, KML e GPX',
          'Histórico e backup',
          'Importação de camadas, com a área líquida do arquivo',
          'Pontos de interesse',
          'Fotos de campo anexadas ao levantamento',
        ],
      },
      pro: {
        titulo: 'TopoWalk Pro',
        sub: 'Compra única, sem assinatura',
        itens: [
          { nome: 'Locação', descricao: 'O app guia até um ponto levantado: distância, azimute e uma seta, com vibração na chegada.' },
          { nome: 'Exportação DXF e CSV', descricao: 'DXF para o AutoCAD e CSV para planilha.' },
          {
            nome: 'PDF com identidade visual',
            descricao: 'Logo, nome da empresa, responsável técnico, registro profissional, nota de rodapé e cor do cabeçalho.',
          },
          { nome: 'Área líquida medida a pé', descricao: 'Desconte açude, benfeitoria ou APP medidos na mesma caminhada.' },
          { nome: 'Fotos no laudo', descricao: 'As fotos de campo entram no laudo em PDF, o documento que vai ao cliente.' },
          { nome: 'Captura Alta', descricao: 'Média de 10 leituras: um ponto mais estável, não mais preciso.' },
        ],
      },
    },
    privacidade:
      'Os seus levantamentos — pontos, medições, fotos e relatórios — ficam no seu aparelho e não são enviados a nenhum servidor nosso.',
    faq: [
      {
        pergunta: 'Como medir uma área?',
        resposta:
          'Vá até o primeiro ponto do terreno e toque em "Começar". Caminhe até os demais pontos e os adicione sequencialmente. Mapeando 3 ou mais pontos, a área do polígono será calculada.',
      },
      {
        pergunta: 'Posso corrigir ou continuar um levantamento já salvo?',
        resposta:
          'Pode. Abra o levantamento no Histórico e toque em "Continuar medindo". Ele volta para a captura: dá para acrescentar pontos, remover qualquer ponto — não só o último — e inserir um ponto entre dois outros. Ao salvar, ele substitui a versão do histórico, então um PDF já entregue deixa de corresponder. Por isso o app pede confirmação antes.',
      },
      {
        pergunta: 'Como faço backup dos meus levantamentos?',
        resposta:
          'No Histórico, toque no menu do canto superior e escolha "Fazer backup do histórico". É gerado um único arquivo, que você pode guardar no Drive, no cartão de memória ou onde preferir. Para recuperar, use "Restaurar backup": os levantamentos do arquivo são acrescentados ao seu histórico, nada do que você já tem é apagado, e levantamentos que já existem são ignorados. Um backup feito por uma versão mais nova do TopoWalk é recusado em vez de importado pela metade.',
      },
      {
        pergunta: 'Posso carregar o KML do meu CAR e caminhar até os vértices?',
        resposta:
          'Pode. No Histórico, abra o menu e toque em "Camadas importadas" e depois em "Importar arquivo". KML, KMZ, GeoJSON, GPX e CSV funcionam — o arquivo do CAR, do SIGEF ou o que o cliente mandou entra como camada de referência, desenhada no mapa sem mexer nos seus levantamentos. Toque em qualquer ponto da camada para caminhar até ele pela tela de locação (Pro). O arquivo é copiado para dentro do app, então a camada continua lá mesmo que você apague ou mova o original.',
      },
      {
        pergunta: 'Como desconto um açude ou uma benfeitoria da área?',
        resposta:
          'Caminhe o talhão normalmente e, com pelo menos 3 pontos fixados, toque em "Área de exclusão". A partir daí cada ponto que você fixar vai para a exclusão, e não para o talhão — caminhe em volta do açude e toque em "Fechar exclusão". Os resultados e o PDF passam a mostrar a área bruta, o que foi descontado e a área líquida. Dá para marcar mais de uma. Duas regras que vale saber: exclusão que cai fora do talhão não é descontada (o app avisa), e se duas exclusões se sobrepõem a sobreposição é contada duas vezes — o app avisa, e o conserto é remedir uma delas. Este recurso é do TopoWalk Pro.',
      },
      {
        pergunta: 'O app fechou no meio do levantamento. Perdi os pontos?',
        resposta:
          'Não. Cada ponto é gravado no instante em que você o captura, fora da memória do app. Ao abrir o TopoWalk de novo, ele oferece continuar de onde você parou. Vale o mesmo se a bateria acabar ou se o Android fechar o app em segundo plano.',
      },
    ],
  },
  en: {
    meta: {
      title: 'TopoWalk: Survey & Altimeter — GHF Software',
      description: 'Land surveying: points, area, slope %, 3D view, PDF export.',
    },
    resumo: {
      tag: 'Topography & GIS',
      descricao:
        'Transforms your smartphone into an advanced field topographic tool with barometric precision. Calculate distances, slopes, and elevation on the fly, generating 100% offline PDF reports.',
      curta: 'Pocket barometric field survey tool.',
    },
    hero: {
      titulo: 'TopoWalk: Survey & Altimeter',
      lead: 'Land surveying: points, area, slope %, 3D view, PDF export. Walk the perimeter, capture points, and get area, perimeter, slope and a print-ready report, all in your pocket.',
      meta: 'No ads · Android 7.0 or later · Free core',
      alt: 'TopoWalk results screen: the polygon area in hectares and, on the Map tab, the surveyed polygon drawn over the map (app interface in Portuguese).',
    },
    funcionalidades: [
      {
        titulo: 'Layer Import (KML/GeoJSON)',
        descricao:
          'Load registry KMLs, Google Earth KMZ, GeoJSON, GPX, or CSV to overlay perimeters on the map and calculate the net area without walking.',
        etiqueta: { texto: 'Free' },
        imagem: 'camadas',
        alt: 'Detail of a layer imported from a KML file in TopoWalk: net area, gross area, and deducted area calculated from the file, and the layer outline drawn on the map (app interface in Portuguese).',
      },
      {
        titulo: 'Exclusion Zones & Net Area',
        descricao:
          'Survey land plots and deduct ponds, protected strips, or structures: automatic calculation of gross, deducted, and net area, exported across PDF, GeoJSON, KML, DXF, and CSV.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'exclusao',
        alt: 'Survey results in TopoWalk: distances, elevation change, slope, the net area highlighted, the gross area and the deducted area, and the attached field photos (app interface in Portuguese).',
      },
      {
        titulo: 'Custom Branded PDF Reports',
        descricao:
          'Generate A4 PDF reports featuring your company branding: add your logo, technical manager name, professional license (CREA/CAU), and custom footers.',
        etiqueta: { texto: 'Pro', pro: true },
        imagem: 'laudo',
        imagemTipo: 'documento',
        alt: 'First page of a PDF report generated by TopoWalk: a header with the company logo and name, the technical manager and the professional license, and the list of measured points with latitude, longitude, and altitude (report in Portuguese).',
      },
      {
        titulo: 'Field Photos & Points of Interest',
        descricao:
          'Attach up to 5 photos per survey and mark points of interest (trees, gates, erosion) with custom icons and notes without affecting area calculations. Photos in the PDF report are part of TopoWalk Pro.',
        etiqueta: { texto: 'Free' },
        imagem: 'pontosFotos',
        alt: 'Survey results in TopoWalk: two attached field photos and, on the map, the polygon with a hollow exclusion area and a marked point of interest (app interface in Portuguese).',
      },
    ],
    todas: [
      {
        titulo: 'Capture',
        itens: [
          {
            nome: 'External GNSS/RTK receiver (Beta)',
            descricao:
              "Pair the receiver in Android's Bluetooth settings and turn on the feature. While the receiver is on, points are only captured with a valid fix.",
            etiqueta: { texto: 'Beta' },
          },
          {
            nome: 'Barometric altitude',
            descricao:
              'If your device has a barometer, TopoWalk prioritizes it for elevation change, with manual calibration against a known altitude. Without one, it uses GPS altitude.',
          },
          {
            nome: 'High capture',
            descricao: 'Average of 10 readings. For boundary markers — about 10 seconds standing still.',
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
      {
        titulo: 'Views & export',
        itens: [
          { nome: '2D profile, 3D view, and map', descricao: 'Elevation profile, isometric view of the polygon, and the OpenStreetMap map.' },
          {
            nome: 'GeoJSON, KML, and GPX',
            descricao: 'For QGIS and ArcGIS, for Google Earth, and for OsmAnd, Wikiloc, and Garmin.',
          },
          {
            nome: 'DXF and CSV',
            descricao: 'DXF (AutoCAD R12 ASCII, in meters on a local plane) and CSV in two files: points and segments.',
            etiqueta: { texto: 'Pro', pro: true },
          },
        ],
      },
      {
        titulo: 'Field & history',
        itens: [
          {
            nome: 'Point Stakeout & Compass',
            descricao:
              'Navigate back to any saved survey point with distance, azimuth, and true-north compass guidance (magnetic declination corrected).',
            etiqueta: { texto: 'Pro', pro: true },
          },
          {
            nome: 'History and backup',
            descricao:
              'Reopen a saved survey to add, remove, or insert points, and export your whole history to a single file.',
          },
        ],
      },
    ],
    prova: [
      {
        titulo: 'Where altitude comes from',
        texto: "From the external receiver, the barometer, or the phone's GPS, in that order of priority.",
      },
      {
        titulo: 'The survey stays on the device',
        texto:
          'Imported layers and photos are copied into the app and are not sent anywhere; photos are saved without EXIF.',
      },
      {
        titulo: 'No made-up accuracy',
        texto:
          'Averaging makes the point steadier, not more accurate: the reported figure never claims better than your phone reports.',
      },
      {
        titulo: 'Protected draft',
        texto:
          'Every point is saved the moment you capture it. If the app closes, the battery runs out, or Android shuts the app down, TopoWalk offers to continue from where you stopped.',
      },
    ],
    planos: {
      tipo: 'gratis-pro',
      lead: "No ads. The app's core is free with no usage limits; TopoWalk Pro is a one-time purchase, no subscription.",
      gratis: {
        titulo: 'Free',
        sub: 'No ads and no usage limits',
        itens: [
          'Point capture and all calculations',
          'Barometric altitude',
          'External GNSS/RTK receiver (Beta)',
          'PDF report',
          'GeoJSON, KML, and GPX export',
          'History and backup',
          "Layer import, with the file's net area",
          'Points of interest',
          'Field photos attached to the survey',
        ],
      },
      pro: {
        titulo: 'TopoWalk Pro',
        sub: 'One-time purchase, no subscription',
        itens: [
          { nome: 'Stake-out', descricao: 'The app guides you to a surveyed point: distance, azimuth, and an arrow, with a vibration on arrival.' },
          { nome: 'DXF and CSV export', descricao: 'DXF for AutoCAD and CSV for spreadsheets.' },
          {
            nome: 'PDF with your branding',
            descricao: 'Logo, company name, technical manager, professional license, footer note, and header color.',
          },
          { nome: 'Net area measured on foot', descricao: 'Subtract a pond, a shed, or a protected strip measured on the same walk.' },
          { nome: 'Photos in the report', descricao: 'Field photos go into the PDF report, the document that goes to your client.' },
          { nome: 'High capture', descricao: 'Average of 10 readings: a steadier point, not a more accurate one.' },
        ],
      },
    },
    privacidade:
      'Your surveys — points, measurements, photos, and reports — remain on your device and are not sent to any of our servers.',
    faq: [
      {
        pergunta: 'How to survey an area?',
        resposta:
          'Navigate to the first point of the terrain and tap "Start". Walk to subsequent points and add them. When you map at least 3 points, it closes a polygon and calculates the area.',
      },
      {
        pergunta: 'Can I fix or continue a survey I already saved?',
        resposta:
          'Yes. Open it in History and tap "Continue measuring". The survey reopens for capture: you can add points, remove any point — not only the last one — and insert a point between two others. When you save, it replaces the version in your history, so a PDF you already delivered will no longer match. That is why it asks for confirmation first.',
      },
      {
        pergunta: 'How do I back up my surveys?',
        resposta:
          'In History, tap the menu in the top corner and choose "Back up history". It writes a single file that you can keep in Drive, on a memory card or wherever you like. To recover it, use "Restore backup": the surveys in the file are added to your history, nothing you already have is deleted, and surveys already present are skipped. A backup made by a newer version of TopoWalk is refused instead of imported halfway.',
      },
      {
        pergunta: 'Can I load the KML of my property and walk to the corners?',
        resposta:
          'Yes. In History, open the menu and tap "Imported layers", then "Import file". KML, KMZ, GeoJSON, GPX and CSV all work — the file from your land registry or from your client comes in as a reference layer, drawn on the map without touching your surveys. Tap any point of the layer to walk to it with the stake-out screen (Pro). The file is copied into the app, so it stays there even if you delete or move the original.',
      },
      {
        pergunta: 'How do I subtract a pond or a building from the area?',
        resposta:
          'Walk the plot as usual and, with at least 3 points marked, tap "Exclusion area". From then on every point you mark goes to the exclusion, not to the plot — walk around the pond and tap "Close exclusion". Results and the PDF then show the gross area, what was subtracted and the net area. You can add more than one. Two rules worth knowing: an exclusion that falls outside the plot is not subtracted (the app says so), and if two exclusions overlap, the overlap is counted twice — the app warns you, and the fix is to re-measure one of them. This is a TopoWalk Pro feature.',
      },
      {
        pergunta: 'The app closed while I was surveying. Did I lose the points?',
        resposta:
          "No. Every point is saved the moment you capture it, outside the app's memory. When you open TopoWalk again it offers to continue from where you stopped. The same applies if the battery runs out or if Android closes the app while it is in the background.",
      },
    ],
  },
} satisfies Record<Idioma, ConteudoApp>;
