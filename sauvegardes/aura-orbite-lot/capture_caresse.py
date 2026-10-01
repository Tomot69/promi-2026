# La capture de la CARESSE, refaite : la première ne montrait rien — le glissement tourne la sphère,
# les îles partaient derrière et la trace (poil couché, 1,5 niveau en moyenne) ne se voyait pas.
# Ici : vue notée AVANT la caresse, remise et figée APRÈS (trace inscrite, creux refermé), puis :
#  · aura_{th}_caresse.png       l'écran, à 2×, la trace face à nous
#  · aura_{th}_caresse_carte.png  la même boule avant | après | l'écart ×8 (une carte, dite comme telle)
import os
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ICI, 'finales')
SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__c_'+nom]=cv.toDataURL('image/png');
  window['__d_'+nom]=cv.getContext('2d').getImageData(0,0,cv.width,cv.height); return cv.width; }"""
CARTE = r"""([bg])=>{ const A=window.__d_avant, B=window.__d_apres, W=A.width, H=A.height;
  const k=document.createElement('canvas'); k.width=W*3+40; k.height=H+60; const q=k.getContext('2d');
  q.fillStyle=bg; q.fillRect(0,0,k.width,k.height);
  const pose=(D,x)=>{ const t=document.createElement('canvas'); t.width=W; t.height=H; t.getContext('2d').putImageData(D,0,0); q.drawImage(t,x,0); };
  pose(A,0); pose(B,W+20);
  const E=q.createImageData(W,H); let n=0, m=0;
  for(let i=0;i<A.data.length;i+=4){ const d=(Math.abs(A.data[i]-B.data[i])+Math.abs(A.data[i+1]-B.data[i+1])+Math.abs(A.data[i+2]-B.data[i+2]))/3;
    const v=Math.min(255,d*8); E.data[i]=v; E.data[i+1]=v*0.85; E.data[i+2]=v*0.4; E.data[i+3]=255; if(d>3) n++; m++; }
  const t=document.createElement('canvas'); t.width=W; t.height=H; t.getContext('2d').putImageData(E,0,0); q.drawImage(t,2*W+40,0);
  q.fillStyle=bg==='#16171B'?'#F4EEE1':'#16171B'; q.font='bold 30px sans-serif';
  q.fillText('avant la caresse',20,H+42); q.fillText('après — trace inscrite',W+40,H+42); q.fillText('l\'écart, amplifié ×8',2*W+60,H+42);
  return k.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def attends(js, ms=20000):
        t = 0
        while t < ms:
            if pg.evaluate(js): return True
            pg.wait_for_timeout(100); t += 100
    def peintes(n=4):
        p0 = pg.evaluate("()=>_aura.etat().peints"); attends("()=>_aura.etat().peints>=%d" % (p0 + n))
    for th, bg in (('dark', '#16171B'), ('light', '#F4EEE1')):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        attends("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"); pg.wait_for_timeout(800)
        attends("()=>{const e=_aura.etat();return !e.emp&&!e.attente&&!e.vlac&&!e.vtan;}")
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); const e=_aura.etat(); window.__vue=[e.lac,e.tan];}")
        peintes(); pg.evaluate(SNAP, 'avant')
        r = pg.evaluate("()=>{const r=document.getElementById('auBoule').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.width*0.392];}")
        cx, cy, R = r
        pg.mouse.move(cx - 0.5 * R, cy + 0.1 * R); pg.mouse.down()
        for k in range(1, 21): pg.mouse.move(cx - 0.5 * R + k * 0.05 * R, cy + 0.1 * R); pg.wait_for_timeout(35)
        pg.wait_for_timeout(150); pg.mouse.up()
        attends("()=>_aura.etat().traces>0"); attends("()=>{const e=_aura.etat();return !e.emp&&!e.attente;}")
        pg.evaluate("()=>_aura.vue(window.__vue[0],window.__vue[1])"); peintes(6)
        pg.evaluate(SNAP, 'apres')
        pg.query_selector('#device').screenshot(path=os.path.join(OUT, 'aura_%s_caresse.png' % th))
        u = pg.evaluate(CARTE, [bg])
        pv = b.new_page(viewport={'width': 1400, 'height': 700})
        pv.set_content('<body style="margin:0;background:%s"><img src="%s" style="width:100%%"></body>' % (bg, u)); pv.wait_for_timeout(300)
        pv.screenshot(path=os.path.join(OUT, 'aura_%s_caresse_carte.png' % th), full_page=True); pv.close()
        print(th, 'caresses :', pg.evaluate("()=>_aura.etat().traces"))
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(false);}")
    print('ERREURS JS', er[:3]); b.close()
