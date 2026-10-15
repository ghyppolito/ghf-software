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
2. **Agente:** na `develop`: `npm ci && npm run build && python3 tools/check_site.py` (confere o
   publicado, `dist/`) e `python3 tools/check_plano.py` verdes.
   Erro aqui **para** o release.
3. **Agente:** checklist do que só o navegador prova, acumulado dos WPs que vão ao ar
   (seção "Só no navegador" de cada WP). Peça ao usuário que olhe **antes** do merge, com
   `python3 -m http.server 8080 -d dist` na `develop` (depois do build).
4. **Usuário:** relata o checklist. Sem o relato, o ritual **não** está concluído.
5. **Usuário:** `gh pr create --base master --head develop` (ou merge direto, como preferir) e
   merge. Quem publica depende da variável de repositório `PAGES_VIA_ACTIONS`: enquanto não
   estiver ligada (Pages em modo "branch master"), o Jekyll publica a raiz — run "pages build
   and deployment" — e o workflow `Deploy` só builda (job `deploy` pulado). Com
   `PAGES_VIA_ACTIONS=true` (Pages em modo "GitHub Actions"), o `deploy.yml` publica `dist/`.
   Confira que o run de quem publica saiu verde.
6. **Agente, depois do merge:** confira no ar — `curl -sI https://ghfsoftware.com/<página>`
   com 200 e, para texto legal, `curl -s https://ghfsoftware.com/lottoexpert-privacy.html | grep -o "Última atualização: [^<]*"`
   com a data nova. Registre "Publicado em AAAA-MM-DD" nos WPs e atualize o `handoff.md` §6.

Ao fim, relate o que foi publicado e o que ficou com o usuário, dizendo explicitamente se o
checklist do navegador foi **reportado** ou se ficou devendo.
