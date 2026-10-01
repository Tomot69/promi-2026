from playwright.sync_api import sync_playwright
MB="http://127.0.0.1:8752/promi-moodboard-H.html"
MARQUE="""()=>{const isF=e=>{const s=e.getAttribute('style')||'';
  return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  [...document.querySelectorAll('div')].filter(isF).forEach((f,i)=>f.setAttribute('data-cadre',i));}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1000})
    pg.goto(MB); pg.wait_for_timeout(4500); pg.evaluate(MARQUE)
    for n in (72,76):
        r=pg.evaluate("""(n)=>{const f=document.querySelector('[data-cadre="'+n+'"]');
          const fr=f.getBoundingClientRect(); const out=[];
          f.querySelectorAll('*').forEach(e=>{
            let t=''; e.childNodes.forEach(k=>{if(k.nodeType===3)t+=k.nodeValue;});
            t=t.replace(/\\s+/g,' ').trim(); if(!t) return;
            const r2=e.getBoundingClientRect(); const c=getComputedStyle(e);
            out.push([Math.round(r2.left-fr.left),Math.round(r2.top-fr.top),
                      Math.round(r2.width),Math.round(r2.height),
                      c.fontSize+'/'+c.fontWeight, c.color, t.slice(0,32)]);});
          return out;}""", n)
        print("════ cadre",n,"════")
        for x in r: print("  @%3d,%3d %3dx%2d %-9s %-22s « %s »"%tuple(x))
    b.close()
