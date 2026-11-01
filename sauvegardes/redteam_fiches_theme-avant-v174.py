#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_fiches_theme.py — LES FICHES : LA VERSION SOMBRE PARTOUT, LA FLÈCHE EN ORANGE (v146, Tom, 14 oct. 2026 — C-132, C-133).

« C-132. Toutes les fiches (Promi, Chiche, Cercle) prennent en mode CLAIR exactement la version qu'elles ont en mode sombre. La fiche est
donc la même dans les deux modes. Promi : fond du bas en #0E78F2 sous le trait. Chiche : #7C3F58. Cercle : #5D4978. Vérifie que chaque
fiche est identique en clair et en sombre : planter, tenir, tenue, reçue, à plusieurs.
C-133. Le départ de la flèche du trait (le chevron où l'on commence à tracer) passe en orange #FB4C0D. Sur TOUTES les fiches, en clair et
en sombre, et quel que soit le design choisi dans Peaufiner. »

Par banc_tom (WebKit, 390 × 844 @3x), sur une Toile relue de la sauvegarde (banc-etats/etat-10.json : mêmes paroles, mêmes places dans les
deux thèmes), complétée des cas qui manquent (reçue, à plusieurs, tenue, un Cercle). L'app est ouverte une fois en clair, une fois en sombre.

  A · IDENTIQUES — pour chaque état, la capture de l'appareil en clair et en sombre : hors de la matière (la dalle, que l'app déclare et qui
      respire avec l'horloge), la part de pixels qui diffèrent de plus de 24 niveaux (somme des trois canaux) est ≤ 0,05 % (EN DUR) ; la
      matière, elle, occupe la même boîte, a la même couleur moyenne (≤ 4 niveaux) et diffère sur ≤ 6 % de ses pixels. États : fiche Promi à tenir · en cours · tenue · à quelqu'un · reçue ; Chiche lancé ·
      reçu · à plusieurs (trois parts) · tenu ; Cercle ; Peaufiner d'un Promi, d'un Chiche, d'un Cercle ; page + Promi (à soi, à
      quelqu'un), Chiche, Cercle. Une image des écarts est gardée pour tout état qui rate (planche-v146/ecart-<état>.png).
  B · LE FOND DU BAS, lu sur l'image sous le trait, dans les deux thèmes : Promi (14, 120, 242) · Chiche (124, 63, 88) · Cercle (93, 73, 120)
      · une parole tenue : la terre (43, 16, 32). EN DUR.
  C · LE CHEVRON : le départ de la flèche du trait est orange (251, 76, 13), lu sur l'image à la pointe déclarée par le trait, sur chaque
      fiche à tracer et sur la page +, dans les deux thèmes, et sous les douze pinceaux de Peaufiner.
Preuve (§7) : sur la version d'avant (`zz-avant-v146.html`, copie à la racine de sauvegardes/app-avant-v146.html) A, B et C rougissent.
Usage : python3 redteam_fiches_theme.py [fichier.html] [--seul=nom] [--sans-pinceaux]
"""
import sys, io, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
import numpy as np
from PIL import Image
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); SEUL = arg('seul', ''); PINCEAUX = '--sans-pinceaux' not in sys.argv
PART_MAX = 0.05          # % de pixels différents entre clair et sombre — EN DUR
CORPS = {'promi': (14, 120, 242), 'chiche': (124, 63, 88), 'nuee': (93, 73, 120), 'tenue': (43, 16, 32)}          # #0E78F2 · #7C3F58 · #5D4978 · #2B1020
ORANGE = (251, 76, 13)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:300]), flush=True)

# les cas qui manquent à la sauvegarde : posés par la donnée, comme le réseau les poserait (le prototype n'en a pas)
PREPARE = """()=>{ window._vivantOff=true; const P=promises.filter(p=>!p.draft); const par=(t)=>P.find(p=>p.title===t);
  const o={};
  P.forEach(p=>{ p.status='encours'; delete p.parts; });          /* on part d'un état connu : tout en cours, puis les cas voulus */
  o.atenir=par('rendre le livre').id; par('rendre le livre').status='atenir';
  o.encours=par('écrire à Lou').id;
  const t=par('faire les crêpes'); t.status='tenu'; t.keptAt=1760000000000; o.tenue=t.id;
  o.aquelquun=par('arroser le ficus').id;
  const r=par('appeler mamie'); r.from='Marion'; r.who='moi'; o.recue=r.id;
  o.chiche=par('courir dimanche').id;
  const cr=par('réparer le vélo'); cr.from='Adrien'; cr.who='moi'; o.chicheRecu=cr.id;
  const cp=par('trier les photos'); cp.chiche=true; cp.who='Rachel, Marion, Nico'; cp.from='moi'; cp.parts={'Marion':'2026-10-12T10:00:00.000Z'}; o.plusieurs=cp.id;
  const ct=par('ranger le garage'); ct.chiche=true; ct.status='tenu'; ct.keptAt=1760000000000; o.chicheTenu=ct.id;
  try{ NUE['potager']='le potager'; NUEEMEM['potager']=['Rachel','Adrien']; const m=par('finir la maquette'); m.nuee='potager'; }catch(e){}
  try{ syncAll(); }catch(e){} try{ queueSave&&queueSave(); }catch(e){}
  return o; }"""
TRAIT = """()=>{ const cv=[...document.querySelectorAll('#dpTrameCv, #csTrameCv, #createSheet canvas[data-trait], #createSheet canvas[data-depart]')].find(c=>c.getBoundingClientRect().width>50 && getComputedStyle(c).visibility!=='hidden' && c.closest('.show')); if(!cv) return null;
  const t=(cv.getAttribute('data-trait')||'').split(','); const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, q=cv.getBoundingClientRect();
  let zones=[]; try{ zones=(window._zonesMatiere?window._zonesMatiere().zones:[])||[]; }catch(e){}
  return {id:cv.id, trait:t, depart:cv.getAttribute('data-depart'), x0:(q.left-d.left)/k, y0:(q.top-d.top)/k, w:q.width/k, zones:zones}; }"""


def capture(pg): return np.asarray(Image.open(io.BytesIO(B.capture(pg))).convert('RGB').resize((780, 1688), Image.LANCZOS)).astype(int)
# ⚠ v146 (C-134) : Peaufiner refuse une fermeture générale dans les 4 s qui suivent un geste fait en lui — le juge DÉCLARE sa sortie
#   (`_peaufSortie`) avant chaque `closeAll`, sinon la fiche suivante s'ouvre sous un Peaufiner resté ouvert.
# ⚠ LE BORD DE L'APPAREIL N'EST PAS LA FICHE : le cadre du téléphone (son filet, ses coins arrondis) appartient à la page, qui suit le thème de
#   l'app — mesuré : 0,19 % de pixels, tous sur le pourtour. On juge l'INTÉRIEUR : 3 pt de retrait, et les quatre coins (34 pt) exclus.
MASQUE = np.ones((1688, 780), dtype=bool); MASQUE[:6, :] = MASQUE[-6:, :] = False; MASQUE[:, :6] = MASQUE[:, -6:] = False
for _y, _x in ((0, 0), (0, 780 - 68), (1688 - 68, 0), (1688 - 68, 780 - 68)): MASQUE[_y:_y + 68, _x:_x + 68] = False


def ouvre_fiche(pg, pid):
    pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2800)


def page_plus(pg, nature, a_qui=False):
    pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(500)
    # la dalle « à planter » de la page + est tirée au hasard à chaque ouverture : on donne le MÊME tirage aux deux thèmes (le hasard n'est pas ce qu'on juge)
    pg.evaluate("()=>{ if(!window.__mr) window.__mr=Math.random; let s=20261014; Math.random=function(){ s=(Math.imul(s,1664525)+1013904223)>>>0; return s/4294967296; }; }")
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(650); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nature)
    for _ in range(40):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }", nature): break
    pg.wait_for_timeout(700)
    if a_qui: B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(900)
    # la même phrase dans les deux thèmes, ÉCRITE par le vrai chemin (l'exemple proposé est tiré au hasard) : on touche le créneau, on écrit
    sel = '#nueePhrase [data-np=nom]' if nature == 'nuee' else '#csPhrase [data-ph=titre]'
    B.tap_sel(pg, sel); pg.wait_for_timeout(500); pg.keyboard.type('Week-end à Marseille' if nature == 'nuee' else 'rendre le livre', delay=25); pg.wait_for_timeout(300)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(1300)


ETATS = [('fiche Promi à tenir', 'f', 'atenir', 'promi'), ('fiche Promi en cours', 'f', 'encours', 'promi'), ('fiche Promi tenue', 'f', 'tenue', 'tenue'), ('fiche Promi à quelqu\'un', 'f', 'aquelquun', None),
         ('fiche Promi reçue', 'f', 'recue', 'promi'), ('fiche Chiche lancé', 'f', 'chiche', 'chiche'), ('fiche Chiche reçu', 'f', 'chicheRecu', 'chiche'), ('fiche Chiche à plusieurs', 'f', 'plusieurs', 'chiche'),
         ('fiche Chiche tenu', 'f', 'chicheTenu', 'tenue'), ('fiche Cercle', 'c', 'potager', 'nuee'), ('Peaufiner Promi', 'p', 'encours', None), ('Peaufiner Chiche', 'p', 'chiche', None), ('Peaufiner Cercle', 'pc', 'potager', None),
         ('page + Promi à soi', '+', 'promi', 'promi'), ('page + Promi à quelqu\'un', '+q', 'promi', 'promi'), ('page + Chiche', '+', 'chiche', 'chiche'), ('page + Cercle', '+', 'nuee', 'nuee')]
if SEUL: ETATS = [e for e in ETATS if SEUL.lower() in e[0].lower()]


def passe(b, sombre):
    ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F); ids = pg.evaluate(PREPARE); pg.wait_for_timeout(900)
    out = {}
    for nom, genre, cle, nat in ETATS:
        try:
            if genre in ('f', 'p'): ouvre_fiche(pg, ids[cle])
            elif genre in ('c', 'pc'):
                pg.evaluate("()=>{ try{ if(window._peaufSortie) window._peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(700); pg.evaluate("k=>openEssaim(k)", cle); pg.wait_for_timeout(3000)
            elif genre == '+': page_plus(pg, cle)
            elif genre == '+q': page_plus(pg, cle, True)
            if genre in ('p', 'pc'): B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1600)
            tr = pg.evaluate(TRAIT); out[nom] = {'img': capture(pg), 'trait': tr, 'zones': (tr or {}).get('zones') or pg.evaluate("()=>{ try{ return window._zonesMatiere().zones; }catch(e){ return []; } }")}
        except Exception as ex:
            out[nom] = {'img': None, 'err': str(ex)[:120]}
    err = pg.__dict__['erreurs'][:2]; return out, err, ctx, pg


def couleur_sous_trait(e):
    """la couleur du corps : une bande de 30 × 6 pt, 40 pt sous le point le plus bas du trait, au milieu de l'écran"""
    t = e['trait']; im = e['img']
    if not t: return None
    try:
        base, amp = float(t['trait'][0]), float(t['trait'][1]); y = int((t['y0'] + base + amp + 40) * 2)
    except Exception:
        # la page + ne déclare pas son onde : on part du chevron (son départ), 70 pt plus bas, dans la marge de gauche
        if not t.get('depart'): return None
        y = int((t['y0'] + float(t['depart'].split(',')[1]) + 70) * 2)
    if y + 12 >= im.shape[0]: return None
    z = im[y:y + 12, 14:36].reshape(-1, 3); return tuple(int(v) for v in np.median(z, axis=0))


def chevron(e):
    """le départ de la flèche : la part de pixels orange dans un carré de 26 pt autour du point déclaré (`data-depart` : x,y en points du canevas)"""
    t = e['trait']
    if not t or not t.get('depart'): return None
    try: x, y = [float(v) for v in t['depart'].split(',')[:2]]
    except Exception: return None
    X, Y = int((t['x0'] + x) * 2), int((t['y0'] + y) * 2); im = e['img']; z = im[max(0, Y - 26):Y + 26, max(0, X - 26):X + 26]
    org = (abs(z[:, :, 0] - ORANGE[0]) + abs(z[:, :, 1] - ORANGE[1]) + abs(z[:, :, 2] - ORANGE[2])) <= 40
    return int(org.sum())


with sync_playwright() as p:
    b = p.webkit.launch()
    C, errC, ctxC, pgC = passe(b, False); S, errS, ctxS, pgS = passe(b, '--temoin' not in sys.argv)          # --temoin : clair contre clair (le bruit de l'instrument)
    for nom, genre, cle, nat in ETATS:
        a, s = C[nom], S[nom]
        if a['img'] is None or s['img'] is None:
            juge('A · %s : la fiche s\'ouvre dans les deux thèmes' % nom, False, a.get('err') or s.get('err')); continue
        d = np.abs(a['img'] - s['img']).sum(axis=2); d[~MASQUE] = 0
        # ⚠ LA MATIÈRE RESPIRE (une dalle du moteur est rendue avec l'horloge : témoin clair contre clair, jusqu'à 0,16 % de pixels, tous dans la
        #   dalle). On juge donc À PART ce que l'app DÉCLARE comme matière (`_zonesMatiere`) : ① hors d'elle, l'image est la même, strictement ;
        #   ② la matière occupe la même boîte dans les deux thèmes ; ③ dans la boîte, la couleur moyenne est la même (à 4 niveaux près) et moins
        #   de 6 % de ses pixels diffèrent (le bord d'une dalle qui respire ; une dalle d'une autre couleur ou d'une autre forme passe loin au-delà).
        zc, zs = a.get('zones') or [], s.get('zones') or []; M = np.zeros_like(MASQUE)
        for z in zc + zs: M[max(0, int((z[1] - 2) * 2)):int((z[1] + z[3] + 2) * 2), max(0, int((z[0] - 2) * 2)):int((z[0] + z[2] + 2) * 2)] = True
        M &= MASQUE; hors = MASQUE & ~M
        memes = len(zc) == len(zs) and all(max(abs(p - q) for p, q in zip(x, y)) <= 1.0 for x, y in zip(zc, zs))
        if M.any():
            ca, cs = a['img'][M].mean(axis=0), s['img'][M].mean(axis=0); dmat = float((d[M] > 24).mean()) * 100; dcol = float(np.abs(ca - cs).max())
        else: dmat = dcol = 0.0
        juge('A · %s : la matière (la dalle) est la même dans les deux thèmes — même boîte, même couleur moyenne (≤ 4 niveaux), ≤ 6 %% de ses pixels' % nom, memes and dcol <= 4.0 and dmat <= 6.0,
             'boîtes %s / %s · écart de couleur moyenne %.1f · %.2f %% des pixels de la matière' % ([[round(v) for v in z] for z in zc][:2], [[round(v) for v in z] for z in zs][:2], dcol, dmat))
        d[~hors] = 0; part = float((d > 24).sum()) / float(max(1, hors.sum())) * 100
        if part > PART_MAX:
            m = (d > 24); ys, xs = np.where(m); vis = a['img'].copy().astype(np.uint8); vis[m] = [255, 0, 255]
            try: Image.fromarray(np.concatenate([a['img'].astype(np.uint8), s['img'].astype(np.uint8), vis], axis=1)).save('planche-v146/ecart-%s.png' % nom.replace(' ', '-').replace("'", ''))
            except Exception: pass
            juge('A · %s : la même image en clair et en sombre (≤ %.2f %% de pixels différents)' % (nom, PART_MAX), False, '%.3f %% · zone x %d–%d, y %d–%d (points)' % (part, xs.min() // 2, xs.max() // 2, ys.min() // 2, ys.max() // 2))
        else:
            juge('A · %s : la même image en clair et en sombre (≤ %.2f %% de pixels différents)' % (nom, PART_MAX), True, '%.3f %%' % part)
        if nat:
            for th, e in (('clair', a), ('sombre', s)):
                c = couleur_sous_trait(e); v = CORPS[nat]
                juge('B · %s, %s : le fond du bas est %s' % (nom, th, '#%02X%02X%02X' % v), bool(c) and abs(c[0] - v[0]) + abs(c[1] - v[1]) + abs(c[2] - v[2]) <= 12, c)
        # le chevron : sur ce qui se trace (une fiche à tracer, la page +)
        if genre in ('+', '+q') or (genre == 'f' and cle in ('atenir', 'encours', 'aquelquun', 'chiche', 'chicheRecu')):
            for th, e in (('clair', a), ('sombre', s)):
                n = chevron(e)
                juge('C · %s, %s : le départ de la flèche est orange #FB4C0D' % (nom, th), n is not None and n >= 60, 'pixels orange autour du départ : %s · déclaré %s' % (n, (e['trait'] or {}).get('depart')))
    # C · sous les douze pinceaux (le dessin du trait choisi dans Peaufiner) : le départ reste orange
    if PINCEAUX and not SEUL:
        for th, pg in (('clair', pgC), ('sombre', pgS)):
            pg.evaluate("()=>{ if(window.__mr){ Math.random=window.__mr; } try{ setPremium(true); }catch(e){} }")
            noms = pg.evaluate("()=>(window._PINCEAU_META||[]).map(p=>p[0])") or []
            ids = pg.evaluate("()=>({a:(promises.find(p=>p.title==='rendre le livre')||{}).id})"); mauvais = []; vus = 0
            for n in noms:
                pg.evaluate("a=>{ const p=promises.find(q=>q.id===a[0]); if(p){ p.trait=a[1]; } }", [ids['a'], n]); ouvre_fiche(pg, ids['a'])
                e = {'img': capture(pg), 'trait': pg.evaluate(TRAIT)}; k = chevron(e); vus += 1
                if k is None or k < 60: mauvais.append('%s (%s)' % (n, k))
            juge('C · %s : sous les %d pinceaux de Peaufiner, le départ de la flèche est orange' % (th, len(noms)), vus >= 8 and not mauvais, ' · '.join(mauvais) or ', '.join(noms))
    juge('aucune erreur de page', not errC and not errS, (errC, errS))
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1500])
sys.exit(0 if ok == len(res) else 1)
