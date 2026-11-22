// Ícone de cada app (o favicon que o Nav e a 404 já usam), para o `<Image>` do astro:assets
// (ADR-006). Por ora só a Home lê daqui (WP-10, fatia 6); Nav e 404 importam os mesmos arquivos e
// migram na fatia 10a (ICONES-APPS-DUPLICADOS-01, junto de APPS-LISTA-DUPLICADA-01).
import type { ImageMetadata } from 'astro';
import type { ChaveApp } from '../i18n/apps';
import lottoexpert from './img/lottoexpert_favicon_v3.png';
import topowalk from './img/topo-walk.png';
import poleposition from './img/poleposition.png';
import eclipsego from './img/eclipse-go-favicon.png';

export const iconesApps: Record<ChaveApp, ImageMetadata> = { lottoexpert, topowalk, poleposition, eclipsego };
