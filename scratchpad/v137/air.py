import sys
from playwright.sync_api import sync_playwright
JS="""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
 const R=s=>{const e=document.querySelector(s); if(!e||!e.textContent.trim()) return null; const r=document.createRange(); r.selectNodeContents(e); const b=r.getBoundingClientRect(); return [(b.top-D.top)/k,(b.bottom-D.top)/k,e.textContent.trim().slice(0,40)];};
 const kr=[...document.querySelectorAll('#detailPoster .kr-n')].map(e=>{const r=document.createRange(); r.selectNodeContents(e); return (r.getBoundingClientRect().bottom-D.top)/k;}).filter(v=>v>0);
 return {noy:kr.length?Math.max(...kr):null, qui:R('#dptQui'), ti:R('#dptTitre'), et:R('#dptQuand')||R('#dptEtat'), tr:R('#dptTrace')};}"""
res={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for f in ('zz-av136.html','app.html'):
        for th in ('light','dark'):
            c=b.new_context(viewport={'width':430,'height':932}); pg=c.new_page()
            pg.add_init_script("try{localStorage.setItem('promi_theme','%s')}catch(e){}"%th)
            pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("t=>{var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){try{setLight(t==='light')}catch(e){d.classList.toggle('light',t==='light')}}}",th)
            for t in ('faire les crêpes','nager le mardi','planter un arbre','courir dimanche','le grand plongeoir'):
                pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(700); pg.evaluate("t=>openDetail(promises.find(q=>q.title===t).id)",t); pg.wait_for_timeout(2600)
                m=pg.evaluate(JS); res[(f,th,t)]=m
            c.close()
    b.close()
print('%-20s %-6s | %-34s | noyaux→phrase | phrase→titre | titre→suivant'%('fiche','thème','phrase'))
for th in ('light','dark'):
    for t in ('faire les crêpes','nager le mardi','planter un arbre','courir dimanche','le grand plongeoir'):
        for f in ('zz-av136.html','app.html'):
            m=res[(f,th,t)]; q,ti,et=m['qui'],m['ti'],m['et'] or m['tr']
            a=(q[0]-m['noy']) if q and m['noy'] else None; b_=(ti[0]-q[1]) if q and ti else None; c_=(et[0]-ti[1]) if et and ti else None
            F=lambda v:'%6.1f'%v if v is not None else '   —  '
            print('%-20s %-6s | %-34s | %s | %s | %s   %s'%(t,th,(q[2] if q else '—'),F(a),F(b_),F(c_),'avant' if 'av' in f else 'APRÈS'))
