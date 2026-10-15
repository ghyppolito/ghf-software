// Astro (ADR-002). Saída estática em dist/, publicada pelo .github/workflows/deploy.yml.
import { cp } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';

// Página ainda não migrada (WP-08) tem a raiz como fonte: não passa pelo compilador do Astro
// (ADR-002 §3), é copiada byte a byte para dist/. Lista fechada, sem glob — arquivo novo na raiz
// só é publicado se entrar aqui. Colisão com página gerada falha o build (errorOnExist).
// Página migrada sai daqui e da raiz no mesmo commit (index.html: fatia 1; lottoexpert.html: fatia 2;
// topowalk.html: fatia 3; poleposition.html: fatia 4; eclipsego.html: fatia 5).
const COPIADOS_DA_RAIZ = [
  'lottoexpert-privacy.html',
  'lottoexpert-terms.html',
  'topowalk-privacy.html',
  'poleposition-privacy.html',
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
