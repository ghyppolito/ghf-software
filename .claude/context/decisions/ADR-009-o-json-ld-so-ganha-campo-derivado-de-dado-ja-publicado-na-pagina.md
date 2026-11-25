# ADR-009 · O JSON-LD só ganha campo derivado de dado já publicado na própria página

**Data:** 2026-11-22 · **Estado:** aceita · **Amplia:** ADR-005 §6 (o conjunto fechado de chaves) ·
**Origem:** `LANDING-JSONLD-CAMPOS-01`, `ORGANIZATION-JSONLD-MINIMO-01` (WP-10, fatia 10a)

## Contexto

O ADR-005 §6 fechou o `MobileApplication` em `name`, `operatingSystem`, `applicationCategory`,
`installUrl` e `offers`, e deixou "novos campos, em WP próprio, com fonte". O `check_site.py` §14
barra chave fora do conjunto. A fatia 6 e a 5 acharam o `Organization` e o `MobileApplication`
mínimos; a fatia 10a do WP-10 é o WP que leva os campos novos, sem texto novo (D25).

## Decisão

1. Campo novo de JSON-LD só entra se o valor sair de um dado que a página já publica, lido da
   mesma fonte que a página usa. Nada é digitado no JSON-LD.
2. `MobileApplication` ganha, nas 8 landings, pela mesma função `mobileApplication` de
   `src/i18n/apps.ts`:
   - `url`: a URL canônica da landing (`rota(lang, pagina)` sobre `https://ghfsoftware.com`);
   - `description`: a `meta description` da página, a mesma string passada ao `Base`;
   - `image`: a URL absoluta do favicon do app em `public/assets/` (URL fixa, ADR-006), o mesmo
     arquivo do `favicon` do `Base`;
   - `offers.availability`: `https://schema.org/InStock`, derivado de o app não ser `indisponivel`.
3. `Organization` ganha `description` (a `meta description` da home na língua), `sameAs` (os
   canais da GHF que o rodapé da home publica, de uma constante só) e `foundingDate`.
4. `inLanguage` fica de fora: a língua da página não é a língua do app, e nenhuma fonte do app diz
   em que línguas ele está. `foundingDate` entra: o usuário respondeu em 2026-11-22 que "Desde 2004"
   é o ano de fundação. O valor sai de `since_2004` em `home.ts` (`"2004"`), e o §14 exige igualdade
   estrita com ele.
5. O `check_site.py` §14 continua com chaves fechadas e passa a conferir cada campo novo contra a
   página: `url` = canonical, `description` = `meta description`, `image` = arquivo existente do
   site, `sameAs` contido nos links externos do `<footer>`, `foundingDate` = o ano de `since_2004`.

## O que isto fecha

Campo de JSON-LD com valor sem par visível na página, como `aggregateRating`, `review`, preço do
Premium, `screenshot` sem captura publicada e texto escrito só para o buscador. Voltar ao conjunto
mínimo custa tirar as chaves de `apps.ts` e do conjunto de `CHAVES_JSONLD`.

## O que isto mantém aberto

`inLanguage` quando o README ou o ASO do app listar as línguas da interface. `screenshot` quando a landing publicar as capturas da D26. Um app retirado da
Play muda o `availability` pelo `indisponivel`, sem editar o JSON-LD.

## Onde olhar

`src/i18n/apps.ts` (`mobileApplication`, `organization`), `src/components/paginas/Pagina*.astro`,
`tools/check_site.py` §14, ADR-005 §6, WP-10 fatia 10a.
