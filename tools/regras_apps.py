#!/usr/bin/env python3
"""Regras da lista de apps do site (WP-10, fatia 10a; D12, D31) como funções puras.

Só biblioteca padrão, de propósito, como tools/regras_i18n.py. Nenhuma função aqui lê disco nem
roda processo: cada uma recebe o texto de `src/i18n/apps.ts`, o HTML da Home, a data de hoje ou uma
função `git`, e devolve dados e listas de erros/avisos. O `check_site.py` as chama sobre o site real
(§20 e §21); `tools/test_regras_apps.py` as chama sobre os casos de `tools/fixtures/apps/`.

  le_apps_ts         lê `ORDEM_APPS` e `apps` de src/i18n/apps.ts por regex, fechado contra falha
                     (sem JSON gerado no build: seria um arquivo a mais em dist/, publicado)
  particionar        cópia fiel de `particionarApps` (apps.ts): a regra D12 com a data de hoje
  hoje_de            a data de hoje em UTC, ou `GHF_HOJE` fora do CI (a guarda de `hojeDoBuild`)
  saida_do_destaque  primeiro dia em que o app sai do destaque (atualizadoEm + 12 meses, com a
                     rolagem de 29/02 do `Date.UTC` do JS)
  avisos_corte       app a 30 dias ou menos de sair do destaque (D31)
  le_home            os `<article>` de `#portfolio` e os links de "Todos os apps" de uma Home
  confere_home       a Home publicada contra uma partição (§20)
  confere_home_hoje  a Home contra a partição de hoje; batendo só a de ontem, aviso (meia-noite UTC)
  confere_tag        `tag` e `atualizadoEm` de um app contra o repositório dele (§21)
  le_fundacao        o ano de `since_2004` de src/i18n/home.ts (o "Desde 2004" do hero)
  confere_adr009     os campos do JSON-LD que o ADR-009 acrescentou, contra a página e apps.ts (§14)
"""
import datetime
import json
import re
from html.parser import HTMLParser

RE_PLAY = re.compile(r"^https://play\.google\.com/store/apps/details\?id=([\w.]+)(?:&|$)")
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
OBRIGATORIOS = ("nome", "id", "pagina", "privacidade", "icone", "atualizadoEm", "tag")
MAX_DESTAQUE = 4
DIAS_AVISO = 30
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def data_iso(texto):
    """`datetime.date` de `AAAA-MM-DD` estrito (2027-02-30 e 2027-13-01 são None, como no JS)."""
    if not isinstance(texto, str) or not RE_DATA.match(texto):
        return None
    try:
        return datetime.date.fromisoformat(texto)
    except ValueError:
        return None


def soma_anos(d, anos):
    """`Date.UTC(ano + anos, mês, dia)` do JS: o dia que não existe no mês rola para o seguinte
    (29/02 − 1 ano = 01/03). O `date(ano - 1, 2, 29)` do Python lançaria erro."""
    return datetime.date(d.year + anos, d.month, 1) + datetime.timedelta(days=d.day - 1)


# ------------------------------------------------------------ leitura de apps.ts
def sem_comentario(texto):
    """`texto` sem comentário de TS (`// … fim da linha` e `/* … */`) fora de aspas (`'`, `"`,
    `` ` ``). As quebras de linha ficam, para a regex por linha continuar valendo; `https://` dentro
    de string fica."""
    saida, i, n, aspa = [], 0, len(texto), None
    while i < n:
        ch = texto[i]
        if aspa:
            saida.append(ch)
            if ch == "\\" and i + 1 < n:
                saida.append(texto[i + 1])
                i += 2
                continue
            if ch == aspa:
                aspa = None
            i += 1
        elif ch in "'\"`":
            aspa = ch
            saida.append(ch)
            i += 1
        elif texto.startswith("//", i):
            fim = texto.find("\n", i)
            i = n if fim < 0 else fim
        elif texto.startswith("/*", i):
            fim = texto.find("*/", i + 2)
            trecho = texto[i:n if fim < 0 else fim + 2]
            saida.append("\n" * trecho.count("\n"))
            i = n if fim < 0 else fim + 2
        else:
            saida.append(ch)
            i += 1
    return "".join(saida)


def le_apps_ts(texto):
    """(apps, ordem, erros). `apps`: chave → {campo: valor} só com os campos `campo: 'valor'` e
    `indisponivel` (True/False); `ordem`: as chaves de `ORDEM_APPS`. Qualquer desvio do formato é
    erro (o check não adivinha)."""
    erros = []
    texto = sem_comentario(texto)
    m = re.search(r"export const ORDEM_APPS\s*=\s*\[([^\]]*)\]", texto)
    if not m:
        return {}, [], ["apps.ts: `export const ORDEM_APPS = [ … ]` não encontrado"]
    ordem = re.findall(r"'(\w+)'", m.group(1))
    if not ordem:
        erros.append("apps.ts: ORDEM_APPS vazia")
    if len(set(ordem)) != len(ordem):
        erros.append(f"apps.ts: ORDEM_APPS com chave repetida: {ordem}")
    m = re.search(r"export const apps\s*=\s*\{(.*?)\n\}\s*as const\b", texto, re.S)
    if not m:
        return {}, ordem, erros + ["apps.ts: `export const apps = { … } as const` não encontrado"]
    corpo = m.group(1)
    apps = {}
    for chave, bloco in re.findall(r"^ {2}(\w+):\s*\{(.*?)^ {2}\},?[ \t]*$", corpo, re.S | re.M):
        if chave in apps:
            erros.append(f"apps.ts: app `{chave}` declarado duas vezes")
        pares = re.findall(r"\b(\w+):\s*'([^']*)'", bloco)
        nomes = [k for k, _ in pares] + re.findall(r"\b(indisponivel):", bloco)
        repetidos = sorted({k for k in nomes if nomes.count(k) > 1})
        if repetidos:
            erros.append(f"apps.ts: `{chave}` com {', '.join(repetidos)} mais de uma vez (o check não escolhe qual vale)")
        campos = dict(pares)
        campos["indisponivel"] = bool(re.search(r"\bindisponivel:\s*true\b", bloco))
        apps[chave] = campos
    if sorted(apps) != sorted(ordem):
        erros.append(f"apps.ts: ORDEM_APPS ({', '.join(ordem)}) não tem exatamente as chaves de apps "
                     f"({', '.join(sorted(apps)) or 'nenhuma lida'})")
    for chave, campos in apps.items():
        faltam = [c for c in OBRIGATORIOS if not campos.get(c)]
        if faltam:
            erros.append(f"apps.ts: `{chave}` sem {', '.join(faltam)} (formato `campo: 'valor'`)")
        elif not campos["icone"].startswith("/assets/"):
            erros.append(f"apps.ts: `{chave}` com icone \"{campos['icone']}\" fora de /assets/ (URL fixa de public/, ADR-006)")
        elif data_iso(campos["atualizadoEm"]) is None:
            erros.append(f"apps.ts: `{chave}` com atualizadoEm \"{campos['atualizadoEm']}\" fora de AAAA-MM-DD válida")
    return apps, ordem, erros


# ------------------------------------------------------------ partição D12
def particionar(apps, ordem, hoje):
    """(destaque, resto, erros): a regra de `particionarApps`. Destaque, na ordem de `ordem`: o app
    não `indisponivel` com `atualizadoEm` ≥ hoje − 12 meses, até 4. `atualizadoEm` no futuro é erro."""
    corte = soma_anos(hoje, -1)
    destaque, resto, erros = [], [], []
    for c in ordem:
        a = apps.get(c, {})
        d = data_iso(a.get("atualizadoEm"))
        if d is None:
            erros.append(f"{a.get('nome', c)}: atualizadoEm {a.get('atualizadoEm')!r} não é uma data AAAA-MM-DD")
            resto.append(c)
            continue
        if d > hoje:
            erros.append(f"{a.get('nome', c)}: atualizadoEm {a['atualizadoEm']} está no futuro (hoje {hoje.isoformat()})")
        if not a.get("indisponivel") and d >= corte and len(destaque) < MAX_DESTAQUE:
            destaque.append(c)
        else:
            resto.append(c)
    return destaque, resto, erros


def hoje_de(environ, agora=None):
    """(data de hoje, erro). Hoje em UTC, como o `new Date()` do build lido em `getUTC*`.
    `GHF_HOJE=AAAA-MM-DD` só fora do CI: com `CI` ou `GITHUB_ACTIONS` é erro, como em `hojeDoBuild`."""
    forcada = environ.get("GHF_HOJE")
    if forcada:
        if environ.get("CI") or environ.get("GITHUB_ACTIONS"):
            return None, "GHF_HOJE é só para teste local; não use no CI nem no deploy"
        d = data_iso(forcada)
        if d is None:
            return None, f"GHF_HOJE={forcada}: não é uma data AAAA-MM-DD válida"
        return d, None
    agora = agora or datetime.datetime.now(datetime.timezone.utc)
    return agora.astimezone(datetime.timezone.utc).date(), None


def saida_do_destaque(atualizado):
    """Primeiro dia em que o app com esta `atualizadoEm` fica fora do destaque: o menor `h` com
    `h − 12 meses > atualizado` (com a rolagem do JS; atualizado em 29/02 sai em 01/03)."""
    h = soma_anos(atualizado, 1) - datetime.timedelta(days=2)
    while soma_anos(h, -1) <= atualizado:
        h += datetime.timedelta(days=1)
    return h


def avisos_corte(apps, destaque, hoje, dias=DIAS_AVISO):
    """Aviso (D31) para cada app em destaque que sai dele em `dias` dias ou menos."""
    avisos = []
    for c in destaque:
        a = apps[c]
        if a.get("indisponivel"):
            continue
        saida = saida_do_destaque(data_iso(a["atualizadoEm"]))
        n = (saida - hoje).days
        if n <= dias:
            avisos.append(f"{a['nome']}: sai do destaque da Home em {saida.isoformat()} ({n} dias) — publique "
                          "release e atualize apps.ts, ou aceite a saída")
    return avisos


# ------------------------------------------------------------ Home publicada
class LeHome(HTMLParser):
    """Dentro de `#portfolio`: cada `<article>` (href do `<h3><a>`, ids da Play, `<time datetime>`)
    e os `href` fora de `<article>` (a lista "Todos os apps")."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.artigos, self.fora = [], []
        self.portfolios = 0
        self._pilha = []

    def _em(self, nome):
        return any(t == nome for t, _ in self._pilha)

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        no_portfolio = any(a.get("id") == "portfolio" for _, a in self._pilha) or d.get("id") == "portfolio"
        if d.get("id") == "portfolio":
            self.portfolios += 1
        if no_portfolio:
            if tag == "article":
                self.artigos.append({"h3": [], "play": [], "time": []})
            elif self._em("article") and self.artigos:
                art = self.artigos[-1]
                if tag == "a" and self._em("h3"):
                    art["h3"].append(d.get("href", ""))
                if tag == "a":
                    m = RE_PLAY.match(d.get("href", ""))
                    if m:
                        art["play"].append((m.group(1), d.get("id")))
                if tag == "time":
                    art["time"].append(d.get("datetime", ""))
            elif tag == "a":
                self.fora.append(d.get("href", ""))
        if tag not in VAZIOS:
            self._pilha.append((tag, d))

    def handle_startendtag(self, tag, attrs):
        pilha = list(self._pilha)
        self.handle_starttag(tag, attrs)
        self._pilha = pilha

    def handle_endtag(self, tag):
        for i in range(len(self._pilha) - 1, -1, -1):
            if self._pilha[i][0] == tag:
                del self._pilha[i:]
                break


def le_home(html):
    leitor = LeHome()
    leitor.feed(html)
    leitor.close()
    return leitor


def confere_home(rotulo, html, apps, destaque, resto, href_de):
    """Erros da Home publicada (`rotulo`: o arquivo, para a mensagem) contra a partição.
    `href_de(caminho pt)` dá o href que o `link()` gera na língua da Home."""
    erros = []
    h = le_home(html)
    if h.portfolios != 1:
        return [f"{rotulo}: {h.portfolios} elementos com id=\"portfolio\" (esperado 1)"]
    por_href = {href_de(a["pagina"]): c for c, a in apps.items()}
    vistos = []
    for n, art in enumerate(h.artigos, 1):
        if len(art["h3"]) != 1 or art["h3"][0] not in por_href:
            erros.append(f"{rotulo}: <article> #{n} sem um <h3><a> para a landing de um app de apps.ts ({art['h3']})")
            continue
        c = por_href[art["h3"][0]]
        a = apps[c]
        vistos.append(c)
        if [i for i, _ in art["play"]] != [a["id"]]:
            erros.append(f"{rotulo}: <article> de {a['nome']} com botão da Play para {[i for i, _ in art['play']]} ≠ [{a['id']}]")
        if art["time"] != [a["atualizadoEm"]]:
            erros.append(f"{rotulo}: <article> de {a['nome']} com <time datetime> {art['time']} ≠ atualizadoEm {a['atualizadoEm']}")
    if vistos != destaque:
        erros.append(f"{rotulo}: cards da Home {vistos} ≠ destaque da D12 hoje, na ordem de ORDEM_APPS, {destaque}")
    for c in resto:
        a = apps[c]
        alvo = href_de(a["privacidade"] if a.get("indisponivel") else a["pagina"])
        if alvo not in h.fora:
            erros.append(f"{rotulo}: {a['nome']} fora do destaque e sem link {alvo} em \"Todos os apps\"")
        if a.get("indisponivel") and href_de(a["pagina"]) in h.fora:
            erros.append(f"{rotulo}: {a['nome']} indisponível com link para a landing em \"Todos os apps\"")
    for c in destaque:
        if href_de(apps[c]["pagina"]) in h.fora:
            erros.append(f"{rotulo}: {apps[c]['nome']} em destaque e também em \"Todos os apps\"")
    return erros


def confere_home_hoje(rotulo, html, apps, ordem, hoje, href_de):
    """(erros, avisos) da Home contra a partição de hoje. Se a de hoje não bate e a de ontem bate,
    o dist/ foi gerado antes da meia-noite UTC: aviso, não erro."""
    destaque, resto, erros = particionar(apps, ordem, hoje)
    if erros:
        return erros, []
    achados = confere_home(rotulo, html, apps, destaque, resto, href_de)
    if achados:
        d_ontem, r_ontem, _ = particionar(apps, ordem, hoje - datetime.timedelta(days=1))
        if not confere_home(rotulo, html, apps, d_ontem, r_ontem, href_de):
            return [], [f"{rotulo}: dist/ gerado ontem (UTC) — refaça o build (o destaque de hoje é {destaque})"]
    return achados, []


# ------------------------------------------------------------ tag do app
def confere_tag(nome, tag, atualizado, git, repo_dir="<repo>"):
    """(erros, avisos) de um app contra o repositório dele. `git(*args)` → (código, stdout bytes).
    Tag ausente é erro mesmo que o clone só esteja sem as tags: a mensagem diz como buscá-las (o
    check não usa rede, e rebaixar a aviso deixaria passar tag digitada errada)."""
    erros, avisos = [], []
    cod, _ = git("rev-parse", "--verify", "--quiet", tag + "^{commit}")
    if cod != 0:
        return [f"{nome}: tag {tag} (apps.ts) não existe no clone local do app — se o clone está sem as tags,"
                f" rode `git -C {repo_dir} fetch --tags` e repita; se continuar, a tag de apps.ts está errada"], []
    cod, out = git("log", "-1", "--format=%cs", tag + "^{commit}")
    data = out.decode().strip() if cod == 0 else ""
    if data != atualizado:
        erros.append(f"{nome}: commit da tag {tag} é de {data or '?'} ≠ atualizadoEm {atualizado} (apps.ts)")
    cod, out = git("tag", "--list", "v*", "--sort=-v:refname")
    tags = out.decode().split() if cod == 0 else []
    if tags and tags[0] != tag:
        nova = tags[0]
        cod, out = git("log", "-1", "--format=%cs", nova + "^{commit}")
        avisos.append(f"{nome}: tag {nova} ({out.decode().strip() if cod == 0 else '?'}) depois de {tag} — "
                      "atualize tag e atualizadoEm em apps.ts")
    return erros, avisos


# ------------------------------------------------------------ JSON-LD do ADR-009 (§14)
RE_FOOTER = re.compile(r"<footer\b.*?</footer>", re.S | re.I)
OFERTA = {"@type": "Offer", "price": "0", "priceCurrency": "BRL"}
EM_ESTOQUE = "https://schema.org/InStock"


def le_fundacao(texto_home):
    """(ano, erros): o ano AAAA de `since_2004` em src/i18n/home.ts, o mesmo em toda língua."""
    valores = re.findall(r"\bsince_2004:\s*'([^']*)'", sem_comentario(texto_home))
    anos = [re.findall(r"\b(\d{4})\b", v) for v in valores]
    if not valores:
        return None, ["home.ts: nenhum `since_2004: '…'` — de onde vem o foundingDate?"]
    if any(len(a) != 1 for a in anos) or len({a[0] for a in anos}) != 1:
        return None, [f"home.ts: since_2004 {valores} sem exatamente um ano AAAA, o mesmo em toda língua"]
    return anos[0][0], []


class LePagina(HTMLParser):
    """canonical, meta description, JSON-LD, texto do `<body>` (sem script/style) e `href` https://
    de dentro de `<footer>`."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicas, self.descricoes, self.jsonld, self.texto, self.rodape = [], [], [], [], []
        self._ld = None
        self._corpo = self._oculto = self._footer = 0

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "body":
            self._corpo = 1
        elif tag in ("script", "style"):
            self._oculto += 1
            if tag == "script" and d.get("type", "").lower() == "application/ld+json":
                self._ld = []
        elif tag == "footer":
            self._footer += 1
        elif tag == "link" and "canonical" in d.get("rel", "").lower().split():
            self.canonicas.append(d.get("href", ""))
        elif tag == "meta" and d.get("name", "").lower() == "description":
            self.descricoes.append(d.get("content", ""))
        if tag == "a" and self._footer and d.get("href", "").startswith("https://"):
            self.rodape.append(d["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._oculto:
            self._oculto -= 1
            if tag == "script" and self._ld is not None:
                self.jsonld.append("".join(self._ld))
                self._ld = None
        elif tag == "footer" and self._footer:
            self._footer -= 1

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)
        elif self._corpo and not self._oculto:
            self.texto.append(data)


def confere_adr009(rotulo, html, app, site, existe, ano_fundacao):
    """Erros dos campos do ADR-009 no JSON-LD da página. `app`: o registro de apps.ts da landing
    (None fora das landings); `site`: `https://ghfsoftware.com/`; `existe(rel)`: o arquivo existe
    em dist/; `ano_fundacao`: o de `le_fundacao`. JSON-LD que não faz parse fica para o §14."""
    pg = LePagina()
    pg.feed(html)
    pg.close()
    erros = []
    descricao = pg.descricoes[0] if len(pg.descricoes) == 1 else None
    canonica = pg.canonicas[0] if len(pg.canonicas) == 1 else None
    corpo = re.sub(r"\s+", " ", " ".join(pg.texto))
    for bruto in pg.jsonld:
        try:
            o = json.loads(bruto)
        except ValueError:
            continue
        if not isinstance(o, dict):
            continue
        tipo = o.get("@type")
        if tipo == "Organization":
            if o.get("description") != descricao:
                erros.append(f"{rotulo}: Organization.description {o.get('description')!r} ≠ meta description {descricao!r} (ADR-009)")
            fundacao = o.get("foundingDate")
            if ano_fundacao is None or fundacao != ano_fundacao:
                erros.append(f"{rotulo}: Organization.foundingDate {fundacao!r} ≠ o ano de since_2004 de home.ts {ano_fundacao!r} (ADR-009)")
            elif not re.search(rf"\b{ano_fundacao}\b", corpo):
                erros.append(f"{rotulo}: Organization.foundingDate {fundacao!r} não aparece no corpo da página (ADR-009)")
            same = o.get("sameAs")
            if not (isinstance(same, list) and same and all(isinstance(u, str) and u.startswith("https://") for u in same)):
                erros.append(f"{rotulo}: Organization.sameAs {same!r} não é lista não vazia de URLs https:// (ADR-009)")
            elif set(same) - set(pg.rodape):
                erros.append(f"{rotulo}: Organization.sameAs com {sorted(set(same) - set(pg.rodape))} fora dos links do <footer> da página (ADR-009)")
        elif tipo == "MobileApplication":
            if app is None:
                erros.append(f"{rotulo}: MobileApplication numa página que não é landing de app de apps.ts")
                continue
            oferta = dict(OFERTA, **({} if app.get("indisponivel") else {"availability": EM_ESTOQUE}))
            if o.get("offers") != oferta:
                erros.append(f"{rotulo}: offers {o.get('offers')!r} ≠ {oferta} (só o download gratuito; preço do Premium nunca;"
                             " InStock só se o app não é `indisponivel`, ADR-009)")
            if canonica is None or o.get("url") != canonica:
                erros.append(f"{rotulo}: MobileApplication.url {o.get('url')!r} ≠ canonical {canonica!r} (ADR-009)")
            if o.get("description") != descricao:
                erros.append(f"{rotulo}: MobileApplication.description {o.get('description')!r} ≠ meta description {descricao!r} (ADR-009)")
            esperada = site.rstrip("/") + app["icone"]
            if o.get("image") != esperada:
                erros.append(f"{rotulo}: MobileApplication.image {o.get('image')!r} ≠ {esperada!r}, o icone de {app['nome']} em apps.ts (ADR-009)")
            elif not existe(app["icone"].lstrip("/")):
                erros.append(f"{rotulo}: MobileApplication.image {esperada!r}: o arquivo não existe no site (ADR-009)")
    return erros
