# Invariantes — detalhe

O que não coube no `CLAUDE.md` por tamanho, mas tem a mesma autoridade. Carregue sob demanda.
Cada regra aponta a guarda que a prova.

## URLs e contratos com os apps

| Regra | Por quê | Guarda |
|---|---|---|
| Os 7 caminhos de `CONTRATUAIS` em `check_site.py` existem em todo deploy | App instalado, Play Console e App Links apontam para eles; App Links não segue redirect (ADR-001) | `check_site.py` §1 — e `--raiz dist` depois do WP-07 |
| `.well-known/assetlinks.json` tem o package `br.com.ghfsoftware.lottoexpert` e as duas impressões digitais | Sem ele, o link do bolão abre no navegador, não no app | `check_site.py` §6; `tools/contrato.sha256`; `include-hidden-files: true` no upload do `deploy.yml` |
| O convite do bolão lê o formato que o app gera (`?d=` GZIP + Base64, v1 e v2) | Formato é do app (ADR-006 lá); a página só decodifica | sem guarda automática — mudança na página exige teste com link real gerado pelo app |
| `CNAME` = `ghfsoftware.com` | Pages perde o domínio sem ele | revisão no `/release` |
| `public/` tem só `assets/`, `.well-known/`, `lotto-expert/` e `CNAME`; nenhum `.html` além do convite; cada arquivo vai a `dist/` byte a byte | O Astro publica o arquivo de `public/` no lugar da página gerada que colide com ele, com o build verde — cópia velha de página contratual iria ao ar calada | `check_site.py` §13 (que também prende o `.htmlvalidateignore` à linha do convite) |

## Conteúdo

| Regra | Por quê | Guarda |
|---|---|---|
| Texto legal é espelho do repositório do app; data igual em `.md`, HTML pt e HTML en | Duas origens derivam; o app faz o usuário aceitar o texto (D7) | `tools/sync_legal.py` é o único que escreve o corpo do `.pt.md`, de um commit do app (`origemCommit`, ADR-004); `check_site.py` §4: corpo = `git show <origemCommit>` com o app presente, `origemCommit` e `en: "pendente"` (erro) sempre; `sync_legal.py <app> --check` no `/legal` |
| Copy do LottoExpert não promete chance, maximização nem prêmio | Política da Play para app de loteria e jogo responsável — mesma régua do `PaywallCopyComplianceTest` do app | `check_site.py` §5 (`COPY_PROIBIDA`, só cresce) |
| Toda string visível existe em pt **e** en | Inglês parcial é pior que nenhum: parece quebrado | `site-qa` AUDITAR; sem guarda automática até o WP-08 |
| `og:image` aponta para arquivo que existe no repositório | Link compartilhado sem imagem — e o convite do bolão é canal viral | `check_site.py` §3 |

## Processo

| Regra | Por quê | Guarda |
|---|---|---|
| `master` é deploy; só o usuário mescla | Mesclar é publicar texto legal que o app em produção aponta (D5) | `/release`; `settings.json` nega `git merge` e `git checkout master` ao agente |
| Um WP `doing` por vez; todo achado tem destino | Fila sem dono vira trabalho invisível | `check_plano.py` |
