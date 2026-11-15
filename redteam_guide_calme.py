#!/usr/bin/env python3
"""
redteam_guide_calme.py — ⚑ v197 (Tom, C-268) : LE GUIDE DU STUDIO NE SE LANCE JAMAIS PAR-DESSUS UNE ACTION, ET SANS TEMPS MORT.

« Si un geste est commencé ou si quelque chose est ouvert, il attend que ce soit fini et que l'écran soit calme, puis se lance ≤ 300 ms après.
Jamais par-dessus une action. »

Banc comme Tom (WebKit, 390 × 844, échelle 3, doigt). Deux paroles plantées par l'app, puis la fin de l'onboarding est rejouée telle que l'app
la fait (`_guide.attend`, l'appel de `terminerSuite`) à t0 — et l'on agit à des instants différents :
  A rien ; B un toucher sur une dalle (à 0, 120 et 400 ms), la fiche ouverte 1,5 s puis fermée par son X ; C un glissé sur la Toile ;
  D une fiche ouverte puis un tracé maintenu sur son trait, puis fermée ; E le + (le menu des natures) ouvert puis refermé ailleurs ;
  F l'onboarding entier au doigt, une dalle touchée dès que l'accueil paraît.
Chaque image est relevée DANS LA PAGE (requestAnimationFrame), sur ce qui est À L'ÉCRAN — jamais sur ce que l'app déclare : un doigt posé
(écouteurs posés avant ceux de l'app), une fiche, une feuille, un écran, le menu des natures qui recouvrent l'appareil, la Toile qui bouge.
Verdicts : ① le guide se lance ; ② à l'instant où il se pose dans le DOM (un observateur), rien de tout cela ; ③ entre la dernière image occupée et cet
instant : ≤ 300 ms (en dur). La première image peinte peut venir après : le lancement occupe le fil ≈ 0,5 s (C-208, préexistant). --fichier=… : une autre version.
"""
import io, os, sys, time, json
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from banc_tom import contexte, ouvre, plante, tap, tap_sel, glisse, droite, pt, attend_parole

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
SEUL = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--seul=')), None)
CHARGE = os.getloadavg()[0]
DELAI = 300                                   # ms — la décision de Tom (C-268), en dur
res = []
SONDE_T = """(()=>{ window.__lt=[]; const enr=(k,f)=>function(){ const a=performance.now(); try{ return f.apply(this,arguments); } finally{ const d=performance.now()-a; if(d>40) __lt.push([Math.round(a-(window.__gt0||0)), Math.round(d), k+':'+String(f.name||'').slice(0,30)+':'+String(f).slice(0,90)]); } };
  const st=window.setTimeout, si=window.setInterval, ra=window.requestAnimationFrame, ri=window.requestIdleCallback;
  window.setTimeout=function(f,ms){ return typeof f==='function'?st(enr('T',f),ms):st(f,ms); }; window.setInterval=function(f,ms){ return typeof f==='function'?si(enr('I',f),ms):si(f,ms); };
  window.requestAnimationFrame=function(f){ return ra(enr('R',f)); }; })();"""
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-112s %s' % ('✅' if cond else '❌', nom, str(detail)[:260]), flush=True)

DOIGT = """(()=>{ window.__gc={doigt:0};
  ['touchstart','pointerdown'].forEach(n=>window.addEventListener(n,e=>{ __gc.doigt=1; __gc.tT=performance.now(); },true));
  ['touchend','touchcancel','pointerup','pointercancel'].forEach(n=>window.addEventListener(n,e=>{ if(e.touches&&e.touches.length) return; __gc.doigt=0; },true)); })();"""
RELEVE = """()=>{ const D=()=>document.getElementById('device').getBoundingClientRect();
  const vis=(el)=>{ if(!el) return false; const c=getComputedStyle(el); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.02) return false;
    const r=el.getBoundingClientRect(), d=D(); const w=Math.min(r.right,d.right)-Math.max(r.left,d.left), h=Math.min(r.bottom,d.bottom)-Math.max(r.top,d.top); return w>2&&h>2; };
  const L=window.__gl=[]; const t0=performance.now(); window.__gt0=t0; window.__glance=null;
  const estOn=()=>{ try{ const g=document.getElementById('guide'), ge=document.getElementById('guideEau'); return !!ge || !!(g && g.getAttribute('data-guide') && g.getAttribute('data-guide')!=='part'); }catch(e){ return false; } };
  const occ=()=>{ const o=[]; if(window.__gc&&__gc.doigt) o.push('doigt');
    if(vis(document.getElementById('detailPoster'))) o.push('fiche');
    if(vis(document.getElementById('createSheet'))) o.push('feuille');
    const ch=document.getElementById('accChoix'); if(ch&&ch.classList.contains('ouvert')&&vis(ch)) o.push('natures');
    document.querySelectorAll('.screen, #feedView, #entierVue, #dessinMode').forEach(e=>{ if(vis(e)) o.push('écran:'+(e.id||e.className)); });
    if(document.getElementById('onbV')) o.push('onboarding');
    try{ const s=window.Toile_state&&Toile_state(); if(s&&s.running) o.push('toile'); }catch(e){}
    return o.join(','); };
  /* l'instant EXACT du lancement : l'heure que `montre` pose au début de sa tâche (`data-pose` — l'observateur n'est appelé qu'à la FIN de cette tâche, ≈ 0,5 s plus
     tard) ; ce qui est à l'écran est lu dans l'observateur : rien ne peut changer au milieu d'une tâche (un toucher attend qu'elle finisse) */
  new MutationObserver(()=>{ if(!window.__glance && estOn()){ const g=document.getElementById('guide'), tp=g&&+g.getAttribute('data-pose'); window.__glance=[Math.round((tp||performance.now())-t0), occ()]; } }).observe(document.body,{subtree:true, childList:true, attributes:true, attributeFilter:['data-guide']});
  (function f(){ const t=performance.now()-t0; L.push([Math.round(t), estOn()?1:0, occ()]); if(t<30000) requestAnimationFrame(f); })(); }"""
OU = """(pas)=>{ pas=pas||6;  const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height, G={};
  for(let y=120;y<700;y+=pas) for(let x=10;x<380;x+=pas){ let h=null; try{ h=Toile.hit((d.left+x*k-r.left)*kx,(d.top+y*k-r.top)*ky); }catch(e){} if(h&&h.pid!=null){ const g=G[h.pid]=G[h.pid]||{n:0,x:0,y:0}; g.n++; g.x+=x; g.y+=y; } }
  let best=null; for(const p in G){ if(!best||G[p].n>best[2]) best=[G[p].x/G[p].n, G[p].y/G[p].n, G[p].n]; } return best; }"""

def bilan(pg, nom, maxi=14000):
    t0 = time.time()
    while time.time() - t0 < maxi / 1000.0:
        L = pg.evaluate("()=>window.__gl||[]")
        if any(f[1] for f in L): pg.wait_for_timeout(150); break
        pg.wait_for_timeout(100)
    L = pg.evaluate("()=>window.__gl||[]")
    i = next((k for k, f in enumerate(L) if f[1]), None)
    juge('%s · ① le guide du Studio se lance' % nom, i is not None, '%d images relevées' % len(L))
    if i is None: return
    G = pg.evaluate("()=>window.__glance")
    occ = G[1] if G else L[i][2]; tl = G[0] if G else L[i][0]
    if os.environ.get('GC_DEBUG'): print('      images :', L[max(0,i-25):i+3])
    juge('%s · ② à l\'instant où il se pose, rien n\'est en cours (ni doigt, ni fiche, ni feuille, ni écran, ni menu, ni Toile qui bouge)' % nom, not occ, 'à %d ms : %s' % (tl, occ or '—'))
    t0 = pg.evaluate("()=>window.__gt0"); tT = pg.evaluate("()=>window.__gc&&__gc.tT")
    tT = (tT - t0) if tT else None
    neuf = lambda o: set(x for x in o.split(',') if x and x not in ('toile', 'doigt'))
    apres = [f for f in L if tl < f[0] <= tl + 400 and neuf(f[2]) - neuf(occ)]
    juge('%s · ②b aucune fiche, feuille ni menu ouverts par un toucher d\'avant ne paraissent sous le guide (400 ms)' % nom, not (tT is not None and tT < tl and apres),
         'dernier toucher à %s ms ; après le lancement : %s' % (None if tT is None else round(tT), apres[:1] or '—'))
    j = max([k for k in range(len(L)) if L[k][0] < tl and L[k][2]] or [-1])
    calme = L[j + 1][0] if j >= 0 else 0
    dit = '%d ms (calme à %d ms : « %s » cesse ; guide posé à %d ms, première image à %d ms)' % (tl - calme, calme, L[j][2] if j >= 0 else '—', tl, L[i][0])
    if CHARGE >= 4: print('      (non jugé : ③ est une durée ; charge du Mac %.1f ≥ 4 — C-137. Relevé : %s)' % (CHARGE, dit))
    else: juge('%s · ③ pas de temps mort : le guide part ≤ %d ms après la dernière image occupée' % (nom, DELAI), tl - calme <= DELAI, dit)

def prepare(b):
    ctx = contexte(b, guide=False); ctx.add_init_script(DOIGT); pg = ouvre(ctx, F)
    for t in ('arroser le figuier', 'écrire à Lou'): plante(pg, t)
    pg.wait_for_timeout(2500)
    d = pg.evaluate(OU)
    return ctx, pg, d

def arme(pg):
    pg.evaluate("()=>{ localStorage.removeItem('promi_guide'); }"); pg.evaluate(RELEVE); pg.evaluate("()=>window._guide.attend(false)")

def ferme_fiche(pg):
    r = tap_sel(pg, '#detailPoster .closeb')
    if not r: pg.evaluate("()=>{ try{ closeAll() }catch(e){} }")

with sync_playwright() as p:
    b = p.webkit.launch()
    cas = []
    def scen(nom, f):
        if SEUL and SEUL not in nom: return
        print('\n── %s' % nom, flush=True)
        ctx, pg, d = prepare(b)
        if not d: juge(nom + ' · une dalle est sur la Toile', False); ctx.close(); return
        try: f(pg, d)
        except Exception as e: juge(nom + ' · le scénario se joue', False, str(e)[:200])
        bilan(pg, nom)
        juge('%s · aucune erreur de page' % nom, not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close()

    def A(pg, d): arme(pg)
    scen('A rien', A)
    for dt in (0, 120, 400):
        def B(pg, d, dt=dt):
            arme(pg); pg.wait_for_timeout(dt); tap(pg, d[0], d[1]); pg.wait_for_timeout(1500); ferme_fiche(pg)
        scen('B une dalle touchée à %d ms, la fiche 1,5 s' % dt, B)
    def C(pg, d):
        arme(pg); pg.wait_for_timeout(100); glisse(pg, droite([200, 420], [120, 330], 30), pas=30, tenue=200)
    scen('C un glissé sur la Toile à 100 ms', C)
    def Dd(pg, d):
        arme(pg); pg.wait_for_timeout(60); tap(pg, d[0], d[1]); pg.wait_for_timeout(1200)
        z = pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'); const t=c&&c.getAttribute('data-trait'); return t? t.split(',').map(Number):null; }")
        y = (z[0] if z else 330); glisse(pg, droite([200, y], [260, y], 20), pas=40, tenue=300); pg.wait_for_timeout(800); ferme_fiche(pg)
    scen('D une fiche ouverte, un tracé maintenu sur son trait, puis fermée', Dd)
    def E(pg, d):
        arme(pg); pg.wait_for_timeout(150); tap_sel(pg, '#createBtn'); pg.wait_for_timeout(1500); tap(pg, 150, 70); pg.wait_for_timeout(700)
        if pg.evaluate("()=>!!document.querySelector('#detailPoster.show')"): ferme_fiche(pg)
    scen('E le + (le menu des natures) à 150 ms, refermé par un toucher sur le plateau', E)

    if not SEUL or 'F' in SEUL:
        print('\n── F l\'onboarding entier au doigt, une dalle touchée dès que l\'accueil paraît', flush=True)
        ctx = contexte(b, onb=False, guide=False); ctx.add_init_script(DOIGT);
        if os.environ.get('GC_SONDE'): ctx.add_init_script(SONDE_T)
        pg = ouvre(ctx, F)
        try:
            tap_sel(pg, '#onbPh'); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
            attend_parole(pg); (tap_sel(pg, '[data-onb="parole"]') or tap_sel(pg, '#onbPh')); pg.wait_for_timeout(300)
            pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
            z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return {l:(r.left-d.left)/k,t:(r.top-d.top)/k,k:r.width/k/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
            a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
            glisse(pg, droite([z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k']], [z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']], 24), pas=22)
            pg.wait_for_timeout(6400)
            for _ in range(8):
                if pg.evaluate("()=>{ const v=document.getElementById('onbV'); return !v || v.getAttribute('data-onb-reste')==='fini' || !document.getElementById('onbReste'); }"): break
                tap(pg, 195, 300); pg.wait_for_timeout(1700)
            pg.wait_for_timeout(300); tap(pg, 195, 300); pg.wait_for_timeout(1000)
            tap_sel(pg, '.onbv-compte .tard')
            for _ in range(200):
                if pg.evaluate("()=>!document.getElementById('onbV')"): break
                pg.wait_for_timeout(25)
            dd = pg.evaluate(OU, 18); pg.evaluate(RELEVE)
            if dd: tap(pg, dd[0], dd[1]); pg.wait_for_timeout(1500); ferme_fiche(pg)
            juge('F · l\'onboarding traversé, une dalle touchée à l\'accueil', bool(dd), dd)
        except Exception as ex: juge('F · le parcours se joue', False, str(ex)[:200])
        if os.environ.get('GC_SONDE'): print('      longues :', [x for x in pg.evaluate('()=>window.__lt||[]') if -200 < x[0] < 1500])
        bilan(pg, 'F'); juge('F · aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close()
    b.close()
ok = sum(1 for _, c in res if c); print('\n%d/%d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
