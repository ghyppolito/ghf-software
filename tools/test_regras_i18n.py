#!/usr/bin/env python3
"""Prova as regras de i18n de tools/regras_i18n.py sobre os casos de tools/fixtures/i18n/ (WP-15).

Só biblioteca padrão (unittest). Rodar da raiz do repositório:

    python3 -m unittest tools/test_regras_i18n.py

Cada caso é uma pasta de tools/fixtures/i18n/ que sobrepõe arquivos ao caso `correto/`: o caso
traz só o que muda, e o resto vem do correto. Arquivos de um caso:
  idiomas.json      o mapa (mesmo formato de src/i18n/idiomas.json)
  legal/<doc>.<código>.md   texto legal com front-matter, uma por língua da página `<doc>.html`
  dist.txt          a lista de arquivos de um dist/ (um caminho por linha)
  hreflang.json     {arquivo de dist/: [[hreflang, href], …]} lidos do <head>
  ui.ts             dicionário no formato de src/i18n/ui.ts
  publicadas.txt    a lista fixa PUBLICADAS do check_site.py

O correto passa sem erro; cada caso inválido falha, e só com a mensagem da regra dele.
"""
import json
import os
import sys
import unittest

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import regras_i18n as i18n  # noqa: E402
from sync_legal import separa  # noqa: E402

FIXTURES = os.path.join(AQUI, "fixtures", "i18n")
SITE = "https://ghfsoftware.com/"
FORA_DO_MAPA = ["lotto-expert/sweepstake-invite/lottoexpert-invite.html"]

# caso inválido → trecho que toda mensagem de erro dele tem
CASOS = {
    "data-divergente": "(regra i)",
    "linha-de-data-errada": "linha de data",
    "h3-fora-de-ordem": "(regra ii)",
    "token-ausente": "`POST_NOTIFICATIONS` 0× ≠ 1× no pt (regra iii)",
    "sdk-ausente": "sem `Firebase Analytics`, que o pt cita (regra iv)",
    "lingua-sem-arquivo": "es/app-privacy.html: ausente",
    "ru-fora-do-mapa": "ru/app-privacy.html: `ru` fora do mapa",
    "pt-na-pasta": "pt/app-privacy.html: `pt/` não existe",
    "pendente": "app-privacy.pt.md: `pendente: ['es']`",
    "origem-na-traducao": "app-privacy.en.md: `origemCommit` na tradução",
    "hreflang-sem-x-default": "es/app-privacy.html: hreflang",
    "ui-sem-bloco": "ui.ts: sem bloco `es`",
    "guarda": "app.html está em PUBLICADAS e falta em `paginas` (regra xii)",
}


def arquivo_do_caso(caso, nome):
    """O arquivo do caso, ou o do `correto/` quando o caso não o sobrepõe."""
    proprio = os.path.join(FIXTURES, caso, nome)
    return proprio if os.path.exists(proprio) else os.path.join(FIXTURES, "correto", nome)


def ler(caso, nome):
    with open(arquivo_do_caso(caso, nome), encoding="utf-8") as f:
        return f.read()


def linhas(caso, nome):
    return [x.strip() for x in ler(caso, nome).splitlines() if x.strip()]


def verifica(caso):
    """Todas as regras de regras_i18n.py sobre um caso, na ordem do check_site.py."""
    mapa = json.loads(ler(caso, "idiomas.json"))
    erros = i18n.valida_mapa(mapa)
    # legais: (i), (vii), linha de data, (ii), (iii), (iv)
    docs = sorted({n.split(".")[0] for n in os.listdir(os.path.join(FIXTURES, "correto", "legal"))})
    for doc in docs:
        linguas = mapa["paginas"].get(doc + ".html", ["pt"])
        textos, fms = {}, {}
        for l in linguas:
            nome = f"legal/{doc}.{l}.md"
            with open(arquivo_do_caso(caso, nome), "rb") as f:
                fm, _, corpo = separa(f.read())
            fms[l], textos[l] = fm, corpo.decode("utf-8")
        erros += i18n.regra_datas(doc, {l: fm.get("lastUpdated") for l, fm in fms.items()})
        erros += i18n.regra_front_matter(doc, fms)
        ano, mes, *dia = fms["pt"]["lastUpdated"].split("-")
        for l in linguas:
            d = mapa["idiomas"][l]
            erros += i18n.regra_linha_data(f"{doc}.{l}.md", textos[l], d["rotuloData"], d["meses"],
                                           ano, int(mes), dia[0] if dia else "")
        erros += i18n.regra_titulos(doc, textos)
        erros += i18n.regra_tokens(doc, textos)
        erros += i18n.regra_sdks(doc, textos)
    # arquivos: (v), (vi), (xii)
    arquivos = set(linhas(caso, "dist.txt"))
    erros += i18n.regra_arquivos_gerados(mapa, arquivos)
    erros += i18n.regra_linguas_fora_do_mapa(mapa, arquivos)
    erros += i18n.regra_guarda(mapa, linhas(caso, "publicadas.txt"), FORA_DO_MAPA)
    # (viii)
    for rel, alternates in json.loads(ler(caso, "hreflang.json")).items():
        erros += i18n.regra_hreflang(mapa, rel, [tuple(x) for x in alternates], SITE)
    # (xi)
    erros += i18n.regra_dicionario("ui.ts", ler(caso, "ui.ts"), mapa, eh_ui=True)
    return erros


class RegrasI18n(unittest.TestCase):
    def test_correto_passa(self):
        self.assertEqual(verifica("correto"), [])

    def test_cada_caso_falha_pela_sua_regra(self):
        pastas = sorted(n for n in os.listdir(FIXTURES) if n != "correto")
        self.assertEqual(pastas, sorted(CASOS), "pasta de tools/fixtures/i18n/ sem entrada em CASOS (ou o contrário)")
        for caso, trecho in sorted(CASOS.items()):
            with self.subTest(caso=caso):
                erros = verifica(caso)
                # a saída do -v mostra a mensagem que cada caso produziu
                for e in erros:
                    print(f"\n  [{caso}] {e}", end="", file=sys.stderr)
                self.assertTrue(erros, f"{caso}: nenhuma regra falhou")
                for e in erros:
                    self.assertIn(trecho, e, f"{caso}: falhou por outra regra")

    def test_data_em_qualquer_lingua(self):
        meses_pt = json.loads(ler("correto", "idiomas.json"))["idiomas"]["pt"]["meses"]
        meses_en = json.loads(ler("correto", "idiomas.json"))["idiomas"]["en"]["meses"]
        self.assertTrue(i18n.confere_data("13 de julho de 2026", meses_pt, "2026", "07", "13"))
        self.assertTrue(i18n.confere_data("July 13, 2026", meses_en, "2026", "07", "13"))
        self.assertTrue(i18n.confere_data("October 2026", meses_en, "2026", "10", ""))
        self.assertFalse(i18n.confere_data("July 14, 2026", meses_en, "2026", "07", "13"))
        self.assertFalse(i18n.confere_data("13 de junho de 2026", meses_pt, "2026", "07", "13"))
        self.assertFalse(i18n.confere_data("1 October 2026", meses_en, "2026", "10", ""))

    def test_hreflang_sem_en_aponta_para_pt(self):
        mapa = json.loads(ler("correto", "idiomas.json"))
        mapa["paginas"]["so-es.html"] = ["pt", "es"]
        esperado = i18n.hreflang_esperado(mapa, "so-es.html", SITE)
        self.assertEqual(esperado["x-default"], SITE + "so-es.html")
        self.assertEqual(i18n.hreflang_esperado(mapa, "index.html", SITE), {})


    def test_link_d23(self):
        mapa = json.loads(ler("correto", "idiomas.json"))
        mapa["paginas"]["tres.html"] = ["pt", "en", "es"]
        mapa["paginas"]["so-pt.html"] = ["pt"]
        mapa["paginas"]["pt-es.html"] = ["pt", "es"]
        mapa["paginas"]["index.html"] = ["pt", "en"]
        mapa["idiomas"]["es"] = dict(mapa["idiomas"]["en"], hreflang="es")
        self.assertEqual(i18n.lingua_do_link(mapa, "es", "tres.html"), "es")
        self.assertEqual(i18n.lingua_do_link(mapa, "es", "index.html"), "en")
        self.assertEqual(i18n.lingua_do_link(mapa, "es", "so-pt.html"), "pt")
        self.assertEqual(i18n.lingua_do_link(mapa, "en", "pt-es.html"), "pt")
        ok = i18n.regra_link
        # mesma língua: sem atributo
        self.assertEqual(ok(mapa, "es/tres.html", "/es/tres.html", "es/tres.html", '<a href="/es/tres.html">'), [])
        # fallback para en com hreflang e lang
        self.assertEqual(ok(mapa, "es/tres.html", "/en/", "en/index.html",
                            '<a href="/en/" hreflang="en" lang="en">'), [])
        self.assertIn("sem `hreflang=", ok(mapa, "es/tres.html", "/en/", "en/index.html", '<a href="/en/">')[0])
        # fallback errado (pt quando há en) e língua errada (pt quando há es)
        self.assertIn("esperado /en/index.html", ok(mapa, "es/tres.html", "/", "index.html",
                                                    '<a href="/" hreflang="pt-BR" lang="pt-BR">')[0])
        self.assertIn("esperado /es/tres.html", ok(mapa, "es/tres.html", "/tres.html", "tres.html", '<a href="/tres.html">')[0])
        # pt também é conferido: pt → página en (pt sempre existe, então é erro)
        self.assertIn("leva a en", ok(mapa, "tres.html", "/en/tres.html", "en/tres.html", '<a href="/en/tres.html">')[0])
        # data-troca-idioma="X": a mesma página em X, hreflang/lang de X quando presentes
        self.assertEqual(ok(mapa, "tres.html", "/en/tres.html", "en/tres.html",
                            '<a href="/en/tres.html" hreflang="en" lang="en" data-troca-idioma="en">'), [])
        self.assertEqual(ok(mapa, "es/tres.html", "/tres.html", "tres.html",
                            '<a href="/tres.html" hreflang="pt-BR" lang="pt-BR" data-troca-idioma="pt">'), [])
        # a língua atual na lista do seletor aponta para a própria página
        self.assertEqual(ok(mapa, "es/tres.html", "/es/tres.html", "es/tres.html",
                            '<a href="/es/tres.html" hreflang="es" lang="es" data-troca-idioma="es" aria-current="true">'), [])
        # o link da faixa não tem hreflang nem lang (vêm da <section lang>): passa
        self.assertEqual(ok(mapa, "tres.html", "/en/tres.html", "en/tres.html",
                            '<a href="/en/tres.html" data-troca-idioma="en" class="x">'), [])
        # outra página, outra língua, atributo incoerente, língua fora da página
        self.assertIn("esperado /en/tres.html", ok(mapa, "tres.html", "/en/", "en/index.html",
                                                   '<a href="/en/" data-troca-idioma="en">')[0])
        self.assertIn("esperado /en/tres.html", ok(mapa, "tres.html", "/es/tres.html", "es/tres.html",
                                                   '<a href="/es/tres.html" data-troca-idioma="en">')[0])
        self.assertIn("`hreflang=\"es\"`", ok(mapa, "tres.html", "/en/tres.html", "en/tres.html",
                                              '<a href="/en/tres.html" hreflang="es" lang="en" data-troca-idioma="en">')[0])
        self.assertIn("`lang=\"pt-BR\"`", ok(mapa, "tres.html", "/en/tres.html", "en/tres.html",
                                             '<a href="/en/tres.html" hreflang="en" lang="pt-BR" data-troca-idioma="en">')[0])
        self.assertIn("fora das línguas", ok(mapa, "so-pt.html", "/en/so-pt.html", "en/so-pt.html",
                                             '<a href="/en/so-pt.html" data-troca-idioma="en">')[0])
        # fora do mapa não entra
        self.assertEqual(ok(mapa, "es/tres.html", "/assets/x.png", "assets/x.png", '<a href="/assets/x.png">'), [])
        # página fora do mapa (a 404, bilíngue por desenho) não entra
        self.assertEqual(ok(mapa, "404.html", "/en/", "en/index.html", '<a href="/en/">'), [])

    def test_ui_sem_blocos_e_erro(self):
        mapa = json.loads(ler("correto", "idiomas.json"))
        self.assertIn("nenhum bloco", i18n.regra_dicionario("ui.ts", "export const ui = {};\n", mapa, eh_ui=True)[0])
        self.assertEqual(i18n.regra_dicionario("apps.ts", "export const apps = {};\n", mapa, eh_ui=False), [])

    def test_linha_de_data(self):
        meses = json.loads(ler("correto", "idiomas.json"))["idiomas"]["en"]["meses"]
        ok = i18n.regra_linha_data
        self.assertEqual(ok("x.en.md", "**Last updated:** July 13, 2026\n", "Last updated:", meses, "2026", 7, "13"), [])
        self.assertIn("sem linha de data", ok("x.en.md", "nada\n", "Last updated:", meses, "2026", 7, "13")[0])
        self.assertIn("≠ lastUpdated 2026-07-13",
                      ok("x.en.md", "**Last updated:** July 14, 2026\n", "Last updated:", meses, "2026", 7, "13")[0])

    def test_redirecionamento(self):
        r = i18n.redirecionamentos
        for forma in ["location.replace('/en/')", "location.assign(u)", "window.location.href = u",
                      "location='/en/'", "document.location = u", "location.pathname = '/en/'",
                      "location.search='?x'", "location.hash = '#a'", "location['href'] = u",
                      "location [\"href\"]=u", "navigation.navigate('/en/')",
                      '<meta http-equiv="refresh" content="0;url=/en/">', "<meta http-equiv=refresh>"]:
            with self.subTest(forma=forma):
                self.assertTrue(r(forma), forma)
        for inocente in ["Permissions-Policy: geolocation=()", "allow=\"geolocation=self\"",
                         "if (location.href == u) {}", "if (location.hash === '#a') {}",
                         "const x = location.pathname;", "relocation = 1", "mylocation.href = u"]:
            with self.subTest(inocente=inocente):
                self.assertEqual(r(inocente), [], inocente)


if __name__ == "__main__":
    unittest.main()
