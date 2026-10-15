// Content collections (WP-08, fatia 6). `legal`: texto legal, um `.md` por documento e idioma,
// `src/content/legal/<app>-<doc>.<idioma>.md`. O pt é cópia byte a byte do `.md` do repositório do
// app, com o front-matter acima do corpo; o en é a tradução (o agente não redige texto legal).
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const legal = defineCollection({
  loader: glob({
    pattern: '*.md',
    base: './src/content/legal',
    // id = nome do arquivo sem `.md` (`eclipsego-privacy.pt`); o padrão do glob tiraria o ponto.
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    // String entre aspas, `AAAA-MM` ou `AAAA-MM-DD`: algumas políticas só têm mês (TopoWalk, Pole
    // Position), e uma data YAML viraria `Date` UTC — em -03 mostraria o dia anterior. Formatada por
    // `dataLegal()` (src/i18n/legal.ts), sem `Date`.
    lastUpdated: z.string().regex(/^\d{4}-\d{2}(-\d{2})?$/, 'lastUpdated: "AAAA-MM" ou "AAAA-MM-DD", entre aspas'),
  }),
});

export const collections = { legal };
