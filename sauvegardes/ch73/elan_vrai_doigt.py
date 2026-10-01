# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 73 · L'ÉLAN AU VRAI DOIGT, SOUS BRIDAGE — l'instrument qui ne ralentit pas avec la machine
# Les deux premiers instruments mentaient, chacun à sa façon, et il a fallu les deux pour le voir :
#   ① `mouse.move` de Playwright : ses mouvements arrivent à ~130 ms d'écart quand le fil est occupé —
#      CLAUDE §8 le dit déjà, « Playwright ne sait pas lancer ».
#   ② un lancer joué DANS la page : son pas vient de `setTimeout`, qui se dilate avec le bridage. Le DOIGT
#      ralentissait donc avec la machine, et la vitesse basse qu'on lisait était en partie honnête.
# ICI : `Input.dispatchMouseEvent` du CDP, avec un HORODATAGE EXPLICITE par mouvement, envoyés depuis le
# processus navigateur. Le doigt balaie 132 pt en 100 ms quel que soit le bridage — comme un vrai doigt — et
# c'est le navigateur qui décide de les regrouper, exactement comme sur un téléphone.
# ⚠ Ce que ça ne remplace toujours pas : un A13 (GPU, mémoire, chauffe), et Safari, qui n'a PAS
#   `getCoalescedEvents` — sur iOS l'app ne verra qu'un mouvement par appel, le cas le plus dur.
#   python3 elan_vrai_doigt.py [facteur ...]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys, time
from playwright.sync_api import sync_playwright
import os
URL = os.environ.get('APP') or 'http://127.0.0.1:8752/app.html'
FACTEURS = [float(x) for x in sys.argv[1:]] or [1, 4, 6, 10]
N_MOUV, DUREE = 7, 0.100
SANS_REGROUPEMENT = bool(os.environ.get('SANS_REGROUPEMENT'))      # 7 mouvements, 100 ms de balayage — la vitesse du doigt, constante

def passe(br, fac):
    pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    cdp = pg.context.new_cdp_session(pg)
    pg.goto(URL, timeout=300000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if SANS_REGROUPEMENT:
        # ⚑ LE CAS iOS. Safari n'a pas `getCoalescedEvents` : l'app y voit UN mouvement par appel, et rien
        #   d'autre. Chromium, lui, regroupe et rend le paquet avec les horodatages d'origine — il CACHE
        #   donc le cas le plus dur, celui du téléphone visé. On l'éteint pour le faire apparaître.
        pg.evaluate("()=>{ try{ PointerEvent.prototype.getCoalescedEvents=function(){ return []; }; }catch(e){} }")
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(120):
        pg.wait_for_timeout(250)
        e = pg.evaluate("()=>window._aura?_aura.etat():null")
        if e and e['pret'] and e['frames'] > 20: break
    pg.wait_for_timeout(1200)
    g = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return {cx:b.left+b.width/2, cy:b.top+b.height/2, sc:d.width/390};}")
    if fac > 1: cdp.send('Emulation.setCPUThrottlingRate', {'rate': fac})
    pg.wait_for_timeout(1500)
    x0, y0, dx = g['cx'] - 70 * g['sc'], g['cy'], 132 * g['sc']
    out = []
    for essai in range(3):
        for _ in range(80):
            if pg.evaluate("()=>{const e=_aura.etat(); return !e.vlac && !e.vtan && !e.emp;}"): break
            pg.wait_for_timeout(150)
        t0 = time.time()
        cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x0, 'y': y0,
                                              'button': 'left', 'buttons': 1, 'clickCount': 1, 'timestamp': t0})
        for k in range(1, N_MOUV + 1):
            u = k / float(N_MOUV)
            cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x0 + dx * u, 'y': y0,
                                                  'button': 'left', 'buttons': 1, 'timestamp': t0 + DUREE * u})
        cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x0 + dx, 'y': y0,
                                              'button': 'left', 'buttons': 0, 'clickCount': 1,
                                              'timestamp': t0 + DUREE + 0.004})
        # ⚠ ON LIT LA VITESSE **AU LÂCHER** (`elan.vlac`), PAS la vitesse courante : celle-ci a déjà
        #   décru (tau 0,55 s), et l'attente avant lecture se dilate avec le bridage — premier jeu de
        #   mesures jeté pour ça (3,70 à ×1 contre 0,47 à ×4 sur une géométrie IDENTIQUE : c'était la
        #   décroissance, pas l'élan).
        for _ in range(60):
            pg.wait_for_timeout(120)
            if pg.evaluate("()=>{const e=_aura.etat(); return !!(e.elan && e.elan.now);}"): break
        out.append(pg.evaluate("()=>{const e=_aura.etat(); return {vlac:(e.elan&&e.elan.vlac), elan:e.elan, ms:e.ms};}"))
        pg.wait_for_timeout(int(4000 * min(3, fac)))
    pg.context.close()
    return out

if __name__ == '__main__':
    print('══ %s ══%s\n   l’élan au lâcher · doigt CDP, 132 pt en 100 ms, horodatages explicites'
          % (URL, '  ·  SANS REGROUPEMENT (le cas iOS/Safari)' if SANS_REGROUPEMENT else ''))
    with sync_playwright() as p:
        br = p.chromium.launch()
        for fac in FACTEURS:
            L = passe(br, fac)
            v = [abs(x['vlac'] or 0) for x in L]
            print('   ×%-4g  vitesse au lâcher : %s rad/s  ·  médiane par image %s ms'
                  % (fac, ' / '.join('%.2f' % x for x in v), ' / '.join('%.0f' % (x['ms'] or 0) for x in L)))
            for x in L:
                e = x.get('elan') or {}
                print('         cadence %5s ms · fenêtre %5s ms · %s échantillon(s) · somme des pas %6s ms · attente %s ms'
                      % (e.get('cadence'), e.get('fenetre'), e.get('echant'), e.get('pas'), e.get('attente')))
            if max(v) < 1.0: print('        ⚠ ÉLAN PERDU à ×%g' % fac)
        br.close()
