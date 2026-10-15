# sonde : où WebKit pose-t-il chaque caractère ? (rectangles de Range contre chasses cumulées du canevas)
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/scratchpad/v146/trace/essai.html'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(1000)
    r = pg.evaluate("""()=>{ const out={}; for(const id of ['t','p','g']){ const el=document.getElementById(id), nd=el.firstChild, st=getComputedStyle(el), c=document.createElement('canvas').getContext('2d');
        c.font=st.fontStyle+' '+st.fontWeight+' '+st.fontSize+' '+st.fontFamily; const ls=parseFloat(st.letterSpacing)||0, txt=nd.nodeValue, rg=document.createRange(), L=[];
        const er=el.getBoundingClientRect();
        for(let i=0;i<Math.min(txt.length,12);i++){ rg.setStart(nd,i); rg.setEnd(nd,i+1); const q=rg.getClientRects()[0]; L.push([txt[i], +(q.left-er.left).toFixed(4), +(c.measureText(txt.slice(0,i)).width+i*ls).toFixed(4), +q.width.toFixed(4), +(c.measureText(txt[i]).width).toFixed(4), +q.top.toFixed(3), +q.height.toFixed(3)]); }
        const m=c.measureText('Hx'); out[id]={ls, L, fa:m.fontBoundingBoxAscent, fd:m.fontBoundingBoxDescent, asc:TraceLettres?0:0, top:er.top}; }
      return out; }""")
    for k, v in r.items():
        print(k, 'ls', v['ls'], 'fontBBox asc/desc', v['fa'], v['fd'], 'top', v['top'])
        for l in v['L']: print('   ', l)
    b.close()
