# ADR-001 · URLs públicas do site são contrato com os apps instalados

**Data:** 2026-10-12 · **Estado:** aceita · **Registro:** retroativo — a regra existia de fato
desde o primeiro link no app; o texto é do setup agêntico.

## Contexto

O LottoExpert em produção aponta para `ghfsoftware.com/lottoexpert-privacy.html` (`AboutScreen`,
onboarding, ficha da Play) e gera links de convite para
`ghfsoftware.com/lotto-expert/sweepstake-invite/lottoexpert-invite.html?d=…`; o
`/.well-known/assetlinks.json` é o que faz o Android abrir esse link no app em vez do navegador
(App Links **não segue redirect** na verificação). Os outros três apps apontam para a sua página
de privacidade a partir da ficha da Play. Nenhum desses caminhos pode mudar sem quebrar aparelho
que não vai atualizar.

## Decisão

Os caminhos listados em `CONTRATUAIS` (`tools/check_site.py`) e no `CLAUDE.md` existem em
todo deploy, como arquivo real (não redirect). Mudança de stack prova isso com
`check_site.py --raiz dist` antes de ir para `master`. Caminho novo que um app passe a citar
entra na lista no mesmo WP que o app o adota.

## O que isto fecha

Renomear páginas "para ficar bonito" (`/lottoexpert/privacy`), trocar `.html` por rota limpa
nessas URLs, mover o convite para outro diretório, e qualquer framework cujo build não consiga
emitir esses caminhos literais. Voltar atrás custa uma versão de cada app e, para o convite,
todos os links já compartilhados.

## O que isto mantém aberto

Páginas **novas** podem usar rota limpa e `/en/`; as contratuais podem ganhar uma versão en
em outro caminho, desde que a original continue servindo o português. Redirects podem existir
**além** do arquivo real, nunca no lugar dele.

## Onde olhar

`tools/check_site.py` (`CONTRATUAIS`), `CLAUDE.md` § "URLs que são contrato",
`../lotto-expert/app/src/main/AndroidManifest.xml` e `AboutScreen.kt` (quem aponta),
`.well-known/assetlinks.json`, `_config.yml`.
