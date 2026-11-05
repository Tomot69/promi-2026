#!/usr/bin/env python3
"""redteam_frappe_douce.py — ⚑ v180b (Tom, C-234 suite) : « quand on commence à taper, la dalle et la vague bougent d'un coup ; le mouvement doit être doux et
continu jusqu'à la position de frappe (même courbe que l'horizon, 300 à 400 ms). Corrige aussi le saut de la vague à la fermeture du clavier. »

Banc WebKit ×3, état exporté de Tom, Promi · Chiche · Cercle, échelles 1 et 0,79. Ce qui est PEINT est piégé : chaque bord de champ dessiné (`_onde.chemin` sur
#csTrameCv et sur #ppMvt, l'onde lue à x = 195) et chaque dalle posée sur le champ (`_poseDalle`). La vague visible est celle de #ppMvt tant qu'il est là.
  O · au toucher sur la phrase : la première image montre la vague à sa place d'avant (± 3 pt) ; elle rejoint sa place de saisie en 300 à 420 ms (comptés de son départ), sans
      revenir en arrière, et aucun pas ne dépasse celui de la courbe de l'horizon pour cette distance (le pic de l'aller-retour quadratique × 1,3 + 2 pt : l'horloge du juge et celle de la page ne tombent pas dans la même image) ;
  F · à la fermeture du clavier (Retour) : la vague descend à sa place puis l'horizon remonte (deux mouvements) : aucun pas au-delà de la borne de la plus grande des deux ;
  D · la dalle : aucun déplacement de plus de 3 pt par image de 16,7 ms, de l'ouverture à 3 s après Retour.
⚠ « ≤ 3 pt par image » (le brief) ne peut pas tenir pour la VAGUE : elle va de 312 à 144 pt ; en 360 ms la courbe de l'horizon y passe à 15 pt par image au pic.
  La règle des 3 pt est jugée sur la dalle ; la vague est jugée sur sa continuité (jamais plus que sa courbe), sa durée et sa première image.
Rouge sur v180a (`--fichier=zz-v180a.html`) : la vague passe d'un coup à sa place de saisie.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), '1,0.79')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
PIEGE = """()=>{ if(window.__fdP) return; window.__fdP=1; window.__fd=[]; const O=window._onde, ch=O.chemin, pd=window._poseDalle; let w={}, d=null;
  O.chemin=function(g,y,a,b){ try{ const id=g&&g.canvas&&g.canvas.id; if((id==='csTrameCv'||id==='ppMvt') && a===0 && b>=389) w[id]=+y(195).toFixed(2); }catch(_){ } return ch.apply(this, arguments); };
  window._poseDalle=function(g,id,x,y,ww,h,o){ const r=pd.apply(this, arguments); try{ if(g&&g.canvas&&g.canvas.id==='csTrameCv'&&r) d=+r.y.toFixed(2); }catch(_){ } return r; };
  (function f(t){ const cs=document.getElementById('createSheet'), mv=document.getElementById('ppMvt');
    if(cs && cs.classList.contains('show')) window.__fd.push([t, mv ? (w.ppMvt!=null?w.ppMvt:null) : (w.csTrameCv!=null?w.csTrameCv:null), d, !!mv]);
    requestAnimationFrame(f); })(performance.now()); }"""
SEL = {'promi': '#csPhrase .ph-m[data-ph="titre"]', 'chiche': '#csPhrase .ph-m[data-ph="titre"]', 'nuee': '#nueePhrase .ph-m[data-np="nom"]'}
def borne(dist): return 2 * abs(dist) * 16.7 / 360 * 1.3 + 2
def mouvement(L, t0, t1):
    """la vague entre deux instants : sa première valeur, sa dernière, la fin du mouvement, le pire pas ramené à 16,7 ms, un retour en arrière"""
    S = [x for x in L if t0 <= x[0] <= t1 and x[1] is not None]
    if len(S) < 3: return None
    v0, vf = S[0][1], S[-1][1]; sg = 1 if vf >= v0 else -1
    fin = next((x[0] for x in S if abs(x[1] - vf) < 0.5), S[-1][0])
    debut = next((S[i - 1][0] for i in range(1, len(S)) if abs(S[i][1] - v0) > 0.5), S[0][0])   # le mouvement se compte de son départ (la latence du toucher n'est pas sa durée)
    R = [S[0]]
    for x in S[1:]:   # deux relevés à moins de 12 ms l'un de l'autre se réunissent (l'horloge du juge et celle de la page ne tombent pas dans la même image)
        if x[0] - R[-1][0] < 12 and len(R) > 1: R[-1] = x
        else: R.append(x)
    pire, arr = 0, 0
    for a, b in zip(R, R[1:]):
        dt = max(1, b[0] - a[0]); dv = b[1] - a[1]
        pire = max(pire, abs(dv) * 16.7 / max(dt, 16.7))
        if dv * sg < -0.6: arr = max(arr, abs(dv))
    return {'v0': v0, 'vf': vf, 'ms': round(fin - debut), 'latence': round(debut - S[0][0]), 'pire': round(pire, 2), 'arriere': round(arr, 2), 'n': len(S)}
CHARGE = B.charge()
print('  charge', CHARGE, '— au-dessus de 4, la durée (cadence) n\'est pas jugée au-delà de 420 ms : seulement sa continuité')
with sync_playwright() as p:
    b = p.webkit.launch()
    for ech in ECH.split(','):
        for nat in ('promi', 'chiche', 'nuee'):
            T = '[%s · ×%s]' % (nat, ech)
            ctx, d = B.contexte_tom(b, echelle=1 if ech == '1' else None)
            pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
            pg.evaluate(PIEGE); pg.wait_for_timeout(400)
            avant = pg.evaluate("()=>{ const L=window.__fd; return L.length?L[L.length-1][1]:null; }")
            t_tap = pg.evaluate("()=>performance.now()"); B.tap_sel(pg, SEL[nat]); pg.wait_for_timeout(900)
            pg.keyboard.type('apprendre le violoncelle', delay=35); pg.wait_for_timeout(700)
            t_ret = pg.evaluate("()=>performance.now()"); pg.keyboard.press('Enter'); pg.wait_for_timeout(3200)
            L = pg.evaluate("()=>window.__fd")
            o = mouvement(L, t_tap, t_ret - 50)
            okO = bool(o and avant is not None and abs(o['v0'] - avant) <= 3 and (300 <= o['ms'] <= 420 or (CHARGE >= 4 and o['ms'] > 300)) and o['arriere'] == 0 and o['pire'] <= borne(o['vf'] - o['v0']))
            juge(T + ' O · le toucher sur la phrase : la vague part de sa place et rejoint la saisie en 300 à 420 ms, sans saut', okO, 'avant %s · %s · borne %.1f' % (avant, o, borne((o['vf'] - o['v0']) if o else 0)))
            f = mouvement(L, t_ret, t_ret + 3150)
            okF = bool(f and f['pire'] <= borne(max(abs(f['vf'] - f['v0']), 170)))
            juge(T + ' F · la fermeture du clavier : la vague rejoint sa place puis l\'horizon, sans saut', okF, f)
            ds = [x for x in L if x[0] >= t_tap and x[2] is not None]; pire = 0
            for a, c in zip(ds, ds[1:]): pire = max(pire, abs(c[2] - a[2]) * 16.7 / max(c[0] - a[0], 16.7))
            juge(T + ' D · la dalle : aucun déplacement de plus de 3 pt par image de 16,7 ms', len(ds) >= 5 and pire <= 3, '%d dessins · pire %.2f pt' % (len(ds), pire))
            ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
