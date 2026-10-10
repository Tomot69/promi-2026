# relève les fonds rendus (clair) : corps et encarts des fiches, fond du Fil et de l'Index
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1] if len(sys.argv)>1 else 'app.html'
JS="""(sel)=>{ // tous les fonds opaques peints dans l'écran visible, avec leur aire
 var dv=document.getElementById('device').getBoundingClientRect(), out={};
 document.querySelectorAll(sel+', '+sel+' *').forEach(function(e){ var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden') return; var r=e.getBoundingClientRect(); if(r.width<30||r.height<20) return;
   if(r.right<dv.left||r.left>dv.right||r.bottom<dv.top||r.top>dv.bottom) return;
   var b=cs.backgroundColor; if(!b||b==='rgba(0, 0, 0, 0)') return; var k=b; out[k]=out[k]||[]; if(out[k].length<4) out[k].push((e.id?'#'+e.id:'.'+(e.className+'').split(' ')[0])+' '+Math.round(r.width)+'×'+Math.round(r.height)+'@'+Math.round(r.top-dv.top)); });
 return out;}"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','fil','bande'].forEach(function(g){localStorage.setItem('geste_vu_'+g,'1')});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setLight(true); closeAll();}"); pg.wait_for_timeout(800)
    def px(x,y):
        import io; from PIL import Image
        im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); dv=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}")
        return '#%02X%02X%02X'%im.getpixel((int((dv[0]+x)*2),int((dv[1]+y)*2)))
    for nom,js,sel in (('fiche Promi à tenir',"openDetail(promises.find(q=>q.title==='faire les crêpes').id)",'#detailPoster'),('Index',"closeAll();document.getElementById('indexBtn')&&document.getElementById('indexBtn').click()",'#indexScreen'),('Fil',"closeAll();setView&&setView('fil')",'#filScreen')):
        pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(2500)
        print('==',nom,'| pixel (12,700):',px(12,700),'(195,640):',px(195,640),'(195,70):',px(195,70),'(40,810):',px(40,810))
        o=pg.evaluate(JS,sel)
        for k,v in o.items(): print('  ',k,v)
    b.close()
