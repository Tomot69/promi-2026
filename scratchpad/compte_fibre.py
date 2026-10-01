from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':900,'height':900})
    pg.goto('http://127.0.0.1:8752/PLANCHE-FIBRE.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=90000)
    r=pg.evaluate("""()=>{
      var S=[],G=67,rnd=Fibre.graine(31);
      for(var j=-2;j<=2;j++)for(var i=-2;i<=2;i++)
        S.push([i*G+(rnd()-.5)*G*0.42, j*G+(rnd()-.5)*G*0.42]);
      var best=1e9,bi=0;
      for(var q=0;q<S.length;q++){var d=Math.hypot(S[q][0],S[q][1]);if(d<best){best=d;bi=q;}}
      var P=Fibre.cellulePlane(S,bi,-2.0);
      var b2=Fibre.boite(P),w=b2[2]-b2[0],h=b2[3]-b2[1],s=67/Math.max(w,h),Q=[];
      for(var i2=0;i2<P.length;i2++)Q.push([(P[i2][0]-b2[0])*s,(P[i2][1]-b2[1])*s]);
      var o={};
      Fibre.mondes.forEach(function(m,ix){
        o[m]=Fibre.implante(m,Q,1,ix*101+7,Fibre.hh(ix*17+3)*Math.PI).length;});
      return o;}""")
    tot=sum(r.values()); n=len(r)
    print("touffes par cellule de 67 px, monde par monde :")
    for k,v in r.items(): print("   %-9s %5d touffes  ->  %6d poils (5 brins)"%(k,v,v*5))
    moy=tot/n
    print("   moyenne %d touffes/cellule"%moy)
    print("SPHERE : 30 cellules visibles de face (audit §5) -> %d touffes, %d poils"%(moy*30, moy*30*5))
    print("         plafond mesure : 125 000 touffes / 500 000 poils a 16,5 ms")
    print("PIRE CAS (le monde le plus dense) : %d touffes, %d poils"%(max(r.values())*30, max(r.values())*30*5))
    b.close()
