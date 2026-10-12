---
id: WP-04
titulo: O convite de bolão compartilha com imagem e a página do Pole Position mostra uma só data
area: landing
status: todo
depende_de: []
adr: [ADR-001]
spec: ""
decisoes: []
tamanho: S
risco: baixo
visual: true
branch: feat/wp-04-og-do-convite-e-data-poleposition
---

# WP-04 — O convite de bolão compartilha com imagem e a página do Pole Position mostra uma só data

**Depende de:** — · **Achados roteados:** `INVITE-OG-IMAGE-01`, `POLEPOSITION-DATA-01`

**Objetivo:** `check_site.py` passa no estado atual do site: o convite tem `og:image` que
existe e `meta description`; `poleposition-privacy.html` tem a mesma data no HTML e no
dicionário i18n, igual ao `.md`.

**Contexto:** saída do `check_site.py` no setup (2026-10-12):
```
lotto-expert/sweepstake-invite/lottoexpert-invite.html: sem meta description
lotto-expert/sweepstake-invite/lottoexpert-invite.html: og:image aponta para /logo_transp.png, que não existe
lotto-expert/sweepstake-invite/lottoexpert-invite.html: referência a https://ghfsoftware.com/logo_transp.png (:12 e :246)
poleposition-privacy.html: data pt `junho de 2026` ≠ docs/POLEPOSITION_PRIVACY_POLICY.md `agosto de 2026`
```
O convite é o canal viral do app: sem imagem, a prévia no WhatsApp é só texto.

**Ler antes:** `lotto-expert/sweepstake-invite/lottoexpert-invite.html:1-30` e `:240-250`;
`poleposition-privacy.html:140-145` e `:243-247`.

**Arquivos-alvo:** `lotto-expert/sweepstake-invite/lottoexpert-invite.html`;
`poleposition-privacy.html`; opcionalmente `assets/lottoexpert_og.png` (1200×630) se o usuário
quiser imagem própria do convite — senão usar `assets/lottoexpert_app_mockup.png`, que já é a
`og:image` da landing.

**Passos:**
1. `og:image` do convite → `https://ghfsoftware.com/assets/lottoexpert_app_mockup.png` (ou a
   nova); `onerror` do `:246` → `../../assets/lottoexpert.png`. `meta description` em pt.
2. `poleposition-privacy.html:142` → "agosto de 2026".
3. `/verify`.

**Critérios de aceite:**
- `python3 tools/check_site.py` **sem erros** (avisos de `og:image` em página legal podem ficar).
- `grep -c logo_transp lotto-expert/sweepstake-invite/lottoexpert-invite.html` = 0.
- `grep -c "junho de 2026" poleposition-privacy.html` = 0.

**Só no navegador:** depois do WP-03 (no ar): colar um link de convite real no WhatsApp e ver
a prévia com imagem. Antes do ar não dá para provar — o WhatsApp lê a URL pública.

**Risco:** baixo. O caminho do convite não muda (ADR-001).
