import io
f='promi-moteur.js'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
T="if(_cibleDalle!=null&&(%s.pid!==_cibleDalle||%s.kind==='gray'))"
rep("var sb=seeds[bi],c=cOf(sb,now),col='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';if(col===_rs&&_ry===sy", "var sb=seeds[bi];"+T%('sb','sb')+"{_rv();continue;}   /* v130 : une dalle seule = SES carrés, engendrés — jamais la Toile découpée */var c=cOf(sb,now),col='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';if(col===_rs&&_ry===sy")
rep("var s=seeds[bi],c=cOf(s,now),ed=(bd2-bd)<5*UK,", "var s=seeds[bi];"+T%('s','s')+"continue;   /* v130 : SES points */var c=cOf(s,now),ed=(bd2-bd)<5*UK,")
rep("var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx+UK*_vv,sy+UK*_vv,T-2*UK*_vv,T-2*UK*_vv);}}}", T%('seeds[bi]','seeds[bi]')+"continue;   /* v130 : SES tesselles */var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx+UK*_vv,sy+UK*_vv,T-2*UK*_vv,T-2*UK*_vv);}}}")
rep("for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0,ins=qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins){if(_G){",
    "for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;"+T%('s','s')+"continue;   /* v130 : SES hachures */var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0,ins=qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins){if(_G){")
_a="var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY),c=cOf(s,now),key="; _i=S.index("function RsilDirect("); _j=S.index(_a,_i); assert _j-_i<1500; S=S[:_j]+"var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY);"+T%('s','s')+"{flush();run=[];rk=null;continue;}   /* v130 : SES ondes */var c=cOf(s,now),key="+S[_j+len(_a):]
# le masque au pixel : plus pour ces cinq mondes (seul le bord de la Toile borne encore)
rep("            if(lx<_bT[0]||lx>_bT[2]||ly<_bT[1]||ly>_bT[3]){ dd[o4+3]=0; continue; }","            if(lx<_bT[0]||lx>_bT[2]||ly<_bT[1]||ly>_bT[3]){ dd[o4+3]=0; continue; }\n            if(_ENGENDRE[theme]) continue;   /* v130 : le monde n'a peint QUE les éléments de cette dalle — rien à découper */")
rep("window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){\n  /* ⚑ v29 (Tom, 23 sept.) — DEUX AJOUTS AU MOTEUR","""/* ⚑ v130 (Tom, C-048 — RÉCIDIVE de la règle du 23 sept.) — UNE DALLE SEULE EST ENGENDRÉE, JAMAIS DÉCOUPÉE DANS LA TOILE.
   « On voit de nouveau des morceaux de Toile capturés dans un cadre, au lieu de vraies dalles engendrées, avec leur forme et leur
   contour réels. C'est interdit, définitivement. » LA CAUSE (présente depuis v29, pas un retour récent : v124 rend la même image) :
   pour les cinq mondes à trame — Buvard, Braille, Tesselle, Taille-douce, Houle — `dalleTrame` peignait TOUTE la Toile autour de la
   dalle, puis l'effaçait pixel par pixel hors de la cellule. Le découpage géométrique ne suit pas les éléments du monde : il tranchait
   les carrés de Buvard (un contour droit au lieu de ses marches) et gardait des éclats des voisines (les « bouts noirs » en sombre).
   DÉSORMAIS le peintre, quand il rend une dalle seule (`_cibleDalle`), ne trace QUE les éléments qui lui appartiennent — ses carrés,
   ses points, ses tesselles, ses hachures, ses ondes — et plus rien n'est découpé : le contour est celui de la matière.
   `redteam_decoupe` famille G (« fragment de Toile ») le juge : aucun élément d'une autre graine dans le canevas d'une dalle. */
var _ENGENDRE={pixel:1,braille:1,mosaique:1,gravure:1,sillons:1};
window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){
  /* ⚑ v29 (Tom, 23 sept.) — DEUX AJOUTS AU MOTEUR""")
io.open(f,'w',encoding='utf-8').write(S)
