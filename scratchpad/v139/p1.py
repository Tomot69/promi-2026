import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:60]); S=S.replace(a,b)
rep("""    '  float t=r<=uR0 ? 1.0 : (r>=uR1 ? 0.0 : 1.0-(r-uR0)/(uR1-uR0)); t=t*t*(3.0-2.0*t); t*=uA;',""",
"""    /* ⚑ v139 (Tom, 9 oct. 2026, C-083) — LE CONTOUR EST UNE LIMITE FRANCHE : « plus de poils épars de longueurs différentes. La silhouette
       est une limite franche, la fourrure s'arrête au bord. » Tout ce qui est en deçà de uR0 est plein (poil sur corps), rien au-delà ;
       un seul pixel de lissage. Le repli de couleur de v137 est retiré : la frange à demi transparente qu'il corrigeait n'existe plus. */
    '  float t=clamp(uR0-r+0.5,0.0,1.0);',""")
a=S.index("    '  float al=f.a+t*(1.0-f.a); vec3 pm=f.rgb*f.a+uCorps*t*(1.0-f.a);',")
b=S.index("    '  o=vec4(pm, al); }'].join('\\n');")
S=S[:a]+"""    '  float fa=uA>0.5 ? 1.0 : f.a; vec3 pm=f.rgb*f.a+uCorps*uA*(1.0-f.a);',
"""+S[b:]
rep("    '  o=vec4(pm, al); }'].join('\\n');","    '  o=vec4(pm*t, fa*t); }'].join('\\n');")
rep("gl.uniform1f(u2.uR0,E.R*1.0); gl.uniform1f(u2.uR1,E.R*1.012);","gl.uniform1f(u2.uR0,E.R*(window._peloteBord||1.0)); gl.uniform1f(u2.uR1,E.R*1.012);")
io.open(f,'w',encoding='utf-8').write(S)
