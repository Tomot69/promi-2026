import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
lot=io.open('scratchpad/v132/lot-dessin.html',encoding='utf-8').read()
assert S.count("</style>\n</body>")==1
S=S.replace("</style>\n</body>","</style>\n"+lot+"</body>")
# la vue entière sait montrer un dessin
rep("""  function source(){ try{ var dp=fiche(); if(!dp) return null;""","""  function source(){ try{ var dp=fiche(); if(!dp) return null;
      /* v132 : la bande porte un dessin (posé, non masqué) — une parole ou un Cercle */
      var dz=window._dessin && window._dessin.sourceVue && window._dessin.sourceVue(); if(dz) return dz;""")
# le partage : la case d'une parole montre son dessin posé et non masqué
rep(""" function _dalleReelle(pid){
  if(_cache[pid]!==undefined)return _cache[pid];""",""" function _dalleReelle(pid){
  if(_cache[pid]!==undefined)return _cache[pid];
  /* v132 (C-042) : un dessin posé et NON MASQUÉ remplace la dalle dans la case ; masqué, il n'est jamais emporté */
  try{ var _dz=window._dessinCase && window._dessinCase(pid); if(_dz){ _cache[pid]=_dz; return _dz; } }catch(e){}""")
io.open('app.html','w',encoding='utf-8').write(S)
