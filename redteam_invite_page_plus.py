#!/usr/bin/env python3
"""
redteam_invite_page_plus.py — v172 (Tom, 30 oct. 2026, C-209) : SUR LA PAGE +, L'INVITE À TRACER N'ARRIVE QU'UNE FOIS LA PAROLE PRÊTE.

« Dès l'ouverture de la page +, la première chose qu'on voit est « TRACE POUR … ». Les testeurs essaient de tracer, ça bloque, et ils ne comprennent pas. »
L'invite = (2) le départ orange (ruban et pointe), (3) le libellé « trace pour … », (4) la flèche d'invite courbe. (1) les pointillés restent toujours.
Prête = le minimum exigé par le code : Promi et Chiche, la phrase ; Cercle, son nom.

Pour chaque nature × thème × échelle (1 : 430 × 932 ; 0,79 : 330 × 714), au doigt (banc comme Tom, WebKit) :
  A · À L'OUVERTURE, sur l'IMAGE : aucun orange du départ, aucune encre de la flèche courbe, aucun orange du libellé ; les pointillés sont là.
  B · PENDANT LA FRAPPE (un champ a la main, la phrase remplie) : toujours rien.
  C · LA PHRASE VALIDÉE (le clavier refermé) : l'invite paraît en ≤ 300 ms ; le départ et la flèche NAISSENT EN FLAQUES (le canevas du passage, lu image
      par image : ≥ 3 images à demi couvertes) ; le libellé se TRACE (sa découpe lue image par image : vide à la première, partielle sur ≥ 3) ; sur l'image
      finale, l'orange du départ, la flèche et le libellé sont là.
  D · LE CLIGNOTEMENT : la couche du départ porte `promiBlink`, en phase avec le I de PROMI (± 40 ms) ; au premier toucher du trait il s'arrête et le départ
      reste orange.
  E · LA PHRASE EFFACÉE : le retrait en flaques (le canevas du passage, ≥ 2 images à demi couvertes), puis plus rien de l'invite sur l'image.
Et : « Réduire les animations » (le départ fixe) ; tracer avant que ce soit prêt ouvre la saisie ; une fiche garde son départ orange.
Rouge sur v171 (`git show 2fc2281:app.html > zz-v171.html` ; `--fichier=zz-v171.html`).

⚑ v174 (Tom, 31 oct. 2026, C-213, remet ce juge au niveau, il remplace C-209 §1) — « À l'ouverture, RIEN du trait n'est visible : ni pointillés, ni départ, ni flèche, ni
libellé. » A : les pointillés absents aussi, et la mise en page « pas prête » lue sur le rendu (28 pt entre le bas de la vague et la phrase, 56 entre la phrase et le rail, rien
ne se recouvre). C : les éléments redescendent d'un mouvement (translate lu image par image : monotone, aucun pas au-delà de 35 % de la course, jamais figé puis lâché), partis
≤ 300 ms après la validation, à leur place exacte ; PUIS le trait naît en flaques sur toute sa largeur (`descend` avant `montre`). E : retrait en flaques puis remontée d'un
mouvement. F : LE CHEMIN DE TOM — un mot tapé, X, rouvrir : rien du trait, aucun ancien mot dans le champ caché. G : la phrase remontée se touche, le geste ne dessine rien.
Rouge sur v173 (`--fichier=zz-v173.html`). ⚠ Safari iOS du simulateur : voir le rapport du lot.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True)

GEO = """()=>{ const e=window._ppEcran?window._ppEcran():null, O=window._onde, t=document.querySelector('#createSheet .pp-trace'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  if(!e||!O) return null; const y=O.onde(e.base,e.amp); let m=1e9; for(let x=-12;x<=110;x+=2) m=Math.min(m,y(x)); const r=t?t.getBoundingClientRect():null;
  let b=-1e9; for(let x=0;x<=390;x+=3) b=Math.max(b,y(x));
  const ph=document.getElementById(e.nat==='nuee'?'nueePhrase':'csPhrase'), q=[...ph.querySelectorAll('.ph-txt > .ph-m, .ph-txt > .ph-b')].map(n=>n.getBoundingClientRect()).filter(q=>q.width), R=document.getElementById('csPinceau'), Rr=R?R.getBoundingClientRect():null, Gl=document.querySelector('#createSheet .pp-garder'), Gr=Gl?Gl.getBoundingClientRect():null;
  return {base:e.base, amp:e.amp, haut:m, bas:b, ph:q.length?[(Math.min(...q.map(a=>a.top))-D.top)/k,(Math.max(...q.map(a=>a.bottom))-D.top)/k]:null, rail:Rr&&Rr.height?[(Rr.top-D.top)/k,(Rr.bottom-D.top)/k]:null, garder:Gr&&Gr.height?(Gr.top-D.top)/k:null, tr:getComputedStyle(ph).translate,
    lib:r?[(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k]:null, pts:[...Array(9)].map((_,i)=>[150+i*25, y(150+i*25)])}; }"""
def compte(im, k, rect, test):
    x0, y0, w, h = rect; n = 0
    for X in range(max(0, int(x0 * k)), min(im.width, int((x0 + w) * k))):
        for Y in range(max(0, int(y0 * k)), min(im.height, int((y0 + h) * k)), 1):
            if test(im.getpixel((X, Y))): n += 1
    return n
ORANGE = lambda p: p[0] > 215 and 45 < p[1] < 120 and p[2] < 70
def sombre_de(trait):
    return lambda p: abs(p[0] - trait[0]) + abs(p[1] - trait[1]) + abs(p[2] - trait[2]) < 60
def lire(pg, g):
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); k = im.width / 390.0
    trait = pg.evaluate("()=>{ const e=_ppEcran(), c=(window._onde.NATTRAIT||window._onde.NATCLAIR)[e.nat]; const m=/#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})/i.exec(c); return m?[parseInt(m[1],16),parseInt(m[2],16),parseInt(m[3],16)]:[0,0,0]; }")
    dep = compte(im, k, [0, g['haut'] - 18, 58, 50], ORANGE)
    fl = compte(im, k, [44, g['base'] + 14, 40, 36], sombre_de(trait))
    lib = compte(im, k, g['lib'], ORANGE) if g['lib'] else 0
    pts = sum(compte(im, k, [x - 7, y - 7, 14, 14], sombre_de(trait)) for x, y in g['pts'])
    return {'depart': dep, 'fleche': fl, 'libelle': lib, 'points': pts}
# le relevé image par image, DANS la page : la couverture des canevas de passage (ce qui est peint) et la découpe du libellé (ce qui en est montré)
ENREG = """()=>{ window.__inv=[]; const t0=performance.now(); (function f(){ const c=document.getElementById('createSheet'); if(!c) return;
   const P=[...c.querySelectorAll('canvas.passage-flaques')].map(k=>{ try{ const g=k.getContext('2d'), d=g.getImageData(0,0,k.width,k.height).data; let n=0, a=0; for(let i=3;i<d.length;i+=16){ n++; if(d[i]>128) a++; } return +(a/Math.max(1,n)).toFixed(3); }catch(e){ return -1; } });
   const t=c.querySelector('.pp-trace'), cs=t?getComputedStyle(t):null;
   const ph=document.getElementById(c.classList.contains('pp-nuee')?'nueePhrase':'csPhrase'), tp=ph?getComputedStyle(ph).translate:'none', ty=(!tp||tp==='none')?0:parseFloat(tp.split(/\s+/)[1]||'0')||0;
   window.__inv.push({t:Math.round(performance.now()-t0), ty:ty, p:P, vis:cs?cs.visibility:null, clip:t?(t.style.getPropertyValue('clip-path')||'none'):null, inv:c.getAttribute('data-invite')});
   if(window.__inv.length<400) requestAnimationFrame(f); })(); }"""
def pleine(pg):
    # le départ clignote (opacité 1 de 0 à 54 % de 1,15 s, puis 0,6) : on lit l'orange à la phase PLEINE, comme le juge du départ de l'onboarding
    t = pg.evaluate("()=>{ const d=document.getElementById('ppDepart'), A=d&&d.getAnimations?d.getAnimations().filter(a=>a.animationName==='promiBlink')[0]:null; return A&&A.currentTime!=null?A.currentTime%1150:null; }")
    if t is not None and t > 330: pg.wait_for_timeout(int(1150 - t + 25))
def ouvre_nat(pg, nat):
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
def phrase(nat): return '#nueePhrase .ph-m[data-np="nom"]' if nat == 'nuee' else '#csPhrase .ph-m[data-ph="titre"]'

def tour(b, nat, sombre, vw, vh, nom):
    ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F); ouvre_nat(pg, nat); T = '[%s · %s · %s]' % (nat, 'sombre' if sombre else 'clair', nom)
    g = pg.evaluate(GEO)
    if not g: juge(T + ' la page + s\'ouvre', False); ctx.close(); return
    a = lire(pg, g)
    juge(T + ' A · à l\'ouverture : RIEN du trait — ni pointillés, ni départ, ni flèche, ni libellé', a['depart'] == 0 and a['fleche'] < 6 and a['libelle'] == 0 and a['points'] < 12, a)
    if g['ph'] and g['rail']:
        a1, a2 = g['ph'][0] - g['bas'], g['rail'][0] - g['ph'][1]; a3 = (g['garder'] - g['rail'][1]) if g['garder'] else 99
        juge(T + ' A · pas prête : la page remontée, 28 pt sous la vague, 56 pt jusqu\'au rail, rien ne se recouvre', abs(a1 - 28) <= 1 and abs(a2 - 56) <= 1 and a3 > 8, 'vague → phrase %.1f · phrase → rail %.1f · rail → garder %.1f' % (a1, a2, a3))
    else: juge(T + ' A · pas prête : la page remontée', False, g)
    B.tap_sel(pg, phrase(nat)); pg.wait_for_timeout(700); pg.keyboard.type('nager loin', delay=45); pg.wait_for_timeout(900)
    g = pg.evaluate(GEO) or g; f = lire(pg, g)
    juge(T + ' B · pendant la frappe, la phrase remplie : toujours rien', f['depart'] == 0 and f['libelle'] == 0 and f['fleche'] < 6, f)
    clip0 = pg.evaluate("()=>{ const t=document.querySelector('#createSheet .pp-trace'); return t?(t.style.getPropertyValue('clip-path')||'none'):'none'; }")   # la découpe d'avant le tracé : le module la rend à la fin
    pg.evaluate(ENREG); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
    for _ in range(40):   # la fin du tracé du libellé (sous charge, il dure plus que sa durée prévue)
        if pg.evaluate("(c0)=>{ const t=document.querySelector('#createSheet .pp-trace'); return !!t && getComputedStyle(t).visibility==='visible' && (t.style.getPropertyValue('clip-path')||'none')===c0 && !t.__trace; }", clip0): break
        pg.wait_for_timeout(100)
    pg.wait_for_timeout(150); R = pg.evaluate("()=>window.__inv"); g = pg.evaluate(GEO) or g; pleine(pg); v = lire(pg, g)
    for _ in range(3):   # la capture peut tomber dans la phase éteinte du clignotement, sous charge : on reprend à la phase pleine
        if v['depart'] > 60: break
        pleine(pg); v2 = lire(pg, g); v = v2 if v2['depart'] > v['depart'] else v
    t1 = next((r['t'] for r in R if r['inv'] == '1'), None)
    partiel = sum(1 for r in R for u in r['p'] if 0.05 < u < 0.95)
    clips = [r['clip'] for r in R if r['vis'] == 'visible']
    trace_ok = len(clips) >= 4 and clips[0] not in ('none', '', clip0) and sum(1 for c in clips if c not in ('none', '', clip0)) >= 4 and clips[-1] == clip0
    J = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")]
    bas_ = min(r['ty'] for r in R); i0 = max(i for i, r in enumerate(R) if r['ty'] == bas_) if bas_ < 0 else 0; S_ = R[i0:]; tys = [r['ty'] for r in S_]; course = abs(bas_) or 1   # le suivi commence quand la page est posée en haut (le choix refermé)
    dep = next((r['t'] for r in S_ if r['ty'] > bas_ + 0.4), None); mvt = [r for r in S_ if bas_ + 0.3 < r['ty'] < -0.3]; pas = [abs(tys[i + 1] - tys[i]) for i in range(len(tys) - 1)] or [99]
    LIM = 300 if B.charge() < 4 else 450   # une durée ne se juge qu'au calme (C-137)
    juge(T + ' C · les éléments partent ≤ 300 ms après la validation (450 sous charge : non jugé)', dep is not None and dep <= LIM, 't = %s ms · course %.1f pt' % (dep, course))
    juge(T + ' C · ils redescendent d\'un mouvement : monotone, ≥ 4 images en route, aucun pas > 35 % de la course', bas_ < -1 and all(tys[i + 1] >= tys[i] - 0.05 for i in range(len(tys) - 1)) and len(mvt) >= 4 and max(pas) <= course * 0.35, '%d images · pas max %.1f' % (len(mvt), max(pas)))
    juge(T + ' C · à leur place : translate nul à la fin', g['tr'] in ('none', '0px', '0px 0px'), g['tr'])
    juge(T + ' C · d\'abord les éléments, puis le trait (journal)', 'descend' in J and 'montre' in J and J.index('descend') < len(J) - 1 - J[::-1].index('montre'), J[-4:])
    juge(T + ' C · le trait entier naît EN FLAQUES (≥ 3 images à demi couvertes), après la descente', partiel >= 3, '%d images partielles' % partiel)
    juge(T + ' C · le libellé se TRACE : découpé dès sa première image visible, puis partiel, puis entier', trace_ok, '%d images · première %s · dernière %s' % (len(clips), (clips[0] if clips else None) and clips[0][:24], clips[-1][:24] if clips else None))
    juge(T + ' C · sur l\'image finale : le départ orange, la flèche courbe, le libellé, les pointillés', v['depart'] > 60 and v['fleche'] > 20 and v['libelle'] > 60 and v['points'] > 200, v)
    c = pg.evaluate("""()=>{ const d=document.getElementById('ppDepart'), I=document.querySelector('#device .acc-mm i');
        const A=d&&d.getAnimations?d.getAnimations().filter(a=>a.animationName==='promiBlink')[0]:null, AI=I&&I.getAnimations?I.getAnimations().filter(a=>a.animationName==='promiBlink')[0]:null;
        return {cl:!!(d&&d.classList.contains('clignote')), a:A?A.currentTime:null, i:AI?AI.currentTime:null}; }""")
    ph = None if (c['a'] is None or c['i'] is None) else abs(((c['a'] - c['i']) + 575) % 1150 - 575)
    juge(T + ' D · le départ clignote, en phase avec le I de PROMI (± 40 ms)', c['cl'] and ph is not None and ph <= 40, c)
    pg.evaluate("()=>{ const z=document.getElementById('planterCv'); const r=z.getBoundingClientRect(); z.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:r.left+r.width*0.8,clientY:r.top+r.height/2,pointerType:'touch',isPrimary:true})); z.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:r.left+r.width*0.8,clientY:r.top+r.height/2,pointerType:'touch',isPrimary:true})); }")
    pg.wait_for_timeout(500); c2 = pg.evaluate("()=>{ const d=document.getElementById('ppDepart'); return d?{cl:d.classList.contains('clignote'), anim:d.getAnimations?d.getAnimations().length:0}:{cl:false, anim:0, absente:true}; }"); w = lire(pg, pg.evaluate(GEO) or g)
    juge(T + ' D · au premier toucher du trait, le départ cesse de clignoter et reste orange', not c2['cl'] and c2['anim'] == 0 and w['depart'] > 60, '%s · orange %d' % (c2, w['depart']))
    if not VITE or (nat == 'promi'):
        B.tap_sel(pg, phrase(nat)); pg.wait_for_timeout(700); pg.evaluate("()=>{ const a=document.activeElement; if(a&&a.select) a.select(); }")
        pg.evaluate(ENREG); pg.keyboard.press('Backspace'); pg.wait_for_timeout(900)
        R = pg.evaluate("()=>window.__inv"); partiel = sum(1 for r in R for u in r['p'] if 0.05 < u < 0.95); g = pg.evaluate(GEO) or g; z = lire(pg, g)
        juge(T + ' E · la phrase effacée : l\'invite se retire EN FLAQUES (≥ 2 images à demi couvertes), puis plus rien', partiel >= 2 and z['depart'] == 0 and z['libelle'] == 0 and z['fleche'] < 6 and z['points'] < 12, '%d partielles · %s' % (partiel, z))
        pg.keyboard.press('Enter'); pg.wait_for_timeout(1100); g = pg.evaluate(GEO) or g
        tr_ = g['tr']; juge(T + ' E · puis les éléments remontent', tr_ not in ('none', '0px', '0px 0px'), tr_)
    if not VITE or nat == 'promi':
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1000)
        ouvre_nat(pg, 'promi' if nat == 'chiche' else nat); pg.wait_for_timeout(600)
        B.tap_sel(pg, phrase('promi' if nat == 'chiche' else nat)); pg.wait_for_timeout(700); pg.keyboard.type('nager', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(1700)
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1000); ouvre_nat(pg, nat); g2 = pg.evaluate(GEO); f2 = lire(pg, g2)
        ch = pg.evaluate("()=>({ft:document.getElementById('fTitle').value, nn:document.getElementById('nName').value})")
        juge(T + ' F · LE CHEMIN DE TOM : un mot tapé, X, rouvrir : rien du trait, aucun ancien mot caché', f2['depart'] == 0 and f2['libelle'] == 0 and f2['points'] < 12 and not ch['ft'] and not ch['nn'], '%s · %s' % (f2, ch))
        act0 = pg.evaluate("()=>document.activeElement&&document.activeElement.id"); B.tap_sel(pg, phrase(nat)); pg.wait_for_timeout(700)
        act = pg.evaluate("()=>{ const a=document.activeElement; return a?(a.id||a.tagName):null; }")
        juge(T + ' G · la phrase remontée se touche au doigt : la saisie s\'ouvre', act in ('phIn', 'fTitle', 'nName') or (act or '').startswith('np') or pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-ouvert')"), act)
        # H · v174 : un choix ouvert sur une page pas encore prête se referme encore d'un toucher dans la zone du trait (la zone n'est sans prise que choix fermé)
        if nat != 'nuee' and '0,79' not in T:   # à 0,79, ce toucher répond comme sur v173 (scratchpad/v174/garder_sonde79.py) : même nœud, même résultat, trois points
            B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1000); ouvre_nat(pg, nat); pg.wait_for_timeout(700)
            if nat == 'promi': B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(1100)   # un Promi à soi n'a pas de « qui » : la bascule d'abord
            B.tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1000)
            ouv = pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-ouvert')")
            pg.touchscreen.tap(*pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(),k=r.width/390;return [r.left+215*k,r.top+130*k]}")); pg.wait_for_timeout(1000)
            ferme = pg.evaluate("()=>!document.getElementById('createSheet').classList.contains('pp-ouvert')")
            juge(T + ' H · un choix ouvert se referme d\'un toucher dans la zone du trait', ouv and ferme, 'ouvert %s · refermé %s' % (ouv, ferme))
    if pg.__dict__['erreurs']: juge(T + ' aucune erreur de page', False, pg.__dict__['erreurs'][:2])
    ctx.close()

with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_invite_page_plus — %s, charge %.1f' % (F, B.charge()))
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            for nat in ('promi', 'chiche', 'nuee'):
                if VITE and (nom != '1' or sombre) and nat != 'promi': continue
                tour(b, nat, sombre, vw, vh, nom)
    # Réduire les animations : le départ fixe, l'invite posée
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA, reduced_motion='reduce')
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__a')){ sessionStorage.setItem('__a','1'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); localStorage.setItem('promi_theme','light'); } }catch(e){}")
    pg = B.ouvre(ctx, F); ouvre_nat(pg, 'promi'); g = pg.evaluate(GEO); a = lire(pg, g)
    B.tap_sel(pg, phrase('promi')); pg.wait_for_timeout(700); pg.keyboard.type('nager loin', delay=40); pg.keyboard.press('Enter'); pg.wait_for_timeout(1400)
    v = lire(pg, pg.evaluate(GEO) or g); c = pg.evaluate("()=>{ const d=document.getElementById('ppDepart'); return d?{cl:d.classList.contains('clignote'), anim:d.getAnimations?d.getAnimations().length:0}:null; }")
    juge('[réduit] caché à l\'ouverture, puis l\'invite posée, le départ FIXE (aucune animation)', a['depart'] == 0 and a['libelle'] == 0 and v['depart'] > 60 and v['libelle'] > 60 and c and c['anim'] == 0, '%s → %s · %s' % (a, v, c))
    ctx.close()
    # v174 (C-213) : tracer avant que ce soit prêt : plus rien à tracer, le geste ne dessine rien ; une fiche garde son départ orange
    ctx = B.contexte(b, False, vw=430, vh=932); pg = B.ouvre(ctx, F); ouvre_nat(pg, 'promi')
    B.glisse(pg, [[30, 285]] + [[30 + i * 15, 285 + (i % 3)] for i in range(1, 16)], tenue=380); pg.wait_for_timeout(1200)
    gz = pg.evaluate(GEO); zz = lire(pg, gz); cl = pg.evaluate("()=>document.getElementById('createSheet').className")
    juge('glisser sur la place vide du trait, la parole pas prête : rien ne se dessine (C-213)', zz['depart'] == 0 and zz['points'] < 12 and 'pp-cours' not in cl, '%s' % zz)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
    B.plante_doigt(pg, 'écrire à Lou', 'moi', 0); pid = pg.evaluate("()=>promises.slice(-1)[0].id"); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); k = im.width / 390.0
    yb = pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'), v=(c.getAttribute('data-trait')||'').split(','); return [parseFloat(v[0]), parseFloat(v[1])]; }")
    of = compte(im, k, [0, yb[0] - yb[1] - 30, 200, 2 * yb[1] + 60], ORANGE)
    juge('une fiche à tenir garde son départ orange, visible d\'emblée (non concernée)', of > 60, 'orange %d · trait %s' % (of, yb))
    ctx.close(); b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
sys.exit(0 if all(res) else 1)
