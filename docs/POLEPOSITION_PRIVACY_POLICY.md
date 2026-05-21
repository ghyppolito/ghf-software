# Política de Privacidade — Pole Position: Race Analytics

**Última atualização:** maio de 2026

Esta Política de Privacidade descreve como o aplicativo **Pole Position: Race Analytics** ("o App", "nós") coleta, usa, armazena e protege as informações dos usuários ("você"). Ao instalar e utilizar o App, você concorda com os termos desta política.

---

## 1. Sobre o Aplicativo

O **Pole Position: Race Analytics** é um aplicativo de telemetria esportiva para Android desenvolvido para pilotos de kart e automobilismo amador. O App utiliza o GPS e os sensores de movimento do dispositivo para registrar voltas, calcular tempos, medir força G lateral e fornecer análise de desempenho em pista.

---

## 2. Dados Coletados

### 2.1 Dados de Localização (GPS)

O App solicita permissão de **localização precisa** (`ACCESS_FINE_LOCATION`) para:

- Detectar o cruzamento da linha de chegada e das linhas de setor com precisão de milissegundos.
- Calcular a velocidade do veículo em tempo real (km/h) a partir dos dados de GPS.
- Centralizar o mapa na posição atual durante a configuração de circuitos.

A localização é utilizada **exclusivamente dentro do dispositivo**. Nenhuma coordenada GPS é transmitida para servidores externos, terceiros ou qualquer serviço de nuvem.

### 2.2 Dados de Sensores de Movimento

O App acessa o **acelerômetro** e o **giroscópio** do dispositivo para:

- Medir a força G lateral durante a pilotagem.
- Exibir dados de aceleração em tempo real no painel.

Os dados dos sensores são processados localmente e em memória. Nenhum dado bruto de sensor é persistido no banco de dados ou transmitido externamente.

### 2.3 Dados Inseridos pelo Usuário

O App armazena localmente no dispositivo:

- **Nomes de circuitos** e coordenadas das linhas de chegada e setor cadastradas pelo usuário.
- **Tempos de volta** e parciais registrados durante as sessões.
- **Notas de sessão** inseridas voluntariamente pelo usuário após cada sessão.
- **Velocidade máxima e mínima** e **força G máxima** por volta.

Todos esses dados são armazenados exclusivamente no banco de dados local do dispositivo (Room/SQLite) e nunca saem do aparelho, exceto quando o próprio usuário escolhe exportá-los.

### 2.4 Dados de Uso Coletados Automaticamente (Firebase Analytics)

O App integra o **Firebase Analytics** (Google LLC) para coleta anônima de métricas de uso. Os dados coletados incluem:

- **Eventos de comportamento no app:** fluxos percorridos (onboarding, criação de circuito, início e encerramento de sessão, análise de sessão), ações de configuração (alteração de tema, orientação, modo de localização, TTS) e ações no histórico.
- **Propriedades agregadas do usuário:** modo de tema, modo TTS ativo, modo de localização, quantidade total de circuitos criados.
- **Dados técnicos do dispositivo:** coletados automaticamente pelo Firebase, incluindo modelo do dispositivo, versão do Android, idioma do sistema e país de origem (derivado do IP, não armazenado como dado bruto).

**O que NÃO é coletado via analytics:**
- Coordenadas de GPS ou localização geográfica real.
- Dados de desempenho de pilotagem (tempos de volta, velocidades, G-force).
- Nomes de circuitos, notas ou qualquer conteúdo inserido pelo usuário.
- Dados que permitam identificar o usuário individualmente (nome, e-mail, CPF etc.).

Esses dados são usados exclusivamente para entender quais funcionalidades são utilizadas e melhorar o App em versões futuras. Não há venda ou compartilhamento dessas informações para fins publicitários.

### 2.5 Dados NÃO Coletados

O App **não coleta, não armazena e não transmite**:

- Nome, e-mail, telefone ou qualquer dado de identificação pessoal.
- Dados de contas de redes sociais ou serviços de terceiros.
- Informações de pagamento.
- Histórico de navegação ou dados de outros aplicativos.
- Dados de localização ou telemetria fora do contexto de uma sessão ativa.
- Relatórios automáticos de falha (Crashlytics ou equivalente).

---

## 3. Uso das Permissões

| Permissão | Finalidade |
|---|---|
| `ACCESS_FINE_LOCATION` | Detecção precisa de cruzamento de linha e velocidade GPS |
| `ACCESS_BACKGROUND_LOCATION` | Manutenção do serviço de telemetria durante sessão ativa com tela desligada |
| `FOREGROUND_SERVICE` | Execução do serviço de telemetria em primeiro plano com notificação visível |
| `FOREGROUND_SERVICE_LOCATION` | Classificação do serviço de localização em primeiro plano (exigência Android 14+) |
| `WAKE_LOCK` | Impede que o processador suspenda durante sessões para garantir captura contínua |
| `HIGH_SAMPLING_RATE_SENSORS` | Acesso a leituras do acelerômetro e giroscópio em alta frequência |
| `INTERNET` | Envio de eventos anônimos ao Firebase Analytics e carregamento do mapa (Google Maps) |

A permissão `ACCESS_BACKGROUND_LOCATION` é utilizada **somente durante sessões de pilotagem ativas**, quando o usuário inicia explicitamente uma sessão no App. Ela garante que o serviço de telemetria continue registrando corretamente mesmo que o piloto minimize o App ou o dispositivo apague a tela durante a corrida. O App não rastreia a localização do usuário fora do contexto de uma sessão ativa.

---

## 4. Armazenamento e Segurança

- Os dados de telemetria (circuitos, sessões, voltas) são armazenados exclusivamente no dispositivo do usuário.
- O App não possui servidor próprio para dados de pilotagem e não os envia a nenhum servidor externo.
- Dados anônimos de uso do app são enviados ao Firebase Analytics (Google LLC) por conexão HTTPS cifrada. Esses dados são gerenciados conforme a [Política de Privacidade do Google](https://policies.google.com/privacy).
- A segurança dos dados locais depende das proteções nativas do sistema operacional Android e do bloqueio do dispositivo do usuário.
- A desinstalação do App remove todos os dados armazenados localmente no dispositivo.

---

## 5. Compartilhamento de Dados

O App não compartilha dados de pilotagem com terceiros de forma automática.

O único mecanismo de compartilhamento de dados de sessão disponível é a **exportação manual de CSV**, acionada exclusivamente pelo usuário no botão de compartilhamento da tela de análise de sessão. O arquivo gerado contém apenas os dados de telemetria da sessão selecionada e é entregue ao aplicativo de compartilhamento escolhido pelo próprio usuário (e-mail, mensageiro, armazenamento em nuvem etc.). O App não retém cópia do arquivo após o compartilhamento.

Dados anônimos de uso (eventos Firebase Analytics) são processados pelo Google conforme descrito na seção 6.

---

## 6. Serviços de Terceiros

### Google Maps SDK for Android

Utilizado para exibição do mapa durante a configuração de circuitos. O App transmite ao SDK do Maps apenas as coordenadas necessárias para renderização do mapa na tela, conforme o funcionamento padrão da biblioteca. Sujeito à [Política de Privacidade do Google](https://policies.google.com/privacy).

### Firebase Analytics (Google LLC)

Utilizado para coleta de métricas anônimas de uso conforme descrito na seção 2.4. Os dados são transmitidos aos servidores do Google e armazenados conforme os termos do Firebase. Sujeito à [Política de Privacidade do Google](https://policies.google.com/privacy) e aos [Termos de Serviço do Firebase](https://firebase.google.com/terms).

### Google Play In-App Review API

Utilizado para exibir o fluxo nativo de avaliação do Google Play em momentos oportunos dentro do App (ex.: após análise de sessões). Nenhum dado inserido pelo usuário nesse fluxo é acessado ou armazenado pelo App — o processo ocorre inteiramente dentro do Google Play. Sujeito à [Política de Privacidade do Google](https://policies.google.com/privacy).

---

## 7. Privacidade de Menores

O App é destinado a uso esportivo e não é direcionado a crianças menores de 13 anos. Não coletamos intencionalmente dados de menores de idade.

---

## 8. Direitos do Usuário

Como os dados de pilotagem são armazenados localmente no seu dispositivo, você tem controle total sobre eles:

- **Acesso:** Os dados podem ser visualizados diretamente nas telas do App.
- **Exportação:** Os dados podem ser exportados via CSV a qualquer momento.
- **Exclusão parcial:** Voltas, sessões e circuitos podem ser excluídos individualmente pelo App.
- **Exclusão total:** A desinstalação do App remove todos os dados armazenados localmente.

Para dados coletados pelo Firebase Analytics, você pode desativar a coleta nas configurações do seu dispositivo Android em **Configurações > Google > Anúncios > Cancelar personalização de anúncios** ou, em versões mais recentes, por meio das opções de privacidade do Google Play Services.

---

## 9. Alterações nesta Política

Esta política pode ser atualizada periodicamente. Alterações relevantes serão comunicadas por meio de atualização do App na Google Play Store. A data da última atualização está indicada no topo deste documento.

---

## 10. Contato

Em caso de dúvidas sobre esta Política de Privacidade, entre em contato pelo repositório oficial do projeto ou pelo e-mail do desenvolvedor.

**Desenvolvido por Gustavo Hyppolito**
