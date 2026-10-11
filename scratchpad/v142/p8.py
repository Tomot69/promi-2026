import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif absent ou multiple', S.count(old), old[:70]); S=S.replace(old,new)
rep("""      else { var _pb=st.querySelector('#stpBas'); if(_pb&&vu(_pb)) L.push(_pb); else ['#stpTons','#stpVue','#stpDots','#stpLab'].forEach(function(s){ var e=st.querySelector(s); if(e&&vu(e)) L.push(e); }); } }
    return L; }""",
"""      else { var _pb=st.querySelector('#stpBas'); if(_pb&&vu(_pb)) L.push(_pb); else ['#stpTons','#stpVue','#stpDots','#stpLab'].forEach(function(s){ var e=st.querySelector(s); if(e&&vu(e)) L.push(e); }); }
      /* ⚑ v142 (Tom, 11 oct. 2026, C-100 — RÉCIDIVE : « sur chaque zone floutée du Studio ») — CE QUI EMPÊCHAIT LE TOUCHER D'ARRIVER : rien ne
         l'attendait. Sur un monde de Ma Parole ! la plus grande zone floutée du Studio est LA TOILE elle-même (`#stBg`, floutée à 1,4 px, tout
         l'écran) ; seuls le panneau du bas et celui des palettes étaient des murs. Touchée, la Toile floutée ne répondait JAMAIS (vu dans le
         simulateur iPhone). Les juges ne touchaient que le panneau. Elle est un mur, la DERNIÈRE de la liste (le panneau passe d'abord). */
      var _tb=st.querySelector('#stBg'); if(_tb&&vu(_tb)){ var _fb=getComputedStyle(_tb).filter; if(_fb&&_fb.indexOf('blur')>=0) L.push(_tb); } }
    return L; }""")
rep("""  function dans(x,y){ var L=murs(); for(var i=0;i<L.length;i++){ var r=L[i].getBoundingClientRect(); if(x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom){""",
"""  function dans(x,y){ var L=murs(); for(var i=0;i<L.length;i++){ var r=L[i].getBoundingClientRect(); if(x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom){
      /* v142 : la Toile floutée du Studio couvre tout l'écran — le plateau, le bouton d'achat et les panneaux posés dessus ne sont pas elle */
      if(L[i].id==='stBg'){ var hb=document.elementFromPoint(x,y); if(!hb) continue; if(hb.closest && hb.closest('button,a,[role=button],#stLockBuy,#stLockCta,#stpBas,#stpPals,.closeb,.enh,.st-plat-h,#stpPlat')) continue;
        var dvb=document.getElementById('device').getBoundingClientRect(), kb=(dvb.width/390)||1, yb=(y-dvb.top)/kb; if(yb<104) continue;   /* le plateau (40 → 100) */
        if(hb===L[i] || L[i].contains(hb) || (hb.closest && hb.closest('#studioScreen'))) return L[i]; continue; }""")
rep("""    if(mur && mur.closest && mur.closest('#studioScreen')){ var _LS=murs().filter(function(e){ return e.closest && e.closest('#studioScreen'); });""",
"""    if(mur && mur.id==='stBg'){ /* v142 : la phrase sur la Toile floutée — entre le plateau (100) et ce qui est posé dessous (le bouton d'achat, sinon le panneau) */
      var _yb=844; ['#stLockBuy','#stpBas','#stpPals'].forEach(function(s){ var e=document.querySelector('#studioScreen '+s); if(e&&vu(e)){ var q=e.getBoundingClientRect(); if(q.height>8) _yb=Math.min(_yb,(q.top-D.top)/k); } });
      r={left:D.left, right:D.right, top:D.top+104*k, bottom:D.top+(_yb-8)*k}; }
    else if(mur && mur.closest && mur.closest('#studioScreen')){ var _LS=murs().filter(function(e){ return e.id!=='stBg' && e.closest && e.closest('#studioScreen'); });""")
rep("""      try{ if(mur && mur.id==='stpPals') mur.classList.add('mur-lu'); }catch(_){ }""",
"""      try{ if(mur && (mur.id==='stpPals'||mur.id==='stpBas'||mur.id==='stBg')) mur.classList.add('mur-lu'); }catch(_){ }   /* v142 : le panneau du bas et la Toile floutée aussi — la phrase y est seule (sur le panneau, le disque crème du thème la rendait illisible : vu dans le simulateur) */""")
rep("""  window.addEventListener('click', function(ev){ if(performance.now()<avaleJusque){ avaleJusque=0; ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  /* la phrase ne survit pas à l'écran qui l'a fait monter (CLAUDE §8) */""",
"""  window.addEventListener('click', function(ev){ if(performance.now()<avaleJusque){ avaleJusque=0; ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  /* ⚑ v142 (C-100) — LE TOUCHER LUI-MÊME, AUSSI : `touchstart` / `touchend`. Le mur n'écoutait que les évènements de pointeur ; là où un toucher
     n'en produit pas (WebKit piloté : 0 phrase sur 15 touchers) ou les annule (`pointercancel` quand le navigateur croit à un défilement),
     rien n'arrivait. Un toucher traité par une voie ne l'est pas par l'autre (`faitA`). */
  var t0=null, faitA=0;
  window.addEventListener('pointerup', function(){ faitA=performance.now(); }, true);
  window.addEventListener('touchstart', function(ev){ var t=ev.changedTouches&&ev.changedTouches[0]; t0=(t&&ev.touches&&ev.touches.length===1)?{x:t.clientX,y:t.clientY,t:performance.now(),id:t.identifier}:null; }, {capture:true, passive:true});
  window.addEventListener('touchend', function(ev){ var d=t0; t0=null; var t=ev.changedTouches&&ev.changedTouches[0]; if(!d||!t||t.identifier!==d.id) return;
    if(Math.hypot(t.clientX-d.x, t.clientY-d.y)>10 || performance.now()-d.t>600) return;
    var X=t.clientX, Y=t.clientY; setTimeout(function(){ if(performance.now()-faitA<120) return;   /* la voie du pointeur vient de le traiter */
      if(agit(X,Y,null)) avaleJusque=performance.now()+700; }, 30); }, {capture:true, passive:true});
  /* la phrase ne survit pas à l'écran qui l'a fait monter (CLAUDE §8) */""")
rep("""<style id="lot-V141-MUR-LU-css">""","""<style id="lot-V142-MUR-LU-css">
/* v142 (C-100) : pendant qu'on lit la phrase d'un mur du Studio, ce qui est sous elle se retire — le contenu du panneau du bas ; le nom du monde sur la Toile floutée */
#studioScreen #stpBas.mur-lu > *{visibility:hidden!important}
#studioScreen:has(#stBg.mur-lu) .stp-m, #studioScreen:has(#stBg.mur-lu) .stp-en, #studioScreen:has(#stBg.mur-lu) .stp-p{visibility:hidden!important}
</style>
<style id="lot-V141-MUR-LU-css">""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
