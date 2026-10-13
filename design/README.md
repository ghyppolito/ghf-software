# design/

Sistema visual do site — decisão do humano, no Claude Design (claude.ai/design), conforme D4.

- `BRIEF.md` — escrito pelo agente no WP-06: marca, os 4 produtos e a hierarquia entre eles,
  anatomia de landing, tokens que já existem, o que preservar, o que resolver.
- `handoff/<AAAA-MM-DD>/` — o export de cada sessão no Claude Design. É a referência que o
  `site-ux` audita e o `site-dev` implementa.

**Handoff vigente:** nenhum ainda — aguarda a sessão do usuário (WP-06, passo 2).

## Regras

- **Cada export é congelado.** `handoff/<data>/` não se edita. Desenho novo é **pasta nova**
  (`handoff/<AAAA-MM-DD>-<tema>/`), e esta página passa a nomeá-la como vigente.
- **Onde o handoff e o brief divergem, o handoff prevalece.** `uploads/` dentro do export é a
  cópia que o Claude Design leu, não a fonte: a fonte é `BRIEF.md`.
- **Texto do export é placeholder.** A copy vem do README/ASO de cada app; o texto legal, do
  repositório do app.
- **Tudo aqui é público** enquanto o Pages publicar em modo branch (o Jekyll publica `design/`).
  Não versionar nada que não possa estar em `ghfsoftware.com/design/...`.

Quando houver biblioteca de componentes no código (depois do WP-08), `/design-sync` pode manter
o projeto de design-system sincronizado com ela, um componente por vez.
