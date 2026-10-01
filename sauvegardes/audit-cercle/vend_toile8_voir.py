# v8 — « Rejoins le Cercle ! », 300 germes, seconde couche terracotta.
# ET UNE PREUVE : doubler les germes ne « dézoome » pas la matière. On rend LE MÊME monde à deux densités
# et on compare la part de pixels du MOTIF : si le motif est ancré en absolu, elle ne bouge pas.
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile8')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile8.html'
PREUVE=r"""()=>{
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const PAL=window.Toile.cols()||[];
  const A=document.createElement('canvas'); A.width=Math.round(W*dpr); A.height=Math.round(H*dpr);
  window.Toile.preview(A,'encre',W,H);
  const tpl=(A.__c.seeds.filter(s=>s.kind!=='gray')[0])||A.__c.seeds[0];
  function rend(n,monde){
    const gc=Math.max(5,Math.round(Math.sqrt(n*W/H))), gr=Math.max(4,Math.round(n/gc));
    const cw=W/gc, ch=H/gr, seeds=[];
    for(let r=0;r<gr;r++) for(let c=0;c<gc;c++){
      const s={}; for(const k in tpl) s[k]=tpl[k];
      s.x=cw*(c+.5); s.y=ch*(r+.5); s.tx=s.x; s.ty=s.y; s.px=null; s.py=null; s.w=0; s.wt=0; s.t0=-99999; s.gc=null;
      s.kind='promi'; s.ci=0; s.c=PAL[0]; seeds.push(s);
    }
    const cv=document.createElement('canvas'); cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    cv.__c={seeds:seeds, th:monde, pw:W, ph:H};
    window.Toile.repaint(cv);
    const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    const pal=PAL[0];
    let motif=0, n2=0;
    for(let i=0;i<d.length;i+=32){ n2++;
      if(Math.abs(d[i]-pal[0])<40&&Math.abs(d[i+1]-pal[1])<40&&Math.abs(d[i+2]-pal[2])<40) motif++; }
    return {germes:seeds.length, cellule:+Math.sqrt(W*H/seeds.length).toFixed(1), motifPct:+(100*motif/n2).toFixed(1)};
  }
  const out={};
  ['braille','sillons','mosaique'].forEach(m=>{ out[m]=[rend(144,m), rend(300,m)]; });
  return out; }"""
MES=r"""()=>{
  const v=window._vendToile||{};
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let pale=null, teintes=0;
  if(cv&&cv.width){ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    const pg=getComputedStyle(document.getElementById('plusScreen')).backgroundColor.match(/\d+/g).map(Number);
    let np=0,n=0; const cnt={};
    for(let i=0;i<d.length;i+=16){ n++;
      if(Math.abs(d[i]-pg[0])<14&&Math.abs(d[i+1]-pg[1])<14&&Math.abs(d[i+2]-pg[2])<14) np++;
      cnt[((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4)]=1; }
    pale=+(100*np/n).toFixed(1); teintes=Object.keys(cnt).length; }
  const h=document.querySelector('#pcCadre .pc-h'), hr=h.getBoundingClientRect();
  const h1=h.querySelector('.pc-h1'), h2=h.querySelector('.pc-h2'), h3=h.querySelector('.pc-h3');
  const mo=document.querySelector('#pcCadre #buyMonth');
  return {vend:v, pale, teintes,
    titre:{txt:h.textContent, lignes:Math.round(hr.height/s/38),
           le:getComputedStyle(h1).color, cercle:getComputedStyle(h2).color, pt:getComputedStyle(h3).color},
    bouton:{ombre:getComputedStyle(mo).boxShadow}}; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th)
        if th=='light':
            P=pg.evaluate(PREUVE)
            print('   PREUVE — doubler les germes ne dézoome pas la matière :')
            for m,(a,b) in P.items():
                print('     %-9s %3d germes (cellule %4.1f) motif %5.1f %%   →   %3d germes (cellule %4.1f) motif %5.1f %%   écart %+.1f pt'
                      % (m, a['germes'], a['cellule'], a['motifPct'], b['germes'], b['cellule'], b['motifPct'], b['motifPct']-a['motifPct']))
        for k in range(2):
            pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
            pg.wait_for_timeout(420)
            pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
            pg.wait_for_timeout(3000)
            m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            tot=sum(v['matieres'].values())
            print('   o%d · %d germes · pixels « comme la page » %s %% · %d teintes · %d ms · Touffe %.0f %% · %d mondes'
                  % (k+1, v['germes'], m['pale'], m['teintes'], v['ms'], 100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
            if k==0:
                print('   TITRE « %s » · %d ligne(s) · « Rejoins le » %s · « Cercle » %s · « ! » %s'
                      % (m['titre']['txt'], m['titre']['lignes'], m['titre']['le'], m['titre']['cercle'], m['titre']['pt']))
                print('   ombre du bouton : %s' % m['bouton']['ombre'])
        pg.context.close()
    br.close()
