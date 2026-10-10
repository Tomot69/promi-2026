import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:80]); S=S.replace(o,n)
# ── 1 · l'onboarding : après le prénom, le principe (E2) ; au rejeu aussi
rep("""      prenom=v; try{ USER.name=v; LS.s('promi_prenom', v); if(typeof _refreshAvatars==='function') _refreshAvatars(); }catch(_){}
      allerParole(true);""",
"""      prenom=v; try{ USER.name=v; LS.s('promi_prenom', v); if(typeof _refreshAvatars==='function') _refreshAvatars(); }catch(_){}
      /* ⚑ E2 (v140, C-075) — après l'identification : l'étape qui dit le principe, puis la VRAIE page + (`lot-E2`). L'écran « parole et trait »
         de l'onboarding, sa plantation simulée et son message de fin ne sont plus joués (tableau garder / supprimer / remplacer : ENGAGEMENT-E2.md). */
      if(window._e2 && window._e2.principe){ etape='principe'; try{ var _bi=document.getElementById('onbIn'); if(_bi) _bi.blur(); }catch(_){} window._e2.principe(rejeu); }
      else allerParole(true);""")
rep("""    if(rejeu && nom){ prenom=nom; allerParole(false); }""",
"""    if(rejeu && nom && window._e2 && window._e2.principe){ prenom=nom; etape='principe'; window._e2.principe(true); }
    else if(rejeu && nom){ prenom=nom; allerParole(false); }""")
# ── 2 · les points du trait à tracer, plus gros, en grandissant vers le haut
rep("""      for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); } }
    /* ⚑ 23 SEPTEMBRE 2026 (Tom) — UN FILET CRÈME SOUS LE TRAIT D'UNE PAROLE TENUE.""",
"""      /* ⚑ E2 (v140, Tom, C-075) — « “TRACE POUR TENIR” et le trait plus visibles […] : plus grands, en grandissant vers le haut, sans déplacer
         ce qui est en dessous. » Les points de la moitié À TRACER passent de Ø 9 à Ø 12 quand la fiche attend un trait ; leur bas ne bouge
         pas (le centre monte de 1,5). Le plein, lui, garde l'épaisseur de son pinceau. */
      var rp=e.trace?(window._e2PointR||6):rr;
      for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x)-(rp-rr),rp,0,6.2832); g.fill(); } }
    /* ⚑ 23 SEPTEMBRE 2026 (Tom) — UN FILET CRÈME SOUS LE TRAIT D'UNE PAROLE TENUE.""")
rep("""        for(var x=cx+esp*1.3; x<W-rr; x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); }""",
"""        var rp=(window._e2PointR||6);   /* E2 (v140) : les points à tracer, Ø 12, grandis vers le haut — comme sur la fiche */
        for(var x=cx+esp*1.3; x<W-rr; x+=esp){ g.beginPath(); g.arc(x,y(x)-(rp-rr),rp,0,6.2832); g.fill(); }""")
# ── 3 · E2bis : « aura-apparait » est branché
rep("""   {id:'aura-apparait', ecran:'l’accueil', quand_dit:'l’Aura paraît dans la barre (au premier tenu)', geste:'la main désigne l’Aura', branche:false, raison:'appartient à E2bis (C-076) : l’identifiant est réservé, rien n’est branché'},""",
"""   {id:'aura-apparait', ecran:'l’accueil', quand_dit:'l’Aura vient de paraître dans la barre (au premier tenu), l’accueil est à l’écran', geste:'la main désigne l’Aura : un appui sur son entrée', branche:true, quand:function(){ try{ return (window._devoile && window._devoile.auraQuand) ? window._devoile.auraQuand() : null; }catch(_){ return null; } }},   /* E2bis (v140, C-076) */""")
io.open('app.html','w',encoding='utf-8').write(S)
