#!/bin/sh
# v207 §1 — la page de la preuve : une version de l'app TELLE QUELLE, et la coquille posée en tête de <head>.
#   sh construire.sh                    la v205 de cette branche (la preuve du 17 nov.)
#   SOURCE=<dossier> VERSION=<nom> sh construire.sh   une autre version (v207 : « v206 corrigée », extraite par git archive)
# ⚑ v207 (séance du 17 nov.) : la page passe en `viewport-fit=cover` — sans lui, la WebView gardait les marges des zones sûres (l'app ne prenait pas tout l'écran).
set -e
ICI="$(cd "$(dirname "$0")" && pwd)"; RACINE="${SOURCE:-$(cd "$ICI/.." && pwd)}"; VERSION="${VERSION:-v205}"
MAC="http://$(ipconfig getifaddr en0):8752"
rm -rf "$ICI/www"; mkdir -p "$ICI/www/variantes"
cp "$RACINE/promi-moteur.js" "$ICI/www/"
cp "$RACINE"/variantes/flaques.js "$RACINE"/variantes/trace-lettres.js "$RACINE"/variantes/trace-chemins-*.js "$ICI/www/variantes/"
sed -e "s#__MAC__#$MAC#" -e "s#__VERSION__#$VERSION#" "$ICI/coquille.js" > "$ICI/www/coquille.js"
python3 - "$RACINE/app.html" "$ICI/www/index.html" <<'PY'
import sys
S = open(sys.argv[1], encoding='utf-8').read()
vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
assert S.count(vp) == 1, 'la balise viewport a changé'
S = S.replace(vp, vp[:-2] + ', viewport-fit=cover">')
i = S.index('<head>') + len('<head>')
open(sys.argv[2], 'w', encoding='utf-8').write(S[:i] + '<script src="coquille.js"></script>' + S[i:])
PY
echo "www construit depuis $RACINE ($VERSION) · relevé envoyé à $MAC"
