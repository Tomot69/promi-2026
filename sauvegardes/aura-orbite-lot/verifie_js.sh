#!/bin/zsh
# CLAUDE.md §7, « après toute modification » — étape 1 : la syntaxe JS de app.html.
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
SP=/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/dcd8febe-cb8b-4dd6-a4f8-2c1646ff8fa4/scratchpad/aura
python3 -c "import re,io; S=io.open('app.html',encoding='utf-8').read();
io.open('$SP/check.js','w',encoding='utf-8').write(''.join(m.group(1)
for m in re.finditer(r'<script[^>]*>(.*?)</script>',S,re.S)))"
node --check $SP/check.js && echo "SYNTAXE JS app.html : OK"
echo "md5 app.html $(md5 -q app.html)"
grep -c 'id="lot-AURA-ORBITE"' app.html | sed 's/^/blocs lot-AURA-ORBITE (script) : /'
