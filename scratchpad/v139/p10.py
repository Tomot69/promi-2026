import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:80]); S=S.replace(a,b)
rep("    PAS_OUTIL: 58,         /* d'un disque d'outil au suivant */","    PAS_OUTIL: 46,         /* d'un disque d'outil au suivant — v139 : 58 → 46, la rangée reçoit un cinquième disque (PHOTO) avant POSER */")
rep("    TAILLES: [2.5, 4.5, 8],          /* fin, moyen, gros — la pointe jamais sous 1 pt */\n    TAILLES_GOMME: [10, 18, 30],",
"""    /* ⚑ v139 (Tom, 9 oct. 2026, C-086) — « Les trois tailles de plume et de gomme doivent être nettement différentes sur la surface : à peu près
       2 · 6 · 14 pt pour la plume. Les trois points du choix le montrent à l'échelle. » (2,5 · 4,5 · 8 et 10 · 18 · 30 avant.) */
    TAILLES: [2, 6, 14],             /* fin, moyen, gros — la pointe jamais sous 1 pt */
    TAILLES_GOMME: [8, 18, 36],
    PHOTO_L: 0.6,          /* une photo importée arrive au centre, large de 60 % de la surface */
    PHOTO_MAX: 1024,       /* son plus grand côté, en pixels, une fois gardée */""")
# le rendu : une photo est un élément de la liste, comme un trait
rep("  function traceUn(g, tr, enCours){ var Q=points(tr); if(!Q.length) return;",
"""  /* ⚑ v139 (C-086) — UNE PHOTO IMPORTÉE EST UN ÉLÉMENT DE LA LISTE, à son rang parmi les traits : {img, x, y, w, h} (centre et taille, en points).
     Elle se dessine entière, opaque ; un trait fait après elle passe dessus, la gomme l'entame comme le reste. */
  var IMGS={};
  function imageDe(src){ var o=IMGS[src]; if(o) return o.complete && o.naturalWidth ? o : null; o=IMGS[src]=new Image();
    o.onload=function(){ MEMO={}; try{ if(M) rebatit(); bandes(); }catch(_){ } }; o.src=src; return (o.complete && o.naturalWidth) ? o : null; }
  function traceUn(g, tr, enCours){ if(tr.img){ var im=imageDe(tr.img); if(im){ g.save(); g.globalAlpha=1; g.globalCompositeOperation='source-over'; g.drawImage(im, tr.x-tr.w/2, tr.y-tr.h/2, tr.w, tr.h); g.restore(); } return; }
    var Q=points(tr); if(!Q.length) return;""")
rep("  function calque(traits, k, hPt){ var cv=document.createElement('canvas'); cv.width=Math.max(1,Math.round(W*k)); cv.height=Math.max(1,Math.round(hPt*k));\n    var g=cv.getContext('2d'); g.setTransform(k,0,0,k,0,0); (traits||[]).forEach(function(tr){ traceUn(g, tr); }); return cv; }",
    "  function calque(traits, k, hPt, sansPhoto){ var cv=document.createElement('canvas'); cv.width=Math.max(1,Math.round(W*k)); cv.height=Math.max(1,Math.round(hPt*k));\n    var g=cv.getContext('2d'); g.setTransform(k,0,0,k,0,0); (traits||[]).forEach(function(tr){ if(sansPhoto && tr.img) return; traceUn(g, tr); }); return cv; }")
rep("  function signature(d){ var n=0; (d.poses||[]).forEach(function(t){ n+=t.pts.length; }); return (d.fond||'')+'|'+(d.poses||[]).length+'|'+n+'|'+(d.h||0); }\n  function entier(d, k){ var cle=signature(d)+'|'+k; if(MEMO[cle]) return MEMO[cle];",
    "  function signature(d){ var n=0; (d.poses||[]).forEach(function(t){ n+= t.img ? (t.img.length+Math.round(t.x*7+t.y*13+t.w*17)) : t.pts.length; }); return (d.fond||'')+'|'+(d.poses||[]).length+'|'+n+'|'+(d.h||0); }\n  function entier(d, k, sansPhoto){ var cle=signature(d)+'|'+k+(sansPhoto?'|sp':''); if(MEMO[cle]) return MEMO[cle];")
rep("g.fillStyle=d.fond; g.fillRect(0,0,cv.width,cv.height); g.drawImage(calque(d.poses, k, hPt), 0, 0);","g.fillStyle=d.fond; g.fillRect(0,0,cv.width,cv.height); g.drawImage(calque(d.poses, k, hPt, sansPhoto), 0, 0);")
# le partage : « jamais une photo importée » (v137) — le dessin partagé est rendu sans ses photos
rep("if(!pose_(d) || d.masque) return null; return {cv:entier(d, 3), fond:d.fond, nat:nat}; }catch(_){ return null; } };",
    "if(!pose_(d) || d.masque) return null; return {cv:entier(d, 3, true) /* v139 : une photo importée dans le dessin n'est pas emportée (v137 : « jamais une photo importée ») — Q à Tom */, fond:d.fond, nat:nat}; }catch(_){ return null; } };")
rep("if(!p || !pose_(p.dessin) || p.dessin.masque) return null; return entier(p.dessin, 2); }catch(_){ return null; } };","if(!p || !pose_(p.dessin) || p.dessin.masque) return null; return entier(p.dessin, 2, true); }catch(_){ return null; } };")
# la rangée : PHOTO, et les points à l'échelle
rep("    b('dz-poser', W-P.MARGE_COTE-P.POSER_L, P.POSER_L, 'Poser', 'Poser le dessin', function(){ sort(true); }).setAttribute('data-outil','poser');",
"""    b('dz-o', x0+4*pas, 0, ICO.photo, 'Photo'+(M.outil==='photo'?', choisie : glisser une photo la déplace, pincer change sa taille. Toucher de nouveau pour en importer une autre':''), function(){ outilPhoto(); }, M.outil==='photo').setAttribute('data-outil','photo');
    b('dz-poser', W-P.MARGE_COTE-P.POSER_L, P.POSER_L, 'Poser', 'Poser le dessin', function(){ sort(true); }).setAttribute('data-outil','poser');""")
rep("""      [6,10,16].forEach(function(dd,i){ var e=document.createElement('button'); e.type='button'; e.className=(M.taille[o]===i?'on':''); e.style.left=(8+i*36)+'px';
        e.innerHTML='<i style="width:'+dd+'px;height:'+dd+'px"></i>';""",
"""      var _xt=8; (o==='gomme'?P.TAILLES_GOMME:P.TAILLES).forEach(function(dd,i){ var e=document.createElement('button'); e.type='button'; e.className=(M.taille[o]===i?'on':''); var bw=Math.max(26, dd+6); e.style.left=_xt+'px'; e.style.width=bw+'px'; e.style.height=bw+'px'; e.style.top=((44-bw)/2)+'px'; e.style.borderRadius=(bw/2)+'px'; _xt+=bw+8; p.style.width=_xt+'px';
        e.innerHTML='<i style="width:'+dd+'px;height:'+dd+'px"></i>';   /* v139 : le point à l'échelle du trait (1 pt pour 1 pt) */""")
rep("  function outil(o){ if(M.outil===o){ deploie(M.deploi===o?null:o); return; } M.outil=o; deploie(null); }",
"""  function outil(o){ if(M.outil===o){ deploie(M.deploi===o?null:o); return; } M.outil=o; deploie(null); }
  /* ⚑ v139 (Tom, 9 oct. 2026, C-086) — « Importer une ou plusieurs photos dans le dessin, chacune déplaçable et redimensionnable au pincement, puis
     posée avec le reste. » Le cinquième disque, PHOTO : le toucher le choisit (et ouvre le sélecteur du téléphone s'il n'y a pas encore de
     photo) ; choisi, toucher une photo sur la surface la prend — un doigt la déplace, deux doigts changent sa taille ; le toucher de nouveau
     en importe d'autres. ANNULER la retire comme un trait ; POSER la pose avec le reste. */
  function photos(){ return M.d.traits.filter(function(t){ return !!t.img; }); }
  function importe(){ var r=$('dessinMode'), inp=r.querySelector('input.dz-photo-in'); if(!inp){ inp=document.createElement('input'); inp.type='file'; inp.accept='image/*'; inp.multiple=true; inp.className='dz-photo-in'; inp.setAttribute('aria-hidden','true'); inp.tabIndex=-1;
      inp.style.cssText='position:absolute;left:-9999px;top:0;width:1px;height:1px;opacity:0'; r.appendChild(inp);
      inp.addEventListener('change', function(){ var F=[].slice.call(inp.files||[]); inp.value=''; F.forEach(function(fi, i){ var rd=new FileReader(); rd.onload=function(){ ajoutePhoto(rd.result, i); }; rd.readAsDataURL(fi); }); }); }
    window._dessinImporte=(window._dessinImporte||0)+1; try{ inp.click(); }catch(_){ } }
  function ajoutePhoto(src, rang){ if(!M) return; var im=new Image(); im.onload=function(){ if(!M) return; var mx=Math.max(im.naturalWidth, im.naturalHeight), s=src;
      if(mx>P.PHOTO_MAX){ try{ var kq=P.PHOTO_MAX/mx, c=document.createElement('canvas'); c.width=Math.round(im.naturalWidth*kq); c.height=Math.round(im.naturalHeight*kq); c.getContext('2d').drawImage(im,0,0,c.width,c.height); s=c.toDataURL('image/jpeg',0.86); }catch(_){ s=src; } }
      var w=W*P.PHOTO_L, h=w*im.naturalHeight/im.naturalWidth; if(h>M.hS*0.7){ h=M.hS*0.7; w=h*im.naturalWidth/im.naturalHeight; }
      var o={img:s, x:W/2+(rang||0)*14, y:M.hS/2+(rang||0)*14, w:Math.round(w*10)/10, h:Math.round(h*10)/10}; M.d.traits.push(o); M.outil='photo'; garde_(); imageDe(s); rebatit(); rangee(); }; im.src=src; }
  function outilPhoto(){ if(M.outil==='photo' || !photos().length){ M.outil='photo'; deploie(null); importe(); return; } M.outil='photo'; deploie(null); }
  function sous(q){ for(var i=M.d.traits.length-1;i>=0;i--){ var t=M.d.traits[i]; if(t.img && Math.abs(q.x-t.x)<=t.w/2 && Math.abs(q.y-t.y)<=t.h/2) return t; } return null; }
  var PH=null;   /* la photo en main : {t, ptrs:{id:{x,y}}, …} */
  function phDebut(e){ var q=pt(e); if(!PH){ var t=sous(q); if(!t) return; PH={t:t, ptrs:{}}; } PH.ptrs[e.pointerId]={x:q.x, y:q.y}; phCale(); try{ e.currentTarget.setPointerCapture(e.pointerId); }catch(_){ } }
  function phCale(){ var ids=Object.keys(PH.ptrs), a=PH.ptrs[ids[0]], b=PH.ptrs[ids[1]]; PH.x0=PH.t.x; PH.y0=PH.t.y; PH.w0=PH.t.w; PH.h0=PH.t.h;
    if(b){ PH.m0={x:(a.x+b.x)/2, y:(a.y+b.y)/2, d:Math.hypot(a.x-b.x, a.y-b.y)||1}; } else { PH.m0={x:a.x, y:a.y, d:0}; } }
  function phBouge(e){ if(!PH || !PH.ptrs[e.pointerId]) return; var q=pt(e); PH.ptrs[e.pointerId]={x:q.x, y:q.y}; var ids=Object.keys(PH.ptrs), a=PH.ptrs[ids[0]], b=PH.ptrs[ids[1]], t=PH.t;
    if(b && PH.m0.d){ var m={x:(a.x+b.x)/2, y:(a.y+b.y)/2, d:Math.hypot(a.x-b.x, a.y-b.y)||1}, f=m.d/PH.m0.d, w=Math.max(24, Math.min(W*4, PH.w0*f)); f=w/PH.w0;
      t.w=w; t.h=PH.h0*f; t.x=m.x+(PH.x0-PH.m0.x)*f; t.y=m.y+(PH.y0-PH.m0.y)*f; }
    else { t.x=PH.x0+(a.x-PH.m0.x); t.y=PH.y0+(a.y-PH.m0.y); }
    if(!RAF) RAF=requestAnimationFrame(function(){ RAF=0; if(M) rebatit(); }); }
  function phFin(e){ if(!PH || !PH.ptrs[e.pointerId]) return; delete PH.ptrs[e.pointerId]; if(Object.keys(PH.ptrs).length){ phCale(); return; }
    var t=PH.t; PH=null; t.x=Math.round(t.x*10)/10; t.y=Math.round(t.y*10)/10; t.w=Math.round(t.w*10)/10; t.h=Math.round(t.h*10)/10; garde_(); rebatit(); }""")
rep("  function debut(e){ if(!M || M.trait || (e.button!=null && e.button>0)) return; e.preventDefault();\n    if(M.deploi){ deploie(null); }",
    "  function debut(e){ if(M && M.outil==='photo'){ e.preventDefault(); if(M.deploi) deploie(null); phDebut(e); return; }   /* v139 : PHOTO choisie — la surface déplace les photos, elle ne trace pas */\n    if(!M || M.trait || (e.button!=null && e.button>0)) return; e.preventDefault();\n    if(M.deploi){ deploie(null); }")
rep("  function bouge(e){ if(!M || !M.trait || e.pointerId!==M.trait.id) return; e.preventDefault();","  function bouge(e){ if(PH){ e.preventDefault(); phBouge(e); return; }\n    if(!M || !M.trait || e.pointerId!==M.trait.id) return; e.preventDefault();")
rep("  function fin(e){ if(!M || !M.trait || e.pointerId!==M.trait.id) return; e.preventDefault();","  function fin(e){ if(PH){ e.preventDefault(); phFin(e); return; }\n    if(!M || !M.trait || e.pointerId!==M.trait.id) return; e.preventDefault();")
rep("    var c=M.c, d=M.d; M.trait=null;\n","    var c=M.c, d=M.d; M.trait=null; PH=null;\n")
rep("  var M=null;   /* l'état du mode","  ICO.photo='<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><rect x=\"3.5\" y=\"5\" width=\"17\" height=\"14\" rx=\"2.5\"/><path d=\"M3.5 15.5l4.8-4.6 4.2 4 2.8-2.6 5.2 4.9\"/><circle cx=\"15.6\" cy=\"9.4\" r=\"1.3\"/></svg>';\n  var M=null;   /* l'état du mode")
rep("choix:function(){ return M ? {trait:choixTrait(), fond:choixFond()} : null; }, surface:surfH, trace:traceUn, entier:entier};",
    "choix:function(){ return M ? {trait:choixTrait(), fond:choixFond()} : null; }, surface:surfH, trace:traceUn, entier:entier, ajoutePhoto:function(src){ ajoutePhoto(src, 0); }, photos:function(){ return M ? photos().map(function(t){ return {x:t.x, y:t.y, w:t.w, h:t.h}; }) : []; }};")
io.open(f,'w',encoding='utf-8').write(S)
