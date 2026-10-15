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

/** hast: `id` dos títulos com prefixo `secao-`. O slug do Astro começaria por dígito
 *  (`1-resumo`), e o html-validate (`valid-id`) exige letra; o `id` serve de âncora (`#secao-1-resumo`).
 *  Roda antes do plugin de ids do Astro, que mantém um `id` já posto. */
export const idDosTitulosLegais = {
  name: 'ghf-id-dos-titulos-legais',
  element: {
    filter: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    visit(node, ctx) {
      if (!ehLegal(ctx)) return;
      // mesmo slug do github-slugger (o do Astro): minúsculas, só letras, números, espaço e hífen
      const slug = ctx
        .textContent(node)
        .toLowerCase()
        .trim()
        .replace(/[^\p{L}\p{N}\s-]/gu, '')
        .replace(/\s/g, '-');
      const usados = (ctx.data.ghfIds ??= new Map());
      const n = usados.get(slug) ?? 0;
      usados.set(slug, n + 1);
      ctx.setProperty(node, 'id', `secao-${slug}${n ? `-${n}` : ''}`);
    },
  },
};
