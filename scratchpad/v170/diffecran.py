import sys, os, io; sys.path.insert(0,'.'); sys.argv=sys.argv[:2]+['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','A'); fz=float(os.environ.get('FZ','42')); ech=float(os.environ.get('ECH','0.7466')); fr=[float(x) for x in os.environ.get('F','0.99999').split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    for m in [x for x in os.environ.get('ADD','').split(',') if x]: pg.add_script_tag(url='http://127.0.0.1:8752/'+m); pg.wait_for_timeout(300)
    h={'À':GRAVE,'É':AIGU,'Deuxio':PENCHE}.get(c,c)
    r=pg.evaluate(GEO_ECRAN,[h,fz,ech,'pose']); clip={'x':r['x'],'y':r['y'],'width':r['w'],'height':r['h']}
    lit=lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(int)
    ref=lit(); pg.evaluate(GEO_ECRAN,[h,fz,ech,'arme']); tiles=[]
    for f in fr:
        pg.evaluate(GEO_ECRAN,[h,fz,ech,f]); cur=lit(); d=np.abs(cur-ref)>12
        rA=np.clip((255-ref)/(231.0)*255,0,255); cA=np.clip((255-cur)/(231.0)*255,0,255); hh,ww=rA.shape
        def dec(m,dx,dy):
            o_=np.zeros_like(m); ys=slice(max(0,dy),hh+min(0,dy)); yd=slice(max(0,-dy),hh+min(0,-dy)); xs=slice(max(0,dx),ww+min(0,dx)); xd=slice(max(0,-dx),ww+min(0,-dx)); o_[yd,xd]=m[ys,xs]; return o_
        rev=(rA>127)&(cA>=rA*0.9); nd=(rA>200)&(cA<rA*0.5); pin=np.zeros(rA.shape,bool)
        for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
            a1=np.zeros(rA.shape,bool); a2=np.zeros(rA.shape,bool)
            for s_ in (1,2,3): a1|=dec(rev,dx*s_,dy*s_); a2|=dec(rev,-dx*s_,-dy*s_)
            pin|=nd&a1&a2
        unr=(rA>127)&(cA<=10); part=(rA>0)&(cA>10)&(cA<rA-10); rp=np.where(rA>0,cA/np.maximum(rA,1),0); vois=np.zeros(rA.shape,bool)
        for dy in range(-2,3):
            for dx in range(-2,3): vois|=dec(unr,dx,dy)|(dec(rA>127,dx,dy)&(dec(rp,dx,dy)<rp-0.05))
        loin=part&~vois
        o=np.stack([cur]*3,2).astype(np.uint8); o[d&(cur>ref)]=[255,170,170]; o[d&(cur<ref)]=[0,0,255]; o[pin]=[0,200,0]; o[loin]=[255,0,255]; print('  loin',int(loin.sum()),'pinces',int(pin.sum())); ys,xs=np.nonzero(loin); print('   ', [(int(x),int(y),int(rA[y,x]),int(cA[y,x]), int(rA[min(y+1,hh-1),x]), int(cA[min(y+1,hh-1),x]), int(rA[y-1,x]), int(cA[y-1,x])) for y,x in list(zip(ys,xs))[:6]])
        ys,xs=np.nonzero(ref<200); tiles.append(Image.fromarray(o).crop((xs.min()-4,ys.min()-4,xs.max()+5,ys.max()+5))); print(f, int(d.sum()))
    W=sum(t.width+3 for t in tiles); o=Image.new('RGB',(W,tiles[0].height),'green'); x=0
    for t in tiles: o.paste(t,(x,0)); x+=t.width+3
    z=int(os.environ.get('Z','4')); o.resize((o.width*z,o.height*z),Image.NEAREST).save('scratchpad/v170/diffecran.png'); b.close()
