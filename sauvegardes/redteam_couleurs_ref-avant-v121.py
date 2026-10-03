#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_couleurs_ref.py — LES COULEURS SONT CELLES D'AVANT v116 (v120, Tom, 2 oct. 2026).

« Hors de la Toile, toutes les couleurs de tous les écrans, en clair et en sombre, redeviennent identiques à la référence
(sauvegardes/app-avant-v116.html) : textes, fonds, corps, filets, pilules, anneaux. Exceptions, et seulement celles-là : la Toile en
sombre garde l'encre de seiche (fond, rampes, grain) ; le fond de la Toile en clair reste à plat ; l'orange des murs. »

Le juge ouvre CHAQUE écran, dans les deux thèmes, sur l'app ET sur la référence (servie avec SON moteur d'alors), et compare :
  · les STYLES CALCULÉS de chaque nœud visible de l'appareil — encre (color, -webkit-text-fill-color), fond, bordures, contour,
    fill / stroke, ombres, image de fond ;
  · des ÉCHANTILLONS DE CANEVAS — les couleurs dominantes de chaque canevas visible (une matière respire : on compare les couleurs
    présentes, pas leur place).
Les exceptions sont NOMMÉES ici, en dur (§7) — rien d'autre n'est toléré :
  E1  les canevas peints par le moteur de la Toile (la Toile, ses aperçus, la Toile du Cercle, le fond du Studio, le partage) ;
  E2  dans un canevas de fiche ou de carte, la MATIÈRE d'une dalle (c'est le moteur : rampes et grain) — le champ, le trait et le
      corps, eux, sont comparés ;
  E3  les mots d'accent des phrases des murs (#FB4C0D, §4) ;
  E4  la Pelote (canevas de l'Aura) : elle a ses juges (redteam_plein, redteam_halo, redteam_contour).
Un nœud qui n'existe que d'un côté (un bouton né ou retiré depuis v116) n'est pas un écart de couleur : il est LISTÉ.

  python3 redteam_couleurs_ref.py            → tous les écrans
  python3 redteam_couleurs_ref.py --liste    → détaille chaque écart
Preuve (§7) : `APP=http://127.0.0.1:8752/<copie de sauvegardes/app-avant-v120.html>` ROUGIT.
"""
import os, re, sys, io, json, math, shutil
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
REF_SRC = os.path.join(ICI, 'sauvegardes', 'app-avant-v116.html')
REF_MOT = os.path.join(ICI, 'sauvegardes', 'promi-moteur-avant-v116.js')
LISTE = '--liste' in sys.argv
SEUL = [a.split('=', 1)[1] for a in sys.argv if a.startswith('--ecran=')]

# la référence, servie à la racine avec SON moteur
S = io.open(REF_SRC, encoding='utf-8').read()
assert S.count('<script src="promi-moteur.js"></script>') == 1
io.open(os.path.join(ICI, 'zz-ref-v116.html'), 'w', encoding='utf-8').write(S.replace('<script src="promi-moteur.js"></script>', '<script src="zz-ref-v116-moteur.js"></script>'))
shutil.copyfile(REF_MOT, os.path.join(ICI, 'zz-ref-v116-moteur.js'))
REF = 'http://127.0.0.1:8752/zz-ref-v116.html'

# les écrans : ceux de redteam_air (34), plus les murs
src = io.open(os.path.join(ICI, 'redteam_air.py'), encoding='utf-8').read()
ECRANS = [(m.group(1), m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$", src, re.M)]
ECRANS.append(('mur · Réglages', "()=>{closeAll(); document.getElementById('settingsBtn').click(); setTimeout(()=>{ try{ var m=document.querySelector('#settingsScreen .s2-cercle, #settingsScreen [data-mur]'); if(m && window._murMonte) window._murMonte(m); }catch(e){} },700);}"))
ECRANS.append(('panneau des palettes', "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); const b=document.getElementById('openStudio2'); if(b) b.click(); setTimeout(()=>{const t=document.querySelector('#studioScreen .stp-ton'); if(t) t.click();},1200);}"))
def _plus(i):
    return "()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][%d]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}" % i
ECRANS = [(n, _plus({'page +': 0, 'page + Chiche': 1, 'page + Nuée': 2}[n]) if n in ('page +', 'page + Chiche', 'page + Nuée') else j) for n, j in ECRANS]
assert len(ECRANS) >= 30, len(ECRANS)

# E1 — les canevas du moteur de la Toile (ids), E4 — la Pelote
TOILE = re.compile(r'^(toile|toileCv|stBg|shCanvas|shareToileBg|stTrameCv|plHeroCv|csTrameCv2)$|Toile|toile|^stp|apercu|^pc', re.I)
PELOTE = re.compile(r'^(auBoule|auPeloteFlaque)$')

COLLECTE = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), out={n:{}, c:{}};
  const vus={};
  function cle(e){ let a=e, ch=[]; for(let k=0;k<3&&a&&a!==document.body;k++){ if(a.id){ ch.unshift('#'+a.id); break; }
      const cl=(a.className&&a.className.baseVal!==undefined?a.className.baseVal:(a.className||'')).toString().trim().split(/\s+/).filter(c=>c&&!/^(on|show|sel|actif|active|pris|ouvert|zzz|tracant|is-|s2-ouv|gone)/.test(c)).slice(0,3).join('.');
      ch.unshift(a.tagName.toLowerCase()+(cl?'.'+cl:'')); a=a.parentElement; }
    if(a&&a.id&&ch[0]!=='#'+a.id) ch.unshift('#'+a.id);
    const k=ch.join(' > '); vus[k]=(vus[k]||0)+1; return k+' ['+vus[k]+']'; }
  const T=document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT); let e;
  while((e=T.nextNode())){
    const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) continue;
    if(r.right<dv.left+1||r.left>dv.right-1||r.bottom<dv.top+1||r.top>dv.bottom-1) continue;
    const cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<0.05) continue;
    let a=e.parentElement, cache=false; while(a&&a!==document.body){ const ca=getComputedStyle(a); if(parseFloat(ca.opacity)<0.05||ca.visibility==='hidden'){ cache=true; break; } a=a.parentElement; } if(cache) continue;
    if(e.id==='promiOnb'||e.closest('#promiOnb')) continue;
    const k=cle(e), o={};
    const txt=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
    if(txt){ o.color=cs.color; if(cs.webkitTextFillColor&&cs.webkitTextFillColor!==cs.color) o.tfill=cs.webkitTextFillColor; if(cs.textShadow&&cs.textShadow!=='none') o.tshadow=cs.textShadow; o.mot=(e.textContent||'').trim().slice(0,24); }
    if(cs.backgroundColor!=='rgba(0, 0, 0, 0)') o.bg=cs.backgroundColor;
    if(cs.backgroundImage&&cs.backgroundImage!=='none') o.bgi=cs.backgroundImage.replace(/url\([^)]{60,}\)/g,'url(…)').slice(0,300);
    ['Top','Right','Bottom','Left'].forEach(c=>{ if(parseFloat(cs['border'+c+'Width'])>0&&cs['border'+c+'Style']!=='none') o['b'+c[0]]=cs['border'+c+'Color']; });
    if(parseFloat(cs.outlineWidth)>0&&cs.outlineStyle!=='none') o.outline=cs.outlineColor;
    if(cs.boxShadow&&cs.boxShadow!=='none') o.shadow=cs.boxShadow.replace(/-?\d+(\.\d+)?px/g,'').replace(/\s+/g,' ').trim();
    if(e instanceof SVGElement && e.tagName!=='svg'){ if(cs.fill&&cs.fill!=='none') o.fill=cs.fill; if(cs.stroke&&cs.stroke!=='none') o.stroke=cs.stroke; }
    if(Object.keys(o).length) out.n[k]=o;
    if(e.tagName==='CANVAS'&&e.width>8&&e.height>8){
      try{ const g=e.getContext('2d'); if(g){ const W=e.width,H=e.height, d=g.getImageData(0,0,W,H).data, h={}; let n=0; const pas=Math.max(1,Math.floor(Math.sqrt(W*H/40000)));
        const kk=W/Math.max(1,e.clientWidth||W), ZM=((e.getAttribute('data-matieres')||e.getAttribute('data-matiere')||'').split(/[;|]/)).map(s=>s.split(',').map(Number)).filter(a=>a.length>=4&&a.every(v=>isFinite(v))).map(a=>[a[0]*kk-3,a[1]*kk-3,(a[0]+a[2])*kk+3,(a[1]+a[3])*kk+3]); let nm=0;
        for(let y=0;y<H;y+=pas) for(let x=0;x<W;x+=pas){ const i=(y*W+x)*4; if(d[i+3]<250) continue; let dm=false; for(const z of ZM){ if(x>=z[0]&&x<=z[2]&&y>=z[1]&&y<=z[3]){ dm=true; break; } } if(dm){ nm++; continue; } n++; const q=(d[i]<<16)|(d[i+1]<<8)|d[i+2]; h[q]=(h[q]||0)+1; }
        const L=Object.keys(h).map(q=>[+q,h[q]/Math.max(1,n)]).filter(a=>a[1]>=0.012).sort((a,b)=>b[1]-a[1]).slice(0,10).map(a=>[(a[0]>>16)&255,(a[0]>>8)&255,a[0]&255,+a[1].toFixed(3)]);
        out.c[e.id||k]={dom:L, n:n, mat:nm, zones:ZM.length, coin:[d[(4*W+4)*4],d[(4*W+4)*4+1],d[(4*W+4)*4+2],d[(4*W+4)*4+3]]}; } }catch(_){ } }
  }
  return out; }"""


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


def pose(pg):
    # un écran qui se compose par minuteurs n'est pas fini quand il paraît (§8) : deux relevés identiques des STYLES, à 0,9 s d'écart
    av = pg.evaluate(COLLECTE)
    for _ in range(4):
        pg.wait_for_timeout(900); ap = pg.evaluate(COLLECTE)
        if json.dumps(ap['n'], sort_keys=True) == json.dumps(av['n'], sort_keys=True): return ap
        av = ap
    return av


def releve(pg, url):
    pg.goto(url); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    R = {}
    for th in ('light', 'dark'):
        pg.evaluate("(t)=>{ try{closeAll()}catch(e){} setTheme(t); }", th); pg.wait_for_timeout(600)
        for nom, js in ECRANS:
            if SEUL and nom not in SEUL: continue
            try:
                pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(350)
                pg.evaluate(js); pg.wait_for_timeout(2600)
                R[(nom, th)] = pose(pg)
            except Exception as ex:
                R[(nom, th)] = {'n': {}, 'c': {}, 'err': str(ex)[:120]}
    return R


# E3 — l'orange des mots des murs (§4) : la seule encre qui peut différer, et seulement vers cette valeur
MUR_ORANGE = 'rgb(251, 76, 13)'

with sync_playwright() as p:
    b = p.webkit.launch()
    def page():
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');Math.random=(function(){var s=20261002;return function(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;};})();}catch(e){}")
        pg = ctx.new_page(); pg.__er = []; pg.on('pageerror', lambda e: pg.__er.append(str(e)[:140])); return pg
    pa = page(); A = releve(pa, APP)
    pr = page(); B = releve(pr, REF)

    def frais(url, nom, th):
        # ⚠ un écran ouvert à la suite d'un autre peut en garder l'état (l'instant, la page + d'une autre nature) : ce n'est pas un
        #   écart de couleur. Tout écran pris en écart est donc REPRIS sur une page fraîche, des deux côtés, avant d'être cru (§7).
        pg = page(); pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(700)
        pg.evaluate(dict(ECRANS)[nom]); pg.wait_for_timeout(3200)
        try: r = pose(pg)
        except Exception as ex: r = {'n': {}, 'c': {}, 'err': str(ex)[:120]}
        pg.context.close(); return r

    def compare_tout(A, B):
        global ecarts, orphelins, compares, cv_ecarts, exceptions
        ecarts = []; orphelins = 0; compares = 0; cv_ecarts = []; exceptions = {'E1': 0, 'E2': 0, 'E3': 0, 'E4': 0}
        for cle in A: compare_un(cle, A[cle], B.get(cle, {'n': {}, 'c': {}}))

    def compare_un(cle, a, r):
        global orphelins, compares
        if True:
            if not a['n'] or not r['n']:
                ecarts.append((cle, '(écran)', 'ouverture', 'app %d nœuds' % len(a['n']), 'réf %d nœuds %s' % (len(r['n']), r.get('err', '')))); return
            for k, o in a['n'].items():
                q = r['n'].get(k)
                if q is None: orphelins += 1; continue
                if o.get('mot') != q.get('mot') and ('mot' in o or 'mot' in q):
                    orphelins += 1; continue                      # pas le même nœud (le texte a changé de place) : listé, pas jugé
                for pr_ in set(list(o) + list(q)) - {'mot'}:
                    compares += 1
                    va, vr = o.get(pr_), q.get(pr_)
                    if va == vr: continue
                    if pr_ in ('color', 'tfill') and va == MUR_ORANGE: exceptions['E3'] += 1; continue
                    ecarts.append((cle, k, pr_, va, vr))
            for k, c in a['c'].items():
                q = r['c'].get(k)
                if PELOTE.search(k): exceptions['E4'] += 1; continue
                if TOILE.search(k): exceptions['E1'] += 1; continue
                if q is None: continue
                if c.get('zones'): exceptions['E2'] += 1          # la matière déclarée est exclue de l'échantillon
                for col in c['dom']:
                    m = min([dE(col[:3], x[:3]) for x in q['dom']] or [99])
                    if m > 2.5:
                        # E2 — la matière d'une dalle : une couleur dominante sans vis-à-vis qui n'est NI le coin (le champ) NI une grande part
                        if not c.get('zones') and col[3] < 0.10 and dE(col[:3], c['coin'][:3]) > 2.5: exceptions['E2'] += 1; continue
                        cv_ecarts.append((cle, k, 'canevas', 'rgb(%d, %d, %d) %.0f %%' % (col[0], col[1], col[2], 100 * col[3]), 'au plus près ΔE %.1f' % m))


    compare_tout(A, B)
    suspects = sorted(set(e[0] for e in ecarts + cv_ecarts))
    for (nom, th) in suspects:
        A[(nom, th)] = frais(APP, nom, th); B[(nom, th)] = frais(REF, nom, th)
    if suspects: print('%d écran(s) repris sur une page fraîche : %s' % (len(suspects), ', '.join('%s[%s]' % (n, t[0]) for n, t in suspects)))
    compare_tout(A, B)
    b.close()

tout = ecarts + cv_ecarts
par = {}
for e in tout: par.setdefault((e[2], str(e[4]), str(e[3])), []).append(e)
print('%d propriétés comparées · %d écrans × 2 thèmes · %d nœuds sans vis-à-vis (listés, non jugés)' % (compares, len(ECRANS) if not SEUL else len(SEUL), orphelins))
print('exceptions nommées : E1 Toile %d canevas · E2 matière de dalle %d · E3 orange des murs %d · E4 Pelote %d' % (exceptions['E1'], exceptions['E2'], exceptions['E3'], exceptions['E4']))
for (pr_, vr, va), L in sorted(par.items(), key=lambda x: -len(x[1])):
    ec = sorted(set('%s[%s]' % (e[0][0], e[0][1][0]) for e in L))
    print('  ✗ %-8s réf %-34s → app %-34s ×%d   %s' % (pr_, vr[:34], va[:34], len(L), ', '.join(ec[:6]) + (' …' if len(ec) > 6 else '')))
    if LISTE:
        for e in L[:12]: print('        %s [%s] · %s' % (e[0][0], e[0][1], e[1][:90]))
if pa.__er or pr.__er: print('erreurs de page : app %s · réf %s' % (pa.__er[:2], pr.__er[:2]))
print('\n%s — %d écart(s) de couleur avec la référence d\'avant v116' % ('✅' if not tout else '❌', len(tout)))
sys.exit(1 if tout else 0)
