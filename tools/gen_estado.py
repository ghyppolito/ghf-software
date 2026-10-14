#!/usr/bin/env python3
"""Gera .claude/context/ESTADO.md a partir dos front-matters dos WPs.

O front-matter de cada WP é a **fonte de verdade** do status; o ESTADO.md é uma
visão gerada. Rode depois de alterar qualquer `status:` e faça commit dos dois.
`python3 tools/gen_estado.py --check` só compara e falha se o arquivo estiver
desatualizado (é o que o CI roda a partir do WP-05).

Mesmo desenho do lotto-expert e do personal-trader (D6).
"""
import glob
import os
import re
import sys

CONTEXTO = ".claude/context"

# Sequência recomendada. Escrita à mão de propósito: a ordem é decisão de produto,
# não derivável do grafo — o grafo só diz o que é *possível*. WP `done` some
# sozinho da tabela; dependência não-`done` aparece como aviso.
SEQUENCIA = [
    ("A · LottoExpert 2.05.02 — publicar política, termos e landing antes de qualquer evolução do site", [
        ("WP-01", "política de privacidade e termos de uso do LottoExpert estão em 23/07/2026 no site e em 12/10/2026 no app (`../lotto-expert/docs/`, commit b5d4ca6): Teimosinha, prestação de contas, premium 14 dias, restauração, Gson, 'Termos de Uso'. Texto legal, risco alto — espelha, não redige"),
        ("WP-02", "landing do LottoExpert não cita Teimosinha nem prestação de contas do bolão; D1 decide o que destacar. Copy sob a régua de jogo responsável (`check_site.py`)"),
        ("WP-04", "OG image do convite de bolão aponta para `logo_transp.png`, que não existe — convite sai sem imagem no WhatsApp; ampliado (2026-10-12): política do Pole Position espelhada do app (setembro/2026, `POST_NOTIFICATIONS`). S, risco alto (legal), entra na mesma publicação"),
        ("WP-03", "publicar `develop → master` (Pages): 10 commits de TopoWalk/Pole Position já esperam + WP-01/02/04. Só o usuário mescla; o agente prepara e confere"),
    ]),
    ("B · fundação — rede de segurança, build e fonte única, nesta ordem", [
            ("WP-07", "stack com build (D2, recomendada Astro): spike que prova URLs contratuais preservadas, `.well-known` e convite intactos, deploy do Pages por Actions; ADR-002. L, risco alto"),
        ("WP-08", "migração das 10 páginas para layout e componentes únicos (nav, footer, tema, i18n por rota `/en/`); conteúdo legal em markdown renderizado. L, depois do WP-07"),
        ("WP-09", "legal como fonte única: `tools/sync_legal.py` importa do repositório do app, data no front-matter, CI acusa divergência. M, depois do WP-08"),
        ("WP-14", "README e `docs/ARQUITETURA.md` refletem a stack nova; `CLAUDE.md` seção Comandos atualizada. S, fecha a trilha B"),
    ]),
    ("C · evolução — design, SEO, performance e medição; WP-06 e WP-19 podem rodar a qualquer momento (são sessões do usuário no Claude Design)", [
        ("WP-06", "brief de design (`design/BRIEF.md`) e sessão no Claude Design (D4): tokens, nav, footer, hero, card de app, seção de features, página legal; export em `design/handoff/<data>/`. Independe da stack"),
        ("WP-19", "export da rodada 3 entregue e auditado; falta o usuário: checklist de navegador da rodada 3 (visual: true)"),
        ("WP-10", "redesign da home e das landings de app com o handoff: hierarquia por app, anatomia única de landing, página legal legível. L, depois do WP-06 e WP-08"),
        ("WP-11", "SEO técnico: sitemap, robots, canonical, hreflang pt/en, JSON-LD (Organization, MobileApplication), OG por página. M, depois do WP-08"),
        ("WP-15", "i18n N-línguas: mapa único página → línguas (`src/i18n/idiomas.ts`), pt na raiz e demais em `/<lang>/`, seletor só com as línguas da página, hreflang/x-default das existentes, check_site compara data, seções e tokens entre versões legais; não publica língua nova. D8, ADR-003. M, risco alto, depois do WP-11"),
        ("WP-16", "política do Pole Position em pt/en/es/fr/it/de, traduzida do pt de origem; pré-condição: cláusula de prevalência do pt no app (D8 b1, `PREVALENCIA-PT-NOS-APPS-01`); o espelho pt fica em dia no WP-04. Texto legal, risco alto — prova o processo na política menor"),
        ("WP-17", "política do TopoWalk em pt/en/es/fr/it/de/ru (5.842 palavras × 6 línguas além do pt); PR por língua. L, risco alto, depois do WP-16"),
        ("WP-18", "landings TopoWalk (7 línguas) e Pole Position (6) com copy das fichas da Play; só se D8 (a2/a3), depois do WP-10 para não traduzir duas vezes"),
        ("WP-12", "performance: fontes self-hosted, ícones SVG inline no lugar do Font Awesome, imagens WebP/AVIF com dimensões, Lighthouse ≥ 90 nas 4 categorias em todas as páginas. M, depois do WP-08"),
        ("WP-13", "medição com consentimento ou sem cookie (D3: Plausible/Umami vs GA4 Consent Mode); evento de clique na Play por app. M, depois do WP-08"),
    ]),
]

# Bloqueios ativos: (WP, motivo, desde). Lista escrita à mão; entrada de WP `done`
# é filtrada, para a tabela seguir o front-matter.
BLOQUEIOS = [
    ("WP-19", "export da rodada 3 entregue e auditado; falta o usuário: checklist de navegador da rodada 3 (visual: true)", "2026-10-13"),
]

wps = []
for caminho in glob.glob(f"{CONTEXTO}/wps/WP-*.md"):
    fm = open(caminho, encoding="utf-8").read().split("---", 2)[1]

    def g(k, d=""):
        m = re.search(rf"^{k}: (.*?)\s*(#.*)?$", fm, re.M)
        return m.group(1).strip().strip('"') if m else d

    def lista(k):
        return [x.strip() for x in g(k, "[]").strip("[]").split(",") if x.strip()]

    wps.append({
        "id": g("id"), "n": int(g("id").split("-")[1]), "tit": g("titulo"),
        "area": g("area"), "status": g("status"), "tam": g("tamanho"),
        "risco": g("risco"), "visual": g("visual") == "true",
        "dep": lista("depende_de"), "adr": lista("adr"),
        "arq": os.path.basename(caminho),
    })
wps.sort(key=lambda r: r["n"])
por_id = {r["id"]: r for r in wps}

L = [
    "# Estado da execução", "",
    "> **Gerado por `tools/gen_estado.py`.** A fonte de verdade do status é o",
    "> front-matter de cada WP em `wps/` — altere lá e regenere este arquivo.",
    "> Status: `todo` · `doing` · `blocked` · `done` · `adiado`", "",
    f"**{len(wps)} WPs** · {sum(1 for r in wps if r['status'] == 'done')} concluídos · "
    f"{sum(1 for r in wps if r['status'] == 'doing')} em andamento", "",
    "## Sequência recomendada", "",
    "Próximo WP = o primeiro da trilha A cujas dependências estejam `done`. "
    "Reordenar é decisão do usuário (`SEQUENCIA` em `tools/gen_estado.py`).", "",
]
for trilha, itens in SEQUENCIA:
    L += [f"**{trilha}**", "", "| # | WP | Status | Nota |", "|---|---|---|---|"]
    n = 0
    for wid, nota in itens:
        r = por_id[wid]
        if r["status"] == "done":
            continue
        n += 1
        pend = [d for d in r["dep"] if d in por_id and por_id[d]["status"] != "done"]
        if pend:
            nota += f" · ⏳ aguarda {', '.join(pend)}"
        L.append(f"| {n} | [{wid} — {r['tit']}](wps/{r['arq']}) | `{r['status']}` | {nota} |")
    L.append("")

L += ["## Todos os WPs", "",
      "| WP | Título | Área | Tam | Risco | Visual | Depende de | ADR | Status |",
      "|---|---|---|---|---|---|---|---|---|"]
for r in wps:
    L.append(f"| [{r['id']}](wps/{r['arq']}) | {r['tit']} | {r['area']} | {r['tam']} | {r['risco']} | "
             f"{'🖥️' if r['visual'] else ''} | {', '.join(r['dep']) or '—'} | "
             f"{', '.join(r['adr']) or '—'} | `{r['status']}` |")

L += ["", "## Bloqueios ativos", "", "| WP | Bloqueado por | Desde |", "|---|---|---|"]
for wid, motivo, desde in BLOQUEIOS:
    if por_id.get(wid, {}).get("status") == "done":
        continue
    L.append(f"| {wid} | {motivo} | {desde} |")
L.append("")

novo = "\n".join(L)
destino = f"{CONTEXTO}/ESTADO.md"
if "--check" in sys.argv:
    atual = open(destino, encoding="utf-8").read() if os.path.exists(destino) else ""
    if atual != novo:
        print(f"❌ {destino} desatualizado — rode `python3 tools/gen_estado.py` e commite")
        sys.exit(1)
    print(f"✅ {destino} em dia ({len(wps)} WPs)")
else:
    open(destino, "w", encoding="utf-8").write(novo)
    print(f"ESTADO.md: {len(wps)} WPs")
