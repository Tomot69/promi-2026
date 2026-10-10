#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_dessin_photo.py — LE DESSIN : DES PHOTOS IMPORTÉES, ET TROIS TAILLES NETTEMENT DIFFÉRENTES (v139, Tom, 9 oct. 2026, C-086).

« Importer une ou plusieurs photos dans le dessin, chacune déplaçable et redimensionnable au pincement, puis posée avec le reste.
Les trois tailles de plume et de gomme doivent être nettement différentes sur la surface : à peu près 2 · 6 · 14 pt pour la plume.
Les trois points du choix le montrent à l'échelle. »
Au vrai doigt (CDP, un et deux doigts), Chromium.
  1 · les tailles décidées (EN DUR) : plume 2 · 6 · 22 (v140 : « le gros pinceau : 22 pt au lieu de 14 »), gomme 8 · 18 · 36 ; les trois points du choix
      sont « plus grands, avec une cible tactile de 44 pt chacun ; les points eux-mêmes grossissent un peu » (v140) : le diamètre du trait + 3 pt ;
  2 · sur la surface, le gros trait couvre au moins quatre fois plus d'encre que le fin (pixels) ;
  3 · le disque PHOTO est dans la rangée, sous le doigt ; sans photo, le toucher ouvre le sélecteur du téléphone ;
  4 · deux photos importées : deux éléments du dessin ; PHOTO choisie, un doigt déplace la photo touchée du geste (± 2 pt),
      deux doigts changent sa taille dans le rapport des doigts (± 5 %), l'autre photo ne bouge pas ; rien n'est tracé ;
  5 · PLUME choisie : tracer sur une photo trace un trait et ne la déplace pas ;
  6 · POSER : les photos sont posées avec le reste, la bande de la fiche les montre (pixels) ;
  7 · ⚑ v140 (Tom, Q435) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_dessin_photo-avant-v140.py) : « un dessin qui contient des photos
      importées part entier, photos comprises. C'est une composition. » Le partage du dessin EMPORTE la photo importée, et le trait ;
  8 · ANNULER retire le dernier élément, photo comprise.
Preuve : sur l'état d'avant (`zz-av139.html`) il rougit.
"""
import sys
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
PHOTO = r"""(c0)=>{ const c=document.createElement('canvas'); c.width=300; c.height=200; const g=c.getContext('2d'); g.fillStyle=c0; g.fillRect(0,0,300,200); return c.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9'); ['tenir','chiche','planter','bande','dessin'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1'));}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} const q=promises.find(p=>p.title==='nager le mardi'); delete q.dessin; openDetail(q.id);}"); pg.wait_for_timeout(2800)
    pg.evaluate("()=>{ window._dessin.ouvre(); }"); pg.wait_for_timeout(900)
    def T(typ, pts): cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': [{'x': x, 'y': y, 'id': i} for i, (x, y) in enumerate(pts)]})
    def tape(sel):
        r = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return [r.left+r.width/2, r.top+r.height/2, !!(h&&(h===e||e.contains(h)))]}", sel)
        if not r: return None
        T('touchStart', [(r[0], r[1])]); pg.wait_for_timeout(50); T('touchEnd', []); pg.wait_for_timeout(450); return r
    S = pg.evaluate("()=>{const r=document.querySelector('#dessinMode .dz-surface').getBoundingClientRect(); return [r.left, r.top, r.width/390]}")
    def P(x, y): return (S[0] + x * S[2], S[1] + y * S[2])
    def trace(y, x0=60, x1=330):
        T('touchStart', [P(x0, y)])
        for i in range(1, 16): T('touchMove', [P(x0 + (x1 - x0) * i / 15.0, y)]); pg.wait_for_timeout(12)
        T('touchEnd', []); pg.wait_for_timeout(300)
    par = pg.evaluate("()=>window._dessinParams ? [window._dessinParams.TAILLES, window._dessinParams.TAILLES_GOMME] : null")
    juge('1 · les tailles décidées : plume 2 · 6 · 22, gomme 8 · 18 · 36', par == [[2, 6, 22], [8, 18, 36]], str(par))
    encre = "()=>{ const c=document.querySelector('#dessinMode .dz-surface canvas'), d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>128) n++; return n; }"
    aires = []; pts_ = None
    for i in range(3):
        for _ in range(3):
            if pg.evaluate("()=>!!document.querySelector('#dessinMode [data-taille]')"): break
            tape('#dessinMode [data-outil="plume"]')
        if i == 0:
            pts_ = pg.evaluate("()=>[].map.call(document.querySelectorAll('#dessinMode .dz-tailles button i'), e=>+e.getBoundingClientRect().width.toFixed(1))")
            cib_ = pg.evaluate("()=>[].map.call(document.querySelectorAll('#dessinMode .dz-tailles button'), e=>{ const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return [+r.width.toFixed(1), +r.height.toFixed(1), !!(h&&(h===e||e.contains(h)))]; })")
        tape('#dessinMode [data-taille="%d"]' % i); n0 = pg.evaluate(encre); trace(120 + 60 * i); aires.append(pg.evaluate(encre) - n0)
    k = S[2]
    juge('1 · les trois points du choix : le diamètre du trait + 3 pt (5 · 9 · 25)', bool(pts_) and len(pts_) == 3 and all(abs(a / k - b_) <= 0.6 for a, b_ in zip(pts_, (5, 9, 25))), str(pts_))
    juge('1 · chaque point a une cible tactile de 44 pt, sous le doigt', bool(cib_) and len(cib_) == 3 and all(c[0] / k >= 43.5 and c[1] / k >= 43.5 and c[2] for c in cib_), str(cib_))
    juge('2 · sur la surface, le gros trait couvre au moins quatre fois plus que le fin', aires[0] > 0 and aires[2] >= 4 * aires[0] and aires[1] >= 2 * aires[0], 'pixels d\'encre : %s' % aires)
    r = tape('#dessinMode [data-outil="photo"]')
    juge('3 · le disque PHOTO est dans la rangée, sous le doigt', bool(r) and r[2], str(r))
    juge('3 · sans photo, le toucher ouvre le sélecteur du téléphone', pg.evaluate("()=>window._dessinImporte||0") == 1 and pg.evaluate("()=>{const i=document.querySelector('#dessinMode input.dz-photo-in'); return !!i && i.multiple && i.accept==='image/*'}"))
    for c0 in ('#E00000', '#00B000'):
        pg.evaluate("(s)=>{ window._dessin.ajoutePhoto(s); }", pg.evaluate(PHOTO, c0)); pg.wait_for_timeout(500)
    ph = lambda: pg.evaluate("()=>window._dessin.photos()")
    A = ph(); n_el = pg.evaluate("()=>window._dessin.etat().traits")
    juge('4 · deux photos importées : deux éléments de plus dans le dessin', len(A) == 2 and n_el == 5, '%d photo(s), %d élément(s)' % (len(A), n_el))
    if len(A) == 2:
        # déplacer la seconde (au-dessus) vers le haut à droite, loin de la première
        x, y = A[1]['x'], A[1]['y']; T('touchStart', [P(x, y)])
        for i in range(1, 11): T('touchMove', [P(x + 8 * i, y - 22 * i)]); pg.wait_for_timeout(15)
        T('touchEnd', []); pg.wait_for_timeout(400); B = ph()
        juge('4 · PHOTO choisie, un doigt déplace la photo touchée du geste (± 2 pt)', abs(B[1]['x'] - x - 80) <= 2 and abs(B[1]['y'] - y + 220) <= 2 and B[0] == A[0], '(%.1f ; %.1f) → (%.1f ; %.1f)' % (x, y, B[1]['x'], B[1]['y']))
        x, y, w = B[0]['x'], B[0]['y'], B[0]['w']
        T('touchStart', [P(x - 30, y)]); T('touchStart', [P(x - 30, y), P(x + 30, y)])
        for i in range(1, 11): T('touchMove', [P(x - 30 - 1.5 * i, y), P(x + 30 + 1.5 * i, y)]); pg.wait_for_timeout(15)
        T('touchEnd', []); pg.wait_for_timeout(400); C = ph()
        juge('4 · deux doigts changent sa taille dans le rapport des doigts (60 → 90 : × 1,5 ± 5 %)', abs(C[0]['w'] / w - 1.5) <= 0.075 and abs(C[0]['x'] - x) <= 2 and C[1] == B[1], 'largeur %.1f → %.1f' % (w, C[0]['w']))
        juge('4 · rien n\'a été tracé pendant ces gestes', pg.evaluate("()=>window._dessin.etat().traits") == 5)
        tape('#dessinMode [data-outil="plume"]'); trace(C[0]['y'], C[0]['x'] - 60, C[0]['x'] + 60); D = ph()
        juge('5 · PLUME choisie : tracer sur une photo trace un trait et ne la déplace pas', pg.evaluate("()=>window._dessin.etat().traits") == 6 and D == C)
        pid = pg.evaluate("()=>cur.id"); tape('#dessinMode [data-outil="poser"]'); pg.wait_for_timeout(1200)
        d = pg.evaluate("()=>{ const d=cur.dessin; return d ? {poses:(d.poses||[]).length, imgs:(d.poses||[]).filter(t=>t.img).length} : null; }")
        juge('6 · POSER : les photos sont posées avec le reste', bool(d) and d['poses'] == 6 and d['imgs'] == 2, str(d))
        px = pg.evaluate("([x,y])=>{ const c=document.querySelector('#detailPoster canvas.dz-bande'); if(!c) return null; const r=c.getBoundingClientRect(), k=c.width/r.width; const q=c.getContext('2d').getImageData(Math.round(x*k*r.width/390), Math.round(y*k*r.width/390),1,1).data; return [q[0],q[1],q[2]]; }", [D[1]['x'] + 20, D[1]['y'] + 20])
        juge('6 · la bande de la fiche montre la photo posée (pixels)', bool(px) and px[1] > 130 and px[0] < 90, str(px))
        comp = pg.evaluate("([id,x,y,tx,ty])=>{ const S=window._dessinPartage({ids:[id]}); if(!S) return null; const g=S.cv.getContext('2d'), k=S.cv.width/390; const a=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data, t=g.getImageData(Math.round(tx*k),Math.round(ty*k),1,1).data; return {photo:[a[0],a[1],a[2]], trait:[t[0],t[1],t[2]], fond:S.fond}; }", [pid, D[1]['x'] + 20, D[1]['y'] + 20, 200, 240])
        juge('7 · le partage du dessin emporte la photo importée (une composition), et le trait', bool(comp) and (comp['photo'][1] > 130 and comp['photo'][0] < 90) and sum(comp['trait']) < 200, str(comp))
        pg.evaluate("()=>{ window._dessin.ouvre(); }"); pg.wait_for_timeout(700); tape('#dessinMode [data-outil="annuler"]'); tape('#dessinMode [data-outil="annuler"]')
        juge('8 · ANNULER retire le dernier élément, photo comprise', pg.evaluate("()=>window._dessin.etat().traits") == 4 and len(ph()) == 1, '%d élément(s), %d photo(s)' % (pg.evaluate("()=>window._dessin.etat().traits"), len(ph())))
    juge('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:12]))
sys.exit(1 if ko else 0)
