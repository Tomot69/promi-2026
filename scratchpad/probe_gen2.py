from playwright.sync_api import sync_playwright
M=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':500,'height':700},device_scale_factor=2)
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('http://127.0.0.1:8752/scratchpad/vraie_toile.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=60000)
    r=pg.evaluate("""async (M)=>{
      function dedans(P,x,y){var n=P.length,c=false;
        for(var i=0,j=n-1;i<n;j=i++){
          var xi=P[i][0],yi=P[i][1],xj=P[j][0],yj=P[j][1];
          if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}
        return c;}
      function att(ms){return new Promise(function(r){setTimeout(r,ms);});}
      var hote=document.getElementById('toileCv'), out={};
      for(var mi=0;mi<M.length;mi++){
        var m=M[mi];
        Toile.setTheme(m); await att(1700);
        var v=Toile.vue(), D=Toile.dalleAbs(2);
        if(!D||!D.poly){out[m]='pas de dalle';continue;}
        /* A · SUR LA TOILE : part de pixels NON-FOND dans le polygone */
        var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9,i;
        for(i=0;i<D.poly.length;i++){x0=Math.min(x0,D.poly[i][0]);x1=Math.max(x1,D.poly[i][0]);
                                     y0=Math.min(y0,D.poly[i][1]);y1=Math.max(y1,D.poly[i][1]);}
        var sx=Math.round((x0*v.s+v.ox)*v.dpr), sy=Math.round((y0*v.s+v.oy)*v.dpr);
        var sw=Math.round((x1-x0)*v.s*v.dpr), sh=Math.round((y1-y0)*v.s*v.dpr);
        var C=document.createElement('canvas'); C.width=sw; C.height=sh;
        C.getContext('2d').drawImage(hote,sx,sy,sw,sh,0,0,sw,sh);
        var dA=C.getContext('2d').getImageData(0,0,sw,sh).data;
        var nA=0,tA=0;
        for(var y=0;y<sh;y++)for(var x=0;x<sw;x++){
          var lx=x0+(x+0.5)/v.dpr/v.s, ly=y0+(y+0.5)/v.dpr/v.s;
          if(!dedans(D.poly,lx,ly))continue; tA++;
          var o=(y*sw+x)*4, mx=Math.max(dA[o],dA[o+1],dA[o+2]), mn=Math.min(dA[o],dA[o+1],dA[o+2]);
          if(mx>=40 && mx-mn>=24) nA++;
        }
        /* B · GENEREE : part de pixels a la couleur de la dalle, dans le polygone */
        var cv=document.createElement('canvas');
        if(!Toile.dalleGeneree(cv,{monde:m,palette:'signal',poly:D.poly,ci:1,lit:0,ang:0.7,pad:24})){out[m]='ECHEC';continue;}
        var dpr=cv.width/cv.__box[2], g2=cv.getContext('2d');
        var dB=g2.getImageData(0,0,cv.width,cv.height).data, col=cv.__col, PB=cv.__poly;
        var nB=0,tB=0;
        for(y=0;y<cv.height;y++)for(x=0;x<cv.width;x++){
          var lx2=(x+0.5)/dpr, ly2=(y+0.5)/dpr;
          if(!dedans(PB,lx2,ly2))continue; tB++;
          /* ⚠ MEME CRITERE DES DEUX COTES. Compter la couleur EXACTE de la
             dalle d'un cote et « tout ce qui est colore » de l'autre fait
             mentir la mesure : une fleur de touffe a un coeur orange et un
             lisere creme qui ne sont pas la couleur du petale. */
          var o2=(y*cv.width+x)*4;
          var mx2=Math.max(dB[o2],dB[o2+1],dB[o2+2]), mn2=Math.min(dB[o2],dB[o2+1],dB[o2+2]);
          if(mx2>=40 && mx2-mn2>=24) nB++;
        }
        out[m]={toile:Math.round(1000*nA/Math.max(1,tA))/10,
                generee:Math.round(1000*nB/Math.max(1,tB))/10};
      }
      return out;}""", M)
    print("part de matiere DANS LA MEME CELLULE :  sur la Toile  /  generee")
    for k,v in r.items():
        if isinstance(v,dict):
            d=v['generee']-v['toile']
            print("  %-9s  %5.1f %%   %5.1f %%   ecart %+5.1f"%(k,v['toile'],v['generee'],d))
        else: print("  %-9s %s"%(k,v))
    print("erreurs",e[:2])
    b.close()
