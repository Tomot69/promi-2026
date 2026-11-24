#!/bin/sh
# R3 — LA VERSION INSTALLÉE SUR L'iPHONE DE TOM, LUE SUR LE TÉLÉPHONE : l'app écrit au démarrage `promi_version` (le commit construit, le
# fichier du script, l'heure) dans son stockage ; on recopie ce stockage sur le Mac et on le lit. L'app doit avoir été lancée après
# l'installation (`xcrun devicectl device process launch --terminate-existing --device <id> fr.autier.promi`).
# Usage : sh outils/version-iphone.sh [id de l'appareil]
APPAREIL="${1:-9DC7D3E2-75F8-56AD-8015-2F4498E9B8BD}"
D="$(mktemp -d)"
xcrun devicectl device copy from --device "$APPAREIL" --domain-type appDataContainer --domain-identifier fr.autier.promi \
  --source Library/WebKit/WebsiteData --destination "$D" >/dev/null 2>&1 || { echo "copie impossible (l'iPhone est-il branché et déverrouillé ?)"; exit 1; }
B="$(find "$D" -name localstorage.sqlite3 | head -1)"
[ -n "$B" ] || { echo "aucun stockage trouvé"; exit 1; }
# le stockage de WebKit : la valeur en UTF-16 ; on la convertit
sqlite3 "$B" "select hex(value) from ItemTable where key='promi_version';" | xxd -r -p | iconv -f UTF-16LE -t UTF-8
echo
rm -rf "$D"
