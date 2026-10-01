# Halin en haute définition (×3), au repos, deux thèmes : planche de 6 morceaux par thème.
import io, base64, sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ['dark','light']:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=3,color_scheme=th)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); Toile.setTheme('halin');}", 'light' if th=='light' else 'dark')
        pg.wait_for_timeout(4000)
        u=pg.evaluate("()=>document.getElementById('toileCv').toDataURL('image/png')")
        im=Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'); im.save('hal_hd_%s.png'%th)
        w,h=im.size; print(th,w,h)
        pg.close()
    b.close()
