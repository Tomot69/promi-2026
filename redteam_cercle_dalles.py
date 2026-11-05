#!/usr/bin/env python3
"""redteam_cercle_dalles.py — ⚑ v179b (Tom, C-231) : LES DALLES DANS LA FICHE D'UN CERCLE.

« Chaque dalle garde la mémoire du monde et de la palette dans lesquels sa parole a été créée, comme dans la Pelote et la liste de l'Aura ; elles ne sont pas
tronquées, et leur arrangement est harmonieux, dans le même esprit que la liste de l'Aura. Le moteur de la Toile n'est pas modifié. »
Banc WebKit ×3, un Cercle de six paroles plantées dans trois mondes (banc-etats/etat-cercle.json), clair et sombre, échelles 1 et 0,79. Chaque rendu de dalle
est PIÉGÉ (`_rendDalle` : l'id et le monde demandés) ; la composition publiée (`_nueeSemis.cases`) ne sert qu'à trouver les boîtes :
  A · chaque parole a sa dalle, une fois ; B · rendue dans le monde de SA plantation (le monde passé au rendu = celui de la parole) — trois mondes ;
  C · des boîtes égales ; D · entières : chaque dalle peinte est sous le plateau (≥ 100 pt), au-dessus de la vague (sous toute sa largeur), dans
      l'appareil, et ne touche pas le bouton photo ; E · rien d'autre n'est peint dans le champ hors des boîtes (lu sur l'image : aucune autre couleur que
      le champ entre plateau et vague, hors des boîtes et du bouton) ; aucune erreur de page.
Rouge sur v178 (`--fichier=zz-v178.html`) : le semis du Studio, des dalles répétées, coupées.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
PIEGE = """()=>{ window.__rd=[]; if(window.__rdP) return; window.__rdP=1; const f=window._rendDalle; window._rendDalle=function(id,w,h,o){ try{ const pile=new Error().stack||''; if(/_ficheNuee|grille|dalleDe/.test(pile)) window.__rd.push([id, o&&o.monde?o.monde.m+'/'+o.monde.p:null]); }catch(_){ } return f.apply(this, arguments); }; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        for vw, vh in ((390, 844), (330, 714)):
            T = '[%s · %d×%d]' % ('sombre' if sombre else 'clair', vw, vh)
            ctx = B.contexte(b, sombre=sombre, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
            pg.evaluate(PIEGE); pg.evaluate("()=>{ closeAll(); window.__rd=[]; openNueeDetail('potager'); }"); pg.wait_for_timeout(2500)
            try: pg.wait_for_function("()=>{ const s=window._nueeSemis; return s && !s.sautees && s.cases.length===promises.filter(q=>q.nuee==='potager').length; }", timeout=8000)
            except Exception: pass   # une dalle différée (budget) se repeint une tâche plus tard
            pg.wait_for_timeout(400)
            P = pg.evaluate("()=>promises.filter(q=>q.nuee==='potager').map(q=>[q.id, q.monde.m+'/'+q.monde.p])")
            S = pg.evaluate("()=>window._nueeSemis&&window._nueeSemis.cases") or []
            rd = pg.evaluate("()=>window.__rd")
            ids = [c['id'] for c in S]
            juge(T + ' A · chaque parole du Cercle a sa dalle, une fois', sorted(ids) == sorted(i for i, m in P), '%d paroles · %d dalles' % (len(P), len(ids)))
            dem = {}
            for i, m in rd: dem.setdefault(i, set()).add(m)
            okB = all(dem.get(i) == {m} for i, m in P) and len(set(m for i, m in P)) == 3
            juge(T + ' B · chaque dalle rendue dans le monde de SA plantation (trois mondes)', okB, {i: sorted(x or '—' for x in dem.get(i, [])) for i, m in P})
            tl = set((round(c['bw'], 2), round(c['bh'], 2)) for c in S)
            juge(T + ' C · des boîtes égales', len(tl) == 1, tl)
            g = pg.evaluate("""()=>{ const dp=document.getElementById('detailPoster'), D=dp.getBoundingClientRect(), k=D.width/390, e=window._nueeSemis, O=window._onde;
              const y=O.onde(e.base, e.amp); let bt=null; { let el=document.elementFromPoint(D.left+349*k, D.top+108*k); while(el && el!==dp){ const r=el.getBoundingClientRect(); if(r.width/k>=30 && r.width/k<=60 && r.height/k>=30 && r.height/k<=60){ bt=[(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k]; break; } el=el.parentElement; } }   /* le bouton photo, trouvé au doigt */
              const vg=[]; for(let x=0;x<=390;x+=1) vg.push(y(x));
              return {cases:e.cases.map(c=>{ const p=c.peint; let m=1e9; for(let x=p.x;x<=p.x+p.w;x+=2) m=Math.min(m,y(x)); return [p.x,p.y,p.w,p.h,m]; }), bouton:bt, vague:vg, D:[D.left,D.top,k]}; }""")
            mauv = []
            for x, y, w, h, m in g['cases']:
                if y < 100 or y + h > m - 4 or x < 0 or x + w > 390: mauv.append([round(x), round(y), round(w), round(h), round(m)])
                bt = g['bouton']
                if bt and not (x + w <= bt[0] or x >= bt[2] or y + h <= bt[1] or y >= bt[3]): mauv.append(['bouton', round(x), round(y)])
            juge(T + ' D · entières : sous le plateau, au-dessus de la vague, dans l\'appareil, hors du bouton photo', S and not mauv, mauv[:4])
            im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); kk = im.width / 390.0
            fond = im.getpixel((int(195 * kk), int(104 * kk)))
            autres = 0; vus = 0
            for yy in range(102, 130, 3):
                for xx in range(4, 386, 3):
                    if any(x - 2 <= xx <= x + w + 2 and y - 2 <= yy <= y + h + 2 for x, y, w, h, m in g['cases']): continue
                    if g['bouton'] and g['bouton'][0] - 4 <= xx <= g['bouton'][2] + 4 and g['bouton'][1] - 4 <= yy <= g['bouton'][3] + 4: continue
                    if yy >= g['vague'][min(390, xx)] - 9: continue   # le trait de la vague
                    px = im.getpixel((int(xx * kk), int(yy * kk))); vus += 1
                    if sum(abs(a - c) for a, c in zip(px, fond)) > 40:
                        autres += 1
                        if '--dump' in sys.argv and autres < 30: print('      ', xx, yy, px, fond)
            juge(T + ' E · rien d\'autre n\'est peint dans la bande hors des boîtes (lu sur l\'image, 102 → 130 pt)', autres <= vus * 0.06, '%d / %d points' % (autres, vus))
            juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
            if '--capture' in sys.argv and not sombre and vw == 390:
                import os; os.makedirs('planche-v179b', exist_ok=True); im.save('planche-v179b/cercle-dalles.png')
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
