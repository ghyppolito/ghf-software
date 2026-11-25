#!/usr/bin/env python3
"""Espelha o texto legal do repositório do app no site (ADR-004, D7, D14).

Só biblioteca padrão, de propósito. Copia o corpo do texto legal (`PRIVACY_POLICY.md`,
`TERMS_OF_SERVICE.md`, `TERMS_OF_USE.md`) de um **commit** do app (`git show <sha>:<caminho>`, nunca
o disco) para `src/content/legal/<app>-<doc>.pt.md`, byte a byte, com o front-matter:

    ---
    lastUpdated: "AAAA-MM[-DD]"
    origemCommit: "<sha de 40>"
    pendente: ["es", …]
    ---

Língua que o app publica e `ORIGENS` declara (ADR-010; hoje o en do TopoWalk) é **espelhada** do
mesmo sha, na mesma execução: `<app>-<doc>.<código>.md` recebe o corpo do arquivo daquela língua byte
a byte, com `lastUpdated` (da linha `**<rótulo da língua>**`, pelo `rotuloData`/`meses` do mapa) e o
mesmo `origemCommit` do pt. Se a data do pt e a da língua espelhada diferem na origem, a cópia é
recusada (o problema volta ao app).

`pendente` lista as línguas da página no mapa `src/i18n/idiomas.json` menos o pt e menos as
espelhadas (ADR-007 §8); página sem tradução feita pelo site não ganha a chave. Nunca abre nem
escreve o `.<código>.md` de língua não espelhada: a tradução é do `site-legal`, que tira cada língua
da lista quando a atualiza e apaga a chave quando ela esvazia. O `check_site.py` importa `ORIGENS`
daqui e confere o corpo de cada língua espelhada contra `origemCommit`.

Uso:
    python3 tools/sync_legal.py <app>|--todos [--doc privacy|terms] [--ref REF]
                                [--apps-dir DIR] [--check] [--forca]

  <app>        lottoexpert | topowalk | poleposition | eclipsego
  --ref        branch, tag ou sha do app (padrão: a ref de ORIGENS, D14)
  --apps-dir   pasta onde estão os repositórios dos apps (padrão: $GHF_APPS_DIR ou `..` do site)
  --check      não escreve; diz igual / atrás / à frente-divergente / origem ausente por doc
  --forca      copia mesmo quando o origemCommit registrado não é ancestral da ref (só esse caso;
               sem origemCommit e corpo ≠ é sempre recusa: use `--ref` explícito)

Saída: 0 = nada a fazer ou cópia feita (ou origem ausente, com aviso); 1 = `--check` achou o que
fazer; 2 = recusa (nada foi escrito).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras_i18n as i18n  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGAL_DIR = os.path.join("src", "content", "legal")

# Tabela única: doc do site (`<app>-<doc>`, nome do `.pt.md` sem a extensão) → (repositório do app
# relativo a --apps-dir, {língua: caminho do .md dentro dele}, ref padrão = branch principal do app,
# D14). O pt é obrigatório; outra língua só entra quando o app a publica, e então é espelhada, não
# traduzida (ADR-010 §1). Declaração explícita: um `.en.md` novo no app não muda o site sozinho (o
# `--check` avisa). O `/legal` cita esta tabela; o `check_site.py` exige que ela cubra exatamente o
# LEGAL dele.
ORIGENS = {
    "lottoexpert-privacy": ("lotto-expert", {"pt": "docs/PRIVACY_POLICY.md"}, "master"),
    "lottoexpert-terms": ("lotto-expert", {"pt": "docs/TERMS_OF_SERVICE.md"}, "master"),
    "topowalk-privacy": ("topo-walk", {"pt": "PRIVACY_POLICY.md", "en": "PRIVACY_POLICY.en.md"}, "master"),
    "topowalk-terms": ("topo-walk", {"pt": "TERMS_OF_USE.md", "en": "TERMS_OF_USE.en.md"}, "master"),
    "poleposition-privacy": ("pole-position/pole-position-app", {"pt": "PRIVACY_POLICY.md"}, "master"),
    "eclipsego-privacy": ("eclipse-go", {"pt": "docs/PRIVACY_POLICY.md"}, "main"),
}


def espelhadas(doc):
    """Línguas além do pt que a origem do doc publica e o site espelha (ADR-010)."""
    return [l for l in ORIGENS[doc][1] if l != "pt"]


def caminho_irmao(caminho, lang):
    """`<BASE>.md` → `<BASE>.<código>.md` (o nome que o app usa para a mesma página em outra língua)."""
    return caminho[: -len(".md")] + f".{lang}.md"

CHAVES = ("lastUpdated", "origemCommit", "pendente")
MAPA = os.path.join(REPO, "src", "i18n", "idiomas.json")
RE_SHA = re.compile(r"^[0-9a-f]{40}$")
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]
RE_DATA = re.compile(r"\*\*Última atualização:\*\*\s*(?:(\d{1,2}) de )?(\w+) de (\d{4})")
# Caminhos que, mudados em origin/master do site, indicam hotfix legal ainda não integrado.
CAMINHOS_HOTFIX = ["src/content/legal/", "docs/*POLICY*", "docs/*TERMS*", "*-privacy.html", "*-terms.html"]


class Recusa(Exception):
    """Caso em que o script não escreve nada e sai com 2."""


def apps_dir_padrao():
    return os.environ.get("GHF_APPS_DIR") or os.path.dirname(REPO)


def repo_presente(apps_dir, repo):
    return os.path.exists(os.path.join(apps_dir, repo, ".git"))


def git(cwd, *args):
    """(código, stdout em bytes). Só leitura nos repositórios dos apps: rev-parse, show,
    merge-base, branch -r --contains."""
    r = subprocess.run(["git", "-C", cwd, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.returncode, r.stdout


def resolve(repo_dir, ref):
    """sha de 40 do commit de `ref`, ou None se a ref não existe."""
    cod, out = git(repo_dir, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    return out.decode().strip() if cod == 0 else None


def mostra(repo_dir, sha, caminho):
    """Bytes de `caminho` no commit `sha`, ou None."""
    cod, out = git(repo_dir, "show", f"{sha}:{caminho}")
    return out if cod == 0 else None


def ancestral(repo_dir, a, b):
    return git(repo_dir, "merge-base", "--is-ancestor", a, b)[0] == 0


def em_remoto(repo_dir, sha):
    cod, out = git(repo_dir, "branch", "-r", "--contains", sha)
    return cod == 0 and bool(out.strip())


def separa(dados):
    """(front-matter como dict ordenado, lista de chaves, corpo em bytes) de um `.<código>.md`.
    None no front-matter se o arquivo não começa com `---\\n … \\n---\\n`. Valor é `"texto"` ou
    lista `["a", "b"]` (vira list); chave fora desses formatos vira chave com valor None (quem
    chama recusa)."""
    m = re.match(rb"---\n(.*?)\n---\n", dados, re.S)
    if not m:
        return None, [], dados
    fm, chaves = {}, []
    for linha in m.group(1).decode("utf-8").split("\n"):
        kv = re.match(r'^([^:\s]+):\s*"([^"]*)"\s*$', linha)
        lista = re.match(r'^([^:\s]+):\s*\[\s*("[^"]*"(?:\s*,\s*"[^"]*")*)?\s*\]\s*$', linha)
        if kv:
            fm[kv.group(1)] = kv.group(2)
            chaves.append(kv.group(1))
        elif lista:
            fm[lista.group(1)] = re.findall(r'"([^"]*)"', lista.group(2) or "")
            chaves.append(lista.group(1))
        else:
            chave = linha.split(":", 1)[0].strip() or linha
            fm[chave] = None
            chaves.append(chave)
    return fm, chaves, dados[m.end():]


def valor(v):
    """Valor do front-matter em YAML: `"texto"` ou `["a", "b"]`."""
    return "[" + ", ".join(f'"{x}"' for x in v) + "]" if isinstance(v, list) else f'"{v}"'


def monta(fm, corpo):
    linhas = ["---"] + [f"{k}: {valor(fm[k])}" for k in CHAVES if fm.get(k) is not None] + ["---", ""]
    return "\n".join(linhas).encode("utf-8") + corpo


def mapa():
    with open(MAPA, encoding="utf-8") as f:
        return json.load(f)


def pendentes(doc):
    """Línguas da página do doc no mapa (src/i18n/idiomas.json), menos o pt e menos as espelhadas:
    as traduções do site que ficam atrás quando o pt muda (ADR-007 §8, ADR-010 §3)."""
    paginas = mapa()["paginas"]
    pagina = f"{doc}.html"
    if pagina not in paginas:
        raise Recusa(f"{doc}: {pagina} fora de `paginas` de src/i18n/idiomas.json")
    return [l for l in paginas[pagina] if l != "pt" and l not in espelhadas(doc)]


def data_da_origem(corpo):
    """`lastUpdated` a partir da linha `**Última atualização:**` da origem; Recusa se faltar."""
    m = RE_DATA.search(corpo.decode("utf-8", errors="replace"))
    if not m:
        raise Recusa("origem sem a linha `**Última atualização:** [D de ]Mês de AAAA`")
    dia, mes, ano = m.groups()
    if mes.lower() not in MESES:
        raise Recusa(f"mês desconhecido na linha de data da origem: {mes!r}")
    n = MESES.index(mes.lower()) + 1
    return f"{ano}-{n:02d}" + (f"-{int(dia):02d}" if dia else "")


def data_da_lingua(nome, corpo, lang, data):
    """Erros da linha `**<rótulo da língua>** <data>` da origem espelhada contra a `data` do pt
    (AAAA-MM[-DD]), pelo `rotuloData`/`meses` da língua no mapa (ADR-010 §2 e §4). Vazio = mesma data."""
    d = mapa()["idiomas"].get(lang)
    if not d:
        return [f"{nome}: língua `{lang}` fora de `idiomas` de src/i18n/idiomas.json"]
    ano, mes, *dia = data.split("-")
    return i18n.regra_linha_data(nome, corpo.decode("utf-8", errors="replace"), d["rotuloData"], d["meses"],
                                 ano, int(mes), dia[0] if dia else "")


def secoes(corpo):
    """{título `## …`: texto da seção} — para dizer ao site-legal onde o texto mudou."""
    out, atual = {}, "(antes da primeira seção)"
    for linha in corpo.decode("utf-8", errors="replace").splitlines():
        if linha.startswith("## "):
            atual = linha[3:].strip()
        out[atual] = out.get(atual, "") + linha + "\n"
    return out


def secoes_alteradas(antes, depois):
    a, d = secoes(antes), secoes(depois)
    nomes = list(d) + [k for k in a if k not in d]
    return [("+ " if k not in a else "- " if k not in d else "~ ") + k
            for k in nomes if a.get(k) != d.get(k)]


def sujo(caminho):
    """True se o arquivo do site tem modificação não commitada (ou não está versionado)."""
    rel = os.path.relpath(caminho, REPO)
    cod, out = git(REPO, "status", "--porcelain", "--", rel)
    return cod == 0 and bool(out.strip())


def aviso_hotfix():
    if resolve(REPO, "origin/master") is None:
        return
    # Conteúdo, não histórico: `HEAD...origin/master` = o que master mudou desde a base comum. Um
    # hotfix já integrado por conteúdo (merge em develop) não aparece.
    cod, out = git(REPO, "diff", "--name-only", "HEAD...origin/master", "--", *CAMINHOS_HOTFIX)
    if cod == 0 and out.strip():
        print("⚠️  hotfix legal em master não integrado — `git merge origin/master` antes do sync:")
        for linha in out.decode().splitlines():
            print(f"     {linha}")


def alvo_de(doc, lang):
    return os.path.join(REPO, LEGAL_DIR, f"{doc}.{lang}.md")


def le_lado(doc, lang):
    """(conteúdo atual ou None, front-matter, corpo) do `.<código>.md` do site; Recusa se o
    front-matter estiver fora do formato."""
    alvo = alvo_de(doc, lang)
    if not os.path.exists(alvo):
        return None, {}, b""
    with open(alvo, "rb") as f:
        atual = f.read()
    fm, chaves, corpo = separa(atual)
    if fm is None:
        raise Recusa(f"{doc}: {os.path.relpath(alvo, REPO)} sem front-matter `---` no topo")
    estranhas = [k for k in chaves if k not in CHAVES or fm[k] is None]
    if estranhas or len(chaves) != len(set(chaves)):
        raise Recusa(f"{doc}: {os.path.relpath(alvo, REPO)} com chave fora de {{{', '.join(CHAVES)}}} ou repetida: {chaves}")
    return atual, fm, corpo


def planeja(doc, args):
    """Decide o que fazer com um doc (o pt e as línguas espelhadas, ADR-010). Devolve (estado,
    [(arquivo, conteúdo novo)], mensagens)."""
    repo, caminhos, ref_padrao = ORIGENS[doc]
    caminho = caminhos["pt"]
    ref = args.ref or ref_padrao
    repo_dir = os.path.join(args.apps_dir, repo)
    alvo = alvo_de(doc, "pt")
    msgs = []

    if not repo_presente(args.apps_dir, repo):
        return "ausente", [], [f"⚠️  {doc}: origem ausente ({repo_dir}) — nada a comparar, nada escrito"]

    sha = resolve(repo_dir, ref)
    if sha is None:
        raise Recusa(f"{doc}: ref `{ref}` não existe em {repo}")
    origem = mostra(repo_dir, sha, caminho)  # None se o arquivo não existe na ref (vê abaixo)
    msgs.append(f"{doc}: origem {repo}@{ref} = {sha}")

    atual, fm, corpo = le_lado(doc, "pt")
    registrado = fm.get("origemCommit")
    if registrado is not None and not RE_SHA.match(registrado):
        raise Recusa(f"{doc}: origemCommit `{registrado}` não é sha de 40 hex minúsculos")
    if registrado and resolve(repo_dir, registrado) is None:
        raise Recusa(f"{doc}: origemCommit {registrado[:7]} não existe em {repo} — `git fetch` no app ou origemCommit inventado")

    # Línguas espelhadas (ADR-010): o arquivo da língua no mesmo sha. Sem nenhuma declarada, o app
    # publicar `<BASE>.en.md` é aviso (ADR-010 §1): o en do site segue traduzido até ORIGENS declarar.
    langs = espelhadas(doc)
    if not langs:
        irmao = caminho_irmao(caminho, "en")
        if mostra(repo_dir, sha, irmao) is not None:
            msgs.append(f"⚠️  {doc}: {repo}@{sha[:7]} publica {irmao}, que ORIGENS não declara — o en do site "
                        "continua tradução; achado (ADR-010 §1)")
    lados = {}
    for l in langs:
        at_l, fm_l, corpo_l = le_lado(doc, l)
        lados[l] = (at_l, fm_l, corpo_l, mostra(repo_dir, sha, caminhos[l]))

    def em_dia(l):
        """A língua espelhada já é a cópia do commit registrado no pt, e a ref não tem en novo."""
        at_l, fm_l, corpo_l, origem_l = lados[l]
        return (at_l is not None and origem_l is not None and corpo_l == origem_l
                and fm_l.get("origemCommit") == registrado
                and mostra(repo_dir, registrado, caminhos[l]) == corpo_l)

    pt_igual = origem is not None and atual is not None and corpo == origem
    atrasadas = [l for l in langs if not (registrado and em_dia(l))]
    if pt_igual and registrado and not atrasadas:
        return "igual", [], msgs + [f"✅ {doc}: nada a fazer ({repo}@{sha[:7]}" + (f"; {', '.join(langs)} espelhado" if langs else "") + ")"]

    if not pt_igual:
        # Corpo do pt diferente.
        if registrado and not ancestral(repo_dir, registrado, sha):
            texto = (f"{doc}: à frente/divergente — o origemCommit {registrado[:7]} não é ancestral de "
                     f"{ref} ({sha[:7]}); copiar desfaria texto publicado")
            if not args.forca:
                if args.check:
                    return "divergente", [], msgs + [f"⛔ {texto}. Escolha a ref (`--ref`) ou use `--forca`"]
                raise Recusa(texto + " — escolha a ref (`--ref`) ou use `--forca`")
            msgs.append(f"⚠️  {texto} — `--forca`, copiando mesmo assim")
        elif atual is not None and not registrado:
            # Sem `--forca` aqui: sem proveniência não há ancestralidade a provar; o caminho é o
            # bootstrap com `--ref` do commit cujo texto o site já espelha (corpo igual).
            texto = f"{doc}: sem origemCommit e corpo ≠ {repo}@{sha[:7]} — não há como saber se é atraso ou edição"
            if args.check:
                return "divergente", [], msgs + [f"⛔ {texto}"]
            raise Recusa(texto + " — rode com `--ref` explícito do commit que o site espelha (o `--forca` não vale aqui)")
    elif registrado and not ancestral(repo_dir, registrado, sha):
        # pt igual, língua espelhada atrás: o mesmo cuidado com a ref antes de trocar o commit.
        texto = (f"{doc}: o origemCommit {registrado[:7]} não é ancestral de {ref} ({sha[:7]}); "
                 f"trocar o commit desfaria texto publicado em {', '.join(atrasadas)}")
        if not args.forca:
            if args.check:
                return "divergente", [], msgs + [f"⛔ {texto}. Escolha a ref (`--ref`) ou use `--forca`"]
            raise Recusa(texto + " — escolha a ref (`--ref`) ou use `--forca`")
        msgs.append(f"⚠️  {texto} — `--forca`, copiando mesmo assim")
    if origem is None:
        raise Recusa(f"{doc}: {caminho} não existe em {repo}@{sha[:7]}")

    data = data_da_origem(origem)
    # Data de cada língua espelhada = a do pt, no mesmo sha (ADR-010 §4). Divergente: o en do app
    # está atrás do pt, e o site não publica pt novo com en velho.
    for l in langs:
        origem_l = lados[l][3]
        if origem_l is None:
            raise Recusa(f"{doc}: {caminhos[l]} não existe em {repo}@{sha[:7]} — ORIGENS declara `{l}` (ADR-010)")
        erros_data = data_da_lingua(f"{repo}@{sha[:7]}:{caminhos[l]}", origem_l, l, data)
        if erros_data:
            texto = (f"{doc}: data do {l} ≠ a do pt ({data}) em {repo}@{sha[:7]} — o {l} do app está atrás do pt; "
                     f"corrigir no app (ADR-010 §4): " + "; ".join(erros_data))
            if args.check:
                return "divergente", [], msgs + [f"⛔ {texto}"]
            raise Recusa(texto)

    if pt_igual and not registrado:
        # Bootstrap: o corpo do pt já é o da origem; só o front-matter ganha o commit.
        escritas = [(alvo, monta(dict(fm, origemCommit=sha), corpo))]
        estado, texto = "bootstrap", f"{doc}: corpo igual a {repo}@{sha[:7]}; falta origemCommit (bootstrap: só o front-matter)"
    elif pt_igual:
        # pt igual, alguma língua espelhada atrás: o pt troca só o commit (mesmo sha nos dois).
        escritas = [(alvo, monta(dict(fm, origemCommit=sha), corpo))]
        estado, texto = "atras" if args.check else "copia", f"{doc}: pt igual; {', '.join(atrasadas)} atrás de {repo}@{sha[:7]}"
    else:
        msgs.append(f"{doc}: seções alteradas: " + (", ".join(secoes_alteradas(corpo, origem)) or "(nenhuma ## — mudança fora de seção)"))
        if atual is not None and fm.get("lastUpdated") == data:
            msgs.append(f"⚠️  {doc}: texto mudou sem data nova ({data}) — achado para o repositório do app")
        for l in langs:
            if registrado and mostra(repo_dir, registrado, caminhos[l]) == lados[l][3]:
                msgs.append(f"⚠️  {doc}: pt mudou e {l} não ({repo}@{registrado[:7]}..{sha[:7]}) — "
                            f"o {l} do app pode estar atrás; achado para o repositório do app (ADR-010 §4)")
        novo = {"lastUpdated": data, "origemCommit": sha}
        linguas = pendentes(doc)
        if linguas:
            novo["pendente"] = linguas
        marcador = f"; pendente: {', '.join(linguas)}" if linguas else ""
        escritas = [(alvo, monta(novo, origem))]
        estado, texto = "atras" if args.check else "copia", f"{doc}: copiado de {repo}@{sha[:7]}; lastUpdated {data}{marcador}"
    for l in langs:
        at_l, fm_l, corpo_l, origem_l = lados[l]
        if corpo_l != origem_l:
            msgs.append(f"{doc}.{l}: seções alteradas: " + (", ".join(secoes_alteradas(corpo_l, origem_l)) or "(nenhuma ## — mudança fora de seção)"))
        escritas.append((alvo_de(doc, l), monta({"lastUpdated": data, "origemCommit": sha}, origem_l)))
    if langs:
        texto += f"; {', '.join(langs)} espelhado de {', '.join(caminhos[l] for l in langs)}"
    if args.check:
        if estado == "bootstrap":
            return estado, [], msgs + [f"{texto} — rode sem `--check`"]
        # Língua espelhada já no sha da ref e com corpo ≠ origem: não é atraso, é edição à mão
        # (o corpo dela só o script escreve, ADR-010).
        editadas = [l for l in langs if lados[l][0] is not None and lados[l][1].get("origemCommit") == sha
                    and lados[l][2] != lados[l][3]]
        if editadas:
            return "divergente", [], msgs + [f"⛔ {doc}.{l}: divergente ({l} editado à mão) — corpo ≠ "
                                             f"{repo}@{sha[:7]}:{caminhos[l]}; rode sem `--check` para recopiar"
                                             for l in editadas]
        return "atras", [], msgs + [f"↻ {doc}: atrás — {repo}@{sha[:7]} tem texto novo ({data})"
                                    + (f"; {texto.removeprefix(f'{doc}: ')}" if pt_igual else "")]
    return estado, escritas, msgs + [f"↻ {texto}"]


def grava(escritas):
    """Grava [(caminho, dados)] quase atomicamente entre arquivos: escreve e faz fsync de todos os
    temporários primeiro; só então os `os.replace`. Falha antes dos replaces remove todos os
    temporários e nenhum arquivo do site muda."""
    tmps = []
    try:
        for caminho, dados in escritas:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(caminho), prefix=".sync_legal.", suffix=".tmp")
            tmps.append(tmp)
            with os.fdopen(fd, "wb") as f:
                f.write(dados)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, os.stat(caminho).st_mode & 0o777 if os.path.exists(caminho) else 0o644)
    except BaseException:
        for tmp in tmps:
            if os.path.exists(tmp):
                os.unlink(tmp)
        raise
    for (caminho, _), tmp in zip(escritas, tmps):
        os.replace(tmp, caminho)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("app", nargs="?")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--doc", choices=["privacy", "terms"])
    ap.add_argument("--ref")
    ap.add_argument("--apps-dir", default=apps_dir_padrao())
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--forca", action="store_true")
    args = ap.parse_args(argv)

    apps = sorted({d.rsplit("-", 1)[0] for d in ORIGENS})
    if args.todos == bool(args.app):
        ap.error(f"diga um app ({' | '.join(apps)}) ou --todos")
    docs = [d for d in ORIGENS if args.todos or d.rsplit("-", 1)[0] == args.app]
    if args.doc:
        docs = [d for d in docs if d.endswith("-" + args.doc)]
    if not docs:
        ap.error(f"nenhum doc para {args.app or '--todos'} {args.doc or ''} — apps: {', '.join(apps)}")

    aviso_hotfix()
    planos = []
    try:
        for doc in docs:
            alvo = alvo_de(doc, "pt")
            for lado in [alvo] + [alvo_de(doc, l) for l in espelhadas(doc)]:
                if not args.check and os.path.exists(lado) and sujo(lado):
                    raise Recusa(f"{doc}: {os.path.relpath(lado, REPO)} tem modificação não commitada — commite ou descarte antes do sync")
            planos.append((doc, alvo) + planeja(doc, args))
    except Recusa as e:
        print(f"❌ recusado, nada escrito: {e}")
        return 2

    if not args.check:
        grava([e for _, _, _, escritas, _ in planos for e in escritas])
    para_fazer = False
    for doc, alvo, estado, escritas, msgs in planos:
        for m in msgs:
            print(m)
        if estado in ("atras", "divergente"):
            para_fazer = True
        if estado == "bootstrap" and args.check:
            para_fazer = True
        if estado == "ausente":
            continue
        # O commit que fica registrado (o novo, se escreveu; senão o do arquivo).
        dados = dict(escritas).get(alvo)
        if dados is not None and not args.check:
            fm = separa(dados)[0]
        elif os.path.exists(alvo):
            with open(alvo, "rb") as f:
                fm = separa(f.read())[0]
        else:
            fm = None
        registrado = (fm or {}).get("origemCommit")
        repo = ORIGENS[doc][0]
        if registrado and RE_SHA.match(registrado) and not em_remoto(os.path.join(args.apps_dir, repo), registrado):
            print(f"⚠️  {doc}: origemCommit {registrado[:7]} não está em nenhum remoto de {repo} — "
                  "texto publicado de commit que só existe na sua máquina")
    if args.check and para_fazer:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
