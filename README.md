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

```
.
├── src/pages/                   # Páginas (Astro): landing corporativa, uma landing por app, as legais e a 404;
│                                #   en/ com os pares em inglês → dist/x.html, dist/en/x.html
├── src/content/legal/           # Políticas e termos, pt e en (espelho do repositório de cada app)
│   ├── lottoexpert-privacy.pt.md / .en.md     → /lottoexpert-privacy.html, /en/lottoexpert-privacy.html
│   ├── lottoexpert-terms.pt.md / .en.md       → /lottoexpert-terms.html, /en/lottoexpert-terms.html
│   ├── topowalk-privacy.pt.md / .en.md        → /topowalk-privacy.html, /en/topowalk-privacy.html
│   ├── poleposition-privacy.pt.md / .en.md    → /poleposition-privacy.html, /en/poleposition-privacy.html
│   └── eclipsego-privacy.pt.md / .en.md       → /eclipsego-privacy.html, /en/eclipsego-privacy.html
├── public/                      # Publicado byte a byte em dist/, sem passar pelo Astro (lista fechada)
│   ├── assets/                  # Imagens, logotipos, favicons e assets visuais das páginas
│   ├── .well-known/             # assetlinks.json (App Links do LottoExpert)
│   ├── lotto-expert/            # Convite do bolão (/lotto-expert/sweepstake-invite/lottoexpert-invite.html)
│   └── CNAME                    # Domínio do GitHub Pages
└── docs/                        # Especificações técnicas e documentação interna dos projetos
    ├── TOPOWALK_README.md
    ├── LOTTOEXPERT_README.md
    ├── POLEPOSITION_README.md
    └── ECLIPSE_GO_README.md
```

---

## 🛡️ Privacidade e Transparência

Todos os documentos legais exigidos pelas diretrizes da **Google Play Store**, **LGPD** (Lei Geral de Proteção de Dados - Lei nº 13.709/2018) e **GDPR** estão publicados e versionados neste repositório.

---

## 📬 Contato

- **Website:** [ghfsoftware.com](https://ghfsoftware.com)
- **Suporte / Contato:** [support@ghfsoftware.com](mailto:support@ghfsoftware.com)
