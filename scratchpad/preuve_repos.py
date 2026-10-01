#!/usr/bin/env python3
"""AU REPOS, EST-CE QUE ÇA VIT ? On mesure sur les images, sans toucher à rien.
   Deux captures espacées, et le pourcentage de pixels qui ont changé."""
from playwright.sync_api import sync_playwright
DIFF=r"""([a,b2,x,y,w,h])=>Promise.all([a,b2].map(u=>new Promise(r=>{
  const im=new Image(); im.onload=()=>{const c=document.createElement('canvas');
    c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
    r(g.getImageData(x,y,w,h).data);}; im.src=u;}))).then(([A,B])=>{
  let n=0,tot=0,som=0;
  for(let i=0;i<A.length;i+=4){
    const la=0.299*A[i]+0.587*A[i+1]+0.114*A[i+2];
    const lb=0.299*B[i]+0.587*B[i+1]+0.114*B[i+2];
    const d=Math.abs(la-lb); som+=d; if(d>26) n++; tot++;
  }
  return {change:+(100*n/tot).toFixed(2), ecart:+(som/tot).toFixed(2)};
});"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':1000}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-SPHERE.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=120000); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.querySelectorAll('figure').forEach((f,i)=>{if(i>0)f.remove();});}")
    fr=pg.query_selector('.fr[data-vif]'); fr.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
    bb=fr.bounding_box(); CLIP={'x':bb['x'],'y':bb['y'],'width':390,'height':470}
    # ⚠ ON NEUTRALISE LA ROTATION D'ENSEMBLE : sinon on mesure la rotation, pas la vie.
    pg.evaluate("()=>{VUE_AUTO=0;}")
    seq=[0,1,2,4,8]
    for i,t in enumerate(seq):
        if i: pg.wait_for_timeout((seq[i]-seq[i-1])*1000)
        pg.screenshot(path='scratchpad/preuve/R%d.png'%t, clip=CLIP)
    pg.close()
    m=b.new_page(); m.goto('http://127.0.0.1:8752/scratchpad/mesure_png.html')
    m.wait_for_function("()=>window.__pret===true", timeout=30000)
    print('── AU REPOS, ROTATION D’ENSEMBLE NEUTRALISÉE — ce qui change tout seul')
    print('   %-22s %10s %10s' % ('écart','pixels changés','écart moyen'))
    for t in seq[1:]:
        r=m.evaluate(DIFF, ['/scratchpad/preuve/R0.png','/scratchpad/preuve/R%d.png'%t,
                            120,260,540,420])
        print('   %-22s %9.2f %% %9.2f' % ('après %d s'%t, r['change'], r['ecart']))
    b.close()
