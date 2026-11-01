#!/usr/bin/env python3
"""redteam_onb_ordre.py — ⚑ v173 (Tom, C-211, C-212) : L'ORDRE DE LA PAGE DE LA PAROLE ; MOINS D'ATTENTE APRÈS « PROMI PLANTÉ ! ».

« “[Prénom], donc.” et “Quid d'un Promi à toi-même ?” arrivent APRÈS la phrase de la parole. Ordre voulu, chaque texte tracé : 1. “[Prénom], donc.” puis “Quid…” ;
2. la phrase de la parole, à compléter ; 3. “Petite ou grande promesse, elle compte.” ; 4. “TRACE POUR PLANTER”, le trait et son départ : ils n'apparaissent
qu'APRÈS que la promesse est complétée, avec la même règle que la page + (C-209) : jamais pendant la frappe, à la fermeture du clavier, libellé tracé, départ et
flèche nés comme dans l'onboarding, départ clignotant jusqu'au premier toucher. Les places restent celles de v172 ; seul l'ordre d'apparition change. »

Banc comme Tom (WebKit, doigt), stockage vierge, le vrai parcours, clavier simulé (`visualViewport`, comme `redteam_clavier_onb`), échelles 1 (390 × 844, l'appareil
à 0,933) et 0,79 (330 × 714), clair et sombre ; v172 servie à côté (`zz-v172.html`) pour les places. Les heures viennent du vrai appel à `TraceLettres.trace`,
la visibilité du style rendu image par image, l'encre de la phrase d'une capture.
  A · chaque texte se trace, dans l'ordre : onbDit · onbQuid · onbPh · onbSous, le suivant après la fin du précédent
  B · tant que son tracé n'a pas commencé, un texte n'est pas visible (style rendu, image par image) ; l'encre de la phrase est absente de l'image pendant « Quid »
  C · la promesse pas complétée (6 s) : ni trait, ni départ, ni libellé ; un toucher là où sera le trait ne plante rien
  D · pendant la frappe : rien, à aucune image
  E · le clavier refermé et posé : l'invite paraît ≤ 300 ms ensuite ; le trait et le départ en flaques (`ouvre`), le libellé TRACÉ ; le départ clignote (promiBlink) en phase avec le I
  F · le premier toucher du trait : le départ reste orange, fixe
  G · la parole effacée : l'invite repart en flaques (`couvre`), puis plus rien ; retapée, elle revient
  H · le trait tracé jusqu'au milieu plante, comme avant
  I · les places (± 0,5 pt) = celles de v172, phrase courte et phrase longue
  J · « Réduire les animations » : tout est posé sans tracé, dans l'ordre de la page ; le trait attend la promesse ; le départ ne clignote pas
  K · C-212 : du plant au titre, et du toucher au paragraphe, plus courts que v172 servie à côté (attendu : 285 et 48 ms ; médiane de trois, le plant lui-même coûte
      quelques centaines de ms, des deux côtés)
Preuve : `--fichier=zz-v172.html` rougit (A, B, C, D, E, G, J).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
REF = 'zz-v172.html'
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
CLAVIER = """(()=>{ const K=336, D=280; let H=innerHeight, h=H; const vv=new EventTarget(); Object.defineProperty(vv,'height',{get:()=>h}); Object.defineProperty(vv,'width',{get:()=>innerWidth});
  Object.defineProperty(vv,'scale',{get:()=>1}); Object.defineProperty(vv,'offsetTop',{get:()=>0}); Object.defineProperty(vv,'pageTop',{get:()=>0});
  try{ Object.defineProperty(window,'visualViewport',{get:()=>vv, configurable:true}); }catch(e){}
  window.__kb={resize:[]}; let anim=0;
  function vers(c){ const h0=h, t0=performance.now(); cancelAnimationFrame(anim);
    (function f(){ const u=Math.min(1,(performance.now()-t0)/D); h=Math.round(h0+(c-h0)*(1-Math.pow(1-u,3))); window.__kb.resize.push([performance.now(), h]); vv.dispatchEvent(new Event('resize')); if(u<1) anim=requestAnimationFrame(f); })(); }
  document.addEventListener('focusin', e=>{ if(e.target && e.target.id==='onbIn') setTimeout(()=>vers(innerHeight-K), 40); }, true);
  document.addEventListener('focusout', e=>{ if(e.target && e.target.id==='onbIn') setTimeout(()=>vers(innerHeight), 30); }, true);
})()"""
SONDE = """()=>{ window.__tr=[]; const T=window.TraceLettres; if(T && !T.__j){ T.__j=1; const tr=T.trace; T.trace=function(c,x,o){ const prep=o&&o.preparer, r=tr.apply(this, arguments); if(!prep){ const q={id:c.id||c.className, t0:performance.now(), t1:0, interrompu:null}; window.__tr.push(q); if(r&&r.fin&&r.fin.then) r.fin.then(v=>{ q.t1=performance.now(); q.interrompu=!!(v&&v.interrompu); }); } return r; }; }
  window.__im=[]; const ids=['onbDit','onbQuid','onbPh','onbSous','onbTrace','onbTrait','onbDepart'];
  (function f(){ const o={t:performance.now()}; ids.forEach(i=>{ const e=document.getElementById(i); if(!e){ o[i]=false; return; } const c=getComputedStyle(e); o[i]=c.display!=='none' && c.visibility!=='hidden'; });
    const fl=[...document.querySelectorAll('#onbV canvas.passage-flaques')].map(k=>k.getAttribute('data-mode')); o.fl=fl; o.dalle=!!document.querySelector('#onbV canvas.onbv-dalle'); window.__im.push(o); if(window.__im.length<9000) requestAnimationFrame(f); })(); }"""
RECTS = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, o={k:k}; ['onbDit','onbQuid','onbPh','onbSous','onbTrace','onbTrait'].forEach(i=>{ const e=document.getElementById(i); if(!e) return; const r=e.getBoundingClientRect(); o[i]=[(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k]; }); return o; }"""
PHASE = """()=>{ const I=document.querySelector('#onbV .onbv-mm i'), d=document.getElementById('onbDepart'); const a=e=>e&&e.getAnimations?e.getAnimations().filter(x=>x.animationName==='promiBlink')[0]:null, A=a(I), Z=a(d);
  return {clig:!!(d&&d.classList.contains('clignote')), anim:d?getComputedStyle(d).animationName:'', ecart:(A&&Z&&A.currentTime!=null&&Z.currentTime!=null)?Math.min(Math.abs((A.currentTime-Z.currentTime)%1150),1150-Math.abs((A.currentTime-Z.currentTime)%1150)):null}; }"""
def debut(b, fichier, vw, vh, sombre=False, clavier=True, reduit=False, nom='Camille'):
    ctx = B.contexte(b, sombre=sombre, onb=False, guide=False, vw=vw, vh=vh)
    if reduit: ctx.add_init_script("(()=>{ const m=window.matchMedia.bind(window); window.matchMedia=q=>/reduced-motion/.test(q)?{matches:true,media:q,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}}:m(q); })()")
    if clavier: ctx.add_init_script(CLAVIER)
    pg = B.ouvre(ctx, fichier, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type(nom, delay=25); pg.wait_for_timeout(400)
    pg.evaluate(SONDE); return ctx, pg
def attend(pg, js, ms=9000):
    for _ in range(int(ms / 60)):
        if pg.evaluate(js): return True
        pg.wait_for_timeout(60)
    return False
def encre_phrase(pg, r):
    """l'encre de la phrase : part des pixels de sa boîte qui s'écartent franchement de la couleur médiane (le fond)"""
    k = r['k']; d = B.dev(pg); x, y, w, h = r['onbPh']
    png = pg.screenshot(clip={'x': d[0] + x * k, 'y': d[1] + y * k, 'width': w * k, 'height': max(10, h * k)})
    im = Image.open(io.BytesIO(png)).convert('RGB'); px = list(im.getdata()); s = sorted(px, key=sum)[len(px) // 2]
    return sum(1 for p in px if abs(p[0] - s[0]) + abs(p[1] - s[1]) + abs(p[2] - s[2]) > 140) / max(1, len(px))
def premier_parcours(b, fichier, vw, vh, sombre, T):
    ctx, pg = debut(b, fichier, vw, vh, sombre)
    r0 = pg.evaluate(RECTS); t_ent = pg.evaluate("()=>performance.now()"); pg.keyboard.press('Enter')
    # A, B
    q_ok = attend(pg, "()=>(window.__tr||[]).some(x=>x.id==='onbQuid')", 6000)
    encre_q = encre_phrase(pg, pg.evaluate(RECTS)) if q_ok else None
    attend(pg, "()=>{ const q=(window.__tr||[]).filter(x=>x.id==='onbSous')[0]; return q&&q.t1>0; }", 9000)
    r_fin = pg.evaluate(RECTS); encre_fin = encre_phrase(pg, r_fin)
    tr = pg.evaluate("()=>window.__tr"); ims = pg.evaluate("()=>window.__im")
    O = ['onbDit', 'onbQuid', 'onbPh', 'onbSous']; par = {}
    for q in tr: par.setdefault(q['id'], q)
    ordre = [q['id'] for q in tr if q['id'] in O]
    suite = all(i in par and par[i]['t1'] > 0 for i in O) and all(par[O[j+1]]['t0'] >= par[O[j]]['t1'] - 5 for j in range(3))
    juge('[%s] A · chaque texte se trace, dans l\'ordre, le suivant après la fin du précédent' % T, ordre == O and suite, ordre)
    trop_tot = {}
    for i in O:
        t0 = par[i]['t0'] if i in par else 1e12
        n = sum(1 for m in ims if m[i] and t_ent + 30 < m['t'] < t0 - 40)
        if n: trop_tot[i] = n
    juge('[%s] B · aucun texte visible avant son tracé, à aucune image' % T, not trop_tot, trop_tot or '%d images' % len(ims))
    juge('[%s] B · pendant « Quid », l\'encre de la phrase n\'est pas sur l\'image' % T, encre_q is not None and encre_q < 0.004 and encre_fin > 0.01, 'encre pendant Quid %s · à la fin %.4f' % (encre_q, encre_fin))
    # C
    pg.wait_for_timeout(6000 if not VITE else 2600); ims = pg.evaluate("()=>window.__im")
    vu = sum(1 for m in ims if m['onbTrait'] or m['onbTrace'] or m['onbDepart'])
    juge('[%s] C · la promesse pas complétée : ni trait, ni départ, ni libellé' % T, vu == 0, '%d images sur %d avec le trait' % (vu, len(ims)))
    nb0 = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
    B.glisse(pg, B.droite([44, r_fin['onbTrait'][1] + 50], [195, r_fin['onbTrait'][1] + 50], 12), pas=14); pg.wait_for_timeout(500)
    a = pg.evaluate("()=>{ const a=document.activeElement; if(a&&a.id==='onbIn') a.blur(); return 1; }"); pg.wait_for_timeout(300)
    juge('[%s] C · un trait tiré là où il sera ne plante rien' % T, pg.evaluate("()=>promises.filter(p=>!p.draft).length") == nb0 and not pg.evaluate("()=>!!document.querySelector('#onbFin[style*=\"block\"]')"))
    # D
    n0 = pg.evaluate("()=>window.__im.length")
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(450); pg.keyboard.type('marcher une heure', delay=45); pg.wait_for_timeout(1200)
    ims = pg.evaluate("n=>window.__im.slice(n)", n0)
    vu = sum(1 for m in ims if m['onbTrait'] or m['onbTrace'] or m['onbDepart'])
    juge('[%s] D · pendant la frappe, le clavier ouvert : rien, à aucune image' % T, vu == 0, '%d images sur %d' % (vu, len(ims)))
    # E
    n0 = pg.evaluate("()=>window.__im.length"); tn = pg.evaluate("()=>performance.now()"); pg.keyboard.press('Enter')
    ok = attend(pg, "()=>{ const t=document.getElementById('onbTrait'); return t&&getComputedStyle(t).display!=='none'; }", 3000)
    pg.wait_for_timeout(120); ph = pg.evaluate(PHASE); pg.wait_for_timeout(1000)
    ims = pg.evaluate("n=>window.__im.slice(n)", n0); kb = pg.evaluate("t=>(window.__kb?window.__kb.resize:[]).filter(x=>x[0]>t).map(x=>x[0])", tn)
    tr2 = [q for q in pg.evaluate("()=>window.__tr") if q['id'] == 'onbTrace']
    t_vu = next((m['t'] for m in ims if m['onbTrait']), None); fin_kb = max(kb) if kb else tn
    juge('[%s] E · après le clavier posé (160 ms), l\'invite paraît ≤ 300 ms ensuite, jamais avant' % T, ok and t_vu is not None and t_vu - fin_kb >= 150 and t_vu - fin_kb <= 160 + 300, 'clavier posé +%s ms · invite +%s ms' % (round(fin_kb - tn), round(t_vu - tn) if t_vu else '—'))
    fl = sum(1 for m in ims if 'ouvre' in (m['fl'] or []))
    juge('[%s] E · le trait et le départ naissent en flaques, le libellé est TRACÉ' % T, fl >= 8 and bool(tr2) and not any(m['onbTrace'] and m['t'] < tr2[0]['t0'] - 40 for m in ims), '%d images de flaques · tracé du libellé %s' % (fl, 'oui' if tr2 else 'non'))
    juge('[%s] E · le départ clignote (promiBlink), en phase avec le I' % T, ph['clig'] and ph['anim'] == 'promiBlink' and ph['ecart'] is not None and ph['ecart'] <= 70, ph)
    # I — les places
    r_ic = pg.evaluate(RECTS)
    # F
    Y = r_ic['onbTrait'][1]; yd = pg.evaluate("()=>{ const t=document.getElementById('onbTrait').getAttribute('data-depart'); return t?parseFloat(t.split(',')[1]):60; }")
    B.glisse(pg, [[44, Y + yd], [46, Y + yd]], pas=20); pg.wait_for_timeout(420)
    ph2 = pg.evaluate(PHASE)
    juge('[%s] F · le premier toucher du trait : le départ reste fixe' % T, not ph2['clig'] and pg.evaluate("()=>getComputedStyle(document.getElementById('onbDepart')).display") != 'none', ph2)
    # G
    n0 = pg.evaluate("()=>window.__im.length")
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(450)
    pg.evaluate("()=>{ const i=document.getElementById('onbIn'); i.value=''; i.dispatchEvent(new Event('input',{bubbles:true})); }"); pg.wait_for_timeout(700)
    ims = pg.evaluate("n=>window.__im.slice(n)", n0); co = sum(1 for m in ims if 'couvre' in (m['fl'] or []))
    juge('[%s] G · la parole effacée : l\'invite repart en flaques, puis plus rien' % T, co >= 5 and not ims[-1]['onbTrait'] and not ims[-1]['onbTrace'] and not ims[-1]['onbDepart'], '%d images de flaques · trait %s' % (co, ims[-1]['onbTrait']))
    pg.keyboard.type('marcher une heure', delay=25); pg.wait_for_timeout(300); pg.keyboard.press('Enter')
    ok = attend(pg, "()=>{ const t=document.getElementById('onbTrait'); return t&&getComputedStyle(t).display!=='none'; }", 3000); pg.wait_for_timeout(1000)
    ph3 = pg.evaluate(PHASE)
    juge('[%s] G · retapée, elle revient, et le départ reclignote' % T, ok and ph3['clig'], ph3)
    # H, K
    pg.evaluate("()=>{ window.__im=window.__im.slice(-5); }"); yd = pg.evaluate("()=>{ const t=document.getElementById('onbTrait').getAttribute('data-depart'); return t?parseFloat(t.split(',')[1]):60; }"); Y = pg.evaluate(RECTS)['onbTrait'][1]
    onde = lambda x: Y + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)
    pts = [[x, onde(x)] for x in range(44, 212, 12)]
    B.glisse(pg, pts, pas=18, tenue=40); ok = attend(pg, "()=>{ const f=document.getElementById('onbFin'); return f&&getComputedStyle(f).display!=='none'; }", 4000)
    juge('[%s] H · le trait tracé plante, « Promi planté ! » paraît' % T, ok and pg.evaluate("()=>promises.filter(p=>!p.draft).length") == nb0 + 1)
    err = [e for e in pg.erreurs if 'version.json' not in e]; juge('[%s] aucune erreur de page' % T, not err, err[:2]); ctx.close()
    return r_ic
def attentes(b, fichier):
    """le plant et le premier toucher, trois fois : la médiane (un chemin court, sans clavier simulé)"""
    A = []
    for _ in range(3):
        ctx, pg = debut(b, fichier, 390, 844, clavier=False); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
        B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=15); pg.keyboard.press('Enter'); pg.wait_for_timeout(1700)
        Y = pg.evaluate(RECTS)['onbTrait'][1]; pts = [[x, Y + pg.evaluate("x=>{ const c=window._onbTraitCotes, y=window._onde.onde(c.base,c.amp); return y(x); }", x)] for x in range(44, 212, 12)]
        B.glisse(pg, pts, pas=18, tenue=40); attend(pg, "()=>(window.__tr||[]).some(x=>/onbv-titre/.test(x.id)&&x.t1>0)", 6000); pg.wait_for_timeout(900)
        tt = next((q for q in pg.evaluate("()=>window.__tr") if 'onbv-titre' in q['id']), None); ims = pg.evaluate("()=>window.__im"); t_pl = next((m['t'] for m in ims if m['dalle']), None)
        pg.evaluate("()=>{ window.__tap=0; window.addEventListener('click',()=>{ if(!window.__tap) window.__tap=performance.now(); },true); }"); B.tap(pg, 195, 500); attend(pg, "()=>(window.__tr||[]).some(x=>/onbv-ton/.test(x.id))", 2500)
        q2 = next((q for q in pg.evaluate("()=>window.__tr") if 'onbv-ton' in q['id']), None); tap = pg.evaluate("()=>window.__tap")
        if tt and t_pl and q2 and tap: A.append((tt['t0'] - t_pl, q2['t0'] - tap))
        ctx.close()
    return (round(sorted(x[0] for x in A)[len(A) // 2]), round(sorted(x[1] for x in A)[len(A) // 2])) if A else (0, 1e9)
def places(b, fichier, vw, vh, phrase):
    ctx = B.contexte(b, onb=False, guide=False, vw=vw, vh=vh); pg = B.ouvre(ctx, fichier, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(450); pg.keyboard.type(phrase, delay=8); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(2400)
    r = pg.evaluate(RECTS); ctx.close(); return r
with sync_playwright() as p:
    b = p.webkit.launch()
    print('fichier :', F, '· charge %.1f' % B.charge())
    cas = [(390, 844, False, 'clair, 390 × 844'), (330, 714, False, 'clair, échelle 0,79')] + ([] if VITE else [(390, 844, True, 'sombre, 390 × 844'), (330, 714, True, 'sombre, échelle 0,79')])
    for vw, vh, so, T in cas: premier_parcours(b, F, vw, vh, so, T)
    if F != REF:
        for ph, nom in (('marcher une heure', 'courte'), ('appeler ma grand-mère tous les dimanches sans exception jusqu’à la fin de l’année qui vient', 'longue')):
            for vw, vh, T in ((390, 844, '390 × 844'), (330, 714, '0,79')):
                a = places(b, REF, vw, vh, ph); c = places(b, F, vw, vh, ph)
                bad = {i: [round(x - y, 2) for x, y in zip(a[i], c[i])] for i in ['onbDit', 'onbQuid', 'onbPh', 'onbSous', 'onbTrace', 'onbTrait'] if max(abs(x - y) for x, y in zip(a[i], c[i])) > 0.5}
                juge('[%s, phrase %s] I · les places = celles de v172 (± 0,5 pt)' % (T, nom), not bad, bad or 'toutes')
    if F != REF:
        a = attentes(b, REF); c = attentes(b, F); ch = B.charge()
        juge('K · C-212 : du plant au titre ≈ 285 ms de moins que v172 ; du toucher au paragraphe ≈ 48 ms de moins (charge %.1f)' % ch, a[0] - c[0] >= 130 and a[1] - c[1] >= 15, 'v172 %s · maintenant %s' % (a, c))
    # J — réduire les animations
    ctx, pg = debut(b, F, 390, 844, reduit=True); pg.keyboard.press('Enter'); pg.wait_for_timeout(1600)
    v = pg.evaluate("()=>['onbDit','onbQuid','onbPh','onbSous'].map(i=>{ const c=getComputedStyle(document.getElementById(i)); return c.visibility; })"); tr = pg.evaluate("()=>window.__tr.length")
    t0 = pg.evaluate("()=>getComputedStyle(document.getElementById('onbTrait')).display")
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(350); pg.keyboard.type('marcher', delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    ph = pg.evaluate(PHASE); t1 = pg.evaluate("()=>getComputedStyle(document.getElementById('onbTrait')).display")
    juge('J · réduire les animations : les quatre textes posés, sans tracé ; le trait attend la promesse ; le départ fixe', all(x == 'visible' for x in v) and tr == 0 and t0 == 'none' and t1 == 'block' and not ph['clig'], (v, tr, t0, t1, ph['clig']))
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
