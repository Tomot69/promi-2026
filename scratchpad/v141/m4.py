import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
old="  if(x1<x0) return null; var j=a*0.13; if(x1-x0>4*j){ x0+=j; x1-=j; } if(y1-y0>4*j){ y0+=j; y1-=j; }\n"
assert S.count(old)==1
S=S.replace(old,"  if(x1<x0) return null;\n")
old="rentrée du joint\n     entre deux dalles ; une parole seule occupe 70 % de la largeur, plusieurs toute la largeur utile. */"
assert S.count(old)==1
S=S.replace(old,"entière. La matière d'une dalle occupe de 58 à 100 % de sa\n     cellule (mesuré sur Ritournelle) : une parole seule voit sa CELLULE cadrée à 108 % de la largeur (sa matière en fait donc 60 % au moins,\n     et reste entière) ; plusieurs, à 100 %. */")
old="  var availW=W*(_bs?(col.length===1?0.70:0.95):0.92), availH=Math.max(1,botB-topB);"
assert S.count(old)==1
S=S.replace(old,"  var availW=W*(_bs?(col.length===1?1.08:1.0):0.92), availH=Math.max(1,botB-topB);")
old="minuscule), rentrée du joint. Échantillonnée"
assert S.count(old)==1
S=S.replace(old,"minuscule). Échantillonnée")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
