#!/usr/bin/env python3
"""
redteam_menu_plus.py — v147 (Tom, 15 oct. 2026, C-142) : LE MENU DU +. « Tout y est trop petit. Grossis tout de 8 à 10 %, proportionnellement : les encarts,
les textes, les espacements. N'abuse pas. Les mots Promi, Chiche et Cercle en PromiLate, +10 % au plus par rapport au texte. Rien ne déborde : sur l'iPhone 16e
(390 × 844) et avec la taille de texte agrandie d'iOS. »
Comme Tom (banc_tom : WebKit, 390 × 844 ×3, doigt) : le + touché, le menu ouvert, clair et sombre. EN DUR (avant : 310 × 62, pas 74, texte 22, aide 13) :
  1 · chaque encart : largeur et hauteur × 1,08 à 1,10 (334,8–341 × 67–68,2), rayon = hauteur / 2 ; le pas entre deux × 1,08 à 1,10 (79,9–81,4) ;
  2 · le texte « Un … » × 1,08 à 1,10 (23,8–24,2 pt), la ligne d'aide × 1,05 à 1,12 (13,7–14,6) ; la nature en PromiLate, au plus 1,10 × le texte ;
  3 · rien ne déborde : chaque texte tient dans son encart (largeur rendue), aucun encart ne sort de l'écran ni ne passe sous la barre (710) ;
      et encore avec le texte agrandi (chaque taille de police × 1,15 — les encarts gardent leurs cotes —, comme le réglage « Taille du texte » de Safari à 115 %) ;
  4 · les trois encarts s'ouvrent toujours au doigt sur leur nature (la page + de la bonne nature).
`--page=` : une autre page servie (la version d'avant : il rougit sur 1 et 2).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
PAGE = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('%s  %s  %s' % ('OK' if c else 'KO', nom, str(d)[:240]), flush=True)
MES = """(z)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, out=[]; const ch=document.getElementById('accChoix'), av=[];
  /* le texte agrandi d'iOS grossit LES TEXTES, pas les encarts (largeur et hauteur en pt fixes) : chaque taille de police × z, rien d'autre */
  if(z) ch.querySelectorAll('.acc-pil, .acc-pil *').forEach(e=>{ av.push([e, e.style.getPropertyValue('font-size'), e.style.getPropertyPriority('font-size')]); e.style.setProperty('font-size', (parseFloat(getComputedStyle(e).fontSize)*z)+'px', 'important'); });
  ch.querySelectorAll('.acc-pil').forEach(p=>{ const r=p.getBoundingClientRect(), cs=getComputedStyle(p), un=p.querySelector('.acc-un')||p.firstChild, sm=p.querySelector('small'), na=p.querySelector('.acc-nat');
    const rg=document.createRange(); rg.selectNodeContents(p); const tr=rg.getBoundingClientRect(); const fsU=un&&un.nodeType===1?parseFloat(getComputedStyle(un).fontSize):parseFloat(cs.fontSize);
    out.push({k:p.getAttribute('data-k'), x:(r.left-D.left)/k, y:(r.top-D.top)/k, w:r.width/k, h:r.height/k, br:parseFloat(cs.borderTopLeftRadius), fs:fsU, sm:sm?parseFloat(getComputedStyle(sm).fontSize):0,
      na:na?{f:getComputedStyle(na).fontFamily.split(',')[0].replace(/["']/g,'').trim(), fs:parseFloat(getComputedStyle(na).fontSize)}:null,
      deborde:(p.scrollWidth>p.clientWidth+1) || (tr.right>r.right-6) || (tr.left<r.left+6), dehors:r.left<D.left||r.right>D.right }); });
  av.reverse().forEach(a=>{ if(a[1]) a[0].style.setProperty('font-size', a[1], a[2]); else a[0].style.removeProperty('font-size'); }); return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('clair', 'sombre'):
        ctx = B.contexte(b, sombre=(th == 'sombre')); pg = B.ouvre(ctx, PAGE)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(900)
        L = pg.evaluate(MES, None)
        if len(L) != 3: juge('[%s] le menu s\'ouvre avec trois encarts' % th, False, L); ctx.close(); continue
        L.sort(key=lambda e: e['y'])
        juge('[%s] 1 · encarts × 1,08 à 1,10 (334,8–341 × 67–68,2), rayon = h/2' % th, all(334.8 <= e['w'] <= 341 and 67 <= e['h'] <= 68.2 and abs(e['br'] - e['h'] / 2) <= 1 for e in L), [(round(e['w'], 1), round(e['h'], 1), e['br']) for e in L])
        pas = [L[i + 1]['y'] - L[i]['y'] for i in range(2)]
        juge('[%s] 1 · le pas entre deux encarts × 1,08 à 1,10 (79,9–81,4)' % th, all(79.9 <= q <= 81.4 for q in pas), [round(q, 1) for q in pas])
        juge('[%s] 2 · « Un … » 23,8–24,2 pt ; l\'aide 13,7–14,6 pt' % th, all(23.8 <= e['fs'] <= 24.2 and 13.7 <= e['sm'] <= 14.6 for e in L), [(e['fs'], e['sm']) for e in L])
        juge('[%s] 2 · la nature en PromiLate, au plus 1,10 × le texte' % th, all(e['na'] and e['na']['f'] == 'PromiLate' and e['na']['fs'] <= 1.10 * e['fs'] + 0.01 for e in L), [e['na'] for e in L])
        juge('[%s] 3 · rien ne déborde (texte dans son encart, encarts dans l\'écran, au-dessus de la barre 710)' % th, not any(e['deborde'] or e['dehors'] for e in L) and max(e['y'] + e['h'] for e in L) <= 710, [(e['k'], e['deborde'], round(e['y'] + e['h'], 1)) for e in L])
        Z = pg.evaluate(MES, '1.15')
        juge('[%s] 3 · avec le texte agrandi (× 1,15) : rien ne déborde' % th, not any(e['deborde'] or e['dehors'] for e in Z), [(e['k'], e['deborde'], e['dehors']) for e in Z])
        ok = True; det = []
        for k in ('promi', 'chiche', 'nuee'):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500); B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k)
            v = False
            for _ in range(30):
                pg.wait_for_timeout(120)
                if pg.evaluate("k=>{ const s=document.getElementById('createSheet'); return !!(s && s.classList.contains('show') && s.classList.contains('pp-'+k)); }", k): v = True; break
            det.append((k, v)); ok = ok and v
        juge('[%s] 4 · chaque encart ouvre, au doigt, la page + de sa nature' % th, ok, det)
        ctx.close()
    b.close()
n = sum(res); print('\n%d / %d' % (n, len(res))); sys.exit(0 if n == len(res) else 1)
