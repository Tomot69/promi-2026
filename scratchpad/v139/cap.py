# capture @3x de l'appareil dans un état donné ; usage : cap.py fichier préfixe [thème]
import sys,io
from playwright.sync_api import sync_playwright
from PIL import Image
f=sys.argv[1]; pre=sys.argv[2]; th=sys.argv[3] if len(sys.argv)>3 else 'light'
ETATS=[('promi-a-tenir',"openDetail(promises.find(q=>q.title==='faire les crêpes').id)"),('promi-tenu',"openDetail(promises.find(q=>q.title==='planter un arbre').id)"),
 ('chiche-a-tenir',"openDetail(promises.find(q=>q.title==='courir dimanche').id)"),('chiche-tenu',"openDetail(promises.find(q=>q.title==='le grand plongeoir').id)"),
 ('cercle',"openEssaim('potager')"),('index',"setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();"),('fil',"setView('fil')")]
if len(sys.argv)>4: ETATS=[e for e in ETATS if e[0] in sys.argv[4].split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');['tenir','chiche','planter','fil','bande','pelote','noyau','dessin','studio-monde','studio-couleur'].forEach(function(g){localStorage.setItem('geste_vu_'+g,'1')});}catch(e){}"%th)
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ETATS:
        pg.evaluate("()=>{try{closeAll()}catch(e){} try{setView('toile')}catch(e){} }"); pg.wait_for_timeout(1000); pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(3200)
        r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='planche-v139/%s-%s.png'%(pre,nom),clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]})
        im=Image.open('planche-v139/%s-%s.png'%(pre,nom)).convert('RGB')
        print(nom,' '.join('(%d,%d) #%02X%02X%02X'%((x,y)+im.getpixel((x*3,y*3))) for x,y in ((8,700),(195,600),(8,330),(40,70),(195,812),(8,835))))
    b.close()
