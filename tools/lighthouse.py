#!/usr/bin/env python3
"""Lighthouse no PR (WP-12, D20 B) — orçamento de desempenho sobre `dist/`.

Só biblioteca padrão, de propósito; o `lighthouse` é o do lockfile (13.5.0 exato, `npx`). Serve
`dist/` com o mesmo servidor da medição do WP-12 (`http.server`, sem gzip), roda o Lighthouse
mobile (padrão: throttling simulado) N vezes em cada página de `tools/orcamento-lighthouse.json`
e confere a mediana — a run do meio pela nota de performance, como na tabela do WP. Falha com
código 1 se encontrar erro.

Regras (veredito do WP-12 §7):
  erro  — acessibilidade, boas práticas e SEO < 0,90 (onde `seo: false`, a 404, que é `noindex`
          de propósito, a nota não conta, mas nenhuma auditoria de SEO além de `is-crawlable` pode
          reprovar); performance < 0,85; LCP > 3,0 s; CLS > 0,1; requisição a outra origem em
          qualquer run; bytes totais ou bytes de imagem acima do orçamento da página
  aviso — performance < 0,90; LCP > 2,5 s
A folga entre erro e aviso é a variação do runner (até 10 pontos nas páginas leves). Bytes e
terceiros não variam entre runs: são eles que pegam a regressão de verdade.

O orçamento em bytes é o medido no fechamento do WP-12 + 20%. Mudou uma página de propósito?
`--medir` imprime os bytes de cada uma; o novo número entra no JSON no mesmo PR.

Uso: python3 tools/lighthouse.py [--raiz dist] [--runs 3] [--medir]
"""
import functools
import http.server
import json
import os
import statistics
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlsplit

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORCAMENTO = os.path.join(RAIZ_REPO, "tools", "orcamento-lighthouse.json")

raiz = "dist"
if "--raiz" in sys.argv:
    raiz = sys.argv[sys.argv.index("--raiz") + 1]
runs = 3
if "--runs" in sys.argv:
    runs = int(sys.argv[sys.argv.index("--runs") + 1])
if runs < 1:
    print("❌ --runs precisa ser 1 ou mais")
    sys.exit(1)
medir = "--medir" in sys.argv
if not os.path.isdir(raiz):
    print(f"❌ {raiz}/ não existe — rode `npm run build`")
    sys.exit(1)

with open(ORCAMENTO, encoding="utf-8") as f:
    orcamento = json.load(f)
regras = orcamento["regras"]


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


servidor = http.server.ThreadingHTTPServer(
    ("127.0.0.1", 0), functools.partial(Silencioso, directory=os.path.abspath(raiz)))
threading.Thread(target=servidor.serve_forever, daemon=True).start()
origem = f"http://127.0.0.1:{servidor.server_address[1]}"


def lighthouse(url, saida):
    # Um Chrome travado não pode gastar o timeout do job inteiro sem dizer em que página parou.
    try:
        r = subprocess.run(
            ["npx", "--no-install", "lighthouse", url, "--output=json", f"--output-path={saida}",
             "--quiet", "--chrome-flags=--headless=new --no-sandbox"],
            cwd=RAIZ_REPO, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"lighthouse passou de 120 s em {url}")
    if r.returncode != 0 or not os.path.isfile(saida):
        raise RuntimeError(f"lighthouse falhou em {url}:\n{r.stderr[-2000:]}")
    with open(saida, encoding="utf-8") as f:
        return json.load(f)


def nota(rel, cat):
    s = rel["categories"][cat]["score"]
    return 0.0 if s is None else s


erros, avisos, linhas = [], [], []
with tempfile.TemporaryDirectory() as tmp:
    for n, (caminho, pagina) in enumerate(orcamento["paginas"].items()):
        # um arquivo por run: nunca se lê o relatório de outra página
        relatorios = [lighthouse(origem + caminho, os.path.join(tmp, f"{n}-{i}.json")) for i in range(runs)]
        perfs = [nota(r, "performance") for r in relatorios]
        m = relatorios[perfs.index(statistics.median_low(perfs))]
        a = m["audits"]
        reqs = a["network-requests"]["details"]["items"]
        total = sum(r.get("transferSize", 0) for r in reqs)
        imagem = sum(r.get("transferSize", 0) for r in reqs if r.get("resourceType") == "Image")
        lcp = a["largest-contentful-paint"]["numericValue"]
        cls = a["cumulative-layout-shift"]["numericValue"]
        cats = {c: nota(m, c) for c in ("performance", "accessibility", "best-practices", "seo")}
        linhas.append(f"{caminho:28} perf {cats['performance']*100:3.0f} ({min(perfs)*100:.0f}–{max(perfs)*100:.0f})"
                      f" · a11y {cats['accessibility']*100:3.0f} · bp {cats['best-practices']*100:3.0f}"
                      f" · seo {cats['seo']*100:3.0f} · LCP {lcp/1000:.2f} s · CLS {cls:.3f}"
                      f" · {total/1024:.0f} KB (img {imagem/1024:.0f} KB)")

        if not pagina.get("seo", True):
            reprovadas = sorted(ref["id"] for ref in m["categories"]["seo"]["auditRefs"]
                                if ref["weight"] and a[ref["id"]]["score"] is not None
                                and a[ref["id"]]["score"] < 1 and ref["id"] != "is-crawlable")
            for aud in reprovadas:
                erros.append(f"{caminho}: SEO reprovada em {aud} (só is-crawlable é esperada, ADR-005 §4)")
        for cat in ("accessibility", "best-practices", "seo"):
            if cat == "seo" and not pagina.get("seo", True):
                continue
            if cats[cat] < regras["categoria_min"]:
                erros.append(f"{caminho}: {cat} {cats[cat]*100:.0f} < {regras['categoria_min']*100:.0f}")
        if cats["performance"] < regras["performance_erro"]:
            erros.append(f"{caminho}: performance {cats['performance']*100:.0f} < {regras['performance_erro']*100:.0f}")
        elif cats["performance"] < regras["performance_aviso"]:
            avisos.append(f"{caminho}: performance {cats['performance']*100:.0f} < {regras['performance_aviso']*100:.0f}")
        if lcp > regras["lcp_erro_ms"]:
            erros.append(f"{caminho}: LCP {lcp/1000:.2f} s > {regras['lcp_erro_ms']/1000} s")
        elif lcp > regras["lcp_aviso_ms"]:
            avisos.append(f"{caminho}: LCP {lcp/1000:.2f} s > {regras['lcp_aviso_ms']/1000} s")
        if cls > regras["cls_max"]:
            erros.append(f"{caminho}: CLS {cls:.3f} > {regras['cls_max']}")
        terceiros = sorted({r["url"] for rel in relatorios
                            for r in rel["audits"]["network-requests"]["details"]["items"]
                            if urlsplit(r["url"]).scheme in ("http", "https")
                            and not r["url"].startswith(origem + "/")})
        for u in terceiros:
            erros.append(f"{caminho}: requisição a outra origem — {u} (ADR-006)")
        if not medir:
            if total > pagina["bytes_total"]:
                erros.append(f"{caminho}: {total} bytes no total > orçamento {pagina['bytes_total']}")
            if imagem > pagina["bytes_imagem"]:
                erros.append(f"{caminho}: {imagem} bytes de imagem > orçamento {pagina['bytes_imagem']}")
        else:
            linhas.append(f"{'':28} medido: bytes_total {total} · bytes_imagem {imagem}"
                          f" (+20%: {round(total*1.2)} · {round(imagem*1.2)})")

servidor.shutdown()
print(f"Lighthouse {runs}× por página, mediana pela performance, {origem} servindo {raiz}/\n")
for linha in linhas:
    print(linha)
print()
for a in avisos:
    print(f"⚠️  {a}")
if erros:
    print(f"\n❌ {len(erros)} erro(s):\n")
    for e in erros:
        print(f"  • {e}")
    sys.exit(1)
print("✅ orçamento cumprido")
