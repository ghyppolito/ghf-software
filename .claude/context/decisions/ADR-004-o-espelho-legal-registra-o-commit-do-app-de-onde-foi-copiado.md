# ADR-004 · O espelho legal registra o commit do app de onde foi copiado

**Data:** 2026-10-15 · **Estado:** aceita · **Complementa:** D7 (o texto legal nasce no
repositório do app; o site é espelho) · **Depende de:** D14, D15

## Contexto

Medido em 2026-10-15 com `cmp`: o corpo dos 5 `.pt.md` de `src/content/legal/` é igual a um
commit do app, mas não a uma mesma referência. LottoExpert bate com `master`; TopoWalk e EclipseGo
batem com commits de branches sem remoto, e a principal do app difere; o checkout do Pole Position
está numa release em andamento (`chore/release-2.2.0`) que difere do que o site publica. Copiar
do disco sobrescreveria texto publicado; copiar da branch principal desfaria três correções. O que
é estável é o commit.

## Decisão

1. **A origem é sempre um commit do app**, lido com `git -C <repo> show <sha>:<caminho>`, com
   `sha = git rev-parse <ref>^{commit}`. Nunca o working tree. A ref padrão é a branch principal
   do app (D14); exceção por `--ref`.
2. **O `.pt.md` guarda o commit** no front-matter (`origemCommit`, 40 hex minúsculos), ao lado de
   `lastUpdated`; o corpo é a cópia byte a byte da origem. Enquanto o en não acompanha, o `.pt.md`
   leva `en: "pendente"`. Nenhuma outra chave.
3. **Quem copia é `tools/sync_legal.py`**, com a tabela única `ORIGENS` (doc → repositório, caminho,
   ref padrão). Ele só escreve o `.pt.md`, nunca o `.en.md`, e recusa a cópia quando o commit
   registrado não é ancestral da ref (desfaria texto publicado), salvo `--forca`.
4. **A comparação de texto é local e determinística**: `check_site.py` confere o corpo do `.pt.md`
   contra `git show <origemCommit>:<caminho>` quando o repositório do app está presente. No CI
   (sem os apps, D15) ele cobra formato, `origemCommit` e o marcador `en: "pendente"` como erro.
   Ref padrão à frente do commit registrado é aviso, não erro: espelhar é decisão do humano (D7).

## O que isto fecha

Editar o corpo do `.pt.md` ou o `origemCommit` à mão; usar o checkout do app como origem;
comparar o site contra uma branch móvel; publicar en atrás do pt sem que o `check_site` acuse.
Voltar atrás custa tirar duas chaves do front-matter e o script; o texto não muda.

## O que isto mantém aberto

Comparar o texto no CI (D15 (B)), em WP próprio com credencial e plano de reversão. Trocar a ref
padrão de um app (uma linha em `ORIGENS`). Línguas além do en (D8): o marcador hoje é só `en`;
quando o WP-15..18 trouxer es/fr/it/de/ru, ADR que substitui ou estende esta.

## Onde olhar

`tools/sync_legal.py` (`ORIGENS`), `tools/check_site.py` §4, `src/content.config.ts`,
`src/content/legal/*.pt.md`, `.claude/commands/legal.md`, `.claude/agents/site-legal.md`;
`decisoes.md` D7, D14, D15; WP-09.
