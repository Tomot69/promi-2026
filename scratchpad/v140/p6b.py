import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
o="""    var cible=pool[(_alea()*pool.length)|0];
    var a=avg();
    var jx=(_alea()-.5)*a*0.5, jy=(_alea()-.5)*a*0.5;"""
assert S.count(o)==1
S=S.replace(o,"""    var cible=pool[(_alea()*pool.length)|0];
    var a=avg();
    var jx=(_alea()-.5)*a*0.5, jy=(_alea()-.5)*a*0.5;
    /* ⚑ v140 (Tom, 10 oct. 2026, C-088) — sous les mondes « faits de leurs seules paroles », tant qu'ils gardent le semis constant (moins
       de SEMIS_NEUF_MIN paroles) : « avec deux, les deux dalles entières ; puis trois ; puis quatre, avec quelques cellules vides, peu ».
       Tirées au hasard dans le semis, deux paroles tombaient aux deux bouts de la Toile : on ne peut pas les voir entières ET de près. La
       parole neuve prend donc la cellule libre LA PLUS PROCHE des paroles déjà là (de leur centre ; la première : du milieu du champ
       dégagé), sans décalage : elles se touchent, et la vue recule d'un cran à chacune. */
    if(_NEUFS[theme] && !_AP && !_semisNeuf() && !(_REPLI[theme] && libres!==gris && pool===libres && pool.length && (pool[0].wt!=null?pool[0].wt:pool[0].w)<_repliW()/2)){
      var _qx=0,_qy=0,_qn=0; for(var _qi=0;_qi<seeds.length;_qi++){ var _qs=seeds[_qi]; if(_qs.kind!=='gray' && _qs.part==null){ _qx+=_qs.x; _qy+=_qs.y; _qn++; } }
      if(_qn){ _qx/=_qn; _qy/=_qn; } else { _qx=W/2; _qy=(HAUT_LIBRE+H-BAS_LIBRE)/2; }
      var _qd=1e18; for(var _qj=0;_qj<pool.length;_qj++){ var _qp=pool[_qj], _qe=(_qp.x-_qx)*(_qp.x-_qx)+(_qp.y-_qy)*(_qp.y-_qy); if(_qe<_qd){ _qd=_qe; cible=_qp; } }
      jx=0; jy=0; }""")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
