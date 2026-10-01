# Capture de la Toile d'un monde (accueil), sombre et clair. python3 toile.py monde [--n=18]
import sys
from playwright.sync_api import sync_playwright
PAL=([a.split('=')[1] for a in sys.argv if a.startswith('--pal=')] or [''])[0]; M=sys.argv[1]; N=int(([a.split('=')[1] for a in sys.argv if a.startswith('--n=')] or ['0'])[0])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ['dark','light']:
        pg.evaluate("async(a)=>{ setTheme(a.th); Toile.setTheme(a.m); if(a.pal) Toile.setPalette(a.pal); if(a.n){ const ids=promises.filter(p=>!p.draft).map(p=>p.id); Toile.sync(ids.slice(0,a.n)); } await new Promise(r=>setTimeout(r,3500)); }", {'m':M,'th':th,'n':N,'pal':PAL})
        pg.locator('#device').screenshot(path='toile_%s_%s%s%s.png'%(M,th,'_%d'%N if N else '',PAL))
    print('erreurs', er[:3])
    b.close()
