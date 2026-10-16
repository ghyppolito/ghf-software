// Textos das páginas legais em volta do corpo (hero, botão de voltar, <title>, description), pt e
// en. O corpo é o `.md` de src/content/legal/. Toda chave nova entra nos dois idiomas no mesmo commit.
// O rótulo da data e os meses são da língua, e vêm de src/i18n/idiomas.json (ADR-007 §2).
import { IDIOMAS, type Idioma } from './idiomas';

export const legal = {
  pt: {
    // Selo do hero. Não tinha `data-i18n` na página antiga (o modo en mostrava o pt); traduzido no WP-22.
    selo: 'Documento Legal',
    voltar_app: 'Voltar para a Página do App',
    voltar_home: 'Voltar para a GHF Software',
    eclipsego_privacy_h1: 'Política de Privacidade — EclipseGo',
    eclipsego_privacy_title: 'Política de Privacidade — EclipseGo — GHF Software',
    eclipsego_privacy_description: 'Política de Privacidade do aplicativo EclipseGo desenvolvido pela GHF Software.',
    topowalk_privacy_h1: 'Política de Privacidade — TopoWalk',
    topowalk_privacy_title: 'Política de Privacidade — TopoWalk — GHF Software',
    topowalk_privacy_description: 'Política de Privacidade do aplicativo TopoWalk desenvolvido pela GHF Software.',
    // O `#` do .md diz "Pole Position: Race Analytics"; o h1 exibido segue o publicado (D-c).
    poleposition_privacy_h1: 'Política de Privacidade — Pole Position',
    poleposition_privacy_title: 'Política de Privacidade — Pole Position — GHF Software',
    poleposition_privacy_description: 'Política de Privacidade do aplicativo Pole Position: Race Analytics desenvolvido pela GHF Software.',
    lottoexpert_privacy_h1: 'Política de Privacidade — LottoExpert',
    lottoexpert_privacy_title: 'Política de Privacidade — LottoExpert — GHF Software',
    lottoexpert_privacy_description: 'Política de Privacidade do aplicativo LottoExpert desenvolvido pela GHF Software.',
    lottoexpert_terms_h1: 'Termos de Uso — LottoExpert',
    lottoexpert_terms_title: 'Termos de Uso — LottoExpert — GHF Software',
    lottoexpert_terms_description: 'Termos de Uso do aplicativo LottoExpert desenvolvido pela GHF Software.',
  },
  en: {
    selo: 'Legal Document',
    voltar_app: 'Back to App Page',
    voltar_home: 'Back to GHF Software',
    eclipsego_privacy_h1: 'Privacy Policy — EclipseGo',
    eclipsego_privacy_title: 'Privacy Policy — EclipseGo — GHF Software',
    eclipsego_privacy_description: 'Privacy Policy of the EclipseGo app developed by GHF Software.',
    topowalk_privacy_h1: 'Privacy Policy — TopoWalk',
    topowalk_privacy_title: 'Privacy Policy — TopoWalk — GHF Software',
    topowalk_privacy_description: 'Privacy Policy of the TopoWalk app developed by GHF Software.',
    poleposition_privacy_h1: 'Privacy Policy — Pole Position',
    poleposition_privacy_title: 'Privacy Policy — Pole Position — GHF Software',
    poleposition_privacy_description: 'Privacy Policy of the Pole Position: Race Analytics app developed by GHF Software.',
    lottoexpert_privacy_h1: 'Privacy Policy — LottoExpert',
    lottoexpert_privacy_title: 'Privacy Policy — LottoExpert — GHF Software',
    lottoexpert_privacy_description: 'Privacy Policy of the LottoExpert app developed by GHF Software.',
    lottoexpert_terms_h1: 'Terms of Use — LottoExpert',
    lottoexpert_terms_title: 'Terms of Use — LottoExpert — GHF Software',
    lottoexpert_terms_description: 'Terms of Use of the LottoExpert app developed by GHF Software.',
  },
} as const satisfies Record<Idioma, Record<string, string>>;

/** Rótulo da data legal na língua (`Última atualização:`, `Last updated:`). */
export function rotuloData(lang: Idioma): string {
  return IDIOMAS[lang].rotuloData;
}

// `lastUpdated` do front-matter (`AAAA-MM` ou `AAAA-MM-DD`) por extenso, no formato da linha
// `**Última atualização:**` / `**Last updated:**` do corpo: "13 de julho de 2026" / "July 13, 2026",
// "setembro de 2026" / "September 2026". Sem `Date`: nada de fuso, nada de dia anterior.
export function dataLegal(lang: Idioma, lastUpdated: string): string {
  const [ano, mes, dia] = lastUpdated.split('-');
  const nomeMes = IDIOMAS[lang].meses[Number(mes) - 1];
  if (!nomeMes) throw new Error(`lastUpdated com mês inválido: ${lastUpdated}`);
  if (lang === 'pt') return dia ? `${Number(dia)} de ${nomeMes} de ${ano}` : `${nomeMes} de ${ano}`;
  return dia ? `${nomeMes} ${Number(dia)}, ${ano}` : `${nomeMes} ${ano}`;
}
