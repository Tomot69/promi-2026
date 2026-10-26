#!/usr/bin/env python3
"""redteam_veille.py — ⚑ v161 (Tom, C-181) : LA VEILLE.

Banc comme Tom (WebKit, 390 × 844 ×3, doigt, Toile de 5 paroles), `?veille=5` (le délai réduit, pour le banc seulement), `?coin=1` pour le coin :
  A · le départ : rien à 4 s ; la veille à 5 s (± 1,5) ; jamais pendant une saisie (un champ a la main, 9 s) ni pendant un geste (un doigt posé, 9 s) ;
  B · un toucher la quitte et rend l'écran EXACT d'avant (l'Index ouvert : les mêmes écrans affichés, rien d'autre d'ouvert) ; le toucher, posé sur une
      carte de l'Index, n'ouvre rien ; la Toile identique avant et après (graines et vue) ;
  C · une couleur différente à chaque rebond, prise dans la palette du Studio (jamais deux fois la même d'affilée) ;
  D · le vert amande #8FE08F au coin, et seulement au coin ; aucun coin avant 60 s de veille (`?coin=1` : le coin forcé tombe entre 60 et 90 s) ;
  E · ⚑ v162 : le logo rebondit sur les BORDS RÉELS de la zone visible (`visualViewport`, moins les zones sûres du système), c'est son ENCRE (140 × 27 pt
      à l'échelle de l'appareil) qui les touche ; toujours entièrement dedans (relevé toutes les 100 ms) — aux fenêtres 430 × 932 (échelle 1), 330 × 714
      (0,79) et 390 × 651 (celle de l'export de Tom) ;
  K · ⚑ v162 : le fond est celui de la Toile du thème (`_fondToileVif`), en clair et en sombre ; chaque couleur prise par le logo tient 3:1 sur lui ;
  F · le verrou de l'écran (Wake Lock, simulé) : demandé au premier toucher, relâché à 10 min de veille (réglé à 4 s pour le banc), redemandé au retour ;
  G · « Réduire les animations » : le logo fixe au centre, aucun rebond ;
  H · ⚑ v162 : la simulation de 2 heures (la même fonction, 30 tirages) sur les bords réels de chaque fenêtre : 0,3 à 0,5 % des rebonds dans un coin (le
      seul hasard de l'angle), aucun avant la première minute ;
  I · sans `?veille=`, sur le banc, elle ne paraît pas (les autres juges ne la voient jamais).
Preuve : `--fichier=zz-v160c.html` rougit (aucune veille).
"""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
V = "()=>{ try{ return _veille(); }catch(e){ return null; } }"
VERROU = """(()=>{ window.__wl=[]; try{ Object.defineProperty(navigator,'wakeLock',{configurable:true, value:{ request:function(t){ var s={released:false, _l:[],
  addEventListener:function(n,f){ this._l.push(f); }, release:function(){ this.released=true; window.__wl.push('relâché'); this._l.forEach(function(f){ try{ f(); }catch(_){ } }); return Promise.resolve(); } };
  window.__wl.push('demandé'); return Promise.resolve(s); } }}); }catch(e){} })();"""
GEO = "()=>{ var c=Toile_cellules(), v=c.view; return [v.s, v.ox, v.oy].concat(c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid, +s.x.toFixed(2), +s.y.toFixed(2)])); }"
ECRANS = "()=>[...document.querySelectorAll('.screen.show,.sheet.show,#indexSheet.show,#detailPoster.show,#createSheet.show,#feedView.show')].map(e=>e.id).sort()"
def ouvre(b, q='?veille=5', reduit=False, attente=1500, vw=390, vh=844, sombre=False):
    ctx = B.contexte(b, vw=vw, vh=vh, sombre=sombre) if not reduit else None
    if reduit:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA, reduced_motion='reduce')
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__a')){ sessionStorage.setItem('__a','1'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}")
    B.toile_pleine(ctx, 5); ctx.add_init_script(VERROU); return ctx, B.ouvre(ctx, F, q=q, attente=attente)
with sync_playwright() as p:
    b = p.webkit.launch()
    # ── A · le départ ──
    ctx, pg = ouvre(b); pg.wait_for_timeout(2500)
    a4 = (pg.evaluate(V) or {}).get('active')
    pg.evaluate("()=>{ window.__fl=[]; new MutationObserver(m=>m.forEach(r=>r.addedNodes.forEach(n=>{ if(n.classList&&n.classList.contains('passage-flaques')) window.__fl.push(n.getAttribute('data-mode')); }))).observe(document.body,{childList:true, subtree:true}); }")
    pg.wait_for_timeout(3000); v = pg.evaluate(V) or {}
    juge('A · rien à 4 s, la veille à 5 s (± 1,5)', a4 is False and v.get('active') and v.get('depuis', 0) <= 2500, 'à 4 s : %s · ensuite : active %s depuis %s ms' % (a4, v.get('active'), v.get('depuis')))
    anim = pg.evaluate("()=>{ const c=document.getElementById('promiVeille'); if(!c) return null; const F=window._fondToileVif(); return [c.getAnimations({subtree:true}).length, getComputedStyle(c).opacity, getComputedStyle(c).backgroundColor, c.querySelectorAll('*').length, 'rgb('+[1,3,5].map(i=>parseInt(F.substr(i,2),16)).join(', ')+')']; }")
    juge('J · la veille : un fond plein (celui de la Toile du thème), le logo seul, aucune animation CSS (ni fondu ni clignotement)', anim and anim[0] == 0 and anim[1] == '1' and anim[2] == anim[4] and anim[3] == 1, anim)
    B.tap(pg, 195, 400); pg.wait_for_timeout(400); fl = pg.evaluate("()=>window.__fl")
    juge('J · l\'entrée et la sortie passent par les flaques (« couvre » puis « ouvre »), aucun fondu', fl == ['couvre', 'ouvre'], fl)
    ctx.close()
    ctx, pg = ouvre(b); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} const i=document.createElement('input'); i.id='__saisie'; document.getElementById('device').appendChild(i); i.focus(); }")
    pg.wait_for_timeout(9000); s1 = (pg.evaluate(V) or {}).get('active')
    pg.evaluate("()=>{ document.getElementById('__saisie').blur(); }"); pg.wait_for_timeout(6500); s2 = (pg.evaluate(V) or {}).get('active')
    juge('A · jamais pendant une saisie (un champ a la main 9 s) ; la saisie finie, elle vient', s1 is False and s2 is True, 'pendant %s · après %s' % (s1, s2))
    ctx.close()
    ctx, pg = ouvre(b); cdp = ctx.new_cdp_session(pg) if False else None
    D = B.dev(pg); x, y = D[0] + 195 * D[4], D[1] + 400 * D[4]
    pg.evaluate("([x,y])=>{ const e=document.elementFromPoint(x,y); e.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:x,clientY:y,pointerType:'touch',isPrimary:true})); }", [x, y])
    pg.wait_for_timeout(9000); g1 = (pg.evaluate(V) or {}).get('active')
    pg.evaluate("([x,y])=>{ const e=document.elementFromPoint(x,y); e.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:x,clientY:y,pointerType:'touch',isPrimary:true})); }", [x, y])
    juge('A · jamais pendant un geste (un doigt posé 9 s)', g1 is False, 'pendant %s' % g1)
    ctx.close()
    # ── B · l'écran exact, rien d'actionné, la Toile identique ──
    ctx, pg = ouvre(b, attente=800)
    POSE = "()=>{ try{ var st=Toile_state(), l=Toile_lecture(), c=l.cible||l.vue; return !st.running && Math.abs(c.s-l.vue.s)<0.0005 && Math.abs(c.oy-l.vue.oy)<0.3; }catch(e){ return true; } }"
    for _ in range(40):
        if pg.evaluate(POSE): break
        pg.wait_for_timeout(100)
    toile0 = pg.evaluate(GEO); pg.wait_for_timeout(1500)
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(1500); e0 = pg.evaluate(ECRANS)
    pg.wait_for_timeout(6500); act = (pg.evaluate(V) or {}).get('active')
    carte = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const c=document.querySelector('#indexList .s4-carte'); if(!c) return null; const r=c.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }")
    if carte: B.tap(pg, carte[0], carte[1])
    pg.wait_for_timeout(2000); e1 = pg.evaluate(ECRANS); v = pg.evaluate(V) or {}
    fiche = pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); return !!(d && d.classList.contains('show')); }")
    juge('B · le toucher quitte la veille et rend l\'écran exact d\'avant (l\'Index), sans rien ouvrir dessous', act and not v.get('active') and e0 == e1 and not fiche and carte is not None,
         'avant %s · après %s · fiche ouverte %s · veille %s→%s' % (e0, e1, fiche, act, v.get('active')))
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(1500)
    for _ in range(40):
        if pg.evaluate(POSE): break
        pg.wait_for_timeout(100)
    toile1 = pg.evaluate(GEO)
    juge('B · la Toile identique avant et après (graines et vue)', toile0 == toile1, 'vue %s → %s' % (toile0[:3], toile1[:3]))
    ctx.close()
    # ── C, E, F, K · couleurs, bords réels, fond, verrou ──
    FEN = [(430, 932), (330, 714), (390, 651)]
    for vw, vh in (FEN[:1] if VITE else FEN):
      for sombre in ((False,) if VITE else (False, True)):
        E = '%dx%d · %s' % (vw, vh, 'sombre' if sombre else 'clair')
        ctx, pg = ouvre(b, attente=800, vw=vw, vh=vh, sombre=sombre); B.tap(pg, 200, 300); pg.wait_for_timeout(300); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} if(window._veilleRegle) window._veilleRegle.VERROU=4000; }")
        w0 = pg.evaluate("()=>window.__wl.slice()")
        pg.wait_for_timeout(6500); pos = []; hors = []; v0 = pg.evaluate(V) or {}
        for i in range(int(160 if not VITE else 100)):
            v = pg.evaluate(V)
            if v and v['logo']:
                x0, y0, w, h = v['logo']; Bn = v['bornes']; pos.append((x0, y0))
                if x0 < Bn['x0'] - 0.5 or y0 < Bn['y0'] - 0.5 or x0 > Bn['x1'] + 0.5 or y0 > Bn['y1'] + 0.5: hors.append((round(x0, 1), round(y0, 1)))
            pg.wait_for_timeout(100)
        v = pg.evaluate(V) or {'couleurs':[], 'tons':[], 'rebonds':0, 'verrou':None, 'cadre':None, 'bornes':None, 'logo':None, 'fond':None}
        reel = pg.evaluate("()=>{ const vv=visualViewport; const p=document.createElement('div'); p.style.cssText='position:fixed;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)'; document.body.appendChild(p); const c=getComputedStyle(p); const r=[vv.width, vv.height, parseFloat(c.paddingTop)||0, parseFloat(c.paddingRight)||0, parseFloat(c.paddingBottom)||0, parseFloat(c.paddingLeft)||0, document.getElementById('device').getBoundingClientRect().width/390]; p.remove(); const l=document.getElementById('promiVeille'); return r.concat([l?getComputedStyle(l).backgroundColor:null, window._fondToileVif?_fondToileVif():null]); }")
        Bn = v['bornes'] or {}; lg = v['logo'] or [0, 0, 0, 0]; k = reel[6]
        bords = Bn and abs(Bn['x0'] - reel[5]) < 0.5 and abs(Bn['y0'] - reel[2]) < 0.5 and abs(Bn['x1'] + lg[2] - (reel[0] - reel[3])) < 0.5 and abs(Bn['y1'] + lg[3] - (reel[1] - reel[4])) < 0.5
        encre = abs(lg[2] - 140 * k) < 0.6 and 24 * k < lg[3] < 30 * k
        xs = [q[0] for q in pos]; touche = bool(xs) and (min(xs) - Bn.get('x0', 0) < 1.5 or Bn.get('x1', 0) - max(xs) < 1.5)
        juge('[%s] E · les bords sont ceux de la zone visible (%.0f × %.0f px, zones sûres %s), l\'encre (%.1f × %.1f px = 140 pt à l\'échelle %.3f) les touche, jamais dehors' % (E, reel[0], reel[1], reel[2:6], lg[2], lg[3], k),
             pos and not hors and bords and encre and touche, 'bornes %s · hors %s · bord touché %s' % ({q: round(Bn[q], 1) for q in ('x0', 'x1', 'y0', 'y1')} if Bn else None, hors[:3], touche))
        def ctr(a, bb):
            def L(h): return sum(c * w for c, w in zip([((int(h[i:i+2], 16) / 255) / 12.92 if int(h[i:i+2], 16) / 255 <= 0.03928 else ((int(h[i:i+2], 16) / 255 + 0.055) / 1.055) ** 2.4) for i in (1, 3, 5)], [0.2126, 0.7152, 0.0722]))
            x, y = L(a), L(bb); return (max(x, y) + 0.05) / (min(x, y) + 0.05)
        FOND = reel[8]; fond_ok = v.get('fond') == FOND and reel[7] == 'rgb(%d, %d, %d)' % tuple(int(FOND[i:i+2], 16) for i in (1, 3, 5))
        mauvais = [c for c in v['couleurs'] if ctr(c, FOND) < 3]
        juge('[%s] K · le fond est celui de la Toile du thème (%s), chaque couleur du logo tient 3:1 sur lui' % (E, FOND), fond_ok and not mauvais, 'fond de la veille %s · couleurs %s · sous 3:1 %s' % (reel[7], v['couleurs'], mauvais))
        C = v['couleurs']; TT = [t.lower() for t in (v['tons'] or [])]; meme = [i for i in range(1, len(C)) if C[i] == C[i - 1]]
        juge('[%s] C · à chaque rebond une autre couleur (palette du Studio), jamais deux fois la même d\'affilée' % E, v['rebonds'] >= 3 and not meme and all(c.lower() in TT for c in C),
             '%d rebonds · %s · tons %s' % (v['rebonds'], C, TT))
        if vw == 430 and not sombre:
            w1 = pg.evaluate("()=>window.__wl.slice()"); etat = v.get('verrou')
            B.tap(pg, 195, 500); pg.wait_for_timeout(800); w2 = pg.evaluate("()=>window.__wl.slice()"); e2 = (pg.evaluate(V) or {}).get('verrou')
            juge('F · le verrou : demandé au premier toucher, relâché à 10 min de veille (4 s ici), redemandé au retour', 'demandé' in w0 and 'relâché' in w1 and etat == 'relâché' and w2.count('demandé') >= 2 and e2 == 'actif',
                 'au toucher %s · pendant %s (%s) · au retour %s (%s)' % (w0, w1, etat, w2, e2))
        ctx.close()
    # ── D · le coin ──
    if not VITE:
        ctx, pg = ouvre(b, q='?veille=3&coin=1', attente=800); pg.wait_for_timeout(98000); v = pg.evaluate(V) or {}
        C = v.get('couleurs') or []; AM = (v.get('amande') or '#8FE08F').upper(); am = [i for i, c in enumerate(C) if c.upper() == AM]; coins = v.get('coins') or []
        juge('D · le coin forcé (?coin=1) tombe entre 60 et 90 s de veille, le logo y prend l\'amande, et seulement là', len(coins) >= 1 and 60000 <= coins[0] <= 90000 and len(am) == len(coins) and all(c >= 60000 for c in coins),
             'coins %s ms · amande (%s) aux rebonds %s · couleurs %s' % (coins, AM, am, C[-6:]))
        ctx.close()
    # ── G · réduire les animations ──
    ctx, pg = ouvre(b, reduit=True, attente=800); pg.wait_for_timeout(6500); a = pg.evaluate(V) or {}; pg.wait_for_timeout(4000); z = pg.evaluate(V) or {}
    ok = a.get('active') and a.get('logo') and z.get('logo') and abs(a['logo'][0] - z['logo'][0]) < 0.01 and z.get('rebonds') == 0 and abs(z['logo'][0] + z['logo'][2] / 2 - (z['bornes']['x0'] + z['bornes']['x1'] + z['logo'][2]) / 2) < 1
    juge('G · « Réduire les animations » : le logo fixe au centre, aucun rebond', ok, 'logo %s → %s · rebonds %s' % (a.get('logo'), z.get('logo'), z.get('rebonds')))
    ctx.close()
    # ── H · deux heures de trajectoire, sur les bords réels de chaque fenêtre ──
    for vw, vh in ((430, 932), (330, 714), (390, 651)):
        ctx, pg = ouvre(b, q='?veille=600', attente=3000, vw=vw, vh=vh)
        S = pg.evaluate("()=>{ if(!window._veilleSimule) return null; let co=0, rb=0, prem=1e9; for(let g=1; g<=30; g++){ const s=_veilleSimule(7200, g*7919); co+=s.coins.length; rb+=s.rebonds; if(s.coins.length) prem=Math.min(prem, s.coins[0]); } return [co, rb, prem]; }")
        ok = bool(S) and S[1] > 0 and 0.3 <= 100 * S[0] / S[1] <= 0.5 and S[2] >= 60
        juge('H · %dx%d : 30 × 2 h sur les bords réels — 0,3 à 0,5 %% des rebonds dans un coin, aucun avant la première minute' % (vw, vh), ok,
             ('%d coins / %d rebonds = %.2f %% · un toutes les %.1f min · premier à %.0f s' % (S[0], S[1], 100 * S[0] / S[1], 30 * 120 / max(1, S[0]), S[2])) if S else 'pas de simulation')
        ctx.close()
    # ── I · sans ?veille, sur le banc : rien ──
    ctx, pg = ouvre(b, q='', attente=800); pg.wait_for_timeout(66000); v = pg.evaluate(V)
    juge('I · sans ?veille=, sur le banc, elle ne paraît pas (66 s sans toucher)', v is not None and not v.get('active'), v and v.get('active'))
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page', not er, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
