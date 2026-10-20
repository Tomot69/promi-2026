#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_fluide.py — L'ANIMATION « TENIR UNE PAROLE » EST FLUIDE (v124, Tom, 3 oct. 2026). Chromium sur le vrai GPU, @3x.

« Quand on complète le trait, l'animation est saccadée. Même durée, même dessin : elle doit devenir fluide. Juge : il joue l'animation
vingt fois. Aucune image au-delà de 20 ms au banc, p95 ≤ 16,7 ms. »

CE QU'ON MESURE, ET POURQUOI (§7, « choisir la grandeur qui a la forme du défaut ») : la saccade est un fil principal BLOQUÉ. L'intervalle
entre deux `requestAnimationFrame` ne peut pas la juger au banc : page AU REPOS, il donne déjà p95 18,3 ms et un maximum de 26,7 ms
(la cadence d'un navigateur sans écran flotte) — le seuil de 20 ms y serait rouge sans animation. Le TEMPS D'UNE IMAGE est donc le
travail du fil principal pour la produire : la somme des tâches du moteur de rendu (`RunTask` de la trace Chromium : script, style, mise en
page, peinture) entre deux rendus d'image (`AnimationFrame::Render`). Seuils EN DUR : aucune image au-delà de 20 ms ; p95 ≤ 16,7 ms.
⚑ v144 (Tom, 12 oct. 2026, C-111) : « le moment tenir, plus lent » — le champ amande dure 2 000 ms (le double), le contrôle 3 porte cette
valeur EN DUR ; original : sauvegardes/redteam_fluide-avant-v144.py.
L'ANIMATION : du lever du doigt (marque `lever`) à 2 700 ms — « le trait se referme » (le champ amande, 2 000 ms), le passage à « juste
après », et ses reprises (jusqu'à 600 ms plus tard). Ce qui tourne APRÈS (les passes de tout le document, la pose complète) n'est pas
l'animation — « aucun travail lourd pendant l'animation, il passe avant ou après » — mais il est RELEVÉ et affiché.
Vingt fois : on rouvre une parole à tenir, on trace le geste à la souris (CDP), on lève.
  1 · aucune image de l'animation au-delà de 20 ms de travail (sur les vingt) ;
  2 · p95 du travail par image ≤ 16,7 ms ;
  3 · la durée est celle que Tom a décidée : « juste après » paraît 2 150 ms (± 80, v155 C-167) après « le trait se referme » ;
  4 · le dessin est celui d'avant : les deux états paraissent (champ amande puis nature), la parole est tenue.
Preuve (§7) : sur `sauvegardes/app-avant-v124.html` il ROUGIT (images de 400 à 580 ms).
"""
import os, sys, json
from playwright.sync_api import sync_playwright

FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 20))
SEUIL, P95, DUREE = 20.0, 16.7, 2850.0   # ⚑ v155 (Tom, C-167) : 2 150 ms d'amande, l'animation va du lever à 2 850 ms · ⚑ v154 (Tom, C-167) : 2 400 ms d'amande, l'animation va du lever à 3 100 ms · ⚑ v144 (Tom, C-111) : l'instant amande dure 2 000 ms (1 000 avant) — l'animation va du lever à 2 700 ms
AMANDE_DECIDE, FIN_RELEVE = 2150, 4650
# ⚑ v125 (Tom, Q379) : « le travail remis après "tenir" part en tâche de fond, découpée, pour qu'un toucher à cet instant ne soit
# jamais retenu ». De la fin de l'animation à 3,5 s après le lever : aucune TÂCHE du fil principal au-delà de deux images (33,4 ms).
TACHE_APRES = 33.4
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-84s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


def images(trace, debut_nom='lever'):
    ev = trace.get('traceEvents', trace) if isinstance(trace, dict) else trace
    # le fil principal du moteur de rendu de LA page : celui qui porte la marque `lever`
    m = [e for e in ev if e.get('name') == debut_nom and 'ts' in e]
    if not m: return None
    pid, tid, t0 = m[0]['pid'], m[0]['tid'], m[0]['ts']
    taches = sorted((e['ts'], e['ts'] + e.get('dur', 0)) for e in ev if e.get('name') == 'RunTask' and e.get('ph') == 'X' and e.get('pid') == pid and e.get('tid') == tid and e.get('dur', 0) > 0)
    debuts = sorted(set(e['ts'] for e in ev if e.get('name') == 'AnimationFrame::Render' and e.get('pid') == pid and 'ts' in e))
    if len(debuts) < 10: debuts = sorted(set(e['ts'] for e in ev if e.get('name') in ('Commit', 'BeginMainThreadFrame') and e.get('pid') == pid and 'ts' in e))
    debuts = [d for d in debuts if t0 - 20000 <= d]
    out = []
    for a, b in zip(debuts, debuts[1:]):
        w = sum(max(0, min(b, y) - max(a, x)) for x, y in taches if y > a and x < b) / 1000.0
        out.append(((a - t0) / 1000.0, w, (b - a) / 1000.0))
    # la tâche du lever elle-même (le clic) tombe avant la première image qui la suit : elle est comptée dans l'image qui la contient
    return out, t0, taches


with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    cdp = ctx.new_cdp_session(pg)
    toutes = []; pires = []; apres_t = []; etats = 0; apres_max = 0.0; tache_max = 0.0
    for k in range(N):
        pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }" % k)
        pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)      # la fiche posée, au repos (les dalles de l'instant se préparent là)
        r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}")
        y = r['y'] + r['h'] / 2
        pg.evaluate("""()=>{ window.__vu=[]; const dp=document.getElementById('detailPoster'); let av='';
          window.__obs=new MutationObserver(()=>{ const s=dp.classList.contains('inst-referme')?'referme':(dp.classList.contains('inst-apres')?'apres':''); if(s!==av){ av=s; window.__vu.push([s, performance.now()]); } });
          window.__obs.observe(dp,{attributes:true,attributeFilter:['class']});
          document.getElementById('tenirCv').addEventListener('pointerup', ()=>{ performance.mark('lever'); window.__t0=performance.now(); }, {capture:true, once:true});
          window.addEventListener('mouseup', ()=>{ if(!window.__t0){ performance.mark('lever'); window.__t0=performance.now(); } }, {capture:true, once:true}); }""")
        pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
        for i in range(1, 26):
            pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
        b.start_tracing(page=pg, categories=['toplevel', 'devtools.timeline', 'disabled-by-default-devtools.timeline', 'blink.user_timing'] + (['disabled-by-default-v8.cpu_profiler', 'v8'] if '--profil' in sys.argv else []))
        pg.wait_for_timeout(60)
        pg.mouse.up(); pg.wait_for_timeout(4700)
        tr = json.loads(b.stop_tracing().decode('utf-8'))
        d = pg.evaluate("()=>{ try{window.__obs.disconnect()}catch(e){} const o={vu:window.__vu, t0:window.__t0, st:(typeof cur!=='undefined'&&cur)?cur.status:null}; window.__t0=0; return o; }")
        r_ = images(tr)
        if '--qui' in sys.argv and r_:         # v142 (C-102) : sans profileur — ce que la trace dit des tâches trop longues (les appels de fonction et les passes du moteur de rendu qu'elles contiennent)
            ev_ = tr.get('traceEvents', tr); t0_ = r_[1]; pid_ = next(e['pid'] for e in ev_ if e.get('name') == 'lever')
            for x, y in r_[2]:
                rel = (x - t0_) / 1000.0; dur = (y - x) / 1000.0
                if not ((-5 <= rel <= DUREE and dur > SEUIL) or (rel > DUREE and rel < FIN_RELEVE and dur > 33.4)): continue
                dans = [e for e in ev_ if e.get('ph') == 'X' and e.get('pid') == pid_ and e.get('ts', 0) >= x and e.get('ts', 0) + e.get('dur', 0) <= y and e.get('dur', 0) > 2500 and e.get('name') in ('FunctionCall', 'TimerFire', 'FireAnimationFrame', 'EventDispatch', 'Layout', 'UpdateLayoutTree', 'Paint', 'PrePaint', 'Layerize', 'Commit', 'MinorGC', 'MajorGC', 'V8.GC_SCAVENGER', 'V8.GC_MARK_COMPACTOR', 'RunMicrotasks', 'EvaluateScript', 'ParseHTML', 'HitTest', 'IntersectionObserverController::computeIntersections', 'UpdateLayerTree', 'Decode Image', 'ImageDecodeTask')]
                desc = []
                for e in sorted(dans, key=lambda q: -q['dur'])[:6]:
                    d_ = (e.get('args') or {}).get('data') or {}
                    desc.append('%s %.0f ms%s' % (e['name'], e['dur'] / 1000.0, (' ' + (d_.get('functionName') or '?') + '@' + str((d_.get('lineNumber') or 0) + 1)) if e['name'] == 'FunctionCall' else (' ' + str(d_.get('type', ''))) if e['name'] == 'EventDispatch' else ''))
                print('   QUI passe %d · tâche de %.0f ms à %d ms : %s' % (k + 1, dur, rel, ' · '.join(desc)))
        if '--profil' in sys.argv and r_:      # v142 (C-102) : qui fait la longue tâche ? les piles échantillonnées par V8, dans la fenêtre de chaque tâche de plus de 100 ms
            ev_ = tr.get('traceEvents', tr); longues = [(x, y) for x, y in r_[2] if y - x > 100000 and x - r_[1] > -50000]
            if longues:
                nd = {}; par = {}; ech = []
                for e in ev_:
                    if e.get('name') != 'ProfileChunk': continue
                    d_ = e['args']['data']; cp = d_.get('cpuProfile', {}); tt = e.get('ts', 0)
                    for n in cp.get('nodes', []):
                        nd[n['id']] = n['callFrame']
                        if 'parent' in n: par[n['id']] = n['parent']
                    tdl = d_.get('timeDeltas', []); 
                    for s_, dl in zip(cp.get('samples', []), tdl): ech.append((s_, dl))
                # les deltas sont relatifs au début du profil : on reconstruit les dates depuis l'évènement `Profile`
                deb = next((e['args']['data']['startTime'] for e in ev_ if e.get('name') == 'Profile'), None); tcur = deb or 0; cnt = {}
                for s_, dl in ech:
                    tcur += dl
                    if not any(x <= tcur <= y for x, y in longues): continue
                    pile = []; q = s_
                    while q in nd and len(pile) < 8:
                        c = nd[q]; nm = c.get('functionName') or '(anonyme)'
                        if nm not in ('(root)',): pile.append('%s@%s' % (nm, c.get('lineNumber', -1) + 1))
                        q = par.get(q)
                    k_ = ' < '.join(pile); cnt[k_] = cnt.get(k_, 0) + dl
                print('   PROFIL passe %d · tâches longues %s' % (k + 1, [(round((x - r_[1]) / 1000), round((y - x) / 1000)) for x, y in longues]))
                for k_, v_ in sorted(cnt.items(), key=lambda z: -z[1])[:8]: print('      %7.1f ms  %s' % (v_ / 1000.0, k_[:400]))
        if not r_: print('   passe %d : marque « lever » absente de la trace' % (k + 1)); continue
        im, t0, _ = r_
        anim = [(a, w) for a, w, _ in im if -5 <= a <= DUREE]; suite = [(a, w) for a, w, _ in im if a > DUREE]
        toutes += [w for _, w in anim]
        pire = max(anim, key=lambda x: x[1]) if anim else (0, 0); pires.append(pire[1])
        apres_max = max(apres_max, max([w for _, w in suite] or [0]))
        tache_max = max(tache_max, max([(y - x) / 1000.0 for x, y in _ if DUREE * 1000 <= x - t0 <= FIN_RELEVE * 1000] or [0]))
        v = {s: tt - d['t0'] for s, tt in d['vu'] if s and d.get('t0')}
        if 'referme' in v and 'apres' in v: apres_t.append(v['apres'] - v['referme'])
        if d['st'] == 'tenu' and 'referme' in v and 'apres' in v: etats += 1
        if '--liste' in sys.argv or pire[1] > SEUIL:
            print('   passe %2d : %d images · la plus longue %.1f ms à %d ms · au-delà de 20 ms : %s · « referme » à %s ms, « après » à %s ms' % (k + 1, len(anim), pire[1], pire[0], [(round(a), round(w, 1)) for a, w in anim if w > SEUIL][:6], round(v.get('referme', -1)), round(v.get('apres', -1))))
    s = sorted(toutes); p95 = s[int(len(s) * 0.95)] if s else 999; p50 = s[len(s) // 2] if s else 999
    n_long = sum(1 for w in toutes if w > SEUIL)
    t('1 · aucune image de l\'animation au-delà de 20 ms de travail (%d animations, %d images)' % (N, len(toutes)), bool(toutes) and n_long == 0, '%d image(s) au-delà · la plus longue %.1f ms' % (n_long, max(pires or [0])))
    t('2 · p95 du travail par image ≤ 16,7 ms', bool(toutes) and p95 <= P95, 'p50 %.1f · p95 %.1f ms' % (p50, p95))
    t('3 · la durée : « juste après » paraît 2 150 ms (± 80, v155 C-167) après « le trait se referme », et l\'app déclare cette valeur', len(apres_t) == N and all(abs(x - AMANDE_DECIDE) <= 80 for x in apres_t) and pg.evaluate("()=>(window._tenirRegle||{}).AMANDE") == AMANDE_DECIDE, '%s' % ('de %d à %d ms' % (min(apres_t), max(apres_t)) if apres_t else 'non relevée'))
    t('4 · le dessin : les deux états paraissent et la parole est tenue, à chaque fois', etats == N, '%d sur %d' % (etats, N))
    t('5 · après l\'animation (1,7 s → 3,5 s) : aucune tâche au-delà de 33,4 ms — un toucher n\'attend jamais plus de deux images', tache_max > 0 and tache_max <= TACHE_APRES, 'la plus longue : %.1f ms' % tache_max)
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    print('   (après l\'animation, relevé : la plus longue image de travail %.1f ms — les passes de tout le document et la pose complète)' % apres_max)
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
