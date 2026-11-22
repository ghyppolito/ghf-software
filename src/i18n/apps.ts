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
  /** link do botão "Google Play": sem `hl`, a Play abre na língua da conta (WP-22; o TopoWalk levava
   *  `&hl=pt_BR` e mandava quem lê em inglês para a ficha em pt) */
  play: string;
  /** caminho pt da landing e da política (os mesmos do Footer e da 404; contrato ADR-001 no caso da
   *  política). O link passa por `link(lang, …)` de idiomas.ts (D23). */
  pagina: string;
  privacidade: string;
  /** Última atualização do app: data (AAAA-MM-DD) do commit da tag de release no repositório do app,
   *  `git log -1 --format=%cs <tag>`, conferida em 2026-11-22 (D30). Muda a cada release publicada. */
  atualizadoEm: string;
  /** só para app retirado da Play: vai para "ver todas" com o selo "Indisponível" e só o link da
   *  política (`GHF Kit v3` §6, D12) */
  indisponivel?: true;
}

const PLAY = 'https://play.google.com/store/apps/details?id=';

export const apps = {
  // Play: TOOLS. Tag v2.05.03
  lottoexpert: {
    nome: 'LottoExpert', id: 'br.com.ghfsoftware.lottoexpert', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.lottoexpert`,
    pagina: 'lottoexpert.html', privacidade: 'lottoexpert-privacy.html', atualizadoEm: '2026-10-12',
  },
  // Play: TOOLS. Tag v4.4.0
  topowalk: {
    nome: 'TopoWalk', id: 'br.com.ghfsoftware.topowalk', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.topowalk`,
    pagina: 'topowalk.html', privacidade: 'topowalk-privacy.html', atualizadoEm: '2026-10-29',
  },
  // Play: SPORTS. Tag v2.2.0 (repositório ../pole-position/pole-position-app)
  poleposition: {
    nome: 'Pole Position', id: 'br.com.ghfsoftware.polepositionapp', categoria: 'SportsApplication', play: `${PLAY}br.com.ghfsoftware.polepositionapp`,
    pagina: 'poleposition.html', privacidade: 'poleposition-privacy.html', atualizadoEm: '2026-10-16',
  },
  // Play: LIFESTYLE. Tag v1.0.1 (tag leve, criada em 2026-11-22 sobre f5c1d6b)
  eclipsego: {
    nome: 'EclipseGo', id: 'br.com.ghfsoftware.eclipsego', categoria: 'LifestyleApplication', play: `${PLAY}br.com.ghfsoftware.eclipsego`,
    pagina: 'eclipsego.html', privacidade: 'eclipsego-privacy.html', atualizadoEm: '2026-07-26',
  },
} as const satisfies Record<string, App>;

export type ChaveApp = keyof typeof apps;

/** Id do acento de cada app em src/styles/tokens.css (`:root[data-app=…]`, `GHF Kit v3` §acento):
 *  o valor de `data-app` no `<html>` (Base.astro, WP-10 fatia 2). Um mapa só. */
export const ACENTO: Record<ChaveApp, 'lotto' | 'topo' | 'pole' | 'eclipse'> = {
  lottoexpert: 'lotto',
  topowalk: 'topo',
  poleposition: 'pole',
  eclipsego: 'eclipse',
};

/** Ordem de toda lista de apps (brief §10, mesmo peso): a fonte única. Footer e 404 passam a ler
 *  daqui na fatia 10a do WP-10 (APPS-LISTA-DUPLICADA-01); por ora só a Home lê. */
export const ORDEM_APPS = ['lottoexpert', 'topowalk', 'poleposition', 'eclipsego'] as const satisfies readonly ChaveApp[];

/** Data de hoje do build. `GHF_HOJE=AAAA-MM-DD` só para teste da regra de destaque (verificação 4 da
 *  especificação da fatia 6), nunca no CI nem no deploy. */
export function hojeDoBuild(): Date {
  const forcada = process.env.GHF_HOJE;
  if (forcada) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(forcada)) throw new Error(`GHF_HOJE=${forcada}: formato não é AAAA-MM-DD`);
    return new Date(forcada + 'T00:00:00Z');
  }
  return new Date();
}

/** Regra D12 (`GHF Kit v3` §6): entra em `destaque`, na ordem de `ORDEM_APPS`, o app que não é
 *  `indisponivel` e cuja `atualizadoEm` é ≥ hoje − 12 meses, até 4; o resto vai para `resto`, na
 *  mesma ordem. Com 5+ apps, o desempate passa a ser a data de publicação (`publicadoEm`, ainda não
 *  existe). A data decide no build: refazer o `dist/` depois do vencimento tira o app da grade sem
 *  commit. Erro de build: `atualizadoEm` fora de AAAA-MM-DD ou no futuro, ou `ORDEM_APPS` sem
 *  exatamente as chaves de `apps`. "Nenhum destaque" não é erro: barrar o build derrubaria um
 *  hotfix legal (D13 item 6). */
export function particionarApps(hoje: Date): { destaque: ChaveApp[]; resto: ChaveApp[] } {
  const chaves = Object.keys(apps).sort();
  const ordem = [...ORDEM_APPS].sort();
  if (chaves.length !== ordem.length || chaves.some((c, i) => c !== ordem[i])) {
    throw new Error(`ORDEM_APPS (${ORDEM_APPS.join(', ')}) não tem exatamente as chaves de apps (${chaves.join(', ')})`);
  }
  const corte = new Date(Date.UTC(hoje.getUTCFullYear() - 1, hoje.getUTCMonth(), hoje.getUTCDate()));
  const destaque: ChaveApp[] = [];
  const resto: ChaveApp[] = [];
  for (const c of ORDEM_APPS) {
    const a: App = apps[c];
    const data = a.atualizadoEm;
    const d = new Date(data + 'T00:00:00Z');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(data) || Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== data) {
      throw new Error(`${a.nome}: atualizadoEm "${data}" não é uma data AAAA-MM-DD`);
    }
    if (d.getTime() > hoje.getTime()) throw new Error(`${a.nome}: atualizadoEm ${data} está no futuro`);
    if (!a.indisponivel && d.getTime() >= corte.getTime() && destaque.length < 4) destaque.push(c);
    else resto.push(c);
  }
  return { destaque, resto };
}

/** Data curta do card ("26 de jul. de 2026" / "Jul 26, 2026"): `medium`, porque o `long` quebra em
 *  duas linhas no card de 1280 px. Em UTC, para não cair no dia anterior. */
export function dataCurta(iso: string, lang: string): string {
  return new Intl.DateTimeFormat(lang === 'pt' ? 'pt-BR' : 'en-US', { dateStyle: 'medium', timeZone: 'UTC' }).format(
    new Date(iso + 'T00:00:00Z'),
  );
}

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
