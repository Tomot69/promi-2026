#!/usr/bin/env python3
"""
banc_tom.py — LE BANC « COMME TOM LA VOIT » (v142, Tom, 11 oct. 2026).

« Pour chaque point visuel, la preuve est une capture prise comme Tom la voit : WebKit, 390 × 844, échelle 3, évènements tactiles réels
(touchstart, touchmove, touchend), en suivant le chemin réel depuis l'accueil. »

Ce que ce banc change face aux juges d'avant, et pourquoi (mesuré en v142) :
  · `navigator.webdriver` est MASQUÉ : sous un navigateur piloté l'app garde le jeu de démonstration (v94) ; sur un vrai téléphone la Toile
    part VIDE et l'état est relu de la sauvegarde. Les juges d'avant jugeaient un état que l'iPhone de Tom n'a jamais.
  · la fenêtre fait 390 × 844 : l'appareil y est RÉDUIT (≈ 0,93), comme dans Safari sur l'iPhone (≈ 0,82 avec ses barres) — pas à l'échelle 1
    comme à 430 × 932. Toute comparaison de deux unités s'y voit.
  · les paroles sont plantées par l'app elle-même (le + → la nature → le bouton de plantation), puis la page est RECHARGÉE quand on le demande.
  · un toucher est `touchscreen.tap` (touchstart / touchend de WebKit) ; un glissé est une suite de TouchEvent ET de PointerEvent posés sur
    l'élément sous le doigt (WebKit piloté n'a pas d'autre voie pour un touchmove ; ils ne sont pas « de confiance », on le sait : ils
    atteignent les gestionnaires de l'app, mais le navigateur ne fait pas DÉFILER une page sur eux — un défilement se pose par `defile`).
"""
import io
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
def contexte(b, sombre=False, stockage=None, onb=True, guide=True, vw=390, vh=844, dsf=3):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dsf, has_touch=True, is_mobile=True, user_agent=UA, color_scheme='dark' if sombre else 'light')
    s = "try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}"
    s += "try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');"
    if onb: s += "localStorage.setItem('promi_onb','1');"
    if guide: s += "localStorage.setItem('promi_guide','1');"
    s += "localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s');" % ('dark' if sombre else 'light')
    for k, v in (stockage or {}).items(): s += "localStorage.setItem(%r,%r);" % (k, v)
    s += "}}catch(e){}"
    ctx.add_init_script(s); return ctx
def toile_pleine(ctx, n=25):
    """⚑ v145 (C-112, R-B) — LA TOILE DE TOM EST PLEINE. Relit, comme un téléphone à l'ouverture, une Toile de n paroles (10, 25 ou 50) plantées par
    l'app elle-même et gardées dans banc-etats/etat-n.json (tout le stockage local ; bâties par scratchpad/v145/etats.py). À appeler après
    `contexte()` et avant `ouvre()`. Le juge de v144 plantait trois paroles sur une Toile vide : il n'a pas vu ce qui saccadait chez Tom."""
    import json
    st = json.load(io.open('banc-etats/etat-%d.json' % n, encoding='utf-8')); st.pop('promi_theme', None)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
def etat_tom(chemin=None):
    """⚑ v160 (C-179) — le dernier état exporté par l'iPhone de Tom (`?export=1` → etats/tom-<date>.json), ou celui qu'on nomme ; None s'il n'y en a pas."""
    import json, glob, os
    if not chemin:
        L = sorted(glob.glob('etats/tom-*.json'))
        if not L: return None
        chemin = L[-1]
    d = json.load(io.open(chemin, encoding='utf-8')); d['_fichier'] = os.path.basename(chemin); return d
def contexte_tom(b, chemin=None, echelle=None, sombre=None):
    """⚑ v160 (C-179, A2) — rejouer EXACTEMENT l'état de Tom : tout son localStorage, sa fenêtre (largeur, hauteur), sa densité, son thème. `echelle=1`
    force une fenêtre de 430 × 932 (l'appareil à l'échelle 1) avec le même stockage. Rend (contexte, état) ; (None, None) sans état exporté."""
    import json
    d = etat_tom(chemin)
    if not d: return None, None
    e = d.get('ecran') or {}; ls = dict(d.get('ls') or {})
    vw, vh = int(e.get('largeur') or 390), int(e.get('hauteur') or 664)
    if echelle == 1: vw, vh = 430, 932
    th = ls.get('promi_theme'); sb = (th == 'dark') if sombre is None else sombre
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=float(e.get('dpr') or 3), has_touch=True, is_mobile=True, user_agent=UA,
                        color_scheme='dark' if (e.get('schema') == 'dark') else 'light', reduced_motion='reduce' if e.get('reduit') else 'no-preference')
    s = "try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}"
    s += "try{ if(!sessionStorage.getItem('__etatTom')){ sessionStorage.setItem('__etatTom','1'); localStorage.clear(); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(ls)
    ctx.add_init_script(s); return ctx, d
def charge():
    """la charge de la machine (moyenne sur une minute) : au-delà de 4 sur ce Mac, une mesure de cadence ne vaut rien (une autre session y lance parfois un simulateur)"""
    import os
    return os.getloadavg()[0]
def ouvre(ctx, fichier='app.html', attente=6500, q=''):
    pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/' + fichier + q); pg.wait_for_timeout(attente); return pg
def dev(pg): return pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height,r.width/390]}")
def pt(pg, x, y):
    """un point donné en cotes de l'appareil (390 × 844) → en pixels de la fenêtre"""
    d = dev(pg); return d[0] + x * d[4], d[1] + y * d[4]
def tap(pg, x, y, appareil=True):
    X, Y = pt(pg, x, y) if appareil else (x, y); pg.touchscreen.tap(X, Y)
def tap_sel(pg, sel):
    r = pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", sel)
    if r: pg.touchscreen.tap(r[0], r[1])
    return r
GLISSE = """async ([pts, pas, tenue, rx, ry])=>{ const el0=document.elementFromPoint(pts[0][0],pts[0][1]); if(!el0) return null; let id=7;
  /* WebKit piloté refuse `new Touch` (« Illegal constructor ») : l'évènement est alors un Event de type touch…, qui porte les mêmes listes */
  const T=(el,x,y)=>{ const o={identifier:id,target:el,clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,radiusX:rx,radiusY:ry,rotationAngle:0,force:0.5}; try{ return new Touch(o); }catch(e){ return o; } };
  const ev=(typ,x,y,fin)=>{ const t=T(el0,x,y), L=fin?[]:[t]; let e; try{ e=new TouchEvent(typ,{bubbles:true,cancelable:true,composed:true,touches:L,targetTouches:L,changedTouches:[t]}); if(!e.changedTouches||!e.changedTouches.length) throw 0; }
    catch(_){ e=new Event(typ,{bubbles:true,cancelable:true,composed:true}); Object.defineProperty(e,'touches',{value:L}); Object.defineProperty(e,'targetTouches',{value:L}); Object.defineProperty(e,'changedTouches',{value:[t]}); }
    el0.dispatchEvent(e); };
  const pe=(typ,x,y)=>el0.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,composed:true,pointerId:id,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,width:rx*2,height:ry*2,pressure:typ==='pointerup'?0:0.5,buttons:typ==='pointerup'?0:1}));
  const att=ms=>new Promise(r=>setTimeout(r,ms));
  pe('pointerdown',pts[0][0],pts[0][1]); ev('touchstart',pts[0][0],pts[0][1]); if(tenue) await att(tenue);
  for(let i=1;i<pts.length;i++){ await att(pas); pe('pointermove',pts[i][0],pts[i][1]); ev('touchmove',pts[i][0],pts[i][1]); }
  await att(pas); const L=pts[pts.length-1]; pe('pointerup',L[0],L[1]); ev('touchend',L[0],L[1],true); return (el0.id||el0.className||el0.tagName)+''; }"""
def glisse(pg, pts, pas=16, tenue=0, appareil=True, rx=11, ry=11):
    """un doigt posé au premier point, qui passe par les suivants (pas ms entre deux), puis se lève ; tenue = ms d'appui avant de bouger"""
    P = [list(pt(pg, x, y)) if appareil else [x, y] for x, y in pts]
    return pg.evaluate(GLISSE, [P, pas, tenue, rx, ry])
def droite(a, b, n=14): return [[a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n] for i in range(n + 1)]
def plante(pg, titre, qui='moi', nature=0, attente=2600):
    """planter par l'app : le + → la tuile de la nature (0 Promi, 1 Chiche) → le titre → le bouton de plantation"""
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("n=>{const x=[...document.querySelectorAll('#createSheet .tile')][n];x&&x.click()}", nature); pg.wait_for_timeout(1500)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a[0];document.getElementById('fWho').value=a[1];window._csEnLair=true;window._csDueISO=null}", [titre, qui])
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(attente)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
def plante_doigt(pg, titre, qui='moi', nature=0, attente=2600):
    """⚑ v145 — planter PAR LE VRAI CHEMIN, AU DOIGT : le + de l'accueil, la pilule de la nature (0 Promi, 1 Chiche), le titre, le bouton.
    `plante()` passe par un clic scripté sur la tuile de la page + : après un Chiche, la phrase GARDE le Chiche (mesuré en v145 : 46 Chiche sur
    50 paroles « Promi ») — la pilule, elle, attend que la page + porte la nature demandée. Rend la nature réellement plantée (True = Chiche)."""
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(350)
    tap_sel(pg, '#createBtn'); pg.wait_for_timeout(650)
    k = ['promi', 'chiche', 'nuee'][nature]
    tap_sel(pg, '.acc-pil[data-k=%s]' % k)
    for _ in range(40):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }", k): break
    pg.wait_for_timeout(500)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a[0];document.getElementById('fWho').value=a[1];window._csEnLair=true;window._csDueISO=null}", [titre, qui])
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(attente)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    return pg.evaluate("()=>{ var p=promises[promises.length-1]; return p ? !!p.chiche : null; }")
def capture(pg, chemin=None, appareil=True):
    d = dev(pg); kw = {'clip': {'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]}} if appareil else {}
    b = pg.screenshot(**kw)
    if chemin: io.open(chemin, 'wb').write(b)
    return b
def image(pg):
    """la capture de l'appareil, ramenée à 390 × 844 (pour lire des pixels en cotes de l'appareil)"""
    from PIL import Image
    return Image.open(io.BytesIO(capture(pg))).convert('RGB').resize((390, 844))
def defile(pg, sel, dy):
    """faire défiler un conteneur de dy points de l'appareil (le navigateur piloté ne défile pas sur un glissé synthétique)"""
    pg.evaluate("([s,d])=>{ const e=document.querySelector(s); if(e){ e.scrollTop+=d; e.dispatchEvent(new Event('scroll')); } }", [sel, dy])
