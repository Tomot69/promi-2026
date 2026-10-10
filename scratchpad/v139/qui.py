import sys
from playwright.sync_api import sync_playwright
JS="""()=>{var dv=document.getElementById('device').getBoundingClientRect(),o=[];
 document.querySelectorAll('#device *, .frame *').forEach(function(e){var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity===0)return; var r=e.getBoundingClientRect(); if(r.width<20||r.height<14)return; if(r.right<=dv.left||r.left>=dv.right||r.bottom<=dv.top||r.top>=dv.bottom)return;
  var b=cs.backgroundColor; if(b==='rgb(247, 240, 222)'||b==='rgb(233, 216, 183)'||b==='rgb(234, 217, 185)') o.push(b.replace('rgb','')+' '+e.tagName+(e.id?'#'+e.id:'')+'.'+(''+e.className).split(' ').slice(0,2).join('.')+' '+Math.round(r.width)+'×'+Math.round(r.height)+' @'+Math.round(r.left-dv.left)+','+Math.round(r.top-dv.top)+' bord:'+cs.borderTopColor);});
 return o;}"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','light');['tenir','chiche','planter','fil','bande'].forEach(function(g){localStorage.setItem('geste_vu_'+g,'1')});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in (('promi',"openDetail(promises.find(q=>q.title==='faire les crêpes').id)"),('tenu',"openDetail(promises.find(q=>q.title==='planter un arbre').id)"),('cercle',"openEssaim('potager')")):
        pg.evaluate("()=>{closeAll();"+js+"}"); pg.wait_for_timeout(3000); print('==',nom)
        for l in pg.evaluate(JS): print('  ',l)
        print('   canevas corps:',pg.evaluate("()=>{var c=document.getElementById('dpTrameCv'); return c?[c.dataset.champ,c.dataset.corps,getComputedStyle(document.getElementById('detailPoster')).backgroundColor,getComputedStyle(document.getElementById('detailPoster'),'::before').backgroundColor]:null}"))
    b.close()
