#!/usr/bin/env python3
"""Prova as regras da lista de apps de tools/regras_apps.py (WP-10, fatia 10a; D12, D31) sobre os
casos de tools/fixtures/apps/.

Só biblioteca padrão (unittest). Rodar da raiz do repositório:

    python3 -B -m unittest tools/test_regras_apps.py

Casos de tools/fixtures/apps/:
  valido.ts                 apps.ts sintético no formato do real: 5 apps, o último `indisponivel`
  sem-atualizado.ts         Beta sem `atualizadoEm`
  ordem-a-mais.ts           ORDEM_APPS com uma chave que `apps` não tem
  data-invalida.ts          Gama com 2026-02-30
  bissexto-inexistente.ts   Gama com 2027-02-29 (2027 não é bissexto)
  home.html                 a Home de valido.ts em 2026-11-22 (4 cards; Eps em "Todos os apps")
  home-trocada.html         home.html com os cards de Beta e Gama trocados
"""
import datetime
import os
import sys
import unittest

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import regras_apps as r  # noqa: E402

FIXTURES = os.path.join(AQUI, "fixtures", "apps")
D = datetime.date


def ler(nome):
    with open(os.path.join(FIXTURES, nome), encoding="utf-8") as f:
        return f.read()


def href_pt(caminho):
    return "/" + caminho


def valido():
    apps, ordem, erros = r.le_apps_ts(ler("valido.ts"))
    assert not erros, erros
    return apps, ordem


class LeituraApps(unittest.TestCase):
    def test_valido(self):
        apps, ordem, erros = r.le_apps_ts(ler("valido.ts"))
        self.assertEqual(erros, [])
        self.assertEqual(ordem, ["alfa", "beta", "gama", "delta", "eps"])
        self.assertEqual(apps["alfa"]["nome"], "Alfa")  # o comentário com `nome: 'Ignorado'` não conta
        self.assertEqual(apps["alfa"]["termos"], "alfa-terms.html")
        self.assertEqual(apps["delta"]["tag"], "v3.1.4")
        self.assertTrue(apps["eps"]["indisponivel"])
        self.assertFalse(apps["alfa"]["indisponivel"])

    def test_sem_atualizado(self):
        _, _, erros = r.le_apps_ts(ler("sem-atualizado.ts"))
        self.assertEqual(len(erros), 1, erros)
        self.assertIn("`beta` sem atualizadoEm", erros[0])

    def test_ordem_a_mais(self):
        _, _, erros = r.le_apps_ts(ler("ordem-a-mais.ts"))
        self.assertEqual(len(erros), 1, erros)
        self.assertIn("não tem exatamente as chaves de apps", erros[0])

    def test_data_invalida(self):
        for caso in ("data-invalida.ts", "bissexto-inexistente.ts"):
            with self.subTest(caso=caso):
                _, _, erros = r.le_apps_ts(ler(caso))
                self.assertEqual(len(erros), 1, erros)
                self.assertIn("`gama` com atualizadoEm", erros[0])

    def test_formato_ausente(self):
        self.assertTrue(r.le_apps_ts("export const outra = 1;")[2])
        self.assertTrue(r.le_apps_ts("export const ORDEM_APPS = ['a'];")[2])


class Particao(unittest.TestCase):
    def test_quatro_em_destaque_e_indisponivel_no_resto(self):
        apps, ordem = valido()
        self.assertEqual(r.particionar(apps, ordem, D(2026, 11, 22)), (["alfa", "beta", "gama", "delta"], ["eps"], []))

    def test_no_maximo_quatro(self):
        apps, ordem = valido()
        apps["eps"] = dict(apps["eps"], indisponivel=False)
        destaque, resto, _ = r.particionar(apps, ordem, D(2026, 11, 22))
        self.assertEqual((destaque, resto), (["alfa", "beta", "gama", "delta"], ["eps"]))
        apps["beta"] = dict(apps["beta"], atualizadoEm="2024-01-01")
        destaque, resto, _ = r.particionar(apps, ordem, D(2026, 11, 22))
        self.assertEqual((destaque, resto), (["alfa", "gama", "delta", "eps"], ["beta"]))

    def test_vencido_vai_para_o_resto(self):
        apps, ordem = valido()
        # Delta (2026-07-26) fica até 2027-07-26 e sai em 2027-07-27
        self.assertEqual(r.particionar(apps, ordem, D(2027, 7, 26))[0], ["alfa", "beta", "gama", "delta"])
        self.assertEqual(r.particionar(apps, ordem, D(2027, 7, 27))[:2], (["alfa", "beta", "gama"], ["delta", "eps"]))

    def test_futuro_e_erro(self):
        apps, ordem = valido()
        erros = r.particionar(apps, ordem, D(2026, 9, 15))[2]
        self.assertEqual(len(erros), 1, erros)
        self.assertIn("Alfa: atualizadoEm 2026-10-01 está no futuro", erros[0])

    def test_29_de_fevereiro_rola_como_o_js(self):
        # Date.UTC(2027, 1, 29) = 01/03/2027: hoje 29/02/2028 corta em 01/03/2027
        self.assertEqual(r.soma_anos(D(2028, 2, 29), -1), D(2027, 3, 1))
        apps = {"x": {"nome": "X", "atualizadoEm": "2027-02-28"}, "y": {"nome": "Y", "atualizadoEm": "2027-03-01"}}
        self.assertEqual(r.particionar(apps, ["x", "y"], D(2028, 2, 29))[:2], (["y"], ["x"]))
        # app atualizado em 29/02 sai em 01/03 do ano seguinte (o JS rola o corte para 01/03)
        self.assertEqual(r.saida_do_destaque(D(2028, 2, 29)), D(2029, 3, 1))
        self.assertEqual(r.saida_do_destaque(D(2026, 7, 26)), D(2027, 7, 27))

    def test_aviso_a_30_dias_e_nenhum_a_31(self):
        apps, _ = valido()
        destaque = ["alfa", "beta", "gama", "delta"]
        avisos = r.avisos_corte(apps, destaque, D(2027, 6, 27))
        self.assertEqual(len(avisos), 1, avisos)
        self.assertIn("Delta: sai do destaque da Home em 2027-07-27 (30 dias)", avisos[0])
        self.assertEqual(r.avisos_corte(apps, destaque, D(2027, 6, 26)), [])

    def test_hoje(self):
        agora = datetime.datetime(2026, 11, 22, 23, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))
        self.assertEqual(r.hoje_de({}, agora), (D(2026, 11, 23), None))  # UTC, não a hora local
        self.assertEqual(r.hoje_de({"GHF_HOJE": "2027-10-20"}), (D(2027, 10, 20), None))
        for env in ({"GHF_HOJE": "2027-10-20", "CI": "true"}, {"GHF_HOJE": "2027-10-20", "GITHUB_ACTIONS": "true"}):
            self.assertIn("só para teste local", r.hoje_de(env)[1])
        self.assertIn("não é uma data", r.hoje_de({"GHF_HOJE": "2027-02-30"})[1])


class Home(unittest.TestCase):
    def test_home_correta(self):
        apps, ordem = valido()
        self.assertEqual(r.confere_home_hoje("index.html", ler("home.html"), apps, ordem, D(2026, 11, 22), href_pt), ([], []))

    def test_cards_trocados_morde(self):
        apps, ordem = valido()
        erros, avisos = r.confere_home_hoje("index.html", ler("home-trocada.html"), apps, ordem, D(2026, 11, 22), href_pt)
        self.assertEqual(avisos, [])
        self.assertEqual(len(erros), 1, erros)
        self.assertIn("cards da Home ['alfa', 'gama', 'beta', 'delta'] ≠ destaque", erros[0])

    def test_meia_noite_e_aviso(self):
        apps, ordem = valido()
        # home.html é a partição de 2027-07-26 (Delta ainda em destaque); hoje 2027-07-27 Delta saiu
        erros, avisos = r.confere_home_hoje("index.html", ler("home.html"), apps, ordem, D(2027, 7, 27), href_pt)
        self.assertEqual(erros, [])
        self.assertEqual(len(avisos), 1, avisos)
        self.assertIn("dist/ gerado ontem (UTC)", avisos[0])
        # dois dias depois é erro
        erros, avisos = r.confere_home_hoje("index.html", ler("home.html"), apps, ordem, D(2027, 7, 28), href_pt)
        self.assertEqual(avisos, [])
        self.assertTrue(any("≠ destaque" in e for e in erros), erros)
        self.assertTrue(any("Delta fora do destaque e sem link /delta.html" in e for e in erros), erros)

    def test_play_e_time_errados(self):
        apps, ordem = valido()
        apps["alfa"] = dict(apps["alfa"], id="com.exemplo.outro", atualizadoEm="2026-10-02")
        erros, _ = r.confere_home_hoje("index.html", ler("home.html"), apps, ordem, D(2026, 11, 22), href_pt)
        self.assertEqual(len(erros), 2, erros)
        self.assertIn("botão da Play para ['com.exemplo.alfa'] ≠ [com.exemplo.outro]", erros[0])
        self.assertIn("<time datetime> ['2026-10-01'] ≠ atualizadoEm 2026-10-02", erros[1])

    def test_indisponivel_precisa_da_politica(self):
        apps, ordem = valido()
        html = ler("home.html").replace('<a href="/eps-privacy.html">', '<a href="/eps.html">')
        erros, _ = r.confere_home_hoje("index.html", html, apps, ordem, D(2026, 11, 22), href_pt)
        self.assertEqual(len(erros), 2, erros)
        self.assertIn("Eps fora do destaque e sem link /eps-privacy.html", erros[0])
        self.assertIn("Eps indisponível com link para a landing", erros[1])


class Tag(unittest.TestCase):
    def git_falso(self, tags, datas):
        def git(*args):
            if args[0] == "rev-parse":
                return (0, b"x") if args[-1].split("^")[0] in datas else (1, b"")
            if args[0] == "log":
                t = args[-1].split("^")[0]
                return (0, datas[t].encode() + b"\n") if t in datas else (128, b"")
            if args[0] == "tag":
                return 0, "\n".join(tags).encode()
            raise AssertionError(args)
        return git

    def test_tag_igual(self):
        git = self.git_falso(["v4.4.0", "v4.3.6"], {"v4.4.0": "2026-10-29", "v4.3.6": "2026-09-01"})
        self.assertEqual(r.confere_tag("TopoWalk", "v4.4.0", "2026-10-29", git), ([], []))

    def test_data_diferente(self):
        git = self.git_falso(["v4.4.0"], {"v4.4.0": "2026-10-29"})
        erros, _ = r.confere_tag("TopoWalk", "v4.4.0", "2026-10-28", git)
        self.assertEqual(erros, ["TopoWalk: commit da tag v4.4.0 é de 2026-10-29 ≠ atualizadoEm 2026-10-28 (apps.ts)"])

    def test_tag_inexistente(self):
        git = self.git_falso(["v4.4.0"], {"v4.4.0": "2026-10-29"})
        erros, _ = r.confere_tag("TopoWalk", "v9.9.9", "2026-10-29", git)
        self.assertEqual(erros, ["TopoWalk: tag v9.9.9 (apps.ts) não existe no repositório do app"])

    def test_tag_mais_nova_e_aviso(self):
        git = self.git_falso(["v4.5.0", "v4.4.0"], {"v4.5.0": "2026-11-20", "v4.4.0": "2026-10-29"})
        erros, avisos = r.confere_tag("TopoWalk", "v4.4.0", "2026-10-29", git)
        self.assertEqual(erros, [])
        self.assertEqual(avisos, ["TopoWalk: tag v4.5.0 (2026-11-20) depois de v4.4.0 — atualize tag e atualizadoEm em apps.ts"])


if __name__ == "__main__":
    unittest.main()
