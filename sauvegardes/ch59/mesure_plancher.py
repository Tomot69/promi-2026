# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 59 · COMBIEN DE DALLES TOMBENT SOUS LE PLANCHER, SUR N CHARGEMENTS
# La couleur d'une dalle est TIRÉE AU HASARD à chaque chargement (`cc()`, Math.random — code de la Toile) :
# une seule passe ne prouve rien, ni dans un sens ni dans l'autre (CLAUDE §7, « un contrôle qui prend un
# défaut aléatoire fait son travail »). On compte donc sur N chargements, dans les deux thèmes, avec
# L'INSTRUMENT DU JUGE : ΔE (CIELAB) entre la sphère AVEC l'île et la sphère SANS, au cœur de l'île, à la
# même vue figée (§7 : sur un objet qui tourne, on compare à l'angle, jamais à l'instant).
#   python3 mesure_plancher.py <url> [n]
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys, math
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
N   = int(sys.argv[2]) if len(sys.argv) > 2 else 10
PLANCHER, FACE = 15.0, 0.35

DALLES = r"""([fond, FACE])=>{
  const cv=document.getElementById('auBoule'), W=cv.width, d=window.__m_avec, s0=window.__m_sans;
  if(!d||!s0) return null;
  const c=W/2, R=W*0.392;
  const comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255);
  const lin=v=>{v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);}, fl=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;
  const lab=(r,g,b)=>{ r=lin(r); g=lin(g); b=lin(b);
    const X=(0.4124*r+0.3576*g+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g+0.0722*b, Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883;
    const fx=fl(X), fy=fl(Y), fz=fl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; };
  const e=_aura.etat(), C=window._auraComp||{}, T=C.iles||[];
  const B=OrbiteMoteur.batIles(C.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan);
  const out=[];
  B.iles.forEach((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct;
    if(Z<=FACE) return;
    const px=c+X*R, py=c+Y*R, rd=Math.max(6, I.r*R*0.5*Z); let n=0; const LA=[0,0,0], LS=[0,0,0];
    for(let y=Math.floor(py-rd); y<=py+rd; y++) for(let x=Math.floor(px-rd); x<=px+rd; x++){
      if(x<0||y<0||x>=W||y>=W||Math.hypot(x-px,y-py)>rd) continue;
      const i=(y*W+x)*4; n++;
      const A=lab(comp(d,i,0),comp(d,i,1),comp(d,i,2)), S=lab(comp(s0,i,0),comp(s0,i,1),comp(s0,i,2));
      for(let t=0;t<3;t++){ LA[t]+=A[t]; LS[t]+=S[t]; } }
    if(!n) return;
    out.push({titre:(T[k]&&T[k].titre)||('île '+k),
              dE:+Math.hypot(LA[0]/n-LS[0]/n, LA[1]/n-LS[1]/n, LA[2]/n-LS[2]/n).toFixed(1)}); });
  return {dalles:out, ch59:e.ch59||null, mesure:e.ch59mesure||null}; }"""

def une_passe(pg, th):
    pg.goto(URL, timeout=180000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(90):
        pg.wait_for_timeout(200)
        e = pg.evaluate("()=>window._aura?_aura.etat():null")
        if e and e['pret'] and e['frames'] > 12: break
    pg.wait_for_timeout(500)
    # la même vue pour tout le monde, rotation figée
    pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
    pg.evaluate("()=>_aura.sansIles(true)"); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
    pg.evaluate("()=>_aura.sansIles(false)"); pg.wait_for_timeout(600)
    fond = [22, 23, 27] if th == 'dark' else [244, 238, 225]
    return pg.evaluate(DALLES, [fond, FACE])

if __name__ == '__main__':
    print('══ %s · %d chargements par thème · plancher ΔE %.0f ══' % (URL, N, PLANCHER))
    tot = {'dark': [0, 0, []], 'light': [0, 0, []]}   # [dalles sous le plancher, chargements fautifs, min par passe]
    cede = 0
    PAIRES = []
    MASQUE = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        for i in range(N):
            for th in ('dark', 'light'):
                pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
                try: r = une_passe(pg, th)
                except Exception as ex: print('   %2d %-6s ERREUR %s' % (i + 1, th, str(ex)[:70])); pg.context.close(); continue
                if not r: print('   %2d %-6s pas de masque' % (i + 1, th)); pg.context.close(); continue
                bas = [d for d in r['dalles'] if d['dE'] < PLANCHER]
                mn = min((d['dE'] for d in r['dalles']), default=None)
                tot[th][0] += len(bas); tot[th][1] += 1 if bas else 0
                if mn is not None: tot[th][2].append(mn)
                c = r.get('ch59') or {}
                nc = sum(1 for v in c.values() if v.get('cede'))
                MS = r.get('mesure') or {}
                if MS:
                    par = {x['titre']: x for x in MS.get('iles', []) if x.get('titre')}
                    for d in r['dalles']:
                        v = par.get(d['titre'])
                        if v and v.get('dE') is not None: MASQUE.append((th, d['titre'], v['dE'], d['dE'], v.get('rang')))
                cede += nc
                print('   %2d %-6s %d île(s) · la plus faible ΔE %5s · sous le plancher : %-38s · cèdent %d'
                      % (i + 1, th, len(r['dalles']), mn, ', '.join('%s %.1f' % (d['titre'][:18], d['dE']) for d in bas) or '—', nc))
                # LE COUPLE (hors lumière → à l'écran) : c'est lui qui dit si le garde-fou peut prédire
                par = {}
                for v in c.values():
                    if v.get('titre'): par[v['titre']] = v
                for d in r['dalles']:
                    v = par.get(d['titre'])
                    if v: PAIRES.append((th, d['titre'], v.get('dE'), d['dE'], bool(v.get('cede')), v.get('apres'), v.get('plein')))
                pg.context.close()
        br.close()
    print()
    for th in ('dark', 'light'):
        n, f, mins = tot[th]
        print('   %-6s %d dalle(s) sous le plancher · %d chargement(s) fautif(s) sur %d · la plus faible médiane %.1f, pire %.1f'
              % (th, n, f, N, sorted(mins)[len(mins) // 2] if mins else -1, min(mins) if mins else -1))
    print('   %d dalle(s) ont CÉDÉ leur teinte (total sur toutes les passes)' % cede)
    if MASQUE:
        print()
        print('   ══ le masque (ce que l’app mesure) contre l’écran (ce que le juge mesure) ══')
        for th in ('dark', 'light'):
            L = [x for x in MASQUE if x[0] == th and x[2] > 0]
            if not L: continue
            rr = sorted(x[3] / x[2] for x in L)
            print('   %-6s %d couple(s) · rapport écran/masque : médiane %.2f, min %.2f, max %.2f'
                  % (th, len(L), rr[len(rr) // 2], rr[0], rr[-1]))
            for x in sorted(L, key=lambda y: y[3])[:5]:
                print('      %-26s masque %6.1f → écran %5.1f  (×%.2f) · rang %s'
                      % (x[1][:26], x[2], x[3], x[3] / x[2], x[4]))
    if PAIRES:
        print()
        print('   ══ le couple « hors lumière → à l’écran » (c’est lui qui dit si le garde-fou peut prédire) ══')
        for th in ('dark', 'light'):
            L = [x for x in PAIRES if x[0] == th and x[2] is not None and x[2] > 0]
            if not L: continue
            r = sorted(x[3] / x[2] for x in L)
            print('   %-6s %d couple(s) · rapport écran/hors-lumière : médiane %.2f, min %.2f, max %.2f'
                  % (th, len(L), r[len(r) // 2], r[0], r[-1]))
            pl = [x for x in L if x[6]]
            if pl:
                bas = sorted(pl, key=lambda y: y[3])[:len(pl) // 3 or 1]
                hau = sorted(pl, key=lambda y: y[3])[-(len(pl) // 3 or 1):]
                print('      la part PLEINE de la dalle : le tiers le moins lisible %.0f %% · le tiers le plus lisible %.0f %%'
                      % (100 * sum(x[6] for x in bas) / len(bas), 100 * sum(x[6] for x in hau) / len(hau)))
            for x in sorted(L, key=lambda y: y[3])[:6]:
                print('      %-26s hors lumière %6.1f → écran %5.1f  (×%.2f) · dalle pleine à %4.0f %%%s'
                      % (x[1][:26], x[2], x[3], x[3] / x[2], 100 * (x[6] or 0), '  a cédé' if x[4] else ''))
