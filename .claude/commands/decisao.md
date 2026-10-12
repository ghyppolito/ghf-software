---
description: Registra uma decisão de produto ou de processo em .claude/context/decisoes.md (arquitetura é /adr)
argument-hint: descrição curta da decisão
---

Decisão: **$ARGUMENTS**

Invoque `site-arquiteto` para acrescentar a linha em `.claude/context/decisoes.md`, com o
próximo `D` da sequência, no formato da tabela existente.

- **Em aberto:** a pergunta, os WPs que ela impacta, as opções com o custo de cada uma e a
  recomendada. Os WPs impactados passam a citá-la em `decisoes:`, e o `/wp` para no pré-voo
  enquanto estiver aberta.
- **Decidida:** `~~Dn~~ **DECIDIDO (AAAA-MM-DD): …**` — o que foi decidido, por quê, o que
  isso fecha e o que mantém aberto.

**Quem decide é o usuário.** O que destacar numa landing, stack, ferramenta de medição,
sistema visual, ordem do backlog, quando publicar: o agente apresenta as opções e para.
Decisão técnica que o código já expressa não se registra — registre o que o próximo agente
erraria sem saber.
