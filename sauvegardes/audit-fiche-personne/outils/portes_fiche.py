# Audit « comme pour le partage » : les PORTES de la fiche de la personne (qui l'ouvre, et cette porte est-elle
# visible au doigt ?) et ses COMMANDES (chaque chose touchable dans la fiche, touchée au doigt). Rien n'est modifié.
import sys, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1]
def page(b, theme='dark'):
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    return pg
VIS = r"""(sel)=>{ const dv=document.getElementById('device').getBoundingClientRect();
  return [...document.querySelectorAll(sel)].map(e=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e);
    const vu=r.width>2&&r.height>2&&c.visibility!=='hidden'&&c.display!=='none'&&r.right>dv.left&&r.left<dv.right&&r.bottom>dv.top&&r.top<dv.bottom;
    let doigt=false; if(vu){ const x=Math.min(Math.max(r.left+r.width/2,dv.left+1),dv.right-1), y=Math.min(Math.max(r.top+r.height/2,dv.top+1),dv.bottom-1); const h=document.elementFromPoint(x,y); doigt=!!(h&&(h===e||e.contains(h))); }
    return {vu:vu, doigt:doigt, p:e.getAttribute('data-p')||'', txt:(e.textContent||'').trim().slice(0,20)}; }); }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    # ── LES PORTES : les appelants d'openPerson (recensés dans le code) et leur hôte à l'écran
    pg = page(b)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(2500)
    for sel in ['#auraScreen .au-n', '#ktoile', '#ksocial', '#kpers', '#ktoile [data-p]', '#ksocial [data-p]', '#kpers [data-p]']:
        print('AURA  %-22s' % sel, json.dumps(pg.evaluate(VIS, sel), ensure_ascii=False)[:230])
    pg.close()
    pg = page(b)
    res = pg.evaluate("""async ()=>{ const out=[]; for(const p of promises.filter(p=>!p.draft).slice(0,30)){ closeAll(); openDetail(p.id); await new Promise(r=>setTimeout(r,600));
        const k=[...document.querySelectorAll('.kring[data-p], #dAura .kring')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>2;});
        if(k.length) out.push(p.id+':'+k.map(e=>e.getAttribute('data-p')||'?').join('/')); } return out; }""")
    print('FICHES avec un disque de personne visible :', len(res), res[:12])
    pg.close()
    # ── LES COMMANDES : dans la fiche de Marion, chaque chose touchable, touchée
    cmds = [('✕ FERMER', '#personSheet .closeb'), ('la poignée', '#personSheet .grip'), ('le visage', '#psAva'), ('le nom', '#psName'),
            ('l\'anneau', '#personSheet .kr-c'), ('la courbe', '#personSheet svg'), ('la légende', '#personSheet .ps-leg3'), ('une rangée', '#psList .row')]
    for nom, sel in cmds:
        pg = page(b); pg.evaluate("()=>{closeAll(); openPerson('Marion');}"); pg.wait_for_timeout(1400)
        v = pg.evaluate(VIS, sel)
        if not v or not v[0]['vu']: print('CMD   %-12s absent ou invisible %s' % (nom, v[:1])); pg.close(); continue
        box = pg.evaluate("(s)=>{const r=document.querySelector(s).getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];}", sel)
        av = pg.evaluate("()=>[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')")
        pg.mouse.click(box[0], box[1]); pg.wait_for_timeout(1200)
        ap = pg.evaluate("()=>[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')")
        cur = pg.evaluate("(s)=>getComputedStyle(document.querySelector(s)).cursor", sel) if pg.evaluate("(s)=>!!document.querySelector(s)", sel) else '?'
        print('CMD   %-12s au doigt %s · curseur %s · avant [%s] → après [%s]' % (nom, v[0]['doigt'], cur, av, ap)); pg.close()
    # ── le glissé vers le bas sur la poignée / la fiche (fermer d'un geste ?)
    pg = page(b); pg.evaluate("()=>{closeAll(); openPerson('Marion');}"); pg.wait_for_timeout(1400)
    dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    x, y0, s = dv[0] + 195 * dv[2], dv[1] + 30 * dv[2], dv[2]
    pg.mouse.move(x, y0); pg.mouse.down()
    for i in range(1, 16): pg.mouse.move(x, y0 + i * 25 * s); pg.wait_for_timeout(16)
    pg.mouse.up(); pg.wait_for_timeout(1200)
    print('GESTE glisser vers le bas depuis le haut → fiche ouverte :', pg.evaluate("()=>document.getElementById('personSheet').classList.contains('show')"))
    pg.close(); b.close()
