import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
# la carte graphique
r("'uniform sampler2D uFur;','uniform vec3 uCorps;','uniform float uA,uR0,uR1,uC2,uW2;','out vec4 o;',","'uniform sampler2D uFur;','uniform vec3 uCorps;','uniform vec3 uBord;','uniform float uA,uR0,uR1,uC2,uW2;','out vec4 o;',")
r("    '  o=vec4(f.rgb*f.a+uCorps*t*(1.0-f.a), f.a+t*(1.0-f.a)); }'].join('\\n');",
"""    /* ⚑ v136 (Tom, C-002, récidive : « une deuxième couche floue autour de la Pelote ») — LE CORPS NE PARAÎT PAS AU BORD. Depuis v123 le corps
       est d'une AUTRE teinte que les poils ; au limbe la fourrure s'amincit, et le disque plein du corps (opaque jusqu'à 0,972 R) y dessinait
       un anneau de sa couleur, plus large d'un côté : un second contour. De 0,86 R au bord, le corps FOND vers la couleur du poil (celle du
       poil présent sur ce pixel, sinon la marche médiane de sa rampe) : au bord il n'y a plus que la couleur de la fourrure. */
    '  float lim=smoothstep(uR0*0.885, uR0*0.985, r); vec3 pb=(f.a>0.02) ? f.rgb : uBord; vec3 cc=mix(uCorps, pb, lim);',
    '  o=vec4(f.rgb*f.a+cc*t*(1.0-f.a), f.a+t*(1.0-f.a)); }'].join('\\n');""")
r("['uFur','uCorps','uA','uR0','uR1','uC2','uW2'].forEach(","['uFur','uCorps','uBord','uA','uR0','uR1','uC2','uW2'].forEach(")
r("gl.uniform3f(u2.uCorps,C[0]/255,C[1]/255,C[2]/255); gl.uniform1f(u2.uA,o.corps?1:0);","gl.uniform3f(u2.uCorps,C[0]/255,C[1]/255,C[2]/255); gl.uniform1f(u2.uA,o.corps?1:0); var _Bd=o.bord||C; gl.uniform3f(u2.uBord,_Bd[0]/255,_Bd[1]/255,_Bd[2]/255);")
# le peintre du processeur : la peau fond vers le poil au bord
r("function peau(B,W,BLOC,OMB,VERS,CORPS){","function peau(B,W,BLOC,OMB,VERS,CORPS,RAYON){")
r("      if(CORPS){ rr=CORPS[0]|0; gg=CORPS[1]|0; bb=CORPS[2]|0; }","""      if(CORPS){ rr=CORPS[0]|0; gg=CORPS[1]|0; bb=CORPS[2]|0;
        /* v136 (C-002) : au bord, le corps fond vers la couleur du poil de ce bloc — plus d'anneau de corps au limbe */
        if(RAYON){ var _rb=Math.hypot((x0+x1)/2-W/2,(y0+y1)/2-W/2), _l0=RAYON*0.972*0.885, _l1=RAYON*0.972*0.985, _lm=_rb<=_l0?0:(_rb>=_l1?1:(_rb-_l0)/(_l1-_l0)); _lm=_lm*_lm*(3-2*_lm);
          if(_lm>0){ rr=(rr*(1-_lm)+(sr/sw)*_lm)|0; gg=(gg*(1-_lm)+(sg/sw)*_lm)|0; bb=(bb*(1-_lm)+(sb/sw)*_lm)|0; } } }""")
r("PK=peau(B,W,PB,o.omb,o.peauVers,o.corps);","PK=peau(B,W,PB,o.omb,o.peauVers,o.corps,R);")
# l'option : la marche médiane de la rampe du poil
r("emp:(EMP && EMP.p>=G.EMP_FIN) ? empPour(EMP) : null, peauVers:peauVers(), corps:corps()};","emp:(EMP && EMP.p>=G.EMP_FIN) ? empPour(EMP) : null, peauVers:peauVers(), corps:corps(), bord:(function(){ try{ var _p=PEL.solR||solEffectif(), _R=M.rampeVelours(_p); return _R[(_R.length*0.55)|0]||_p; }catch(_){ return null; } })()};")
io.open('app.html','w',encoding='utf-8').write(S)
