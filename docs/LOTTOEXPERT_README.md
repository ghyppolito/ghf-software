# LottoExpert

**LottoExpert** é uma solução de engenharia estatística para apostadores das Loterias da Caixa Econômica Federal (Mega-Sena, Lotofácil, Quina, Lotomania, Timemania, Dupla Sena, Dia de Sorte, +Milionária e Super Sete). O aplicativo foi desenhado com foco em **processamento local e privacidade**, utilizando algoritmos matemáticos para gerar matrizes de fechamento diretamente no dispositivo do usuário, sem dependência de servidores externos.

---

## Principais Funcionalidades

### Gerador de Jogos
- **Motor de Fechamentos (Math Engine):** Implementação de combinações matemáticas C(n,k) via `Sequence` para evitar estouro de memória em grandes desdobramentos.
- **Seleção de Dezenas por Volante:** Suporte completo ao desdobramento das loterias — o usuário escolhe quantas dezenas jogar por volante (dentro do range oficial da Caixa), com cálculo automático do custo por volante (`initialCost × C(n, drawSize)`).
- **Filtros Base:** Paridade par/ímpar, equilíbrio de primos, prevenção de sequências longas, somatória e moldura.
- **Filtros Pro:** Distribuição por quadrantes, gap médio entre dezenas e priorização de dezenas atrasadas (ciclo).
- **Probabilidade Real:** Exibição da chance matemática exata de acerto baseada no pool de dezenas selecionado.

### Resultados e Sincronização
- **Sincronização com API Oficial da CEF:** Consome diretamente a API pública da Caixa Econômica Federal (`servicebus2.caixa.gov.br/portaldeloterias/api/`) para obter os resultados oficiais.
- **Histórico Offline:** Armazena os últimos concursos localmente via Room Database para consulta instantânea sem internet.
- **Agendamento Inteligente (WorkManager + AlarmManager):** Sincronização diária às 21h, com filtro por dia de sorteio de cada loteria — a Mega-Sena, por exemplo, só sincroniza às quartas e sábados.

### Jogos Salvos
- **Conferência Automática:** Cruza os tickets salvos com os últimos sorteios e exibe acertos com destaque.
- **Jogos Próprios:** O usuário pode criar e salvar manualmente seus próprios jogos através de um seletor de dezenas interativo.
- **Distinção Visual:** Cards diferenciam jogos gerados pelo algoritmo (ícone de foguete) de jogos criados pelo usuário (ícone de lápis), com data/hora de criação exibida em cada card.

### Conferência por OCR (Check-Scan)
- **Scanner de Bilhete:** Usa a câmera do dispositivo (CameraX) e reconhecimento de texto com ML Kit para escanear um bilhete físico e identificar as dezenas automaticamente.
- **Cruzamento Instantâneo:** Compara as dezenas extraídas com os últimos sorteios e exibe a premiação estimada.
- **Processamento 100% Local:** O ML Kit executa o reconhecimento de texto no próprio dispositivo — nenhuma imagem é enviada para servidores externos.

### Compartilhamento e Exportação
- **PDF Promocional:** Gera um PDF com layout comercial — header com gradiente na cor da loteria, bolas numeradas e rodapé promocional do app. Compartilhado via seletor de apps (WhatsApp, Drive, e-mail etc.).
- **Texto Promocional:** Compartilhamento via texto formatado com emojis e bloco de divulgação do app.

### Outras
- **Estatísticas:** Frequência, atraso e taxa de aparecimento de cada dezena nos últimos sorteios.
- **Backtesting:** Simulação retroativa para avaliar o desempenho de estratégias em sorteios passados.
- **Monetização:** Integração com Google Play Billing Library para desbloqueio de recursos premium.

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Kotlin 1.9+ |
| UI | Jetpack Compose + Material Design 3 |
| Injeção de Dependências | Dagger Hilt |
| Persistência | Room Database v3 (com migrations explícitas) |
| Rede | Retrofit + OkHttp |
| Concorrência | Kotlin Coroutines + Flow |
| Background Work | WorkManager (HiltWorker) + AlarmManager |
| Câmera | CameraX (camera-camera2, camera-lifecycle, camera-view) |
| OCR | ML Kit Text Recognition |
| Billing | Google Play Billing Library 6.1 |
| Testes | JUnit 4 + Mockito-Kotlin + kotlinx-coroutines-test |

---

## Estrutura do Projeto (Clean Architecture)

```
app/
├── data/
│   ├── billing/        # BillingManager (Google Play)
│   ├── local/          # Room: entities, DAOs, migrations, converters
│   ├── remote/         # Retrofit API + DTOs
│   ├── repository/     # Implementações dos repositórios
│   └── worker/         # SyncWorker (HiltWorker) + SyncAlarmReceiver
├── di/                 # Módulos Hilt (Database, Network, UseCases)
├── domain/
│   ├── export/         # PdfExporter
│   ├── math/           # CombinatoricsEngine, FilterEngine, MatrixGenerator
│   ├── model/          # LotteryConfig, DrawResult, etc.
│   ├── ocr/            # BilhetParser
│   ├── repository/     # Interfaces de repositório
│   ├── strategy/       # LotteryStrategy por loteria + Factory
│   └── usecase/        # ComputeNumberStats, CheckTicketMatches
└── ui/
    ├── navigation/     # NavGraph + Screen
    ├── screens/        # dashboard, generator, results, statistics,
    │                   # backtesting, savedgames, scan
    └── theme/          # Tema Material 3
```

---

## Como Executar

1. Clone o repositório.
2. Abra no **Android Studio Hedgehog (2023.1.1) ou superior**.
3. Configure o JDK para o **Java 17**.
4. Sincronize o Gradle e aguarde o download das dependências.
5. Execute `./gradlew assembleDebug` ou rode diretamente no Android Studio.

Para rodar os testes unitários:
```bash
./gradlew test
```

---

## Documentação Adicional

| Documento | Descrição |
|---|---|
| [SPECS.md](docs/SPECS.md) | Especificação técnica do MVP (Sprints 1–5) |
| [SPECS2.md](docs/SPECS2.md) | Roadmap de funcionalidades futuras |
| [ASO_METADATA.md](docs/ASO_METADATA.md) | Estratégia de loja (título, descrição, keywords) |
| [PRIVACY_POLICY.md](docs/PRIVACY_POLICY.md) | Política de Privacidade |

---

## Licença

Desenvolvido por **Gustavo Hyppolito**. Uso restrito conforme termos de licenciamento acordados.
