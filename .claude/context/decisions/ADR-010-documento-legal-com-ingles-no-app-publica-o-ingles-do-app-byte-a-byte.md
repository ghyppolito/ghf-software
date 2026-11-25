# ADR-010 · Documento legal com inglês no app publica o inglês do app, byte a byte

**Data:** 2026-11-25 · **Estado:** aceita · **Emenda:** ADR-004 §2–§3 (só o `.pt.md` guarda o
commit; o script nunca escreve o `.en.md`), ADR-007 §8 (a tradução não tem `origemCommit`) e a D7
("traduz o en") · **Origem:** WP-26, pergunta 7, respondida pelo usuário em 2026-11-25: "O inglês
do app, cópia exata."

## Contexto

O TopoWalk publica o texto legal em duas línguas, em `origin/master` (`cfbff63`, commit `873343b`):
`TERMS_OF_USE.md` + `TERMS_OF_USE.en.md` e `PRIVACY_POLICY.md` + `PRIVACY_POLICY.en.md`. As duas
versões trazem a linha "novembro de 2026" / "November 2026". Pela D7, o site traduziria um inglês
próprio, e o mesmo documento teria dois textos em inglês públicos (o do GitHub e o do site). A D7
existe para evitar isso: "duas origens derivam". Hoje LottoExpert e EclipseGo (`docs/`) não têm
`.en.md`.

## Decisão

1. **A origem é declarada por documento e por língua.** Em `tools/sync_legal.py`, `ORIGENS` passa a
   dizer, para cada doc, o caminho do pt e, quando existir, o caminho do en no mesmo repositório,
   por exemplo `"topowalk-terms": ("topo-walk", {"pt": "TERMS_OF_USE.md", "en": "TERMS_OF_USE.en.md"}, "master")`.
   A declaração é explícita e não é descoberta pelo nome do arquivo. Se o app ganhar um `.en.md`, o
   comportamento do site não muda sozinho. O `--check` avisa quando a origem tem `<BASE>.en.md` e
   `ORIGENS` não o declara, e esse aviso vira achado.
2. **Doc com en na origem:** o `.en.md` do site é o corpo do en do app no commit, **byte a byte**,
   lido com `git show <sha>:<caminho en>`. O front-matter tem `lastUpdated` (tirado da linha
   `**Last updated:**` do corpo en, pelo `rotuloData`/`meses` do en em `src/i18n/idiomas.json`) e
   `origemCommit` próprio. O `sync_legal.py` copia o pt e o en do **mesmo** sha, na mesma execução,
   e grava o mesmo `origemCommit` nos dois. O en não entra em `pendente`, porque é cópia e não
   tradução. Emenda a ADR-004 §2 ("Nenhuma outra chave" passa a valer por língua) e a ADR-007 §8
   ("o `.<código>.md` não tem `origemCommit`" passa a valer só para língua traduzida pelo site).
3. **O `sync_legal.py` escreve o `.en.md` só quando a origem o declara.** Emenda a ADR-004 §3. Para
   doc sem en na origem, nada muda: o script não toca o `.en.md`, e o en continua sendo tradução do
   site (D7 original, `site-legal`).
4. **Datas divergentes na origem: a cópia é recusada.** Se a data do pt e a do en da origem diferem
   no sha pedido, o `sync_legal.py` recusa (sai com 2, sem escrever) e diz que o en do app está
   atrás do pt. O problema volta ao repositório do app: o site não publica pt novo com en velho,
   e não completa o en por conta própria. Se a data é a mesma, mas o pt mudou entre o
   `origemCommit` antigo e o novo e o en não mudou, o `--check` e a cópia avisam ("pt mudou e en
   não"). É aviso, não recusa: no mesmo mês, pode ser correção só do pt.
5. **`check_site.py` §4, com o repositório do app presente:** o corpo do `.en.md` de doc com en na
   origem é comparado byte a byte com `git show <origemCommit>:<caminho en>`, como o pt. O
   `origemCommit` do en tem de ser igual ao do pt. A regra i (mesma `lastUpdated` em todas as
   línguas) continua reprovando data divergente. **No CI (sem os apps, D15):** o `.en.md` de doc com
   en declarado tem de ter `origemCommit` válido, e o de doc sem en declarado não pode ter. As regras
   ii–iv do §12 (estrutura pt/en) continuam valendo sobre o en copiado. Quando falham, quem corrige é
   o app, e o site não edita o corpo.
6. **Outras línguas (D8 (b1)):** es, fr, it, de e ru continuam traduzidas pelo site **a partir do
   pt**, com `pendente` e sem `origemCommit`. A mesma regra vale para qualquer língua que o app passe
   a publicar: ela entra em `ORIGENS` e deixa de ser traduzida. Isso pede só uma linha na tabela, não
   um ADR novo.

## O que isto fecha

- O site traduzir o inglês de um documento cujo app já publica inglês.
- Editar o corpo do `.en.md` espelhado à mão, mesmo para corrigir erro: a correção é no app.
- Publicar pt e en de commits diferentes.
- Publicar par com datas diferentes.

Voltar atrás custa tirar a língua en de `ORIGENS`, o `origemCommit` do `.en.md` e o ramo do §4. O
texto en publicado fica, e passa a ser mantido como tradução.

## O que isto mantém aberto

- Declarar en no LottoExpert, EclipseGo e Pole Position quando os apps publicarem `.en.md` (uma
  linha em `ORIGENS` por doc, no WP do `/legal` daquele app).
- Comparar o texto no CI (D15 (B)).
- Um app com inglês como língua de origem e pt traduzido não está coberto. Pede ADR próprio.

## Consequências no WP-26 (a atualizar no próprio WP)

- `tools/sync_legal.py`: forma nova de `ORIGENS`, cópia do en, recusa por data (§4 acima), aviso de
  en não declarado e de "pt mudou e en não", `--check` reporta pt e en (igual / atrás / divergente).
- `tools/check_site.py` §4 e `tools/regras_i18n.py` (`regra_front_matter`): `origemCommit` no en
  permitido e exigido só para doc com en declarado, igual ao do pt; comparação byte a byte do en.
  Fixture nova em `tools/fixtures/` e caso em `tools/test_regras_i18n.py`.
- `.claude/agents/site-legal.md`: com en na origem, **só confere** (estrutura, links, nome do
  documento, o que o §12 acusa) e devolve divergência ao usuário como achado do app. Não traduz e
  não edita. Sem en na origem, traduz como hoje.
- `.claude/commands/legal.md`: passo 3 (a quem chamar), tabela, seção de hotfix (passo 5, "traduz
  o en" vale só para doc sem en na origem).
- `docs/ARQUITETURA.md` §5: quem tem `origemCommit`, e "o inglês é tradução" passa a ser
  condicional.
- `CLAUDE.md` § Fontes de verdade: "traduz para o inglês" passa a valer só para documento sem
  inglês no app.

## Onde olhar

`tools/sync_legal.py` (`ORIGENS`), `tools/check_site.py` §4, `tools/regras_i18n.py`
(`regra_datas`, `regra_front_matter`), `src/content/legal/topowalk-*.en.md`,
`.claude/agents/site-legal.md`, `.claude/commands/legal.md`, `docs/ARQUITETURA.md` §5; ADR-004,
ADR-007 §8; `decisoes.md` D7, D8, D14, D15; WP-26.
