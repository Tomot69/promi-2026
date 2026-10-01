#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Colle le cadre du moodboard et la capture d'app côte à côte, avec une règle de cotes.
   Usage : python3 scratchpad/duo.py <nom> <theme>"""
import sys, os, base64
from playwright.sync_api import sync_playwright
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
nom=sys.argv[1]; th=sys.argv[2] if len(sys.argv)>2 else 'dark'
dossier=sys.argv[3] if len(sys.argv)>3 else 'scratchpad/s1b'
mb=os.path.join(R,'scratchpad/mb','%s_%s.png'%(nom,th))
ap=os.path.join(R,dossier,'%s_%s.png'%(nom,th))
out=os.path.join(R,'scratchpad/duo_%s_%s.png'%(nom,th))
def b64(p):
    return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
reperes=[36,110,190,270,350,418,484,538,592,668,760,844]
lignes=''.join('<div class="r" style="top:%dpx"><b>%d</b></div>'%(y,y) for y in reperes)
HTML="""<!doctype html><meta charset=utf-8><style>
body{margin:0;background:#0b0b0d;font:11px ui-monospace,monospace;color:#8a8a95}
.wrap{display:flex;gap:34px;padding:26px 26px 10px}
.col{position:relative;width:390px}
.col img{width:390px;height:844px;display:block;border-radius:36px}
.cap{padding:6px 0;color:#d8d8e0;font:12px ui-monospace}
.r{position:absolute;left:0;width:390px;height:0;border-top:1px dashed rgba(255,60,60,.55);pointer-events:none}
.r b{position:absolute;right:-30px;top:-7px;color:#ff6b6b;font-weight:400;font-size:10px}
</style><div class=wrap>
<div><div class=cap>MOODBOARD — %s / %s</div><div class=col><img src="%s">%s</div></div>
<div><div class=cap>APP</div><div class=col><img src="%s">%s</div></div>
</div>"""%(nom,th,b64(mb),lignes,b64(ap),lignes)
tmp=os.path.join(R,'scratchpad/_duo.html'); open(tmp,'w').write(HTML)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':920,'height':920}, device_scale_factor=2)
    pg.goto('file://'+tmp); pg.wait_for_timeout(600)
    pg.screenshot(path=out, full_page=True); b.close()
print(out)
