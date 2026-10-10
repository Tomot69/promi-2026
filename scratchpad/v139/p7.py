import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
a='<style id="lot-V139-OMBRE-css">'
assert S.count(a)==1
S=S.replace(a,"""<style id="lot-V139-CREME-css">
/* ⚑ v139 (Tom, 9 oct. 2026, C-084) — LE CRÈME DES FICHES EN CLAIR. « En clair, le corps des fiches (sous le trait) et leurs encarts prennent le
   crème du fond des pages du Fil et de l'Index, au lieu du blanc actuel, jugé trop blanc. Seulement dans les fiches ; le reste ne bouge pas. »
   Le corps et l'encart du haut passent de #F7F0DE à #EAD9B9 (le fond de l'Index : `--c-creme90-2`). Les cartes du fil d'un Cercle, qui
   étaient déjà à #E9D8B7 sur le corps clair, prennent en échange #F7F0DE — la même paire que sur la page du Fil (cartes claires sur ce
   crème) ; sans cela elles se confondaient avec le corps (ΔE 0,6). Le sombre ne bouge pas ; la page + non plus. */
#device.light #detailPoster#detailPoster{background-color:var(--c-creme90-2)!important}
#device.light #detailPoster#detailPoster .enh{background-color:var(--c-creme90-2)!important}
#device.light #detailPoster#detailPoster #dpDetails{background-color:var(--c-creme90-2)!important}
#device.light #detailPoster#detailPoster .nf-item{background-color:var(--c-creme95)!important}
</style>
"""+a)
io.open(f,'w',encoding='utf-8').write(S)
