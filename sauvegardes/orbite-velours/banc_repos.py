# ⚑ LA VRAIE QUESTION N'EST PAS « COMBIEN DE POILS », C'EST « QUAND ».
#   Au repos l'Orbite ne bouge pas : il n'y a aucune raison de la repeindre
#   soixante fois par seconde. On mesure donc les deux regimes.
from playwright.sync_api import sync_playwright
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
    r=pg.evaluate("""async ()=>{
      var sc=document.getElementById('auraScreen');
      var cv=document.createElement('canvas'); cv.style.cssText='width:342px;height:342px;display:block';
      sc.insertBefore(cv,sc.firstChild);
      var _D=[[0.62,0.31,0.72],[-0.47,0.83,-0.30],[0.18,-0.55,0.81],
              [-0.79,-0.37,0.49],[0.34,0.88,0.33],[0.71,-0.62,-0.33]];
      var _K=[9.7,13.1,17.9,23.3,29.1,37.7], _A=[0.0059,0.0041,0.0029,0.0019,0.0012,0.0007];
      var _PH=[0.4,1.9,2.7,0.9,1.4,2.2], FR=[];
      for(var i=0;i<6;i++) FR.push([_A[i],_D[i][0]*_K[i],_D[i][1]*_K[i],_D[i][2]*_K[i],_PH[i]]);
      var T4=[2.5,4.4,5.7,7.3].map(function(t){return t*342/620;});
      var A=atlasAlpha(GRAIN_POIL,T4,24,6,0.15,0.78,true,3);
      var T=batIles(24,[[58,84,255],[143,160,255],[240,122,46],[200,180,255]],
                    {pxr:620*0.392,palette:'nuit'});
      function opts(sem){return {css:342,R:0.392,tailles:T4,atlas:A,semis:sem,relief:FR,
        env:[1,0,1.31,0.77,-1.05,0.4,-0.83,1.49,0.61,1.9],kn:0.55,lac:2.9,tan:0.32,
        pal:[[58,84,255]],trame:T,libre:false,velours2:1,pousse:0.7,
        sol:[58,84,255],fond:'#16171B',traces:[]};}
      var out={};
      /* 1 · UNE passe pleine densite : le prix de l'image au repos, paye une fois */
      var semH=semisPavage(360000,77,0.0,[4.7,5.3,4.1,0.6,1.9,1.1,6.7,5.9,7.3,2.4,0.7,1.5],4,false,0);
      var oH=opts(semH); peint(cv,oH);
      var t=[]; for(var k=0;k<7;k++){var t0=performance.now();peint(cv,oH);t.push(performance.now()-t0);}
      t.sort(function(a,b){return a-b;}); out.pleine_une_passe=+t[3].toFixed(2);
      /* 2 · le repos VRAI : on garde l'image et on la reblitte */
      var snap=document.createElement('canvas'); snap.width=cv.width; snap.height=cv.height;
      snap.getContext('2d').drawImage(cv,0,0);
      var g=cv.getContext('2d'); var t2=[];
      await new Promise(function(R){var k=0;function tick(){
        var t0=performance.now(); g.clearRect(0,0,cv.width,cv.height); g.drawImage(snap,0,0);
        t2.push(performance.now()-t0);
        if(++k<60) requestAnimationFrame(tick); else R();} requestAnimationFrame(tick);});
      t2.sort(function(a,b){return a-b;}); out.repos_image_gardee=+t2[30].toFixed(3);
      cv.remove(); return out;
    }""")
    print(r); b.close()
