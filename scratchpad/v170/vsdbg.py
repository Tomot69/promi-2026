import sys, os, json; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','E'); fz=float(os.environ.get('FZ','25'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'pose']); pg.evaluate("()=>{TraceLettres._debug=true; TraceLettres._vs=[];}"); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'arme'])
    v=pg.evaluate("()=>TraceLettres._vs"); 
    for g in v: print(g['car'], json.dumps([{k:(round(x,1) if isinstance(x,(int,float)) else x) for k,x in s.items() if k!='cible'} for s in g['steps']]))
    print(pg.evaluate("()=>JSON.stringify(TraceLettres.parcours('PromiLate','E','h').ordre)"))
    b.close()
