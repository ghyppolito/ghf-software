# TopoWalk

Aplicativo Android para **levantamento topográfico de campo** usando GPS e barômetro do dispositivo. Suporta medições com múltiplos pontos, cálculo de área de polígonos, declividade e desnível, visualização 3D isométrica, mapa OpenStreetMap, histórico persistente e editável com backup/restauração, e exportação em PDF, GeoJSON, KML e GPX.

**Sem anúncios.** O núcleo do app é gratuito e sem limite de uso: captura, todos os cálculos, altitude barométrica, receptor GNSS externo, relatório em PDF, exportação GeoJSON/KML/GPX, histórico e backup. O **TopoWalk Pro** — compra única, sem assinatura — acrescenta exportação DXF e CSV, PDF com a identidade visual da empresa e locação (voltar até um ponto levantado).

---

## Funcionalidades

### Medição topográfica
- Captura de **2 ou mais pontos** georreferenciados em sequência
- Cálculo automático de grandezas por segmento e totais, incluindo **declividade em porcentagem** e **ganho/perda de elevação** ao longo da caminhada
- Suporte a polígono fechado (≥ 3 pontos) com cálculo de área
- **Nomear pontos** ("canto da cerca", "mourão 12") — o nome acrescenta à numeração e aparece no PDF e em todos os arquivos exportados
- **Editar um levantamento já salvo**: reabrir para acrescentar pontos, remover qualquer ponto (não só o último) ou inserir um ponto entre dois outros. Ao salvar, substitui a versão do histórico — pede confirmação antes, porque um PDF já entregue deixa de corresponder
- **Rascunho protegido**: o app fechar, a bateria acabar ou o Android encerrar o processo em segundo plano não perde os pontos já capturados — o TopoWalk oferece continuar de onde parou

### Receptor GNSS/RTK externo (Bluetooth)
Opcional e **desligado por padrão**. Conecta-se a um receptor GNSS/RTK externo já pareado via **Bluetooth Classic (SPP)**, interpreta as sentenças **NMEA 0183** (GGA/GST/RMC) e usa posição e altitude de precisão centimétrica no lugar do GPS interno. Exibe qualidade do fix (RTK FIX/FLOAT), satélites, HDOP e precisão horizontal ao vivo, com campo de **altura de antena/bastão**. Quando ligado, um ponto só é capturado com fix válido — nunca há queda silenciosa para o GPS do aparelho. Em builds de debug, um **receptor RTK simulado** reproduz um fluxo NMEA de exemplo para teste sem hardware.

### Altitude
Prioridade **receptor externo > barômetro > GPS interno**. Prioriza o **barômetro** quando não há receptor externo (`h = 44330 × (1 − (p/p₀)^(1/5.255))`) com calibração manual de offset, e fallback automático para a altitude GPS quando o sensor de pressão não está presente.

### Visualizações
- **Perfil 2D** — gráfico vetorial de elevação ao longo da distância percorrida
- **Vista 3D isométrica** — projeção isométrica do polígono com altitude real (apenas ≥ 3 pontos)
- **Mapa OpenStreetMap** — sobreposição da demarcação sobre mapa de relevo (OpenTopoMap), sem API key

### Histórico
- Salvamento local das medições com nome e observações opcionais
- Lista com **scroll infinito** (Jetpack Paging 3) para performance em grandes volumes
- Detalhes de cada medição com tabela de segmentos, gráficos e exportação
- **Backup e restauração**: exporta todo o histórico para um único arquivo, que pode ser guardado no Drive, no cartão de memória ou onde preferir. Restaurar **acrescenta** ao histórico — nada existente é apagado, duplicatas são ignoradas, e um backup gerado por uma versão mais nova do app é recusado em vez de importado pela metade

### Importação (novo)
- **Camadas de referência** — carregue o KML do CAR, um KMZ do Google Earth, um GeoJSON, uma trilha GPX ou um CSV de coordenadas e veja o perímetro desenhado no mapa, ao lado dos seus levantamentos
- **É gratuito** — importar não exige o Pro; só *caminhar até* um ponto da camada usa a Locação, que é Pro
- **Somente leitura** — a camada não vira levantamento nem entra no histórico: o dado que o cliente mandou e o dado medido em campo ficam separados de propósito
- **Fica no aparelho** — o conteúdo é copiado para dentro do app, então a camada sobrevive a apagar ou mover o arquivo original. Nada é enviado para lugar nenhum
- **Recusa em vez de travar** — arquivo acima de 8 MB ou 20.000 pontos, formato desconhecido ou arquivo sem coordenada válida viram aviso legível, cada um com o seu texto
- **Área líquida do arquivo, de graça** — se o KML ou o GeoJSON trouxer recortes internos (a APP do CAR, por exemplo), o app desconta e mostra bruta, descontado e líquida, sem ninguém caminhar nada. Medir a própria exclusão a pé é que é o recurso Pro

### Áreas de exclusão · área líquida (novo, Pro)
- Meça o talhão e **desconte** o açude, a benfeitoria, a APP ou o afloramento: o app mostra área bruta, o que foi descontado e a **área líquida** — o número que o produtor rural de fato usa
- A exclusão é medida na mesma caminhada: com o perímetro fechado, toque em "Área de exclusão" e cada ponto passa a ir para o anel em vez do talhão, com uma faixa dizendo isso o tempo todo
- **Nada sai errado em silêncio:** exclusão fora do talhão não é descontada e a tela diz por quê; exclusões que se sobrepõem são descontadas com aviso, porque a interseção acaba contada duas vezes. O aviso vai também para o PDF
- Propagada aos quatro formatos: furos no `Polygon` do GeoJSON, `innerBoundaryIs` no KML, camada própria no DXF e a coluna `anel` no CSV. **Sem exclusão, o DXF e o CSV continuam exatamente o que sempre foram**

### Pontos de interesse (novo)
- Marque a árvore de referência, o portão, a erosão — **sem que entre no cálculo**: nem distância, nem perímetro, nem área
- Seis ícones e uma descrição livre; a descrição é opcional, o ícone já diz alguma coisa
- É **grátis**. Aparece no mapa, no PDF (seção própria) e em todos os formatos exportados
- No GPX sai com `<type>` distinguindo anotação de ponto medido — sem isso, outra ferramenta misturaria os dois e a área calculada de lá sairia errada

### Precisão da captura (novo)
- Três modos: **Rápida** (1 leitura, instantânea), **Padrão** (média de 3) e **Alta** (média de 10, Pro)
- **O corte é no modo, não na precisão.** Rápida e Padrão são grátis e cobrem o uso normal; a Alta troca dez segundos parado por um ponto mais estável, útil em marco de divisa
- **A precisão informada nunca promete mais do que o aparelho reporta.** A média elimina ruído, não o erro sistemático do GNSS — se as leituras espalharem, o número piora e o usuário sabe que vale refazer o ponto
- Durante a coleta o botão vira contador e dá saída: dá para desistir sem esperar
- Com receptor RTK externo a captura segue instantânea — ele já entrega centímetros

### Fotos de campo (novo)
- Até **5 fotos por levantamento** — o marco, o portão, a erosão —, tiradas na hora ou escolhidas da galeria
- **Anexar é grátis.** O que é Pro é a foto **no laudo em PDF**, que é o documento que vai ao cliente
- **Nenhuma permissão de câmera ou de armazenamento** é pedida: a câmera do sistema e o seletor de fotos entregam ao app só o arquivo escolhido
- A cópia é reduzida a 1280 px e gravada **sem EXIF** — a rotação é aplicada na imagem, e a geolocalização que a câmera anota não vai junto
- Apagar o levantamento apaga as fotos dele; o original da galeria nunca é tocado

### Exportação
- **PDF** — relatório A4 completo com cabeçalho, pontos, resultados, tabela de segmentos, perfil 2D e vista 3D
- **GeoJSON** — compatível com QGIS, ArcGIS e demais SIGs
- **KML** — compatível com Google Earth e aplicações similares
- **GPX** — trilha e waypoints, compatível com OsmAnd, Wikiloc e Garmin
- **DXF** (Pro) — AutoCAD R12 ASCII, em metros num plano local
- **CSV** (Pro) — dois arquivos: pontos e segmentos, RFC 4180 com BOM
- Todos os formatos carregam os nomes que você deu aos pontos
- **Área fecha o perímetro; trilha não.** Quando o levantamento tem área, DXF, GeoJSON e KML saem com o contorno fechado — o SIG e o CAD medem a área sozinhos. Percurso aberto sai aberto, para não inventar um lado que você não caminhou

### TopoWalk Pro (compra única)
Quatro funcionalidades voltadas a quem **entrega o levantamento a um cliente**:

- **Locação** — escolha um ponto de um levantamento salvo e o app guia até ele: distância, azimute e uma seta, com vibração na chegada. A tolerância acompanha o equipamento (≈3 m no GPS interno, 0,10 m com RTK), e a seta corrige a declinação magnética — sem isso ela apontaria para o lado errado *com a distância diminuindo mesmo assim*. Aparelho sem bússola degrada para o azimute numérico em vez de exibir uma seta parada
- **Exportação DXF** — AutoCAD R12 ASCII, em metros num plano local com o primeiro ponto na origem, em camadas separadas para pontos, linhas e rótulos. **Não é georreferenciado**: forma, distâncias e ângulos corretos, mas o desenho não cai sozinho em UTM — a lat/lon da origem vai gravada no arquivo para permitir posicioná-lo
- **Exportação CSV** — dois arquivos, pontos e segmentos, compartilhados juntos. RFC 4180 com BOM de UTF-8: vírgula como separador e ponto decimal, para abrir em qualquer software. (O Excel em pt-BR espera ponto e vírgula e vai pedir *Dados > De texto*)
- **PDF com identidade visual** — logo, nome da empresa, responsável técnico, registro profissional, nota de rodapé e cor do cabeçalho em todo relatório gerado

Quem já usava o TopoWalk antes do lançamento do Pro recebe acesso **vitalício e gratuito**, detectado automaticamente na primeira abertura. A concessão fica registrada no aparelho — sem conta de usuário, ela não acompanha uma reinstalação em outro celular.

### Internacionalização
Suporte a 7 idiomas com detecção automática pelo sistema:

| Código | Idioma |
|---|---|
| `en` | Inglês (padrão/fallback) |
| `pt-rBR` | Português — Brasil |
| `es` | Espanhol |
| `fr` | Francês |
| `it` | Italiano |
| `de` | Alemão |
| `ru` | Russo |

---

## Grandezas calculadas

### Por segmento (P_n → P_n+1)

| Grandeza | Descrição | Método |
|---|---|---|
| Distância Horizontal | Distância em planta entre pontos consecutivos | Fórmula de Haversine |
| Desnível (ΔH) | Diferença de altitude entre os pontos | Altitude do receptor externo, barométrica ou GPS |
| Distância Inclinada | Comprimento real do segmento | Pitágoras (√(H² + ΔH²)) |
| Ângulo de Inclinação | Ângulo da rampa em graus | arctan(ΔH / H) |
| Azimute | Direção geográfica do segmento | atan2 sobre coordenadas locais |

### Totais

| Grandeza | Descrição |
|---|---|
| Distância Horizontal Total | Soma das distâncias horizontais dos segmentos |
| Desnível Total (líquido) | Diferença de altitude entre o primeiro e o último ponto |
| Distância Inclinada Total | Soma das distâncias inclinadas dos segmentos |
| Ângulo Geral | Ângulo calculado com base nos totais |
| **Declividade (%)** | Ângulo geral convertido em porcentagem — 8% = 8 m de subida a cada 100 m percorridos. Ausente quando o ângulo se aproxima de 90° (parede) |
| **Ganho de elevação** | Soma dos desníveis positivos dos segmentos — quanto se subiu, no total |
| **Perda de elevação** | Soma dos desníveis negativos dos segmentos — quanto se desceu, no total |
| Área do Polígono | Área da demarcação fechada (≥ 3 pontos), em m², ha ou alqueires |

---

## Requisitos

- Android 7.0 (API 24) ou superior
- GPS (localização precisa)
- Permissões: `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `INTERNET`; `BLUETOOTH_CONNECT` (opcional, apenas para receptor externo)
- Barômetro (opcional — melhora a precisão da altitude)
- Bússola / magnetômetro (opcional — a seta da locação; sem ele o app mostra o azimute)
- Receptor GNSS/RTK externo com Bluetooth (opcional — precisão centimétrica)
- Conexão de dados (opcional — necessária apenas para carregar tiles do mapa)

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Kotlin |
| UI | Jetpack Compose + Material 3 |
| Navegação | Navigation Compose |
| Arquitetura | MVVM + StateFlow |
| Localização | FusedLocationProviderClient (Play Services) |
| GNSS/RTK externo | Bluetooth Classic (SPP) + parser NMEA 0183 próprio |
| Altitude | Android SensorManager — `TYPE_PRESSURE` |
| Banco de dados | Room 2.8 + KSP |
| Paginação | Jetpack Paging 3 (`room-paging`) |
| Mapa | osmdroid 6.1.20 — OpenStreetMap / OpenTopoMap |
| PDF | Android `PdfDocument` API + `FileProvider` |
| Exportação geo | GeoJSON, KML e GPX gerados internamente |
| Backup | Storage Access Framework — arquivo único, versionado |
| Exportação CAD/planilha | DXF (AutoCAD R12 ASCII) e CSV (RFC 4180) gerados internamente |
| Compra no app | Google Play Billing 9 — compra única, atrás de `LicenseGateway` |
| Bússola | Android SensorManager — `TYPE_ROTATION_VECTOR` + `GeomagneticField` |
| Compartilhamento | `Intent.ACTION_SEND` |
| Analytics/crash | Firebase Analytics + Crashlytics |
| Avaliação in-app | Play In-App Review API |
| i18n | Android String Resources (`values-XX`) |
| Performance | Baseline Profile + Macrobenchmark (módulo `:macrobenchmark`) |

---

## Estrutura do Projeto

```
app/src/main/java/br/com/ghfsoftware/topowalk/
│
├── MainActivity.kt
├── di/
│   └── AppContainer.kt               # Raiz de composição manual (não Hilt) — todo o grafo do app numa tela
│
├── billing/                          # Licença Pro — regra pura, SDK numa borda só
│   ├── LicenseResolver.kt            # Decide a licença. Distingue "não comprou" de "Play não respondeu"
│   ├── ProLicense.kt                 # Estado observável + cache; concessão vitalícia por cima
│   ├── LicenseGateway.kt             # Interface + ProOffer (Loading/Available/Unavailable)
│   ├── PlayLicenseGateway.kt         # Única classe que toca o BillingClient
│   ├── FakeLicenseGateway.kt         # Debug e teste; o R8 a remove do release
│   └── promo/                        # Migração do Pro legado (T-030) — temporário, ver DECOMISSIONAMENTO.md
│       ├── PromoCodeService.kt       # Interface + PromoClaimOutcome (cada recusa é um caso)
│       ├── DeviceIdHash.kt           # SHA-256 salgado do Android ID; o cru nunca sai do aparelho
│       ├── FirebasePromoCodeService.kt # Única classe que toca Firebase; App Check sob demanda
│       └── FakePromoCodeService.kt   # Debug e teste
│
├── domain/                           # Lógica pura, sem Android
│   ├── MigrationState.kt             # O que a tela de migração mostra; o Play vence o código guardado
│   ├── StakeOut.kt                   # computeStakeOut, tolerância por equipamento, azimute verdadeiro
│   ├── HeadingFilter.kt              # Suavização da bússola no círculo (seno/cosseno), não no número
│   ├── LocalPlane.kt                 # Projeção lat/lon → metros, base do DXF
│   ├── NetArea.kt                    # Área líquida: desconta anéis, julga fora/sobreposto
│   ├── ExclusionOverlay.kt           # O que de cada anel vira furo e o que vira só contorno
│   ├── ImageDownscale.kt             # Subamostragem e proporção, compartilhadas por logo e foto
│   ├── PhotoConstraints.kt           # Teto por medição, tamanho e qualidade da foto
│   ├── PositionAverage.kt            # Média de leituras GPS + modos de captura (F-14)
│   └── LogoConstraints.kt            # Aceita/reduz o logo antes de decodificar
│
├── data/
│   ├── PreferencesManager.kt         # Preferências: receptor externo, altura de antena, licença em cache
│   ├── PdfBranding.kt                # Identidade visual do laudo (F-07), com normalização
│   ├── BrandingStore.kt              # Persistência da identidade visual
│   ├── LogoStore.kt                  # Copia e reduz o logo para dentro do app (nunca guarda a URI)
│   ├── model/
│   │   ├── TopoPoint.kt              # Lat, lon, altitude, fonte (AltitudeSource), precisão GPS, label opcional
│   │   └── Waypoint.kt               # Ponto de interesse (F-09) — fora de todo cálculo
│   ├── photo/                        # Fotos de campo (F-03)
│   │   └── PhotoStore.kt             # Copia, gira pelo EXIF e reduz para dentro do app
│   ├── io/                           # Importação de arquivos externos (F-18) — puro, sem Android
│   │   ├── ImportedLayer.kt          # Modelo da camada + limites + resultado da importação
│   │   ├── GeoImporter.kt            # Porta de entrada: detecta formato, aplica limites, abre KMZ
│   │   ├── GeoJsonLayerParser.kt     # GeoJSON — [lon, lat, alt], Feature/Geometry/Collection
│   │   ├── KmlLayerParser.kt         # KML/KMZ — Placemark, MultiGeometry; anel interno é da F-21
│   │   ├── GpxLayerParser.kt         # GPX — wpt vira ponto, trkseg/rte viram linha
│   │   ├── CsvLayerParser.kt         # CSV — separador detectado, RFC 4180, colunas por cabeçalho
│   │   ├── SecureXml.kt              # SAX com DOCTYPE recusado — defesa contra XXE
│   │   ├── LayerArea.kt              # Área líquida da camada, pelo mesmo NetArea do medido
│   │   ├── LayerImportManager.kt     # Caso de uso: ler, interpretar, gravar
│   │   └── DocumentSource.kt         # Borda de leitura via Storage Access Framework
│   ├── backup/                       # Backup e restauração do histórico
│   │   ├── BackupFile.kt             # Formato do arquivo (envelope versionado)
│   │   ├── BackupCodec.kt            # Codifica/decodifica; recusa arquivo de versão futura
│   │   ├── BackupManager.kt          # Caso de uso: exportar / restaurar
│   │   └── BackupStorage.kt          # Borda de arquivo via Storage Access Framework
│   ├── repository/
│   │   ├── MeasurementRepository.kt  # Porta única de I/O do histórico (save/update/delete/findById)
│   │   ├── DraftRepository.kt        # Rascunho do levantamento em andamento
│   │   ├── ImportedLayerRepository.kt # Camadas importadas: cabeçalho para a lista, geometria sob demanda
│   │   ├── PhotoRepository.kt        # Fotos: arquivo e linha sempre juntos, na ordem certa
│   │   └── BackupRepository.kt       # Exportar tudo / restaurar sem duplicar
│   └── db/
│       ├── AppDatabase.kt            # Room database (schema versionado, exportSchema = true)
│       ├── Migrations.kt             # Migrações explícitas (fallbackToDestructiveMigration proibido)
│       ├── MeasurementDao.kt         # Queries + PagingSource
│       ├── MeasurementEntity.kt      # Entidade persistida
│       ├── DraftMeasurementEntity.kt # Rascunho em andamento, linha única
│       ├── ImportedLayerEntity.kt    # Camada importada (geometria em JSON)
│       └── ImportedLayerDao.kt       # Lista observável, leitura e remoção de camadas
│
├── sensors/
│   ├── BarometerSensor.kt            # Leitura de pressão + calibração de offset
│   ├── Compass.kt                    # Interface da bússola + declinação magnética
│   └── RotationVectorCompass.kt      # TYPE_ROTATION_VECTOR + GeomagneticField
│
├── location/                         # Pipeline do receptor GNSS/RTK externo
│   ├── GnssTransport.kt              # Interface de stream de bytes
│   ├── BluetoothSppTransport.kt      # Implementação real via Bluetooth Classic (SPP)
│   ├── ReplayTransport.kt            # Reproduz um log NMEA (receptor simulado / testes)
│   ├── BluetoothPairedDevices.kt     # Lista de dispositivos Bluetooth pareados
│   ├── NmeaStreamBuffer.kt           # Fragmenta o stream em linhas NMEA completas
│   ├── NmeaParser.kt                 # Parser das sentenças GGA/GST/RMC
│   ├── GnssFix.kt                    # Fix consolidado: posição, altitude, qualidade
│   ├── PointBuilder.kt               # Decide a fonte (externo/barômetro/GPS) de cada ponto
│   └── ExternalGnssManager.kt        # Ciclo de vida da conexão + GnssFixAssembler + StateFlow
│
├── ui/
│   ├── TopoViewModel.kt              # Estado e lógica de medição, edição e continuação de levantamento
│   ├── HistoryViewModel.kt           # Paginação do histórico + backup/restauração
│   ├── FixQualityUi.kt               # Apresentação da qualidade do fix (RTK FIX/FLOAT etc.)
│   ├── pro/
│   │   ├── ProViewModel.kt           # Fluxo de compra e restauração + eventos de funil
│   │   └── ProMigrationViewModel.kt  # Migração do Pro legado (T-030) — fila, código, resgate
│   ├── branding/
│   │   └── BrandingViewModel.kt      # Rascunho da identidade visual do PDF
│   ├── layers/
│   │   └── LayersViewModel.kt        # Camadas importadas: lista, importação e camada aberta
│   ├── photos/
│   │   └── PhotosViewModel.kt        # Fotos do levantamento aberto + gate da licença no PDF
│   ├── stakeout/
│   │   └── StakeOutViewModel.kt      # Locação — recebe posição do TopoViewModel, não tem fonte própria
│   ├── navigation/
│   │   ├── AppNavigation.kt          # Só o mapa de destinos
│   │   ├── Routes.kt                 # Uma função por rota, com gate de licença e paywall
│   │   ├── SettingsRoutes.kt         # Rotas de Configurações — hub, identidade do laudo e migração do Pro
│   │   ├── LayersRoute.kt            # Rota das camadas importadas, com o gate no vértice
│   │   └── StakeOutTarget.kt
│   ├── screens/
│   │   ├── OnboardingScreen.kt       # Tutorial inicial (primeira execução)
│   │   ├── HomeScreen.kt             # Fiação da captura de pontos (desenho em ui/screens/home/)
│   │   ├── SettingsScreen.kt         # Hub de configurações — receptor externo, calibração, laudo
│   │   ├── ProMigrationScreen.kt     # Levar o Pro legado para a conta Google (T-030)
│   │   ├── ExternalGpsScreen.kt      # Fiação do receptor GNSS/RTK externo
│   │   ├── ResultsScreen.kt          # Fiação de métricas, gráficos e exportação
│   │   ├── HistoryScreen.kt          # Fiação do histórico (desenho em ui/screens/history/)
│   │   ├── StakeOutScreen.kt         # Locação (Pro)
│   │   ├── LayersScreen.kt           # Fiação das camadas importadas (desenho em ui/screens/layers/)
│   │   ├── PdfBrandingScreen.kt      # Personalização do laudo (Pro)
│   │   ├── home/                     # Diálogos e cartões da captura: rótulo, ações do ponto, rascunho…
│   │   ├── history/                  # Cartão, detalhe, backup, continuar edição, escolha do ponto a locar
│   │   ├── layers/                   # Lista, estado vazio, folha da camada e mapa da camada
│   │   ├── stakeout/                 # Seta, distância e estado de chegada
│   │   ├── branding/                 # Campos, paleta de cor e escolha do logo
│   │   ├── help/                     # Cartão do Pro e paywall dentro da Ajuda
│   │   └── HelpScreen.kt             # Tutorial do app e FAQ
│   ├── components/
│   │   ├── ElevationProfileChart.kt  # Perfil 2D de elevação
│   │   ├── IsometricPolygonChart.kt  # Vista 3D isométrica
│   │   ├── ChartTabs.kt              # Abas de gráfico compartilhadas entre telas
│   │   ├── ProUpgradeBottomSheet.kt  # Paywall — preço sempre do Play, nunca literal
│   │   ├── ComingSoonSheet.kt        # Fake door; some quando a superfície Pro liga
│   │   ├── OsmMapView.kt             # Mapa OSM via osmdroid (AndroidView)
│   │   └── SegmentsTable.kt          # Tabela colapsável de detalhes por segmento
│   └── theme/
│       └── Theme.kt                  # Material 3 — paleta Terrain
│
└── util/
    ├── TopoCalculator.kt             # Haversine, Pitágoras, arctan, área de polígono
    ├── TerrainMetrics.kt             # Declividade %, ganho e perda de elevação
    ├── PdfGenerator.kt               # Relatório A4 paginado (i18n via context.getString)
    ├── GeoExporter.kt                # Exportação GeoJSON, KML e GPX, com rótulos de ponto
    ├── DxfExporter.kt                # DXF R12 ASCII (Pro) — Locale.US obrigatório
    ├── CsvExporter.kt                # CSV em dois arquivos (Pro) — RFC 4180 + BOM
    ├── PdfAreaSection.kt             # Bloco de área do laudo: bruta, descontada e líquida
    ├── PdfPhotoPage.kt               # Página de fotos do laudo, em grade 2×2 (Pro)
    ├── PdfWaypointSection.kt         # Seção de pontos de interesse do laudo
    ├── WaypointLabels.kt             # Nome de cada ícone de waypoint, num lugar só
    ├── AreaUnit.kt                   # Conversão m² → ha / alqueires
    ├── AnalyticsHelper.kt            # Eventos do Firebase Analytics (inclui o funil de compra)
    ├── CrashReporter.kt              # Non-fatals do Crashlytics
    └── ReviewHelper.kt               # Fluxo de avaliação in-app (Play In-App Review)
```

---

## Como Executar

### Pré-requisitos

- Android Studio Hedgehog (2023.1) ou superior
- JDK 17
- Android SDK com API 36 instalada

### Build

```bash
# Debug
./gradlew assembleDebug

# Release
./gradlew assembleRelease
```

O APK gerado estará em `app/build/outputs/apk/`.

### Instalação direta no dispositivo

```bash
./gradlew installDebug
```

### Testes

```bash
# Testes unitários (JVM, Robolectric)
./gradlew testDebugUnitTest

# Testes instrumentados de UI (requer dispositivo/emulador conectado)
./gradlew connectedDebugAndroidTest
```

---

## Relatório PDF

O PDF gerado em A4 (595 × 842 pts) contém:

- **Cabeçalho** com o nome da medição — e, no Pro, com o logo, o nome da empresa, o responsável técnico, o registro profissional e a cor escolhida
- **Data e observações** da medição
- **Pontos de medição** — coordenadas, altitude, fonte (receptor externo, barômetro ou GPS) e nome, quando o ponto foi nomeado
- **Resultados totais** — grid com as grandezas calculadas e área (quando aplicável)
- **Tabela de segmentos** — detalhamento por segmento (distância, desnível, ângulo, azimute, distância inclinada)
- **Perfil topográfico** — gráfico 2D vetorial de elevação
- **Vista 3D isométrica** — página dedicada para polígonos (≥ 3 pontos)
- **Rodapé** com versão do app e data de geração — no Pro, o nome da empresa substitui o crédito padrão, com uma nota livre opcional

O arquivo é salvo temporariamente no `cacheDir` do app e compartilhado via `FileProvider`, sem necessidade de permissão de armazenamento externo. O conteúdo do PDF é gerado no idioma ativo do dispositivo.

---

## Privacidade

O TopoWalk **não tem anúncios**. Levantamentos, coordenadas e PDFs ficam no aparelho — nada disso sai para servidor nenhum. O app envia apenas eventos de uso (Firebase Analytics) e relatórios de falha (Crashlytics); qualquer trecho de dado bruto amostrado num relatório de falha é truncado a 16 caracteres e não carrega coordenadas. O identificador de publicidade (`AD_ID`) é removido explicitamente do manifesto, mesmo vindo por transitividade do Firebase.

A compra do Pro é processada **inteiramente pelo Google Play**: nenhum dado de pagamento passa pelo app, e nenhum identificador de conta é enviado ao Play (o `obfuscatedAccountId` não é usado — o TopoWalk não tem contas). O app recebe de volta apenas "existe ou não uma compra ativa neste aparelho".

Os dados da empresa no laudo (nome, responsável técnico, registro profissional, logo) ficam **somente no aparelho** e não aparecem em nenhum evento de analytics nem em relatório de falha. Eles só deixam o dispositivo dentro de um PDF que o próprio usuário decide compartilhar — que é o objetivo do recurso.

**Uma exceção, temporária e delimitada:** a migração do Pro legado (T-030) é o único recurso que
guarda algo num servidor do GHF Software — um identificador do aparelho **embaralhado**, um
identificador de sessão anônima, a data do pedido e o código entregue. Sem nome, sem e-mail, sem
login, e **sem tocar em nenhum dado de levantamento**. Só acontece se o usuário abrir a tela e
pedir o código: quem nunca abre não estabelece conexão alguma. O serviço é desligado ao fim da
migração — ver [`DECOMISSIONAMENTO.md`](DECOMISSIONAMENTO.md).

Detalhamento completo em [`PRIVACY_POLICY.md`](PRIVACY_POLICY.md).

---

## Desenvolvedor

**GHF Software** — `br.com.ghfsoftware`
