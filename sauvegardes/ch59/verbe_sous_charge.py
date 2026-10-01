# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 75 · LA PAGE + SOUS CHARGE — ce que le 3/6 mesurait vraiment
# `redteam_verbe` avait donné 3/6, les trois rouges en thème SOMBRE (`h=0`), et j'en avais fait un chantier
# « préexistant ». Machine au repos, QUATRE versions de l'app donnent 6/6, y compris celle que j'avais
# déclarée fautive (`app-avant-cercle-toile.html`) : le 3/6 mesurait LA MACHINE, pas le produit — le piège
# du §7, « un contrôle qui mesure une machine saturée ne mesure pas le produit ».
# Reste la vraie question : la page + rend-elle des hauteurs nulles quand le fil principal est saturé ?
# On la pose avec le SUBSTITUT déclaré — le bridage CPU du CDP — et non en saturant le Mac au hasard.
#   python3 verbe_sous_charge.py [facteur ...]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys, os
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
APP = 'file://' + os.path.join(ICI, '..', '..', 'app.html')
FACTEURS = [float(x) for x in sys.argv[1:]] or [1, 4, 6, 10]
VERBES = ('je promets', 'je me promets', 'promets-moi', 'promettez-moi', 'chiche')

def passe(b, theme, fac):
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    cdp = pg.context.new_cdp_session(pg)
    if fac > 1: cdp.send('Emulation.setCPUThrottlingRate', {'rate': fac})
    pg.goto(APP, timeout=300000); pg.wait_for_timeout(int(6800 * max(1, fac / 2)))
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.toggle('light', t==='light'))", theme)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(int(700 * fac))
    pg.evaluate("()=>{const t=document.querySelector('#createSheet .tile[data-kind=promi]');if(t)t.click();}")
    pg.wait_for_timeout(int(1100 * fac))
    r = pg.evaluate(r"""()=>{const pb=document.querySelector('#csPhrase .ph-b');
      if(!pb)return{f:0};const b=pb.getBoundingClientRect();const c=getComputedStyle(pb);
      return {f:1,h:b.height,txt:(pb.textContent||'').trim().toLowerCase(),
        vis:c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>0.1};}""")
    ok = bool(r.get('f') and r.get('vis') and r.get('h', 0) > 24 and any(v in r.get('txt', '') for v in VERBES))
    pg.evaluate("()=>{const a=document.getElementById('planterAlt');if(a)a.click();}"); pg.wait_for_timeout(int(400 * fac))
    cta = pg.evaluate(r"""()=>{const b=document.getElementById('addPromi');if(!b)return{f:0};
      const r=b.getBoundingClientRect();const c=getComputedStyle(b);
      return {f:1,h:Math.round(r.height),vis:c.display!=='none'&&c.visibility!=='hidden'};}""")
    ok2 = bool(cta.get('vis')) and cta.get('h', 0) > 24
    pg.close()
    return ok, r.get('h', 0), ok2, cta.get('h', 0)

if __name__ == '__main__':
    print('══ la page + sous bridage CPU · le verbe de la phrase et le bouton de la bascule ══')
    with sync_playwright() as p:
        b = p.chromium.launch()
        for fac in FACTEURS:
            for theme in ('light', 'dark'):
                ok, h, ok2, h2 = passe(b, theme, fac)
                print('   ×%-4g %-6s verbe %s (h %5.1f) · bouton %s (h %3s)'
                      % (fac, theme, 'OK ' if ok else 'KO ', h, 'OK ' if ok2 else 'KO ', h2))
        b.close()
