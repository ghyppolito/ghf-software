// Astro (ADR-002). Saída estática em dist/, publicada pelo .github/workflows/deploy.yml.
import { cp } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';

// Até o WP-08, as páginas da raiz são a fonte: não passam pelo compilador do Astro (ADR-002 §3),
// são copiadas byte a byte para dist/. Lista fechada, sem glob — arquivo novo na raiz só é
// publicado se entrar aqui. Colisão com página gerada falha o build (errorOnExist).
const COPIADOS_DA_RAIZ = [
  'index.html',
  'lottoexpert.html',
  'lottoexpert-privacy.html',
  'lottoexpert-terms.html',
  'topowalk.html',
  'topowalk-privacy.html',
  'poleposition.html',
  'poleposition-privacy.html',
  'eclipsego.html',
  'eclipsego-privacy.html',
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
  integrations: [copiaRaiz()],
});
