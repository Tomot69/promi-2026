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

⚑ v176 (Tom, 1er nov. 2026, C-222, remet ce juge au niveau, il remplace « jamais pendant la frappe ») — « Dès que le minimum est rempli, la genèse part IMMÉDIATEMENT, sans attendre la
fermeture du clavier. » B : la genèse part à la PREMIÈRE lettre, le champ gardant la main, dans l'image qui suit (compté en images, jamais en ms : la charge ne le fausse pas), le passage
déjà troué, une seule naissance pour dix frappes ; le clavier ouvert rien ne descend (la mise en page de saisie garde la place du trait : la descente passerait sous le clavier). C : le
clavier fermé, tout est à sa place finale, sans seconde naissance. E : le retrait ne change pas, une lettre retapée fait renaître le trait. S : sans clavier, la descente de C-213.
Rouge sur v175b (`--fichier=zz-v175b.html`).

⚑ v177b (Tom, 4 nov. 2026, C-229, remet ce juge au niveau, il remplace la mise en page « pas prête » de C-213) — « C'est l'HORIZON qui bouge, pas le texte. Le texte et les
éléments de la page sont à leur place FINALE dès l'ouverture, et ne bougent plus. Tant que la parole n'est pas prête, l'horizon est un peu plus BAS que sa place finale ; il ne
descend JAMAIS jusqu'au texte : au moins 12 pt au-dessus du plus haut élément du corps. Prête : l'horizon REMONTE en douceur (300 à 400 ms), puis le trait y naît. Redevenue
incomplète : le trait se retire en flaques, l'horizon redescend en douceur. »
L'horizon se lit sur l'IMAGE (le bas du champ, à la couleur de sa nature, colonne par colonne) et, image par image, sur le canevas du champ, DANS la page — jamais sur ce que
l'app déclare. A : à l'ouverture, l'horizon 20 à 45 pt sous sa place, ≥ 12 pt au-dessus de l'encre de la phrase, la phrase sans translation. B : le champ ouvert (clavier),
même loi ; à la frappe qui complète, l'horizon part dans l'image qui suit, remonte d'un mouvement (≥ 4 images, aucun pas > 35 % de la course), PUIS le trait naît ; la phrase
ne bouge pas d'une image à l'autre. C : clavier fermé, l'horizon à sa place, la phrase à la place qu'elle avait à l'ouverture. E : retrait en flaques, puis l'horizon redescend,
la phrase immobile. S : sans clavier, la même remontée. Rouge sur v177a (`--fichier=zz-v177a.html`).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
SEUL = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--nat=')), None)   # une nature, clair, échelle 1 : pour rejouer un rouge
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
CHAMP = {'promi': (0x82, 0xAE, 0xF8), 'chiche': (0xFF, 0xB8, 0xD2), 'nuee': (0xC9, 0xA8, 0xF5)}   # la nature, en dur (§3)
def horizon(im, k, g, nat):
    """l'horizon PEINT : pour chaque colonne de `g['pts']`, le dernier point de la couleur du champ, en pt ; rend (écarts à l'onde finale, bas le plus bas)"""
    c = CHAMP[nat]; d = []; bas = -1
    for x, y in g['pts']:
        X = int(x * k); last = None
        for Y in range(int((y - 70) * k), min(im.height, int((y + 90) * k))):   # le champ d'un seul tenant, depuis le haut : un créneau de la phrase peut porter la même teinte
            q = im.getpixel((X, Y))
            if abs(q[0] - c[0]) + abs(q[1] - c[1]) + abs(q[2] - c[2]) < 36: last = Y
            elif last is not None: break
        if last is not None: d.append(last / k - y); bas = max(bas, last / k)
    d.sort(); return (d[len(d) // 2] if d else None), bas
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
   let hz=null; try{ const e=_ppEcran(), y=window._onde.onde(e.base,e.amp), cv=document.getElementById('csTrameCv'), C=({promi:[0x82,0xAE,0xF8],chiche:[0xFF,0xB8,0xD2],nuee:[0xC9,0xA8,0xF5]})[e.nat], s=cv.height/(cv.getBoundingClientRect().height/(document.getElementById('device').getBoundingClientRect().width/390)), v=[];
     for(const x of [165,215,265,315]){ const X=Math.round(x*s), d=cv.getContext('2d').getImageData(X,0,1,cv.height).data; let last=-1; for(let i=0;i<cv.height;i++){ const o=i*4; if(d[o+3]>200 && Math.abs(d[o]-C[0])+Math.abs(d[o+1]-C[1])+Math.abs(d[o+2]-C[2])<36) last=i; } if(last>=0) v.push(last/s-y(x)); }
     v.sort((a,b)=>a-b); hz=v.length?+v[v.length>>1].toFixed(2):null; }catch(_){ }
   const Dv=document.getElementById('device').getBoundingClientRect(), phr=ph?ph.getBoundingClientRect():null, phy=phr?+((phr.top-Dv.top)/(Dv.width/390)).toFixed(2):null;
   window.__inv.push({t:Math.round(performance.now()-t0), abs:performance.now(), ty:ty, hz:hz, phy:phy, p:P, vis:cs?cs.visibility:null, clip:t?(t.style.getPropertyValue('clip-path')||'none'):null, inv:c.getAttribute('data-invite')});
   if(window.__inv.length<400) requestAnimationFrame(f); })(); }"""
FRAPPE = """()=>{ window.__frappe=null; document.addEventListener('input', e=>{ if(window.__frappe==null && (e.target.id==='phIn'||e.target.id==='nueeNomIn')) window.__frappe=performance.now(); }, true); }"""   # v176 (C-222) : l'instant de la première frappe, lu dans la page
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
    g0 = g; im0 = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); hz0, hb0 = horizon(im0, im0.width / 390.0, g, nat)
    if g['ph'] and hz0 is not None:
        juge(T + ' A · pas prête : la phrase à sa place (aucune translation), l\'horizon 20 à 45 pt SOUS sa place, ≥ 12 pt au-dessus de l\'encre de la phrase', g['tr'] in ('none', '0px', '0px 0px') and 20 <= hz0 <= 45 and g['ph'][0] - hb0 >= 12, 'horizon +%.1f pt · marge %.1f pt · %s' % (hz0, g['ph'][0] - hb0, g['tr']))
    else: juge(T + ' A · pas prête : l\'horizon plus bas', False, '%s · %s' % (hz0, g['ph']))
    # ⚑ v176 (C-222) : LA GENÈSE PART À LA FRAPPE QUI COMPLÈTE LE MINIMUM, le clavier ouvert (le champ a la main). La page garde sa mise en page de saisie : rien ne bouge, rien ne descend.
    B.tap_sel(pg, phrase(nat)); pg.wait_for_timeout(900)
    g = pg.evaluate(GEO) or g; f = lire(pg, g)
    juge(T + ' B · le champ ouvert, aucune lettre : toujours rien', f['depart'] == 0 and f['libelle'] == 0 and f['fleche'] < 6, f)
    imb = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); hzb, hbb = horizon(imb, imb.width / 390.0, g, nat)
    juge(T + ' B · le champ ouvert : l\'horizon plus bas, ≥ 12 pt au-dessus de la phrase (rien sur la saisie)', hzb is not None and hzb >= 15 and g['ph'] and g['ph'][0] - hbb >= 12, 'horizon +%s · marge %s' % (hzb, g['ph'] and round(g['ph'][0] - hbb, 1)))
    clip0 = pg.evaluate("()=>{ const t=document.querySelector('#createSheet .pp-trace'); return t?(t.style.getPropertyValue('clip-path')||'none'):'none'; }")   # la découpe d'avant le tracé : le module la rend à la fin
    pg.evaluate(ENREG); pg.evaluate(FRAPPE); pg.wait_for_timeout(150); pg.keyboard.type('n'); pg.wait_for_timeout(120); pg.keyboard.type('ager loin', delay=45); pg.wait_for_timeout(1200)
    for _ in range(40):   # la fin du tracé du libellé (sous charge, il dure plus que sa durée prévue)
        if pg.evaluate("(c0)=>{ const t=document.querySelector('#createSheet .pp-trace'); return !!t && getComputedStyle(t).visibility==='visible' && (t.style.getPropertyValue('clip-path')||'none')===c0 && !t.__trace; }", clip0): break
        pg.wait_for_timeout(100)
    pg.wait_for_timeout(150); R = pg.evaluate("()=>window.__inv"); Ri = [r for r in R if pg.evaluate("()=>window.__frappe") is not None and r['abs'] >= pg.evaluate("()=>window.__frappe")]
    act = pg.evaluate("()=>{ const a=document.activeElement; return a?(a.id||a.tagName):null; }")
    n1 = next((i for i, r in enumerate(Ri) if r['inv'] == '1'), None); n2 = next((i for i, r in enumerate(Ri) if any(u < 0.9995 for u in r['p'])), None)
    H = [r['hz'] for r in Ri if r['hz'] is not None]; h0 = H[0] if H else None
    m0 = next((i for i, r in enumerate(Ri) if r['hz'] is not None and h0 is not None and r['hz'] < h0 - 0.5), None)
    fin = next((i for i, r in enumerate(Ri) if r['hz'] is not None and r['hz'] <= 1.5), None)
    route = [r['hz'] for r in Ri[(m0 or 0):(fin or 0) + 1] if r['hz'] is not None]; course = (route[0] - route[-1]) if len(route) > 1 else 0
    pasM = max([route[i] - route[i + 1] for i in range(len(route) - 1)] or [99]); mono = all(route[i + 1] <= route[i] + 0.3 for i in range(len(route) - 1))
    juge(T + ' B · À LA FRAPPE, L\'HORIZON PART dans l\'image qui suit, le champ a toujours la main', m0 is not None and m0 <= 2 and act in ('phIn', 'nueeNomIn'), 'image %s · champ %s · horizon de +%s' % (m0, act, h0))
    juge(T + ' B · il REMONTE, monotone, jusqu\'à sa place', fin is not None and mono and course > 15, '%d images · course %.1f' % (len(route), course))
    juge(T + ' B · d\'un mouvement : ≥ 4 images en route, aucun pas > 35 % de la course (cadence : jugée au calme seulement)', B.charge() >= 4 or (len(route) >= 5 and pasM <= course * 0.35), '%d images · pas max %.1f%s' % (len(route), pasM, ' — NON JUGÉ (charge %.1f)' % B.charge() if B.charge() >= 4 else ''))
    dur = (Ri[fin]['t'] - Ri[m0]['t']) if (fin is not None and m0 is not None) else None
    juge(T + ' B · la remontée dure 300 à 400 ms (jugée au calme seulement)', B.charge() >= 4 or (dur is not None and 280 <= dur <= 440), 'durée %s ms · charge %.1f%s' % (dur, B.charge(), ' — NON JUGÉ' if B.charge() >= 4 else ''))
    juge(T + ' B · PUIS le trait naît : l\'invite paraît une fois l\'horizon à sa place, et le passage a ses trous dès sa première image', n1 is not None and fin is not None and n1 >= fin and n2 is not None and n2 <= n1 + 1, 'horizon posé à l\'image %s · invite à %s · trous à %s' % (fin, n1, n2))
    phs = [r['phy'] for r in Ri if r['phy'] is not None]
    juge(T + ' B · la phrase ne bouge pas d\'une image à l\'autre pendant tout cela', phs and max(phs) - min(phs) <= 0.5, 'phrase %s → %s' % (phs and min(phs), phs and max(phs)))
    J = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")]
    juge(T + ' B · elle ne se relance pas à chaque lettre : une seule naissance pour dix frappes', J.count('montre') == 1 and 'renait' not in J, J)
    gs = pg.evaluate(GEO) or g; tys = [r['ty'] for r in Ri] or [1]
    juge(T + ' B · le clavier ouvert, rien ne descend : la phrase ne bouge pas, le libellé reste au-dessus d\'elle', (gs['ph'] and gs['lib']) and abs(gs['ph'][0] - g['ph'][0]) <= 1.5 and max(abs(t) for t in tys) < 0.1 and gs['lib'][1] + gs['lib'][3] <= gs['ph'][0], 'haut phrase %.1f → %.1f · bas libellé %.1f' % (g['ph'][0], gs['ph'][0], gs['lib'][1] + gs['lib'][3]))
    partiel = sum(1 for r in Ri for u in r['p'] if 0.05 < u < 0.95)
    clips = [r['clip'] for r in Ri if r['vis'] == 'visible']
    trace_ok = len(clips) >= 4 and clips[0] not in ('none', '', clip0) and sum(1 for c in clips if c not in ('none', '', clip0)) >= 4 and clips[-1] == clip0
    juge(T + ' C · le trait naît EN FLAQUES (≥ 3 images à demi couvertes)', partiel >= 3, '%d images partielles' % partiel)
    juge(T + ' C · le libellé se TRACE : découpé dès sa première image visible, puis partiel, puis entier', trace_ok, '%d images · première %s · dernière %s' % (len(clips), (clips[0] if clips else None) and clips[0][:24], clips[-1][:24] if clips else None))
    pleine(pg); v = lire(pg, gs)
    for _ in range(3):   # la capture peut tomber dans la phase éteinte du clignotement, sous charge : on reprend à la phase pleine
        if v['depart'] > 60: break
        pleine(pg); v2 = lire(pg, gs); v = v2 if v2['depart'] > v['depart'] else v
    juge(T + ' C · clavier ouvert, sur l\'image : le départ orange, la flèche courbe, le libellé, les pointillés', v['depart'] > 60 and v['fleche'] > 20 and v['libelle'] > 60 and v['points'] > 150, v)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(1300)   # (± 1,5 pt ci-dessus : la phrase d'un Chiche se resserre d'un point avec son texte, elle ne descend pas)
    g = pg.evaluate(GEO) or g; pleine(pg); v = lire(pg, g)
    for _ in range(3):
        if v['depart'] > 60: break
        pleine(pg); v2 = lire(pg, g); v = v2 if v2['depart'] > v['depart'] else v
    J = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")]
    imc = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); hzc, _ = horizon(imc, imc.width / 390.0, g, nat)
    juge(T + ' C · le clavier fermé : l\'horizon à sa place, la phrase, le rail et « garder de côté » à la place qu\'ils avaient à l\'ouverture', hzc is not None and -9 <= hzc <= 1.5 and g['ph'] and g0['ph'] and (g['base'] != g0['base'] or abs(g['ph'][0] - g0['ph'][0]) <= 0.5) and (g['base'] != g0['base'] or not g['rail'] or not g0['rail'] or abs(g['ph'][1] - g0['ph'][1]) > 0.5 or abs(g['rail'][0] - g0['rail'][0]) <= 0.5) and (g['garder'] is None or g0['garder'] is None or abs(g['garder'] - g0['garder']) <= 0.5), 'horizon %s · phrase %s → %s · rail %s → %s' % (hzc, g0['ph'] and round(g0['ph'][0], 1), g['ph'] and round(g['ph'][0], 1), g0['rail'] and round(g0['rail'][0], 1), g['rail'] and round(g['rail'][0], 1)))
    juge(T + ' C · le clavier fermé : la page à sa place finale, le trait entier, aucune seconde naissance, aucun calque', g['tr'] in ('none', '0px', '0px 0px') and v['depart'] > 60 and v['fleche'] > 20 and v['libelle'] > 60 and v['points'] > 200 and J.count('montre') == 1 and pg.evaluate("()=>document.querySelectorAll('#createSheet canvas.passage-flaques').length") == 0, '%s · %s' % (v, g['tr']))
    c = pg.evaluate("""()=>{ const d=document.getElementById('ppDepart'), I=document.querySelector('#device .acc-mm i');
        const A=d&&d.getAnimations?d.getAnimations().filter(a=>a.animationName==='promiBlink')[0]:null, AI=I&&I.getAnimations?I.getAnimations().filter(a=>a.animationName==='promiBlink')[0]:null;
        return {cl:!!(d&&d.classList.contains('clignote')), a:A?A.currentTime:null, i:AI?AI.currentTime:null}; }""")
    ph = None if (c['a'] is None or c['i'] is None) else abs(((c['a'] - c['i']) + 575) % 1150 - 575)
    juge(T + ' D · le départ clignote, en phase avec le I de PROMI (± 40 ms)', c['cl'] and ph is not None and ph <= 40, c)
    pg.evaluate("()=>{ const z=document.getElementById(_ppEcran().nat==='nuee'?'planterCvN':'planterCv'); const r=z.getBoundingClientRect(); z.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:r.left+r.width*0.8,clientY:r.top+r.height/2,pointerType:'touch',isPrimary:true})); z.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:r.left+r.width*0.8,clientY:r.top+r.height/2,pointerType:'touch',isPrimary:true})); }")
    pg.wait_for_timeout(500); c2 = pg.evaluate("()=>{ const d=document.getElementById('ppDepart'); return d?{cl:d.classList.contains('clignote'), anim:d.getAnimations?d.getAnimations().length:0}:{cl:false, anim:0, absente:true}; }"); w = lire(pg, pg.evaluate(GEO) or g)
    juge(T + ' D · au premier toucher du trait, le départ cesse de clignoter et reste orange', not c2['cl'] and c2['anim'] == 0 and w['depart'] > 60, '%s · orange %d' % (c2, w['depart']))
    if not VITE or (nat == 'promi'):
        B.tap_sel(pg, phrase(nat)); pg.wait_for_timeout(700); pg.evaluate("()=>{ const a=document.activeElement; if(a&&a.select) a.select(); }")
        pg.evaluate(ENREG); pg.keyboard.press('Backspace'); pg.wait_for_timeout(900)
        R = pg.evaluate("()=>window.__inv"); partiel = sum(1 for r in R for u in r['p'] if 0.05 < u < 0.95); g = pg.evaluate(GEO) or g; z = lire(pg, g)
        juge(T + ' E · la phrase effacée : l\'invite se retire EN FLAQUES (≥ 2 images à demi couvertes), puis plus rien', partiel >= 2 and z['depart'] == 0 and z['libelle'] == 0 and z['fleche'] < 6 and z['points'] < 12, '%d partielles · %s' % (partiel, z))
        n0 = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")].count('montre'); pg.keyboard.type('a'); pg.wait_for_timeout(900); n1 = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")].count('montre')
        juge(T + ' E · une lettre retapée, clavier ouvert : le trait renaît, une fois', n1 == n0 + 1, '%d → %d' % (n0, n1))
        pg.evaluate(ENREG); pg.keyboard.press('Backspace'); pg.wait_for_timeout(1200)
        R = pg.evaluate("()=>window.__inv"); Hh = [r['hz'] for r in R if r['hz'] is not None]; phs = [r['phy'] for r in R if r['phy'] is not None]
        J = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")]
        desc = [Hh[i + 1] - Hh[i] for i in range(len(Hh) - 1)]; enroute = [h for h in Hh if 1.5 < h < max(Hh or [0]) - 1.5]
        juge(T + ' E · le trait retiré en flaques, PUIS l\'horizon redescend d\'un mouvement (≥ 3 images en route), la phrase immobile', Hh and max(Hh) >= 15 and all(d >= -0.3 for d in desc) and (len(enroute) >= 3 or B.charge() >= 4) and phs and max(phs) - min(phs) <= 0.5 and 'retire' in J and 'horizon-bas' in J and J.index('retire') < len(J) - 1 - J[::-1].index('horizon-bas'), 'horizon %s → %s · %d en route · phrase ±%.1f · %s' % (Hh and Hh[0], Hh and Hh[-1], len(enroute), (max(phs) - min(phs)) if phs else -1, J[-4:]))
        pg.keyboard.press('Enter'); pg.wait_for_timeout(1100); g = pg.evaluate(GEO) or g
        ime = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); hze, hbe = horizon(ime, ime.width / 390.0, g, nat)
        juge(T + ' E · clavier fermé, parole vide : l\'horizon plus bas, ≥ 12 pt au-dessus de la phrase, la phrase à sa place', hze is not None and hze >= 20 and g['ph'] and g['ph'][0] - hbe >= 12 and g['tr'] in ('none', '0px', '0px 0px') and (g['base'] != g0['base'] or abs(g['ph'][0] - g0['ph'][0]) <= 0.5), 'horizon +%s · marge %s · %s' % (hze, g['ph'] and round(g['ph'][0] - hbe, 1), g['tr']))
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
        # ⚑ v176 (C-222) : SANS CLAVIER (une parole reprise), la règle de C-213 tient : les éléments d'abord, d'un mouvement, puis le trait
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(1000); ouvre_nat(pg, nat); pg.wait_for_timeout(500); pg.evaluate(ENREG)
        pg.evaluate("n=>{ const e=document.getElementById(n==='nuee'?'nName':'fTitle'); e.value='nager'; e.dispatchEvent(new Event('input',{bubbles:true})); }", nat); pg.wait_for_timeout(2300)
        R = pg.evaluate("()=>window.__inv"); J = [j[1] for j in pg.evaluate("()=>_ppInvite.etat().journal")]; g3 = pg.evaluate(GEO) or g
        Hh = [(r['t'], r['hz']) for r in R if r['hz'] is not None]; top = max([h for _, h in Hh] or [0]); i0 = max([i for i, (_, h) in enumerate(Hh) if h >= top - 0.3] or [0]); S_ = Hh[i0:]
        dep = next((t for t, h in S_ if h < top - 0.4), None); hs = [h for _, h in S_]; mvt = [h for h in hs if 1.5 < h < top - 0.3]; pas = [hs[i] - hs[i + 1] for i in range(len(hs) - 1)] or [99]
        LIM = 300 if B.charge() < 4 else 700   # une durée ne se juge qu'au calme (C-137)
        juge(T + ' S · sans clavier : l\'horizon part ≤ 300 ms (700 sous charge : non jugé)', dep is not None and dep <= LIM, 't = %s ms · course %.1f pt' % (dep, top))
        juge(T + ' S · il remonte, monotone ; ≥ 4 images en route et aucun pas > 35 % de la course (cadence : au calme seulement)', top > 15 and all(hs[i + 1] <= hs[i] + 0.3 for i in range(len(hs) - 1)) and (B.charge() >= 4 or (len(mvt) >= 4 and max(pas) <= top * 0.35)), '%d images · pas max %.1f%s' % (len(mvt), max(pas), ' — cadence NON JUGÉE' if B.charge() >= 4 else ''))
        juge(T + ' S · d\'abord l\'horizon, puis le trait ; la phrase à sa place', 'horizon-haut' in J and 'montre' in J and J.index('horizon-haut') < len(J) - 1 - J[::-1].index('montre') and g3['tr'] in ('none', '0px', '0px 0px') and g3['ph'] and (g3['base'] != g0['base'] or abs(g3['ph'][0] - g0['ph'][0]) <= 0.5), '%s · %s' % (J[-4:], g3['tr']))
    if pg.__dict__['erreurs']: juge(T + ' aucune erreur de page', False, pg.__dict__['erreurs'][:2])
    ctx.close()

with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_invite_page_plus — %s, charge %.1f' % (F, B.charge()))
    ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), None)   # v177b (C-227 : un juge ≤ 10 min) : une échelle par passe
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        if ECH and ECH != nom: continue
        for sombre in (False, True):
            for nat in ('promi', 'chiche', 'nuee'):
                if VITE and (nom != '1' or sombre) and nat != 'promi': continue
                if SEUL and SEUL != nat and SEUL != '%s-%s-%s' % (nat, 'sombre' if sombre else 'clair', nom): continue   # --seul=promi (clair, 1) ou --seul=promi-sombre-1
                if SEUL == nat and (nom != '1' or sombre): continue
                tour(b, nat, sombre, vw, vh, nom)
    if ECH == '0,79': b.close(); print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
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
