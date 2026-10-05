/* PLANCHE v127 (C-042) — le trait « stylet » : une peinture pleine et opaque, contours lissés. Rien de ceci n'est dans l'app. */
window.PEN = (function(){
  function cr(P, n){ /* Catmull-Rom : points {x,y,t,p} → rééchantillonnés */ var o=[]; for(var i=0;i<P.length-1;i++){ var a=P[Math.max(0,i-1)], b=P[i], c=P[i+1], d=P[Math.min(P.length-1,i+2)];
      for(var k=0;k<n;k++){ var u=k/n, u2=u*u, u3=u2*u; function f(q){ return 0.5*((2*b[q])+(-a[q]+c[q])*u+(2*a[q]-5*b[q]+4*c[q]-d[q])*u2+(-a[q]+3*b[q]-3*c[q]+d[q])*u3); }
        o.push({x:f('x'), y:f('y'), t:b.t+(c.t-b.t)*u, p:(b.p==null?1:b.p)+((c.p==null?1:c.p)-(b.p==null?1:b.p))*u}); } } o.push(P[P.length-1]); return o; }
  /* largeurs : base (pt), variante E1 | E2 */
  function largeurs(Q, base, v){ var n=Q.length, s=[0], i; for(i=1;i<n;i++) s.push(s[i-1]+Math.hypot(Q[i].x-Q[i-1].x, Q[i].y-Q[i-1].y)); var L=s[n-1]||1;
    var vit=[]; for(i=0;i<n;i++){ var a=Math.max(0,i-3), b=Math.min(n-1,i+3), dt=Math.max(1,(Q[b].t-Q[a].t)); vit.push((s[b]-s[a])/dt); }   /* pt par ms, lissée */
    var court = L < base*3.2, E2 = v==='E2', fin = E2?0.25:0.10, deb = E2?0.20:0.12, surD = E2?0.38:0.16, w=[];
    for(i=0;i<n;i++){ var u=s[i]/L, k=1;
      if(!court){ if(u<deb){ var q=1-u/deb; k*=1+surD*q*q; }                       /* plus épais au début */
        k*=Math.max(0.72, Math.min(1.06, 1.06-0.42*vit[i]));                        /* un peu plus fin quand le geste est rapide */
        if(u>1-fin){ var z=(1-u)/fin; k*=Math.pow(z,0.85); } }                       /* effilé à la fin */
      k*=(Q[i].p==null?1:(0.55+0.45*Q[i].p*2>1.35?1.35:0.55+0.45*Q[i].p*2));       /* la pression d'un stylet (1 = doigt) */
      w.push(Math.max(1, base*k)); }
    return {w:w, court:court}; }
  function trace(g, P, base, v, col){ if(!P.length) return; if(P.length===1){ g.fillStyle=col; g.beginPath(); g.arc(P[0].x,P[0].y,Math.max(1,base)/2,0,6.2832); g.fill(); return; }
    var Q=cr(P, 8), W=largeurs(Q, base, v).w, n=Q.length, G=[], D=[], i;
    for(i=0;i<n;i++){ var a=Q[Math.max(0,i-1)], b=Q[Math.min(n-1,i+1)], dx=b.x-a.x, dy=b.y-a.y, m=Math.hypot(dx,dy)||1, nx=-dy/m, ny=dx/m, h=W[i]/2;
      G.push([Q[i].x+nx*h, Q[i].y+ny*h]); D.push([Q[i].x-nx*h, Q[i].y-ny*h]); }
    g.fillStyle=col; g.beginPath(); g.moveTo(G[0][0],G[0][1]); for(i=1;i<n;i++) g.lineTo(G[i][0],G[i][1]); for(i=n-1;i>=0;i--) g.lineTo(D[i][0],D[i][1]); g.closePath(); g.fill();
    for(i=0;i<n;i+=1){ g.beginPath(); g.arc(Q[i].x,Q[i].y,W[i]/2,0,6.2832); g.fill(); } }   /* disques le long du trait : ni trou aux virages serrés, ni bout carré */
  /* des gestes d'essai : points + temps (ms) */
  function geste(F, a, b, n, dur, lent){ var P=[], i; for(i=0;i<=n;i++){ var u=a+(b-a)*i/n, q=F(u); P.push({x:q[0], y:q[1], t:0}); }
    /* le temps : plus lent dans les courbes */ var T=0; P[0].t=0; for(i=1;i<P.length;i++){ var d=Math.hypot(P[i].x-P[i-1].x,P[i].y-P[i-1].y), c=1; if(i<P.length-1){ var x1=P[i].x-P[i-1].x,y1=P[i].y-P[i-1].y,x2=P[i+1].x-P[i].x,y2=P[i+1].y-P[i].y; var an=Math.abs(Math.atan2(x1*y2-y1*x2, x1*x2+y1*y2)); c=1+an*(lent||2.2); } T+=d*c; P[i].t=T; }
    var k=dur/(T||1); P.forEach(function(p){ p.t*=k; }); return P; }
  /* « elle » en cursive : e l l e — une suite de boucles */
  function mot(x0, y0, h){ var S=[0.52,1,1,0.52], pas=h*0.58, P=[]; return geste(function(u){ var i=Math.min(3,Math.floor(u)), f=u-i, hh=h*S[i], ang=f*6.2832;
        var x=x0+(i+f)*pas+Math.sin(ang)*hh*0.30-(1-Math.cos(ang))*hh*0.04, y=y0-(1-Math.cos(ang))*hh*0.5; return [x,y]; }, -0.12, 4.12, 150, 1500, 2.4); }
  function coeur(cx, cy, r){ return geste(function(u){ var t=u*6.2832+3.1416; return [cx+r*0.0625*16*Math.pow(Math.sin(t),3), cy-r*0.0625*(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))]; }, 0.02, 0.985, 70, 900, 1.6); }
  function rapide(x0, y0, l){ return geste(function(u){ return [x0+l*u, y0-l*0.22*Math.sin(u*2.6)]; }, 0, 1, 12, 150, 0.4); }
  function lent(x0, y0, l){ return geste(function(u){ return [x0+l*u, y0-l*0.10*Math.sin(u*9.2)]; }, 0, 1, 60, 2600, 1.2); }
  function point(x, y){ return [{x:x,y:y,t:0},{x:x+1.2,y:y+0.4,t:30}]; }
  function etoile(cx, cy, r){ return geste(function(u){ var k=Math.floor(u), f=u-k, a0=-1.5708+k*2.5133, a1=-1.5708+(k+1)*2.5133; return [cx+r*(Math.cos(a0)*(1-f)+Math.cos(a1)*f), cy+r*(Math.sin(a0)*(1-f)+Math.sin(a1)*f)]; }, 0, 5, 50, 800, 0.5); }
  return {trace:trace, mot:mot, coeur:coeur, rapide:rapide, lent:lent, point:point, etoile:etoile};
})();
