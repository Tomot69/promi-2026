import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif absent ou multiple', S.count(old), old[:80]); S=S.replace(old,new)
rep("""  T.guide={ studio:'Chacun sa matière. La tienne est au Studio.',   /* les mots de Tom (lot v141) */
            plus:'Tout le reste part d’ici.',                      /* les mots de Tom (lot v141) */
            plusTard:'Plus tard' };""",
"""  /* ⚑ v142 (Tom, 11 oct. 2026, C-094 — RÉCIDIVE : « pas de zones arty, Studio pas grossi, pas fluide, ça fait bordel, pas d'étape sur le + »).
     CE QUI N'ALLAIT PAS, NOMMÉ : ① « pas fluide » — le flou était UNE couche dont le MASQUE (jusqu'à 25 dégradés radiaux) était réécrit à chaque
     image : le navigateur re-tramait un masque de 1170 × 2532 px à chaque image ; ② « pas de zones arty » — 24 ellipses qui se recouvraient :
     un seul nuage à bord mou, pas des taches ; ③ « Studio pas grossi » — l'agrandissement tenait à une règle CSS (`transform`) sur le bouton
     de la barre, sans effet là où une autre règle de la barre gagne ; il est posé EN LIGNE, et mesuré ; ④ « pas d'étape sur le + » — après
     le toucher du Studio, le guide attendait 2,5 s puis, l'accueil toujours à l'écran (le Studio met plusieurs secondes à se bâtir sur
     l'iPhone), montrait l'étape du + AVANT que le Studio ne paraisse : le Studio la recouvrait, le guide se retirait, tout était fini.
     AUJOURD'HUI : le flou est une couche dont la DÉCOUPE (`clip-path`, un tracé vectoriel) grandit — six taches à bord courbe, nées de six
     points, qui s'étendent et se rejoignent jusqu'à tout couvrir en 1,8 s ; ce qui reste net est un trou FIXE du masque (tramé une fois) ;
     l'étape du + n'arrive qu'une fois le Studio VU ouvert, puis refermé. */
  T.guide={ studio:'Vingt mondes pour une seule Toile. Le tien est au Studio.',   /* les mots de Tom (lot v142) */
            plus:'Promi, Chiche ou Cercle : tout commence par ce +.',            /* les mots de Tom (lot v142) */
            plusTard:'Plus tard' };""")
rep("""  var CLE='promi_guide', INSTALLE=1500, DISSOUT=380, ATTENTE=800;""","""  var CLE='promi_guide', INSTALLE=1800, DISSOUT=380, ATTENTE=800, TACHES=6, GROS={studio:1.15, plus:1.10};""")
i0=S.index("  /* les zones : huit foyers sur une grille bousculée, trois ellipses chacun — tirées une fois par apparition */")
i1=S.index("  function image(){ if(!etat || (etat!=='studio' && etat!=='plus' && etat!=='part')) return;")
S=S[:i0]+"""  /* les taches : six foyers sur une grille bousculée (2 × 3) ; chacune est une forme fermée à bord courbe (dix rayons inégaux, reliés par des
     courbes), tirée une fois par apparition ; elle naît à son heure (0 à 0,3 de la durée) et grandit doucement jusqu'à couvrir sa part. */
  function zones(){ var sd=((Date.now()&0x7fffffff)|1), R=function(){ sd=(Math.imul(sd,1103515245)+12345)&0x7fffffff; return sd/0x7fffffff; }, L=[], ordre=[0,1,2,3,4,5];
    for(var i=5;i>0;i--){ var j=(R()*(i+1))|0, t=ordre[i]; ordre[i]=ordre[j]; ordre[j]=t; }
    for(var n=0;n<TACHES;n++){ var gx=n%2, gy=(n/2)|0, M=[], NA=10;
      for(var a=0;a<NA;a++) M.push(0.80+R()*0.40);
      L.push({x:98+gx*194+(R()-0.5)*80, y:140+gy*282+(R()-0.5)*110, R:350, M:M, rot:R()*6.283, d:ordre[n]*0.06}); }
    return L; }
  function ease(v){ return v<=0?0:(v>=1?1:v*v*v*(v*(v*6-15)+10)); }
  /* le tracé de la découpe à l'instant u (0 → 1) : l'union des taches ; à 1, l'écran entier */
  function chemin(u){ if(u>=1) return 'M0 0H390V844H0Z'; var s='';
    for(var i=0;i<Z.length;i++){ var b=Z[i], v=ease((u-b.d)/(1-b.d)); if(v<=0.004) continue; var NA=b.M.length, P=[], a;
      for(a=0;a<NA;a++){ var an=b.rot+a/NA*6.283185, r=b.R*v*b.M[a]; P.push([b.x+Math.cos(an)*r, b.y+Math.sin(an)*r]); }
      s+='M'+P[0][0].toFixed(1)+' '+P[0][1].toFixed(1);
      for(a=0;a<NA;a++){ var p0=P[(a-1+NA)%NA], p1=P[a], p2=P[(a+1)%NA], p3=P[(a+2)%NA];   /* une courbe lisse par les points (Catmull-Rom → Bézier) */
        s+='C'+(p1[0]+(p2[0]-p0[0])/6).toFixed(1)+' '+(p1[1]+(p2[1]-p0[1])/6).toFixed(1)+' '+(p2[0]-(p3[0]-p1[0])/6).toFixed(1)+' '+(p2[1]-(p3[1]-p1[1])/6).toFixed(1)+' '+p2[0].toFixed(1)+' '+p2[1].toFixed(1); }
      s+='Z'; }
    return s||'M0 0H0V0Z'; }
  function masque(u){ var f=$('guideFlou'); if(!f) return; var c='path(nonzero, "'+chemin(u)+'")'; f.style.webkitClipPath=c; f.style.clipPath=c; f.setAttribute('data-u', u.toFixed(3)); }
  /* le trou : ce qui reste net — un masque FIXE (une image vectorielle, tramée une fois) : l'écran plein, moins un rectangle arrondi */
  function poseTrou(){ var f=$('guideFlou'); if(!f||!trou) return; var x=trou.x-trou.w/2, y=trou.y-trou.h/2, r=Math.min(trou.r, trou.w/2, trou.h/2), w=trou.w, h=trou.h;
    var d='M0 0H390V844H0Z M'+(x+r)+' '+y+'h'+(w-2*r)+'a'+r+' '+r+' 0 0 1 '+r+' '+r+'v'+(h-2*r)+'a'+r+' '+r+' 0 0 1 '+(-r)+' '+r+'h'+(-(w-2*r))+'a'+r+' '+r+' 0 0 1 '+(-r)+' '+(-r)+'v'+(-(h-2*r))+'a'+r+' '+r+' 0 0 1 '+r+' '+(-r)+'Z';
    var svg="url(\\"data:image/svg+xml;utf8,"+encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' width='390' height='844' viewBox='0 0 390 844'><path fill='black' fill-rule='evenodd' d='"+d+"'/></svg>")+"\\")";
    f.style.webkitMaskImage=svg; f.style.maskImage=svg; f.style.webkitMaskSize='390px 844px'; f.style.maskSize='390px 844px'; f.style.webkitMaskRepeat='no-repeat'; f.style.maskRepeat='no-repeat'; }
"""+S[i1:]
rep("""  function retire(){ try{ cancelAnimationFrame(raf); }catch(_){ } var g=$('guide'); if(g) g.remove(); dev.classList.remove('guide-studio'); dev.classList.remove('guide-plus'); trou=null; }""",
"""  function retire(){ try{ cancelAnimationFrame(raf); }catch(_){ } var g=$('guide'); if(g) g.remove(); dev.classList.remove('guide-studio'); dev.classList.remove('guide-plus'); trou=null;
    if(grossi){ try{ grossi.n.style.removeProperty('transform'); grossi.n.style.removeProperty('transform-origin'); if(grossi.av) grossi.n.style.setProperty('transform', grossi.av[0], grossi.av[1]); }catch(_){ } grossi=null; } }
  var grossi=null;""")
rep("""    trou={x:(r.left+r.width/2-D.left)/kk, y:(r.top+r.height/2-D.top)/kk, r:(quoi==='studio'?37:50)};   /* 37 : l'icône grossie et son nom, sans mordre sur « AURA » ; 50 : la hauteur de la barre — le + dans un rond d'encart, sans mordre sur ses voisines */""",
"""    /* ce qui reste net est AGRANDI (15 % le Studio, 10 % le +), posé en ligne sur le vrai bouton, depuis son centre — et rendu à la fin */
    var gr=GROS[quoi], av=cible.style.getPropertyValue('transform'); grossi={n:cible, av:av?[av, cible.style.getPropertyPriority('transform')]:null};
    cible.style.setProperty('transform-origin','50% 50%','important'); cible.style.setProperty('transform','scale('+gr+')','important');
    var w0=r.width/kk, h0=r.height/kk;
    trou=(quoi==='studio') ? {x:(r.left+r.width/2-D.left)/kk, y:(r.top+r.height/2-D.top)/kk, w:w0*gr+10, h:h0*gr+10, r:16}        /* l'icône et le mot STUDIO, agrandis, 5 pt d'air */
                           : {x:(r.left+r.width/2-D.left)/kk, y:(r.top+r.height/2-D.top)/kk, w:Math.max(w0,h0)*gr+10, h:Math.max(w0,h0)*gr+10, r:999};   /* le + et son encart rond, agrandis */""")
rep("""    c.style.cssText='position:absolute;left:'+(trou.x-trou.r)+'px;top:'+(trou.y-trou.r)+'px;width:'+(trou.r*2)+'px;height:'+(trou.r*2)+'px;border-radius:50%;margin:0;padding:0;max-width:none;background:transparent'; g.appendChild(c);
    dev.appendChild(g); dev.classList.add('guide-'+quoi);""",
"""    c.style.cssText='position:absolute;left:'+(trou.x-trou.w/2)+'px;top:'+(trou.y-trou.h/2)+'px;width:'+trou.w+'px;height:'+trou.h+'px;border-radius:'+Math.min(trou.r,trou.w/2)+'px;margin:0;padding:0;max-width:none;background:transparent'; g.appendChild(c);
    dev.appendChild(g); dev.classList.add('guide-'+quoi); poseTrou();""")
rep("""      if(trou && Math.hypot(x-trou.x, yy-trou.y)<=trou.r+4){ if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); return; }""",
"""      if(trou && Math.abs(x-trou.x)<=trou.w/2+4 && Math.abs(yy-trou.y)<=trou.h/2+4){ if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); return; }""")
rep("""      else if(vuStudio || now-tVu>2500){ if(!tAcc) tAcc=now; if(now-tAcc>=450){ tAcc=0; montre('plus'); } } }""",
"""      else if(vuStudio || now-tVu>20000){ if(!tAcc) tAcc=now; if(now-tAcc>=ATTENTE){ tAcc=0; montre('plus'); } } }   /* v142 : seulement une fois le Studio VU ouvert puis refermé (20 s : un Studio qui ne s'ouvrirait jamais) ; le même calme de 0,8 s */""")
# le CSS
rep("""#device #guideFlou{position:absolute;left:0;top:0;width:390px;height:844px;margin:0;padding:0;max-width:none;pointer-events:none;
  -webkit-backdrop-filter:blur(4.8px);backdrop-filter:blur(4.8px);-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}""",
"""#device #guideFlou{position:absolute;left:0;top:0;width:390px;height:844px;margin:0;padding:0;max-width:none;pointer-events:none;
  -webkit-backdrop-filter:blur(4.8px);backdrop-filter:blur(4.8px);-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;will-change:clip-path}""")
rep("""#device#device.guide-studio #accBarre #studioBtn{transform:scale(1.2)!important;transform-origin:50% 50%!important}
#device#device.guide-plus #accBarre #createBtn{transform:scale(1.1)!important;transform-origin:50% 50%!important}""",
"""/* v142 : l'agrandissement (15 % le Studio, 10 % le +) est posé EN LIGNE par le guide (lot-V141-GUIDE, `grossi`) — une règle ici ne gagnait pas partout */""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
