import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':651},device_scale_factor=3); pg=ctx.new_page(); pg.set_content('<body style="margin:0;background:#fff"></body>')
    for ech in (1, 0.7466):
        for prop in ('clip-path','mask'):
            pg.evaluate("""a=>{ const [e,pr]=a; document.body.innerHTML='<div id=w style="position:fixed;left:10px;top:10px;transform-origin:0 0;transform:scale('+e+')"><div id=t style="width:200px;height:100px;background:#000"></div></div>';
              const t=document.getElementById('t'); const d='M0 0L200 0L200 37.3L0 62.1Z';
              if(pr==='clip-path') t.style.clipPath='path(\"'+d+'\")'; else { t.style.webkitMaskImage='url(\"data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'200\\' height=\\'100\\'><path d=\\''+d+'\\'/></svg>')+'\")'; t.style.webkitMaskSize='200px 100px'; } }""", [ech, prop])
            pg.wait_for_timeout(200)
            im=np.asarray(Image.open(io.BytesIO(pg.screenshot(clip={'x':10,'y':10,'width':150,'height':60}))).convert('L')).astype(int)
            # le bord oblique : nombre de niveaux de gris distincts et hauteur des marches sur une colonne
            col=im[:, 200]; part=((im>10)&(im<245)).sum()
            print(ech, prop, 'pixels partiels', int(part), 'niveaux', len(set(im[(im>10)&(im<245)].tolist())))
            Image.fromarray(im[60:200,0:200].astype('uint8')).resize((800,560),Image.NEAREST).save('scratchpad/v170/clip-%s-%s.png'%(ech,prop))
    b.close()
