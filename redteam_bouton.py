#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_bouton.py — « PARTAGER MA PELOTE » : PROMILATE, ET UNE COULEUR DE LA PALETTE (v124, Tom, 3 oct. 2026). WebKit.

« Le texte passe en PromiLate, en capitales et sans capitale accentuée : « PARTAGER MA PELOTE ». Hauteur de capitale identique à celle de
« TRACE POUR LANCER ». Le bouton garde sa grammaire, seul le texte change. Sa couleur est tirée au hasard dans la palette choisie au
Studio, à chaque ouverture de l'Aura. Elle n'est jamais celle des poils ni celle du corps de la Pelote, à cette même ouverture. Seules
les teintes assez contrastées avec le fond peuvent être tirées : ≥ 3:1. Si aucune ne l'est, le texte prend l'encre du mode. Jamais de
kaki. Juge : sur 50 ouvertures et quatre palettes, dans les deux thèmes, trois teintes toujours distinctes (poils, corps, texte),
contraste et règle du kaki toujours tenus. »

Valeurs EN DUR (§7) : le mot « PARTAGER MA PELOTE » ; PromiLate 15 px, chasse 0 (les phrases du trait) ; la grammaire du bouton 342 × 60,
trait 2, rayon 30 ; contraste 3:1 ; le kaki de v115 ; l'encre du mode #201908 (clair) / #F7F0DE (sombre).
Quatre palettes (Ingénu, Candide, Irascible, Taciturne), 50 ouvertures chacune, les deux thèmes alternés (25 + 25).
LE VERDICT VIENT DU RENDU : la couleur CALCULÉE du texte du bouton ; le fond CALCULÉ de la page ; le corps = la peau peinte (`__po`) ;
le poil = le ton de palette du sol (`_aura.sol()`), recoupé avec la palette lue (`Toile.cols()`).
  1 · le mot, la police, la taille, la chasse — et la grammaire du bouton inchangée ;
  2 · la hauteur de capitale = celle de « TRACE POUR LANCER » (mesurée : `measureText` dans la police calculée de chacun) ;
  3 · le texte n'est jamais le ton des poils, jamais la teinte du corps ;
  4 · contraste ≥ 3:1 face au fond, à chaque ouverture ; jamais kaki ;
  5 · quand le texte est l'encre du mode : aucun ton de la palette n'était tirable (hors poils, hors corps, non kaki, ≥ 3:1) — recalculé ici ;
  6 · un hasard : au moins deux couleurs de texte différentes par palette (quand au moins deux sont tirables).
Preuve (§7) : sur `sauvegardes/app-avant-v124.html` il ROUGIT.
"""
import os, sys, io, re, math
ICI = os.path.dirname(os.path.abspath(__file__))
_src = io.open(os.path.join(ICI, 'redteam_corps.py'), encoding='utf-8').read()
exec(_src[_src.index('def lin(v):'):_src.index('# ce qui est PEINT')])      # lin, lab, dE00, oklch, kaki — les mêmes que le juge du corps
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
N = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--n=')), 50))
PALETTES = ['signal', 'candide', 'irascible', 'taciturne']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-92s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


def lumrel(c): return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])
def contraste(a, b):
    x, y = lumrel(a), lumrel(b); return (max(x, y) + 0.05) / (min(x, y) + 0.05)
def rgb(v): return [int(x) for x in re.findall(r'\d+', v or '')[:3]] or None


LIT = r"""()=>{ const bt=document.getElementById('auPartage'), cv=document.getElementById('auBoule'); if(!bt||!cv||!cv.__po||!cv.__po.width) return null;
  const cs=getComputedStyle(bt), r=bt.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  const pd=cv.__po.getContext('2d').getImageData(0,0,cv.__po.width,cv.__po.height).data, R=[],G=[],B=[];
  for(let i=0;i<pd.length;i+=4){ if(pd[i+3]>250){ R.push(pd[i]); G.push(pd[i+1]); B.push(pd[i+2]); } }
  const med=a=>{a.sort((x,y)=>x-y); return a[a.length>>1]};
  let fond=null, a=bt; while(a&&a!==document.documentElement){ const m=/rgba?\((\d+)[, ]+(\d+)[, ]+(\d+)(?:[, \/]+([\d.]+))?\)/.exec(getComputedStyle(a).backgroundColor); if(m&&(m[4]===undefined||+m[4]>0.98)){ fond=[+m[1],+m[2],+m[3]]; break; } a=a.parentElement; }
  const cap=(el,txt)=>{ const s=getComputedStyle(el), c=document.createElement('canvas').getContext('2d'); c.font=s.fontStyle+' '+s.fontWeight+' '+s.fontSize+' '+s.fontFamily; const m=c.measureText(txt); return m.actualBoundingBoxAscent; };
  const tr=document.getElementById('dptTrace')||document.querySelector('.tenir-lab,.pp-trace');
  return {mot:bt.textContent.trim(), col:cs.color, fill:cs.webkitTextFillColor, ff:cs.fontFamily, fs:cs.fontSize, fw:cs.fontWeight, ls:cs.letterSpacing, tt:cs.textTransform,
          box:[(r.left-dv.left)/k,(r.width)/k,(r.height)/k], bw:cs.borderTopWidth, br:cs.borderTopLeftRadius, fond:fond,
          corps:R.length?[med(R),med(G),med(B)]:null, sol:(()=>{try{return _aura.sol().idx}catch(e){return null}})(), pal:Toile.cols().map(c=>[c[0]|0,c[1]|0,c[2]|0]),
          capBt:cap(bt,'TRACE POUR LANCER'), capTr:tr?cap(tr,'TRACE POUR LANCER'):null, trFf:tr?getComputedStyle(tr).fontFamily:null, trFs:tr?getComputedStyle(tr).fontSize:null}; }"""

with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','5')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto(APP); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    # une fiche ouverte une fois : la phrase du trait existe, on lit SA police (la référence de hauteur de capitale)
    pg.evaluate("()=>{ try{ openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id); }catch(e){} }"); pg.wait_for_timeout(2500)
    premier = None
    for pal in PALETTES:
        n_lu = 0; meme_poil = 0; meme_corps = 0; bas = 99.0; n_kaki = 0; encre_fausse = 0; vus = set(); tirables_max = 0; ex = ''
        for i in range(N):
            th = 'light' if i % 2 == 0 else 'dark'
            pg.evaluate("([t,p])=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); setTheme(t); try{Toile.setPalette(p)}catch(e){} }", [th, pal]); pg.wait_for_timeout(350)
            pg.evaluate("()=>{ document.querySelectorAll('.screen.show').forEach(s=>{ if(s.id!=='auraScreen'&&s.id!=='studioScreen'&&s.id!=='settingsScreen') s.classList.remove('show'); }); document.getElementById('souffleBtn').click(); }")
            m = None
            for _ in range(40):
                pg.wait_for_timeout(350); pg.evaluate("()=>{ try{ _aura.pelote(); }catch(e){} }"); m = pg.evaluate(LIT)
                if m and m.get('corps'): break
            if not m or not m.get('corps'): continue
            pg.wait_for_timeout(250); m2 = pg.evaluate(LIT); m = m2 or m          # la couleur se pose à la passe de mise en place : on relit
            n_lu += 1
            if premier is None: premier = m
            c = rgb(m['col']); f = m['fond'] or ([247, 240, 222] if th == 'light' else [5, 3, 2]); encre = [32, 25, 8] if th == 'light' else [247, 240, 222]
            poil = m['pal'][m['sol']] if m['sol'] is not None else None
            if poil and dE00(c, poil) < 2: meme_poil += 1
            if dE00(c, m['corps']) < 2: meme_corps += 1
            r_ = contraste(c, f)
            if r_ < bas: bas = r_; ex = 'ouverture %d [%s] texte %s sur %s' % (i + 1, th, c, f)
            # ⚠ l'encre du mode clair #201908 est elle-même dans la plage du kaki (h 87°, L 0,21 — CLAUDE.md v114 : « hors périmètre ») : le repli
            #   DÉCIDÉ (« le texte prend l'encre du mode ») n'est pas un tirage — la règle du kaki juge les teintes TIRÉES
            if c != encre and kaki(c): n_kaki += 1
            # ce qui était tirable, recalculé ici : hors poils, hors corps (le ton de palette le plus proche du corps), non kaki, ≥ 3:1
            ic = min(range(len(m['pal'])), key=lambda k: dE00(m['corps'], m['pal'][k]))
            tirables = [k for k in range(len(m['pal'])) if k != m['sol'] and k != ic and not kaki(m['pal'][k]) and contraste(m['pal'][k], f) >= 3]
            tirables_max = max(tirables_max, len(set(tuple(m['pal'][k]) for k in range(len(m['pal'])) if not kaki(m['pal'][k]) and contraste(m['pal'][k], f) >= 3)))
            if c == encre and tirables: encre_fausse += 1
            if c != encre and not any(dE00(c, m['pal'][k]) < 1 for k in range(len(m['pal']))): encre_fausse += 1     # ni l'encre ni un ton de la palette
            vus.add((th, tuple(c)))
        t('[%s] les %d ouvertures sont lues' % (pal, N), n_lu == N, '%d lues' % n_lu)
        t('3 · [%s] le texte n\'est jamais le ton des poils' % pal, n_lu > 0 and meme_poil == 0, '%d ouverture(s)' % meme_poil)
        t('3 · [%s] le texte n\'est jamais la teinte du corps' % pal, n_lu > 0 and meme_corps == 0, '%d ouverture(s)' % meme_corps)
        t('4 · [%s] contraste ≥ 3:1 face au fond, à chaque ouverture' % pal, n_lu > 0 and bas >= 3, 'le plus bas : %.2f · %s' % (bas, ex))
        t('4 · [%s] jamais kaki' % pal, n_lu > 0 and n_kaki == 0, '%d ouverture(s)' % n_kaki)
        t('5 · [%s] le texte est un ton de la palette ; l\'encre du mode seulement quand aucun ton n\'était tirable' % pal, n_lu > 0 and encre_fausse == 0, '%d ouverture(s) fautive(s)' % encre_fausse)
        t('6 · [%s] la couleur se tire au hasard (au moins deux couleurs vues quand au moins deux tons sont tirables)' % pal, n_lu > 0 and (len(set(c for _, c in vus)) >= 2 or tirables_max < 2), '%d couleur(s) vue(s), jusqu\'à %d ton(s) tirable(s)' % (len(set(c for _, c in vus)), tirables_max))
    m = premier or {}
    t('1 · le mot : « PARTAGER MA PELOTE » (capitales, aucune accentuée)', m.get('mot') == 'PARTAGER MA PELOTE', repr(m.get('mot')))
    t('1 · PromiLate, 15 px, chasse 0, écrit tel quel', str(m.get('ff', '')).lstrip('"\'').startswith('PromiLate') and m.get('fs') == '15px' and m.get('ls') in ('normal', '0px') and m.get('tt') == 'none', '%s · %s · %s · %s' % (m.get('ff'), m.get('fs'), m.get('ls'), m.get('tt')))
    t('1 · la grammaire du bouton n\'a pas bougé : 342 × 60 à x 24, trait 2, rayon 30', bool(m) and abs(m['box'][0] - 24) < 0.5 and abs(m['box'][1] - 342) < 0.5 and abs(m['box'][2] - 60) < 0.5 and m['bw'] == '2px' and m['br'] == '30px', '%s · %s · %s' % ([round(v, 1) for v in m.get('box', [])], m.get('bw'), m.get('br')))
    t('2 · la hauteur de capitale = celle de « TRACE POUR LANCER »', bool(m) and m.get('capTr') and abs(m['capBt'] - m['capTr']) < 0.15, 'bouton %.2f · phrase du trait %.2f (%s %s)' % (m.get('capBt') or 0, m.get('capTr') or 0, m.get('trFf'), m.get('trFs')))
    t('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:8]))
sys.exit(1 if ko else 0)
