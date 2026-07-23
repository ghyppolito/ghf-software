# LottoExpert

**LottoExpert** é uma solução de engenharia estatística para apostadores das Loterias da Caixa Econômica Federal. O aplicativo foi desenhado com foco em **processamento local e privacidade** — toda a geração de fechamentos, conferência de bilhetes e reconhecimento OCR acontece no próprio dispositivo. Os resultados oficiais dos sorteios são sincronizados via infraestrutura própria no Google Cloud Platform, sem expor dados do usuário a nenhum servidor.

---

## Funcionalidades

### Gerador de Fechamentos (Algoritmo Especialista)
- **Motor Combinatório:** Implementação de C(n,k) via `Sequence` lazy para evitar estouro de memória em desdobramentos grandes.
- **Seleção por Volante:** O usuário escolhe quantas dezenas jogar por volante dentro do range oficial de cada loteria. O custo total é calculado automaticamente em tempo real (`custo_base × C(n, drawSize)`).
- **Filtros Base:** Paridade par/ímpar, somatória da combinação, moldura/borda e dezenas repetidas de sorteios anteriores.
- **Filtros Pro (premium):** Distribuição por quadrantes, gap médio entre dezenas e priorização de dezenas em ciclo de atraso.
- **Probabilidade Real:** Exibição da chance matemática exata de acerto para o pool selecionado via distribuição hipergeométrica.
- **Limite de Budget:** O usuário define o valor máximo a gastar (até R$ 1.000); o gerador produz exatamente o número de jogos cabível nesse budget.
- **Exportação Direta:** Os jogos gerados podem ser exportados como PDF ou salvos na carteira com um toque.

### Resultados e Sincronização
- **Infraestrutura Própria (GCP):** Os resultados são coletados da API pública da Caixa por um Cloud Function (`lottery-sync`) e armazenados em um bucket GCS privado. O app consulta o segundo Cloud Function (`lottery-serve`), nunca a API da Caixa diretamente.
- **Firebase App Check:** Cada requisição ao `lottery-serve` carrega um token de atestação do Play Integrity, garantindo que apenas instalações legítimas do app acessem a infraestrutura.
- **Histórico Offline:** Todo o histórico de concursos é armazenado localmente via Room Database para consulta instantânea sem internet.
- **Sync Inteligente:** Sincronização automática via WorkManager + AlarmManager em 4 janelas diárias (08:30, 12:30, 22:30 e 23:35 BRT, com jitter por dispositivo), enfileirada como trabalho único. Fora das janelas noturnas, loterias cujo último sorteio esperado já está no banco são puladas — corta ~2/3 das requisições diárias.
- **Coleta Horária no Servidor:** O `lottery-sync` varre a API da Caixa de hora em hora (08:30–23:30 BRT), cobrindo os atrasos imprevisíveis da publicação oficial; o `max-age` servido pelo `lottery-serve` acompanha essas janelas.
- **Resiliência e Erros:** OkHttp disk cache (5 MB) reduz requisições redundantes. Sistema de retentativa automática com banners de status e retry manual.
- **Delta Sync:** Apenas os concursos novos são buscados; o histórico já salvo não é baixado novamente.
- **Onboarding e Compliance:** Fluxo guiado para novos usuários, garantindo aceitação de Termos de Uso, Política de Privacidade e avisos de Jogo Responsável (Play Store Ready).

### Meus Jogos (Carteira de Tickets)
- **Conferência Automática:** Cruza todos os tickets salvos com os últimos sorteios e destaca acertos com faixa de premiação (ex: "Quina no Concurso #2850").
- **Agrupamento por Geração:** Jogos gerados em uma mesma sessão são agrupados automaticamente (janela de 10s), facilitando a visualização de fechamentos inteiros.
- **Jogos Próprios:** O usuário cria e salva manualmente seus jogos via seletor de dezenas interativo (bottom sheet).
- **Distinção Visual:** Cards diferenciam jogos gerados pelo algoritmo (ícone foguete) de jogos inseridos manualmente (ícone pessoa), com data e hora de criação.
- **Ativar/Desativar:** Cada jogo pode ser marcado como inativo sem ser excluído, removendo-o das conferências.
- **Exportação em PDF:** Cada grupo de jogos pode ser exportado como PDF e compartilhado via qualquer app (WhatsApp, Drive, e-mail etc.). Usuários free recebem PDF com marca d'água; premium recebem PDF limpo.

### Bolão (Sweepstake)
- **Criação de Bolão:** O usuário cria um bolão informando nome, loteria, número do concurso alvo e total de cotas.
- **Copiar Bolão (Premium):** Reutilize a estrutura de um bolão existente — mesmos jogos e participantes — em um novo concurso com um toque, sem recadastrar nada. Acessível pelo ícone de cópia na lista de bolões.
- **Gerenciamento de Participantes:** Adicione participantes com nome e número de cotas. O valor por cota é calculado automaticamente com base no custo total dos jogos.
- **Vinculação de Jogos:** Associe tickets salvos da carteira ao bolão com um toque.
- **Compartilhamento Multi-Format:**
    - **Links Mágicos (Deep Links):** Gera um convite compacto codificado (GZIP + Base64) que permite importação automática entre dispositivos. Disponível para todos os usuários — canal de aquisição viral.
    - **QR Code:** Card de compartilhamento inclui QR code gerado localmente para convite presencial sem necessidade de digitar link.
    - **PDF de Bolão:** Gera um documento profissional com todos os jogos e detalhes das cotas. Usuários free recebem PDF com marca d'água; premium recebem PDF limpo.
- **Importação Dinâmica:** Detecta convites via link ou via clipboard para rápida adesão a grupos existentes.
- **Conferência do Bolão:** Resultado consolidado do bolão cruzado com os sorteios reais.
- **Regras Freemium:**

    | Feature | Free | Premium |
    |---|---|---|
    | Criar bolão | 1 bolão ativo | Ilimitados |
    | Copiar bolão para novo concurso | — | ✓ |
    | Participantes por bolão | Máximo 10 | Ilimitado |
    | Compartilhar deep link + QR code | ✓ | ✓ |
    | PDF do bolão | Com marca d'água | Limpo |

### Jogos por Concurso e Conferência Automática
- **Participações por Concurso:** Ao salvar um jogo (gerador, scan ou manual) ou tocar em "Joguei de novo", o app registra a participação no concurso escolhido com o **custo congelado** no momento da aposta — é o vínculo jogo↔concurso que sustenta todo o acompanhamento financeiro.
- **Tela "Jogos por Concurso":** Organiza os jogos POR CONCURSO (complementando "Meus Jogos", que agrupa por lote de geração), com seções "Aguardando sorteio" e "Conferidos", resultado oficial ao lado dos jogos e acertos destacados em ouro contra aquele sorteio específico.
- **Registro em Lote:** Registra todos os jogos de um lote de geração em um concurso com um toque, ou copia os jogos de um concurso para outro com o seletor pré-marcado.
- **Conferência Automática (Premium):** Após cada sincronização, as participações pendentes são apuradas com acertos e **prêmio real** (extraído das faixas de premiação do sorteio) e resumidas em uma notificação por loteria. O usuário free confere manualmente, participação a participação.
- **Reconciliação Local:** A apuração roda também na abertura do app e quando um sorteio novo chega pela tela de Resultados — não depende da janela de sync. Idempotente por `checkedAt IS NULL`.
- **Badges por Categoria:** Contador de conferências não vistas independente do de acertos — abrir "Meus Jogos" não apaga o aviso desta tela e vice-versa.
- **Gate Freemium:** Free acompanha até 5 jogos por concurso; o gate vive no use case, valendo para todos os fluxos de registro.

### Meu Desempenho (Dashboard Financeiro — Premium)
- **Saldo Real, Sem Maquiagem:** Total apostado × prêmios recebidos × **saldo** e ROI, por período (Mês / Ano / Tudo). Jogo responsável em primeiro lugar: participações não conferidas contam no apostado e nunca no ganho.
- **Bolões Incluídos:** O rateio usa a cota do próprio usuário (`myShares/totalShares`) sobre custo e prêmio, com a taxa do organizador fora da conta (é repasse, não aposta). Escopos **Tudo / Meus jogos / Bolões**, separando o que você organiza do que você apenas participa.
- **Evolução Mensal:** Barras dos últimos 6 meses, maior prêmio, faixa mais atingida e breakdown por loteria — agregação pura, em uma única leitura das participações.
- **Relatório Mensal:** Worker diário com dedupe mensal notifica o fechamento do mês anterior e abre a tela dedicada (também alcançável pelo dashboard).

### Desdobramentos com Garantia (Premium)
- **Garantia Provada, Não Estimada:** Modo alternativo do Gerador para **Lotomania, Lotofácil e Timemania**: o usuário escolhe mais dezenas que um jogo único e recebe uma matriz fixa com garantia parcial demonstrada ("se X das suas dezenas saírem, algum jogo faz ao menos Y pontos").
- **Provado Offline por ILP:** As matrizes vivem como JSON por loteria em `assets/desdobramentos/` e são geradas e **provadas** por um solver de programação inteira (`tools/desdobramentos/build_wheels.py`) — adversário infactível é a prova. Novas loterias são drop-in.
- **Overlay de Times na Timemania:** Cada jogo recebe um Time do Coração distinto, pulverizando a chance do prêmio do time.

### Estratégias Salvas e Bolão Recorrente (Premium)
- **Presets de Geração:** Salva a configuração completa do gerador (dezenas, filtros, budget) e regenera com um toque. JSON versionado e tolerante a campos desconhecidos. Free salva 1 preset; premium, ilimitados.
- **Bolão Recorrente:** Com o toggle ligado, o bolão é copiado automaticamente para o próximo concurso após o sorteio, com notificação ao organizador. Idempotente por (nome, loteria, concurso destino).

### Alertas Inteligentes (Premium)
- **Filtro de Limiar no Acumulado:** Só notifica acumulados acima do valor que o usuário definir.
- **Dezena Monitorada:** Avisa quando uma dezena escolhida volta a sair após atraso longo ou assume o topo do atraso.
- **Lembrete de Jogo:** Para quem tem o hábito naquela loteria e ainda não registrou participação no concurso de hoje. As notificações têm precedência entre si para nunca duplicar a mesma mensagem.

### Jornadas Guiadas
- **Primeiro Uso:** Checklist "Comece por aqui" na Home conduz pela cadeia que revela o valor do app (escolher loteria → ver resultado → gerar jogos → registrar no concurso → acompanhar → conhecer o bolão). Os passos se marcam sozinhos quando a ação real acontece, e dicas contextuais aparecem no topo das telas do passo corrente.
- **Pós-Compra (Premium):** Checklist "Seu Premium" ataca a descoberta das features compradas — backup, alertas, desdobramento, desempenho e backtesting viram linhas clicáveis que navegam direto para o recurso. Disparado pela transição para assinante, cobrindo também quem restaura a assinatura em outro aparelho.
- **Domínio Puro:** Toda a lógica das duas jornadas é testável sem Android; os componentes de UI são genéricos e servem às duas.

### Conferência por OCR (Check-Scan)
- **Scanner de Bilhete:** Usa CameraX + ML Kit Text Recognition para escanear um bilhete físico e extrair as dezenas automaticamente.
- **Burst Multi-Captura com Consenso:** Um toque no obturador dispara uma sequência de leituras (até 4; 6 no Super Sete) e um jogo só é aceito quando lido de forma idêntica em ≥2 capturas com dominância sobre leituras divergentes — eliminando falsos positivos de captura única (rótulo do jogo lido como dezena, dígito trocado pelo OCR). Leituras contestadas abrem uma grade de revisão com as dezenas em dúvida destacadas.
- **Leitor Dedicado da Lotomania:** A fonte matricial da cartela de 50 números não é reconhecida pelo ML Kit; um leitor próprio por template matching faz até 5 leituras com votação por dezena e abre a revisão pré-marcada.
- **Cruzamento Instantâneo:** Compara as dezenas lidas com os últimos sorteios e exibe a premiação estimada.
- **Avaliação na Play Store:** Ao detectar um bilhete premiado, o app solicita avaliação nativa via Google Play In-App Review API.
- **100% Local:** O reconhecimento de texto é executado no dispositivo — nenhuma imagem sai do aparelho.

### Estatísticas
- **Frequência e Atraso:** Exibe para cada dezena o número de aparições, a taxa de frequência, os sorteios desde a última saída e a frequência recente (últimos 20 concursos).
- **Histórico Configurável:** A janela de análise pode ser ajustada pelo usuário.

### Backtesting
- **Simulação Histórica:** Testa uma estratégia de fechamento contra todos os sorteios reais armazenados localmente.
- **Relatório de ROI:** Calcula quanto o usuário teria gasto e quanto teria recebido em prêmios se tivesse usado aquela estratégia no passado.
- **Breakdown por Faixa:** Detalha os acertos por tier de premiação (ex: quantas "Quinas" e "Quadras" foram atingidas).

### Notificações Inteligentes
- **Alerta de Acumulada:** Notifica quando o prêmio principal de uma loteria acumula.
- **Confirmação de Acerto:** Após sync, notifica se algum ticket salvo ou bolão acertou alguma faixa de premiação.
- **Lembrete de Sorteio:** Aviso matinal quando há sorteio hoje para jogos ou bolões salvos pelo usuário.
- **Resiliência pós-Reboot:** `BootReceiver` reagenda automaticamente os alarmes de sync (08:30, 12:30, 22:30 e 23:35 BRT) e lembretes após reinicialização do dispositivo, sem necessidade de abrir o app.
- **Onboarding de Permissão:** A permissão de notificação é solicitada em uma página dedicada do onboarding, com explicação prévia do valor de cada tipo de alerta — antes de o sistema Android exibir o diálogo nativo.
- **Configurações no App:** Tela em **Sobre → Notificações** exibe o status global de permissão e oferece atalhos diretos para as configurações de cada canal no Android.
- **Design Moderno:** Ícone vetorial monocromático otimizado para a barra de status (compliance Android 14+), evitando o efeito "quadrado branco".
- **Canais Granulares:** Três canais distintos (`results`, `alerts` e `reminders`) para controle total do usuário.

### Exportação PDF
- **Layout Profissional:** Header com gradiente na cor oficial da loteria, bolas numeradas por jogo e rodapé promocional.
- **Marca d'água Dinâmica:** Usuários free recebem rodapé com marca d'água; usuários premium recebem PDF limpo.
- **Paginação Automática:** PDFs com múltiplos jogos são paginados automaticamente em formato A4.
- **Compatível com FileProvider:** Compartilhamento seguro via `Intent.ACTION_SEND` sem exposição do caminho interno do arquivo.

### Backup no Google Drive (Premium)
- **Backup Manual e Automático:** Salva jogos, bolões e preferências na pasta oculta do app (`appDataFolder`) no Google Drive da própria conta do usuário — via WorkManager diário quando ativado.
- **Autorização Moderna:** Usa a Identity Authorization API (`drive.appdata`), sem SDK pesado do Drive — cliente REST próprio via OkHttp + Gson.
- **Restauração com Merge Idempotente:** Reinsere os itens preservando os IDs originais (`REPLACE`/`IGNORE` nos DAOs), sem apagar dados criados localmente após o backup.
- **Zero Acesso do Desenvolvedor:** Os dados trafegam diretamente entre o dispositivo e a conta Google do usuário; o escopo `drive.appdata` restringe o acesso apenas à pasta de dados do próprio app.

### Widget de Tela Inicial (gratuito)
- **Jetpack Glance:** Widget configurável por instância, com uma loteria selecionável por widget.
- **Conteúdo Combinado:** Último resultado (concurso, dezenas, "Acumulou") + próximo sorteio (concurso, prêmio estimado, data e contagem regressiva).
- **Refresh Automático:** Atualizado ao final de cada sincronização (4 janelas/dia), ao sincronizar pela tela de Resultados e a cada 6h via `updatePeriodMillis`.
- **Sem Gate:** O widget é gratuito para todos os usuários.

### Badges de Atualizações Não Vistas
- **Indicador por Loteria:** Contador de novidades (novo resultado, acerto em jogo/bolão) exibido na Home e no menu, zerado individualmente ao abrir cada tela.
- **Destaque "NOVO":** Concursos ainda não vistos recebem chip e borda de destaque na tela de Resultados.
- **Fonte Única:** `UpdatesBadgeStore` (DataStore), incrementado nos mesmos pontos já deduplicados do `SyncWorker`.

---

## Modelo Freemium

O LottoExpert utiliza Google Play Billing Library v7+ com três planos Premium e produto vitalício. Os gates estão concentrados em funcionalidades de escala e produtividade, mantendo uso básico e aquisição viral gratuitos.

### Planos Premium

| Plano | Preço | Produto no Play Console |
|-------|-------|------------------------|
| Mensal | R$ 7,90/mês | `premium_monthly` (SUBS) |
| Anual ⭐ | R$ 34,90/ano | `premium_annual` (SUBS) |
| Vitalício | R$ 69,90 (único) | `expert_lifetime` (INAPP) |

O paywall abre com o plano Anual pré-selecionado. Compradores legados do `expert_lifetime` continuam Premium sem nenhuma ação.

### Features por tier

| Feature | Free | Premium |
|---|---|---|
| Loterias disponíveis (Mega-Sena e Lotofácil) | ✓ | ✓ |
| Loterias avançadas (7 loterias) | — | ✓ |
| Filtros Pro no Gerador | — | ✓ |
| Desdobramentos com garantia | — | ✓ |
| Estratégias salvas (presets) | 1 preset | Ilimitados |
| OCR de bilhetes | 3 capturas de teste | Ilimitado |
| Backtesting histórico | — | ✓ |
| Jogos salvos | Até 10 | Ilimitado |
| Jogos acompanhados por concurso | Até 5 por concurso | Ilimitado |
| Conferência das participações | Manual | Automática pós-sorteio + notificação |
| Dashboard "Meu desempenho" | Amostra desfocada | ✓ |
| Relatório mensal | — | ✓ |
| Alertas inteligentes (limiar, dezena monitorada, lembrete) | — | ✓ |
| Backup no Google Drive | — | ✓ |
| Widget de tela inicial | ✓ | ✓ |
| PDF limpo (sem marca d'água) | — | ✓ |
| Bolões simultâneos | 1 ativo | Ilimitado |
| Participantes por bolão | Até 10 | Ilimitado |
| Compartilhar deep link + QR code de bolão | ✓ | ✓ |
| Copiar bolão para novo concurso | — | ✓ |
| Bolão recorrente (renovação automática) | — | ✓ |

Em builds de debug, o `BillingManager` opera em modo mock com toggle manual na tela **Sobre → Developer Options**.

---

## Loterias Suportadas

| Loteria | Dezenas | Seleção | Custo Base |
|---------|---------|---------|------------|
| Lotofácil | 1–25 | 15–20 | R$ 3,50 |
| Mega-Sena | 1–60 | 6–20 | R$ 6,00 |
| Quina | 1–80 | 5–15 | R$ 3,00 |
| Lotomania | 1–100 | 50 | R$ 3,00 |
| Timemania | 1–80 | 10 | R$ 3,50 |
| Dupla Sena | 1–50 | 6–15 | R$ 3,00 |
| Dia de Sorte | 1–31 | 7–15 | R$ 2,50 |
| +Milionária | 1–50 + trevos | 6 | R$ 6,00 |
| Super Sete | 0–9 (7 col.) | 7 | R$ 3,00 |

Os preços são mantidos atualizados via **Firebase Remote Config** (`LotteryPriceRepository`). O script `infra/scripts/update_prices.py` raspa os valores do portal oficial da CEF e os publica automaticamente. Os valores do XML `remote_config_defaults.xml` servem como fallback offline.

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Kotlin 1.9+ |
| UI | Jetpack Compose + Material Design 3 |
| Injeção de Dependências | Dagger Hilt 2.50 |
| Persistência | Room Database v23 (migrations explícitas + banco de seed pré-carregado) |
| Rede | Retrofit 2.9 + OkHttp 4.12 (disk cache 5 MB) |
| Concorrência | Kotlin Coroutines + Flow |
| Background Work | WorkManager (HiltWorker) + AlarmManager |
| Câmera | CameraX 1.3 |
| OCR | ML Kit Text Recognition 16.0 |
| Billing | Google Play Billing Library 7+ (INAPP + SUBS) |
| Segurança de API | Firebase App Check (Play Integrity / Debug) |
| Configuração Remota | Firebase Remote Config |
| Avaliação | Google Play In-App Review 2.0 |
| Observabilidade | Firebase Crashlytics + Firebase Analytics + Timber 5.0 |
| Infraestrutura backend | Google Cloud Platform (Cloud Functions Gen 2 + GCS) |
| Testes | JUnit 4 + Mockito-Kotlin + kotlinx-coroutines-test |

---

## Arquitetura

Clean Architecture com três camadas bem delimitadas e MVVM na camada de apresentação.

```
app/
├── data/
│   ├── backup/         BackupManager, DriveAuthManager, DriveBackupClient, BackupSerializer (Drive, Premium)
│   ├── billing/        BillingManager — mock em debug, Google Play em release; FreemiumConfig
│   ├── local/          Room DB v23: entities, DAOs, migrations, converters,
│   │                   UpdatesBadgeStore, SyncStatusStore, UserPreferences (DataStore)
│   ├── mapper/         DrawResultMapper (DTO → Entity → Domain)
│   ├── remote/         LotteryDataApi (Retrofit → GCP), AppCheckInterceptor, DTOs, LotteryPriceRepository
│   ├── repository/     DrawResultRepositoryImpl, WheelRepositoryImpl, JourneyRepositoryImpl
│   └── worker/         SyncWorker, MonthlyReportWorker, ReminderWorker, BackupWorker,
│                       SyncAlarmReceiver, ReminderAlarmReceiver, BootReceiver, AlarmScheduler
├── di/                 DatabaseModule, NetworkModule, RepositoryModule, RemoteConfigModule
├── domain/
│   ├── analytics/      AnalyticsManager + AnalyticsEvent (eventos tipados via sealed class)
│   ├── export/         PdfExporter (marca d'água por tier; bloco de resultado oficial por concurso)
│   ├── journey/        OnboardingJourney (primeiro uso) + PremiumJourney (pós-compra) — puros
│   ├── math/           CombinatoricsEngine, FilterEngine, MatrixGenerator, ProbabilityCalculator,
│   │                   DesdobramentoEngine (matrizes com garantia)
│   ├── model/          DrawResult, LotteryConfig, Wheel, SharedSweepstake
│   ├── ocr/            BilhetParser, ScanConsensus, LotomaniaGridReader + LotomaniaConsensus
│   ├── repository/     DrawResultRepository, WheelRepository, JourneyRepository (interfaces)
│   ├── strategy/       9 implementações de LotteryStrategy + Factory
│   └── usecase/        CheckTicketMatchesUseCase, ComputeNumberStatsUseCase, AutoCheckUseCase,
│                       CheckSweepstakeUseCase, RegisterTicketEntryUseCase, CopySweepstakeUseCase,
│                       TicketDrawMatcher + PrizeValuation, PerformanceAggregator,
│                       ContestGamesAggregator, WatchedNumberAlertEvaluator
└── ui/
    ├── components/     PaywallBottomSheet (gate freemium reutilizável), UnseenCountBadge,
    │                   GamePickerSheet, TicketBalls, JourneyChecklistCard + JourneyHintBar
    ├── journey/        JourneyUiMappers — adapta o estado de domínio para os componentes
    ├── navigation/     NavGraph + Screen (18 rotas)
    ├── notifications/  NotificationHelper — 3 canais e faixas de notification ID
    ├── screens/        dashboard, generator, results, statistics, backtesting, savedgames,
    │                   contestgames, performance, report (relatório mensal), premium,
    │                   scan, sweepstake (bolão), backup, datamanagement,
    │                   notifications, onboarding, about, help, terms, responsiblegambling
    ├── theme/          Tema Material 3 com cores dinâmicas por loteria
    └── widget/         Widget de tela inicial (gratuito) via Jetpack Glance
```

---

## Como Executar

1. Clone o repositório.
2. Abra no **Android Studio Hedgehog (2023.1.1) ou superior**.
3. Configure o JDK para o **Java 17**.
4. Sincronize o Gradle e aguarde o download das dependências.
5. Execute `./gradlew assembleDebug` ou rode diretamente pelo Android Studio.

```bash
# Build debug
./gradlew assembleDebug

# Testes unitários
./gradlew test

# Lint
./gradlew lint
```

> **Nota:** Em debug, o `BillingManager` opera em modo mock. O status premium pode ser alternado manualmente em **Sobre → Developer Options** para testar todos os fluxos de paywall sem compra real.

---

## Scripts de Infraestrutura

| Script | Descrição |
|--------|-----------|
| `infra/scripts/bootstrap_history.py` | Popula o bucket GCS com os últimos N concursos de cada loteria (executar uma vez após o deploy) |
| `infra/scripts/update_prices.py` | Raspa os preços mínimos do portal CEF e publica no Firebase Remote Config |
| `infra/scripts/run_update_prices.sh` | Wrapper que cria o virtualenv Python e executa o script acima |
| `tools/desdobramentos/build_wheels.py` | Gera e **prova** por ILP as matrizes de desdobramento publicadas em `assets/desdobramentos/` |

As Cloud Functions vivem em `infra/functions/`: `lottery_sync` (coleta horária da API da Caixa → bucket GCS), `lottery_serve` (leitura autenticada por App Check, consumida pelo app) e `billing_events` (receptor RTDN do Play Billing, log-only, para medir churn).

```bash
# Popular histórico inicial (após terraform apply)
python infra/scripts/bootstrap_history.py \
  --project SEU_PROJECT_ID \
  --bucket SEU_PROJECT_ID-lottery-results \
  --credentials infra/terraform/service-account.json \
  --count 100

# Atualizar preços remotos
cd infra/scripts
./run_update_prices.sh --credentials SERVICE_ACCOUNT.json --project SEU_PROJECT_ID
```

O deploy completo da infraestrutura GCP está documentado em [docs/GCP_DEPLOY.md](docs/GCP_DEPLOY.md).

---

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [ARQUITETURA.md](docs/ARQUITETURA.md) | Documento completo de arquitetura (camadas, DB, rede, padrões, testes) |
| [SPECS.md](docs/SPECS.md) | Especificação técnica do MVP (Sprints 1–5) — ✅ Implementado |
| [SPECS2.md](docs/SPECS2.md) | Especificação das evoluções (Sprints 6–8 + extras) — ✅ Implementado |
| [SPECS3.md](docs/SPECS3.md) | Especificação do Premium de retenção (Sprints P1–P4) — ✅ Implementado |
| [PREMIUM_ROADMAP.md](docs/PREMIUM_ROADMAP.md) | Roadmap de retenção e valor recorrente do Premium |
| [ROADMAP_FUTURO.md](docs/ROADMAP_FUTURO.md) | Evoluções previstas além do escopo atual |
| [MATURIDADE_E_CONCORRENTES.md](docs/MATURIDADE_E_CONCORRENTES.md) | Avaliação de maturidade (9,5/10) e análise competitiva |
| [PLANO_LANCAMENTO.md](docs/PLANO_LANCAMENTO.md) | Plano de lançamento com checklist Go/No-Go |
| [PLANO_MARKETING.md](docs/PLANO_MARKETING.md) | Estratégia de marketing e aquisição |
| [PLANO_VENDAS.md](docs/PLANO_VENDAS.md) | Funil de conversão, paywall e KPIs de vendas |
| [ASO_METADATA.md](docs/ASO_METADATA.md) | Estratégia de loja (título, descrição, keywords) |
| [PRIVACY_POLICY.md](docs/PRIVACY_POLICY.md) | Política de Privacidade |
| [TERMS_OF_SERVICE.md](docs/TERMS_OF_SERVICE.md) | Termos de Serviço |
| [GOOGLE_PLAY_POLITICAS.md](docs/GOOGLE_PLAY_POLITICAS.md) | Preenchimento das políticas da Play Store (classificação como Ferramenta, IARC, Data Safety) |
| [GOOGLE_PLAY_BILLING_SETUP.md](docs/GOOGLE_PLAY_BILLING_SETUP.md) | Criação e configuração dos 3 produtos de billing no Play Console (INAPP + SUBS, base plans, testes) |
| [PROJECAO_FINANCEIRA.md](docs/PROJECAO_FINANCEIRA.md) | Projeção financeira D+180: unit economics, cenários, custos GCP/ads, painel de acompanhamento mensal |
| [GCP_DEPLOY.md](docs/GCP_DEPLOY.md) | Deploy da infraestrutura GCP (Cloud Functions, GCS, App Check, bootstrap) |
| [RTDN_SETUP.md](docs/RTDN_SETUP.md) | Receptor de notificações do Play Billing (`billing-events`, log-only) para medir churn |
| [DRIVE_BACKUP_SETUP.md](docs/DRIVE_BACKUP_SETUP.md) | Setup do OAuth e do escopo `drive.appdata` do backup no Google Drive |

---

## Licença

Desenvolvido por **Gustavo Hyppolito**. Uso restrito conforme termos de licenciamento acordados.
