#!/bin/sh
# v207 §1 — la page de la preuve : la v205 de référence, TELLE QUELLE, et la coquille posée en tête de <head>.
set -e
ICI="$(cd "$(dirname "$0")" && pwd)"; RACINE="$(cd "$ICI/.." && pwd)"
MAC="http://$(ipconfig getifaddr en0):8752"
rm -rf "$ICI/www"; mkdir -p "$ICI/www/variantes"
cp "$RACINE/promi-moteur.js" "$ICI/www/"
cp "$RACINE"/variantes/flaques.js "$RACINE"/variantes/trace-lettres.js "$RACINE"/variantes/trace-chemins-*.js "$ICI/www/variantes/"
sed "s#__MAC__#$MAC#" "$ICI/coquille.js" > "$ICI/www/coquille.js"
python3 - "$RACINE/app.html" "$ICI/www/index.html" <<'PY'
import sys
S = open(sys.argv[1], encoding='utf-8').read(); i = S.index('<head>') + len('<head>')
open(sys.argv[2], 'w', encoding='utf-8').write(S[:i] + '<script src="coquille.js"></script>' + S[i:])
PY
echo "www construit · relevé envoyé à $MAC"
