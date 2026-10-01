# -*- coding: utf-8 -*-
"""L'AIR À L'ENCRE — sur l'image RENDUE (§7, famille 9 : aux boîtes ET à l'encre).
   On découpe la bande entre le bas des prénoms et le haut de « CE QUE TU AS TENU »,
   et on cherche les lignes d'encre réelles."""
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
SUF = sys.argv[2] if len(sys.argv)>2 else ''
BOX=r"""()=>{var dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
 function b(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();
  return {y:(r.top-dv.top)/sc,b:(r.bottom-dv.top)/sc};}
 var bas=-1; document.querySelectorAll('#auraScreen .au-lb').forEach(function(e){
   var r=e.getBoundingClientRect(); var v=(r.bottom-dv.top)/sc; if(v>bas) bas=v;});
 var lg=b('#auraScreen .au-lg'), mo=b('#auraScreen .au-mo h3');
 return {basPrenoms:bas, lg:lg, mo:mo, sc:sc, dx:dv.left, dy:dv.top};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    for theme in ('sombre','clair'):
        pg.goto(URL); pg.wait_for_timeout(6300)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>{var d=document.getElementById('device');d.classList.toggle('light',t==='clair');document.querySelectorAll('.frame').forEach(f=>f.classList.toggle('light',t==='clair'));}",theme)
        pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(3800)
        m=pg.evaluate(BOX)
        pg.locator('#device').screenshot(path='cap/aura-bande-%s%s.png'%(theme,SUF))
        im=Image.open('cap/aura-bande-%s%s.png'%(theme,SUF)).convert('RGB')
        k=im.width/390.0
        y0=int((m['basPrenoms']-16)*k); y1=int((m['mo']['b']+6)*k)
        px=im.load()
        fond=px[int(6*k), int((m['basPrenoms']+14)*k)]   # un point sûrement vide
        lignes=[]
        for y in range(max(0,y0), min(im.height,y1)):
            n=0
            for x in range(int(24*k), int(366*k), 2):
                c=px[x,y]
                if abs(c[0]-fond[0])+abs(c[1]-fond[1])+abs(c[2]-fond[2])>40: n+=1
            lignes.append((y/k, n))
        # regrouper en blocs d'encre
        blocs=[]; cur=None
        for yy,n in lignes:
            if n>0:
                if cur is None: cur=[yy,yy]
                else: cur[1]=yy
            else:
                if cur is not None and cur[1]-cur[0]>=1.5: blocs.append(tuple(cur))
                cur=None
        if cur is not None and cur[1]-cur[0]>=1.5: blocs.append(tuple(cur))
        print('══ %s ══  blocs d\'encre trouvés : %s'%(theme, ' · '.join('%.1f→%.1f'%b for b in blocs)))
        if len(blocs)>=3:
            pre, leg, mo = blocs[0], blocs[1], blocs[2]
            h=leg[0]-pre[1]; bb=mo[0]-leg[1]
            print('    à l\'encre : AU-DESSUS %.2f · EN DESSOUS %.2f   → écart %.2f  %s'
                  %(h,bb,abs(h-bb), 'ÉGAL' if abs(h-bb)<2 else '✗'))
        elif len(blocs)==2:
            print('    (deux blocs seulement — la légende touche un voisin ?)')
    b.close()
