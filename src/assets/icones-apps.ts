// Ícone de cada app (o mesmo PNG do favicon da aba), para o `<Image>` do astro:assets (ADR-006).
// A fonte única: Nav, 404, Home e "Todos os apps" (ListaApps.astro) leem daqui (WP-10, fatia 10a;
// ICONES-APPS-DUPLICADOS-01).
import type { ImageMetadata } from 'astro';
import type { ChaveApp } from '../i18n/apps';
import lottoexpert from './img/lottoexpert_favicon_v3.png';
import topowalk from './img/topo-walk.png';
import poleposition from './img/poleposition.png';
import eclipsego from './img/eclipse-go-favicon.png';

export const iconesApps: Record<ChaveApp, ImageMetadata> = { lottoexpert, topowalk, poleposition, eclipsego };
