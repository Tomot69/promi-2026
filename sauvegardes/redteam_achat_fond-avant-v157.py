#!/usr/bin/env python3
"""redteam_achat_fond.py — ⚑ v156 (Tom, C-170 rouvert, Q564) : L'ENCART D'ACHAT FLOUTE LA TOILE DU STUDIO, JAMAIS UNE IMAGE PÉRIMÉE.

« Dans l'encart qui paraît avant l'achat (« ton achat reste sur ce téléphone… »), il y a un flou abstrait, et SOUS ce flou on voit l'ANCIENNE Toile. Le
flou de cet encart se fait en flaques (même langage que le guide). Ce qui est flouté dessous, c'est la Toile qu'on regarde à ce moment dans le Studio : le
monde et la couleur affichés, pas la Toile de l'accueil, ni une image en cache. Ce fond est préparé avant l'ouverture de l'encart, sans saccade. Juge :
ouvrir l'encart d'achat depuis chaque monde payant affiché dans le Studio ; le fond flouté correspond à la Toile du Studio, jamais à une image périmée. »
Banc comme Tom (WebKit 390 × 844 ×3, une Toile de 25 paroles, AUCUN compte : l'encart paraît), chaque monde payant, « Adopte ce design » touché au doigt :
  A · le fond de l'encart est la Toile du Studio floutée : comparée au Studio pris à l'instant où l'encart s'ouvre (flouté à 4,8 de même), écart ≤ 12 ; et elle est
      loin de la Toile de l'accueil restée dessous (≥ 2 × plus loin) ; le monde déclaré est celui affiché
  B · ce flou paraît EN FLAQUES (une couverture qui va de 0 à 1, gardée sous le panneau) ; plus de voile
  C · il est préparé AVANT l'ouverture (au toucher) ; la préparation coûte au plus 40 ms — sa durée n'est jugée qu'au calme
Preuve : `--fichier=zz-av155.html` rougit (A, B).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
MAX = int(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--n=')), '12'))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)
MESURE = """()=>{ const h=document.getElementById('accRappelCompte'), fc=document.getElementById('achatFond'), f=window._fondAchatPose||null;
  const bg=document.getElementById('stBg'), tc=document.getElementById('toileCv');
  function petit(src, flou){ const c=document.createElement('canvas'); c.width=390; c.height=844; c.getContext('2d').drawImage(src,0,0,390,844); const s=document.createElement('canvas'); s.width=78; s.height=169;
    s.getContext('2d').drawImage(flou?Flaques.floute(c,4.8):c,0,0,78,169); return s.getContext('2d').getImageData(0,0,78,169).data; }
  function ec(a,b){ let e=0; for(let i=0;i<a.length;i+=4) e+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]); return e/(a.length/4*3); }
  let r={sur:h?h.classList.contains('sur-studio'):false, voile:h?getComputedStyle(h).backgroundColor:null, fond:!!fc, monde:f?f.monde:null, aff:(document.getElementById('studioScreen').getAttribute('data-stp-monde')||'')+'|'+((window.Toile&&Toile.mondeCourant)?Toile.mondeCourant().p:'')};
  if(f){ const s=document.createElement('canvas'); s.width=78; s.height=169; s.getContext('2d').drawImage(f.flou,0,0,78,169); const A=s.getContext('2d').getImageData(0,0,78,169).data;
    const snap=(window.__snaps||[])[(window.__snaps||[]).length-1]||bg; r.eStudio=ec(A, petit(snap,true)); r.eAccueil=ec(A, petit(tc,true)); r.prep=Math.round(f.t-(window.__tTouche||0)); r.avOuv=Math.round((window.__tOuv||0)-f.t); }
  return r; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); vus = []
    ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); }"); pg.wait_for_timeout(400)
    for tour in range(30):
        if len(vus) >= MAX: break
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
        w = None
        for i in range(24):
            w = pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')?window._lockedWorld:null")
            if w and w not in vus: break
            if '--debug' in sys.argv: print('   glisse', i, w)
            B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500); w = None
        if not w: break
        vus.append(w)
        pg.evaluate("""()=>{ window.__snaps=window.__snaps||[]; if(!window.__oc){ const oc=window._onbCompte; window.__oc=1; window._onbCompte=function(){ try{ window.__tOuv=performance.now(); const bg=document.getElementById('stBg'), c=document.createElement('canvas'); c.width=390; c.height=844; c.getContext('2d').drawImage(bg,0,0,390,844); window.__snaps.push(c); }catch(e){} return oc.apply(this, arguments); }; } }""")
        pg.evaluate("""()=>{ window.__u=[]; window.__tTouche=0; document.addEventListener('touchstart', ()=>{ if(!window.__tTouche) window.__tTouche=performance.now(); }, {capture:true, once:true});
          (function f(){ const c=document.getElementById('achatFond'); if(c) window.__u.push(+c.getAttribute('data-u')); if(window.__u.length<600 && !(window.__u.length && window.__u[window.__u.length-1]>=1)) requestAnimationFrame(f); })(); }""")
        c = pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
        pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1800)
        m = pg.evaluate(MESURE); us = pg.evaluate("()=>window.__u")
        ok_a = m.get('eStudio') is not None and m['eStudio'] <= 12 and m['eAccueil'] >= 2 * max(1, m['eStudio']) and m['monde'] == m['aff']
        juge('[%s] A · le fond de l\'encart est la Toile du Studio floutée (monde et couleur affichés), loin de la Toile de l\'accueil' % w, ok_a,
             'écart au Studio %s · à l\'accueil %s · monde %s / affiché %s' % (m.get('eStudio') and round(m['eStudio'], 1), m.get('eAccueil') and round(m['eAccueil'], 1), m['monde'], m['aff']))
        juge('[%s] B · ce flou paraît en flaques (0 → 1, gardé sous le panneau), sans voile' % w, m['sur'] and m['fond'] and us and min(us) < 0.2 and max(us) >= 0.99 and m['voile'] in ('rgba(0, 0, 0, 0)', 'transparent'),
             'flaques %s → %s (%d images) · voile %s' % (us and round(min(us), 2), us and round(max(us), 2), len(us), m['voile']))
        calme = B.charge() < 4
        juge('[%s] C · préparé AVANT l\'ouverture, au toucher%s' % (w, '' if calme else ' (sa durée non jugée : charge ≥ 4)'), m.get('prep') is not None and -60 <= m['prep'] <= 200 and m.get('avOuv', -1) >= 0, 'préparé %s ms après le toucher (le doigt posé), %s ms avant l\'ouverture' % (m.get('prep'), m.get('avOuv')))
        # « Acheter sans compte » : l'encart part ; on passe au monde suivant
        t = pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if t: pg.touchscreen.tap(t[0], t[1])
        VU = "()=>{ const h=document.getElementById('accRappelCompte'); return !!(h && h.classList.contains('vu') && h.querySelector('.onbv-compte .lab') && /Garder ton achat/.test(h.querySelector('.onbv-compte .lab').textContent)); }"
        for _ in range(60):   # le second encart paraît ≈ 0,9 s après la fermeture du premier (plus sous charge)
            pg.wait_for_timeout(100)
            if pg.evaluate(VU): break
        pg.wait_for_timeout(1200)
        # le second moment (« Garder ton achat », juste après) : son fond aussi est le Studio de cet instant ; « Plus tard »
        m2 = pg.evaluate(MESURE)
        if m2['sur'] or pg.evaluate("()=>document.getElementById('accRappelCompte').classList.contains('vu')"):
            pg.wait_for_timeout(600); m2 = pg.evaluate(MESURE)
            juge('[%s] A · le second encart (« Garder ton achat ») floute aussi la Toile du Studio de cet instant' % w, m2.get('eStudio') is not None and m2['eStudio'] <= 12 and m2['eAccueil'] >= 2 * max(1, m2['eStudio']),
                 'écart au Studio %s · à l\'accueil %s' % (m2.get('eStudio') and round(m2['eStudio'], 1), m2.get('eAccueil') and round(m2['eAccueil'], 1)))
            t = pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
            if t: pg.touchscreen.tap(t[0], t[1])
            for _ in range(40):
                pg.wait_for_timeout(100)
                if not pg.evaluate("()=>{ const h=document.getElementById('accRappelCompte'); return !!(h && h.classList.contains('vu')); }"): break
            pg.wait_for_timeout(600)
            if '--debug' in sys.argv: print('   après le second :', pg.evaluate("()=>({vu:document.getElementById('accRappelCompte').className, panneaux:document.querySelectorAll('#accRappelCompte .onbv-compte').length, studio:document.getElementById('studioScreen').className})"))
        if '--debug' in sys.argv: print('   après :', pg.evaluate("()=>({vu:document.getElementById('accRappelCompte').className, lock:document.getElementById('studioScreen').classList.contains('world-locked'), compte:localStorage.getItem('promi_compte'), own:JSON.stringify(typeof _ownedDesigns!=='undefined'?_ownedDesigns:null)})"), t)
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page (%d mondes : %s)' % (len(vus), ', '.join(vus)), not er and len(vus) >= min(MAX, 12), er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
