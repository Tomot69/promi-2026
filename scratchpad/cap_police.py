# -*- coding: utf-8 -*-
"""LA HAUTEUR DE CAPITALE RENDUE, police chargée — deux polices à la même taille en px
   ne donnent PAS la même taille à l'œil."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    print(pg.evaluate(r"""async ()=>{ await document.fonts.ready;
      const out={};
      for(const ff of ['PromiLate','Gilbert','Fraunces','Atkinson']){
        const c=document.createElement('canvas'), g=c.getContext('2d');
        g.font='700 27px '+ff;
        const m=g.measureText('H');
        const m2=g.measureText('Réglages');
        out[ff]={cap:+( (m.actualBoundingBoxAscent+m.actualBoundingBoxDescent) ).toFixed(1),
                 larg:+m2.width.toFixed(1)};
      }
      return out;}"""))
    b.close()
