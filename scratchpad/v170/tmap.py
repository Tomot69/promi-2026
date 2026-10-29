import sys, os, io; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','M'); fz=float(os.environ.get('FZ','42')); ech=float(os.environ.get('ECH','0.7466')); N=int(os.environ.get('N','80'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    h={'À':GRAVE,'É':AIGU}.get(c,c)
    r=pg.evaluate(GEO_ECRAN,[h,fz,ech,'pose']); clip={'x':r['x'],'y':r['y'],'width':r['w'],'height':r['h']}
    lit=lambda: np.clip((255-np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(float))/231*255,0,255)
    ref=lit(); pg.evaluate("()=>{TraceLettres._debug=true; TraceLettres._Tmap=[];}"); pg.evaluate(GEO_ECRAN,[h,fz,ech,'arme'])
    tm=pg.evaluate("()=>TraceLettres._Tmap.filter(m=>m.car!==' ')")[-1]
    hh,ww=ref.shape; first=np.full((hh,ww),9.0); pinf=np.full((hh,ww),9.0)
    rev_prev=None; pinc=np.zeros((hh,ww),np.uint8); pinlist={}
    def dec(m,dx,dy):
        o_=np.zeros_like(m); ys=slice(max(0,dy),hh+min(0,dy)); yd=slice(max(0,-dy),hh+min(0,-dy)); xs=slice(max(0,dx),ww+min(0,dx)); xd=slice(max(0,-dx),ww+min(0,-dx)); o_[yd,xd]=m[ys,xs]; return o_
    for k in range(1,N+1):
        f=k/N*0.999; pg.evaluate(GEO_ECRAN,[h,fz,ech,f]); cur=lit()
        rev=(ref>127)&(cur>=ref*0.9); first[rev&(first>8)]=f
        nd=(ref>200)&(cur<ref*0.5); pin=np.zeros(ref.shape,bool)
        for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
            a1=np.zeros(ref.shape,bool); a2=np.zeros(ref.shape,bool)
            for s_ in (1,2,3): a1|=dec(rev,dx*s_,dy*s_); a2|=dec(rev,-dx*s_,-dy*s_)
            pin|=nd&a1&a2
        pinc=np.where(pin,pinc+1,0)
        for y,x in np.argwhere(pinc>=2): pinlist.setdefault((y,x),f)
    X0=clip['x']*3; Y0=clip['y']*3; W=tm['W']; H=tm['H']; T=np.array(tm['T']).reshape(H,W); T0=np.array(tm['T0']).reshape(H,W); A=np.array(tm['A']).reshape(H,W); Cc=np.array(tm['C']).reshape(H,W); tot=tm['tot']
    ox=int(round(tm['X0']-X0)); oy=int(round(tm['Y0']-Y0)); print('offset raster→screen',tm['X0']-X0,tm['Y0']-Y0, 'tot',tot)
    # alignment check: compare A with ref
    sub=ref[oy:oy+H, ox:ox+W]; print('A vs ref mean abs diff', np.abs(sub-A).mean(), 'shift tests:', [(dx,dy,round(float(np.abs(ref[oy+dy:oy+dy+H, ox+dx:ox+dx+W]-A).mean()),1)) for dx in (-1,0,1) for dy in (-1,0,1)])
    for (y,x),f in sorted(pinlist.items(), key=lambda q:q[1])[:20]:
        ry,rx=y-oy,x-ox; print('pin scr',(x,y),'at f',round(f,3),'ref',int(ref[y,x]),'obs first',round(float(first[y,x]),3), 'A',int(A[ry,rx]) if 0<=ry<H and 0<=rx<W else None,'C',int(Cc[ry,rx]) if 0<=ry<H and 0<=rx<W else None,'T0',round(T0[ry,rx]/tot,3) if 0<=ry<H and 0<=rx<W else None,'T',round(T[ry,rx]/tot,3) if 0<=ry<H and 0<=rx<W else None)
    ys,xs=np.nonzero((A>250)&(T0>=0)); o=[]; 
    for ry,rx in zip(ys,xs):
        y,x=ry+oy,rx+ox
        if 0<=y<hh and 0<=x<ww and first[y,x]<9: o.append((T[ry,rx]/tot, first[y,x], x, y, T0[ry,rx]/tot, Cc[ry,rx]))
    o=np.array(o); pf=np.polyfit(o[:,0],o[:,1],1); print('fit obs = %.3f*T + %.3f'%tuple(pf)); res=o[:,1]-np.polyval(pf,o[:,0]); idx=np.argsort(-res)[:15]
    for i in idx: print('  late', [round(v,3) for v in o[i]], 'res', round(res[i],3))
    import json; json.dump({'segs':tm['segs'],'lx0':tm['lx0'],'ly0':tm['ly0'],'s0':tm['s0'],'tot':tot}, open('scratchpad/v170/tmap.json','w'))
    np.save('scratchpad/v170/tmap.npy', np.array([first[oy:oy+H, ox:ox+W], T/tot, T0/tot, A, Cc]))
    b.close()
