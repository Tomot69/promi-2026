# les memes densites, mais on GARDE L'IMAGE : la question n'est pas seulement
# « ca tient ? », c'est « c'est encore beau une fois allege ? »
import base64, io as _io
from playwright.sync_api import sync_playwright
from PIL import Image
DENS=[360000,160000,110000,75000]
SRC=['/scratchpad/toile-extrait.js','/scratchpad/_m_base.js','/scratchpad/_v_moteur.js',
     '/scratchpad/_v_iles.js','/scratchpad/_f_dalle.js','/scratchpad/_v_semis.js',
     '/scratchpad/_v_peint.js']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{try{document.getElementById('souffleBtn').click();}catch(e){}}")
    pg.wait_for_timeout(1000)
    for s in SRC: pg.add_script_tag(url='http://127.0.0.1:8752'+s)
    pg.wait_for_timeout(400)
    imgs=pg.evaluate("""(DENS)=>{
      var cv=document.createElement('canvas');
      cv.style.cssText='width:342px;height:342px';
      document.body.appendChild(cv);
      var _D=[[0.62,0.31,0.72],[-0.47,0.83,-0.30],[0.18,-0.55,0.81],
              [-0.79,-0.37,0.49],[0.34,0.88,0.33],[0.71,-0.62,-0.33]];
      var _K=[9.7,13.1,17.9,23.3,29.1,37.7], _A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
      var _PH=[0.4,1.9,2.7,0.9,1.4,2.2], FR=[];
      for(var i=0;i<6;i++) FR.push([_A[i],_D[i][0]*_K[i],_D[i][1]*_K[i],_D[i][2]*_K[i],_PH[i]]);
      var T4=[2.5,4.4,5.7,7.3].map(function(t){return t*342/620;});
      var A=atlasAlpha(GRAIN_POIL,T4,24,6,0.15,0.78,true,3);
      var T=batIles(24,[[58,84,255],[143,160,255],[240,122,46],[200,180,255]],
                    {pxr:620*0.392,palette:'nuit'});
      var G=m_gestes(6,17);
      for(var t=0;t<G.length;t++){G[t].w=0.115+G[t].w*1.35;G[t].f=Math.min(1,0.62+G[t].f*0.55);}
      var out=[];
      for(var d=0;d<DENS.length;d++){
        var sem=semisPavage(DENS[d],77,0.0,[4.7,5.3,4.1,0.6,1.9,1.1,6.7,5.9,7.3,2.4,0.7,1.5],4,false,0);
        peint(cv,{css:342,R:0.392,tailles:T4,atlas:A,semis:sem,relief:FR,
          env:[1,0,1.31,0.77,-1.05,0.4,-0.83,1.49,0.61,1.9],kn:0.55,lac:2.9,tan:0.32,
          pal:[[58,84,255]],trame:T,libre:false,velours2:1,pousse:0.7,
          sol:[58,84,255],fond:'#16171B',traces:G});
        out.push(cv.toDataURL('image/png'));
      }
      cv.remove(); return out;
    }""",DENS)
    b.close()
ims=[Image.open(_io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB') for d in imgs]
W=sum(i.width for i in ims)+24*(len(ims)+1); H=max(i.height for i in ims)+48
o=Image.new('RGB',(W,H),(22,23,27)); x=24
for im in ims: o.paste(im,(x,24)); x+=im.width+24
o.save('scratchpad/pav/vel/_densites.png'); print('ok', o.size, DENS)
