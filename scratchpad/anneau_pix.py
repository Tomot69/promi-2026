import sys, base64
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
JS = r"""async ([u,box])=>{ const im=new Image(); im.src=u; await im.decode();
  const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const g=c.getContext('2d'); g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data, W=c.width;
  const cx=box.cx, cy=box.cy, R=box.r, N=360, out=[];
  for(let i=0;i<N;i++){ const a=i*Math.PI*2/N, x=Math.round(cx+R*Math.cos(a)), y=Math.round(cy+R*Math.sin(a)), k=(y*W+x)*4;
    out.push('#'+[d[k],d[k+1],d[k+2]].map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase()); }
  const cnt={}; out.forEach(h=>cnt[h]=(cnt[h]||0)+1);
  return Object.entries(cnt).sort((a,b)=>b[1]-a[1]).slice(0,10); }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e); if(s.animationName&&s.animationName!=='none') e.style.animationPlayState='paused';});}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(800)
        box=pg.evaluate("""()=>{const e=document.getElementById('createBtn'); const r=e.getBoundingClientRect();
          const p=document.getElementById('device').getBoundingClientRect(); const s=1;
          return {cx:(r.left+r.width/2-p.left)*2, cy:(r.top+r.height/2-p.top)*2, r:(r.width/2-6)*2};}""")
        u='data:image/png;base64,'+base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        print(th, pg.evaluate(JS,[u,box]))
    b.close()
