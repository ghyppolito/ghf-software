# Política de Privacidade — TopoWalk

**Última atualização:** julho de 2026

Esta Política de Privacidade descreve como o aplicativo **TopoWalk**, desenvolvido por **GHF Software**, trata as informações do usuário. Ao utilizar o TopoWalk, você concorda com os termos descritos neste documento.

---

## 1. Quem Somos

O TopoWalk é um aplicativo Android desenvolvido por **GHF Software** para fins de levantamento topográfico de campo. Não somos uma empresa de coleta de dados e não operamos servidores de armazenamento de informações pessoais.

---

## 2. Dados Acessados e Utilizados pelo Aplicativo

### 2.1 Localização (GPS)

- **O que é acessado:** Latitude, longitude e altitude dos pontos marcados pelo usuário durante a medição.
- **Finalidade:** Exclusivamente para realizar os cálculos topográficos (distância horizontal, desnível, distância inclinada, ângulo de inclinação, azimute e área de polígono) e para gerar a visualização no mapa.
- **Quando é acessado:** Somente enquanto o aplicativo está aberto e em uso ativo (foreground). O app não acessa a localização em segundo plano.
- **Retenção:** Os dados de localização ficam na memória durante a sessão. Se o usuário optar por **salvar a medição**, as coordenadas são armazenadas localmente no banco de dados do dispositivo (ver seção 5). Nenhum dado de localização é enviado a servidores externos.

### 2.2 Sensor de Pressão Atmosférica (Barômetro)

- **O que é acessado:** Leitura da pressão atmosférica do sensor físico do dispositivo.
- **Finalidade:** Calcular a altitude dos pontos com maior precisão do que o GPS isolado, por meio da fórmula barométrica padrão.
- **Quando é acessado:** Continuamente enquanto o aplicativo está aberto, exclusivamente para conversão de pressão em altitude.
- **Retenção:** Os valores de pressão brutos não são armazenados. Apenas a altitude derivada é usada nos cálculos e, opcionalmente, salva com a medição.

### 2.3 Bluetooth (Receptor GNSS/RTK Externo — opcional, em Beta)

- **O que é acessado:** Conexão Bluetooth com um receptor GNSS/RTK externo já pareado, escolhido pelo usuário, para leitura das sentenças de posição (NMEA 0183).
- **Finalidade:** Obter coordenadas e altitude de alta precisão a partir do receptor externo, em vez do GPS interno do aparelho.
- **Quando é acessado:** Somente quando o usuário ativa explicitamente o recurso "Receptor GNSS externo" e seleciona um dispositivo. O recurso vem **desligado por padrão**.
- **Escopo:** O aplicativo **não faz descoberta** de dispositivos e não usa a permissão `BLUETOOTH_SCAN`; apenas dispositivos já pareados nas configurações do Android são listados. Os dados recebidos permanecem no aparelho, são usados apenas para os cálculos e, opcionalmente, salvos com a medição. **Nada é transmitido a terceiros.**
- **Status Beta:** O recurso está sinalizado como Beta dentro do aplicativo. Isso não altera o tratamento de dados descrito acima — nenhuma informação adicional é coletada por conta do estágio de testes.

### 2.4 Acesso à Internet (Tiles de Mapa)

- **O que é acessado:** O aplicativo realiza requisições HTTP à rede de tiles do **OpenStreetMap** (OpenTopoMap) para exibir o mapa de relevo na tela de visualização.
- **Finalidade:** Renderizar o mapa de fundo sobre o qual a demarcação é plotada.
- **Dados enviados:** Apenas as coordenadas geográficas dos tiles necessários para renderizar a área visível — informação genérica de posição geográfica, sem identificação do usuário.
- **Quando é acessado:** Somente quando o usuário navega para a aba "Mapa" dentro de uma medição ou no histórico.
- **Armazenamento em cache:** O osmdroid pode armazenar tiles em cache local para melhorar a performance. Esse cache contém apenas imagens de mapa, sem dados pessoais do usuário.

### 2.5 Envio de Feedback por E-mail (opcional)

- **O que acontece:** Na tela do receptor GNSS externo, o botão "Enviar feedback" abre o **aplicativo de e-mail do próprio usuário** com uma mensagem pré-preenchida endereçada a `support@ghfsoftware.com`.
- **Dados pré-preenchidos na mensagem:** versão do TopoWalk, versão do Android e fabricante/modelo do aparelho. Nenhuma coordenada, medição ou dado do histórico é incluído.
- **Controle do usuário:** A mensagem só é enviada se o usuário decidir enviá-la, podendo editar ou apagar qualquer parte do texto antes disso. O TopoWalk não envia nada automaticamente e não tem acesso à conta de e-mail do usuário.
- **O que recebemos:** Ao optar por enviar, o usuário nos revela o endereço de e-mail utilizado, junto ao conteúdo da mensagem. Esses e-mails são usados exclusivamente para responder e corrigir problemas do recurso, não são compartilhados com terceiros nem usados para marketing, e podem ser excluídos mediante solicitação ao mesmo endereço.

---

## 3. Dados NÃO Coletados

O TopoWalk **não coleta, não armazena remotamente e não transmite**:

- Nome, e-mail ou qualquer dado de identificação pessoal
- Endereço IP ou dados de rede além do necessário para carregar tiles de mapa e enviar eventos de analytics
- Localização em segundo plano ou histórico de localização fora do uso ativo do app
- ID de publicidade (o aplicativo remove explicitamente esta permissão)

Única exceção: se o usuário voluntariamente nos escrever pelo botão "Enviar feedback" (seção 2.5), passamos a conhecer o endereço de e-mail que ele escolheu usar e o conteúdo que ele escreveu. Isso depende sempre de uma ação explícita do usuário e não ocorre em nenhum outro fluxo do aplicativo.

---

## 4. Analytics — Firebase Analytics (Google)

A partir da versão 3.10, o TopoWalk utiliza o **Firebase Analytics**, um serviço de análise de uso fornecido pelo Google LLC.

### O que é coletado e enviado ao Firebase:

- **Interações no app:** telas visualizadas, funcionalidades utilizadas (ex.: captura de pontos, exportação de arquivos, acesso ao histórico) e fluxo de navegação.
- **ID de instalação do Firebase:** identificador anônimo gerado pelo SDK para agregar sessões. Não identifica pessoalmente o usuário e pode ser redefinido desinstalando e reinstalando o app.
- **Informações do dispositivo:** modelo, versão do sistema operacional e idioma — coletados automaticamente pelo SDK para segmentação de relatórios.

### O que NÃO é coletado pelo Firebase:

- Coordenadas GPS ou dados das medições topográficas
- Nome, e-mail ou qualquer informação pessoal inserida no app
- ID de publicidade (explicitamente removido do app)

### Finalidade:

Os dados são utilizados exclusivamente para entender como os usuários interagem com o app, identificar funcionalidades mais usadas e orientar melhorias futuras. Não são utilizados para publicidade ou personalização.

### Retenção e controle:

Os dados são retidos pelo Google conforme a [Política de Privacidade do Google](https://policies.google.com/privacy). O usuário pode limpar o ID de instalação do Firebase desinstalando o aplicativo.

---

## 5. Compartilhamento de Dados com Terceiros

O TopoWalk compartilha dados com os seguintes terceiros:

| Terceiro | Dados compartilhados | Finalidade |
|---|---|---|
| **Google LLC (Firebase Analytics)** | Interações no app, ID de instalação, informações do dispositivo | Analytics de uso |
| **OpenStreetMap / OpenTopoMap** | Coordenadas dos tiles de mapa solicitados | Renderização do mapa |

O aplicativo não integra SDKs de publicidade, redes sociais ou qualquer outro serviço externo além dos listados acima.

---

## 6. Armazenamento Local

### 6.1 Banco de Dados (Histórico de Medições)

Quando o usuário opta por salvar uma medição, os seguintes dados são armazenados **localmente no dispositivo** em um banco de dados Room (SQLite), acessível apenas pelo aplicativo:

- Nome e observações informados pelo usuário
- Coordenadas (latitude, longitude, altitude) de cada ponto da medição
- Resultados calculados (distâncias, desníveis, ângulos, área)
- Data e hora da medição

Esses dados **nunca são enviados a servidores externos** e permanecem no dispositivo até que o usuário os exclua manualmente pelo aplicativo ou desinstale o app.

### 6.2 Relatórios em PDF

Ao solicitar a geração de um relatório PDF, o aplicativo:

1. Cria o arquivo PDF temporariamente no **diretório de cache privado** do app (`cacheDir`), acessível apenas pelo próprio aplicativo.
2. Compartilha o arquivo via `FileProvider` com o aplicativo de sua escolha (WhatsApp, e-mail, Google Drive, etc.) usando o mecanismo padrão do Android.
3. O arquivo permanece no cache até que o sistema operacional realize a limpeza automática ou o usuário limpe os dados do app.

O TopoWalk não tem acesso ao destino escolhido pelo usuário para o compartilhamento — essa operação é gerenciada inteiramente pelo sistema Android e pelo aplicativo receptor.

### 6.3 Exportação GeoJSON e KML

O usuário pode exportar medições nos formatos GeoJSON e KML. Esses arquivos são gerados localmente no cache do dispositivo e compartilhados da mesma forma que o PDF (seção 6.2). O app não tem acesso ao destino do compartilhamento.

---

## 7. Permissões do Aplicativo

| Permissão | Motivo |
|---|---|
| `ACCESS_FINE_LOCATION` | Obter coordenadas GPS precisas para os pontos de medição |
| `ACCESS_COARSE_LOCATION` | Permissão complementar exigida pelo Android para localização |
| `INTERNET` | Carregar tiles de mapa do OpenStreetMap e enviar eventos ao Firebase Analytics |
| `VIBRATE` | Feedback háptico ao capturar um ponto de medição |
| `BLUETOOTH_CONNECT` (Android 12+) | Conectar a um receptor GNSS/RTK externo já pareado, quando o recurso é ativado pelo usuário |
| `BLUETOOTH` / `BLUETOOTH_ADMIN` (Android 11 e anteriores) | Equivalente às versões antigas do Android para a mesma conexão |

O aplicativo não solicita acesso à câmera, microfone, contatos ou armazenamento externo. O ID de publicidade (`AD_ID`) é explicitamente removido do app e não é coletado.

---

## 8. Uso por Menores

O TopoWalk não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados de menores. Por se tratar de uma ferramenta técnica de campo, o uso por menores deve ocorrer sob supervisão de um adulto responsável.

---

## 9. Segurança

Os dados de medição do TopoWalk são processados e armazenados exclusivamente no dispositivo do usuário. A comunicação com serviços externos (Firebase Analytics e OpenStreetMap) é realizada exclusivamente via HTTPS com criptografia em trânsito. Os dados enviados ao Firebase não contêm informações pessoais identificáveis. A segurança dos dados armazenados localmente é gerenciada pelo sistema operacional Android e pelo isolamento de aplicativos (sandbox).

---

## 10. Alterações nesta Política

Podemos atualizar esta Política de Privacidade periodicamente. Alterações relevantes serão comunicadas por meio de uma nova versão do aplicativo publicada na Google Play Store. A data de "Última atualização" no topo deste documento sempre refletirá a versão vigente.

Recomendamos que você revise esta política periodicamente.

---

## 11. Contato

Dúvidas, solicitações ou comentários sobre esta Política de Privacidade podem ser enviados para:

**GHF Software**
E-mail: **support@ghfsoftware.com**

---

*Esta política foi elaborada em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018), o Regulamento Geral de Proteção de Dados da União Europeia (GDPR) e as políticas de privacidade da Google Play Store.*
