// Plugins do Sätteri (processador de markdown do Astro 7) para o texto legal de
// src/content/legal/ — só para esses arquivos; outro markdown passa intocado.
//
// O `.md` do app é copiado byte a byte, com `# Título` e `**Última atualização:** …` no corpo. A
// página mostra o título e a data no hero (data do front-matter `lastUpdated`): os dois saem do
// corpo renderizado, para aparecerem uma vez cada. O arquivo não é alterado.

const ROTULO_DATA = /^(Última atualização|Last updated):$/;

function ehLegal(ctx) {
  return Boolean(ctx.fileURL && ctx.fileURL.pathname.includes('/src/content/legal/'));
}

/** mdast: omite o primeiro `# …` e o parágrafo que começa por `**Última atualização:**`/`**Last updated:**`. */
export const omiteCabecalhoLegal = {
  name: 'ghf-omite-cabecalho-legal',
  heading(node, ctx) {
    if (!ehLegal(ctx) || node.depth !== 1 || ctx.data.ghfH1Omitido) return;
    ctx.data.ghfH1Omitido = true;
    ctx.removeNode(node);
  },
  paragraph(node, ctx) {
    if (!ehLegal(ctx) || ctx.data.ghfDataOmitida) return;
    const primeiro = node.children[0];
    if (primeiro?.type === 'strong' && ROTULO_DATA.test(ctx.textContent(primeiro).trim())) {
      ctx.data.ghfDataOmitida = true;
      ctx.removeNode(node);
    }
  },
};

/** hast: envolve a tabela num contêiner com rolagem horizontal (o `overflow-x-auto mb-4` da página antiga). */
export const envolveTabelaLegal = {
  name: 'ghf-envolve-tabela-legal',
  element: {
    filter: ['table'],
    visit(node, ctx) {
      if (!ehLegal(ctx)) return;
      ctx.wrapNode(node, { type: 'element', tagName: 'div', properties: { className: ['legal-tabela'] }, children: [] });
    },
  },
};

// Host do próprio site, com ou sem `www.`, por http ou https (o `.md` do app escreve `https://ghfsoftware.com/`).
const SITE = /^https?:\/\/(www\.)?ghfsoftware\.com\//i;

/** hast: link para o próprio site (`https://ghfsoftware.com/x.html`, como o `.md` do app escreve) vira
 *  caminho a partir da raiz (`/x.html`), na mesma aba, como a página antiga (WP-08, fatia 8: termos do
 *  LottoExpert, §8). No `.en.md`, página `.html` aponta para o par `/en/x.html` — desde a fatia 8 toda
 *  página `.html` do site tem par en (um par ausente quebra o link, e o §3 do `check_site.py` acusa);
 *  asset e o convite do bolão (`lotto-expert/…`) não têm par e ficam em `/`. O `.md` não é alterado:
 *  o `.en.md` mantém a URL do pt. Roda antes de `linksExternosLegais`. */
export const linksInternosLegais = {
  name: 'ghf-links-internos-legais',
  element: {
    filter: ['a'],
    visit(node, ctx) {
      if (!ehLegal(ctx)) return;
      const href = node.properties?.href;
      if (typeof href !== 'string' || !SITE.test(href)) return;
      const caminho = href.replace(SITE, '');
      const arquivo = caminho.split(/[?#]/)[0];
      const temPar = arquivo.endsWith('.html') && !arquivo.startsWith('lotto-expert/');
      const emIngles = ctx.fileURL.pathname.endsWith('.en.md');
      ctx.setProperty(node, 'href', (emIngles && temPar ? '/en/' : '/') + caminho);
    },
  },
};

/** hast: link externo (`href` começando por `http`) abre em outra aba, com `rel="noopener noreferrer"`.
 *  O markdown não tem `target`; as páginas antigas abriam em outra aba (WP-08, fatia 7). Sem `noopener`,
 *  a página aberta alcançaria esta por `window.opener` (`POLEPOSITION-NOOPENER-01`). `mailto:`,
 *  âncoras internas e o próprio site (`linksInternosLegais`) ficam como estão. */
export const linksExternosLegais = {
  name: 'ghf-links-externos-legais',
  element: {
    filter: ['a'],
    visit(node, ctx) {
      if (!ehLegal(ctx)) return;
      const href = node.properties?.href;
      if (typeof href !== 'string' || !/^https?:/i.test(href) || SITE.test(href)) return;
      ctx.setProperty(node, 'target', '_blank');
      ctx.setProperty(node, 'rel', ['noopener', 'noreferrer']);
    },
  },
};

/** hast: `id` dos títulos pela posição na hierarquia, igual em todas as línguas (ADR-007 §6,
 *  WP-15): o 2º `##` é `secao-2`, o 1º `###` dentro dele é `secao-2-1` (níveis abaixo seguem o mesmo
 *  padrão). Do texto, a âncora mudaria a cada tradução e levaria acento (`LEGAL-SLUG-ACENTO-01`).
 *  Pré-condição: a mesma sequência de `##`/`###` no `.pt.md` e em cada tradução — o `check_site.py`
 *  cobra (regra ii). O prefixo `secao-` mantém o `id` começando por letra (html-validate `valid-id`).
 *  Roda antes do plugin de ids do Astro, que mantém um `id` já posto. O `# título` já saiu do corpo
 *  (`omiteCabecalhoLegal`), por isso a contagem começa no `##`. */
export const idDosTitulosLegais = {
  name: 'ghf-id-dos-titulos-legais',
  element: {
    filter: ['h2', 'h3', 'h4', 'h5', 'h6'],
    visit(node, ctx) {
      if (!ehLegal(ctx)) return;
      const nivel = Number(node.tagName[1]) - 2; // h2 → 0, h3 → 1…
      const contagem = (ctx.data.ghfTitulos ??= []);
      contagem[nivel] = (contagem[nivel] ?? 0) + 1;
      contagem.length = nivel + 1; // um título novo zera os níveis abaixo dele
      const posicao = Array.from(contagem, (n) => n ?? 0).join('-');
      ctx.setProperty(node, 'id', `secao-${posicao}`);
    },
  },
};
