# « LE PEIGNÉ » MESURÉ (Tom, 10 sept. : « mesure avant de choisir … vois si le peigné seul fait passer le pire au-dessus
# du plancher ; s'il n'y arrive pas, dis-le »). Sur la COPIE expérimentale (scratchpad/app-aura-epi.html — jamais insérée),
# à la même page, à la même vue figée, l'épi de chaque île en trois modes :
#   actuel   — l'épi du produit (le poil de l'île tourne autour de son centre : 0,74 radial + 0,62 tangentiel)
#   sans     — le poil de l'île suit le peigne du sol (ce que donnerait une île SANS peigné)
#   travers  — le poil de l'île couché à 90° du peigne du sol (le peigné le plus contrasté possible en orientation)
# On recharge jusqu'à trouver des dalles ROUGES (sous le plancher, en mode actuel), et pour chacune on relève :
#   ΔE (la mesure du juge, importée) et ΔE pixel à pixel (qui voit le GRAIN, pas seulement la couleur moyenne).
#   python3 mesure_peigne.py URL DOSSIER [chargements max] [rouges voulus]
import sys, os, io, base64, json, importlib.util
from PIL import Image
from playwright.sync_api import sync_playwright
APP = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
sp = importlib.util.spec_from_file_location('juge', os.path.join(APP, 'releve-aura.py')); J = importlib.util.module_from_spec(sp); sp.loader.exec_module(J)
URL, OUT = sys.argv[1], sys.argv[2]; KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 12; VOULUS = int(sys.argv[4]) if len(sys.argv) > 4 else 6
os.makedirs(OUT, exist_ok=True)
MODES = [None, 'sans', 'travers']; NOM = {None: 'actuel', 'sans': 'sans', 'travers': 'travers'}
PIX = r"""([fond, k])=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=window.__m_avec, s0=window.__m_sans, c=W/2, R=W*0.392;
  const comp=(D,i,t)=>D[i+t]*(D[i+3]/255)+fond[t]*(1-D[i+3]/255);
  const lin=v=>{ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); }, fl=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;
  const lab=(r,g,b)=>{ r=lin(r); g=lin(g); b=lin(b); const X=(0.4124*r+0.3576*g+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g+0.0722*b, Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;
    const fx=fl(X), fy=fl(Y), fz=fl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; };
  const e=_aura.etat(), B=OrbiteMoteur.batIles(_auraComp.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}}), I=B.iles[k];
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan), o=I.c;
  const X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct, px=c+X*R, py=c+Y*R, rd=Math.max(6, I.r*R*0.5*Z);
  let n=0, s=0; for(let y=Math.floor(py-rd); y<=py+rd; y++) for(let x=Math.floor(px-rd); x<=px+rd; x++){ if(x<0||y<0||x>=W||y>=W||Math.hypot(x-px,y-py)>rd) continue;
    const i=(y*W+x)*4, A=lab(comp(d,i,0),comp(d,i,1),comp(d,i,2)), S=lab(comp(s0,i,0),comp(s0,i,1),comp(s0,i,2)); n++; s+=Math.hypot(A[0]-S[0],A[1]-S[1],A[2]-S[2]); }
  return {pix:s/n, x:px, y:py, r:I.r*R}; }"""
rouges = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for ch in range(1, KMAX + 1):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if not pg.evaluate("()=>!!(window._aura&&_aura.regleEpi)"): print('❌ la copie ne porte pas regleEpi'); sys.exit(2)
        def peintes(n=8):
            p0 = pg.evaluate("()=>_aura.etat().peints")
            for _ in range(300):
                if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
                pg.wait_for_timeout(50)
        for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
            pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(80):
                pg.wait_for_timeout(250)
                if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}")
            res = {}; imgs = {}
            for m in MODES + [None]:          # le dernier « actuel » vérifie que la sonde s'est défaite
                pg.evaluate("(m)=>_aura.regleEpi(m)", m); peintes()
                if pg.evaluate("()=>_aura.etat().erreur"): print('❌ erreur du peintre', pg.evaluate("()=>_aura.etat().erreur")[:160]); sys.exit(2)
                pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__u=cv.toDataURL('image/png'); window.__m_sans=null;}")
                pg.evaluate("()=>_aura.sansIles(true)"); peintes()
                pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
                pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
                mm = pg.evaluate(J.MATIERE, [fond]); pix = {dl['k']: pg.evaluate(PIX, [fond, dl['k']]) for dl in mm['dalles']}
                cle = NOM[m] if NOM[m] not in res else 'actuel-retour'
                res[cle] = (mm, pix); imgs[cle] = pg.evaluate("()=>window.__u")
            pg.evaluate("()=>{_aura.regleEpi(null); _aura.fige(false);}")
            A = {dl['k']: dl for dl in res['actuel'][0]['dalles']}; Rt = {dl['k']: dl for dl in res['actuel-retour'][0]['dalles']}
            defait = max(abs(A[k]['dE'] - Rt[k]['dE']) for k in A) if set(A) == set(Rt) else 99
            for k, dl in A.items():
                if dl['dE'] >= J.DALLE_DE_MIN: continue
                ligne = {'ch': ch, 'th': th, 'titre': dl['titre'], 'defait': round(defait, 2)}
                for nm in ('actuel', 'sans', 'travers'):
                    d2 = next(x for x in res[nm][0]['dalles'] if x['k'] == k); ligne[nm] = (round(d2['dE'], 1), round(res[nm][1][k]['pix'], 1))
                rouges.append(ligne)
                q = res['actuel'][1][k]; h = int(max(60, q['r'] * 1.5)); box = (int(q['x'] - h), int(q['y'] - h), int(q['x'] + h), int(q['y'] + h))
                pl = Image.new('RGB', (3 * 240 + 20, 240), tuple(fond))
                for j, nm in enumerate(('sans', 'actuel', 'travers')):
                    im = Image.open(io.BytesIO(base64.b64decode(imgs[nm].split(',')[1]))).convert('RGBA'); fo = Image.new('RGBA', im.size, tuple(fond) + (255,)); fo.alpha_composite(im)
                    pl.paste(fo.convert('RGB').crop(box).resize((240, 240)), (j * 250, 0))
                pl.save(os.path.join(OUT, 'ch%d-%s-%s.png' % (ch, th, dl['titre'][:18].replace(' ', '_'))))
                print('ROUGE ch%d %-5s « %s »  ΔE (juge) / ΔE pixel :  sans %s · actuel %s · travers %s   (sonde défaite à %.2f près)'
                      % (ch, th, dl['titre'], ligne['sans'], ligne['actuel'], ligne['travers'], defait))
        pg.close()
        if len(rouges) >= VOULUS: break
    b.close()
print('\n%d dalles rouges en %d chargements (plancher du juge : ΔE %.0f)' % (len(rouges), ch, J.DALLE_DE_MIN))
if rouges:
    pire = min(rouges, key=lambda x: x['actuel'][0])
    passent = [r for r in rouges if r['travers'][0] >= J.DALLE_DE_MIN]
    print('le pire : « %s » (ch%d, %s) — actuel %.1f → travers %.1f (sans : %.1f)' % (pire['titre'], pire['ch'], pire['th'], pire['actuel'][0], pire['travers'][0], pire['sans'][0]))
    print('le peigné en travers fait passer le plancher à %d dalle(s) rouge(s) sur %d' % (len(passent), len(rouges)))
json.dump(rouges, open(os.path.join(OUT, 'rouges.json'), 'w'), ensure_ascii=False, indent=1)
