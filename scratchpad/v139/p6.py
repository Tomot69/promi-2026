import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("  function mesAffiche(txt){ if(!MES) return; txt=(MES.version||'')+'\\n'+txt;",
    "  function mesAffiche(txt){ if(!MES) return; txt=(MES.version||'')+'\\n'+txt+(window._peloteContact?'\\ncontact lu : '+window._peloteContact:'');   /* v139 : le rayon du contact tel que le toucher le donne, pour étalonner sur l'iPhone */")
rep("    return {a:a, el:elp, dmax:G.PROF*a, ax:ax, capteur:cap, rx:rx, ry:ry};",
    "    if(MES) window._peloteContact=cap ? (Math.round(rx*10)/10+' × '+Math.round(ry*10)/10+' pt'+(TCH.t?' (toucher, '+Math.round(TCH.rot)+'°)':' (pointeur)')+' → demi-axe '+Math.round(a*K.Rpt)+' pt') : 'aucun (pouce par défaut)';\n    return {a:a, el:elp, dmax:G.PROF*a, ax:ax, capteur:cap, rx:rx, ry:ry};")
io.open(f,'w',encoding='utf-8').write(S)
