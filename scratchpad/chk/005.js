
/* === FOND « A · crème moyen » : mosaïque baked une fois === */
(function(){
  function bakeFond(base, dalleForce){
    var W=260, H=520;                 // ratio téléphone, léger
    var c=document.createElement('canvas'); c.width=W; c.height=H;
    var g=c.getContext('2d');
    var SIG=[[130,174,248],[201,168,245],[221,77,35],[41,21,71]];
    var pts=[]; for(var i=0;i<30;i++)pts.push([Math.random()*W, Math.random()*H]);
    var colIdx={}; [0,3,5,8,11,14,17,20,23,26].forEach(function(k,j){colIdx[k]=SIG[j%4];});
    var S=5;
    for(var y=0;y<H;y+=S)for(var x=0;x<W;x+=S){
      var bd=1e9,bi=0;
      for(var k=0;k<pts.length;k++){var dx=x-pts[k][0],dy=y-pts[k][1],d=dx*dx+dy*dy;if(d<bd){bd=d;bi=k;}}
      var col, cc=colIdx[bi];
      if(cc){ col=[base[0]+(cc[0]-base[0])*dalleForce, base[1]+(cc[1]-base[1])*dalleForce, base[2]+(cc[2]-base[2])*dalleForce]; }
      else { var w=((bi*13)%9)-4; col=[base[0]+w, base[1]+w, base[2]+w-3]; }
      g.fillStyle='rgb('+(col[0]|0)+','+(col[1]|0)+','+(col[2]|0)+')';
      g.fillRect(x,y,S,S);
    }
    return c.toDataURL();
  }
  try{
    var clair = bakeFond([228,224,217], 0.22);   // warm-neutre clair, pas jaune, texte lisible
    var sombre= bakeFond([18,19,24], 0.30);        // équivalent sombre
    var r=document.documentElement.style;
    r.setProperty('--fond-clair', 'url('+clair+')');
    r.setProperty('--fond-sombre','url('+sombre+')');
  }catch(e){}
})();
