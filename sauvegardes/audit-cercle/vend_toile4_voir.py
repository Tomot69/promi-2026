# TOILE ENGENDRÉE — cinq ouvertures, deux thèmes. On mesure la densité, le mélange des matières,
# la variation, le coût, et on déclenche la SIGNATURE AU VRAI DOIGT.
import json, os, itertools
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile4')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile4.html'
MES=r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let fond=null, teintes=0;
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data;
    const cs=getComputedStyle(document.querySelector('#pcCadre .pc-toile')).backgroundColor.match(/\d+/g).map(Number);
    let nf=0, n=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++;
      if(Math.abs(d[i]-cs[0])<10&&Math.abs(d[i+1]-cs[1])<10&&Math.abs(d[i+2]-cs[2])<10) nf++;
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    fond=+(100*nf/n).toFixed(1); teintes=Object.keys(cnt).length; }
  return {vend:window._vendToile||null, fond, teintes,
          eclat:!!document.querySelector('#pcCadre #buyMonth .pc-eclat'),
          pose:document.querySelector('#pcCadre #buyMonth').classList.contains('pc-pose'),
          sig:window._vendSignature||0}; }"""
def ouvre(pg):
    pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
    pg.wait_for_timeout(450)
    pg.evaluate("()=>{ const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2200)
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        ctx=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th); sigs=[]
        for k in range(5):
            ouvre(pg); m=pg.evaluate(MES); v=m['vend']
            if not v: print('   o%d · RIEN PUBLIÉ'%(k+1)); continue
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            sigs.append(v['sig'])
            mats=sorted(v['matieres'].items(), key=lambda x:-x[1])
            print('   o%d · %d germes (%d colorés) · fond visible %s%% · %d teintes · %d ms · matières %s'
                  % (k+1, v['germes'], v['colores'], m['fond'], m['teintes'], v['ms'], mats))
        print('   → 5 semis distincts : %s (%d/5)' % (len(set(sigs))==len(sigs) and len(sigs)==5, len(set(sigs))))
        print('   → éclat du bouton présent : %s · pose jouée : %s' % (m['eclat'], m['pose']))
        # LA SIGNATURE AU VRAI DOIGT
        b=pg.evaluate("()=>{const e=document.querySelector('#pcCadre #buyMonth');const r=e.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2};}")
        avant=pg.evaluate("()=>window._vendSignature||0")
        pg.touchscreen.tap(b['x'], b['y']); pg.wait_for_timeout(180)
        pg.locator('#pcCadre #buyMonth').screenshot(path=os.path.join(OUT,'%s_bouton_signature.png'%th))
        pg.wait_for_timeout(400)
        apres=pg.evaluate("()=>window._vendSignature||0")
        print('   → signature au doigt : %d → %d  (%s)' % (avant, apres, 'DÉCLENCHÉE' if apres>avant else 'PAS DÉCLENCHÉE'))
        ctx.close()
    br.close()
