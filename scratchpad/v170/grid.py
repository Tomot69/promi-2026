import sys, os, io; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','S'); fz=float(os.environ.get('FZ','29')); f=float(os.environ.get('F','0.25')); cx,cy=[int(v) for v in os.environ.get('XY','49,75').split(',')]; R_=int(os.environ.get('RAD','8'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    r=pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'pose']); clip={'x':r['x'],'y':r['y'],'width':r['w'],'height':r['h']}
    lit=lambda: np.clip((255-np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(float))/231*255,0,255)
    ref=lit(); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'arme']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,f]); cur=lit()
    for y in range(cy-R_,cy+R_+1):
        print('%3d '%y+' '.join(('  .' if ref[y,x]<30 else ('%3d'%int(100*cur[y,x]/max(ref[y,x],1)))) for x in range(cx-R_-4,cx+R_+5)))
    b.close()
