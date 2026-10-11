import io
S=io.open('promi-moteur.js',encoding='utf-8').read()
# 1 · le cadrage serré : sur les CELLULES des paroles (poids final), pas sur les graines + une marge
old="""  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;
  var bw=Math.max(1,maxX-minX), bh=Math.max(1,maxY-minY);
  var topB=HAUT_LIBRE, botB=H-BAS_LIBRE;    /* zone utile (barre haut + dock evites) */
  var availW=W*0.92, availH=Math.max(1,botB-topB);
  var s=Math.min(availW/bw, availH/bh);
  s=Math.max(1.0, Math.min(s, _serre?3.6:2.0));"""
assert S.count(old)==1
new="""  /* ⚑ v141 (Tom, 10 oct. 2026, C-088 — RÉCIDIVE : « trop dézoomé ») — les cibles, sur 390 pt : une parole → sa dalle fait au moins 60 % de la
     largeur ; deux, trois, quatre → toutes entières ; au plus deux cellules vides entièrement visibles jusqu'à quatre paroles.
     POURQUOI C'EST REVENU : v140 cadrait les GRAINES avec une marge (0,8 puis 1,25 cellule). Une marge autour de points ne dit rien de la
     taille des dalles : à une parole la dalle faisait 50 % de la largeur, à trois ou quatre la vue montrait 5 et 7 cellules vides.
     On cadre maintenant ce qu'on VOIT : la boîte des CELLULES des paroles, calculée à leur poids final (`_boiteSerre`), rentrée du joint
     entre deux dalles ; une parole seule occupe 70 % de la largeur, plusieurs toute la largeur utile. */
  var _bs=_serre?_boiteSerre(col):null;
  if(_bs){ minX=_bs.x0; maxX=_bs.x1; minY=_bs.y0; maxY=_bs.y1; } else { minX-=pad;maxX+=pad;minY-=pad;maxY+=pad; }
  var bw=Math.max(1,maxX-minX), bh=Math.max(1,maxY-minY);
  var topB=HAUT_LIBRE, botB=H-BAS_LIBRE;    /* zone utile (barre haut + dock evites) */
  if(_bs){ topB=H*(112/844); botB=H*(698/844); }   /* serré : entre le plateau (40 → 100) et la barre (710), 12 pt d'air */
  var availW=W*(_bs?(col.length===1?0.70:0.95):0.92), availH=Math.max(1,botB-topB);
  var s=Math.min(availW/bw, availH/bh);
  s=Math.max(1.0, Math.min(s, _serre?(_bs?5.0:3.6):2.0));"""
S=S.replace(old,new)
old="var HAUT_LIBRE=176, BAS_LIBRE=138;\nfunction autoView(){"
assert S.count(old)==1
new="""var HAUT_LIBRE=176, BAS_LIBRE=138;
/* v141 — la boîte des cellules des paroles, à leur poids FINAL (une dalle qui arrive part d'un poids négatif : sa cellule du moment est
   minuscule), rentrée du joint. Échantillonnée au pas de 3 autour de chaque parole. */
function _poidsFin(s){ return (s.kind!=='gray' && s.wFin!=null) ? s.wFin : (s.wt!=null?s.wt:(s.w||0)); }
function _boiteSerre(col){ try{
  var a=avg(), R=a*1.7, x0=1e9,y0=1e9,x1=-1e9,y1=-1e9, P=[], i, k;
  for(i=0;i<seeds.length;i++){ var q=seeds[i]; P.push([(q.tx!=null?q.tx:q.x),(q.ty!=null?q.ty:q.y),_poidsFin(q),q]); }
  for(i=0;i<col.length;i++){ var c=col[i], cx=(c.tx!=null?c.tx:c.x), cy=(c.ty!=null?c.ty:c.y), wc=_poidsFin(c);
    for(var y=Math.max(0,cy-R); y<=Math.min(H,cy+R); y+=3) for(var x=Math.max(0,cx-R); x<=Math.min(W,cx+R); x+=3){
      var d=Math.sqrt((x-cx)*(x-cx)+(y-cy)*(y-cy))-wc, ok=true;
      for(k=0;k<P.length;k++){ if(P[k][3]===c) continue; var e=Math.sqrt((x-P[k][0])*(x-P[k][0])+(y-P[k][1])*(y-P[k][1]))-P[k][2]; if(e<d){ ok=false; break; } }
      if(ok){ if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } } }
  if(x1<x0) return null; var j=a*0.13; if(x1-x0>4*j){ x0+=j; x1-=j; } if(y1-y0>4*j){ y0+=j; y1-=j; }
  return {x0:x0,y0:y0,x1:x1,y1:y1}; }catch(_){ return null; } }
function autoView(){"""
S=S.replace(old,new)
# 2 · Q449 : plus de dalle sous la barre du bas ; et un amas qui monte plutôt qu'il ne s'étale
old="    var libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-BAS_LIBRE;});"
assert S.count(old)==1
new="""    /* ⚑ v141 (Tom, 10 oct. 2026, Q449) : « on ne plante plus de dalle sous la barre du bas ». La barre commence à 710 (sur 844) ; une dalle
       plantée à 706 passait dessous de moitié (mesuré : une boîte de 702 à 788). La borne basse laisse la place d'une dalle entière
       (0,62 cellule) et de son décalage (0,25 cellule) au-dessus de la barre. */
    var _basP=H*(134/844)+avg()*0.87;
    var libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-_basP;});
    if(!libres.length) libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-BAS_LIBRE;});"""
S=S.replace(old,new)
old="if(_qe<_qd){ _qd=_qe; cible=_qp; } }"
assert S.count(old)==1
old2="_qe=(_qp.x-_qx)*(_qp.x-_qx)+(_qp.y-_qy)*(_qp.y-_qy);"
assert S.count(old2)==1
S=S.replace(old2,"_qe=(_qp.x-_qx)*(_qp.x-_qx)*3.2+(_qp.y-_qy)*(_qp.y-_qy);   /* v141 : l'écran est haut — l'amas monte plutôt qu'il ne s'étale (un écart en largeur compte 1,8 fois) */")
io.open('promi-moteur.js','w',encoding='utf-8').write(S)
