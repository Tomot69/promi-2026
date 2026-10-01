# LE PLANCHER DES DALLES prouvé contre un vrai défaut (CLAUDE.md §7), avec le code du juge importé (MATIERE,
# DALLE_DE_MIN). Les couleurs des dalles sont tirées au hasard : on ne peut pas attendre le défaut, on le FABRIQUE.
#   · MORD  — le sol de la sphère prend la couleur BRUTE de sa dalle la plus lisible (la dominante de sa vraie dalle,
#             rendue par le moteur) : c'est le mécanisme naturel du bleu sur bleu, rendu voulu.
#             Le juge doit NOMMER cette dalle (et toute autre dalle de la même couleur).
#   · PASSE — le sol poussé loin de toutes les dalles (la candidate la plus éloignée en CIELAB). Aucune dalle nommée.
#   · la sonde se DÉFAIT exactement : la page tel quel est remesurée à la fin (écart boule ↔ page et ΔE île par île).
#   python3 preuve_plancher.py URL DOSSIER
import sys, os, io, base64, importlib.util
from PIL import Image
from playwright.sync_api import sync_playwright
APP = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
sp = importlib.util.spec_from_file_location('juge_aura', os.path.join(APP, 'releve-aura.py'))
J = importlib.util.module_from_spec(sp); sp.loader.exec_module(J)
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
CAND = [[20, 120, 60], [200, 40, 40], [230, 200, 40], [30, 30, 35], [240, 120, 20]]
# la couleur BRUTE de la dalle d'une île : la dominante (quantifiée sur 5 bits, comme batIles) de sa vraie dalle
DOM = r"""(k)=>{ const x=_auraComp.iles[k], cv=document.createElement('canvas'); cv.width=160; cv.height=160;
  Toile.dalleTrame(cv, x.pid, 1, x.monde); const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, cnt={};
  for(let i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; const q=((d[i]>>3)<<10)|((d[i+1]>>3)<<5)|(d[i+2]>>3); cnt[q]=(cnt[q]||0)+1; }
  const t=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a])[0]|0; return [((t>>10)&31)*8+4, ((t>>5)&31)*8+4, (t&31)*8+4]; }"""
# la couleur moyenne (RGB composé sur la page) au cœur de chaque île, avec et sans elle — la mesure propre à la sonde
MOY = r"""([fond, face])=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=window.__m_avec, s0=window.__m_sans, c=W/2, R=W*0.392;
  const comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), e=_aura.etat(), T=_auraComp.iles||[];
  const B=OrbiteMoteur.batIles(_auraComp.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan), out=[];
  B.iles.forEach((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct; if(Z<=face) return;
    const px=c+X*R, py=c+Y*R, rd=Math.max(6, I.r*R*0.5*Z); let n=0; const a=[0,0,0], s=[0,0,0];
    for(let y=Math.floor(py-rd); y<=py+rd; y++) for(let x=Math.floor(px-rd); x<=px+rd; x++){ if(x<0||y<0||x>=W||y>=W||Math.hypot(x-px,y-py)>rd) continue;
      const i=(y*W+x)*4; n++; for(let t=0;t<3;t++){ a[t]+=comp(d,i,t); s[t]+=comp(s0,i,t); } }
    out.push({k:k, titre:(T[k]&&T[k].titre)||('île '+k), avec:a.map(v=>v/n), sans:s.map(v=>v/n)}); });
  return out; }"""

def lab(c):
    def lin(v):
        v /= 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(x) for x in c)
    X, Y, Z = (0.4124*r + 0.3576*g + 0.1805*b) / 0.95047, 0.2126*r + 0.7152*g + 0.0722*b, (0.0193*r + 0.1192*g + 0.9505*b) / 1.08883
    f = lambda t: t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
    return (116*f(Y) - 16, 500*(f(X) - f(Y)), 200*(f(Y) - f(Z)))
def dE(a, b):
    A, B = lab(a), lab(b); return sum((x - y) ** 2 for x, y in zip(A, B)) ** .5
clamp = lambda v: max(0, min(255, int(round(v))))

ok = True
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def peintes(n=8):
        p0 = pg.evaluate("()=>_aura.etat().peints")
        for _ in range(300):
            if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
            pg.wait_for_timeout(50)
    def ouvre(th):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
    def mesure(fond, nom=None):
        pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
        e = pg.evaluate("()=>_aura.etat().erreur")
        if e: print('❌  PREUVE INVALIDE : erreur du peintre', e[:200]); b.close(); sys.exit(2)
        pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__u=cv.toDataURL('image/png'); window.__m_sans=null;}")
        pg.evaluate("()=>_aura.sansIles(true)"); peintes()
        pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
        pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
        mm = pg.evaluate(J.MATIERE, [fond]); my = pg.evaluate(MOY, [fond, J.ILE_DE_FACE])
        if nom:
            u = pg.evaluate("()=>window.__u"); im = Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
            f = Image.new('RGBA', im.size, tuple(fond) + (255,)); f.alpha_composite(im); f.convert('RGB').save(os.path.join(OUT, nom + '.png'))
        pg.evaluate("()=>_aura.fige(false)"); return mm, my
    def nommees(mm):
        if mm['verif'] is None or mm['verif'] > 1e-6: return None
        return [dl['titre'] for dl in mm['dalles'] if dl['dE'] < J.DALLE_DE_MIN]
    def ligne(mm): return ' '.join('%s %.1f' % (dl['titre'][:14], dl['dE']) for dl in mm['dalles'])
    for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
        ouvre(th)
        m0, my0 = mesure(fond, th + '-tel-quel')
        print('\n[%s] tel quel : %s  →  nommées %s' % (th, ligne(m0), nommees(m0)))
        # MORD — la dalle la plus lisible ; le sol prend SA couleur brute (la couleur dominante de sa dalle, rendue par
        # le moteur dans son monde — stable dans une page, vérifié : couleur_dalle.py). C'est le mécanisme NATUREL du
        # bleu sur bleu (« rapporter le livre » tirée à 76,101,255 sur un sol à 58,84,255), rendu voulu.
        # (Premier essai, retiré : la couleur vue au cœur de l'île « corrigée de l'ombrage » — elle ne noyait pas la
        #  cible, 90 → 30 : le peintre n'est pas une multiplication.)
        cible = max(m0['dalles'], key=lambda x: x['dE'])
        sol = pg.evaluate(DOM, cible['k'])
        pg.evaluate("(c)=>_aura.regleSol(c)", sol)
        m1, _ = mesure(fond, th + '-mord')
        pg.evaluate("()=>{_aura.regleSol(null); _aura.reglePeauC(null);}")
        n1 = nommees(m1); bon = n1 is not None and cible['titre'] in n1; ok &= bon
        print('[%s] MORD  — sphère à la couleur de « %s » (sol %s) : %s  →  nommées %s  %s' % (th, cible['titre'], sol, ligne(m1), n1, '✅' if bon else '❌'))
        # PASSE — le sol le plus éloigné de toutes les dalles
        loin = max(CAND, key=lambda c: min(dE(c, x['avec']) for x in my0))
        pg.evaluate("(c)=>_aura.regleSol(c)", loin)
        m2, _ = mesure(fond, th + '-passe')
        pg.evaluate("()=>{_aura.regleSol(null); _aura.reglePeauC(null);}")
        n2 = nommees(m2); bon = n2 == []; ok &= bon
        print('[%s] PASSE — sol %s, loin de toutes : %s  →  nommées %s  %s' % (th, loin, ligne(m2), n2, '✅' if bon else '❌'))
        # la sonde s'est défaite : tel quel, remesuré
        m3, _ = mesure(fond)
        dmax = max(abs(a['dE'] - c['dE']) for a, c in zip(m0['dalles'], m3['dalles'])) if len(m0['dalles']) == len(m3['dalles']) else 99
        bon = abs(m3['boule'] - m0['boule']) < 0.5 and dmax < 0.5; ok &= bon
        print('[%s] défait — boule ↔ page %.2f puis %.2f, ΔE île par île à %.2f près  %s' % (th, m0['boule'], m3['boule'], dmax, '✅' if bon else '❌'))
    b.close()
print('\n%s' % ('✅  le plancher des dalles mord, et seulement là' if ok else '❌  le plancher des dalles ne tient pas sa preuve'))
sys.exit(0 if ok else 1)
