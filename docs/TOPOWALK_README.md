# TopoWalk

Aplicativo Android para **levantamento topográfico de campo** usando GPS e barômetro do dispositivo. Suporta medições com múltiplos pontos, cálculo de área de polígonos, visualização 3D isométrica, mapa OpenStreetMap, histórico persistente com exportação e relatório em PDF.

---

## Funcionalidades

### Medição topográfica
- Captura de **2 ou mais pontos** georreferenciados em sequência
- Cálculo automático de grandezas por segmento e totais
- Suporte a polígono fechado (≥ 3 pontos) com cálculo de área

### Altitude
Prioriza o **barômetro** quando disponível (`h = 44330 × (1 − (p/p₀)^(1/5.255))`) com calibração manual de offset, e fallback automático para a altitude GPS quando o sensor de pressão não está presente.

### Visualizações
- **Perfil 2D** — gráfico vetorial de elevação ao longo da distância percorrida
- **Vista 3D isométrica** — projeção isométrica do polígono com altitude real (apenas ≥ 3 pontos)
- **Mapa OpenStreetMap** — sobreposição da demarcação sobre mapa de relevo (OpenTopoMap), sem API key

### Histórico
- Salvamento local das medições com nome e observações opcionais
- Lista com **scroll infinito** (Jetpack Paging 3) para performance em grandes volumes
- Detalhes de cada medição com tabela de segmentos, gráficos e exportação

### Exportação
- **PDF** — relatório A4 completo com cabeçalho, pontos, resultados, tabela de segmentos, perfil 2D e vista 3D
- **GeoJSON** — compatível com QGIS, ArcGIS e demais SIGs
- **KML** — compatível com Google Earth e aplicações similares

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
| Desnível (ΔH) | Diferença de altitude entre os pontos | Altitude barométrica ou GPS |
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
| Área do Polígono | Área da demarcação fechada (≥ 3 pontos), em m², ha ou alqueires |

---

## Requisitos

- Android 7.0 (API 24) ou superior
- GPS (localização precisa)
- Permissões: `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `INTERNET`
- Barômetro (opcional — melhora a precisão da altitude)
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
| Altitude | Android SensorManager — `TYPE_PRESSURE` |
| Banco de dados | Room 2.7 + KSP |
| Paginação | Jetpack Paging 3 (`room-paging`) |
| Mapa | osmdroid 6.1.20 — OpenStreetMap / OpenTopoMap |
| PDF | Android `PdfDocument` API + `FileProvider` |
| Exportação geo | GeoJSON e KML gerados internamente |
| Compartilhamento | `Intent.ACTION_SEND` |
| i18n | Android String Resources (`values-XX`) |

---

## Estrutura do Projeto

```
app/src/main/java/br/com/ghfsoftware/topowalk/
│
├── MainActivity.kt
│
├── data/
│   ├── model/
│   │   ├── TopoPoint.kt              # Lat, lon, altitude, fonte, precisão GPS
│   │   └── AltitudeSource.kt         # Enum: BAROMETER | GPS
│   └── db/
│       ├── AppDatabase.kt            # Room database
│       ├── MeasurementDao.kt         # Queries + PagingSource
│       └── MeasurementEntity.kt      # Entidade persistida
│
├── sensors/
│   └── BarometerSensor.kt            # Leitura de pressão + calibração de offset
│
├── ui/
│   ├── TopoViewModel.kt              # Estado e lógica de medição
│   ├── HistoryViewModel.kt           # Paginação do histórico
│   ├── TopoResult.kt                 # Modelo de resultado (in-memory)
│   ├── navigation/
│   │   └── AppNavigation.kt
│   ├── screens/
│   │   ├── HomeScreen.kt             # Captura de pontos + GPS badge
│   │   ├── ResultsScreen.kt          # Métricas + gráficos + exportação
│   │   └── HistoryScreen.kt          # Lista paginada + bottom sheet de detalhes
│   ├── components/
│   │   ├── TopoCharts.kt             # ElevationProfileChart, IsometricPolygonChart
│   │   ├── OsmMapView.kt             # Mapa OSM via osmdroid (AndroidView)
│   │   └── SegmentsTable.kt          # Tabela colapsável de detalhes por segmento
│   └── theme/
│       └── Theme.kt                  # Material 3 — paleta Terrain
│
└── util/
    ├── TopoCalculator.kt             # Haversine, Pitágoras, arctan, área de polígono
    ├── PdfGenerator.kt               # Relatório A4 paginado (i18n via context.getString)
    ├── GeoExporter.kt                # Exportação GeoJSON e KML
    └── AreaFormatter.kt              # Conversão m² → ha / alqueires
```

---

## Como Executar

### Pré-requisitos

- Android Studio Hedgehog (2023.1) ou superior
- JDK 11
- Android SDK com API 35 instalada

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

---

## Relatório PDF

O PDF gerado em A4 (595 × 842 pts) contém:

- **Cabeçalho** com identidade visual e nome da medição
- **Data e observações** da medição
- **Pontos de medição** — coordenadas, altitude e fonte (barômetro ou GPS)
- **Resultados totais** — grid com as grandezas calculadas e área (quando aplicável)
- **Tabela de segmentos** — detalhamento por segmento (distância, desnível, ângulo, azimute, distância inclinada)
- **Perfil topográfico** — gráfico 2D vetorial de elevação
- **Vista 3D isométrica** — página dedicada para polígonos (≥ 3 pontos)
- **Rodapé** com versão do app e data de geração

O arquivo é salvo temporariamente no `cacheDir` do app e compartilhado via `FileProvider`, sem necessidade de permissão de armazenamento externo. O conteúdo do PDF é gerado no idioma ativo do dispositivo.

---

## Desenvolvedor

**GHF Software** — `br.com.ghfsoftware`
