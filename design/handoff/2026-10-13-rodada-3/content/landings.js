// Conteúdo das landings. Fonte: READMEs dos apps (uploads/*_README.md). Só pt existe; outras línguas viram [copy: …].
// Regra: entre landings só mudam os tokens --app-* (acc, accLight, accEdge) e este conteúdo. O template é um só (Landing App.dc.html).
window.GHF_LANDINGS = {
lotto: {
  name: 'LottoExpert', fav: 'assets/lottoexpert_favicon_v3.png', acc: '#A78BFA', accLight: '#6D28D9', accEdge: '#6B5BA8',
  langs: ['pt','en'], playHref: 'https://play.google.com/store/apps/details?id=br.com.ghfsoftware.lottoexpert', privacyHref: 'Legal LottoExpert.dc.html', termsHref: 'lottoexpert-terms.html',
  links: ['features','plans','faq','privacy'],
  hero: { kicker: 'LottoExpert · Loterias da Caixa', title: 'Fechamentos, conferência e bolão, calculados no seu aparelho.',
    lead: 'Gere fechamentos com o custo à vista, confira bilhetes pela câmera e organize bolões com prestação de contas. Os resultados oficiais chegam sincronizados; seus jogos não saem do celular.',
    meta: 'Grátis, com planos Premium opcionais · Android · +18', img: 'assets/lottoexpert_app_mockup.png',
    alt: 'Celular com a tela de estatísticas do LottoExpert: frequência de cada dezena da Lotofácil em barras horizontais.' },
  features: [
    { t: 'Gerador de fechamentos com o custo à vista', shot: 'Gerador', tag: 'Grátis · filtros Pro no Premium', d: 'Escolha quantas dezenas jogar e o custo total aparece em tempo real. Defina um limite de gasto, até R$ 1.000, e o gerador produz exatamente o número de jogos que cabe nele. A chance matemática exata do conjunto fica na tela.' },
    { t: 'Conferência de bilhete pela câmera', shot: 'Conferir bilhete', tag: '3 capturas grátis · ilimitado no Premium', d: 'Aponte para o bilhete físico: o app faz várias leituras e só aceita um jogo quando elas concordam. O reconhecimento roda no aparelho; a imagem não é salva nem enviada.' },
    { t: 'Bolão com cotas, convite e prestação de contas', shot: 'Bolão', tag: '1 bolão grátis · ilimitados no Premium', d: 'Crie o bolão, adicione participantes e cotas, e o valor por cota sai do custo dos jogos. Convide por link ou QR code. Depois do sorteio, gere a imagem de prestação de contas para o grupo.' },
    { t: 'Meu desempenho: apostado, recebido e saldo', shot: 'Meu desempenho', tag: 'Premium', pro: true, d: 'Total apostado, valor recebido e saldo por mês, ano ou desde o início, com bolões pela sua cota. Jogos ainda não conferidos contam no apostado, nunca no recebido.' }],
  groups: [
    { t: 'Gerar jogos', items: [{ n: 'Desdobramento simples', d: 'todas as combinações das suas dezenas, com dezenas fixas.', tag: 'Grátis até 10 jogos' }, { n: 'Desdobramentos com cobertura provada', d: 'matriz fixa com garantia matemática parcial, provada offline.', tag: 'Premium', pro: true }, { n: 'Filtros Pro', d: 'quadrantes, gap médio, ciclo de atraso.', tag: 'Premium', pro: true }, { n: 'Estratégias salvas', d: 'regenere a configuração com um toque.', tag: '1 grátis' }] },
    { t: 'Acompanhar', items: [{ n: 'Jogos por concurso', d: 'aguardando sorteio e conferidos, lado a lado com o resultado.', tag: 'Grátis até 5' }, { n: 'Conferência automática', d: 'depois de cada sincronização, com notificação.', tag: 'Premium', pro: true }, { n: 'Relatório mensal', d: 'fechamento do mês anterior.', tag: 'Premium', pro: true }, { n: 'Alertas', d: 'limiar de acumulado, dezena monitorada, lembrete de jogo.', tag: 'Premium', pro: true }] },
    { t: 'Analisar', items: [{ n: 'Estatísticas', d: 'frequência e atraso por dezena, janela ajustável.', tag: 'Grátis' }, { n: 'Backtesting', d: 'uma estratégia contra os sorteios já armazenados.', tag: 'Premium', pro: true }, { n: 'Resultados offline', d: 'histórico de concursos salvo no aparelho.', tag: 'Grátis' }] },
    { t: 'Organizar', items: [{ n: 'PDF de jogos e de bolão', d: 'cards ou volante para preencher.', tag: 'Marca d’água no grátis' }, { n: 'Backup no Google Drive', d: 'na sua conta; o desenvolvedor não acessa.', tag: 'Premium', pro: true }, { n: 'Copiar e renovar bolão', d: 'para o próximo concurso, manual ou automático.', tag: 'Premium', pro: true }, { n: 'Widget de tela inicial', d: 'último resultado e próximo sorteio.', tag: 'Grátis' }] }],
  gallery: [{ img: 'assets/lottoexpert_app_mockup.png', alt: 'Estatísticas: frequência das dezenas da Lotofácil, com etiquetas quente, neutra e fria.', cap: 'Estatísticas de frequência' }, { cap: 'Gerador' }, { cap: 'Conferir bilhete' }, { cap: 'Bolão' }, { cap: 'Meu desempenho' }],
  proof: [{ k: 'Sem anúncios', v: 'Nenhum SDK de publicidade.' }, { k: 'Cálculo no aparelho', v: 'Geração, conferência e leitura de bilhete rodam offline.' }, { k: 'Resultados oficiais', v: 'Da Caixa, sincronizados em quatro janelas por dia.' }, { k: 'Sem conta', v: 'Nada de cadastro, e-mail ou CPF.' }],
  plans: { type: 'tiers', lead: 'Os três planos pagos liberam o mesmo Premium. A compra é feita pela Google Play, que mostra o preço final.',
    items: [{ n: 'Grátis', price: 'R$ 0', per: '', d: 'Mega-Sena e Lotofácil, conferência manual, 1 bolão ativo.' }, { n: 'Mensal', price: 'R$ 7,90', per: ' /mês', d: 'Assinatura; cancele pela Google Play.' }, { n: 'Anual', price: 'R$ 34,90', per: ' /ano', d: 'Assinatura; equivale a R$ 2,91 por mês.', mark: true }, { n: 'Vitalício', price: 'R$ 69,90', per: ' uma vez', d: 'Compra única, sem renovação.' }],
    colFree: 'Grátis', colPro: 'Premium', colProSub: 'Mensal, Anual, Vitalício', colFeature: 'Recurso',
    compare: [['Loterias','Mega-Sena e Lotofácil','As 9 loterias'],['Jogos salvos','Até 10','Ilimitado'],['Jogos acompanhados por concurso','Até 5','Ilimitado'],['Conferência das participações','Manual','Automática, com notificação'],['Conferência pela câmera','3 capturas de teste','Ilimitada'],['Desdobramento simples','Até 10 jogos','Até 150 jogos (teto técnico)'],['Desdobramentos com cobertura provada','—','Incluído'],['Filtros Pro e backtesting','—','Incluído'],['Meu desempenho e relatório mensal','Amostra desfocada','Incluído'],['Alertas inteligentes','—','Incluído'],['Backup no Google Drive','—','Incluído'],['PDF','Com marca d’água','Limpo'],['Bolões','1 ativo, até 10 participantes','Ilimitados'],['Widget e convite por link/QR','Incluído','Incluído']],
    note: 'Jogo responsável. O LottoExpert organiza jogos e faz contas; não muda a probabilidade de nenhum sorteio. Proibido para menores de 18 anos. Defina um limite de gasto antes de apostar.' },
  privacy: 'Seus jogos, bolões e estratégias ficam no aparelho; o app envia só métricas de uso pseudônimas, que você pode desligar.',
  faq: [
    { q: 'Funciona sem internet?', a: 'Gerar jogos, conferir bilhetes pela câmera e consultar o histórico já baixado funcionam offline. Para receber resultados novos, o app precisa de conexão.' },
    { q: 'Tem anúncios?', a: 'Não. O app não exibe anúncios nem integra SDK de publicidade.' },
    { q: 'O que o Premium acrescenta?', a: 'As outras sete loterias, conferência automática depois do sorteio, desdobramentos com cobertura provada, backtesting, backup no Google Drive e limites maiores para jogos, bolões e participantes. A tabela de planos lista tudo.' },
    { q: 'O app muda a probabilidade de um sorteio?', a: 'Não. Ele mostra a probabilidade exata do que você escolheu, organiza jogos e confere resultados. O sorteio não depende do app.' },
    { q: 'Preciso criar conta?', a: 'Não. O backup no Google Drive (Premium) usa a sua própria conta Google, e o desenvolvedor não tem acesso a ele.' },
    { q: 'Como cancelo a assinatura?', a: 'Pela Google Play, em Pagamentos e assinaturas. O plano Vitalício é compra única e não renova.' }],
  notice: 'Jogo responsável · +18. Loterias são jogos de azar. O app não vende apostas. Aposte só o que cabe no seu orçamento. [copy: redação final do aviso, vinda do app]'
},
topo: {
  name: 'TopoWalk', fav: 'assets/topo-walk.png', acc: '#E38A57', accLight: '#A0491C', accEdge: '#8A5233',
  langs: ['pt','en','es','fr','it','de','ru'], playHref: '#', privacyHref: 'topowalk-privacy.html',
  links: ['features','freepro','faq','privacy'],
  hero: { kicker: 'TopoWalk · Levantamento topográfico de campo', title: 'Levantamento topográfico de campo, com o GPS e o barômetro do celular.',
    lead: 'Pontos georreferenciados, área de polígonos, declividade e desnível, vista 3D isométrica, mapa OpenStreetMap e exportação em PDF, GeoJSON, KML e GPX.',
    meta: 'Sem anúncios · núcleo gratuito · Pro em compra única · Android 7.0 ou superior', img: 'assets/topowalk_screenshot.png',
    alt: 'Celular na trilha com o histórico do TopoWalk: área de 13,6268 ha, vista 3D do polígono e botões PDF, GeoJSON e KML.' },
  features: [
    { t: 'Pontos, área, declividade e desnível', shot: 'Medição', tag: 'Grátis', d: 'Capture 2 ou mais pontos em sequência. O app calcula, por segmento e no total, distância, declividade em porcentagem e ganho e perda de elevação. Com 3 pontos ou mais, fecha o polígono e mostra a área em m², ha ou alqueires.' },
    { t: 'Receptor GNSS/RTK externo', shot: 'Receptor externo', tag: 'Grátis · opcional', d: 'Desligado por padrão. Conecta via Bluetooth a um receptor já pareado e usa posição e altitude de precisão centimétrica. Com ele ligado, um ponto só é capturado com fix válido: nunca há queda silenciosa para o GPS do aparelho.' },
    { t: 'Exporta para o seu SIG e o seu CAD', shot: 'Exportação', tag: 'PDF, GeoJSON, KML e GPX grátis · DXF e CSV no Pro', d: 'PDF A4 com perfil 2D e vista 3D, GeoJSON para QGIS e ArcGIS, KML para o Google Earth, GPX para OsmAnd, Wikiloc e Garmin. Todos os formatos levam os nomes que você deu aos pontos.' },
    { t: 'Área líquida: desconte açude, benfeitoria ou APP', shot: 'Área de exclusão', tag: 'Pro · grátis a partir de arquivo', pro: true, d: 'Meça o talhão e a exclusão na mesma caminhada; o app mostra área bruta, o que foi descontado e a área líquida. Se o KML do CAR já trouxer os recortes, o desconto é grátis.' }],
  groups: [
    { t: 'Medir', items: [{ n: 'Nomear pontos', d: 'o nome aparece no PDF e em todos os arquivos exportados.', tag: 'Grátis' }, { n: 'Editar levantamento salvo', d: 'acrescentar, remover ou inserir pontos.', tag: 'Grátis' }, { n: 'Rascunho protegido', d: 'o app fechar não perde os pontos já capturados.', tag: 'Grátis' }, { n: 'Precisão da captura', d: 'Rápida e Padrão; Alta faz média de 10 leituras.', tag: 'Alta no Pro' }, { n: 'Altitude barométrica', d: 'com calibração manual e fallback para o GPS.', tag: 'Grátis' }] },
    { t: 'Ver', items: [{ n: 'Perfil 2D', d: 'elevação ao longo da distância percorrida.', tag: 'Grátis' }, { n: 'Vista 3D isométrica', d: 'polígono com altitude real.', tag: 'Grátis' }, { n: 'Mapa OpenStreetMap', d: 'demarcação sobre OpenTopoMap, sem API key.', tag: 'Grátis' }] },
    { t: 'Organizar', items: [{ n: 'Histórico com backup e restauração', d: 'um arquivo único; restaurar acrescenta, não apaga.', tag: 'Grátis' }, { n: 'Importar camadas', d: 'KML do CAR, KMZ, GeoJSON, GPX ou CSV, só leitura.', tag: 'Grátis' }, { n: 'Pontos de interesse', d: 'marcações fora de todo cálculo.', tag: 'Grátis' }, { n: 'Fotos de campo', d: 'até 5 por levantamento, gravadas sem EXIF.', tag: 'Grátis' }] },
    { t: 'Entregar ao cliente', items: [{ n: 'Locação', d: 'o app guia até um ponto levantado.', tag: 'Pro', pro: true }, { n: 'Exportação DXF', d: 'AutoCAD R12 ASCII, em metros num plano local.', tag: 'Pro', pro: true }, { n: 'Exportação CSV', d: 'pontos e segmentos, RFC 4180.', tag: 'Pro', pro: true }, { n: 'PDF com identidade visual', d: 'logo, empresa, responsável técnico e registro.', tag: 'Pro', pro: true }, { n: 'Fotos no laudo em PDF', d: 'anexar continua grátis.', tag: 'Pro', pro: true }] }],
  proof: [{ k: 'Sem anúncios', v: 'Nenhum anúncio no app.' }, { k: 'Pro em compra única', v: 'Sem assinatura.' }, { k: 'Levantamentos no aparelho', v: 'Coordenadas e PDFs não saem para servidor nenhum.' }, { k: 'Sem conta', v: 'O TopoWalk não tem contas de usuário.' }],
  plans: { type: 'freepro', lead: 'O núcleo é gratuito e sem limite de uso. O Pro é para quem entrega o levantamento a um cliente: compra única, sem assinatura.',
    freeT: 'Grátis', freeSub: 'sem limite de uso', proT: 'Pro', proSub: 'compra única · preço na Google Play',
    free: ['Captura de pontos e todos os cálculos','Altitude barométrica','Receptor GNSS/RTK externo via Bluetooth','Relatório em PDF','Exportação GeoJSON, KML e GPX','Histórico editável, backup e restauração','Importar camadas (KML do CAR, KMZ, GeoJSON, GPX, CSV)','Pontos de interesse e fotos de campo'],
    pro: [{ n: 'Locação', d: 'O app guia até um ponto levantado: distância, azimute e seta, com vibração na chegada.' }, { n: 'Exportação DXF', d: 'AutoCAD R12 ASCII, em metros num plano local.' }, { n: 'Exportação CSV', d: 'Pontos e segmentos, RFC 4180.' }, { n: 'PDF com a identidade da empresa', d: 'Logo, responsável técnico, registro profissional e cor do cabeçalho.' }, { n: 'Áreas de exclusão', d: 'Desconta açude, benfeitoria ou APP e mostra a área líquida.' }, { n: 'Precisão Alta', d: 'Média de 10 leituras por ponto.' }, { n: 'Fotos no laudo em PDF', d: 'Anexar continua grátis.' }],
    note: 'Quem já usava o TopoWalk antes do Pro recebe acesso vitalício e gratuito, detectado na primeira abertura.' },
  privacy: 'Levantamentos, coordenadas e PDFs ficam no aparelho; o app envia só eventos de uso e relatórios de falha, sem coordenadas.',
  faq: [
    { q: 'Precisa de internet?', a: 'Não para medir. A conexão de dados só é necessária para carregar os tiles do mapa.' },
    { q: 'Tem anúncios?', a: 'Não. O TopoWalk não tem anúncios.' },
    { q: 'O que o Pro acrescenta?', a: 'Locação, exportação DXF e CSV, PDF com a identidade visual da empresa, áreas de exclusão medidas a pé, precisão Alta e fotos no laudo em PDF. Compra única, sem assinatura.' },
    { q: 'O DXF é georreferenciado?', a: 'Não. Sai em metros num plano local, com o primeiro ponto na origem: forma, distâncias e ângulos corretos. A lat/lon da origem vai gravada no arquivo para permitir posicioná-lo.' },
    { q: 'Funciona com receptor RTK?', a: 'Sim, via Bluetooth Classic (SPP), lendo sentenças NMEA 0183. É opcional e vem desligado.' },
    { q: 'Quais aparelhos são compatíveis?', a: 'Android 7.0 ou superior, com GPS. Barômetro e bússola são opcionais: melhoram a altitude e a seta da locação.' }]
},
pole: {
  name: 'Pole Position', fav: 'assets/poleposition.png', acc: '#5FD47E', accLight: '#2A7741', accEdge: '#2F6B49',
  langs: ['pt','en','es','fr','it','de'], playHref: '#', privacyHref: 'poleposition-privacy.html',
  links: ['features','faq','privacy'],
  hero: { kicker: 'Pole Position · Race Analytics', title: 'O smartphone como painel de bordo, com análise completa de sessão.',
    lead: 'Para pilotos de kart e automobilismo amador: cronômetro com parciais, delta da melhor volta, força G e voz do engenheiro. 100% offline.',
    meta: 'Android 8.0 ou superior · 100% offline · [copy: preço ou modelo de cobrança]', img: 'assets/pole_real_mockup.png',
    alt: 'Celular preso ao volante de um kart na pista, com o painel do Pole Position: cronômetro, volta, velocidade e parciais.' },
  features: [
    { t: 'Painel do piloto legível sob sol direto', img: 'assets/pole_live_dashboard.png', alt: 'Painel ao vivo: cronômetro grande, delta, parciais coloridas e barra de força G.', tag: '[copy: grátis ou pago]', d: 'Alto contraste, em retrato ou paisagem. Cronômetro com dígitos tabelados, delta da melhor volta e parciais em três cores. Ao fechar uma volta, tempo e parciais ficam congelados por 3 segundos para conferir.' },
    { t: 'Cronometragem por vetor, ao milissegundo', shot: 'Detecção de linha', tag: '[copy: grátis ou pago]', d: 'A linha é detectada por intersecção de segmentos, sem raio de distância, o que elimina detecções falsas. O instante de cruzamento é interpolado, independente da frequência do GPS, capturado a 10 Hz.' },
    { t: 'Análise de sessão e de traçado', img: 'assets/pole_session_analysis.png', alt: 'Análise de sessão: melhor volta, volta ideal teórica, média, consistência e lista de voltas com delta.', tag: '[copy: grátis ou pago]', d: 'Histórico por circuito, detalhe de cada volta com velocidades, força G máxima e parciais. O traçado GPS da melhor volta, opcional por pista, gera gráficos e compara sessões.' },
    { t: 'Circuito configurado no mapa', shot: 'Configurar circuito', tag: '[copy: grátis ou pago]', d: 'Busque o endereço, posicione a mira sobre a linha de chegada e ajuste o ângulo em passos de 1° e 15°. Marque até 2 linhas de setor. Para trackday, o modo Pista Aberta precisa só da linha de início.' }],
  groups: [
    { t: 'Telemetria', items: [{ n: 'GPS de 10 Hz', d: 'com suporte a antenas externas Bluetooth.' }, { n: 'Força G suavizada', d: 'filtro passa-baixa no acelerômetro.' }, { n: 'Giroscópio', d: 'rotação angular registrada.' }] },
    { t: 'No cockpit', items: [{ n: 'Voz do engenheiro', d: 'tempo de volta e de setor por voz, configuráveis em separado.' }, { n: 'Barra de força G lateral', d: 'carga lateral nas curvas.' }, { n: 'Bloquear notificações', d: 'durante a sessão.' }, { n: 'Brilho e orientação', d: 'independentes do sistema, fixáveis para o cockpit.' }] },
    { t: 'Depois da sessão', items: [{ n: 'Card de compartilhamento', d: 'imagem com contorno da pista, gráficos e QR code, montada no aparelho.' }, { n: 'Exportação CSV', d: 'uma linha por volta.' }, { n: 'Modo Pista Aberta', d: 'cada passagem pela linha de início fecha uma volta.' }] }],
  gallery: [{ img: 'assets/pole_dashboard_mockup.png', alt: 'Painel com tempo de volta, gráfico de velocidade, acelerador e freio, marcha e parciais por setor.', cap: 'Painel e parciais' }, { img: 'assets/pole_session_analysis.png', alt: 'Lista de voltas da sessão com a melhor destacada.', cap: 'Análise de sessão' }, { img: 'assets/pole_live_dashboard.png', alt: 'Painel ao vivo do Pole Position.', cap: 'Painel ao vivo' }],
  proof: [{ k: '100% offline', v: 'GPS, traçado e sensores nunca saem do aparelho.' }, { k: 'Detecção por vetor', v: 'Sem raio de distância; sem detecções falsas.' }, { k: 'Traçado no aparelho', v: 'No máximo 3 sessões por pista.' }],
  privacy: 'GPS, traçado, sensores e o que você escreve ficam no aparelho; saem só métricas anônimas de uso e relatórios de falha, sem coordenadas.',
  faq: [
    { q: 'Funciona sem internet?', a: 'Sim. O app é 100% offline: GPS, traçado e sensores são processados só no aparelho.' },
    { q: 'Preciso de antena externa?', a: 'Não é obrigatório. A captura é otimizada para 10 Hz e aceita antenas externas Bluetooth.' },
    { q: 'Serve para pista sem linha de chegada?', a: 'Sim, no modo Pista Aberta: só a linha de início é necessária, e cada passagem fecha uma volta.' },
    { q: 'Quantos setores posso marcar?', a: 'Até 2 linhas de setor, ou seja, 3 parciais.' },
    { q: 'Como recebo os tempos por voz?', a: 'Conecte um fone Bluetooth. A voz do engenheiro anuncia cada volta e cada setor, configuráveis em separado.' },
    { q: 'Quais aparelhos são compatíveis?', a: 'Android 8.0 ou superior, com Google Play Services.' }]
},
eclipse: {
  name: 'EclipseGo', fav: 'assets/eclipse-go-favicon.png', acc: '#EE737D', accLight: '#AE3646', accEdge: '#8A3A44',
  langs: ['pt','en'], playHref: '#', privacyHref: 'eclipsego-privacy.html',
  links: ['features','faq','privacy'],
  hero: { kicker: 'EclipseGo · Eclipses solares e lunares', title: 'Se um eclipse é visível de onde você está, e a que horas.',
    lead: 'Mostra se um eclipse solar ou lunar é visível da localização escolhida, com horários de início, pico e fim. Totalmente offline: eclipses, cidades e cálculos estão no próprio aparelho.',
    meta: '100% offline · Android 8.0 ou superior · [copy: preço ou modelo de cobrança]', img: 'assets/eclipse_screenshot.png',
    alt: 'Mão segurando o celular com o EclipseGo aberto no eclipse solar total de 12 de agosto de 2026, visto de Praia, Cabo Verde.' },
  features: [
    { t: 'Visível ou não, com início, pico e fim', img: 'assets/eclipse_phone_screen.png', alt: 'Tela do eclipse de 12 de agosto de 2026: céu simulado, linha do tempo e horários de início, pico e fim.', tag: '[copy: grátis ou pago]', d: 'Para cada eclipse, o app diz se ele é visível da localização escolhida e mostra os horários locais. A linha do tempo interativa percorre o evento do início ao fim.' },
    { t: 'Três modos de localização', shot: 'Seletor de localização', tag: '[copy: grátis ou pago]', d: 'Minha localização, pelo GPS; melhor localização visível mais próxima; ou uma localização personalizada, buscando a cidade.' },
    { t: 'Calendário anual e busca', shot: 'Calendário', tag: '[copy: grátis ou pago]', d: 'Veja os eclipses do ano em um calendário ou busque por data e por evento.' }],
  proof: [{ k: '100% offline', v: 'Nenhuma chamada de rede.' }, { k: 'Sem backend', v: 'Nenhum servidor próprio.' }, { k: 'Cidades no aparelho', v: 'Busca sem acento e sem maiúsculas.' }],
  privacy: 'O EclipseGo não faz chamadas de rede: eclipses, cidades e cálculos ficam no aparelho.',
  faq: [
    { q: 'Funciona sem internet?', a: 'Sim, totalmente offline. Os dados de eclipses e de cidades vêm empacotados no app.' },
    { q: 'Preciso liberar a localização?', a: 'Não. Sem GPS ou sem permissão, o app usa uma cidade padrão, e você pode buscar qualquer cidade.' },
    { q: 'Quais anos o app cobre?', a: '[copy: faixa de anos coberta pelos dados de eclipses]' }]
}
};
