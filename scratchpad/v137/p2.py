import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""    '  o=vec4(f.rgb*f.a+uCorps*t*(1.0-f.a), f.a+t*(1.0-f.a)); }'].join('\\n');""",
"""    /* ⚑ v137 (Tom, 8 oct. 2026, C-002) — LE LISERÉ DU BORD PART. « Sur les derniers 8 % du rayon, la fourrure prend une autre couleur que
       l'intérieur, et ça fait la deuxième couche que Tom voit. La fourrure du bord prend les couleurs de l'intérieur. » Cause : au bord
       les poils sont vus de profil, ils s'empilent — le poil y couvre le corps, alors qu'à l'intérieur on voit poil ET corps mêlés.
       Parade : au-delà de 0,92 R, la COULEUR d'un pixel est celle de son vis-à-vis à l'intérieur (même angle, rayon replié autour de
       0,92 R : poil sur corps, comme partout) ; son OPACITÉ reste la sienne — la silhouette ne bouge pas d'un pixel. Fondu de 0,90 à 0,93 R. */
    '  float al=f.a+t*(1.0-f.a); vec3 pm=f.rgb*f.a+uCorps*t*(1.0-f.a);',
    '  float rb=uR0*(0.92/0.972), w=clamp((r-rb*(0.90/0.92))/(rb*(0.03/0.92)),0.0,1.0); w=w*w*(3.0-2.0*w)*uA;',
    '  if(w>0.0 && al>0.0){ vec2 d=vec2(gl_FragCoord.x-uC2, gl_FragCoord.y-(uW2-uC2)); float rr=max(2.0*rb-r, rb*0.80);',
    '    vec4 g=texelFetch(uFur, ivec2(vec2(uC2, uW2-uC2)+d*(rr/max(r,1.0))), 0);',
    '    vec3 ci=g.rgb*g.a+uCorps*(1.0-g.a); pm=mix(pm, ci*al, w); }',
    '  o=vec4(pm, al); }'].join('\\n');""")
io.open('app.html','w',encoding='utf-8').write(S)
