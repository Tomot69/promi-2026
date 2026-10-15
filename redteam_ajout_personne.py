#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_ajout_personne.py — AJOUTER UNE PERSONNE, PAGE + ET FICHE (v146, Tom, 14 oct. 2026 — C-122, bug bloquant).

« Supprime l'encart supplémentaire. Toucher la zone en pointillés ouvre le clavier dans cette zone même : le texte s'écrit là, et nulle
part ailleurs. Validation : un « + », pas un « v ». Il est à droite du nom, sur la même ligne, sans encart. Couleur : l'orange de l'app
#FB4C0D. Gras, à la hauteur des majuscules et des lettres hautes du texte saisi. Il paraît dès le premier caractère. La touche Retour
valide aussi. Le nom validé est posé ; une nouvelle ligne en pointillés se propose pour le suivant. Rien ne passe sous le clavier : la
fiche défile pour garder la ligne visible. »

Par banc_tom (WebKit, 390 × 844 @3x, vrai toucher, vrai chemin : le +, la pilule de la nature, le mot de la phrase, la zone en
pointillés). Les valeurs décidées sont EN DUR : l'orange (251, 76, 13), la zone en pointillés, 14 pt d'air au-dessus du clavier (8 exigés).
Le navigateur piloté n'a pas de clavier : sa hauteur est SIMULÉE par `visualViewport.height` (336 pt, celle d'un iPhone), ce que l'app lit.
Le verdict du « + » vient de l'IMAGE (sa couleur, sa hauteur comparée à celle de la capitale du nom, son épaisseur) ; le reste, du rendu.

  A · page + · Promi « à qui »       1 personne (validée au +), puis plantée au trait : UNE parole
  B · page + · Chiche « à qui »      2 personnes (le +, puis Retour), plantée : UNE parole
  C · page + · Promi « à qui »       4 personnes (+, Retour, +, Retour), en sombre, plantée : UNE parole à quatre
  D · fiche · Peaufiner « À QUI »    1 personne de plus sur une parole plantée (la liste défile dans sa carte)
  E · page + · Cercle « avec »       2 personnes

Preuve (§7) : `python3 redteam_ajout_personne.py sauvegardes/app-avant-v146.html` — la version d'avant : il rougit.
Usage : python3 redteam_ajout_personne.py [fichier.html] [--port=8752] [--seul=A]
"""
import sys, io, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); PORT = arg('port', '8752'); SEUL = arg('seul', '')
ORANGE = (251, 76, 13)          # #FB4C0D — l'orange du point de départ d'une action (Tom, v146)
CLAVIER = 336                   # la hauteur du clavier simulé, en points de la fenêtre (iPhone)
AIR = 8                         # la ligne se tient au moins 8 pt au-dessus du clavier (l'app en vise 14)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:300]), flush=True)

GN = '#createSheet .gn, #dpdCorps .gn'
ETAT = r"""(sel)=>{ const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
  const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  const R=e=>{ if(!e) return null; const q=e.getBoundingClientRect(); return {x:(q.left-dv.left)/k, y:(q.top-dv.top)/k, w:q.width/k, h:q.height/k, fx:q.left, fy:q.top, fw:q.width, fh:q.height}; };
  const vu=e=>{ const cs=getComputedStyle(e), q=e.getBoundingClientRect(); return cs.display!=='none' && cs.visibility!=='hidden' && parseFloat(cs.opacity)>0.05 && q.width>4 && q.height>4; };
  const z=g.querySelector(':scope > .ph-add'), cs=z?getComputedStyle(z):null, L=g.querySelector(':scope > .gn-liste');
  /* les ENCARTS de la ligne d'ajout : tout nœud visible, hors de la liste des profils, qui porte un contour ou un fond — la zone exceptée */
  const encarts=[...g.querySelectorAll('*')].filter(e=>e!==z && !(L&&L.contains(e)) && vu(e)).filter(e=>{ const c=getComputedStyle(e);
      const bord=['Top','Right','Bottom','Left'].some(s=>parseFloat(c['border'+s+'Width'])>0.5 && c['border'+s+'Style']!=='none');
      const fond=c.backgroundColor && !/rgba\(0, 0, 0, 0\)|transparent/.test(c.backgroundColor) && !e.classList.contains('ph-caret');
      const q=e.getBoundingClientRect(); return (bord||fond) && q.width>30 && q.height>16; }).map(e=>(e.className||e.tagName)+'');
  const champs=[...document.querySelectorAll('#device input, #device textarea')].filter(vu).filter(e=>{ const q=e.getBoundingClientRect(), a=g.getBoundingClientRect(); return q.bottom>a.top-4 && q.top<a.bottom+80; }).map(e=>(e.id||e.className)+'');
  const T=z&&z.querySelector('.gn-txt'), PL=z&&z.querySelector('.gn-plus'), plv=PL&&vu(PL);
  let cap=null; if(T&&T.firstChild&&T.textContent){ const r=document.createRange(); r.setStart(T.firstChild,0); r.setEnd(T.firstChild,1); const q=r.getBoundingClientRect(); cap={fx:q.left,fy:q.top,fw:q.width,fh:q.height}; }
  const pc=PL?getComputedStyle(PL):null, cfg=g._gens; let pris=null; try{ pris=cfg?cfg.choisis():null; }catch(e){}
  const vv=window.visualViewport, clav=(vv && window.innerHeight-vv.height>100)?(vv.offsetTop+vv.height):null;
  let dessus=null; if(z){ const q=z.getBoundingClientRect(), e=document.elementFromPoint(q.left+q.width/2, q.top+q.height/2); dessus=!!(e && (e===z || z.contains(e))); }
  return {zone:R(z), bord:cs?cs.borderTopStyle:null, edit:z?z.classList.contains('gn-edit'):false, mot:z?z.textContent.trim():null,
    txt:T?T.textContent:null, txtR:R(T), encre:T?getComputedStyle(T).color:null, cap:cap,
    plus:plv?R(PL):null, plusBord:pc?(parseFloat(pc.borderTopWidth)||0):null, plusFond:pc?pc.backgroundColor:null,
    encarts:encarts, champs:champs, barre:!!g.querySelector('.gn-barre'),
    actif:(document.activeElement&&(document.activeElement.id||document.activeElement.className||document.activeElement.tagName))+'',
    saisie:document.activeElement && /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName),
    pris:pris, prises:[...g.querySelectorAll('.gn-liste .ph-o.on[data-v]')].map(b=>b.getAttribute('data-v')),
    clavier:clav, dessus:dessus, decale:(document.getElementById('device').style.translate||''), hote:g.closest('#createSheet')?'page':'fiche'}; }"""
KB = """h=>{ const vv=window.visualViewport; if(!vv) return; if(h==null){ try{ delete vv.height; }catch(e){} } else Object.defineProperty(vv,'height',{get(){return h},configurable:true}); vv.dispatchEvent(new Event('resize')); }"""


def clavier(pg, ouvert):
    pg.evaluate(KB, (844 - CLAVIER) if ouvert else None); pg.wait_for_timeout(350)


def proche(c, ref, tol=60): return abs(int(c[0]) - ref[0]) + abs(int(c[1]) - ref[1]) + abs(int(c[2]) - ref[2]) <= tol


def lit_plus(pg, e):
    """sur l'IMAGE : la couleur du « + », sa hauteur, son épaisseur ; la hauteur de la capitale du nom. En points de la fenêtre."""
    import numpy as np
    from PIL import Image
    z = e['zone']; clip = {'x': max(0, z['fx']), 'y': max(0, z['fy']), 'width': z['fw'], 'height': z['fh']}
    im = np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')).astype(int); s = im.shape[1] / z['fw']
    def boite(r): return [int(round((r['fx'] - z['fx']) * s)), int(round((r['fy'] - z['fy']) * s)), int(round(r['fw'] * s)), int(round(r['fh'] * s))]
    out = {}
    if e.get('plus'):
        x, y, w, h = boite(e['plus']); m = 3
        sub = im[max(0, y - m):y + h + m, max(0, x - m):x + w + m]
        org = (abs(sub[:, :, 0] - ORANGE[0]) + abs(sub[:, :, 1] - ORANGE[1]) + abs(sub[:, :, 2] - ORANGE[2])) <= 45
        out['orange'] = int(org.sum())
        if org.sum() > 12:
            rows = np.where(org.any(axis=1))[0]; cols = np.where(org.any(axis=0))[0]
            out['h'] = (rows[-1] - rows[0] + 1) / s; out['w'] = (cols[-1] - cols[0] + 1) / s
            out['fut'] = int(org[rows[0] + 1].sum()) / s          # l'épaisseur de la barre debout, lue sur sa première rangée pleine
            out['bas'] = (max(0, y - m) + rows[-1] + 1) / s
            # tout ce qui est peint dans la boîte du « + » est orange (aucun encart, aucun fond)
            # le fond de la zone, lu DANS la zone, à gauche, loin du pointillé et du nom (une première écriture le lisait en haut : sur un tiret)
            H0 = im.shape[0]; fond = np.median(im[int(H0 * 0.35):int(H0 * 0.65), int(22 * s):int(40 * s)].reshape(-1, 3), axis=0)
            # « autre » = un pixel qui n'est NI le fond, NI l'orange, NI un mélange des deux (le bord lissé du tracé) : sa distance au segment
            #   fond → orange, dans l'espace des couleurs. (Une première écriture comptait les pixels « loin de l'orange et loin du fond » :
            #   elle prenait le lissage du bord, 11 à 130 pixels selon le fond.)
            O = np.array(ORANGE, dtype=float); d = O - fond; v = sub.astype(float) - fond
            u = np.clip((v * d).sum(axis=2) / max(1.0, float((d * d).sum())), 0, 1)
            ecart = np.sqrt(((v - u[:, :, None] * d) ** 2).sum(axis=2))
            out['autre'] = int((ecart > 40).sum())
    if e.get('cap') and e.get('encre'):
        c = [int(v) for v in e['encre'].replace('rgb(', '').replace('rgba(', '').replace(')', '').split(',')[:3]]
        x, y, w, h = boite(e['cap']); sub = im[max(0, y - 6):y + h + 6, max(0, x):x + w]
        ink = (abs(sub[:, :, 0] - c[0]) + abs(sub[:, :, 1] - c[1]) + abs(sub[:, :, 2] - c[2])) <= 60
        if ink.sum() > 12:
            rows = np.where(ink.any(axis=1))[0]; out['cap'] = (rows[-1] - rows[0] + 1) / s; out['capBas'] = (max(0, y - 6) + rows[-1] + 1) / s
    return out


def ouvre_page(pg, nature, mot):
    pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(450)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(650)
    B.tap_sel(pg, '.acc-pil[data-k=%s]' % nature)
    for _ in range(40):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }", nature): break
    pg.wait_for_timeout(700)
    if nature == 'promi':
        B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(1000)        # « Je me promets » se retourne : « Je promets à … »
    B.tap_sel(pg, mot); pg.wait_for_timeout(1100)


def joue(pg, nom, noms, plante=None):
    """la ligne d'ajout, pour chaque personne de `noms` : toucher, écrire, valider (le +, puis Retour, en alternance)"""
    e0 = pg.evaluate(ETAT, GN)
    if not e0 or not e0['zone']:
        juge('%s : la zone en pointillés est là' % nom, False, e0); return
    juge('%s : au repos, la zone en pointillés « + ajouter quelqu’un »' % nom, e0['bord'] == 'dashed' and e0['mot'] == '+ ajouter quelqu’un', '%s · « %s »' % (e0['bord'], e0['mot']))
    deja = list(e0['pris'] or [])
    for i, n in enumerate(noms):
        avant = pg.evaluate(ETAT, GN); z = avant['zone']
        if i == 0:
            pg.touchscreen.tap(z['fx'] + z['fw'] / 2, z['fy'] + z['fh'] / 2); pg.wait_for_timeout(120)
            e = pg.evaluate(ETAT, GN) or {}
            juge('%s : toucher la zone ouvre le clavier (une entrée a le focus, dans le geste)' % nom, e.get('saisie'), e.get('actif'))
            zz = e.get('zone') or {}
            juge('%s : la zone ne bouge pas, elle reste en pointillés' % nom, bool(zz) and abs(zz['x'] - z['x']) < 1 and abs(zz['w'] - z['w']) < 1 and abs(zz['h'] - z['h']) < 1 and abs(zz['y'] - z['y']) < 1 and e.get('bord') == 'dashed',
                 'avant [%.0f %.0f %.0f %.0f] · après %s · %s' % (z['x'], z['y'], z['w'], z['h'], zz and [round(zz[c]) for c in 'xywh'], e.get('bord')))
            juge('%s : aucun second encart, aucun champ visible à côté' % nom, not e.get('barre') and not e.get('encarts') and not e.get('champs'), 'barre %s · encarts %s · champs %s' % (e.get('barre'), e.get('encarts'), e.get('champs')))
            clavier(pg, True)
        e = pg.evaluate(ETAT, GN) or {}
        zz = e.get('zone')
        ok = bool(zz) and e.get('clavier') is not None and zz['fy'] + zz['fh'] <= e['clavier'] - AIR and zz['fy'] >= 0 and e.get('dessus')
        juge('%s : %d personne(s) — la ligne est au-dessus du clavier, visible' % (nom, len(deja) + i), ok, zz and 'bas de la ligne %.0f · haut du clavier %s · décalage « %s »' % (zz['fy'] + zz['fh'], e.get('clavier'), e.get('decale')))
        # le premier caractère : le « + » paraît
        pg.keyboard.type(n[0], delay=30); pg.wait_for_timeout(60)
        e = pg.evaluate(ETAT, GN) or {}
        juge('%s : « %s » — le « + » paraît dès le premier caractère' % (nom, n), e.get('txt') == n[0] and bool(e.get('plus')), 'écrit « %s » · + %s' % (e.get('txt'), bool(e.get('plus'))))
        pg.keyboard.type(n[1:], delay=30); pg.wait_for_timeout(420)
        e = pg.evaluate(ETAT, GN) or {}
        t, pl, zz = e.get('txtR'), e.get('plus'), e.get('zone')
        dans = bool(t and zz) and t['x'] >= zz['x'] and t['x'] + t['w'] <= zz['x'] + zz['w'] and t['y'] >= zz['y'] and t['y'] + t['h'] <= zz['y'] + zz['h']
        juge('%s : « %s » s\'écrit dans la zone, et nulle part ailleurs' % (nom, n), e.get('txt') == n and dans and not e.get('champs') and not e.get('encarts'), 'texte « %s » · dans la zone %s · champs %s · encarts %s' % (e.get('txt'), dans, e.get('champs'), e.get('encarts')))
        if pl and t:
            juge('%s : le « + » est à droite du nom, sur la même ligne, sans encart' % nom, 3 <= pl['x'] - (t['x'] + t['w']) <= 22 and abs((pl['y'] + pl['h'] / 2) - (t['y'] + t['h'] / 2)) <= 5 and (e.get('plusBord') or 0) == 0 and 'rgba(0, 0, 0, 0)' in (e.get('plusFond') or ''),
                 'écart %.1f pt · centres %.1f / %.1f · contour %s · fond %s' % (pl['x'] - (t['x'] + t['w']), pl['y'] + pl['h'] / 2, t['y'] + t['h'] / 2, e.get('plusBord'), e.get('plusFond')))
            m = lit_plus(pg, e)
            if i == 0:
                try: B.capture(pg, 'planche-v146/ajout-%s.png' % nom.split(' ')[0])
                except Exception: pass
            juge('%s : le « + » est orange #FB4C0D (lu sur l\'image), rien d\'autre dans sa boîte' % nom, m.get('orange', 0) > 60 and m.get('autre', 99) <= 6, m)
            juge('%s : le « + » a la hauteur de la capitale du nom (± 1 pt), posé sur la même ligne de base, et il est gras' % nom,
                 'h' in m and 'cap' in m and abs(m['h'] - m['cap']) <= 1.0 and abs(m['bas'] - m['capBas']) <= 1.0 and m['fut'] >= 0.17 * m['h'],
                 'hauteur du + %.2f · capitale %.2f · bas %.2f / %.2f · épaisseur %.2f' % (m.get('h', 0), m.get('cap', 0), m.get('bas', 0), m.get('capBas', 0), m.get('fut', 0)))
        else:
            juge('%s : le « + » est à droite du nom, sur la même ligne, sans encart' % nom, False, 'pas de « + » (%s)' % (e.get('mot'),))
        # la validation : le +, puis Retour, en alternance
        if i % 2 == 0 and pl:
            # v146 : le champ ne perd JAMAIS le focus au toucher du « + » (il le perdait 30 ms : clavier qui clignote, lettres perdues)
            pg.evaluate("()=>{ window.__fo=0; if(!window.__foArm){ window.__foArm=1; document.addEventListener('focusout', e=>{ if(e.target && e.target.id==='gnSaisie') window.__fo++; }, true); } }")
            pg.touchscreen.tap(pl['fx'] + pl['fw'] / 2, pl['fy'] + pl['fh'] / 2); comment = 'le +'
        else:
            pg.keyboard.press('Enter'); comment = 'Retour'
        pg.wait_for_timeout(950)
        e = pg.evaluate(ETAT, GN) or {}
        juge('%s : %s valide « %s » — le nom est posé' % (nom, comment, n), n in (e.get('pris') or []) and n in (e.get('prises') or []), 'choisis %s · pastilles prises %s' % (e.get('pris'), e.get('prises')))
        if comment == 'le +': fo = pg.evaluate("()=>window.__fo"); juge('%s : toucher le « + » garde le clavier — le champ ne perd jamais le focus' % nom, fo == 0, '%s perte(s) de focus' % fo)
        zz = e.get('zone')
        juge('%s : après « %s », une nouvelle ligne en pointillés se propose, vide, et le clavier reste' % (nom, n),
             bool(zz) and e.get('bord') == 'dashed' and not e.get('txt') and not e.get('plus') and e.get('saisie') and not e.get('barre') and not e.get('encarts'),
             'zone %s · %s · texte « %s » · + %s · focus %s' % (bool(zz), e.get('bord'), e.get('txt'), bool(e.get('plus')), e.get('actif')))
    e = pg.evaluate(ETAT, GN) or {}; zz = e.get('zone')
    juge('%s : %d personne(s) — la ligne suivante est encore au-dessus du clavier' % (nom, len(deja) + len(noms)), bool(zz) and e.get('clavier') is not None and zz['fy'] + zz['fh'] <= e['clavier'] - AIR and zz['fy'] >= 0 and e.get('dessus'),
         zz and 'bas %.0f · clavier %s · décalage « %s »' % (zz['fy'] + zz['fh'], e.get('clavier'), e.get('decale')))
    juge('%s : les %d personnes sont là, dans l\'ordre' % (nom, len(noms)), (e.get('pris') or [])[-len(noms):] == noms, e.get('pris'))
    # le clavier se retire : la zone reprend son mot, l'appareil revient à sa place
    clavier(pg, False); pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(500)
    e = pg.evaluate(ETAT, GN) or {}
    juge('%s : clavier retiré, la zone reprend « + ajouter quelqu’un » et rien ne reste décalé' % nom, e.get('mot') == '+ ajouter quelqu’un' and not e.get('decale') and e.get('bord') == 'dashed', '« %s » · décalage « %s »' % (e.get('mot'), e.get('decale')))


def plante_au_trait(pg, nom, titre, noms, chiche):
    """planter par le geste (70 pt, la règle en demande 60) : UNE parole, à toutes les personnes"""
    pg.evaluate("a=>{ document.getElementById('fTitle').value=a; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} window._csEnLair=true; window._csDueISO=null; }", titre); pg.wait_for_timeout(300)
    n0 = pg.evaluate("()=>promises.length")
    z = pg.evaluate("()=>{ const c=document.getElementById('planterZone'); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }")
    if not z:
        juge('%s : plantée au trait' % nom, False, 'pas de zone de trait'); return None
    y = z[1] + z[3] * 0.45; B.glisse(pg, [[40 + 80 * i / 10.0, y] for i in range(11)], pas=60); pg.wait_for_timeout(3400)
    r = pg.evaluate("()=>{ var p=promises[promises.length-1]; return {n:promises.length, id:p.id, who:p.who, titre:p.title, chiche:!!p.chiche}; }")
    qui = [x.strip() for x in str(r['who']).split(',')]
    juge('%s : plantée au trait — UNE parole, à %s' % (nom, ', '.join(noms)), r['n'] == n0 + 1 and qui == noms and r['chiche'] == chiche, '%d → %d paroles · « %s » à « %s » · chiche %s' % (n0, r['n'], r['titre'], r['who'], r['chiche']))
    pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    return r['id']


with sync_playwright() as p:
    b = p.webkit.launch()
    def page(sombre=False):
        ctx = B.contexte(b, sombre=sombre); pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500); return pg
    pg = page()
    try:
        pid = None
        if SEUL in ('', 'A', 'D'):
            ouvre_page(pg, 'promi', '#csPhrase [data-ph=qui]')
            joue(pg, 'A · page + · Promi · 1 personne', ['Rachel'])
            pid = plante_au_trait(pg, 'A', 'rendre le livre', ['Rachel'], False)
        if SEUL in ('', 'B'):
            ouvre_page(pg, 'chiche', '#csPhrase [data-ph=qui]')
            joue(pg, 'B · page + · Chiche · 2 personnes', ['Marion', 'Nico'])
            plante_au_trait(pg, 'B', 'le grand plongeoir', ['Marion', 'Nico'], True)
        if SEUL in ('', 'D') and pid is not None:
            pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(600); pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2400)
            B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
            c = pg.evaluate("""()=>{ const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>/^À QUI$/.test(((r.querySelector('.s2-lab')||{}).textContent||'').trim())); if(!r) return null; const q=(r.querySelector('.s2-lab')||r).getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }""")
            if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
            joue(pg, 'D · fiche · Peaufiner « À QUI » · 1 de plus', ['Adrien'])
            w = pg.evaluate("i=>promises.find(p=>p.id===i).who", pid)
            juge('D · la parole de la fiche porte les deux personnes', [x.strip() for x in str(w).split(',')] == ['Rachel', 'Adrien'], w)
        if SEUL in ('', 'E'):
            ouvre_page(pg, 'nuee', '#nueePhrase [data-np=avec]')
            joue(pg, 'E · page + · Cercle « avec » · 2 personnes', ['Lou', 'Sam'])
            m = pg.evaluate("()=>(window.newNueeMembers||[]).slice()")
            juge('E · le Cercle en cours porte ses deux membres', m == ['Lou', 'Sam'], m)
        juge('aucune erreur de page (clair)', not pg.erreurs, pg.erreurs[:2])
        if SEUL in ('', 'C'):
            pg.context.close(); pg = page(sombre=True)
            ouvre_page(pg, 'promi', '#csPhrase [data-ph=qui]')
            joue(pg, 'C · page + · Promi · 4 personnes · sombre', ['Rachel', 'Marion', 'Nico', 'Adrien'])
            plante_au_trait(pg, 'C', 'venir au concert', ['Rachel', 'Marion', 'Nico', 'Adrien'], False)
            juge('aucune erreur de page (sombre)', not pg.erreurs, pg.erreurs[:2])
    except Exception as ex:
        juge('le juge va au bout', False, str(ex).replace('\n', ' ')[:300])
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1500])
sys.exit(0 if ok == len(res) else 1)
