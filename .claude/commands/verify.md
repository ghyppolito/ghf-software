---
description: Roda a verificação local do site — o mesmo que o CI cobra no PR
allowed-tools: Bash(python3:*), Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(diff:*), Bash(sha256sum:*)
---

Descubra o que o diff tocou — `git diff --name-only develop...HEAD` mais `git status --porcelain`
— e rode na ordem, parando no primeiro erro.

**Sempre** (o mesmo que o job `site` do `pr.yml` cobra, mais o escopo):
```bash
python3 tools/gen_estado.py --check && python3 tools/check_plano.py
npm ci && npm run build && python3 tools/check_site.py --raiz dist
(cd dist && sha256sum --quiet -c ../tools/contrato.sha256)   # convite, assetlinks, og:image do convite, CNAME (D13)
npx html-validate 'dist/**/*.html'
lychee --offline --no-progress --root-dir "$PWD/dist" 'dist/**/*.html'   # se o binário não estiver instalado: "não verificado"
git diff --stat develop...HEAD        # nenhum arquivo fora dos Arquivos-alvo do WP (escrituração em .claude/context/ é permitida)
```

**Tocou página legal (`src/content/legal/*.md`, `src/layouts/LegalLayout.astro`,
`src/pages/**/*-privacy.astro`, `src/pages/**/*-terms.astro`):**
```bash
python3 tools/check_site.py          # §4: com o app presente, o corpo do .pt.md = git show origemCommit:<caminho> (ADR-004)
python3 tools/sync_legal.py --todos --check   # informativo: o app avançou além do origemCommit? (D14)
```
O `check_site.py` falhar em "pt ≠ <app>@<sha>" = texto editado à mão ou bootstrap errado: o WP não
terminou. Não compare com o disco do app (`diff … ../<app>/…`): o checkout do app pode estar em
outra branch. `sync_legal --check` com "à frente/divergente" não é erro do site — é o app com
texto ainda não espelhado (ou espelhado de branch fora da principal); decidir a ref é do usuário.
Aviso "origem ausente" num WP legal = a comparação de texto não rodou, então **não passou**: traga o app para `..` (ou `$GHF_APPS_DIR`) e rode de novo.

**Tocou `public/`:** o `check_site.py` §13 já confere a lista fechada e cada arquivo byte a byte
contra `dist/`; arquivo de `tools/contrato.sha256` mudou = decisão do usuário (D13).

**Mudou algo visível:** diga o que só o navegador prova (página, viewport 360/768/1280,
idioma pt e en) — é checklist para o usuário, não "verificado". Com o Claude in Chrome
disponível, sirva `dist/` com `python3 -m http.server 8080 -d dist` e olhe; cole o que viu.

Relate o que rodou, o que **não** rodou e por quê, e o que falhou — com a saída real. Bloco
que não rodou é "não verificado", nunca "passou".

**Não conserte uma regra do `check_site.py` afrouxando-a.** Se passou a falhar, ou a página
regrediu ou a regra estava errada, e essas duas coisas se resolvem de formas opostas. Diga qual
das duas antes de mexer. A lista `COPY_PROIBIDA` só cresce.

Nunca faça merge em `master`, push, nem altere `public/CNAME` sem WP que o peça.
