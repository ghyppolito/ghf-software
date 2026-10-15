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
  5. copy do LottoExpert respeita jogo responsável (mesma régua do PaywallCopyComplianceTest do app),
     no publicado (PAGINAS_LOTTO) e nas fontes Astro (FONTES_LOTTO)
  6. .well-known/assetlinks.json é JSON válido com o package do LottoExpert
  7. toda página de PUBLICADAS existe — na raiz do repositório como `.html` (página ainda copiada)
     ou como `src/pages/<x>.astro` (gerada); com `--raiz` fora da raiz (ex.: `dist/`), existe lá,
     e as que não estão em EN_PENDENTE têm o par `en/<x>`. Página esquecida em COPIADOS_DA_RAIZ do
     astro.config.mjs sairia do ar com o build verde
  8. hreflang: página com par en declara pt-BR e en, recíprocos, e os dois existem
  9. página em `en/` com link interno para página que tem par en aponta para o par

Na raiz do repositório, link para página gerada (`index.html`, `en/…`) resolve contra a fonte em
`src/pages/`; o arquivo de verdade só existe em `dist/`, onde a checagem é sobre o publicado.
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

# Tudo o que o site publica em pt — lista fixa, não derivada da raiz (que encolhe a cada fatia do
# WP-08 e deixaria página sumir calada). Página nova entra aqui no WP que a cria.
PUBLICADAS = [
    "index.html",
    "lottoexpert.html", "lottoexpert-privacy.html", "lottoexpert-terms.html",
    "topowalk.html", "topowalk-privacy.html",
    "poleposition.html", "poleposition-privacy.html",
    "eclipsego.html", "eclipsego-privacy.html",
    "lotto-expert/sweepstake-invite/lottoexpert-invite.html",
]

# Páginas ainda sem `/en/`. Só encolhe: a fatia que cria `en/<x>` tira `<x>` daqui no mesmo
# commit (espelho de COM_PAR_EN em src/i18n/ui.ts). Termina vazia no fim do WP-08. O convite
# não tem par en (formato é do app).
EN_PENDENTE = [
    "lottoexpert-privacy.html", "lottoexpert-terms.html",
    "topowalk-privacy.html",
    "poleposition.html", "poleposition-privacy.html",
    "eclipsego.html", "eclipsego-privacy.html",
]
SEM_PAR_EN = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
COM_PAR = [x for x in PUBLICADAS if x not in EN_PENDENTE and x not in SEM_PAR_EN]

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
                 "lotto-expert/sweepstake-invite/lottoexpert-invite.html",
                 "en/index.html", "en/lottoexpert.html", "en/lottoexpert-privacy.html", "en/lottoexpert-terms.html"]
# Fontes das páginas do LottoExpert já geradas pelo Astro: lidas sempre, a partir da raiz do
# repositório — na raiz não há o .html gerado, e a régua tem de valer antes do build também.
FONTES_LOTTO = ["src/i18n/home.ts", "src/components/Home.astro",
                "src/i18n/lottoexpert.ts", "src/components/LottoExpert.astro"]

erros, avisos = [], []


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def p(rel):
    return os.path.join(raiz, rel)


NA_RAIZ_DO_REPO = os.path.realpath(raiz) == os.path.realpath(REPO)


def fonte_gerada(rel):
    """`index.html` → `src/pages/index.astro`; `en/` e `en` → `src/pages/en/index.astro`.

    Segmento que começa com `_` (o Astro não publica) ou `[` (rota dinâmica, não página
    literal) não conta como fonte."""
    rel = rel.replace(os.sep, "/").lstrip("/")
    if rel in ("", ".") or rel.endswith("/"):
        rel = rel.rstrip(".") + "index.html"
    elif not rel.endswith(".html") and os.path.isdir(os.path.join(REPO, "src", "pages", rel)):
        rel += "/index.html"  # diretório sem barra (`en`), como o servidor estático resolve
    if not rel.endswith(".html"):
        return None
    if any(seg.startswith(("_", "[")) for seg in rel.split("/")):
        return None
    return os.path.join(REPO, "src", "pages", rel[: -len(".html")] + ".astro")


def existe_pagina(rel):
    """Na raiz do repositório, página gerada conta pela fonte; fora dela, só o arquivo."""
    if os.path.exists(p(rel)):
        return True
    if NA_RAIZ_DO_REPO:
        f = fonte_gerada(rel)
        return bool(f and os.path.exists(f))
    return False


SITE = "https://ghfsoftware.com/"


def url_para_rel(url):
    """URL absoluta do site → arquivo publicado (`/` e `/en/` → `index.html`)."""
    if not url.startswith(SITE):
        return None
    rel = url[len(SITE):].split("#")[0].split("?")[0]
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return rel


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
        destino = os.path.normpath(destino)
        if os.path.isdir(destino):
            destino = os.path.join(destino, "index.html")  # `/en/` publicado é `en/index.html`
        if not os.path.exists(destino):
            sufixo = "/" if alvo.endswith("/") else ""
            gerada = NA_RAIZ_DO_REPO and fonte_gerada(os.path.relpath(destino, raiz) + sufixo)
            if not (gerada and os.path.exists(gerada)):
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


def sem_tags(html):
    """Texto da página sem marcação: o markdown renderiza `<strong>Última atualização:</strong> 13
    de …`, que a regex sobre o HTML cru não casaria."""
    texto = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    texto = re.sub(r"<[^>]+>", " ", texto)
    return re.sub(r"\s+", " ", texto)


def datas_em(html, padrao):
    """União das datas achadas no texto sem tags (`<strong>Última atualização:</strong> …`) e no
    HTML cru (atributos como `<meta content="Última atualização: …">` e o dicionário JS das
    páginas ainda copiadas). Nenhuma das duas buscas sozinha cobre tudo."""
    achadas = re.findall(padrao, sem_tags(html)) + re.findall(padrao, html)
    return list(dict.fromkeys(achadas))


for pagina, md in LEGAL.items():
    fonte = os.path.join(REPO, md)
    if not os.path.exists(fonte):
        erros.append(f"{md}: fonte legal ausente no repositório — a data de {pagina} não tem com o que comparar")
        continue
    m = re.search(r"\*\*Última atualização:\*\*\s*" + RE_PT, ler(fonte))
    if not m:
        erros.append(f"{md}: sem linha `**Última atualização:** [D de ]Mês de AAAA`")
        continue
    ref = pt(m.groups())
    ref_txt = " de ".join(x for x in ref if x)
    # (página, idioma que ela tem de ter): a pt, e o par en quando existe (ou deveria existir).
    alvos = [(pagina, "pt")]
    if pagina not in EN_PENDENTE or os.path.exists(p("en/" + pagina)):
        alvos.append(("en/" + pagina, "en"))
    for alvo, idioma in alvos:
        if not os.path.exists(p(alvo)):
            if alvo != pagina and not NA_RAIZ_DO_REPO:
                erros.append(f"{alvo}: página legal en ausente ({pagina} saiu de EN_PENDENTE)")
            continue  # pt ausente já é erro no §1; en na raiz do repositório é gerada (só em dist/)
        html = ler(p(alvo))
        datas_pt = list(dict.fromkeys(pt(x) for x in datas_em(html, r"Última atualização:\s*" + RE_PT)))
        datas_en = datas_em(html, r"Last updated:\s*" + RE_EN)
        for d in datas_pt:
            if d != ref:
                erros.append(f"{alvo}: data pt `{' de '.join(x for x in d if x)}` ≠ {md} `{ref_txt}`")
        for mo, d, a in datas_en:
            if (d or "", MESES.get(mo.lower(), "?"), a) != (ref[0], MESES.get(ref[1], "?"), ref[2]):
                erros.append(f"{alvo}: data en `{mo} {d + ', ' if d else ''}{a}` ≠ {md} `{ref_txt}`")
        # A data do idioma da página é obrigatória; a do outro idioma só existe nas páginas
        # ainda copiadas (dicionário JS) — lá a ausência continua aviso.
        if idioma == "pt" and not datas_pt:
            erros.append(f"{alvo}: nenhuma `Última atualização:` encontrada")
        if idioma == "en" and not datas_en:
            erros.append(f"{alvo}: nenhuma `Last updated:` encontrada")
        if idioma == "pt" and not datas_en and pagina in EN_PENDENTE:
            avisos.append(f"{alvo}: nenhuma `Last updated:` encontrada no HTML")

# ------------------------------------------------------------ 5: copy
for rel, caminho in [(r, p(r)) for r in PAGINAS_LOTTO] + [(r, os.path.join(REPO, r)) for r in FONTES_LOTTO]:
    if not os.path.exists(caminho):
        if rel in FONTES_LOTTO:
            erros.append(f"{rel}: fonte do LottoExpert em FONTES_LOTTO ausente — atualize a lista")
        continue
    texto = ler(caminho)
    for n, linha in enumerate(texto.splitlines(), 1):
        for padrao in COPY_PROIBIDA:
            for m in re.finditer(padrao, linha, re.I):
                # Trecho em volta do match: em dist/ a página sai minificada numa linha só.
                trecho = re.sub(r"\s+", " ", linha[max(0, m.start() - 40): m.end() + 40]).strip()
                erros.append(f"{rel}:{n}: copy fere jogo responsável (`{padrao}`): …{trecho}…")

# ------------------------------------------------------------ 6: assetlinks
try:
    al = json.loads(ler(p(".well-known/assetlinks.json")))
    pacotes = {e.get("target", {}).get("package_name") for e in al}
    if "br.com.ghfsoftware.lottoexpert" not in pacotes:
        erros.append("assetlinks.json: sem br.com.ghfsoftware.lottoexpert")
except Exception as e:  # noqa: BLE001
    erros.append(f"assetlinks.json inválido: {e}")

# ------------------------------------------------------------ 7: nada fica para trás
# Lista fixa (PUBLICADAS), não o glob da raiz: a raiz encolhe a cada fatia do WP-08, e página que
# não chega ao publicado sai do ar sem nenhum outro check perceber (os links não a citam).
for rel in EN_PENDENTE + SEM_PAR_EN:
    if rel not in PUBLICADAS:
        erros.append(f"check_site.py: {rel} em EN_PENDENTE/SEM_PAR_EN mas fora de PUBLICADAS")
for rel in PUBLICADAS:
    if not existe_pagina(rel):
        onde = "na raiz nem em src/pages/" if NA_RAIZ_DO_REPO else f"em {raiz} — falta em COPIADOS_DA_RAIZ do astro.config.mjs ou em src/pages/?"
        erros.append(f"página publicada ausente {onde}: {rel}")
    en = "en/" + rel
    if rel in COM_PAR and not existe_pagina(en):
        erros.append(f"par en ausente: {en} ({rel} não está em EN_PENDENTE)")
    if rel in EN_PENDENTE and existe_pagina(en):
        erros.append(f"{en} existe, mas {rel} continua em EN_PENDENTE — tire-o da lista (e ponha em COM_PAR_EN de src/i18n/ui.ts)")
# Página .html na raiz do repositório que não está em PUBLICADAS não vai ao ar (lista fechada do
# astro.config.mjs): ou entra na lista, ou sai da raiz.
for c in sorted(glob.glob(os.path.join(REPO, "*.html"))):
    if os.path.basename(c) not in PUBLICADAS:
        erros.append(f"{os.path.basename(c)} na raiz do repositório e fora de PUBLICADAS")

# ------------------------------------------------------------ 8: hreflang
# Página com par en declara os dois idiomas, com os mesmos dois endereços nas duas pontas, e os
# dois existem. Só sobre arquivos presentes: na raiz do repositório, a página gerada é provada
# em dist/.
RE_ALT = re.compile(r"<link\b[^>]*>", re.I)


def hreflangs(html):
    out = {}
    for tag in RE_ALT.findall(html):
        if not re.search(r'rel="alternate"', tag):
            continue
        lang = re.search(r'hreflang="([^"]+)"', tag)
        href = re.search(r'href="([^"]+)"', tag)
        if lang and href:
            out[lang.group(1)] = href.group(1)
    return out


for rel in COM_PAR:
    for lado in (rel, "en/" + rel):
        if not os.path.exists(p(lado)):
            continue
        alt = hreflangs(ler(p(lado)))
        for lang, esperado in (("pt-BR", rel), ("en", "en/" + rel)):
            if lang not in alt:
                erros.append(f"{lado}: sem <link rel=\"alternate\" hreflang=\"{lang}\">")
                continue
            destino = url_para_rel(alt[lang])
            if destino != esperado:
                erros.append(f"{lado}: hreflang {lang} aponta para {alt[lang]}, esperado o de {esperado}")
            elif not existe_pagina(destino):
                erros.append(f"{lado}: hreflang {lang} aponta para {alt[lang]}, que não existe")

# ------------------------------------------------------------ 9: en aponta para en
# Link interno de página em en/ para página que tem par en vai para o par. A troca de idioma é a
# exceção declarada: só o link marcado `data-troca-idioma` (componente TrocaIdioma) é isento.
for caminho in paginas:
    rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
    if not rel.startswith("en/"):
        continue
    base = os.path.dirname(caminho)
    for tag in re.findall(r"<a\b[^>]*>", ler(caminho), re.I):
        href = re.search(r'href="([^"#?]*)[^"]*"', tag)
        if not href or re.search(r"\bdata-troca-idioma\b", tag):
            continue
        alvo = href.group(1)
        if alvo.startswith(SITE):
            alvo = "/" + alvo[len(SITE):]
        if re.match(r"^(https?:|mailto:|tel:|javascript:|data:|//)", alvo) or alvo == "":
            continue
        destino = os.path.join(raiz, alvo.lstrip("/")) if alvo.startswith("/") else os.path.join(base, alvo)
        destino = os.path.relpath(os.path.normpath(destino), raiz).replace(os.sep, "/")
        if destino == ".":
            destino = "index.html"
        elif alvo.endswith("/"):
            destino += "/index.html"
        if destino in COM_PAR:
            erros.append(f"{rel}: href=\"{href.group(1)}\" leva ao pt; o par en é /en/{destino}")

# ------------------------------------------------------------ 10: dicionários pt = en
# O `satisfies` dos dicionários em src/i18n/ aceita en com chaves a menos e o build não roda
# checagem de tipos: chave só em pt sairia vazia em /en/ sem erro. Lido do repositório, como §5.
for ts in sorted(glob.glob(os.path.join(REPO, "src/i18n/*.ts"))):
    blocos = re.findall(r"^  (pt|en): \{\n(.*?)^  \}", ler(ts), re.S | re.M)
    chaves = {lang: set(re.findall(r"^    (\w+):", corpo, re.M)) for lang, corpo in blocos}
    if not chaves:
        continue
    nome = os.path.relpath(ts, REPO)
    if set(chaves) != {"pt", "en"}:
        erros.append(f"{nome}: dicionário sem bloco pt e en no formato esperado")
        continue
    for lang, outro in (("pt", "en"), ("en", "pt")):
        for falta in sorted(chaves[lang] - chaves[outro]):
            erros.append(f"{nome}: chave `{falta}` existe em {lang} e falta em {outro}")

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
