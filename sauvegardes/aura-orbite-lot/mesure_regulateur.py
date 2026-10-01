# Le régulateur de densité, mesuré — les trois questions de Tom (10 sept.) :
#  B · LE SAUT DE PALIER EN MOUVEMENT : premier passage à un palier jamais servi, sphère qui tourne —
#      la plus longue image autour du changement (le semis et le cache se refont).
#  A · EST-CE QUE ÇA SE VOIT : la même vue figée à 110 000, 90 000, 75 000 poils, deux thèmes —
#      part et amplitude des pixels qui changent, luminance moyenne, planche à 2× pour l'œil.
#  C · QUAND ÇA SE DÉCLENCHE, ET SI ÇA REMONTE : processeur ralenti ×4 et un lancer aussitôt ;
#      chaque changement de palier est journalisé avec l'état du geste à cet instant ; puis on
#      rend le processeur et on attend la remontée.
#   python3 mesure_regulateur.py URL SORTIE_DIR
import sys, os, json, base64, time
from playwright.sync_api import sync_playwright

URL = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)

SNAPL = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__s_'+nom]=
  cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window['__u_'+nom]=cv.toDataURL('image/png'); return cv.width; }"""
# part (> 3 niveaux), amplitude moyenne (niveaux) sur la boule ; et luminance moyenne de chaque image
# COMPOSÉE sur le fond de l'écran (le canevas est transparent, le fond se voit entre les poils)
DIFF = r"""([a,b,fond])=>{ const A=window['__s_'+a], B=window['__s_'+b];
  const W=Math.round(Math.sqrt(A.length/4)), c=W/2, R=W*0.392; let n=0, ch=0, am=0, la=0, lb=0;
  const comp=(D,i,k)=>{ const al=D[i+3]/255; return D[i+k]*al+fond[k]*(1-al); };
  const lum=(D,i)=>0.2126*comp(D,i,0)+0.7152*comp(D,i,1)+0.0722*comp(D,i,2);
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ if(Math.hypot(x-c,y-c)>R*0.95) continue; const i=(y*W+x)*4; n++;
    const d=(Math.abs(comp(A,i,0)-comp(B,i,0))+Math.abs(comp(A,i,1)-comp(B,i,1))+Math.abs(comp(A,i,2)-comp(B,i,2)))/3;
    am+=d; if(d>3) ch++; la+=lum(A,i); lb+=lum(B,i); }
  return {part:ch/n, amp:am/n, lumA:la/n, lumB:lb/n}; }"""
# journal image par image : [ms, palier, dt réel, ms peintre, vlac, vtan, creux?, doigt?]
JOURNAL = r"""(ms)=>new Promise(res=>{ const out=[], t0=performance.now(); let k0=_aura.etat().tick;
  (function f(){ const e=_aura.etat();
    if(e.tick!==k0){ k0=e.tick; out.push([Math.round(performance.now()-t0), e.palier, e.dtReel, e.dernier, e.vlac, e.vtan, !!e.emp, !!e.prise]); }
    if(performance.now()-t0<ms) requestAnimationFrame(f); else res(out); })(); })"""
LANCE = r"""async ([x0,y0,dx,n,pas])=>{ const t=document.querySelector('#auraScreen .au-prise');
  const o=(x)=>({pointerId:7,pointerType:'mouse',isPrimary:true,clientX:x,clientY:y0,bubbles:true,cancelable:true,buttons:1});
  t.dispatchEvent(new PointerEvent('pointerdown',o(x0)));
  for(let k=1;k<=n;k++){ await new Promise(r=>setTimeout(r,pas)); t.dispatchEvent(new PointerEvent('pointermove',o(x0+dx*k/n))); }
  t.dispatchEvent(new PointerEvent('pointerup',o(x0+dx))); return _aura.etat().elan; }"""

def page(b):
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    return pg

def ouvre(pg, th):
    pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(100):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(800)

def attends(pg, js, ms=20000):
    t = 0
    while t < ms:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(100); t += 100
    return False

def peintes(pg, n=4):
    p0 = pg.evaluate("()=>_aura.etat().peints"); attends(pg, "()=>_aura.etat().peints>=%d" % (p0 + n))

R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    # ── B · le premier passage à un palier, en mouvement ─────────────────────────────
    pg = page(b)
    pg.evaluate("()=>localStorage.setItem('promi_orbite_palier','0')")
    ouvre(pg, 'dark')
    pg.evaluate("()=>{_aura.palier(0);}"); pg.wait_for_timeout(1500)
    jr = pg.evaluate("""async ()=>{ const J=(%s)(3000); setTimeout(()=>_aura.palier(1), 1000); return await J; }""" % JOURNAL)
    av = [x for x in jr if x[0] < 1000]; ap = [x for x in jr if x[0] >= 1000]
    R['B'] = dict(avant_max_ms=max(x[2] for x in av) * 1000, apres_max_ms=max(x[2] for x in ap) * 1000,
                  peintre_max=max(x[3] for x in ap), palier_fin=jr[-1][1],
                  moment=next((x[0] for x in jr if x[1] == 90000), None))
    print('B · premier passage 110 000 → 90 000, sphère qui tourne : plus longue image avant %.0f ms, AU CHANGEMENT %.0f ms (peintre %.0f ms)'
          % (R['B']['avant_max_ms'], R['B']['apres_max_ms'], R['B']['peintre_max']))
    pg.close()
    # ── A · la même vue, trois paliers, deux thèmes ─────────────────────────────────
    R['A'] = {}
    pg = page(b)
    for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
        ouvre(pg, th)
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); const e=_aura.etat(); window.__vue=[e.lac,e.tan];}")
        for i, N in enumerate((110000, 90000, 75000)):
            pg.evaluate("(i)=>{_aura.palier(i); _aura.vue(window.__vue[0],window.__vue[1]);}", i)
            attends(pg, "()=>_aura.etat().palier===%d" % N); peintes(pg, 6)
            pg.evaluate(SNAPL, '%s%d' % (th, N))
            pg.query_selector('#auBoule').screenshot(path=os.path.join(OUT, 'palier_%s_%d.png' % (th, N)))
        for N in (90000, 75000):
            d = pg.evaluate(DIFF, ['%s110000' % th, '%s%d' % (th, N), fond])
            R['A']['%s %d' % (th, N)] = d
            print('A · %-5s 110 000 → %6d : %.1f %% des pixels changent, %.1f niveaux en moyenne · luminance %.1f → %.1f (%+.1f)'
                  % (th, N, 100 * d['part'], d['amp'], d['lumA'], d['lumB'], d['lumB'] - d['lumA']))
        # la planche : les trois paliers, la boule entière puis le centre agrandi ×3
        u = [pg.evaluate("(k)=>window['__u_'+k]", '%s%d' % (th, N)) for N in (110000, 90000, 75000)]
        bg = '#16171B' if th == 'dark' else '#F4EEE1'; fg = '#F4EEE1' if th == 'dark' else '#16171B'
        cel = ''.join('<div style="display:inline-block;margin:0 10px"><div style="font:bold 26px sans-serif;color:%s;padding:8px 0">%s poils</div>'
                      '<div style="width:420px;height:420px;background:%s url(%s) center/420px 420px no-repeat"></div>'
                      '<div style="width:420px;height:420px;margin-top:10px;background:%s url(%s) 50%% 42%%/1260px 1260px no-repeat;image-rendering:pixelated"></div></div>'
                      % (fg, lbl, bg, x, bg, x) for lbl, x in zip(('110 000', '90 000', '75 000'), u))
        pv = b.new_page(viewport={'width': 1360, 'height': 960})
        pv.set_content('<body style="margin:0;padding:10px;background:%s">%s</body>' % (bg, cel)); pv.wait_for_timeout(300)
        pv.screenshot(path=os.path.join(OUT, 'paliers_%s.png' % th), full_page=True); pv.close()
        pg.evaluate("()=>{_aura.fige(false); _aura.palier(0);}")
    pg.close()
    # ── C · sous charge : quand ça cède, et si ça remonte ────────────────────────────
    pg = page(b)
    pg.evaluate("()=>localStorage.setItem('promi_orbite_palier','0')")
    ouvre(pg, 'dark')
    pg.evaluate("()=>{_aura.relisse(); _aura.palier(0);}"); pg.wait_for_timeout(2500)
    cdp = pg.context.new_cdp_session(pg)
    bx = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.width*0.392];}")
    cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
    t0 = time.time()
    J = pg.evaluate_handle("(ms)=>{ window.__J=(%s)(ms); return 1; }" % JOURNAL, 26000)
    pg.evaluate(LANCE, [bx[0] - 0.3 * bx[2], bx[1], 0.6 * bx[2], 6, 16])
    attends(pg, "()=>_aura.etat().palier===75000", 22000)
    t_bas = time.time() - t0
    cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
    jr = pg.evaluate("async ()=>await window.__J")
    ch = []
    for a, c in zip(jr, jr[1:]):
        if c[1] != a[1]: ch.append(dict(ms=c[0], de=a[1], a=c[1], vlac=round(c[4], 3), vtan=round(c[5], 3), creux=c[6], doigt=c[7], image_ms=round(c[2] * 1000)))
    t1 = time.time()
    J2 = pg.evaluate("(ms)=>(%s)(ms)" % JOURNAL, 30000)
    ch2 = []
    for a, c in zip(J2, J2[1:]):
        if c[1] != a[1]: ch2.append(dict(ms=c[0], de=a[1], a=c[1], image_ms=round(c[2] * 1000)))
    R['C'] = dict(cede=ch, remonte=ch2, fin=pg.evaluate("()=>_aura.etat().palier"), elan_fin=next((x[0] for x in jr if x[4] == 0 and x[0] > 300), None))
    print('C · sous ×4, un lancer au départ (élan éteint à %s ms) :' % R['C']['elan_fin'])
    for c in ch: print('    à %5d ms  %6d → %6d · élan %s (vlac %.3f) · creux %s · doigt %s · cette image : %d ms'
                       % (c['ms'], c['de'], c['a'], 'EN COURS' if c['vlac'] or c['vtan'] else 'éteint', c['vlac'], c['creux'], c['doigt'], c['image_ms']))
    print('    processeur rendu → sur 30 s :')
    for c in ch2: print('    à %5d ms  %6d → %6d · cette image : %d ms' % (c['ms'], c['de'], c['a'], c['image_ms']))
    print('    palier à la fin : %s' % R['C']['fin'])
    pg.close(); b.close()
json.dump(R, open(os.path.join(OUT, 'regulateur.json'), 'w'), indent=1, ensure_ascii=False)
print('planches :', sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
