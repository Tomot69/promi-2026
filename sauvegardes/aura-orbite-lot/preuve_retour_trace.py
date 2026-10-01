# Deux vérifications demandées par Tom sur la correction du retour de l'empreinte (10 sept.) :
#  A · LA DURÉE DU RETOUR, avant/après — on n'échange pas un saut contre une traîne.
#      Appui de 950 ms, lâcher, puis chaque image peinte (vue figée) : écart moyen au repos, en
#      niveaux, sur la zone du doigt. On relève quand il passe sous 50 % et 10 % de l'écart au
#      lâcher, sous 1 niveau (plus rien à l'œil), et quand l'empreinte est retirée.
#  B · LA TRACE NE S'ÉTEINT PAS avec le creux. Une caresse ; une fois le creux refermé et la
#      caresse inscrite : part des pixels de la boule qui la portent, et son amplitude. Puis 5 s
#      plus tard, même vue : elle ne doit pas avoir bougé d'un niveau.
#   python3 preuve_retour_trace.py NOM1=URL1 NOM2=URL2 ...
import sys, statistics as st
from playwright.sync_api import sync_playwright

SEUL_B = '--trace' in sys.argv
VERS = [a.split('=', 1) for a in sys.argv[1:] if '=' in a]
REPS = 3
TX, TY = -0.40, -0.30

SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__snap_'+nom]=
  cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); return cv.width; }"""
# part des pixels de la boule qui changent (> 3 niveaux sur un canal) ET écart moyen en niveaux
DIFFA = r"""([a,b])=>{ const A=window['__snap_'+a], B=window['__snap_'+b]; if(!A||!B||A.length!==B.length) return null;
  const W=Math.round(Math.sqrt(A.length/4)), c=W/2, R=W*0.392; let n=0, ch=0, am=0;
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ if(Math.hypot(x-c,y-c)>R*0.95) continue;
    const i=(y*W+x)*4; n++; const d=(Math.abs(A[i]-B[i])+Math.abs(A[i+1]-B[i+1])+Math.abs(A[i+2]-B[i+2]))/3;
    am+=d; if(Math.abs(A[i]-B[i])>3||Math.abs(A[i+1]-B[i+1])>3||Math.abs(A[i+2]-B[i+2])>3) ch++; }
  return [ch/n, am/n]; }"""
REC = r"""([tx,ty])=>new Promise(res=>{
  const cv=document.getElementById('auBoule'), g=cv.getContext('2d'), W=cv.width, c=W/2, R=W*0.392;
  const zx=c+tx*R, zy=c+ty*R, zr=0.35*R, A=window.__snap_repos;
  const x0=Math.max(0,Math.floor(zx-zr)), y0=Math.max(0,Math.floor(zy-zr));
  const w=Math.min(W,Math.ceil(zx+zr))-x0, h=Math.min(W,Math.ceil(zy+zr))-y0;
  const out=[]; let lastP=-1, apres=0; const t0=performance.now();
  function tick(){ const e=_aura.etat();
    if(e.peints!==lastP){ lastP=e.peints; const d=g.getImageData(x0,y0,w,h).data; let n=0, aR=0;
      for(let yy=0;yy<h;yy+=2) for(let xx=0;xx<w;xx+=2){ if(Math.hypot(x0+xx-zx,y0+yy-zy)>zr) continue; n++;
        const i=(yy*w+xx)*4, j=((y0+yy)*W+x0+xx)*4;
        aR+=(Math.abs(d[i]-A[j])+Math.abs(d[i+1]-A[j+1])+Math.abs(d[i+2]-A[j+2]))/3; }
      out.push([performance.now()-t0, e.emp?e.emp.p:null, aR/n]);
      if(!e.emp && ++apres>=3) return res(out); }
    if(performance.now()-t0>20000) return res(out);
    requestAnimationFrame(tick); }
  requestAnimationFrame(tick); })"""

def premier(seq, cond):
    return next((r[0] / 1000 for r in seq if cond(r)), float('nan'))

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for nom, url in VERS:
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        er = []; pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>setTheme('dark')"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(700)
        def attends(js, ms=15000):
            t = 0
            while t < ms:
                if pg.evaluate(js): return True
                pg.wait_for_timeout(100); t += 100
            return False
        def peintes(n=3):
            p0 = pg.evaluate("()=>_aura.etat().peints"); attends("()=>_aura.etat().peints>=%d" % (p0 + n))
        r = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2,b.width*0.392];}")
        cx, cy, R = r
        L = res[nom] = []
        for k in range(REPS):
            # A · la durée du retour
            attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp&&!e.attente;}")
            if SEUL_B:
                pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); const e=_aura.etat(); window.__vue=[e.lac,e.tan];}")
                A = dict(a0=0, t50=0, t10=0, t1=0, retrait=0, reste=0)
            else:
              attends("()=>{const e=_aura.etat();return !e.vlac&&!e.vtan&&!e.emp&&!e.attente;}")
              pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); const e=_aura.etat(); window.__vue=[e.lac,e.tan];}")
              peintes(); pg.evaluate(SNAP, 'repos')
              pg.mouse.move(cx + TX * R, cy + TY * R); pg.mouse.down(); pg.wait_for_timeout(950); pg.mouse.up()
              seq = pg.evaluate(REC, [TX, TY])
              a0 = seq[0][2]
              ret = premier(seq, lambda x: x[1] is None)
              ecart_fin = next((seq[i - 1][2] for i, x in enumerate(seq) if x[1] is None and i), float('nan'))
              A = dict(a0=a0, t50=premier(seq, lambda x: x[2] <= 0.5 * a0), t10=premier(seq, lambda x: x[2] <= 0.1 * a0),
                       t1=premier(seq, lambda x: x[2] <= 1.0), retrait=ret, reste=ecart_fin)
            # B · la trace survit au creux
            attends("()=>{const e=_aura.etat();return !e.emp&&!e.attente;}")
            pg.evaluate("()=>{_aura.relisse(); _aura.vue(window.__vue[0],window.__vue[1]);}")
            peintes(); pg.evaluate(SNAP, 'nu')
            n0 = pg.evaluate("()=>_aura.etat().traces")
            pg.mouse.move(cx - 0.5 * R, cy + 0.1 * R); pg.mouse.down()
            for j in range(1, 21): pg.mouse.move(cx - 0.5 * R + j * 0.05 * R, cy + 0.1 * R); pg.wait_for_timeout(35)
            pg.wait_for_timeout(150); pg.mouse.up()
            attends("()=>_aura.etat().traces>%d" % n0)
            attends("()=>{const e=_aura.etat();return !e.emp&&!e.attente;}")
            emp_t1 = pg.evaluate("()=>_aura.etat().emp")
            pg.evaluate("()=>_aura.vue(window.__vue[0],window.__vue[1])"); peintes()
            pal = [pg.evaluate("()=>_aura.etat().palier")]
            pg.evaluate(SNAP, 't1'); t1 = pg.evaluate(DIFFA, ['nu', 't1'])
            pg.wait_for_timeout(5000)
            pg.evaluate("()=>_aura.vue(window.__vue[0],window.__vue[1])"); peintes()
            pal.append(pg.evaluate("()=>_aura.etat().palier"))
            pg.evaluate(SNAP, 't2'); t2 = pg.evaluate(DIFFA, ['t1', 't2']); t2n = pg.evaluate(DIFFA, ['nu', 't2'])
            pg.evaluate("()=>{_aura.relisse(); _aura.vue(window.__vue[0],window.__vue[1]);}"); peintes()
            pal.append(pg.evaluate("()=>_aura.etat().palier"))
            pg.evaluate(SNAP, 'nu2'); t2r = pg.evaluate(DIFFA, ['nu2', 't2'])
            B = dict(traces=pg.evaluate("()=>_aura.etat().traces"), emp=emp_t1, part=t1[0], amp=t1[1],
                     bouge_5s=t2[1], part_5s=t2n[0], pal=pal, part_5r=t2r[0], amp_5r=t2r[1])
            L.append((A, B))
            print('%-8s #%d  A: écart au lâcher %.1f niv · 50 %% à %.2f s · 10 %% à %.2f s · < 1 niveau à %.2f s · retirée à %.2f s (restait %.2f niv)'
                  % (nom, k + 1, A['a0'], A['t50'], A['t10'], A['t1'], A['retrait'], A['reste']))
            print('%-8s #%d  B: %d caresse(s), creux %s · la trace : %.1f %% des pixels, %.2f niv · 5 s après : l\'image bouge de %.3f niv · paliers %s · la trace à 5 s, contre un relissage même vue même palier : %.1f %% des pixels, %.2f niv'
                  % (nom, k + 1, B['traces'], 'refermé' if not B['emp'] else 'OUVERT', 100 * B['part'], B['amp'], B['bouge_5s'], B['pal'], 100 * B['part_5r'], B['amp_5r']))
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(false);}")
        if er: print(nom, 'ERREURS JS', er[:3])
        pg.close()
    b.close()

print('\n%-8s %8s %8s %10s %10s %10s   %8s %8s %10s %8s' % ('', '50 %', '10 %', '< 1 niv', 'retirée', 'restait', 'trace %', 'niv', 'à 5 s %', 'niv'))
for nom, L in res.items():
    m = lambda f: st.mean(f(x) for x in L)
    print('%-8s %7.2fs %7.2fs %9.2fs %9.2fs %8.2f n   %7.1f%% %8.2f %9.1f%% %8.2f' % (
        nom, m(lambda x: x[0]['t50']), m(lambda x: x[0]['t10']), m(lambda x: x[0]['t1']), m(lambda x: x[0]['retrait']),
        m(lambda x: x[0]['reste']), 100 * m(lambda x: x[1]['part']), m(lambda x: x[1]['amp']), 100 * m(lambda x: x[1]['part_5r']), m(lambda x: x[1]['amp_5r'])))
