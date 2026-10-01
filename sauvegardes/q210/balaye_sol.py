# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# Q210 · VOIE A — LE SOL DU CLAIR S'ASSOMBRIT, LA PEAU RESTE CLAIRE
# Tom, 12 sept. : « Si aucune couleur de la palette n'est assez loin du sol pâle, c'est le sol qu'il faut
# changer, pas les dalles qu'il faut tordre. » On balaie l'assombrissement du POIL (le sol), la peau gardant
# sa teinte claire (§1.2 + K.PEAU_CREME) — c'est l'inversion de Q182, en degrés.
# ON NE TOUCHE À RIEN : `_aura.regleSol([r,g,b])` existe déjà pour la mesure.
# On mesure les DEUX familles de critères, dans la même page (les couleurs de dalle sont tirées au hasard :
# une comparaison entre pages ne vaut rien) :
#   · Q210 — l'écart de chaque île au sol, ΔE (CIELAB), avec l'île et sans elle. Plancher 15.
#   · Q182 — ce que le juge porte EN DUR : boule ↔ page 85 en clair (±8), contour ≥ 42.
#   python3 balaye_sol.py [n_pages]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys, math
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
PLANCHER, FACE = 15.0, 0.35
BOULE_CLAIR, TOL, CONTOUR_MIN = 85.0, 8.0, 42.0      # les valeurs DÉCIDÉES, portées en dur (Q182)
FOND = [244, 238, 225]

# les degrés d'assombrissement du poil : 1,00 = la nature telle quelle (l'état livré)
DEGRES = [float(x) for x in (__import__('os').environ.get('DEGRES') or '1.00 0.80 0.65 0.50 0.38 0.28').split()]
# ⚑ DEUXIÈME DIMENSION : la PEAU. Assombrir le poil ne touche QUE les poils du sol (les îles gardent la
#   couleur de leur dalle, index ≠ 0 dans la table de `batIles`) — donc on peut rendre à la boule la clarté
#   qu'elle perd, par la peau, sans rien rendre aux îles. `_aura.reglePeauC([r,g,b])` existe déjà.
PEAUX = [('celle décidée (A2)', None),           # NAT_CLAIR tirée à 60 % vers le crème
         ('le crème du corps', [244, 238, 225]),
         ('blanc', [255, 255, 255])]
if __import__('os').environ.get('PEAUX') == 'court': PEAUX = PEAUX[:2]

MESURE = r"""([fond, FACE])=>{
  const cv=document.getElementById('auBoule'), W=cv.width, d=window.__m_avec, s0=window.__m_sans;
  if(!d||!s0) return null;
  const c=W/2, R=W*0.392;
  const comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255);
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b;
  const lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  const lin=v=>{v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);}, fl=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;
  const lab=(r,g,b)=>{ r=lin(r); g=lin(g); b=lin(b);
    const X=(0.4124*r+0.3576*g+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g+0.0722*b, Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;
    const fx=fl(X), fy=fl(Y), fz=fl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; };
  /* boule ↔ page et contour, la métrique du §3 — sur la boule AVEC ses îles */
  const dedans=[], limbe=[];
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const r=Math.hypot(x-c,y-c)/R; if(r>1) continue;
    const i=(y*W+x)*4, l=lum(d,i); if(r<=0.90) dedans.push(l); else if(r>=0.95) limbe.push(l); }
  const moy=a=>a.reduce((s,v)=>s+v,0)/a.length, pg=L(fond[0],fond[1],fond[2]);
  /* les îles, une à une, là où le moteur les pose */
  const e=_aura.etat(), C=window._auraComp||{}, T=C.iles||[];
  const B=OrbiteMoteur.batIles(C.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan);
  const iles=[];
  B.iles.forEach((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct;
    if(Z<=FACE) return;
    const px=c+X*R, py=c+Y*R, rd=Math.max(6, I.r*R*0.5*Z); let n=0; const LA=[0,0,0], LS=[0,0,0];
    for(let y=Math.floor(py-rd); y<=py+rd; y++) for(let x=Math.floor(px-rd); x<=px+rd; x++){
      if(x<0||y<0||x>=W||y>=W||Math.hypot(x-px,y-py)>rd) continue;
      const i=(y*W+x)*4; n++;
      const A=lab(comp(d,i,0),comp(d,i,1),comp(d,i,2)), S=lab(comp(s0,i,0),comp(s0,i,1),comp(s0,i,2));
      for(let t=0;t<3;t++){ LA[t]+=A[t]; LS[t]+=S[t]; } }
    if(!n) return;
    iles.push({titre:(T[k]&&T[k].titre)||('île '+k),
               dE:+Math.hypot(LA[0]/n-LS[0]/n, LA[1]/n-LS[1]/n, LA[2]/n-LS[2]/n).toFixed(1)}); });
  return {boule:+Math.abs(moy(dedans)-pg).toFixed(1), contour:+Math.abs(moy(limbe)-pg).toFixed(1), iles:iles}; }"""

def deux_images(pg):
    pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
    pg.evaluate("()=>_aura.sansIles(true)"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
    pg.evaluate("()=>_aura.sansIles(false)"); pg.wait_for_timeout(900)

if __name__ == '__main__':
    print('══ Q210 · le sol du clair s’assombrit, la peau reste claire ══')
    print('   décidé (Q182, en dur dans le juge) : boule ↔ page %.0f ± %.0f en clair · contour ≥ %.0f · plancher des îles ΔE %.0f'
          % (BOULE_CLAIR, TOL, CONTOUR_MIN, PLANCHER))
    RES = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        for page in range(PAGES):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(URL, timeout=300000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(1400)
            pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(120):
                pg.wait_for_timeout(250)
                e = pg.evaluate("()=>window._aura?_aura.etat():null")
                if e and e['pret'] and e['frames'] > 20: break
            pg.wait_for_timeout(800)
            pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); pg.wait_for_timeout(800)
            nat = pg.evaluate("()=>(window._auraComp||{}).sol")
            for deg in DEGRES:
                sol = None if deg == 1.00 else [int(round(nat[0] * deg)), int(round(nat[1] * deg)), int(round(nat[2] * deg))]
                for nomP, pc in PEAUX:
                    if deg == 1.00 and pc is not None: continue      # la référence n'a qu'une peau
                    pg.evaluate("(c)=>_aura.regleSol(c)", sol)
                    pg.evaluate("(c)=>_aura.reglePeauC(c)", pc); pg.wait_for_timeout(1700)
                    deux_images(pg)
                    r = pg.evaluate(MESURE, [FOND, FACE])
                    if r: RES.setdefault((deg, nomP), []).append(r)
            pg.evaluate("()=>{_aura.regleSol(null); _aura.reglePeauC(null);}")
            pg.context.close()
        br.close()
    print()
    print('   poil    peau                 boule↔page   contour   îles : plus faible · médiane   sous le plancher')
    for deg in DEGRES:
        for nomP, pc in PEAUX:
            L = RES.get((deg, nomP))
            if not L: continue
            b = sum(x['boule'] for x in L) / len(L)
            ct = sum(x['contour'] for x in L) / len(L)
            toutes = sorted(d['dE'] for x in L for d in x['iles'])
            bas = [d for x in L for d in x['iles'] if d['dE'] < PLANCHER]
            ok = abs(b - BOULE_CLAIR) <= TOL and ct >= CONTOUR_MIN and not bas
            print('   ×%.2f   %-20s %7.1f %s %7.1f %s %7.1f · %6.1f %12s  %s'
                  % (deg, nomP, b, '✓' if abs(b - BOULE_CLAIR) <= TOL else '✗',
                     ct, '✓' if ct >= CONTOUR_MIN else '✗',
                     toutes[0], toutes[len(toutes) // 2], '%d / %d' % (len(bas), len(toutes)),
                     '◀ TIENT TOUT' if ok else ''))
