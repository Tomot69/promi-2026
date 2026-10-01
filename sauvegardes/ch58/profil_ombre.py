# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 58 · LE PROFIL — la part du fil principal que prend l'ombre de dalle, écran par écran
# Le chantier demandait « un profil avant/après sur l'accueil (Toile), le Fil et l'Index ». On échantillonne
# le profileur du CDP à 0,5 ms, 8 s par écran, et on additionne le temps PROPRE des images de `frame` — plus
# le temps de mise en page, qui au profileur est attribué à la fonction qui LIT (§8), donc à `frame` elle-même.
#   python3 profil_ombre.py <url>
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys, collections
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
ECRANS = [('l’accueil (Toile)', "()=>{}"),
          ('le Fil',            "()=>{const b=document.getElementById('feedBtn')||document.getElementById('filBtn'); if(b)b.click();}"),
          ('l’Index',           "()=>{const b=document.getElementById('indexBtn'); if(b)b.click();}"),
          ('les Réglages',      "()=>document.getElementById('settingsBtn').click()"),
          ('l’Aura',            "()=>document.getElementById('souffleBtn').click()")]

def part(prof):
    """la part du temps échantillonné passée dans `frame` et dans ce qu'elle déclenche"""
    noeuds = {n['id']: n for n in prof['nodes']}
    propre = collections.Counter()
    for sid in prof['samples']: propre[sid] += 1
    tot = sum(propre.values()) or 1
    ombre, mep = 0, 0
    for nid, n in propre.items():
        cf = noeuds.get(nid, {}).get('callFrame', {})
        nom = cf.get('functionName', '')
        if nom == 'frame': ombre += n
        if nom in ('(program)',): mep += 0
    return 100.0 * ombre / tot, tot

if __name__ == '__main__':
    print('══ %s ══  part du fil principal passée dans `frame` (l’ombre de dalle)' % URL)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=180000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        cdp = pg.context.new_cdp_session(pg)
        cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500})
        for nom, js in ECRANS:
            pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.sheet.show,.poster.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(400)
            try: pg.evaluate(js)
            except Exception: pass
            pg.wait_for_timeout(2500)
            cdp.send('Profiler.start'); pg.wait_for_timeout(8000)
            prof = cdp.send('Profiler.stop')['profile']
            pc, n = part(prof)
            print('   %-20s `frame` : %5.2f %% du fil  (%d échantillons)' % (nom, pc, n))
        br.close()
