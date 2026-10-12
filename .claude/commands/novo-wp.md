---
description: Transforma uma ideia, achado, bug ou evolução em Work Package no backlog — o único caminho de entrada de trabalho novo
argument-hint: descrição do que se quer (ou o bug com a evidência — URL, captura, saída do check_site.py)
---

Pedido: **$ARGUMENTS**

1. **Já existe?** Procure em `.claude/context/ESTADO.md` e `achados-novos.md`. Se um WP aberto
   cobre, proponha ampliá-lo em vez de criar outro. Se é um achado já roteado, diga para onde.
2. **Evidência.** Um WP cita `arquivo:linha`, saída do `check_site.py`, diff contra o
   repositório do app, captura ou número medido (Lighthouse). Sem evidência, é palpite.
3. Invoque `site-arquiteto` para escrever `.claude/context/wps/WP-NN-slug.md` a partir de
   `wps/_TEMPLATE.md`. Decisão de produto embutida (o que destacar, stack, analytics, design)
   vira `/decisao` e entra em `decisoes:`. Toca texto legal, URL contratual ou deploy →
   `risco: alto`. Algum critério só o navegador prova → `visual: true`.
4. WP grande (`L`) ou que mistura conteúdo com mudança de stack: quebre.
5. Proponha a posição em `SEQUENCIA` (`tools/gen_estado.py`) — trilha A, B ou C — e
   **pergunte ao usuário** antes de editar a ordem. Nada entra na frente da trilha A enquanto
   o LottoExpert 2.05.02 não estiver publicado.
6. `python3 tools/gen_estado.py && python3 tools/check_plano.py`.

Não comece a implementar. Este comando termina com o WP escrito e a pergunta sobre prioridade.
