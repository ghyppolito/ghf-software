// Conteúdo da landing do EclipseGo (eclipsego.html), pt e en, no formato único de landing.ts (WP-10,
// fatia 5; D29). Origem de cada frase (D25):
// - `meta`: o `title` e a `description` já publicados (WP-21: o `title` é o `hero_badge`; a
//   `description` é o "Resumo em uma frase" de ../eclipse-go/docs/EclipseGoContent.md).
// - `resumo`: as chaves `app_eclipse_tag`, `app_eclipse_desc` e `hero_eclipse_desc` da home
//   antiga, movidas sem edição; o card da Home lê daqui `tag` e `curta` (WP-10, fatia 6).
// - `hero`: `hero_badge`, `hero_title_1` + `hero_title_2` e `hero_desc` publicados; a `meta` é a
//   resposta 3 do usuário (2026-11-22: app gratuito; `minSdk 26` do README = Android 8.0).
// - `funcionalidades`: `feat3_*`, `feat2_*` e `feat4_*` publicados (o `feat1` "100% Offline" virou
//   a prova 1); só a primeira tem captura (resposta 1 do usuário). `alt` traduzido no en
//   (ECLIPSE-EN-ROTULOS-PT-01).
// - `prova`, `privacidade` e `faq`: README e política de privacidade do app (§1, §2.1), SPEC §2.6 e
//   §3.5, e `app/src/main/assets/eclipses.json` (139 eclipses, 2017-02-11 a 2047-12-16, conferido
//   em 2026-11-22: se o arquivo mudar, a pergunta 3 muda).
import type { Idioma } from './idiomas';
import type { ConteudoApp } from './landing';

export const eclipsego = {
  pt: {
    meta: {
      title: 'EclipseGo: Previsão de Eclipses Offline — GHF Software',
      description:
        'Descubra se e quando você vai poder ver o próximo eclipse solar ou lunar, sem precisar de internet.',
    },
    resumo: {
      tag: 'Astronomia & GPS',
      descricao:
        'Cálculo local de visibilidade e linha do tempo de eclipses solares e lunares. Totalmente offline com suporte a GPS e busca por cidades.',
      curta: 'Previsão local de eclipses 100% offline.',
    },
    hero: {
      kicker: 'Previsão de Eclipses Offline',
      titulo: 'EclipseGo: Sombra & Luz no seu Bolso',
      lead: 'Saiba exatamente se um eclipse solar ou lunar é visível de onde você está. Um aplicativo totalmente offline que calcula horários locais de início, pico e fim sem fazer qualquer chamada de rede.',
      meta: '100% offline · Android 8.0 ou superior · Grátis',
      alt: 'Mão segurando o celular com o EclipseGo aberto no eclipse solar total de 12 de agosto de 2026, visto de Praia, Cabo Verde.',
    },
    funcionalidades: [
      {
        titulo: 'Linha do Tempo do Evento',
        descricao:
          'Gráfico interativo e slider que demonstram o progresso exato da cobertura (início → pico → fim) no fuso horário local.',
        imagem: 'tela',
        alt: 'Tela do EclipseGo no eclipse solar total de 12 de agosto de 2026: céu simulado, linha do tempo da simulação, seletor de localização e horários de início, pico e fim do parcial.',
      },
      {
        titulo: 'Modos de Localização',
        icone: 'location-crosshairs',
        descricao:
          'Minha localização (GPS), busca por cidade ou a ferramenta exclusiva que localiza o ponto de melhor visibilidade mais próximo de você.',
      },
      {
        titulo: 'Calendário Completo',
        icone: 'calendar-days',
        descricao:
          'Acesse o histórico e as datas futuras de eclipses solares e lunares com mecanismos rápidos de busca e filtragem.',
      },
    ],
    prova: [
      { titulo: '100% offline', texto: 'Eclipses, cidades e cálculos de visibilidade ficam no próprio aparelho.' },
      { titulo: 'Sem chamadas de rede', texto: 'O app não depende de internet nem de backend próprio.' },
      {
        titulo: 'Cidades no aparelho',
        texto: 'Mais de 34 mil cidades, com busca sem acento e sem distinção de maiúsculas.',
      },
    ],
    privacidade:
      'O EclipseGo não realiza chamadas de rede, não possui servidores próprios e não coleta, transmite ou compartilha dados pessoais com terceiros.',
    faq: [
      {
        pergunta: 'Funciona sem internet?',
        resposta:
          'Sim, totalmente offline. Os dados de eclipses, as cidades e os cálculos de visibilidade vêm empacotados no próprio aparelho.',
      },
      {
        pergunta: 'Preciso liberar a localização?',
        resposta:
          'Não. A permissão de localização é opcional. Sem GPS ou sem permissão, o app usa uma cidade padrão, e você pode buscar qualquer cidade.',
      },
      {
        pergunta: 'Quais anos o app cobre?',
        resposta: 'De 2017 a 2047: 139 eclipses solares e lunares, todos empacotados no app.',
      },
      {
        pergunta: 'E se o eclipse não for visível do meu local?',
        resposta:
          'O app avisa e deixa você trocar para a melhor localização visível mais próxima ou escolher qualquer outra.',
      },
    ],
  },
  en: {
    meta: {
      title: 'EclipseGo: Offline Eclipse Prediction — GHF Software',
      description:
        'Find out if and when you will be able to see the next solar or lunar eclipse, no internet needed.',
    },
    resumo: {
      tag: 'Astronomy & GPS',
      descricao:
        'Local calculations of solar and lunar eclipse visibility and timeline. Fully offline with GPS support and city database search.',
      curta: '100% offline local eclipse forecasting.',
    },
    hero: {
      kicker: 'Offline Eclipse Prediction',
      titulo: 'EclipseGo: Shadow & Light in Your Pocket',
      lead: 'Know exactly if a solar or lunar eclipse is visible from your location. A fully offline application that calculates local start, peak, and end times without making any network calls.',
      meta: '100% offline · Android 8.0 or later · Free',
      alt: 'Hand holding a phone with EclipseGo open on the total solar eclipse of August 12, 2026, seen from Praia, Cape Verde (app interface in Portuguese).',
    },
    funcionalidades: [
      {
        titulo: 'Event Timeline',
        descricao:
          'Interactive graphic and slider showing the exact progress of coverage (start → peak → end) in your local timezone.',
        imagem: 'tela',
        alt: 'EclipseGo screen for the total solar eclipse of August 12, 2026: simulated sky, simulation timeline, location selector, and the start, peak, and end times of the partial phase (app interface in Portuguese).',
      },
      {
        titulo: 'Location Modes',
        icone: 'location-crosshairs',
        descricao:
          'My location (GPS), city search, or the exclusive tool that finds the nearest location with the best visibility.',
      },
      {
        titulo: 'Full Calendar',
        icone: 'calendar-days',
        descricao:
          'Access past and future dates of solar and lunar eclipses with fast searching and filtering mechanisms.',
      },
    ],
    prova: [
      { titulo: '100% offline', texto: 'Eclipses, cities, and visibility calculations stay on the device.' },
      { titulo: 'No network calls', texto: 'The app depends on neither the internet nor a backend of its own.' },
      { titulo: 'Cities on the device', texto: 'Over 34,000 cities, with search that ignores accents and letter case.' },
    ],
    privacidade:
      'EclipseGo does not make network calls, does not have its own servers, and does not collect, transmit, or share personal data with third parties.',
    faq: [
      {
        pergunta: 'Does it work without internet?',
        resposta:
          'Yes, fully offline. The eclipse data, the cities, and the visibility calculations are packaged on your device.',
      },
      {
        pergunta: 'Do I have to allow location access?',
        resposta:
          'No. Location permission is optional. Without GPS or permission, the app uses a default city, and you can search for any city.',
      },
      {
        pergunta: 'Which years does the app cover?',
        resposta: 'From 2017 to 2047: 139 solar and lunar eclipses, all packaged in the app.',
      },
      {
        pergunta: 'What if the eclipse is not visible from my location?',
        resposta:
          'The app tells you and lets you switch to the nearest location where it is visible, or choose any other.',
      },
    ],
  },
} satisfies Record<Idioma, ConteudoApp>;
