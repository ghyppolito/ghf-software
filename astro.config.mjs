// Astro (ADR-002). Saída estática em dist/, publicada pelo .github/workflows/deploy.yml.
import { defineConfig, fontProviders } from 'astro/config';
import { satteri } from '@astrojs/markdown-satteri';
import {
  envolveTabelaLegal,
  idDosTitulosLegais,
  linksExternosLegais,
  linksInternosLegais,
  omiteCabecalhoLegal,
} from './src/markdown/legal.mjs';

// public/ (ADR-002 §3): o que vai ao ar sem passar pelo compilador do Astro, copiado byte a byte
// para dist/ — imagens (assets/), App Links (.well-known/), o convite do bolão (lotto-expert/,
// contrato byte a byte, D13) e o domínio (CNAME). Lista fechada, sem página: o Astro, se um arquivo
// de public/ colide com página gerada, publica o de public/ e só avisa ("Skipping…"), com o build
// verde. A guarda é o §13 do tools/check_site.py: primeiro nível de public/ fechado, nenhum .html
// além do convite e todo arquivo de public/ igual byte a byte ao de dist/ (WP-08, fatia 9).

// SEO (WP-11, ADR-005): sem @astrojs/sitemap. Com `build.format: 'preserve'` ele emite
// `/eclipsego` e `/en` (sem `.html`, sem barra), divergindo do canonical. sitemap.xml e robots.txt
// saem dos endpoints src/pages/sitemap.xml.ts e src/pages/robots.txt.ts, da mesma lista de rotas
// do canonical e do hreflang (src/i18n/ui.ts).

// Fonte (WP-12, ADR-006 §3): a Inter é servida pelo site, sem Google Fonts. Um woff2 variável,
// recortado do InterVariable.woff2 4.001 do handoff (design/handoff/2026-10-13-rodada-3/fonts/,
// OFL — src/assets/fonts/OFL.txt): eixo wght 400–800 (os pesos que o CSS compilado usa), opsz
// fixo em 14 (o padrão que o Google Fonts servia) e a faixa "latin" do Google Fonts + U+2192 (→).
// Recorte com fontTools 4.61, fora do CI:
//   fonttools varLib.instancer InterVariable.woff2 wght=400:800 opsz=14 -o inst.ttf
//   pyftsubset inst.ttf --flavor=woff2 --output-file=src/assets/fonts/inter-latin-wght.woff2 \
//     --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2192,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
// O <Font preload> do Base.astro emite o @font-face, o preload e o fallback com métricas
// ajustadas (`optimizedFallbacks`, padrão), que segura o CLS da troca de fonte.
const fontes = [
  {
    provider: fontProviders.local(),
    name: 'Inter',
    cssVariable: '--fonte-inter',
    fallbacks: ['sans-serif'],
    options: {
      variants: [
        {
          src: ['./src/assets/fonts/inter-latin-wght.woff2'],
          weight: '400 800',
          style: 'normal',
          display: 'swap',
        },
      ],
    },
  },
];

export default defineConfig({
  site: 'https://ghfsoftware.com',
  fonts: fontes,
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
  //   `id` dos títulos ganham o prefixo `secao-` (o slug começaria por dígito: `valid-id`); link
  //   externo abre em outra aba com `rel="noopener noreferrer"` (fatia 7); link para o próprio site
  //   (`https://ghfsoftware.com/x.html` no .md) vira `/x.html` — `/en/x.html` no .en.md —, na
  //   mesma aba (fatia 8).
  markdown: {
    processor: satteri({
      features: { smartPunctuation: false, gfm: true },
      mdastPlugins: [omiteCabecalhoLegal],
      hastPlugins: [envolveTabelaLegal, idDosTitulosLegais, linksInternosLegais, linksExternosLegais],
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
});
