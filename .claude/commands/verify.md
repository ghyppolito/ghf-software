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

**Tocou página legal (`*-privacy.html`, `*-terms.html`, `docs/*_POLICY.md`, `docs/*_TERMS*.md`,
`src/content/legal/*.md`, `src/layouts/LegalLayout.astro`):**
```bash
diff -q ../lotto-expert/docs/PRIVACY_POLICY.md docs/LOTTOEXPERT_PRIVACY_POLICY.md
diff -q ../lotto-expert/docs/TERMS_OF_SERVICE.md docs/LOTTOEXPERT_TERMS_OF_SERVICE.md
diff <(sed '1,/^---$/d' src/content/legal/eclipsego-privacy.pt.md) ../eclipse-go/docs/PRIVACY_POLICY.md   # migrada: sem o front-matter
```
(e o equivalente do app tocado). Saída vazia = espelho fiel. Diferença = o WP não terminou.

**Tocou nav, footer ou `tailwind.config` (antes do WP-08):** confira que a mudança está nas 10
páginas — `grep -c '<trecho novo>' *.html` com 10 linhas ≠ 0.

**Tocou `package.json`, `astro.config.*` ou `src/`:** além do bloco acima, `cmp` de cada
arquivo copiado da raiz com o seu par em `dist/` — a integração copia byte a byte até o WP-08.

**Mudou algo visível:** diga o que só o navegador prova (página, viewport 360/768/1280,
idioma pt e en) — é checklist para o usuário, não "verificado". Com o Claude in Chrome
disponível, sirva `dist/` com `python3 -m http.server 8080 -d dist` e olhe; cole o que viu.

Relate o que rodou, o que **não** rodou e por quê, e o que falhou — com a saída real. Bloco
que não rodou é "não verificado", nunca "passou".

**Não conserte uma regra do `check_site.py` afrouxando-a.** Se passou a falhar, ou a página
regrediu ou a regra estava errada, e essas duas coisas se resolvem de formas opostas. Diga qual
das duas antes de mexer. A lista `COPY_PROIBIDA` só cresce.

Nunca faça merge em `master`, push, nem altere `CNAME`/`_config.yml` sem WP que o peça.
