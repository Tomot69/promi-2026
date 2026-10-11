import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import io as _io
R=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for F in sys.argv[1:]:
        ctx=B.contexte(b,sombre=True); pg=B.ouvre(ctx,F)
        pg.evaluate("()=>{try{setPremium(true)}catch(e){} Toile.setTheme('ritournelle')}"); pg.wait_for_timeout(1500)
        R.append(Image.open(_io.BytesIO(B.capture(pg))).convert('RGB').resize((390,844)))
        pg.evaluate("()=>{ try{ obReplay(); }catch(e){} }"); pg.wait_for_timeout(2500)
        R.append(Image.open(_io.BytesIO(B.capture(pg))).convert('RGB').resize((390,844)))
        print(F, pg.evaluate("()=>({onb:!!document.getElementById('onbV'), vides:(Toile.env&&Toile.env.videsVus)})"))
        ctx.close()
    b.close()
W=Image.new('RGB',(400*len(R),844),'white')
for i,im in enumerate(R): W.paste(im,(i*400,0))
W.save('scratchpad/v143/onb3-vue.png')
