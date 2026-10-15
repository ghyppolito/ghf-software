#!/usr/bin/env python3
"""Espelha o texto legal do repositório do app no site (ADR-004, D7, D14).

Só biblioteca padrão, de propósito. Copia o corpo de `PRIVACY_POLICY.md`/`TERMS_OF_SERVICE.md`
de um **commit** do app (`git show <sha>:<caminho>`, nunca o disco) para
`src/content/legal/<app>-<doc>.pt.md`, byte a byte, com o front-matter:

    ---
    lastUpdated: "AAAA-MM[-DD]"
    origemCommit: "<sha de 40>"
    en: "pendente"
    ---

Nunca abre nem escreve `.en.md`: a tradução é do `site-legal`, que tira a linha `en: "pendente"`
depois. O `check_site.py` importa `ORIGENS` daqui e confere o corpo contra `origemCommit`.

Uso:
    python3 tools/sync_legal.py <app>|--todos [--doc privacy|terms] [--ref REF]
                                [--apps-dir DIR] [--check] [--forca]

  <app>        lottoexpert | topowalk | poleposition | eclipsego
  --ref        branch, tag ou sha do app (padrão: a ref de ORIGENS, D14)
  --apps-dir   pasta onde estão os repositórios dos apps (padrão: $GHF_APPS_DIR ou `..` do site)
  --check      não escreve; diz igual / atrás / à frente-divergente / origem ausente por doc
  --forca      copia mesmo quando o origemCommit registrado não é ancestral da ref

Saída: 0 = nada a fazer ou cópia feita (ou origem ausente, com aviso); 1 = `--check` achou o que
fazer; 2 = recusa (nada foi escrito).
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGAL_DIR = os.path.join("src", "content", "legal")

# Tabela única: doc do site (`<app>-<doc>`, nome do `.pt.md` sem a extensão) → (repositório do app
# relativo a --apps-dir, caminho do .md dentro dele, ref padrão = branch principal do app, D14).
# O `/legal` cita esta tabela; o `check_site.py` exige que ela cubra exatamente o LEGAL dele.
ORIGENS = {
    "lottoexpert-privacy": ("lotto-expert", "docs/PRIVACY_POLICY.md", "master"),
    "lottoexpert-terms": ("lotto-expert", "docs/TERMS_OF_SERVICE.md", "master"),
    "topowalk-privacy": ("topo-walk", "PRIVACY_POLICY.md", "master"),
    "poleposition-privacy": ("pole-position/pole-position-app", "PRIVACY_POLICY.md", "master"),
    "eclipsego-privacy": ("eclipse-go", "docs/PRIVACY_POLICY.md", "main"),
}

CHAVES = ("lastUpdated", "origemCommit", "en")
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
    """(front-matter como dict ordenado, lista de chaves, corpo em bytes) de um `.pt.md`/`.en.md`.
    None no front-matter se o arquivo não começa com `---\\n … \\n---\\n`. Chave fora do formato
    `chave: "valor"` vira chave com valor None (quem chama recusa)."""
    m = re.match(rb"---\n(.*?)\n---\n", dados, re.S)
    if not m:
        return None, [], dados
    fm, chaves = {}, []
    for linha in m.group(1).decode("utf-8").split("\n"):
        kv = re.match(r'^([^:\s]+):\s*"([^"]*)"\s*$', linha)
        if kv:
            fm[kv.group(1)] = kv.group(2)
            chaves.append(kv.group(1))
        else:
            chave = linha.split(":", 1)[0].strip() or linha
            fm[chave] = None
            chaves.append(chave)
    return fm, chaves, dados[m.end():]


def monta(fm, corpo):
    linhas = ["---"] + [f'{k}: "{fm[k]}"' for k in CHAVES if fm.get(k) is not None] + ["---", ""]
    return "\n".join(linhas).encode("utf-8") + corpo


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


def planeja(doc, args):
    """Decide o que fazer com um doc. Devolve (estado, conteúdo novo ou None, mensagens)."""
    repo, caminho, ref_padrao = ORIGENS[doc]
    ref = args.ref or ref_padrao
    repo_dir = os.path.join(args.apps_dir, repo)
    alvo = os.path.join(REPO, LEGAL_DIR, f"{doc}.pt.md")
    msgs = []

    if not repo_presente(args.apps_dir, repo):
        return "ausente", None, [f"⚠️  {doc}: origem ausente ({repo_dir}) — nada a comparar, nada escrito"]

    sha = resolve(repo_dir, ref)
    if sha is None:
        raise Recusa(f"{doc}: ref `{ref}` não existe em {repo}")
    origem = mostra(repo_dir, sha, caminho)  # None se o arquivo não existe na ref (vê abaixo)
    msgs.append(f"{doc}: origem {repo}@{ref} = {sha}")

    if os.path.exists(alvo):
        with open(alvo, "rb") as f:
            atual = f.read()
        fm, chaves, corpo = separa(atual)
        if fm is None:
            raise Recusa(f"{doc}: {os.path.relpath(alvo, REPO)} sem front-matter `---` no topo")
        estranhas = [k for k in chaves if k not in CHAVES or fm[k] is None]
        if estranhas or len(chaves) != len(set(chaves)):
            raise Recusa(f"{doc}: front-matter com chave fora de {{{', '.join(CHAVES)}}} ou repetida: {chaves}")
    else:
        atual, fm, corpo = None, {}, b""
    registrado = fm.get("origemCommit")
    if registrado is not None and not RE_SHA.match(registrado):
        raise Recusa(f"{doc}: origemCommit `{registrado}` não é sha de 40 hex minúsculos")
    if registrado and resolve(repo_dir, registrado) is None:
        raise Recusa(f"{doc}: origemCommit {registrado[:7]} não existe em {repo} — `git fetch` no app ou origemCommit inventado")

    if origem is not None and atual is not None and corpo == origem:
        if registrado:
            return "igual", None, msgs + [f"✅ {doc}: nada a fazer ({repo}@{sha[:7]})"]
        novo = dict(fm, origemCommit=sha)
        return "bootstrap", monta(novo, corpo), msgs + [f"{doc}: corpo igual a {repo}@{sha[:7]}; falta origemCommit (bootstrap: só o front-matter)"]

    # Corpo diferente.
    if registrado and not ancestral(repo_dir, registrado, sha):
        texto = (f"{doc}: à frente/divergente — o origemCommit {registrado[:7]} não é ancestral de "
                 f"{ref} ({sha[:7]}); copiar desfaria texto publicado")
        if not args.forca:
            if args.check:
                return "divergente", None, msgs + [f"⛔ {texto}. Escolha a ref (`--ref`) ou use `--forca`"]
            raise Recusa(texto + " — escolha a ref (`--ref`) ou use `--forca`")
        msgs.append(f"⚠️  {texto} — `--forca`, copiando mesmo assim")
    elif atual is not None and not registrado:
        texto = f"{doc}: sem origemCommit e corpo ≠ {repo}@{sha[:7]} — não há como saber se é atraso ou edição"
        if not args.forca:
            if args.check:
                return "divergente", None, msgs + [f"⛔ {texto}"]
            raise Recusa(texto + " — rode com `--ref` do commit que o site espelha, ou `--forca`")
        msgs.append(f"⚠️  {texto} — `--forca`, copiando mesmo assim")
    if origem is None:
        raise Recusa(f"{doc}: {caminho} não existe em {repo}@{sha[:7]}")

    data = data_da_origem(origem)
    msgs.append(f"{doc}: seções alteradas: " + (", ".join(secoes_alteradas(corpo, origem)) or "(nenhuma ## — mudança fora de seção)"))
    if atual is not None and fm.get("lastUpdated") == data:
        msgs.append(f"⚠️  {doc}: texto mudou sem data nova ({data}) — achado para o repositório do app")
    if args.check:
        return "atras", None, msgs + [f"↻ {doc}: atrás — {repo}@{sha[:7]} tem texto novo ({data})"]
    novo = {"lastUpdated": data, "origemCommit": sha, "en": "pendente"}
    return "copia", monta(novo, origem), msgs + [f"↻ {doc}: copiado de {repo}@{sha[:7]}; lastUpdated {data}; en pendente"]


def grava(caminho, dados):
    pasta = os.path.dirname(caminho)
    fd, tmp = tempfile.mkstemp(dir=pasta, prefix=".sync_legal.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(dados)
        if os.path.exists(caminho):
            os.chmod(tmp, os.stat(caminho).st_mode & 0o777)
        else:
            os.chmod(tmp, 0o644)
        os.replace(tmp, caminho)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


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
            alvo = os.path.join(REPO, LEGAL_DIR, f"{doc}.pt.md")
            if not args.check and os.path.exists(alvo) and sujo(alvo):
                raise Recusa(f"{doc}: {os.path.relpath(alvo, REPO)} tem modificação não commitada — commite ou descarte antes do sync")
            planos.append((doc, alvo) + planeja(doc, args))
    except Recusa as e:
        print(f"❌ recusado, nada escrito: {e}")
        return 2

    para_fazer = False
    for doc, alvo, estado, dados, msgs in planos:
        for m in msgs:
            print(m)
        if estado in ("atras", "divergente"):
            para_fazer = True
        if dados is not None and not args.check:
            grava(alvo, dados)
        if estado == "bootstrap" and args.check:
            para_fazer = True
        if estado == "ausente":
            continue
        # O commit que fica registrado (o novo, se escreveu; senão o do arquivo).
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
