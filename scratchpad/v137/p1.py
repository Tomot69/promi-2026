import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""      if(recu){ fin(from+' me lance\\u00a0: chiche', '<b>'+esc(from)+'</b> me lance\\u00a0: chiche'); }
      else { var lw=W.length?liste(W, deplie, p.id):null, la=(A.length && String(p.avec)!==String(p.who))?liste(A, deplie, p.id):null, pt='', ph='';
        if(lw){ pt+='À '+lw.txt; ph+='À '+lw.html; }
        if(la){ pt+=(pt?' · ':'')+(pt?'avec ':'Avec ')+la.txt; ph+=(ph?' · ':'')+(ph?'avec ':'Avec ')+la.html; }
        if(pt){ fin(pt+' · chiche', ph+' · chiche'); } else { fin('Chiche','Chiche'); } } }""",
"""      /* ⚑ v137 (Tom, 8 oct. 2026, Q412) — LES CHICHE PRENNENT L'EXPRESSION COURANTE : à soi « T’es pas chiche de » · lancé « Marion, t’es pas
         chiche de » · à plusieurs « Marion et Rachel, vous êtes pas chiches de » (« … + x personnes » au-delà de trois) · reçu « Marion me
         dit : t’es pas chiche de ». Ceux à qui on le lance et ceux avec qui on le fait sont les mêmes personnes interpellées (une liste). */
      var TU='t\\u2019es pas chiche', VOUS='vous êtes pas chiches';
      if(recu){ fin(from+' me dit\\u00a0: '+TU, '<b>'+esc(from)+'</b> me dit\\u00a0: '+TU); }
      else { var C=W.slice(); A.forEach(function(x){ if(C.indexOf(x)<0) C.push(x); });
        if(!C.length){ fin('T\\u2019es pas chiche','T\\u2019es pas chiche'); }
        else { var lc=liste(C, deplie, p.id), vb=(C.length>1)?VOUS:TU; fin(lc.txt+', '+vb, lc.html+', '+vb); } } }""")
r("""     Chiche lancé     « À Marion · avec Rachel · chiche de »     Chiche à soi     « Chiche de »
     Chiche reçu      « Marion me lance : chiche de »            (mot manquant, le plus sobre — à valider)""",
"""     ⚑ v137 (Tom, Q412) — les formes nommées sont VALIDÉES ; les Chiche prennent l'expression courante :
     Chiche à soi     « T’es pas chiche de »                     Chiche lancé     « Marion, t’es pas chiche de »
     à plusieurs      « Marion et Rachel, vous êtes pas chiches de » (« … + x personnes » au-delà de trois)
     Chiche reçu      « Marion me dit : t’es pas chiche de »""")
io.open('app.html','w',encoding='utf-8').write(S)
