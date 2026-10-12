---
description: Executa um Work Package do site — pré-voo, arquiteto, ux, dev/legal, verify, auditoria em paralelo e escrituração
argument-hint: WP-NN (sem argumento, propõe o próximo da sequência em ESTADO.md)
---

WP: **$ARGUMENTS**

Sem número: leia `.claude/context/ESTADO.md`, proponha o primeiro WP da trilha A cujas
dependências estejam `done` e **pergunte** antes de começar.

## 1. Pré-voo (você, sem subagente)

Leia o arquivo do WP em `.claude/context/wps/`. Pare e diga o que falta se:
- `status` não é `todo` (um `doing` por vez — `check_plano.py` cobra)
- alguma dependência não está `done`
- alguma decisão em `decisoes:` está em aberto em `decisoes.md` — **quem decide é o usuário**
- há achados em `achados-novos.md` roteados a este WP: liste-os, entram no escopo

Marque `status: doing`, crie a branch `feat/wp-NN-slug` a partir de `develop` (D5) e
regenere o `ESTADO.md`.

## 2. Arquiteto

Invoque `site-arquiteto` com o WP. Veredito: aprovado / reprovado com o motivo. Toca URL
contratual, deploy ou stack → ADR antes do código. `tamanho: S` + `risco: baixo` pula esta
etapa, **nunca** em texto legal, URL contratual ou deploy.

## 3. UX (só se o WP toca aparência)

Invoque `site-ux` em modo DESENHAR. A especificação dele é o que o `site-dev` implementa.
"Sem referência no handoff" → pergunte ao usuário antes de seguir.

## 4. Implementação

- `area: legal` → `site-legal` (espelha, não redige).
- Demais → `site-dev`, com o WP, o veredito do arquiteto e a especificação do ux.
Só os Arquivos-alvo. Arquivo fora da lista = parar e reportar.

## 5. `/verify`

## 6. Commit e auditoria em paralelo

Commit `WP-NN: …` (sem push). Na **mesma mensagem**, invoque sobre o diff `develop...HEAD`:
`site-qa` (AUDITAR), `site-seo-perf` e, se tocou tela, `site-ux` (AUDITAR). Achado de
severidade alta no escopo do WP: corrige, `/verify` de novo, commit. Fora do escopo:
`achados-novos.md`.

## 7. Escrituração

Invoque `site-docs`: status (`done` só com todo critério coberto e todo `visual: true`
reportado pelo usuário), `ESTADO.md`, triagem, "Onde parei" do `handoff.md`.

Ao final, diga ao usuário: o que foi feito, o que **ele** precisa olhar no navegador (página,
viewport, idioma), e se o WP espera `/release` para ir ao ar.
