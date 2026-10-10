import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
o="""  var pad=avg()*1.3;                        /* marge d'une dalle autour */
  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;"""
assert S.count(o)==1
S=S.replace(o,"""  var pad=avg()*1.3;                        /* marge d'une dalle autour */
  /* ⚑ v140 (Tom, 10 oct. 2026, C-088) — LE ZOOM DE DÉPART DES MONDES « FAITS DE LEURS SEULES PAROLES », TANT QU'ILS GARDENT LE SEMIS
     CONSTANT (moins de SEMIS_NEUF_MIN paroles, v139) : « Bien plus zoomé qu'en v139 : avec une parole, on voit une dalle entière et un peu
     autour ; avec deux, les deux dalles entières ; puis trois ; puis quatre, avec quelques cellules vides, peu. Le zoom recule pas à pas
     avec le nombre de paroles. » On cadre les dalles colorées avec une marge de 0,8 cellule (1,3 ailleurs), et le plafond du zoom passe
     de 2 à 3,6 : à une parole la dalle fait les deux tiers de la largeur ; chaque parole de plus élargit le cadre, la vue recule. */
  var _serre=!!(_NEUFS[theme] && !_AP && !_semisNeuf()); if(_serre) pad=avg()*0.8;
  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;""")
o="""  s=Math.max(1.0, Math.min(s, 2.0));        /* jamais plus loin que la Toile entiere, plafond 2.0 */"""
assert S.count(o)==1
S=S.replace(o,"""  s=Math.max(1.0, Math.min(s, _serre?3.6:2.0));        /* jamais plus loin que la Toile entiere, plafond 2.0 (3,6 : v140, voir plus haut) */""")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
