# L'ÉCRAN QUI VEND, SUR LE BAS DE LA PLANCHE (Tom, 11 sept., Q205). Patch sur app.html, motifs uniques.
#   · « Prendre l'année » perd son prix (il est écrit en grand au-dessus) — le libellé de la planche ;
#   · le bloc `lot-CERCLE-VEND-css` (le mien, de ce soir) est RÉÉCRIT pour le nouvel écran : un seul propriétaire ;
#   · un script `lot-CERCLE-VEND` pose le cadre, les trois vraies dalles, « 29 € », et y range les deux boutons et les deux notes.
import hashlib, io, os, re
RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(RACINE, 'app.html')
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == 'a543d1e196b42378d16a462cdcabd769', 'app.html a changé : ' + avant

def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:90]
    S = S.replace(old, new)

# 1 · le libellé du bouton de l'année — celui de la planche (« 29 € » est écrit en grand juste au-dessus)
remplace("""<button class="pl-buy sec" id="buyYear">Prendre l'année — 29&nbsp;€ <span>soit 2,42&nbsp;€/mois · −39&nbsp;%</span></button>""",
         """<button class="pl-buy sec" id="buyYear">Prendre l'année</button>""")

# 2 · le bloc CSS de ce soir, réécrit pour le nouvel écran
DEB = '<style id="lot-CERCLE-VEND-css">'
assert S.count(DEB) == 1
i = S.index(DEB); j = S.index('</style>', i) + len('</style>')
CSS = DEB + """
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — LE BAS DE LA PLANCHE (Tom, 11 sept. 2026, Q205) : « Oui, prends le bas de la planche. Trois mondes
   en vraies dalles, « 29 € » en grand, « Prendre l'année » en premier. C'est l'écran qui porte le revenu : il doit montrer
   ce qu'on achète, pas l'expliquer en cinq lignes. » — et deux choses à tenir : « les vraies dalles, rendues par le moteur,
   dans les trois mondes payants — Sillons, Gravure, Terrazzo. Pas un visuel » ; « l'essai de 14 jours reste visible, sous
   « Prendre l'année ». »
   Les COTES sont celles du bas de la planche (PLANCHE-CERCLE-2/-AB, `ecran_qui_vend`), ses écarts gardés au pixel ; le bloc
   remonte sous le plateau à 132 — la cote où la planche posait son premier bloc (plateau 40 + 60 + 32). Écran 390 × 844 :
   `#plusScreen` vit hors de `#device`, décalé de 16 (CLAUDE §8) — tout se range dans UN CADRE posé sur l'appareil.
   Ce bloc remplace celui de la version corrigée (encre des boutons, marge 24, contour) : un seul propriétaire.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
/* 1 · CE QUI NE SE MONTRE PLUS, NOMMÉMENT : le visuel, le titre, la phrase, les cinq lignes, et le conteneur des boutons
   (vidé : les boutons sont rangés dans le cadre). Pas `.pl-eb` : c'est le titre du plateau (lot du plateau, § 3). */
#plusScreen>#plHeroCv,#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat,#plusScreen>.pl-plans{display:none!important}
/* 2 · le cadre, et ses cotes (écran 390) */
#plusScreen #plCadre{position:absolute!important;width:390px!important;height:844px!important;margin:0!important;
  pointer-events:none;z-index:2}
#plusScreen #plCadre>*{position:absolute!important;margin:0!important;box-sizing:border-box!important}
#plusScreen #plCadre .plv-dal{top:132px!important;width:98px!important;height:98px!important;opacity:1!important;filter:none!important;
  mix-blend-mode:normal!important}
#plusScreen #plCadre .plv-nom{top:238px!important;width:98px!important;text-align:center;font-family:Bricolage,system-ui,sans-serif;
  font-weight:600;font-size:13px;letter-spacing:-.01em;line-height:1.3}
#plusScreen #plCadre .plv-prix{left:24px!important;top:276px!important;width:342px!important;text-align:center;
  font-family:Bricolage,system-ui,sans-serif;font-weight:700;font-size:56px;letter-spacing:-.03em;line-height:1}
#plusScreen #plCadre .plv-sous{left:24px!important;top:342px!important;width:342px!important;text-align:center;
  font-family:ApfelMid,system-ui,sans-serif;font-weight:500;font-size:15px;line-height:1.15}
#plusScreen #plCadre #buyYear,#plusScreen #plCadre #buyMonth{left:24px!important;width:342px!important;max-width:342px!important;
  height:62px!important;min-height:62px!important;border-radius:31px!important;border-width:2px!important;border-style:solid!important;
  display:flex!important;align-items:center!important;justify-content:center!important;padding:0 16px!important;
  font-family:Bricolage,system-ui,sans-serif!important;font-weight:700!important;letter-spacing:-.01em!important;
  box-shadow:none!important;pointer-events:auto!important}
#plusScreen #plCadre #buyYear{top:386px!important;font-size:19px!important}
#plusScreen #plCadre #buyMonth{top:464px!important;font-size:17px!important}
#plusScreen #plCadre .pl-note{left:24px!important;width:342px!important;text-align:center!important;font-family:Apfel,system-ui,sans-serif!important;
  font-weight:400!important;font-size:14px!important;line-height:1.3!important;opacity:1!important}
#plusScreen #plCadre .pl-note.plv-n1{top:548px!important}
#plusScreen #plCadre .pl-note.plv-n2{top:574px!important}
/* 3 · les encres — celles de la planche (T), deux thèmes ; `-webkit-text-fill-color` = `color` (§3) ; aucune opacité sur un
   texte (la seconde note était à .70, sous le plancher de 72 % du §6 : elle prend une teinte pleine). */
.frame:not(.light) #plusScreen #plCadre .plv-prix,.frame:not(.light) #plusScreen #plCadre .plv-sous,
#device:not(.light) #plusScreen #plCadre .plv-prix,#device:not(.light) #plusScreen #plCadre .plv-sous{color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important}
.frame:not(.light) #plusScreen #plCadre .plv-nom,#device:not(.light) #plusScreen #plCadre .plv-nom{color:#C9C4B4!important;-webkit-text-fill-color:#C9C4B4!important}
.frame:not(.light) #plusScreen #plCadre .pl-note,#device:not(.light) #plusScreen #plCadre .pl-note{color:#A8A396!important;-webkit-text-fill-color:#A8A396!important}
.frame:not(.light) #plusScreen #plCadre #buyYear,#device:not(.light) #plusScreen #plCadre #buyYear{background:#F4EEE1!important;border-color:#F4EEE1!important;
  color:#12142A!important;-webkit-text-fill-color:#12142A!important}
.frame:not(.light) #plusScreen #plCadre #buyMonth,#device:not(.light) #plusScreen #plCadre #buyMonth{background:transparent!important;border-color:#F4EEE1!important;
  color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important}
.frame.light #plusScreen #plCadre .plv-prix,.frame.light #plusScreen #plCadre .plv-sous,
#device.light #plusScreen #plCadre .plv-prix,#device.light #plusScreen #plCadre .plv-sous{color:#16171B!important;-webkit-text-fill-color:#16171B!important}
.frame.light #plusScreen #plCadre .plv-nom,#device.light #plusScreen #plCadre .plv-nom{color:#4A463C!important;-webkit-text-fill-color:#4A463C!important}
.frame.light #plusScreen #plCadre .pl-note,#device.light #plusScreen #plCadre .pl-note{color:#6B6658!important;-webkit-text-fill-color:#6B6658!important}
.frame.light #plusScreen #plCadre #buyYear,#device.light #plusScreen #plCadre #buyYear{background:#16171B!important;border-color:#16171B!important;
  color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important}
.frame.light #plusScreen #plCadre #buyMonth,#device.light #plusScreen #plCadre #buyMonth{background:transparent!important;border-color:#16171B!important;
  color:#16171B!important;-webkit-text-fill-color:#16171B!important}
</style>
<script id="lot-CERCLE-VEND">
/* ⚑ L'ÉCRAN QUI VEND — le cadre, les trois VRAIES dalles, « 29 € » (Q205). Voir le bloc CSS juste au-dessus. */
(function(){
  var MONDES = [['sillons', 'Sillons'], ['gravure', 'Gravure'], ['terrazzo', 'Terrazzo']];
  function ps(){ return document.getElementById('plusScreen'); }
  function P(e, k, v){ if(!e) return; if(e.style.getPropertyValue(k) === v && e.style.getPropertyPriority(k) === 'important') return;
    e.style.setProperty(k, v, 'important'); }
  var CAD = null, CVS = [];
  /* bâti UNE fois : c'est le contenu propre de l'écran (pas un nœud posé par une ouverture — rien à ranger à closeAll). Les deux
     boutons y sont DÉPLACÉS, pas recopiés : leurs id, leurs achats et le chemin « par-dessus » du mur restent les leurs. */
  function bati(){
    var s = ps(); if(!s) return false;
    if(CAD && CAD.isConnected) return true;
    CAD = document.createElement('div'); CAD.id = 'plCadre'; CVS = [];
    MONDES.forEach(function(m, i){
      var c = document.createElement('canvas'); c.className = 'plv-dal'; c.setAttribute('data-monde', m[0]);
      c.style.setProperty('left', (24 + i * 122) + 'px', 'important'); CAD.appendChild(c); CVS.push(c);
      var n = document.createElement('div'); n.className = 'plv-nom'; n.textContent = m[1];
      n.style.setProperty('left', (24 + i * 122) + 'px', 'important'); CAD.appendChild(n);
    });
    var px = document.createElement('div'); px.className = 'plv-prix'; px.textContent = '29\\u00a0€'; CAD.appendChild(px);
    var so = document.createElement('div'); so.className = 'plv-sous'; so.textContent = 'soit 2,42\\u00a0€/mois · −39\\u00a0%'; CAD.appendChild(so);
    var y = document.getElementById('buyYear'), mo = document.getElementById('buyMonth');
    if(y) CAD.appendChild(y);                   /* « Prendre l'année » en premier (Tom) */
    if(mo) CAD.appendChild(mo);                 /* l'essai de 14 jours dessous, visible */
    [].slice.call(s.querySelectorAll(':scope > .pl-note')).forEach(function(n, k){ n.classList.add(k ? 'plv-n2' : 'plv-n1'); CAD.appendChild(n); });
    s.appendChild(CAD);
    return true;
  }
  /* le cadre sur l'APPAREIL — en cotes de DISPOSITION (offset*, insensibles à la transformation d'ouverture), comme le
     lot du plateau : l'écran vit sous `.frame`, décalé de 16 (CLAUDE §8). */
  function off(e, anc){ var x = 0, y = 0; while(e && e !== anc){ x += e.offsetLeft; y += e.offsetTop; e = e.offsetParent; } return [x, y]; }
  function pose(){
    var s = ps(), dv = document.getElementById('device'); if(!s || !dv || !bati()) return;
    var fr = s.closest('.frame') || document.body, a = off(dv, fr), b = off(s, fr);
    P(CAD, 'left', (a[0] - b[0]) + 'px'); P(CAD, 'top', (a[1] - b[1]) + 'px');
  }
  /* ⚑ LES VRAIES DALLES (CLAUDE §4) : Toile.dalleTrame(src, id, 1, monde), échelle 1, le monde passé en 4ᵉ argument — le monde
     courant, seul `m` changé (sillons, gravure, terrazzo), comme la planche. Les Promi : les TROIS DERNIERS plantés de
     l'utilisateur (déterministe, jamais un tirage) — sa propre matière, dans le monde qu'il achèterait. Une dalle se rend UNE
     fois par Promi et par monde (cache) ; elle se pose dans sa boîte sans être étirée (le rapport de la source est gardé). */
  var CACHE = {};
  function mondeDe(w){ var b = {}; try{ b = window.Toile.mondeCourant() || {}; }catch(_){ } return {m: w, p: b.p, h: b.h}; }
  function ids(){ try{ return promises.filter(function(q){ return !q.draft && !q.req; }).map(function(q){ return q.id; })
                                   .sort(function(a, b){ return b - a; }).slice(0, 3); }catch(_){ return []; } }
  function source(id, mo){
    var k = id + '|' + mo.m + '/' + mo.p + '/' + mo.h; if(CACHE[k]) return CACHE[k];
    var c = document.createElement('canvas'), ok = false;
    try{ ok = window.Toile.dalleTrame(c, id, 1, mo); }catch(_){ }
    if(!ok || !c.width) return null;
    return (CACHE[k] = c);
  }
  function peint(){
    if(!bati()) return;
    var I = ids(), comp = [], dpr = Math.min(2, window.devicePixelRatio || 1);
    CVS.forEach(function(cv, i){
      var w = cv.getAttribute('data-monde'), W = Math.round(98 * dpr);
      if(cv.width !== W){ cv.width = W; cv.height = W; }
      var g = cv.getContext('2d'); if(!g) return; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, W);
      var id = I.length ? I[i % I.length] : null, mo = mondeDe(w), src = id != null ? source(id, mo) : null, dw = 0, dh = 0;
      if(src){ var r = Math.min(W / src.width, W / src.height); dw = src.width * r; dh = src.height * r;
        g.drawImage(src, (W - dw) / 2, (W - dh) / 2, dw, dh); }
      comp.push({monde: w, id: id, ok: !!src, source: src ? [src.width, src.height] : null,
                 pose: src ? [Math.round(dw / dpr * 10) / 10, Math.round(dh / dpr * 10) / 10] : null});
    });
    /* l'app PUBLIE ce qu'elle vient de composer (CLAUDE §7 : on compare la composition, pas la respiration du monde) */
    window._vendDalles = comp;
  }
  window._vendPeint = function(){ pose(); peint(); };
  /* à chaque ouverture (la classe `.show` que le code pose — jamais une géométrie, §8) ; peint après insertion, à 0, 60, 200
     et 600 ms (§4, règle 5) ; l'observateur ne regarde que la CLASSE et compare avant d'agir. */
  var ouvert = false;
  function veille(){
    var s = ps(); if(!s) return;
    new MutationObserver(function(){
      var o = s.classList.contains('show'); if(o === ouvert) return; ouvert = o; if(!o) return;
      try{ s.scrollTop = 0; }catch(_){ }
      [0, 60, 200, 600].forEach(function(d){ setTimeout(function(){ try{ pose(); peint(); }catch(_){ } }, d); });
    }).observe(s, {attributes: true, attributeFilter: ['class']});
  }
  try{ bati(); veille(); }catch(_){ }
})();
</script>"""
S = S[:i] + CSS + S[j:]
io.open(F, 'w', encoding='utf-8').write(S)
print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
