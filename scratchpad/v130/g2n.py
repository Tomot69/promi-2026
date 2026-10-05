from playwright.sync_api import sync_playwright
import base64
P=r"""()=>{ window.__g=[]; const f=Toile.dalleTrame; Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
 try{ const mi=dcv.__dalleInfo&&dcv.__dalleInfo.monde; if(!mi||mi.m!=='mosaique') return r;
  const g=dcv.getContext('2d'), w=dcv.width,h=dcv.height, d=g.getImageData(0,0,w,h).data, H={}; let n=0; for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const q=(d[i]>>3)+','+(d[i+1]>>3)+','+(d[i+2]>>3); H[q]=(H[q]||0)+1; }
  let m=null,mc=0; for(const q in H) if(H[q]>mc){ mc=H[q]; m=q; } if(!m||n<=60) return r; const c=m.split(',').map(v=>v*8+4); let au=0; const A={};
  for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; if(Math.max(Math.abs(d[i]-c[0]),Math.abs(d[i+1]-c[1]),Math.abs(d[i+2]-c[2]))>48){ au++; const q=(d[i]>>4)*16+','+(d[i+1]>>4)*16+','+(d[i+2]>>4)*16; A[q]=(A[q]||0)+1; } }
  const pc=100*au/n; if(pc>0.3){ const p=promises.find(x=>x.id===pid); window.__g.push({pid:pid, t:p?p.title:'?', nu:p?p.nuee:'', w:w,h:h, pc:+pc.toFixed(2), dom:c.join('/'), autres:Object.entries(A).sort((a,b)=>b[1]-a[1]).slice(0,4).map(e=>e[0]+'×'+e[1]).join(' '), opts:JSON.stringify(opts||{}).slice(0,80), url:dcv.toDataURL()}); } }catch(e){}
 return r; }; }"""
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','light')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{Toile.setPalette&&Toile.setPalette('signal')}catch(e){}}")
    for m in ('pixel','braille','mosaique'):
        pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m);}", m); pg.wait_for_timeout(2500)
        if m=='mosaique': pg.evaluate(P)
        for js in ("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}","()=>{closeAll(); setView('toile'); ouvrirIndex();}"):
            pg.evaluate(js); pg.wait_for_timeout(2600)
    G=pg.evaluate("()=>window.__g"); print(len(G))
    for i,x in enumerate(G):
        print('   ',{k:v for k,v in x.items() if k!='url'})
        if i<3: open(SC+'g2n-%d.png'%i,'wb').write(base64.b64decode(x['url'].split(',')[1]))
    b.close()
