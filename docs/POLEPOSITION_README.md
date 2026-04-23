# Pole Position — Race Analytics

**Pole Position** é um aplicativo nativo para Android desenvolvido como alternativa profissional e 100% offline a hardwares de telemetria como MyChron e Alfano. Focado em pilotos de kart e automobilismo amador, o app transforma o smartphone em um painel de bordo de alta performance com análise completa de sessão.

---

## Funcionalidades

### Telemetria em Tempo Real

- **GPS de Alta Frequência (10 Hz):** Captura de posição otimizada com suporte a antenas externas Bluetooth.
- **Detecção de Linha por Vetor:** Algoritmo de intersecção de segmentos de reta — não depende de raio de distância, elimina detecções falsas.
- **Interpolação de Milissegundo:** Cálculo preciso do instante exato de cruzamento da linha, independentemente da frequência do GPS.
- **Força G Suavizada:** Filtro passa-baixa (EMA) aplicado ao acelerômetro para eliminar jitter e exibir leitura estável.
- **Giroscópio:** Leitura de rotação angular disponível para análise futura.

### Painel do Piloto (Live Dashboard)

- **Interface F1:** Design de alto contraste (preto / branco / verde neon) otimizado para visibilidade sob sol direto, em portrait e landscape.
- **Cronômetro da Volta Atual:** Exibição principal em fonte monospace com dígitos tabelados (sem "samba" de números).
- **Congelamento Pós-Volta:** Ao fechar uma volta, tempo e parciais ficam congelados por 3 segundos para o piloto conferir antes de atualizar.
- **Delta da Melhor Volta:** Mostra a diferença em relação à melhor volta registrada. Se a volta completada for um novo recorde, exibe o ganho sobre o recorde anterior.
- **Parciais com 3 Níveis de Cor:**
  - Roxo — melhor parcial de todas as sessão
  - Verde — melhor que a parcial da volta anterior, mas não a melhor de todas
  - Amarelo — pior que a volta anterior e que o melhor histórico
- **Última Volta:** Mesma escala de cores das parciais.
- **Barra de Força G Lateral:** Visualização dinâmica da carga lateral em curvas.
- **Indicadores de Status:** GPS, sessão ativa, out-lap, número de volta.
- **Voz do Engenheiro (TTS):** Feedback por voz dos tempos ao completar cada volta.

### Configuração de Circuito

- **Mapa Híbrido (satélite + nomes):** Posicionamento visual preciso da linha de chegada e setores.
- **Mira com Rotação de Gate:** Controle de bearing da linha em passos de 1° e 15° para alinhar exatamente com a pista. Reset automático para o heading do GPS.
- **Busca de Endereço:** Campo de pesquisa para navegar até qualquer local no mapa.
- **Centralização na Localização Atual:** Botão FAB para recentrar o mapa na posição do GPS em tempo real.
- **Limite de 2 Setores:** Máximo de 2 linhas de setor (3 parciais) para manter o layout do painel coerente.
- **Setores Habilitados/Desabilitados:** O painel evidencia visualmente quais setores estão ativos com base na configuração do circuito.

### Análise de Sessão

- **Histórico por Circuito:** Lista de todos os circuitos com suas sessões agrupadas.
- **Detalhe de Volta:** Tela dedicada por volta com velocidade máxima, velocidade mínima, G-force máxima, parciais e delta em relação à melhor volta da sessão.
- **Exportação CSV:** Exporta todos os dados da sessão em formato CSV com colunas alinhadas — uma linha por volta, incluindo tempo formatado, velocidades, G-force e parciais.

### Configurações

- **Modo de Exibição:** Claro, Escuro ou Seguir Sistema (padrão).
- **Orientação de Tela:** Portrait, Landscape ou Automático (padrão) — fixável para uso no cockpit.
- **Modo de Localização:** Sempre ativo ou Apenas em Sessão (padrão) — economiza bateria fora da pista.

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Kotlin |
| UI | Jetpack Compose (Material 3) |
| Arquitetura | MVVM + StateFlow |
| Injeção de Dependência | Hilt |
| Persistência | Room Database (com migrações) |
| Localização | Google Play Services — Priority High Accuracy |
| Sensores | SensorManager (Accelerometer, Gyroscope) |
| Concorrência | Kotlin Coroutines & Flow |
| Serviço em Background | Foreground Service (TelemetryService) |
| Mapa | Google Maps Compose |
| TTS | Android TextToSpeech |
| Preferências | SharedPreferences via AppPreferences singleton |

---

## Estrutura do Projeto

```
br.com.ghfsoftware.polepositionapp
├── core/
│   ├── di/             # Módulos Hilt (AppModule, LocationModule)
│   ├── preferences/    # AppPreferences (SharedPreferences)
│   └── util/           # GeometryUtil (cálculo de gates, intersecção de vetores)
├── data/
│   ├── local/
│   │   ├── dao/        # SessionDao, TrackDao
│   │   ├── entities/   # TrackEntity, SplitEntity, SessionEntity, LapEntity, LapSplitEntity
│   │   └── AppDatabase # Room Database (versão 3, com migrações)
├── service/
│   └── TelemetryService  # Coração do app — GPS, sensores, cronômetro, detecção de volta
└── ui/
    ├── history/        # HistoryScreen + HistoryViewModel
    ├── session/        # SessionAnalyzerScreen + SessionViewModel
    ├── settings/       # SettingsScreen
    └── track/          # TrackConfigScreen + TrackViewModel
    MainActivity.kt     # NavHost, Dashboard (Portrait/Landscape), HomeScreen
```

---

## Como Usar

### 1. Configurar o Circuito

1. Na tela inicial, toque em **Criar Circuito**.
2. Busque o endereço ou navegue pelo mapa até a pista.
3. Posicione a mira sobre a linha de chegada e ajuste o bearing da linha com os botões de rotação.
4. Toque em **LINHA DE CHEGADA** para marcar.
5. Opcionalmente, marque até 2 linhas de setor com o botão **SETOR**.
6. Dê um nome ao circuito e toque em **SALVAR**.

### 2. Iniciar uma Sessão

1. Na tela inicial, selecione o circuito desejado.
2. Configure se deseja ignorar a out-lap.
3. Toque em **GO** para iniciar o monitoramento.
4. A primeira passagem pela linha de chegada inicia o cronômetro.

### 3. No Cockpit

- Fixe o celular firmemente no suporte.
- Com o kart parado e nivelado, toque em **CALIBRAR** para zerar os sensores de Força G.
- Conecte fone de ouvido Bluetooth para receber os tempos por voz.

### 4. Analisar a Sessão

1. Após tocar em **STOP**, adicione uma nota opcional à sessão.
2. Acesse o **Histórico** para ver todas as sessões por circuito.
3. Toque em uma sessão para ver a lista de voltas com tempos e delta.
4. Toque em uma volta para ver o detalhe completo (velocidades, G-force, parciais).
5. Toque no ícone de compartilhamento para exportar os dados em CSV.

---

## Requisitos

- Android 8.0 (API 26) ou superior
- Permissões: Localização (Precisa — em primeiro plano), Sensores
- Google Play Services

---

## Licença

Projeto desenvolvido para uso em telemetria esportiva amadora.

**Desenvolvido por Gustavo Hyppolito**
