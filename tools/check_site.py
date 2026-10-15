#!/usr/bin/env python3
"""Rede de segurança do site — roda no /verify e no CI do PR.

Só biblioteca padrão, de propósito. Confere o site publicado: `dist/`, saída do `npm run build`
(ADR-002). Sem `--raiz`, usa `dist/` e falha pedindo o build se ele não existir. A raiz do
repositório não é verificada como site: nenhuma página vem dela (desde a fatia 8 do WP-08). As
fontes (src/, public/) são lidas sempre da raiz do repositório. Falha com código 1 se encontrar
erro.

Checa:
  1. URLs contratuais (ADR-001) existem
  2. cada página tem <html lang>, <title>, meta description e og:image (sem og:image é erro desde o WP-11)
  3. href/src locais resolvem para arquivo existente; og:image em ghfsoftware.com resolve localmente;
     nenhum `<a>`, `<area>` ou `<form>` com `target="_blank"` sem o token `noopener` em `rel`, em
     qualquer página de `dist/` (lido por html.parser, não por regex)
  4. "Última atualização" da página legal (pt e en) bate com a da fonte — lida sempre da raiz do
     repositório; fonte ausente é erro. A fonte é o `lastUpdated` do front-matter do `.pt.md` de
     src/content/legal/, que tem de bater com a linha do corpo do `.pt.md`, e o `lastUpdated` do
     `.en.md` (e a linha `**Last updated:**` dele) com o do pt. Proveniência (ADR-004): front-matter
     só com `lastUpdated`, `origemCommit` e `en`; o `.pt.md` tem `origemCommit` de 40 hex e não tem
     `en: "pendente"` (en atrás do pt); o `.en.md` não tem nem um nem outro; `ORIGENS` de
     tools/sync_legal.py cobre exatamente LEGAL. Com o repositório do app presente
     (`$GHF_APPS_DIR` ou `--apps-dir`, padrão `..`): corpo do `.pt.md` igual byte a byte a
     `git show <origemCommit>:<caminho>` (erro), commit inexistente no app (erro), commit fora de
     remoto (aviso), ref padrão com texto diferente (aviso). Sem o repositório (o CI, D15): um aviso
     por repositório, sem erro
  5. copy do LottoExpert respeita jogo responsável (mesma régua do PaywallCopyComplianceTest do app),
     no publicado (PAGINAS_LOTTO) e nas fontes Astro (FONTES_LOTTO)
  6. .well-known/assetlinks.json é JSON válido com o package do LottoExpert
  7. toda página de PUBLICADAS existe em `dist/`, e as que não estão em EN_PENDENTE têm o par
     `en/<x>`; nenhum `.html` na raiz do repositório (não vai ao ar)
  8. hreflang: página com par en declara pt-BR e en, recíprocos, e os dois existem
  9. página em `en/` com link interno para página que tem par en aponta para o par
 10. dicionários de src/i18n/ têm as mesmas chaves em pt e en
 11. `dist/` não é mais antigo que as fontes (src/, public/, configs, package.json, fontes de
     LEGAL): sem isso, o check daria verde sobre um build velho
 12. página legal, pt e en: um só `<h1`, um só rótulo de data do idioma da página, nenhuma aspa
     tipográfica que o `.md` não tenha; link do corpo para o próprio site é caminho a partir
     da raiz (nunca `https://ghfsoftware.com/…`), sem `target`, e em `en/` aponta para o par; e
     `.pt.md` e `.en.md` com a mesma contagem de `## `, `### `, linhas de tabela, itens de lista,
     links, crases (`code`) e `---`
 13. public/ (copiado byte a byte para dist/, ADR-002 §3): primeiro nível é a lista fechada
     PUBLIC; nenhum `.html` além do convite; nenhum symlink; todo arquivo de public/ igual byte a
     byte ao de dist/.
     O Astro publica o arquivo de public/ no lugar da página gerada que colide com ele, com o build
     verde — sem esta guarda, uma cópia velha de página contratual iria ao ar calada; e o
     `.htmlvalidateignore` da raiz isenta do html-validate só o convite (congelado pelo sha256, D13),
     e `rules` do `.htmlvalidate.json` é exatamente `{"no-inline-style": "off"}`
 14. SEO técnico (WP-11, ADR-005). Toda página de `dist/` está em INDEXAVEIS (as 20 com par),
     NOINDEX (a 404) ou CONGELADAS (o convite, o mesmo `.html` de tools/contrato.sha256, isento de
     tudo aqui). Fora de CONGELADAS: um só canonical, igual ao og:url e à URL da própria página
     (`/x.html`, `/`, `/en/`); hreflang pt-BR, en e x-default (= en), recíprocos, só nas
     INDEXAVEIS; `noindex` só e sempre nas NOINDEX; og:* e twitter:* completos; og:image:width e
     height juntos e iguais ao tamanho real do arquivo (cabeçalho PNG/JPEG lido aqui).
     `robots.txt` igual ao literal ROBOTS (nenhum `Disallow`), gerado por src/pages/robots.txt.ts;
     `sitemap.xml` (src/pages/sitemap.xml.ts) faz parse, seus `<loc>` são exatamente as URLs das
     INDEXAVEIS (sem repetir, cada uma existe em dist/) e cada `<url>` traz os mesmos três hreflang
     da página. JSON-LD: cada `<script type="application/ld+json">` faz `json.loads`; `Organization`
     só nas duas home, `MobileApplication` só nas 8 landings, nenhum nas demais; chaves exatamente
     as permitidas (sem `aggregateRating`, `review`, preço do Premium); `installUrl` com o mesmo
     `id` do botão da Play da página; o texto do JSON-LD (já decodificado) passa pela régua do §5
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

sys.dont_write_bytecode = True  # importar sync_legal não deixa tools/__pycache__ no repositório
from sync_legal import ORIGENS, RE_SHA, CHAVES, apps_dir_padrao, repo_presente, resolve, mostra, em_remoto, separa  # noqa: E402

raiz = "dist"
if "--raiz" in sys.argv:
    raiz = sys.argv[sys.argv.index("--raiz") + 1]
APPS_DIR = apps_dir_padrao()
if "--apps-dir" in sys.argv:
    APPS_DIR = sys.argv[sys.argv.index("--apps-dir") + 1]
if not os.path.isdir(raiz):
    print(f"❌ {raiz}/ não existe — rode `npm run build` (o check confere o site gerado, não a raiz)")
    sys.exit(1)

# Raiz do repositório = pasta acima de tools/, independente do cwd. As fontes legais
# (src/content/legal/*.md) são lidas daqui: não são publicadas, e a data legal tem de ser
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
EN_PENDENTE = []
SEM_PAR_EN = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
COM_PAR = [x for x in PUBLICADAS if x not in EN_PENDENTE and x not in SEM_PAR_EN]

# página legal → markdown de origem no site (`.pt.md` de src/content/legal/, com front-matter
# `lastUpdated`; o `.en.md` é o mesmo nome com `.en.md`). A origem da origem é o repositório do app.
LEGAL = {
    "lottoexpert-privacy.html": "src/content/legal/lottoexpert-privacy.pt.md",
    "lottoexpert-terms.html": "src/content/legal/lottoexpert-terms.pt.md",
    "topowalk-privacy.html": "src/content/legal/topowalk-privacy.pt.md",
    "poleposition-privacy.html": "src/content/legal/poleposition-privacy.pt.md",
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
# Fontes das páginas do LottoExpert (src/): a régua roda sobre elas, lidas da raiz do repositório,
# sempre que o check roda — além do HTML gerado em dist/ (PAGINAS_LOTTO), que o check exige.
FONTES_LOTTO = ["src/i18n/home.ts", "src/components/Home.astro",
                "src/i18n/lottoexpert.ts", "src/components/LottoExpert.astro",
                "src/i18n/legal.ts", "src/i18n/apps.ts",
                "src/content/legal/lottoexpert-privacy.pt.md", "src/content/legal/lottoexpert-privacy.en.md",
                "src/content/legal/lottoexpert-terms.pt.md", "src/content/legal/lottoexpert-terms.en.md"]

erros, avisos = [], []


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def p(rel):
    return os.path.join(raiz, rel)


SITE = "https://ghfsoftware.com/"
SITE_HOST = re.compile(r"^https?://(www\.)?ghfsoftware\.com/", re.I)  # host do site em link do texto legal (§12)


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
        fontes = (["src", "public", "astro.config.mjs", "tailwind.config.mjs", "postcss.config.mjs", "package.json"]
                  + list(LEGAL.values())
                  + [md[: -len(".pt.md")] + ".en.md" for md in LEGAL.values() if md.endswith(".pt.md")])
        t, novo = mais_novo(fontes)
        if t > os.path.getmtime(gerado):
            erros.append(f"dist/ mais antigo que as fontes ({novo}) — rode `npm run build`")

# ------------------------------------------------------------ 1: contratuais
for rel in CONTRATUAIS:
    if not os.path.exists(p(rel)):
        erros.append(f"URL contratual ausente (ADR-001): /{rel}")

# ------------------------------------------------------------ 2 e 3: páginas
paginas = sorted(glob.glob(p("**/*.html"), recursive=True))
# Link que abre outra aba sem `noopener` deixa a página aberta alcançar esta por `window.opener`
# (TARGET-BLANK-SEM-NOOPENER-01). Vale para todo `dist/`, com ou sem aspas no atributo.
# Lido por html.parser (não regex): atributo é atributo — `data-rel`, `title="rel=noopener"` e `>`
# dentro de aspas não enganam. Olha `a`, `area` e `form`; `rel` tem de ter o token `noopener`.
TAGS_COM_TARGET = ("a", "area", "form")


class SemNoopener(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.achados = []

    def handle_starttag(self, tag, attrs):
        if tag not in TAGS_COM_TARGET:
            return
        d = {k.lower(): (v or "") for k, v in attrs}
        if d.get("target", "").strip().lower() != "_blank":
            return
        if "noopener" not in d.get("rel", "").lower().split():
            self.achados.append(self.get_starttag_text() or f"<{tag}>")

    handle_startendtag = handle_starttag


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
        erros.append(f"{rel}: sem og:image (toda página tem, inclusive legal e 404 — WP-11)")
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
            erros.append(f"{rel}: {attr}=\"{alvo}\" não resolve")
    # og:image em onerror e afins (o convite usa fallback por JS)
    for alvo in re.findall(r"https://ghfsoftware\.com/([A-Za-z0-9_./-]+\.(?:png|jpg|webp|svg))", html):
        if not os.path.exists(p(alvo)):
            erros.append(f"{rel}: referência a https://ghfsoftware.com/{alvo}, que não existe")
    leitor = SemNoopener()
    leitor.feed(html)
    leitor.close()
    for tag in leitor.achados:
        erros.append(f"{rel}: target=\"_blank\" sem rel=\"noopener\": {tag}")

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
    HTML cru (atributos como `<meta content="Última atualização: …">`). Nenhuma das duas buscas
    sozinha cobre tudo."""
    achadas = re.findall(padrao, sem_tags(html)) + re.findall(padrao, html)
    return list(dict.fromkeys(achadas))


MESES_NUM = list(MESES_PT)  # "janeiro" … "dezembro", na ordem


def ler_md(caminho):
    """Texto de um .md legal sem tradução de newline (open em modo texto converte CRLF em LF e
    esconderia o front-matter em CRLF que separa(), em bytes, não reconhece)."""
    with open(caminho, "rb") as f:
        return f.read().decode("utf-8")


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
    ref_fm, texto = front_matter(md, ler_md(fonte))
    if ref_fm is None:
        continue
    m = re.search(r"\*\*Última atualização:\*\*\s*" + RE_PT, texto)
    if not m:
        erros.append(f"{md}: sem linha `**Última atualização:** [D de ]Mês de AAAA`")
        continue
    ref = pt(m.groups())
    ref = (str(int(ref[0])) if ref[0] else "", ref[1], ref[2])
    if ref != ref_fm:
        erros.append(f"{md}: front-matter `lastUpdated` ({txt(ref_fm)}) ≠ linha `**Última atualização:**` do corpo ({txt(ref)})")
        continue
    md_en = md[: -len(".pt.md")] + ".en.md"
    if not os.path.exists(os.path.join(REPO, md_en)):
        erros.append(f"{md_en}: tradução ausente ({pagina} tem par en)")
    else:
        ref_en, corpo_en = front_matter(md_en, ler_md(os.path.join(REPO, md_en)))
        if ref_en is not None and ref_en != ref:
            erros.append(f"{md_en}: `lastUpdated` ({txt(ref_en)}) ≠ o do pt ({txt(ref)})")
        m_en = re.search(r"\*\*Last updated:\*\*\s*" + RE_EN, corpo_en)
        if not m_en:
            erros.append(f"{md_en}: sem linha `**Last updated:** Mês [D,] AAAA`")
        elif (str(int(m_en[2])) if m_en[2] else "", MESES.get(m_en[1].lower(), "?"), m_en[3]) != \
                (ref[0], MESES.get(ref[1], "?"), ref[2]):
            erros.append(f"{md_en}: linha `**Last updated:**` ({m_en[1]} {m_en[2] or ''} {m_en[3]}) ≠ {txt(ref)}")
    ref_txt = " de ".join(x for x in ref if x)
    # (página, idioma que ela tem de ter): a pt e o par en.
    for alvo, idioma in ((pagina, "pt"), ("en/" + pagina, "en")):
        if not os.path.exists(p(alvo)):
            if alvo != pagina:
                erros.append(f"{alvo}: página legal en ausente")
            continue  # pt ausente já é erro no §1
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
        # A data do idioma da página é obrigatória.
        if idioma == "pt" and not datas_pt:
            erros.append(f"{alvo}: nenhuma `Última atualização:` encontrada")
        if idioma == "en" and not datas_en:
            erros.append(f"{alvo}: nenhuma `Last updated:` encontrada")

# Proveniência (ADR-004). Sempre (inclusive no CI): formato do front-matter, origemCommit no pt,
# `en: "pendente"` como erro, nada disso no en, ORIGENS = LEGAL. Com o repositório do app presente:
# o corpo do pt é o `git show` do commit registrado, byte a byte (lido em binário: CRLF, BOM e
# newline final contam).
docs_legal = {os.path.basename(md)[: -len(".pt.md")] for md in LEGAL.values()}
if set(ORIGENS) != docs_legal:
    erros.append(f"ORIGENS de tools/sync_legal.py ≠ LEGAL do check_site.py: só em ORIGENS "
                 f"{sorted(set(ORIGENS) - docs_legal)}, só em LEGAL {sorted(docs_legal - set(ORIGENS))}")
ausentes = set()
for md in LEGAL.values():
    doc = os.path.basename(md)[: -len(".pt.md")]
    for lado in (md, md[: -len(".pt.md")] + ".en.md"):
        if not os.path.exists(os.path.join(REPO, lado)):
            continue  # ausência já é erro acima
        with open(os.path.join(REPO, lado), "rb") as f:
            fm, chaves, corpo_b = separa(f.read())
        if fm is None:
            erros.append(f"{lado}: front-matter fora do formato `---\\n…\\n---\\n` em LF — rode tools/sync_legal.py")
            continue
        estranhas = [k for k in chaves if k not in CHAVES or fm[k] is None]
        if estranhas or len(chaves) != len(set(chaves)):
            erros.append(f"{lado}: front-matter com chave fora de {{{', '.join(CHAVES)}}}, sem aspas ou repetida: {chaves}")
        if lado.endswith(".en.md"):
            for k in ("origemCommit", "en"):
                if k in fm:
                    erros.append(f"{lado}: `{k}` no .en.md — proveniência e marcador ficam só no .pt.md (ADR-004)")
            continue
        if "en" in fm:
            if fm["en"] == "pendente":
                erros.append(f"{lado}: `en: \"pendente\"` — en atrás do pt — traduzir e tirar o marcador")
            else:
                erros.append(f"{lado}: `en: {fm['en']!r}` — o único valor é \"pendente\" (e só enquanto o en está atrás)")
        sha = fm.get("origemCommit")
        if not sha or not RE_SHA.match(sha):
            erros.append(f"{lado}: front-matter sem `origemCommit: \"<sha de 40 hex minúsculos>\"` — rode tools/sync_legal.py")
            continue
        if doc not in ORIGENS:
            continue  # já é erro (ORIGENS ≠ LEGAL)
        repo, caminho, ref_padrao = ORIGENS[doc]
        repo_dir = os.path.join(APPS_DIR, repo)
        if not repo_presente(APPS_DIR, repo):
            if repo not in ausentes:
                ausentes.add(repo)
                avisos.append(f"{repo}: origem ausente ({repo_dir}) — comparação de texto pulada")
            continue
        if resolve(repo_dir, sha) is None:
            erros.append(f"{lado}: origemCommit {sha[:7]} não existe em {repo} — `git fetch` no app ou origemCommit inventado")
            continue
        origem = mostra(repo_dir, sha, caminho)
        if origem != corpo_b:
            erros.append(f"{lado}: pt ≠ {repo}@{sha[:7]}:{caminho} — texto editado à mão? rode sync_legal")
            continue
        if not em_remoto(repo_dir, sha):
            avisos.append(f"{lado}: origemCommit {sha[:7]} não está em nenhum remoto de {repo} — texto publicado de commit que só existe na sua máquina")
        sha_ref = resolve(repo_dir, ref_padrao)
        if sha_ref is None:
            avisos.append(f"{lado}: ref padrão `{ref_padrao}` não existe em {repo}")
        elif mostra(repo_dir, sha_ref, caminho) != corpo_b:
            app = doc.rsplit("-", 1)[0]
            avisos.append(f"{lado}: {repo}@{ref_padrao} ({sha_ref[:7]}) — texto da ref padrão ≠ origemCommit — "
                          f"`python3 tools/sync_legal.py {app} --check` diz se é atraso ou divergência")

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
    if not os.path.exists(p(rel)):
        erros.append(f"página publicada ausente em {raiz} — falta em src/pages/?: {rel}")
    en = "en/" + rel
    if rel in COM_PAR and not os.path.exists(p(en)):
        erros.append(f"par en ausente: {en} ({rel} não está em EN_PENDENTE)")
    if rel in EN_PENDENTE and os.path.exists(p(en)):
        erros.append(f"{en} existe, mas {rel} continua em EN_PENDENTE — tire-o da lista (e ponha em COM_PAR_EN de src/i18n/ui.ts)")
# Página .html na raiz do repositório não vai ao ar (o Astro publica src/pages/ e public/): página
# nasce em src/pages/.
for c in sorted(glob.glob(os.path.join(REPO, "*.html"))):
    erros.append(f"{os.path.basename(c)} na raiz do repositório — não vai ao ar; página nasce em src/pages/")

# ------------------------------------------------------------ 8: hreflang
# Página com par en declara os dois idiomas, com os mesmos dois endereços nas duas pontas, e os
# dois existem (a ausência de um dos lados já é erro no §7).
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
            elif not os.path.exists(p(destino)):
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

# ------------------------------------------------------------ 12: página legal
# O que o plugin omiteCabecalhoLegal e o `smartPunctuation: false` do astro.config.mjs garantem,
# provado no publicado: título e data aparecem uma vez (no hero), as aspas são as do .md do app; e
# o .en.md tem a mesma estrutura do .pt.md (seção ou tabela perdida na tradução).
TIPOGRAFICAS = "“”‘’"
ROTULO = {"pt": "Última atualização", "en": "Last updated"}
for pagina, md in LEGAL.items():
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
        # Link do corpo para o próprio site (o `.md` do app escreve `https://ghfsoftware.com/x.html`):
        # o plugin linksInternosLegais de src/markdown/legal.mjs o torna `/x.html` (`/en/x.html` no
        # en, só para página `.html` — asset e o convite `lotto-expert/…` não têm par), na mesma aba,
        # como a página antiga. O host vale com ou sem `www.`, por http ou https. URL absoluta sai do ar com o domínio de teste,
        # abre outra aba e, em `en/`, leva ao pt.
        ini = html.find('class="legal-corpo')
        fim = html.find('<div class="max-w-4xl mx-auto mt-8 text-center">', ini)
        corpo = html[ini:fim] if ini >= 0 and fim > ini else ""
        if not corpo:
            erros.append(f"{alvo}: corpo legal (`.legal-corpo`) não encontrado — a regra dos links do próprio site não tem onde olhar")
        for tag in re.findall(r"<a\b[^>]*>", corpo, re.I):
            href = re.search(r'href="([^"]*)"', tag)
            if not href:
                continue
            h = href.group(1)
            if SITE_HOST.match(h) or h.startswith("//"):
                resto = SITE_HOST.sub("", h)
                arq = resto.split("#")[0].split("?")[0]
                par = lang == "en" and arq.endswith(".html") and not arq.startswith("lotto-expert/")
                erros.append(f"{alvo}: link legal para o próprio site com URL absoluta ({h}) — esperado `/{'en/' if par else ''}{resto}` (plugin linksInternosLegais desligado?)")
            elif h.startswith("/"):
                if re.search(r"\btarget=", tag):
                    erros.append(f"{alvo}: link legal para o próprio site com target (abre outra aba): {tag}")
                destino = h.lstrip("/").split("#")[0].split("?")[0] or "index.html"
                if lang == "en" and destino in COM_PAR:
                    erros.append(f"{alvo}: link legal {h} leva ao pt; o par en é /en/{destino}")
    for nome, padrao in (("`## `", r"^## "), ("`### `", r"^### "), ("linhas de tabela `|`", r"^\|"),
                         ("itens de lista", r"^\s*([-*]|\d+\.) "), ("links `](`", r"\]\("),
                         ("crases `` ` `` (code)", r"`"), ("`---`", r"^---$")):
        # o `---` do front-matter conta igual nos dois lados
        n = {lang: len(re.findall(padrao, texto_md[lang], re.M)) for lang in ("pt", "en")}
        if n["pt"] != n["en"]:
            erros.append(f"{base_md}.en.md: {n['en']} {nome} ≠ {n['pt']} do .pt.md — tradução com estrutura diferente")

# ------------------------------------------------------------ 13: public/
# public/ vai a dist/ byte a byte (ADR-002 §3). Ao colidir com página gerada, o Astro publica o
# arquivo de public/ e só avisa ("Skipping src/pages/x.astro…"), com o build verde: uma cópia velha
# de página contratual iria ao ar no lugar da gerada. (a) primeiro nível fechado; (b) nenhum .html
# além do convite (contrato byte a byte, D13); (c) cada arquivo de public/ igual ao de dist/.
PUBLIC = ["assets", ".well-known", "lotto-expert", "CNAME"]
HTML_EM_PUBLIC = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
pasta_public = os.path.join(REPO, "public")
if not os.path.isdir(pasta_public):
    erros.append("public/ ausente — imagens, App Links, convite e CNAME não iriam ao ar")
else:
    for nome in sorted(os.listdir(pasta_public)):
        if nome not in PUBLIC:
            erros.append(f"public/{nome}: fora da lista fechada de public/ ({', '.join(PUBLIC)}) — o check_site.py não o conhece")
    for nome in PUBLIC:
        if not os.path.exists(os.path.join(pasta_public, nome)):
            erros.append(f"public/{nome}: ausente (lista fechada de public/)")
    # Symlink em public/ (arquivo ou diretório) é erro: os.walk não desce em diretório-link, mas o
    # Astro copia o conteúdo dele para dist/ — uma página velha iria ao ar sem o check ver.
    for pasta, dirs, arqs in os.walk(pasta_public):
        for nome in sorted(dirs + arqs):
            c = os.path.join(pasta, nome)
            if os.path.islink(c):
                rel = os.path.relpath(c, pasta_public).replace(os.sep, "/")
                erros.append(f"public/{rel}: symlink em public/ — o Astro copia o alvo sem o check_site.py ver; use arquivo real")
        for nome in sorted(arqs):
            c = os.path.join(pasta, nome)
            rel = os.path.relpath(c, pasta_public).replace(os.sep, "/")
            if rel.lower().endswith((".html", ".htm")) and rel not in HTML_EM_PUBLIC:
                erros.append(f"public/{rel}: página em public/ — o Astro a publica no lugar da gerada; página nasce em src/pages/")
            publicado = p(rel)
            if not os.path.isfile(publicado):
                erros.append(f"public/{rel}: ausente em {raiz}/ — rode `npm run build`")
            else:
                with open(c, "rb") as fa, open(publicado, "rb") as fb:
                    if fa.read() != fb.read():
                        erros.append(f"public/{rel}: diferente de {raiz}/{rel} — public/ vai ao ar byte a byte")
# (d) o html-validate roda sobre dist/ com as regras do preset `recommended` em erro; só o convite,
# congelado pelo sha256 (D13), fica de fora. Glob mais largo esconderia página do validador. Quando
# o convite mudar (novo tools/contrato.sha256), ele sai do ignore no mesmo PR.
IGNORE_HTMLVALIDATE = ["dist/lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
arq_ignore = os.path.join(REPO, ".htmlvalidateignore")
if not os.path.exists(arq_ignore):
    erros.append(".htmlvalidateignore ausente — o convite (2 espaços no fim de linha, congelado) reprova o html-validate")
else:
    linhas = [x.strip() for x in ler(arq_ignore).splitlines() if x.strip() and not x.strip().startswith("#")]
    if linhas != IGNORE_HTMLVALIDATE:
        erros.append(f".htmlvalidateignore: {linhas} ≠ {IGNORE_HTMLVALIDATE} — só o convite fica fora do html-validate")

# As regras do preset ficam em erro: só `no-inline-style` é desligada. Rebaixar uma regra para
# "warn" faz o html-validate sair com código 0 e esconde o problema.
REGRAS_HTMLVALIDATE = {"no-inline-style": "off"}
arq_hv = os.path.join(REPO, ".htmlvalidate.json")
try:
    regras = json.loads(ler(arq_hv)).get("rules")
except (OSError, ValueError) as e:
    erros.append(f".htmlvalidate.json ilegível: {e}")
else:
    if regras != REGRAS_HTMLVALIDATE:
        erros.append(f".htmlvalidate.json: rules = {regras} ≠ {REGRAS_HTMLVALIDATE} — nenhuma regra do preset é rebaixada")

# ------------------------------------------------------------ 14: SEO técnico
# ADR-005. Canonical, og:url, <loc> do sitemap e href de hreflang são a mesma string: SITE + o
# caminho literal (`/x.html`, `/`, `/en/`). O convite fica fora de toda regra de SEO: é congelado
# byte a byte (D13), e a lista é a mesma do tools/contrato.sha256 (conferida abaixo).
CONGELADAS = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
INDEXAVEIS = COM_PAR + ["en/" + x for x in COM_PAR]
NOINDEX = ["404.html"]
OG_OBRIGATORIAS = ["og:type", "og:site_name", "og:url", "og:title", "og:description", "og:image",
                   "og:locale", "twitter:card", "twitter:title", "twitter:description", "twitter:image"]

arq_contrato = os.path.join(REPO, "tools", "contrato.sha256")
html_contrato = sorted(linha.split()[-1] for linha in ler(arq_contrato).splitlines()
                       if linha.strip() and linha.split()[-1].endswith(".html")) if os.path.exists(arq_contrato) else []
if html_contrato != sorted(CONGELADAS):
    erros.append(f"check_site.py: CONGELADAS {CONGELADAS} ≠ páginas de tools/contrato.sha256 {html_contrato}")


def url_canonica(rel):
    """URL pública de um arquivo de dist/: `index.html` vira a pasta (`/`, `/en/`)."""
    return SITE + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)


class Cabeca(HTMLParser):
    """Lê canonical, hreflang, meta (property/name) e o texto de cada `<script type=application/ld+json>`."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicas, self.alternates, self.meta, self.jsonld = [], [], {}, []
        self._ld = None

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "link":
            rels = d.get("rel", "").lower().split()
            if "canonical" in rels:
                self.canonicas.append(d.get("href", ""))
            if "alternate" in rels and "hreflang" in d:
                self.alternates.append((d["hreflang"], d.get("href", "")))
        elif tag == "meta":
            chave = d.get("property") or d.get("name")
            if chave:
                self.meta.setdefault(chave.lower(), []).append(d.get("content", ""))
        elif tag == "script" and d.get("type", "").lower() == "application/ld+json":
            self._ld = []

    handle_startendtag = handle_starttag

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            self.jsonld.append("".join(self._ld))
            self._ld = None


def dimensoes(caminho):
    """(largura, altura) de um PNG ou JPEG pelo cabeçalho; None se o formato for outro."""
    with open(caminho, "rb") as f:
        b = f.read()
    if b[:8] == b"\x89PNG\r\n\x1a\n" and b[12:16] == b"IHDR":
        return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    if b[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF:
                return None
            marcador = b[i + 1]
            if marcador == 0xFF:
                i += 1
                continue
            if 0xC0 <= marcador <= 0xCF and marcador not in (0xC4, 0xC8, 0xCC):
                return int.from_bytes(b[i + 7:i + 9], "big"), int.from_bytes(b[i + 5:i + 7], "big")
            i += 2 + int.from_bytes(b[i + 2:i + 4], "big")
    return None


cabecas = {}
for caminho in paginas:
    rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
    if rel in CONGELADAS:
        continue
    if rel not in INDEXAVEIS and rel not in NOINDEX:
        erros.append(f"{rel}: página fora de INDEXAVEIS, NOINDEX e CONGELADAS do §14 — classifique-a")
        continue
    c = Cabeca()
    c.feed(ler(caminho))
    c.close()
    cabecas[rel] = c
    propria = url_canonica(rel)
    if len(c.canonicas) != 1:
        erros.append(f"{rel}: {len(c.canonicas)} <link rel=\"canonical\"> (esperado 1)")
    elif c.canonicas[0] != propria:
        erros.append(f"{rel}: canonical {c.canonicas[0]} ≠ a URL da própria página {propria}")
    og_url = c.meta.get("og:url", [])
    if og_url and og_url != c.canonicas[:1]:
        erros.append(f"{rel}: og:url {og_url} ≠ canonical {c.canonicas[:1]}")
    for chave in OG_OBRIGATORIAS:
        if len(c.meta.get(chave, [])) != 1 or not c.meta[chave][0].strip():
            erros.append(f"{rel}: {chave} ausente, vazio ou repetido ({len(c.meta.get(chave, []))}×)")
    # hreflang: só nas INDEXAVEIS, exatamente pt-BR, en e x-default (= en, D8/D18), recíprocos (o par
    # declara os mesmos três endereços, porque os dois apontam para as mesmas URLs esperadas).
    alt = dict(c.alternates)
    if rel in INDEXAVEIS:
        pt_rel = rel[len("en/"):] if rel.startswith("en/") else rel
        esperado = {"pt-BR": url_canonica(pt_rel), "en": url_canonica("en/" + pt_rel), "x-default": url_canonica("en/" + pt_rel)}
        if len(c.alternates) != len(alt) or alt != esperado:
            erros.append(f"{rel}: hreflang {sorted(c.alternates)} ≠ esperado {sorted(esperado.items())} (x-default = en)")
    elif c.alternates:
        erros.append(f"{rel}: hreflang {c.alternates} numa página sem par (só as INDEXAVEIS declaram)")
    # indexação: `noindex` só e sempre nas NOINDEX
    tem_noindex = any("noindex" in v.lower() for k in ("robots", "googlebot") for v in c.meta.get(k, []))
    if rel in NOINDEX and not tem_noindex:
        erros.append(f"{rel}: sem <meta name=\"robots\" content=\"noindex\"> (está em NOINDEX)")
    if rel not in NOINDEX and tem_noindex:
        erros.append(f"{rel}: noindex numa página indexável — some do Google")
    # og:image: largura e altura declaradas juntas e iguais às do arquivo (D16)
    larg, alt_img = c.meta.get("og:image:width", []), c.meta.get("og:image:height", [])
    imagem = (c.meta.get("og:image") or [""])[0]
    if bool(larg) != bool(alt_img) or len(larg) > 1 or len(alt_img) > 1:
        erros.append(f"{rel}: og:image:width {larg} e og:image:height {alt_img} — os dois juntos, uma vez, ou nenhum")
    elif larg and imagem.startswith(SITE) and os.path.isfile(p(imagem[len(SITE):])):
        real = dimensoes(p(imagem[len(SITE):]))
        if real is None:
            erros.append(f"{rel}: og:image {imagem} não é PNG nem JPEG legível — não dá para conferir width/height")
        elif (larg[0], alt_img[0]) != (str(real[0]), str(real[1])):
            erros.append(f"{rel}: og:image:width×height {larg[0]}×{alt_img[0]} ≠ tamanho real de {imagem} ({real[0]}×{real[1]})")

# robots.txt e sitemap.xml: endpoints do Astro (ADR-005 §1), nunca public/ (§13 já barra).
ROBOTS = "User-agent: *\nAllow: /\n\nSitemap: https://ghfsoftware.com/sitemap.xml\n"
for fonte in ("src/pages/robots.txt.ts", "src/pages/sitemap.xml.ts"):
    if not os.path.isfile(os.path.join(REPO, fonte)):
        erros.append(f"{fonte}: ausente — robots.txt e sitemap.xml saem de endpoint do Astro (ADR-005)")
if not os.path.isfile(p("robots.txt")):
    erros.append(f"{raiz}/robots.txt ausente")
else:
    robots = ler(p("robots.txt"))
    for n, linha in enumerate(robots.splitlines(), 1):
        if re.match(r"\s*disallow\s*:", linha, re.I):
            erros.append(f"robots.txt:{n}: `{linha.strip()}` — nenhum Disallow (convite, assetlinks e og são lidos por robô)")
    if robots != ROBOTS:
        erros.append(f"robots.txt ≠ o literal do ADR-005 §4: {robots!r}")
NS_SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
NS_XHTML = "{http://www.w3.org/1999/xhtml}"
if not os.path.isfile(p("sitemap.xml")):
    erros.append(f"{raiz}/sitemap.xml ausente")
else:
    try:
        urlset = ET.parse(p("sitemap.xml")).getroot()
    except ET.ParseError as e:
        erros.append(f"sitemap.xml não faz parse: {e}")
        urlset = None
    if urlset is not None and urlset.tag != NS_SM + "urlset":
        erros.append(f"sitemap.xml: raiz {urlset.tag} ≠ {NS_SM}urlset")
    elif urlset is not None:
        esperadas = {url_canonica(r): r for r in INDEXAVEIS}
        locs = []
        for u in urlset.findall(NS_SM + "url"):
            loc = (u.findtext(NS_SM + "loc") or "").strip()
            locs.append(loc)
            rel = esperadas.get(loc)
            if rel is None:
                erros.append(f"sitemap.xml: <loc>{loc}</loc> não é a URL canônica de nenhuma página indexável "
                             f"(convite, 404, URL sem .html ou /en sem barra?)")
                continue
            if not os.path.isfile(p(rel)):
                erros.append(f"sitemap.xml: <loc>{loc}</loc> não existe em {raiz}/ ({rel})")
            alts = sorted((x.get("hreflang"), x.get("href")) for x in u.findall(NS_XHTML + "link"))
            pagina = sorted(cabecas[rel].alternates) if rel in cabecas else None
            if pagina is not None and alts != pagina:
                erros.append(f"sitemap.xml: hreflang de {loc} {alts} ≠ o da página {pagina}")
        repetidas = sorted({x for x in locs if locs.count(x) > 1})
        if repetidas:
            erros.append(f"sitemap.xml: <loc> repetido: {repetidas}")
        faltam = sorted(set(esperadas) - set(locs))
        if faltam:
            erros.append(f"sitemap.xml: faltam páginas indexáveis: {faltam}")

# JSON-LD (ADR-005 §6): o que cada página declara, com as chaves fechadas. Dados de src/i18n/apps.ts.
JSONLD_TIPO = {"index.html": "Organization", "en/index.html": "Organization"}
for app in ("lottoexpert.html", "topowalk.html", "poleposition.html", "eclipsego.html"):
    JSONLD_TIPO[app] = JSONLD_TIPO["en/" + app] = "MobileApplication"
CHAVES_JSONLD = {
    "Organization": {"@context", "@type", "name", "url", "logo"},
    "MobileApplication": {"@context", "@type", "name", "operatingSystem", "applicationCategory", "installUrl", "offers"},
}
# applicationCategory: o enum do Google para SoftwareApplication (nunca o valor cru da Play, `TOOLS`)
CATEGORIAS = {f"{c}Application" for c in (
    "Game", "SocialNetworking", "Travel", "Shopping", "Sports", "Lifestyle", "Business", "Design",
    "Developer", "Driving", "Educational", "Health", "Finance", "Security", "Browser", "Communication",
    "DesktopEnhancement", "Entertainment", "Multimedia", "Home", "Utilities", "Reference")}
OFERTA = {"@type": "Offer", "price": "0", "priceCurrency": "BRL"}
RE_PLAY = re.compile(r"^https://play\.google\.com/store/apps/details\?id=([\w.]+)(?:&|$)")


class BotoesPlay(HTMLParser):
    """`id` de cada `<a href>` para a ficha de um app na Play."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            m = RE_PLAY.match(dict(attrs).get("href") or "")
            if m:
                self.ids.append(m.group(1))


for rel, c in sorted(cabecas.items()):
    objetos = []
    for n, bruto in enumerate(c.jsonld, 1):
        try:
            objetos.append(json.loads(bruto))
        except ValueError as e:
            erros.append(f"{rel}: JSON-LD #{n} não faz parse: {e}")
            continue
        # §5 sobre o texto decodificado: `\u0061` não esconde "maximiza" da régua
        texto = json.dumps(objetos[-1], ensure_ascii=False)
        for padrao in COPY_PROIBIDA:
            for m in re.finditer(padrao, texto, re.I):
                erros.append(f"{rel}: JSON-LD fere jogo responsável (`{padrao}`): …{texto[max(0, m.start() - 40): m.end() + 40]}…")
    tipos = [o.get("@type") if isinstance(o, dict) else type(o).__name__ for o in objetos]
    esperado = [JSONLD_TIPO[rel]] if rel in JSONLD_TIPO else []
    if len(c.jsonld) == len(objetos) and tipos != esperado:
        erros.append(f"{rel}: JSON-LD com @type {tipos} ≠ esperado {esperado}")
    for o in objetos:
        if not isinstance(o, dict) or o.get("@type") not in CHAVES_JSONLD:
            continue
        tipo = o["@type"]
        if set(o) != CHAVES_JSONLD[tipo]:
            erros.append(f"{rel}: {tipo} com chaves {sorted(set(o))} ≠ {sorted(CHAVES_JSONLD[tipo])} "
                         f"(sobrando: {sorted(set(o) - CHAVES_JSONLD[tipo])}, faltando: {sorted(CHAVES_JSONLD[tipo] - set(o))})")
        if o.get("@context") != "https://schema.org":
            erros.append(f"{rel}: {tipo} com @context {o.get('@context')!r} ≠ 'https://schema.org'")
        if tipo == "Organization":
            if o.get("url") != SITE or o.get("name") != "GHF Software":
                erros.append(f"{rel}: Organization com name/url {o.get('name')!r}/{o.get('url')!r} ≠ 'GHF Software'/{SITE!r}")
            logo = o.get("logo", "")
            if not (isinstance(logo, str) and logo.startswith(SITE) and os.path.isfile(p(logo[len(SITE):]))):
                erros.append(f"{rel}: Organization.logo {logo!r} não é URL absoluta de arquivo do site")
            continue
        if o.get("operatingSystem") != "Android":
            erros.append(f"{rel}: MobileApplication.operatingSystem {o.get('operatingSystem')!r} ≠ 'Android'")
        if o.get("applicationCategory") not in CATEGORIAS:
            erros.append(f"{rel}: applicationCategory {o.get('applicationCategory')!r} fora do enum do Google (`UtilitiesApplication`, …)")
        if o.get("offers") != OFERTA:
            erros.append(f"{rel}: offers {o.get('offers')!r} ≠ {OFERTA} (só o download gratuito; preço do Premium nunca)")
        if not isinstance(o.get("name"), str) or not o["name"].strip():
            erros.append(f"{rel}: MobileApplication sem name")
        m = RE_PLAY.match(o.get("installUrl") or "")
        botoes = BotoesPlay()
        botoes.feed(ler(p(rel)))
        ids = set(botoes.ids)
        if not m or o["installUrl"] != f"https://play.google.com/store/apps/details?id={m.group(1)}":
            erros.append(f"{rel}: installUrl {o.get('installUrl')!r} não é `https://play.google.com/store/apps/details?id=<id>`")
        elif ids != {m.group(1)}:
            erros.append(f"{rel}: installUrl com id {m.group(1)} ≠ id do botão da Play da página {sorted(ids)}")

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
