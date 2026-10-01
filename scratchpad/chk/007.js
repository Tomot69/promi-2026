
/* === jauge du slide Studio onboarding === */
(function(){
  var PKEYS=['primesautier','candide','gouailleur','alangui','irascible','foret','braise','lavande','agrume','ardoise'];
  var _init=false, _cov=null, _pos=0, _vel=0, _drag=false, _last=0, _raf=null, _pts=null, _appliedKey=null;
  function pcols(){ try{ return (window.Toile&&window.Toile.palettes)?window.Toile.palettes():null; }catch(e){return null;} }
  function mix(a,b,u){return [a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u,a[2]+(b[2]-a[2])*u];}
  window.initObJauge=function(){
    var prev=document.getElementById('obStPrev'), jc=document.getElementById('obStJauge');
    if(!jc)return;
    var PAL=pcols(); if(!PAL)return;
    var keys=PKEYS.filter(function(k){return PAL[k];}); var N=keys.length;
    _cov=new Array(180).fill(0);
    var DPR=Math.min(2,window.devicePixelRatio||1);
    function fit(cv,h){var r=cv.getBoundingClientRect();var w=Math.round(r.width||cv.offsetWidth||300),hh=Math.round(r.height||h||150);cv.width=w*DPR;cv.height=hh*DPR;cv.getContext('2d').setTransform(DPR,0,0,DPR,0,0);return {width:w,height:hh};}
    var jr=fit(jc,104); var pr=prev?fit(prev,150):{width:1,height:1};
    if(!_pts){_pts=[];for(var i=0;i<16;i++)_pts.push([Math.random(),Math.random(),i%4]);}var pts=_pts;
    function covAt(u){var idx=u*(_cov.length-1),i0=Math.floor(idx),f=idx-i0;var A=_cov[i0]||0,B=_cov[Math.min(_cov.length-1,i0+1)]||0;return A+(B-A)*f;}
    function curKey(){var pf=_pos*(N-1);return keys[Math.round(pf)];}
    function drawPrev(){
      var g=prev.getContext('2d'),W=pr.width,H=pr.height,Sz=5;
      var pf=_pos*(N-1),j=Math.floor(Math.min(N-1.001,pf)),u=pf-j;
      var A=PAL[keys[j]].cols||PAL[keys[j]], B=(PAL[keys[Math.min(N-1,j+1)]].cols||PAL[keys[Math.min(N-1,j+1)]]);
      var P=pts.map(function(p){return {x:p[0]*W,y:p[1]*H,ci:p[2]};});
      for(var y=0;y<H;y+=Sz)for(var x=0;x<W;x+=Sz){
        var bd=1e9,bi=0;for(var k=0;k<P.length;k++){var dx=x-P[k].x,dy=y-P[k].y,d=dx*dx+dy*dy;if(d<bd){bd=d;bi=k;}}
        var c=mix(A[P[bi].ci],B[P[bi].ci],u);
        var rec=Math.min(1,covAt(P[bi].x/W)/3);
        var gris=(c[0]*0.34+c[1]*0.5+c[2]*0.16);
        c=mix([gris,gris,gris],c,rec);
        g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(x,y,Sz,Sz);
      }
      var nm=document.getElementById('obStName'); if(nm){var pp=PAL[curKey()];nm.textContent=(pp&&pp.name)?pp.name:curKey();}
    }
    function galet(g,cx,cy,cc,R){R=R||9;g.save();g.beginPath();g.arc(cx,cy+2,R+3,0,6.28);g.fillStyle='rgba(0,0,0,.25)';g.fill();
      g.beginPath();g.arc(cx,cy,R,0,6.28);var bg=g.createLinearGradient(cx-R,cy-R,cx+R,cy+R);bg.addColorStop(0,'#fff');bg.addColorStop(1,'#EDE1D6');g.fillStyle=bg;g.fill();
      g.lineWidth=4;g.strokeStyle='rgb('+(cc[0]|0)+','+(cc[1]|0)+','+(cc[2]|0)+')';g.beginPath();g.arc(cx,cy,R,0,6.28);g.stroke();
      g.beginPath();g.arc(cx,cy,R*0.34,0,6.28);g.fillStyle='rgb('+(cc[0]|0)+','+(cc[1]|0)+','+(cc[2]|0)+')';g.fill();g.restore();}
    function drawJauge(){
      var g=jc.getContext('2d'),W=jr.width,H=104,midY=52,jx=18,jw=W-36,th=18;
      if(!_drag){_pos+=_vel;_vel*=0.90;if(Math.abs(_vel)<0.0012){var t=Math.round(_pos*(N-1))/(N-1);_pos+=(t-_pos)*0.12;if(Math.abs(t-_pos)<0.0008){_pos=t;}_vel=0;}}
      _pos=Math.max(0,Math.min(1,_pos));
      g.clearRect(0,0,W,H);
      /* dégradé CONTINU : fondu doux à travers toutes les couleurs de toutes les palettes
         (comme le noyau) — plus de couleurs, aucune cassure nette entre palettes */
      /* fondu horizontal abstrait : couleurs distinctes et marquées, couches floues (beau, doux) */
      var grd=g.createLinearGradient(jx,0,jx+jw,0);
      var SPECTRE=[[201,168,245],[146,193,254],[130,174,248],[141,198,210],[110,171,115],[238,180,15],[221,77,35],[221,193,224],[201,168,245]];
      for(var si=0;si<SPECTRE.length;si++){var cc2=SPECTRE[si];grd.addColorStop(si/(SPECTRE.length-1),"rgb("+cc2[0]+","+cc2[1]+","+cc2[2]+")");}
      /* halo doux dessous (fondu) */
      g.save();g.globalAlpha=.26;g.filter='blur(14px)';g.strokeStyle=grd;g.lineWidth=th+16;g.lineCap='round';g.beginPath();g.moveTo(jx,midY);g.lineTo(jx+jw,midY);g.stroke();g.restore();
      /* barre NETTE par-dessus (contours francs) */
      g.strokeStyle=grd;g.lineWidth=th;g.lineCap='round';g.beginPath();g.moveTo(jx,midY);g.lineTo(jx+jw,midY);g.stroke();

      /* rail discret sous le dégradé */
      var pf=_pos*(N-1),j=Math.floor(Math.min(N-1.001,pf));
      var A=(PAL[keys[j]].cols||PAL[keys[j]])[0],B=(PAL[keys[Math.min(N-1,j+1)]].cols||PAL[keys[Math.min(N-1,j+1)]])[0];
      var cc=mix(A,B,pf-j);
      galet(g,jx+_pos*jw,midY,cc,14);
      /* nom de la teinte (le preview n'existe plus, on met à jour ici) */
      var nm=document.getElementById('obStName');if(nm){var pp=PAL[curKey()];nm.textContent=(pp&&pp.name)?pp.name:curKey();}
    }
    function loop(){drawJauge();if(prev)drawPrev();var nk=curKey();if(nk!==_appliedKey){_appliedKey=nk;apply();}_raf=requestAnimationFrame(loop);}
    if(_raf)cancelAnimationFrame(_raf); loop();
    /* choix du design : clic sur un encart change le monde/structure de la Toile */
    (function(){var host=document.getElementById("obStudio"); if(!host||host.__dsel)return; host.__dsel=true;
      var dots=document.getElementById("obStDesigns");
      var order=["encre","braille","sillons","gravure","terrazzo","touffe"];
      window._obExplored=false;
      function lockBtn(){try{var bo=document.getElementById("btnOb");if(bo)bo.classList.toggle("ob-locked",!window._obExplored);}catch(e){}}
      function setD(w){
        if(dots){var ch=dots.querySelectorAll(".obd");for(var k=0;k<ch.length;k++)ch[k].classList.toggle("on",ch[k].dataset.w===w);}
        if(w!==order[0])window._obExplored=true;
        try{window.Toile.setTheme(w);window.Toile_autoView&&0;}catch(e){}
        lockBtn();
      }
      if(dots){var ch=dots.querySelectorAll(".obd");for(var k=0;k<ch.length;k++){(function(el){el.addEventListener("click",function(){setD(el.dataset.w);});})(ch[k]);}}
      try{window.Toile.setTheme("pixel");}catch(e){}
      lockBtn();
    })();;
    function ux(ev){var r=jc.getBoundingClientRect(),jx=14,jw=r.width-28;var cx=(ev.touches?ev.touches[0].clientX:ev.clientX)-r.left;return Math.max(0,Math.min(1,(cx-jx)/jw));}
    function paint(from,to){var A=Math.min(from,to),B=Math.max(from,to);var ia=Math.floor(A*(_cov.length-1)),ib=Math.ceil(B*(_cov.length-1));for(var i=ia;i<=ib;i++)_cov[i]=Math.min(3,_cov[i]+0.5);}
    function apply(){try{window.Toile.setPalette(curKey());}catch(e){} try{if(window.onPaletteChange)window.onPaletteChange();}catch(e){}}
    if(!jc._bound){jc._bound=true;
      function down(ev){_drag=true;var u=ux(ev);_last=u;_pos=u;_vel=0;ev.stopPropagation();if(ev.cancelable)ev.preventDefault();}
      function move(ev){if(!_drag)return;var u=ux(ev);paint(_last,u);var d=u-_pos;_vel=_vel*0.55+d*0.45;_last=u;_pos=u;ev.stopPropagation();if(ev.cancelable)ev.preventDefault();}
      function up(){if(!_drag)return;_drag=false;/* l'inertie prend le relais dans drawJauge (poids du galet) */}
      jc.addEventListener('mousedown',down);window.addEventListener('mousemove',move);window.addEventListener('mouseup',up);
      jc.addEventListener('touchstart',down,{passive:false});jc.addEventListener('touchmove',move,{passive:false});window.addEventListener('touchend',up);
    }
    apply();
  };
})();
