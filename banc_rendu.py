#!/usr/bin/env python3
"""
banc_rendu.py — LE BANC DE RENDU DE RÉFÉRENCE (Tom, 30 sept. 2026, assainissement lot 1).
C'est lui qui jugera le portage : graine fixe × monde × taille → une image, comparée AU PIXEL.

  · le HASARD est amorcé avant que l'app ne charge (Math.random → mulberry32, graine GRAINE) : jeu de démonstration,
    semis, couleurs — tout est tiré de la même suite à chaque passage ;
  · l'HORLOGE est figée pendant chaque rendu (performance.now → T_FIGE) : la matière qui « respire » est prise au même instant ;
  · on attend que le monde soit AU REPOS (préparation, croissance, relâchement) : deux rendus séparés de REPOS ms doivent
    être identiques, sinon le monde est déclaré « instable » (et le banc le DIT, il ne le cache pas) ;
  · pour chaque monde (les 20 de `order`, palette par défaut, teinte 0) :
        toile-sombre / toile-clair   la Toile entière, `Toile.renderTo(cv, 1, clair)`, SANS les titres des dalles   390 × H
        dalle-<nature>-k<k>          `Toile.dalleTrame(cv, pid, k, {m, p, h})`, 4 paroles (Promi, Chiche, tenue, d'un Cercle) × 3 tailles
  · chaque image est rangée en PNG dans banc-rendu/<version>/ avec son empreinte (sha1 des pixels RGBA).

Usage :
  python3 banc_rendu.py --figer            pose la référence (banc-rendu/ref/)
  python3 banc_rendu.py                    compare à la référence : 0 pixel différent attendu, sinon le détail
  python3 banc_rendu.py --deux             passe DEUX fois de suite sans référence : prouve que le banc est déterministe
  python3 banc_rendu.py --monde=touffe     un seul monde
  python3 banc_rendu.py URL ...            une autre version de l'app (pour prouver qu'il prend une différence)
Moteur : WebKit (celui de l'iPhone). Les mondes GPU (Madrure) sont rendus par le chemin que WebKit headless prend.
"""
import sys, os, json, hashlib, base64, io, time
from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
URL = ARGS[0] if ARGS else 'http://127.0.0.1:8752/app.html'
FIGER = '--figer' in sys.argv
DEUX = '--deux' in sys.argv
SEUL = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--monde=')), None)
ICI = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ICI, 'banc-rendu', 'ref')
GRAINE = 0x5EED2026
T_FIGE = 123456.0          # ms — l'instant auquel toute matière est prise
REPOS = 1500               # ms entre deux rendus qui doivent être identiques
ATTENTE_MAX = 20000        # ms — au-delà, le monde est déclaré instable
KS = [0.5, 1, 2]           # les trois tailles d'une dalle (k du moteur)
PAROLES = [('promi', 'nager le mardi'), ('chiche', 'courir dimanche'), ('tenu', 'planter un arbre'), ('cercle', 'arroser les tomates')]   # par TITRE, jamais par id (§8)

AMORCE = """(()=>{ let a=%d>>>0; window.__amorce=function(s){ a=s>>>0; };
  Math.random=function(){ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1);
  t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; };
  try{ localStorage.setItem('promi_onb','1'); }catch(e){}
  /* les minuteurs RÉELS posés pendant le démarrage sont notés : quand le banc prend la main, il les reprend en temps piloté */
  const rST=window.setTimeout, rSI=window.setInterval, rCT=window.clearTimeout, rCI=window.clearInterval; window.__reels=new Map(); let n=0;
  window.setTimeout=function(cb,ms,...a){ const k=++n; const id=rST(function(){ window.__reels.delete(id); if(typeof cb==='function') cb(...a); },ms); window.__reels.set(id,{k,cb,ms:+ms||0,a,rep:0}); return id; };
  window.setInterval=function(cb,ms,...a){ const k=++n; const id=rSI(cb,ms,...a); window.__reels.set(id,{k,cb,ms:+ms||0,a,rep:Math.max(16,+ms||0)}); return id; };
  if(window.requestIdleCallback){ const rIC=window.requestIdleCallback.bind(window); window.requestIdleCallback=function(cb,o){ const k=++n; const id=rST(function(){ window.__reels.delete(id); cb({didTimeout:false,timeRemaining:()=>50}); },1); window.__reels.set(id,{k,cb:()=>cb({didTimeout:false,timeRemaining:()=>50}),ms:1,a:[],rep:0}); return id; }; window.cancelIdleCallback=function(i){ window.__reels.delete(i); rCT(i); }; }
  window.clearTimeout=function(i){ window.__reels.delete(i); return rCT(i); }; window.clearInterval=function(i){ window.__reels.delete(i); return rCI(i); };
  window.__reelsCoupe=function(){ const L=[...window.__reels.entries()].sort((x,y)=>x[1].k-y[1].k); for(const [id,e] of L){ rCT(id); rCI(id); } window.__reels.clear(); return L.map(x=>x[1]); };
})();""" % GRAINE
# Après le chargement, le banc PREND LA MAIN sur le temps : l'horloge (performance.now) ne bouge que quand il fait avancer une
# image, et les images de l'app (requestAnimationFrame) ne passent que quand il les donne. Rien ne dépend plus de la machine.
PILOTE = """()=>{ if(window.__vt!=null) return; window.__vt=%r; const pn=performance.now.bind(performance);
  performance.now=()=>window.__vt; window.__q=[]; let id=1;
  window.requestAnimationFrame=cb=>{ window.__q.push([id,cb]); return id++; };
  window.cancelAnimationFrame=i=>{ window.__q=window.__q.filter(x=>x[0]!==i); };
  /* les minuteurs aussi : un setTimeout de l'app, posé pendant qu'on pose un monde, ne passe plus en temps réel entre deux
     appels du banc (vu sur Brouillamini : son cache se bâtissait sur un état transitoire, un nombre variable de fois) */
  const T=[]; let tid=1e6;
  /* ceux du démarrage : coupés en temps réel, repris ici, dans leur ordre de pose ; un intervalle repart à son pas, un délai à son délai */
  for(const e of (window.__reelsCoupe?window.__reelsCoupe():[])){ if(typeof e.cb!=='function') continue; T.push({i:tid++,at:window.__vt+(e.rep||Math.max(0,e.ms)),cb:e.cb,a:e.a||[],rep:e.rep||0}); }
  window.setTimeout=(cb,ms,...a)=>{ if(typeof cb!=='function') return 0; const i=tid++; T.push({i,at:window.__vt+Math.max(0,+ms||0),cb,a}); return i; };
  window.setInterval=(cb,ms,...a)=>{ if(typeof cb!=='function') return 0; const i=tid++; T.push({i,at:window.__vt+Math.max(16,+ms||0),cb,a,rep:Math.max(16,+ms||0)}); return i; };
  window.clearTimeout=window.clearInterval=i=>{ for(let k=T.length-1;k>=0;k--) if(T[k].i===i) T.splice(k,1); };
  /* et les rappels « quand le fil est libre » (requestIdleCallback) : un travail de fond ne passe plus quand la machine veut */
  window.requestIdleCallback=(cb,o)=>window.setTimeout(()=>cb({didTimeout:false,timeRemaining:()=>50}),1);
  window.cancelIdleCallback=i=>window.clearTimeout(i);
  const minuteurs=()=>{ for(let garde=0;garde<500;garde++){ let m=-1; for(let k=0;k<T.length;k++) if(T[k].at<=window.__vt&&(m<0||T[k].at<T[m].at||(T[k].at===T[m].at&&T[k].i<T[m].i))) m=k;
      if(m<0) return; const t=T[m]; if(t.rep){ t.at+=t.rep; } else T.splice(m,1); try{ t.cb(...t.a); }catch(e){} } };
  window.__images=n=>{ for(let i=0;i<n;i++){ window.__vt+=1000/60; minuteurs(); const q=window.__q; window.__q=[]; for(const [,cb] of q){ try{ cb(window.__vt); }catch(e){} } } }; }""" % T_FIGE
IMAGES = 240               # images données au monde après l'avoir posé (4 s d'horloge virtuelle)

POSE = """(a)=>{ const [monde,graine,neufs]=a;
  /* changer de FAMILLE ressème (v35) : on passe par l'autre famille, puis on revient, la graine remise juste avant */
  const autre = neufs.indexOf(monde)>=0 ? 'encre' : 'esquille';
  Toile.setTheme(autre); window.__amorce(graine); Toile.setTheme(monde); return Toile.getTheme(); }"""

RENDU = """(a)=>{ const [monde,T,KS,PAR]=a; const out={};
  {
    const img=(cv)=>{ const g=cv.getContext('2d'); const d=g.getImageData(0,0,cv.width,cv.height).data;
      let h=0x811c9dc5; for(let i=0;i<d.length;i++){ h^=d[i]; h=Math.imul(h,16777619)>>>0; }
      return {w:cv.width,h:cv.height,fnv:h.toString(16),png:cv.toDataURL('image/png')}; };
    /* sans les titres des dalles : leur glyphe dépend du moteur de texte, il ne coïncidera jamais au pixel en Swift (§8 bis) */
    const lab=window._shLabels; window._shLabels=false;
    try{ for(const cl of [false,true]){ const cv=document.createElement('canvas');
      out['toile-'+(cl?'clair':'sombre')] = Toile.renderTo(cv,1,cl) ? img(cv) : null; } } finally { window._shLabels=lab; }
    const M={m:monde,p:Toile.getPalette(),h:Toile.getHue?Toile.getHue():0};
    for(const [nat,titre] of PAR){ const p=promises.find(x=>x.title===titre);
      for(const k of KS){ const nom='dalle-'+nat+'-k'+k; if(!p){ out[nom]={err:'parole introuvable'}; continue; }
        const cv=document.createElement('canvas'); let ok=false; try{ ok=Toile.dalleTrame(cv,p.id,k,M); }catch(e){ out[nom]={err:String(e)}; continue; }
        out[nom] = (ok&&cv.width) ? img(cv) : {err:'rien de rendu'}; } }
  }
  return out; }"""


def passe(url, mondes_voulus=None):
    res = {}
    with sync_playwright() as p:
        b = p.webkit.launch()
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script(AMORCE)
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(url); pg.wait_for_timeout(8000)
        mondes = pg.evaluate("""()=>{ const s=document.body.innerHTML; const m=/order=\\[([^\\]]+)\\]/.exec([...document.scripts].map(x=>x.textContent).join('\\n'));
            return m ? m[1].replace(/['"\\s]/g,'').split(',') : []; }""")
        # un seul monde : on pose quand même ceux qui le précèdent (sans les garder) — un monde qui prépare hors du fil (Ramage)
        # garde un état d'un monde à l'autre ; posé seul, il ne partirait pas du même endroit que dans la passe entière
        garder = set(mondes_voulus) if mondes_voulus else None
        if mondes_voulus: mondes = mondes[:max(mondes.index(m) for m in mondes_voulus if m in mondes) + 1]
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} try{ setPremium(true); }catch(e){} }")
        pg.evaluate(PILOTE)   # AVANT de toucher aux mondes : sinon leurs caches se bâtissent sur le temps réel (vu sur Chamade)
        neufs = pg.evaluate("()=>{ const r=[]; for(const m of %s){ Toile.setTheme(m); if(Toile.semisNeuf()) r.push(m); } return r; }" % json.dumps(mondes))
        for m in mondes:
            t0 = time.time()
            # le monde est posé DEUX fois, sous la même graine : les deux rendus doivent être identiques (sinon INSTABLE).
            # Entre les images données, du temps réel passe : ce qu'un Worker calcule (Ramage) a le temps d'arriver.
            avant = None; r = None; stable = False
            for essai in range(3):
                pg.evaluate(POSE, [m, GRAINE, neufs])
                for _ in range(IMAGES // 40): pg.evaluate("()=>window.__images(40)"); pg.wait_for_timeout(120)
                # un monde qui prépare hors du fil (Ramage : un Worker) : on attend que son rendu cesse de bouger
                prec = None
                for _ in range(40):
                    r = pg.evaluate(RENDU, [m, T_FIGE, KS, PAROLES])
                    emp = {k: (v or {}).get('fnv') for k, v in r.items()}
                    if emp == prec: break
                    prec = emp; pg.evaluate("()=>window.__images(20)"); pg.wait_for_timeout(250)
                if emp == avant: stable = True; break
                avant = emp
            if garder is not None and m not in garder: continue
            res[m] = {'stable': stable, 'duree': round(time.time() - t0, 1), 'images': r}
            print('  %-12s %s  %4.1f s  %s' % (m, 'stable  ' if stable else 'INSTABLE', res[m]['duree'],
                  ' '.join('%s:%s' % (k.replace('dalle-', '').replace('toile-', 'T-'), (v or {}).get('fnv', 'ERR')[:6]) for k, v in r.items())), flush=True)
        b.close()
    return res, errs


def range_(res, dossier):
    os.makedirs(dossier, exist_ok=True); manifeste = {}
    for m, R in res.items():
        manifeste[m] = {'stable': R['stable'], 'images': {}}
        for nom, im in R['images'].items():
            if not im or 'png' not in im: manifeste[m]['images'][nom] = {'err': (im or {}).get('err', 'absent')}; continue
            f = '%s__%s.png' % (m, nom)
            open(os.path.join(dossier, f), 'wb').write(base64.b64decode(im['png'].split(',', 1)[1]))
            manifeste[m]['images'][nom] = {'fichier': f, 'w': im['w'], 'h': im['h'], 'fnv': im['fnv']}
    json.dump({'url': URL, 'graine': GRAINE, 't_fige': T_FIGE, 'ks': KS, 'paroles': PAROLES, 'mondes': manifeste},
              open(os.path.join(dossier, 'manifeste.json'), 'w'), ensure_ascii=False, indent=1)
    return manifeste


def ecart_pixels(fa, fb):
    """nombre de pixels différents et écart maximal entre deux PNG (PIL)."""
    from PIL import Image, ImageChops
    A = Image.open(fa).convert('RGBA'); B = Image.open(fb).convert('RGBA')
    if A.size != B.size: return None, 'taille %s ≠ %s' % (A.size, B.size)
    D = ImageChops.difference(A, B); px = D.getdata()
    n = sum(1 for q in px if any(q)); mx = max((max(q) for q in px), default=0)
    return n, 'max %d' % mx


if __name__ == '__main__':
    voulus = [SEUL] if SEUL else None
    if DEUX:
        print('── passe 1'); r1, e1 = passe(URL, voulus)
        print('── passe 2'); r2, e2 = passe(URL, voulus)
        diff = [(m, k) for m in r1 for k in r1[m]['images'] if (r1[m]['images'][k] or {}).get('fnv') != (r2[m]['images'].get(k) or {}).get('fnv')]
        inst = [m for m in r1 if not (r1[m]['stable'] and r2[m]['stable'])]
        print('\nDÉTERMINISME : %d image(s) différente(s) d\'une passe à l\'autre sur %d · mondes instables : %s · erreurs JS : %d'
              % (len(diff), sum(len(r1[m]['images']) for m in r1), inst or 'aucun', len(e1) + len(e2)))
        for m, k in diff[:40]: print('   ≠', m, k)
        sys.exit(0 if not diff and not inst else 1)
    if FIGER and voulus and os.path.exists(os.path.join(REF, 'manifeste.json')):
        import shutil; shutil.copy(os.path.join(REF, 'manifeste.json'), os.path.join(REF, 'manifeste.json.avant'))
    res, errs = passe(URL, voulus)
    if FIGER:
        man = range_(res, REF)
        if voulus:   # ⚑ v115 : figer UN monde FUSIONNE dans le manifeste — il l'écrasait, et les autres mondes sortaient de la comparaison
            try:
                av = json.load(open(os.path.join(REF, 'manifeste.json.avant')))['mondes']; av.update(man); man = av
            except Exception: pass
            d = json.load(open(os.path.join(REF, 'manifeste.json'))); d['mondes'] = man
            json.dump(d, open(os.path.join(REF, 'manifeste.json'), 'w'), ensure_ascii=False, indent=1)
        n = sum(1 for m in man.values() for v in m['images'].values() if 'fichier' in v)
        print('\nRéférence figée : %d images, %d mondes → %s' % (n, len(man), REF))
        sys.exit(0)
    if not os.path.exists(os.path.join(REF, 'manifeste.json')):
        print('Aucune référence : python3 banc_rendu.py --figer'); sys.exit(1)
    ref = json.load(open(os.path.join(REF, 'manifeste.json')))['mondes']
    tmp = os.path.join(ICI, 'banc-rendu', 'dernier'); man = range_(res, tmp)
    ecarts = []; n_img = 0
    for m, R in ref.items():
        if voulus and m not in voulus: continue
        for nom, v in R['images'].items():
            n_img += 1; w = (man.get(m) or {}).get('images', {}).get(nom)
            if not w or 'fichier' not in w or 'fichier' not in v:
                if (w or {}).get('err') != v.get('err'): ecarts.append((m, nom, 'absente', ''))
                continue
            if w['fnv'] == v['fnv']: continue
            n, d = ecart_pixels(os.path.join(REF, v['fichier']), os.path.join(tmp, w['fichier']))
            ecarts.append((m, nom, n, d))
    print('\n%d image(s) comparée(s) · %d différente(s) · erreurs JS : %d' % (n_img, len(ecarts), len(errs)))
    for e in ecarts[:60]: print('   ≠ %-12s %-18s %s px  %s' % e)
    print('✅ AU PIXEL.' if not ecarts and not errs else '❌ LE RENDU A CHANGÉ.')
    sys.exit(0 if not ecarts and not errs else 1)
