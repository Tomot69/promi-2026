#!/usr/bin/env python3
"""
redteam_flash.py — RIEN NE PARAÎT UNE FRACTION DE SECONDE (Tom, 30 sept. 2026 : « c'est la deuxième fois qu'ils reviennent »).

Relevé IMAGE PAR IMAGE, dans la page (une passe par requestAnimationFrame), en WebKit ET en Chromium, au vrai doigt
(contexte tactile) :
  A · l'OUVERTURE de l'app (utilisateur revenu, onboarding passé)
  B · le + de l'accueil → Un Promi · Un Chiche · Une Nuée
  C · PLANTER chacun des trois (le trait tracé jusqu'au bout)

Trois familles, et elles ont la forme des défauts vus (v103) :
  1 · PREMIER PLAN — une grille 6 × 11 sur l'appareil : à chaque image, la couche du dessus qui PEINT (opacité effective
      ≥ .12). Une couche qui paraît puis disparaît en moins de 800 ms, sans être là au début ni à la fin, est un flash.
      L'ancien chrome (.topbar, .footer, .statusbar) ne paraît JAMAIS.
  2 · LA PAGE + PARAÎT COMPOSÉE — à chaque image où elle est visible : sa nature (pp-<nature>), son plateau (.enh) à
      l'encre FINALE, et sa phrase à sa mise en page FINALE (positions relatives à la phrase : le glissement est permis,
      pas la recomposition). Vu en v103 : un plateau vide, un champ crème, la phrase d'un seul bloc, la phrase du Promi
      sous la tuile du Chiche.
  3 · UNE PLANTATION COUPE — une fois la page + fermée, elle ne se remontre plus (vu : elle reprenait son aspect d'avant
      ~100 ms, puis son plateau traînait seul sur la Toile).

Seuils EN DUR (§7) : 800 ms, 2 points de grille, opacité .12. Prouvé contre sauvegardes/app-avant-v103b.html.
Usage : python3 redteam_flash.py [url] [webkit,chromium]
"""
import sys, json
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
MOTEURS = sys.argv[2].split(',') if len(sys.argv) > 2 else ['webkit', 'chromium']
COURT_MS = 800      # une apparition plus courte, ni au début ni à la fin, est un flash
POINTS = 2          # points de grille (sur 66) pour compter une couche
INTERDITS = ('.topbar', '.footer', '.statusbar')

SONDE = r"""
(function(){ if(window.__fl) return; var F=window.__fl={on:false,frames:[],t0:0};
  function effOp(e){ var o=1; while(e&&e.nodeType===1){ var s=getComputedStyle(e); if(s.visibility==='hidden'||s.display==='none') return 0; o*=parseFloat(s.opacity); if(o<0.02) return 0; e=e.parentElement; } return o; }
  function peint(e){ if(/^(CANVAS|IMG|SVG|svg|VIDEO|path|circle|rect|polygon)$/.test(e.tagName)) return true;
    var s=getComputedStyle(e), bg=s.backgroundColor; if(bg && bg!=='transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg)) return true;
    if(s.backgroundImage && s.backgroundImage!=='none') return true;
    for(var n=e.firstChild;n;n=n.nextSibling) if(n.nodeType===3 && n.textContent.trim()) return true; return false; }
  function nom(x){ if(!x) return ''; if(x.id) return '#'+x.id; var c=(x.className&&x.className.baseVal!==undefined)?x.className.baseVal:x.className; return '.'+(String(c||'').split(' ')[0]||x.tagName); }
  function cle(e){ var dv=document.getElementById('device'), fr=dv&&dv.parentElement, ch=[];
    while(e && e!==document.body && e!==document.documentElement){ var p=e.parentElement; ch.unshift(e); if(p===dv||p===fr||p===document.body) break; e=p; }
    return nom(ch[0])+(ch[1]?'>'+nom(ch[1]):''); }
  function page(){ var cs=document.getElementById('createSheet'); if(!cs) return null; var s=getComputedStyle(cs), dv=document.getElementById('device');
    var r=cs.getBoundingClientRect(), b=dv.getBoundingClientRect(); var vu = s.visibility!=='hidden' && parseFloat(s.opacity)>0.05 && Math.min(r.bottom,b.bottom)-Math.max(r.top,b.top)>40;
    if(!vu) return {vu:false};
    var ph=document.getElementById('csPhrase'), o=ph?ph.getBoundingClientRect():{left:0,top:0}, sig='';
    if(ph) ph.querySelectorAll('*').forEach(function(e){ var q=e.getBoundingClientRect(); if(q.width && getComputedStyle(e).visibility!=='hidden') sig+=Math.round(q.left-o.left)+','+Math.round(q.top-o.top)+','+Math.round(q.width)+';'; });
    var mk=cs.querySelector('.enh .enh-t');
    var tc=document.getElementById('csTrameCv'), tr=tc?getComputedStyle(tc).transform:'none', ech=1;
    if(tr && tr!=='none'){ var mm=tr.match(/matrix\(([^,]+)/); if(mm) ech=parseFloat(mm[1]); }
    return {vu:true, ech:ech, cls:cs.className, enh:!!cs.querySelector('.enh'), encre:mk?getComputedStyle(mk).webkitTextFillColor||getComputedStyle(mk).color:null, sig:sig}; }
  function pas(){ if(F.on){ var dv=document.getElementById('device'); if(dv){ var r=dv.getBoundingClientRect(), m={};
      for(var i=0;i<6;i++) for(var j=0;j<11;j++){ var L=document.elementsFromPoint(r.left+r.width*(i+.5)/6, r.top+r.height*(j+.5)/11);
        for(var k=0;k<L.length;k++){ var e=L[k]; if(e===dv||e===document.body||e===document.documentElement) break;
          if(effOp(e)<0.12 || !peint(e)) continue; var c=cle(e); m[c]=(m[c]||0)+1; break; } }
      F.frames.push({t:Math.round(performance.now()-F.t0), m:m, p:page()}); } }
    requestAnimationFrame(pas); }
  F.go=function(){ F.frames=[]; F.t0=performance.now(); F.on=true; };
  F.stop=function(){ F.on=false; return F.frames; };
  requestAnimationFrame(pas); })();
"""

res = []
def t(nom, ok, detail=''):
    res.append(ok); print(('  ✅ ' if ok else '  ❌ ') + nom + ('  — ' + detail if detail else ''))

def flashs(fr, geste_ms=0):
    """famille 1 : les couches qui paraissent moins de COURT_MS, ni au début ni à la fin."""
    out = []
    if not fr: return out
    cles = set(k for f in fr for k in f['m'])
    for k in cles:
        run = None
        for i, f in enumerate(fr):
            v = f['m'].get(k, 0) >= POINTS
            if v and run is None: run = [i, i]
            elif v: run[1] = i
            if (not v or i == len(fr) - 1) and run is not None:
                a, b = run; run = None
                dur = (fr[b + 1]['t'] if b + 1 < len(fr) else fr[-1]['t']) - fr[a]['t']
                # le ruban du trait PENDANT le geste est le doigt lui-même, pas un flash
                if k.endswith('.pp-trace') and fr[a]['t'] < geste_ms: continue
                # une PARTIE d'écran (clé « couche>partie ») qui paraît pendant que son écran est là et s'en va AVEC lui
                # n'apparaît pas : c'est le premier plan qui change à l'intérieur d'un même écran (la dalle qui couvre
                # le champ met les pastilles du pinceau devant). La plantation reste gardée par C2 et C3.
                if '>' in k:
                    L = k.split('>')[0]
                    tot = lambda f: sum(v for kk, v in f['m'].items() if kk.split('>')[0] == L)
                    if a > 0 and tot(fr[a - 1]) >= POINTS and (b + 1 >= len(fr) or all(tot(fr[x]) < POINTS for x in range(b + 1, min(len(fr), b + 3)))):
                        continue
                if dur < COURT_MS and a > 2 and b < len(fr) - 3:
                    out.append('%s à %d ms, %d ms' % (k, fr[a]['t'], dur))
    for k in cles:
        if k.split('>')[0] in INTERDITS and any(f['m'].get(k, 0) for f in fr):
            out.append('%s (ancien chrome) à %d ms' % (k, next(f['t'] for f in fr if f['m'].get(k, 0))))
    return sorted(out)

def ouvre(b):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    ctx.add_init_script(SONDE)
    return ctx, ctx.new_page()

def tap(pg, sel):
    r = pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", sel)
    if r: pg.touchscreen.tap(r[0], r[1])
    return r

def trace(pg, zone):
    r = pg.evaluate("s=>{const e=document.getElementById(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}", zone)
    if not r or r[2] < 10: return False
    y = r[1] + r[3] / 2; x0 = r[0] + 30; x1 = r[0] + r[2] - 20
    pg.mouse.move(x0, y); pg.mouse.down()
    for i in range(1, 16): pg.mouse.move(x0 + (x1 - x0) * i / 15, y); pg.wait_for_timeout(16)
    pg.mouse.up(); return True

for mot in MOTEURS:
    print('\n══ %s' % mot)
    with sync_playwright() as p:
        b = getattr(p, mot).launch(**({'args': ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist']} if mot == 'chromium' else {}))
        # A · l'ouverture
        ctx, pg = ouvre(b)
        ctx.add_init_script("requestAnimationFrame(function g(){ if(window.__fl) window.__fl.go(); else requestAnimationFrame(g); })")
        pg.goto(URL); pg.wait_for_timeout(7000)
        fr = pg.evaluate("()=>__fl.stop()")
        f = flashs(fr)
        t('A · ouverture : rien ne paraît une fraction de seconde (%d images)' % len(fr), not f and len(fr) > 30, '; '.join(f))
        ctx.close()
        for nat in ('promi', 'chiche', 'nuee'):
            ctx, pg = ouvre(b); pg.goto(URL); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.wait_for_timeout(500)
            # B · le + et la nature
            pg.evaluate("()=>__fl.go()")
            tap(pg, '#createBtn'); pg.wait_for_timeout(900)
            tap(pg, '#accChoix .acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(1800)
            fr = pg.evaluate("()=>__fl.stop()")
            f = flashs(fr)
            t('B1 · + → %s : aucun flash au premier plan (%d images)' % (nat, len(fr)), not f and len(fr) > 20, '; '.join(f))
            vus = [x for x in fr if x['p'] and x['p']['vu']]
            fin = vus[-1]['p'] if vus else None
            mauvais = []
            if not fin: mauvais.append('la page + ne paraît jamais')
            else:
                for x in vus:
                    q = x['p']; pb = []
                    if 'pp-' + nat not in q['cls'].split(): pb.append('nature ' + ' '.join(c for c in q['cls'].split() if c.startswith('pp')))
                    if not q['enh']: pb.append('plateau absent')
                    elif q['encre'] != fin['encre']: pb.append('plateau encre %s (finale %s)' % (q['encre'], fin['encre']))
                    if q['sig'] != fin['sig']: pb.append('phrase pas à sa mise en page finale')
                    if pb: mauvais.append('%d ms : %s' % (x['t'], ', '.join(pb)))
            t('B2 · + → %s : la page + paraît COMPOSÉE dès sa première image (%d images vues)' % (nat, len(vus)), not mauvais, '; '.join(mauvais[:4]))
            # C · planter
            if nat == 'nuee': pg.evaluate("()=>{var f=document.getElementById('nName'); if(f){f.value='juge flash'; f.dispatchEvent(new Event('input',{bubbles:true}));}}")
            else: pg.evaluate("()=>{var f=document.getElementById('fTitle'); if(f){f.value='juge flash'; f.dispatchEvent(new Event('input',{bubbles:true}));}}")
            pg.wait_for_timeout(400)
            n0 = pg.evaluate("()=>promises.length")
            pg.evaluate("()=>__fl.go()")
            ok = trace(pg, 'planterZoneN' if nat == 'nuee' else 'planterZone'); pg.wait_for_timeout(2600)
            fr = pg.evaluate("()=>__fl.stop()"); n1 = pg.evaluate("()=>promises.length")
            f = flashs(fr, geste_ms=500)   # le trait se trace en ~0,3 s (15 pas de 16 ms)
            t('C1 · planter %s : aucun flash au premier plan (%d → %d paroles)' % (nat, n0, n1), ok and n1 == n0 + 1 and not f, '; '.join(f) or ('' if n1 == n0 + 1 else 'rien planté'))
            # la page + visible, cachée, puis visible à nouveau = elle se remontre
            # la dalle a couvert l'écran (échelle > 2) : la page + ne doit plus JAMAIS paraître avec sa dalle à sa taille
            couvert = None; retour = None
            for x in fr:
                q = x['p']
                if not (q and q['vu']): continue
                if q.get('ech', 1) > 2 and couvert is None: couvert = x['t']
                elif couvert is not None and q.get('ech', 1) < 1.5: retour = x['t']; break
            t('C3 · planter %s : après la couverture, la page + ne reprend pas son aspect d\'avant' % nat, retour is None,
              ('dalle couvrante à %d ms, page + redevenue celle d\'avant à %d ms' % (couvert, retour)) if retour else ('couverture à %s ms' % couvert))
            etats = [bool(x['p'] and x['p']['vu']) for x in fr]
            revient = None
            for i in range(1, len(etats)):
                if etats[i] and not etats[i - 1] and any(etats[:i]): revient = fr[i]['t']; break
            ferme = next((fr[i]['t'] for i in range(len(etats)) if any(etats[:i]) and not etats[i]), None)
            t('C2 · planter %s : la page + coupe et ne se remontre pas (fermée à %s ms)' % (nat, ferme), revient is None and ferme is not None,
              ('se remontre à %d ms' % revient) if revient else ('' if ferme else 'ne se ferme pas'))
            ctx.close()
        b.close()

n = len(res); k = sum(res)
print('\n%d/%d' % (k, n))
sys.exit(0 if k == n else 1)
