# EclipseGo

EclipseGo é um aplicativo Android nativo (Kotlin + Jetpack Compose) que mostra se um eclipse solar ou lunar é visível a partir de uma localização escolhida pelo usuário, além dos horários do evento (início, pico e fim).

O aplicativo funciona **totalmente offline**: todos os dados de eclipses, cidades/localizações e os cálculos de visibilidade são empacotados no próprio dispositivo — não há chamadas de rede. Veja a [política de privacidade](docs/PRIVACY_POLICY.md) e a [especificação completa do produto](docs/SPEC.md) (em português).

## Principais características

- **100% offline** — nenhuma dependência de internet ou backend próprio.
- **Três modos de localização**: minha localização (GPS), melhor localização visível mais próxima, e localização personalizada (busca por cidade).
- **Calendário anual de eclipses** e busca por data/evento.
- **Linha do tempo interativa** do evento (início → pico → fim).

## Requisitos

- Android Studio (versão compatível com AGP 8.13.x / Kotlin 2.0.21)
- JDK 11
- Android SDK: `minSdk` 26, `targetSdk`/`compileSdk` 35

## Build e testes

Todos os comandos abaixo usam o Gradle Wrapper a partir da raiz do repositório:

```bash
./gradlew build                    # build completo
./gradlew testDebugUnitTest        # testes unitários (JVM, Robolectric)
./gradlew connectedAndroidTest     # testes instrumentados de UI (requer device/emulador)
./gradlew lint                     # lint do Android
```

Rodar uma classe ou método de teste específico:

```bash
./gradlew testDebugUnitTest --tests "br.com.ghfsoftware.eclipsego.domain.VisibilityCalculatorTest"
./gradlew testDebugUnitTest --tests "br.com.ghfsoftware.eclipsego.domain.VisibilityCalculatorTest.someMethodName"
```

Testes instrumentados (Compose UI) podem ser filtrados da mesma forma com `connectedAndroidTest --tests "..."`.

## Arquitetura

MVVM com um único `EclipseViewModel` (`ui/viewmodel/EclipseViewModel.kt`) orquestrando o app; não há biblioteca de navegação — `EclipseGoApp.kt` é uma máquina de estados manual (`Screen`: SPLASH → MAIN/CALENDAR/SEARCH) controlada por `uiState.loading` e uma duração mínima de splash.

**Fluxo de dados**: `data/source` (carregadores de assets/Room) → `data/repository` (acesso somente leitura, cacheado em memória) → `domain` (funções puras de cálculo) → `EclipseViewModel` (orquestração, exposta como um único `StateFlow<EclipseUiState>`) → `ui/screens` (telas Compose stateless dirigidas inteiramente por `EclipseUiState`).

- **`data/model`**: data classes simples (`Eclipse`, `City`, `Geo`, `LocalCircumstances`, `EclipseType`).
- **`data/source`**: carrega os dados brutos.
  - `EclipseDataSource` lê `eclipses.json` dos assets.
  - Cidades são armazenadas via Room (`CityDatabase`, `CityDao`, `CityEntity`) em vez de parseadas a cada abertura do app — `CityDataSource` semeia o banco a partir de `cities.json` na primeira execução (~34 mil linhas). `CityEntity.normalize()` é usado para busca insensível a acentos/maiúsculas.
- **`data/repository`**: `EclipseRepository` e `CityRepository` são as únicas interfaces com as quais o ViewModel conversa. `DefaultCityRepository` cacheia `cityDao.getAll()` mapeado para objetos de domínio em um `lazy`.
- **`domain`**: lógica de cálculo pura e testável — `VisibilityCalculator` (se um eclipse é visível a partir de uma coordenada, e horários locais de início/pico/fim), `NearestVisibleLocationFinder` (cidade visível mais próxima), `TimelineMapper` (posição do slider ↔ progresso do evento), `GeoMath` (auxiliares de distância/azimute geográficos). Sem dependências de Android — é aqui que ficam os testes unitários de domínio.
- **`location`**: `DeviceLocationProvider` encapsula o `FusedLocationProvider`; usa uma cidade padrão (`CityRepository.defaultCity()`) como fallback quando GPS/permissão não estão disponíveis.
- **`ui/viewmodel`**: `EclipseUiState` é o único objeto de estado imutável renderizado por todas as telas; `EclipseViewModel` o modifica via `MutableStateFlow`. `LocationMode` (MINHA / MELHOR / PERSONALIZADA) representa as três abas de seleção de localização da spec.
- **`ui/screens`**: `SplashScreen`, `MainScreen` (o "telão" — visão do céu, seletor de localização, painel de dados do evento, slider da linha do tempo), `CalendarScreen` (calendário anual de eclipses), `SearchScreen` (busca por data/eclipse). Todas stateless, recebendo `EclipseUiState` e callbacks.
- **`ui/calendar`, `ui/format`, `ui/icons`, `ui/theme`**: modelo da grade do calendário, formatação de data/hora, ícones customizados de eclipse e tema Compose, respectivamente.

## Testes

Testes unitários (`app/src/test`) espelham os pacotes `data/repository`, `data/source`, `domain` e `ui/viewmodel`, usando JUnit + Truth + Robolectric + `kotlinx-coroutines-test` (veja `MainDispatcherRule.kt`, `TestFixtures.kt`). Testes instrumentados Compose (`app/src/androidTest`) cobrem `MainScreen`, `CalendarScreen` e `SearchScreen` (`UiTestFixtures.kt`).

## Documentação adicional

- [docs/SPEC.md](docs/SPEC.md) — especificação completa do produto (em português).
- [docs/PRIVACY_POLICY.md](docs/PRIVACY_POLICY.md) — política de privacidade do aplicativo.
