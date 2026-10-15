#!/usr/bin/env python3
"""Rede de segurança do site — roda no /verify e no CI do PR.

Só biblioteca padrão, de propósito. Confere o site publicado: `dist/`, saída do `npm run build`
(ADR-002). Sem `--raiz`, usa `dist/` e falha pedindo o build se ele não existir. Desde a fatia 6
do WP-08 a raiz do repositório não é mais verificada: uma URL contratual
(`eclipsego-privacy.html`) só existe em `dist/`. As fontes (src/, docs/) são lidas sempre da raiz
do repositório. Falha com código 1 se encontrar erro.

Checa:
  1. URLs contratuais (ADR-001) existem
  2. cada página tem <html lang>, <title>, meta description e og:image
  3. href/src locais resolvem para arquivo existente; og:image em ghfsoftware.com resolve localmente
  4. "Última atualização" da página legal (pt e en) bate com a da fonte — lida sempre da raiz do
     repositório; fonte ausente é erro. Fonte em docs/ (páginas ainda copiadas): a linha
     `**Última atualização:**`. Fonte em src/content/legal/ (páginas migradas): o `lastUpdated`
     do front-matter do `.pt.md`, que tem de bater com a linha do corpo do `.pt.md`, e o
     `lastUpdated` do `.en.md` (e a linha `**Last updated:**` dele) com o do pt
  5. copy do LottoExpert respeita jogo responsável (mesma régua do PaywallCopyComplianceTest do app),
     no publicado (PAGINAS_LOTTO) e nas fontes Astro (FONTES_LOTTO)
  6. .well-known/assetlinks.json é JSON válido com o package do LottoExpert
  7. toda página de PUBLICADAS existe em `dist/` (o ramo da raiz do repositório, que aceitava
     `src/pages/<x>.astro` como prova, é legado — ver abaixo),
     e as que não estão em EN_PENDENTE têm o par `en/<x>`. Página esquecida em COPIADOS_DA_RAIZ do
     astro.config.mjs sairia do ar com o build verde
  8. hreflang: página com par en declara pt-BR e en, recíprocos, e os dois existem
  9. página em `en/` com link interno para página que tem par en aponta para o par
 10. dicionários de src/i18n/ têm as mesmas chaves em pt e en
 11. `dist/` não é mais antigo que as fontes (src/, configs, package.json, COPIADOS_DA_RAIZ do
     astro.config.mjs, fontes de LEGAL): sem isso, o check daria verde sobre um build velho
 12. página legal migrada (fonte em src/content/legal/), pt e en: um só `<h1`, um só rótulo de
     data do idioma da página, nenhuma aspa tipográfica que o `.md` não tenha, nenhum link
     `target="_blank"` sem `rel="noopener"`; e `.pt.md` e `.en.md` com a mesma contagem de `## `,
     `### `, linhas de tabela, itens de lista, links, crases (`code`) e `---`

Modo raiz (`--raiz .`) não é mais suportado desde a fatia 6 do WP-08: uma URL contratual
(`eclipsego-privacy.html`) só existe em `dist/`, e o §1 falharia na raiz. Os ramos que ainda o
tratam — `NA_RAIZ_DO_REPO`, `fonte_gerada`, `existe_pagina` (link para página gerada resolvido
contra a fonte em `src/pages/`) — ficam até a fatia 9, que os remove.
"""
import glob
import json
import os
import re
import sys

raiz = "dist"
if "--raiz" in sys.argv:
    raiz = sys.argv[sys.argv.index("--raiz") + 1]
if not os.path.isdir(raiz):
    print(f"❌ {raiz}/ não existe — rode `npm run build` (o check confere o site gerado, não a raiz)")
    sys.exit(1)

# Raiz do repositório = pasta acima de tools/, independente do cwd. As fontes legais (docs/*.md,
# src/content/legal/*.md) são lidas daqui: não são publicadas, e a data legal tem de ser
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
    "poleposition-privacy.html",
]
SEM_PAR_EN = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
COM_PAR = [x for x in PUBLICADAS if x not in EN_PENDENTE and x not in SEM_PAR_EN]

# página legal → markdown de origem no site. A origem da origem é o repositório do app. Página
# migrada (WP-08) aponta para o `.pt.md` de src/content/legal/, com front-matter `lastUpdated`; o
# `.en.md` é o mesmo nome com `.en.md`. As outras seguem em docs/ até a sua fatia.
LEGAL = {
    "lottoexpert-privacy.html": "docs/LOTTOEXPERT_PRIVACY_POLICY.md",
    "lottoexpert-terms.html": "docs/LOTTOEXPERT_TERMS_OF_SERVICE.md",
    "topowalk-privacy.html": "src/content/legal/topowalk-privacy.pt.md",
    "poleposition-privacy.html": "docs/POLEPOSITION_PRIVACY_POLICY.md",
    "eclipsego-privacy.html": "src/content/legal/eclipsego-privacy.pt.md",
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


# Legado do modo raiz (`--raiz .`), sem suporte desde a fatia 6 do WP-08 — uma URL contratual só
# existe em dist/. NA_RAIZ_DO_REPO, fonte_gerada e existe_pagina saem na fatia 9.
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


# ------------------------------------------------------------ 11: dist/ desatualizado
# O check confere o que o build gerou; dist/ mais velho que uma fonte é verde sobre um site que
# não é o do commit. Vale para `dist/` do repositório (padrão ou `--raiz dist`); no CI o build
# roda depois do checkout, então dist/ é sempre o mais novo. Diretórios contam (arquivo apagado
# muda o mtime do diretório).
def copiados_da_raiz():
    cfg = os.path.join(REPO, "astro.config.mjs")
    if not os.path.exists(cfg):
        return []
    m = re.search(r"const COPIADOS_DA_RAIZ = \[(.*?)\];", ler(cfg), re.S)
    if not m:
        erros.append("astro.config.mjs: COPIADOS_DA_RAIZ não encontrado — a checagem de dist/ desatualizado não sabe o que a raiz publica")
        return []
    return re.findall(r"'([^']+)'", m.group(1))


def mais_novo(rels):
    """(mtime, caminho relativo) do arquivo ou diretório mais novo entre `rels` (recursivo)."""
    melhor = (0.0, "")
    for rel in rels:
        alvo = os.path.join(REPO, rel)
        if not os.path.exists(alvo):
            continue
        andar = os.walk(alvo) if os.path.isdir(alvo) else [(os.path.dirname(alvo), [], [os.path.basename(alvo)])]
        if os.path.isdir(alvo):
            melhor = max(melhor, (os.path.getmtime(alvo), rel))
        for pasta, dirs, arqs in andar:
            for nome in dirs + arqs:
                c = os.path.join(pasta, nome)
                melhor = max(melhor, (os.path.getmtime(c), os.path.relpath(c, REPO)))
    return melhor


if os.path.realpath(raiz) == os.path.realpath(os.path.join(REPO, "dist")):
    gerado = p("index.html")
    if not os.path.exists(gerado):
        erros.append(f"{raiz}/index.html ausente — rode `npm run build`")
    else:
        fontes = (["src", "astro.config.mjs", "tailwind.config.mjs", "postcss.config.mjs", "package.json"]
                  + copiados_da_raiz() + list(LEGAL.values())
                  + [md[: -len(".pt.md")] + ".en.md" for md in LEGAL.values() if md.endswith(".pt.md")])
        t, novo = mais_novo(fontes)
        if t > os.path.getmtime(gerado):
            erros.append(f"dist/ mais antigo que as fontes ({novo}) — rode `npm run build`")

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


MESES_NUM = list(MESES_PT)  # "janeiro" … "dezembro", na ordem


def front_matter(md, texto):
    """(lastUpdated como (dia, mês pt, ano), corpo) de um .md de src/content/legal/; None se o
    front-matter ou o `lastUpdated: "AAAA-MM[-DD]"` faltar (erro registrado)."""
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    if not m:
        erros.append(f"{md}: sem front-matter (`---` / `lastUpdated: \"AAAA-MM-DD\"` / `---`) no topo")
        return None, texto
    corpo = texto[m.end():]
    lu = re.search(r'^lastUpdated:\s*"(\d{4})-(\d{2})(?:-(\d{2}))?"\s*$', m.group(1), re.M)
    if not lu or not 1 <= int(lu.group(2)) <= 12:
        erros.append(f"{md}: front-matter sem `lastUpdated: \"AAAA-MM\"` ou `\"AAAA-MM-DD\"` válido")
        return None, corpo
    ano, mes, dia = lu.groups()
    return (str(int(dia)) if dia else "", MESES_NUM[int(mes) - 1], ano), corpo


def txt(d):
    return " de ".join(x for x in d if x)


for pagina, md in LEGAL.items():
    fonte = os.path.join(REPO, md)
    if not os.path.exists(fonte):
        erros.append(f"{md}: fonte legal ausente no repositório — a data de {pagina} não tem com o que comparar")
        continue
    texto = ler(fonte)
    colecao = md.startswith("src/content/legal/")
    if colecao:
        ref_fm, texto = front_matter(md, texto)
        if ref_fm is None:
            continue
    m = re.search(r"\*\*Última atualização:\*\*\s*" + RE_PT, texto)
    if not m:
        erros.append(f"{md}: sem linha `**Última atualização:** [D de ]Mês de AAAA`")
        continue
    ref = pt(m.groups())
    ref = (str(int(ref[0])) if ref[0] else "", ref[1], ref[2])
    if colecao:
        if ref != ref_fm:
            erros.append(f"{md}: front-matter `lastUpdated` ({txt(ref_fm)}) ≠ linha `**Última atualização:**` do corpo ({txt(ref)})")
            continue
        md_en = md[: -len(".pt.md")] + ".en.md"
        if not os.path.exists(os.path.join(REPO, md_en)):
            erros.append(f"{md_en}: tradução ausente ({pagina} tem par en)")
        else:
            ref_en, corpo_en = front_matter(md_en, ler(os.path.join(REPO, md_en)))
            if ref_en is not None and ref_en != ref:
                erros.append(f"{md_en}: `lastUpdated` ({txt(ref_en)}) ≠ o do pt ({txt(ref)})")
            m_en = re.search(r"\*\*Last updated:\*\*\s*" + RE_EN, corpo_en)
            if not m_en:
                erros.append(f"{md_en}: sem linha `**Last updated:** Mês [D,] AAAA`")
            elif (str(int(m_en[2])) if m_en[2] else "", MESES.get(m_en[1].lower(), "?"), m_en[3]) != \
                    (ref[0], MESES.get(ref[1], "?"), ref[2]):
                erros.append(f"{md_en}: linha `**Last updated:**` ({m_en[1]} {m_en[2] or ''} {m_en[3]}) ≠ {txt(ref)}")
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
        datas_pt = [(str(int(d)) if d else "", mo, a) for d, mo, a in datas_pt]
        datas_en = datas_em(html, r"Last updated:\s*" + RE_EN)
        datas_en = [(mo, str(int(d)) if d else "", a) for mo, d, a in datas_en]
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

# ------------------------------------------------------------ 12: página legal migrada
# O que o plugin omiteCabecalhoLegal e o `smartPunctuation: false` do astro.config.mjs garantem,
# provado no publicado: título e data aparecem uma vez (no hero), as aspas são as do .md do app; e
# o .en.md tem a mesma estrutura do .pt.md (seção ou tabela perdida na tradução).
TIPOGRAFICAS = "“”‘’"
ROTULO = {"pt": "Última atualização", "en": "Last updated"}
for pagina, md in LEGAL.items():
    if not md.startswith("src/content/legal/"):
        continue
    base_md = md[: -len(".pt.md")]
    fontes_md = {lang: os.path.join(REPO, f"{base_md}.{lang}.md") for lang in ("pt", "en")}
    if not all(os.path.exists(f) for f in fontes_md.values()):
        continue  # ausência já é erro no §4
    texto_md = {lang: ler(f) for lang, f in fontes_md.items()}
    for alvo, lang in ((pagina, "pt"), ("en/" + pagina, "en")):
        if not os.path.exists(p(alvo)):
            continue  # ausência já é erro no §1/§4/§7
        html = ler(p(alvo))
        n_h1 = len(re.findall(r"<h1\b", html, re.I))
        if n_h1 != 1:
            erros.append(f"{alvo}: {n_h1} `<h1` (esperado 1 — o `# título` do .md não pode sair no corpo)")
        # o rótulo com dois-pontos: o texto pode citar a data pelo nome (TopoWalk, seção 12: `A data
        # de "Última atualização" no topo…`)
        n_rot = sem_tags(html).count(ROTULO[lang] + ":")
        if n_rot != 1:
            erros.append(f"{alvo}: {n_rot} rótulo(s) `{ROTULO[lang]}:` no texto (esperado 1 — a linha de data do .md não pode sair no corpo)")
        for ch in TIPOGRAFICAS:
            if html.count(ch) > texto_md[lang].count(ch):
                erros.append(f"{alvo}: aspa tipográfica `{ch}` ({html.count(ch)}×) além das de {base_md}.{lang}.md "
                             f"({texto_md[lang].count(ch)}×) — smartPunctuation ligado?")
        # Link que abre outra aba sem `noopener` deixa a página aberta alcançar esta por
        # `window.opener` (plugin linksExternosLegais de src/markdown/legal.mjs). A régua para o
        # site inteiro é de TARGET-BLANK-SEM-NOOPENER-01 (fatia 9).
        for tag in re.findall(r"<a\b[^>]*>", html, re.I):
            if re.search(r'target="_blank"', tag) and not re.search(r'rel="[^"]*\bnoopener\b', tag):
                erros.append(f"{alvo}: link com target=\"_blank\" sem rel=\"noopener\": {tag}")
    for nome, padrao in (("`## `", r"^## "), ("`### `", r"^### "), ("linhas de tabela `|`", r"^\|"),
                         ("itens de lista", r"^\s*([-*]|\d+\.) "), ("links `](`", r"\]\("),
                         ("crases `` ` `` (code)", r"`"), ("`---`", r"^---$")):
        # o `---` do front-matter conta igual nos dois lados
        n = {lang: len(re.findall(padrao, texto_md[lang], re.M)) for lang in ("pt", "en")}
        if n["pt"] != n["en"]:
            erros.append(f"{base_md}.en.md: {n['en']} {nome} ≠ {n['pt']} do .pt.md — tradução com estrutura diferente")

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
