// Dados de cada app na Google Play (WP-11, ADR-005 §6): uma fonte para o botão "Google Play" da
// landing e da home e para o JSON-LD `MobileApplication` — os dois não têm como divergir.
//
// `categoria` é o enum do schema.org/Google (`*Application`), mapeado da categoria da ficha da Play
// (D17, lida no JSON-LD público da ficha em 2026-10-15; o valor cru da Play vai no comentário, para
// quem conferir). Os 4 apps são gratuitos para baixar: `offers` com preço 0 BRL. Preço do Premium
// ou do Pro nunca entra (vem da Play e do Remote Config), nem `aggregateRating`/`review`.
// App que mudar de categoria ou deixar de ser gratuito muda uma linha aqui.

export interface App {
  /** nome do app (o mesmo da página) */
  nome: string;
  /** applicationId na Play */
  id: string;
  /** enum do schema.org para `applicationCategory` */
  categoria: 'UtilitiesApplication' | 'SportsApplication' | 'LifestyleApplication';
  /** link do botão "Google Play", como a página sempre publicou (o TopoWalk leva `&hl=pt_BR`) */
  play: string;
}

const PLAY = 'https://play.google.com/store/apps/details?id=';

export const apps = {
  // Play: TOOLS
  lottoexpert: { nome: 'LottoExpert', id: 'br.com.ghfsoftware.lottoexpert', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.lottoexpert` },
  // Play: TOOLS
  topowalk: { nome: 'TopoWalk', id: 'br.com.ghfsoftware.topowalk', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.topowalk&hl=pt_BR` },
  // Play: SPORTS
  poleposition: { nome: 'Pole Position', id: 'br.com.ghfsoftware.polepositionapp', categoria: 'SportsApplication', play: `${PLAY}br.com.ghfsoftware.polepositionapp` },
  // Play: LIFESTYLE
  eclipsego: { nome: 'EclipseGo', id: 'br.com.ghfsoftware.eclipsego', categoria: 'LifestyleApplication', play: `${PLAY}br.com.ghfsoftware.eclipsego` },
} as const satisfies Record<string, App>;

export type ChaveApp = keyof typeof apps;

/** JSON-LD `MobileApplication` da landing: exatamente as chaves do ADR-005 §6. */
export function mobileApplication(chave: ChaveApp) {
  const a = apps[chave];
  return {
    '@context': 'https://schema.org',
    '@type': 'MobileApplication',
    name: a.nome,
    operatingSystem: 'Android',
    applicationCategory: a.categoria,
    installUrl: PLAY + a.id,
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'BRL' },
  };
}

/** JSON-LD `Organization` da home. */
export const organization = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'GHF Software',
  url: 'https://ghfsoftware.com/',
  logo: 'https://ghfsoftware.com/assets/GHFSoftware.png',
};
