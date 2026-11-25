// Dados de cada app na Google Play (WP-11, ADR-005 §6): uma fonte para o botão "Google Play" da
// landing e da home e para o JSON-LD `MobileApplication` — os dois não têm como divergir.
//
// `categoria` é o enum do schema.org/Google (`*Application`), mapeado da categoria da ficha da Play
// (D17, lida no JSON-LD público da ficha em 2026-10-15; o valor cru da Play vai no comentário, para
// quem conferir). Os 4 apps são gratuitos para baixar: `offers` com preço 0 BRL. Preço do Premium
// ou do Pro nunca entra (vem da Play e do Remote Config), nem `aggregateRating`/`review`.
// App que mudar de categoria ou deixar de ser gratuito muda uma linha aqui.

import { hreflang, rota, type Idioma } from './idiomas';
import { SITE } from './ui';

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
  /** caminho pt dos termos de uso, quando o app tem (URL contratual, ADR-001); o Footer lista */
  termos?: string;
  /** caminho do favicon do app em public/assets/ (URL fixa, ADR-006): o `favicon` do Base na
   *  landing e o `image` do JSON-LD (ADR-009) */
  icone: string;
  /** tag de release do app no repositório dele, cuja data de commit é `atualizadoEm`
   *  (`check_site.py` §21 confere as duas) */
  tag: string;
  /** Última atualização do app: data (AAAA-MM-DD) do commit da tag de release no repositório do app,
   *  `git log -1 --format=%cs <tag>`, conferida em 2026-11-22 (D30). Muda a cada release publicada. */
  atualizadoEm: string;
  /** só para app retirado da Play: vai para "ver todas" com o selo "Indisponível" e só o link da
   *  política (`GHF Kit v3` §6, D12) */
  indisponivel?: true;
}

const PLAY = 'https://play.google.com/store/apps/details?id=';

// Formato lido por tools/regras_apps.py (check_site.py §20 e §21): um `campo: 'valor'` por chave,
// aspas simples; `indisponivel: true` sem aspas. Campo novo lido pelo Python entra lá também.

export const apps = {
  // Play: TOOLS
  lottoexpert: {
    nome: 'LottoExpert', id: 'br.com.ghfsoftware.lottoexpert', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.lottoexpert`,
    pagina: 'lottoexpert.html', privacidade: 'lottoexpert-privacy.html', termos: 'lottoexpert-terms.html',
    icone: '/assets/lottoexpert_favicon_v3.png', tag: 'v2.05.03', atualizadoEm: '2026-10-12',
  },
  // Play: TOOLS
  topowalk: {
    nome: 'TopoWalk', id: 'br.com.ghfsoftware.topowalk', categoria: 'UtilitiesApplication', play: `${PLAY}br.com.ghfsoftware.topowalk`,
    pagina: 'topowalk.html', privacidade: 'topowalk-privacy.html', termos: 'topowalk-terms.html',
    icone: '/assets/topo-walk.png', tag: 'v4.4.0', atualizadoEm: '2026-10-29',
  },
  // Play: SPORTS (repositório ../pole-position-app)
  poleposition: {
    nome: 'Pole Position', id: 'br.com.ghfsoftware.polepositionapp', categoria: 'SportsApplication', play: `${PLAY}br.com.ghfsoftware.polepositionapp`,
    pagina: 'poleposition.html', privacidade: 'poleposition-privacy.html',
    icone: '/assets/poleposition.png', tag: 'v2.2.0', atualizadoEm: '2026-10-16',
  },
  // Play: LIFESTYLE (a tag v1.0.1 é leve, criada em 2026-11-22 sobre f5c1d6b)
  eclipsego: {
    nome: 'EclipseGo', id: 'br.com.ghfsoftware.eclipsego', categoria: 'LifestyleApplication', play: `${PLAY}br.com.ghfsoftware.eclipsego`,
    pagina: 'eclipsego.html', privacidade: 'eclipsego-privacy.html',
    icone: '/assets/eclipse-go-favicon.png', tag: 'v1.0.1', atualizadoEm: '2026-07-26',
  },
} as const satisfies Record<string, App>;

export type ChaveApp = keyof typeof apps;

/** Id do acento de cada app em src/styles/tokens.css (`[data-app=…]`, `GHF Kit v3` §acento):
 *  o valor de `data-app` no `<html>` (Base.astro, WP-10 fatia 2). Um mapa só. */
export const ACENTO: Record<ChaveApp, 'lotto' | 'topo' | 'pole' | 'eclipse'> = {
  lottoexpert: 'lotto',
  topowalk: 'topo',
  poleposition: 'pole',
  eclipsego: 'eclipse',
};

/** Ordem de toda lista de apps (brief §10, mesmo peso): a fonte única. Home, Footer e 404 leem
 *  daqui (WP-10, fatia 10a; APPS-LISTA-DUPLICADA-01). */
export const ORDEM_APPS = ['lottoexpert', 'topowalk', 'poleposition', 'eclipsego'] as const satisfies readonly ChaveApp[];

/** Cor de cada app (faixa, quadrado e seta): classe inteira literal, porque o Tailwind não detecta
 *  concatenação; ele varre os `.ts` de src/. */
export const COR_APP: Record<ChaveApp, { fundo: string; texto: string }> = {
  lottoexpert: { fundo: 'bg-app-lotto', texto: 'text-app-lotto' },
  topowalk: { fundo: 'bg-app-topo', texto: 'text-app-topo' },
  poleposition: { fundo: 'bg-app-pole', texto: 'text-app-pole' },
  eclipsego: { fundo: 'bg-app-eclipse', texto: 'text-app-eclipse' },
};

/** Canais da GHF: o padrão do Footer e o `sameAs` do JSON-LD `Organization` (ADR-009). */
export const REDES_GHF = {
  youtube: 'https://www.youtube.com/channel/UCZfKMp0qRRIEu103Vb3OGJg',
  instagram: 'https://www.instagram.com/ghfsoftware/',
};

/** Data de hoje do build. `GHF_HOJE=AAAA-MM-DD` só para teste da regra de destaque (verificação 4 da
 *  especificação da fatia 6), nunca no CI nem no deploy. */
export function hojeDoBuild(): Date {
  const forcada = process.env.GHF_HOJE;
  if (forcada) {
    // Guarda: a data forçada nunca chega ao dist/ do PR nem do deploy.
    if (process.env.CI || process.env.GITHUB_ACTIONS) throw new Error('GHF_HOJE é só para teste local; não use no CI nem no deploy');
    const d = new Date(forcada + 'T00:00:00Z');
    // Mesmo teste de `atualizadoEm`: o regex sozinho deixa passar 2027-13-45 (Invalid Date) e 2027-02-30.
    if (!/^\d{4}-\d{2}-\d{2}$/.test(forcada) || Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== forcada) {
      throw new Error(`GHF_HOJE=${forcada}: não é uma data AAAA-MM-DD válida`);
    }
    return d;
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
export function dataCurta(iso: string, lang: Idioma): string {
  // Locale do idiomas.json (fonte única das línguas): uma língua nova sai com a data dela, não em en.
  return new Intl.DateTimeFormat(hreflang(lang), { dateStyle: 'medium', timeZone: 'UTC' }).format(
    new Date(iso + 'T00:00:00Z'),
  );
}

/** JSON-LD `MobileApplication` da landing (ADR-005 §6, ampliado pelo ADR-009): só campo derivado
 *  de dado que a página já publica. `descricao` é a `meta description` da landing (a mesma string do
 *  `Base`); `url` é a canônica; `image`, o favicon do app (o mesmo arquivo do `favicon` do `Base`);
 *  `availability` sai de o app não ser `indisponivel`. */
export function mobileApplication(chave: ChaveApp, lang: Idioma, descricao: string) {
  const a: App = apps[chave];
  return {
    '@context': 'https://schema.org',
    '@type': 'MobileApplication',
    name: a.nome,
    url: SITE + rota(lang, a.pagina),
    description: descricao,
    image: SITE + a.icone,
    operatingSystem: 'Android',
    applicationCategory: a.categoria,
    installUrl: PLAY + a.id,
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'BRL',
      ...(a.indisponivel ? {} : { availability: 'https://schema.org/InStock' }),
    },
  };
}

/** JSON-LD `Organization` da home (ADR-009): `descricao` é a `meta description` da home na língua;
 *  `fundacao`, o ano do "Desde 2004" que a home publica (resposta do usuário, 2026-11-22: é o ano
 *  de fundação); `sameAs`, os canais do rodapé (REDES_GHF). */
export function organization(descricao: string, fundacao: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'GHF Software',
    url: 'https://ghfsoftware.com/',
    logo: 'https://ghfsoftware.com/assets/GHFSoftware.png',
    description: descricao,
    foundingDate: fundacao,
    sameAs: Object.values(REDES_GHF),
  };
}
