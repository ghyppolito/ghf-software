---
description: Publica o site — prepara e confere o PR develop → master (Pages serve master); o merge é do usuário
---

**`master` é o site no ar.** Mesclar `develop` nela é deploy — e deploy de texto legal que o app
em produção aponta. Por isso o merge é do usuário; o agente prepara e confere.

**Limites do agente:** nunca faz merge em `master`, nunca faz push sem pedido, nunca altera
`CNAME` ou `_config.yml` aqui.

1. **Agente:** `git fetch` e `git log --oneline master..develop`. Liste o que vai ao ar, e
   marque o que é texto legal (urgente) e o que é landing. Se há WP `doing` cujo código está
   em `develop`, diga — vai ao ar pela metade?
2. **Agente:** na `develop`: `python3 tools/check_site.py` e `python3 tools/check_plano.py`
   verdes. Erro aqui **para** o release.
3. **Agente:** checklist do que só o navegador prova, acumulado dos WPs que vão ao ar
   (seção "Só no navegador" de cada WP). Peça ao usuário que olhe **antes** do merge, com
   `python3 -m http.server 8080` na `develop`.
4. **Usuário:** relata o checklist. Sem o relato, o ritual **não** está concluído.
5. **Usuário:** `gh pr create --base master --head develop` (ou merge direto, como preferir) e
   merge. Pages publica em ~1 min.
6. **Agente, depois do merge:** confira no ar — `curl -sI https://ghfsoftware.com/<página>`
   com 200 e, para texto legal, `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -o "Última atualização: [^<]*"`
   com a data nova. Registre "Publicado em AAAA-MM-DD" nos WPs e atualize o `handoff.md` §6.

Ao fim, relate o que foi publicado e o que ficou com o usuário, dizendo explicitamente se o
checklist do navegador foi **reportado** ou se ficou devendo.
