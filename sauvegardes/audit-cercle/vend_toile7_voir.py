# v7 — pastilles peintes à la taille finale, 150 germes sans cellule neutre, « Rejoins le Cercle »,
# second bouton mauve (2) et terracotta (4). ⚠ le titre doit tenir sur UNE ligne.
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile7')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile7.html'
MES=r"""()=>{
  const v=window._vendToile||{};
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let fond=null, teintes=0, pale=null;
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data;
    const cs=getComputedStyle(document.querySelector('#pcCadre .pc-toile')).backgroundColor.match(/\d+/g).map(Number);
    const pg=getComputedStyle(document.getElementById('plusScreen')).backgroundColor.match(/\d+/g).map(Number);
    let nf=0,np=0,n=0,vides=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++;
      if(d[i+3]<10){ vides++; continue; }
      if(Math.abs(d[i]-cs[0])<12&&Math.abs(d[i+1]-cs[1])<12&&Math.abs(d[i+2]-cs[2])<12) nf++;
      if(Math.abs(d[i]-pg[0])<14&&Math.abs(d[i+1]-pg[1])<14&&Math.abs(d[i+2]-pg[2])<14) np++;
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    fond=+(100*(nf+vides)/n).toFixed(2); pale=+(100*np/n).toFixed(2); teintes=Object.keys(cnt).length; }
  const h=document.querySelector('#pcCadre .pc-h'), hr=h.getBoundingClientRect();
  const ch=[...document.querySelectorAll('#pcCadre .pc-ch')];
  const yr=document.querySelector('#pcCadre #buyYear'), ys=getComputedStyle(yr);
  const a2=document.querySelectorAll('#pcCadre .pc-arg')[1];
  return {vend:v, fond, pale, teintes,
    titre:{txt:h.textContent, h:+(hr.height/s).toFixed(1), lignes:Math.round(hr.height/s/38)},
    pastilles:ch.map(c=>({m:c.getAttribute('data-m'), dalle:c.getAttribute('data-dalle'), k:c.getAttribute('data-echelle'),
       canevas:[c.width,c.height], css:[getComputedStyle(c).width,getComputedStyle(c).height]})),
    arg2:{t:a2.querySelector('b').textContent, d:a2.querySelector('i').textContent},
    option:{txt:yr.textContent, fond:ys.backgroundColor, filet:ys.borderTopColor, encre:ys.color}}; }"""
def ouvre(pg,b):
    pg.evaluate("(b)=>{ window._vendBouton=b; try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }", b)
    pg.wait_for_timeout(420)
    pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
    pg.wait_for_timeout(2600)
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th)
        for b in ('2','4'):
            ouvre(pg,b); m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_b%s.png'%(th,b)))
            if b=='2':
                tot=sum(v['matieres'].values())
                print('   %d germes (%d colorés) · fond+vide %s %% · pixels « pâles comme la page » %s %% · %d teintes · %d ms · Touffe %.0f %% · %d mondes'
                      % (v['germes'], v['colores'], m['fond'], m['pale'], m['teintes'], v['ms'],
                         100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
                print('   TITRE « %s » · hauteur %s → %d ligne(s)  ⚠ doit valoir 1' % (m['titre']['txt'], m['titre']['h'], m['titre']['lignes']))
                print('   arg 2 : « %s » — %s' % (m['arg2']['t'], m['arg2']['d']))
                for q in m['pastilles']:
                    print('   pastille %-9s dalle #%-4s k=%-6s canevas %s → css %s' % (q['m'], q['dalle'], q['k'], q['canevas'], q['css']))
            print('   option b%s « %s » · fond %s · encre %s' % (b, m['option']['txt'], m['option']['fond'], m['option']['encre']))
        pg.context.close()
    br.close()
