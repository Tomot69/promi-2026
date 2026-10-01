# L'élision suit-elle la frappe ? On tape un mot lettre par lettre dans la page + et on relit la phrase après chaque touche.
import sys
from playwright.sync_api import sync_playwright
MOT=([a for a in sys.argv[1:] if not a.startswith('--')] or ['aller voir la mer'])[0]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click();}"); pg.wait_for_timeout(1200)
    NAT=([a.split('=')[1] for a in sys.argv if a.startswith('--nat=')] or ['promi'])[0]
    pg.locator('[data-kind=%s]'%NAT).first.tap(); pg.wait_for_timeout(1500)
    info=pg.evaluate("()=>[...document.querySelectorAll('#csPhrase [data-ph]')].map(e=>e.dataset.ph+':'+e.textContent.trim())")
    print('pastilles', info)
    el=pg.locator('#csPhrase [data-ph=quoi], #csPhrase [data-ph=titre], #csPhrase [data-ph=parole]').first
    el.tap(); pg.wait_for_timeout(700)
    foc=pg.evaluate("()=>{const a=document.activeElement; return a?(a.id||a.className||a.tagName):null}")
    print('focus', foc)
    for i,c in enumerate(MOT):
        pg.keyboard.type(c); pg.wait_for_timeout(120)
        print(repr(MOT[:i+1]).ljust(14), pg.evaluate("()=>{const b=document.getElementById('csPhrase'); return b? b.textContent.replace(/\\s+/g,' ').trim().slice(0,70):null}"))
    pg.locator('#device').screenshot(path='sauvegardes/v46/elision.png')
    if '--efface' in sys.argv:
        for k in range(len(MOT)):
            pg.keyboard.press('Backspace'); pg.wait_for_timeout(100)
        pg.keyboard.type('b'); pg.wait_for_timeout(150)
        print('efface puis b :', pg.evaluate("()=>document.querySelector('#csPhrase .ph-li').textContent"))
    b.close()
