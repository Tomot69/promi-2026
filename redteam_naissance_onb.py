#!/usr/bin/env python3
"""redteam_naissance_onb.py — ⚑ v182a (Tom, 6 nov. 2026, C-237 récidive, règle C-247) : « quand on trace le demi-trait sur la page + (Promi, Chiche), la dalle naît
mais elle n'est pas assez grosse, et elle n'a pas l'animation qu'elle a dans l'onboarding. Taille, animation, naissance, vol jusqu'à la Toile : EXACTEMENT ceux
de l'onboarding, par le même code. Juge : la séquence de la page + et celle de l'onboarding comparées image par image (taille, positions, durées). »

Banc WebKit ×3, 430 × 932 ; l'onboarding sur un stockage vierge, la page + sur une Toile de dix paroles (Promi, puis Chiche). Chaque image après le trait, lue dans
la page (la boîte de `.onbv-dalle`, son échelle, sa largeur posée) :
  A · la largeur de la dalle (avant échelle) : celle de l'onboarding, ± 1 pt ;
  B · la naissance : la même transition (le texte de `transition`), l'échelle à la première image ≤ 0,1, le même sommet (± 0,03), le même temps pour atteindre 0,8
      (± 60 ms), la largeur VUE à son sommet ± 2 pt ;
  C · le vol : il part au même instant (± 60 ms) et dure autant (± 80 ms) ; à l'arrivée la dalle a la taille de sa cellule (± 3 pt) et son centre sur elle (± 4 pt).
Rouge sur v181b (`--fichier=zz-v181b.html`) : A, B (la largeur vue), C (la taille à l'arrivée).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
src = open('redteam_moitie.py', encoding='utf-8').read()
exec(src.split('REF = None')[0].split('from playwright.sync_api import sync_playwright')[1].replace("F = next", "F_ = next").replace("res = []", "").replace("def juge", "def _juge"))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
SUIT = """()=>{ window.__fr=[]; let t0=null, el=null; (function f(){ const e=document.querySelector('.onbv-dalle'); if(e && e!==el){ el=e; t0=performance.now(); }
  if(el && el.isConnected){ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=el.getBoundingClientRect(), m=new DOMMatrix(getComputedStyle(el).transform);
    window.__fr.push({t:performance.now()-t0, s:Math.hypot(m.a,m.b), w:parseFloat(el.style.width), vw:r.width/k, cx:(r.left+r.width/2-D.left)/k, cy:(r.top+r.height/2-D.top)/k, tr:el.style.transition}); }
  if(!t0 || performance.now()-t0<2400) requestAnimationFrame(f); })(); }"""
def cles(c):
    if not c: return None
    deb = c[0]; pic = max((x['s'] for x in c if x['t'] <= 700), default=0); vis = max((x['vw'] for x in c if x['t'] <= 700), default=0)
    t08 = next((x['t'] for x in c if x['s'] >= 0.8), None)
    vol = next((x['t'] for x in c if x['t'] > 700 and abs(x['cx'] - deb['cx']) + abs(x['cy'] - deb['cy']) > 1.5), None)
    fv = [x for x in c if x['t'] > 700]; arr = None
    for i in range(1, len(fv)):
        if abs(fv[i]['cx'] - fv[i - 1]['cx']) + abs(fv[i]['cy'] - fv[i - 1]['cy']) < 0.2 and vol and fv[i]['t'] > vol + 200: arr = fv[i]; break
    return {'w': c[0]['w'], 's0': c[0]['s'], 'pic': pic, 'vu': vis, 't08': t08, 'vol': vol, 'arr': arr and arr['t'], 'arrW': arr and arr['vw'], 'arrC': arr and (arr['cx'], arr['cy']), 'tr': c[0]['tr']}
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, onb=False, guide=False, vw=430, vh=932); pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=15); pg.keyboard.press('Enter'); pg.wait_for_timeout(1900)
    pg.evaluate(SUIT)
    Dy = pg.evaluate("()=>{ var D=document.getElementById('device').getBoundingClientRect(), r=document.getElementById('onbTrait').getBoundingClientRect(); return (r.top-D.top)/(D.width/390); }")
    pts = [[x, Dy + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)] for x in range(44, 212, 12)]
    B.glisse(pg, pts, pas=18, tenue=40); pg.wait_for_timeout(2600)
    O = cles(pg.evaluate("()=>window.__fr")); ctx.close()
    print('  onboarding', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in O.items() if k != 'tr'}, flush=True)
    for k in ('promi', 'chiche'):
        ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, 7000)
        ouvre_nature(pg, k); remplit(pg, k, 'marcher le dimanche')
        pg.evaluate(SUIT); B.glisse(pg, points(pg, list(range(44, 212, 12))), pas=18, tenue=40); pg.wait_for_timeout(2600)
        Pp = cles(pg.evaluate("()=>window.__fr")); cell = pg.evaluate("()=>{ const c=(()=>{ const id=promises[promises.length-1].id, c=document.createElement('canvas'); if(!Toile.dalleTrame(c,id,1)) return null; const r=window._dalleSurToile?window._dalleSurToile(c,null):null; return r; })(); return c?[c.w, c.x+c.w/2, c.y+c.h/2]:null; }")   # ⚑ v183b (C-237 suite) — CONTRAT RÉÉCRIT (original en sauvegarde) : la place où la Toile vivante peint la dalle, plus la boîte de la cellule sans la vue
        print('  page + %s' % k, {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in Pp.items() if kk != 'tr'} if Pp else None, 'cellule', cell, flush=True)
        T = '[%s]' % k
        if not Pp: juge(T + ' la dalle naît', False); ctx.close(); continue
        juge(T + ' A · la largeur de la dalle = celle de l\'onboarding (± 1 pt)', abs(Pp['w'] - O['w']) <= 1, (Pp['w'], O['w']))
        juge(T + ' B · la naissance : même transition, s0 ≤ 0,1, même sommet, même temps jusqu\'à 0,8, même largeur vue', Pp['tr'] == O['tr'] and Pp['s0'] <= 0.1 and abs(Pp['pic'] - O['pic']) <= 0.03 and Pp['t08'] is not None and O['t08'] is not None and abs(Pp['t08'] - O['t08']) <= 60 and abs(Pp['vu'] - O['vu']) <= 2,
             {'s0': round(Pp['s0'], 3), 'pic': (round(Pp['pic'], 3), round(O['pic'], 3)), 't08': (Pp['t08'] and round(Pp['t08']), O['t08'] and round(O['t08'])), 'vu': (round(Pp['vu'], 1), round(O['vu'], 1))})
        ok_c = Pp['vol'] is not None and abs(Pp['vol'] - O['vol']) <= 60 and Pp['arrW'] and cell and abs(Pp['arrW'] - cell[0]) <= 3 and abs(Pp['arrC'][0] - cell[1]) <= 4 and abs(Pp['arrC'][1] - cell[2]) <= 4
        juge(T + ' C · le vol : même départ, se pose à la taille et au centre de sa cellule', ok_c, {'vol': (Pp['vol'] and round(Pp['vol']), O['vol'] and round(O['vol'])), 'arrivée': (Pp['arrW'] and round(Pp['arrW'], 1), cell and round(cell[0], 1)), 'centre': (Pp['arrC'], cell and cell[1:])})
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
