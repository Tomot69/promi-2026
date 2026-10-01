from playwright.sync_api import sync_playwright
import json
JS = r"""
() => {
  const out = {};
  const gone = (id)=>{const n=document.getElementById(id); if(!n) return 'ABSENT DU DOM';
    const cs=getComputedStyle(n), r=n.getBoundingClientRect();
    return (cs.display==='none'?'display:none':cs.visibility==='hidden'?'visibility:hidden':(+cs.opacity<=0.02?'opacity 0':(r.width*r.height===0?'0 x 0':'VU '+Math.round(r.width)+'x'+Math.round(r.height))));};
  const clsState=(sel)=>{const n=document.querySelector(sel); if(!n) return 'ABSENT DU DOM';
    const cs=getComputedStyle(n), r=n.getBoundingClientRect();
    return (cs.display==='none'?'display:none':(r.width*r.height===0?'0 x 0':'VU'));};
  ['kEvolve','plusCta','kStats','kLegend','kPct','kCount','kBalance','kEquilibre','kTogether','kessaims','ksocial','kpers','kBestNue','kDelta','ringLeg','kxaxis','kchart','kLens','auraSeal','souffleLine','karmaCercle'].forEach(i=>out[i]=gone(i));
  ['.klabel','.kbig','.kst','.pp-leg','.k-intro .lbl-free','.k-intro .lbl-prem'].forEach(s=>out[s]=clsState(s));
  return out;
}
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for prem in (False, True):
        pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/app.html')
        pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if prem: pg.evaluate("()=>setPremium(true)")
        pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        pg.wait_for_timeout(2500)
        print('=== PREMIUM' if prem else '=== GRATUIT')
        for k,v in pg.evaluate(JS).items(): print(f'  {k:<26} {v}')
        pg.close()
    b.close()
