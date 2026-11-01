#!/usr/bin/env python3
"""redteam_guide_retour.py — ⚑ v162 (Tom, C-166, RÉCIDIVE) : ONBOARDING — APRÈS LE STUDIO, LE FOND ET LE TEMPS.

« a. le flou met trop de temps à quitter le Studio avant que la zone nette paraisse sur le + ; b. si l'on a changé le monde ou la couleur, le fond flouté
montre ENCORE l'ancien monde. Le fond flouté est TOUJOURS recalculé à partir de la Toile réelle. Le flou commence à quitter le Studio au plus 100 ms après la
fin de la fermeture du Studio. La zone nette du + est ouverte au plus 800 ms après. »
Le chemin de Tom, au doigt (banc comme Tom : WebKit, ×3) : l'onboarding entier (prénom, parole, trait, « Promi planté ! », quatre touchers, « Plus tard »),
le guide paraît, le Studio touché dans sa zone nette ; avec ou sans changement (le monde glissé puis une palette touchée) ; le Studio refermé VITE (400 ms
après le dernier toucher). Tout se lit sur ce qui est peint, image par image : la fin de la fermeture = le Studio sorti de l'écran (sa boîte) ; « le flou
quitte le Studio » = l'eau du guide (son canevas) repasse sur l'entrée du Studio ; « la zone du + ouverte » = plus d'eau sur tout le disque du +.
  A · le flou quitte le Studio ≤ 100 ms après la fin de la fermeture ;
  B · la zone du + est ouverte ≤ 800 ms après la fin de la fermeture ;
  C · le fond flouté, la zone du + ouverte puis 2 s plus tard, est celui de la Toile réelle (l'accueil copié et flouté à 4,8 maintenant : ≤ 0,2 % des valeurs
      à plus de 6 niveaux) ;
  D · aucune erreur de page.
Durées : au calme (charge < 4) à la borne ; sous charge, à 1 s près — un délai de plusieurs secondes est une attente écrite dans le code, pas la charge. Preuve : `--fichier=zz-v161.html` rougit (A, B, et C avec changement).
"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
CLAVIER = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
TRAIT = open('redteam_onboarding_complet.py', encoding='utf-8').read().split('TRAIT = """')[1].split('"""')[0]
def trace(pg):
    z = pg.evaluate(TRAIT); a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
COMPARE = """async ()=>{ const g=document.getElementById('guide'); const f=g&&g.__flou; if(!f||!window._guide) return null; const net=await _guide.image(); const fr=Flaques.floute(net, 4.8);
  const a=f.getContext('2d').getImageData(0,0,f.width,f.height).data, b=fr.getContext('2d').getImageData(0,0,fr.width,fr.height).data; if(a.length!==b.length) return {taille:false};
  let n=0; for(let i=0;i<a.length;i++){ if(Math.abs(a[i]-b[i])>6) n++; } return {part:+(n/a.length).toFixed(5)}; }"""
# l'eau du guide sous un point (alpha de son canevas) ; la fin de la fermeture du Studio : sa boîte hors de l'appareil
SUIT = """(tr)=>{ window.__R={ferme:null, quitte:null, plus:null, sec:null, nsec:0}; const t0=performance.now(); const D=document.getElementById('device');
  const pts=n=>{ const e=document.querySelector(n); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, Math.min(r.width,r.height)*0.30]; };
  const S=pts('#studioBtn'), P=pts('#createBtn'), Dk=D.getBoundingClientRect(), kk=Dk.width/390;
  const Z=[]; for(let i=0;i<5;i++) for(let j=0;j<5;j++) Z.push([Dk.left+(tr.x-tr.w/2+tr.w*(i+0.5)/5)*kk, Dk.top+(tr.y-tr.h/2+tr.h*(j+0.5)/5)*kk]);   /* toute la zone nette du Studio : 25 points */
  function eau(p, rayon){ const c=document.getElementById('guideEau'); if(!c) return null; const q=c.getBoundingClientRect(), k=c.width/q.width, x=c.getContext('2d'); let m=0;
    const pp=rayon?[[0,0],[1,0],[-1,0],[0,1],[0,-1],[.7,.7],[-.7,.7],[.7,-.7],[-.7,-.7]]:[[0,0]];
    for(const o of pp){ const X=Math.round((p[0]+o[0]*p[2]-q.left)*k), Y=Math.round((p[1]+o[1]*p[2]-q.top)*k); const a=x.getImageData(X,Y,1,1).data[3]; if(a>m) m=a; } return m; }
  (function f(){ const now=performance.now()-t0, st=document.getElementById('studioScreen'), Dr=D.getBoundingClientRect(), r=st.getBoundingClientRect();
    const sorti=!st.classList.contains('show') && (r.top>=Dr.bottom-1 || getComputedStyle(st).display==='none' || +getComputedStyle(st).opacity<0.01);
    if(sorti && window.__R.ferme==null) window.__R.ferme=now;
    if(!st.classList.contains('show') && window.__R.quitte==null){ const V=Z.map(z=>eau([z[0], z[1], 0])||0);
      if(!window.__R.sec){ window.__R.sec=V.map(v=>v<=2); window.__R.nsec=window.__R.sec.filter(Boolean).length; window.__R.debut=now; }   /* les points secs quand le Studio commence à se refermer : la zone nette */
      else if(V.some((v,i)=>window.__R.sec[i] && v>4)) window.__R.quitte=now; }
    if(window.__R.quitte!=null && window.__R.ferme!=null && window.__R.plus==null){ const a=eau(P, true); if(a!=null && a<8) window.__R.plus=now; }
    if(now<9000 && window.__R.plus==null) requestAnimationFrame(f); })(); return [S, P]; }"""
def passe(b, sombre, change):
    T = '%s · %s' % ('sombre' if sombre else 'clair', 'monde et palette changés' if change else 'sans changement')
    ctx = B.contexte(b, sombre=sombre, onb=False, guide=False); ctx.add_init_script(CLAVIER); pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200)
    B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(600); pg.keyboard.type('marcher une heure', delay=12); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(2200); trace(pg); pg.wait_for_timeout(5600)
    for _ in range(4): B.tap(pg, 195, 300); pg.wait_for_timeout(3800)
    try: B.tap_sel(pg, '.onbv-compte .tard')
    except Exception: pass
    for _ in range(150):
        if pg.evaluate("()=>{const g=document.getElementById('guide');return !!(g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier'))}"): break
        pg.wait_for_timeout(120)
    pg.wait_for_timeout(1600); tr = pg.evaluate("()=>window._guide&&_guide.etat().trou")
    if not tr: juge('[%s] le guide paraît à l\'étape du Studio' % T, False); ctx.close(); return
    B.tap(pg, tr['x'], tr['y']); pg.wait_for_timeout(2600)
    m0 = pg.evaluate("()=>JSON.stringify(Toile.mondeCourant())")
    if change:
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500)
        c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton');if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")
        if c: B.tap(pg, c[0], c[1], appareil=False); pg.wait_for_timeout(900)
        c = pg.evaluate("()=>{ const P=[...document.querySelectorAll('#stpPals .st3-p')].filter(b=>!b.classList.contains('on') && b.getBoundingClientRect().width>4); const b=P[Math.min(5,P.length-1)]; if(!b) return null; const r=b.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if c: B.tap(pg, c[0], c[1], appareil=False)
    pg.wait_for_timeout(400)
    pg.evaluate(SUIT, tr); c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .closeb');const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")
    B.tap(pg, c[0], c[1], appareil=False); ch = B.charge()
    for _ in range(80):
        R = pg.evaluate("()=>window.__R")
        if R['plus'] is not None: break
        pg.wait_for_timeout(120)
    R = pg.evaluate("()=>{ const r=Object.assign({}, window.__R); delete r.sec; return r; }"); m1 = pg.evaluate("()=>JSON.stringify(Toile.mondeCourant())"); calme = ch < 4
    q = None if R['ferme'] is None or R['quitte'] is None else R['quitte'] - R['ferme']
    o = None if R['ferme'] is None or R['plus'] is None else R['plus'] - R['ferme']
    nj = '' if calme else ' — sous charge %.1f : jugé à 1 s près' % ch
    juge('[%s] A · le flou quitte le Studio ≤ 100 ms après la fin de sa fermeture%s' % (T, nj), R.get('nsec', 0) >= 4 and q is not None and q <= (100 if calme else 1100), 'après %s ms · %s' % (None if q is None else round(q), R))
    juge('[%s] B · la zone du + est ouverte ≤ 800 ms après la fin de la fermeture%s' % (T, nj), o is not None and o <= (800 if calme else 1800), 'après %s ms' % (None if o is None else round(o)))
    c1 = pg.evaluate(COMPARE); pg.wait_for_timeout(2000); c2 = pg.evaluate(COMPARE)
    dg = pg.evaluate('''async ()=>{ const g=document.getElementById('guide'); const a=await _guide.image(), b=await _guide.image(true), f=g.__net; const D=(x,y)=>{const p=x.getContext('2d').getImageData(0,0,390,844).data,q=y.getContext('2d').getImageData(0,0,390,844).data;let n=0;for(let i=0;i<p.length;i++) if(Math.abs(p[i]-q[i])>6)n++;return +(n/p.length).toFixed(4)}; return {copie_rendu:D(a,b), copie_fond:D(a,f), rendu_fond:D(b,f), sig0:g.getAttribute('data-flou-sig'), sig:_guideFlou.sig(), refait:g.getAttribute('data-flou-refait'), etat:_guide.etat().etat}; }''')
    print('     diag', dg)
    if '--images' in sys.argv:
        import base64
        for nom, rendu in (('copie', 'false'), ('rendu', 'true')):
            u = pg.evaluate("async ()=>{ const c=await _guide.image(%s); return c.toDataURL(); }" % rendu)
            open('/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/ba9f9609-0e81-476f-bcc9-424c0208300e/scratchpad/gr-%s-%s.png' % (nom, 's' if sombre else 'c'), 'wb').write(base64.b64decode(u.split(',')[1]))
    juge('[%s] C · le fond flouté est celui de la Toile réelle, la zone du + ouverte puis 2 s plus tard' % T, (m1 != m0) == change and c1 and c2 and c1.get('part', 1) <= 0.002 and c2.get('part', 1) <= 0.002,
         'monde %s → %s · à l\'ouverture %s · 2 s après %s' % (m0, m1, c1, c2))
    er = [x for x in pg.erreurs if 'version.json' not in x]
    juge('[%s] D · aucune erreur de page' % T, not er, er[:2]); ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        for change in ((True,) if '--images' in sys.argv else (False, True)): passe(b, sombre, change)
        if '--images' in sys.argv: break
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
