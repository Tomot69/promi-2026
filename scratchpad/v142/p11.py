import io
f='promi-moteur.js'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif', S.count(old), old[:70]); S=S.replace(old,new)
# 1 · une parole qui a sa place la reprend EXACTEMENT (semis constant)
rep("""    var _pl=_placeLue(); if(_pl){ var _px=_pl[0]*W, _py=_pl[1]*H, _pd=1e18; for(var _pj=0;_pj<gris.length;_pj++){ var _pg=gris[_pj], _pe=(_pg.x-_px)*(_pg.x-_px)+(_pg.y-_py)*(_pg.y-_py); if(_pe<_pd){ _pd=_pe; cible=_pg; } } jx=0; jy=0; }
    else _placeNote(cible.x+jx, cible.y+jy);
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');""",
"""    var _pl=_placeLue(), _plx=null, _ply=null; if(_pl){ var _px=_pl[0]*W, _py=_pl[1]*H, _pd=1e18; for(var _pj=0;_pj<gris.length;_pj++){ var _pg=gris[_pj], _pe=(_pg.x-_px)*(_pg.x-_px)+(_pg.y-_py)*(_pg.y-_py); if(_pe<_pd){ _pd=_pe; cible=_pg; } } jx=0; jy=0; _plx=_px; _ply=_py; }
    else _placeNote(cible.x+jx, cible.y+jy);
    var s=mk(Math.max(8,Math.min(W-8,(_plx!=null?_plx:cible.x+jx))), Math.max(8,Math.min(H-8,(_ply!=null?_ply:cible.y+jy))), 'promi');   /* v142 : la cellule vide la plus proche lui cède la place, et la dalle revient là où on l'a laissée */""")
# 2 · famille des mondes neufs : la place gardée aussi
rep("""      if(!s){ var p=_auVide(j); s=mk(p.x,p.y,'promi');""","""      if(!s){ _plantePid=list[j]; _planteNuee=null; var _pn=_placeLue(); _plantePid=null; var p=_pn?{x:_pn[0]*W,y:_pn[1]*H}:_auVide(j); s=mk(p.x,p.y,'promi');""")
rep("""      if(!t){ var p2=_auVide(list.length+q); t=mk(p2.x,p2.y,'nuee');""","""      if(!t){ _planteNuee=nk[q]; _plantePid=null; var _pn2=_placeLue(); _planteNuee=null; var p2=_pn2?{x:_pn2[0]*W,y:_pn2[1]*H}:_auVide(list.length+q); t=mk(p2.x,p2.y,'nuee');""")
# 3 · la boucle : pendant qu'on tire une dalle, la Toile se réorganise autour d'elle à chaque image
rep("""  if(grow){relax();relax();relax();mv=true;}
  if(grow)mv=true;var an=mv;""","""  if(_tire){ relax(); _tirePince(); mv=true; }   /* v142 (C-101) : la poussée se propage pendant qu'on déplace une dalle */
  if(grow){relax();relax();relax();mv=true;}
  if(grow)mv=true;var an=mv;""")
# 4 · le geste
rep("""host.addEventListener('pointerdown',function(e){e.stopPropagation();try{host.setPointerCapture(e.pointerId);}catch(_){}vTarget=null;_inert=null;window._panMain=0;""",
"""/* ⚑ v142 (Tom, 11 oct. 2026, C-101) — DÉPLACER UNE DALLE SUR SA TOILE. « Toucher simple = ouvrir la fiche, inchangé. Un appui de 0,8 s attrape la
   dalle : elle se soulève à peine (léger agrandissement, sans ombre) et suit le doigt partout. Les voisines se réorganisent sur son passage,
   fluidement, dans la manière de chaque monde. Au lâcher, elle reste où on l'a posée, et la place est gardée. Défilement, zoom et toucher
   simple inchangés ; aucun rebond, fondu ni ombre ; on ne pose pas une dalle sous la barre. »
   Un doigt posé sans bouger (moins de TIRE_JEU points) pendant TIRE_MS sur une dalle : sa graine suit le doigt (dans le repère de la Toile,
   quel que soit le zoom), son poids monte un peu (la cellule grandit : c'est le « soulèvement », sans rien dessiner autour), et à chaque
   image les autres graines se repoussent (`relax`) — chaque monde les suit à SA manière (son ressort, son dessin). Au lâcher : la graine
   reste, son poids revient, sa place est écrite sur la parole (`p.place`) ou le Cercle (`NUEPLACE`) et sauvegardée. Sa place est bornée
   au champ dégagé (ni sous le plateau, ni sous la barre : les bornes de la plantation). Un doigt qui bouge avant 0,8 s déplace la Toile,
   comme avant ; un second doigt rend la dalle et zoome, comme avant. */
var _tire=null, _tireP=null, _tireT=0, TIRE_MS=800, TIRE_JEU=8, TIRE_GROS=0.07;
function _toileXY(L){ return {x:(L.x-view.ox)/view.s, y:(L.y-view.oy)/view.s}; }
function _graineSous(x,y){ var b=null, bd=1e18; for(var i=0;i<seeds.length;i++){ var q=seeds[i]; if(q.part!=null) continue; var d=Math.sqrt((x-q.x)*(x-q.x)+(y-q.y)*(y-q.y))-(q.w||0); if(d<bd){ bd=d; b=q; } }
  return (b && b.kind!=='gray' && (b.pid!=null || b.nuee)) ? b : null; }
function _tireBornes(){ var a=avg(); return [8, W-8, HAUT_LIBRE, H-(H*(134/844)+a*0.87)]; }
function _tirePince(){ if(!_tire) return; var s=_tire.s; s.x=_tire.x; s.y=_tire.y; s.tx=_tire.x; s.ty=_tire.y; if(s.vx!=null){ s.vx=0; s.vy=0; } }
function _tireDebut(){ _tireT=0; if(!_tireP || _AP) return; var L=ptrs[_tireP.id]; if(!L || Object.keys(ptrs).length!==1) { _tireP=null; return; }
  var t=_toileXY(L), s=_graineSous(t.x,t.y); _tireP=null; if(!s) return;
  var gros=avg()*TIRE_GROS; _tire={id:L&&_tireId, s:s, dx:s.x-t.x, dy:s.y-t.y, x:s.x, y:s.y, wt0:s.wt, wFin0:s.wFin, gros:gros, t0:performance.now()};
  s.wAt=0; s.wt=(s.wt!=null?s.wt:s.w)+gros; if(s.wFin!=null) s.wFin=s.wt;
  _pan=null; _inert=null; vTarget=null; window._dalleTiree=(s.pid!=null?s.pid:s.nuee); window._tMouv=performance.now();
  try{ if(navigator.vibrate) navigator.vibrate(8); }catch(_){ } lastChange=performance.now(); kick(); }
var _tireId=null;
function _tireBouge(L){ if(!_tire) return; var t=_toileXY(L), B=_tireBornes();
  _tire.x=Math.max(B[0], Math.min(B[1], t.x+_tire.dx)); _tire.y=Math.max(B[2], Math.min(B[3], t.y+_tire.dy));
  _tirePince(); relax(); _tirePince(); window._tMouv=performance.now(); lastChange=performance.now(); kick(); }
function _tireFin(garde){ clearTimeout(_tireT); _tireT=0; _tireP=null; if(!_tire) return; var s=_tire.s, T=_tire; _tire=null;
  s.wt=T.wt0; if(T.wFin0!=null) s.wFin=T.wFin0; s.tx=T.x; s.ty=T.y;
  if(garde){ try{ if(s.pid!=null){ _plantePid=s.pid; _planteNuee=null; } else { _planteNuee=s.nuee; _plantePid=null; } _placeNote(T.x, T.y, true); }finally{ _plantePid=null; _planteNuee=null; } }
  window._dalleTiree=null; window._dalleLachee=performance.now(); relax(); s.tx=T.x; s.ty=T.y; window.Toile.paintOrder=null; lastChange=performance.now(); kick(); }
window.Toile_tire=function(){ return _tire?{pid:(_tire.s.pid!=null?_tire.s.pid:null), nuee:_tire.s.nuee||null, x:_tire.x, y:_tire.y, vue:{s:view.s,ox:view.ox,oy:view.oy}}:null; };
window.Toile_tireRegle={MS:TIRE_MS, JEU:TIRE_JEU, GROS:TIRE_GROS};
host.addEventListener('pointerdown',function(e){e.stopPropagation();try{host.setPointerCapture(e.pointerId);}catch(_){}vTarget=null;_inert=null;window._panMain=0;""")
rep("""  if(k.length===2){var a=ptrs[k[0]],b=ptrs[k[1]];pinch={d:Math.hypot(a.x-b.x,a.y-b.y)||1,s:view.s,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,ox:view.ox,oy:view.oy};_pan=null;}
  else if(k.length===1){_pan={ox:view.ox,oy:view.oy,h:[[ptrs[k[0]].t,ptrs[k[0]].x,ptrs[k[0]].y]]};}
  kick();});""",
"""  if(k.length===2){ _tireFin(true); var a=ptrs[k[0]],b=ptrs[k[1]];pinch={d:Math.hypot(a.x-b.x,a.y-b.y)||1,s:view.s,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,ox:view.ox,oy:view.oy};_pan=null;}
  else if(k.length===1){_pan={ox:view.ox,oy:view.oy,h:[[ptrs[k[0]].t,ptrs[k[0]].x,ptrs[k[0]].y]]};
    clearTimeout(_tireT); _tireId=e.pointerId; _tireP={id:e.pointerId, x:ptrs[k[0]].x, y:ptrs[k[0]].y}; _tireT=setTimeout(_tireDebut, TIRE_MS); }   /* v142 (C-101) : 0,8 s sans bouger → la dalle est attrapée */
  kick();});""")
rep("""host.addEventListener('pointermove',function(e){if(!ptrs[e.pointerId])return;e.stopPropagation();var pr=ptrs[e.pointerId],L=_loc(e);ptrs[e.pointerId]=L;var k=Object.keys(ptrs);""",
"""host.addEventListener('pointermove',function(e){if(!ptrs[e.pointerId])return;e.stopPropagation();var pr=ptrs[e.pointerId],L=_loc(e);ptrs[e.pointerId]=L;var k=Object.keys(ptrs);
  if(_tire){ if(k.length===1){ _tireBouge(L); try{ e.preventDefault(); }catch(_){ } } return; }   /* v142 : la dalle suit le doigt — la Toile ne défile pas */
  if(_tireP && _tireP.id===e.pointerId && Math.hypot(L.x-_tireP.x, L.y-_tireP.y)>TIRE_JEU){ clearTimeout(_tireT); _tireT=0; _tireP=null; }   /* le doigt a bougé avant 0,8 s : c'est un défilement */""")
rep("""function pu(e){e.stopPropagation();var L=ptrs[e.pointerId];delete ptrs[e.pointerId];var k=Object.keys(ptrs);""",
"""function pu(e){e.stopPropagation();var L=ptrs[e.pointerId];delete ptrs[e.pointerId];var k=Object.keys(ptrs);
  clearTimeout(_tireT); _tireT=0; _tireP=null; if(_tire){ _tireFin(true); _pan=null; kick(); return; }   /* v142 : au lâcher, la dalle reste où on l'a posée */""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
