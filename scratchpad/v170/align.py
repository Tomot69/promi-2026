import sys, os, io; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
ech=float(os.environ.get('ECH','0.7466'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    for rond in (0,4,8,16):
        tot=[]
        for c,fz in [(c_,f_) for c_ in 'UPEO' for f_ in (19,25,29,42)]:
            r=pg.evaluate(GEO_ECRAN,[c,fz,ech,'pose']); clip={'x':r['x'],'y':r['y'],'width':r['w'],'height':r['h']}
            ref=np.clip((255-np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(float))/231*255,0,255)
            pg.evaluate("r=>{TraceLettres._debug=true; TraceLettres._Tmap=[]; TraceLettres._rond=r;}", rond); pg.evaluate(GEO_ECRAN,[c,fz,ech,'arme']); pg.evaluate(GEO_ECRAN,[c,fz,ech,0.5])
            tm=pg.evaluate("()=>TraceLettres._Tmap")[-1]; W=tm['W']; H=tm['H']; A=np.array(tm['o']['A'],float).reshape(H,W)
            ox=int(round(tm['X0']-clip['x']*3)); oy=int(round(tm['Y0']-clip['y']*3))
            best=sorted((float(np.abs(ref[oy+dy:oy+dy+H, ox+dx:ox+dx+W]-A).mean()),dx,dy) for dx in (-1,0,1) for dy in (-1,0,1))
            d0=float(np.abs(ref[oy:oy+H, ox:ox+W]-A).mean()); tot.append(d0)
            rp=ref[oy:oy+H, ox:ox+W].sum(1); ap=A.sum(1); cp_=ref[oy:oy+H, ox:ox+W].sum(0); acp=A.sum(0)
            def edges(p):
                m=p.max(); idx=np.nonzero(p>0.5*m)[0]; return idx[0], idx[-1]
            def sub(p):
                m=p.max(); i=np.nonzero(p>0.5*m)[0]; a,b_=i[0],i[-1]; fa=a-(p[a]-0.5*m)/max(p[a]-p[a-1],1e-9); fb=b_+(p[b_]-0.5*m)/max(p[b_]-p[b_+1],1e-9); return round(fa,2), round(fb,2)
            print('   rows ref',sub(rp),'A',sub(ap),' cols ref',sub(cp_),'A',sub(acp))
            print(rond,c,fz,'tY %.3f oy %.3f tX %.3f ox %.3f'%(tm['tY'],tm['oyabs'],tm['tX'],tm['oxabs']),'d0 %.1f'%d0,'best',[(round(q[0],1),q[1],q[2]) for q in best[:2]])
            pg.evaluate("()=>{ if(window.__CG){ window.__CG.stop(); window.__CG=null; } }")
        print('ROND',rond,'moy',round(sum(tot)/len(tot),2))
    b.close()
