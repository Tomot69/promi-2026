# LES PIÈCES RÉELLES pour les partis de l'écran qui vend (Tom, 12 sept.) : rien de dessiné à la main.
#   1 · le TRAIT, ses deux modes : la moitié donnée (Promi) et le trait ENTIER (Nuée, mode complet du §2.6)
#   2 · les ANNEAUX de la rangée d'une fiche : le tien et celui d'une personne
#   3 · les QUATRE RANGÉES du mur, floutées, SANS son encart (il ne mènerait nulle part sur cet écran)
#   4 · les trois dalles des mondes payants, peintes par le moteur (comme l'écran qui vend)
# On note aussi tout CHIFFRE visible dans ces pièces : « on voit quoi, jamais combien ».
import base64, json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'partis')
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
CHIFFRES = r"""(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const out=[]; const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n;
  while((n=w.nextNode())){ const t=n.textContent.trim(); if(t && /[0-9]/.test(t) && n.parentElement.checkVisibility()) out.push(t.slice(0,30)); } return out; }"""
R = {}
def prends(pg, nom, sel, marge=0):
    m = pg.evaluate("""([s,g])=>{ const e=document.querySelector(s); if(!e) return null; e.scrollIntoView({block:'center'});
        const r=e.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
        return {x:r.left-g, y:r.top-g, width:r.width+2*g, height:r.height+2*g, w390:+(r.width/sc).toFixed(1), h390:+(r.height/sc).toFixed(1)}; }""", [sel, marge])
    if not m or m['width'] < 4 or m['height'] < 4: print('   ⚠ pièce absente ou vide :', nom, sel, m and [m['w390'], m['h390']]); return
    pg.wait_for_timeout(250)
    png = pg.screenshot(clip={k: m[k] for k in ('x', 'y', 'width', 'height')})
    open(os.path.join(OUT, nom + '.png'), 'wb').write(png)
    R[nom] = {'cotes390': [m['w390'], m['h390']], 'chiffres': pg.evaluate(CHIFFRES, sel)}
    print('   %-28s %sx%s  chiffres : %s' % (nom, m['w390'], m['h390'], R[nom]['chiffres']))
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        print('══', th)
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        # 1 · le trait d'un Promi (moitié donnée) et sa rangée d'anneaux
        pg.evaluate(BASE); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee); openDetail(p.id); }"); pg.wait_for_timeout(1800)
        prends(pg, '%s_trait_moitie' % th, '#tenirZone')
        prends(pg, '%s_anneaux' % th, '#dAura')
        # 3 · les quatre rangées du mur, floutées, sans l'encart
        pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1800)
        pg.evaluate("""()=>{ const b=document.querySelector('#detailPoster .s2-cercle'); if(!b) return; const e=b.querySelector('.s2-encart');
            if(e) e.style.setProperty('visibility','hidden','important'); b.setAttribute('data-partis','1'); }""")
        prends(pg, '%s_mur_rangees' % th, '#detailPoster .s2-cercle')
        # 2 bis · le trait ENTIER : celui d'une Nuée (mode complet)
        pg.evaluate(BASE); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1800)
        prends(pg, '%s_trait_entier' % th, '#tenirZone')
        # 4 · les trois dalles des mondes payants
        for w in ('sillons', 'gravure', 'terrazzo'):
            u = pg.evaluate("""(w)=>{ const id=promises.filter(q=>!q.draft&&!q.req).map(q=>q.id).sort((a,b)=>b-a)[0]; const c=document.createElement('canvas');
                const mo=Object.assign({}, Toile.mondeCourant(), {m:w}); if(!Toile.dalleTrame(c,id,1,mo)||!c.width) return null; return c.toDataURL('image/png'); }""", w)
            if u: open(os.path.join(OUT, '%s_dalle_%s.png' % (th, w)), 'wb').write(base64.b64decode(u.split(',')[1])); print('   dalle', w, 'peinte')
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'pieces.json'), 'w'), ensure_ascii=False, indent=1)
