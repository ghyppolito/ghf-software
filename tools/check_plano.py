#!/usr/bin/env python3
"""Verifica a consistência do backlog em .claude/context/.

Roda no /verify e, a partir do WP-05, no CI do PR. Copiado do lotto-expert (D6). Falha com código 1 se encontrar
inconsistência. Consistência por
construção, não por vigilância.

Checa:
  1. front-matter válido (id = nome do arquivo, status/area/tamanho/risco em faixa)
  2. toda dependência aponta para um WP existente, sem ciclo
  3. todo ADR citado existe em decisions/; todo `spec:` citado existe em docs/
  4. toda decisão citada existe em decisoes.md (aviso se ainda estiver em aberto)
  5. ESTADO.md lista exatamente os WPs existentes, com o mesmo status
  6. todo link relativo em .claude/context/**/*.md resolve
  7. todo achado de achados-novos.md tem destino; WP de destino existe e não está `done`;
     fila de `triagem` com no máximo MAX_TRIAGEM
  8. no máximo um WP `doing` (dois é alguém que parou no meio sem registrar)
  9. nenhum .claude/context/**/*.md com marcador de conflito de merge (`<<<<<<< `/`>>>>>>> `)
"""
import glob
import os
import re
import sys

CONTEXTO = ".claude/context"
STATUS = {"todo", "doing", "blocked", "done", "adiado"}
AREAS = {"legal", "landing", "design", "infra", "seo", "docs"}
TAMANHOS = {"S", "M", "L"}
RISCOS = {"baixo", "medio", "alto"}
MAX_TRIAGEM = 10

erros, avisos = [], []


def frontmatter(texto):
    partes = texto.split("---", 2)
    return partes[1] if len(partes) > 2 else ""


def campo(fm, chave, padrao=""):
    m = re.search(rf"^{chave}: (.*?)\s*(#.*)?$", fm, re.M)
    return m.group(1).strip().strip('"') if m else padrao


def lista(fm, chave):
    return [x.strip() for x in campo(fm, chave, "[]").strip("[]").split(",") if x.strip()]


# ---------------------------------------------------------------- carregar
wps = {}
for caminho in sorted(glob.glob(f"{CONTEXTO}/wps/WP-*.md")):
    fm = frontmatter(open(caminho, encoding="utf-8").read())
    wid = campo(fm, "id")
    nome = os.path.basename(caminho)
    if not wid:
        erros.append(f"{caminho}: front-matter sem `id`")
        continue
    if not nome.startswith(wid + "-"):
        erros.append(f"{caminho}: id `{wid}` não bate com o nome do arquivo")
    dados = {
        "arquivo": caminho,
        "status": campo(fm, "status"),
        "area": campo(fm, "area"),
        "tamanho": campo(fm, "tamanho"),
        "risco": campo(fm, "risco"),
        "depende": lista(fm, "depende_de"),
        "adr": lista(fm, "adr"),
        "spec": campo(fm, "spec"),
        "decisoes": lista(fm, "decisoes"),
    }
    # ------------------------------------------------------------- 1: faixas
    for k, faixa in (("status", STATUS), ("area", AREAS), ("tamanho", TAMANHOS), ("risco", RISCOS)):
        if dados[k] not in faixa:
            erros.append(f"{wid}: `{k}: {dados[k]}` fora de {sorted(faixa)}")
    wps[wid] = dados

# ------------------------------------------------------- 2: dependências
for wid, d in wps.items():
    for dep in d["depende"]:
        if dep not in wps:
            erros.append(f"{wid}: depende de {dep}, que não existe")

VISITANDO, PRONTO = 1, 2
marca = {}


def visita(no, caminho):
    if marca.get(no) == PRONTO:
        return
    if marca.get(no) == VISITANDO:
        erros.append("CICLO de dependências: " + " → ".join(caminho + [no]))
        return
    marca[no] = VISITANDO
    for dep in wps.get(no, {}).get("depende", []):
        if dep in wps:
            visita(dep, caminho + [no])
    marca[no] = PRONTO


for wid in wps:
    visita(wid, [])

# --------------------------------------------------------- 3: ADR e spec
adrs = {os.path.basename(p)[:7] for p in glob.glob(f"{CONTEXTO}/decisions/ADR-*.md")}
for wid, d in wps.items():
    for adr in d["adr"]:
        if adr not in adrs:
            erros.append(f"{wid}: cita {adr}, que não existe em {CONTEXTO}/decisions/")
    if d["spec"] and not os.path.exists(d["spec"]):
        erros.append(f"{wid}: `spec: {d['spec']}` não existe")

# ------------------------------------------------------------ 4: decisões
decisoes_txt = open(f"{CONTEXTO}/decisoes.md", encoding="utf-8").read()
decididas = set(re.findall(r"^\| ~~(D\d+)~~", decisoes_txt, re.M))
abertas = set(re.findall(r"^\| (D\d+) \|", decisoes_txt, re.M))
for wid, d in wps.items():
    for dec in d["decisoes"]:
        if dec in decididas:
            continue
        if dec in abertas:
            if d["status"] in ("todo", "doing"):
                avisos.append(f"{wid} cita {dec}, ainda em aberto — o /wp para no pré-voo")
        else:
            erros.append(f"{wid}: cita {dec}, que não existe em decisoes.md")

# ------------------------------------------------------------- 5: ESTADO
estado = open(f"{CONTEXTO}/ESTADO.md", encoding="utf-8").read()
na_tabela = dict(re.findall(r"^\| \[(WP-\d+)\]\(wps/[^)]+\).*?\| `(\w+)` \|$", estado, re.M))
for wid in wps:
    if wid not in na_tabela:
        erros.append(f"{wid} não aparece na tabela de ESTADO.md — rode tools/gen_estado.py")
    elif na_tabela[wid] != wps[wid]["status"]:
        erros.append(f"{wid}: ESTADO.md diz `{na_tabela[wid]}`, front-matter diz `{wps[wid]['status']}` — regenere")
for wid in na_tabela:
    if wid not in wps:
        erros.append(f"ESTADO.md lista {wid}, que não tem arquivo em wps/")

# --------------------------------------------------------------- 6: links
n_links = 0
for caminho in glob.glob(f"{CONTEXTO}/**/*.md", recursive=True):
    base = os.path.dirname(caminho)
    for alvo in re.findall(r"\]\(((?:\.\.?/|wps/|decisions/)[^)#]+)\)", open(caminho, encoding="utf-8").read()):
        n_links += 1
        if not os.path.exists(os.path.normpath(os.path.join(base, alvo))):
            erros.append(f"LINK QUEBRADO em {caminho}: {alvo}")

# ------------------------------------------------------------ 7: destino
# achados-novos.md sem dono é uma fila sem saída: o agente registra e ninguém
# puxa. A última coluna diz quem é o dono. Um WP `done` não pode ser dono de
# trabalho aberto — o achado ficaria invisível de novo, com cara de resolvido.
em_triagem = 0
for n, linha in enumerate(open(f"{CONTEXTO}/achados-novos.md", encoding="utf-8"), 1):
    if not re.match(r"^\| ~{0,2}20\d\d-", linha):
        continue
    destino = re.split(r"(?<!\\)\|", linha.rstrip().rstrip("|"))[-1].strip()
    m = re.match(r"`(WP-\d+|aceito|resolvido|nota|triagem)`", destino)
    if not m:
        erros.append(f"achados-novos.md:{n}: sem destino válido na última coluna (`{destino[:40]}`)")
        continue
    alvo = m.group(1)
    if alvo == "triagem":
        em_triagem += 1
    elif alvo.startswith("WP-"):
        if alvo not in wps:
            erros.append(f"achados-novos.md:{n}: roteado para {alvo}, que não existe")
        elif wps[alvo]["status"] == "done":
            erros.append(f"achados-novos.md:{n}: roteado para {alvo}, que está `done` — reroteie")
if em_triagem > MAX_TRIAGEM:
    erros.append(f"{em_triagem} achados em `triagem` (máx. {MAX_TRIAGEM}) — rode a triagem")
elif em_triagem:
    avisos.append(f"{em_triagem} achado(s) aguardando triagem")

# -------------------------------------------------------------- 8: doing
doing = [w for w, d in wps.items() if d["status"] == "doing"]
if len(doing) > 1:
    erros.append(f"mais de um WP `doing` ({', '.join(doing)}) — um por vez; o outro é `blocked` ou `todo`")

# ----------------------------------------------------------- 9: conflito
# Um conflito de merge esquecido num WP, no ESTADO.md ou no achados-novos.md
# só era pego se quebrasse front-matter ou tabela por acaso. O espaço depois dos sete
# sinais é como o git escreve o marcador — sem ele, uma linha de documentação que
# comece com `<<<<<<<` não vira falso positivo.
for caminho in sorted(glob.glob(f"{CONTEXTO}/**/*.md", recursive=True)):
    for n, linha in enumerate(open(caminho, encoding="utf-8"), 1):
        if re.match(r"^(<<<<<<<|>>>>>>>) ", linha):
            erros.append(f"CONFLITO não resolvido em {caminho}:{n}")

# ------------------------------------------------------------- resultado
print(f"WPs: {len(wps)} | ADRs: {len(adrs)} | links verificados: {n_links}")
for a in avisos:
    print(f"⚠️  {a}")
if erros:
    print(f"\n❌ {len(erros)} inconsistência(s):\n")
    for e in erros:
        print(f"  • {e}")
    sys.exit(1)
print("✅ plano consistente")
