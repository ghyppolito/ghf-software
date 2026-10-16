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
  4. data da página legal, em cada língua dela no mapa (src/i18n/idiomas.json, ADR-007), bate com
     a da fonte — lida sempre da raiz do repositório; fonte ausente é erro. A fonte é o
     `lastUpdated` do front-matter do `.pt.md` de src/content/legal/, que tem de bater com a linha
     do corpo do `.pt.md`; cada tradução `.<código>.md` tem o mesmo `lastUpdated` (regra i) e a
     linha `**<rótulo da língua>**` com a mesma data (mês pelo nome da língua no mapa).
     Proveniência (ADR-004): front-matter só com `lastUpdated`, `origemCommit` e `pendente`; o
     `.pt.md` tem `origemCommit` de 40 hex e não tem `pendente` (tradução atrás do pt); a tradução
     não tem nem um nem outro (regra vii); `ORIGENS` de tools/sync_legal.py cobre exatamente LEGAL. Com o repositório do app presente
     (`$GHF_APPS_DIR` ou `--apps-dir`, padrão `..`): corpo do `.pt.md` igual byte a byte a
     `git show <origemCommit>:<caminho>` (erro), commit inexistente no app (erro), commit fora de
     remoto (aviso), ref padrão com texto diferente (aviso). Sem o repositório (o CI, D15): um aviso
     por repositório, sem erro
  5. copy do LottoExpert respeita jogo responsável (mesma régua do PaywallCopyComplianceTest do app),
     no publicado (PAGINAS_LOTTO) e nas fontes Astro (FONTES_LOTTO)
  6. .well-known/assetlinks.json é JSON válido com o package do LottoExpert
  7. toda página de PUBLICADAS existe em `dist/`; as chaves de `paginas` do mapa mais o convite são
     PUBLICADAS (regra xii); toda língua do mapa gerou a página (regra v); nada em `<código>/` para
     língua fora do mapa da página, e nunca `pt/` (regra vi); nenhum `.html` na raiz do
     repositório (não vai ao ar)
  8. hreflang (no laço do §14): um por língua da página no mapa mais `x-default` (en se houver,
     senão pt), recíprocos; página com uma língua só, ou fora do mapa, sem hreflang (regra viii);
     og:locale da língua da página e um og:locale:alternate por outra língua dela (regra ix)
  9. link interno de toda página vai à página de destino na língua da página; se o destino não a
     tem, en, senão pt (D23), com `hreflang` e `lang` do destino; o link marcado
     `data-troca-idioma="X"` (seletor e faixa) leva à mesma página na língua X, com `hreflang`/
     `lang` de X quando os tem
 10. dicionários de src/i18n/ com as mesmas chaves em todos os blocos de língua, cada bloco de
     língua do mapa, e ui.ts com um bloco por língua do mapa (regra xi)
 11. `dist/` não é mais antigo que as fontes (src/, public/, configs, package.json, fontes de
     LEGAL): sem isso, o check daria verde sobre um build velho
 12. página legal, em cada língua do mapa: um só `<h1`, um só rótulo de data da língua da página,
     nenhuma aspa tipográfica que o `.md` não tenha; link do corpo para o próprio site é caminho a
     partir da raiz (nunca `https://ghfsoftware.com/…`), sem `target`, e em `<código>/` aponta para
     a página na língua quando ela existe; e cada tradução com a mesma contagem de `## `, `### `,
     linhas de tabela, itens de lista, links, crases (`code`) e `---` do `.pt.md`, a mesma
     sequência de níveis `##`/`###` (regra ii), cada `` `token` `` do pt o mesmo número de vezes
     (regra iii) e os SDKs de regras_i18n.SDKS que o pt cita (regra iv)
 13. public/ (copiado byte a byte para dist/, ADR-002 §3): primeiro nível é a lista fechada
     PUBLIC; nenhum `.html` além do convite; nenhum symlink; todo arquivo de public/ igual byte a
     byte ao de dist/.
     O Astro publica o arquivo de public/ no lugar da página gerada que colide com ele, com o build
     verde — sem esta guarda, uma cópia velha de página contratual iria ao ar calada; e o
     `.htmlvalidateignore` da raiz isenta do html-validate só o convite (congelado pelo sha256, D13),
     e `rules` do `.htmlvalidate.json` é exatamente `{"no-inline-style": "off"}`
 14. SEO técnico (WP-11, ADR-005). Toda página de `dist/` está em INDEXAVEIS (as do mapa, em cada língua),
     NOINDEX (a 404) ou CONGELADAS (o convite, o mesmo `.html` de tools/contrato.sha256, isento das
     regras e sem canonical, hreflang, JSON-LD nem meta robots). Fora de CONGELADAS: um só canonical, igual ao og:url e à URL da própria página
     (`/x.html`, `/`, `/en/`); hreflang como no §8; `noindex` (ou `none`) só e sempre nas NOINDEX; og:* e twitter:* completos; og:image
     é arquivo do site (nunca externo) e twitter:image é igual a ele; og:image:width e
     height juntos e iguais ao tamanho real do arquivo (cabeçalho PNG/JPEG lido aqui).
     `robots.txt` igual ao literal ROBOTS (nenhum `Disallow`), gerado por src/pages/robots.txt.ts;
     `sitemap.xml` (src/pages/sitemap.xml.ts) faz parse, seus `<loc>` são exatamente as URLs das
     INDEXAVEIS (sem repetir, cada uma existe em dist/) e cada `<url>` traz os mesmos três hreflang
     da página. JSON-LD: cada `<script type="application/ld+json">` faz `json.loads`; `Organization`
     só nas duas home, `MobileApplication` só nas 8 landings, nenhum nas demais; chaves exatamente
     as permitidas (sem `aggregateRating`, `review`, preço do Premium); `name` e
     `applicationCategory` os da landing (APP_DA_PAGINA, D17); `installUrl` com o mesmo
     `id` do botão da Play da página; o texto do JSON-LD (já decodificado) passa pela régua do §5.
     Título e descrição (WP-21): `<title>` (uma vez, lido com as entidades decodificadas) com no
     máximo TITLE_MAX caracteres e description com no máximo DESCRIPTION_MAX; og:title =
     twitter:title = `<title>` e og:description = twitter:description = description (uma fonte só
     por página); nas INDEXAVEIS, o `<title>` sem ` - ` e com a marca unida por ` — ` (termina em
     ` — GHF Software` ou começa com `GHF Software — `); cada tradução com `<title>` e description
     diferentes dos do pt. O convite (CONGELADAS) fica isento.
 15. Desempenho (WP-12, ADR-006), em toda página de `dist/` fora de CONGELADAS (o convite, D13):
     (a) fonte servida pelo site — nenhuma menção a `fonts.googleapis`/`fonts.gstatic`, e um
         `<link rel="preload" as="font">` para arquivo de `dist/`
     (b) ícone em SVG inline — nenhum recurso de outra origem (`<link href>`, `src`/`srcset` de
         `<script>`, `<img>`, `<source>`, `<iframe>`, `<video>`, `<audio>`, `<embed>`, `url()` de
         CSS inline; o Font Awesome vinha do cdnjs), nenhuma menção a `cdnjs` e nenhuma classe
         `fa-*`; todo `<svg>` com `aria-hidden="true"` ou `role="img"` com `<title>`/`aria-label`
     (c) imagem pelo astro:assets — toda `<img>` com `width` e `height`; nenhuma `<img>` ou
         `<source>` (src ou srcset, absoluto ou relativo à página) nem ícone (`rel` com `icon`)
         apontando para `assets/` da raiz (a cópia de public/ é para URL fixa: og:image, JSON-LD
         e convite); no máximo um `fetchpriority="high"` por página, nunca junto de `loading="lazy"`
 16. sem redirecionamento (ADR-007 §1, regra x): nenhum `location.replace`/`location.assign`/
     `location[.href|.pathname|.search|.hash] =`/`location[`/`navigation.navigate(` nem
     `<meta http-equiv="refresh">` em `.html` ou `.js` de `dist/`, fora do convite (CONGELADAS)
 17. acessibilidade estrutural (WP-22), em toda página de `dist/` fora de CONGELADAS (o Lighthouse
     só mede 9): (a) exatamente um `<main>`; (b) títulos sem salto de nível (`h(n)` → `h(n+2)` é
     erro); (c) `<a>`/`<button>` com `aria-label` e texto visível: as palavras do texto visível
     (sem o que é `aria-hidden`, `sr-only` ou `<svg>`) aparecem em sequência no `aria-label`,
     normalizados como o axe (NFKD, sem acento, sem o que está entre parênteses, minúsculas);
     (d) nenhum `href` com `hl=pt_BR` ou `locale=pt_BR` em página que não é pt

As regras de i18n (i)–(viii), (x)–(xii), a linha de data e o link `data-troca-idioma` são funções
puras de tools/regras_i18n.py, provadas por tools/test_regras_i18n.py (casos de
tools/fixtures/i18n/ e casos em linha).
"""
import glob
import json
import os
import posixpath
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

sys.dont_write_bytecode = True  # importar sync_legal não deixa tools/__pycache__ no repositório
from sync_legal import ORIGENS, RE_SHA, CHAVES, apps_dir_padrao, repo_presente, resolve, mostra, em_remoto, separa  # noqa: E402
import regras_i18n as i18n  # noqa: E402

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

# Línguas de cada página: src/i18n/idiomas.json (ADR-007 §2), o mesmo mapa que o build lê. O
# convite fica fora (formato é do app, uma língua só, congelado). PUBLICADAS não é derivada do mapa:
# é a guarda de que apagar uma linha do JSON não tira a página do ar calada (regra xii, §7).
FORA_DO_MAPA = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]
try:
    MAPA = i18n.carrega_mapa(os.path.join(REPO, "src", "i18n", "idiomas.json"))
except (OSError, ValueError) as e:
    print(f"❌ src/i18n/idiomas.json ilegível ({e}) — sem o mapa de línguas o check não sabe o que conferir")
    sys.exit(1)
erros_mapa = i18n.valida_mapa(MAPA)
if erros_mapa:
    print("❌ " + "\n❌ ".join(erros_mapa))
    sys.exit(1)
IDIOMAS = MAPA["idiomas"]
LINGUAS = MAPA["paginas"]  # caminho pt → línguas, a primeira é pt


def linguas_de(pagina):
    return LINGUAS.get(pagina, ["pt"])


def traducoes(pagina):
    return [l for l in linguas_de(pagina) if l != "pt"]


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
PAGINAS_LOTTO = ["index.html", "lottoexpert.html", "lottoexpert-privacy.html", "lottoexpert-terms.html"]
PAGINAS_LOTTO = ([i18n.arquivo(l, x) for x in PAGINAS_LOTTO for l in linguas_de(x)]
                 + ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"])
# Fontes das páginas do LottoExpert (src/): a régua roda sobre elas, lidas da raiz do repositório,
# sempre que o check roda — além do HTML gerado em dist/ (PAGINAS_LOTTO), que o check exige.
FONTES_LOTTO = ["src/i18n/home.ts", "src/components/Home.astro",
                "src/i18n/lottoexpert.ts", "src/components/LottoExpert.astro",
                "src/i18n/legal.ts", "src/i18n/apps.ts"]
FONTES_LOTTO += [f"src/content/legal/{doc}.{l}.md" for doc in ("lottoexpert-privacy", "lottoexpert-terms")
                 for l in linguas_de(doc + ".html")]

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
                  + [md[: -len(".pt.md")] + f".{l}.md" for pg, md in LEGAL.items() for l in traducoes(pg)])
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
    ano_ref, mes_ref = ref[2], MESES_NUM.index(ref[1]) + 1
    # Traduções (regra i e linha de data no rótulo da língua, mês pelo nome do mapa)
    for lang in traducoes(pagina):
        md_l = md[: -len(".pt.md")] + f".{lang}.md"
        if not os.path.exists(os.path.join(REPO, md_l)):
            erros.append(f"{md_l}: tradução ausente ({pagina} tem `{lang}` no mapa)")
            continue
        _, corpo_l = front_matter(md_l, ler_md(os.path.join(REPO, md_l)))
        erros.extend(i18n.regra_linha_data(md_l, corpo_l, IDIOMAS[lang]["rotuloData"], IDIOMAS[lang]["meses"],
                                           ano_ref, mes_ref, ref[0]))
    ref_txt = " de ".join(x for x in ref if x)
    # Cada página da língua do mapa: a data de toda língua que aparecer bate; a da página é obrigatória.
    for lang in linguas_de(pagina):
        alvo = i18n.arquivo(lang, pagina)
        if not os.path.exists(p(alvo)):
            continue  # ausência já é erro no §1 (pt) ou no §7 (regra v)
        html = ler(p(alvo))
        for outra, dados in IDIOMAS.items():
            # texto sem tags e HTML cru (atributo `content="…"`); trecho com marcação é descartado
            frags = list(dict.fromkeys(i18n.fragmentos_data(sem_tags(html), dados["rotuloData"])
                                       + i18n.fragmentos_data(html, dados["rotuloData"])))
            for frag in frags:
                if not i18n.confere_data(frag, dados["meses"], ano_ref, mes_ref, ref[0]):
                    erros.append(f"{alvo}: data {outra} `{frag.strip()}` ≠ {md} `{ref_txt}`")
            if outra == lang and not frags:
                erros.append(f"{alvo}: nenhuma `{dados['rotuloData']}` encontrada")

# Proveniência (ADR-004). Sempre (inclusive no CI): formato do front-matter, origemCommit no pt,
# `pendente` como erro e nada disso na tradução (regra vii), a mesma data em todas (regra i),
# ORIGENS = LEGAL. Com o repositório do app presente:
# o corpo do pt é o `git show` do commit registrado, byte a byte (lido em binário: CRLF, BOM e
# newline final contam).
docs_legal = {os.path.basename(md)[: -len(".pt.md")] for md in LEGAL.values()}
if set(ORIGENS) != docs_legal:
    erros.append(f"ORIGENS de tools/sync_legal.py ≠ LEGAL do check_site.py: só em ORIGENS "
                 f"{sorted(set(ORIGENS) - docs_legal)}, só em LEGAL {sorted(docs_legal - set(ORIGENS))}")
ausentes = set()
for md in LEGAL.values():
    doc = os.path.basename(md)[: -len(".pt.md")]
    pagina = os.path.basename(md)[: -len(".pt.md")] + ".html"
    fms = {}
    for lang in linguas_de(pagina):
        lado = md[: -len(".pt.md")] + f".{lang}.md"
        if not os.path.exists(os.path.join(REPO, lado)):
            continue  # ausência já é erro acima
        with open(os.path.join(REPO, lado), "rb") as f:
            fm, chaves, corpo_b = separa(f.read())
        if fm is None:
            erros.append(f"{lado}: front-matter fora do formato `---\\n…\\n---\\n` em LF — rode tools/sync_legal.py")
            continue
        fms[lang] = fm
        estranhas = [k for k in chaves if k not in CHAVES or fm[k] is None]
        if estranhas or len(chaves) != len(set(chaves)):
            erros.append(f"{lado}: front-matter com chave fora de {{{', '.join(CHAVES)}}}, sem aspas ou repetida: {chaves}")
        if lang != "pt":
            continue
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
    if "pt" in fms:
        erros.extend(i18n.regra_datas(doc, {l: fm.get("lastUpdated") for l, fm in fms.items()}))
        erros.extend(i18n.regra_front_matter(doc, fms))

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
# Lista fixa (PUBLICADAS), não o glob da raiz nem o mapa: página que não chega ao publicado sai do
# ar sem nenhum outro check perceber (os links não a citam). O mapa tem de bater com ela (regra
# xii); toda língua do mapa gerou a página (v); nenhuma pasta de língua fora do mapa, nem `pt/` (vi).
erros.extend(i18n.regra_guarda(MAPA, PUBLICADAS, FORA_DO_MAPA))
for rel in PUBLICADAS:
    if not os.path.exists(p(rel)):
        erros.append(f"página publicada ausente em {raiz} — falta em src/pages/?: {rel}")
arquivos_dist = set()
for pasta, _, arqs in os.walk(raiz):
    for nome in arqs:
        arquivos_dist.add(os.path.relpath(os.path.join(pasta, nome), raiz).replace(os.sep, "/"))
erros.extend(i18n.regra_arquivos_gerados(MAPA, arquivos_dist))
erros.extend(i18n.regra_linguas_fora_do_mapa(MAPA, arquivos_dist))
# Página .html na raiz do repositório não vai ao ar (o Astro publica src/pages/ e public/): página
# nasce em src/pages/.
for c in sorted(glob.glob(os.path.join(REPO, "*.html"))):
    erros.append(f"{os.path.basename(c)} na raiz do repositório — não vai ao ar; página nasce em src/pages/")

# ------------------------------------------------------------ 8: hreflang
# Regras viii e ix: rodam no laço do §14, que já lê o <head> de cada página.

# ------------------------------------------------------------ 9: a língua aponta para a língua
# Link interno de qualquer página vai à página de destino na língua dela; se o destino não existe
# nessa língua, en, senão pt (D23), com `hreflang`/`lang` do destino (regras_i18n.regra_link). O
# link marcado `data-troca-idioma="X"` (seletor e faixa) tem a regra dele: a mesma página em X.
for caminho in paginas:
    rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
    base = os.path.dirname(caminho)
    for tag in re.findall(r"<a\b[^>]*>", ler(caminho), re.I):
        href = re.search(r'\shref="([^"#?]*)[^"]*"', tag)
        if not href:
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
        erros.extend(i18n.regra_link(MAPA, rel, href.group(1), destino, tag))

# ------------------------------------------------------------ 10: dicionários
# O `satisfies` dos dicionários em src/i18n/ aceita bloco com chaves a menos e o build não roda
# checagem de tipos: chave só em pt sairia vazia na tradução sem erro. Lido do repositório, como §5.
for ts in sorted(glob.glob(os.path.join(REPO, "src/i18n/*.ts"))):
    nome = os.path.relpath(ts, REPO)
    erros.extend(i18n.regra_dicionario(nome, ler(ts), MAPA, eh_ui=os.path.basename(ts) == "ui.ts"))

# ------------------------------------------------------------ 12: página legal
# O que o plugin omiteCabecalhoLegal e o `smartPunctuation: false` do astro.config.mjs garantem,
# provado no publicado: título e data aparecem uma vez (no hero), as aspas são as do .md do app; e
# cada tradução tem a mesma estrutura do .pt.md (seção, tabela, token ou SDK perdido na tradução).
TIPOGRAFICAS = "“”‘’"
for pagina, md in LEGAL.items():
    base_md = md[: -len(".pt.md")]
    fontes_md = {lang: os.path.join(REPO, f"{base_md}.{lang}.md") for lang in linguas_de(pagina)}
    if not all(os.path.exists(f) for f in fontes_md.values()):
        continue  # ausência já é erro no §4
    texto_md = {lang: ler(f) for lang, f in fontes_md.items()}
    for lang in linguas_de(pagina):
        alvo = i18n.arquivo(lang, pagina)
        if not os.path.exists(p(alvo)):
            continue  # ausência já é erro no §1/§4/§7
        html = ler(p(alvo))
        n_h1 = len(re.findall(r"<h1\b", html, re.I))
        if n_h1 != 1:
            erros.append(f"{alvo}: {n_h1} `<h1` (esperado 1 — o `# título` do .md não pode sair no corpo)")
        # o rótulo com dois-pontos: o texto pode citar a data pelo nome (TopoWalk, seção 12: `A data
        # de "Última atualização" no topo…`)
        rotulo = IDIOMAS[lang]["rotuloData"]
        n_rot = sem_tags(html).count(rotulo)
        if n_rot != 1:
            erros.append(f"{alvo}: {n_rot} rótulo(s) `{rotulo}` no texto (esperado 1 — a linha de data do .md não pode sair no corpo)")
        for ch in TIPOGRAFICAS:
            if html.count(ch) > texto_md[lang].count(ch):
                erros.append(f"{alvo}: aspa tipográfica `{ch}` ({html.count(ch)}×) além das de {base_md}.{lang}.md "
                             f"({texto_md[lang].count(ch)}×) — smartPunctuation ligado?")
        # Link do corpo para o próprio site (o `.md` do app escreve `https://ghfsoftware.com/x.html`):
        # o plugin linksInternosLegais de src/markdown/legal.mjs o torna `/x.html` (`/en/x.html` no
        # en, só para página `.html` — asset e o convite `lotto-expert/…` não têm par), na mesma aba,
        # como a página antiga. O host vale com ou sem `www.`, por http ou https. URL absoluta sai do ar com o domínio de teste,
        # abre outra aba e, em `<código>/`, leva ao pt.
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
                par = lang != "pt" and lang in LINGUAS.get(arq, [])
                erros.append(f"{alvo}: link legal para o próprio site com URL absoluta ({h}) — esperado `/{lang + '/' if par else ''}{resto}` (plugin linksInternosLegais desligado?)")
            elif h.startswith("/"):
                if re.search(r"\btarget=", tag):
                    erros.append(f"{alvo}: link legal para o próprio site com target (abre outra aba): {tag}")
                destino = h.lstrip("/").split("#")[0].split("?")[0] or "index.html"
                if lang != "pt" and lang in LINGUAS.get(destino, []):
                    erros.append(f"{alvo}: link legal {h} leva ao pt; a página em {lang} é /{lang}/{destino}")
    for nome, padrao in (("`## `", r"^## "), ("`### `", r"^### "), ("linhas de tabela `|`", r"^\|"),
                         ("itens de lista", r"^\s*([-*]|\d+\.) "), ("links `](`", r"\]\("),
                         ("crases `` ` `` (code)", r"`"), ("`---`", r"^---$")):
        # o `---` do front-matter conta igual nos dois lados
        n = {lang: len(re.findall(padrao, texto, re.M)) for lang, texto in texto_md.items()}
        for lang in traducoes(pagina):
            if n[lang] != n["pt"]:
                erros.append(f"{base_md}.{lang}.md: {n[lang]} {nome} ≠ {n['pt']} do .pt.md — tradução com estrutura diferente")
    doc = os.path.basename(base_md)
    erros.extend(i18n.regra_titulos(doc, texto_md))
    erros.extend(i18n.regra_tokens(doc, texto_md))
    erros.extend(i18n.regra_sdks(doc, texto_md))

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
INDEXAVEIS = [i18n.arquivo(l, x) for x, linguas in LINGUAS.items() for l in linguas]
NOINDEX = ["404.html"]
# Cabe no resultado de busca sem corte (title) e no snippet (description) — WP-21
TITLE_MAX = 60
DESCRIPTION_MAX = 160
MARCA = "GHF Software"
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
    """Lê canonical, hreflang, meta (property/name), o texto de cada `<title>` e o de cada
    `<script type=application/ld+json>`. O `<title>` de dentro de um `<svg>` (dica do ícone,
    components/Icon.astro) não é título da página e fica de fora."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicas, self.alternates, self.meta, self.jsonld, self.titulos = [], [], {}, [], []
        self._ld = None
        self._titulo = None
        self._svg = 0

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "svg":
            self._svg += 1
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
        elif tag == "title" and not self._svg:
            self._titulo = []

    def handle_startendtag(self, tag, attrs):
        if tag != "svg":  # `<svg/>` vazio não abre nível
            self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)
        if self._titulo is not None:
            self._titulo.append(data)

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg:
            self._svg -= 1
        if tag == "script" and self._ld is not None:
            self.jsonld.append("".join(self._ld))
            self._ld = None
        elif tag == "title" and self._titulo is not None:
            self.titulos.append("".join(self._titulo))
            self._titulo = None


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
        # isenta das regras, mas sem marcação de SEO (ADR-005 §5): canonical, hreflang, JSON-LD ou
        # noindex no convite seriam edição do arquivo congelado — o sha256 também pega, o check diz o quê
        c = Cabeca()
        c.feed(ler(caminho))
        c.close()
        marcas = ((["canonical"] if c.canonicas else []) + (["hreflang"] if c.alternates else [])
                  + (["JSON-LD"] if c.jsonld else []) + (["meta robots"] if c.meta.get("robots") else []))
        if marcas:
            erros.append(f"{rel}: {', '.join(marcas)} na página congelada — o convite fica fora de toda regra de SEO (D13)")
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
    # título e descrição (WP-21): o cartão de compartilhamento repete o <title> e a description, sem
    # texto próprio; os dois cabem na SERP; nas INDEXAVEIS, a marca vem unida por travessão, o do h1
    titulo = c.titulos[0] if len(c.titulos) == 1 else None
    descricao = (c.meta.get("description") or [None])[0]
    if len(c.meta.get("description", [])) > 1:
        erros.append(f"{rel}: {len(c.meta['description'])} <meta name=\"description\"> (esperado 1)")
    if titulo is None:
        erros.append(f"{rel}: {len(c.titulos)} <title> (esperado 1)")
    else:
        if len(titulo) > TITLE_MAX:
            erros.append(f"{rel}: <title> com {len(titulo)} caracteres (máximo {TITLE_MAX}): {titulo!r}")
        if c.meta.get("og:title", [None])[0] != titulo:
            erros.append(f"{rel}: og:title {c.meta.get('og:title')} ≠ <title> {titulo!r}")
        if rel in INDEXAVEIS:
            if " - " in titulo:
                erros.append(f"{rel}: <title> com ' - ' — o separador é ' — ', o do h1: {titulo!r}")
            if not (titulo.endswith(" — " + MARCA) or titulo.startswith(MARCA + " — ")):
                erros.append(f"{rel}: <title> sem a marca unida por travessão ('… — {MARCA}' ou '{MARCA} — …'): {titulo!r}")
    if c.meta.get("twitter:title") != c.meta.get("og:title"):
        erros.append(f"{rel}: twitter:title {c.meta.get('twitter:title')} ≠ og:title {c.meta.get('og:title')}")
    if descricao is not None:
        if len(descricao) > DESCRIPTION_MAX:
            erros.append(f"{rel}: description com {len(descricao)} caracteres (máximo {DESCRIPTION_MAX}): {descricao!r}")
        if c.meta.get("og:description", [None])[0] != descricao:
            erros.append(f"{rel}: og:description {c.meta.get('og:description')} ≠ description {descricao!r}")
    if c.meta.get("twitter:description") != c.meta.get("og:description"):
        erros.append(f"{rel}: twitter:description {c.meta.get('twitter:description')} ≠ og:description {c.meta.get('og:description')}")
    # §8. hreflang (regra viii): um por língua da página no mapa e x-default (en se houver, senão pt,
    # D8/D18), recíprocos — cada língua declara os mesmos endereços, porque todas apontam para as
    # URLs que o mapa dá. Página com uma língua só, ou fora do mapa (a 404), não declara.
    erros.extend(i18n.regra_hreflang(MAPA, rel, c.alternates, SITE))
    # og:locale da língua e um og:locale:alternate por outra língua da página (regra ix)
    lang_pag, pt_rel = i18n.pagina_de(rel)
    esperado_alt = sorted(IDIOMAS[l]["ogLocale"] for l in linguas_de(pt_rel) if l != lang_pag)
    if c.meta.get("og:locale", [None])[:1] != [IDIOMAS[lang_pag]["ogLocale"]]:
        erros.append(f"{rel}: og:locale {c.meta.get('og:locale')} ≠ {IDIOMAS[lang_pag]['ogLocale']!r} (regra ix)")
    if sorted(c.meta.get("og:locale:alternate", [])) != esperado_alt:
        erros.append(f"{rel}: og:locale:alternate {c.meta.get('og:locale:alternate', [])} ≠ {esperado_alt} (regra ix)")
    # indexação: `noindex` só e sempre nas NOINDEX
    # `none` = `noindex, nofollow` para o Google: conta como noindex
    tem_noindex = any(re.search(r"\b(noindex|none)\b", v, re.I) for k in ("robots", "googlebot") for v in c.meta.get(k, []))
    if rel in NOINDEX and not tem_noindex:
        erros.append(f"{rel}: sem <meta name=\"robots\" content=\"noindex\"> (está em NOINDEX)")
    if rel not in NOINDEX and tem_noindex:
        erros.append(f"{rel}: noindex numa página indexável — some do Google")
    # og:image: largura e altura declaradas juntas e iguais às do arquivo (D16)
    larg, alt_img = c.meta.get("og:image:width", []), c.meta.get("og:image:height", [])
    imagem = (c.meta.get("og:image") or [""])[0]
    if imagem and not (imagem.startswith(SITE) and os.path.isfile(p(imagem[len(SITE):]))):
        erros.append(f"{rel}: og:image {imagem} não é URL absoluta de arquivo do site ({SITE}…)")
    tw_imagem = c.meta.get("twitter:image", [])
    if tw_imagem and tw_imagem[:1] != [imagem]:
        erros.append(f"{rel}: twitter:image {tw_imagem} ≠ og:image {imagem!r}")
    if bool(larg) != bool(alt_img) or len(larg) > 1 or len(alt_img) > 1:
        erros.append(f"{rel}: og:image:width {larg} e og:image:height {alt_img} — os dois juntos, uma vez, ou nenhum")
    elif larg and imagem.startswith(SITE) and os.path.isfile(p(imagem[len(SITE):])):
        real = dimensoes(p(imagem[len(SITE):]))
        if real is None:
            erros.append(f"{rel}: og:image {imagem} não é PNG nem JPEG legível — não dá para conferir width/height")
        elif (larg[0], alt_img[0]) != (str(real[0]), str(real[1])):
            erros.append(f"{rel}: og:image:width×height {larg[0]}×{alt_img[0]} ≠ tamanho real de {imagem} ({real[0]}×{real[1]})")

# tradução com o mesmo <title> ou a mesma description do pt: texto herdado, não traduzido (WP-21);
# compara sem caixa e com espaços normalizados, para um espaço a mais não valer como tradução
def _norm(textos):
    return [" ".join(t.split()).casefold() for t in textos]

for pt_rel in LINGUAS:
    for lang in traducoes(pt_rel):
        tr = i18n.arquivo(lang, pt_rel)
        a, b = cabecas.get(pt_rel), cabecas.get(tr)
        if a is None or b is None:
            continue
        if a.titulos and _norm(a.titulos) == _norm(b.titulos):
            erros.append(f"{tr}: <title> igual ao do pt {a.titulos[0]!r}")
        if a.meta.get("description") and _norm(a.meta["description"]) == _norm(b.meta.get("description", [])):
            erros.append(f"{tr}: description igual à do pt {a.meta['description'][0]!r}")

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
JSONLD_TIPO = {i18n.arquivo(l, "index.html"): "Organization" for l in linguas_de("index.html")}
for app in ("lottoexpert.html", "topowalk.html", "poleposition.html", "eclipsego.html"):
    for l in linguas_de(app):
        JSONLD_TIPO[i18n.arquivo(l, app)] = "MobileApplication"
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
# app de cada landing (D17): name e applicationCategory esperados — espelho de src/i18n/apps.ts,
# declarado aqui para que um dado trocado lá (ou uma landing lendo a chave errada) não passe
APP_DA_PAGINA = {}
for pagina, nome, categoria in (
    ("lottoexpert.html", "LottoExpert", "UtilitiesApplication"),
    ("topowalk.html", "TopoWalk", "UtilitiesApplication"),
    ("poleposition.html", "Pole Position", "SportsApplication"),
    ("eclipsego.html", "EclipseGo", "LifestyleApplication"),
):
    for l in linguas_de(pagina):
        APP_DA_PAGINA[i18n.arquivo(l, pagina)] = (nome, categoria)
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
        if rel in APP_DA_PAGINA and (o.get("name"), o.get("applicationCategory")) != APP_DA_PAGINA[rel]:
            erros.append(f"{rel}: MobileApplication name/applicationCategory {o.get('name')!r}/{o.get('applicationCategory')!r} "
                         f"≠ {APP_DA_PAGINA[rel][0]!r}/{APP_DA_PAGINA[rel][1]!r} (D17)")
        m = RE_PLAY.match(o.get("installUrl") or "")
        botoes = BotoesPlay()
        botoes.feed(ler(p(rel)))
        ids = set(botoes.ids)
        if not m or o["installUrl"] != f"https://play.google.com/store/apps/details?id={m.group(1)}":
            erros.append(f"{rel}: installUrl {o.get('installUrl')!r} não é `https://play.google.com/store/apps/details?id=<id>`")
        elif ids != {m.group(1)}:
            erros.append(f"{rel}: installUrl com id {m.group(1)} ≠ id do botão da Play da página {sorted(ids)}")

# ------------------------------------------------------------ 15: desempenho
# WP-12, ADR-006. O convite fica fora (CONGELADAS, D13): ele ainda carrega Inter do Google e o pako
# do cdnjs, e só muda num WP que aceite novo tools/contrato.sha256.
RE_FONTE_GOOGLE = re.compile(r"fonts\.(googleapis|gstatic)\.com", re.I)


def urls_srcset(v):
    return [c.strip().split()[0] for c in v.split(",") if c.strip()]


class Recursos(HTMLParser):
    """`href` de cada `<link rel=preload as=font>`; recursos de outra origem; classes `fa-*`; cada
    `<img>` e `<source>` (atributos); `href` dos `<link>` de ícone; quantos `fetchpriority=high`
    e quantos deles com `loading=lazy`; `<svg>` sem nome acessível nem `aria-hidden`."""

    COM_SRC = ("script", "img", "source", "iframe", "video", "audio", "embed")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.preload_fonte, self.externos, self.classes_fa = [], [], []
        self.imgs, self.icones, self.prioridade_alta, self.alta_lazy = [], [], 0, 0
        self.svgs, self.svgs_sem_nome = [], 0

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "link" and "preload" in d.get("rel", "").lower().split() and d.get("as", "").lower() == "font":
            self.preload_fonte.append(d.get("href", ""))
        urls = [d.get("href", "")] if tag == "link" else []
        if tag in self.COM_SRC:
            urls += [d.get("src", "")] + urls_srcset(d.get("srcset", ""))
        urls += re.findall(r"url\(\s*['\"]?([^'\")\s]+)", d.get("style", ""))
        # canonical e hreflang são do próprio site (SITE); qualquer outro absoluto é terceiro
        for url in urls:
            if re.match(r"^(https?:)?//", url, re.I) and not url.startswith(SITE):
                self.externos.append(f"<{tag}> {url}")
        self.classes_fa += [c for c in d.get("class", "").split() if c.startswith("fa-") or c in ("fa", "fas", "fab", "far")]
        if tag in ("img", "source"):
            self.imgs.append((tag, d))
        if tag == "link" and any("icon" in r for r in d.get("rel", "").lower().split()):
            self.icones.append(d.get("href", ""))
        if d.get("fetchpriority", "").lower() == "high":
            self.prioridade_alta += 1
            if d.get("loading", "").lower() == "lazy":
                self.alta_lazy += 1
        # <svg> decorativo é aria-hidden; o que tem sentido é role=img com <title> ou aria-label
        # (components/Icon.astro). O nome só se sabe no </svg>: o <title> é filho.
        if tag == "svg":
            oculto = d.get("aria-hidden", "").lower() == "true"
            self.svgs.append(oculto or (d.get("role") == "img" and bool(d.get("aria-label", "").strip())))
        elif tag == "title" and self.svgs:
            self.svgs[-1] = self.svgs[-1] or "titulo"

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "svg":
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "svg" and self.svgs:
            if not self.svgs.pop():
                self.svgs_sem_nome += 1


for caminho in paginas:
    rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
    if rel in CONGELADAS:
        continue
    html = ler(caminho)
    r = Recursos()
    r.feed(html)
    # (a) a Inter é do site (astro.config.mjs, `fonts`): Google Fonts bloqueava o render (~830 ms)
    m = RE_FONTE_GOOGLE.search(html)
    if m:
        erros.append(f"{rel}: {m.group(0)} — a fonte é servida pelo site (ADR-006 §3), sem Google Fonts")
    if not r.preload_fonte:
        erros.append(f"{rel}: sem <link rel=\"preload\" as=\"font\"> — o <Font preload> do Base.astro sumiu")
    for href in r.preload_fonte:
        if not href.startswith("/") or href.startswith("//") or not os.path.isfile(p(href.lstrip("/"))):
            erros.append(f"{rel}: preload de fonte {href!r} não é arquivo de {raiz}/")
    # (b) nada de terceiro no carregamento da página; ícone é <svg> do components/Icon.astro
    for x in r.externos:
        erros.append(f"{rel}: {x} — recurso de outra origem (ADR-006 §5: nenhum terceiro em página gerada)")
    if re.search(r"cdnjs", html, re.I):
        erros.append(f"{rel}: menciona cdnjs — o Font Awesome saiu (ADR-006 §4)")
    if r.classes_fa:
        erros.append(f"{rel}: classe(s) do Font Awesome {sorted(set(r.classes_fa))} — ícone é <Icon> (SVG inline, ADR-006 §4)")
    if r.svgs_sem_nome:
        erros.append(f"{rel}: {r.svgs_sem_nome} <svg> sem aria-hidden=\"true\" nem role=\"img\" com <title>/aria-label — use <Icon> (ADR-006 §4)")
    # (c) <img> sai do <Image>/getImage() do astro:assets: WebP com o tamanho de exibição, width e
    # height (sem salto de layout) e nunca o PNG/JPEG de public/assets/ (até 736 KB cada)
    def de_public_assets(u):
        # absoluto (`/assets/x`, `https://…/assets/x`) ou relativo à página (`assets/x`, `../assets/x`)
        u = re.sub(r"^https?://[^/]+", "", u.split("#")[0].split("?")[0])
        if not u or re.match(r"^[a-z][a-z0-9+.-]*:", u, re.I):
            return False
        alvo = u.lstrip("/") if u.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(rel), u))
        return alvo.startswith("assets/")
    for tag, d in r.imgs:
        nome = d.get("src") or d.get("srcset") or "?"
        if tag == "img" and not (d.get("width", "").strip() and d.get("height", "").strip()):
            erros.append(f"{rel}: <img {nome}> sem width e height — use <Image> de astro:assets (ADR-006 §1)")
        for u in [d.get("src", "")] + urls_srcset(d.get("srcset", "")):
            if de_public_assets(u):
                erros.append(f"{rel}: <{tag}> com {u} — imagem exibida sai de src/assets/img/ pelo astro:assets, não de public/assets/ (ADR-006 §2)")
    for href in r.icones:
        if de_public_assets(href):
            erros.append(f"{rel}: ícone {href} — sai do getImage() do Base.astro (48 px), não de public/assets/ (ADR-006 §1)")
    if r.prioridade_alta > 1:
        erros.append(f"{rel}: {r.prioridade_alta} elementos com fetchpriority=\"high\" — no máximo um, o LCP medido (ADR-006 §1)")
    if r.alta_lazy:
        erros.append(f"{rel}: fetchpriority=\"high\" junto de loading=\"lazy\" — o LCP não pode esperar o lazy (ADR-006 §1)")

# ------------------------------------------------------------ 16: sem redirecionamento
# ADR-007 §1, regra x: a língua nunca muda sozinha — nem por script, nem por <meta refresh>. O
# convite (CONGELADAS) fica fora: é congelado byte a byte (D13).
# A expressão (com fronteira de palavra: `geolocation=` passa) é regras_i18n.RE_REDIRECT, provada
# forma a forma em tools/test_regras_i18n.py.
for rel in sorted(arquivos_dist):
    if rel in CONGELADAS or not rel.endswith((".html", ".js")):
        continue
    for trecho in i18n.redirecionamentos(ler(p(rel))):
        erros.append(f"{rel}: `{trecho}` — nada redireciona no site; a sugestão de língua é um link (ADR-007 §1/§7)")

# ------------------------------------------------------------ 17: acessibilidade estrutural
# WP-22. O Lighthouse do CI mede 9 páginas; isto vale para todas as de dist/ fora do convite
# (CONGELADAS, D13). Landmark, ordem de títulos, nome acessível que contém o rótulo visível (WCAG
# 2.5.3, como o `label-content-name-mismatch` do axe) e link para loja/rede social forçado em pt
# numa página de outra língua.
RE_LINK_PT = re.compile(r"[?&](?:amp;)?(hl|locale)=pt(?:[_-]BR)?\b", re.I)


def palavras_axe(texto):
    """Palavras como o axe as compara (`curateTokens`): NFKD, sem acento nem pontuação, sem o que
    está entre parênteses, minúsculas. `English (EN)` → ["english"]: o `EN` some."""
    texto = unicodedata.normalize("NFKD", texto)
    anterior = None
    while anterior != texto:
        anterior, texto = texto, re.sub(r"\([^()]*\)", "", texto)
    texto = "".join(" " if unicodedata.category(c)[0] not in "LN" else c for c in texto)
    return texto.lower().split()


def contem_em_sequencia(nome, rotulo):
    return any(nome[i:i + len(rotulo)] == rotulo for i in range(len(nome) - len(rotulo) + 1))


class Estrutura(HTMLParser):
    """Quantos `<main>`; níveis dos títulos na ordem; (aria-label, texto visível) de cada `<a>` e
    `<button>` com `aria-label`."""

    VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.mains, self.titulos, self.rotulos = 0, [], []
        self.pilha = []  # (tag, oculto) de cada elemento aberto
        self.abertos = []  # [tag, aria-label, texto visível, profundidade]

    def oculto(self):
        return bool(self.pilha) and self.pilha[-1][1]

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "main":
            self.mains += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.titulos.append(int(tag[1]))
        if tag in self.VAZIOS:
            return
        esconde = (self.oculto() or tag in ("svg", "script", "style", "template")
                   or d.get("aria-hidden", "").lower() == "true" or "sr-only" in d.get("class", "").split())
        self.pilha.append((tag, esconde))
        if tag in ("a", "button") and d.get("aria-label", "").strip():
            self.abertos.append([tag, d["aria-label"], "", len(self.pilha)])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VAZIOS:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.oculto():
            for a in self.abertos:
                a[2] += data

    def handle_endtag(self, tag):
        # fecha-tag sem par (um </p> que o HTML fechou implícito) não esvazia a pilha
        if tag not in (aberto for aberto, _ in self.pilha):
            return
        while self.pilha:
            aberto, _ = self.pilha.pop()
            if self.abertos and self.abertos[-1][3] == len(self.pilha) + 1:
                self.rotulos.append(tuple(self.abertos.pop()[:3]))
            if aberto == tag:
                break


for caminho in paginas:
    rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
    if rel in CONGELADAS:
        continue
    html = ler(caminho)
    e = Estrutura()
    e.feed(html)
    # (a) um <main> por página: o Lighthouse `landmark-one-main`; dois seria componente com <main>
    # dentro de página que já o tem. Conta só a tag: o site não usa `role="main"`
    if e.mains != 1:
        erros.append(f"{rel}: {e.mains} <main> — toda página tem exatamente um (WP-22)")
    # (b) título sem pular nível na descida (Lighthouse `heading-order`); subir pode pular
    for antes, depois in zip(e.titulos, e.titulos[1:]):
        if depois > antes + 1:
            erros.append(f"{rel}: <h{depois}> logo depois de <h{antes}> — título pula nível (WP-22)")
            break
    # (c) nome acessível contém o texto visível, palavra por palavra (WCAG 2.5.3)
    for tag, rotulo, visivel in e.rotulos:
        v = palavras_axe(visivel)
        if v and not contem_em_sequencia(palavras_axe(rotulo), v):
            erros.append(f"{rel}: <{tag} aria-label=\"{rotulo}\"> com texto visível {visivel.strip()!r}"
                         " — o nome acessível tem de conter o texto visível, fora de parênteses (WCAG 2.5.3, WP-22)")
    # (d) quem lê em outra língua não cai na loja ou na rede social forçada em pt
    if i18n.pagina_de(rel)[0] != "pt":
        for href in re.findall(r'\shref="([^"]*)"', html):
            if RE_LINK_PT.search(href):
                erros.append(f"{rel}: {href} — link com a língua fixa em pt numa página que não é pt (WP-22)")

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
