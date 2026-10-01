# LES TROIS PARTIS POUR LA BANDE MORTE + la Touffe dominante + la signature retirée.
import json, os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile5')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile5.html'
MES=r"""()=>{
  const v=window._vendToile||{};
  const s2=document.querySelector('#pcCadre .pc-sub .pc-s2');
  const ch=[...document.querySelectorAll('#pcCadre .pc-ch')];
  const vus=ch.filter(c=>getComputedStyle(c).display!=='none');
  let pleines=0;
  vus.forEach(c=>{ if(!c.width) return; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
    let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>10) n++; if(n>0) pleines++; });
  return {vend:v, accentPose:s2?getComputedStyle(s2).color:null,
          pastillesVues:vus.length, pastillesPleines:pleines,
          sigCss:!!document.querySelector('#pcCadre .pc-sig'),
          sigFn:typeof window._vendSignature};
}"""
def ouvre(pg, parti):
    pg.evaluate("(p)=>{ window._vendAccent=p; try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }", parti)
    pg.wait_for_timeout(420)
    pg.evaluate("()=>{ const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2200)
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th)
        for parti in ('off','a','b','c'):
            ouvre(pg,parti); m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_%s.png'%(th,parti)))
            if parti=='off':
                mats=sorted(v['matieres'].items(), key=lambda x:-x[1])
                tot=sum(v['matieres'].values())
                print('   matières : %s   → Touffe = %.0f %% du pavage, %d mondes présents'
                      % (mats, 100*v['matieres'].get('touffe',0)/tot, len(v['matieres'])))
                a=v.get('accent')
                print('   accent mesuré : départ %s → %s · écart de luminosité %s (fond %s), %d pas'
                      % (a['depart'], a['rgb'], a['ecart'], a['fond'], a['pas']))
                print('   signature : CSS présent=%s · compteur=%s  (retirée si False/undefined)' % (m['sigCss'], m['sigFn']))
            print('   parti %-3s · accent posé %s · pastilles vues %d, pleines %d'
                  % (parti, m['accentPose'], m['pastillesVues'], m['pastillesPleines']))
        pg.context.close()
    br.close()
