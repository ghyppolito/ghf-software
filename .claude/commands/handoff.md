---
description: Encerra a sessão — reescreve o contexto de execução para que a próxima retome sem reler tudo
---

Invoque `site-docs` para reescrever `.claude/context/handoff.md` **do zero** (não acumule
histórico), fazer a triagem de `achados-novos.md` e regerar o `ESTADO.md`.

O handoff responde seis coisas, nesta ordem:

1. onde parei, em uma frase — WP, branch, etapa do ciclo, o que está commitado e o que não
2. o que está quebrado ou pela metade **agora** — qual página, qual regra do `check_site.py`
3. o que **só o navegador prova** e ainda não foi visto pelo usuário — página, viewport, idioma
4. a próxima ação concreta
5. decisões desta sessão que não foram para `decisoes.md` nem viraram ADR, e por quê
6. o que está **esperando publicação** — `git log --oneline master..develop`: o que `develop`
   tem que o site no ar (`master`) não tem, e se há texto legal entre eles (urgência)

Ao final: `python3 tools/gen_estado.py && python3 tools/check_plano.py`, com a saída colada.

Seja honesto sobre o que ficou incompleto. Um handoff que descreve a sessão como mais
concluída do que foi custa mais caro que um que não existe.
