#!/usr/bin/env python3
"""Regras de i18n do site (WP-15, ADR-007) como funções puras.

Só biblioteca padrão, de propósito. Nenhuma função aqui lê disco além de `carrega_mapa`: cada uma
recebe o mapa (`src/i18n/idiomas.json`), os textos e a lista de arquivos, e devolve a lista de
erros (vazia = passou). O `check_site.py` as chama sobre o site real; o
`tools/test_regras_i18n.py` as chama sobre os casos de `tools/fixtures/i18n/`, porque um `dist/`
sintético inteiro esbarraria nas regras do check que leem `src/` da raiz.

Regras (numeração do veredito do WP-15):
  (i)    mesmo `lastUpdated` em todas as línguas de uma página legal
  (ii)   mesma sequência de níveis `##`/`###` (pré-condição das âncoras por posição, ADR-007 §6)
  (iii)  cada `` `token` `` do pt aparece o mesmo número de vezes em cada tradução
  (iv)   cada SDK de SDKS que aparece no pt aparece em cada tradução
  (v)    toda língua do mapa gerou o arquivo da página
  (vi)   nenhum arquivo em `<código>/` para língua fora do mapa da página; nunca `pt/`
  (vii)  sem `pendente` no front-matter; tradução sem `origemCommit` nem `pendente` (ADR-004)
  (viii) hreflang: um por língua mais `x-default` (en se houver, senão pt); página com uma língua
         só não tem hreflang
  (§9)   link interno vai à página na língua da página; se o destino não a tem, en, senão pt (D23),
         com `hreflang` e `lang` do destino quando ele está em outra língua; o link
         `data-troca-idioma="X"` leva à mesma página em X
  (x)    nada redireciona: `location.replace/assign(`, `location[.href|.pathname|.search|.hash] =`,
         `location[`, `navigation.navigate(`, `<meta http-equiv="refresh">`
  (xi)   cada dicionário de src/i18n/*.ts com as mesmas chaves em todos os blocos de língua, e
         ui.ts com um bloco para cada língua do mapa
  (xii)  chaves de `paginas` mais as páginas fora do mapa (o convite) = PUBLICADAS
"""
import collections
import json
import re

# Nomes de SDK que a tradução não pode perder (regra iv). "Google" sozinho cobre "Google Play
# Services", "Termos do Google" e afins: some numa tradução só se o trecho inteiro sumiu.
SDKS = ["Firebase Analytics", "Firebase Crashlytics", "Google Play Billing", "Cloud Firestore", "Google"]
CAMPOS_IDIOMA = ("hreflang", "ogLocale", "nome", "rotuloData", "meses")
# Pasta de primeiro nível de dist/ que é língua: duas letras minúsculas (ISO 639-1, ADR-007 §1).
RE_PASTA_LINGUA = re.compile(r"^[a-z]{2}$")
RE_TITULO = re.compile(r"^(#{2,3}) ", re.M)
RE_TOKEN = re.compile(r"`([^`\n]+)`")
RE_BLOCO = re.compile(r"^  ([a-z]{2}): \{\n(.*?)^  \}", re.S | re.M)
RE_CHAVE = re.compile(r"^    (\w+):", re.M)


def carrega_mapa(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def valida_mapa(mapa):
    """Forma do mapa: o que o src/i18n/idiomas.ts recusa no build, repetido aqui para o check não
    confiar num JSON que o build não leu."""
    erros = []
    idiomas, paginas = mapa.get("idiomas"), mapa.get("paginas")
    if not isinstance(idiomas, dict) or not isinstance(paginas, dict):
        return ["idiomas.json: sem os objetos `idiomas` e `paginas`"]
    if list(idiomas)[:1] != ["pt"]:
        erros.append("idiomas.json: `pt` tem de ser a primeira língua de `idiomas`")
    for codigo, d in idiomas.items():
        if not RE_PASTA_LINGUA.match(codigo):
            erros.append(f"idiomas.json: código `{codigo}` fora do ISO 639-1 em minúsculas")
        faltam = [c for c in CAMPOS_IDIOMA if not d.get(c)]
        if faltam:
            erros.append(f"idiomas.json: {codigo} sem {', '.join(faltam)}")
        elif len(d["meses"]) != 12:
            erros.append(f"idiomas.json: {codigo} com {len(d['meses'])} meses (esperado 12)")
    for pagina, linguas in paginas.items():
        if not linguas or linguas[0] != "pt":
            erros.append(f"idiomas.json: {pagina} não começa por `pt` ({linguas})")
        if len(set(linguas)) != len(linguas):
            erros.append(f"idiomas.json: {pagina} com língua repetida ({linguas})")
        for l in linguas:
            if l not in idiomas:
                erros.append(f"idiomas.json: {pagina} com língua `{l}` fora de `idiomas`")
    return erros


def arquivo(lang, caminho):
    """Arquivo publicado da página na língua: pt na raiz, as outras em `<código>/`."""
    return caminho if lang == "pt" else f"{lang}/{caminho}"


def pagina_de(rel):
    """(língua, caminho pt) de um arquivo de dist/: `en/x.html` → ("en", "x.html")."""
    primeiro, _, resto = rel.partition("/")
    if resto and RE_PASTA_LINGUA.match(primeiro):
        return primeiro, resto
    return "pt", rel


def url(site, lang, caminho):
    """URL pública (canonical, hreflang, sitemap): `index.html` vira a pasta (`/`, `/en/`)."""
    return site + ("" if lang == "pt" else f"{lang}/") + ("" if caminho == "index.html" else caminho)


# ------------------------------------------------------------ (i) data
def regra_datas(doc, datas):
    """`datas`: {língua: lastUpdated do front-matter}. Toda tradução com a data do pt."""
    ref = datas.get("pt")
    return [f"{doc}.{l}.md: `lastUpdated` {d!r} ≠ o do pt {ref!r} (regra i)"
            for l, d in datas.items() if l != "pt" and d != ref]


# ------------------------------------------------------------ (ii) títulos
def niveis(md):
    """Sequência de níveis dos títulos `##`/`###` do markdown: [2, 3, 3, 2, …]."""
    return [len(m) for m in RE_TITULO.findall(md)]


def regra_titulos(doc, mds):
    """`mds`: {língua: texto do .md}. A sequência de níveis da tradução é a do pt."""
    erros, ref = [], niveis(mds["pt"])
    for l, texto in mds.items():
        if l == "pt":
            continue
        seq = niveis(texto)
        if seq != ref:
            i = next((k for k, (a, b) in enumerate(zip(ref, seq)) if a != b), min(len(ref), len(seq)))
            erros.append(f"{doc}.{l}.md: sequência de títulos `##`/`###` diverge do pt no título {i + 1} "
                         f"({len(seq)} títulos, pt tem {len(ref)}) — a âncora por posição sairia trocada (regra ii)")
    return erros


# ------------------------------------------------------------ (iii) tokens
def regra_tokens(doc, mds):
    """Cada `` `token` `` do pt (permissão, produto, evento) com a mesma contagem na tradução."""
    erros, ref = [], collections.Counter(RE_TOKEN.findall(mds["pt"]))
    for l, texto in mds.items():
        if l == "pt":
            continue
        n = collections.Counter(RE_TOKEN.findall(texto))
        for token, q in sorted(ref.items()):
            if n[token] != q:
                erros.append(f"{doc}.{l}.md: `{token}` {n[token]}× ≠ {q}× no pt (regra iii)")
    return erros


# ------------------------------------------------------------ (iv) SDKs
def regra_sdks(doc, mds):
    erros = []
    for l, texto in mds.items():
        if l == "pt":
            continue
        for sdk in SDKS:
            if sdk in mds["pt"] and sdk not in texto:
                erros.append(f"{doc}.{l}.md: sem `{sdk}`, que o pt cita (regra iv)")
    return erros


# ------------------------------------------------------------ (v) e (vi) arquivos
def regra_arquivos_gerados(mapa, arquivos):
    """`arquivos`: caminhos de dist/, relativos e com `/`. Toda língua do mapa gerou a página."""
    return [f"{arquivo(l, p)}: ausente — {p} tem `{l}` no mapa (regra v)"
            for p, linguas in mapa["paginas"].items() for l in linguas if arquivo(l, p) not in arquivos]


def regra_linguas_fora_do_mapa(mapa, arquivos):
    """Nada em `pt/`; em `<código>/`, só páginas cuja lista no mapa tem o código."""
    erros = []
    for rel in sorted(arquivos):
        lang, caminho = pagina_de(rel)
        if lang == "pt":
            if rel.startswith("pt/"):
                erros.append(f"{rel}: `pt/` não existe — o pt fica na raiz (ADR-007 §1, regra vi)")
            continue
        if lang not in mapa["paginas"].get(caminho, []):
            erros.append(f"{rel}: `{lang}` fora do mapa de {caminho} — página sem a língua não é gerada (regra vi)")
    return erros


# ------------------------------------------------------------ (vii) front-matter
def regra_front_matter(doc, fms):
    """`fms`: {língua: front-matter já separado (dict)}. `pendente` reprova; a tradução não carrega
    proveniência (ADR-004)."""
    erros = []
    for l, fm in fms.items():
        if l == "pt":
            if "pendente" in fm:
                erros.append(f"{doc}.pt.md: `pendente: {fm['pendente']}` — tradução atrás do pt; "
                             f"traduzir e tirar cada língua da lista (regra vii)")
            continue
        for chave in ("origemCommit", "pendente"):
            if chave in fm:
                erros.append(f"{doc}.{l}.md: `{chave}` na tradução — proveniência e marcador ficam só no .pt.md (regra vii)")
    return erros


# ------------------------------------------------------------ (viii) hreflang
def hreflang_esperado(mapa, caminho, site):
    """{hreflang: URL} que a página declara; vazio para página com uma língua só ou fora do mapa."""
    linguas = mapa["paginas"].get(caminho, ["pt"])
    if len(linguas) < 2:
        return {}
    esperado = {mapa["idiomas"][l]["hreflang"]: url(site, l, caminho) for l in linguas}
    esperado["x-default"] = url(site, "en" if "en" in linguas else "pt", caminho)
    return esperado


def regra_hreflang(mapa, rel, alternates, site):
    """`alternates`: [(hreflang, href)] lidos do `<head>` de `rel`."""
    lang, caminho = pagina_de(rel)
    esperado = hreflang_esperado(mapa, caminho, site)
    if not esperado:
        return [f"{rel}: hreflang {alternates} numa página com uma língua só (regra viii)"] if alternates else []
    if len(alternates) != len(dict(alternates)) or dict(alternates) != esperado:
        return [f"{rel}: hreflang {sorted(alternates)} ≠ esperado {sorted(esperado.items())} "
                f"(x-default = en se houver, senão pt; regra viii)"]
    return []


# ------------------------------------------------------------ §9 links (D23)
def lingua_do_link(mapa, lang, caminho):
    """Língua do destino de um link de uma página em `lang` para `caminho` (D23 (A), ADR-007 §5):
    `lang` se o destino a tem; senão en, se tem; senão pt — a regra do x-default."""
    linguas = mapa["paginas"].get(caminho, ["pt"])
    if lang in linguas:
        return lang
    return "en" if "en" in linguas else "pt"


def regra_link(mapa, rel, href, destino, tag):
    """`rel`: a página (arquivo de dist/); `href`: como escrito; `destino`: arquivo de dist/ a que o
    href leva; `tag`: o `<a …>` inteiro. Página de origem ou de destino fora do mapa não entra: a 404
    é bilíngue por desenho (um bloco por língua, cada um com o seu link) e o convite e os assets não
    têm língua.

    O link marcado `data-troca-idioma="X"` (seletor e faixa de sugestão) sai da regra D23 e entra
    noutra: leva à **mesma página** na língua X (`destino == arquivo(X, origem)`), X é uma língua da
    página no mapa, e `hreflang`/`lang`, quando o link os tem, são os de X. O link da faixa não leva
    nenhum dos dois: a língua vem do `<section lang>`/`<template lang>` que o contém."""
    lang_pag, origem = pagina_de(rel)
    if origem not in mapa["paginas"]:
        return []
    troca = re.search(r'\sdata-troca-idioma(?:="([^"]*)")?', tag)
    if troca:
        x = troca.group(1) or ""
        if x not in mapa["paginas"][origem]:
            return [f"{rel}: data-troca-idioma=\"{x}\" fora das línguas de {origem} no mapa (§9)"]
        if destino != arquivo(x, origem):
            return [f"{rel}: data-troca-idioma=\"{x}\" com href=\"{href}\" leva a {destino}; "
                    f"esperado /{arquivo(x, origem)} — a mesma página na língua do link (§9)"]
        h = mapa["idiomas"][x]["hreflang"]
        for atributo in ("hreflang", "lang"):
            m = re.search(rf'\s{atributo}="([^"]*)"', tag)
            if m and m.group(1) != h:
                return [f"{rel}: data-troca-idioma=\"{x}\" com `{atributo}=\"{m.group(1)}\"`; "
                        f"esperado `{h}` (WCAG 3.1.2, §9)"]
        return []
    lang_alvo, caminho = pagina_de(destino)
    if caminho not in mapa["paginas"]:
        return []
    esperado = lingua_do_link(mapa, lang_pag, caminho)
    if lang_alvo != esperado:
        return [f"{rel}: href=\"{href}\" leva a {lang_alvo}; esperado /{arquivo(esperado, caminho)} "
                f"(mesma língua se o destino a tem, senão en, senão pt — D23, §9)"]
    if esperado != lang_pag:
        h = mapa["idiomas"][esperado]["hreflang"]
        for atributo in ("hreflang", "lang"):
            if not re.search(rf'\s{atributo}="{re.escape(h)}"', tag):
                return [f"{rel}: href=\"{href}\" leva a {esperado} sem `{atributo}=\"{h}\"` (WCAG 3.1.2, D23, §9)"]
    return []


# ------------------------------------------------------------ (xi) dicionários
def blocos(texto):
    """{língua: chaves} dos blocos `  xx: {` … `  }` de um dicionário de src/i18n/."""
    return {lang: set(RE_CHAVE.findall(corpo)) for lang, corpo in RE_BLOCO.findall(texto)}


def regra_dicionario(nome, texto, mapa, eh_ui):
    """Mesmas chaves em todos os blocos; língua do bloco no mapa; `ui.ts` com todas as línguas."""
    b = blocos(texto)
    if not b:
        # ui.ts é o dicionário de toda página: sem bloco lido, o formato mudou e a regra ficaria
        # calada. Os outros podem não ter blocos (só tipos e funções).
        return [f"{nome}: nenhum bloco `  xx: {{` … `  }}` encontrado (regra xi)"] if eh_ui else []
    erros = []
    idiomas = list(mapa["idiomas"])
    if "pt" not in b:
        erros.append(f"{nome}: dicionário sem bloco pt (regra xi)")
    for l in sorted(set(b) - set(idiomas)):
        erros.append(f"{nome}: bloco `{l}` fora das línguas de idiomas.json (regra xi)")
    if eh_ui:
        for l in idiomas:
            if l not in b:
                erros.append(f"{nome}: sem bloco `{l}` — toda língua de idiomas.json tem o seu em ui.ts (regra xi)")
    ref = b.get("pt", set())
    for l, chaves in b.items():
        if l == "pt":
            continue
        for falta in sorted(ref - chaves):
            erros.append(f"{nome}: chave `{falta}` existe em pt e falta em {l} (regra xi)")
        for sobra in sorted(chaves - ref):
            erros.append(f"{nome}: chave `{sobra}` existe em {l} e falta em pt (regra xi)")
    return erros


# ------------------------------------------------------------ (xii) guarda
def regra_guarda(mapa, publicadas, fora_do_mapa):
    """O mapa não tira página do ar calado: as chaves dele mais as de fora (o convite) são a lista
    fixa PUBLICADAS do check."""
    mapa_e_fora = set(mapa["paginas"]) | set(fora_do_mapa)
    erros = []
    for p in sorted(set(publicadas) - mapa_e_fora):
        erros.append(f"idiomas.json: {p} está em PUBLICADAS e falta em `paginas` (regra xii)")
    for p in sorted(mapa_e_fora - set(publicadas)):
        erros.append(f"idiomas.json: {p} em `paginas` e fora de PUBLICADAS do check_site.py (regra xii)")
    return erros


# ------------------------------------------------------------ data por extenso (§4 do check)
def fragmentos_data(texto, rotulo):
    """Trecho entre cada `rotulo` e o primeiro ano (4 dígitos) depois dele, sem marcação."""
    return re.findall(re.escape(rotulo) + r"\s*([^<>\n]{0,60}?\b\d{4})\b", texto)


def confere_data(fragmento, meses, ano, mes, dia):
    """O trecho cita exatamente o mês (nome da língua), o ano e o dia (se houver) de `lastUpdated`.
    Serve a qualquer língua sem conhecer a ordem dela ("13 de julho de 2026", "July 13, 2026")."""
    baixo = fragmento.casefold()
    citados = [m for m in meses if re.search(r"(?<!\w)" + re.escape(m.casefold()) + r"(?!\w)", baixo)]
    numeros = sorted(int(n) for n in re.findall(r"\d+", fragmento))
    esperado = sorted([int(ano)] + ([int(dia)] if dia else []))
    return citados == [meses[int(mes) - 1]] and numeros == esperado


def regra_linha_data(nome, corpo, rotulo, meses, ano, mes, dia):
    """Linha `**<rotulo>** <data>` do .md da língua: existe, e cada uma cita a data de `lastUpdated`
    (`ano`, `mes` 1–12, `dia` ou "") com o mês pelo nome da língua (`meses` do mapa)."""
    esperado = f"{int(ano):04d}-{int(mes):02d}" + (f"-{int(dia):02d}" if dia else "")
    frags = fragmentos_data(corpo, f"**{rotulo}**")
    if not frags:
        return [f"{nome}: sem linha de data `**{rotulo}** <data>`"]
    return [f"{nome}: linha de data `**{rotulo}** {x.strip()}` ≠ lastUpdated {esperado}"
            for x in frags if not confere_data(x, meses, ano, mes, dia)]


# ------------------------------------------------------------ (x) sem redirecionamento (§16 do check)
# Fronteira de palavra antes de `location`: `geolocation=` (Permissions-Policy) não é redirect.
RE_REDIRECT = re.compile(
    r"\blocation\.(?:replace|assign)\s*\("
    r"|\blocation(?:\.(?:href|pathname|search|hash))?\s*=(?!=)"
    r"|\blocation\s*\["
    r"|\bnavigation\.navigate\s*\("
    r"|http-equiv=[\"']?refresh",
    re.I,
)


def redirecionamentos(texto):
    """Cada trecho de `texto` (HTML ou JS publicado) que muda de página sozinho (ADR-007 §1, regra x)."""
    return [m.group(0) for m in RE_REDIRECT.finditer(texto)]
