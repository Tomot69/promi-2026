#!/usr/bin/env python3
"""
redteam_transitions_onb.py — LES TRANSITIONS DE L'ONBOARDING, EN FLAQUES (v148, Tom, 16 oct. 2026 — C-141 rouvert ; v147 : l'écriture d'avant,
sauvegardes/redteam_transitions_onb-avant-v148.py).

« Les transitions de l'onboarding sont encore cheap. Le flou en flaques, lui, est validé : c'est donc ce langage-là qui sert aux transitions. Le
balayage d'écran qui suit la page de texte : supprime-le. À sa place, des flaques abstraites, comme celles du flou, remplacent l'écran : la page
suivante naît en flaques et recouvre l'ancienne. Toutes les autres transitions passent au même langage, sauf l'arrivée douce des encarts.
Rien n'arrive d'un coup. Pas de balayage, pas de fondu. »

Le juge lit la page IMAGE PAR IMAGE (un relevé à chaque `requestAnimationFrame`), par le vrai chemin au doigt (stockage vierge, Chromium, vrai GPU,
390 × 844), en clair et en sombre. Un PASSAGE est un canevas `.passage-flaques` (mode « ouvre » : il couvre, puis s'ouvre en flaques ; « couvre » :
il naît en flaques par-dessus) ; on lit sa part couverte à chaque image.
  T1 · l'arrivée sur le prénom : le voile couvre tout à la première image, s'ouvre sans jamais se refermer, sans demi-teinte ; EN FLAQUES (rejoué
       image par image : ≥ 12 pas, jamais plus de 20 % d'un coup, et dès le premier quart PLUSIEURS trous séparés — des flaques nées à différents
       endroits, pas des cellules qui s'ouvrent depuis le milieu) ; les textes n'arrivent qu'après, par le tracé ;
  T2 · le trait du premier Promi : il naît en flaques 1 s après le prénom (v155, C-169 ; avant : à la première lettre) — un passage « ouvre » sur lui, qui part couvert et s'ouvre ;
  T3 · la page du trait part : un passage « couvre » la recouvre (de presque rien à tout) ; aucun nœud à demi transparent (pas de fondu) ;
  T4 · de « Promi planté ! » au compte : PLUS DE BALAYAGE (le message n'est jamais découpé d'un bord) ; il est recouvert en flaques ; le panneau du
       compte naît en flaques à sa place (il ne glisse pas) ;
  T5 · du compte à l'accueil : le panneau est recouvert en flaques ; puis un passage plein écran s'ouvre en flaques, les voisines déjà parties ;
  T6 · l'arrivée douce des encarts (validée, intouchable) : le plateau descend et la barre monte par aplats (≥ 15 images, sans retour) ;
  et, au calme seulement (C-137) : les durées et le guide.
Preuve (§7) : `--fichier=zz-av147.html` rougit (T1 : cellules, pas de flaques ; T2–T5 : aucun passage).
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
        rec.blocs=[].map.call(v.children, function(e){ if(e===mm||e.classList.contains('voile-cellules')||e.classList.contains('passage-flaques')) return null; var c=getComputedStyle(e); if(c.display==='none') return null;
          var r=e.getBoundingClientRect(), y0=(r.top-D.top)/K, y1=(r.bottom-D.top)/K, h=Math.max(0, Math.min(y1, 844-bas, 844)-Math.max(y0, 0)), w=Math.max(0, Math.min(r.right, D.right)-Math.max(r.left, D.left))/K;
          return [String(e.className).slice(0,24), c.visibility==='hidden'?0:Math.round(h*w), c.transitionProperty, c.transitionDuration]; }).filter(Boolean);
        if((k++)%3===0){ var op=0; v.querySelectorAll('*').forEach(function(e){ var o=+getComputedStyle(e).opacity; if(o>0.02&&o<0.98 && e.getBoundingClientRect().width>2) op++; }); rec.op=op; }
        if(mm){ var a=mm.getBoundingClientRect(), am=document.querySelector('#accPlat .acc-mm'), b=am?am.getBoundingClientRect():null; rec.mmEcart=b?Math.max(Math.abs(a.left-b.left), Math.abs(a.top-b.top), Math.abs(a.width-b.width))/K:null;
          rec.mmB=[Math.round((a.left-D.left)/K), Math.round((a.top-D.top)/K), Math.round(a.width/K)]; rec.amB=b?[Math.round((b.left-D.left)/K), Math.round((b.top-D.top)/K), Math.round(b.width/K)]:null; } }
      var pl=document.getElementById('accPlat'), br=document.getElementById('accBarre'); rec.pl=pl?pl.style.transform:''; rec.br=br?br.style.transform:'';
      try{ rec.vois=window.Toile_voisinesEtat?Toile_voisinesEtat():null; }catch(_){ rec.vois=null; }
      rec.guide=!!document.getElementById('guide'); rec.compte=!!document.querySelector('.onbv-compte');
      rec.pass=[].map.call(document.querySelectorAll('canvas.passage-flaques'), function(c){ var r=c.getBoundingClientRect(); return {m:c.getAttribute('data-mode'), u:+(c.getAttribute('data-u')||0), cl:String(c.className),
        r:[Math.round((r.left-D.left)/K), Math.round((r.top-D.top)/K), Math.round(r.width/K), Math.round(r.height/K)], c:(function(){ try{ if(!c.width) return null; var q=document.createElement('canvas'); q.width=20; q.height=20; var g=q.getContext('2d'); g.drawImage(c,0,0,20,20); var d=g.getImageData(0,0,20,20).data, n=0; for(var i=3;i<d.length;i+=4) if(d[i]>10) n++; return n/400; }catch(_){ return null; } })()}; });
      var fn=document.getElementById('onbFin'); rec.finClip=fn?(fn.style.clipPath||fn.style.webkitClipPath||''):''; rec.finVu=fn?(getComputedStyle(fn).display!=='none'):false;
      var cp=document.querySelector('.onbv-compte'); rec.cptTr=cp?(cp.style.transform||getComputedStyle(cp).transform):null; rec.cptR=cp?(function(){ var r=cp.getBoundingClientRect(); return [Math.round((r.left-D.left)/K), Math.round((r.top-D.top)/K), Math.round(r.width/K), Math.round(r.height/K)]; })():null;
      var tr=document.getElementById('onbTrait'); rec.trait=tr?getComputedStyle(tr).display!=='none':false; var hh=document.getElementById('onbHaut'); rec.haut=hh?[getComputedStyle(hh).display, getComputedStyle(hh).visibility, +getComputedStyle(hh).opacity]:null;
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

def suite_c(S, pred):
    """la vie d'un passage, image par image : [(t, c, u)] du premier passage qui répond à `pred` (par mode et place)"""
    out = []
    for s in S:
        L = [q for q in (s.get('pass') or []) if pred(q)]
        if L: out.append((s['t'], L[0]['c'] if L[0]['c'] is not None else -1, L[0]['u']))
    return out
def monotone(C, sens):
    return all((b_[1] - a_[1]) * sens >= -0.03 for a_, b_ in zip(C, C[1:]))
def taches(cv_alpha, W, H, seuil=10, mini=4):
    """le nombre de trous séparés (pixels ouverts, 4-connexes) d'au moins `mini` cellules"""
    vu = [False] * (W * H); n = 0
    for i0 in range(W * H):
        if vu[i0] or cv_alpha[i0] >= seuil: continue
        pile = [i0]; vu[i0] = True; k = 0
        while pile:
            i = pile.pop(); k += 1; x, y = i % W, i // W
            for j in ((i - 1) if x > 0 else -1, (i + 1) if x < W - 1 else -1, (i - W) if y > 0 else -1, (i + W) if y < H - 1 else -1):
                if j >= 0 and not vu[j] and cv_alpha[j] < seuil: vu[j] = True; pile.append(j)
        if k >= mini: n += 1
    return n

def pas_fin(pg, cdp):
    """un toucher sur « Promi planté ! » fait paraître le paragraphe suivant (C-124 §9) ; on attend qu'il soit écrit"""
    if not pg.evaluate("()=>!!window._onbFinPas"):   # une version d'avant le pas à pas (v147) : un toucher fait venir tout le reste
        toucher(cdp, pg, 195, 120); pg.wait_for_timeout(2500); attend(pg); return False
    a = pg.evaluate("()=>(window._onbFinPas&&_onbFinPas())||{pas:0}")['pas']; toucher(cdp, pg, 195, 120)
    for _ in range(100):
        pg.wait_for_timeout(120); e = pg.evaluate("()=>(window._onbFinPas&&_onbFinPas())||{pas:0,enCours:false}")
        if e['pas'] > a and not e['enCours']: break
    attend(pg); return True

def passe(b, th):
    T = th; print('\n── %s' % T)
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','%s'); }catch(e){}" % ('light' if th == 'clair' else 'dark'))
    ctx.add_init_script(SONDE)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(6500); attend(pg)
    S = pg.evaluate("()=>window.__T")
    # ── T1 · l'arrivée sur le prénom
    V = [(s['t'], s['voile']) for s in S if s['onb']]
    av = [(t, v) for t, v in V if v]
    if not av:
        juge('[%s] T1 · un voile du fond de la Toile couvre la page, puis s\'ouvre en flaques' % T, False, 'aucun voile vu')
    else:
        premier = av[0][1]; ouv = [v[0] for _, v in av]; mid = max(v[2] for _, v in av)
        pas = [b_ - a_ for a_, b_ in zip(ouv, ouv[1:])]; marches = len(set(round(x, 3) for x in ouv))
        duree = (av[-1][0] - next(t for t, v in av if v[0] > 0.01)) / 1000.0 if any(v[0] > 0.01 for _, v in av) else 0
        juge('[%s] T1 · à la première image le voile couvre la page (≥ 95 %%), rien de la Toile ne paraît encore' % T, premier[1] >= 0.95, 'plein %.0f %% · ouvert %.0f %%' % (premier[1] * 100, premier[0] * 100))
        if CHARGE < 4:
            juge('[%s] T1 · en direct : ≥ 12 pas, jamais plus de 20 %% d\'un coup' % T, marches >= 12 and max(pas or [1]) <= 0.20, '%d pas · plus grand %.0f %% · ouvert de %.0f à %.0f %%' % (marches, max(pas or [0]) * 100, ouv[0] * 100, ouv[-1] * 100))
            juge('[%s] T1 · en 0,8 à 1,6 s' % T, 0.8 <= duree <= 1.6, '%.2f s' % duree)
        else: print('      (non jugé en direct : cadence, charge du Mac %.1f ≥ 4 — C-137 ; relevé : %d pas, plus grand %.0f %%, %.2f s)' % (CHARGE, marches, max(pas or [0]) * 100, duree))
        juge('[%s] T1 · le voile ne se referme jamais' % T, min(pas or [0]) >= -0.002, 'plus grand recul %.1f %%' % (-min(pas or [0]) * 100))
        juge('[%s] T1 · ni fondu ni dégradé : aucun pixel à demi transparent dans le voile (≤ 3 %%, le lissage du bord des flaques)' % T, mid <= 0.03, '%.1f %% au plus' % (mid * 100))
        t_fin = av[-1][0]
        avant = [s for s in S if s['onb'] and s['t'] <= t_fin and (s['mm'] or s['ph']) and not (s['mmClip'] and s['mmClip'] != 'none') and not (s['phClip'] and s['phClip'] != 'none')]
        trace_ = any(s['t'] > t_fin and ((s['mmClip'] and s['mmClip'] != 'none') or (s['phClip'] and s['phClip'] != 'none')) for s in S)
        juge('[%s] T1 · le mot-marque et « Toi, c\'est … ? » n\'arrivent qu\'APRÈS la Toile, par le tracé (une découpe), jamais d\'un coup' % T, not avant and trace_, '%d image(s) avec du texte entier avant la fin du voile · tracé vu %s' % (len(avant), trace_))
    V2 = pg.evaluate("""()=>{ const v=document.getElementById('onbV'); if(!v||!window._passageFlaques) return null;
        const c=_passageFlaques(v,{mode:'ouvre', attend:true, couleur:'#DFCAA4', duree:1100, graine:4242}); if(!c||!c.image) return null;
        const p=document.createElement('canvas'); p.width=39; p.height=84; const g=p.getContext('2d',{willReadFrequently:true}), out=[];
        const q=document.createElement('canvas'); q.width=78; q.height=168; const gq=q.getContext('2d',{willReadFrequently:true});
        for(let t=0;t<=1120;t+=20){ c.image(t); g.clearRect(0,0,39,84); g.drawImage(c.canevas,0,0,39,84); const d=g.getImageData(0,0,39,84).data; let o=0,m=0,n=0; for(let i=3;i<d.length;i+=4){ n++; if(d[i]<10) o++; else if(d[i]<=245) m++; }
          gq.clearRect(0,0,78,168); gq.drawImage(c.canevas,0,0,78,168); const e=gq.getImageData(0,0,78,168).data, A=[]; for(let i=3;i<e.length;i+=4) A.push(e[i]);
          out.push([o/n, m/n, A]); }
        c.canevas.remove(); return out; }""")
    if V2:
        ouv = [x[0] for x in V2]; pas2 = [b_ - a_ for a_, b_ in zip(ouv, ouv[1:])]; marches = len(set(round(x, 3) for x in ouv))
        juge('[%s] T1 · le voile joué image par image (20 ms) s\'ouvre progressivement : ≥ 12 pas, jamais plus de 20 %% d\'un coup, jamais en arrière, de 0 à 100 %%, sans demi-teinte' % T,
             marches >= 12 and max(pas2) <= 0.20 and min(pas2) >= -0.002 and ouv[0] <= 0.06 and ouv[-1] >= 0.98 and max(x[1] for x in V2) <= 0.03, '%d pas · plus grand %.0f %% · de %.0f à %.0f %% · demi-teintes %.1f %%' % (marches, max(pas2) * 100, ouv[0] * 100, ouv[-1] * 100, max(x[1] for x in V2) * 100))
        q_ = [(o, taches(A, 78, 168)) for o, m, A in V2 if 0.08 <= o <= 0.45]
        nt = max([n for o, n in q_] or [0])
        juge('[%s] T1 · EN FLAQUES : quand 8 à 45 %% sont ouverts, plusieurs trous séparés (≥ 3) — des flaques nées à divers endroits, pas un front qui s\'ouvre' % T, nt >= 3, 'trous séparés au plus : %d (%s)' % (nt, [(round(o * 100), n) for o, n in q_][:8]))
    else: juge('[%s] T1 · le voile s\'ouvre en flaques (_passageFlaques)' % T, False, 'pas de passage en flaques dans la page')
    # ── T2 · le trait du premier Promi naît en flaques
    c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
    # ⚑ v155 (Tom, C-169 §4.4) : le trait et « trace pour planter » paraissent 1 s APRÈS la validation du prénom (plus à la première lettre de la parole)
    pg.keyboard.press('Enter'); pg.wait_for_function("()=>!window._onbInvite||!window._onbInvite.etat().ecrit", timeout=12000); 
    c = centre(pg, '[data-onb="parole"]'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300)   # ⚑ v153 (C-164) : le clavier est fermé après le prénom
    # ⚑ v173 (C-211) : le trait paraît la promesse complétée, le clavier refermé (plus 1,5 s après le prénom)
    pg.keyboard.type('marcher une heure', delay=25); pg.wait_for_timeout(300); pg.evaluate("()=>{ window.__T.length=0; }"); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
    S = pg.evaluate("()=>window.__T"); attend(pg); pg.wait_for_timeout(600)
    i_tr = next((i for i, s in enumerate(S) if s.get('trait')), None)
    if i_tr is None: juge('[%s] T2 · le trait paraît 1 s après le prénom (v155)' % T, False, 'pas de trait')
    else:
        P0 = [q for q in (S[i_tr].get('pass') or []) if q['m'] == 'ouvre' and q['r'][1] > 250]
        juge('[%s] T2 · à l\'image où le trait paraît, il est COUVERT (l\'image de la Toile, ≥ 85 %%) — rien n\'arrive d\'un coup' % T, bool(P0) and P0[0]['c'] is not None and P0[0]['c'] >= 0.85, P0[:1])
        C = suite_c(S[i_tr:], lambda q: q['m'] == 'ouvre' and q['r'][1] > 250)
        inter = sum(1 for t, c_, u in C if 0.1 < c_ < 0.85)
        juge('[%s] T2 · puis la couverture s\'ouvre en flaques jusqu\'au bout, sans jamais se refermer' % T, len(C) >= 2 and monotone(C, -1) and C[-1][2] >= 0.75, '%d images · de %.0f à %.0f %% · u final %.2f' % (len(C), (C[0][1] if C else 0) * 100, (C[-1][1] if C else 0) * 100, C[-1][2] if C else 0))
        if CHARGE < 4: juge('[%s] T2 · en direct : ≥ 4 images intermédiaires' % T, inter >= 4, '%d' % inter)
    # ── T3 · la page du trait part : la Toile la recouvre en flaques
    pg.evaluate("()=>{ window.__T.length=0; }"); trace(pg, cdp); pg.wait_for_timeout(6400)
    S = pg.evaluate("()=>window.__T")
    C = suite_c(S, lambda q: q['m'] == 'couvre' and q['r'][1] < 520)
    juge('[%s] T3 · la page du trait est recouverte EN FLAQUES (un passage qui naît de presque rien et couvre tout, sans reculer)' % T, len(C) >= 2 and C[0][1] <= 0.25 and max(c_ for t, c_, u in C) >= 0.85 and monotone(C, 1), '%d images · de %.0f à %.0f %%' % (len(C), (C[0][1] if C else 0) * 100, (max(c_ for t, c_, u in C) if C else 0) * 100))
    i_h = next((i for i, s in enumerate(S) if s.get('haut') and s['haut'][1] == 'hidden'), None)
    cache_ok = i_h is not None and any(q['m'] == 'couvre' and (q['c'] or 0) >= 0.85 for s in S[max(0, i_h - 1):i_h + 1] for q in (s.get('pass') or []))
    juge('[%s] T3 · la page n\'est retirée que sous la couverture (≥ 85 %% couvert à cet instant)' % T, cache_ok, 'retirée à l\'image %s' % i_h)
    fondu = [round(s['haut'][2], 2) for s in S if s.get('haut') and s['haut'][0] != 'none' and s['haut'][1] != 'hidden' and s['haut'][2] < 0.98]
    juge('[%s] T3 · pas de fondu : la page reste opaque jusqu\'à ce qu\'elle soit couverte' % T, not fondu, fondu[:5])
    # ── « Promi planté ! » pas à pas, puis le compte
    for _ in range(3):
        if not pas_fin(pg, cdp): break
    fini_ = pg.evaluate("()=>{ const v=document.getElementById('onbV'); return v?v.getAttribute('data-onb-reste'):null; }")
    pg.wait_for_timeout(600); pg.evaluate("()=>{ window.__T.length=0; }"); toucher(cdp, pg, 195, 120); pg.wait_for_timeout(2600)
    S = pg.evaluate("()=>window.__T")
    if not any(s.get('compte') for s in S):
        juge('[%s] le parcours va jusqu\'au compte (trois touchers pour les trois paragraphes, un quatrième pour le compte)' % T, False, 'reste : %s' % fini_); ctx.close(); return
    clips = sorted(set(s.get('finClip') for s in S if s.get('finClip') not in ('', 'none', None)))
    juge('[%s] T4 · PLUS DE BALAYAGE : « Promi planté ! » n\'est jamais découpé d\'un bord' % T, not clips, clips[:3])
    C = suite_c([s for s in S if s.get('finVu')], lambda q: q['m'] == 'couvre')
    juge('[%s] T4 · « Promi planté ! » est recouvert EN FLAQUES avant de partir (≥ 85 %% couvert, sans reculer)' % T, len(C) >= 2 and max(c_ for t, c_, u in C) >= 0.85 and monotone(C, 1), '%d images · au plus %.0f %%' % (len(C), (max(c_ for t, c_, u in C) if C else 0) * 100))
    i_c = next((i for i, s in enumerate(S) if s.get('compte')), None)
    P0 = [q for q in (S[i_c].get('pass') or []) if q['m'] == 'ouvre' and S[i_c].get('cptR') and abs(q['r'][1] - S[i_c]['cptR'][1]) <= 8]
    juge('[%s] T4 · le panneau du compte naît EN FLAQUES à sa place : couvert à sa première image (≥ 85 %%)' % T, bool(P0) and (P0[0]['c'] or 0) >= 0.85, P0[:1])
    C = suite_c(S[i_c:], lambda q: q['m'] == 'ouvre' and q['r'][1] > 300)
    juge('[%s] T4 · puis la couverture s\'ouvre en flaques jusqu\'au bout, sans jamais se refermer' % T, len(C) >= 2 and monotone(C, -1) and C[-1][2] >= 0.75, '%d images · u final %.2f' % (len(C), C[-1][2] if C else 0))
    tops = [s['cptR'][1] for s in S if s.get('cptR')]
    juge('[%s] T4 · le panneau ne glisse pas : il est à sa place dès sa première image (± 1 pt)' % T, bool(tops) and max(tops) - min(tops) <= 1, '%s → %s' % (min(tops or [0]), max(tops or [0])))
    # ── T5 · du compte à l'accueil
    pg.evaluate("()=>{ window.__T.length=0; }")
    c = centre(pg, '.onbv-compte .tard'); t_tap = pg.evaluate("()=>Math.round(performance.now()-window.__T0)")
    if c: toucher(cdp, pg, c[0], c[1])
    pg.wait_for_timeout(5200)
    S = pg.evaluate("()=>window.__T")
    if not c or not S:
        juge('[%s] « Plus tard » mène à l\'accueil' % T, False); ctx.close(); return
    C = suite_c([s for s in S if s.get('compte')], lambda q: q['m'] == 'couvre')
    juge('[%s] T5 · le panneau du compte est recouvert EN FLAQUES avant de partir (≥ 85 %%, sans reculer)' % T, len(C) >= 2 and max(c_ for t, c_, u in C) >= 0.85 and monotone(C, 1), '%d images · au plus %.0f %%' % (len(C), (max(c_ for t, c_, u in C) if C else 0) * 100))
    PL = lambda q: q['m'] == 'ouvre' and q['r'][2] >= 380 and q['r'][3] >= 800
    C = suite_c(S, PL)
    juge('[%s] T5 · puis l\'écran entier s\'ouvre EN FLAQUES sur l\'accueil (couvert à sa première image, ouvert jusqu\'au bout, sans reculer)' % T, len(C) >= 2 and C[0][1] >= 0.9 and monotone(C, -1) and C[-1][2] >= 0.75, '%d images · de %.0f à %.0f %% · u final %.2f' % (len(C), (C[0][1] if C else 0) * 100, (C[-1][1] if C else 0) * 100, C[-1][2] if C else 0))
    vo = [s.get('vois') for s in S if any(PL(q) and (q['c'] or 1) < 0.7 for q in (s.get('pass') or []))]
    juge('[%s] T5 · les voisines sont parties SOUS la couverture : dès que l\'accueil paraît, il n\'en reste aucune' % T, bool(vo) and all(not x for x in vo), '%d image(s) · voisines %s' % (len(vo), [len(x) if x else 0 for x in vo[:4]]))
    i0 = next((i for i, s in enumerate(S) if s['pl'] and ty(s['pl']) < -1), None)
    deb = S[i0]['t'] if i0 is not None else None
    if S:
        noms = {}
        for s in S:
            if not s['onb']: break
            for nm, a, tp, td in (s.get('blocs') or []):
                noms.setdefault(nm, []).append(a)
        sauts = []
        for nm, L in noms.items():
            a0 = max(L) if L else 0
            if a0 < 200 or 'onbv-compte' in nm: continue   # le panneau du compte : retiré SOUS sa couverture en flaques (jugé juste au-dessus)
            mx = max([max(0, a_ - b_) for a_, b_ in zip(L, L[1:])] or [0])
            sauts.append((nm, round(mx * 100.0 / a0), round(min(L[-3:]) * 100.0 / a0) if len(L) >= 3 else 100))
        juge('[%s] T5 · rien ne disparaît d\'un coup : ce qui reste de la page passe derrière la barre (≤ 35 %% de sa surface par image, ≤ 5 %% avant d\'être masqué)' % T,
             all(sp <= 35 and fin <= 5 for _, sp, fin in sauts), sauts[:4] or 'aucun bloc à l\'écran')
    ops = max([s.get('op', 0) for s in S if s['onb']] or [0])
    juge('[%s] T5 · ni fondu ni dégradé : aucun nœud de l\'onboarding à demi transparent pendant la sortie' % T, ops == 0, '%d nœud(s) au pire' % ops)
    # ── T6 · l'arrivée douce des encarts (validée par Tom : on n'y touche plus)
    P = [ty(s['pl']) for s in S if s['onb'] and s['pl']]; Bb = [ty(s['br']) for s in S if s['onb'] and s['br']]
    juge('[%s] T6 · (validé, inchangé) le plateau descend et la barre monte par aplats : ≥ 15 images, sans revenir en arrière, jusqu\'à leur place' % T,
         len(P) >= 15 and len(Bb) >= 15 and all(b_ >= a_ - 0.01 for a_, b_ in zip(P, P[1:])) and all(b_ <= a_ + 0.01 for a_, b_ in zip(Bb, Bb[1:])) and P[0] <= -100 and Bb[0] >= 100,
         '%d / %d images · plateau %.0f → %.0f · barre %.0f → %.0f' % (len(P), len(Bb), P[0] if P else 0, P[-1] if P else 0, Bb[0] if Bb else 0, Bb[-1] if Bb else 0))
    dern = [s for s in S if s['onb'] and s.get('mmEcart') is not None]
    ecart = dern[-1]['mmEcart'] if dern else None
    mm_vu = bool(dern) and any((s.get('mmB') or [0, 0, 0])[2] > 2 for s in dern)
    if mm_vu: juge('[%s] T6 · le mot-marque de l\'onboarding finit EXACTEMENT sur celui du plateau (± 1 pt)' % T, ecart is not None and ecart <= 1.0, '%s pt' % (None if ecart is None else round(ecart, 2)))
    t_g = next((s['t'] for s in S if s['guide']), None)
    t_calme = max([s['t'] for s in S if (s['onb'] or s.get('bouge')) and (t_g is None or s['t'] < t_g)] or [0])
    if CHARGE >= 4: print('      (non jugé : durées, charge du Mac %.1f ≥ 4 — C-137 ; relevé : arrivée des encarts à %s ms du toucher, dernier mouvement à %s ms, guide à %s ms)' % (CHARGE, None if deb is None else deb - t_tap, t_calme - t_tap, None if t_g is None else t_g - t_tap))
    else:
        juge('[%s] T6 · puis le guide : 0,05 à 0,85 s après que plus rien ne bouge (v144 : 0,6 s ; v155 : 0,35 s ; v156, C-094 : 0,25 s)' % T, t_g is not None and 0.05 <= (t_g - t_calme) / 1000.0 <= 0.85, 'dernier mouvement à %s ms · guide à %s ms' % (t_calme - t_tap, None if t_g is None else t_g - t_tap))
        juge('[%s] enchaînement · du toucher au guide, pas de temps mort : 4,5 s au plus (le panneau recouvert, l\'écran qui s\'ouvre, les encarts, le calme)' % T, t_g is not None and (t_g - t_tap) <= 4500, '%s ms' % (None if t_g is None else t_g - t_tap))
    err = pg.evaluate("()=>window.__Terr||null")
    juge('[%s] aucune erreur de page (ni de la sonde)' % T, not er and not err, (er[:2], err))
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ([TH] if TH else ['clair', 'sombre']): passe(b, th)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
