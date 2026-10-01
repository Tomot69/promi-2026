# LA TOILE EN DALLES SUPERPOSÉES — collection de vraies dalles rendue une fois, poses tirées à chaque ouverture.
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toileA')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toileA.html'
MES=r"""()=>{
  const v=window._vendToile||{};
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let vide=null, teintes=0, plage=null;
  if(cv&&cv.width){ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    let nv=0,n=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++; if(d[i+3]<20){ nv++; continue; }
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    vide=+(100*nv/n).toFixed(2); teintes=Object.keys(cnt).length;
    /* LISIBILITÉ : longueur moyenne des plages d'une même couleur sur une ligne. 1,8 = confetti. */
    const W=cv.width,H=cv.height; let runs=0,tot=0;
    for(let y=4;y<H;y+=8){ let prev=-1,len=0;
      for(let x=0;x<W;x++){ const o=(y*W+x)*4;
        const q=((d[o]>>4)<<8)|((d[o+1]>>4)<<4)|(d[o+2]>>4);
        if(q===prev) len++; else { if(prev>=0){ runs++; tot+=len; } prev=q; len=1; } }
      runs++; tot+=len; }
    plage=+(tot/Math.max(1,runs)).toFixed(1); }
  return {vend:v, vide, teintes, plage}; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)")
        pg.wait_for_timeout(500)
        # on laisse le bâti de fond finir : c'est l'état normal après quelques secondes d'app
        try: pg.wait_for_function("()=>window._vendFond && window._vendFond.faites>=window._vendFond.total", timeout=60000)
        except Exception: pass
        print('══',th); sigs=[]
        for k in range(3):
            pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
            pg.wait_for_timeout(420)
            pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
            pg.wait_for_timeout(2600)
            m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            if not v.get('superposees'): print('   ⚠ pas la superposition :', json.dumps(v)[:180]); continue
            sigs.append(v['sig']); tot=sum(v['matieres'].values())
            print('   o%d · collection %d (%d ms) · %d poses (%d ms) · FOND %s %% · %d teintes · PLAGE %s px · Touffe %.0f %% · %d mondes'
                  % (k+1, v['collection'], v['collectionMs'], v['poses'], v['posesMs'], m['vide'], m['teintes'],
                     m['plage'], 100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
            if k==0: print('        cotes des premières dalles : %s' % v['cotes'])
        print('   → trois ouvertures distinctes : %s' % (len(set(sigs))==3))
        pg.context.close()
    br.close()
