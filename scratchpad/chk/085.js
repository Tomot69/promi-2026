
/* ⚑ LA PETITE TOILE D'UNE NUÉE (Q213, Tom 13 sept.) — dans l'Index et le Fil, les dalles d'une Nuée « occupent l'espace de la carte, réparties, comme une petite Toile ». Vraies dalles du moteur, dans leur monde (§4) ; chaque dalle prend une case du champ, hors du libellé, décalée et dimensionnée par SON id : même semis à chaque ouverture (§4, semis déterministe). */
window._petiteToile=function(g,A,Lr,ids){ try{
  var n=ids.length; if(n<2) return false;
  var ratio=A.w/A.h, cols=Math.max(1,Math.round(Math.sqrt(n*ratio*1.25))), rows=Math.ceil((n+2)/cols);
  while(cols*rows<n+3){ rows++; }
  var cw=A.w/cols, ch=A.h/rows, cells=[];
  for(var r=0;r<rows;r++)for(var c=0;c<cols;c++){ var cx=A.x+c*cw, cy=A.y+r*ch;
    if(cx < Lr.x+Lr.w && cy < Lr.y+Lr.h) continue; cells.push([cx,cy]); }
  var h=function(v,s){ var x=((v*2654435761)^(s*40503))>>>0; x^=x>>>15; x=Math.imul(x,2246822519)>>>0; x^=x>>>13; return (x%1000)/1000; };
  var cle=ids.reduce(function(a,b){return a+b;},0);
  cells.sort(function(a,b){ return h(Math.round(a[0]*7+a[1]*13),cle)-h(Math.round(b[0]*7+b[1]*13),cle); });
  var pick=cells.slice(0,n).sort(function(a,b){ return (a[1]-b[1])||(a[0]-b[0]); });
  var ok=false, rects=[];
  var _sxP=Math.hypot(g.getTransform().a,g.getTransform().b)||1;
  ids.forEach(function(pid,k){ var cel=pick[k]; if(!cel) return;
    var q=null; try{ q=promises.filter(function(x){return x.id===pid;})[0]; }catch(_){}
    /* ⚑ v29 — rendue par le moteur à la taille de sa case, posée 1:1 (redteam_decoupe) */
    var sz=Math.min(cw,ch)*(0.92+0.22*h(pid,3)), t=null;
    try{ t=window._rendDalle(pid, sz*_sxP, sz*_sxP);   /* ⚑ v34 : suit le Studio (Tom) */ }catch(_){ return; }
    if(!t||!t.width) return;
    var w=t.width/_sxP, hh=t.height/_sxP;
    var jx=(h(pid,1)-0.5)*Math.max(0,cw-w)*0.9, jy=(h(pid,2)-0.5)*Math.max(0,ch-hh)*0.9;
    var rx=cel[0]+(cw-w)/2+jx, ry=cel[1]+(ch-hh)/2+jy;
    /* ⚑ RIEN DEVANT LE LIBELLÉ (13 sept.) : la réserve n'écartait que les cases dont le COIN y tombe ; la dalle, centrée, jusqu'à 1,14 case
       et décalée, montait dans la zone du libellé 9 chargements sur 12 (sa hauteur respire avec dalleTrame). On borne la BOÎTE PEINTE. */
    if(rx < Lr.x+Lr.w && rx+w > Lr.x && ry < Lr.y+Lr.h && ry+hh > Lr.y) ry = Lr.y+Lr.h;
    window._poseUn(g, t, rx+w/2, ry+hh/2); rects.push([Math.round(rx),Math.round(ry),Math.round(w),Math.round(hh)]); ok=true; });
  window._ptRects=rects; return ok; }catch(e){ return false; } };