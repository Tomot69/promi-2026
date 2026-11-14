"""⚑ v201a (Tom, C-267, sa capture du 13 nov.) — UNE FICHE NE RESTE JAMAIS AU REPOS LA VAGUE À DEMI SOUS LA BANDE ; revenue en haut, son trait est celui de l'ouverture.

Banc : WebKit, ×3, la molette (le seul défilement natif du banc : les glissés de banc_tom ne font défiler aucun conteneur), Promi, Chiche, Cercle, échelle 1 (430 × 932)
et la fenêtre de Tom (390 × 651, l'appareil à 0,7466 ; ×3). Chaque fiche porte six mots (elle défile au-delà de la jonction).
  A · un défilement arrêté dans la zone coupée ]a, z[ (lu sur l'app, contrôlé sur l'image : le haut peint de la vague contre 112) finit, au repos, hors d'elle
  B · un mot envoyé (le glissement de C-260) ne laisse pas la fiche dans la zone
  C · après 1, 3 et 10 allers-retours lents puis lancés, revenue en haut et immobile : la zone du trait (100 → 340 pt) identique AU PIXEL à l'ouverture
  --sonde : la règle du repos coupée (window._ficheSure identité, aucun glissement de repos) — A et B rougissent.
"""
import sys, io, os; sys.path.insert(0, '.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
SONDE = '--sonde' in sys.argv
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,cercle').split(',')
VUES = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--vues=')), '1,tom').split(',')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, d), flush=True)
MOTS = "Array.from({length:6},(_,i)=>({t:'mot '+i+' qui tient de la place sur sa ligne',by:'Marion',d:'2026-11-01T09:00:00Z',vu:true}))"
def ouvre(pg, nat):
    pg.evaluate("()=>{ try{ _peaufSortie() }catch(e){} closeAll(); }"); pg.wait_for_timeout(700)
    if nat == 'cercle': pg.evaluate("()=>{ var k=Object.keys(NUE)[0]; var o=window._cercleMots.de(k); o.comments.length=0; %s.forEach(c=>o.comments.push(c)); _cercleMots.garde(); openEssaim(k); }" % MOTS)
    else: pg.evaluate("n=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.nuee&&!x.chiche); if(n==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; } p.comments=%s; delete p.parts; openDetail(p.id); }" % MOTS, nat)
    pg.wait_for_timeout(3000)
def etat(pg): return pg.evaluate("()=>{ const d=document.getElementById('detailPoster'), r=window._ficheRepos&&window._ficheRepos(); return {s:d.scrollTop, b:r&&r.bornes}; }")
def zone(pg, d):
    k = d[4]; png = pg.screenshot(clip={'x': d[0], 'y': d[1] + 100 * k, 'width': 390 * k, 'height': 240 * k})
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16)
def roule(pg, d, dy, pas, ms):
    pg.mouse.move(d[0] + 195 * d[4], d[1] + 520 * d[4]); n = max(1, int(abs(dy) / pas)); s = dy / n
    for _ in range(n): pg.mouse.wheel(0, s); pg.wait_for_timeout(ms)
def pose(pg, timeout=2500):
    """attend que le défilement ne bouge plus (deux relevés à 300 ms identiques)"""
    av = None
    for _ in range(int(timeout / 300) + 2):
        pg.wait_for_timeout(300); s = pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
        if av is not None and abs(s - av) < 0.1: return s
        av = s
    return av
with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_repos_fiche — %s, charge %.1f%s' % (F, B.charge(), ' · SONDE' if SONDE else ''), flush=True)
    for vue in VUES:
        for nat in NATS:
            T = '[%s · %s]' % (vue, nat)
            vw, vh = (390, 651) if vue == 'tom' else (430, 932)   # la fenêtre de Tom (l'appareil à 0,7466)
            ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=False, user_agent=B.UA)   # la molette n'existe pas en « mobile »
            ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__rf')){ sessionStorage.setItem('__rf','1'); ['promi_onb','promi_guide','promi_veille_off'].forEach(k=>localStorage.setItem(k,'1')); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
            B.toile_pleine(ctx, 'cercle')
            pg = B.ouvre(ctx, F)
            if nat == 'cercle' and not pg.evaluate("()=>typeof NUE!=='undefined' && Object.keys(NUE).length>0"):
                juge(T + ' un Cercle à ouvrir', False, 'aucun'); ctx.close(); continue
            if SONDE: pg.evaluate("()=>{ window._ficheSure=function(t){return t;}; Object.defineProperty(window.__doigts,'t',{get(){return -1e9;},set(v){}}); window.addEventListener('wheel', e=>e.stopPropagation(), {capture:true, passive:true}); }")
            ouvre(pg, nat); d = B.dev(pg); e0 = etat(pg); bo = e0['b']
            if not bo: juge(T + ' les bornes de la zone sont lues', False, e0); ctx.close(); continue
            ref = zone(pg, d)
            # A · arrêté dans la zone, à la molette
            fins = []
            for f in (0.25, 0.5, 0.75):
                pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.style.scrollBehavior='auto'; d.scrollTop=0; }"); pg.wait_for_timeout(400)
                cible = bo['a'] + (min(bo['z'], bo['m']) - bo['a']) * f
                roule(pg, d, cible, 8, 16); s = pose(pg)
                fins.append((round(cible, 1), round(s, 1)))
            mauvais = [x for x in fins if bo['a'] + 0.5 < x[1] < bo['z'] - 0.5]
            juge(T + ' A · arrêté dans la zone coupée ]%.1f, %.1f[, il n’y reste pas' % (bo['a'], bo['z']), not mauvais, fins)
            # B · un mot envoyé
            pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=0; }"); pg.wait_for_timeout(500)
            env = pg.evaluate("""async ()=>{ const l=document.getElementById('cm5Ligne'); if(!l) return 'pas de ligne'; const r=l.getBoundingClientRect(), m=l.querySelector('.cm5-mot')||l;
                const pe=(el,typ,x,y)=>el.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y}));
                pe(m,'pointerdown',r.left+60,r.top+20); pe(m,'pointerup',r.left+60,r.top+20); await new Promise(z=>setTimeout(z,450));
                const s=l.querySelector('.cm5-saisie'); if(!s) return 'pas de saisie'; s.value='Un mot neuf envoyé'; s.dispatchEvent(new Event('input',{bubbles:true}));
                const f=l.querySelector('.cm5-va'), q=f.getBoundingClientRect(); pe(f,'pointerdown',q.left+q.width/2,q.top+q.height/2); pe(f,'pointerup',q.left+q.width/2,q.top+q.height/2); return 'ok'; }""")
            s = pose(pg, 3000); bo2 = etat(pg)['b'] or bo
            juge(T + ' B · un mot envoyé : la fiche ne s’arrête pas dans la zone', env == 'ok' and not (bo2['a'] + 0.5 < s < bo2['z'] - 0.5), '%s · s %.1f · zone ]%.1f, %.1f[' % (env, s, bo2['a'], bo2['z']))
            # C · allers-retours, puis revenue en haut : le trait de l'ouverture au pixel
            ouvre(pg, nat); ref = zone(pg, d); bo = etat(pg)['b']; mx = bo['m']
            for n in (1, 3, 10):
                for mode, pas, ms in (('lent', 6, 16), ('lancé', 60, 8)):
                    for _ in range(n): roule(pg, d, mx, pas, ms); roule(pg, d, -mx - 60, pas, ms)
                    roule(pg, d, -200, 40, 16); s = pose(pg, 3000); pg.wait_for_timeout(400)
                    im = zone(pg, d); diff = np.abs(im - ref).max(axis=2); nb = int((diff > 8).sum())
                    juge(T + ' C · %d aller(s)-retour(s) %s, revenue en haut : la zone du trait = l’ouverture' % (n, mode), s <= 0.5 and nb == 0, 's %.1f · pixels écartés %d' % (s, nb))
            err = [x for x in pg.erreurs if 'version.json' not in x]; juge(T + ' aucune erreur de page', not err, err[:2]); ctx.close()
    b.close()
ok = sum(res); print('\n  %s %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
