// Tailwind 3.4.19 compilado no build (ADR-003). Uma configuração para o site inteiro: é a união
// das configs inline das 10 páginas (WP-08). O que variava por página (cores brand.*, a escala
// amber do TopoWalk, as sombras glow e a fonte mono) é variável CSS, com valor por tema em
// src/styles/global.css (`<html data-tema="…">`).
//
// Classe montada por concatenação de string não é detectada (a Play CDN detectava, porque
// observava o DOM): é proibida. O que não puder ser literal vai para `safelist`, com o porquê.

// rgb(var(--x) / <alpha-value>) mantém os modificadores de opacidade (`bg-brand-primary/20`).
const cor = (variavel) => `rgb(var(${variavel}) / <alpha-value>)`;

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,md,mdx,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        // Só poleposition.html declarava `mono` (JetBrains Mono); nas outras vale a pilha padrão.
        mono: 'var(--fonte-mono)',
      },
      colors: {
        brand: {
          base: cor('--brand-base'),
          surface: cor('--brand-surface'),
          primary: cor('--brand-primary'),
          primaryHover: cor('--brand-primary-hover'),
          secondary: cor('--brand-secondary'),
          accent: cor('--brand-accent'),
        },
        // topowalk.html sobrescrevia 400/500/600/900 (terracota); os demais tons são os padrão.
        amber: {
          400: cor('--amber-400'),
          500: cor('--amber-500'),
          600: cor('--amber-600'),
          900: cor('--amber-900'),
        },
      },
      boxShadow: {
        glow: 'var(--sombra-glow)',
        'glow-blue': 'var(--sombra-glow-blue)',
        'glow-indigo': '0 0 25px rgba(99, 102, 241, 0.35)',
        'glow-accent': '0 0 20px rgba(132, 204, 22, 0.4)',
        'glow-amber': '0 0 20px rgba(181, 84, 28, 0.4)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'tech-grid':
          'linear-gradient(to right, #1f2937 1px, transparent 1px), linear-gradient(to bottom, #1f2937 1px, transparent 1px)',
      },
    },
  },
  plugins: [],
};
