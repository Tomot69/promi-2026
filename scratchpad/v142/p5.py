import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif absent ou multiple', S.count(old), old[:70]); S=S.replace(old,new)
rep("""      var hFil=Math.round(fil.getBoundingClientRect().height/sc2);
      var mn=document.getElementById('dpMain');
      if(mn) mn.style.setProperty('min-height', Math.max(760, yFil+hFil+30)+'px', 'important');""",
"""      fil.style.setProperty('min-height', Math.max(0, 748-yFil)+'px', 'important');   /* v142 (C-096) : un fil court descend jusqu'à 12 pt du bandeau (760) — son bouton, dernière ligne, s'y pose */
      var hFil=Math.round(fil.getBoundingClientRect().height/sc2);
      var mn=document.getElementById('dpMain');
      if(mn) mn.style.setProperty('min-height', Math.max(760, yFil+hFil+12)+'px', 'important');""")
rep("""      var mn=document.getElementById('dpMain');
      if(mn){ var h=Math.round(fil.getBoundingClientRect().height/sc);
        mn.style.setProperty('min-height', Math.max(760, y+h+30)+'px','important'); }""",
"""      fil.style.setProperty('min-height', Math.max(0, 748-y)+'px', 'important');   /* v142 (C-096) : voir `_ficheNuee` */
      var mn=document.getElementById('dpMain');
      if(mn){ var h=Math.round(fil.getBoundingClientRect().height/sc);
        mn.style.setProperty('min-height', Math.max(760, y+h+12)+'px','important'); }""")
rep("""<style id="lot-V141-MUR-LU-css">""",
"""<style id="lot-V142-CERCLE-css">
/* ⚑ v142 (Tom, 11 oct. 2026, C-096 — RÉCIDIVE) — LA FICHE D'UN CERCLE, COMME TOM LA VOIT.
   POURQUOI C'EST REVENU : le bandeau Peaufiner et le bouton « + Planter dans le Cercle » sont COLLANTS (`position:sticky`). Quand l'appareil
   est réduit à l'écran (Safari sur l'iPhone : ≈ 0,82 ; une fenêtre de 390 × 844 : 0,93), WebKit borne un élément collant au bas de la zone
   VISIBLE comptée en points d'écran, pas en points de l'appareil : le bandeau se collait à 703 au lieu de 760 (57 pt = 844 × 0,067), le fil
   passait dessous ET se voyait sous lui. Les juges ouvraient la fiche à l'échelle 1 (430 × 932), sur le Cercle du jeu de démonstration (neuf
   paroles). `--colle` porte l'écart MESURÉ sur le bandeau lui-même (lot-V142-CERCLE) ; il vaut 0 là où le navigateur compte juste.
   Et un fil COURT (une parole) : son bouton restait sous sa dernière carte, loin du bandeau — il descend à 12 pt au-dessus (le fil a pour
   hauteur minimale ce qui le sépare du bandeau, posée par ses deux poseurs). */
#detailPoster.dp-nuee:not(.s2-ouv) > #dpDetails, #detailPoster.dp-mode-nuee:not(.s2-ouv) > #dpDetails{bottom:calc(0px - var(--colle,0px))!important}
#detailPoster.dp-nuee:not(.s2-ouv) #dpNueeFil .nf-tete, #detailPoster.dp-mode-nuee:not(.s2-ouv) #dpNueeFil .nf-tete{bottom:calc(96px - var(--colle,0px))!important}
#device#device #detailPoster.dp-nuee:not(.s2-ouv) #dpNueeFil .nf-tete, #device#device #detailPoster.dp-mode-nuee:not(.s2-ouv) #dpNueeFil .nf-tete{margin-top:auto!important}
</style>
<script id="lot-V142-CERCLE">
(function(){
  var essais=0;
  function mesure(){ try{
    var P=document.getElementById('detailPoster'), dev=document.getElementById('device'); if(!P||!dev||!P.classList.contains('show')) return;
    if(!(P.classList.contains('dp-nuee')||P.classList.contains('dp-mode-nuee'))||P.classList.contains('s2-ouv')) return;
    var D=document.getElementById('dpDetails'), M=document.getElementById('dpMain'); if(!D||!M||M.offsetHeight<759.5) return;   /* le bandeau n'est collé que si la colonne le pousse au bas de l'écran */
    var e=dev.getBoundingClientRect().width/390; if(!(e>0)) return;
    var err=(P.getBoundingClientRect().bottom-D.getBoundingClientRect().bottom)/e;
    if(Math.abs(err)<0.5) { essais=0; return; }
    if(++essais>6) return;   /* on compare avant d'agir, et l'on renonce plutôt que de tourner */
    var cur=parseFloat(dev.style.getPropertyValue('--colle'))||0, v=Math.max(0, Math.min(400, cur+err));
    dev.style.setProperty('--colle', v.toFixed(2)+'px'); requestAnimationFrame(mesure);
  }catch(_){ } }
  function demande(){ essais=0; requestAnimationFrame(function(){ requestAnimationFrame(mesure); }); setTimeout(mesure,350); setTimeout(mesure,1200); }
  var f0=window._ficheNuee; if(typeof f0==='function'){ window._ficheNuee=function(){ var r=f0.apply(this,arguments); try{ demande(); }catch(_){ } return r; }; }
  window.addEventListener('resize', function(){ try{ var dev=document.getElementById('device'); if(dev) dev.style.removeProperty('--colle'); demande(); }catch(_){ } });
  window._colleMesure=mesure;
})();
</script>
<style id="lot-V141-MUR-LU-css">""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
