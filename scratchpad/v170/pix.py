import sys, os, io; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','M'); fz=float(os.environ.get('FZ','52')); ech=float(os.environ.get('ECH','0.7466')); fr=float(os.environ.get('F','0.7778'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    r=pg.evaluate(GEO_ECRAN,[c,fz,ech,'pose']); clip={'x':r['x'],'y':r['y'],'width':r['w'],'height':r['h']}
    lit=lambda: np.clip((255-np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(float))/231*255,0,255)
    ref=lit(); pg.evaluate("()=>{TraceLettres._debug=true; TraceLettres._Tmap=[];}"); pg.evaluate(GEO_ECRAN,[c,fz,ech,'arme']); pg.evaluate(GEO_ECRAN,[c,fz,ech,fr]); cur=lit()
    tm=pg.evaluate("()=>TraceLettres._Tmap")[-1]; o=tm['o']; W=tm['W']; H=tm['H']; tot=tm['tot']
    ox=int(round(tm['X0']-clip['x']*3)); oy=int(round(tm['Y0']-clip['y']*3))
    hh,ww=ref.shape; rev=(ref>127)&(cur>=ref*0.9); nd=(ref>200)&(cur<ref*0.5)
    def dec(m,dx,dy):
        o_=np.zeros_like(m); ys=slice(max(0,dy),hh+min(0,dy)); yd=slice(max(0,-dy),hh+min(0,-dy)); xs=slice(max(0,dx),ww+min(0,dx)); xd=slice(max(0,-dx),ww+min(0,-dx)); o_[yd,xd]=m[ys,xs]; return o_
    pin=np.zeros(ref.shape,bool)
    for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
        a1=np.zeros(ref.shape,bool); a2=np.zeros(ref.shape,bool)
        for s_ in (1,2,3): a1|=dec(rev,dx*s_,dy*s_); a2|=dec(rev,-dx*s_,-dy*s_)
        pin|=nd&a1&a2
    for y,x in np.argwhere(pin):
        print('pin',x,y,'ref',int(ref[y,x]),'cur',int(cur[y,x]))
        for yy in range(y-3,y+4):
            row=[]
            for xx in range(x-4,x+5):
                ry,rx=yy-oy,xx-ox; k=ry*W+rx
                row.append('%3d/%3d/%s%s %.3f>%.3f'%(int(ref[yy,xx]), o['A'][k] if 0<=k<W*H else -1, 'C' if o['a2'][k] else '-', 'R' if rev[yy,xx] else ('n' if nd[yy,xx] else '.'), o['T0'][k]/tot if o['T0'][k] is not None and o['T0'][k]<1e300 else 9, o['T'][k]/tot if o['T'][k] is not None and o['T'][k]<1e300 else 9))
            print('  '+' | '.join(row))
    b.close()
