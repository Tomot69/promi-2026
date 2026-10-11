import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
from PIL import Image
import io as _io
R={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for F in sys.argv[1:]:
        for sombre in (False,True):
            ctx=contexte(b,sombre=sombre,onb=False,guide=False,gestes_vus=False)
            # premier lancement réel : pas de thème mémorisé
            pg=ouvre(ctx,F,attente=7000); L=[]
            L.append(Image.open(_io.BytesIO(capture(pg))).convert('RGB').resize((390,844)))
            print(F,sombre,pg.evaluate("()=>{const o=document.getElementById('onbV')||document.getElementById('promiOnb'); const d=document.getElementById('device'); const cs=getComputedStyle(o||d); const cv=document.getElementById('toileCv'); return {onb:o&&o.id, bg:cs.backgroundColor, light:d.classList.contains('light')||document.documentElement.classList.contains('light'), theme:localStorage.getItem('promi_theme'), monde:Toile.getTheme()}}"))
            R[(F,sombre)]=L[0]; ctx.close()
    b.close()
W=Image.new('RGB',(400*len(R),844),'white')
for i,(k,im) in enumerate(R.items()): W.paste(im,(i*400,0))
W.save('scratchpad/v143/onb-vue.png')
