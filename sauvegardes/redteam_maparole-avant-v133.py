#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_maparole.py — L'ORANGE DE MA PAROLE !, ISOLÉ (v122, Tom, 3 oct. 2026).

« Crée un jeton dédié, --orange-maparole (#FB4C0D, et #FF7A55 sur les trois corps sombres de Peaufiner), appliqué uniquement aux
textes de Ma Parole ! dans les zones floues. Juge : #FB4C0D et #FF7A55 n'apparaissent nulle part ailleurs, dans aucun écran ni aucun thème. »

Valeurs EN DUR (§7) : #FB4C0D = rgb(251, 76, 13) · #FF7A55 = rgb(255, 122, 85).
  A · la source : les deux hex (et leurs triplets) n'existent que dans le bloc des jetons (`--c-orange-maparole`, `-corps`) ; ces jetons ne
      sont lus que par `#murPhrase` (qui pose `--orange-maparole`) ; `--orange-maparole` n'est lu que par `#murPhrase .mp` ; le moteur
      (`promi-moteur.js`) n'en porte aucun ;
  B · le rendu : 36 écrans × 2 thèmes (ceux de redteam_air) — aucun nœud visible ne porte l'une des deux couleurs (encre, fond, bordures,
      contour, fill, stroke, ombres, image de fond), et aucun canevas n'en a plus de 20 pixels exacts ;
  C · les murs : la phrase qui porte « Ma Parole ! », montée au doigt sur le Peaufiner d'une fiche — ses mots `.mp` en #FF7A55 sur le corps
      sombre, en #FB4C0D en clair ; le reste de la phrase n'est ni l'un ni l'autre.
Preuve (§7) : `--sonde` pose l'orange de Ma Parole ! sur « ✕ FERMER » → A et B ROUGISSENT ; sur `sauvegardes/app-avant-v122.html`, A rougit.
"""
import os, re, sys, io
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
SONDE = '--sonde' in sys.argv
ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)', 'rgb(255, 134, 100)')
# ⚑ v131 (Tom, 5 oct. 2026) — CONTRAT ÉTENDU (original : sauvegardes/redteam_maparole-avant-v131.py) : une TROISIÈME valeur, #FF8664, « même
#   teinte OKLCH que #FB4C0D, éclaircie jusqu'à 3:1 » sur le corps cobalt #273CEB d'un Promi (jeton --c-orange-maparole-cobalt). Elle non plus
#   n'existe nulle part ailleurs. Le Peaufiner mesuré en C est celui d'un Promi : en sombre, c'est elle qu'on attend.
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('%-80s %s  %s' % (nom, 'OK' if cond else 'KO', detail))


S = io.open(os.path.join(ICI, FICHIER), encoding='utf-8').read()
if SONDE:
    S = S.replace('</head>', '<style id="sonde-maparole">#device .closeb{color:var(--c-orange-maparole)!important;-webkit-text-fill-color:var(--c-orange-maparole)!important}</style></head>', 1)
    print('SONDE : « ✕ FERMER » est peint de l\'orange de Ma Parole !')
SERVI = 'zz-maparole.html'
io.open(os.path.join(ICI, SERVI), 'w', encoding='utf-8').write(S)
M = io.open(os.path.join(ICI, 'promi-moteur.js'), encoding='utf-8').read()

# ── A · la source
HEX = re.compile(r'#(?:FB4C0D|FF7A55|FF8664)\b|\b251\s*,\s*76\s*,\s*13\b|\b255\s*,\s*122\s*,\s*85\b|\b255\s*,\s*134\s*,\s*100\b', re.I)
# les commentaires ne peignent rien : on les retire (en gardant les sauts de ligne, pour les numéros) avant de chercher
def _sans_comm(m): return '\n' * m.group(0).count('\n')
NUE = re.sub(r'/\*.*?\*/', _sans_comm, S, flags=re.S)
NUE = re.sub(r'(?m)^\s*//.*$', '', NUE)
lignes = NUE.split('\n')
hors = [(i + 1, l.strip()[:90]) for i, l in enumerate(lignes) if HEX.search(l) and not re.search(r'--c-orange-maparole(-corps|-cobalt)?\s*:\s*#(FB4C0D|FF7A55|FF8664)', l, re.I)]
t('A · #FB4C0D et #FF7A55 n\'existent que dans le bloc des jetons', not hors, '; '.join('l.%d %s' % h for h in hors[:3]) or '')
t('A · le moteur n\'en porte aucun', not HEX.search(M), '')
lec = re.findall(r'([^{}]{0,120})\{[^{}]*var\(--c-orange-maparole(?:-corps)?\)', NUE)
t('A · les jetons ne sont lus que par #murPhrase (qui pose --orange-maparole)', bool(lec) and all(re.search(r'#murPhrase(\.sur-corps(\.sur-cobalt)?)?\s*$', s.strip()) for s in lec), ' | '.join(s.strip()[-60:] for s in lec))
lec2 = re.findall(r'([^{}]{0,120})\{[^{}]*var\(--orange-maparole\)', NUE)
t('A · --orange-maparole n\'est lu que par « #murPhrase .mp »', bool(lec2) and all(s.strip().endswith('#murPhrase .mp') for s in lec2), ' | '.join(s.strip()[-60:] for s in lec2))

if '--statique' in sys.argv:      # la source seule, sans navigateur
    try: os.remove(os.path.join(ICI, SERVI))
    except Exception: pass
    print('\n%d / %d' % (ok[0], ok[0] + len(ko))); sys.exit(1 if ko else 0)

# ── B · le rendu
src = io.open(os.path.join(ICI, 'redteam_air.py'), encoding='utf-8').read()
ECRANS = [(m.group(1), m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$", src, re.M)]
SCAN = r"""(OR)=>{ const dv=document.getElementById('device').getBoundingClientRect(), out=[];
  const T=document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT); let e;
  while((e=T.nextNode())){ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) continue;
    if(r.right<dv.left||r.left>dv.right||r.bottom<dv.top||r.top>dv.bottom) continue;
    const cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) continue;
    if(e.closest('#murPhrase')) continue;
    const v=[cs.color,cs.webkitTextFillColor,cs.backgroundColor,cs.borderTopColor,cs.borderBottomColor,cs.borderLeftColor,cs.borderRightColor,cs.outlineColor,cs.fill,cs.stroke,cs.boxShadow,cs.textShadow,cs.backgroundImage].join(' | ');
    for(const o of OR) if(v.indexOf(o)>=0){ out.push((e.id||e.className||e.tagName).toString().slice(0,40)+' ← '+o); break; }
    if(e.tagName==='CANVAS'&&e.width>4){ try{ const d=e.getContext('2d').getImageData(0,0,e.width,e.height).data; let n=0;
      for(let i=0;i<d.length;i+=4){ if(d[i+3]>250&&((d[i]===251&&d[i+1]===76&&d[i+2]===13)||(d[i]===255&&d[i+1]===122&&d[i+2]===85))) n++; }
      if(n>20) out.push('canevas '+(e.id||e.className)+' : '+n+' pixels'); }catch(_){} } }
  return out; }"""
ETAT = """()=>{const p=document.getElementById('murPhrase'); if(!p) return null; const m=p.querySelector('.mp'), s=getComputedStyle(p);
  return {leve:p.classList.contains('leve'), texte:p.textContent, mp:m?getComputedStyle(m).color:null, mpf:m?getComputedStyle(m).webkitTextFillColor:null, reste:s.color}}"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + SERVI); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{setPremium(false)}catch(e){}}", th); pg.wait_for_timeout(600)
        trouves = []
        for nom, js in ECRANS:
            try:
                pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(300)
                pg.evaluate(js); pg.wait_for_timeout(2200)
                trouves += ['%s · %s' % (nom, x) for x in pg.evaluate(SCAN, list(ORANGE))]
            except Exception as ex:
                trouves.append('%s · ERREUR %s' % (nom, str(ex)[:60]))
        t('B · [%s] aucun nœud ni canevas ne porte #FB4C0D ni #FF7A55 (%d écrans)' % (th, len(ECRANS)), not trouves, '; '.join(trouves[:4]) + (' …(+%d)' % (len(trouves) - 4) if len(trouves) > 4 else ''))
        # C · la phrase qui porte « Ma Parole ! », montée au doigt sur le Peaufiner d'une fiche
        pg.evaluate("()=>{ try{closeAll()}catch(e){} const PH=window._murPhrases||[]; const i=PH.findIndex(s=>s.indexOf('Ma Parole')>=0); localStorage.setItem('promi_murs', JSON.stringify({n:Math.max(0,i),t:Date.now(),der:Math.max(0,i)-1,decouvert:1})); const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0]; openDetail(p.id); }"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
        c = pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(!e)return null;const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(800)
        e = pg.evaluate(ETAT) or {}
        attendu = ORANGE[2] if th == 'dark' else ORANGE[0]
        t('C · [%s] sur le Peaufiner : « Ma Parole ! » en %s' % (th, '#FF8664 (corps cobalt d\'un Promi)' if th == 'dark' else '#FB4C0D'), bool(e.get('leve')) and e.get('mp') == attendu and e.get('mpf') == attendu, '%r · mp %s · reste %s' % ((e.get('texte') or '')[:40], e.get('mp'), e.get('reste')))
        t('C · [%s] le reste de la phrase n\'est pas l\'orange de Ma Parole !' % th, e.get('reste') not in ORANGE, str(e.get('reste')))
        t('[%s] aucune erreur de page' % th, not er, '; '.join(er[:2]))
        ctx.close()
    b.close()
try: os.remove(os.path.join(ICI, SERVI))
except Exception: pass
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:6]))
sys.exit(1 if ko else 0)
