import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
a="var P=onde(cv, e.base, e.amp, 30, e.nat==='nuee' ? 360 : 195); return P ? {cible:cs, chemin:P, trace:{de:0, pointille:true, ep:6}} : null; }},"
assert S.count(a)==1
S=S.replace(a,"var P=onde(cv, e.base, e.amp, 30, 360);   /* v139 : jusqu'au bout pour les trois natures — au vrai doigt, s'arrêter au milieu (30 → 195) ne plante pas (mesuré) */ return P ? {cible:cs, chemin:P, trace:{de:0, pointille:true, ep:6}} : null; }},")
a="geste:'tracer le trait pour planter (entier pour un Cercle)'"
assert S.count(a)==1
S=S.replace(a,"geste:'tracer le trait pour planter, jusqu’au bout'")
io.open(f,'w',encoding='utf-8').write(S)
