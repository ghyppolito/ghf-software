// Caso válido de src/i18n/apps.ts (tools/test_regras_apps.py): o formato que tools/regras_apps.py lê.
const PLAY = 'https://play.google.com/store/apps/details?id=';

export const apps = {
  // comentário com `campo: 'valor'` não conta: nome: 'Ignorado'
  alfa: {
    nome: 'Alfa', id: 'com.exemplo.alfa', categoria: 'UtilitiesApplication', play: `${PLAY}com.exemplo.alfa`,
    pagina: 'alfa.html', privacidade: 'alfa-privacy.html', termos: 'alfa-terms.html',
    icone: '/assets/alfa.png', tag: 'v1.2.0', atualizadoEm: '2026-10-01',
  },
  beta: {
    nome: 'Beta', id: 'com.exemplo.beta', categoria: 'SportsApplication', play: `${PLAY}com.exemplo.beta`,
    pagina: 'beta.html', privacidade: 'beta-privacy.html',
    icone: '/assets/beta.png', tag: 'v2.0.0', atualizadoEm: '2026-09-01',
  },
  gama: {
    nome: 'Gama', id: 'com.exemplo.gama', categoria: 'LifestyleApplication', play: `${PLAY}com.exemplo.gama`,
    pagina: 'gama.html', privacidade: 'gama-privacy.html',
    icone: '/assets/gama.png', tag: 'v0.9.1', atualizadoEm: '2026-02-30',
  },
  delta: {
    nome: 'Delta', id: 'com.exemplo.delta', categoria: 'UtilitiesApplication', play: `${PLAY}com.exemplo.delta`,
    pagina: 'delta.html', privacidade: 'delta-privacy.html',
    icone: '/assets/delta.png', tag: 'v3.1.4', atualizadoEm: '2026-07-26',
  },
  eps: {
    nome: 'Eps', id: 'com.exemplo.eps', categoria: 'UtilitiesApplication', play: `${PLAY}com.exemplo.eps`,
    pagina: 'eps.html', privacidade: 'eps-privacy.html',
    icone: '/assets/eps.png', tag: 'v1.0.0', atualizadoEm: '2026-06-01', indisponivel: true,
  },
} as const satisfies Record<string, App>;

export const ORDEM_APPS = ['alfa', 'beta', 'gama', 'delta', 'eps'] as const satisfies readonly ChaveApp[];
