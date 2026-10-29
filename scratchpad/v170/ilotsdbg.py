import sys, os; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]
src=src.replace("        age = np.where(isl, age + 1, 0).astype(np.uint8);","        DBGI.append((i, [(len(m_), int(sum(q[1] for q in m_)/len(m_)), int(sum(q[0] for q in m_)/len(m_))) for m_ in composantes(isl)] if isl.any() else []))\n        age = np.where(isl, age + 1, 0).astype(np.uint8);",1)
DBGI=[]; exec(src)
ech=float(os.environ.get('ECH','0.7466'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    o=geo_ecran(pg,PENCHE,25,ech); print(o['ilots'],o['ilotMax'])
    for d in DBGI:
        if d[1]: print(d)
    b.close()
