# Política de Privacidade — LottoExpert

**Última atualização:** 02 de Maio de 2026

Esta Política de Privacidade descreve como o aplicativo **LottoExpert** coleta, usa e protege suas informações. Nosso compromisso fundamental é com a **privacidade absoluta** e a segurança dos dados dos usuários.

---

## 1. Princípio Geral: Privacidade por Padrão

O LottoExpert é um aplicativo **Offline-First e Privacy-First**. Todo processamento de dados — geração de jogos, análise estatística, conferência de bilhetes e armazenamento do histórico — ocorre **exclusivamente no seu dispositivo**. Nenhuma informação pessoal ou estratégia de aposta é transmitida a servidores do desenvolvedor.

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

- Histórico de sorteios: Resultados das loterias obtidos da API pública da CEF, salvos para consulta offline.
- Jogos salvos: Tickets gerados pelo algoritmo ou criados manualmente pelo usuário.
- Bolões: Dados de grupos criados pelo usuário, incluindo nomes de participantes e vinculação de cotas.
- Preferências de filtros: Configurações locais de uso da interface.

O usuário tem total controle sobre esses dados e pode **excluí-los manualmente** a qualquer momento através das opções de "Limpar" ou "Remover" dentro do aplicativo. Ao **desinstalar o aplicativo**, todos esses dados locais são removidos permanentemente do dispositivo.

---

## 4. Comunicação com Serviços de Terceiros

Para o funcionamento do app, comunicamos com os seguintes serviços externos:

### 4.1 API Pública da Caixa Econômica Federal
- **Finalidade:** Obter os resultados oficiais dos sorteios das loterias brasileiras.
- **Dados enviados:** Nenhum dado pessoal. A requisição é anônima e serve exclusivamente para leitura de dados públicos.
- **Endpoint:** `servicebus2.caixa.gov.br/portaldeloterias/api/`
- **Frequência:** Sincronização automática diária às 21h (após os sorteios), restrita aos dias de sorteio de cada loteria. O usuário também pode atualizar manualmente.

### 4.2 Google Play Billing
- **Finalidade:** Processar compras in-app para desbloqueio de recursos premium (Status PRO).
- **Dados tratados pelo Google:** Dados de pagamento gerenciados exclusivamente pelo Google Play. O LottoExpert recebe apenas a confirmação criptografada da transação para liberar os recursos — sem acesso a dados de cartão ou métodos de pagamento.
- **Política do Google:** Sujeita aos [Termos de Serviço do Google Play](https://play.google.com/about/play-terms/).

### 4.3 Firebase Remote Config (Google)
- **Finalidade:** Manter os preços mínimos das apostas atualizados sem necessidade de atualizar o aplicativo. Os valores são lidos pelo app para exibir estimativas de custo ao usuário.
- **Dados enviados:** Nenhum dado pessoal. A requisição inclui apenas metadados técnicos anônimos do app (identificador do aplicativo e versão), utilizados pelo Firebase para controle de taxa de requisições.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.4 Google Play In-App Review
- **Finalidade:** Exibir a caixa de diálogo nativa do Google Play solicitando avaliação do aplicativo após uma experiência positiva (ex.: conferência de bilhete premiado).
- **Dados tratados pelo Google:** O fluxo de avaliação é gerenciado inteiramente pelo Google Play. O LottoExpert não coleta nem visualiza o conteúdo ou a nota da avaliação enviada.
- **Política do Google:** Sujeita aos [Termos de Serviço do Google Play](https://play.google.com/about/play-terms/).

### 4.4 Firebase Crashlytics (Google)
- **Finalidade:** Detectar e registrar falhas técnicas (crashes) do aplicativo para diagnóstico e correção pelo desenvolvedor.
- **Dados enviados:** Stack trace anônimo da falha, versão do app, tipo de dispositivo e versão do Android. **Nenhum dado pessoal é transmitido:** não coletamos identificadores de usuário, dados de jogo, estratégias ou qualquer informação inserida pelo usuário.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.5 Firebase Analytics (Google)
- **Finalidade:** Medir o uso agregado e anônimo das funcionalidades do app — como geração de jogos, scan de bilhetes e exportação de PDF — para melhorar a experiência do usuário e orientar o desenvolvimento.
- **Dados enviados:** Eventos de uso anônimos e agregados (ex.: `generate_matrix`, `scan_ocr`, `view_paywall`). **Nenhum identificador de usuário, nenhuma dezena selecionada e nenhum dado financeiro é transmitido.**
- **Configurações de privacidade adicionais:** A coleta de Advertising ID (GAID) está **desativada**. Nenhum sinal de personalização de anúncios é coletado.
- **Política do Google:** Sujeita à [Política de Privacidade do Google](https://policies.google.com/privacy).

### 4.6 Links Mágicos (Deep Links)
- **Finalidade:** Compartilhamento de dados de bolões entre usuários.
- **Funcionamento:** O app gera um link que contém os dados do bolão codificados via GZIP e Base64.
- **Privacidade:** O desenvolvedor não tem acesso aos links gerados ou compartilhados. Como os dados estão contidos na própria URL, a segurança do compartilhamento depende da cautela do usuário ao enviar o link para terceiros.

---

## 5. Permissões Solicitadas

| Permissão | Motivo |
|---|---|
| `INTERNET` | Baixar resultados oficiais dos sorteios da CEF e processar compras via Google Play. |
| `BILLING` | Validar e processar compras de recursos premium via Google Play Store. |
| `CAMERA` | Escanear bilhetes físicos para conferência automática de dezenas (funcionalidade OCR). A câmera só é ativada quando o usuário abre explicitamente a tela de escaneamento. Nenhuma imagem é armazenada ou transmitida. |
| `POST_NOTIFICATIONS` | Exibir alertas de resultados, prêmios acumulados e lembretes de sorteio (requer permissão explícita no Android 13+). |
| `RECEIVE_BOOT_COMPLETED` | Reagendar a sincronização automática após reinicialização do dispositivo. |
| `SCHEDULE_EXACT_ALARM` / `USE_EXACT_ALARM` | Agendar a sincronização diária de resultados no horário correto (21h). |

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
- Utilizamos Firebase Analytics exclusivamente com eventos anônimos e agregados para fins de melhoria do produto, sem coleta de Advertising ID ou identificadores de usuário (ver seção 4.5).
- Não utilizamos SDKs de publicidade ou rastreadores de comportamento para fins comerciais.
- O código-fonte pode ser auditado conforme termos de licenciamento do projeto.

---

## 9. Alterações nesta Política

Podemos atualizar esta Política de Privacidade ocasionalmente para refletir novas funcionalidades ou exigências legais. A data de "Última atualização" no topo deste documento indica quando a versão atual entrou em vigor. Recomendamos revisar este documento periodicamente.

---

## 10. Contato

Para dúvidas, solicitações ou relatos sobre privacidade e tratamento de dados, entre em contato através do canal oficial de suporte na **Google Play Store** na página do aplicativo LottoExpert.

---

*LottoExpert — Sua sorte, processada com engenharia e privacidade.*
