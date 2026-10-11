import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; tag=sys.argv[2] if len(sys.argv)>2 else 'ap'; sombre=len(sys.argv)>3
HIT="""(kind)=>{ let sx=0,sy=0,n=0; for(let y=110;y<700;y+=4)for(let x=4;x<386;x+=4){const h=Toile.hit(x,y); if(h&&(kind==='nuee'?h.kind==='nuee':h.pid!=null)){sx+=x;sy+=y;n++;}} return n?[sx/n,sy/n,n]:null; }"""
INFO="""(sel)=>{ const dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; const e=document.querySelector(sel); if(!e) return null; const o=[]; for(let q=e;q&&q.id!=='detailPoster';q=q.parentElement){ const c=getComputedStyle(q), r=q.getBoundingClientRect(); o.push({n:q.id||q.className, y:Math.round((r.top-dv.top)/k), x:Math.round((r.left-dv.left)/k), w:Math.round(r.width/k), h:Math.round(r.height/k), bg:c.backgroundColor, bd:c.borderTopWidth+' '+c.borderTopColor, rad:c.borderRadius, col:c.color, fs:c.fontSize, ff:c.fontFamily.slice(0,14), tt:c.textTransform, ls:c.letterSpacing, ta:c.textAlign, fw:c.fontWeight, lh:c.lineHeight, st:(q.getAttribute("style")||"").slice(0,200), avant:getComputedStyle(q,"::before").width, tx:(q.children.length?'':q.textContent.trim())}); } return JSON.stringify(o); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b,sombre=sombre); pg=ouvre(ctx,F)
    plante(pg,'boire un verre'); pg.wait_for_timeout(1500)
    h=pg.evaluate(HIT,'promi'); tap(pg,h[0],h[1]); pg.wait_for_timeout(3000)
    tap(pg,150,812); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{ const P=document.getElementById('detailPoster'); P.scrollTop=99999; [...P.querySelectorAll('*')].forEach(e=>{ if(e.scrollHeight>e.clientHeight+20&&/(auto|scroll)/.test(getComputedStyle(e).overflowY)) e.scrollTop=99999; }); }"); pg.wait_for_timeout(900)
    capture(pg,'scratchpad/v142/c2-%s-promi.png'%tag)
    print('PROMI', pg.evaluate("()=>[...document.querySelectorAll('#detailPoster *')].filter(e=>!e.children.length&&/supprimer ce/i.test(e.textContent)).map(e=>e.id+'.'+e.className+' < '+e.parentElement.id+'.'+e.parentElement.className).join(' | ')"))
    sel=pg.evaluate("()=>{const e=[...document.querySelectorAll('#detailPoster *')].find(e=>!e.children.length&&/supprimer ce/i.test(e.textContent)&&e.getBoundingClientRect().height>0); if(e){e.setAttribute('data-x142','1'); return '[data-x142]';} return null}")
    if sel: print(pg.evaluate(INFO,sel))
    pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const n=document.getElementById('nName'), f=document.getElementById('nFirst'), b=document.getElementById('addNuee'); n.value='le potager'; if(f) f.value='semer les radis'; b.click(); }"); pg.wait_for_timeout(3500)
    pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
    h=pg.evaluate(HIT,'nuee'); tap(pg,h[0],h[1]); pg.wait_for_timeout(3500)
    tap(pg,150,800); pg.wait_for_timeout(2200)
    capture(pg,'scratchpad/v142/c2-%s-cercle-peauf.png'%tag)
    pg.evaluate("()=>{ const P=document.getElementById('detailPoster'); P.scrollTop=99999; [...P.querySelectorAll('*')].forEach(e=>{ if(e.scrollHeight>e.clientHeight+20&&/(auto|scroll)/.test(getComputedStyle(e).overflowY)) e.scrollTop=99999; }); }"); pg.wait_for_timeout(1200)
    capture(pg,'scratchpad/v142/c2-%s-cercle-bas.png'%tag)
    print('CERCLE', pg.evaluate(INFO,'#npDiss .np-lab'))
    print(pg.erreurs); b.close()
