from playwright.sync_api import sync_playwright
JS=r"""()=>{const out=[];
 document.querySelectorAll('.fr').forEach((f,fi)=>{
  const ns=[...f.querySelectorAll('*')].filter(n=>{const cs=getComputedStyle(n),r=n.getBoundingClientRect();
    return cs.display!=='none'&&r.height>4&&[...n.childNodes].some(c=>c.nodeType===3&&c.nodeValue.trim());});
  ns.sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top);
  for(let i=0;i<ns.length-1;i++){const a=ns[i].getBoundingClientRect(),b=ns[i+1].getBoundingClientRect();
    if(ns[i].contains(ns[i+1])||ns[i+1].contains(ns[i]))continue;
    const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left); if(ox<=0)continue;
    const g=b.top-a.bottom; if(g>=0&&g<10)
      out.push(fi+' :: «'+ns[i].textContent.trim().slice(0,20)+'» → «'+ns[i+1].textContent.trim().slice(0,20)+'» : '+g.toFixed(1)+' px');}
 }); return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1800,'height':1200},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-TROIS-PARTIS.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=30000); pg.wait_for_timeout(1800)
    r=pg.evaluate(JS); print(len(r),'paires sous 10 px')
    for x in r: print('  ',x)
    b.close()
