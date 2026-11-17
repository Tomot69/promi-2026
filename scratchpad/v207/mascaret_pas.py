# C-295 : l'aperçu de Mascaret au Studio, image par image — combien il change d'une image à l'autre (une animation lisse change un peu à chaque image ;
# une saccade = des images figées puis un saut). Gratuit (monde verrouillé, comme Tom), Toile de l'export de Tom. Usage : FICH=app.html python3 ... [--guide]
import sys, os, json; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html')
SONDE="""()=>new Promise(res=>{ const bg=document.getElementById('stBg'); const c=document.createElement('canvas'); c.width=78; c.height=169;
  const g=c.getContext('2d',{willReadFrequently:true}); let av=null, out=[], t0=performance.now(), tp=null;
  (function f(t){ g.drawImage(bg,0,0,78,169); const d=g.getImageData(0,0,78,169).data; let s=0;
    if(av){ for(let i=0;i<d.length;i+=4){ s+=Math.abs(d[i]-av[i])+Math.abs(d[i+1]-av[i+1])+Math.abs(d[i+2]-av[i+2]); } }
    if(av) out.push([Math.round(t-tp), Math.round(s/(78*169)*100)/100]); av=d.slice(); tp=t;
    if(performance.now()-t0<%d) requestAnimationFrame(f); else res(out); })(performance.now()); })"""
guide='--guide' in sys.argv
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, guide=not guide); pg=B.ouvre(ctx,F)
    pg.evaluate("()=>{ closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    vus=[]
    for i in range(24):
        m=pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m=='mascaret' or m in vus: break
        vus.append(m); B.glisse(pg, B.droite([300,420],[90,420],10), pas=16); pg.wait_for_timeout(1500)
    print(F, 'monde', pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')"), 'charge %.1f'%B.charge())
    if '--sansprep' in sys.argv: pg.evaluate("()=>{ Toile.apercuCompose=null; Toile.apercuPrepare=function(){return true}; Toile.apercuPrepareProchain=function(){return true}; }")
    pg.wait_for_timeout(4000)
    r=pg.evaluate(SONDE % 12000)
    ch=[x[1] for x in r]; dt=[x[0] for x in r]
    nul=sum(1 for v in ch if v<0.05); 
    print('images',len(r),'figées (Δ<0,05)',nul,'dt>20',sum(1 for v in dt if v>20),'Δ p50 %.2f p95 %.2f max %.2f'%(sorted(ch)[len(ch)//2], sorted(ch)[int(.95*len(ch))], max(ch)))
    s=''.join('_' if v<0.05 else ('.' if v<1 else ('o' if v<4 else 'X')) for v in ch)
    for i in range(0,len(s),120): print('  ',s[i:i+120])
    json.dump(r, open('scratchpad/v207/mascaret_%s%s.json'%(os.path.basename(F).replace('.html',''),'_g' if guide else ''),'w'))
    b.close()
