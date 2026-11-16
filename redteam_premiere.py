"""⚑ v205 (Tom, C-282 : « beaucoup trop lent ; le texte disparaît direct quand on commence à taper — pas sec, mais smooth rapide ») — À LA PREMIÈRE LETTRE,
LE TEXTE D'EXEMPLE PART EN ENTIER, D'UN SEUL GESTE RAPIDE ET DOUX.
« Toutes ses lettres en même temps, en environ 150 ms, avec une sortie amortie. Ni le détracé standard, ni une lettre après l'autre, ni une disparition d'un coup.
L'encart en pointillés reste : il se resserre en douceur, puis s'adapte en douceur à la largeur du texte tapé. La lettre tapée paraît immédiatement, posée au-dessus
de l'exemple qui s'efface. Même code pour l'onboarding et la page +. Juge : toutes les lettres de l'exemple ont disparu 150 ms (± 20) après la première frappe, avec
une opacité décroissante à chaque image, sans saut. Largeur de l'encart continue. Première lettre visible à l'image qui suit la frappe. »
(Les originaux : sauvegardes/redteam_premiere-avant-v205.py, -avant-v204.py.)
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé. Onboarding (la parole) et page + d'un Promi (le titre) ; la première lettre 0, 50, 150 et 400 ms après la fin
du retour de l'exemple, puis 5 lettres rapides. Relevé dans la page, APRÈS chaque peinture : la copie de l'exemple (`.v203-ex`, son opacité calculée), ses trous, le
texte tapé (ses boîtes), la largeur de l'encart.
  A · la lettre tapée est dans la place à l'image qui suit la touche
  B · la copie de l'exemple : sa dernière image visible ≤ 170 ms après la touche, la première sans elle ≥ 130 ms (150 ± 20)
  C · son opacité baisse à CHAQUE image depuis la touche (la première image après la touche déjà < 0,98), sans saut (au plus 0,40 par image de ≤ 20 ms)
  D · toutes ses lettres ensemble : une seule copie, aucun détracé ni aucune petite copie (aucun `TraceLettres.trace` sur l'exemple, aucune `.v204-l`)
  E · la largeur de l'encart est continue : au plus 6 pt/ms entre deux images à moins de 40 ms — une transition de cette page n'y arrive pas (au plus ≈ 4), un saut de l'encart en une image (≈ 11) le dépasse ; une transition suit l'horloge : une image longue avance d'autant
  F · la lettre tapée est posée au-dessus : à chaque image, chaque lettre tapée (et le curseur) est dans un trou de la copie
--sonde (l'exemple retiré d'un coup) : B et C rougissent · --sonde-largeur (l'encart vu deux fois plus large pendant deux images) : E rougit · --fichier= · --delais 0,50"""
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
  T.trace=function(el, c, op){ const r=o.apply(this, arguments); try{ if(!(op&&op.preparer) && el && el.closest && (el.closest('.v203-ex') || el.closest('#onbPh .onbv-pm, #csPhrase [data-ph=titre]'))){ const rec={t:performance.now(), inv:!!(op&&op.inverse), ex:!!el.closest('.v203-ex')};
      window.__P.traces.push(rec); if(r && r.fin) r.fin.then((z)=>{ rec.fin=performance.now(); }); } }catch(e){} return r; }; })(); })();"""
SONDE = r"""(()=>{ window.__sondePrem=1; })();"""   # l'exemple part d'un coup (un crochet de premiere())
SONDE_L = r"""(()=>{ let fait=0; document.addEventListener('input', ()=>{ if(fait) return; fait=1; setTimeout(()=>{ let n=0; const S='#csPhrase [data-ph=titre], #onbPh .onbv-pm[data-onb=parole]'; (function f(){ const e=document.querySelector(S); if(e){ if(n<3){ e.style.setProperty('transform','scaleX(1.8)','important'); e.style.setProperty('transform-origin','0 0','important'); } else e.style.removeProperty('transform'); } if(n++<3) requestAnimationFrame(f); })(); }, 80); }, true); })();"""   # l'encart sans transition : sa largeur saute   # l'encart sans transition : sa largeur saute
REC = r"""(sel)=>{ window.__I=[]; window.__K=null; document.addEventListener('input', function k(){ if(window.__K==null) window.__K=performance.now(); }, true);
  const k=(window.__sc||1), t0=performance.now(), mc=new MessageChannel(); mc.port1.onmessage=()=>lis(); function f(){ mc.port2.postMessage(0); }
  function trous(w){ if(!w) return []; const cp=getComputedStyle(w).clipPath||'', W=w.getBoundingClientRect(), H=[], re=/M\s*([-\d.]+)\s+([-\d.]+)\s+H\s*([-\d.]+)\s+V\s*([-\d.]+)/g; let m;
    while((m=re.exec(cp))){ if(+m[1]<=-9999) continue; H.push([W.left+(+m[1])*k, W.top+(+m[2])*k, W.left+(+m[3])*k, W.top+(+m[4])*k]); } return H; }
  function lis(){ const now=performance.now(), w=document.querySelector('.v203-exw'), gx=w?w.querySelector('.v203-ex'):null, pl=document.querySelector(sel);
    let tb=null; if(pl){ const Q=[], tw=document.createTreeWalker(pl, NodeFilter.SHOW_TEXT), rg=document.createRange(); let n; while((n=tw.nextNode())){ const t=n.nodeValue||''; for(let q=0;q<t.length;q++){ if(/\s/.test(t[q])) continue; rg.setStart(n,q); rg.setEnd(n,q+1); const r=rg.getBoundingClientRect(); if(r.width>0.3) Q.push(r); } }
      pl.querySelectorAll('.ph-caret').forEach(c=>{ const r=c.getBoundingClientRect(); if(r.width>0.3) Q.push(r); }); if(Q.length) tb=Q.map(q=>[q.left,q.top,q.right,q.bottom]); }
    const vu=!!(gx && gx.getClientRects().length && getComputedStyle(gx).visibility!=='hidden'), op=vu?+getComputedStyle(gx).opacity:null, D=document.getElementById('device').getBoundingClientRect(), kd=D.width/390;
    window.__I.push({t:now, w:vu, op:op, nex:document.querySelectorAll('.v203-ex').length, nl:document.querySelectorAll('.v204-l').length, H:trous(w), tb:tb, lw:pl?pl.getBoundingClientRect().width/kd:null, txt:pl?(pl.textContent||'').trim().slice(0,12):''});
    if(now-t0<3000) requestAnimationFrame(f); } requestAnimationFrame(f); }"""
def scenario(pg, sel, champ, ouvrir, delai, nom):
    for _ in range(4):
        if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
        ouvrir(); pg.wait_for_timeout(900)
    # l'exemple vient de se tracer : on l'efface en tapant, puis on attend la fin de son retour (son tracé, inchangé)
    n0 = pg.evaluate("()=>window.__P.traces.filter(x=>!x.inv && !x.ex).length")
    pg.keyboard.press('x'); pg.wait_for_timeout(500); pg.keyboard.press('Backspace')
    try: pg.wait_for_function("(n)=>{ const t=window.__P.traces.filter(x=>!x.inv && !x.ex); return t.length>n && t[t.length-1].fin; }", arg=n0, timeout=8000)
    except Exception: juge('[%s · %d ms] l’exemple revient par son tracé' % (nom, delai), False); return
    pg.wait_for_timeout(delai)
    n1 = pg.evaluate("()=>window.__P.traces.length")
    pg.evaluate("()=>{ window.__sc=(document.getElementById('device').getBoundingClientRect().width/390)||1; }")
    pg.evaluate(REC, sel); pg.keyboard.press('m'); pg.wait_for_timeout(16); pg.keyboard.type('arche', delay=35); pg.wait_for_timeout(2400)
    I = pg.evaluate("()=>window.__I"); K = pg.evaluate("()=>window.__K"); TR = pg.evaluate("()=>window.__P.traces")[n1:]
    apres = [x for x in I if K and x['t'] >= K]
    a_ok = bool(apres) and apres[0]['txt'].startswith('m')
    vis = [x for x in apres if x['w'] and (x['op'] or 0) > 0.02]; gone = [x for x in apres if not x['w'] or (x['op'] or 0) <= 0.02]
    t_last = round(vis[-1]['t'] - K) if vis else None; t_gone = round(gone[0]['t'] - K) if gone else None
    b_ok = t_gone is not None and t_gone >= 130 and (t_last is None or t_last <= 170)
    sauts = []; prev = None; prevt = K
    for x in apres:
        if not x['w']: break
        if prev is None and x['op'] >= 0.98: sauts.append(('première image à %.2f' % x['op'], round(x['t'] - K)))
        if prev is not None:
            if x['op'] >= prev - 1e-4 and prev > 0.02: sauts.append(('ne baisse pas', round(x['t'] - K), round(prev, 3), round(x['op'], 3)))
            if x['t'] - prevt <= 20 and prev - x['op'] > 0.40: sauts.append(('saut', round(x['t'] - K), round(prev, 3), round(x['op'], 3)))
        prev = x['op']; prevt = x['t']
    juge('[%s · %d ms] A · la lettre tapée à l’image qui suit la touche' % (nom, delai), a_ok, apres[0]['txt'] if apres else None)
    juge('[%s · %d ms] B · l’exemple parti en 150 ± 20 ms (dernière image visible %s ms, première sans lui %s ms)' % (nom, delai, t_last, t_gone), b_ok)
    juge('[%s · %d ms] C · son opacité baisse à chaque image, sans saut' % (nom, delai), bool(vis) and not sauts, sauts[:3])
    ex_tr = [x for x in TR if x['ex']]
    juge('[%s · %d ms] D · toutes ses lettres ensemble (une copie, aucun détracé, aucune petite copie)' % (nom, delai), not ex_tr and all(x['nex'] <= 1 and x['nl'] == 0 for x in apres), {'traces': len(ex_tr), 'copies': max([x['nex'] for x in apres] or [0]), 'petites': max([x['nl'] for x in apres] or [0])})
    lw = [(x['t'], x['lw']) for x in apres if x['lw'] is not None]
    # la vitesse, pas le pas d'une image (une transition suit l'horloge : sur une image longue elle avance d'autant) — entre deux images à moins de 40 ms
    vit = [abs(lw[i][1] - lw[i - 1][1]) / max(1, lw[i][0] - lw[i - 1][0]) for i in range(1, len(lw)) if lw[i][0] - lw[i - 1][0] <= 40]
    vmax = max(vit or [0]); longues = sum(1 for i in range(1, len(lw)) if lw[i][0] - lw[i - 1][0] > 40)
    juge('[%s · %d ms] E · la largeur de l’encart est continue (au plus 6 pt/ms : %.2f ; %d image(s) de plus de 40 ms non jugée(s))' % (nom, delai, vmax, longues), vmax <= 6)
    if vmax > 6: print('     largeurs :', [(round(t - K), round(w, 1)) for t, w in lw][:24])
    hors = []
    for x in apres:
        if not x['w'] or not x['tb'] or (x['op'] or 0) <= 0.02: continue
        for tb in x['tb']:
            if not any(tb[0] >= h[0] - 0.5 and tb[1] >= h[1] - 0.5 and tb[2] <= h[2] + 0.5 and tb[3] <= h[3] + 0.5 for h in x['H']): hors.append((round(x['t'] - K), [round(v) for v in tb])); break
    juge('[%s · %d ms] F · la lettre tapée posée au-dessus de l’exemple (dans un trou de la copie, à chaque image)' % (nom, delai), not hors, hors[:3])
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
        if '--sonde-largeur' in A_: ctx.add_init_script(SONDE_L)
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
