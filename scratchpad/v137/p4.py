import io,re
S=io.open('app.html',encoding='utf-8').read()
L=S.split('\n')
def idx(pred, start=0):
    for i in range(start,len(L)):
        if pred(L[i]): return i
    raise Exception('absent')
# 1 · CSS
i=idx(lambda l:l.startswith('#auraScreen.au2 .au-ombre{position:absolute!important;left:142.786px')); assert L[i+1].startswith('  margin:0!important;pointer-events:none;z-index:0;background:radial-gradient(closest-side,rgba(var(--c-brun09-rgb)')
L[i:i+2]=["/* ⚑ v137 (Tom, 8 oct. 2026, C-071) — « Code mort : retire le peintre du halo et ses règles CSS, et tout ce qui servait l'ombre. » Les règles de",
          "   `.au-ombre`, `.au-flaque` et `.au-halo` sont RETIRÉES : ces nœuds n'existent plus depuis v136. Plus aucun effet autour de la Pelote. */"]
for deb in ('#device:not(.light) #auraScreen.au2 .au-ombre{background:radial-gradient','#auraScreen.au2 .au-flaque{position:absolute','#device:not(.light) #auraScreen.au2 .au-flaque{display:none}','#auraScreen.au2 .au-halo{position:absolute'):
    j=idx(lambda l,d=deb:l.startswith(d)); del L[j]
# 2 · le peintre du halo (lot-V119-PELOTE) : dose, grain, CIBLE, _haloPelote
a=idx(lambda l:l.startswith("  /* l'opacité qui donne l'écart voulu entre le fond et (fond + ton × opacité)")); b=idx(lambda l:l.startswith("  var CIBLE={ras:7"),a)
del L[a:b+1]
c=idx(lambda l:l.startswith("  CIBLE.ras=REG.haloRas; CIBLE.mi=REG.haloRas*2.9/7;")); del L[c]
a=idx(lambda l:l.startswith("  /* W : le côté du canevas ; R : le rayon de la boule ; RS : celui de la silhouette")); b=idx(lambda l:l=="  };",a)
assert L[a+1].startswith("  window._haloPelote=function(")
L[a:b+1]=["  /* ⚑ v137 (Tom, 8 oct. 2026, C-071) — le peintre du halo (`window._haloPelote`, sa trame, son dosage) est RETIRÉ : plus aucun effet autour de la Pelote. */"]
# 3 · l'Aura : halo(), HAL, tonLumiere
a=idx(lambda l:l.startswith("  /* ⚑ v119, repris en v120 — LE MINI HALO : la lumière du velours qui déborde")); b=idx(lambda l:l.startswith("  var HAL={cv:null, cle:'', n:0};"),a)
L[a:b+1]=["  /* ⚑ v137 (Tom, 8 oct. 2026, C-071) — le mini halo (v119–v126), son canevas, sa teinte et sa respiration sont RETIRÉS du code. */"]
a=idx(lambda l:l.startswith("  /* ⚑ v125 (Tom, 3 oct. 2026) — « LE HALO PREND LA COULEUR DU CORPS")); b=idx(lambda l:l.startswith("    return [Math.round(c[0]),Math.round(c[1]),Math.round(c[2])]; }"),a)
assert b-a<12; del L[a:b+1]
a=idx(lambda l:l=="  function halo(){"); b=idx(lambda l:l=="  }",a); assert b-a<22,(b-a)
del L[a:b+1]
S='\n'.join(L)
def r(x,y,n=1):
    global S
    assert S.count(x)==n,(x[:60],S.count(x)); S=S.replace(x,y)
r("  window._peloteLumiere={etat:function(){ return {cle:HAL.cle, u:souffleU(), halo:!!(HCV&&HCV.width>300), ton:(function(){ try{ return tonLumiere(); }catch(_){ return null; } })()}; },\n                         recalibre:function(){ HAL.cle=''; }};",
  "  window._peloteLumiere={etat:function(){ return {cle:'', u:souffleU(), halo:false, ton:null}; }, recalibre:function(){}};   /* v137 : plus de halo ; `u` (le souffle) reste lu par les juges */")
r("var CAD, BO, CV, PRISE, MOT, INV, NX, LG, CPT, MO, GR, BT, D=null, FIN, HALO, OMBRE, FLAQUE, HCV;","var CAD, BO, CV, PRISE, MOT, INV, NX, LG, CPT, MO, GR, BT, D=null, FIN;")
io.open('app.html','w',encoding='utf-8').write(S)
S=io.open('app.html',encoding='utf-8').read()
r("      halo(); }catch(e){ window._auraErreur=String(e&&e.stack||e); PEL.pret=false; return; }","      }catch(e){ window._auraErreur=String(e&&e.stack||e); PEL.pret=false; return; }")
r("           halo(); PEL.peints=(PEL.peints||0)+1; }catch(e){ window._auraErreur=String(e&&e.stack||e); }","           PEL.peints=(PEL.peints||0)+1; }catch(e){ window._auraErreur=String(e&&e.stack||e); }")
r("    try{ HAL.cle=''; }catch(_){}            /* v125 : le halo se refait à la première image (il gardait la teinte de l'ouverture d'avant jusqu'à vingt images) */\n","")
io.open('app.html','w',encoding='utf-8').write(S)
