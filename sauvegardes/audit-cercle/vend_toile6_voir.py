# v6 — 120 germes, vraies pastilles, « Cercle » en mauve, trois essais de second bouton.
# ET UNE PREUVE : l'attribution par seaux rend-elle EXACTEMENT la règle brute ?
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile6')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile6.html'
PREUVE=r"""()=>{
  const own=window._vendOwn, S=window._vendSeeds, dpr=window._vendDpr;
  if(!own||!S) return 'rien publié';
  const W=Math.round(346*dpr), H=Math.round(206*dpr);
  let n=0, faux=0;
  for(let k=0;k<4000;k++){
    const x=(Math.random()*W)|0, y=(Math.random()*H)|0;
    const lx=(x+0.5)/dpr, ly=(y+0.5)/dpr;
    let bd=1e18, bi=0;
    for(let q=0;q<S.length;q++){ const ex=lx-S[q][0], ey=ly-S[q][1], d=ex*ex+ey*ey; if(d<bd){bd=d;bi=q;} }
    n++; if(own[y*W+x]!==bi) faux++;
  }
  return {testes:n, divergences:faux}; }"""
MES=r"""()=>{
  const v=window._vendToile||{};
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let fond=null, teintes=0;
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data;
    const cs=getComputedStyle(document.querySelector('#pcCadre .pc-toile')).backgroundColor.match(/\d+/g).map(Number);
    let nf=0,n=0,vides=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++;
      if(d[i+3]<10){ vides++; continue; }          /* ⚠ SANS L'ALPHA je comptais un canevas TRANSPARENT comme « 0 % de fond » */
      if(Math.abs(d[i]-cs[0])<10&&Math.abs(d[i+1]-cs[1])<10&&Math.abs(d[i+2]-cs[2])<10) nf++;
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    fond=+(100*(nf+vides)/n).toFixed(1); teintes=Object.keys(cnt).length; }
  const ch=[...document.querySelectorAll('#pcCadre .pc-ch')];
  const h2=document.querySelector('#pcCadre .pc-h .pc-h2'), h1=document.querySelector('#pcCadre .pc-h .pc-h1');
  const s2=document.querySelector('#pcCadre .pc-sub .pc-s2');
  const yr=document.querySelector('#pcCadre #buyYear'), ys=getComputedStyle(yr);
  return {vend:v, fond, teintes,
    pastilles:ch.map(c=>({m:c.getAttribute('data-m'), dalle:c.getAttribute('data-dalle'),
                          matiere:c.getAttribute('data-matiere'), px:[c.width,c.height],
                          css:[getComputedStyle(c).width,getComputedStyle(c).height]})),
    titre:{le:getComputedStyle(h1).color, cercle:getComputedStyle(h2).color},
    sous:{police:getComputedStyle(s2).fontFamily.split(',')[0], graisse:getComputedStyle(s2).fontWeight, couleur:getComputedStyle(s2).color},
    option:{fond:ys.backgroundColor, filet:ys.borderTopColor, encre:ys.color}}; }"""
def ouvre(pg, b):
    pg.evaluate("(b)=>{ window._vendBouton=b; try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }", b)
    pg.wait_for_timeout(420)
    pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
    pg.wait_for_timeout(2400)
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th)
        for b in ('1','2','3'):
            ouvre(pg,b); m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_b%s.png'%(th,b)))
            if b=='1':
                tot=sum(v['matieres'].values())
                print('   %d germes (%d colorés) · fond visible %s%% · %d teintes · %d ms · Touffe %.0f %% · %d mondes'
                      % (v['germes'], v['colores'], m['fond'], m['teintes'], v['ms'],
                         100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
                print('   PREUVE seaux vs règle brute :', json.dumps(pg.evaluate(PREUVE), ensure_ascii=False))
                print('   titre : « Le » %s · « Cercle » %s · mauve écart %s' % (m['titre']['le'], m['titre']['cercle'], v['mauve']['ecart']))
                print('   sous-titre : %s %s %s' % (m['sous']['police'], m['sous']['graisse'], m['sous']['couleur']))
                for q in m['pastilles']:
                    print('   pastille %-9s dalle #%s · canevas %s → %s · matière %s' % (q['m'], q['dalle'], q['px'], q['css'], q['matiere']))
            print('   bouton %s · fond %s · filet %s · encre %s' % (b, m['option']['fond'], m['option']['filet'], m['option']['encre']))
        pg.context.close()
    br.close()
