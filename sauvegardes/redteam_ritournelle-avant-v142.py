#!/usr/bin/env python3
"""
redteam_ritournelle.py — RITOURNELLE, LE ZOOM DE DÉPART (v141, Tom, 10 oct. 2026 — C-088, RÉCIDIVE : « trop dézoomé »).

LES CIBLES, EN DUR (§7), sur un écran de 390 pt de large :
  · une parole    → sa dalle fait au moins 60 % de la largeur (234 pt), entière ;
  · deux, trois, quatre paroles → toutes entières à l'écran (entre le plateau et la barre) ;
  · jusqu'à quatre paroles → au plus DEUX cellules vides entièrement visibles.
« Entière » et la largeur se jugent sur ce qui est PEINT (sous Ingénu, seules les dalles des paroles portent le bleu Promi ou le rose Chiche).
Une cellule vide est « entièrement visible » quand toute sa cellule est à l'écran et qu'elle ne passe ni sous le plateau ni sous la barre.
WebKit (le moteur de l'iPhone). Les paroles sont plantées UNE À UNE sur une Toile vide, comme un vrai départ ; trois départs pour une parole.
Preuve : rouge sur l'état d'avant (python3 redteam_ritournelle.py zz-av141.html).
"""
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
LARGEUR_MIN = 0.60 * 390; VIDES_MAX = 2
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
CEL = """()=>{ if(!window.Toile_lecture) return null; const L=Toile_lecture(), v=L.vue, G=L.graines; const st={};
  for(let y=1;y<L.H;y+=2) for(let x=1;x<L.W;x+=2){ let bd=1e18,bk=-1; for(let k=0;k<G.length;k++){ const d=Math.hypot(x-G[k].x,y-G[k].y)-G[k].w; if(d<bd){bd=d;bk=k;} }
    const sx=x*v.s+v.ox, sy=y*v.s+v.oy; const o=st[bk]=st[bk]||{de:0,ch:0}; if(sx<0||sx>L.W||sy<0||sy>L.H) o.de++; else if(sx>=24&&sx<=366&&((sy>=40&&sy<=100)||(sy>=710&&sy<=810))) o.ch++; }
  let vides=0; for(const k in st){ if(G[k].kind==='gray' && st[k].de===0 && st[k].ch===0) vides++; }
  return {s:v.s, vides:vides, paroles:G.filter(g=>g.kind!=='gray').length}; }"""
def dalle(c): return (abs(c[0]-130) < 26 and abs(c[1]-174) < 26 and abs(c[2]-248) < 26) or (abs(c[0]-255) < 22 and abs(c[1]-184) < 24 and abs(c[2]-210) < 26)
def depart(b, n):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=1, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6000)
    pg.evaluate("(n)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} var L=promises.filter(p=>!p.nuee&&!p.draft).slice(0,n); promises.length=0; L.forEach(p=>promises.push(p)); try{for(var k in NUE){ if(k!=='soi') delete NUE[k]; }}catch(e){} Toile.setTheme('ritournelle'); Toile.sync([]); }", n); pg.wait_for_timeout(1200)
    for k in range(1, n + 1): pg.evaluate("(k)=>{ Toile.sync(promises.slice(0,k).map(p=>p.id)); }", k); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ try{Toile_recadre()}catch(e){} }"); pg.wait_for_timeout(4500)
    o = pg.evaluate(CEL)
    r = pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
    im = Image.open(io.BytesIO(pg.screenshot(clip={'x': r[0], 'y': r[1], 'width': r[2], 'height': r[3]}))).convert('RGB').resize((390, 844)); px = im.load()
    xs = []; ys = []
    for y in range(104, 706, 2):
        for x in range(0, 390, 2):
            if dalle(px[x, y]): xs.append(x); ys.append(y)
    ctx.close()
    return o, ([min(xs), max(xs), min(ys), max(ys)] if xs else None)
with sync_playwright() as p:
    b = p.webkit.launch()
    for essai in range(3):
        o, bo = depart(b, 1); w = (bo[1] - bo[0]) if bo else 0
        juge('une parole (départ %d) : sa dalle fait au moins 60 %% de la largeur (≥ 234 pt), entière' % (essai + 1), bool(bo) and w >= LARGEUR_MIN and bo[0] >= 4 and bo[1] <= 385 and bo[2] > 104 and bo[3] < 704, 'largeur peinte %d pt (%.0f %%) · boîte %s · zoom %s' % (w, w / 3.9, bo, o and round(o['s'], 2)))
        juge('une parole (départ %d) : au plus deux cellules vides entièrement visibles' % (essai + 1), o is not None and o['vides'] <= VIDES_MAX, 'non mesurable (pas de lecture du moteur)' if o is None else '%d cellule(s) vide(s) entière(s)' % o['vides'])
    for n in (2, 3, 4):
        o, bo = depart(b, n)
        juge('%d paroles : toutes entières à l\'écran, entre le plateau et la barre' % n, bool(bo) and bo[0] >= 4 and bo[1] <= 385 and bo[2] > 104 and bo[3] < 704 and (bo[1] - bo[0]) >= 200, 'la matière des paroles tient dans %s · zoom %s' % (bo, o and round(o['s'], 2)))
        juge('%d paroles : au plus deux cellules vides entièrement visibles' % n, o is not None and o['vides'] <= VIDES_MAX, 'non mesurable (pas de lecture du moteur)' if o is None else '%d cellule(s) vide(s) entière(s)' % o['vides'])
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
