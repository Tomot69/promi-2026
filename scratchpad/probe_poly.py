from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':500,'height':700})
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('http://127.0.0.1:8752/scratchpad/vraie_toile.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=60000)
    r=pg.evaluate("""()=>{
      function conv(P){
        var n=P.length, s=0, ok=true;
        for(var i=0;i<n;i++){
          var a=P[i],b=P[(i+1)%n],c=P[(i+2)%n];
          var cr=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);
          if(Math.abs(cr)<1e-9) continue;
          var sg=cr>0?1:-1;
          if(s===0)s=sg; else if(sg!==s) ok=false;
        }
        return ok;
      }
      function dedans(P,x,y){var n=P.length,c=false;
        for(var i=0,j=n-1;i<n;j=i++){
          var xi=P[i][0],yi=P[i][1],xj=P[j][0],yj=P[j][1];
          if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}
        return c;}
      var out=[];
      for(var pid=1;pid<=8;pid++){
        var D=null; try{D=Toile.dalleAbs(pid);}catch(x){}
        if(!D||!D.poly) continue;
        var P=D.poly;
        /* le site : le centroide, comme dans dalleGeneree */
        var qx=0,qy=0,i;
        for(i=0;i<P.length;i++){qx+=P[i][0];qy+=P[i][1];}
        qx/=P.length; qy/=P.length;
        /* les voisines en miroir */
        var cx=qx, cy=qy, N=[];
        for(i=0;i<P.length;i++){
          var a=P[i], bb=P[(i+1)%P.length];
          var ex=bb[0]-a[0], ey=bb[1]-a[1], L=Math.hypot(ex,ey); if(L<1e-6)continue;
          var nx=ey/L, ny=-ex/L;
          if((cx-a[0])*nx+(cy-a[1])*ny>0){nx=-nx;ny=-ny;}
          var h=(qx-a[0])*nx+(qy-a[1])*ny;
          N.push([qx-2*h*nx, qy-2*h*ny]);
        }
        /* combien de points du polygone ont bien la graine cible pour plus proche ? */
        var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
        for(i=0;i<P.length;i++){x0=Math.min(x0,P[i][0]);x1=Math.max(x1,P[i][0]);
                                y0=Math.min(y0,P[i][1]);y1=Math.max(y1,P[i][1]);}
        var tot=0, ok=0;
        for(var y=y0;y<y1;y+=1.5)for(var x=x0;x<x1;x+=1.5){
          if(!dedans(P,x,y))continue;
          tot++;
          var dt=Math.hypot(x-qx,y-qy), mn=1e18;
          for(i=0;i<N.length;i++) mn=Math.min(mn,Math.hypot(x-N[i][0],y-N[i][1]));
          if(dt<=mn) ok++;
        }
        out.push({pid:pid, n:P.length, convexe:conv(P),
                  dedans:tot?Math.round(1000*ok/tot)/10:0});
      }
      return out;}""")
    for x in r: print(x)
    print("erreurs",e[:2])
    b.close()
