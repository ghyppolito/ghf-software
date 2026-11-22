// Formato único do conteúdo de uma landing de app (WP-10, fatia 5; D29). Template em
// src/components/landing/ (`Landing App.dc.html` da rodada 3); cada app tem um dicionário
// `src/i18n/<app>.ts` com `{ pt, en } satisfies Record<Idioma, ConteudoApp>`.
//
// Copy (D25): cada frase do conteúdo vem do dicionário publicado, do README/ASO do app ou de uma
// resposta do usuário registrada no WP; nunca do export. Os rótulos de interface de
// `rotulosLanding` são os de `content/i18n.js` do export.
//
// Espelho (ADR-007): `exigeEspelho` falha o build se uma língua tem bloco, item ou imagem que a
// outra não tem, ou texto vazio. Não há faixa de "língua parcial" (`LA:13-20` do export).
import { rota, type Idioma } from './idiomas';
import type { ChaveUi } from './ui';
import type { ChaveApp } from './apps';

export interface Etiqueta {
  texto: string;
  /** etiqueta do plano pago: no acento do app */
  pro?: boolean;
}

export interface Funcionalidade {
  titulo: string;
  descricao: string;
  etiqueta?: Etiqueta;
  /** chave em `imagens.funcionalidades` do `Landing`, igual em todas as línguas */
  imagem?: string;
  /** obrigatório se há imagem */
  alt?: string;
}

export interface GrupoTodas {
  titulo: string;
  itens: { nome: string; descricao: string; etiqueta?: Etiqueta }[];
}

export interface Fato {
  titulo: string;
  texto: string;
}

export interface Pergunta {
  pergunta: string;
  resposta: string;
}

export type Planos = {
  lead: string;
  /** nota do plano; `selo` é o círculo ao lado (o "18" do LottoExpert); `termos` é o caminho pt da
   *  página de termos, ex.: 'lottoexpert-terms.html' */
  nota?: { texto: string; selo?: string; termos?: string };
} & (
  | {
      tipo: 'niveis';
      niveis: { nome: string; preco: string; periodo?: string; descricao: string; destaque?: boolean }[];
      comparacao: {
        colRecurso: string;
        colGratis: string;
        colPago: string;
        colPagoSub: string;
        linhas: [string, string, string][];
      };
    }
  | {
      tipo: 'gratis-pro';
      gratis: { titulo: string; sub: string; itens: string[] };
      pro: { titulo: string; sub: string; itens: { nome: string; descricao: string }[]; nota?: string };
    }
);

export interface ConteudoApp {
  /** <head>; og e twitter repetem (WP-21) */
  meta: { title: string; description: string };
  /** lido pela Home (fatia 6) */
  resumo: { tag: string; descricao: string; curta: string };
  hero: { kicker?: string; titulo: string; lead: string; meta?: string; alt: string };
  /** 1 a 4 (Kit v3: no máximo 4 destaques) */
  funcionalidades: Funcionalidade[];
  todas?: GrupoTodas[];
  /** 2 a 4 */
  prova?: Fato[];
  planos?: Planos;
  /** uma frase; o link da política vem do rótulo */
  privacidade: string;
  faq: Pergunta[];
  /** aviso no fim da página (jogo responsável do LottoExpert, fatia 9) */
  aviso?: string;
}

interface RotulosLanding {
  cta: string;
  features: string;
  seeAll: string;
  proof: string;
  faq: string;
  plans: string;
  freepro: string;
  privacy: string;
  privacyPolicy: string;
  /** com `{app}` no lugar do nome */
  ctaH: string;
  terms: string;
}

// `cta`, `features`, `seeAll`, `proof`, `faqH`, `plans`, `freepro`, `privacy`, `privacyPolicy`,
// `ctaH` e `terms` de `content/i18n.js` do export (rodada 3).
export const rotulosLanding: Record<Idioma, RotulosLanding> = {
  pt: {
    cta: 'Baixar na Google Play',
    features: 'Funcionalidades',
    seeAll: 'Ver todas as funcionalidades',
    proof: 'Como o app trabalha',
    faq: 'Perguntas frequentes',
    plans: 'Planos',
    freepro: 'Grátis e Pro',
    privacy: 'Privacidade',
    privacyPolicy: 'Política de privacidade',
    ctaH: 'Baixe o {app}',
    terms: 'Termos de uso',
  },
  en: {
    cta: 'Get it on Google Play',
    features: 'Features',
    seeAll: 'See all features',
    proof: 'How the app works',
    faq: 'Frequently asked questions',
    plans: 'Plans',
    freepro: 'Free & Pro',
    privacy: 'Privacy',
    privacyPolicy: 'Privacy policy',
    ctaH: 'Get {app}',
    terms: 'Terms of use',
  },
};

/** Todo texto (string) de um valor, com o caminho, para achar o vazio. */
function textos(valor: unknown, caminho: string, saida: [string, string][]): [string, string][] {
  if (typeof valor === 'string') saida.push([caminho, valor]);
  else if (Array.isArray(valor)) valor.forEach((v, i) => textos(v, `${caminho}[${i}]`, saida));
  else if (valor && typeof valor === 'object') {
    for (const [k, v] of Object.entries(valor)) textos(v, caminho ? `${caminho}.${k}` : k, saida);
  }
  return saida;
}

/** Forma de um conteúdo sem o texto: blocos presentes, contagens, chaves de imagem e flags `pro`.
 *  Duas línguas com a mesma forma são espelho uma da outra. */
function forma(c: ConteudoApp): unknown {
  return {
    hero: { kicker: c.hero.kicker !== undefined, meta: c.hero.meta !== undefined },
    funcionalidades: c.funcionalidades.map((f) => ({
      imagem: f.imagem ?? null,
      etiqueta: f.etiqueta ? { pro: !!f.etiqueta.pro } : null,
    })),
    todas: c.todas?.map((g) => g.itens.map((i) => (i.etiqueta ? { pro: !!i.etiqueta.pro } : null))) ?? null,
    prova: c.prova?.length ?? null,
    planos: c.planos
      ? {
          tipo: c.planos.tipo,
          nota: c.planos.nota ? { selo: c.planos.nota.selo !== undefined, termos: c.planos.nota.termos ?? null } : null,
          ...(c.planos.tipo === 'niveis'
            ? { niveis: c.planos.niveis.map((n) => !!n.destaque), linhas: c.planos.comparacao.linhas.length }
            : { gratis: c.planos.gratis.itens.length, pro: c.planos.pro.itens.length, notaPro: c.planos.pro.nota !== undefined }),
        }
      : null,
    faq: c.faq.length,
    aviso: c.aviso !== undefined,
  };
}

/** Falha o build se as línguas de uma landing não são espelho (ADR-007) ou se o conteúdo sai do
 *  template: texto vazio, imagem sem `alt` ou sem arquivo, mais de 4 destaques ou fatos. */
export function exigeEspelho(app: string, c: Record<Idioma, ConteudoApp>, chavesImagem: string[] = []): void {
  const erros: string[] = [];
  const linguas = Object.keys(c) as Idioma[];
  const base = linguas[0];
  for (const l of linguas) {
    const x = c[l];
    for (const [onde, texto] of textos(x, '', [])) {
      if (texto.trim() === '') erros.push(`[${l}] ${onde}: texto vazio`);
    }
    if (x.funcionalidades.length < 1 || x.funcionalidades.length > 4) {
      erros.push(`[${l}] funcionalidades: ${x.funcionalidades.length} (1 a 4)`);
    }
    if (x.prova && (x.prova.length < 2 || x.prova.length > 4)) erros.push(`[${l}] prova: ${x.prova.length} (2 a 4)`);
    x.funcionalidades.forEach((f, i) => {
      if (f.imagem === undefined) return;
      if (!f.alt) erros.push(`[${l}] funcionalidades[${i}]: imagem \`${f.imagem}\` sem alt`);
      if (!chavesImagem.includes(f.imagem)) erros.push(`[${l}] funcionalidades[${i}]: imagem \`${f.imagem}\` não passada ao Landing`);
    });
    if (l !== base && JSON.stringify(forma(x)) !== JSON.stringify(forma(c[base]))) {
      erros.push(`[${l}] não é espelho de [${base}]: blocos, contagens, imagens ou etiquetas pro diferem`);
    }
  }
  if (erros.length) throw new Error(`landing ${app}:\n  ${erros.join('\n  ')}`);
}

/** Itens do Nav da landing: as âncoras das seções que existem e a política do app. */
export function itensNav(c: ConteudoApp, lang: Idioma, app: ChaveApp): { href: string; chave: ChaveUi }[] {
  const itens: { href: string; chave: ChaveUi }[] = [{ href: '#funcionalidades', chave: 'nav_funcionalidades' }];
  if (c.planos) itens.push({ href: '#planos', chave: c.planos.tipo === 'gratis-pro' ? 'nav_gratis_pro' : 'nav_planos' });
  itens.push({ href: '#faq', chave: 'nav_faq' });
  itens.push({ href: rota(lang, `${app}-privacy.html`), chave: 'nav_privacidade' });
  return itens;
}
