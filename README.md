# GHF Software — Website & Documentação Oficial

Repositório central do site oficial da **GHF Software** ([ghfsoftware.com](https://ghfsoftware.com)) e portal de transparência, políticas de privacidade, termos de uso e documentação técnica dos aplicativos desenvolvidos.

---

## 🚀 Sobre a GHF Software

A **GHF Software** desenvolve aplicações mobile nativas para Android e soluções de engenharia de software com foco em alta performance, processamento *offline-first*, precisão de sensores e privacidade dos dados do usuário.

---

## 📱 Aplicativos no Portfólio

| Aplicativo | Descrição | Documentação Técnica | Política de Privacidade / Termos |
|---|---|---|---|
| **TopoWalk** | Levantamento topográfico de campo com receptores GNSS/RTK Bluetooth, altimetria barométrica, cálculos de declividade (%), áreas de polígonos, laudos PDF e exportações SIG (GeoJSON, KML, GPX). | [TOPOWALK_README.md](docs/TOPOWALK_README.md) | [Política de Privacidade](https://ghfsoftware.com/topowalk-privacy.html) / [Markdown](src/content/legal/topowalk-privacy.pt.md) |
| **LottoExpert** | Engenharia estatística combinatória para loterias, conferência automática de bilhetes via OCR local, bolões, dashboard financeiro e sincronização resiliente via GCP. | [LOTTOEXPERT_README.md](docs/LOTTOEXPERT_README.md) | [Política de Privacidade](https://ghfsoftware.com/lottoexpert-privacy.html) / [Markdown](src/content/legal/lottoexpert-privacy.pt.md) — [Termos de Uso](https://ghfsoftware.com/lottoexpert-terms.html) / [Markdown](src/content/legal/lottoexpert-terms.pt.md) |
| **Pole Position: Race Analytics** | Telemetria esportiva para automobilismo amador e karting. Medição de força G lateral/longitudinal via acelerômetro/giroscópio, cronometragem por GPS e análise de melhor volta. | [POLEPOSITION_README.md](docs/POLEPOSITION_README.md) | [Política de Privacidade](https://ghfsoftware.com/poleposition-privacy.html) / [Markdown](src/content/legal/poleposition-privacy.pt.md) |
| **EclipseGo** | Calculadora astronômica 100% offline para visualização e horários de eclipses solares e lunares com base na posição geográfica do usuário. | [ECLIPSE_GO_README.md](docs/ECLIPSE_GO_README.md) | [Política de Privacidade](https://ghfsoftware.com/eclipsego-privacy.html) / [Markdown](src/content/legal/eclipsego-privacy.pt.md) |

---

## 🌐 Estrutura do Repositório

O site é gerado pelo [Astro](https://astro.build) a partir de `src/` e publicado a partir de `dist/`.
Detalhe de cada parte em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

```
.
├── src/
│   ├── pages/                 # Rotas: pt na raiz (index.astro, lottoexpert.astro, …, 404.astro),
│   │   │                      #   robots.txt.ts e sitemap.xml.ts
│   │   └── [lang]/            # As outras línguas de cada página (hoje en) → dist/en/x.html
│   ├── layouts/               # Base.astro (<head> único) e LegalLayout.astro (páginas legais)
│   ├── components/            # Nav, Footer, seletor e sugestão de idioma, corpo de cada landing;
│   │   └── paginas/           #   a página inteira, com a prop `lang`
│   ├── i18n/                  # idiomas.json (línguas do site e de cada página) e os dicionários
│   ├── content/legal/         # Políticas e termos por língua (o pt é cópia do repositório do app)
│   ├── markdown/legal.mjs     # Plugins do texto legal
│   ├── assets/                # Imagens exibidas (otimizadas pelo build) e a fonte Inter
│   ├── icons/fa/              # Ícones SVG inline
│   └── styles/global.css      # Temas e tipografia do texto legal
├── public/                    # Copiado byte a byte para dist/ (lista fechada)
│   ├── assets/                # Arquivos de URL fixa: og:image, imagens do convite
│   ├── .well-known/           # assetlinks.json (App Links do LottoExpert)
│   ├── lotto-expert/          # Convite do bolão (/lotto-expert/sweepstake-invite/lottoexpert-invite.html)
│   └── CNAME                  # Domínio do GitHub Pages
├── tools/                     # Verificações em Python (check_site.py, check_plano.py, sync_legal.py, …)
├── docs/                      # ARQUITETURA.md, AVALIACAO.md e o README técnico de cada app
├── design/                    # Brief e handoff do sistema visual
├── astro.config.mjs           # Configuração do Astro
└── tailwind.config.mjs        # Tokens de cor e fonte da marca
```

Cada arquivo de `src/content/legal/` vira uma URL: `src/content/legal/lottoexpert-privacy.pt.md` →
`/lottoexpert-privacy.html`, `src/content/legal/lottoexpert-privacy.en.md` → `/en/lottoexpert-privacy.html`.

---

## 🛠️ Como rodar

Precisa de Node 22.22 e Python 3.

```bash
npm ci && npm run build                # gera dist/
python3 -m http.server 8080 -d dist    # abre em http://localhost:8080
python3 tools/check_site.py            # verifica dist/: URLs contratuais, links, metadados, datas legais, copy
python3 tools/check_plano.py           # verifica o backlog
```

Os demais checks do CI (contrato byte a byte, regras de i18n, html-validate, lychee, Lighthouse)
estão na seção "Comandos" do [`CLAUDE.md`](CLAUDE.md).

---

## 🚢 Como publicar

1. O trabalho nasce numa branch `feat/…` a partir de `develop` e vai por PR para `develop`. O
   workflow `.github/workflows/pr.yml` roda os checks `plano`, `site` e `lighthouse`.
2. **`develop → master` é deploy.** Só o mantenedor faz esse merge, pelo ritual `/release`
   (`.claude/commands/release.md`), depois de conferir no navegador o que só ele prova.
3. O push em `master` dispara `.github/workflows/deploy.yml`, que builda, verifica e publica `dist/`
   no GitHub Pages (modo "GitHub Actions").

---

## 🛡️ Privacidade e Transparência

Todos os documentos legais exigidos pelas diretrizes da **Google Play Store**, **LGPD** (Lei Geral de Proteção de Dados - Lei nº 13.709/2018) e **GDPR** estão publicados neste site. O texto nasce e é versionado no repositório de cada app; aqui fica a cópia publicada (`src/content/legal/`).

---

## 📬 Contato

- **Website:** [ghfsoftware.com](https://ghfsoftware.com)
- **Suporte / Contato:** [support@ghfsoftware.com](mailto:support@ghfsoftware.com)
