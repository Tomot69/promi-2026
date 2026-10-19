#!/usr/bin/env python3
"""redteam_tenir_e3.py — ⚑ E3 (v153, C-077) : LE MOMENT « TENIR », AVEC L'AMENDEMENT A1 (il prime sur ENGAGEMENT.md).

A1 : ni onde sur les dalles, ni menthe ; le moment « tenir » est le rideau validé par Tom (C-118, C-156). E3 se réduit à :
  R4 · L'INVARIANCE. Deux paroles qui diffèrent sur tout — A : à soi, « un jour », 3 mots, sans Cercle ; B : à Rachel, demain, 30 mots, dans un
       Cercle — donnent la MÊME séquence. Lue sur les PIXELS du rideau, image par image (jamais sur une valeur que l'app déclare) : le départ (le
       front sort du trait), la fin de la descente (le front à la barre), le retour au repos (le rideau parti). Deux passes de chacune, en
       alternance ; on compare les médianes : écart ≤ 16 ms sur chaque instant ; le MOUVEMENT (du lever à la fin de la descente) ≤ 1 000 ms.
       ⚠ L'instant entier (le rideau posé 2 s, puis remonté) dure ≈ 2,6 s : c'est la durée validée par Tom (C-111, C-118) — la borne de 1 000 ms
       d'ENGAGEMENT.md s'applique au mouvement (question écrite, Q554). Les durées ne se jugent qu'au calme (charge < 4, C-137) ; au-dessus,
       « non jugé », relevé affiché. La FORME de la séquence (mêmes étapes, le front qui ne fait que descendre puis remonter, la parole tenue)
       se juge toujours.
  H  · le crochet `promiHaptique('tenir')` existe, est appelé UNE fois, au lever, avant la première image du rideau ; il ne fait rien.
  RM · « Réduire les animations » : la fiche passe tenue SANS rideau, en UN seul changement d'aplat, SANS fondu — aucune couche de rideau, aucun
       instant, aucune opacité intermédiaire ni animation pendant la séquence ; la parole est tenue ; un seul changement de l'aspect de la fiche.
  LT · aucune tâche longue au-delà de 50 ms pendant la séquence, sous le monde le plus coûteux (Chromium, vrai GPU, PerformanceObserver
       « longtask ») — jugé au calme seulement.
Banc comme Tom (banc_tom : WebKit, 390 × 844 ×3, le trait tracé au doigt). Pas de vidéo (C-137).
Preuve : `--fichier=zz-av152.html` rougit (H, RM).
"""
import sys, os, statistics; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
R4_SEUL = '--r4' in sys.argv
CHARGE = B.charge()
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %-100s %s' % ('OK' if ok else 'KO', nom, str(d)[:300]), flush=True)
MOTS30 = ' '.join(['rendre', 'à', 'Rachel', 'le', 'grand', 'livre', 'rouge', 'de', 'cuisine', 'que', 'sa', 'grand-mère', 'lui', 'avait', 'offert',
                   'pour', 'ses', 'vingt', 'ans', 'avant', 'la', 'fin', 'du', 'mois', 'sans', 'faute', 'et', 'bien', 'emballé', 'aussi'])
SONDE = """()=>{ window.__lever=0; window.__img=[]; window.__hap=[];
  const hp=window.promiHaptique; window.promiHaptique=function(n){ window.__hap.push([performance.now(), n, !!document.getElementById('tenirMaree')]); if(hp) return hp.apply(this, arguments); };
  document.addEventListener('touchend', function(){ if(!window.__lever) window.__lever=performance.now(); }, {capture:true, once:true});
  window._mareeReleve=function(g, cv, t, u, T){ const k=cv.width/390, W=cv.width, H=cv.height; const fr=[];
    for(const x of [40,100,160,220,280,340]){ const col=g.getImageData(Math.round(x*k),0,1,H).data; let bas=-1; for(let y=H-1;y>=0;y--){ if(col[4*y+3]>200){ bas=y/k; break; } } if(bas>T.y(x)+9) fr.push(bas); }
    fr.sort((a,b)=>a-b); window.__img.push([performance.now(), fr.length>=3?fr[fr.length>>1]:null]); };
  (function f(){ const m=!!document.getElementById('tenirMaree'); (window.__pres=window.__pres||[]).push([performance.now(), m]); if(window.__pres.length<600) requestAnimationFrame(f); })(); }"""
def prepare(pg, cas):
    if cas == 'A':
        B.plante(pg, 'rendre le livre')
    else:
        B.plante(pg, 'rendre le livre', qui='Rachel')
        pg.evaluate("t=>{ const p=promises[promises.length-1]; p.title=t; p.who='Rachel'; p.nuee='famille'; p.due=1; delete p.dueISO; try{ saveState(); }catch(e){} try{ syncAll(); }catch(e){} }", MOTS30)
    pg.wait_for_timeout(700)
    return pg.evaluate("()=>{ const p=promises[promises.length-1]; return {titre:p.title.split(' ').length, qui:p.who, nuee:p.nuee||null, due:p.due, st:p.status}; }")
def tenir(pg):
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    pg.evaluate(SONDE)
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    y = z[1] + z[3] * 0.45
    B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    for _ in range(40):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>{ const P=window.__pres||[]; const vu=P.findIndex(x=>x[1]); return vu>=0 && P.slice(vu).some(x=>!x[1]); }"): break
    d = pg.evaluate("()=>({lev:window.__lever, img:window.__img, pres:window.__pres, hap:window.__hap, st:promises[promises.length-1].status, inst:window._instant})")
    L = d['lev'] or 0; img = [(t - L, f) for t, f in d['img'] if f is not None]
    dep = next((t for t, f in img), None); desc = next((t for t, f in img if f >= 735), None)
    vu = next((i for i, x in enumerate(d['pres']) if x[1]), None)
    repos = next((x[0] - L for x in d['pres'][vu:] if not x[1]), None) if vu is not None else None
    # la forme : le front ne fait que descendre jusqu'à la barre, puis remonter
    fr = [f for t, f in img]; i_max = fr.index(max(fr)) if fr else 0
    descend = all(b >= a - 2 for a, b in zip(fr[:i_max], fr[1:i_max + 1])); remonte = all(b <= a + 2 for a, b in zip(fr[i_max:], fr[i_max + 1:]))
    return {'dep': dep, 'desc': desc, 'repos': repos, 'forme': bool(fr) and descend and remonte and max(fr) >= 735, 'st': d['st'], 'hap': d['hap'], 'lev': L, 'img0': (d['img'][0][0] if d['img'] else None), 'n': len(img)}
with sync_playwright() as p:
    b = p.webkit.launch()
    # ── R4
    M = {'A': [], 'B': []}; desc = {}
    for cas in ['A', 'B', 'A', 'B']:
        ctx = B.contexte(b); pg = B.ouvre(ctx, F); desc[cas] = prepare(pg, cas); M[cas].append(tenir(pg)); ctx.close()
    print('   A : %s\n   B : %s' % (desc['A'], desc['B']))
    for cas in 'AB':
        for m in M[cas]: print('   %s : départ %s · descente finie %s · repos %s ms · %d images · forme %s · statut %s' % (cas, *(round(m[k]) if m[k] is not None else None for k in ('dep', 'desc', 'repos')), m['n'], m['forme'], m['st']))
    juge('R4 · les deux paroles diffèrent bien sur tout (à soi / à Rachel · un jour / demain · 3 / 30 mots · sans / dans un Cercle)',
         desc['A']['qui'] == 'moi' and desc['B']['qui'] == 'Rachel' and desc['A']['titre'] == 3 and desc['B']['titre'] == 30 and not desc['A']['nuee'] and desc['B']['nuee'] == 'famille' and desc['B']['due'] == 1,
         '%s · %s' % (desc['A'], desc['B']))
    juge('R4 · la même séquence pour les deux : le rideau part, descend jusqu\'à la barre sans remonter, remonte, s\'en va ; la parole est tenue',
         all(m['forme'] and m['st'] == 'tenu' and None not in (m['dep'], m['desc'], m['repos']) for c in 'AB' for m in M[c]))
    med = {c: {k: statistics.median([m[k] for m in M[c] if m[k] is not None] or [0]) for k in ('dep', 'desc', 'repos')} for c in 'AB'}
    ec = {k: abs(med['A'][k] - med['B'][k]) for k in ('dep', 'desc', 'repos')}
    rel = 'écarts A/B : départ %.0f · descente %.0f · repos %.0f ms ; mouvement (lever → barre) A %.0f / B %.0f ms' % (ec['dep'], ec['desc'], ec['repos'], med['A']['desc'], med['B']['desc'])
    if CHARGE >= 4:
        print('--  R4 · durées NON JUGÉES (charge du Mac %.1f ≥ 4, C-137) — relevé : %s' % (CHARGE, rel))
    else:
        juge('R4 · invariance : chaque instant à 16 ms près entre A et B ; le mouvement (du lever au rideau à la barre) ≤ 1 000 ms', max(ec.values()) <= 16 and max(med['A']['desc'], med['B']['desc']) <= 1000, rel)
    if not R4_SEUL:
        # ── H · le crochet
        h = M['A'][0]['hap']
        juge('H · promiHaptique(\'tenir\') est appelé une fois, au lever, avant la première image du rideau', len(h) == 1 and h[0][1] == 'tenir' and M['A'][0]['img0'] is not None and h[0][0] <= M['A'][0]['img0'] and h[0][0] - M['A'][0]['lev'] < 60,
             'appels %s · lever → appel %s ms' % ([x[1] for x in h], round(h[0][0] - M['A'][0]['lev']) if h else '—'))
        # ── RM · « Réduire les animations »
        ctx = B.contexte(b); pg = B.ouvre(ctx, F); pg.emulate_media(reduced_motion='reduce'); prepare(pg, 'A')
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
        pg.evaluate("""()=>{ window.__rm=[]; window.__hap=[]; const hp=window.promiHaptique; window.promiHaptique=function(n){ window.__hap.push(n); if(hp) return hp.apply(this, arguments); };
          window.__lever=0; document.addEventListener('touchend', ()=>{ if(!window.__lever) window.__lever=performance.now(); }, {capture:true, once:true});
          (function f(){ const dp=document.getElementById('detailPoster'); let mid=0, an=0;
            const mids={}; let ix=0; dp.querySelectorAll('*').forEach(e=>{ ix++; const c=getComputedStyle(e); const o=+c.opacity; if(o>0.02 && o<0.98 && c.visibility!=='hidden' && c.display!=='none' && e.getBoundingClientRect().width>2) mids[(e.id||e.className||e.tagName)+'#'+ix]=+o.toFixed(3); }); mid=mids;
            try{ an=dp.getAnimations({subtree:true}).filter(a=>a.playState==='running' && !(a.effect && a.effect.getTiming && a.effect.getTiming().iterations===Infinity)).length; }catch(e){}
            const sig=[...dp.classList].filter(c=>/^(f-|inst-)/.test(c)).sort().join(' ')+'|'+(window._instant||'')+'|'+(document.getElementById('dptQuand')||{}).textContent;
            window.__rm.push([performance.now(), sig, !!document.getElementById('tenirMaree'), mid, an]); if(window.__rm.length<400) requestAnimationFrame(f); })(); }""")
        z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
        y = z[1] + z[3] * 0.45; B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(3500)
        d = pg.evaluate("()=>({rm:window.__rm, lev:window.__lever, st:promises[promises.length-1].status, hap:window.__hap})")
        i0 = max([i for i, x in enumerate(d['rm']) if x[0] < d['lev']] or [0]); apres = d['rm'][i0:]   # depuis la dernière image AVANT le lever
        sigs = [x[1] for x in apres]; chg = sum(1 for a, b_ in zip(sigs, sigs[1:]) if a != b_)
        juge('RM · mouvement réduit : la parole est tenue, sans rideau ni instant (aucune couche, aucun « juste après »)', d['st'] == 'tenu' and not any(x[2] for x in apres) and not any('inst-' in s for s in sigs),
             'statut %s · images avec rideau %d · états vus %s' % (d['st'], sum(1 for x in apres if x[2]), sorted(set(sigs))[:4]))
        # un FONDU : une opacité intermédiaire qui CHANGE d'une image à l'autre (un aplat fixe du dessin à 0,62 n'en est pas un)
        vals = {}
        for x in apres:
            for k_, v_ in (x[3] or {}).items(): vals.setdefault(k_, set()).add(v_)
        fondus = sorted(k_ for k_, s_ in vals.items() if len(s_) > 1)
        juge('RM · un seul changement de l\'aspect de la fiche, sans fondu (aucune opacité qui varie, aucune animation en cours)', chg == 1 and not fondus and max([x[4] for x in apres] or [0]) == 0,
             'changements %d · fondus %s · animations au pire %d · %d images · aplats fixes à demi-opacité : %s' % (chg, fondus[:4], max([x[4] for x in apres] or [0]), len(apres), sorted(set(k_.split('#')[0] for k_ in vals))[:5]))
        juge('RM · le crochet haptique est appelé aussi (le moment a lieu, sans mouvement)', d['hap'] == ['tenir'], d['hap'])
        ctx.close()
    b.close()
    # ── LT · tâches longues, Chromium, vrai GPU, sous les mondes les plus coûteux
    if not R4_SEUL:
        if CHARGE >= 4:
            print('--  LT · tâches longues NON JUGÉES (charge du Mac %.1f ≥ 4, C-137)' % CHARGE)
        else:
            c = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
            pire = []
            for monde in ('touffe', 'madrure', 'ramage'):
                ctx = B.contexte(c); pg = B.ouvre(ctx, F); pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }", monde); pg.wait_for_timeout(1500); prepare(pg, 'A')
                pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
                pg.evaluate("()=>{ window.__lt=[]; window.__lever=0; document.addEventListener('touchend', ()=>{ if(!window.__lever) window.__lever=performance.now(); }, {capture:true, once:true}); new PerformanceObserver(l=>{ l.getEntries().forEach(e=>window.__lt.push([e.startTime, e.duration])); }).observe({entryTypes:['longtask']}); }")
                z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
                y = z[1] + z[3] * 0.45; B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(3500)
                d = pg.evaluate("()=>({lt:window.__lt, lev:window.__lever})")
                seq = [round(du) for st, du in d['lt'] if d['lev'] <= st <= d['lev'] + 2800]
                pire.append((monde, max(seq or [0]), seq)); ctx.close()
            c.close()
            juge('LT · aucune tâche longue au-delà de 50 ms pendant la séquence (Touffe, Madrure, Ramage ; Chromium, vrai GPU)', all(x[1] <= 50 for x in pire), ' · '.join('%s %s' % (m, s) for m, _, s in pire))
ok = sum(res); print('\n%d / %d   (charge %.1f)' % (ok, len(res), CHARGE))
sys.exit(0 if ok == len(res) else 1)
