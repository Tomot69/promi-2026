# Developpement : injecte le bloc dans la VRAIE app (app.html intact), ouvre l'Aura,
# capture les deux themes a 2x, et rend l'etat publie.
import sys, os, io, json, subprocess
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['python3', os.path.join(ICI, 'fabrique.py')], check=True, capture_output=True)
CSS = io.open(os.path.join(ICI, 'aura.css'), encoding='utf-8').read()
MOT = io.open(os.path.join(ICI, 'moteur.js'), encoding='utf-8').read()
JS = io.open(os.path.join(ICI, 'aura.js'), encoding='utf-8').read()
SUF = sys.argv[1] if len(sys.argv) > 1 else ''
THROTTLE = float(os.environ.get('THR', '0'))

def injecte(pg):
    pg.add_style_tag(content=CSS)
    pg.add_script_tag(content=MOT)
    pg.add_script_tag(content=JS)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    injecte(pg)
    if THROTTLE:
        cdp = pg.context.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate', {'rate': THROTTLE})
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}")
        for _ in range(60):
            pg.wait_for_timeout(250)
            e = pg.evaluate("()=>window._aura&&_aura.etat()")
            if e and e['pret'] and e['frames'] > 20: break
        pg.wait_for_timeout(800)
        e = pg.evaluate("()=>window._aura&&_aura.etat()")
        comp = pg.evaluate("()=>window._auraComp")
        cov = pg.evaluate("""()=>[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show')].map(x=>x.id||x.className)""")
        print(th, 'ETAT', json.dumps(e)[:600])
        print(th, 'COMP', json.dumps(comp, ensure_ascii=False)[:900])
        print(th, 'SHOW', cov)
        pg.query_selector('#device').screenshot(path=os.path.join(ICI, 'dev_%s%s.png' % (th, SUF)))
    print('ERREURS', er[:4])
    b.close()
