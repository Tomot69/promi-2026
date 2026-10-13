#!/usr/bin/env python3
"""v145 (C-118, C-094) — la matière des deux pages de variantes, prise sur l'app réelle (banc_tom, WebKit @3x) :
  variantes/dalle-<nature>-<thème>.png      la vraie dalle du moteur, rendue à 228 × 190 pt @3x, teinte comme la bande d'une fiche
  variantes/accueil-<thème>.png             l'accueil au repos, Toile de 25 paroles
  variantes/accueil-<thème>-flou1|2|3.jpg   le même, flouté à 2,4 · 4,8 · 9,6 pt (un flou gaussien, comme `blur()` en CSS)"""
import sys, io, base64, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter
import banc_tom as B
quoi = sys.argv[1:] or ['dalles', 'accueil']
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        th = 'sombre' if sombre else 'clair'
        if 'dalles' in quoi:
            ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx)
            B.plante_doigt(pg, 'rendre le livre', 'moi', 0); B.plante_doigt(pg, 'écrire à Lou', 'Rachel', 0); B.plante_doigt(pg, 'le grand plongeoir', 'moi', 1); B.plante_doigt(pg, 'arroser le ficus', 'moi', 0)
            P = pg.evaluate("()=>promises.map(p=>({id:p.id,title:p.title}))")
            for nat, titre in (('promi', 'écrire à Lou'), ('chiche', 'le grand plongeoir')):
                pid = [x for x in P if x['title'] == titre][0]['id']
                pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(900); pg.evaluate("id=>{ openDetail(id); }", pid); pg.wait_for_timeout(3000)
                d = pg.evaluate("([pid,nat])=>{ var o=window._ppRampe?{rampe:window._ppRampe(nat)}:undefined, c=window._rendDalle(pid, 228*3, 190*3, o, true), cv=c&&(c.cv||c.canvas||c); return cv&&cv.toDataURL?[cv.toDataURL('image/png'), cv.width, cv.height]:null; }", [pid, nat])
                if d:
                    io.open('variantes/dalle-%s-%s.png' % (nat, th), 'wb').write(base64.b64decode(d[0].split(',')[1])); print('dalle', nat, th, d[1], '×', d[2], flush=True)
            ctx.close()
        if 'accueil' in quoi:
            ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, attente=9000)
            geo = pg.evaluate("""()=>{ var d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, o={};
              ['studioBtn','souffleBtn','createBtn','filBtn'].forEach(function(id){ var e=document.getElementById(id); if(!e) return; var r=e.getBoundingClientRect(); o[id]=[+((r.left-d.left)/k).toFixed(1), +((r.top-d.top)/k).toFixed(1), +(r.width/k).toFixed(1), +(r.height/k).toFixed(1)]; });
              var b=document.querySelector('.acc-barre'); if(b){ var r=b.getBoundingClientRect(); o.barre=[+((r.left-d.left)/k).toFixed(1), +((r.top-d.top)/k).toFixed(1), +(r.width/k).toFixed(1), +(r.height/k).toFixed(1)]; }
              var s=document.getElementById('studioBtn'); if(s){ var L=[].slice.call(s.querySelectorAll('*')).concat([s]).map(function(e){ var q=e.getBoundingClientRect(); return [q.left,q.top,q.right,q.bottom,q.width]; }).filter(function(q){ return q[4]>2; });
                o.studioVu=[+((Math.min.apply(0,L.map(q=>q[0]))-d.left)/k).toFixed(1), +((Math.min.apply(0,L.map(q=>q[1]))-d.top)/k).toFixed(1), +((Math.max.apply(0,L.map(q=>q[2]))-d.left)/k).toFixed(1), +((Math.max.apply(0,L.map(q=>q[3]))-d.top)/k).toFixed(1)]; }
              return o; }""")
            # le rappel « Garder ta Toile » n'est pas à l'écran à la fin du premier parcours : on le retire de l'image de fond
            pg.evaluate("()=>{ var r=document.getElementById('accRappel'); if(r) r.style.setProperty('display','none','important'); }"); pg.wait_for_timeout(400)
            print('accueil', th, json.dumps(geo), flush=True)
            im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); im.save('variantes/accueil-%s.png' % th, optimize=True)
            petit = im.resize((390, 844), Image.LANCZOS)
            for i, s in enumerate((2.4, 4.8, 9.6)): petit.filter(ImageFilter.GaussianBlur(radius=s)).save('variantes/accueil-%s-flou%d.jpg' % (th, i + 1), quality=92)
            ctx.close()
    b.close()
