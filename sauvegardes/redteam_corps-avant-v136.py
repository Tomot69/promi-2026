#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_corps.py — LE CORPS DE LA PELOTE (v123, Tom, 3 oct. 2026). WebKit.

« Le corps : l'intérieur et la surface de la Pelote, sous les poils, prennent une autre teinte de la palette choisie au Studio. Jamais
celle des poils. Tirée au hasard parmi les teintes de la palette, à chaque ouverture, comme les poils. ΔE00 ≥ 15 entre le corps et la
teinte dominante des poils, et jamais de kaki (si la teinte tirée est kaki, on tire la suivante). Juge : sur 50 ouvertures et quatre
palettes, le corps n'a jamais la teinte des poils, et l'écart et la règle du kaki sont toujours tenus. »

Valeurs EN DUR (§7) : l'écart 15 (ΔE00) ; le kaki de v115 : OKLCH h 78–140°, C 0,015–0,10, L 0,20–0,80. Quatre palettes : Ingénu
(`signal`), Candide, Irascible, Taciturne. 50 ouvertures par palette, les deux thèmes alternés.
LE VERDICT VIENT DE CE QUI EST PEINT (§7), pas de ce que l'app déclare :
  · le CORPS = la couleur de la peau pleine que le peintre pose sous les poils (le calque opaque `__po` du canevas `#auBoule`, celui que
    `redteam_plein` juge) — sa médiane ;
  · le POIL = la teinte dominante de la fourrure : la couleur moyenne de la rampe de velours du sol (`PeloteMoteur.rampeVelours`), la
    rampe que le peintre emploie ; et, relue sur l'image, la MARCHE de cette rampe la plus peinte (parmi les pixels plus proches d'une
    marche que du corps — le bac brut le plus fréquent est un mélange poil + corps, il ne dit pas la teinte du poil). Sur une version
    sans `_aura.corps`, le bac brut.
Contrôles, par palette :
  1 · ΔE00(corps, poil) ≥ 15 à chaque ouverture (face à la rampe ET face au bac dominant de l'image) ;
  2 · le corps n'est jamais kaki ;
  3 · le corps n'a jamais la teinte des poils : ce n'est pas le ton de palette du sol (ni le plus proche des tons de la palette) ;
  4 · le tirage est un hasard : sur 50 ouvertures, au moins deux tons de corps différents (pour un même sol, quand la palette le permet).
Preuve (§7) : sur `sauvegardes/app-avant-v123.html` il ROUGIT (la peau y est la moyenne assombrie de son poil).
"""
import os, sys, math
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 50))
PALETTES = ['signal', 'candide', 'irascible', 'taciturne']
ECART = 15.0
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-86s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


def lin(v):
    v /= 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def lab(c):
    r, g, b = lin(c[0]), lin(c[1]), lin(c[2])
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047; y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b; z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def dE00(c1, c2):
    L1, a1, b1 = lab(c1); L2, a2, b2 = lab(c2); R = math.pi / 180
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2); Cb = (C1 + C2) / 2; G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    ap1 = (1 + G) * a1; ap2 = (1 + G) * a2; Cp1 = math.hypot(ap1, b1); Cp2 = math.hypot(ap2, b2)
    h1 = (math.degrees(math.atan2(b1, ap1)) + 360) % 360; h2 = (math.degrees(math.atan2(b2, ap2)) + 360) % 360
    dL = L2 - L1; dC = Cp2 - Cp1; dh = h2 - h1
    if Cp1 * Cp2 == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dH = 2 * math.sqrt(Cp1 * Cp2) * math.sin(dh * R / 2); Lb = (L1 + L2) / 2; Cpb = (Cp1 + Cp2) / 2; hb = h1 + h2
    if Cp1 * Cp2 != 0: hb = (h1 + h2) / 2 if abs(h1 - h2) <= 180 else ((h1 + h2 + 360) / 2 if h1 + h2 < 360 else (h1 + h2 - 360) / 2)
    T = 1 - 0.17 * math.cos((hb - 30) * R) + 0.24 * math.cos(2 * hb * R) + 0.32 * math.cos((3 * hb + 6) * R) - 0.20 * math.cos((4 * hb - 63) * R)
    Sl = 1 + 0.015 * (Lb - 50) ** 2 / math.sqrt(20 + (Lb - 50) ** 2); Sc = 1 + 0.045 * Cpb; Sh = 1 + 0.015 * Cpb * T
    Rt = -2 * math.sqrt(Cpb ** 7 / (Cpb ** 7 + 25 ** 7)) * math.sin(60 * R * math.exp(-((hb - 275) / 25) ** 2))
    return math.sqrt((dL / Sl) ** 2 + (dC / Sc) ** 2 + (dH / Sh) ** 2 + Rt * (dC / Sc) * (dH / Sh))


def oklch(c):
    r, g, b = lin(c[0]), lin(c[1]), lin(c[2])
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3); m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3); s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s; a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s; bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), (math.degrees(math.atan2(bb, a)) + 360) % 360


def kaki(c):
    L, C, h = oklch(c); return 78 <= h <= 140 and 0.015 <= C <= 0.10 and 0.20 <= L <= 0.80


# ce qui est PEINT : la peau pleine (`__po`), le bac dominant de la fourrure, la rampe de velours du sol, la palette
LIT = r"""()=>{ const cv=document.getElementById('auBoule'); if(!cv||!cv.width||!cv.__po||!cv.__po.width) return null;
  const pg=cv.__po.getContext('2d'), pd=pg.getImageData(0,0,cv.__po.width,cv.__po.height).data, R=[],G=[],B=[];
  for(let i=0;i<pd.length;i+=4){ if(pd[i+3]>250){ R.push(pd[i]); G.push(pd[i+1]); B.push(pd[i+2]); } }
  if(!R.length) return null; const med=a=>{a.sort((x,y)=>x-y); return a[a.length>>1]};
  const W=cv.width, d=cv.getContext('2d').getImageData(0,0,W,W).data, h={}; let n=0;
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const i=(y*W+x)*4; if(d[i+3]<250) continue; if(Math.hypot(x-W/2,y-W/2)>W*0.33) continue; n++;
    const k=(d[i]>>4)+','+(d[i+1]>>4)+','+(d[i+2]>>4); const o=h[k]||(h[k]=[0,0,0,0]); o[0]++; o[1]+=d[i]; o[2]+=d[i+1]; o[3]+=d[i+2]; }
  const top=Object.values(h).sort((a,b)=>b[0]-a[0])[0];
  let sol=null, ramp=null; try{ const s=_aura.sol(); sol=s.idx; }catch(e){}
  let eff=null; try{ eff=(_aura.corps&&_aura.corps().poil)||null; }catch(e){}
  const pal=Toile.cols().map(c=>[c[0]|0,c[1]|0,c[2]|0]);
  /* la rampe de velours du sol EFFECTIF : sans `_aura.corps` (version d'avant), on la déduit du bac dominant */
  let dom=[top[1]/top[0],top[2]/top[0],top[3]/top[0]];
  try{ const base=eff||dom; const RV=PeloteMoteur.rampeVelours(base); let a=[0,0,0]; RV.forEach(c=>{a[0]+=c[0];a[1]+=c[1];a[2]+=c[2]}); ramp=a.map(v=>v/RV.length);
    /* ⚠ le bac le plus fréquent de l'image est un MÉLANGE : le corps se voit entre les poils (mesuré : il tombait à ΔE00 10 du corps).
       La teinte dominante des POILS = la marche de la rampe de velours la plus peinte, parmi les pixels plus proches d'une marche que du corps. */
    if(eff){ const C=[med(R.slice()),med(G.slice()),med(B.slice())], cnt=RV.map(()=>0), d2=(p,q)=>(p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2;
      for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const i=(y*W+x)*4; if(d[i+3]<250) continue; if(Math.hypot(x-W/2,y-W/2)>W*0.33) continue; const p=[d[i],d[i+1],d[i+2]];
        let bi=0, bd=1e9; for(let k=0;k<RV.length;k++){ const e=d2(p,RV[k]); if(e<bd){ bd=e; bi=k; } } if(bd<d2(p,C)) cnt[bi]++; }
      let bk=0; for(let k=1;k<cnt.length;k++) if(cnt[k]>cnt[bk]) bk=k; dom=[RV[bk][0],RV[bk][1],RV[bk][2]]; } }catch(e){}
  /* v125 : la teinte du halo — la couleur que porte son canevas (elle est la même sur tous ses pixels) */
  let halo=null; try{ const h=document.getElementById('auPeloteHalo'), hd=h.getContext('2d').getImageData(0,(h.height/2)|0,h.width,1).data; let am=0; for(let i=0;i<hd.length;i+=4){ if(hd[i+3]>am){ am=hd[i+3]; halo=[hd[i],hd[i+1],hd[i+2]]; } } if(am<24) halo=null;   /* le pixel le plus opaque : à faible alpha la couleur relue est quantifiée */ }catch(e){}
  return {halo:halo, corps:[med(R),med(G),med(B)], dom:dom, part:top[0]/n, sol:sol, ramp:ramp, pal:pal,
          decl:(()=>{try{return _aura.corps?_aura.corps():null}catch(e){return null}})(), peint:cv.__peints||null}; }"""

with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','2')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(APP); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for pal in PALETTES:
        pires = {'ramp': 999, 'dom': 999}; n_kaki = 0; n_meme = 0; n_lu = 0; corps_vus = {}; ex = ''; halo_ko = 0; ex_h = ''; suite_ko = 0; ex_s = ''; avant = None
        for i in range(N):
            th = 'light' if i % 2 == 0 else 'dark'
            pg.evaluate("([t,p])=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); setTheme(t); try{Toile.setPalette(p)}catch(e){} }", [th, pal]); pg.wait_for_timeout(350)
            pg.evaluate("()=>{ document.querySelectorAll('.screen.show').forEach(s=>{ if(s.id!=='auraScreen'&&s.id!=='studioScreen') s.classList.remove('show'); }); document.getElementById('souffleBtn').click(); }")
            m = None
            for _ in range(40):
                pg.wait_for_timeout(350)
                pg.evaluate("()=>{ try{ _aura.pelote(); }catch(e){} }")
                m = pg.evaluate(LIT)
                if m: break
            if not m: continue
            n_lu += 1; c = m['corps']
            e1 = dE00(c, m['ramp']) if m['ramp'] else 0; e2 = dE00(c, m['dom'])
            if e1 < pires['ramp']: pires['ramp'] = e1; ex = 'ouverture %d [%s] corps %s · poil (rampe) %s · sol n° %s' % (i + 1, th, [round(v) for v in c], [round(v) for v in m['ramp']], m['sol'])
            pires['dom'] = min(pires['dom'], e2)
            if kaki(c): n_kaki += 1
            # la teinte des poils : le ton de palette du sol — le corps n'en vient pas (le ton de palette le plus proche du corps n'est pas le sol)
            proche = min(range(len(m['pal'])), key=lambda k: dE00(c, m['pal'][k]))
            if m['sol'] is not None and (proche == m['sol'] or dE00(c, m['pal'][m['sol']]) < 5): n_meme += 1
            corps_vus.setdefault(m['sol'], set()).add(tuple(round(v / 6) for v in c))
            # ⚑ v125 (Tom) — « le halo prend la couleur du corps » : sa teinte OKLCH est celle du corps (à 8° près ; sa clarté peut s'écarter
            #   du fond pour faire une lumière). Et d'une ouverture à l'autre, ni le même sol ni le même corps (redteam d'avant : rien ne l'interdisait).
            if i < 20:
                h = m.get('halo'); oc = oklch(c); oh = oklch(h) if h else None
                if not h or not (abs((oh[2] - oc[2] + 180) % 360 - 180) <= 8 or oc[1] < 0.03 or oh[1] < 0.02):
                    halo_ko += 1; ex_h = 'ouverture %d [%s] halo %s · corps %s' % (i + 1, th, h, [round(v) for v in c])
            d = m.get('decl') or {}
            ici = (d.get('solIdx'), d.get('idx'))
            if avant is not None and len(m['pal']) > 2 and (ici[0] == avant[0] or (ici[1] == avant[1] and ici[1] is not None and ici[1] >= 0)):
                suite_ko += 1; ex_s = 'ouverture %d : sol %s corps %s après sol %s corps %s' % (i + 1, ici[0], ici[1], avant[0], avant[1])
            avant = ici
        t('[%s] les %d ouvertures sont lues (la peau pleine est peinte)' % (pal, N), n_lu == N, '%d lues' % n_lu)
        t('1 · [%s] ΔE00(corps, poil) ≥ 15 à chaque ouverture — face à la rampe de velours' % pal, n_lu > 0 and pires['ramp'] >= ECART, 'le pire : %.1f · %s' % (pires['ramp'], ex))
        t('1 · [%s] ΔE00(corps, poil) ≥ 15 — face à la couleur dominante lue sur la fourrure' % pal, n_lu > 0 and pires['dom'] >= ECART, 'le pire : %.1f' % pires['dom'])
        t('2 · [%s] le corps n\'est jamais kaki' % pal, n_lu > 0 and n_kaki == 0, '%d ouverture(s) kaki' % n_kaki)
        t('3 · [%s] le corps n\'a jamais la teinte des poils' % pal, n_lu > 0 and n_meme == 0, '%d ouverture(s) où le corps est le ton du sol' % n_meme)
        t('5 · [%s] v125 : la teinte du halo est celle du corps (vingt ouvertures)' % pal, n_lu > 0 and halo_ko == 0, '%d ouverture(s) · %s' % (halo_ko, ex_h))
        t('6 · [%s] v125 : jamais le même sol ni le même corps deux ouvertures de suite' % pal, n_lu > 0 and suite_ko == 0, '%d fois · %s' % (suite_ko, ex_s))
        t('4 · [%s] le corps se tire au hasard (au moins deux corps différents sur %d ouvertures)' % (pal, N), len(set().union(*corps_vus.values())) >= 2 if corps_vus else False, '%s' % {k: len(v) for k, v in corps_vus.items()})
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:8]))
sys.exit(1 if ko else 0)
