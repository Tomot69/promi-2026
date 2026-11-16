"""⚑ v204 (Tom, C-282 refait) — À LA PREMIÈRE LETTRE, L'EXEMPLE GARDE SON DÉTRACÉ STANDARD ; SEULES LES LETTRES SOUS LE TEXTE TAPÉ PARTENT PLUS VITE.
« Le détracé de l'exemple reprend sa durée et son sens standard (Atkinson, de la fin vers le début). Seules les lettres de l'exemple qui se trouvent sous le texte tapé
et sous le curseur disparaissent plus vite : par le même détracé, accéléré et amorti (≈ 150 ms), au fur et à mesure que le texte tapé avance sur elles. Aucune lettre ne
disparaît d'un coup. La lettre tapée paraît immédiatement et ne recouvre jamais une lettre de l'exemple. Même code pour l'onboarding et la page +. Juge : durée totale du
détracé égale au standard ; seules les lettres sous le texte tapé partent plus vite ; aucune lettre n'a d'image où elle passe d'entière à absente ; aucun chevauchement à
aucune image ; première lettre à 0, 50, 150 et 400 ms, puis 5 lettres rapides. » (L'original de v203 : sauvegardes/redteam_premiere-avant-v204.py.)
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé. Onboarding (la parole) et page + d'un Promi (le titre), ×4 délais. Relevé dans la page, APRÈS chaque peinture :
le texte tapé (ses boîtes), les découpes des deux copies (`.v203-exw` : la grande, `.v204-vite` : les petites), les petites copies (`.v204-l`) et l'encre de chaque canevas.
  A · la lettre tapée est dans la place à l'image qui suit la touche
  B · à chaque image, aucune lettre tapée (ni le curseur) ne recouvre une lettre de l'exemple encore montrée : là où elles se croisent, les deux copies sont retirées
  C · le détracé de la grande copie a la durée d'un tracé standard du même texte (± 15 %), sans accélération
  D · les petites copies : seulement des lettres atteintes par la frappe (au plus les lettres tapées + 2), chacune prévue en 100 à 220 ms (≈ 150), au plus 350 ms réelles (le départ d'un tracé — sa mesure, sa première image — compris)
  E · une lettre qui quitte la grande copie est, à cette image-là, portée par sa petite copie (aucune lettre ne saute)
  F · chaque petite copie s'éteint par un détracé AMORTI mené jusqu'au bout, jamais coupé (sa dernière image ≈ 5 % de son encre : la courbe 1 − (1 − p)², pas ≤ 34 ms)
--sonde (la grande copie détracée deux fois plus vite, comme en v203 clôture : C rougit) · --fichier="""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__P={traces:[]}; (function a(){ const T=window.TraceLettres; if(!T||!T.trace){ setTimeout(a,50); return; } if(T.__p) return; T.__p=1; const o=T.trace;
  T.trace=function(el, c, op){ const r=o.apply(this, arguments); try{ if(!(op&&op.preparer) && el && el.closest && (el.closest('.v203-ex') || el.closest('.v204-vite') || el.closest('#onbPh .onbv-pm, #csPhrase [data-ph=titre]'))){ const rec={t:performance.now(), inv:!!(op&&op.inverse), ex:!!(el.closest&&el.closest('.v203-ex')), vite:!!(el.classList&&el.classList.contains('v204-l')), vit:(op&&op.vitesse)||1, am:!!(op&&op.amorti), n:(el.textContent||'').length};
      window.__P.traces.push(rec); if(r && r.fin) r.fin.then((z)=>{ rec.fin=performance.now(); rec.int=!!(z&&z.interrompu); rec.prevu=r.mesure&&r.mesure.prevu; rec.reel=r.mesure&&r.mesure.reel; }); } }catch(e){} return r; }; })(); })();"""
SONDE = r"""(()=>{ (function a(){ const T=window.TraceLettres; if(!T||!T.trace){ setTimeout(a,50); return; } if(T.__s) return; T.__s=1; const o=T.trace; T.trace=function(el, c, op){ if(op && op.inverse && el && el.classList && el.classList.contains('v203-ex')) op=Object.assign({}, op, {vitesse:2, amorti:true}); return o.call(this, el, c, op); }; })(); })();"""   # le détracé de v203 clôtureupe (aucune zone retirée)
REC = r"""(sel)=>{ window.__I=[]; window.__K=null; document.addEventListener('input', function k(){ if(window.__K==null) window.__K=performance.now(); }, true);
  const k=(window.__sc||1), t0=performance.now(), mc=new MessageChannel(); mc.port1.onmessage=()=>lis(); function f(){ mc.port2.postMessage(0); }
  function trous(w){ if(!w) return []; const cp=getComputedStyle(w).clipPath||'', W=w.getBoundingClientRect(), H=[], re=/M\s*([-\d.]+)\s+([-\d.]+)\s+H\s*([-\d.]+)\s+V\s*([-\d.]+)/g; let m;
    while((m=re.exec(cp))){ if(+m[1]<=-9999) continue; H.push([W.left+(+m[1])*k, W.top+(+m[2])*k, W.left+(+m[3])*k, W.top+(+m[4])*k, +m[1], +m[2]]); } return H; }
  function encre(cv){ if(!cv || !cv.width) return null; try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>40) n++; return n; }catch(e){ return null; } }
  function lis(){ const now=performance.now(), w=document.querySelector('.v203-exw:not(.v204-vite)'), wv=document.querySelector('.v204-vite'), pl=document.querySelector(sel);
    let tb=null; if(pl){ const Q=[], tw=document.createTreeWalker(pl, NodeFilter.SHOW_TEXT), rg=document.createRange(); let n; while((n=tw.nextNode())){ const t=n.nodeValue||''; for(let q=0;q<t.length;q++){ if(/\s/.test(t[q])) continue; rg.setStart(n,q); rg.setEnd(n,q+1); const r=rg.getBoundingClientRect(); if(r.width>0.3) Q.push(r); } }
      pl.querySelectorAll('.ph-caret').forEach(c=>{ const r=c.getBoundingClientRect(); if(r.width>0.3) Q.push(r); }); if(Q.length) tb=Q.map(q=>[q.left,q.top,q.right,q.bottom]); }   /* chaque lettre tapée et le curseur */
    const ls=wv?[...wv.querySelectorAll('.v204-l')].map((s,i)=>{ if(!s.__id) s.__id=Math.random().toString(36).slice(2,7); const r=s.getBoundingClientRect(), cv=s.nextElementSibling&&s.nextElementSibling.tagName==='CANVAS'?s.nextElementSibling:null; return {id:s.__id, r:[r.left,r.top,r.right,r.bottom], ink:cv?encre(cv):'dom', n:(s.textContent||'').length}; }):[];
    const cvm=w?w.querySelector('canvas[data-trace]'):null;
    const exl=[]; const gx=w?w.querySelector('.v203-ex'):null; if(gx){ const tw=document.createTreeWalker(gx, NodeFilter.SHOW_TEXT), rg=document.createRange(); let n; while((n=tw.nextNode())){ const t=n.nodeValue||''; for(let q=0;q<t.length;q++){ if(/\s/.test(t[q])) continue; rg.setStart(n,q); rg.setEnd(n,q+1); const r=rg.getBoundingClientRect(); if(r.width>0.3) exl.push([r.left,r.top,r.right,r.bottom]); } } }
    window.__I.push({t:now, w:!!w, exl:exl, H:trous(w), Hv:trous(wv), ls:ls, ink:encre(cvm), tb:tb, txt:pl?(pl.textContent||'').trim().slice(0,12):''});
    if(now-t0<3500) requestAnimationFrame(f); } requestAnimationFrame(f); }"""
def scenario(pg, sel, champ, ouvrir, delai, nom):
    for _ in range(4):
        if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
        ouvrir(); pg.wait_for_timeout(900)
    # l'exemple vient de se tracer : on l'efface en tapant, puis on attend la fin de son retour
    n0 = pg.evaluate("()=>window.__P.traces.filter(x=>!x.inv && !x.ex).length")
    pg.keyboard.press('x'); pg.wait_for_timeout(500); pg.keyboard.press('Backspace')
    pg.wait_for_function("(n)=>{ const t=window.__P.traces.filter(x=>!x.inv && !x.ex); return t.length>n && t[t.length-1].fin; }", arg=n0, timeout=8000)   # l'exemple revenu : son tracé standard, FINI
    pg.wait_for_timeout(delai)
    std = pg.evaluate("()=>{ const t=window.__P.traces.filter(x=>!x.inv && !x.ex); return t[t.length-1].prevu; }")
    n1 = pg.evaluate("()=>window.__P.traces.length")
    pg.evaluate("()=>{ window.__sc=(document.getElementById('device').getBoundingClientRect().width/390)||1; }")   # l'échelle de l'appareil : la découpe est en pt
    pg.evaluate(REC, sel); pg.keyboard.press('m'); pg.wait_for_timeout(16); pg.keyboard.type('arche', delay=35); pg.wait_for_timeout(2600)
    I = pg.evaluate("()=>window.__I"); K = pg.evaluate("()=>window.__K")
    TR = pg.evaluate("()=>window.__P.traces")[n1:]
    ex = [x for x in TR if x['ex'] and x['inv']][:1]; vite = [x for x in TR if x['vite']]
    apres = [x for x in I if K and x['t'] >= K]
    a_ok = bool(apres) and apres[0]['txt'].startswith('m')
    dedans = lambda r, H: any(r[0] >= h[0] - 0.5 and r[1] >= h[1] - 0.5 and r[2] <= h[2] + 0.5 and r[3] <= h[3] + 0.5 for h in H)
    mauvais = []
    for x in apres:
        if not x['w'] or not x['tb']: continue
        # une lettre tapée ne recouvre aucune lettre de l'exemple encore montrée : chaque point de leur intersection est dans un trou (grande copie : ses lettres ;
        # petites copies : leurs boîtes) — échantillonné tous les 1 pt
        def recouvre(tb, boites, H):
            for L in boites:
                x0, y0, x1, y1 = max(tb[0], L[0]), max(tb[1], L[1]), min(tb[2], L[2]), min(tb[3], L[3])
                if x1 - x0 < 1 or y1 - y0 < 1: continue
                yy = y0 + 0.5
                while yy < y1:
                    xx = x0 + 0.5
                    while xx < x1:
                        if not any(h[0] <= xx <= h[2] and h[1] <= yy <= h[3] for h in H): return [round(v) for v in L]
                        xx += 1
                    yy += 1
            return None
        for tb in x['tb']:
            r1 = recouvre(tb, x.get('exl') or [], x['H']); r2 = recouvre(tb, [l['r'] for l in x['ls']], x['Hv'])
            if r1 or r2: mauvais.append((round(x['t'] - K), [round(v) for v in tb], 'grande' if r1 else 'petite', r1 or r2)); break
    juge('[%s · %d ms] A · la lettre tapée tout de suite' % (nom, delai), a_ok, apres[0]['txt'] if apres else None)
    juge('[%s · %d ms] B · à chaque image, aucune lettre tapée ne recouvre une lettre de l\'exemple encore montrée' % (nom, delai), not mauvais and any(x['w'] for x in apres), mauvais[:3])
    if ex and ex[0].get('prevu') and std:
        juge('[%s · %d ms] C · le détracé de l\'exemple a la durée standard (%s ms pour %s), sans accélération' % (nom, delai, ex[0]['prevu'], std), abs(ex[0]['prevu'] - std) <= 0.15 * std and ex[0]['vit'] == 1)
    else: juge('[%s · %d ms] C · le détracé relevé' % (nom, delai), False, {'ex': ex, 'std': std})
    nv = sum(x['n'] for x in vite); dur = [round(x['fin'] - x['t']) for x in vite if x.get('fin')]; prv = [x.get('prevu') for x in vite]
    juge('[%s · %d ms] D · seules les lettres atteintes partent vite (%d lettres, au plus 2 × 6 + 2 : une lettre de l’exemple peut être plus étroite qu’une lettre tapée), prévue en 100 à 220 ms, au plus 350 ms départ compris (réel %s · prévu %s)' % (nom, delai, nv, dur, prv), 0 < nv <= 14 and dur and all(p_ and 100 <= p_ <= 220 for p_ in prv) and all(d <= 350 for d in dur) and len(dur) == len(vite))
    sautes = []; prevH = []
    for x in apres:
        if not x['w']: prevH = []; continue
        tbs = x['tb'] or []
        neufs = [h for h in x['H'] if not any(abs(h[4] - p[4]) < 1.5 and abs(h[5] - p[5]) < 1.5 for p in prevH) and not any(abs(h[0] - (t[0] - 0.6 * (x.get('k') or 1))) < 2.5 and abs(h[1] - t[1]) < 2.5 for t in tbs)]
        for h in neufs:   # un trou neuf de la grande copie (une lettre qui la quitte) : une petite copie la porte à cette image
            lig = sorted([l['r'] for l in x['ls'] if abs((l['r'][1] + l['r'][3]) / 2 - (h[1] + h[3]) / 2) < (h[3] - h[1])])   # les petites copies de sa ligne : leur réunion couvre la lettre (2,5 pt : la boîte d'une lettre contre l'avance du texte)
            cx = h[0] + 2.5
            for r_ in lig:
                if r_[0] <= cx + 0.5 and r_[2] > cx: cx = r_[2]
            if cx < h[2] - 2.5 and not dedans(h, [[t[0] - 2.5, t[1] - 2.5, t[2] + 2.5, t[3] + 2.5] for t in tbs]):
                sautes.append((round(x['t'] - K), [round(v) for v in h], [[round(v) for v in l['r']] for l in x['ls']][:3]))
        prevH = x['H']
    juge('[%s · %d ms] E · une lettre qui quitte la grande copie est portée par sa petite copie (aucune ne saute)' % (nom, delai), not sautes, sautes[:3])
    mal = [x for x in vite if not (x['inv'] and x['am']) or x.get('int') or not x.get('fin')]
    juge('[%s · %d ms] F · chaque petite copie s\'éteint par un détracé amorti mené jusqu\'au bout, jamais coupé (%d)' % (nom, delai, len(vite)), vite and not mal, mal[:2])
    for _ in range(6): pg.keyboard.press('Backspace'); pg.wait_for_timeout(40)
    pg.wait_for_timeout(2500)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_premiere — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    for lieu in ('onboarding', 'page +'):
        if lieu == 'onboarding':
            ctx = B.contexte(b, onb=False, guide=False)
        else:
            ctx = B.contexte(b); B.toile_pleine(ctx, 10)
        ctx.add_init_script(CLAV); ctx.add_init_script(INIT)
        if '--sonde' in A_: ctx.add_init_script(SONDE)
        pg = B.ouvre(ctx, F, attente=7000)
        if lieu == 'onboarding':
            B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000); B.attend_parole(pg)
            sel, champ, ouvrir = '#onbPh .onbv-pm[data-onb=parole]', 'onbIn', (lambda: B.tap_sel(pg, '#onbPh [data-onb="parole"]'))
        else:
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
            sel, champ, ouvrir = '#csPhrase [data-ph=titre]', 'phIn', (lambda: B.tap_sel(pg, '#csPhrase [data-ph=titre]'))
        for d in ([int(x) for x in A_[A_.index('--delais')+1].split(',')] if '--delais' in A_ else (0, 50, 150, 400)): scenario(pg, sel, champ, ouvrir, d, lieu)
        ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
