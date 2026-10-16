#!/usr/bin/env python3
"""
redteam_transitions_onb.py — LES TRANSITIONS DE L'ONBOARDING (v147, Tom, 15 oct. 2026 — C-141).

« Les transitions sont cheap. Elles agressent l'œil tant elles sont banales et pas travaillées. […] Chacune s'enchaîne sur la suivante sans
coupure. Le langage est celui de la Toile vivante : le Voronoi se résorbe ou naît dalle par dalle, et le reste se déplace par aplats.
Interdits : fondu, dégradé, coupe sèche, tout ce qui arrive d'un coup. »

Le juge lit la page IMAGE PAR IMAGE (un relevé à chaque `requestAnimationFrame`, posé avant le chargement), par le vrai chemin au doigt
(stockage vierge, Chromium avec le vrai GPU, 390 × 844), en clair et en sombre :
  T1 · L'ARRIVÉE SUR LA PAGE DU PRÉNOM — la Toile NAÎT cellule par cellule : le voile (le fond de la Toile) couvre tout à la première image,
       puis s'ouvre en au moins 12 pas, jamais plus de 20 % d'un coup, sans jamais se refermer, en 0,8 à 1,6 s ; aucun pixel à demi
       transparent (≤ 3 % : le lissage du bord des cellules) ; le mot-marque et la phrase n'arrivent qu'APRÈS, par le tracé (une découpe) ;
  T2 · LES DALLES ENTRE L'ONBOARDING ET LE GUIDE — les voisines se résorbent UNE À UNE : leurs départs sont étalés (60 à 120 ms d'écart),
       jamais deux en même temps ; à la fin il n'en reste aucune ;
  T3 · LA PAGE AVANT L'ACCUEIL — rien ne disparaît en une image : chaque bloc de la page descend et passe derrière la barre (sa surface
       visible baisse de 35 % au plus d'une image à l'autre, jusqu'à presque rien, avant d'être masqué) ; le panneau du compte glisse
       (une transition de `transform`) ; aucun nœud de l'onboarding n'est à demi transparent (ni fondu ni dégradé) ;
  T4 · L'ARRIVÉE SUR L'ACCUEIL — le plateau descend et la barre monte par aplats (au moins 15 images, sans jamais revenir en arrière) ;
       le mot-marque de l'onboarding finit EXACTEMENT sur celui du plateau (± 1 pt) ; puis le guide (0,4 à 1,6 s plus tard) ;
  et l'enchaînement : du toucher sur « Plus tard » au début de la descente, 0,7 s au plus.
Preuve (§7) : `--fichier=zz-av146.html` (avant v147) — il rougit (T1 : pas de voile ; T3 : la page masquée en une image).
Usage : python3 redteam_transitions_onb.py [--fichier=…] [--theme=clair|sombre]
"""
import sys, time, os
from playwright.sync_api import sync_playwright
CHARGE = float(os.popen('sysctl -n vm.loadavg').read().split()[1])
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
TH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--theme=')), None)
URL = 'http://127.0.0.1:8752/' + F
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-112s %s' % ('✅' if c else '❌', nom, str(d)[:260]), flush=True)

SONDE = r"""(function(){ window.__T=[]; var t0=performance.now(), petit=null, k=0; window.__T0=t0;
  function voile(){ var v=document.getElementById('onbV'); if(!v) return null; var cv=v.querySelector('canvas.voile-cellules'); if(!cv||!cv.width) return null;
    if(!petit){ petit=document.createElement('canvas'); petit.width=39; petit.height=84; }
    var g=petit.getContext('2d',{willReadFrequently:true}); g.clearRect(0,0,39,84); g.drawImage(cv,0,0,39,84); var d=g.getImageData(0,0,39,84).data, o=0, p=0, m=0;
    for(var i=3;i<d.length;i+=4){ if(d[i]<10) o++; else if(d[i]>245) p++; else m++; } var n=o+p+m; return [o/n, p/n, m/n]; }
  function vis(e){ if(!e) return 0; var c=getComputedStyle(e); return (c.display!=='none' && c.visibility!=='hidden')?1:0; }
  (function f(){ try{ if(!document.getElementById('device')){ requestAnimationFrame(f); return; }
      var t=performance.now()-t0, v=document.getElementById('onbV'), D=document.getElementById('device').getBoundingClientRect(), K=D.width/390, rec={t:Math.round(t)};
      rec.onb=!!v; rec.voile=voile();
      var mm=v&&v.querySelector('.onbv-mm'), ph=document.getElementById('onbPh');
      rec.mm=vis(mm); rec.mmClip=mm?(mm.style.clipPath||''):''; rec.ph=vis(ph); rec.phClip=ph?(ph.style.clipPath||''):'';
      if(v){ var bas=0, cp=v.style.clipPath||''; var mt=/inset\(0px 0px ([\d.]+)px/.exec(cp)||/inset\(0 0 ([\d.]+)px/.exec(cp); if(mt) bas=+mt[1];
        rec.blocs=[].map.call(v.children, function(e){ if(e===mm||e.classList.contains('voile-cellules')) return null; var c=getComputedStyle(e); if(c.display==='none') return null;
          var r=e.getBoundingClientRect(), y0=(r.top-D.top)/K, y1=(r.bottom-D.top)/K, h=Math.max(0, Math.min(y1, 844-bas, 844)-Math.max(y0, 0)), w=Math.max(0, Math.min(r.right, D.right)-Math.max(r.left, D.left))/K;
          return [String(e.className).slice(0,24), c.visibility==='hidden'?0:Math.round(h*w), c.transitionProperty, c.transitionDuration]; }).filter(Boolean);
        if((k++)%3===0){ var op=0; v.querySelectorAll('*').forEach(function(e){ var o=+getComputedStyle(e).opacity; if(o>0.02&&o<0.98 && e.getBoundingClientRect().width>2) op++; }); rec.op=op; }
        if(mm){ var a=mm.getBoundingClientRect(), am=document.querySelector('#accPlat .acc-mm'), b=am?am.getBoundingClientRect():null; rec.mmEcart=b?Math.max(Math.abs(a.left-b.left), Math.abs(a.top-b.top), Math.abs(a.width-b.width))/K:null;
          rec.mmB=[Math.round((a.left-D.left)/K), Math.round((a.top-D.top)/K), Math.round(a.width/K)]; rec.amB=b?[Math.round((b.left-D.left)/K), Math.round((b.top-D.top)/K), Math.round(b.width/K)]:null; } }
      var pl=document.getElementById('accPlat'), br=document.getElementById('accBarre'); rec.pl=pl?pl.style.transform:''; rec.br=br?br.style.transform:'';
      try{ rec.vois=window.Toile_voisinesEtat?Toile_voisinesEtat():null; }catch(_){ rec.vois=null; }
      rec.guide=!!document.getElementById('guide'); rec.compte=!!document.querySelector('.onbv-compte');
      try{ var st=window.Toile_state&&Toile_state(); rec.bouge=!!(st&&st.running); }catch(_){ rec.bouge=null; }
      window.__T.push(rec); if(window.__T.length>9000) window.__T.splice(0, 3000); }catch(e){ window.__Terr=String(e); }
    requestAnimationFrame(f); })(); })();"""

def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def centre(pg, sel): return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
TRACE_FINI = "()=>![...document.querySelectorAll('#onbV .onbv-a')].some(e=>getComputedStyle(e).display!=='none' && (e.style.visibility==='hidden' || (e.style.clipPath && e.style.clipPath!=='none')))"
def attend(pg):
    for _ in range(60):
        if pg.evaluate(TRACE_FINI): break
        pg.wait_for_timeout(150)
def trace(pg, cdp):
    z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    if not z or not z['dep']: return False
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); pg.wait_for_timeout(90)
    for i in range(1, 25):
        u = i / 24.0; cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * u, 'y': y0 + (y1 - y0) * u - 14 * z['k'] * (1 - abs(2 * u - 1))}]}); pg.wait_for_timeout(22)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); return True
def ty(s):
    import re
    m = re.search(r'translateY\((-?[\d.]+)px\)', s or ''); return float(m.group(1)) if m else 0.0

def passe(b, th):
    T = th; print('\n── %s' % T)
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','%s'); }catch(e){}" % ('light' if th == 'clair' else 'dark'))
    ctx.add_init_script(SONDE)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(6500); attend(pg)
    S = pg.evaluate("()=>window.__T")
    # ── T1
    V = [(s['t'], s['voile']) for s in S if s['onb']]
    av = [(t, v) for t, v in V if v]
    if not av:
        juge('[%s] T1 · un voile du fond de la Toile couvre la page, puis la Toile naît cellule par cellule' % T, False, 'aucun voile vu')
    else:
        premier = av[0][1]; ouv = [v[0] for _, v in av]; mid = max(v[2] for _, v in av)
        fin_i = next((i for i, (t, v) in enumerate(V) if t > av[-1][0] and not v), None)
        pas = [b_ - a_ for a_, b_ in zip(ouv, ouv[1:])]; marches = len(set(round(x, 3) for x in ouv))
        duree = (av[-1][0] - next(t for t, v in av if v[0] > 0.01)) / 1000.0 if any(v[0] > 0.01 for _, v in av) else 0
        juge('[%s] T1 · à la première image le voile couvre la page (≥ 95 %%), rien de la Toile ne paraît encore' % T, premier[1] >= 0.95, 'plein %.0f %% · ouvert %.0f %%' % (premier[1] * 100, premier[0] * 100))
        if CHARGE < 4:
            juge('[%s] T1 · en direct : ≥ 12 pas, jamais plus de 20 %% d\'un coup, jamais en arrière' % T, marches >= 12 and max(pas or [1]) <= 0.20 and min(pas or [0]) >= -0.002, '%d pas · plus grand %.0f %% · ouvert de %.0f à %.0f %%' % (marches, max(pas or [0]) * 100, ouv[0] * 100, ouv[-1] * 100))
            juge('[%s] T1 · en 0,8 à 1,6 s' % T, 0.8 <= duree <= 1.6, '%.2f s' % duree)
        else: print('      (non jugé en direct : cadence, charge du Mac %.1f ≥ 4 — C-137 ; relevé : %d pas, plus grand %.0f %%, %.2f s)' % (CHARGE, marches, max(pas or [0]) * 100, duree))
        juge('[%s] T1 · le voile ne se referme jamais' % T, min(pas or [0]) >= -0.002, 'plus grand recul %.1f %%' % (-min(pas or [0]) * 100))
        juge('[%s] T1 · ni fondu ni dégradé : aucun pixel à demi transparent dans le voile (≤ 3 %%, le lissage du bord des cellules)' % T, mid <= 0.03, '%.1f %% au plus' % (mid * 100))
        t_fin = av[-1][0]
        avant = [s for s in S if s['onb'] and s['t'] <= t_fin and (s['mm'] or s['ph']) and not (s['mmClip'] and s['mmClip'] != 'none') and not (s['phClip'] and s['phClip'] != 'none')]
        trace_ = any(s['t'] > t_fin and ((s['mmClip'] and s['mmClip'] != 'none') or (s['phClip'] and s['phClip'] != 'none')) for s in S)
        juge('[%s] T1 · le mot-marque et « Toi, c\'est … ? » n\'arrivent qu\'APRÈS la Toile, par le tracé (une découpe), jamais d\'un coup' % T, not avant and trace_, '%d image(s) avec du texte entier avant la fin du voile · tracé vu %s' % (len(avant), trace_))
    V2 = pg.evaluate("""()=>{ const v=document.getElementById('onbV'); if(!v||!window._voileCellules) return null; const c=_voileCellules(v,{mode:'nait', attend:true, duree:1100}); if(!c||!c.image) return null;
        const p=document.createElement('canvas'); p.width=39; p.height=84; const g=p.getContext('2d',{willReadFrequently:true}), out=[];
        const tc=document.getElementById('toileCv').getBoundingClientRect(), V=v.getBoundingClientRect(), kx=c.canevas.width/V.width, ky=c.canevas.height/V.height;
        const sx=Math.max(0,(tc.left-V.left)*kx), sy=Math.max(0,(tc.top-V.top)*ky), sw=Math.min(c.canevas.width-sx, tc.width*kx), sh=Math.min(c.canevas.height-sy, tc.height*ky);
        for(let t=0;t<=1120;t+=20){ c.image(t); g.clearRect(0,0,39,84); g.drawImage(c.canevas,sx,sy,sw,sh,0,0,39,84); const d=g.getImageData(0,0,39,84).data; let o=0,m=0,n=0; for(let i=3;i<d.length;i+=4){ n++; if(d[i]<10) o++; else if(d[i]<=245) m++; } out.push([o/n, m/n]); }
        c.canevas.remove(); return out; }""")
    if V2:
        ouv = [x[0] for x in V2]; pas2 = [b_ - a_ for a_, b_ in zip(ouv, ouv[1:])]; marches = len(set(round(x, 3) for x in ouv))
        juge('[%s] T1 · la Toile naît CELLULE PAR CELLULE — le voile joué image par image (20 ms) : ≥ 12 pas, jamais plus de 20 %% d\'un coup, jamais en arrière, de 0 à 100 %%' % T,
             marches >= 12 and max(pas2) <= 0.20 and min(pas2) >= -0.002 and ouv[0] <= 0.06 and ouv[-1] >= 0.98 and max(x[1] for x in V2) <= 0.03, '%d pas · plus grand %.0f %% · de %.0f à %.0f %% · demi-teintes %.1f %%' % (marches, max(pas2) * 100, ouv[0] * 100, ouv[-1] * 100, max(x[1] for x in V2) * 100))
    else: juge('[%s] T1 · le voile se joue image par image' % T, False, 'pas de voile')
    # ── le parcours jusqu'au compte
    c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900); attend(pg)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(900); attend(pg)
    trace(pg, cdp); pg.wait_for_timeout(6400)
    toucher(cdp, pg, 195, 300); pg.wait_for_timeout(2500); attend(pg); toucher(cdp, pg, 195, 300); pg.wait_for_timeout(1500); attend(pg)
    pg.evaluate("()=>{ window.__T.length=0; }")
    c = centre(pg, '.onbv-compte .tard'); t_tap = pg.evaluate("()=>Math.round(performance.now()-window.__T0)")
    if c: toucher(cdp, pg, c[0], c[1])
    pg.wait_for_timeout(4200)
    S = pg.evaluate("()=>window.__T")
    if not c or not S:
        juge('[%s] le parcours va jusqu\'au compte' % T, False); ctx.close(); return
    # ── T2 · les voisines
    v0 = next((s['vois'] for s in S if s['vois']), None)
    deps = sorted(d['depart'] for d in (next((s['vois'] for s in S if s['vois'] and all(x['depart'] is not None for x in s['vois'])), []) or []))
    ecarts = [b_ - a_ for a_, b_ in zip(deps, deps[1:])]
    restant = S[-1]['vois']
    juge('[%s] T2 · les voisines se résorbent UNE À UNE (départs étalés de 60 à 120 ms, jamais deux ensemble), il n\'en reste aucune' % T,
         bool(v0) and len(v0) >= 3 and len(deps) == len(v0) and ecarts and min(ecarts) >= 60 and max(ecarts) <= 120 and restant == [],
         '%d voisines · écarts %s ms · restantes %s' % (len(v0 or []), ecarts[:8], len(restant) if restant is not None else None))
    # ── T3 · la page
    i0 = next((i for i, s in enumerate(S) if s['pl'] and ty(s['pl']) < -1), None)
    deb = S[i0]['t'] if i0 is not None else None
    if CHARGE < 4: juge('[%s] enchaînement · du toucher sur « Plus tard » au début de la descente : 0,7 s au plus' % T, deb is not None and deb - t_tap <= 700, '%s ms' % (None if deb is None else deb - t_tap))
    if S:
        noms = {}
        for s in S:
            if not s['onb']: break
            for nm, a, tp, td in (s.get('blocs') or []):
                noms.setdefault(nm, []).append(a)
        sauts = []
        for nm, L in noms.items():
            a0 = max(L) if L else 0
            if a0 < 200: continue
            mx = max([max(0, a_ - b_) for a_, b_ in zip(L, L[1:])] or [0])
            sauts.append((nm, round(mx * 100.0 / a0), round(min(L[-3:]) * 100.0 / a0) if len(L) >= 3 else 100))
        juge('[%s] T3 · rien ne disparaît d\'un coup : chaque bloc de la page passe derrière la barre (≤ 35 %% de sa surface par image, ≤ 5 %% avant d\'être masqué)' % T,
             bool(sauts) and all(sp <= 35 and fin <= 5 for _, sp, fin in sauts), sauts[:4])
    cpt = next((b_ for s in S for b_ in (s.get('blocs') or []) if 'onbv-compte' in b_[0]), None)
    juge('[%s] T3 · le panneau du compte s\'en va en GLISSANT (une transition de transform, ≥ 0,3 s), pas d\'un coup' % T, bool(cpt) and 'transform' in cpt[2] and float((cpt[3] or '0s').split(',')[0].rstrip('s') or 0) >= 0.3, cpt)
    ops = max([s.get('op', 0) for s in S if s['onb']] or [0])
    juge('[%s] T3 · ni fondu ni dégradé : aucun nœud de l\'onboarding à demi transparent pendant la sortie' % T, ops == 0, '%d nœud(s) au pire' % ops)
    # ── T4 · l'accueil
    P = [ty(s['pl']) for s in S if s['onb'] and s['pl']]; B = [ty(s['br']) for s in S if s['onb'] and s['br']]
    juge('[%s] T4 · le plateau descend et la barre monte par aplats : ≥ 15 images, sans revenir en arrière, jusqu\'à leur place' % T,
         len(P) >= 15 and len(B) >= 15 and all(b_ >= a_ - 0.01 for a_, b_ in zip(P, P[1:])) and all(b_ <= a_ + 0.01 for a_, b_ in zip(B, B[1:])) and P[0] <= -100 and B[0] >= 100,
         '%d / %d images · plateau %.0f → %.0f · barre %.0f → %.0f' % (len(P), len(B), P[0] if P else 0, P[-1] if P else 0, B[0] if B else 0, B[-1] if B else 0))
    dern = [s for s in S if s['onb'] and s.get('mmEcart') is not None]
    ecart = dern[-1]['mmEcart'] if dern else None
    mm_vu = bool(dern) and any((s.get('mmB') or [0, 0, 0])[2] > 2 for s in dern)
    if '--dbg' in sys.argv: print('   mm', [(s['t'] - t_tap, s.get('mmB'), s.get('amB')) for s in dern[-4:]]); print('   blocs', [(s['t'] - t_tap, s.get('blocs')) for s in S[i0:i0 + 40:6]] if i0 is not None else None)
    if mm_vu: juge('[%s] T4 · le mot-marque de l\'onboarding finit EXACTEMENT sur celui du plateau (± 1 pt), puis la page s\'en va sans que rien ne change' % T, ecart is not None and ecart <= 1.0, '%s pt' % (None if ecart is None else round(ecart, 2)))
    else: print('      (T4 · le mot-marque de l\'onboarding n\'est pas à l\'écran à l\'étape du compte : c\'est celui du plateau qui descend avec lui)')
    t_off = next((s['t'] for s in S if not s['onb']), None); t_g = next((s['t'] for s in S if s['guide']), None)
    t_calme = max([s['t'] for s in S if (s['onb'] or s.get('bouge')) and (t_g is None or s['t'] < t_g)] or [0])
    if CHARGE >= 4: print('      (non jugé : durées, charge du Mac %.1f ≥ 4 — C-137 ; relevé : descente à %s ms du toucher, dernier mouvement à %s ms, guide à %s ms)' % (CHARGE, None if deb is None else deb - t_tap, t_calme - t_tap, None if t_g is None else t_g - t_tap))
    else: juge('[%s] T4 · puis le guide : 0,4 à 1,2 s après que plus rien ne bouge (la décision de v144 : 0,6 s)' % T, t_g is not None and 0.4 <= (t_g - t_calme) / 1000.0 <= 1.2, 'dernier mouvement à %s ms · guide à %s ms' % (t_calme - t_tap, None if t_g is None else t_g - t_tap))
    if CHARGE < 4: juge('[%s] enchaînement · du toucher au guide, pas de temps mort : 3,5 s au plus (la sortie, la Toile qui reprend son cadrage pendant elle, puis le calme)' % T, t_g is not None and (t_g - t_tap) <= 3500, '%s ms' % (None if t_g is None else t_g - t_tap))
    err = pg.evaluate("()=>window.__Terr||null")
    juge('[%s] aucune erreur de page (ni de la sonde)' % T, not er and not err, (er[:2], err))
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ([TH] if TH else ['clair', 'sombre']): passe(b, th)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
