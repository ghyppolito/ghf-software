#!/usr/bin/env python3
"""Rede de segurança do site — roda no /verify e, a partir do WP-05, no CI do PR.

Só biblioteca padrão, de propósito: funciona hoje (sem build) e depois do WP-07
(apontando para `dist/` com `--raiz dist`). Falha com código 1 se encontrar erro.

Checa:
  1. URLs contratuais (ADR-001) existem
  2. cada página tem <html lang>, <title>, meta description e og:image
  3. href/src locais resolvem para arquivo existente; og:image em ghfsoftware.com resolve localmente
  4. "Última atualização" da página legal (pt e en) bate com a do .md em docs/ — lido sempre
     da raiz do repositório, também com `--raiz dist`; .md ausente é erro
  5. copy do LottoExpert respeita jogo responsável (mesma régua do PaywallCopyComplianceTest do app)
  6. .well-known/assetlinks.json é JSON válido com o package do LottoExpert
"""
import glob
import json
import os
import re
import sys

raiz = "."
if "--raiz" in sys.argv:
    raiz = sys.argv[sys.argv.index("--raiz") + 1]

# Raiz do repositório = pasta acima de tools/, independente do cwd. As fontes legais (docs/*.md)
# são lidas daqui mesmo com `--raiz dist`: docs/ não é publicado, e a data legal tem de ser
# conferida contra a fonte, não contra o que foi para o ar (ADR-002 §7).
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTRATUAIS = [
    ".well-known/assetlinks.json",
    "lottoexpert-privacy.html", "lottoexpert-terms.html",
    "topowalk-privacy.html", "poleposition-privacy.html", "eclipsego-privacy.html",
    "lotto-expert/sweepstake-invite/lottoexpert-invite.html",
]

# página legal → markdown de origem no site. A origem da origem é o repositório do app.
LEGAL = {
    "lottoexpert-privacy.html": "docs/LOTTOEXPERT_PRIVACY_POLICY.md",
    "lottoexpert-terms.html": "docs/LOTTOEXPERT_TERMS_OF_SERVICE.md",
    "topowalk-privacy.html": "docs/TOPOWALK_PRIVACY_POLICY.md",
    "poleposition-privacy.html": "docs/POLEPOSITION_PRIVACY_POLICY.md",
    "eclipsego-privacy.html": "docs/ECLIPSE_GO_PRIVACY_POLICY.md",
}

MESES_PT = {"janeiro": "January", "fevereiro": "February", "março": "March", "abril": "April",
         "maio": "May", "junho": "June", "julho": "July", "agosto": "August",
         "setembro": "September", "outubro": "October", "novembro": "November", "dezembro": "December"}
MESES = dict(MESES_PT, **{v.lower(): v for v in MESES_PT.values()})

# Jogo responsável: o app garante matemática provada, não chance. Termos novos entram aqui,
# nunca saem — a lista só cresce (como a do app).
COPY_PROIBIDA = [
    r"aumenta\w*\s+(a\s+|as\s+|sua\s+|suas\s+)?chance",
    r"maximiz",
    r"garant\w+\s+(de\s+|o\s+|seu\s+)?pr[êe]mio",
    r"increase\w*\s+(your\s+)?(odds|chances)",
    r"guarantee\w*\s+(a\s+|your\s+)?(prize|win)",
]
PAGINAS_LOTTO = ["index.html", "lottoexpert.html", "lottoexpert-privacy.html", "lottoexpert-terms.html",
                 "lotto-expert/sweepstake-invite/lottoexpert-invite.html"]

erros, avisos = [], []


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def p(rel):
    return os.path.join(raiz, rel)


# ------------------------------------------------------------ 1: contratuais
for rel in CONTRATUAIS:
    if not os.path.exists(p(rel)):
        erros.append(f"URL contratual ausente (ADR-001): /{rel}")

# ------------------------------------------------------------ 2 e 3: páginas
paginas = sorted(glob.glob(p("*.html")) + glob.glob(p("lotto-expert/**/*.html"), recursive=True)
                 + glob.glob(p("en/**/*.html"), recursive=True))
n_links = 0
for caminho in paginas:
    html = ler(caminho)
    rel = os.path.relpath(caminho, raiz)
    base = os.path.dirname(caminho)
    if not re.search(r"<html[^>]*\blang=", html):
        erros.append(f"{rel}: <html> sem lang")
    if not re.search(r"<title>[^<]+</title>", html):
        erros.append(f"{rel}: sem <title>")
    if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', html) and \
       not re.search(r'<meta\s+content="[^"]+"\s+name="description"', html):
        erros.append(f"{rel}: sem meta description")
    m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    if not m:
        avisos.append(f"{rel}: sem og:image (landing deve ter; página legal pode não ter)")
    else:
        og = m.group(1)
        if og.startswith("https://ghfsoftware.com/"):
            alvo = og[len("https://ghfsoftware.com/"):]
            if not os.path.exists(p(alvo)):
                erros.append(f"{rel}: og:image aponta para /{alvo}, que não existe no repositório")
    for attr, alvo in re.findall(r'\b(href|src)="([^"#?]+)[^"]*"', html):
        if re.match(r"^(https?:|mailto:|tel:|javascript:|data:|//)", alvo) or alvo in ("", "/"):
            continue
        n_links += 1
        destino = os.path.join(raiz, alvo.lstrip("/")) if alvo.startswith("/") else os.path.join(base, alvo)
        if not os.path.exists(os.path.normpath(destino)):
            erros.append(f"{rel}: {attr}=\"{alvo}\" não resolve")
    # og:image em onerror e afins (o convite usa fallback por JS)
    for alvo in re.findall(r"https://ghfsoftware\.com/([A-Za-z0-9_./-]+\.(?:png|jpg|webp|svg))", html):
        if not os.path.exists(p(alvo)):
            erros.append(f"{rel}: referência a https://ghfsoftware.com/{alvo}, que não existe")

# ------------------------------------------------------------ 4: datas legais
# Aceita "12 de Outubro de 2026" e "setembro de 2026" (sem dia). A comparação é
# por (dia, mês, ano) normalizados; dia ausente é "".
RE_PT = r"(?:(\d{1,2}) de )?(\w+) de (\d{4})"
RE_EN = r"(\w+)(?: (\d{1,2}),)? (\d{4})"


def pt(m):
    return (m[0] or "", m[1].lower(), m[2])


for pagina, md in LEGAL.items():
    fonte = os.path.join(REPO, md)
    if not os.path.exists(fonte):
        erros.append(f"{md}: fonte legal ausente no repositório — a data de {pagina} não tem com o que comparar")
        continue
    if not os.path.exists(p(pagina)):
        continue  # página contratual ausente já é erro no §1
    m = re.search(r"\*\*Última atualização:\*\*\s*" + RE_PT, ler(fonte))
    if not m:
        erros.append(f"{md}: sem linha `**Última atualização:** [D de ]Mês de AAAA`")
        continue
    ref = pt(m.groups())
    html = ler(p(pagina))
    datas_pt = [pt(x) for x in re.findall(r"Última atualização:\s*" + RE_PT, html)]
    datas_en = re.findall(r"Last updated:\s*" + RE_EN, html)
    for d in datas_pt:
        if d != ref:
            erros.append(f"{pagina}: data pt `{' de '.join(x for x in d if x)}` ≠ {md} `{' de '.join(x for x in ref if x)}`")
    for mo, d, a in datas_en:
        if (d or "", MESES.get(mo.lower(), "?"), a) != (ref[0], MESES.get(ref[1], "?"), ref[2]):
            erros.append(f"{pagina}: data en `{mo} {d + ', ' if d else ''}{a}` ≠ {md} `{' de '.join(x for x in ref if x)}`")
    if not datas_pt:
        avisos.append(f"{pagina}: nenhuma `Última atualização:` encontrada no HTML")
    if not datas_en:
        avisos.append(f"{pagina}: nenhuma `Last updated:` encontrada no HTML")

# ------------------------------------------------------------ 5: copy
for rel in PAGINAS_LOTTO:
    if not os.path.exists(p(rel)):
        continue
    texto = ler(p(rel))
    for n, linha in enumerate(texto.splitlines(), 1):
        for padrao in COPY_PROIBIDA:
            if re.search(padrao, linha, re.I):
                erros.append(f"{rel}:{n}: copy fere jogo responsável (`{padrao}`): {linha.strip()[:90]}")

# ------------------------------------------------------------ 6: assetlinks
try:
    al = json.loads(ler(p(".well-known/assetlinks.json")))
    pacotes = {e.get("target", {}).get("package_name") for e in al}
    if "br.com.ghfsoftware.lottoexpert" not in pacotes:
        erros.append("assetlinks.json: sem br.com.ghfsoftware.lottoexpert")
except Exception as e:  # noqa: BLE001
    erros.append(f"assetlinks.json inválido: {e}")

# ------------------------------------------------------------ resultado
print(f"páginas: {len(paginas)} | links locais verificados: {n_links}")
for a in avisos:
    print(f"⚠️  {a}")
if erros:
    print(f"\n❌ {len(erros)} erro(s):\n")
    for e in erros:
        print(f"  • {e}")
    sys.exit(1)
print("✅ site consistente")
