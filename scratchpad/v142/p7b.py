import io
f='promi-moteur.js'; S=io.open(f,encoding='utf-8').read()
def rep(old,new):
    global S
    assert S.count(old)==1, ('motif absent ou multiple', S.count(old), old[:70]); S=S.replace(old,new)
rep("""function _videsVus(n){""",
"""/* ⚑ v142 (Tom, 11 oct. 2026, C-088 et C-101) — LA PLACE D'UNE DALLE EST GARDÉE. Une parole (ou un Cercle) retient où sa dalle a été plantée
   ou posée (`p.place` = [x/W, y/H], sauvegardé avec elle ; un Cercle : `NUEPLACE[clé]`). POURQUOI : en rouvrant l'app, `sync` replantait
   chaque parole dans une cellule vide TIRÉE AU HASARD — mesuré sous Ritournelle : trois paroles plantées côte à côte revenaient aux trois
   coins de la Toile, et la vue ne pouvait plus les montrer de près. Une parole qui a une place reprend la cellule vide la plus proche d'elle. */
var _plantePid=null, _planteNuee=null;
function _placeLue(){ try{ if(_AP) return null;
  if(_plantePid!=null){ for(var i=0;i<promises.length;i++){ if(promises[i].id===_plantePid){ var p=promises[i].place; return (p&&p.length===2)?p:null; } } return null; }
  if(_planteNuee){ var m=window.NUEPLACE&&window.NUEPLACE[_planteNuee]; return (m&&m.length===2)?m:null; } }catch(_){ } return null; }
function _placeNote(x,y,force){ try{ if(_AP) return; var v=[+(x/W).toFixed(4),+(y/H).toFixed(4)], ecrit=false;
  if(_plantePid!=null){ for(var i=0;i<promises.length;i++){ if(promises[i].id===_plantePid){ if(force||!promises[i].place){ promises[i].place=v; ecrit=true; } break; } } }
  else if(_planteNuee){ window.NUEPLACE=window.NUEPLACE||{}; if(force||!window.NUEPLACE[_planteNuee]){ window.NUEPLACE[_planteNuee]=v; ecrit=true; try{ localStorage.setItem('promi_nueplace',JSON.stringify(window.NUEPLACE)); }catch(_){ } } }
  if(ecrit){ clearTimeout(_placeNote._t); _placeNote._t=setTimeout(function(){ try{ if(typeof saveState==='function') saveState(); }catch(_){ } },400); } }catch(_){ } }
try{ window.NUEPLACE=JSON.parse(localStorage.getItem('promi_nueplace')||'{}')||{}; }catch(_){ window.NUEPLACE={}; }
function _videsVus(n){""")
rep("""        var np=window.Toile.plantOne(true);
        if(!np) np=_celluleEnPlus('promi',j);""","""        _plantePid=list[j]; _planteNuee=null; var np=null; try{ np=window.Toile.plantOne(true); }finally{ _plantePid=null; }
        if(!np) np=_celluleEnPlus('promi',j);""")
rep("""        var _ns=window.Toile.plantOne(true); if(!_ns)_ns=_celluleEnPlus('nuee',list.length+_nk.length);""",
"""        _planteNuee=_nk; _plantePid=null; var _ns=null; try{ _ns=window.Toile.plantOne(true); }finally{ _planteNuee=null; } if(!_ns)_ns=_celluleEnPlus('nuee',list.length+_nk.length);""")
rep("""else{s=window.Toile.plantOne();if(!s)s=addP('promi');}if(s&&id!=null){s.pid=id;_dalleFigee(true);}""",
"""else{_plantePid=id;_planteNuee=null;try{s=window.Toile.plantOne();}finally{_plantePid=null;}if(!s)s=addP('promi');}if(s&&id!=null){s.pid=id;_dalleFigee(true);}""")
rep("""      jx=0; jy=0; }
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');""",
"""      jx=0; jy=0; }
    /* v142 : une parole qui a SA place reprend la cellule vide la plus proche d'elle, sans décalage */
    var _pl=_placeLue(); if(_pl){ var _px=_pl[0]*W, _py=_pl[1]*H, _pd=1e18; for(var _pj=0;_pj<gris.length;_pj++){ var _pg=gris[_pj], _pe=(_pg.x-_px)*(_pg.x-_px)+(_pg.y-_py)*(_pg.y-_py); if(_pe<_pd){ _pd=_pe; cible=_pg; } } jx=0; jy=0; }
    else _placeNote(cible.x+jx, cible.y+jy);
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
