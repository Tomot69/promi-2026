import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""  function nbMoisson(){ return (D && D.T.length>=K.RANG2) ? K.MOISSON : 3; }""",
"""  /* ⚑ v131 (Tom, 5 oct. 2026, C-052) : « La liste « Ce que tu as tenu » de l'Aura montre TOUTES les paroles tenues, dans l'ordre
     chronologique, l'Aura défilant. Plus de limite à 3 ou 6. » (remplace Q187 : trois dalles, six dès cinq tenues.) */
  function nbMoisson(){ return D ? D.T.length : 0; }""")
rep("""    var L=D.T.slice(-nbMoisson()).reverse();
    L.forEach(function(p){ GR.appendChild(cellule(p)); });""","""    var L=D.T.slice();   /* v131 : toutes, dans l'ordre où elles ont été tenues */
    L.forEach(function(p){ GR.appendChild(cellule(p)); });""")
rep("""      moisson:D.T.slice(-nbMoisson()).reverse().map(function(p){ return p.id; }),""","""      moisson:D.T.map(function(p){ return p.id; }),""")
io.open('app.html','w',encoding='utf-8').write(S)
