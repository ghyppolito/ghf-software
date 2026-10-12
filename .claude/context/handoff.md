# Handoff

> Reescrito do zero a cada sessão por `/handoff` (`site-docs`). Não acumule histórico aqui —
> histórico é o git, `ESTADO.md` e os ADRs.

**Fim da sessão de 2026-10-12** (setup agêntico; sem mudança em página). Branch `develop`.
Nada commitado nesta sessão — o setup inteiro está na árvore de trabalho, à espera de revisão
e commit pelo usuário.

## 1. Onde parei

WP-01 `done`; WP-02 `blocked` só pela verificação visual do usuário (código e auditoria em
1c01b08, 7dd934f). Branches empilhadas, nada mesclado em develop: `feat/wp-01-…` ← `feat/wp-02-…`
(mesclar na ordem). Próximo: WP-04 (convite + política do Pole Position), depois `/release`.

## 2. Quebrado ou pela metade agora

- `python3 tools/check_site.py` **falha** no estado atual do site, de propósito — são bugs
  reais, roteados: OG do convite e `meta description` (`WP-04`), data do Pole Position
  (`WP-04`). Até o WP-04 fechar, o `/verify` de outro WP vai mostrar esses erros; não os
  "conserte" afrouxando a regra.
- Caminhos de origem de `/legal` conferidos para os 4 apps (tabela em `.claude/commands/legal.md`).

## 3. O que só o navegador prova

Nada desta sessão.

## 4. Próxima ação

1. Usuário revisa e commita o setup (`git add -A && git commit`), na `develop`.
2. `/wp WP-01` — espelhar política e termos do LottoExpert 2.05.02. Depois WP-02 (D1 decidida: A), WP-04,
   e `/release` (WP-03).
3. D2, D3 e D4 podem esperar a trilha A; D4 (Claude Design) pode começar em paralelo quando
   o usuário quiser (WP-06 escreve o brief).

## 5. Decisões fora de `decisoes.md` e ADR

- O `check_plano.py` é cópia do lotto-expert com `AREAS` e `visual` adaptados — registrado em D6.
- `og:image` ausente é **aviso**, não erro, em `check_site.py` (página legal pode não ter);
  `og:image` apontando para arquivo inexistente é erro. Não virou invariante porque pode mudar
  no WP-11.

## 6. Esperando publicação

`git log --oneline master..develop` = **10 commits** (TopoWalk: política e landing; Pole
Position: política com Crashlytics e landing; EclipseGo: link da Play). **Há texto legal entre
eles** — `WP-03` publica, junto do LottoExpert 2.05.02.
