#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_origine.py — LA DALLE D'ORIGINE DANS LA BANDE HAUTE D'UNE FICHE (v118, Tom, Q365 tranchée, 2 oct. 2026).

« Avec La dalle d'origine, la bande haute de la fiche prend la couleur d'origine, sauf si elle passe sous le seuil de
redteam_tonsurton face au champ. Dans ce cas seulement, la rampe de Q30 s'applique. »

Le seuil est écrit EN DUR ici (§7) : ΔE 15, CIELAB — celui de redteam_tonsurton. Pour un Promi et un Chiche, sous cinq palettes
de plantation (dont Ingénu, où la dalle a la couleur même du champ), l'option prise :
  1 · le juge rend LUI-MÊME la dalle dans son monde de plantation et mesure son écart au champ (pixels, pas la valeur de l'app) ;
  2 · il lit ce que la fiche a PEINT dans la zone de matière (les pixels du canevas, hors champ) ;
  3 · écart ≥ 15 → la fiche doit porter la couleur d'ORIGINE (plus proche de l'origine que de la rampe) : il rougit si la
      rampe s'applique alors que la couleur d'origine passerait ;
  4 · écart < 15 → la fiche doit porter la RAMPE de Q30 ;
  5 · dans tous les cas, la matière peinte se lit sur son champ (ΔE ≥ 15, et elle occupe sa place) : il rougit si une dalle
      d'origine produit du ton sur ton.
Les cas à moins de 2 du seuil ne sont pas jugés sur 3/4 (deux mesures d'une matière qui respire peuvent tomber de part et
d'autre) ; ils restent jugés sur 5.
Preuves (§7) :
  · `APP=http://127.0.0.1:8752/<copie de sauvegardes/app-avant-v118.html à la racine> python3 redteam_origine.py` ROUGIT
    (la rampe s'y applique toujours) ;
  · `python3 redteam_origine.py --sonde` force la couleur d'origine sans garde → il ROUGIT sur Ingénu (ton sur ton).
"""
import os, sys, math
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
SEUIL = 15.0          # ΔE CIELAB — la décision (redteam_tonsurton, Q216)
MARGE = 2.0
CHAMPS = {'promi': (130, 174, 248), 'chiche': (255, 184, 210)}     # les natures, en dur (§3)
PALETTES = ['signal', 'irascible', 'primesautier', 'taciturne', 'truculent']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-66s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-66s KO  %s' % (nom, detail))


def lab(c):
    def lin(v):
        v /= 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = lin(c[0]), lin(c[1]), lin(c[2])
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047; y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))


def dE(a, b):
    A, B = lab(a), lab(b); return math.sqrt(sum((A[i] - B[i]) ** 2 for i in range(3)))


# la dalle rendue par le moteur, moyenne des pixels opaques : dans son monde de plantation, puis sous la rampe de Q30
REF = r"""([id, nat])=>{ const p=promises.find(q=>q.id===id);
  function moy(opts){ const c=document.createElement('canvas'); if(!Toile.dalleTrame(c, id, 2, p.monde, opts)||!c.width) return null;
    const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0,r=0,g=0,b=0;
    for(let i=0;i<d.length;i+=4) if(d[i+3]>200){ n++; r+=d[i]; g+=d[i+1]; b+=d[i+2]; } return n?[r/n,g/n,b/n,n/(c.width*c.height)]:null; }
  return {orig:moy(undefined), rampe:moy({rampe:window._ppRampe(nat)})}; }"""

# ce que la fiche a peint : le champ (au coin du canevas) et la matière (les pixels de sa zone qui ne sont pas le champ)
FICHE = r"""()=>{ const cv=document.getElementById('dpTrameCv'); if(!cv||!cv.width) return null; const g=cv.getContext('2d');
  const k=cv.width/390, m=(cv.getAttribute('data-matiere')||'').split(',').map(Number); if(m.length<4) return {sans:1};
  const ch=g.getImageData(Math.round(4*k),Math.round(4*k),1,1).data;
  const x=Math.round(m[0]*k), y=Math.round(m[1]*k), w=Math.round(m[2]*k), h=Math.round(m[3]*k), d=g.getImageData(x,y,w,h).data;
  let n=0,r=0,gg=0,b=0; for(let i=0;i<d.length;i+=4){ if(Math.abs(d[i]-ch[0])+Math.abs(d[i+1]-ch[1])+Math.abs(d[i+2]-ch[2])>10){ n++; r+=d[i]; gg+=d[i+1]; b+=d[i+2]; } }
  return {champ:[ch[0],ch[1],ch[2]], mat:n?[r/n,gg/n,b/n]:null, part:n/(w*h), decl:cv.getAttribute('data-origine'), rect:m}; }"""


def passe(b, moteur, sonde):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setTheme('light')}catch(e){}}")
    if sonde:
        pg.evaluate("()=>{ window._origineBande=function(p){ return (p&&p.dalleOrigine)?{dE:99, origine:true}:null; }; }")
        print('SONDE : la couleur d\'origine est forcée, sans garde de ton sur ton')
    ids = pg.evaluate("""()=>({promi:(promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.photo&&!q.chiche&&q.status!=='tenu')||{}).id,
                              chiche:(promises.find(q=>q.chiche&&!q.draft&&!q.photo&&q.status!=='tenu')||{}).id})""")
    for nat, pid in ids.items():
        if pid is None: t('[%s] une fiche %s existe' % (moteur, nat), False); continue
        for pal in PALETTES:
            tag = '[%s] %s · %s' % (moteur, nat, pal)
            pg.evaluate("([id,pal])=>{ closeAll(); const p=promises.find(q=>q.id===id); p.__av=p.__av||{m:p.monde,o:p.dalleOrigine}; p.monde={m:'encre',p:pal,h:0}; p.dalleOrigine=true; openDetail(id); }", [pid, pal])
            pg.wait_for_timeout(1500)
            ref = pg.evaluate(REF, [pid, nat]); f = pg.evaluate(FICHE)
            if not ref or not ref.get('orig') or not f or not f.get('champ'): t(tag + ' · mesurable', False, str(f)[:120]); continue
            champ = f['champ']; d0 = dE(ref['orig'], CHAMPS[nat])
            t(tag + ' · le champ est celui de la nature', dE(champ, CHAMPS[nat]) < 3, str(champ))
            if not f['mat'] or f['part'] < 0.5 * ref['orig'][3] * 0.5:
                t(tag + ' · la matière se lit sur son champ', False, 'TON SUR TON : %.1f %% de la zone se distingue du champ (origine à ΔE %.1f)' % (100 * f['part'], d0)); continue
            dm = dE(f['mat'], champ); do = dE(f['mat'], ref['orig']); dr = dE(f['mat'], ref['rampe'])
            t(tag + ' · la matière se lit sur son champ (ΔE ≥ 15)', dm >= SEUIL, 'ΔE %.1f' % dm)
            if abs(d0 - SEUIL) < MARGE: print('%-66s —   au seuil (origine à ΔE %.1f) : non jugé sur la branche' % (tag, d0)); continue
            if d0 >= SEUIL: t(tag + ' · origine à ΔE %.1f → la couleur d\'ORIGINE' % d0, do < dr and do < 8, 'à l\'origine %.1f · à la rampe %.1f · app : %s' % (do, dr, f['decl']))
            else: t(tag + ' · origine à ΔE %.1f → la RAMPE de Q30' % d0, dr < do and dr < 8, 'à la rampe %.1f · à l\'origine %.1f · app : %s' % (dr, do, f['decl']))
        pg.evaluate("(id)=>{ closeAll(); const p=promises.find(q=>q.id===id); if(p&&p.__av){ p.monde=p.__av.m; p.dalleOrigine=p.__av.o; delete p.__av; } }", pid)
    # sans l'option : la rampe de Q30, comme avant
    if ids.get('promi') is not None:
        pg.evaluate("(id)=>{ closeAll(); const p=promises.find(q=>q.id===id); p.dalleOrigine=false; openDetail(id); }", ids['promi']); pg.wait_for_timeout(1400)
        ref = pg.evaluate(REF, [ids['promi'], 'promi']); f = pg.evaluate(FICHE)
        t('[%s] sans l\'option, la bande garde la rampe de Q30' % moteur, bool(f and f.get('mat')) and dE(f['mat'], ref['rampe']) < 8, str(f.get('decl') if f else None))
    t('[%s] aucune erreur de page' % moteur, not er, '; '.join(er[:2]))
    ctx.close()


with sync_playwright() as p:
    sonde = '--sonde' in sys.argv
    for moteur in ('webkit', 'chromium'):
        b = getattr(p, moteur).launch(); passe(b, moteur, sonde); b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:8]))
sys.exit(1 if ko else 0)
