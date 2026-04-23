# Política de Privacidade — TopoWalk

**Última atualização:** abril de 2026

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

### 2.3 Acesso à Internet (Tiles de Mapa)

- **O que é acessado:** O aplicativo realiza requisições HTTP à rede de tiles do **OpenStreetMap** (OpenTopoMap) para exibir o mapa de relevo na tela de visualização.
- **Finalidade:** Renderizar o mapa de fundo sobre o qual a demarcação é plotada.
- **Dados enviados:** Apenas as coordenadas geográficas dos tiles necessários para renderizar a área visível — informação genérica de posição geográfica, sem identificação do usuário.
- **Quando é acessado:** Somente quando o usuário navega para a aba "Mapa" dentro de uma medição ou no histórico.
- **Armazenamento em cache:** O osmdroid pode armazenar tiles em cache local para melhorar a performance. Esse cache contém apenas imagens de mapa, sem dados pessoais do usuário.

---

## 3. Dados NÃO Coletados

O TopoWalk **não coleta, não armazena remotamente e não transmite**:

- Nome, e-mail ou qualquer dado de identificação pessoal
- Dados de uso, telemetria ou analytics
- Informações do dispositivo (modelo, IMEI, versão de SO)
- Endereço IP ou dados de rede além do necessário para carregar tiles de mapa
- Localização em segundo plano ou histórico de localização fora do uso ativo do app

---

## 4. Compartilhamento de Dados com Terceiros

**Não compartilhamos dados pessoais com terceiros.**

O aplicativo não integra SDKs de publicidade, plataformas de analytics (como Firebase Analytics, Crashlytics ou similares), redes sociais ou qualquer serviço externo de coleta de dados pessoais.

A única comunicação externa do app é com os servidores de tiles do **OpenStreetMap** (opentopomap.org), exclusivamente para renderização do mapa, conforme descrito na seção 2.3.

---

## 5. Armazenamento Local

### 5.1 Banco de Dados (Histórico de Medições)

Quando o usuário opta por salvar uma medição, os seguintes dados são armazenados **localmente no dispositivo** em um banco de dados Room (SQLite), acessível apenas pelo aplicativo:

- Nome e observações informados pelo usuário
- Coordenadas (latitude, longitude, altitude) de cada ponto da medição
- Resultados calculados (distâncias, desníveis, ângulos, área)
- Data e hora da medição

Esses dados **nunca são enviados a servidores externos** e permanecem no dispositivo até que o usuário os exclua manualmente pelo aplicativo ou desinstale o app.

### 5.2 Relatórios em PDF

Ao solicitar a geração de um relatório PDF, o aplicativo:

1. Cria o arquivo PDF temporariamente no **diretório de cache privado** do app (`cacheDir`), acessível apenas pelo próprio aplicativo.
2. Compartilha o arquivo via `FileProvider` com o aplicativo de sua escolha (WhatsApp, e-mail, Google Drive, etc.) usando o mecanismo padrão do Android.
3. O arquivo permanece no cache até que o sistema operacional realize a limpeza automática ou o usuário limpe os dados do app.

O TopoWalk não tem acesso ao destino escolhido pelo usuário para o compartilhamento — essa operação é gerenciada inteiramente pelo sistema Android e pelo aplicativo receptor.

### 5.3 Exportação GeoJSON e KML

O usuário pode exportar medições nos formatos GeoJSON e KML. Esses arquivos são gerados localmente no cache do dispositivo e compartilhados da mesma forma que o PDF (seção 5.2). O app não tem acesso ao destino do compartilhamento.

---

## 6. Permissões do Aplicativo

| Permissão | Motivo |
|---|---|
| `ACCESS_FINE_LOCATION` | Obter coordenadas GPS precisas para os pontos de medição |
| `ACCESS_COARSE_LOCATION` | Permissão complementar exigida pelo Android para localização |
| `INTERNET` | Carregar tiles de mapa do OpenStreetMap para a visualização cartográfica |

Nenhuma outra permissão é solicitada. O aplicativo não solicita acesso à câmera, microfone, contatos ou armazenamento externo.

---

## 7. Uso por Menores

O TopoWalk não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados de menores. Por se tratar de uma ferramenta técnica de campo, o uso por menores deve ocorrer sob supervisão de um adulto responsável.

---

## 8. Segurança

O TopoWalk processa todas as informações localmente no dispositivo e não transmite dados pessoais para servidores externos. A única comunicação de rede é com servidores públicos de tiles de mapa, sem envio de dados de identificação pessoal. A segurança dos dados armazenados localmente é gerenciada pelo sistema operacional Android e pelo isolamento de aplicativos (sandbox).

---

## 9. Alterações nesta Política

Podemos atualizar esta Política de Privacidade periodicamente. Alterações relevantes serão comunicadas por meio de uma nova versão do aplicativo publicada na Google Play Store. A data de "Última atualização" no topo deste documento sempre refletirá a versão vigente.

Recomendamos que você revise esta política periodicamente.

---

## 10. Contato

Dúvidas, solicitações ou comentários sobre esta Política de Privacidade podem ser enviados para:

**GHF Software**
E-mail: **[seu e-mail de contato]**

---

*Esta política foi elaborada em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018), o Regulamento Geral de Proteção de Dados da União Europeia (GDPR) e as políticas de privacidade da Google Play Store.*
