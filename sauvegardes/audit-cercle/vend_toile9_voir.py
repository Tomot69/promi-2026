# v9 — LA TOILE EST FAITE DE VRAIES DALLES : un rendu du moteur par cellule, découpé sur son polygone exact.
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile9')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile9.html'
MES=r"""()=>{
  const v=window._vendToile||{};
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let pale=null, teintes=0, vide=null;
  if(cv&&cv.width){ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    const pg=getComputedStyle(document.getElementById('plusScreen')).backgroundColor.match(/\d+/g).map(Number);
    let np=0,n=0,nv=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++;
      if(d[i+3]<10){ nv++; continue; }
      if(Math.abs(d[i]-pg[0])<14&&Math.abs(d[i+1]-pg[1])<14&&Math.abs(d[i+2]-pg[2])<14) np++;
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    pale=+(100*np/n).toFixed(1); vide=+(100*nv/n).toFixed(2); teintes=Object.keys(cnt).length; }
  const mo=document.querySelector('#pcCadre #buyMonth');
  const yr=document.querySelector('#pcCadre #buyYear');
  return {vend:v, pale, vide, teintes, ombre:getComputedStyle(mo).boxShadow,
          option:{fond:getComputedStyle(yr).backgroundColor, encre:getComputedStyle(yr).color}}; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th); sigs=[]
        for k in range(2):
            pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
            pg.wait_for_timeout(420)
            pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
            pg.wait_for_timeout(3400)
            m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            if not v.get('parCellule'): print('   ⚠ PAS le rendu par cellule :', json.dumps(v)[:200]); continue
            sigs.append(v['sig'])
            tot=sum(v['matieres'].values())
            print('   o%d · %d germes, %d cellules peintes · %s sommets en moyenne · Toile %d ms (total %d ms)'
                  % (k+1, v['germes'], v['cellulesPeintes'], v['sommetsMoyens'], v['msToile'], v['ms']))
            print('        vide %s %% · « comme la page » %s %% · %d teintes · Touffe %.0f %% · %d mondes'
                  % (m['vide'], m['pale'], m['teintes'], 100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
            if k==0: print('        ombre du bouton %s · option fond %s encre %s' % (m['ombre'], m['option']['fond'], m['option']['encre']))
        print('   → deux ouvertures distinctes : %s' % (len(set(sigs))==2))
        pg.context.close()
    br.close()
