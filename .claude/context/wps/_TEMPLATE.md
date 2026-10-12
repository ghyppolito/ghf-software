<!--
Template de Work Package. Copie para WP-NN-slug-curto.md, preencha e APAGUE este comentário.
O arquivo começa com "_" para o gen_estado.py/check_plano.py ignorarem o template.

O que o check_plano.py cobra:
- `id:` igual ao prefixo do nome do arquivo; status inicial sempre `todo`.
- `area:` em legal | landing | design | infra | seo | docs — decide quem implementa (legal → site-legal).
- `depende_de:` só WP existente, sem ciclo. `adr:` só ADR existente em decisions/.
- `spec:` o arquivo de docs/ que é a fonte (ex.: docs/AVALIACAO.md) — o agente lê SÓ a seção citada.
- `decisoes:` IDs de decisoes.md que o WP precisa ver decididas antes do pré-voo.
- `visual: true` quando algum critério só se prova no navegador (layout, idioma, compartilhamento)
  — o usuário olha e reporta; o WP só fecha depois.
-->
---
id: WP-NN
titulo: Título curto, no afirmativo
area: landing            # legal | landing | design | infra | seo | docs
status: todo             # todo | doing | blocked | done | adiado
depende_de: []
adr: []                  # ex.: [ADR-001]
spec: ""                 # ex.: docs/AVALIACAO.md — seção citada no corpo
decisoes: []             # ex.: [D1]
tamanho: S               # S (≤ 1 sessão) | M | L — S + risco baixo pula as etapas 2–3 do ciclo
risco: baixo             # baixo | medio | alto — alto = texto legal, URL contratual, deploy
visual: false            # true = há critério que só o navegador prova
branch: feat/wp-NN-slug-curto
---

# WP-NN — Título

**Depende de:** — · **Achados roteados:** —

**Objetivo:** uma frase. O que passa a ser verdade que hoje não é.

**Contexto:** por que agora, e a evidência — `arquivo:linha`, saída do `check_site.py`, diff
contra o repositório do app, número medido. Sem evidência, é palpite.

**Ler antes:** a seção exata de `docs/AVALIACAO.md`, o ADR, o arquivo de origem. Nada além disso.

**Arquivos-alvo:** lista fechada. Tocar arquivo fora dela = parar e reportar. A escrituração em `.claude/context/` (status, `ESTADO.md`, achados) é sempre permitida e não entra na lista.

**Passos:**
1. …

**Critérios de aceite:** cada um verificável por comando, regra do `check_site.py` ou item de
roteiro de navegador — não por leitura.
- …

**Só no navegador:** *(obrigatório se `visual: true`)* página, viewport (360/768/1280), idioma,
o que ver. O usuário reporta; sem o relato o WP não fecha.

**Irreversível:** *(obrigatório se toca URL contratual, deploy ou texto legal)* o que sai do
site e não volta, e como o app instalado se comporta.

**Risco:** nível e o que pode dar errado de específico.
