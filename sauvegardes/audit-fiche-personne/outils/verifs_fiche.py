# Les deux « à vérifier » de l'audit de la fiche de la personne (rien n'est modifié) :
#  1 · la forme floue (::before) BOUGE-t-elle ? (--gx/--gy/--grot et la transformation calculée, relevées sur 2 s)
#  2 · une rangée touchée AU DOIGT ouvre-t-elle la fiche de son Promi ? (et la fiche de la personne se ferme-t-elle ?)
#  3 · la graisse du nom : ce que la cascade demande, ce que lot-POLICES a posé en ligne
import sys, json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(sys.argv[1]); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); openPerson('Marion');}"); pg.wait_for_timeout(1500)
    rel = []
    for _ in range(5):
        rel.append(pg.evaluate("""()=>{ const sh=document.getElementById('personSheet'), c=getComputedStyle(sh), a=getComputedStyle(sh,'::before');
            return [c.getPropertyValue('--gx').trim(), c.getPropertyValue('--gy').trim(), c.getPropertyValue('--grot').trim(), a.transform]; }"""))
        pg.wait_for_timeout(500)
    print('1 · la forme, toutes les 0,5 s :', json.dumps(rel))
    print('3 · le nom :', pg.evaluate("""()=>{ const n=document.getElementById('psName'), c=getComputedStyle(n);
        return JSON.stringify({ff:c.fontFamily, fw:c.fontWeight, inline:n.getAttribute('style'), faces:[...document.fonts].filter(f=>/Bricolage/i.test(f.family)).map(f=>f.weight+'/'+f.status)}); }"""))
    dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width];}")
    row = pg.evaluate("""()=>{ const r=document.querySelector('#personSheet #psList .row'); const b=r.getBoundingClientRect(); return {id:r.getAttribute('data-id'), x:b.left+b.width/2, y:b.top+b.height/2, titre:r.textContent.slice(0,30)}; }""")
    pg.mouse.click(row['x'], row['y']); pg.wait_for_timeout(1500)
    print('2 · rangée touchée :', json.dumps(row, ensure_ascii=False), '→', pg.evaluate("""()=>JSON.stringify({fichePersonne:document.getElementById('personSheet').classList.contains('show'),
        detail:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean), titre:((document.querySelector('#detailPoster h1, #detailPoster .dp-title, #dTitle')||{}).textContent||'').slice(0,40)})"""))
    b.close()
