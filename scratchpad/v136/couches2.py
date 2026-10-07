from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
SC='scratchpad/v136/'; TAG=(__import__('sys').argv[2] if len(__import__('sys').argv)>2 else 'ap'); IDS=['auPeloteHalo','auPeloteOmbre','auBoule','auBouleGL']
NOMS={'tout':'tout','auPeloteHalo':'le halo seul','auPeloteOmbre':'l’ombre seule','auBoule':'le canevas 2D seul','auBouleGL':'la Pelote seule (carte graphique)','sanshalo':'tout, sans le halo'}
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'app.html')); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); document.getElementById('souffleBtn').click();}",th); pg.wait_for_timeout(5200)
        pg.evaluate("()=>{ try{ _aura.fige(true); }catch(e){} }"); pg.wait_for_timeout(400)
        print(th, pg.evaluate("(I)=>I.map(i=>{const e=document.getElementById(i); if(!e) return i+' ABSENT'; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), s=getComputedStyle(e); let n=-1; try{ if(e.tagName==='CANVAS'&&i!=='auBouleGL'){ const d=e.getContext('2d').getImageData(0,0,e.width,e.height).data; n=0; for(let k=3;k<d.length;k+=40) if(d[k]>8) n++; } }catch(_){ } return i+' '+[Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)].join(',')+' z'+s.zIndex+' op'+s.opacity+' peints:'+n+' '+s.backgroundImage.slice(0,50)})", IDS))
        clip={'x':20+25,'y':44+85,'width':340,'height':340}
        def cap(n): pg.wait_for_timeout(250); pg.screenshot(path=SC+'c2-'+TAG+'-%s-%s.png'%(th,n), clip=clip)
        cap('tout')
        for i in IDS:
            pg.evaluate("(a)=>{ let s=document.getElementById('zzIso'); if(!s){ s=document.createElement('style'); s.id='zzIso'; document.head.appendChild(s); } s.textContent=a[0].filter(x=>x!==a[1]).map(x=>'#'+x+'{visibility:hidden!important}').join(''); }",[IDS,i]); cap(i)
        pg.evaluate("()=>{ document.getElementById('zzIso').textContent='#auPeloteHalo{visibility:hidden!important}'; }"); cap('sanshalo')
        ctx.close()
    b.close()
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',34)
P=Image.new('RGB',(6*1040+60,2*1100+40),(255,255,255)); d=ImageDraw.Draw(P)
for j,th in enumerate(('light','dark')):
    for i,n in enumerate(['tout','auPeloteHalo','auPeloteOmbre','auBoule','auBouleGL','sanshalo']):
        x=20+i*1040; y=20+j*1100; d.text((x,y+10),('clair' if th=='light' else 'sombre')+' · '+NOMS[n],fill=(32,25,8),font=f); P.paste(Image.open(SC+'c2-'+TAG+'-%s-%s.png'%(th,n)),(x,y+70))
P.save('planche-v136/pelote-couches-'+TAG+'.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v136/pelote-couches-'+TAG+'-tel.png')
