// PostCSS do Vite do Astro compila o Tailwind 3 (ADR-003). Sem integração do Astro.
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
