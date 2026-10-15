# -*- coding: utf-8 -*-
import io
P = 'app.html'; S = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global S
    assert S.count(old) == n, (S.count(old), old[:110])
    S = S.replace(old, new)
DEV = "(document.getElementById('device')&&document.getElementById('device').classList.contains('light'))"
FC = "(window._ficheClair?window._ficheClair():false)"
# 0 · la porte : la fiche et la page + ne lisent plus le thème de l'app
rep("""<style id="lot-TOKENS-css">""",
"""<script id="lot-V146-THEME">
/* ⚑ v146 (Tom, 14 oct. 2026 — C-132) — LA FICHE ET LA PAGE + SONT EN VERSION SOMBRE DANS LES DEUX MODES. Le code qui les peint ne lit plus
   `#device.light` : il demande `_ficheClair()` (toujours faux) ; ce qui peint AUSSI ailleurs (une passe commune, un anneau, la main) demande
   `_clairPour(element)` — faux dans la fiche, la page + et tout ce qui porte `.th-sombre`, le thème de l'app partout ailleurs.
   `_enSombre(f)` rend une dalle du moteur comme en sombre, le temps de l'appel (le moteur lit `_shThemeOverride`). */
window._ficheClair=function(){ return false; };
window._clairPour=function(el){ try{ if(el && el.closest && el.closest('#detailPoster,#createSheet,.th-sombre')) return false; }catch(_){}
  var d=document.getElementById('device'); return !!(d && d.classList.contains('light')); };
window._enSombre=function(f){ var av=window._shThemeOverride; window._shThemeOverride=false; try{ return f(); } finally { window._shThemeOverride=(av===undefined?null:av); } };
</script>
<style id="lot-TOKENS-css">""")
# 1 · lot-S1B-geo : le poseur de la fiche
rep("""    var light=!!(document.getElementById('device')||{classList:{contains:function(){return false;}}}).classList.contains('light');
    var n = dp.classList.contains('dp-chiche')?'chiche'""",
    """    var light=""" + FC + """;   /* v146 (C-132) : la fiche est la version sombre dans les deux modes */
    var n = dp.classList.contains('dp-chiche')?'chiche'""")
rep("""var _clairT=!!""" + DEV + """; if(!_clairT) encre = CREME;""", """var _clairT=""" + FC + """; if(!_clairT) encre = CREME;""")
rep("""var _colQui = dp.classList.contains('f-tenue') ? (""" + DEV + """ ? '#201908' : CREME) : e.colTexte;""",
    """var _colQui = dp.classList.contains('f-tenue') ? (""" + FC + """ ? '#201908' : CREME) : e.colTexte;""")
rep("""var _colQd = (p && p.status==='tenu') ? (""" + DEV + """ ? '#00341A' : '#8FE08F') : e.colTexte;""",
    """var _colQd = (p && p.status==='tenu') ? (""" + FC + """ ? '#00341A' : '#8FE08F') : e.colTexte;""")
rep("""    var light=document.getElementById('device').classList.contains('light');
    var natCol=NATCOL.nuee, col=NATTRAIT.nuee, colTexte= light?window._NATTXT.nuee:NATCLAIR.nuee;""",
    """    var light=""" + FC + """;   /* v146 (C-132) */
    var natCol=NATCOL.nuee, col=NATTRAIT.nuee, colTexte= light?window._NATTXT.nuee:NATCLAIR.nuee;""")
# 2 · le filet du trait (script des cotes de la fiche et de la page +)
rep("""      var _sombre = !document.getElementById('device').classList.contains('light') && !(window._sansFiletCercle && window._sansFiletCercle(cv));""",
    """      var _sombre = !(window._clairPour?window._clairPour(cv):document.getElementById('device').classList.contains('light')) && !(window._sansFiletCercle && window._sansFiletCercle(cv));""")
# 3 · lot-S5 : l'instant et la fiche tenue
rep("""    var _clair=!!""" + DEV + """;
    var TXT=_clair?'#00341A':MENTHE;""", """    var _clair=""" + FC + """;   /* v146 (C-132) */
    var TXT=_clair?'#00341A':MENTHE;""")
rep("""return !!(dp && dp.classList.contains('f-tenue') && !(dv && dv.classList.contains('light'))); }catch(_){ return false; } }   /* v136 : la terre n'existe plus qu'en sombre */""",
    """return !!(dp && dp.classList.contains('f-tenue') && !""" + FC + """); }catch(_){ return false; } }   /* v136 : la terre n'existe plus qu'en sombre · v146 (C-132) : la fiche est sombre dans les deux modes — la terre revient partout */""")
rep("""    var dev=document.getElementById('device');
    var clair=!!(dev&&dev.classList.contains('light'));
    var encreCorps = (clair && !(nom!=='arrive' && _surTerre())) ? ENCRE : CREME;""",
    """    var dev=document.getElementById('device');
    var clair=""" + FC + """;   /* v146 (C-132) */
    var encreCorps = (clair && !(nom!=='arrive' && _surTerre())) ? ENCRE : CREME;""")
# 4 · lot-PHOTO : le bouton photo
rep("""      if(dev && dev.classList.contains('light') && !aPhoto)
        b.style.setProperty('color', '#201908', 'important'); }catch(_){}""",
    """      if(dev && (window._clairPour?window._clairPour(b):dev.classList.contains('light')) && !aPhoto)
        b.style.setProperty('color', '#201908', 'important'); }catch(_){}""")
# 5 · lot-NUEE-PEAUFINER
rep("""    var clair = document.getElementById('device').classList.contains('light');
    var encre = clair ? ENCRE : CREME;
    var lab   = clair ? MAUVE : CLAIRN;""", """    var clair = """ + FC + """;   /* v146 (C-132) */
    var encre = clair ? ENCRE : CREME;
    var lab   = clair ? MAUVE : CLAIRN;""")
rep("""      if(b.id === 'npDiss'){ var _cd = document.getElementById('device').classList.contains('light') ? 'var(--c-brun09)' : 'var(--c-creme95)';""",
    """      if(b.id === 'npDiss'){ var _cd = """ + FC + """ ? 'var(--c-brun09)' : 'var(--c-creme95)';""")
# 6 · lot-PLATEAU-PARTOUT : l'encre d'un plateau suit l'écran qui le porte
rep("""    var b = sc.querySelector('.enh'); if(!b) return;
    var clair = !!document.querySelector('#device.light,.device.light,.frame.light');
    var encre = clair ? '#201908' : '#F7F0DE';""",
    """    var b = sc.querySelector('.enh'); if(!b) return;
    var clair = window._clairPour ? window._clairPour(sc) : !!document.querySelector('#device.light,.device.light,.frame.light');   /* v146 (C-132) : le plateau d'une fiche est celui du sombre */
    var encre = clair ? '#201908' : '#F7F0DE';""")
# 7 · lot-PINCEAU : la rangée du pinceau vit sur la page + et dans Peaufiner
rep("""  function corpsEncre(){
    var clair = !!document.querySelector('#device.light,.device.light,.frame.light');""",
    """  function corpsEncre(){
    var clair = """ + FC + """;   /* v146 (C-132) : la page + et Peaufiner sont en version sombre */""")
# 8 · lot-V145-PARTS : la liste des noms, posée sur la fiche
rep("""var S=etat(p), clair=dv.classList.contains('light');""", """var S=etat(p), clair=""" + FC + """;""")
io.open(P, 'w', encoding='utf-8').write(S); print('ok')
