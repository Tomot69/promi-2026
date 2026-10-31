#!/usr/bin/env python3
"""redteam_trait_105.py — ⚑ v162 (Tom, C-184) : LE TRAIT 5 % PLUS GROS, PAS PLUS.

⚠ REMPLACÉ depuis v163a par `redteam_trait_k.py` (le facteur réglable, défaut 1,15) : ce juge porte ×1,05 et rougit par décision. Gardé pour l'histoire.

« Dans les trois pages + et sur toutes les fiches : le trait (pointillé et continu), la flèche et sa pointe grossissent de 5 % exactement ; aussi le trait
validé ou lancé d'un Cercle ; rien d'autre ne change ; l'onboarding n'est pas concerné. » Le juge PIÈGE les appels de dessin sur le canevas du trait (l'épaisseur
au moment de chaque `stroke`, le rayon de chaque `arc` rempli), sur la version d'avant servie à côté (`--ref=zz-v161.html`) et sur celle-ci, écran par écran :
  A · la page + d'un Promi, d'un Chiche, d'un Cercle ; la fiche d'un Promi et d'un Chiche à tenir, d'un Promi tenu, d'un Cercle : chaque épaisseur et chaque
      rayon × 1,05 ± 0,005, et rien d'autre (le même nombre d'appels, les mêmes valeurs à 1,05 près) ;
  B · l'onboarding : le trait identique au pixel (au même réglage d'onde, `?onde=1`, l'amplitude de v161).
⚠ L'instant « tenir » (son propre peintre, le même facteur) n'est pas mesuré ici : il ne dure qu'un instant.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ref=')), 'zz-v161.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
PIEGE = """(()=>{ window.__T={}; const C=CanvasRenderingContext2D.prototype, st=C.stroke, ar=C.arc, fi=C.fill;
  function cle(g){ const c=g.canvas; return c && (c.id||c.className||'?'); }
  C.stroke=function(){ try{ const k=cle(this); if(window.__on && window.__on.indexOf(k)>=0){ (window.__T[k]=window.__T[k]||[]).push(['L', +this.lineWidth.toFixed(4)]); } }catch(_){ } return st.apply(this, arguments); };
  C.arc=function(x,y,r){ try{ const k=cle(this); if(window.__on && window.__on.indexOf(k)>=0){ (window.__T[k]=window.__T[k]||[]).push(['R', +(+r).toFixed(4)]); } }catch(_){ } return ar.apply(this, arguments); };
})();"""
def releve(b, fichier, quoi):
    ctx = B.contexte(b); B.toile_pleine(ctx, 5); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, fichier)
    if quoi.startswith('plus-'):
        nat = quoi[5:]; pg.evaluate("()=>{ window.__on=['csTrameCv','planterCv','csTrait','ppTrait']; window.__T={}; }")
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
    else:
        nat = {'fiche-promi': 0, 'fiche-chiche': 1, 'fiche-tenu': 0}.get(quoi)
        if quoi == 'fiche-cercle':
            pg.evaluate("()=>{ window.__on=['dpTrameCv']; window.__T={}; window.openNueeDetail('famille'); }")
        else:
            pg.evaluate("q=>{ window.__on=['dpTrameCv']; window.__T={}; const L=promises.filter(p=>!p.draft && (q[1]? p.status==='tenu' : p.status!=='tenu') && (!!p.chiche)===(q[0]===1)); if(L.length) openDetail(L[0].id); }", [nat, quoi == 'fiche-tenu'])
        pg.wait_for_timeout(2600)
    T = pg.evaluate("()=>window.__T"); ctx.close()
    L = []; [L.extend(v) for v in T.values()]; return L
def trait_onb(b, fichier):
    ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, fichier, q='?onde=1', attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200)
    B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500); pg.keyboard.type('marcher une heure', delay=15); pg.evaluate("()=>document.getElementById('onbIn').blur()"); pg.wait_for_timeout(2500)
    d = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); const g=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let h=2166136261; for(let i=0;i<g.length;i+=1){ h^=g[i]; h=Math.imul(h,16777619)>>>0; } return [c.width,c.height,h]; }")
    ctx.close(); return d
with sync_playwright() as p:
    b = p.webkit.launch()
    for quoi in ('plus-promi', 'plus-chiche', 'plus-nuee', 'fiche-promi', 'fiche-chiche', 'fiche-tenu', 'fiche-cercle'):
        a = releve(b, REF, quoi); n = releve(b, F, quoi)
        pa = [x for x in a if x[1] > 0]; pn = [x for x in n if x[1] > 0]
        # le trait : chaque VALEUR d'épaisseur et de rayon d'avant (la pointe, le trait, la flèche d'invite, les points Ø 12) × 1,05, et aucune autre valeur
        #   (le nombre d'appels varie d'une ouverture à l'autre : la page se repeint plus ou moins souvent — on compare les ensembles de valeurs)
        va = sorted(set(tuple(x) for x in pa)); vn = sorted(set(tuple(x) for x in pn)); attendu = sorted(set((t, round(v * 1.05, 4)) for t, v in va))
        ok = bool(va) and len(vn) == len(attendu) and all(a[0] == b_[0] and abs(a[1] - b_[1]) <= 0.005 * a[1] for a, b_ in zip(attendu, vn))
        juge('[%s] A · chaque épaisseur et chaque rayon du trait (pointe, trait, flèche d\'invite, points) × 1,05 ± 0,005, aucune autre valeur' % quoi, ok,
             'avant %s · maintenant %s' % (va, vn))
    oa = trait_onb(b, REF); on = trait_onb(b, F)
    juge('B · l\'onboarding : le trait identique au pixel (?onde=1)', oa == on, 'avant %s · maintenant %s' % (oa, on))
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
