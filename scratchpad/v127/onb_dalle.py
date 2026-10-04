# la dalle de la nouvelle parole sur la dernière diapositive : sa boîte à l'écran (points 390×844), et celles des autres dalles colorées
import sys, json, io
from playwright.sync_api import sync_playwright
from PIL import Image
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG = sys.argv[2] if len(sys.argv)>2 else 'x'
def joue(pg):
    pg.mouse.click(20+195, 44+260); pg.wait_for_timeout(300); pg.keyboard.type('Tom', delay=40); pg.wait_for_timeout(400)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    pg.keyboard.type('appeler Mamie dimanche', delay=25); pg.wait_for_timeout(500)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    r = pg.evaluate("()=>{const c=document.getElementById('onbTrait').getBoundingClientRect(); return [c.left,c.top,c.width,c.height]}")
    y = r[1]+r[3]*0.6; pg.mouse.move(r[0]+r[2]*0.11, y); pg.mouse.down()
    for i in range(1,26): pg.mouse.move(r[0]+r[2]*(0.11+0.42*i/25), y); pg.wait_for_timeout(16)
    pg.mouse.up(); pg.wait_for_timeout(4200)
BOITE = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, cv=document.getElementById('toileCv'), R=cv.getBoundingClientRect(), sx=R.width/cv.clientWidth;
  const p=promises.filter(q=>!q.draft).slice(-1)[0]; const a=Toile.dalleAbs(p.id);
  const B=(a)=>a?[+((R.left-dv.left+a.minx*sx)/k).toFixed(2), +((R.top-dv.top+a.miny*sx)/k).toFixed(2), +(a.w*sx/k).toFixed(2), +(a.h*sx/k).toFixed(2)]:null;
  const fin=document.getElementById('onbFin'), fr=fin&&fin.getBoundingClientRect();
  const V=[]; for(let i=0;i<12;i++){ try{ const b=Toile.dalleAbs(900000001+i); if(b) V.push(B(b)); }catch(e){} }
  return {principale:B(a), voisines:V, fin: fr?[+((fr.top-dv.top)/k).toFixed(1), +((fr.bottom-dv.top)/k).toFixed(1)]:null, monde:Toile.getTheme(), pal:Toile.getPalette()}; }"""
if __name__=='__main__':
    with sync_playwright() as p:
        b=p.webkit.launch()
        for th in ('light','dark'):
            for rep in range(2 if th=='light' else 1):
                ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
                ctx.add_init_script("try{localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
                pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
                pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(7000)
                pg.evaluate("(t)=>{ try{ if((localStorage.getItem('promi_theme')||'')!==t || document.documentElement.classList.contains('light')!==(t==='light')) setTheme(t) }catch(e){} }", th); pg.wait_for_timeout(600)
                joue(pg); r=pg.evaluate(BOITE); print(TAG, th, json.dumps(r, ensure_ascii=False))
                pg.screenshot(path='scratchpad/v127/fin-%s-%s.png'%(TAG,th), clip={'x':20,'y':44,'width':390,'height':844})
                ctx.close()
        b.close()
