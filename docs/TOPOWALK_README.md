# TopoWalk

Aplicativo Android para **levantamento topográfico de campo** usando GPS e barômetro do dispositivo. Suporta medições com múltiplos pontos, cálculo de área de polígonos, declividade e desnível, visualização 3D isométrica, mapa OpenStreetMap, histórico persistente e editável com backup/restauração, e exportação em PDF, GeoJSON, KML e GPX.

100% gratuito: sem anúncios e sem compras no app.

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

### Exportação
- **PDF** — relatório A4 completo com cabeçalho, pontos, resultados, tabela de segmentos, perfil 2D e vista 3D
- **GeoJSON** — compatível com QGIS, ArcGIS e demais SIGs
- **KML** — compatível com Google Earth e aplicações similares
- **GPX** — trilha e waypoints, compatível com OsmAnd, Wikiloc e Garmin
- Todos os formatos carregam os nomes que você deu aos pontos

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
├── data/
│   ├── PreferencesManager.kt         # Preferências: receptor externo, altura de antena, último dispositivo
│   ├── model/
│   │   └── TopoPoint.kt              # Lat, lon, altitude, fonte (AltitudeSource), precisão GPS, label opcional
│   ├── backup/                       # Backup e restauração do histórico
│   │   ├── BackupFile.kt             # Formato do arquivo (envelope versionado)
│   │   ├── BackupCodec.kt            # Codifica/decodifica; recusa arquivo de versão futura
│   │   ├── BackupManager.kt          # Caso de uso: exportar / restaurar
│   │   └── BackupStorage.kt          # Borda de arquivo via Storage Access Framework
│   ├── repository/
│   │   ├── MeasurementRepository.kt  # Porta única de I/O do histórico (save/update/delete/findById)
│   │   ├── DraftRepository.kt        # Rascunho do levantamento em andamento
│   │   └── BackupRepository.kt       # Exportar tudo / restaurar sem duplicar
│   └── db/
│       ├── AppDatabase.kt            # Room database (schema versionado, exportSchema = true)
│       ├── Migrations.kt             # Migrações explícitas (fallbackToDestructiveMigration proibido)
│       ├── MeasurementDao.kt         # Queries + PagingSource
│       ├── MeasurementEntity.kt      # Entidade persistida
│       └── DraftMeasurementEntity.kt # Rascunho em andamento, linha única
│
├── sensors/
│   └── BarometerSensor.kt            # Leitura de pressão + calibração de offset
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
│   ├── navigation/
│   │   └── AppNavigation.kt
│   ├── screens/
│   │   ├── OnboardingScreen.kt       # Tutorial inicial (primeira execução)
│   │   ├── HomeScreen.kt             # Fiação da captura de pontos (desenho em ui/screens/home/)
│   │   ├── ExternalGpsScreen.kt      # Fiação do receptor GNSS/RTK externo
│   │   ├── ResultsScreen.kt          # Fiação de métricas, gráficos e exportação
│   │   ├── HistoryScreen.kt          # Fiação do histórico (desenho em ui/screens/history/)
│   │   ├── home/                     # Diálogos e cartões da captura: rótulo, ações do ponto, rascunho…
│   │   ├── history/                  # Cartão, detalhe, backup, continuar edição
│   │   └── HelpScreen.kt             # Tutorial do app e FAQ
│   ├── components/
│   │   ├── TopoCharts.kt             # ElevationProfileChart, IsometricPolygonChart
│   │   ├── ChartTabs.kt              # Abas de gráfico compartilhadas entre telas
│   │   ├── ComingSoonSheet.kt        # Fake door de DXF/CSV — mede prioridade, não gera arquivo
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
    ├── AreaUnit.kt                   # Conversão m² → ha / alqueires
    ├── AnalyticsHelper.kt            # Eventos do Firebase Analytics (inclui o fake door)
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

- **Cabeçalho** com identidade visual e nome da medição
- **Data e observações** da medição
- **Pontos de medição** — coordenadas, altitude, fonte (receptor externo, barômetro ou GPS) e nome, quando o ponto foi nomeado
- **Resultados totais** — grid com as grandezas calculadas e área (quando aplicável)
- **Tabela de segmentos** — detalhamento por segmento (distância, desnível, ângulo, azimute, distância inclinada)
- **Perfil topográfico** — gráfico 2D vetorial de elevação
- **Vista 3D isométrica** — página dedicada para polígonos (≥ 3 pontos)
- **Rodapé** com versão do app e data de geração

O arquivo é salvo temporariamente no `cacheDir` do app e compartilhado via `FileProvider`, sem necessidade de permissão de armazenamento externo. O conteúdo do PDF é gerado no idioma ativo do dispositivo.

---

## Privacidade

O TopoWalk **não tem anúncios e não tem compras no app**. Levantamentos, coordenadas e PDFs ficam no aparelho — nada disso sai para servidor nenhum. O app envia apenas eventos de uso (Firebase Analytics) e relatórios de falha (Crashlytics); qualquer trecho de dado bruto amostrado num relatório de falha é truncado a 16 caracteres e não carrega coordenadas. O identificador de publicidade (`AD_ID`) é removido explicitamente do manifesto, mesmo vindo por transitividade do Firebase.

---

## Desenvolvedor

**GHF Software** — `br.com.ghfsoftware`
