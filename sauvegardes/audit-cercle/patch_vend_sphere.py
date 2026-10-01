# L'ÉCRAN QUI VEND, COMPOSITION SIMPLE (Tom, 12 sept.) : une sphère framboise en en-tête · le prix, « Prendre l'année »,
# l'essai · trois lignes qui NOMMENT. Un seul objet visuel. Les trois dalles disparaissent (elles deviennent une ligne).
# Appliqué sur la COPIE — app.html n'est pas touchée tant que Tom n'a pas vu.
import hashlib, io, os, sys
RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(RACINE, 'scratchpad', 'app-vend-sphere.html')
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '3ac4975ccaed06419950963a8804a212', 'la copie a changé : ' + avant
def remplace(old, new, quoi):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple (%s) : %r' % (quoi, old[:70])
    S = S.replace(old, new); print('  ✔', quoi)

# ── 1 · LA VITESSE — décision Tom du 12 sept. : un tour en 100 s, sur LES DEUX sphères.
remplace("var G = { AUTO:6.283185307/120,",
 "var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept. 2026) : « accélère-la encore un peu des deux côtés ».\n"
 "   Bornes de l'historique : 84 s jugé TROP VIF (5 sept.), 120 s TOUJOURS TROP LENT (12 sept.) — 100 s est entre les deux, +20 %.\n"
 "   L'écran qui vend porte la MÊME valeur : c'est une décision, pas un réglage. Juge : releve-aura.py, AUTO_DECIDE en dur. */",
 'G.AUTO : un tour en 100 s')

# ── 2 · LA PORTE PUBLIQUE — le lot de l'Aura reste le SEUL propriétaire de ses constantes ; il PEINT pour l'appelant.
remplace("    sansIles:function(b){ ORB.sansIles=!!b; var S=semis(); S.__stCle=null; },",
"""    sansIles:function(b){ ORB.sansIles=!!b; var S=semis(); S.__stCle=null; },
    /* ⚑ UNE SECONDE SPHÈRE, AILLEURS (Tom, 12 sept.) — l'écran qui vend en porte une, plus petite, framboise, à la MÊME
       vitesse. FROISSE, ENV, KN, PXR, MAG, le semis et l'atlas restent PRIVÉS : le lot ne les publie pas, il peint pour
       l'appelant. `sur` surcharge ce que l'appelant décide (css, R, sol, lac, tan, trame, fond). */
    peintSur:function(cv, sur){
      if(!cv) return false;
      var o; try{ atlas(); semis(); o=opts(); }catch(e){ return false; }
      if(sur) for(var k in sur){ if(Object.prototype.hasOwnProperty.call(sur,k)) o[k]=sur[k]; }
      if(!o.trame) return false;
      try{ M.peint(cv, o); }catch(e){ return false; }
      return true;
    },
    /* les îles de CETTE sphère : de VRAIES dalles du moteur (§4 règle 1), en nombre, dans les mondes demandés —
       `dalleGeneree` n'existe pas dans l'app, le rappel `dalle` est donc obligatoire (voir batIles). */
    faitIles:function(n, mondes){
      try{
        var P = window.promises.filter(function(q){ return !q.draft && !q.req; }).map(function(q){ return q.id; }).sort(function(a,b){ return b-a; });
        if(!P.length) return null;
        var base = {}; try{ base = window.Toile.mondeCourant() || {}; }catch(e){}
        return M.batIles(n, window.Toile.cols(), {pxr:PXR, mag:MAG, palette:window.Toile.getPalette(),
          dalle:function(k, I, g){
            var w = mondes[k % mondes.length], mo = {m:w, p:base.p, h:base.h};
            var s = dalleDe({id:P[k % P.length], monde:mo}); if(!s) return null;
            var cote = Math.max(s.width, s.height);
            return {cv:s, sx:s.width/2, sy:s.height/2, kk:cote/(g/(PXR/MAG)), monde:w};
          }});
      }catch(e){ return null; }
    },""", 'porte publique _aura.peintSur + _aura.faitIles')

# ── 3 · LE LOT — en fin de fichier (règle du projet : un bloc neuf se pose à la FIN).
BLOC = r"""
<style id="lot-VEND-SPHERE-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — COMPOSITION SIMPLE (Tom, 12 sept. 2026) : « une sphère, pleine et belle, qui tourne… puis le prix…
   puis une liste sobre et courte de ce que le Cercle ouvre. Une ligne par chose, sans aperçu, sans vignette, sans matière. »
   UN SEUL OBJET VISUEL : la sphère porte la matière, le reste NOMME. Les trois dalles de la version d'hier disparaissent —
   elles deviennent la troisième ligne (renversement assumé de la consigne du 11, confirmé par Tom le 12).
   Tout tient AU-DESSUS DU PLI : la dernière ligne finit à 830, l'écran se lit sans défiler.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#plusScreen #plCadre .plv-dal,#plusScreen #plCadre .plv-nom{display:none!important}
#plusScreen #plCadre .plv-sph{position:absolute!important;left:79px!important;top:104px!important;width:232px!important;height:232px!important;
  opacity:1!important;filter:none!important;mix-blend-mode:normal!important;pointer-events:none!important}
#plusScreen #plCadre .plv-prix,#plusScreen #plCadre.plv-sans .plv-prix{top:366px!important}
#plusScreen #plCadre .plv-sous,#plusScreen #plCadre.plv-sans .plv-sous{top:432px!important}
#plusScreen #plCadre #buyYear,#plusScreen #plCadre.plv-sans #buyYear{top:470px!important}
#plusScreen #plCadre #buyMonth,#plusScreen #plCadre.plv-sans #buyMonth{top:548px!important}
#plusScreen #plCadre .pl-note.plv-n1,#plusScreen #plCadre.plv-sans .pl-note.plv-n1{top:632px!important}
#plusScreen #plCadre .pl-note.plv-n2,#plusScreen #plCadre.plv-sans .pl-note.plv-n2{top:658px!important}
/* les trois lignes — elles NOMMENT, elles n'expliquent pas */
#plusScreen #plCadre .plv-li{position:absolute!important;left:24px!important;width:342px!important}
#plusScreen #plCadre .plv-li b{display:block;font-family:Bricolage,system-ui,sans-serif;font-weight:600;font-size:15px;
  letter-spacing:-.01em;line-height:1.2}
#plusScreen #plCadre .plv-li i{display:block;font-style:normal;font-family:ApfelMid,system-ui,sans-serif;font-weight:500;
  font-size:13px;line-height:1.25;margin-top:3px}
.frame:not(.light) #plusScreen #plCadre .plv-li b,#device:not(.light) #plusScreen #plCadre .plv-li b{color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important}
.frame:not(.light) #plusScreen #plCadre .plv-li i,#device:not(.light) #plusScreen #plCadre .plv-li i{color:#A8A396!important;-webkit-text-fill-color:#A8A396!important}
.frame.light #plusScreen #plCadre .plv-li b,#device.light #plusScreen #plCadre .plv-li b{color:#16171B!important;-webkit-text-fill-color:#16171B!important}
.frame.light #plusScreen #plCadre .plv-li i,#device.light #plusScreen #plCadre .plv-li i{color:#6B6658!important;-webkit-text-fill-color:#6B6658!important}
</style>
<script id="lot-VEND-SPHERE">
/* ⚑ LA SPHÈRE DE L'ÉCRAN QUI VEND — voir le bloc CSS juste au-dessus. */
(function(){
  var MONDES = ['sillons', 'gravure', 'terrazzo'];   /* les trois mondes payants — c'est ce qu'on achète, montré sans être listé */
  var N_ILES = 14;                                   /* « richement remplie » : plus que la Toile d'aujourd'hui */
  var CSS = 232, R = 0.392, TAN = 0.32;              /* 232 contre 296 sur l'Aura — plus petite, même rapport de rayon */
  var SOL = [250, 34, 88];                           /* framboise = NAT.chiche. PAS terracotta : c'est la couleur de l'état « à tenir » */
  var LIGNES = [['La parole qu’on te tient', 'ce que je tiens · ce qu’on me tient'],
                ['Chaque parole se règle', 'récurrence, rappel, importance, mémoire'],
                ['Trois mondes de plus', 'Sillons, Gravure, Terrazzo']];
  var TOPS = [698, 746, 794];
  var CV = null, ILES = null, lac = 3.04, t0 = 0, raf = 0, ms = [];
  function cad(){ return document.getElementById('plCadre'); }
  function ps(){ return document.getElementById('plusScreen'); }
  function bati(){
    var C = cad(); if(!C) return false;
    if(CV && CV.isConnected) return true;
    CV = document.createElement('canvas'); CV.className = 'plv-sph'; C.appendChild(CV);
    LIGNES.forEach(function(L, i){
      var d = document.createElement('div'); d.className = 'plv-li';
      d.style.setProperty('top', TOPS[i] + 'px', 'important');
      var b = document.createElement('b'); b.textContent = L[0];
      var s = document.createElement('i'); s.textContent = L[1];
      d.appendChild(b); d.appendChild(s); C.appendChild(d);
    });
    return true;
  }
  /* le semis (110 000 points) se bâtit UNE fois, à l'ouverture, AVANT la première image — jamais sous les yeux (Q181) */
  function prepare(){
    if(ILES) return true;
    if(!window._aura || !window._aura.faitIles) return false;
    ILES = window._aura.faitIles(N_ILES, MONDES);
    return !!ILES;
  }
  function image(t){
    raf = 0;
    var s = ps(); if(!s || !s.classList.contains('show')) return;   /* un écran est visible s'il porte `.show` (§8) — jamais offsetParent */
    var dt = t0 ? Math.min(0.1, (t - t0) / 1000) : 0; t0 = t;        /* le TEMPS RÉEL, jamais « une image = 16 ms » (§8) */
    var A = 6.283185307 / 100;                                       /* un tour en 100 s — la même valeur que l'Aura (décision Tom) */
    try{ A = window._aura.G.AUTO; }catch(e){}
    lac += A * dt;
    var d0 = performance.now();
    window._aura.peintSur(CV, {css: CSS, R: R, sol: SOL, lac: lac, tan: TAN, trame: ILES, fond: 'rgba(0,0,0,0)'});
    ms.push(performance.now() - d0); if(ms.length > 60) ms.shift();
    window._vendSphere = {iles: N_ILES, mondes: MONDES, sol: SOL, css: CSS, lac: lac, auto: A,
                          ms: ms.slice().sort(function(a, b){ return a - b; })[ms.length >> 1]};
    raf = requestAnimationFrame(image);
  }
  function demarre(){
    if(!bati() || !prepare()) return;
    t0 = 0; if(!raf) raf = requestAnimationFrame(image);
  }
  function arrete(){ if(raf){ cancelAnimationFrame(raf); raf = 0; } }
  window._vendSphereGo = demarre;
  var ouvert = false;
  function veille(){
    var s = ps(); if(!s) return;
    new MutationObserver(function(){
      var o = s.classList.contains('show'); if(o === ouvert) return; ouvert = o;   /* on compare avant d'agir (§8) */
      if(o){ try{ bati(); }catch(_){ } setTimeout(demarre, 0); } else arrete();
    }).observe(s, {attributes: true, attributeFilter: ['class']});
  }
  try{ bati(); veille(); }catch(_){ }
})();
</script>
"""
assert S.count('</body>') == 1, 'pas un seul </body>'
S = S.replace('</body>', BLOC + '</body>'); print('  ✔ lot-VEND-SPHERE posé en fin de fichier')
io.open(F, 'w', encoding='utf-8').write(S)
print('copie', avant, '→', hashlib.md5(S.encode('utf-8')).hexdigest())
