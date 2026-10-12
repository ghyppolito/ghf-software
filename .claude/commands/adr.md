---
description: Registra uma decisão arquitetural em .claude/context/decisions/
argument-hint: descrição curta da decisão
---

Decisão: **$ARGUMENTS**

Invoque `site-arquiteto` para escrever `.claude/context/decisions/ADR-NNN-slug.md`, com o
próximo número da sequência. Formato:

```markdown
# ADR-NNN · Título (uma afirmação)

**Data:** AAAA-MM-DD · **Estado:** aceita | substituída por ADR-MMM

## Contexto
Três linhas. O que forçou a decisão — o fato medido, o bug de campo, a exigência do app.

## Decisão
O que foi decidido, na afirmativa.

## O que isto fecha
As alternativas que deixam de estar disponíveis, e o custo de voltar atrás.

## O que isto mantém aberto
O que continua sendo possível depois desta decisão.

## Onde olhar
Arquivos, regras do check_site.py, WPs.
```

**Não escreva ADR para o que `docs/AVALIACAO.md` ou um ADR anterior já decidiu** — cite e
pare. Se a decisão nova contradiz uma anterior, marque a antiga como `substituída por` no
mesmo commit. Decisão de **produto** (o que destacar, analytics, design) não é ADR — é `/decisao`.
