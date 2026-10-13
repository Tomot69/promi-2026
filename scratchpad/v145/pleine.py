#!/usr/bin/env python3
"""v145 (C-112, RÉCIDIVE) — LA TOILE REMPLIE COMME CELLE DE TOM : planter puis retirer une parole sur une Toile de 10, 25, 50 paroles (relue de la
sauvegarde, comme sur un téléphone), par banc_tom (WebKit 390 × 844 @3x). Chaque image et chaque rappel sont chronométrés.
usage : pleine.py [fichier] --mondes=encre,touffe,… --n=10,25,50 [--sombre] [--port=8752] [--sortie=nom]"""
import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
MONDES = arg('mondes', 'encre,touffe,mosaique,ritournelle,brouillamini').split(',')
NS = [int(x) for x in arg('n', '10,25,50').split(',')]
THEMES = [True] if '--sombre' in sys.argv else ([False, True] if '--deux' in sys.argv else [False])
PORT = arg('port', '8752'); SORTIE = arg('sortie', 'pleine'); CHARGE_MAX = float(arg('charge', '4'))
PROF = re.search(r'PROF = r"""(.*?)"""', io.open('redteam_evol.py', encoding='utf-8').read(), re.S).group(1)
def etat(n):
    st = json.load(io.open('scratchpad/v145/etats/etat-%d.json' % n, encoding='utf-8')); st.pop('promi_theme', None)
    return "try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st)
def releve(pg, duree=3500):
    r = pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice()})"); t0 = r['t0']
    I = [r['F'][i + 1] - r['F'][i] for i in range(len(r['F']) - 1) if t0 <= r['F'][i] <= t0 + duree]
    P = [(e[0] - t0, e[1], e[2], e[3]) for e in r['P'] if 0 <= e[0] - t0 <= duree]
    return I, P
def resume(I, P):
    mo = sorted(e[1] for e in P if 'image | frame' in e[2]); au = [e for e in P if 'image | frame' not in e[2] and not (e[0] < 60 and 'écouteur' in e[2])]
    pire = max(au, key=lambda e: e[1]) if au else (0, 0, '', 0)
    return {'images': len(I), 'sup20': sum(1 for x in I if x > 20), 'sup33': sum(1 for x in I if x > 33.4), 'pire': round(max(I or [0])), 'exces': round(sum(x - 16.7 for x in I if x > 20)),
            'moteur_n': len(mo), 'moteur_p50': round(mo[len(mo) // 2], 1) if mo else 0, 'moteur_p95': round(mo[min(len(mo) - 1, int(len(mo) * .95))], 1) if mo else 0, 'moteur_max': round(mo[-1], 1) if mo else 0,
            'moteur_somme': round(sum(mo)), 'autre_pire': round(pire[1], 1), 'autre_quoi': pire[2][:90], 'autre_t': round(pire[0]), 'autres': sorted([(round(e[1], 1), round(e[0]), e[2][:70]) for e in au if e[1] > 12], reverse=True)[:6]}
OUT = []
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in THEMES:
        for n in NS:
            for m in MONDES:
                import os, time
                t_att = time.time()
                while os.getloadavg()[0] > CHARGE_MAX and time.time() - t_att < 900: time.sleep(5)   # la machine est partagée (une autre session y lance des tests et un simulateur) : on attend le calme
                charge0 = os.getloadavg()[0]
                ctx = B.contexte(b, sombre=sombre); ctx.add_init_script(etat(n)); ctx.add_init_script(PROF)
                pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
                pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500)
                pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(4500)
                n0 = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
                if '--sans-minis' in sys.argv: pg.evaluate("()=>{ window.peintMinis=function(){}; }")
                # repos : la page sans rien faire, 2 s (le bruit du banc)
                pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); pg.wait_for_timeout(2200); Ir, Pr = releve(pg, 2000)
                pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
                pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
                pg.evaluate("()=>{document.getElementById('fTitle').value='tenir bon';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(3200)
                pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(4000)
                I, P = releve(pg); r1 = resume(I, P); n1 = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
                pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(3500)
                pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
                pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); B.tap_sel(pg, '.v16-oui'); pg.wait_for_timeout(4000)
                I2, P2 = releve(pg); r2 = resume(I2, P2); n2 = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
                charge1 = os.getloadavg()[0]
                ligne = {'charge': [round(charge0, 1), round(charge1, 1)], 'monde': m, 'n': n, 'sombre': sombre, 'ok': [n0, n1, n2], 'repos': {'sup20': sum(1 for x in Ir if x > 20), 'pire': round(max(Ir or [0]))}, 'planter': r1, 'retirer': r2, 'erreurs': pg.erreurs[:2]}
                OUT.append(ligne)
                for nom, r in (('planter', r1), ('retirer', r2)):
                    print('%-12s n=%2d %s %-7s | images %3d · >20 ms : %2d · >33 : %2d · pire %3d · excès %4d ms | moteur p50 %5.1f p95 %5.1f max %5.1f (%d img, %d ms) | autre %5.1f ms à %d (%s)' % (m, n, 'S' if sombre else 'C', nom, r['images'], r['sup20'], r['sup33'], r['pire'], r['exces'], r['moteur_p50'], r['moteur_p95'], r['moteur_max'], r['moteur_n'], r['moteur_somme'], r['autre_pire'], r['autre_t'], r['autre_quoi'][:60]), flush=True)
                if charge1 > CHARGE_MAX + 2: print('   ⚠ machine chargée pendant la mesure (charge %.1f → %.1f) : à refaire' % (charge0, charge1), flush=True)
                if [n0, n1, n2] != [n, n + 1, n] or pg.erreurs: print('   ⚠ comptes', [n0, n1, n2], pg.erreurs[:2], flush=True)
                ctx.close()
                io.open('scratchpad/v145/%s.json' % SORTIE, 'w', encoding='utf-8').write(json.dumps(OUT, ensure_ascii=False, indent=0))
    b.close()
