import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
# 1 · le peintre : le cadrage choisi au doigt
rep("""    g.globalAlpha=1; g.globalCompositeOperation='source-over';
    g.drawImage(im, sx,sy,sw,sh, b.x,b.y,b.w,b.h);""",
"""    g.globalAlpha=1; g.globalCompositeOperation='source-over';
    /* ⚑ v139 (Tom, 9 oct. 2026, C-085) — LE CADRAGE AU DOIGT. Tant qu'on n'a rien touché, la photo garde sa boîte (ci-dessous). Dès qu'on la pince ou
       qu'on la glisse (`p.photoCadre` = {z, dx, dy, n}), elle se dessine ENTIÈRE, à z fois sa taille de couverture, centrée sur le centre de
       la boîte décalé de (dx, dy) : « elle peut remplir tout le haut, être très zoomée ou dézoomée ». Le découpage reste celui de l'onde. */
    window._photoCentre={x:b.x+b.w/2, y:b.y+b.h/2, s0:Math.max(b.w/im.width, b.h/im.height), w:im.width, h:im.height};
    var pc=p.photoCadre; if(pc && pc.n===src.length){ var s1=window._photoCentre.s0*pc.z, dw=im.width*s1, dh=im.height*s1;
      g.drawImage(im, b.x+b.w/2+pc.dx-dw/2, b.y+b.h/2+pc.dy-dh/2, dw, dh); }
    else
    g.drawImage(im, sx,sy,sw,sh, b.x,b.y,b.w,b.h);""")
rep("      if(d && !d.photo && !d.req){ d.photo=ph; }","      if(d && !d.photo && !d.req){ d.photo=ph; var _pc=(window._phrase||{}).photoCadre; if(_pc && _pc.n===ph.length) d.photoCadre={z:_pc.z, dx:_pc.dx, dy:_pc.dy, n:_pc.n};   /* v139 : le cadrage suit la photo à la plantation */ }")
# 2 · la vue en entier : le bouton, la porte de dansBande, le garde du cadrage
rep("""    v.innerHTML='<img alt=""><button type="button" class="ev-x" aria-label="Fermer">✕ Fermer</button>';""",
"""    v.innerHTML='<img alt=""><button type="button" class="ev-x" aria-label="Fermer">✕ Fermer</button><button type="button" class="ev-garde" data-v139="enregistrer">Enregistrer la photo</button>';""")
rep("""    v.classList.add('ouv'); return true; }
  window._entier={ouvre:ouvre, ferme:ferme, ouverte:ouverte};""",
"""    var eg=v.querySelector('.ev-garde'); if(eg){ eg.style.display = s.quoi==='photo' ? '' : 'none'; }   /* v139 : seulement pour une photo */
    v.classList.add('ouv'); return true; }
  /* ⚑ v139 (Tom, 9 oct. 2026, C-085) — « En plein écran, un petit bouton “Enregistrer la photo”. » La photo d'origine, entière : la feuille de
     partage du téléphone quand elle sait prendre un fichier (elle porte « Enregistrer l'image »), sinon un téléchargement. */
  function enregistre(){ var v=document.getElementById('entierVue'), im=v&&v.querySelector('img'), src=im&&im.getAttribute('src'); if(!src) return false;
    window._entierEnregistre=(window._entierEnregistre||0)+1;
    var ext=(/^data:image\\/(png|webp|gif)/.exec(src)||[])[1]||'jpg', nom='promi-photo.'+ext;
    function telecharge(){ try{ var a=document.createElement('a'); a.href=src; a.download=nom; a.rel='noopener'; document.body.appendChild(a); a.click(); a.parentNode.removeChild(a); }catch(_){ } }
    try{ if(navigator.share && navigator.canShare && /^data:/.test(src)){ var p=src.split(','), bin=atob(p[1]), u=new Uint8Array(bin.length); for(var i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i);
        var fi=new File([u], nom, {type:(/^data:([^;]+)/.exec(src)||[])[1]||'image/jpeg'}); if(navigator.canShare({files:[fi]})){ navigator.share({files:[fi]}).catch(function(){}); return true; } } }catch(_){ }
    telecharge(); return true; }
  window._entier={ouvre:ouvre, ferme:ferme, ouverte:ouverte, enregistre:enregistre};""")
rep("""    if(g.vue){ if(ouverte()){ ferme(); AVALE=performance.now(); e.preventDefault(); e.stopPropagation(); } return; }      /* un nouveau toucher, ou ✕ : referme */""",
"""    if(g.vue){ if(ouverte()){ if(e.target && e.target.closest && e.target.closest('.ev-garde')){ enregistre(); AVALE=performance.now(); e.preventDefault(); e.stopPropagation(); return; }   /* v139 : le bouton n'est pas « un nouveau toucher » */
        ferme(); AVALE=performance.now(); e.preventDefault(); e.stopPropagation(); } return; }      /* un nouveau toucher, ou ✕ : referme */
    if(window._cadreT && performance.now()-window._cadreT<500) return;   /* v139 : on vient de cadrer la photo — ce lever n'est pas un toucher */""")
rep("""    if(ouverte()){ if(e.target && e.target.closest && e.target.closest('#entierVue')){ ferme(); e.preventDefault(); e.stopPropagation(); } return; }""",
"""    if(ouverte()){ if(e.target && e.target.closest && e.target.closest('.ev-garde')){ enregistre(); e.preventDefault(); e.stopPropagation(); return; }
      if(e.target && e.target.closest && e.target.closest('#entierVue')){ ferme(); e.preventDefault(); e.stopPropagation(); } return; }""")
rep("  window._entier.annonce=annonce;","  window._entier.annonce=annonce; window._entier.dansBande=dansBande; window._entier.hote=fiche;")
rep("#device #entierVue.ouv{display:block}","""#device #entierVue.ouv{display:block}
/* v139 (C-085) : le petit bouton « Enregistrer la photo » — la grammaire des contours (2 px, rayon = hauteur ÷ 2), crème sur la seiche */
#device #entierVue .ev-garde{position:absolute;left:50%;bottom:46px;transform:translateX(-50%);height:44px;padding:0 20px;border-radius:22px;border:2px solid var(--c-creme95);background:var(--c-seiche10);color:var(--c-creme95);-webkit-text-fill-color:var(--c-creme95);font-family:Gilbert,system-ui;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin:0;white-space:nowrap;cursor:pointer;max-width:none}""")
# 3 · le geste
a=S.index('<style id="lot-E1-GESTES-css">')
S=S[:a]+r"""<script id="lot-V139-CADRE">
/* ⚑ v139 (Tom, 9 oct. 2026, C-085) — LA PHOTO D'UNE FICHE SE CADRE AU DOIGT. « Recadrer au pincement, comme dans Photos sur iPhone, avec la même
   sensibilité : on écarte ou on rapproche deux doigts pour zoomer, on glisse pour déplacer. Elle peut remplir tout le haut, être très zoomée ou
   dézoomée. Le cadrage est mémorisé par fiche. » Fiche (Promi, Chiche) et page + ; un Cercle ne porte pas de photo.
   · deux doigts : le zoom suit l'écart des doigts (rapport 1:1), le point sous leur milieu reste sous leur milieu ; un doigt : la photo suit le doigt ;
   · le cadrage vit sur ce qui porte la photo (`p.photoCadre` = {z, dx, dy, n}, en points de l'écran 390) et se sauvegarde avec lui ;
   · un toucher sans glisser reste le toucher qui ouvre la photo en entier ; un pincement ou un glissement ne l'ouvre pas ;
   · pendant le geste, rien d'autre ne le reçoit (ni le défilement de la fiche, ni son Peaufiner). Bornes : z de 0,3 à 8. */
(function(){
  var ZMIN=0.3, ZMAX=8, SEUIL=10;
  function hote(){ try{ return window._entier.hote(); }catch(_){ return null; } }
  function porteur(dp){ try{ if(!dp || document.getElementById('dessinMode') || (window._entier.ouverte && window._entier.ouverte())) return null;
      if(dp.classList.contains('s2-ouv') || dp.classList.contains('pp-peauf')) return null;
      if(window._dessin && window._dessin.sourceVue && window._dessin.sourceVue()) return null;                       /* la bande montre un dessin */
      if(dp.id==='createSheet') return (window._phrase && window._phrase.photo) ? window._phrase : null;
      if(dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee')) return null;
      return (typeof cur!=='undefined' && cur && cur.photo) ? cur : null; }catch(_){ return null; } }
  function toile(dp){ return document.getElementById(dp.id==='createSheet' ? 'csTrameCv' : 'dpTrameCv'); }
  function cadre(p){ var c=p.photoCadre; if(!c || c.n!==p.photo.length) c=p.photoCadre={z:1, dx:0, dy:0, n:p.photo.length}; return c; }
  var RAF=0;
  function repeint(dp){ if(RAF) return; RAF=requestAnimationFrame(function(){ RAF=0; try{ if(dp.id==='createSheet'){ if(window._ppTrait) _ppTrait(); } else if(window._ficheTrait) _ficheTrait(); }catch(_){ } }); }
  function sauve(){ try{ if(window.saveState) saveState(); }catch(_){ } }
  var G=null;   /* {dp, p, k, r, mode:'attente'|'glisse'|'pince', … } */
  function milieu(t){ return {x:(t[0].clientX+t[1].clientX)/2, y:(t[0].clientY+t[1].clientY)/2, d:Math.hypot(t[0].clientX-t[1].clientX, t[0].clientY-t[1].clientY)||1}; }
  function debut(e){ var t=e.touches; if(!t || !t.length) return; var dp=hote(), p=porteur(dp); if(!p){ G=null; return; }
    if(t.length===1){ if(!window._entier.dansBande(t[0].clientX, t[0].clientY)){ G=null; return; }
      var cv=toile(dp), r=cv.getBoundingClientRect(); G={dp:dp, p:p, k:r.width/390||1, r:r, mode:'attente', x0:t[0].clientX, y0:t[0].clientY}; return; }
    if(t.length===2){ if(!G){ if(!window._entier.dansBande(t[0].clientX, t[0].clientY) && !window._entier.dansBande(t[1].clientX, t[1].clientY)) return; var cv2=toile(dp), r2=cv2.getBoundingClientRect(); G={dp:dp, p:p, k:r2.width/390||1, r:r2}; }
      var c=cadre(G.p), m=milieu(t); G.mode='pince'; G.m0=m; G.z0=c.z; G.dx0=c.dx; G.dy0=c.dy; window._cadreT=performance.now(); try{ e.preventDefault(); }catch(_){ } e.stopPropagation(); } }
  function bouge(e){ if(!G) return; var t=e.touches, c;
    if(G.mode==='pince' && t.length>=2){ c=cadre(G.p); var m=milieu(t), C=window._photoCentre||{x:195,y:150}, z=Math.max(ZMIN, Math.min(ZMAX, G.z0*m.d/G.m0.d)), f=z/G.z0;
      /* le point de la photo qui était sous le milieu des doigts y reste : centre' = milieu' + (centre − milieu) × f */
      var cx0=G.r.left+(C.x+G.dx0)*G.k, cy0=G.r.top+(C.y+G.dy0)*G.k;
      c.z=z; c.dx=(m.x+(cx0-G.m0.x)*f-G.r.left)/G.k-C.x; c.dy=(m.y+(cy0-G.m0.y)*f-G.r.top)/G.k-C.y;
      window._cadreT=performance.now(); try{ e.preventDefault(); }catch(_){ } e.stopPropagation(); repeint(G.dp); return; }
    if(t.length!==1) return;
    if(G.mode==='attente'){ if(Math.hypot(t[0].clientX-G.x0, t[0].clientY-G.y0)<SEUIL) return; c=cadre(G.p); G.mode='glisse'; G.x0=t[0].clientX; G.y0=t[0].clientY; G.dx0=c.dx; G.dy0=c.dy; }
    if(G.mode==='glisse'){ c=cadre(G.p); c.dx=G.dx0+(t[0].clientX-G.x0)/G.k; c.dy=G.dy0+(t[0].clientY-G.y0)/G.k; window._cadreT=performance.now(); try{ e.preventDefault(); }catch(_){ } e.stopPropagation(); repeint(G.dp); } }
  function fin(e){ if(!G) return; var t=e.touches||[];
    if(G.mode==='pince' && t.length===1){ var c=cadre(G.p); G.mode='glisse'; G.x0=t[0].clientX; G.y0=t[0].clientY; G.dx0=c.dx; G.dy0=c.dy; window._cadreT=performance.now(); return; }   /* un doigt reste : il continue de déplacer */
    if(t.length) return;
    var actif=(G.mode==='pince' || G.mode==='glisse'); if(actif){ window._cadreT=performance.now(); sauve(); try{ e.stopPropagation(); }catch(_){ } } G=null; }
  document.addEventListener('touchstart', debut, {capture:true, passive:false});
  document.addEventListener('touchmove', bouge, {capture:true, passive:false});
  document.addEventListener('touchend', fin, {capture:true, passive:false});
  document.addEventListener('touchcancel', function(){ if(G && G.mode!=='attente'){ window._cadreT=performance.now(); sauve(); } G=null; }, {capture:true});
  /* pendant qu'on cadre, les événements de pointeur du même geste ne vont à personne d'autre */
  ['pointermove','pointerup','pointercancel','click'].forEach(function(n){ document.addEventListener(n, function(e){
    if((G && (G.mode==='pince' || G.mode==='glisse')) || (n!=='pointermove' && window._cadreT && performance.now()-window._cadreT<350 && e.pointerType!=='mouse')){ e.stopImmediatePropagation(); if(n==='click') e.preventDefault(); } }, true); });
  window._photoCadre={etat:function(){ var dp=hote(), p=porteur(dp); return p ? {z:(p.photoCadre||{}).z||1, dx:(p.photoCadre||{}).dx||0, dy:(p.photoCadre||{}).dy||0, pose:!!(p.photoCadre && p.photoCadre.n===p.photo.length)} : null; },
    remet:function(){ var dp=hote(), p=porteur(dp); if(p){ delete p.photoCadre; repeint(dp); sauve(); } }, bornes:{ZMIN:ZMIN, ZMAX:ZMAX}};
})();
</script>
"""+S[a:]
io.open(f,'w',encoding='utf-8').write(S)
