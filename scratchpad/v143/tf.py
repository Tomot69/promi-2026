import sys, io
sys.argv=[sys.argv[0],'app.html']
src=io.open('redteam_trace.py',encoding='utf-8').read(); tete=src.split("    R = {r: bande(110, r) for r in (6, 12, 18)}")[0]
essai='''
    for d,r in ((0.14,10),(1.5,10),(0.45,6),(0.45,16)):
        t=bande(100,r,duree=d); print(d,r,'f méd',t['f'],[round(a.get('f') or 0,2) for a in pg.evaluate("()=>_aura.tracesGeo()")][:14], pg.evaluate("()=>window.__dbg"))
    b.close()
'''
exec(compile(tete+essai,'t','exec'))
