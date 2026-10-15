// Textos das páginas legais em volta do corpo (hero, botão de voltar, <title>, description), pt e
// en. O corpo é o `.md` de src/content/legal/. Toda chave nova entra nos dois idiomas no mesmo commit.
import type { Idioma } from './ui';

export const legal = {
  pt: {
    // Selo do hero. Não tinha `data-i18n` na página antiga: o modo en mostrava o pt (transportado).
    selo: 'Documento Legal',
    rotulo_data: 'Última atualização:',
    voltar_app: 'Voltar para a Página do App',
    voltar_home: 'Voltar para a GHF Software',
    eclipsego_privacy_h1: 'Política de Privacidade — EclipseGo',
    eclipsego_privacy_title: 'Política de Privacidade EclipseGo - GHF Software',
    eclipsego_privacy_description: 'Política de Privacidade do aplicativo EclipseGo desenvolvido pela GHF Software.',
    topowalk_privacy_h1: 'Política de Privacidade — TopoWalk',
    topowalk_privacy_title: 'Política de Privacidade TopoWalk - GHF Software',
    topowalk_privacy_description: 'Política de Privacidade do aplicativo TopoWalk desenvolvido pela GHF Software.',
    // O `#` do .md diz "Pole Position: Race Analytics"; o h1 exibido segue o publicado (D-c).
    poleposition_privacy_h1: 'Política de Privacidade — Pole Position',
    poleposition_privacy_title: 'Política de Privacidade Pole Position - GHF Software',
    poleposition_privacy_description: 'Política de Privacidade do aplicativo Pole Position: Race Analytics desenvolvido pela GHF Software.',
  },
  en: {
    selo: 'Documento Legal',
    rotulo_data: 'Last updated:',
    voltar_app: 'Back to App Page',
    voltar_home: 'Back to GHF Software',
    eclipsego_privacy_h1: 'Privacy Policy — EclipseGo',
    eclipsego_privacy_title: 'EclipseGo Privacy Policy - GHF Software',
    eclipsego_privacy_description: 'Privacy Policy of the EclipseGo app developed by GHF Software.',
    topowalk_privacy_h1: 'Privacy Policy — TopoWalk',
    topowalk_privacy_title: 'TopoWalk Privacy Policy - GHF Software',
    topowalk_privacy_description: 'Privacy Policy of the TopoWalk app developed by GHF Software.',
    poleposition_privacy_h1: 'Privacy Policy — Pole Position',
    poleposition_privacy_title: 'Pole Position Privacy Policy - GHF Software',
    poleposition_privacy_description: 'Privacy Policy of the Pole Position: Race Analytics app developed by GHF Software.',
  },
} as const satisfies Record<Idioma, Record<string, string>>;

const MESES = {
  pt: ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
};

// `lastUpdated` do front-matter (`AAAA-MM` ou `AAAA-MM-DD`) por extenso, no formato da linha
// `**Última atualização:**` / `**Last updated:**` do corpo: "13 de julho de 2026" / "July 13, 2026",
// "setembro de 2026" / "September 2026". Sem `Date`: nada de fuso, nada de dia anterior.
export function dataLegal(lang: Idioma, lastUpdated: string): string {
  const [ano, mes, dia] = lastUpdated.split('-');
  const nomeMes = MESES[lang][Number(mes) - 1];
  if (!nomeMes) throw new Error(`lastUpdated com mês inválido: ${lastUpdated}`);
  if (lang === 'pt') return dia ? `${Number(dia)} de ${nomeMes} de ${ano}` : `${nomeMes} de ${ano}`;
  return dia ? `${nomeMes} ${Number(dia)}, ${ano}` : `${nomeMes} ${ano}`;
}
