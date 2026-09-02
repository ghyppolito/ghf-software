# Política de Privacidade — TopoWalk

**Última atualização:** setembro de 2026

Esta Política de Privacidade descreve como o aplicativo **TopoWalk**, desenvolvido por **GHF Software**, trata as informações do usuário. Ao utilizar o TopoWalk, você concorda com os termos descritos neste documento.

---

## 1. Quem Somos

O TopoWalk é um aplicativo Android desenvolvido por **GHF Software** para fins de levantamento topográfico de campo. Não somos uma empresa de coleta de dados.

Os seus levantamentos — pontos, medições, fotos e relatórios — **ficam no seu aparelho** e não são enviados a nenhum servidor nosso. A única exceção é o serviço de **migração do TopoWalk Pro** descrito na seção 2.11, que existe por tempo limitado, guarda apenas um identificador sem nome nem e-mail, e **não toca nos seus dados de levantamento**.

---

## 2. Dados Acessados e Utilizados pelo Aplicativo

### 2.1 Localização (GPS)

- **O que é acessado:** Latitude, longitude e altitude dos pontos marcados pelo usuário durante a medição.
- **Finalidade:** Exclusivamente para realizar os cálculos topográficos (distância horizontal, desnível, distância inclinada, ângulo de inclinação, azimute e área de polígono) e para gerar a visualização no mapa.
- **Quando é acessado:** Somente enquanto o aplicativo está aberto e em uso ativo (foreground). O app não acessa a localização em segundo plano.
- **Retenção:** Os dados de localização ficam na memória durante a sessão. Se o usuário optar por **salvar a medição**, as coordenadas são armazenadas localmente no banco de dados do dispositivo (ver seção 8.1). O GHF Software não envia esses dados a servidores próprios; veja a seção 8.4 sobre o backup manual que o próprio TopoWalk oferece e a seção 8.5 sobre o backup automático do sistema Android, que pode incluir esse banco de dados na conta Google do próprio usuário.

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

### 2.5 Nomes de Pontos e Rótulos (a partir da versão 4.0)

- **O que é acessado:** Texto opcional que o usuário digita para identificar um ponto capturado (ex.: "canto da cerca", "mourão 12").
- **Finalidade:** Facilitar o reconhecimento de pontos na lista de captura, no relatório PDF e nos arquivos exportados.
- **Retenção:** Armazenado junto com a medição, nos mesmos termos da seção 8.1. Nunca é enviado a servidores do GHF Software nem ao Firebase.

### 2.6 Envio de Feedback por E-mail (opcional)

- **O que acontece:** Na tela do receptor GNSS externo, o botão "Enviar feedback" abre o **aplicativo de e-mail do próprio usuário** com uma mensagem pré-preenchida endereçada a `support@ghfsoftware.com`.
- **Dados pré-preenchidos na mensagem:** versão do TopoWalk, versão do Android e fabricante/modelo do aparelho. Nenhuma coordenada, medição ou dado do histórico é incluído.
- **Controle do usuário:** A mensagem só é enviada se o usuário decidir enviá-la, podendo editar ou apagar qualquer parte do texto antes disso. O TopoWalk não envia nada automaticamente e não tem acesso à conta de e-mail do usuário.
- **O que recebemos:** Ao optar por enviar, o usuário nos revela o endereço de e-mail utilizado, junto ao conteúdo da mensagem. Esses e-mails são usados exclusivamente para responder e corrigir problemas do recurso, não são compartilhados com terceiros nem usados para marketing, e podem ser excluídos mediante solicitação ao mesmo endereço.

### 2.7 Sensores de Orientação — Bússola (a partir da versão 4.1)

- **O que é acessado:** Leitura do sensor de vetor de rotação do aparelho (que o Android compõe a partir de magnetômetro, acelerômetro e giroscópio), para determinar para onde o aparelho está apontado.
- **Finalidade:** Exclusivamente para desenhar a seta da tela de **Locação**, que orienta o usuário até um ponto já levantado. A correção entre o norte magnético e o norte geográfico é calculada no próprio aparelho, a partir da posição atual e do modelo geomagnético do Android.
- **Quando é acessado:** Somente enquanto a tela de Locação está aberta. O sensor é desligado ao sair dela.
- **Retenção:** As leituras existem apenas em memória, durante o uso da tela. **Nada é armazenado nem transmitido.** Aparelhos sem bússola simplesmente não exibem a seta — o recurso degrada mostrando o azimute numérico.

### 2.8 Identidade Visual do Relatório (a partir da versão 4.1)

Esta é a única parte do TopoWalk em que o usuário informa dados **sobre si mesmo ou sobre sua empresa**. Merece leitura atenta.

- **O que o usuário pode informar:** nome da empresa, nome do responsável técnico, registro profissional (CREA, CAU ou equivalente), uma nota de rodapé livre, uma cor e um arquivo de imagem para servir de logotipo.
- **Finalidade:** Compor o cabeçalho e o rodapé dos relatórios em PDF gerados pelo usuário, para que o documento entregue ao cliente dele tenha a identidade da empresa dele, e não a do aplicativo.
- **Como o logotipo é obtido:** pelo seletor de arquivos do próprio Android (Storage Access Framework). O aplicativo **não pede permissão de armazenamento** e **não enxerga nenhum outro arquivo** além do único que o usuário escolher. A imagem é redimensionada e copiada para a área privada do aplicativo; o arquivo original permanece onde estava e não é alterado.
- **Onde esses dados ficam:** exclusivamente no dispositivo, nas preferências locais do aplicativo e na sua área privada de arquivos. **Nunca são enviados ao GHF Software, ao Firebase, ao Google Play nem a qualquer terceiro.** Eles não aparecem em nenhum evento de analytics nem em relatório de falha.
- **Quando esses dados saem do dispositivo:** apenas quando o **próprio usuário** compartilha um relatório em PDF — porque eles fazem parte visível do documento, que é justamente o objetivo do recurso. O destino desse compartilhamento é escolhido pelo usuário e está fora do controle do aplicativo (mesmos termos da seção 8.2).
- **Como remover:** a tela "Personalizar o laudo em PDF" permite apagar o logotipo e esvaziar cada campo a qualquer momento. Limpar os dados do aplicativo também remove tudo.

### 2.9 Arquivos Importados — Camadas de Referência (a partir da versão 4.2)

- **O que é acessado:** um único arquivo por vez, escolhido pelo usuário no seletor do próprio Android (Storage Access Framework), nos formatos KML, KMZ, GeoJSON, GPX ou CSV. O aplicativo **não pede permissão de armazenamento** e **não enxerga nenhum outro arquivo** além do que o usuário selecionar.
- **Finalidade:** exibir o perímetro ou os pontos do arquivo como camada de referência sobre o mapa, e permitir caminhar até esses pontos pela tela de Locação. É o caso de quem já tem o KML do CAR, do SIGEF ou o arquivo enviado por um cliente.
- **O que o arquivo pode conter:** coordenadas e nomes de pontos escolhidos por quem gerou o arquivo. Esse conteúdo pode ser um dado sobre um imóvel — e é por isso que ele merece esta seção.
- **Onde fica:** o conteúdo é copiado para a **área privada do aplicativo, no próprio aparelho** (o arquivo original permanece onde estava e não é alterado). A cópia existe porque a permissão sobre o arquivo escolhido expira, e sem ela a camada desapareceria sozinha depois de algum tempo.
- **Para onde não vai:** o conteúdo importado **nunca é enviado** ao GHF Software, ao Firebase, ao Google Play nem a qualquer terceiro. Não aparece em evento de analytics nem em relatório de falha — o que se registra é apenas que houve uma importação, de qual formato e com quantos pontos, sem nenhuma coordenada.
- **Como remover:** a tela "Camadas importadas" permite remover cada camada a qualquer momento; remover apaga a cópia interna e não toca no arquivo original. Limpar os dados do aplicativo também remove tudo.

### 2.10 Fotos de Campo (a partir da versão 4.2)

Esta seção descreve o **único dado do aplicativo que pode conter imagem de pessoas ou de propriedade**, e merece leitura atenta.

- **O que o usuário pode anexar:** até 5 fotos por levantamento, tiradas na hora pela câmera ou escolhidas da galeria do aparelho.
- **Finalidade:** documentar o campo — o marco, o portão, a erosão — junto do levantamento correspondente, e opcionalmente incluí-las no relatório em PDF que o usuário entrega ao cliente dele.
- **O aplicativo NÃO pede permissão de câmera nem de armazenamento.** A foto tirada na hora passa pelo aplicativo de câmera do próprio sistema (`ACTION_IMAGE_CAPTURE`), e a escolha na galeria passa pelo seletor de fotos do Android — nos dois casos o aplicativo recebe apenas o arquivo que o usuário selecionou, e **não enxerga nenhuma outra foto do aparelho**.
- **Onde ficam:** o aplicativo faz uma **cópia reduzida** (no máximo 1280 px, JPEG) na sua área privada, no próprio aparelho. A foto original permanece onde estava e não é alterada. A cópia existe porque o endereço temporário devolvido pela câmera ou pela galeria perde validade, e sem ela a foto sumiria do levantamento depois de algum tempo.
- **Metadados:** a cópia é gravada **sem os metadados EXIF do original** — o que inclui a geolocalização que a câmera do celular costuma anotar. Só a orientação é preservada, aplicada diretamente na imagem para que a foto não saia deitada no relatório. Na prática, a cópia guardada pelo TopoWalk carrega **menos** informação que o arquivo original.
- **Para onde não vão:** as fotos **nunca são enviadas** ao GHF Software, ao Firebase, ao Google Play nem a qualquer terceiro. Não aparecem em evento de analytics nem em relatório de falha — o que se registra é apenas que houve um anexo e quantas fotos o levantamento passou a ter, sem nenhuma imagem e sem nenhum nome de arquivo.
- **Quando saem do dispositivo:** apenas quando o **próprio usuário** compartilha um relatório em PDF que as inclui — porque elas fazem parte visível do documento, que é o objetivo do recurso. O destino é escolhido pelo usuário e está fora do controle do aplicativo (mesmos termos da seção 8.2).
- **Como remover:** cada foto pode ser removida individualmente na tela do levantamento. Apagar o levantamento apaga as fotos dele junto. Limpar os dados do aplicativo remove tudo. Em nenhum desses casos o arquivo original da galeria é tocado.

### 2.11 Migração do TopoWalk Pro para a conta Google (a partir da versão 4.3)

Quem já usava o TopoWalk antes de o Pro existir recebeu o acesso de graça (seção 6). Essa
concessão fica registrada **no aparelho**, e por isso não acompanharia sozinha uma troca de
celular. Este recurso resolve isso: o usuário obtém um **código promocional do Google Play**,
resgata na Play Store, e o acesso passa a pertencer à **conta Google dele**.

É o **único** recurso do TopoWalk que guarda algo num servidor operado pelo GHF Software, e
existe por **tempo limitado** — encerrada a migração, o serviço é desligado e os dados abaixo
são apagados.

**Prazo:** o pedido de código pode ser feito até **31 de março de 2027**. Depois dessa data o
serviço é desligado em definitivo e todos os registros descritos nesta seção são apagados.

- **Quando acontece:** somente quando o usuário abre a tela "Levar o Pro para sua conta" e
  toca em pedir o código. Quem nunca abre essa tela **não estabelece nenhuma conexão** com o
  nosso servidor: o aplicativo não abre sessão, não gera identificador e não envia nada.
- **O que é enviado e guardado:**
  - Um **identificador do aparelho embaralhado** (hash SHA-256). O identificador original
    **não é enviado** e não pode ser recuperado a partir do que guardamos.
  - Um **identificador de sessão anônima** gerado pelo Firebase — um número aleatório, sem
    nome, sem e-mail e sem senha. Não é uma conta e não exige cadastro.
  - A **data e hora** do pedido e o **código promocional** entregue.
- **O que NÃO é enviado:** nome, e-mail, conta Google, dados de pagamento, localização,
  levantamentos, fotos ou qualquer conteúdo produzido no aplicativo.
- **Para que serve o identificador embaralhado:** os códigos são limitados pelo Google a uma
  quantidade fixa por trimestre. Sem uma forma de reconhecer que um mesmo aparelho já foi
  atendido, pedidos repetidos esgotariam o estoque e deixariam sem código quem tem direito.
  Ele serve **só** para isso: entregar um código por aparelho.
- **Verificação de integridade:** o pedido é acompanhado de uma atestação do **Google Play
  Integrity**, que confirma ao nosso servidor que a chamada vem do aplicativo TopoWalk
  genuíno, instalado pela Play Store. Essa verificação é feita pelo Google e **não nos revela
  nada sobre o usuário**.
- **Onde ficam:** Cloud Firestore e Cloud Functions, hospedados no Google Cloud, sob conta do
  GHF Software.
- **Por quanto tempo:** até **31 de março de 2027**, data limite para pedir um código.
  Encerrada a campanha, os registros são exportados para conferência e apagados, e o serviço
  é desligado.
- **Como pedir a exclusão:** escreva para `support@ghfsoftware.com` informando o código que
  recebeu. Apagamos o registro correspondente.

---

## 3. Dados NÃO Coletados

O TopoWalk **não coleta, não armazena remotamente e não transmite**:

- Nome, e-mail ou qualquer dado de identificação pessoal — inclusive no serviço de migração do Pro (seção 2.11), que **não pede login e não recebe nome nem e-mail**
- Endereço IP ou dados de rede além do necessário para carregar tiles de mapa e enviar eventos de analytics e relatórios de falha
- Localização em segundo plano ou histórico de localização fora do uso ativo do app
- ID de publicidade (o aplicativo remove explicitamente esta permissão)

Duas observações de precisão:

1. **Feedback por e-mail.** Se o usuário voluntariamente nos escrever pelo botão "Enviar feedback" (seção 2.6), passamos a conhecer o endereço de e-mail que ele escolheu usar e o conteúdo que ele escreveu. Isso depende sempre de uma ação explícita do usuário e não ocorre em nenhum outro fluxo do aplicativo.
2. **Migração do TopoWalk Pro (seção 2.11).** Esse recurso envia ao nosso servidor um identificador embaralhado do aparelho e um identificador de sessão anônimo. Nenhum dos dois carrega nome, e-mail ou conta, e nenhum deles é usado fora dessa finalidade. É a **única** situação em que o aplicativo guarda algo num servidor nosso.
3. **Identidade visual do relatório (a partir da versão 4.1).** O usuário pode digitar o próprio nome e o registro profissional para que apareçam no PDF (seção 2.8). Esses dados **são pessoais**, mas ficam **somente no aparelho dele**: o GHF Software não os recebe, não os armazena e não tem como acessá-los. Eles só deixam o dispositivo dentro de um PDF que o próprio usuário decide compartilhar.

---

## 4. Analytics — Firebase Analytics (Google)

A partir da versão 3.10, o TopoWalk utiliza o **Firebase Analytics**, um serviço de análise de uso fornecido pelo Google LLC.

### O que é coletado e enviado ao Firebase:

- **Interações no app:** telas visualizadas, funcionalidades utilizadas (ex.: captura de pontos, exportação de arquivos, acesso ao histórico) e fluxo de navegação.
- **Interesse em formatos futuros (versão 4.0):** o menu de exportação lista DXF e CSV como formatos planejados; tocar neles não gera arquivo algum, apenas registra um evento anônimo (que o formato foi visto, e, se o usuário tocar num botão de confirmação dentro da tela, que ele tem interesse nele). **Nenhum contato é coletado nesse fluxo** — o aplicativo não pergunta e-mail nem telefone, e não existe lista de espera. Esta medição **termina na versão 4.1**, quando os dois formatos passam a existir de verdade.
- **Funil de compra (a partir da versão 4.1):** eventos anônimos registrando que a tela de compra foi aberta, de qual funcionalidade ela foi aberta, que uma compra foi iniciada, e se ela foi concluída, cancelada ou falhou. **Não é registrado o preço, a moeda, a forma de pagamento, nem qualquer identificador da conta Google ou do meio de pagamento** — apenas o passo do fluxo. Servem para saber se a tela de compra é compreensível, não para identificar quem comprou.
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

## 5. Relatórios de Erro — Firebase Crashlytics (Google)

A partir da versão 3.13, o TopoWalk utiliza o **Firebase Crashlytics**, serviço do Google LLC para relatório de falhas. Ele existe para detectar problemas que o usuário não consegue reportar sozinho — em especial falhas de conexão com o receptor GNSS/RTK externo, que ocorrem em campo e sem mensagem de erro útil.

### O que é coletado e enviado ao Crashlytics:

- **Falhas do aplicativo:** tipo da exceção, stack trace e estado da thread no momento do erro.
- **Falhas não fatais do receptor externo:** motivo da desconexão, exceção original do Bluetooth, número da tentativa de reconexão e um trecho de até 16 caracteres do início do fluxo de dados do receptor — deliberadamente curto para conter apenas o cabeçalho da sentença (tipo e hora), nunca coordenadas.
- **Contexto técnico da sessão:** se o receptor externo está ativado, nome do modelo do receptor pareado, estado da conexão, qualidade do fix (ex.: `RTK_FIXED`), número de satélites e HDOP.
- **Falhas de compra e de leitura do logotipo (a partir da versão 4.1):** o código de erro devolvido pelo Google Play quando a confirmação de uma compra não é aceita, e o stack trace de uma imagem que não pôde ser lida como logotipo. **Nenhum dos dois contém o conteúdo da imagem, os dados da empresa, o preço ou qualquer identificador da conta.**
- **Informações do dispositivo e ID de instalação do Firebase:** coletados automaticamente pelo SDK, nos mesmos termos da seção 4.

### O que NÃO é coletado pelo Crashlytics:

- Coordenadas GPS, altitudes ou qualquer dado das medições do usuário
- Nome, notas ou arquivos exportados dos levantamentos
- Nome, e-mail ou qualquer informação pessoal inserida no app
- Logotipo, nome da empresa, responsável técnico ou registro profissional (seção 2.8)

### Finalidade:

Exclusivamente diagnosticar e corrigir defeitos do aplicativo. Os dados não são utilizados para publicidade, personalização ou perfilamento.

### Retenção e controle:

Os relatórios são retidos pelo Google conforme a [Política de Privacidade do Google](https://policies.google.com/privacy) e a [documentação do Crashlytics](https://firebase.google.com/support/privacy).

---

## 6. Compras no Aplicativo — Google Play Billing (a partir da versão 4.1)

A partir da versão 4.1, o TopoWalk oferece uma **compra única e definitiva** (TopoWalk Pro), processada pelo **Google Play Billing**, serviço do Google LLC.

### Quem processa o pagamento

**O pagamento é processado inteiramente pelo Google.** O TopoWalk **nunca** vê, recebe ou armazena número de cartão, dados bancários, endereço de cobrança ou qualquer informação de pagamento. Essa tela é do Google Play, não do aplicativo, e o que acontece nela é regido pela [Política de Privacidade do Google](https://policies.google.com/privacy) e pelos Termos de Serviço do Google Play.

### O que o aplicativo envia ao Google Play

- O identificador do produto (`topowalk_pro`), para consultar o preço e abrir a tela de compra.
- Uma confirmação de que a compra foi recebida (exigida pelo Google; sem ela a compra é estornada automaticamente em três dias).

O aplicativo **não envia nenhum identificador de conta, de usuário ou de dispositivo criado por nós** ao Google Play. O recurso que o Google oferece para associar uma compra a uma conta interna do desenvolvedor (`obfuscatedAccountId`) **não é utilizado**.

O TopoWalk **não tem contas de usuário**: não há cadastro, login, senha nem perfil. O serviço de migração do Pro (seção 2.11) usa uma sessão anônima do Firebase, que é um identificador aleatório gerado pelo próprio aparelho — não é uma conta, não pede credencial e não guarda nome nem e-mail.

### O que o aplicativo recebe e guarda

- **O preço já formatado** na moeda do usuário, para exibir na tela. O aplicativo não sabe qual é a moeda nem o país — recebe o texto pronto do Google.
- **Se existe ou não uma compra ativa** para o aparelho, consultado a cada abertura do aplicativo. Essa resposta é guardada localmente como um simples "sim ou não", para que o aplicativo não pisque "não comprado" enquanto consulta. **Nenhum dado da conta Google é guardado.**

### Por que a consulta se repete

A verificação acontece a cada sessão porque é assim que um **reembolso** chega ao aplicativo: se o usuário pedir a devolução do dinheiro ao Google, a compra deixa de constar e o acesso é retirado. O oposto também vale — quem reinstala o aplicativo recupera o acesso sem pagar de novo.

### Acesso concedido sem compra

Usuários que já tinham o TopoWalk instalado antes do lançamento do TopoWalk Pro recebem o acesso **gratuitamente e em definitivo**. Essa concessão é registrada **apenas no aparelho**, e não envolve o Google Play, conta de usuário nem qualquer dado pessoal.

Por ser registrada no aparelho, ela não acompanharia sozinha uma troca de celular. Para resolver isso, o aplicativo oferece a **migração do Pro** descrita na seção 2.11: o usuário obtém um código promocional, resgata na Play Store, e o acesso passa a pertencer à conta Google dele — voltando sozinho em qualquer aparelho onde ele entrar com a mesma conta.

### Menores de idade

Compras no Google Play estão sujeitas aos controles parentais e às exigências de autenticação do próprio Google Play. O TopoWalk não implementa verificação de idade própria e não tem como saber a idade de quem compra.

---

## 7. Compartilhamento de Dados com Terceiros

O TopoWalk compartilha dados com os seguintes terceiros:

| Terceiro | Dados compartilhados | Finalidade |
|---|---|---|
| **Google LLC (Firebase Analytics)** | Interações no app, ID de instalação, informações do dispositivo | Analytics de uso |
| **Google LLC (Firebase Crashlytics)** | Stack traces, falhas do receptor externo, contexto técnico da sessão, ID de instalação, informações do dispositivo | Diagnóstico de falhas |
| **OpenStreetMap / OpenTopoMap** | Coordenadas dos tiles de mapa solicitados | Renderização do mapa |
| **Google LLC (Google Play Billing)** — a partir da versão 4.1 | Identificador do produto e confirmação de compra. Nenhum identificador de conta criado por nós; nenhum dado de pagamento passa pelo aplicativo | Processar a compra do TopoWalk Pro |
| **Google LLC (Firebase Authentication)** — migração do Pro, seção 2.11 | Uma sessão **anônima**: identificador aleatório gerado pelo aparelho. Sem nome, sem e-mail, sem senha | Identificar a chamada ao nosso serviço de migração |
| **GHF Software (Cloud Firestore e Cloud Functions, hospedados no Google Cloud)** — migração do Pro, seção 2.11 | Identificador embaralhado do aparelho, identificador de sessão anônima, data e hora do pedido e o código promocional entregue | Entregar um código a cada usuário e impedir que o estoque seja esgotado por pedidos repetidos |

O aplicativo não integra SDKs de publicidade, redes sociais ou qualquer outro serviço externo além dos listados acima.

---

## 8. Armazenamento Local

### 8.1 Banco de Dados (Histórico de Medições)

Quando o usuário opta por salvar uma medição, os seguintes dados são armazenados **localmente no dispositivo** em um banco de dados Room (SQLite), acessível apenas pelo aplicativo:

- Nome e observações informados pelo usuário
- Coordenadas (latitude, longitude, altitude) de cada ponto da medição
- Resultados calculados (distâncias, desníveis, ângulos, área)
- Data e hora da medição

Esses dados **nunca são enviados a servidores do GHF Software** e permanecem no dispositivo até que o usuário os exclua manualmente pelo aplicativo ou limpe os dados do app. Veja a seção 8.4 sobre o backup manual que o próprio TopoWalk oferece, e a seção 8.5 sobre o backup automático do sistema Android — os dois são independentes entre si.

### 8.2 Relatórios em PDF

Ao solicitar a geração de um relatório PDF, o aplicativo:

1. Cria o arquivo PDF temporariamente no **diretório de cache privado** do app (`cacheDir`), acessível apenas pelo próprio aplicativo.
2. Compartilha o arquivo via `FileProvider` com o aplicativo de sua escolha (WhatsApp, e-mail, Google Drive, etc.) usando o mecanismo padrão do Android.
3. O arquivo permanece no cache até que o sistema operacional realize a limpeza automática ou o usuário limpe os dados do app.

O TopoWalk não tem acesso ao destino escolhido pelo usuário para o compartilhamento — essa operação é gerenciada inteiramente pelo sistema Android e pelo aplicativo receptor.

### 8.3 Exportação de Arquivos

O usuário pode exportar medições em **GeoJSON, KML e GPX** (a partir da versão 4.0) e em **DXF e CSV** (a partir da versão 4.1). Esses arquivos são gerados localmente no cache do dispositivo e compartilhados da mesma forma que o PDF (seção 8.2). O app não tem acesso ao destino do compartilhamento.

A exportação em CSV gera **dois arquivos** — um com os pontos e outro com os segmentos —, compartilhados juntos. O DXF contém, além da geometria, a latitude e a longitude do primeiro ponto do levantamento, gravadas como texto dentro do arquivo para permitir posicionar o desenho; é o mesmo dado de coordenada que os demais formatos já carregam.

### 8.4 Backup e Restauração do Histórico (a partir da versão 4.0)

O TopoWalk permite que o usuário exporte manualmente **todo o histórico de medições** para um único arquivo, e o restaure depois — no mesmo aparelho, após reinstalação, ou em outro aparelho.

- **Como funciona:** ao tocar em "Fazer backup do histórico", o app usa o seletor de arquivos do próprio Android (Storage Access Framework) para que o usuário escolha onde gravar o arquivo — Google Drive, cartão de memória, armazenamento interno ou qualquer outro local listado pelo sistema. **O app grava diretamente no local escolhido pelo usuário**, sem passar pelo seletor de compartilhamento entre aplicativos usado pelo PDF e pelos demais formatos (seções 8.2 e 8.3), e sem enviar o arquivo a servidores do GHF Software.
- **O que o arquivo contém:** nome, observações, coordenadas, altitude, resultados calculados e rótulos de ponto de cada medição salva — os mesmos dados já descritos na seção 8.1, reunidos num arquivo só.
- **Restaurar:** ao escolher "Restaurar backup" e selecionar um arquivo (pelo mesmo seletor do sistema), as medições do arquivo são acrescentadas ao histórico do dispositivo. Nada do que já está salvo é apagado, e medições já existentes são identificadas e não duplicadas. Um arquivo gerado por uma versão mais nova do TopoWalk do que a instalada é recusado, para não corromper o banco de dados local.
- **Controle do usuário:** o GHF Software não tem acesso a esse arquivo em nenhum momento — ele existe apenas no local que o próprio usuário escolheu ao gravá-lo, sob o controle e a responsabilidade dele (incluindo a segurança de sua própria conta Google Drive, se for esse o destino escolhido).

Este mecanismo é independente do Backup Automático do sistema Android, descrito na seção 8.5.

### 8.5 Backup Automático do Sistema Android

O TopoWalk **não opera nenhum serviço de backup ou sincronização em nuvem próprio**. No entanto, o aplicativo não desativa o recurso de **Backup automático do Android** ("Backup by Google"), que é um mecanismo do próprio sistema operacional, independente do TopoWalk:

- Se o usuário tiver esse recurso ativado em sua conta Google (é o padrão de fábrica na maioria dos aparelhos Android) e o aparelho satisfizer as condições definidas pelo próprio Android (conectado ao Wi-Fi, carregando e ocioso), o sistema operacional pode, periodicamente e em segundo plano, incluir os dados do TopoWalk — incluindo o banco de dados local do histórico de medições — no backup da conta Google do usuário.
- Esse backup é armazenado e gerenciado pela **infraestrutura do Google**, associada à própria conta Google do usuário — o GHF Software não tem acesso a esse backup, não o recebe, não o controla e não pode excluí-lo.
- Caso o usuário reinstale o TopoWalk no mesmo aparelho ou em outro aparelho conectado à mesma conta Google, o Android pode restaurar automaticamente esses dados a partir desse backup.
- Usuários que não desejam que o histórico de medições seja incluído nesse backup do sistema podem desativar o "Backup do Google" para o dispositivo, ou para o TopoWalk especificamente, nas configurações do Android (Configurações → Sistema → Backup, variando conforme o fabricante e a versão do Android).

**Atenção quanto à identidade visual do relatório (seção 2.8):** o logotipo copiado e os dados da empresa ficam na área privada e nas preferências do aplicativo, e por isso também podem ser incluídos nesse backup automático do sistema — na conta Google do próprio usuário, sempre fora do alcance do GHF Software. Quem não quiser isso pode desativar o backup do sistema conforme descrito acima.

Esta seção descreve o comportamento padrão do Android para o gerenciamento de dados. Ela não altera nenhum outro compromisso desta política: o GHF Software continua sem operar servidores próprios de armazenamento de dados do usuário e sem ter acesso a esse conteúdo em nenhum momento.

### 8.6 Dados fora do aparelho (migração do Pro)

Todo o restante da seção 8 descreve armazenamento **no próprio aparelho**. A única exceção do
aplicativo é o serviço de migração do Pro (seção 2.11), que guarda num servidor do GHF Software
um identificador embaralhado do aparelho, um identificador de sessão anônima, a data do pedido
e o código entregue — nada mais, e nada que identifique a pessoa. Os levantamentos, as fotos e
os relatórios **nunca** saem do aparelho por esse caminho.

---

## 9. Permissões do Aplicativo

| Permissão | Motivo |
|---|---|
| `ACCESS_FINE_LOCATION` | Obter coordenadas GPS precisas para os pontos de medição |
| `ACCESS_COARSE_LOCATION` | Permissão complementar exigida pelo Android para localização |
| `INTERNET` | Carregar tiles de mapa do OpenStreetMap, enviar eventos ao Firebase Analytics e relatórios de falha ao Crashlytics e, **quando o usuário pede a migração do Pro** (seção 2.11), falar com o nosso servidor |
| `VIBRATE` | Feedback háptico ao capturar um ponto de medição |
| `BLUETOOTH_CONNECT` (Android 12+) | Conectar a um receptor GNSS/RTK externo já pareado, quando o recurso é ativado pelo usuário |
| `BLUETOOTH` / `BLUETOOTH_ADMIN` (Android 11 e anteriores) | Equivalente às versões antigas do Android para a mesma conexão |
| `com.android.vending.BILLING` (a partir da versão 4.1) | Exigida pelo Google Play para oferecer a compra do TopoWalk Pro. É adicionada automaticamente pela biblioteca do Google e **não dá acesso a nenhum dado do aparelho** |

**A bússola usada na Locação (seção 2.7) e a escolha do logotipo (seção 2.8) não exigem permissão alguma:** sensores de orientação são livres no Android, e o seletor de arquivos entrega ao aplicativo apenas o único arquivo que o usuário escolher.

O aplicativo não solicita acesso ao microfone, aos contatos nem ao armazenamento externo. **Também não solicita permissão de câmera** — as fotos de campo (seção 2.10) entram pelo aplicativo de câmera do sistema e pelo seletor de fotos do Android, que entregam ao TopoWalk somente o arquivo escolhido pelo usuário. O ID de publicidade (`AD_ID`) é explicitamente removido do app e não é coletado.

---

## 10. Uso por Menores

O TopoWalk não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados de menores. Por se tratar de uma ferramenta técnica de campo, o uso por menores deve ocorrer sob supervisão de um adulto responsável.

A partir da versão 4.1, a compra do TopoWalk Pro é processada pelo Google Play e está sujeita aos controles parentais e às exigências de autenticação desse serviço (seção 6). O TopoWalk não realiza verificação de idade própria.

---

## 11. Segurança

Os dados de medição do TopoWalk são processados e armazenados exclusivamente no dispositivo do usuário. A comunicação com serviços externos (Firebase Analytics e OpenStreetMap) é realizada exclusivamente via HTTPS com criptografia em trânsito. Os dados enviados ao Firebase não contêm informações pessoais identificáveis. A segurança dos dados armazenados localmente é gerenciada pelo sistema operacional Android e pelo isolamento de aplicativos (sandbox).

A partir da versão 4.1, **nenhum dado de pagamento transita pelo aplicativo**: a compra é conduzida inteiramente pela tela do Google Play, e o TopoWalk recebe de volta apenas a informação de que existe ou não uma compra ativa (seção 6).

---

## 12. Alterações nesta Política

Podemos atualizar esta Política de Privacidade periodicamente. Alterações relevantes serão comunicadas por meio de uma nova versão do aplicativo publicada na Google Play Store. A data de "Última atualização" no topo deste documento sempre refletirá a versão vigente.

Recomendamos que você revise esta política periodicamente.

---

## 13. Contato

Dúvidas, solicitações ou comentários sobre esta Política de Privacidade podem ser enviados para:

**GHF Software**
E-mail: **support@ghfsoftware.com**

---

*Esta política foi elaborada em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018), o Regulamento Geral de Proteção de Dados da União Europeia (GDPR) e as políticas de privacidade da Google Play Store.*
