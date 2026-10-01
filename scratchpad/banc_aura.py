# ⚑ LE BUDGET D'IMAGE, MESURE DANS L'APP REELLE.
#   On charge app.html, on ouvre l'ecran Aura, et on INJECTE le peintre a
#   l'execution (addScriptTag) : le fichier n'est pas modifie d'un octet.
#   La sphere tourne dans un vrai #device de 390x844, avec tout l'ecran autour
#   — c'est ce « autour » qui manquait a la planche.
import json, sys
from playwright.sync_api import sync_playwright

DENS = [int(x) for x in (sys.argv[1:] or ['360000','240000','160000','110000','75000','50000'])]
SRC = ['/scratchpad/toile-extrait.js','/scratchpad/_m_base.js','/scratchpad/_v_moteur.js',
       '/scratchpad/_v_iles.js','/scratchpad/_f_dalle.js','/scratchpad/_v_semis.js',
       '/scratchpad/_v_peint.js']

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    err = []; pg.on('pageerror', lambda e: err.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html')
    pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    # l'ecran Aura, ouvert pour de vrai
    pg.evaluate("()=>{try{document.getElementById('souffleBtn').click();}catch(e){}}")
    pg.wait_for_timeout(1200)
    for s in SRC:
        pg.add_script_tag(url='http://127.0.0.1:8752'+s)
    pg.wait_for_timeout(400)
    print('erreurs au chargement :', err[:3])

    res = pg.evaluate("""async (DENS)=>{
      var sc=document.getElementById('auraScreen');
      var host=document.createElement('div');
      host.style.cssText='position:relative;width:342px;height:342px;margin:8px auto';
      var cv=document.createElement('canvas');
      cv.style.cssText='width:342px;height:342px;display:block';
      host.appendChild(cv); sc.insertBefore(host, sc.firstChild);
      /* le relief, recopie de la planche (elle ne peut pas etre chargee ici :
         elle batit sa propre page au chargement) */
      var _D=[[ 0.62, 0.31, 0.72],[-0.47, 0.83,-0.30],[ 0.18,-0.55, 0.81],
              [-0.79,-0.37, 0.49],[ 0.34, 0.88, 0.33],[ 0.71,-0.62,-0.33]];
      var _K=[9.7,13.1,17.9,23.3,29.1,37.7];
      var _A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
      var _PH=[0.4,1.9,2.7,0.9,1.4,2.2], FROISSE_B=[];
      for(var i9=0;i9<_D.length;i9++)
        FROISSE_B.push([_A[i9], _D[i9][0]*_K[i9], _D[i9][1]*_K[i9], _D[i9][2]*_K[i9], _PH[i9]]);
      var out=[];
      var A=atlasAlpha(GRAIN_POIL,[2.5,4.4,5.7,7.3].map(function(t){return t*342/620;}),
                       24,6,0.15,0.78,true,3);
      for(var di=0; di<DENS.length; di++){
        var N=DENS[di];
        var sem=semisPavage(N,77,0.0,[4.7,5.3,4.1,0.6,1.9,1.1,6.7,5.9,7.3,2.4,0.7,1.5],4,false,0);
        var T=batIles(24,[[58,84,255],[143,160,255],[240,122,46],[200,180,255]],
                      {pxr:620*0.392, palette:'nuit'});
        var o={css:342,R:0.392,tailles:[2.5,4.4,5.7,7.3].map(function(t){return t*342/620;}),
               atlas:A,semis:sem,relief:FROISSE_B,env:[1,0, 1.31,0.77,-1.05,0.4, -0.83,1.49,0.61,1.9],
               kn:0.55,lac:2.9,tan:0.32,pal:[[58,84,255]],trame:T,libre:false,
               velours2:1,pousse:0.7,sol:[58,84,255],fond:'#16171B',traces:[]};
        peint(cv,o);                       /* une passe pour bâtir le cache */
        var ms=[];
        await new Promise(function(res2){
          var k=0;
          function tick(){
            o.lac=2.9+k*0.035;             /* la sphere TOURNE : rien n'est cache */
            var t0=performance.now(); peint(cv,o); ms.push(performance.now()-t0);
            if(++k<70) requestAnimationFrame(tick); else res2();
          }
          requestAnimationFrame(tick);
        });
        ms.sort(function(a,b){return a-b;});
        out.push({poils:N, mediane:+ms[35].toFixed(2), d9:+ms[62].toFixed(2),
                  max:+ms[69].toFixed(2), sur20:ms.filter(function(x){return x>20;}).length});
      }
      host.remove();
      return out;
    }""", DENS)
    for r in res:
        print("%7d poils   mediane %6.2f ms   9e decile %6.2f   max %6.2f   images > 20 ms : %d/70"
              % (r['poils'], r['mediane'], r['d9'], r['max'], r['sur20']))
    print('erreurs :', err[:3])
    b.close()
