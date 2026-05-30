# Política de Privacidade — LottoExpert

**Última atualização:** 19 de Maio de 2026

Esta Política de Privacidade descreve como o aplicativo **LottoExpert** coleta, usa e protege suas informações. Nosso compromisso fundamental é com a **privacidade** e a segurança dos dados dos usuários.

---

## 1. Princípio Geral: Privacidade por Padrão

O LottoExpert é um aplicativo **Privacy-First**. Todo processamento de dados — geração de jogos, análise estatística, conferência de bilhetes e armazenamento do histórico — ocorre **exclusivamente no seu dispositivo**. Nenhuma informação pessoal, estratégia de aposta ou jogo criado por você é transmitida a qualquer servidor.

Para obter os resultados oficiais dos sorteios, o app comunica com servidores próprios do desenvolvedor hospedados no Google Cloud Platform (GCP) — descritos na Seção 4.1. Essas requisições são anônimas e não contêm qualquer dado pessoal.

---

## 2. Dados que o App NÃO Coleta

O LottoExpert **não coleta, não transmite e não armazena** em servidores remotos:

- Suas dezenas selecionadas ou estratégias de jogo
- Jogos criados ou salvos por você
- Seu histórico de apostas
- Dados de identificação pessoal (e-mail, telefone, CPF)
- Imagens capturadas pela câmera
- Dados de localização

**Nota sobre nomes em Bolões:** Os nomes de participantes inseridos no módulo "Meus Bolões" são armazenados exclusivamente no banco de dados local do seu dispositivo e nunca são enviados para nossos servidores. Esses nomes só deixam o aparelho se e quando você optar explicitamente por compartilhar um link de convite ou exportar um PDF.

---

## 3. Dados Tratados Localmente no Dispositivo

Os seguintes dados são armazenados no banco de dados privado do app (Room Database, SQLite), acessível apenas pelo próprio aplicativo:

- **Histórico de sorteios:** Resultados das loterias obtidos da nossa infraestrutura de dados (GCP), salvos para consulta offline.
- **Jogos salvos:** Tickets gerados pelo algoritmo ou criados manualmente pelo usuário.
- **Bolões:** Dados de grupos criados pelo usuário, incluindo nomes de participantes e vinculação de cotas.
- **Preferências de filtros:** Configurações locais de uso da interface.

O usuário tem total controle sobre esses dados e pode **excluí-los manualmente** a qualquer momento através das opções de "Limpar" ou "Remover" dentro do aplicativo. Ao **desinstalar o aplicativo**, todos esses dados locais são removidos permanentemente do dispositivo.

---

## 4. Comunicação com Serviços Externos

Para o funcionamento do app, comunicamos com os seguintes serviços externos:

### 4.1 Infraestrutura de Dados do Desenvolvedor (Google Cloud Platform)

- **Finalidade:** Fornecer os resultados oficiais dos sorteios das loterias brasileiras ao aplicativo.
- **Funcionamento:** Os resultados são coletados periodicamente da API pública da Caixa Econômica Federal por um processo automatizado do desenvolvedor e armazenados em um banco de dados privado hospedado no Google Cloud Platform (GCP). O aplicativo consulta esse banco de dados para sincronizar os resultados — sem chamar a API da Caixa diretamente.
- **Dados enviados pelo app:** Nenhum dado pessoal. A requisição inclui apenas o nome da loteria e, opcionalmente, o número do concurso solicitado. Adicionalmente, um token de atestação do Firebase App Check é enviado para autenticar que a requisição parte de uma instalação legítima do aplicativo (ver Seção 4.2).
- **Dados armazenados no servidor:** Apenas os resultados públicos dos sorteios. Nenhum dado do usuário é gravado nos servidores do desenvolvedor.
- **Frequência:** Sincronização automática três vezes ao dia (aproximadamente 22:30, 08:30 e 12:30 BRT), garantindo que os resultados estejam disponíveis mesmo em caso de atraso na publicação oficial. O usuário também pode atualizar manualmente.
- **Provedor de infraestrutura:** Google Cloud Platform. Sujeito à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.2 Firebase App Check (Google)

- **Finalidade:** Garantir que apenas instalações legítimas do LottoExpert possam acessar a infraestrutura de dados do desenvolvedor (Seção 4.1), protegendo contra uso abusivo da API por aplicações não autorizadas.
- **Funcionamento:** O App Check utiliza o **Google Play Integrity** para gerar um token de atestação que confirma a integridade do dispositivo e da instalação do app. Esse token é enviado junto com cada requisição de sincronização. O token não contém dados pessoais, não identifica o usuário individualmente e não é armazenado pelo desenvolvedor.
- **Dados processados pelo Google:** A avaliação de integridade do dispositivo é realizada pelo Google Play Integrity. O LottoExpert não tem acesso ao conteúdo do token — apenas à confirmação de que ele é válido.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy) e aos [Termos do Google Play Integrity](https://developer.android.com/google/play/integrity).

### 4.3 Google Play Billing

- **Finalidade:** Processar compras e assinaturas in-app para desbloqueio de recursos Premium. O app oferece três modalidades: assinatura mensal, assinatura anual e compra única vitalícia.
- **Dados tratados pelo Google:** Dados de pagamento e histórico de compras gerenciados exclusivamente pelo Google Play. O LottoExpert recebe apenas a confirmação criptografada da transação para liberar os recursos Premium — sem acesso a dados de cartão, métodos de pagamento ou informações financeiras do usuário.
- **Política do Google:** Sujeita aos [Termos de Serviço do Google Play](https://play.google.com/about/play-terms/).

### 4.4 Firebase Remote Config (Google)

- **Finalidade:** Manter os preços mínimos das apostas atualizados sem necessidade de atualizar o aplicativo. Os valores são lidos pelo app para exibir estimativas de custo ao usuário.
- **Dados enviados:** Nenhum dado pessoal. A requisição inclui apenas metadados técnicos anônimos do app (identificador do aplicativo e versão), utilizados pelo Firebase para controle de taxa de requisições.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.5 Google Play In-App Review

- **Finalidade:** Exibir a caixa de diálogo nativa do Google Play solicitando avaliação do aplicativo após uma experiência positiva (ex.: conferência de bilhete premiado).
- **Dados tratados pelo Google:** O fluxo de avaliação é gerenciado inteiramente pelo Google Play. O LottoExpert não coleta nem visualiza o conteúdo ou a nota da avaliação enviada.
- **Política do Google:** Sujeita aos [Termos de Serviço do Google Play](https://play.google.com/about/play-terms/).

### 4.6 Firebase Crashlytics (Google)

- **Finalidade:** Detectar e registrar falhas técnicas (crashes) do aplicativo para diagnóstico e correção pelo desenvolvedor.
- **Dados enviados:** Stack trace anônimo da falha, versão do app, tipo de dispositivo e versão do Android. **Nenhum dado pessoal é transmitido:** não coletamos identificadores de usuário, dados de jogo, estratégias ou qualquer informação inserida pelo usuário.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.7 Firebase Analytics (Google)

- **Finalidade:** Medir o uso agregado e anônimo das funcionalidades do app para melhorar a experiência do usuário, orientar o desenvolvimento e — em forma estritamente agregada, sem identificação individual — otimizar campanhas publicitárias do próprio desenvolvedor em plataformas como Google Ads e Meta Ads (Facebook/Instagram). Nenhum dado individual é compartilhado com essas plataformas; o uso é restrito a métricas agregadas de conversão (ex.: quantidade total de usuários que realizaram uma compra) para calibrar públicos de anúncios de forma estatística.
- **Dados enviados:** Eventos de uso pseudônimos e agregados. Exemplos de eventos coletados: `generate_matrix`, `scan_ocr`, `export_pdf`, `sweepstake_created`, `sweepstake_copied`, `backtest_run`, `view_paywall`, `purchase_premium`, `ticket_checked`, `trial_scan_used`, `sync_complete`, `sync_error`, `onboarding_completed`, `notification_permission_granted`. **Nenhuma dezena selecionada, nenhum dado financeiro e nenhum dado pessoal identificável é transmitido.**
- **Identificador técnico:** O Firebase Analytics utiliza um `app_instance_id` pseudônimo por instalação, que não permite identificar o usuário individualmente. Esse identificador pode ser redefinido a qualquer momento desinstalando e reinstalando o aplicativo.
- **Advertising ID:** A coleta do Advertising ID (GAID) está **desativada** de forma explícita no código do aplicativo. O LottoExpert não exibe anúncios e não integra nenhum SDK de publicidade de terceiros.
- **Base legal (LGPD):** Legítimo interesse do desenvolvedor (Art. 7º, IX, LGPD) para melhoria do produto e otimização de campanhas próprias, com dados tratados de forma agregada e pseudônima, sem impacto desproporcional ao usuário.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.8 Links de Compartilhamento e QR Code (Bolões)

- **Finalidade:** Compartilhamento de dados de bolões entre usuários via link ou QR code.
- **Funcionamento:** O app gera um link (e opcionalmente um QR code) que contém os dados do bolão codificados via GZIP e Base64, sem passar por servidores do desenvolvedor.
- **Privacidade:** O desenvolvedor não tem acesso aos links ou QR codes gerados. Como os dados estão contidos na própria URL, a segurança do compartilhamento depende da cautela do usuário ao enviar o link ou imagem para terceiros.

---

## 5. Permissões Solicitadas

| Permissão | Motivo |
|---|---|
| `INTERNET` | Sincronizar resultados dos sorteios com a infraestrutura de dados do desenvolvedor (GCP), processar compras e assinaturas via Google Play, e comunicar com serviços Firebase. |
| `BILLING` | Validar e processar compras únicas e assinaturas de recursos Premium via Google Play Store. |
| `CAMERA` | Escanear bilhetes físicos para conferência automática de dezenas (funcionalidade OCR). A câmera só é ativada quando o usuário abre explicitamente a tela de escaneamento. Nenhuma imagem é armazenada ou transmitida. |
| `POST_NOTIFICATIONS` | Exibir alertas de resultados, prêmios acumulados e lembretes de sorteio (requer permissão explícita no Android 13+). A permissão é solicitada durante o onboarding, com explicação prévia sobre o que será notificado. O usuário pode gerenciar ou revogar cada tipo de notificação individualmente nas configurações do Android ou dentro do próprio app (Sobre → Notificações). |
| `RECEIVE_BOOT_COMPLETED` | Reagendar automaticamente os alarmes de sincronização e lembretes após reinicialização do dispositivo, garantindo que as notificações continuem funcionando sem necessidade de abrir o app. |

---

## 6. Processamento de Imagens (OCR)

A funcionalidade "Conferir Bilhete" utiliza a câmera do dispositivo e o **ML Kit Text Recognition** (Google) para identificar dezenas em um bilhete físico fotografado.

- O processamento OCR ocorre **inteiramente no dispositivo** — o ML Kit opera offline, sem enviar imagens para servidores do Google ou do desenvolvedor.
- As imagens capturadas **não são salvas** em nenhum local (galeria, cache ou banco de dados).
- Apenas as dezenas identificadas no texto são utilizadas, descartando a imagem imediatamente após o processamento.

---

## 7. Público-Alvo e Restrição de Idade

O LottoExpert é destinado a usuários **maiores de 18 anos**, dada a natureza do conteúdo (loterias e jogos de azar regulamentados pela legislação brasileira). Não coletamos intencionalmente informações de menores de idade. Caso identifique uso indevido por menor, entre em contato através do canal de suporte na Google Play Store.

---

## 8. Segurança dos Dados

- Todo dado armazenado localmente fica no diretório privado do app, protegido pelo sandbox do Android.
- As requisições à infraestrutura do desenvolvedor (GCP) são autenticadas via Firebase App Check e transmitidas exclusivamente via HTTPS.
- O bucket de dados no GCP possui acesso público bloqueado — somente o serviço de sincronização do desenvolvedor pode gravar, e somente o serviço de leitura autenticado por App Check pode servir dados ao app.
- Utilizamos Firebase Analytics exclusivamente com eventos anônimos e agregados para fins de melhoria do produto, sem coleta de Advertising ID ou identificadores de usuário (ver seção 4.7).
- Não utilizamos SDKs de publicidade ou rastreadores de comportamento para fins comerciais.

---

## 9. Lei Geral de Proteção de Dados (LGPD)

O LottoExpert respeita integralmente a **Lei nº 13.709/2018 (LGPD)**. Esta seção descreve as bases legais utilizadas para cada tratamento de dados e os direitos garantidos ao titular.

### 9.1 Bases Legais

| Tratamento | Base Legal (LGPD) |
| :--- | :--- |
| Sincronização de resultados dos sorteios (GCP) | Execução de contrato / legítimo interesse — Art. 7º, V e IX |
| Firebase App Check (atestação de integridade) | Legítimo interesse — proteção contra uso abusivo da infraestrutura — Art. 7º, IX |
| Google Play Billing (compras e assinaturas) | Execução de contrato — Art. 7º, V |
| Firebase Crashlytics (diagnóstico de falhas) | Legítimo interesse — manutenção e melhoria do serviço — Art. 7º, IX |
| Firebase Analytics (uso agregado do app) | Legítimo interesse — melhoria do produto e otimização de campanhas próprias — Art. 7º, IX |
| Firebase Remote Config (preços de apostas) | Legítimo interesse — Art. 7º, IX |
| Dados locais (jogos, bolões, preferências) | Execução de contrato / consentimento implícito pelo uso — Art. 7º, V |

### 9.2 Direitos do Titular

Como titular de dados, você tem os seguintes direitos garantidos pela LGPD (Art. 18):

- **Confirmação e acesso:** confirmar se seus dados são tratados e acessá-los.
- **Correção:** solicitar a correção de dados incompletos, inexatos ou desatualizados.
- **Eliminação:** solicitar a exclusão dos dados tratados com base em consentimento.
- **Portabilidade:** solicitar a portabilidade dos dados a outro fornecedor de serviço.
- **Informação:** ser informado sobre as entidades com as quais seus dados são compartilhados.
- **Revogação do consentimento:** revogar o consentimento a qualquer momento.
- **Oposição:** opor-se ao tratamento realizado com base em legítimo interesse, quando este causar impacto desproporcional.

**Como exercer seus direitos:** entre em contato pelo canal oficial de suporte na página do aplicativo na Google Play Store. Responderemos em até 15 dias úteis.

**Dado local:** para eliminar dados armazenados no dispositivo (jogos salvos, bolões, preferências), utilize as opções de exclusão dentro do próprio app ou desinstale o aplicativo.

### 9.3 Transferência Internacional de Dados

Os serviços Firebase (Analytics, Crashlytics, App Check, Remote Config) e Google Cloud Platform são operados pelo Google, com servidores localizados fora do Brasil. Essas transferências são realizadas com base nas cláusulas contratuais padrão do Google, que fornecem garantias equivalentes às exigidas pela LGPD (Art. 33, II). Consulte a [Política de Privacidade do Google](https://policies.google.com/privacy) para detalhes.

---

## 10. Alterações nesta Política

Podemos atualizar esta Política de Privacidade ocasionalmente para refletir novas funcionalidades ou exigências legais. A data de "Última atualização" no topo deste documento indica quando a versão atual entrou em vigor. Recomendamos revisar este documento periodicamente.

---

## 11. Contato

Para dúvidas, solicitações ou relatos sobre privacidade e tratamento de dados, entre em contato através do canal oficial de suporte na **Google Play Store** na página do aplicativo LottoExpert.

---

*LottoExpert — Sua sorte, processada com engenharia e privacidade.*
