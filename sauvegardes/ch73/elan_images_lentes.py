# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 73 · LE CAS QUI SÉPARE LES DEUX VERSIONS : des mouvements ESPACÉS DE 200 ms
# Avec un doigt normal (7 mouvements en 100 ms), l'élan tient dans les deux versions, à ×1 comme à ×10 —
# le « 0,00 rad/s » du chantier était mon instrument (un lancer joué dans la page, dont le pas vient de
# `setTimeout` et se dilate avec le bridage), pas le produit.
# Reste le cas que la fenêtre figée à 90 ms ne peut pas traiter, et qui est celui d'un appareil vraiment
# lent : quand les images durent 200 ms, le doigt ne livre que DEUX mouvements, espacés de 200 ms. Le plus
# ancien tombe hors de la fenêtre, il ne reste qu'un instant — et un instant n'est pas une durée.
#   APP=<url> python3 elan_images_lentes.py [écart_ms ...]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import os, sys, time
from playwright.sync_api import sync_playwright
URL = os.environ.get('APP') or 'http://127.0.0.1:8752/app.html'
ECARTS = [float(x) for x in sys.argv[1:]] or [16, 60, 120, 200, 320]

def passe(br, ecart):
    pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    cdp = pg.context.new_cdp_session(pg)
    pg.goto(URL, timeout=300000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{ try{ PointerEvent.prototype.getCoalescedEvents=function(){ return []; }; }catch(e){} }")
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(120):
        pg.wait_for_timeout(250)
        e = pg.evaluate("()=>window._aura?_aura.etat():null")
        if e and e['pret'] and e['frames'] > 20: break
    pg.wait_for_timeout(1200)
    g = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return {cx:b.left+b.width/2, cy:b.top+b.height/2, sc:d.width/390};}")
    x0, y0, dx = g['cx'] - 70 * g['sc'], g['cy'], 132 * g['sc']
    out = []
    for essai in range(3):
        for _ in range(60):
            if pg.evaluate("()=>{const e=_aura.etat(); return !e.vlac && !e.vtan && !e.emp;}"): break
            pg.wait_for_timeout(150)
        t0 = time.time(); pas = ecart / 1000.0
        cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x0, 'y': y0,
                                              'button': 'left', 'buttons': 1, 'clickCount': 1, 'timestamp': t0})
        # le MÊME balayage, livré en mouvements espacés de `ecart` — c'est la cadence de l'appareil
        n = 2 if ecart >= 120 else max(2, int(round(100.0 / ecart)))
        for k in range(1, n + 1):
            u = k / float(n)
            cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x0 + dx * u, 'y': y0,
                                                  'button': 'left', 'buttons': 1, 'timestamp': t0 + pas * k})
            time.sleep(pas)
        cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x0 + dx, 'y': y0,
                                              'button': 'left', 'buttons': 0, 'clickCount': 1,
                                              'timestamp': t0 + pas * n + 0.004})
        for _ in range(50):
            pg.wait_for_timeout(120)
            if pg.evaluate("()=>{const e=_aura.etat(); return !!(e.elan && e.elan.now);}"): break
        out.append(pg.evaluate("()=>{const e=_aura.etat(); return {elan:e.elan};}"))
        pg.wait_for_timeout(2500)
    pg.context.close()
    return out, n

if __name__ == '__main__':
    print('══ %s ══  mouvements espacés (sans regroupement — le cas iOS)' % URL)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for ec in ECARTS:
            L, n = passe(br, ec)
            v = [abs((x['elan'] or {}).get('vlac') or 0) for x in L]
            e = L[-1]['elan'] or {}
            print('   écart %4.0f ms (%d mouvement(s))  vitesse au lâcher : %s rad/s   %s'
                  % (ec, n, ' / '.join('%.2f' % x for x in v),
                     '⚠ ÉLAN PERDU' if max(v) < 1.0 else ''))
            print('        fenêtre %s ms · %s échantillon(s) retenu(s) · somme des pas %s ms'
                  % (e.get('fenetre'), e.get('echant'), e.get('pas')))
        br.close()

# ═══ CE QUE LA FENÊTRE PROTÉGEAIT, et qu'on ne casse pas : UN DOIGT QUI S'ARRÊTE NE LANCE PAS ══════════════
# La fenêtre de 90 ms servait à ça. En la faisant suivre la cadence, on doit garder la protection : on
# balaie vite (16 ms entre les mouvements), on TIENT immobile, puis on lâche. L'élan doit être NUL.
def arret(url, tenues=(0, 120, 300, 600)):
    with sync_playwright() as p:
        br = p.chromium.launch()
        print('══ %s ══  un doigt qui s’ARRÊTE avant de lâcher' % url)
        for tenue in tenues:
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            cdp = pg.context.new_cdp_session(pg)
            pg.goto(url, timeout=300000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(120):
                pg.wait_for_timeout(250)
                e = pg.evaluate("()=>window._aura?_aura.etat():null")
                if e and e['pret'] and e['frames'] > 20: break
            pg.wait_for_timeout(1200)
            g = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return {cx:b.left+b.width/2, cy:b.top+b.height/2, sc:d.width/390};}")
            x0, y0, dx = g['cx'] - 70 * g['sc'], g['cy'], 132 * g['sc']
            t0 = time.time()
            cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x0, 'y': y0,
                                                  'button': 'left', 'buttons': 1, 'clickCount': 1, 'timestamp': t0})
            for k in range(1, 7):
                cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x0 + dx * k / 6.0, 'y': y0,
                                                      'button': 'left', 'buttons': 1, 'timestamp': t0 + 0.016 * k})
                time.sleep(0.016)
            time.sleep(tenue / 1000.0)
            cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x0 + dx, 'y': y0,
                                                  'button': 'left', 'buttons': 0, 'clickCount': 1,
                                                  'timestamp': t0 + 0.096 + tenue / 1000.0})
            for _ in range(50):
                pg.wait_for_timeout(120)
                if pg.evaluate("()=>{const e=_aura.etat(); return !!(e.elan && e.elan.now);}"): break
            e = (pg.evaluate("()=>_aura.etat().elan") or {})
            v = abs(e.get('vlac') or 0)
            attendu = 'un élan' if tenue < 90 else 'AUCUN élan'
            ok = (v > 1.0) if tenue < 90 else (v < 1.0)
            print('   immobile %4d ms avant le lâcher → %6.2f rad/s  (attendu : %s)  %s'
                  % (tenue, v, attendu, '✓' if ok else '✗ RATÉ'))
            pg.context.close()
        br.close()
