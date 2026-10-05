import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("pointer-events:none!important;max-width:none!important;display:block}","pointer-events:none!important;max-width:none!important;display:block!important;visibility:visible!important;opacity:1!important}")
rep("""    /* la place : au-dessus du bouton, comme avant — recalculée, le menu a changé de hauteur */
    var k=((dev()||{}).getBoundingClientRect ? dev().getBoundingClientRect().width : 390)/390||1, h=m.getBoundingClientRect().height/k, top=parseFloat(b.style.top)||0;
    m.style.setProperty('top', Math.round(top-10-h)+'px', 'important'); };""",
"""    /* la place : À GAUCHE du bouton, son bas aligné sur le bas du bouton — au-dessus de lui, quatre ou cinq lignes passaient sous le
       plateau (le plateau finit à 100). Jamais plus haut que 106. */
    var k=((dev()||{}).getBoundingClientRect ? dev().getBoundingClientRect().width : 390)/390||1, h=m.getBoundingClientRect().height/k, top=parseFloat(b.style.top)||0, gauche=parseFloat(b.style.left)||332;
    m.style.setProperty('left', '24px', 'important'); m.style.setProperty('width', Math.max(120, gauche-8-24)+'px', 'important');
    m.style.setProperty('top', Math.max(106, Math.round(top+34-h))+'px', 'important'); };""")
io.open('app.html','w',encoding='utf-8').write(S)
