# CHANTIER 69 — de bout en bout : sur la page +, on choisit un pinceau, on plante ; le Promi né garde son trait, et sa fiche le montre.
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
KO = []
def ok(nom, c, d):
    print('   %s %s  %s' % ('✓' if c else '✗', nom, d))
    if not c: KO.append(nom)
with sync_playwright() as p:
    br = p.chromium.launch()
    for th, choix in (('dark', 1), ('light', 2)):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.evaluate("()=>document.getElementById('createBtn').click()")
        for i in range(15):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-choix')"): break
        for e in range(5):
            pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(700)
            if pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('pp-choix')"): break
        # le pinceau : un toucher sur une pastille de la rangée de la page + (au point, comme un doigt)
        # ⚠ le toucher sur la pastille ne prenait pas toujours : on relève CE QUI EST SOUS LE DOIGT avant de toucher, on réessaie,
        #   et on nomme l'intercepteur — si quelque chose recouvre les pastilles, c'est un défaut du PRODUIT (chantier 62 ?)
        essais = []
        for e in range(3):
            pt = pg.evaluate("""(k)=>{ const b=[...document.querySelectorAll('#csPinceau .pc-t')][k]; if(!b) return null; b.scrollIntoView({block:'nearest', inline:'nearest'});
                const r=b.getBoundingClientRect(); const x=r.left+r.width/2, y=r.top+r.height/2; const h=document.elementFromPoint(x,y);
                return {x, y, t:b.getAttribute('data-t'), sous:(h&&(h===b||b.contains(h)))?'la pastille':(h?((h.id?'#'+h.id:'')+'.'+String(h.className).split(' ').slice(0,2).join('.')+' « '+(h.textContent||'').trim().slice(0,24)+' »'):'rien')}; }""", choix)
            if not pt: break
            pg.wait_for_timeout(250); pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(500)
            pris = pg.evaluate("()=>window._ppPinceau || null"); essais.append((pt['sous'], pris))
            if pris == pt['t']: break
        choisi = pg.evaluate("()=>window._ppPinceau || null")
        ok('%s · le toucher sur la pastille « %s » est pris (sous le doigt : la pastille)' % (th, pt and pt['t']), choisi == (pt and pt['t']) and essais and essais[0][0] == 'la pastille', essais)
        # on plante (le geste mène à #addPromi — CLAUDE §8) avec une phrase
        avant = pg.evaluate("()=>Math.max(...promises.map(q=>q.id))")
        pg.evaluate("()=>{ window._phrase=Object.assign({}, window._phrase||{}, {sens:'faire', qui:'Moi', titre:'essayer le pinceau', quand:'un jour'}); const f=document.getElementById('fTitle'); if(f) f.value='essayer le pinceau'; if(window._phraseRendu) _phraseRendu(); }")
        pg.wait_for_timeout(300); pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(900)
        ne = pg.evaluate("(a)=>{ const n=promises.filter(q=>q.id>a); return n.map(q=>({id:q.id, titre:q.title, trait:q.trait||null})); }", avant)
        ok('%s · le Promi planté porte le pinceau choisi (« %s »)' % (th, pt and pt['t']), len(ne) == 1 and ne[0]['trait'] == (pt and pt['t']) == choisi, (choisi, ne))
        if ne:
            pg.evaluate(BASE); pg.evaluate("(i)=>openDetail(i)", ne[0]['id']); pg.wait_for_timeout(1400)
            pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
            v = pg.evaluate("()=>{ const r=document.getElementById('dpTraitReg'); return r ? (r.querySelector('.s2-val')||{}).textContent : null; }")
            ok('%s · sa fiche, rouverte, montre ce trait dans Peaufiner (LE TRAIT)' % th, v == (pt and pt['t']), v)
        pg.context.close()
    br.close()
print('══ %d raté(s)' % len(KO)); [print('   ✗ ' + k) for k in KO]
