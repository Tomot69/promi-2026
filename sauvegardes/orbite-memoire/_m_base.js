/* ════════════════════════════════════════════════════════════════════════════
   LA MÉMOIRE DE LA MAIN — les fondations communes aux trois planches.

   ⚑ CE QUI EST NOUVEAU, ET QUI VIENT DE DEUX ETUDES INDEPENDANTES :
   un objet numerique QUI SE SOUVIENT DES GESTES DE SON PROPRIETAIRE. La patine
   est l'organe, pas l'ornement. Avec trois conditions posees par Tom :
     1 · LA FORME RESTE BELLE. Une empreinte ne rend jamais l'objet difforme :
         on doit pouvoir tracer un cercle parfait autour, quelle que soit
         l'histoire des gestes.
     2 · LA MATIERE RESISTE. Ni mou, ni slime, ni caoutchouc — quelque chose
         entre la ceramique crue, la cire minerale et la pierre tendre. Une
         matiere qui n'existe pas.
     3 · CA REVIENT. La deformation est reelle sur le moment, puis la forme
         spherique revient — lentement. CE QUI RESTE N'EST PAS UN CREUX :
         c'est une trace DANS la matiere — un lustre, un grain, une chroma qui
         a monte.

   ⚠ TROIS INTERDITS QUI FONT LE « MEGA CHEAP », ET ON NE LES TOUCHE PAS :
     aucun degrade · aucune ombre portee · aucune tache speculaire.
   Toute la lumiere passe donc par LE GRAIN : chaque marque est un aplat franc,
   et c'est le NOMBRE de marques et leur marche de ton qui font le volume.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LA PALETTE, PILOTEE EN LUMINANCE PERCUE ──────────────────────────────
   Acquis paye au lot precedent : le bleu ne pese que 11 % dans la luminance
   (0,299 R + 0,587 V + 0,114 B). Regler une CLARTE HSL sur une teinte
   bleu-violet ne veut rien dire a l'oeil. On resout en luminance. */
function m_r2h(c){var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),
  h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);
  h=mx===r?((g-b)/d+(g<b?6:0)):mx===g?((b-r)/d+2):((r-g)/d+4);h/=6;}return [h,s,l];}
function m_h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;
  if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}
  if(s===0){var v=l*255;return [v,v,v];}
  var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;
  return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
function m_lum(c){return 0.299*c[0]+0.587*c[1]+0.114*c[2];}
function m_versLum(h,s,cible){
  var sat=s,c;
  for(var e=0;e<7;e++){
    var lo=0.02,hi=0.985;
    for(var i=0;i<22;i++){var m=(lo+hi)/2;c=m_h2r(h,sat,m);
      if(m_lum(c)<cible)lo=m;else hi=m;}
    c=m_h2r(h,sat,(lo+hi)/2);
    if(Math.abs(m_lum(c)-cible)<3)return c;
    sat*=0.80;
  }
  return c;
}

/* ── LE SEMIS D'UNE SPHERE — reseau de Fibonacci, perturbe ───────────────── */
function m_h(i){var x=(i*2654435761)>>>0;x^=x>>>15;x=(x*2246822519)>>>0;
  x^=x>>>13;x=(x*3266489917)>>>0;x^=x>>>16;return (x>>>8)/16777216;}
function m_semis(N){
  var P=new Float32Array(N*3), GOLD=2.399963229728653;
  var pas=Math.sqrt(12.566370614/N);
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    var x=Math.cos(a)*r, z=Math.sin(a)*r;
    x+=(m_h(i*3+1)-0.5)*pas*0.96; y+=(m_h(i*5+2)-0.5)*pas*0.96;
    z+=(m_h(i*7+4)-0.5)*pas*0.96;
    var m=Math.hypot(x,y,z)||1;
    P[i*3]=x/m; P[i*3+1]=y/m; P[i*3+2]=z/m;
  }
  return P;
}

/* ── LA VEINE DE LA MATIERE — le lit mineral, pas un peignage ────────────
   Une pierre tendre a un LIT : des plans de depot, tres basse frequence. Ce
   n'est pas une fourrure peignee ; c'est ce qui donne a la matiere son sens
   sans qu'elle ait l'air d'un pelage. */
function m_veine(x,y,z){
  var e=0.04;
  function f(a,b,c){return Math.sin(1.7*a+0.4)*Math.cos(1.3*b-0.9)
                        +0.55*Math.sin(2.1*c+1.7)*Math.cos(1.9*a+0.2);}
  var gx=f(x+e,y,z)-f(x-e,y,z), gy=f(x,y+e,z)-f(x,y-e,z), gz=f(x,y,z+e)-f(x,y,z-e);
  var d=gx*x+gy*y+gz*z; gx-=d*x; gy-=d*y; gz-=d*z;
  var m=Math.hypot(gx,gy,gz)||1;
  return [gx/m,gy/m,gz/m];
}

/* ════════════════════════════════════════════════════════════════════════════
   LES GESTES — ce que la main a laissé.
   Un geste est un ARC sur la sphere : un depart, une direction, une longueur.
   Il n'y a AUCUN creux : le geste ne deforme pas, il POLIT. On garde donc, par
   point, une part de « poli » entre 0 et 1 — et c'est elle qui fera monter la
   chroma, affiner le grain et coucher la marque.
   ⚠ Determinisme : meme Orbite, memes gestes. Rien n'est tire au hasard.
   ════════════════════════════════════════════════════════════════════════════ */
function m_gestes(n,graine){
  var G=[], k;
  for(k=0;k<n;k++){
    var s=graine+k*97;
    /* un depart quelconque sur la sphere */
    var u=m_h(s*3+1)*2-1, ph=m_h(s*5+2)*6.283185, r=Math.sqrt(Math.max(0,1-u*u));
    var a=[Math.cos(ph)*r, u, Math.sin(ph)*r];
    /* une direction tangente */
    var hx=0,hy=1,hz=0; if(Math.abs(a[1])>0.9){hx=1;hy=0;}
    var e1=[a[1]*hz-a[2]*hy, a[2]*hx-a[0]*hz, a[0]*hy-a[1]*hx];
    var m1=Math.hypot(e1[0],e1[1],e1[2])||1; e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
    var e2=[a[1]*e1[2]-a[2]*e1[1], a[2]*e1[0]-a[0]*e1[2], a[0]*e1[1]-a[1]*e1[0]];
    var an=m_h(s*7+3)*6.283185, ca=Math.cos(an), sa=Math.sin(an);
    var d=[e1[0]*ca+e2[0]*sa, e1[1]*ca+e2[1]*sa, e1[2]*ca+e2[2]*sa];
    G.push({a:a, d:d,
            L:0.45+m_h(s*11+5)*1.05,          /* la longueur de la caresse */
            w:0.055+m_h(s*13+7)*0.075,        /* sa largeur */
            f:0.45+m_h(s*17+9)*0.55});        /* combien elle a poli */
  }
  return G;
}
/* la part de poli en un point : distance a l'arc le plus proche */
function m_poli(G,x,y,z){
  var best=0;
  for(var k=0;k<G.length;k++){
    var g=G[k];
    /* projection sur le grand cercle porte par (a,d) */
    var t=Math.atan2(x*g.d[0]+y*g.d[1]+z*g.d[2], x*g.a[0]+y*g.a[1]+z*g.a[2]);
    if(t<0) t=0; else if(t>g.L) t=g.L;       /* borne : c'est un ARC, pas un cercle */
    var ct=Math.cos(t), st=Math.sin(t);
    var px=g.a[0]*ct+g.d[0]*st, py=g.a[1]*ct+g.d[1]*st, pz=g.a[2]*ct+g.d[2]*st;
    var dp=x*px+y*py+z*pz; if(dp>1)dp=1; else if(dp<-1)dp=-1;
    var an=Math.acos(dp);
    if(an<g.w){
      var v=1-an/g.w; v=v*v*(3-2*v);          /* un bord doux, pas un ruban */
      v*=g.f;
      if(v>best) best=v;
    }
  }
  return best;
}
