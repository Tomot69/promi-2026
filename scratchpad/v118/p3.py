# v118 §3 — Q365 tranchée : avec « La dalle d'origine », la bande haute prend la COULEUR d'origine, sauf ton sur ton (ΔE < 15) → rampe de Q30
import io
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:70]); S=S.replace(old,new)
rep("""      if(e.aplat && !(p&&p.photo)){
        try{ if(window._ppRampe) src.__o={rampe:window._ppRampe(e.nat)}; }catch(_){}
      }""",
"""      if(e.aplat && !(p&&p.photo)){
        /* ⚑ v118 (Tom, Q365 tranchée) : avec « La dalle d'origine », la bande haute prend la COULEUR d'origine — sauf si elle
           tombe sous le seuil du ton sur ton face au champ (ΔE 15, redteam_tonsurton) : alors seulement, la rampe de Q30. */
        var _ob=null; try{ _ob=window._origineBande ? window._origineBande(p, e.natCol) : null; }catch(_){ _ob=null; }
        if(!(_ob && _ob.origine)){ try{ if(window._ppRampe) src.__o={rampe:window._ppRampe(e.nat)}; }catch(_){} }
        try{ cv.setAttribute('data-origine', _ob ? ((_ob.origine?'origine':'rampe')+'|'+_ob.dE.toFixed(1)) : ''); }catch(_){}
      }""")
rep("""   · la bande haute d'une fiche garde la rampe de Q30 (sa couleur dit la nature) — voir QUESTIONS Q365 ;""",
    """   · ⚑ v118 (Q365 tranchée) : la bande haute d'une fiche prend la couleur d'origine, sauf ton sur ton (lot-V118-ORIGINE) ;""")
rep("""  /* le menu ne survit pas à la fiche (§8, « rien ne survit à closeAll ») */
  (window._rangeurs=window._rangeurs||[]).push(ferme);
})();
</script>""",
"""  /* le menu ne survit pas à la fiche (§8, « rien ne survit à closeAll ») */
  (window._rangeurs=window._rangeurs||[]).push(ferme);
})();
</script>
<script id="lot-V118-ORIGINE">
/* ⚑ v118 (Tom, Q365 tranchée) — « Avec La dalle d'origine, la bande haute de la fiche prend la couleur d'origine, sauf si elle
   passe sous le seuil de redteam_tonsurton face au champ. Dans ce cas seulement, la rampe de Q30 s'applique. »
   Le seuil est celui du juge : ΔE 15 (CIELAB), entre le Lab MOYEN de la dalle rendue dans son monde de plantation — DÉCLARÉ par
   le moteur (`__dalleInfo.lab`, jamais relu en pixels : redteam_decoupe) — et la couleur du champ (la nature). */
(function(){
  var SEUIL=15, MEMO={};
  window._seuilOrigine=SEUIL;
  function lin(c){ c/=255; return c<=0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); }
  function f(t){ return t>0.008856 ? Math.pow(t,1/3) : 7.787*t+16/116; }
  function lab(r,g,b){ r=lin(r); g=lin(g); b=lin(b);
    var x=(0.4124564*r+0.3575761*g+0.1804375*b)/0.95047, y=0.2126729*r+0.7151522*g+0.0721750*b, z=(0.0193339*r+0.1191920*g+0.9503041*b)/1.08883;
    return [116*f(y)-16, 500*(f(x)-f(y)), 200*(f(y)-f(z))]; }
  function rgb(s){ s=''+s; var m=/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(s.trim());
    if(m) return [parseInt(m[1],16),parseInt(m[2],16),parseInt(m[3],16)];
    m=/(\\d+)[, ]+(\\d+)[, ]+(\\d+)/.exec(s); return m ? [+m[1],+m[2],+m[3]] : null; }
  /* null : l'option n'est pas prise (ou rien à mesurer) ; sinon {dE, origine} */
  window._origineBande=function(p, natCol){
    try{ if(!(p && p.dalleOrigine && p.monde && p.monde.m && window.Toile && window.Toile.dalleTrame)) return null;
      var c=rgb(natCol); if(!c) return null;
      var k=p.id+'|'+p.monde.m+'|'+p.monde.p+'|'+p.monde.h+'|'+(p.dalle?p.dalle.ci+','+p.dalle.lit:'')+'|'+c.join(',');
      if(MEMO[k]) return MEMO[k];
      var cv=document.createElement('canvas');
      if(!window.Toile.dalleTrame(cv, p.id, 1, p.monde, {donnees:true}) || !cv.__dalleInfo || !cv.__dalleInfo.lab) return null;
      var L=cv.__dalleInfo.lab, F=lab(c[0],c[1],c[2]);
      var d=Math.sqrt((L[0]-F[0])*(L[0]-F[0])+(L[1]-F[1])*(L[1]-F[1])+(L[2]-F[2])*(L[2]-F[2]));
      return (MEMO[k]={dE:d, origine:d>=SEUIL});
    }catch(_){ return null; }
  };
})();
</script>""")
io.open('app.html','w',encoding='utf-8').write(S); print('ok')
