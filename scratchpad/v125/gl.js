/* ⚑ v125 (Tom, 3 oct. 2026) — LA PELOTE PASSE À LA CARTE GRAPHIQUE. « Mesuré sur iPhone 16e, au palier de 75 000 poils : image p50
   187 ms, 5 images/s. Cause à nommer : les poils sont recalculés à chaque image. » CONFIRMÉ à la lecture : `peint` repasse, en
   JavaScript, sur chaque poil visible (rotation, projection, lumière du velours, choix de la marche de couleur), puis recopie son
   tampon pixel par pixel (`verse`) — 75 000 à 220 000 fois par image, sur le fil principal.
   LA PARADE : les poils ne bougent pas dans le repère de l'objet. Leur état (`S.__st` : position, normale, flux, couleur, poli) est
   envoyé UNE FOIS à la carte graphique ; à chaque image elle fait elle-même la rotation, la projection et la lumière (le souffle
   compris), et pose le tampon du poil — un rectangle instancié par poil, lu dans le même atlas. Plus un seul poil n'est recalculé en
   JavaScript. Ce sont LES MÊMES poils, aux mêmes pixels, dans les mêmes couleurs : pas de texture plaquée sur une sphère, donc ni
   couture ni pôle, et la frange de la silhouette reste celle du poil.
   · la règle de `verse` (« le plus opaque gagne » : `if(v>B[o2]) B[o2]=v`, l'alpha en poids fort) devient un test de profondeur :
     la profondeur écrite est 1 − alpha ;
   · sous la fourrure, le corps plein (v120, v123) : le même disque (opaque jusqu'à 0,972 R, fondu jusqu'à 1,012 R) ;
   · le toucher (l'empreinte, le prénom effleuré) reste peint par `peint` : il déforme des poils image par image — ces images-là
     gardent le peintre d'origine ; dès que la main est levée et le creux refermé, la carte graphique reprend.
   WebGL 2 ; s'il manque, `peintGL` rend `false` et le peintre d'origine peint, comme avant. */
var _GL=null;
function _glProg(gl, vs, fs){
  function sh(t,s){ var o=gl.createShader(t); gl.shaderSource(o,s); gl.compileShader(o);
    if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)) throw new Error('shader : '+gl.getShaderInfoLog(o)); return o; }
  var p=gl.createProgram(); gl.attachShader(p,sh(gl.VERTEX_SHADER,vs)); gl.attachShader(p,sh(gl.FRAGMENT_SHADER,fs)); gl.linkProgram(p);
  if(!gl.getProgramParameter(p,gl.LINK_STATUS)) throw new Error('programme : '+gl.getProgramInfoLog(p));
  return p;
}
function _glInit(W){
  var cv=document.createElement('canvas'); cv.width=W; cv.height=W;
  var gl=cv.getContext('webgl2', {alpha:true, premultipliedAlpha:true, antialias:false, depth:false, stencil:false, preserveDrawingBuffer:true, powerPreference:'high-performance'});
  if(!gl) return null;
  var VS=['#version 300 es','precision highp float;',
    'layout(location=0) in vec2 aCoin;','layout(location=1) in vec3 aPos;','layout(location=2) in vec3 aNrm;','layout(location=3) in float aRel;',
    'layout(location=4) in vec3 aFlux;','layout(location=5) in vec4 aE0;','layout(location=6) in vec4 aE1;','layout(location=7) in float aVar;',
    'uniform float uCl,uSl,uCt,uSt,uR,uFOC,uC,uW,uVel,uDoux,uPousse,uNCOL,uNT,uILE,uETAGE,uM,uCell,uGrid,uORI,uNVAR;','uniform vec2 uAtlas;','uniform sampler2D uPal;',
    'out vec2 vUV;','flat out vec3 vCol;',
    'const vec3 L=vec3(-0.58,-0.72,0.380);','const float TAU=6.283185307179586;',
    'void main(){',
    '  float ci=aE0.x; gl_Position=vec4(2.0,2.0,2.0,1.0); vUV=vec2(0.0); vCol=vec3(0.0);',
    '  if(ci<0.0) return;',
    '  float Zt=-aPos.x*uSl+aPos.z*uCl, Z2=aPos.y*uSt+Zt*uCt;',
    '  if(Z2<0.0) return;',
    '  float X2=aPos.x*uCl+aPos.z*uSl, Y2=aPos.y*uCt-Zt*uSt;',
    '  float rrp=1.0+aRel*pow(max(Z2,0.0),0.60); X2*=rrp; Y2*=rrp; Z2*=rrp;',
    '  float nX=aNrm.x*uCl+aNrm.z*uSl, nZt=-aNrm.x*uSl+aNrm.z*uCl, nY=aNrm.y*uCt-nZt*uSt, nZ2=aNrm.y*uSt+nZt*uCt;',
    '  float k=uFOC/(uFOC-Z2*uR);',
    '  float px=floor(uC+X2*uR*k), py=floor(uC+Y2*uR*k);',
    '  if(px<26.0||py<26.0||px>uW-26.0||py>uW-26.0) return;',
    '  float fX=aFlux.x*uCl+aFlux.z*uSl, fZt=-aFlux.x*uSl+aFlux.z*uCl;',
    '  float fY=aFlux.y*uCt-fZt*uSt, fZv=aFlux.y*uSt+fZt*uCt;',
    '  float fx2=fX*aE1.y-fY*aE1.z; fY=fX*aE1.z+fY*aE1.y; fX=fx2;',
    '  float dl=max(0.0, nX*L.x+nY*L.y+nZ2*L.z);',
    '  float lum=0.30+0.70*pow(dl,0.74);',
    '  float tl=fX*L.x+fY*L.y+fZv*L.z;',
    '  float s1=sqrt(max(0.0,1.0-tl*tl));',
    '  if(uVel>0.0){ float tv=fZv; float s2=sqrt(max(0.0,1.0-tv*tv)); float kk=max(0.0,s1*s2-tl*tv); float k2=kk*kk, k4=k2*k2;',
    '    lum+=uVel*(uDoux>0.5 ? (0.26*s1*dl+0.44*k4) : (0.26*s1*dl+0.62*k4*k2)); }',
    '  lum=min(lum,1.0);',
    '  float po=aE0.z, ew=aE0.w;',
    '  float lu=(s1-0.78)*(11.5+16.0*ew); lu=max(lu,-1.0-1.4*ew);',
    '  float mar=trunc((lum-0.30)*16.4+5.4+aE0.y+lu+po*2.6+uPousse*1.4);',
    '  mar=min(mar,uM-3.0); mar=clamp(mar,0.0,uM-1.0);',
    '  float zz=(Z2+1.0)*0.5, tai;',
    '  if(uILE>0.5 && ci>0.0 && uNT>1.0){ tai=0.0; }',
    '  else { float b0=(uILE>0.5 && uNT>1.0)?1.0:0.0; float z3=zz*(1.0-0.72*uPousse)+0.72*uPousse; tai=clamp(b0+floor(z3*(uNT-b0)), b0, uNT-1.0); }',
    '  if(ci>=uNCOL && tai>0.0) tai-=1.0;',
    '  if(uILE<0.5 && aE1.x<18.0 && tai>0.0) tai-=1.0;',
    '  if(po>0.34 && tai>0.0) tai-=1.0;',
    '  if(ew>0.30 && tai<uNT-1.0) tai+=1.0;',
    '  float a=atan(fY,fX); if(a<0.0) a+=TAU;',
    '  float sec=clamp(floor(a/TAU*uORI),0.0,uORI-1.0);',
    '  float spr=tai*uORI*uNVAR+sec*uNVAR+aVar;',
    '  float et=(po>0.10+0.62*aE1.w && ci<uNCOL)?uETAGE:0.0;',
    '  vCol=texelFetch(uPal, ivec2(int(et+ci*uM+mar),0), 0).rgb;',
    '  float m=(uCell-1.0)*0.5;',
    '  vec2 P=vec2(px,py)+aCoin*uCell-vec2(m);',
    '  vec2 cel=vec2(mod(spr,uGrid), floor(spr/uGrid));',
    '  vUV=(cel*uCell+aCoin*uCell)/uAtlas;',
    '  gl_Position=vec4(P.x/uW*2.0-1.0, 1.0-P.y/uW*2.0, 0.0, 1.0);',
    '}'].join('\n');
  var FS=['#version 300 es','precision highp float;','in vec2 vUV;','flat in vec3 vCol;','uniform sampler2D uAt;','out vec4 o;',
    'void main(){ float a=texture(uAt,vUV).r; if(a<=0.0) discard; o=vec4(vCol,a); gl_FragDepth=1.0-a; }'].join('\n');
  var VS2=['#version 300 es','void main(){ vec2 p=vec2(float((gl_VertexID<<1)&2), float(gl_VertexID&2)); gl_Position=vec4(p*2.0-1.0,0.0,1.0); }'].join('\n');
  var FS2=['#version 300 es','precision highp float;','uniform sampler2D uFur;','uniform vec3 uCorps;','uniform float uA,uR0,uR1,uC2,uW2;','out vec4 o;',
    'void main(){ vec4 f=texelFetch(uFur, ivec2(gl_FragCoord.xy), 0);',
    '  float r=distance(vec2(gl_FragCoord.x, uW2-gl_FragCoord.y), vec2(uC2));',
    '  float t=r<=uR0 ? 1.0 : (r>=uR1 ? 0.0 : 1.0-(r-uR0)/(uR1-uR0)); t=t*t*(3.0-2.0*t); t*=uA;',
    '  o=vec4(f.rgb*f.a+uCorps*t*(1.0-f.a), f.a+t*(1.0-f.a)); }'].join('\n');
  var G={cv:cv, gl:gl, W:W};
  G.p1=_glProg(gl,VS,FS); G.p2=_glProg(gl,VS2,FS2);
  G.u1={}; ['uCl','uSl','uCt','uSt','uR','uFOC','uC','uW','uVel','uDoux','uPousse','uNCOL','uNT','uILE','uETAGE','uM','uCell','uGrid','uORI','uNVAR','uAtlas','uPal','uAt'].forEach(function(n){ G.u1[n]=gl.getUniformLocation(G.p1,n); });
  G.u2={}; ['uFur','uCorps','uA','uR0','uR1','uC2','uW2'].forEach(function(n){ G.u2[n]=gl.getUniformLocation(G.p2,n); });
  G.vao=gl.createVertexArray(); gl.bindVertexArray(G.vao);
  G.bCoin=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,G.bCoin); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([0,0,1,0,0,1,1,1]),gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
  G.bQ=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,G.bQ);
  [[1,3,0],[2,3,12],[3,1,24],[4,3,28]].forEach(function(a){ gl.enableVertexAttribArray(a[0]); gl.vertexAttribPointer(a[0],a[1],gl.FLOAT,false,40,a[2]); gl.vertexAttribDivisor(a[0],1); });
  G.bE=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,G.bE);
  [[5,4,0],[6,4,16],[7,1,32]].forEach(function(a){ gl.enableVertexAttribArray(a[0]); gl.vertexAttribPointer(a[0],a[1],gl.FLOAT,false,36,a[2]); gl.vertexAttribDivisor(a[0],1); });
  gl.bindVertexArray(null);
  G.vao2=gl.createVertexArray();
  /* la cible de la fourrure : couleur + profondeur */
  G.tFur=gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,G.tFur); gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA8,W,W,0,gl.RGBA,gl.UNSIGNED_BYTE,null);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
  G.rb=gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER,G.rb); gl.renderbufferStorage(gl.RENDERBUFFER,gl.DEPTH_COMPONENT24,W,W);
  G.fb=gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER,G.fb);
  gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,G.tFur,0); gl.framebufferRenderbuffer(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT,gl.RENDERBUFFER,G.rb);
  if(gl.checkFramebufferStatus(gl.FRAMEBUFFER)!==gl.FRAMEBUFFER_COMPLETE) throw new Error('cible incomplète');
  gl.bindFramebuffer(gl.FRAMEBUFFER,null);
  G.tAt=gl.createTexture(); G.tPal=gl.createTexture();
  cv.addEventListener('webglcontextlost', function(e){ try{ e.preventDefault(); }catch(_){} _GL=null; }, false);
  return G;
}
/* l'atlas : un tampon par (taille, orientation × variante), au niveau d'alpha le plus haut (le seul que la boucle emploie : `pres=1`) */
function _glAtlas(G, A, NT){
  var gl=G.gl, NS=NT*ORI*NVAR, m=0, s, j, t;
  for(s=0;s<NS;s++){ t=A[s*NIVA+NIVA-1]; for(j=0;j<t.rel.length;j++){ var a=Math.abs(t.rel[j][0]), b=Math.abs(t.rel[j][1]); if(a>m)m=a; if(b>m)m=b; } }
  var CELL=2*m+1, GRID=ORI, rows=Math.ceil(NS/GRID), TW=GRID*CELL, TH=rows*CELL, D8=new Uint8Array(TW*TH);
  for(s=0;s<NS;s++){ t=A[s*NIVA+NIVA-1]; var ox=(s%GRID)*CELL+m, oy=((s/GRID)|0)*CELL+m;
    for(j=0;j<t.rel.length;j++) D8[(oy+t.rel[j][0])*TW+ox+t.rel[j][1]]=t.al[j]; }
  gl.pixelStorei(gl.UNPACK_ALIGNMENT,1);
  gl.bindTexture(gl.TEXTURE_2D,G.tAt); gl.texImage2D(gl.TEXTURE_2D,0,gl.R8,TW,TH,0,gl.RED,gl.UNSIGNED_BYTE,D8);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  G.atlas=A; G.cell=CELL; G.grid=GRID; G.tw=TW; G.th=TH; G.nt=NT;
}
/* l'état des poils, envoyé une fois (il ne change qu'avec le semis, les îles ou une caresse inscrite) */
function _glEtat(G, E){
  var gl=G.gl, ST=E.ST, N=ST.n, Q=ST.Q, CIX=ST.ci, BRD=ST.bd, POL=ST.po, EW=ST.ew, NC=E.NCOL, TDL=E.TDL, X=new Float32Array(N*9), i;
  for(i=0;i<N;i++){ var ci=CIX[i], st=0, o=i*9;
    if(ci>=NC){ st=TDL[ci-NC]; ci=NC; }
    var ja=(((i*2246822519)>>>0)%2048/2048-0.5)*0.74;
    X[o]=ci; X[o+1]=st; X[o+2]=POL?POL[i]/255:0; X[o+3]=EW?EW[i]/255:0;
    X[o+4]=BRD[i]; X[o+5]=Math.cos(ja); X[o+6]=Math.sin(ja); X[o+7]=(((i*2654435761)>>>0)%1024)/1024; X[o+8]=i%NVAR; }
  gl.bindBuffer(gl.ARRAY_BUFFER,G.bQ); gl.bufferData(gl.ARRAY_BUFFER, Q.subarray ? Q.subarray(0,N*10) : new Float32Array(Q).subarray(0,N*10), gl.STATIC_DRAW);
  gl.bindBuffer(gl.ARRAY_BUFFER,G.bE); gl.bufferData(gl.ARRAY_BUFFER, X, gl.STATIC_DRAW);
  G.st=ST; G.n=N; G.envois=(G.envois||0)+1;
}
function peintGL(cv,o){
  try{
    if(window._peloteGL===false) return false;
    if(o.emp || o.effleure || o.pastilles || o.nuLum || o.sonde || o.sansVerse || o.sansPeau || o.sansPlein || o.contre || o.duvet || o.dresse || !o.velours2) return false;
    var o2={}; for(var kq in o) o2[kq]=o[kq]; o2.seulementEtat=true;
    var E=peint(cv,o2); if(!E || !E.ST) return false;
    if(cv.__ntch) return false;                                   /* des poils encore marqués par un toucher : le peintre d'origine les rend */
    var W=E.W;
    if(!_GL || _GL.W!==W){ if(_GL===false) return false; _GL=_glInit(W); if(!_GL){ _GL=false; return false; } }
    var G=_GL, gl=G.gl;
    if(G.atlas!==E.A || G.nt!==E.TAI.length) _glAtlas(G, E.A, E.TAI.length);
    if(G.st!==E.ST || G.n!==E.ST.n) _glEtat(G, E);
    /* la table des couleurs (le sol, les îles, leurs marches) : elle suit la palette, le thème et le sol tiré */
    var COL=E.COL, nP=COL.length, kP='';
    if(!G.pal || G.pal.length!==nP*4) G.pal=new Uint8Array(nP*4);
    for(var c=0;c<nP;c++){ var v=COL[c]; G.pal[c*4]=v&255; G.pal[c*4+1]=(v>>>8)&255; G.pal[c*4+2]=(v>>>16)&255; G.pal[c*4+3]=255; }
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D,G.tPal);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA8,nP,1,0,gl.RGBA,gl.UNSIGNED_BYTE,G.pal);
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,G.tAt);
    /* 1 · la fourrure, dans sa cible : le plus opaque gagne */
    gl.bindFramebuffer(gl.FRAMEBUFFER,G.fb); gl.viewport(0,0,W,W);
    gl.disable(gl.BLEND); gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LESS); gl.depthMask(true);
    gl.clearColor(0,0,0,0); gl.clearDepth(1); gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    gl.useProgram(G.p1); var u=G.u1;
    gl.uniform1f(u.uCl,Math.cos(o.lac)); gl.uniform1f(u.uSl,Math.sin(o.lac)); gl.uniform1f(u.uCt,Math.cos(o.tan)); gl.uniform1f(u.uSt,Math.sin(o.tan));
    gl.uniform1f(u.uR,E.R); gl.uniform1f(u.uFOC,E.FOC); gl.uniform1f(u.uC,W/2); gl.uniform1f(u.uW,W);
    gl.uniform1f(u.uVel,o.velours||0); gl.uniform1f(u.uDoux,o.doux?1:0); gl.uniform1f(u.uPousse,E.POUSSE);
    gl.uniform1f(u.uNCOL,E.NCOL); gl.uniform1f(u.uNT,E.TAI.length); gl.uniform1f(u.uILE,E.ILE?1:0); gl.uniform1f(u.uETAGE,E.ETAGE); gl.uniform1f(u.uM,MARCHES);
    gl.uniform1f(u.uCell,G.cell); gl.uniform1f(u.uGrid,G.grid); gl.uniform1f(u.uORI,ORI); gl.uniform1f(u.uNVAR,NVAR); gl.uniform2f(u.uAtlas,G.tw,G.th);
    gl.uniform1i(u.uPal,1); gl.uniform1i(u.uAt,0);
    gl.bindVertexArray(G.vao); gl.drawArraysInstanced(gl.TRIANGLE_STRIP,0,4,G.n);
    /* 2 · la fourrure sur le corps plein, vers le canevas */
    gl.bindFramebuffer(gl.FRAMEBUFFER,null); gl.viewport(0,0,W,W); gl.disable(gl.DEPTH_TEST);
    gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(G.p2); var u2=G.u2, C=o.corps||[0,0,0];
    gl.bindTexture(gl.TEXTURE_2D,G.tFur); gl.uniform1i(u2.uFur,0);
    gl.uniform3f(u2.uCorps,C[0]/255,C[1]/255,C[2]/255); gl.uniform1f(u2.uA,o.corps?1:0);
    gl.uniform1f(u2.uR0,E.R*0.972); gl.uniform1f(u2.uR1,E.R*1.012); gl.uniform1f(u2.uC2,W/2); gl.uniform1f(u2.uW2,W);
    gl.bindVertexArray(G.vao2); gl.drawArrays(gl.TRIANGLES,0,3);
    gl.bindVertexArray(null);
    /* 3 · vers le canevas de la Pelote (celui que l'écran, le partage et les juges lisent) */
    if(cv.width!==W || cv.height!==W){ cv.width=W; cv.height=W; }
    var g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.globalCompositeOperation='copy'; g.drawImage(G.cv,0,0); g.globalCompositeOperation='source-over';
    /* la peau pleine que le juge du corps relit (`__po`) : la teinte du corps, à plat */
    if(o.corps){ if(!cv.__po || cv.__po.__gl!==1){ cv.__po=document.createElement('canvas'); cv.__po.width=4; cv.__po.height=4; cv.__po.__gl=1; }
      var kc=C.join(','); if(cv.__po.__k!==kc){ cv.__po.__k=kc; var pg=cv.__po.getContext('2d'); pg.fillStyle='rgb('+(C[0]|0)+','+(C[1]|0)+','+(C[2]|0)+')'; pg.fillRect(0,0,4,4); } }
    cv.__gl=(cv.__gl||0)+1;
    return true;
  }catch(e){ window._peloteGLErreur=String(e&&e.stack||e); _GL=false; return false; }
}
