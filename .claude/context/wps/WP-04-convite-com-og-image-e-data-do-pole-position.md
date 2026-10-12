---
id: WP-04
titulo: O convite de bolão compartilha com imagem e a política do Pole Position no site é a do app
area: legal
status: todo
depende_de: []
adr: [ADR-001]
spec: ""
decisoes: [D7]
tamanho: S
risco: alto
visual: true
branch: feat/wp-04-og-do-convite-e-data-poleposition
---

# WP-04 — O convite de bolão compartilha com imagem e a política do Pole Position no site é a do app

**Depende de:** — · **Achados roteados:** `INVITE-OG-IMAGE-01`, `POLEPOSITION-DATA-01`, `POLEPOSITION-ATRAS-01`

**Ampliado em 2026-10-12 (decisão do usuário):** além da data divergente, o WP espelha a política do
Pole Position do repositório do app (`/legal poleposition`). Por isso `area: legal` e `risco: alto`;
a parte do convite segue sendo do `site-dev`, a da política é do `site-legal`.

**Objetivo:** `check_site.py` passa no estado atual do site: o convite tem `og:image` que
existe e `meta description`; `poleposition-privacy.html` tem a mesma data no HTML e no
dicionário i18n, igual ao `.md`; e o `.md` e o HTML (pt e en) do Pole Position dizem o que
`../pole-position/pole-position-app/PRIVACY_POLICY.md` diz (setembro de 2026, com `POST_NOTIFICATIONS`).

**Contexto:** saída do `check_site.py` no setup (2026-10-12):
```
lotto-expert/sweepstake-invite/lottoexpert-invite.html: sem meta description
lotto-expert/sweepstake-invite/lottoexpert-invite.html: og:image aponta para /logo_transp.png, que não existe
lotto-expert/sweepstake-invite/lottoexpert-invite.html: referência a https://ghfsoftware.com/logo_transp.png (:12 e :246)
poleposition-privacy.html: data pt `junho de 2026` ≠ docs/POLEPOSITION_PRIVACY_POLICY.md `agosto de 2026`
```
O convite é o canal viral do app: sem imagem, a prévia no WhatsApp é só texto.

E a política do Pole Position está atrás do app (`diff ../pole-position/pole-position-app/PRIVACY_POLICY.md docs/POLEPOSITION_PRIVACY_POLICY.md`,
2026-10-12): data "setembro de 2026" na origem vs "agosto de 2026" no site, e a linha da permissão
`POST_NOTIFICATIONS` (origem `:140`, tabela da §3 "Uso das Permissões") ausente no site. Texto
legal desatualizado no ar.

**Ler antes:** `lotto-expert/sweepstake-invite/lottoexpert-invite.html:1-30` e `:240-250`;
`poleposition-privacy.html:140-145` e `:243-247`; o diff acima (só as linhas que mudaram);
`.claude/agents/site-legal.md`.

**Arquivos-alvo:** `lotto-expert/sweepstake-invite/lottoexpert-invite.html`;
`poleposition-privacy.html` (data e §3 em pt e en); `docs/POLEPOSITION_PRIVACY_POLICY.md` (cópia
idêntica da origem); opcionalmente `assets/lottoexpert_og.png` (1200×630) se o usuário
quiser imagem própria do convite — senão usar `assets/lottoexpert_app_mockup.png`, que já é a
`og:image` da landing.

**Passos:**
1. `og:image` do convite → `https://ghfsoftware.com/assets/lottoexpert_app_mockup.png` (ou a
   nova); `onerror` do `:246` → `../../assets/lottoexpert.png`. `meta description` em pt.
2. `site-legal`: `cp ../pole-position/pole-position-app/PRIVACY_POLICY.md docs/POLEPOSITION_PRIVACY_POLICY.md`;
   em `poleposition-privacy.html`, a linha `POST_NOTIFICATIONS` na tabela da §3 (pt e tradução en)
   e a data "setembro de 2026" / "September 2026" em todo lugar (HTML estático e dicionário i18n).
3. `/verify`.

**Critérios de aceite:**
- `python3 tools/check_site.py` **sem erros** (avisos de `og:image` em página legal podem ficar).
- `grep -c logo_transp lotto-expert/sweepstake-invite/lottoexpert-invite.html` = 0.
- `grep -c "junho de 2026\|agosto de 2026" poleposition-privacy.html` = 0;
  `grep -c "setembro de 2026" poleposition-privacy.html` ≥ 2; `grep -c "September 2026" poleposition-privacy.html` ≥ 1.
- `diff -q ../pole-position/pole-position-app/PRIVACY_POLICY.md docs/POLEPOSITION_PRIVACY_POLICY.md` sem saída.
- `grep -c "POST_NOTIFICATIONS" poleposition-privacy.html` ≥ 2 (pt e en).

**Só no navegador:** depois do WP-03 (no ar): colar um link de convite real no WhatsApp e ver
a prévia com imagem. Antes do ar não dá para provar — o WhatsApp lê a URL pública.
Antes do ar: `poleposition-privacy.html` em pt e en, 360 e 1280 px — data no topo e a linha
`POST_NOTIFICATIONS` na tabela de permissões.

**Risco:** alto por ser texto legal (espelho, não redação — D7); baixo tecnicamente. Os caminhos
do convite e da política não mudam (ADR-001).
