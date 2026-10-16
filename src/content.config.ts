// Content collections (WP-08, fatia 6). `legal`: texto legal, um `.md` por documento e idioma,
// `src/content/legal/<app>-<doc>.<idioma>.md`. O pt é cópia byte a byte do `.md` do repositório do
// app, com o front-matter acima do corpo; o en é a tradução (o agente não redige texto legal).
// O pt é escrito por tools/sync_legal.py (ADR-004).
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import dados from './i18n/idiomas.json';

// Códigos de língua do mapa (src/i18n/idiomas.json, ADR-007 §2): os valores aceitos em `pendente`.
const CODIGOS = Object.keys(dados.idiomas) as [string, ...string[]];

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
    // Commit do app de onde o corpo do `.pt.md` foi copiado (ADR-004), e as traduções que ficaram
    // atrás dele (`pendente: ["en", …]`, ADR-007 §8), gravados por tools/sync_legal.py. Opcionais
    // porque o schema vale para todas as línguas: "obrigatório no pt, proibido na tradução" e
    // `pendente` como erro são regras do check_site.py (§4, regra vii) — o build passa com o
    // marcador para o pt continuar visível no dist/ local.
    origemCommit: z.string().regex(/^[0-9a-f]{40}$/, 'origemCommit: sha de 40 hex minúsculos, entre aspas').optional(),
    pendente: z.array(z.enum(CODIGOS)).nonempty().optional(),
  }).strict(), // chave fora destas três falha o build
});

export const collections = { legal };
