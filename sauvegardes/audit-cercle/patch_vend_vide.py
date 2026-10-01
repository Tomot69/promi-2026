# L'ÉCRAN QUI VEND, SANS AUCUN PROMI (Tom, 11 sept., nuit) : « cache la rangée et remonte le prix. Trois cases vides sur l'écran
# qui vend, c'est pire que pas de dalles du tout — ça dit « il n'y a rien à montrer ». » Patch sur app.html, motifs uniques.
import hashlib, io, os
RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(RACINE, 'app.html')
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '8b3c8cb167bbb379defb460f5c02bc39', 'app.html a changé : ' + avant
def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:90]
    S = S.replace(old, new)

# 1 · le CSS : la variante sans dalles — la rangée (dalles + noms, 132 → 254) disparaît, tout le bloc remonte de 144 (le prix
#     prend la cote où commençaient les dalles) ; les écarts de la planche entre les blocs sont gardés.
remplace("""#plusScreen #plCadre .pl-note.plv-n2{top:574px!important}""",
"""#plusScreen #plCadre .pl-note.plv-n2{top:574px!important}
/* ⚑ SANS AUCUN PROMI (Tom, 11 sept., nuit) : « cache la rangée et remonte le prix ». L'état est la CLASSE `plv-sans` que le script
   pose d'après les données (aucun Promi planté) — jamais une géométrie (§8). Le bloc remonte de 144 : le prix prend la cote des dalles. */
#plusScreen #plCadre.plv-sans .plv-dal,#plusScreen #plCadre.plv-sans .plv-nom{display:none!important}
#plusScreen #plCadre.plv-sans .plv-prix{top:132px!important}
#plusScreen #plCadre.plv-sans .plv-sous{top:198px!important}
#plusScreen #plCadre.plv-sans #buyYear{top:242px!important}
#plusScreen #plCadre.plv-sans #buyMonth{top:320px!important}
#plusScreen #plCadre.plv-sans .pl-note.plv-n1{top:404px!important}
#plusScreen #plCadre.plv-sans .pl-note.plv-n2{top:430px!important}""")

# 2 · le script : la classe suit les données, et l'app la publie
remplace("""    var I = ids(), comp = [], dpr = Math.min(2, window.devicePixelRatio || 1);""",
"""    var I = ids(), comp = [], dpr = Math.min(2, window.devicePixelRatio || 1);
    /* sans aucun Promi planté, pas de dalle à montrer : la rangée se cache (la classe ne change que si elle diffère) */
    if(CAD.classList.contains('plv-sans') !== !I.length) CAD.classList.toggle('plv-sans', !I.length);""")
remplace("""    window._vendDalles = comp;""", """    comp.sans = !I.length; window._vendDalles = comp; window._vendSans = !I.length;""")

# 3 · à l'ouverture, on pose DANS LA FOULÉE (micro-tâche de l'observateur, avant toute image) : aucune image ne montre la rangée
#     vide d'un utilisateur sans Promi ; puis les repeintes du §4 (60, 200, 600 ms)
remplace("""      [0, 60, 200, 600].forEach(function(d){ setTimeout(function(){ try{ pose(); peint(); }catch(_){ } }, d); });""",
"""      try{ pose(); peint(); }catch(_){ }
      [60, 200, 600].forEach(function(d){ setTimeout(function(){ try{ pose(); peint(); }catch(_){ } }, d); });""")

io.open(F, 'w', encoding='utf-8').write(S)
print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
