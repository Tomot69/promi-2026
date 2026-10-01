import sys, collections
from playwright.sync_api import sync_playwright
WK='--webkit' in sys.argv
POSE=r"""()=>{ window.__G=[]; const P=CanvasRenderingContext2D.prototype, g0=P.getImageData;
  P.getImageData=function(){ const t=performance.now(); const r=g0.apply(this,arguments); const dt=performance.now()-t;
    const st=(new Error().stack||'').split('\n').slice(2,3).map(s=>{const m=s.match(/at (\S+) .*?:(\d+):\d+/)||s.match(/(\w[\w$.]*)?@.*?:(\d+):\d+/); return m?((m[1]||'?')+':'+m[2]):s.slice(0,40);}).join('');
    let wr=null; try{ wr=this.getContextAttributes?this.getContextAttributes().willReadFrequently:null; }catch(_){}
    window.__G.push([st, this.canvas.width+'x'+this.canvas.height, +dt.toFixed(1), wr]); return r; }; }"""
with sync_playwright() as p:
    b=p.webkit.launch() if WK else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(3000)
    pg.evaluate(POSE); pg.evaluate("()=>{var k=null; for(var q in NUE){k=q;break;} closeAll(); openNueeDetail(k);}"); pg.wait_for_timeout(3500)
    G=pg.evaluate("()=>window.__G"); c=collections.defaultdict(lambda:[0,0.0,set()])
    for s,sz,dt,wr in G: c[s][0]+=1; c[s][1]+=dt; c[s][2].add(wr)
    for s,(n,t,w) in sorted(c.items(),key=lambda x:-x[1][1])[:8]: print('%-40s %4d lectures %7.0f ms  willRead=%s' % (s,n,t,w))
    print('les 5 plus lentes :', sorted(G,key=lambda x:-x[2])[:5])
    b.close()
