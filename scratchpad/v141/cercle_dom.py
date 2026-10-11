import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("(k)=>{closeAll();openEssaim(k);}",sys.argv[1] if len(sys.argv)>1 else 'potager'); pg.wait_for_timeout(3000)
    Q="""()=>{const D=document.getElementById('device').getBoundingClientRect(); const out=[]; document.querySelectorAll('#detailPoster *').forEach(e=>{ const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden') return; const r=e.getBoundingClientRect(); if(r.width<20||r.height<10) return; const t=(e.childElementCount<=3?(e.textContent||''):'').trim().slice(0,34); if(!/Planter|Dissoudre|COMMENTAIRES|Commentaires|PIÈCES|Peaufiner/i.test(t) && !/np-|nf-add|s2-cercle|nq/.test(e.className+e.id)) return; out.push([e.tagName,e.id,(''+e.className).slice(0,30),t,Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height),c.position,c.borderTopWidth,c.borderRadius.slice(0,6),c.overflowY]); }); return out; }"""
    print('── fiche'); [print(x) for x in pg.evaluate(Q)]
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1800)
    print('── Peaufiner'); [print(x) for x in pg.evaluate(Q)]
    print(pg.evaluate("()=>[...document.querySelectorAll('#detailPoster *')].filter(e=>{const c=getComputedStyle(e);return /(auto|scroll)/.test(c.overflowY)&&e.scrollHeight>e.clientHeight+2}).map(e=>[e.id||e.className,e.scrollHeight,e.clientHeight])"))
    b.close()
