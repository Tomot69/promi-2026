#!/usr/bin/env python3
"""
redteam_couronne.py — LA COURONNE DE LA PELOTE RESPIRE, ET RIEN D'AUTRE (v115, Tom).
A · captures à t = 0,3 s (immobile) et t = 4,6 s (maximum) après l'affichage complet de l'Aura : la différence se limite à l'anneau
    des fibres (r ∈ [silhouette − 6 ; silhouette + 0,12 D + 2]) — et elle EXISTE (sinon la couronne ne respire pas). La boule est
    figée (`_aura.fige`) : sur un objet qui tourne on compare à l'angle, jamais à l'instant (CLAUDE.md §8).
B · « Réduire les animations » : deux captures à 5 s d'écart identiques, et la couronne à mi-cycle (s = 1).
C · rien au-delà de 0,12 D : aucun pixel de la couronne hors de silhouette + 0,12 D, à son maximum.
Rougi : python3 redteam_couronne.py sauvegardes/app-avant-v115.html (A) · python3 redteam_couronne.py --fautive-reduit (B)
"""
import sys, os, io, math, shutil, time
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
S=2; CX,CY=195,276.532; RSIL=121.0; LMAX=0.12*232.064
ARG=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
tmp=None
if '/' in ARG: shutil.copy(ARG,'zz-cour.html'); ARG=tmp='zz-cour.html'
if '--fautive-reduit' in sys.argv:
    t=open('app.html',encoding='utf-8').read(); assert "reduit=window.matchMedia('(prefers-reduced-motion: reduce)').matches;" in t
    open('zz-cour.html','w',encoding='utf-8').write(t.replace("reduit=window.matchMedia('(prefers-reduced-motion: reduce)').matches;","reduit=false;")); ARG=tmp='zz-cour.html'
def cap(pg): return Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
def zones(A,B):
    d=ImageChops.difference(A,B).convert('L').point(lambda v:255 if v>10 else 0); px=d.load(); dedans=dehors=0; loin=0
    for y in range(0,d.height):
        for x in range(0,d.width):
            if px[x,y]:
                r=math.hypot(x/S-CX,y/S-CY)
                if RSIL-6<=r<=RSIL+LMAX+2: dedans+=1
                else: dehors+=1
    return dedans,dehors
def attend_t0(pg):
    for _ in range(80):
        e=pg.evaluate("()=>window._couronne?_couronne.etat():null")
        if e and e.get('t0') is not None: return e['t0']
        pg.wait_for_timeout(50)
    return None
ok=True
with sync_playwright() as p:
    b=p.webkit.launch()
    # A · la respiration
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(7000)
    if '--fautive-reduit' not in sys.argv:
        # on ouvre SOI-MÊME et on guette le départ dès le toucher (un utilitaire qui attend 4 s laisse passer le départ)
        pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800)
        pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
        pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}")
        t0=attend_t0(pg)
        if t0 is None:
            print('A ✗ la couronne ne déclare aucun départ (pas de couronne, ou elle ne respire pas)'); ok=False
        else:
            while pg.evaluate("()=>performance.now()") < t0-300: pg.wait_for_timeout(10)
            A=cap(pg); sA=pg.evaluate("()=>_couronne.etat().s")
            while pg.evaluate("()=>performance.now()") < t0+4000: pg.wait_for_timeout(20)
            B=cap(pg); sB=pg.evaluate("()=>_couronne.etat().s")
            dedans,dehors=zones(A,B)
            bonA = dedans>200 and dehors==0 and sB>sA
            print('A %s à 0,3 s s=%.3f · à 4,6 s s=%.3f · pixels changés dans l\'anneau %d · HORS de l\'anneau %d'%('OK' if bonA else '✗',sA,sB,dedans,dehors)); ok=ok and bonA
            # C · l'étendue : rien au-delà de silhouette + 0,12 D, à son maximum
            pg.evaluate("()=>{document.getElementById('auBoule').style.visibility='hidden'}"); C1=cap(pg)
            pg.evaluate("()=>{document.getElementById('auPeloteCouronne').style.visibility='hidden'}"); C0=cap(pg)
            pg.evaluate("()=>{document.getElementById('auBoule').style.visibility='';document.getElementById('auPeloteCouronne').style.visibility=''}")
            d=ImageChops.difference(C1,C0).convert('L').point(lambda v:255 if v>6 else 0); px=d.load(); rmax=0
            for y in range(d.height):
                for x in range(d.width):
                    if px[x,y]: rmax=max(rmax, math.hypot(x/S-CX,y/S-CY))
            bonC = 0 < rmax <= RSIL+LMAX+1
            print('C %s la couronne s\'arrête à %.1f de la silhouette (au plus 0,12 D = %.1f)'%('OK' if bonC else '✗', rmax-RSIL, LMAX)); ok=ok and bonC
    ctx.close()
    # B · Réduire les animations
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=S,reduced_motion='reduce')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(7000)
    ouvre(pg,0); pg.evaluate("()=>{try{_aura.fige(true)}catch(e){}}"); pg.wait_for_timeout(1500)
    A=cap(pg); pg.wait_for_timeout(5000); B=cap(pg)
    dedans,dehors=zones(A,B); s=pg.evaluate("()=>window._couronne?_couronne.etat().s:null")
    bonB = dedans==0 and dehors==0 and s is not None and abs(s-1)<1e-6
    print('B %s « Réduire les animations » : s=%s · pixels changés en 5 s : anneau %d, ailleurs %d'%('OK' if bonB else '✗',s,dedans,dehors)); ok=ok and bonB
    b.close()
if tmp: os.remove(tmp)
print('✅ la couronne respire, et rien d\'autre' if ok else '❌ la couronne ne tient pas sa loi'); sys.exit(0 if ok else 1)
