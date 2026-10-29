import sys, os, re; sys.path.insert(0,'.'); sys.argv=['x']
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
c=os.environ.get('C','M'); fz=float(os.environ.get('FZ','52')); fr=[float(v) for v in os.environ.get('F','0.7778').split(',')]; X,Y=[int(v) for v in os.environ.get('XY','90,49').split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }"); pg.add_style_tag(content='#device{visibility:hidden!important} body{background:#fff!important}')
    r=pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'pose']); pg.evaluate(GEO_ECRAN,[c,fz,0.7466,'arme'])
    for f in fr:
        pg.evaluate(GEO_ECRAN,[c,fz,0.7466,f])
        res=pg.evaluate("""a=>{ const [cx,cy,X,Y]=a; const el=document.getElementById('gEl'), er=el.getBoundingClientRect(), k=er.width/el.offsetWidth;
          const lx=(cx+(X+0.5)/3-er.left)/k, ly=(cy+(Y+0.5)/3-er.top)/k; const cp=getComputedStyle(el).clipPath; const d=cp.slice(cp.indexOf('"')+1, cp.lastIndexOf('"'));
          const subs=d.split(/(?=M)/).filter(s=>s.trim()); const hits=[];
          subs.forEach((s,i)=>{ const n=(s.match(/-?[\\d.]+/g)||[]).map(Number); let P; if(s.includes('h')){ const c=n[2]; P=[[n[0],n[1]],[n[0]+c,n[1]],[n[0]+c,n[1]+c],[n[0],n[1]+c]]; } else { P=[]; for(let j=0;j+1<n.length;j+=2) P.push([n[j],n[j+1]]); }
            let ins=false; for(let a2=0,b2=P.length-1;a2<P.length;b2=a2++){ if(((P[a2][1]>ly)!==(P[b2][1]>ly)) && (lx < (P[b2][0]-P[a2][0])*(ly-P[a2][1])/(P[b2][1]-P[a2][1])+P[a2][0])) ins=!ins; }
            const dmin=Math.min(...P.map((q,j)=>{ const q2=P[(j+1)%P.length]; const dx=q2[0]-q[0], dy=q2[1]-q[1], l2=dx*dx+dy*dy; let u=l2?((lx-q[0])*dx+(ly-q[1])*dy)/l2:0; u=Math.max(0,Math.min(1,u)); return Math.hypot(q[0]+dx*u-lx,q[1]+dy*u-ly); }));
            if(ins || dmin<1) hits.push([i, ins, +dmin.toFixed(3), s.includes('h')?'sq':P.length, s.slice(0,90)]); });
          return {lx,ly,k,hits}; }""",[r['x'],r['y'],X,Y])
        print(f, round(res['lx'],3), round(res['ly'],3), res['k']); [print('  ',h) for h in res['hits']]
    b.close()
