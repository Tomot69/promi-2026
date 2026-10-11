# relevé des couleurs RENDUES, zone par zone, pour le tableau b : v118 (578ec80) et l'état courant
import json, sys
from playwright.sync_api import sync_playwright
FICHES=[('Promi à tenir','faire les crêpes'),('Promi en cours','nager le mardi'),('Promi tenue','planter un arbre'),
        ('Chiche tenu à deux','le grand plongeoir'),('Chiche lancé','courir dimanche')]
Z=r"""()=>{ const g=(id)=>document.getElementById(id); const cs=(e)=>e?getComputedStyle(e):null; const dp=g('detailPoster');
  const cv=g('dpTrameCv'); let champ=null; try{ const d=cv.getContext('2d').getImageData(6,6,1,1).data; champ='rgb('+d[0]+', '+d[1]+', '+d[2]+')'; }catch(e){}
  const pl=dp.querySelector('.enh'); const nat=g('dptNat');
  const ring=[...dp.querySelectorAll('canvas.kr-c')][0]; let arcs=[];
  try{ const d=ring.getContext('2d').getImageData(0,0,ring.width,ring.height).data, h={}; let n=0; for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const k=d[i]+','+d[i+1]+','+d[i+2]; h[k]=(h[k]||0)+1; }
    arcs=Object.entries(h).filter(a=>a[1]/n>0.04).sort((a,b)=>b[1]-a[1]).slice(0,4).map(a=>'#'+a[0].split(',').map(v=>(+v).toString(16).padStart(2,'0')).join('').toUpperCase()); }catch(e){}
  /* le trait : la couleur la plus fréquente du canevas qui n'est ni le champ ni le corps, au voisinage de l'onde (data-onde déclarée) */
  let trait=null; try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, W=cv.width, H=cv.height, h={}; const sat=(r,g_,b)=>Math.max(r,g_,b)-Math.min(r,g_,b);
    const c0=champ; for(let y=Math.floor(H*0.15);y<H*0.75;y+=2) for(let x=0;x<W;x+=3){ const i=(y*W+x)*4; if(d[i+3]<250) continue; const k=d[i]+','+d[i+1]+','+d[i+2]; h[k]=(h[k]||0)+1; }
    const L=Object.entries(h).sort((a,b)=>b[1]-a[1]).slice(0,6).map(a=>'#'+a[0].split(',').map(v=>(+v).toString(16).padStart(2,'0')).join('').toUpperCase()); trait=L.join(' '); }catch(e){}
  const c=(e)=>{ const s=cs(e); return s?(s.webkitTextFillColor||s.color):null; };
  return {champ:champ, corps:cs(dp).backgroundColor, plateau:pl?cs(pl).backgroundColor:null, motMarque:c(nat), titre:c(g('dptTitre')), aQui:c(g('dptQui')), echeance:c(g('dptQuand')), trace:c(g('dptTrace')), anneau:arcs.join(' '), canevas:trait}; }"""
def hexa(v):
    import re
    if not v or 'rgb' not in v: return v
    n=[int(x) for x in re.findall(r'\d+',v)[:3]]; return '#%02X%02X%02X'%tuple(n)
R={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for ver,url in (('v118','zz-ref-v118.html'),('actuel','app.html')):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('light','dark'):
            pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t)}",th); pg.wait_for_timeout(600)
            for nom,ti in FICHES:
                pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}",ti); pg.wait_for_timeout(2600)
                z=pg.evaluate(Z); R[(ver,th,nom)]={k:(hexa(v) if k not in('anneau','canevas') else v) for k,v in z.items()}
            pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(2800)
            z=pg.evaluate(Z); R[(ver,th,'Cercle')]={k:(hexa(v) if k not in('anneau','canevas') else v) for k,v in z.items()}
            pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500)
            R[(ver,th,'page +')]=pg.evaluate("()=>{const s=document.getElementById('createSheet'); const cv=document.getElementById('csTrameCv'); let ch=null; try{const d=cv.getContext('2d').getImageData(6,6,1,1).data; ch=[d[0],d[1],d[2]];}catch(e){} const ph=document.getElementById('csPhrase'); const pl=s.querySelector('.enh'); return {corps:getComputedStyle(s).backgroundColor, champ:ch?('rgb('+ch.join(', ')+')'):null, plateau:pl?getComputedStyle(pl).backgroundColor:null, phrase:ph?getComputedStyle(ph).color:null};}")
            R[(ver,th,'page +')]={k:hexa(v) for k,v in R[(ver,th,'page +')].items()}
            pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
            R[(ver,th,'Index')]=pg.evaluate("()=>{const s=document.getElementById('indexSheet'); const c=document.querySelector('#indexList .s4-carte'); const pl=s.querySelector('.enh'); const et=c&&c.querySelector('.s4-et'); const ti=c&&c.querySelector('.s4-ti'); const nl=c&&c.querySelector('.s4-natlab'); return {fond:getComputedStyle(s).backgroundColor, plateau:pl?getComputedStyle(pl).backgroundColor:null, carte_corps:c?getComputedStyle(c).backgroundColor:null, carte_titre:ti?getComputedStyle(ti).color:null, carte_etat:et?getComputedStyle(et).color:null, carte_libelle:nl?getComputedStyle(nl).color:null};}")
            R[(ver,th,'Index')]={k:hexa(v) for k,v in R[(ver,th,'Index')].items()}
        ctx.close()
    b.close()
json.dump({'|'.join(k):v for k,v in R.items()}, open('scratchpad/v122/zones.json','w'), ensure_ascii=False, indent=1)
for k in sorted(R, key=lambda x:(x[2],x[1],x[0])):
    print('%-7s %-5s %-20s %s'%(k[0],k[1],k[2], ' · '.join('%s %s'%(a,b_) for a,b_ in R[k].items())))
