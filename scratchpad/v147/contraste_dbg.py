import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
exec(open('redteam_contraste_trait.py',encoding='utf-8').read().split('res = []; LIGNES = []')[0].split('SEUIL = 3.0')[1].replace("PAGE = next","PAGE0 = next"), globals())
OUT=sys.argv[1]; QUOI=sys.argv[2]; TH=sys.argv[3] if len(sys.argv)>3 else 'clair'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True,is_mobile=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s');}catch(e){}" % ('light' if TH=='clair' else 'dark'))
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    sel='#dpTrameCv'
    if QUOI=='cercle': pg.evaluate("()=>openNueeDetail(Object.keys(NUE)[0])")
    elif QUOI=='chiche': pg.evaluate("()=>openDetail(promises.find(p=>p.chiche&&!p.draft&&p.status!=='tenu').id)")
    elif QUOI=='promi': pg.evaluate("()=>openDetail(promises.find(p=>!p.chiche&&!p.draft&&!p.nuee&&p.status!=='tenu').id)")
    elif QUOI=='index': pg.evaluate("()=>ouvrirIndex()"); sel='#indexList canvas[data-trait], #feedView canvas[data-trait]'
    elif QUOI=='fil': pg.evaluate("()=>document.getElementById('filBtn').click()"); sel='#indexList canvas[data-trait], #feedView canvas[data-trait]'
    elif QUOI.startswith('plus'): pg.evaluate("(k)=>{ document.getElementById('createBtn').click(); setTimeout(()=>{ const b=document.querySelector('.acc-pil[data-k='+k+']'); if(b) b.click(); }, 600); }", QUOI.split('-')[1]); sel='#csTrameCv'
    pg.wait_for_timeout(3500)
    G=pg.evaluate(GEO, sel); pg.screenshot(path=OUT); im=Image.open(OUT).convert('RGB'); d=ImageDraw.Draw(im)
    for g in G:
        bx=g['box']; d.rectangle([bx[0]*3,bx[1]*3,(bx[0]+bx[2])*3,(bx[1]+bx[3])*3], outline=(255,0,255), width=3)
        for s in g['S']:
            for yy,c in ((s['y'],(255,0,0)),(s['h'],(0,255,0)),(s['b'],(0,0,255))): d.ellipse([s['x']*3-5,yy*3-5,s['x']*3+5,yy*3+5], outline=c, width=2)
    im.save(OUT); print([ (g['col'], g['mode'], g['box']) for g in G][:6])
    print(pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'); return c&&[c.getAttribute('data-trait'), c.width, c.height, c.getBoundingClientRect().height] }"))
    b.close()
