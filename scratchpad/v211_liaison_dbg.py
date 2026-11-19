import sys, re; sys.path.insert(0, '.')
import os
FF=os.environ.get('FF','app.html'); sys.argv=['x']
src=open('redteam_liaison.py',encoding='utf-8').read()
exec(src.split('with sync_playwright() as p:')[0])
REC2 = REC.replace("window.__fr.push([t, cp===", "window.__fr.push([Math.round(performance.now()), document.querySelectorAll(sel).length, (e.__nid=e.__nid||(window.__nn=(window.__nn||0)+1)), ink, cp.slice(0,20), t, cp===")
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); ctx.add_init_script(CLAV)
    pg = B.ouvre(ctx, FF)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
    B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500)
    for i, mot in enumerate(['aller', 'écrire', 'Être']):
        if i == 2: pg.evaluate(REC2, '#csPhrase .ph-li')
        pg.keyboard.type(mot, delay=45); pg.wait_for_timeout(1500)
        for _ in range(len(mot)): pg.keyboard.press('Backspace'); pg.wait_for_timeout(40)
        pg.wait_for_timeout(1500)
    pg.evaluate("()=>__frStop()"); fr = pg.evaluate("()=>__fr"); prev=None
    for x in fr:
        k=str(x[1:])
        if k!=prev: print(x); prev=k
    b.close()
