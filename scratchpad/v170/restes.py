import sys, os, io, base64; sys.path.insert(0,'.'); sys.argv=sys.argv[:1]
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} TraceLettres._debug=true; TraceLettres._restes=[]; }")
    pg.evaluate(GEO_ECRAN,[os.environ.get('C','A'),float(os.environ.get('FZ','42')),0.7466,'pose']); pg.evaluate(GEO_ECRAN,[os.environ.get('C','A'),float(os.environ.get('FZ','42')),0.7466,'arme'])
    r=pg.evaluate("()=>TraceLettres._restes.map(x=>({car:x.car,n:x.n,tot:x.tot,tmax:x.tmax,c1:x.c1,c2:x.c2}))")
    for x in r:
        print(x['car'], x['n'], x['tot'], x['tmax'])
        a=Image.open(io.BytesIO(base64.b64decode(x['c1'].split(',')[1]))); c=Image.open(io.BytesIO(base64.b64decode(x['c2'].split(',')[1])))
        A_=np.asarray(a)[:,:,3]; C_=np.asarray(c)[:,:,3]; o=np.zeros(A_.shape+(3,),np.uint8)+255; o[A_>16]=[80,80,80]; o[(A_>16)&(C_<=250)]=[255,0,0]; o[(A_<=16)&(C_>0)]=[200,220,255]
        Image.fromarray(o).resize((o.shape[1]*4,o.shape[0]*4),Image.NEAREST).save('scratchpad/v170/restes.png')
    b.close()
