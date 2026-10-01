# Bobinette : la trame AU REPOS avant et après une plantation — combien d'arcs diffèrent vraiment, et à quelle distance de la dalle.
from playwright.sync_api import sync_playwright
import statistics as st
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('bobinette');}")
    pg.wait_for_timeout(3500)
    snap="()=>{ Toile.redraw&&Toile.redraw(); const E=window._bobEtatPub||{}; const o={}; for(const k in E) o[k]=E[k].sg+'#'+E[k].A[0].toFixed(0)+','+E[k].A[1].toFixed(0); return o; }"
    pg.evaluate("()=>{ window.Toile_liven&&Toile_liven(); }"); pg.wait_for_timeout(600)
    A=pg.evaluate(snap)
    r=pg.evaluate("()=>{ const id=9001; promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); const s=Toile.addPromi(id); return [s.x,s.y]; }")
    pg.wait_for_timeout(4000); pg.evaluate("()=>{ window.Toile_liven&&Toile_liven(); }"); pg.wait_for_timeout(600)
    B=pg.evaluate(snap)
    diff=[k for k in A if k in B and A[k]!=B[k]]
    import math
    sp=pg.evaluate("()=>(window._bobAnim||{}).sp||0")
    ds=[]
    for k in diff:
        x,y=map(float,B[k].split('#')[1].split(','))
        ds.append(math.hypot(x-r[0],y-r[1])/(sp or 1))
    cat={'retourné':0,'bobine':0,'couleur':0}
    for k in diff:
        a=A[k].split('#')[0].split('|'); bb=B[k].split('#')[0].split('|')
        if a[0]!=bb[0]: cat['retourné']+=1
        elif a[2]!=bb[2]: cat['bobine']+=1
        else: cat['couleur']+=1
    print(cat)
    print('arcs communs',len([k for k in A if k in B]),'| différents au repos',len(diff),'| distance médiane',round(st.median(ds),1) if ds else '-', '| au-delà de 3 pas',sum(1 for d in ds if d>3),'| sp',round(sp,1))
    b.close()
