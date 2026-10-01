# -*- coding: utf-8 -*-
"""JUGE DE LA FICHE D'UNE PERSONNE — lot-FICHE-PERSONNE (11 septembre 2026).

Ce qu'il vérifie, et comment il ne peut PAS être trompé par l'ancienne fiche restée dans le DOM (Tom : « tes contrôles
pourraient passer au vert en lisant une fiche qui n'est plus à l'écran — c'est le faux vert de redteam_ecrans ») :
  · il lit L'ÉCRAN : la présence se mesure en PIXELS sur la capture de l'appareil, un texte ne compte que s'il est
    touché AU DOIGT (elementFromPoint en son centre, dans l'appareil) ;
  · la composition se compare aux DONNÉES qu'il recalcule lui-même (qui / de qui / avec) — jamais à ce que l'app déclare ;
  · les cotes décidées sont ÉCRITES ICI (§2.9, plateau, gestes) — le juge porte la décision, l'app la respecte (§7).
Familles : 1 présence peinte · 2 composition · 3 cotes · 4 polices · 5 les infractions de l'audit · 6 lisibilité ·
7 l'état vide · 8 les portes · 9 les deux gestes AU DOIGT, jusqu'au Promi planté.
   python3 releve-fiche-personne.py [URL]
"""
import sys, io, os, json, base64
from PIL import Image
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
# ⚑ LES DÉCISIONS, EN DUR
PLATEAU = (24, 40, 342, 60)          # §5 · la grammaire des contours
NOYAU = 58; ARC = 6; VISAGE = 36     # §2.9 · le Noyau d'une personne
NOYAU_XY = (24, 124)
COL_X = 24                           # la colonne du plateau
CARTE = (165, 198); CARTES_X = (24, 201)   # la carte d'Index (§3.9), deux par ligne
GESTE = (167, 62); GESTES_X = (24, 199)    # la paire de gestes (§5 : 168 × 62, trait 2, rayon 31)
MARGE_BAS = 22; PLI = 844
TITRE_LISTE = 'Ce que vous partagez'  # Tom, 11 sept.
TITRE_TENUES = 'Tenu ensemble'        # VALIDÉ par Tom, 11 sept. 2026 (Q193)
GESTES = ('+ Planter un Promi', '+ Lancer un Chiche')   # « + Lancer un Chiche » : validé par Tom
LEGENDE = ('tenues', 'en cours', 'à tenir')
# les infractions de l'audit (AUDIT-FICHE-PERSONNE.md § C) — aucun de ces mots ne doit être À L'ÉCRAN
INTERDITS = ['harmonie', 'rayonnante', 'solide', 'installée', 'naissante', 'à tisser', 'échangé', ' reçu', ' donné',
             'comment ça évolue', 'réciproque', 'portes un peu plus', 'toi envers eux', 'eux envers toi', '%',
             'promesse', 'votre', 'aucun promi']
ARCS = {'tenu': (43, 232, 140), 'encours': (143, 160, 255), 'rate': (240, 122, 46)}

R = []
def t(fam, nom, ok, d=''): R.append((fam, nom, bool(ok), d))

# ── ce que l'écran montre : nœuds TOUCHÉS au doigt, avec leur boîte (repère 390) et leur police ──
ECRAN = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, sh=document.getElementById('personSheet');
  const R=(e)=>{const r=e.getBoundingClientRect(); return [ (r.left-dv.left)/s, (r.top-dv.top)/s, r.width/s, r.height/s ];};
  const touche=(e)=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return false; const x=r.left+r.width/2, y=r.top+r.height/2;
    if(x<dv.left||x>dv.right||y<dv.top||y>dv.bottom) return false; const h=document.elementFromPoint(x,y); return !!(h&&(h===e||e.contains(h)||h.contains(e))); };
  const textes=[]; sh.querySelectorAll('*').forEach(e=>{ const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim(); if(!t) return;
    if(!touche(e)) return; const c=getComputedStyle(e); let op=1; for(let x=e;x&&x!==document.body;x=x.parentElement) op*=+getComputedStyle(x).opacity;
    textes.push({t:t, box:R(e), ff:c.fontFamily.split(',')[0].replace(/"/g,''), fw:c.fontWeight, fs:parseFloat(c.fontSize), tt:c.textTransform, col:c.color, fill:c.webkitTextFillColor, op:+op.toFixed(2),
      cls:String(e.className||''), id:e.id||'', dansCarte:!!e.closest('.s4-carte')}); });
  const cad=document.getElementById('psCadre'), q=(s)=>cad?[...cad.querySelectorAll(s)]:[];
  /* VISIBLE = une boîte à l'écran ET touchée au doigt — un nœud masqué par son parent garde son propre `display` */
  const vieux={}; ['#psSub','#psMirror','#psList','.grip','.ps-head'].forEach(k=>{ const e=sh.querySelector(k); if(!e){ vieux[k]=null; return; } const r=e.getBoundingClientRect();
    vieux[k]={boite:r.width>0&&r.height>0, touche:touche(e), txt:(e.textContent||'').trim().slice(0,40)}; });
  const ny=cad&&cad.querySelector('.ps-ny'), vis=cad&&cad.querySelector('.ps-vis');
  const arcs=ny?[...ny.querySelectorAll('circle.ps-arc')].map(c=>({part:+c.getAttribute('data-part'), l:parseFloat(c.getAttribute('stroke-dasharray')), sw:parseFloat(c.getAttribute('stroke-width')), r:parseFloat(c.getAttribute('r'))})):[];
  const plat=sh.querySelector('.enh');
  return {montre:sh.classList.contains('show'), cadre:cad?R(cad):null, fiche:cad?cad.getAttribute('data-fiche'):null, plateau:plat?R(plat):null,
    nom:(document.getElementById('psName')||{}).textContent, textes:textes,
    noyau:ny?R(ny):null, visage:vis?R(vis):null, visBg:vis?getComputedStyle(vis).backgroundImage.slice(0,40):null, arcs:arcs,
    cartes:q('.s4-carte').map(k=>{ const cv=k.querySelector('canvas'); return {box:R(k), ti:(k.querySelector('.s4-ti')||{}).textContent, touche:touche(k), et:(k.querySelector('.s4-et')||{}).textContent,
      champ:cv&&cv.getAttribute('data-champ'), matiere:cv&&cv.getAttribute('data-matiere')}; }),
    tenues:q('.ps-c').map(k=>({box:R(k), t:(k.querySelector('span')||{}).textContent, cv:R(k.querySelector('canvas'))})),
    titres:q('.ps-h').map(e=>({t:e.textContent, box:R(e), touche:touche(e)})), legende:q('.ps-lg span').map(e=>e.textContent),
    gestes:q('.ps-bt').map(e=>({t:e.textContent, box:R(e), touche:touche(e)})),
    avant:getComputedStyle(sh,'::before').display, vieux:vieux,
    gris:[...sh.querySelectorAll('svg path,svg line,svg polyline')].filter(p=>touche(p)).map(p=>getComputedStyle(p).stroke)}; }"""
ATTENDU = r"""(n)=>{ const L=promises.filter(p=>p&&!p.draft&&(p.who===n||p.from===n||p.avec===n));
  return {titres:L.map(p=>p.title), tenues:L.filter(p=>p.status==='tenu').map(p=>p.title), t:L.filter(p=>p.status==='tenu').length,
          e:L.filter(p=>p.status==='encours').length, r:L.filter(p=>p.status!=='tenu'&&p.status!=='encours').length}; }"""
INDEX_POLICES = r"""()=>{ const c=document.querySelector('#indexSheet .s4-carte'); if(!c) return null; const f=(s)=>{const e=c.querySelector(s), g=getComputedStyle(e); return g.fontFamily.split(',')[0]+' '+g.fontWeight;};
  return {eb:f('.s4-eb'), ti:f('.s4-ti'), et:f('.s4-et')}; }"""

def page(b, has_touch=False):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=has_touch)
    pg = ctx.new_page(); err = []; pg.on('pageerror', lambda e: err.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    return ctx, pg, err
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
def capture(pg):
    d = dev(pg); png = pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})
    return Image.open(io.BytesIO(png)).convert('RGB'), d[2] / 390.0 * 2   # px d'image par pt 390 (dsf 2)
def aura_tap(pg, nom):
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(250)
    pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(600)
    pt = pg.evaluate("""(n)=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()===n); if(!lb) return null; const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
        for(const x of document.querySelectorAll('#auraScreen .au-nb')){ const r=x.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""", nom)
    if not pt: return False
    pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1700); return True
def fond(im, k):   # la couleur du fond de la fiche, lue sous le Noyau (x 12)
    return im.getpixel((int(12 * k), int(300 * k)))
def part_peinte(im, k, box, bg, seuil=40):
    x, y, w, h = box; n = p = 0
    for yy in range(int(y * k), int((y + h) * k), 3):
        for xx in range(int(x * k), int((x + w) * k), 3):
            if 0 <= xx < im.width and 0 <= yy < im.height:
                c = im.getpixel((xx, yy)); n += 1
                if abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2]) > seuil: p += 1
    return p / n if n else 0
def couleur(s):
    if not s: return None
    s = s.strip()
    if s.startswith('#') and len(s) == 7: return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))
    v = [int(float(x)) for x in s.replace('rgb(', '').replace(')', '').split(',')[:3] if x.strip()]
    return tuple(v) if len(v) == 3 else None
def part_couleur(im, k, box, rgb, tol=40):
    x, y, w, h = box; n = p = 0
    for yy in range(int(y * k), int((y + h) * k), 3):
        for xx in range(int(x * k), int((x + w) * k), 3):
            if 0 <= xx < im.width and 0 <= yy < im.height:
                c = im.getpixel((xx, yy)); n += 1
                if abs(c[0] - rgb[0]) < tol and abs(c[1] - rgb[1]) < tol and abs(c[2] - rgb[2]) < tol: p += 1
    return p / n if n else 0
def part_loin(im, k, box, rgb, seuil=60):
    x, y, w, h = box; n = p = 0
    for yy in range(int(y * k), int((y + h) * k), 3):
        for xx in range(int(x * k), int((x + w) * k), 3):
            if 0 <= xx < im.width and 0 <= yy < im.height:
                c = im.getpixel((xx, yy)); n += 1
                if abs(c[0] - rgb[0]) + abs(c[1] - rgb[1]) + abs(c[2] - rgb[2]) > seuil: p += 1
    return p / n if n else 0
def couleur_presente(im, k, box, rgb, tol=40):
    x, y, w, h = box
    for yy in range(int(y * k), int((y + h) * k), 2):
        for xx in range(int(x * k), int((x + w) * k), 2):
            if 0 <= xx < im.width and 0 <= yy < im.height:
                c = im.getpixel((xx, yy))
                if abs(c[0] - rgb[0]) < tol and abs(c[1] - rgb[1]) < tol and abs(c[2] - rgb[2]) < tol: return True
    return False

SONDE = os.environ.get('SONDE_FICHE', '')
SONDES = {
  'cartes-vides': "()=>{ document.querySelectorAll('#psCadre .s4-carte canvas').forEach(c=>c.getContext('2d').clearRect(0,0,c.width,c.height)); }",
  'harmonie':     "()=>{ const s=document.getElementById('psSub'), h=document.querySelector('#personSheet .ps-head'); if(s){ s.textContent='votre harmonie : rayonnante · ta parole : rayonnante'; }"
                  "  if(h){ h.style.setProperty('display','flex','important'); h.style.setProperty('position','absolute','important'); h.style.setProperty('left','40px','important'); h.style.setProperty('top','60px','important'); h.style.setProperty('z-index','50','important'); } }",
}
def juge_fiche(pg, th, nom, porte):
    if SONDE in SONDES and nom == 'Rachel': pg.evaluate(SONDES[SONDE]); pg.wait_for_timeout(150)
    E = pg.evaluate(ECRAN); A = pg.evaluate(ATTENDU, nom); tag = '[%s · %s · %s]' % (th, nom, porte)
    t('8 portes', tag + ' la fiche s\'ouvre, la NOUVELLE fiche', E['montre'] and E['fiche'] == nom, 'montre %s · cadre de %s' % (E['montre'], E['fiche']))
    if not E['cadre']: t('1 présence', tag + ' pas de cadre : la fiche refaite n\'est pas à l\'écran', False); return E, A
    im, k = capture(pg); bg = fond(im, k)
    # ── 1 · PRÉSENCE PEINTE (pixels de l'écran) ──
    if A['titres']:
        for c in E['cartes']:
            if c['box'][1] + c['box'][3] <= 844 and c['box'][1] >= 100:
                # LE PEINTRE DÉCLARE ce qu'il a versé (`data-champ`, `data-matiere` — la doctrine de redteam_champ) ;
                # le juge vérifie que L'ÉCRAN le porte : le champ de cette couleur, et une dalle posée dessus.
                cc = couleur(c['champ']); z = [float(v) for v in (c['matiere'] or '0,0,0,0').split(',')]
                pc = part_couleur(im, k, c['box'], cc) if cc else 0
                pm = part_loin(im, k, (c['box'][0] + z[0], c['box'][1] + z[1], z[2], z[3]), cc) if cc and z[2] > 4 else 0
                t('1 présence', tag + ' carte « %s » : le champ (%s) est peint à l\'écran' % (c['ti'], c['champ']), pc > 0.15, 'part du champ %.2f' % pc)
                t('1 présence', tag + ' carte « %s » : sa dalle est posée sur le champ' % c['ti'], pm > 0.15, 'part de la dalle %.2f' % pm)
        for c in E['tenues']:
            pp = part_peinte(im, k, c['cv'], bg, 30)
            t('1 présence', tag + ' dalle tenue « %s » peinte' % c['t'], pp > 0.15, 'part peinte %.2f' % pp)
        for part, cle in ((0, 'tenu'), (1, 'encours'), (2, 'rate')):
            if A[{'tenu': 't', 'encours': 'e', 'rate': 'r'}[cle]]:
                t('1 présence', tag + ' l\'arc « %s » du Noyau est à l\'écran' % cle, couleur_presente(im, k, E['noyau'], ARCS[cle]), '')
    if E['visage']: t('1 présence', tag + ' le visage est dans l\'anneau', part_peinte(im, k, E['visage'], bg) > 0.8 and 'gradient' in (E['visBg'] or '') or 'url' in (E['visBg'] or ''), E['visBg'])
    # ── 2 · COMPOSITION contre les données ──
    vus = [c['ti'] for c in E['cartes']]
    t('2 composition', tag + ' une carte par parole partagée (qui · de qui · avec), dans l\'ordre', vus == A['titres'], 'vu %s · attendu %s' % (vus, A['titres']))
    t('2 composition', tag + ' « Tenu ensemble » = les paroles tenues', [c['t'] for c in E['tenues']] == A['tenues'], '%s / %s' % ([c['t'] for c in E['tenues']], A['tenues']))
    n = len(A['titres']) or 1
    L = {a['part']: a['l'] for a in E['arcs']}; tot = 2 * 3.14159265 * ((NOYAU - ARC) / 2)
    for part, cnt in ((0, A['t']), (1, A['e']), (2, A['r'])):
        vu = (L.get(part, 0) + (2 if len(E['arcs']) > 1 and part in L else 0)) / tot
        t('2 composition', tag + ' l\'anneau compte toute la liste — arc %d' % part, abs(vu - cnt / n) < 0.02 if A['titres'] else not E['arcs'], 'vu %.3f · attendu %.3f' % (vu, cnt / n))
    # ── 3 · COTES ──
    near = lambda a, b, e=1.5: abs(a - b) <= e
    p = E['plateau']; t('3 cotes', tag + ' le plateau 24/40/342×60', p and all(near(a, b) for a, b in zip(p, PLATEAU)), str(p and [round(v, 1) for v in p]))
    t('3 cotes', tag + ' le cadre tombe sur l\'appareil (0, 0, 390 × 844)', all(near(a, b) for a, b in zip(E['cadre'], (0, 0, 390, 844))), str([round(v, 1) for v in E['cadre']]))
    y = E['noyau']; t('3 cotes', tag + ' le Noyau du §2.9 : 58 à (24, 124)', y and near(y[0], NOYAU_XY[0]) and near(y[1], NOYAU_XY[1]) and near(y[2], NOYAU) and near(y[3], NOYAU), str(y and [round(v, 1) for v in y]))
    if E['arcs']: t('3 cotes', tag + ' l\'arc fait 6', all(near(a['sw'], ARC, 0.01) for a in E['arcs']), str([a['sw'] for a in E['arcs']]))
    v = E['visage']; t('3 cotes', tag + ' l\'image au centre fait 36', v and near(v[2], VISAGE) and near(v[0] + v[2] / 2, NOYAU_XY[0] + NOYAU / 2), str(v and [round(q, 1) for q in v]))
    for h in E['titres']: t('3 cotes', tag + ' « %s » sur la colonne (x 24)' % h['t'], near(h['box'][0], COL_X), '%.1f' % h['box'][0])
    for i, c in enumerate(E['cartes']):
        t('3 cotes', tag + ' carte %d : 165 × 198 à x %d' % (i + 1, CARTES_X[i % 2]), near(c['box'][2], CARTE[0]) and near(c['box'][3], CARTE[1]) and near(c['box'][0], CARTES_X[i % 2]), str([round(q, 1) for q in c['box']]))
    for i, g in enumerate(E['gestes']):
        b = g['box']; bas = b[1] + b[3]
        t('3 cotes', tag + ' geste « %s » : 167 × 62, entier ou franchement sous le pli' % g['t'], near(b[2], GESTE[0]) and near(b[3], GESTE[1]) and near(b[0], GESTES_X[i]) and (bas <= PLI - MARGE_BAS + 1 or b[1] >= PLI - 1), str([round(q, 1) for q in b]))
    # ── 4 · POLICES ──
    T = E['textes']
    def pol(pred): return [x for x in T if pred(x)]
    for x in pol(lambda x: x['id'] == 'psName'): t('4 polices', tag + ' le nom : Bricolage 700', x['ff'] == 'Bricolage' and x['fw'] == '700', '%s %s' % (x['ff'], x['fw']))
    for x in pol(lambda x: 'closeb' in x['cls']): t('4 polices', tag + ' ✕ Fermer : ApfelMid 500 (composant commun)', x['ff'] == 'ApfelMid' and x['fw'] == '500', '%s %s' % (x['ff'], x['fw']))
    for x in pol(lambda x: 'ps-h' in x['cls']): t('4 polices', tag + ' « %s » : Bricolage 600, capitales' % x['t'], x['ff'] == 'Bricolage' and x['fw'] == '600' and x['tt'] == 'uppercase', '%s %s %s' % (x['ff'], x['fw'], x['tt']))
    for x in pol(lambda x: 'ps-bt' in x['cls']): t('4 polices', tag + ' geste « %s » : Bricolage 700' % x['t'], x['ff'] == 'Bricolage' and x['fw'] == '700', '%s %s' % (x['ff'], x['fw']))
    lg = [x for x in T if x['t'] in LEGENDE and not x['dansCarte']]
    for x in lg: t('4 polices', tag + ' légende « %s » : Bricolage 600' % x['t'], x['ff'] == 'Bricolage' and x['fw'] == '600', '%s %s' % (x['ff'], x['fw']))
    # ── 5 · LES INFRACTIONS DE L'AUDIT — aucune à l'écran, et l'ancienne fiche ne se voit pas ──
    visibles = ' | '.join(x['t'] for x in T).lower()
    for mot in INTERDITS:
        t('5 infractions', tag + ' « %s » n\'est pas à l\'écran' % mot.strip(), mot not in visibles, '')
    for kk, vv in E['vieux'].items():
        t('5 infractions', tag + ' l\'ancien %s ne se voit pas' % kk, (not vv) or (not vv['boite'] and not vv['touche']), str(vv))
    t('5 infractions', tag + ' l\'ombre de dalle animée ne passe plus derrière', E['avant'] == 'none', E['avant'])
    t('5 infractions', tag + ' aucune ligne grise à l\'écran', not E['gris'], str(E['gris'][:3]))
    t('5 infractions', tag + ' le Noyau n\'est jamais seul au centre de l\'écran (§2.9, 58)', E['noyau'] and E['noyau'][2] <= NOYAU + 1, '')
    # ── 6 · LISIBILITÉ ──
    for x in T:
        if x['fs'] < 12: t('6 lisibilité', tag + ' « %s » : %.1f px, sous 12 (§6)' % (x['t'][:24], x['fs']), False)
        if x['op'] < 0.72: t('6 lisibilité', tag + ' « %s » : opacité %.2f, sous 72 %% (§6)' % (x['t'][:24], x['op']), False)
        if x['col'] != x['fill']: t('6 lisibilité', tag + ' « %s » : -webkit-text-fill-color ≠ color (§3)' % x['t'][:24], False)
    t('6 lisibilité', tag + ' %d textes à l\'écran, tous ≥ 12 px, ≥ 72 %%, fill = color' % len(T),
      all(x['fs'] >= 12 and x['op'] >= 0.72 and x['col'] == x['fill'] for x in T), '')
    # ── 7 · les titres de section ──
    titres = [h['t'] for h in E['titres']]
    t('7 libellés', tag + ' « %s » titre la liste %s' % (TITRE_LISTE, 'quand il y a des paroles' if A['titres'] else '— absent sans parole'), (TITRE_LISTE in titres) == bool(A['titres']), str(titres))
    t('7 libellés', tag + ' « %s » %s' % (TITRE_TENUES, 'présent (des paroles tenues)' if A['tenues'] else 'absent (rien de tenu)'), (TITRE_TENUES in titres) == bool(A['tenues']), str(titres))
    t('7 libellés', tag + ' la légende nomme les trois arcs, seulement s\'il y a des arcs', (tuple(E['legende']) == LEGENDE) == bool(A['titres']), str(E['legende']))
    t('7 libellés', tag + ' les deux gestes, et leurs mots', [g['t'] for g in E['gestes']] == list(GESTES), str([g['t'] for g in E['gestes']]))
    return E, A

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        ctx, pg, err = page(b)
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        # la référence de police : les cartes de l'Index, dans CETTE page
        pg.evaluate("()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();else document.getElementById('indexSheet').classList.add('show');}"); pg.wait_for_timeout(1800)
        ip = pg.evaluate(INDEX_POLICES)
        ok = aura_tap(pg, 'Rachel'); t('8 portes', '[%s] la rangée de l\'Aura ouvre la fiche de Rachel, au doigt' % th, ok)
        E, A = juge_fiche(pg, th, 'Rachel', 'Aura')
        tx = pg.evaluate("""()=>[...document.querySelectorAll('#psCadre .s4-carte')].map(k=>{ const f=(s)=>{const e=k.querySelector(s), g=getComputedStyle(e); return g.fontFamily.split(',')[0]+' '+g.fontWeight;}; return {eb:f('.s4-eb'), ti:f('.s4-ti'), et:f('.s4-et')}; })""")
        t('4 polices', '[%s] les cartes de la fiche ont les polices des cartes de l\'Index' % th, ip and all(c == ip for c in tx), 'Index %s · fiche %s' % (ip, tx[:1]))
        # défilée jusqu'au bout : les gestes entiers, 22 du bas
        pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); if(c) c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(500)
        g = pg.evaluate("()=>[...document.querySelectorAll('#psCadre .ps-bt')].map(e=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, r=e.getBoundingClientRect(); return (r.bottom-dv.top)/s;})")
        t('3 cotes', '[%s] défilée jusqu\'au bout : les gestes finissent à 844 − 22' % th, g and all(abs(v - (PLI - MARGE_BAS)) <= 1.5 for v in g), str([round(v, 1) for v in g]))
        im, k = capture(pg); im.save('sauvegardes/audit-fiche-personne/apres/juge-rachel-bas-%s.png' % th)
        # l'état vide — une personne réelle de l'app, sans parole partagée
        pg.evaluate("()=>{ openPerson('Nico'); }"); pg.wait_for_timeout(1300)
        E2, A2 = juge_fiche(pg, th, 'Nico', 'vide')
        t('7 vide', '[%s] l\'état vide : l\'anneau sans arc, aucune section, les deux gestes entiers' % th,
          not E2['arcs'] and not E2['titres'] and len(E2['gestes']) == 2 and all(q['box'][1] + q['box'][3] <= PLI - MARGE_BAS + 1 for q in E2['gestes']), '')
        im, k = capture(pg); im.save('sauvegardes/audit-fiche-personne/apres/juge-nico-%s.png' % th)
        # l'autre porte : le disque d'une personne sur une fiche
        pg.evaluate("()=>{ closeAll(); openDetail(126); }"); pg.wait_for_timeout(1200)
        kr = pg.evaluate("()=>{ const k=[...document.querySelectorAll('.kring[data-p]')].find(e=>e.getAttribute('data-p')==='Rachel'&&e.getBoundingClientRect().width>0); if(!k) return null; const r=k.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if kr: pg.mouse.click(kr[0], kr[1]); pg.wait_for_timeout(1600)
        t('8 portes', '[%s] le disque de Rachel sur une fiche ouvre SA nouvelle fiche, au doigt' % th, kr and pg.evaluate("()=>{const c=document.getElementById('psCadre'); return !!(c&&c.getAttribute('data-fiche')==='Rachel'&&document.getElementById('personSheet').classList.contains('show'));}"), str(kr))
        # ⚑ UNE DALLE TENUE MÈNE À SA FICHE (Tom, 11 sept. : « une dalle est une parole tenue — on doit pouvoir y aller »)
        #   « Tenu ensemble » : toucher une dalle ouvre la fiche de CE Promi ; un glissement n'ouvre rien.
        pg.evaluate("()=>{ closeAll(); openPerson('Rachel'); }"); pg.wait_for_timeout(1500)
        tc = pg.evaluate("""()=>{ const c=[...document.querySelectorAll('#psCadre .ps-c')].find(c=>{ const r=c.getBoundingClientRect(); if(r.height<=0) return false;
            const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return h && c.contains(h); }); if(!c) return null;
            const r=c.getBoundingClientRect(); return {pid:+c.getAttribute('data-pid'), t:(c.querySelector('span')||{}).textContent, x:r.left+r.width/2, y:r.top+r.height/2}; }""")
        FI = "()=>({fiche:document.getElementById('detailPoster').classList.contains('show'), cur:(typeof cur!=='undefined'&&cur)?cur.id:null})"
        if not tc: t('8 portes', '[%s] « Tenu ensemble » : une dalle touchable' % th, False, 'aucune')
        else:
            sc = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().width/390")
            pg.mouse.move(tc['x'], tc['y']); pg.mouse.down(); pg.mouse.move(tc['x'] + 30 * sc, tc['y'], steps=6); pg.mouse.up(); pg.wait_for_timeout(500)
            g1 = pg.evaluate(FI)
            t('8 portes', '[%s] « Tenu ensemble » : un glissement sur « %s » n\'ouvre rien' % (th, tc['t']), not g1['fiche'], str(g1))
            pg.evaluate("()=>{ closeAll(); openPerson('Rachel'); }"); pg.wait_for_timeout(1500)
            pg.mouse.click(tc['x'], tc['y']); pg.wait_for_timeout(1000); g2 = pg.evaluate(FI)
            t('8 portes', '[%s] « Tenu ensemble » : toucher « %s » ouvre SA fiche, au doigt' % (th, tc['t']), g2['fiche'] and g2['cur'] == tc['pid'], 'fiche %s · Promi %s, attendu %s' % (g2['fiche'], g2['cur'], tc['pid']))
        t('8 portes', '[%s] aucune erreur de page' % th, not err, str(err[:2]))
        ctx.close()
    # ── 9 · LES DEUX GESTES, AU DOIGT, jusqu'au Promi planté ──
    for geste, chiche in (('promi', False), ('chiche', True)):
        ctx, pg, err = page(b, has_touch=True); cdp = ctx.new_cdp_session(pg)
        aura_tap(pg, 'Rachel')
        pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); if(c) c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(400)
        bx = pg.evaluate("(g)=>{ const e=document.querySelector('#psCadre .ps-bt[data-geste='+g+']'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }", geste)
        if not bx: t('9 gestes', '[%s] le geste est absent' % geste, False); ctx.close(); continue
        pg.mouse.click(bx[0], bx[1]); pg.wait_for_timeout(1500)
        st = pg.evaluate("""()=>({page:document.getElementById('createSheet').classList.contains('show'), phrase:((document.getElementById('csPhrase')||{}).textContent||'').replace(/\\s+/g,' '),
             qui:[...document.querySelectorAll('#csPhrase [data-ph=qui]')].map(e=>e.textContent.trim()).join(' ')})""")
        t('9 gestes', '[%s] le geste ouvre la page +, et la phrase porte déjà « Rachel »' % geste, st['page'] and 'Rachel' in st['qui'], 'fente « qui » : %r' % st['qui'])
        fe = pg.evaluate("()=>{ const e=document.querySelector('#csPhrase [data-ph=titre]'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if fe: pg.mouse.click(fe[0], fe[1]); pg.wait_for_timeout(350)
        titre = 'essai du juge ' + geste
        pg.keyboard.type(titre, delay=15); pg.wait_for_timeout(300)
        n0 = pg.evaluate("()=>promises.length")
        # le trait : le doigt part du point gauche et passe les deux tiers (le seuil du geste)
        z = pg.evaluate("()=>{ const c=document.getElementById('planterCv'); if(!c) return null; const r=c.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        if z:
            x0, y0 = z[0] + z[2] * 42 / 308, z[1] + z[3] * 52 / 118; x1 = z[0] + z[2] * 250 / 308
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); pg.wait_for_timeout(60)
            for i in range(1, 13):
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * i / 12, 'y': y0 + (i % 3 - 1) * 2}]}); pg.wait_for_timeout(30)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1500)
        nouv = pg.evaluate("(n0)=>promises.slice(n0).map(p=>({t:p.title, who:p.who, chiche:!!p.chiche, etat:p.chicheEtat||null}))", n0)
        bon = [q for q in nouv if q['t'] == titre and q['who'] == 'Rachel' and q['chiche'] == chiche]
        t('9 gestes', '[%s] tracé au doigt : %s planté pour Rachel, sans la ressaisir' % (geste, 'un Chiche lancé' if chiche else 'un Promi'), bool(bon), json.dumps(nouv, ensure_ascii=False))
        t('9 gestes', '[%s] aucune erreur de page' % geste, not err, str(err[:2]))
        ctx.close()
    b.close()

fams = {}
for f, n, ok, d in R: fams.setdefault(f, []).append((n, ok, d))
rates = [(f, n, d) for f, n, ok, d in R if not ok]
for f in sorted(fams):
    k = sum(1 for _, ok, _ in fams[f] if ok); print('%-16s %d/%d' % (f, k, len(fams[f])))
for f, n, d in rates: print('   ❌ %s · %s  %s' % (f, n, d))
print('\n%s' % ('✅  LA FICHE DE LA PERSONNE AU VERT — %d contrôles' % len(R) if not rates else '❌  %d ÉCART(S) sur %d contrôles' % (len(rates), len(R))))
sys.exit(0 if not rates else 1)
