# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 58 · « UN ÉCRAN EST VISIBLE S'IL PORTE .show » — on le VÉRIFIE avant de s'en servir
# La boucle `frame()` tient pour visible tout élément dont `offsetParent` n'est pas nul. La parade du §8 est
# la classe `.show`. Avant de changer la boucle, on vérifie que les deux coïncident sur les nœuds qu'elle
# touche, écran par écran, dans les deux thèmes : un faux négatif éteindrait l'ombre sur un écran VISIBLE.
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
SEL = '.tuto-fond, #createSheet, #settingsScreen'
ETAT = r"""([SEL])=>{
  const dv=document.getElementById('device').getBoundingClientRect();
  return [...document.querySelectorAll(SEL)].map(e=>{
    const r=e.getBoundingClientRect();
    /* « vraiment vu » : il est dans l'appareil, il a une surface, et il n'est pas transparent */
    const k=getComputedStyle(e), dedans=(r.bottom>dv.top+4 && r.top<dv.bottom-4 && r.width>8 && r.height>8);
    return {id:e.id||('.'+e.className.split(' ')[0]), show:e.classList.contains('show'),
            off:!!e.offsetParent, vu:dedans && +k.opacity>0.05 && k.visibility!=='hidden' && k.display!=='none',
            op:+(+k.opacity).toFixed(2), y:Math.round(r.top-dv.top)};
  }); }"""
PORTES = [
    ('rien (accueil)',   "()=>{}"),
    ('la page +',        "()=>document.getElementById('createBtn').click()"),
    ('les Réglages',     "()=>document.getElementById('settingsBtn').click()"),
    ('le Fil',           "()=>{const b=document.getElementById('feedBtn')||document.getElementById('filBtn'); if(b)b.click();}"),
    ('l’Index',          "()=>{const b=document.getElementById('indexBtn'); if(b)b.click();}"),
    ('l’Aura',           "()=>document.getElementById('souffleBtn').click()"),
    ('le Cercle',        "()=>{const b=document.getElementById('cercleTopBtn'); if(b)b.click();}"),
    ('le partage',       "()=>{const b=document.getElementById('shareBtn'); if(b)b.click();}"),
]
if __name__ == '__main__':
    print('══ .show contre offsetParent, sur les nœuds que `frame()` touche ══')
    dis = 0
    with sync_playwright() as p:
        br = p.chromium.launch()
        for th in ('dark', 'light'):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(URL, timeout=180000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1200)
            for nom, js in PORTES:
                pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.sheet.show,.poster.show').forEach(s=>s.classList.remove('show'));}")
                pg.wait_for_timeout(350)
                try: pg.evaluate(js)
                except Exception: pass
                pg.wait_for_timeout(1400)
                E = pg.evaluate(ETAT, [SEL])
                mauvais = [e for e in E if e['show'] != e['vu']]
                offtrop = [e for e in E if e['off'] and not e['vu']]
                dis += len(mauvais)
                print('   %-6s %-16s %2d nœud(s) · .show==vu partout : %s%s · offsetParent vrai mais PAS vu : %d'
                      % (th, nom, len(E), 'oui' if not mauvais else 'NON',
                         '' if not mauvais else ' → ' + ', '.join('%s(show=%s vu=%s op=%s y=%s)' % (m['id'], m['show'], m['vu'], m['op'], m['y']) for m in mauvais[:3]),
                         len(offtrop)))
            pg.context.close()
        br.close()
    print()
    print('   %s' % ('✅  .show et « vraiment vu » coïncident partout : la parade du §8 est sûre.' if not dis
                     else '❌  %d désaccord(s) : la parade éteindrait l’ombre sur un écran visible.' % dis))
