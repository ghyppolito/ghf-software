// Astro (ADR-002). Saída estática em dist/, publicada pelo .github/workflows/deploy.yml.
import { cp } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import { satteri } from '@astrojs/markdown-satteri';
import { envolveTabelaLegal, idDosTitulosLegais, omiteCabecalhoLegal } from './src/markdown/legal.mjs';

// Página ainda não migrada (WP-08) tem a raiz como fonte: não passa pelo compilador do Astro
// (ADR-002 §3), é copiada byte a byte para dist/. Lista fechada, sem glob — arquivo novo na raiz
// só é publicado se entrar aqui. Colisão com página gerada falha o build (errorOnExist).
// Página migrada sai daqui e da raiz no mesmo commit (index.html: fatia 1; lottoexpert.html: fatia 2;
// topowalk.html: fatia 3; poleposition.html: fatia 4; eclipsego.html: fatia 5; eclipsego-privacy.html:
// fatia 6).
const COPIADOS_DA_RAIZ = [
  'lottoexpert-privacy.html',
  'lottoexpert-terms.html',
  'topowalk-privacy.html',
  'poleposition-privacy.html',
  'assets',
  '.well-known',
  'lotto-expert',
  'CNAME',
];

const raizDoRepositorio = new URL('./', import.meta.url);

function copiaRaiz() {
  return {
    name: 'ghf:copia-raiz',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        for (const item of COPIADOS_DA_RAIZ) {
          await cp(
            fileURLToPath(new URL(item, raizDoRepositorio)),
            fileURLToPath(new URL(item, dir)),
            { recursive: true, errorOnExist: true, force: false },
          );
        }
        logger.info(`${COPIADOS_DA_RAIZ.length} itens copiados da raiz para dist/`);
      },
    },
  };
}

export default defineConfig({
  site: 'https://ghfsoftware.com',
  // 'preserve': x.astro → x.html e en/index.astro → en/index.html (ADR-002 §2).
  build: { format: 'preserve' },
  // Markdown (texto legal, src/content/legal/). Sätteri é o processador padrão do Astro 7; ele é
  // declarado aqui só para receber opções — `markdown.smartypants`/`gfm` estão obsoletos no Astro 7
  // e passam a ser `features` do processador.
  // - smartPunctuation: false — o texto legal sai com as aspas, travessões e reticências do .md do
  //   app, sem trocar `"` por “ ” (WP-08, fatia 6).
  // - gfm: ligado (padrão) — as políticas têm tabelas. Efeito colateral aceito: o GFM transforma o
  //   e-mail do texto (`support@ghfsoftware.com`) em link `mailto:`; a página antiga mostrava o
  //   mesmo texto sem link. O texto não muda, e o link é o que o leitor faria à mão.
  // - plugins (src/markdown/legal.mjs): o `# título` e a linha `**Última atualização:**` do corpo
  //   não são renderizados (o hero mostra os dois); a tabela ganha o contêiner com rolagem; os
  //   `id` dos títulos ganham o prefixo `secao-` (o slug começaria por dígito: `valid-id`).
  markdown: {
    processor: satteri({
      features: { smartPunctuation: false, gfm: true },
      mdastPlugins: [omiteCabecalhoLegal],
      hastPlugins: [envolveTabelaLegal, idDosTitulosLegais],
    }),
  },
  vite: {
    build: {
      // Alvo explícito do minificador de CSS (lightningcss, ADR-003 §4). Sem ele, a regra com
      // `-webkit-backdrop-filter` e `backdrop-filter` saía com um só dos dois (o vidro do nav e
      // dos cards perdia o blur no Chrome ou no Safari < 18); com alvo, saem os dois, como no
      // <style> das páginas antigas. Navegadores do antigo padrão `modules` do Vite.
      cssTarget: ['chrome87', 'edge88', 'firefox78', 'safari14'],
    },
  },
  integrations: [copiaRaiz()],
});
