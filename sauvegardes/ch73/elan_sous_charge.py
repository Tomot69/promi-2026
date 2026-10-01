# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 73 · L'ÉLAN SUR UN APPAREIL LENT — le juge ou le produit ?
# Le chantier disait : « quand la médiane par image dépasse ~24 ms et que la plus longue image pendant l'élan
# atteint 83–100 ms, la vitesse au lâcher sort à 0,00 rad/s. Soit le juge ne sait plus lancer sous charge,
# soit le produit perd l'élan sur un appareil lent. Non tranché. »
# Ici on tranche la part qu'on peut trancher sans téléphone : le lancer est joué DANS LA PAGE, cadencé
# (CLAUDE §8 : « Playwright ne sait pas lancer »), et on bride le CPU par le CDP — ×1, ×4, ×6, ×10.
#
# ⚠ CE QUE CE SUBSTITUT NE REPRODUIT PAS, et il faut le dire :
#   · LE REGROUPEMENT DES ÉVÉNEMENTS. Sur un vrai téléphone, le navigateur regroupe les `pointermove` et les
#     livre en paquet APRÈS une image lente, chacun gardant son horodatage d'origine — c'est pour ça que le
#     produit lit `e.timeStamp` et `e.getCoalescedEvents()`. Un événement synthétique a un `timeStamp` en
#     LECTURE SEULE, posé à l'instant du dispatch : on ne peut pas fabriquer un paquet tardif. Ce test mesure
#     donc l'autre moitié du risque — des mouvements ESPACÉS parce que les images sont lentes.
#   · le GPU, la mémoire et la chauffe d'un A13. Le bridage ne ralentit que le fil principal.
#   python3 elan_sous_charge.py [facteur ...]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
FACTEURS = [float(x) for x in sys.argv[1:]] or [1, 4, 6, 10]
# ⚑ À VITESSE DE DOIGT CONSTANTE. Premier jeu de mesures, jeté : le lancer était « 6 mouvements espacés de
#   16 ms », or `setTimeout(16)` devient 58 à 148 ms sous bridage — le DOIGT ralentissait avec la machine, et
#   la vitesse basse qu'on lisait était en partie juste. Un vrai doigt balaie la même distance dans le même
#   temps RÉEL, quel que soit le processeur ; ce qui change, c'est le NOMBRE de mouvements qu'il reçoit. On
#   fixe donc la durée (`DUREE` ms) et le balayage, et on dispatche à chaque tick ce que l'horloge permet.
LANCE_V = r"""async ([x0,y0,dx,duree])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  const av=_aura.etat(), t0=performance.now();
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  let n=0, u=0;
  while(u<1){ await new Promise(r=>setTimeout(r,8));
    u=Math.min(1,(performance.now()-t0)/duree);
    t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*u))); n++; }
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx)));
  const ap=_aura.etat();
  return {vlac:ap.vlac, elan:ap.elan, ms:ap.ms, mouvements:n,
          balaye:+(performance.now()-t0).toFixed(0)}; }"""
LANCE = r"""async ([x0,y0,dx,n,pas])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  const av=_aura.etat();
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  for(let k=1;k<=n;k++){ await new Promise(r=>setTimeout(r,pas)); t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*k/n))); }
  const t1=performance.now();
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx)));
  const ap=_aura.etat();
  return {vlac:ap.vlac, elan:ap.elan, ms:ap.ms, dtReel:ap.dtReel, images:ap.frames-av.frames,
          duree:+(t1-0).toFixed(0)}; }"""

def passe(br, fac):
    pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    cdp = pg.context.new_cdp_session(pg)
    pg.goto(URL, timeout=300000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(120):
        pg.wait_for_timeout(250)
        e = pg.evaluate("()=>window._aura?_aura.etat():null")
        if e and e['pret'] and e['frames'] > 20: break
    pg.wait_for_timeout(1200)
    r = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return {cx:b.left+b.width/2, cy:b.top+b.height/2, sc:d.width/390};}")
    # le bridage n'entre en jeu qu'APRÈS le bâti : on mesure le geste, pas l'ouverture
    if fac > 1: cdp.send('Emulation.setCPUThrottlingRate', {'rate': fac})
    pg.wait_for_timeout(1500)
    out = []
    for essai in range(3):
        for _ in range(80):
            if pg.evaluate("()=>{const e=_aura.etat(); return !e.vlac && !e.vtan && !e.emp;}"): break
            pg.wait_for_timeout(150)
        out.append(pg.evaluate(LANCE_V, [r['cx'] - 70 * r['sc'], r['cy'], 132 * r['sc'], 100]))
        pg.wait_for_timeout(int(4000 * min(3, fac)))
    pg.context.close()
    return out

if __name__ == '__main__':
    print('══ l’élan au lâcher, sous bridage CPU · lancer joué DANS la page, 6 mouvements cadencés ══')
    with sync_playwright() as p:
        br = p.chromium.launch()
        for fac in FACTEURS:
            L = passe(br, fac)
            v = [abs(x['vlac'] or 0) for x in L]
            print('   ×%-4g  vitesse au lâcher : %s rad/s  ·  balayage %s ms en %s mouvement(s)  ·  médiane par image %s ms'
                  % (fac, ' / '.join('%.2f' % x for x in v),
                     ' / '.join(str(x['balaye']) for x in L), ' / '.join(str(x['mouvements']) for x in L),
                     ' / '.join('%.0f' % (x['ms'] or 0) for x in L)))
            e = L[-1].get('elan') or {}
            print('         dernier essai : cadence %s ms · fenêtre %s ms · %s échantillon(s) · attente avant le lâcher %s ms'
                  % (e.get('cadence'), e.get('fenetre'), e.get('echant'), e.get('attente')))
            if max(v) < 1.0: print('        ⚠ ÉLAN PERDU à ×%g — la vitesse au lâcher tombe sous 1 rad/s' % fac)
        br.close()
