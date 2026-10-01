# LA FAMILLE « LA MATIÈRE » PROUVÉE SUR LE CAS RÉEL (Tom, 10 sept. : « l'île bleu-sur-bleu au chargement où elle tombe
# à 212 cellules doit être prise — pas un défaut posé »). Rien n'est posé : on recharge jusqu'à ce que le tirage du
# moteur mette une dalle sur la couleur de la sphère. Sur les MÊMES pixels (même page, même vue figée) :
#   · l'ANCIEN juge (sauvegardes/releve-aura-avant-plancher.py : masque seuillé, composantes ≥ 300, borne relative)
#   · le NOUVEAU juge (releve-aura.py : chaque île réelle à son centre, plancher ΔE, borne relative en luminance)
#   · le plus gros morceau de chaque île réelle dans le masque — ce que le filtre à 300 gardait ou jetait
# Il faut : une dalle réelle sous le plancher, JETÉE par l'ancien filtre, et NOMMÉE par le nouveau juge.
#   python3 preuve_cas_reel.py URL DOSSIER [chargements max]
import sys, os, io, base64, importlib.util
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
APP = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
def charge(nom, chemin):
    sp = importlib.util.spec_from_file_location(nom, chemin); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
J = charge('juge_neuf', os.path.join(APP, 'releve-aura.py'))
V = charge('juge_ancien', os.path.join(APP, 'sauvegardes/releve-aura-avant-plancher.py'))
URL, OUT = sys.argv[1], sys.argv[2]; KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 10; os.makedirs(OUT, exist_ok=True)
FRAG = r"""([fond, face])=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=window.__m_avec, s0=window.__m_sans, c=W/2, R=W*0.392;
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b, comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  const S=2, G=Math.ceil(W/S), M=new Int8Array(G*G);
  for(let y=0;y<W;y+=S) for(let x=0;x<W;x+=S){ if(Math.hypot(x-c,y-c)/R>0.90) continue; const i=(y*W+x)*4; if(Math.abs(lum(d,i)-lum(s0,i))>12) M[(y/S)*G+(x/S)]=1; }
  const lbl=new Int32Array(G*G).fill(-1), taille=[];
  for(let k=0;k<G*G;k++){ if(!M[k]||lbl[k]>=0) continue; const id=taille.length; let pile=[k], n=0; lbl[k]=id;
    while(pile.length){ const q=pile.pop(); n++; const qx=q%G, qy=(q/G)|0;
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const nx=qx+dx, ny=qy+dy; if(nx<0||ny<0||nx>=G||ny>=G) continue; const z=ny*G+nx; if(M[z]&&lbl[z]<0){ lbl[z]=id; pile.push(z); } } }
    taille.push(n); }
  const e=_aura.etat(), T=_auraComp.iles||[], B=OrbiteMoteur.batIles(_auraComp.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan), out=[];
  B.iles.forEach((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct; if(Z<=face) return;
    const px=c+X*R, py=c+Y*R, rr=I.r*R*0.9, ids=new Set(); let cel=0;
    for(let y=Math.floor((py-rr)/S); y<=(py+rr)/S; y++) for(let x=Math.floor((px-rr)/S); x<=(px+rr)/S; x++){ if(x<0||y<0||x>=G||y>=G||Math.hypot(x*S-px,y*S-py)>rr) continue; const z=y*G+x; if(lbl[z]>=0){ ids.add(lbl[z]); cel++; } }
    const t=[...ids].map(i=>taille[i]); out.push({k:k, titre:(T[k]&&T[k].titre)||('île '+k), x:px, y:py, r:I.r*R, plusGros:t.length?Math.max(...t):0, morceaux:t.length, cellules:cel}); });
  return out; }"""
def vieux(th, mm, dk):   # l'ancien critère des dalles, tel qu'il était écrit (écart et contour mis à part : ils ne jugent pas les dalles)
    if not mm['iles']: return ['aucune île mesurée']
    if th == 'light' and dk and dk['iles'] and (mm['med'] < dk['med'] - V.DALLES_MARGE or mm['min'] < dk['min'] - V.DALLES_MARGE): return ['dalles noyées']
    return []
def neuf(th, mm, dk):
    f = ['« %s » illisible (ΔE %.1f)' % (x['titre'], x['dE']) for x in mm['dalles'] if x['dE'] < J.DALLE_DE_MIN]
    if th == 'light' and dk and dk['iles'] and (mm['med'] < dk['med'] - J.DALLES_MARGE or mm['min'] < dk['min'] - J.DALLES_MARGE): f.append('dalles noyées (relatif)')
    return f
trouve = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for ch in range(1, KMAX + 1):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        def peintes(n=8):
            p0 = pg.evaluate("()=>_aura.etat().peints")
            for _ in range(300):
                if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
                pg.wait_for_timeout(50)
        R = {}
        for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
            pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(80):
                pg.wait_for_timeout(250)
                if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
            if pg.evaluate("()=>_aura.etat().erreur"): print('❌ erreur du peintre'); sys.exit(2)
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__u=cv.toDataURL('image/png'); window.__m_sans=null;}")
            pg.evaluate("()=>_aura.sansIles(true)"); peintes()
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
            pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
            mn = pg.evaluate(J.MATIERE, [fond]); mv = pg.evaluate(V.MATIERE, [fond]); fr = pg.evaluate(FRAG, [fond, J.ILE_DE_FACE]); u = pg.evaluate("()=>window.__u")
            pg.evaluate("()=>_aura.fige(false)")
            R[th] = (mn, mv, fr, u, fond)
        for th in ('dark', 'light'):
            mn, mv, fr, u, fond = R[th]
            fv, fn = vieux(th, mv, R['dark'][1]), neuf(th, mn, R['dark'][0])
            faible = min(mn['dalles'], key=lambda x: x['dE']); f0 = next(x for x in fr if x['k'] == faible['k'])
            jete = f0['plusGros'] < V.ILE_MIN_CELLS
            print('chargement %d · %-5s · ΔE %s · la plus faible « %s » ΔE %.1f, |Δlum| %.1f, plus gros morceau %d cellules en %d morceaux (%s)'
                  % (ch, th, ' '.join('%.0f' % x['dE'] for x in mn['dalles']), faible['titre'], faible['dE'], faible['lum'], f0['plusGros'], f0['morceaux'],
                     'JETÉE par le filtre à 300' if jete else 'gardée'))
            print('       ancien juge : %d îles comptées, la plus faible %s → %s   |   nouveau juge → %s'
                  % (mv['iles'], mv['min'] and round(mv['min'], 1), fv or 'rien', fn or 'rien'))
            if faible['dE'] < J.DALLE_DE_MIN:
                im = Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA'); fo = Image.new('RGBA', im.size, tuple(fond) + (255,)); fo.alpha_composite(im)
                fo = fo.convert('RGB'); dr = ImageDraw.Draw(fo); dr.ellipse([f0['x'] - f0['r'], f0['y'] - f0['r'], f0['x'] + f0['r'], f0['y'] + f0['r']], outline=(255, 0, 0), width=3)
                nom = 'ch%d-%s-%s.png' % (ch, th, faible['titre'][:20].replace(' ', '_')); fo.save(os.path.join(OUT, nom))
                if jete and any(faible['titre'] in x for x in fn) and not fv: trouve.append((ch, th, faible['titre'], f0['plusGros'], faible['dE'], nom))
        pg.close()
        if ch >= 3 and trouve: break
    b.close()
print()
if trouve:
    for t in trouve: print('✅  CAS RÉEL PRIS — chargement %d, %s : « %s », plus gros morceau %d cellules (jetée par l\'ancien filtre, l\'ancien juge ne dit rien), ΔE %.1f → NOMMÉE par le nouveau juge  [%s]' % t)
else: print('❌  aucun cas réel « jeté par le filtre ET nommé » dans %d chargements' % ch)
sys.exit(0 if trouve else 1)
