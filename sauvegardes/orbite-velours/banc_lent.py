# ⚑ LE BUDGET EN ROTATION LENTE PERMANENTE — il n'y a pas d'etat immobile.
#   Et on cherche a RATTRAPER la matiere perdue : moins de poils, mais plus
#   gros. La couverture vaut N x (surface d'un brin) — si N tombe de 3,3 fois,
#   le brin doit grandir d'autant. Reste a savoir ce que ca coute.
import sys
from playwright.sync_api import sync_playwright
SRC=['/scratchpad/toile-extrait.js','/scratchpad/_m_base.js','/scratchpad/_v_moteur.js',
     '/scratchpad/_v_iles.js','/scratchpad/_f_dalle.js','/scratchpad/_v_semis.js',
     '/scratchpad/_v_peint.js']
CAS=[(160000,1.0),(130000,1.0),(110000,1.0),(110000,1.35),(110000,1.7),
     (90000,1.7),(75000,1.9)]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{try{document.getElementById('souffleBtn').click();}catch(e){}}")
    pg.wait_for_timeout(1000)
    for s in SRC: pg.add_script_tag(url='http://127.0.0.1:8752'+s)
    pg.wait_for_timeout(400)
    r=pg.evaluate("""async (CAS)=>{
      var sc=document.getElementById('auraScreen');
      var cv=document.createElement('canvas'); cv.style.cssText='width:342px;height:342px;display:block';
      sc.insertBefore(cv,sc.firstChild);
      var _D=[[0.62,0.31,0.72],[-0.47,0.83,-0.30],[0.18,-0.55,0.81],
              [-0.79,-0.37,0.49],[0.34,0.88,0.33],[0.71,-0.62,-0.33]];
      var _K=[9.7,13.1,17.9,23.3,29.1,37.7], _A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
      var _PH=[0.4,1.9,2.7,0.9,1.4,2.2], FR=[];
      for(var i=0;i<6;i++) FR.push([_A[i],_D[i][0]*_K[i],_D[i][1]*_K[i],_D[i][2]*_K[i],_PH[i]]);
      var T=batIles(24,[[58,84,255],[143,160,255],[240,122,46],[200,180,255]],
                    {pxr:620*0.392,palette:'nuit'});
      var G=m_gestes(6,17);
      for(var t=0;t<G.length;t++){G[t].w=0.115+G[t].w*1.35;G[t].f=Math.min(1,0.62+G[t].f*0.55);}
      var out=[];
      for(var c=0;c<CAS.length;c++){
        var N=CAS[c][0], gros=CAS[c][1];
        var T4=[2.5,4.4,5.7,7.3].map(function(x){return x*gros*342/620;});
        var A=atlasAlpha(GRAIN_POIL,T4,24,6,0.15,0.78,true,3);
        var sem=semisPavage(N,77,0.0,[4.7,5.3,4.1,0.6,1.9,1.1,6.7,5.9,7.3,2.4,0.7,1.5],4,false,0);
        var o={css:342,R:0.392,tailles:T4,atlas:A,semis:sem,relief:FR,
          env:[1,0,1.31,0.77,-1.05,0.4,-0.83,1.49,0.61,1.9],kn:0.55,lac:2.9,tan:0.32,
          pal:[[58,84,255]],trame:T,libre:false,velours2:1,pousse:0.7,
          sol:[58,84,255],fond:'#16171B',traces:G};
        peint(cv,o);
        /* ⚑ LA ROTATION LENTE, CELLE DU PRODUIT : un tour en ~50 s,
           soit 0,0021 rad par image. Elle ne s'arrete jamais. */
        var ms=[];
        await new Promise(function(R2){var k=0;function tick(){
          o.lac=2.9+k*0.0021;
          var t0=performance.now(); peint(cv,o); ms.push(performance.now()-t0);
          if(++k<80) requestAnimationFrame(tick); else R2();} requestAnimationFrame(tick);});
        ms.sort(function(a,b){return a-b;});
        /* la couverture : part du disque encore a l'encre */
        var g=cv.getContext('2d'), W=cv.width, d=g.getImageData(0,0,W,W).data;
        var cx=W/2, R=W*0.392, tot=0, trous=0;
        for(var y=(cx-R)|0;y<cx+R;y+=2) for(var x=(cx-R)|0;x<cx+R;x+=2){
          if((x-cx)*(x-cx)+(y-cx)*(y-cx) > R*R*0.80) continue;
          var q=(y*W+x)*4, L=0.299*d[q]+0.587*d[q+1]+0.114*d[q+2];
          tot++; if(L<42) trous++;
        }
        out.push({poils:N, gros:gros, mediane:+ms[40].toFixed(2), d9:+ms[71].toFixed(2),
                  sur20:ms.filter(function(x){return x>20;}).length,
                  trous:+(100*trous/tot).toFixed(2), img:cv.toDataURL('image/png')});
      }
      cv.remove(); return out;
    }""",CAS)
    import base64, io as _io
    from PIL import Image
    ims=[]
    for x in r:
        print("%7d poils x%.2f   mediane %6.2f ms   9e dec %6.2f   >20ms %2d/80   encre %5.2f %%"
              % (x['poils'],x['gros'],x['mediane'],x['d9'],x['sur20'],x['trous']))
        ims.append(Image.open(_io.BytesIO(base64.b64decode(x['img'].split(',')[1]))).convert('RGB'))
    W=sum(i.width for i in ims)+24*(len(ims)+1); H=max(i.height for i in ims)+48
    o=Image.new('RGB',(W,H),(22,23,27)); x=24
    for im in ims: o.paste(im,(x,24)); x+=im.width+24
    o.save('scratchpad/pav/vel/_lent.png')
    b.close()
