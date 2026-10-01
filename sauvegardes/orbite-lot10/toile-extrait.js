
(function(){
var host=document.getElementById('toileCv'); if(!host)return;
var SIGNAL=[[208,176,255],[58,84,255],[240,122,46],[143,160,255]];
var PALS={signal:{name:'Signal',cols:SIGNAL},terre:{name:'Terre',cols:[[214,138,79],[168,96,64],[122,142,92],[221,190,140]]},ocean:{name:'Océan',cols:[[74,176,196],[58,110,196],[122,206,180],[168,140,224]]},aurore:{name:'Aurore',cols:[[247,168,184],[255,206,148],[196,184,240],[150,206,214]]},nuit:{name:'Nuit',cols:[[92,104,196],[150,96,180],[64,150,150],[196,120,110]]},foret:{name:'Forêt',cols:[[96,150,96],[64,110,88],[150,180,120],[190,200,140]]},braise:{name:'Braise',cols:[[214,96,72],[180,72,88],[230,150,90],[150,70,110]]},lavande:{name:'Lavande',cols:[[176,150,224],[140,130,210],[206,170,220],[150,180,224]]},agrume:{name:'Agrume',cols:[[224,190,70],[180,200,90],[120,180,120],[230,160,80]]},ardoise:{name:'Ardoise',cols:[[120,140,170],[96,110,150],[150,160,190],[110,150,170]]}};
var palKey='signal',hueShift=0;
function rotc(c,deg){var r=c[0]/255,gg=c[1]/255,bb=c[2]/255,mx=Math.max(r,gg,bb),mn=Math.min(r,gg,bb),l=(mx+mn)/2,hh,s,d=mx-mn;if(d===0){hh=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);hh=mx===r?((gg-bb)/d+(gg<bb?6:0)):mx===gg?((bb-r)/d+2):((r-gg)/d+4);hh/=6;}hh=(hh+deg/360)%1;if(hh<0)hh+=1;function h2(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}var q=l<0.5?l*(1+s):l+s-l*s,pp=2*l-q;return [Math.round(h2(pp,q,hh+1/3)*255),Math.round(h2(pp,q,hh)*255),Math.round(h2(pp,q,hh-1/3)*255)];}
function curPAL(){var base=PALS[palKey].cols;return hueShift?base.map(function(c){return rotc(c,hueShift);}):base;}
var PAL=SIGNAL;
var GPIX=[[40,42,49],[48,50,58],[35,37,44],[54,57,65],[44,47,55]], GBRA=[[27,29,36],[33,36,44],[23,25,32],[38,41,50],[30,33,41]], GLI=[[54,57,66],[62,65,74],[48,51,60],[68,71,80],[58,61,70]];var GMOS=[[58,60,70],[66,69,80],[50,53,63],[72,75,86],[62,65,76]], GENC=[[22,23,30],[28,30,38],[18,20,26],[33,35,44],[25,27,35]];
var TON=[1.0,0.76,1.24,0.88,1.12];
/* LUMIERE sur les dalles colorees : lift de clarte en HSL -> teinte et saturation STRICTEMENT preservees.
   LITS[0]=0 -> le code couleur exact de la palette est toujours present. Aucun assombrissement. */
var LITS=[0,0.10,0.04,0.14,0.07];
function _r2h(c){var r=c[0]/255,g2=c[1]/255,b2=c[2]/255,mx=Math.max(r,g2,b2),mn=Math.min(r,g2,b2),h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);h=mx===r?((g2-b2)/d+(g2<b2?6:0)):mx===g2?((b2-r)/d+2):((r-g2)/d+4);h/=6;}return [h,s,l];}
function _h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}if(s===0){var v=l*255;return [v,v,v];}var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
var _palLit=null;
function PALL(){if(_palLit)return _palLit;var base=curPAL(),out=[];for(var i=0;i<base.length;i++){var hs=_r2h(base[i]),row=[];for(var k=0;k<LITS.length;k++){row.push(LITS[k]===0?[base[i][0],base[i][1],base[i][2]]:_h2r(hs[0],hs[1],Math.min(0.965,hs[2]+LITS[k]*(1-hs[2]))));}out.push(row);}_palLit=out;return out;}
/* OMBRE sur les dalles grises : assombrit vers le noir, eclaire vers le blanc — jamais d'ecretage. */
function _shadeG(c,tone,shade){
  var t=(tone||1)-1, sh=shade||1, o=[0,0,0];
  var clair=isLightM();
  /* En clair, les dalles vides sont une crème CHAUDE : le ton ne les assombrit
     qu'à peine (sinon elles virent au gris terne), et ce qu'il enlève, il l'enlève
     surtout au bleu — l'ombre reste chaude au lieu de devenir cendreuse. */
  if(clair){
    /* le ton module doucement — assez pour qu'on voie la mosaïque, jamais assez
       pour la ternir. Et ce qu'il enlève, il l'enlève surtout au bleu : l'ombre
       reste chaude, elle ne vire pas à la cendre. */
    var d=(t<0)?(1+t*0.30):(1+t*0.12);
    var chaud=[1.0,0.985,0.958];
    for(var i=0;i<3;i++){
      var v=c[i]*d*(1+(sh-1)*0.5);
      if(t<0)v*=chaud[i];
      o[i]=v<0?0:(v>255?255:v);
    }
    return o;
  }
  for(var i=0;i<3;i++){var v=c[i];v=(t<0)?v*(1+t*0.9):(v+(255-v)*(t*0.35));v*=sh;o[i]=v<0?0:(v>255?255:v);}
  return o;
}
var TH={pixel:{g:GPIX},braille:{g:GBRA},sillons:{g:GLI},gravure:{g:GLI},mosaique:{g:GMOS},encre:{g:GENC},eclats:{g:GMOS},terrazzo:{g:GENC},touffe:{g:GENC}};
var theme='encre', g,W,H,DPR, seeds=[], lastChange=0, running=false, lastNuee=null, view={s:1,ox:0,oy:0}, _qT0=0;
function isLightM(){if(typeof window!=='undefined'&&window._shThemeOverride!=null)return window._shThemeOverride;var d=document.getElementById('device');return d&&d.classList.contains('light');}
/* mode clair : du CRÈME, pas du gris. La Toile doit respirer, pas ternir. */
var GLIGHT=[[250,243,229],[255,250,239],[244,235,219],[252,246,234],[247,239,224]];
function grays(){return isLightM()?GLIGHT:TH[theme].g;}
function size(){
  var st=host.parentNode;
  var w=st.clientWidth, h=st.clientHeight;
  /* la Toile est cachée (on est dans le Fil) : on ne touche à RIEN.
     Sans ce garde-fou, un redimensionnement pendant le Fil — la barre d'URL du
     téléphone qui bouge au scroll, par exemple — mettait le canvas à 0x0
     et la Toile ne revenait jamais. */
  if(!w||!h)return;
  DPR=Math.min(2,window.devicePixelRatio||1);
  W=w; H=h; host.width=W*DPR; host.height=H*DPR;
  g=host.getContext('2d'); if(!seeds.length)seedGray(); kick();
}
window.Toile_resize=size;
function mk(x,y,k){return {x:x,y:y,tx:x,ty:y,gray:grays()[(Math.random()*5)|0],gc:null,ci:null,c:null,t0:0,kind:k||'gray',w:0,wt:0,tone:TON[(Math.random()*TON.length)|0],lit:0,shade:0.96+Math.random()*0.08,ang:Math.random()*Math.PI,ph:Math.random()*6.28,am:0.6+Math.random()*0.7};}
function avg(){return Math.sqrt(W*H/Math.max(1,seeds.length));}
function seedGray(){seeds=[];var base=72,gc=Math.max(2,Math.round(W/base)),gr=Math.max(3,Math.round(H/base)),cw=W/gc,ch=H/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++){if(Math.random()<0.14)continue;seeds.push(mk(cw*(c+.5)+(Math.random()-.5)*cw*.55,ch*(r+.5)+(Math.random()-.5)*ch*.55));}var ex=Math.round(gc*gr*0.28);for(var e=0;e<ex;e++)seeds.push(mk(Math.random()*W,Math.random()*H));}
function nbU(s){var u={},l=avg()*1.6;l*=l;for(var j=0;j<seeds.length;j++){var o=seeds[j];if(o===s||o.ci==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<l)u[o.ci]=true;}return u;}
function iposNuee(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();if(!col.length)return ipos();var cx=0,cy=0;col.forEach(function(s){cx+=s.x;cy+=s.y;});cx/=col.length;cy/=col.length;var topB=H*0.17,botB=H*0.84;for(var t=0;t<40;t++){var a=Math.random()*6.28,r=(1.7+Math.random()*0.7)*ac;var x=Math.max(8,Math.min(W-8,cx+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,cy+Math.sin(a)*r));if(col.length<15&&(y<topB||y>botB))continue;var ok=true;for(var j=0;j<col.length;j++){var dx=x-col[j].x,dy=y-col[j].y;if(dx*dx+dy*dy<(ac*1.45)*(ac*1.45)){ok=false;break;}}if(ok)return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,cx+(Math.random()-.5)*ac*2)),y:Math.max(topB,Math.min(botB,cy+(Math.random()-.5)*ac*2))};}
function ipos(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();var few=col.length<15,topB=H*0.17,botB=H*0.84;function danger(x,y){if(!few)return false;if(y<topB||y>botB)return true;if(x>W*0.6&&y<H*0.2)return true;return false;}if(!col.length)return {x:W/2+(Math.random()-.5)*ac,y:H*0.5+(Math.random()-.5)*ac};var an=col[(Math.random()*col.length)|0];for(var t=0;t<12;t++){var sp=(Math.random()<0.72)?(0.95+Math.random()*0.22):(1.45+Math.random()*0.7);var a=Math.random()*6.28,r=ac*sp;var x=Math.max(8,Math.min(W-8,an.x+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,an.y+Math.sin(a)*r));if(!danger(x,y))return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,an.x+(Math.random()-.5)*ac)),y:Math.max(topB,Math.min(botB,an.y+(Math.random()-.5)*ac))};}
function cc(s){var u=nbU(s),av=[];for(var p=0;p<PAL.length;p++)if(!u[p])av.push(p);return av.length?av[(Math.random()*av.length)|0]:((Math.random()*PAL.length)|0);}
function tones(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();for(var i=0;i<col.length;i++)col[i].lit=null;for(var i=0;i<col.length;i++){var s=col[i],u={};for(var j=0;j<col.length;j++){if(j===i)continue;var o=col[j];if(o.lit==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<(ac*1.5)*(ac*1.5))u[o.lit]=true;}var pk=0;for(var t=0;t<LITS.length;t++){if(!u[t]){pk=t;break;}}s.lit=pk;}}
/* ---------- LE RECUL ----------
   Une Toile de 70 cellules avec un seul Promi, vue en entier, c'est un écran vide
   et triste. On se rapproche donc des premières dalles — puis, à CHAQUE dalle
   plantée, la vue RECULE d'un cran. Les proportions ne changent jamais : c'est le
   cadrage qui s'ouvre, à mesure que la Toile se remplit de couleur.
   Au-delà d'une dizaine de Promi, on voit la Toile entière : elle se suffit. */
var vTarget=null;
/* le champ clair : la barre du haut (titre + bascule Toile/Fil) et le dock */
var HAUT_LIBRE=176, BAS_LIBRE=138;
function autoView(){
  /* Zoom intelligent : on cadre les dalles COLOREES (pas toute la Toile),
     en gardant une marge et en plafonnant le zoom pour ne jamais tomber
     dans le vide ni grossir betement une seule dalle. Beaucoup de dalles
     => Toile entiere (elle se suffit). Barre du haut et dock evites. */
  var col=seeds.filter(function(s){return s.kind!=='gray';});
  if(!col.length){ vTarget={s:1,ox:0,oy:0}; return; }
  var n=col.length;
  if(n>=20){ vTarget={s:1,ox:0,oy:0}; return; }   /* Toile bien remplie : Toile entiere */
  /* bounding-box de TOUTES les dalles colorees -> on les cadre toutes a l'ecran */
  var minX=1e9,maxX=-1e9,minY=1e9,maxY=-1e9;
  col.forEach(function(s){if(s.x<minX)minX=s.x;if(s.x>maxX)maxX=s.x;if(s.y<minY)minY=s.y;if(s.y>maxY)maxY=s.y;});
  var pad=avg()*1.3;                        /* marge d'une dalle autour */
  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;
  var bw=Math.max(1,maxX-minX), bh=Math.max(1,maxY-minY);
  var topB=HAUT_LIBRE, botB=H-BAS_LIBRE;    /* zone utile (barre haut + dock evites) */
  var availW=W*0.92, availH=Math.max(1,botB-topB);
  var s=Math.min(availW/bw, availH/bh);
  s=Math.max(1.0, Math.min(s, 2.0));        /* jamais plus loin que la Toile entiere, plafond 2.0 */
  var cx=(minX+maxX)/2, cy=(minY+maxY)/2, scx=W/2, scy=(topB+botB)/2;
  var _ox=scx-cx*s, _oy=scy-cy*s;
  /* clamp : les bords de la Toile restent colles aux bords de l ecran (jamais de vide) */
  _ox=Math.max(W-W*s, Math.min(0, _ox));
  _oy=Math.max(H-H*s, Math.min(0, _oy));
  vTarget={ s:s, ox:_ox, oy:_oy };
}
window.Toile_autoView=function(){autoView();kick();};
function relax(){var ac=avg();for(var i=0;i<seeds.length;i++){var s=seeds[i],fx=0,fy=0;for(var j=0;j<seeds.length;j++){if(j===i)continue;var o=seeds[j];var dx=s.x-o.x,dy=s.y-o.y,d=Math.sqrt(dx*dx+dy*dy);var w=ac*(0.92+s.w*0.026+o.w*0.026);if(d<w&&d>0.01){var f=(w-d)/d*0.16;fx+=dx*f;fy+=dy*f;}}s.tx=Math.max(6,Math.min(W-6,s.x+fx));s.ty=Math.max(6,Math.min(H-6,s.y+fy));}
}
function ease(p){return p<0?0:p>1?1:p*p*(3-2*p);}
function kick(){if(!running){running=true;requestAnimationFrame(frame);}}
function liven(){_qT0=performance.now();kick();}window.Toile_liven=liven;window.Toile_probe=function(){var o=[];for(var i=0;i<seeds.length;i++){if(seeds[i].kind!=='gray'){var s=seeds[i];o.push([Math.round(((s.px==null?s.x:s.px)-s.x)*10)/10,Math.round(((s.py==null?s.y:s.py)-s.y)*10)/10]);}}return o;};window.Toile_state=function(){return {running:running,qt:_qT0,theme:theme};};window.Toile_previewLive=function(pcv,th,pw,ph){
  if(!pcv||!pcv.getContext)return;
  th=(th&&TH[th])?th:'encre';
  var dpr=Math.min(2,window.devicePixelRatio||1);
  pcv.width=Math.round(pw*dpr);pcv.height=Math.round(ph*dpr);pcv.style.width=pw+'px';pcv.style.height=ph+'px';
  if(!pcv.__pls||pcv.__plth!==th||Math.abs((pcv.__plpw||0)-pw)>2){
    try{window.Toile.preview(pcv,th,pw,ph);}catch(e){}
    var src=(pcv.__c&&pcv.__c.seeds)?pcv.__c.seeds:[];
    var tpl=null;for(var _i=0;_i<src.length;_i++){if(src[_i].kind!=='gray'){tpl=src[_i];break;}}
    tpl=tpl||src[0]||{ci:0,c:null,tone:1,lit:0,shade:1,ang:0,w:0};
    pcv.__pls=src.map(function(o){return {x:o.x,y:o.y,gray:false,gc:null,ci:tpl.ci,c:tpl.c,kind:'promi',tone:tpl.tone,lit:tpl.lit,shade:tpl.shade,ang:o.ang,w:o.w,t0:-99999};});
    var im=(typeof _pdImgs!=='undefined'&&_pdImgs[th])?_pdImgs[th]:null;
    var iw=(im&&im.naturalWidth)||420, ih=(im&&im.naturalHeight)||420;
    var TAR=pw*0.52, kk=TAR/Math.max(iw,ih), bw=iw*kk, bh=ih*kk;
    var bL=pw-Math.round(pw*0.03)-bw, bT=Math.round(ph*0.40)-bh/2;
    pcv.__box={cx:bL+bw/2, cy:bT+bh/2, rx:bw/2, ry:bh/2};
    var N=48, pts=[];for(var _a=0;_a<N;_a++){pts.push({ang:_a/N*6.2832, ph:Math.random()*6.28, fr:1.4+Math.random()*1.9});}
    pcv.__cpts=pts;
    pcv.__plth=th;pcv.__plpw=pw;pcv.__plph=ph;
  }
  pcv.__plqt=performance.now();
  if(pcv.__plraf)cancelAnimationFrame(pcv.__plraf);
  var _d=pcv.width/pw;
  function step(){
    var age=performance.now()-pcv.__plqt, DUR=1300, quiv=age<DUR, env=Math.exp(-age/430);
    var box=pcv.__box, pts=pcv.__cpts;
    var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};
    try{
      g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};seeds=pcv.__pls;
      g.setTransform(_d,0,0,_d,0,0);g.clearRect(0,0,pw,ph);
      var AMP=quiv?(box.rx*0.05)*env+2.5*env:0;
      var P=[];
      for(var i=0;i<pts.length;i++){
        var pt=pts[i];
        var wob=Math.sin(age*0.004*pt.fr+pt.ph)*AMP + Math.sin(age*0.0026+pt.ang*3+pt.ph)*AMP*0.55;
        P.push([box.cx+Math.cos(pt.ang)*(box.rx+wob), box.cy+Math.sin(pt.ang)*(box.ry+wob)]);
      }
      g.save();g.beginPath();
      var n=P.length, mx=(P[n-1][0]+P[0][0])/2, my=(P[n-1][1]+P[0][1])/2;
      g.moveTo(mx,my);
      for(var j=0;j<n;j++){var c=P[j], nnx=(P[j][0]+P[(j+1)%n][0])/2, nny=(P[j][1]+P[(j+1)%n][1])/2;g.quadraticCurveTo(c[0],c[1],nnx,nny);}
      g.closePath();g.clip();
      RD[theme](performance.now(),0,0,pw,ph);
      g.restore();
    }catch(e){}
    g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;
    if(quiv)pcv.__plraf=requestAnimationFrame(step);else pcv.__plraf=0;
  }
  step();
};
function cAt(x,y){var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}return seeds[bi];}
function cOf(s,now){var g0=s.gc||(s.gc=_shadeG(s.gray,s.tone,s.shade));if(s.kind==='gray'&&(s.t0===0||now-s.t0>760))return g0;var p=ease((now-s.t0)/760);var to=s.ci!=null?PALL()[s.ci][s.lit|0]:g0;var c=[g0[0]+(to[0]-g0[0])*p,g0[1]+(to[1]-g0[1])*p,g0[2]+(to[2]-g0[2])*p];for(var q=0;q<3;q++){if(c[q]>255)c[q]=255;if(c[q]<0)c[q]=0;}return c;}
function Rpix(now,x0,y0,x1,y1){var STEP=5;g.setTransform(DPR,0,0,DPR,0,0);for(var sy=0;sy<H;sy+=STEP){for(var sx=0;sx<W;sx+=STEP){var lx=(sx+2.5-view.ox)/view.s,ly=(sy+2.5-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx,sy,STEP+1,STEP+1);}}}
function Rbra(now,x0,y0,x1,y1){var DOT=9,sx=Math.floor(x0/DOT)*DOT+DOT*.5,sy=Math.floor(y0/DOT)*DOT+DOT*.5;for(var y=sy;y<y1;y+=DOT){for(var x=sx;x<x1;x+=DOT){var bd=1e18,bd2=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd2=bd;bd=d;bi=k;}else if(d<bd2)bd2=d;}var s=seeds[bi],c=cOf(s,now),ed=(bd2-bd)<5,rad=(s.kind==='gray')?2:(ed?2:2.9);g.beginPath();g.arc(x,y,rad,0,6.2832);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fill();}}}
function Rsil(now,x0,y0,x1,y1){g.lineCap='round';g.lineJoin='round';var SP=6,AMP=4.5,WL=0.018,LS=6;function wv(xx,ln){return AMP*Math.sin(xx*WL+ln*.55)+AMP*.62*Math.sin(xx*WL*2.4-ln*.42+1.2);}var li=Math.floor(y0/SP);for(var bY=li*SP+SP*.5;bY<y1;bY+=SP,li++){var sX=Math.max(0,x0),run=[],rk=null,rcl=false;function flush(){if(run.length>1){g.beginPath();g.strokeStyle='rgb('+rk+')';g.lineWidth=rcl?1.5:0.85;g.moveTo(run[0][0],run[0][1]);for(var q=1;q<run.length;q++)g.lineTo(run[q][0],run[q][1]);g.stroke();}}for(var x=sX;x<=x1;x+=LS){var y=bY+wv(x,li);var s=cAt(x,bY),c=cOf(s,now),key=(c[0]|0)+','+(c[1]|0)+','+(c[2]|0);if(rk!==null&&key!==rk){var last=run[run.length-1];flush();run=[last];}run.push([x,y]);rk=key;rcl=(s.kind!=='gray');}flush();}}
function Rgra(now,x0,y0,x1,y1){g.lineCap='round';g.lineJoin='round';var HS=8,SS=5,ac=avg();for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=cl?2:1.05;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,ex=qx-_kx,ey=qy-_ky,d=Math.sqrt(ex*ex+ey*ey)-seeds[k].w;if(d<bd){bd=d;bi=k;}}var ins=(bi===ci)&&qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins&&!run){run=true;g.beginPath();g.moveTo(qx,qy);}else if(ins){g.lineTo(qx,qy);}else if(run){g.stroke();run=false;}}if(run)g.stroke();}}}
function Rmos(now,x0,y0,x1,y1){var T=11;g.setTransform(DPR,0,0,DPR,0,0);for(var sy=0;sy<H;sy+=T){for(var sx=0;sx<W;sx+=T){var lx=(sx+T/2-view.ox)/view.s,ly=(sy+T/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx+1,sy+1,T-2,T-2);}}}
function Renc(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var px=_sx*view.s+view.ox,py=_sy*view.s+view.oy;var rad=sp*0.6*view.s;if(px<-rad*2.5||px>W+rad*2.5||py<-rad*2.5||py>H+rad*2.5)continue;var c=cOf(s,now);g.save();g.translate(px,py);if(s.drot)g.rotate(s.drot);if(s.dsx)g.scale(s.dsx,s.dsy);g.fillStyle='rgba('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+',.9)';var sd=((k+1)*2654435761)>>>0,rnd=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};for(var b=0;b<9;b++){var _ex=(rnd()-.5)*rad*1.2,_ey=(rnd()-.5)*rad,_rx=rad*(.32+rnd()*.42),_ry=rad*(.16+rnd()*.32),_ea=rnd()*3.14;if(s.dw){var _wp=s.ph+b*1.7;_ex+=Math.sin(now*0.006+_wp)*rad*0.22*s.dw;_ey+=Math.cos(now*0.0072+_wp)*rad*0.18*s.dw;_rx*=1+Math.sin(now*0.0085+_wp)*0.26*s.dw;_ry*=1+Math.cos(now*0.0079+_wp)*0.26*s.dw;_ea+=Math.sin(now*0.005+_wp)*0.6*s.dw;}g.beginPath();g.ellipse(_ex,_ey,_rx,_ry,_ea,0,6.3);g.fill();}g.restore();}}
function Rblok(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var c=cOf(s,now);var h=((s.x*13.1+s.y*7.7)%100+100)%100/100;var bw=sp*(0.74+h*0.32),bh=sp*(0.74+(1-h)*0.32);var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);g.save();g.translate(_sx,_sy);g.rotate((h-0.5)*0.36);g.fillStyle="rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";g.beginPath();var rr=Math.min(bw,bh)*0.14;var xx=-bw/2,yy=-bh/2;g.moveTo(xx+rr,yy);g.arcTo(xx+bw,yy,xx+bw,yy+bh,rr);g.arcTo(xx+bw,yy+bh,xx,yy+bh,rr);g.arcTo(xx,yy+bh,xx,yy,rr);g.arcTo(xx,yy,xx+bw,yy,rr);g.closePath();g.fill();g.restore();}}

function Rterr(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var c=cOf(s,now);var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var sd=((k+1)*2654435761)>>>0;var rr=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};g.fillStyle="rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";for(var e=0;e<7;e++){var a=rr()*6.2832,rd=rr()*sp*0.46;var ex=_sx+Math.cos(a)*rd,ey=_sy+Math.sin(a)*rd;var w2=sp*(0.11+rr()*0.19),h2=sp*(0.08+rr()*0.15);g.save();g.translate(ex,ey);g.rotate(rr()*3.1416);g.beginPath();var sides=4+((rr()*3)|0);for(var s2=0;s2<sides;s2++){var an=s2/sides*6.2832;var px=Math.cos(an)*w2*(0.7+rr()*0.5),py=Math.sin(an)*h2*(0.7+rr()*0.5);s2?g.lineTo(px,py):g.moveTo(px,py);}g.closePath();g.fill();g.restore();}}}
function _tfInk(){return isLightM()?[34,28,21]:[246,241,231];}
function _tfHand(g,pts,jit,rnd){g.beginPath();var n=pts.length;for(var i=0;i<=n;i++){var A=pts[i%n],B=pts[(i+1)%n];var ax=A[0]+(rnd()-.5)*jit, ay=A[1]+(rnd()-.5)*jit;if(i===0){g.moveTo(ax,ay);continue;}var mx=(A[0]+B[0])/2+(rnd()-.5)*jit*1.3, my=(A[1]+B[1])/2+(rnd()-.5)*jit*1.3;g.quadraticCurveTo(mx,my,ax,ay);}g.closePath();}
function _tfStroke(g,w,col,alpha){g.lineJoin="round";g.lineCap="round";g.strokeStyle="rgba("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+","+(alpha==null?1:alpha)+")";g.lineWidth=w;g.stroke();}
function _tfFill(g,col,rnd,off){g.save();g.translate((rnd()-.5)*off,(rnd()-.5)*off);g.fillStyle="rgb("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+")";g.fill();g.restore();}
function _tfPetal(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.8+j(), j()*0.6, len+j());g.bezierCurveTo(-wid*0.72+bend+j(), len*0.8+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function _tfPetalR(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};var tw=wid*0.3;g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.82, tw+bend+j(), len*0.95);g.quadraticCurveTo(bend+j(), len*1.0, -tw+bend+j(), len*0.95);g.bezierCurveTo(-wid*0.72+bend+j(), len*0.82+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function Rtouf(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));var ink=_tfInk();for(var i=0;i<seeds.length;i++){var s=seeds[i];var c=cOf(s,now);var sx=(s.px!=null?s.px:s.x),sy=(s.py!=null?s.py:s.y);var _sd=((i+1)*2654435761)>>>0;var rnd=function(){_sd=(_sd*1103515245+12345)&0x7fffffff;return _sd/0x7fffffff;};var heart=(s.kind==="gray")?[150,150,153]:[240,122,46];var n=3+((rnd()*3)|0);for(var f2=0;f2<n;f2++){var ox=sx+(rnd()-.5)*sp*0.86, oy=sy+(rnd()-.5)*sp*0.8;var R=sp*(0.13+rnd()*0.2);var stage=rnd();g.strokeStyle="rgba("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+",0.6)";g.lineWidth=Math.max(1.2,R*0.2);g.lineCap="round";g.beginPath();g.moveTo(ox+(rnd()-.5)*5,oy+sp*0.5);g.quadraticCurveTo(ox+(rnd()-.5)*R,oy+sp*0.2,ox,oy);g.stroke();g.save();g.translate(ox,oy);g.rotate(rnd()*6.2832);if(stage<0.24){var bp=[[-R*0.4,R*0.3],[-R*0.34,-R*0.4],[0,-R*0.72],[R*0.34,-R*0.4],[R*0.4,R*0.3]];_tfHand(g,bp,R*0.08,rnd);_tfFill(g,c,rnd,R*0.08);_tfHand(g,bp,R*0.08,rnd);_tfStroke(g,Math.max(1.1,R*0.17),ink,0.9);}else{var np=6+((rnd()*3)|0);for(var k=0;k<np;k++){if(stage>0.8&&rnd()<0.2)continue;g.save();g.rotate(k/np*6.2832+(rnd()-.5)*0.34);var len=R*(0.85+rnd()*0.6), wid=R*(0.26+rnd()*0.16);var _rd=(((i*13+f2*7+k*5)%10)<2);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfFill(g,c,rnd,R*0.09);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfStroke(g,Math.max(1,R*0.16),ink,0.88);g.restore();}g.beginPath();g.arc((rnd()-.5)*R*0.12,(rnd()-.5)*R*0.12,R*0.3,0,6.2832);g.fillStyle="rgb("+heart[0]+","+heart[1]+","+heart[2]+")";g.fill();_tfStroke(g,Math.max(1,R*0.15),ink,0.85);}g.restore();}}}
var RD={pixel:Rpix,braille:Rbra,sillons:Rsil,gravure:Rgra,mosaique:Rmos,encre:Renc,eclats:Rblok,terrazzo:Rterr,touffe:Rtouf};

/* --- LES ÉTIQUETTES, sur la Toile elle-même ---
   L'app fournit le texte (window.Toile.labelOf) et dit si le mode est actif
   (window.Toile.labelsOn). L'encre est choisie par dalle : claire sur une
   dalle sombre, sombre sur une dalle claire — jamais de contour, jamais de voile. */
function _lum(c){
  function l(v){v/=255;return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);}
  return 0.2126*l(c[0])+0.7152*l(c[1])+0.0722*l(c[2]);
}
function _fit(gg,txt,max){
  if(gg.measureText(txt).width<=max)return txt;
  var t=txt;
  while(t.length>1&&gg.measureText(t+'…').width>max)t=t.slice(0,-1);
  return t+'…';
}
function _labels(now){
  /* pendant l'onboarding, la Toile est un décor : pas de texte sur les dalles,
     même si le Studio est réglé « avec texte » */
  var _ob=document.getElementById('promiOnb');
  if(_ob&&!_ob.classList.contains('gone'))return;
  var T=window.Toile;
  if(!T||typeof T.labelsOn!=='function'||!T.labelsOn())return;
  if(typeof T.labelOf!=='function')return;
  g.setTransform(DPR,0,0,DPR,0,0);
  g.textAlign='center';g.textBaseline='middle';
  var ac=avg();                                  /* écart moyen entre dalles */
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    if(s.kind==='gray')continue;
    /* un Promi masque au partage n'affiche pas son texte non plus */
    if(window._shLabels!==undefined&&s.pid!=null&&(window.shareHidden||{})[s.pid])continue;
    var L=null;try{L=T.labelOf(s);}catch(e){}
    if(!L||!L.title)continue;
    /* la dalle est dessinée à px/py (position réellement occupée) : l'étiquette doit suivre,
       sinon le texte reste à côté de sa dalle. */
    var _lx=(s.px!=null?s.px:s.x), _ly=(s.py!=null?s.py:s.y);
    var sx=_lx*view.s+view.ox, sy=_ly*view.s+view.oy;
    if(sx<-60||sy<-40||sx>W+60||sy>H+40)continue;
    var wmax=Math.max(28, ac*view.s*0.86);       /* on reste DANS la dalle */
    var col=cOf(s,now);
    var ink=(_lum(col)>0.179)?'#101218':'#FFFFFF';
    var fs=Math.max(7.5, Math.min(13, ac*view.s*0.155));
    g.fillStyle=ink;
    if(L.who){
      g.font='600 '+(fs*0.68).toFixed(1)+'px Apfel,system-ui,sans-serif';
      g.globalAlpha=0.72;
      g.fillText(_fit(g,String(L.who).toUpperCase(),wmax), sx, sy-fs*0.72);
      g.globalAlpha=1;
    }
    g.font='500 '+fs.toFixed(1)+'px Apfel,system-ui,sans-serif';
    g.fillText(_fit(g,L.title,wmax), sx, sy+fs*0.34);
  }
}

/* --- LA FORME RÉELLE D'UNE DALLE ---
   Pour que l'Index montre la MÊME dalle que la Toile, et non un pictogramme.
   On découpe le cadre par les bissectrices, exactement comme le rendu. */
function _cellPoly(s){
  var poly=[[0,0],[W,0],[W,H],[0,H]];
  for(var k=0;k<seeds.length;k++){
    var o=seeds[k]; if(o===s)continue;
    var dx=o.x-s.x, dy=o.y-s.y;
    var d=Math.sqrt(dx*dx+dy*dy); if(d<0.001)continue;
    var nx=dx/d, ny=dy/d;
    /* la frontière se décale du côté de la dalle la plus « lourde » */
    var m=d/2 + ((s.w||0)-(o.w||0))/2;
    var px=s.x+nx*m, py=s.y+ny*m;
    var out=[],n=poly.length;
    for(var i=0;i<n;i++){
      var A=poly[i], B=poly[(i+1)%n];
      var da=(A[0]-px)*nx+(A[1]-py)*ny;
      var db=(B[0]-px)*nx+(B[1]-py)*ny;
      if(da<=0)out.push(A);
      if((da<0&&db>0)||(da>0&&db<0)){
        var t=da/(da-db);
        out.push([A[0]+(B[0]-A[0])*t, A[1]+(B[1]-A[1])*t]);
      }
    }
    poly=out; if(poly.length<3)return null;
  }
  return poly;
}
var LIVE={encre:1,terrazzo:1,touffe:1,eclats:1};
function frame(now){if(!g){running=false;return;}var _ss=document.getElementById('studioScreen');if(_ss&&_ss.classList.contains('show')){requestAnimationFrame(frame);return;}var _stg=document.getElementById('stage');if(_stg&&_stg.style.display==='none'){running=false;return;}
  /* une dalle qui vient de se planter GRANDIT : elle pousse ses voisines, et la
     Toile entière se réajuste autour d'elle tant que la place n'est pas faite. */
  var grow=false;
  for(var q=0;q<seeds.length;q++){
    var sq=seeds[q];
    if(sq.wt==null)sq.wt=sq.w;
    if(Math.abs(sq.wt-sq.w)>0.04){ sq.w+=(sq.wt-sq.w)*0.13; grow=true; }
    else if(sq.w!==sq.wt){ sq.w=sq.wt; grow=true; }
  }
  if(grow)relax();
  var mv=false,grow=false;
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    /* la poussée retombe : la dalle s'est fait sa place, elle se détend */
    if(s.wAt&&now>=s.wAt){s.wt=s.wFin;s.wAt=0;}
    if(s.wt!==undefined&&Math.abs(s.wt-s.w)>0.04){s.w+=(s.wt-s.w)*0.17;grow=true;}
    s.x+=(s.tx-s.x)*.22;s.y+=(s.ty-s.y)*.22;
    if(Math.abs(s.tx-s.x)+Math.abs(s.ty-s.y)>.6)mv=true;
  }
  /* tant qu'une dalle grandit, la Toile entière se recalcule autour d'elle */
  /* la poussée se propage de proche en proche : toute la Toile réagit */
  if(grow){relax();relax();relax();mv=true;}
  if(grow)mv=true;var an=mv;for(i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray'&&now-seeds[i].t0<760)an=true;if(!Object.keys(ptrs).length){
    if(vTarget){
      /* la vue glisse vers son cadrage : un recul doux, jamais un saut */
      var ds=vTarget.s-view.s, dx=vTarget.ox-view.ox, dy=vTarget.oy-view.oy;
      if(Math.abs(ds)>0.003||Math.abs(dx)>0.6||Math.abs(dy)>0.6){
        view.s+=ds*0.085; view.ox+=dx*0.085; view.oy+=dy*0.085; an=true;
      }else{
        view.s=vTarget.s; view.ox=vTarget.ox; view.oy=vTarget.oy;
      }
    }
    var ts=Math.max(0.48,Math.min(5,view.s));
    if(Math.abs(ts-view.s)>0.002){view.s+=(ts-view.s)*0.3;an=true;}else{view.s=ts;}
    cp();
  }g.setTransform(DPR,0,0,DPR,0,0);g.clearRect(0,0,W,H);var bg=g.createLinearGradient(0,0,W*0.55,H);if(isLightM()){
    /* le fond se creuse d'un ton : sans cela, les dalles vides — crème, très claires —
       se noyaient dedans, et les mondes braille/sillons/gravure ne dessinaient plus rien.
       En sombre, on ne touche à rien : c'est déjà juste. */
    bg.addColorStop(0,'#E2D8C4');bg.addColorStop(1,'#D4C8AF');
  }else{bg.addColorStop(0,'#14161d');bg.addColorStop(1,'#0a0b10');}g.fillStyle=bg;g.fillRect(0,0,W,H);g.setTransform(view.s*DPR,0,0,view.s*DPR,view.ox*DPR,view.oy*DPR);var x0=Math.max(0,(-view.ox)/view.s),y0=Math.max(0,(-view.oy)/view.s),x1=Math.min(W,(-view.ox)/view.s+W/view.s),y1=Math.min(H,(-view.oy)/view.s+H/view.s);var rr=14;g.save();g.beginPath();g.moveTo(rr,0);g.arcTo(W,0,W,H,rr);g.arcTo(W,H,0,H,rr);g.arcTo(0,H,0,0,rr);g.arcTo(0,0,W,0,rr);g.closePath();g.clip();var _isG=(theme==='pixel'||theme==='mosaique'||theme==='braille'||theme==='sillons'||theme==='gravure');var _dur=_isG?850:1100;var _qa=performance.now()-_qT0,_quiv=(_qT0>0&&_qa>=0&&_qa<_dur);for(var _pi=0;_pi<seeds.length;_pi++){var _ps=seeds[_pi];if(_ps.kind==='gray'){_ps.px=_ps.x;_ps.py=_ps.y;continue;}if(_ps.ph==null){_ps.ph=Math.random()*6.28;_ps.am=0.6+Math.random()*0.7;}if(_quiv){var _LA=(typeof window!=='undefined'&&window._liveAmp!=null)?window._liveAmp:1;var _env=Math.exp(-_qa/(_isG?300:380));var _pa=_isG?11:7,_pay=_isG?8:5;_ps.px=_ps.x+Math.sin(_qa*0.0092+_ps.ph)*_pa*_ps.am*_env*_LA;_ps.py=_ps.y+Math.cos(_qa*0.0096+_ps.ph)*_pay*_ps.am*_env*_LA;_ps.dsx=1+Math.sin(_qa*0.0100+_ps.ph)*0.09*_env*_LA;_ps.dsy=1+Math.cos(_qa*0.0112+_ps.ph*1.2)*0.09*_env*_LA;_ps.drot=Math.sin(_qa*0.0085+_ps.ph*0.7)*0.08*_env*_LA;_ps.dw=_env*_LA;}else{_ps.px=_ps.x;_ps.py=_ps.y;_ps.dsx=1;_ps.dsy=1;_ps.drot=0;_ps.dw=0;}}if(seeds.length)RD[theme](now,x0,y0,x1,y1);g.restore();
  try{_labels(now);}catch(e){}if(an||now-lastChange<170||_quiv)requestAnimationFrame(frame);else running=false;}
function addP(k){
  if(!seeds.length)seedGray();
  var p=(k==='nuee')?iposNuee():ipos();
  var s=mk(p.x,p.y,k||'promi');
  s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();
  /* Elle naît minuscule, POUSSE pour se faire une place — les voisines s'écartent —
     puis se détend jusqu'à sa taille de croisière. C'est le geste : une dalle s'insère,
     la Toile entière se réajuste autour d'elle, puis se repose. */
  s.w=-22; s.wt=(k==='nuee')?18:12;
  s.wFin=(k==='nuee')?14:3.4; s.wAt=performance.now()+380;
  seeds.push(s);
  if(k==='nuee'){lastNuee=s;}
  relax();tones();lastChange=s.t0;var te=document.getElementById('toileEmpty');if(te)te.style.display='none';kick();return s;}
var nueeCells={};window.Toile={addPromi:function(id){var s=window.Toile.plantOne();if(!s)s=addP('promi');if(s&&id!=null)s.pid=id;return s;},
  /* la dalle sous le doigt : même métrique que le rendu, au pixel près */
  hit:function(cx,cy){
    if(!seeds.length)return null;
    var lx=(cx-view.ox)/view.s, ly=(cy-view.oy)/view.s;
    var bd=1e18,bs=null;
    for(var k=0;k<seeds.length;k++){
      var dx=lx-seeds[k].x, dy=ly-seeds[k].y;
      var d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;
      if(d<bd){bd=d;bs=seeds[k];}
    }
    if(!bs||bs.kind==='gray')return null;
    return {pid:(bs.pid!=null?bs.pid:null), kind:bs.kind, nuee:bs.nuee||null};
  },
  /* remet la Toile en accord avec les Promi réels : 1 Promi = 1 dalle */
  sync:function(list){
    if(!seeds.length)seedGray();
    /* Les dalles REDEVIENNENT des cellules vides — on ne les SUPPRIME pas.
       Avant, sync() les arrachait du tableau : quand l'onboarding laissait une
       Toile pleine de couleur (donc zéro cellule vide), il ne restait qu'une
       poignée de cellules. La Toile paraissait alors monstrueusement zoomée. */
    for(var i=0;i<seeds.length;i++){
      var s=seeds[i];
      if(s.kind!=='gray'){
        var v=mk(s.x,s.y,'gray');
        v.w=s.w; v.wt=0; v.wFin=0; v.wAt=0;
        seeds[i]=v;
      }
    }
    nueeCells={};
    /* chaque Promi reprend sa place parmi les cellules vides : le nombre de
       cellules ne bouge pas, la Toile garde ses proportions */
    for(var j=0;j<list.length;j++){
      var np=window.Toile.plantOne(true);
      if(np)np.pid=list[j];
    }
    relax();tones();lastChange=performance.now();
    autoView();
    kick();
  },
  /* --- completion : on colore les cellules DEJA en place, dans un ordre fixe --- */
  paintOrder:null,
  /* la forme EXACTE de la dalle d'un Promi, ramenée dans un carré de côté `box`
     (l'Index montre ainsi la même dalle que la Toile, pas un pictogramme) */
  dalleAbs:function(pid){
    var s=null;for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;var poly=null;try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var st=null;try{st=STRUCT[state.structure];}catch(e){}
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){if(poly[j][0]<minx)minx=poly[j][0];if(poly[j][0]>maxx)maxx=poly[j][0];if(poly[j][1]<miny)miny=poly[j][1];if(poly[j][1]>maxy)maxy=poly[j][1];}
    return {poly:poly,minx:minx,miny:miny,w:maxx-minx,h:maxy-miny,round:(st&&st.round)||2,stroke:(st&&st.stroke)||'none',sw:(st&&st.sw)||1};
  },
  roundPathOf:function(pts,r){try{return roundPath(pts,r);}catch(e){return null;}},
  shapeOf:function(pid,box){
    box=box||30;
    var s=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;
    var poly=null; try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){
      if(poly[j][0]<minx)minx=poly[j][0]; if(poly[j][0]>maxx)maxx=poly[j][0];
      if(poly[j][1]<miny)miny=poly[j][1]; if(poly[j][1]>maxy)maxy=poly[j][1];
    }
    var w=maxx-minx, h=maxy-miny; if(w<=0||h<=0)return null;
    var pad=box*0.12, inner=box-pad*2;
    var k=Math.min(inner/w, inner/h);
    var ox=pad+(inner-w*k)/2, oy=pad+(inner-h*k)/2;
    var d='';
    for(var q=0;q<poly.length;q++){
      var X=(ox+(poly[q][0]-minx)*k).toFixed(1), Y=(oy+(poly[q][1]-miny)*k).toFixed(1);
      d+=(q?'L':'M')+X+' '+Y+' ';
    }
    return d+'Z';
  },
  reserved:[],
  /* L'onboarding plante de VRAIES dalles : elles s'insèrent entre les autres,
     qui s'écartent. Le même geste que dans l'app — plus aucun fondu. */
  plantOne:function(dejaPosee){
    var gris=[];
    for(var i=0;i<seeds.length;i++)if(seeds[i].kind==='gray')gris.push(seeds[i]);
    if(!gris.length)return null;
    /* le champ clair : ni sous la barre du haut, ni sous le dock. Une dalle plantée
       là serait illisible — on préfère toujours une cellule dégagée. */
    var libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-BAS_LIBRE;});
    var pool=libres.length?libres:gris;
    var cible=pool[(Math.random()*pool.length)|0];
    var a=avg();
    var jx=(Math.random()-.5)*a*0.5, jy=(Math.random()-.5)*a*0.5;
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');
    s.ci=cc(s);s.c=PAL[s.ci];
    s.t0=performance.now();      /* la dalle se REMPLIT (gris -> couleur) en prenant sa place */
    if(dejaPosee){ s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; s.t0=performance.now()-900; }
    else { s.w=-22; s.wt=12; s.wFin=3.4; s.wAt=performance.now()+380; }
    seeds.push(s);
    var k=seeds.indexOf(cible);      /* la cellule grise qui l'accueille s'efface : densite constante */
    if(k>=0)seeds.splice(k,1);
    window.Toile.paintOrder=null;
    relax();tones();lastChange=performance.now();
    autoView();      /* la vue recule d'un cran */
    kick();
    return s;
  },
  unplantOne:function(){
    for(var i=seeds.length-1;i>=0;i--){
      if(seeds[i].kind==='promi'&&seeds[i].pid==null){
        var s=seeds[i];
        var g=mk(s.x,s.y,'gray'); g.w=-9; g.wt=0;
        seeds.splice(i,1,g);
        window.Toile.paintOrder=null;
        relax();tones();lastChange=performance.now();kick();
        return true;
      }
    }
    return false;
  },
  colored:function(){var n=0;for(var i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray')n++;return n;},
  scale:function(){return view.s;},       /* le zoom courant : sert à distinguer un pincement d'un appui long */
  fingers:function(){return Object.keys(ptrs).length;},
  /* la Toile s'eclaircit sous les blocs de texte : a reappliquer des qu'elle bouge */
  applyReserve:function(){
    var R=window.Toile.reserved; if(!R||!R.length||!seeds.length)return;
    var lite=0,bl=-1;
    for(var p=0;p<PAL.length;p++){
      var c=PAL[p], L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
      if(L>bl){bl=L;lite=p;}
    }
    for(var z=0;z<R.length;z++){
      var rz=R[z];
      for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=6){
        for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=6){
          var bd=1e18,bs=null;
          for(var m=0;m<seeds.length;m++){
            var sm=seeds[m];
            var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
            if(dd<bd){bd=dd;bs=sm;}
          }
          if(bs&&bs.kind!=='gray'&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}
        }
      }
    }
  },
  /* NB : window.Toile.repaint est déjà pris par le Studio — d'où un autre nom */
  redraw:function(){lastChange=performance.now();kick();},
  /* la Toile elle-même : Partager s'en sert pour poster CE QU'ON VOIT.
     Ces deux méthodes étaient appelées par shareToile() mais n'existaient pas :
     le poster retombait sur un vieux rendu mosaïque figé, en « pixel ». */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la Toile telle qu'elle est, à l'instant : c'est elle qu'on partage */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la couleur EXACTE qu'a la dalle en ce moment sur la Toile */
  colorOf:function(pid){
    for(var i=0;i<seeds.length;i++){
      var s=seeds[i];
      if(s.pid===pid&&s.kind!=='gray'){
        var c=cOf(s,performance.now());
        return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';
      }
    }
    return null;
  },
  reserve:function(rects){window.Toile.reserved=rects||[];},
  cells:function(){if(!seeds.length)seedGray();return seeds.length;},
  paint:function(n){
    if(!seeds.length)seedGray();
    var T=window.Toile;
    if(!T.paintOrder||T.paintOrder.length!==seeds.length){
      var o=[];for(var i=0;i<seeds.length;i++)o.push(i);
      for(var j=o.length-1;j>0;j--){var r=(Math.random()*(j+1))|0;var t=o[j];o[j]=o[r];o[r]=t;}
      T.paintOrder=o;
    }
    /* la teinte la plus CLAIRE de la palette : c'est elle qui passe sous le texte */
    function _lightest(){
      var best=0,bl=-1;
      for(var p=0;p<PAL.length;p++){
        var c=PAL[p];
        var L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
        if(L>bl){bl=L;best=p;}
      }
      return best;
    }
    var ord=T.paintOrder,now=performance.now(),changed=0;
    n=Math.max(0,Math.min(ord.length,n|0));
    for(var q=0;q<ord.length;q++){
      var s=seeds[ord[q]];if(!s)continue;
      if(q<n){                                   /* doit etre coloree */
        if(s.kind==='gray'){
          s.kind='promi';s.ci=cc(s);s.c=PAL[s.ci];s.gc=null;
          s.t0=now-900;                 /* sa couleur est là tout de suite : aucun fondu */
          s.w=-9; s.wt=3.4;             /* elle arrive minuscule, puis prend sa place */
          changed++;
        }
      }else{                                     /* doit revenir au gris */
        if(s.kind==='promi'){s.kind='gray';s.gray=grays()[(Math.random()*5)|0];s.ci=null;s.t0=0;s.gc=null;s.w=0;s.wt=0;changed++;}
      }
    }
    /* la Toile RÉAGIT à l'arrivée des dalles puis se stabilise — exactement comme dans l'app */
    /* toute la Toile se réajuste, puis se stabilise — comme dans l'app */
    if(changed){relax();relax();relax();}
    /* aucune dalle bleue ne doit recouvrir les accents bleus du texte (le « i » de Promi,
       le libellé « Promi… ») : leur couleur, elle, ne s'adapte pas. On échantillonne
       vraiment la zone — le centre d'une grande dalle peut être loin tout en la couvrant. */
    /* LA TOILE FAIT DE LA PLACE AU TEXTE : toute dalle qui passe sous un bloc de
       texte prend la teinte la plus claire de la palette. L'encre sombre est alors
       lisible partout, sans jamais rien recalculer. On échantillonne vraiment la
       zone : le centre d'une grande dalle peut être loin d'elle tout en la couvrant. */
    var R=window.Toile.reserved;
    if(R&&R.length){
      var lite=_lightest();
      for(var z=0;z<R.length;z++){
        var rz=R[z];
        for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=5){
          for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=5){
            var bd2=1e18,bs=null;
            for(var m=0;m<seeds.length;m++){
              var sm=seeds[m];
              var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
              if(dd<bd2){bd2=dd;bs=sm;}
            }
            if(bs&&bs.kind!=='gray'&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}
          }
        }
      }
    }
    tones();lastChange=now;kick();
  },
  removePromi:function(){for(var i=seeds.length-1;i>=0;i--){if(seeds[i].kind==='promi'){seeds.splice(i,1);relax();tones();lastChange=performance.now();kick();break;}}},cols:function(){return curPAL();},addNuee:function(key){var s=addP('nuee');if(key){nueeCells[key]=s;s.nuee=key;}if(key)nueeCells[key]=s;},addMember:function(key){var an=(key&&nueeCells[key])?nueeCells[key]:lastNuee;if(!an){addP('promi');return;}var a=Math.random()*6.28,r=avg()*.9;var s=mk(an.x+Math.cos(a)*r,an.y+Math.sin(a)*r,'promi');s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();seeds.push(s);relax();tones();lastChange=s.t0;kick();},setTheme:function(t){if(!TH[t])return;theme=t;/* le fond des pages suit le design choisi */try{setTimeout(function(){if(window.auTrame)window.auTrame();if(window.shTrame)window.shTrame();if(window.csDalles)window.csDalles();if(window.shFond)window.shFond();if(window.ixTrame)window.ixTrame();if(window.fdRefresh)window.fdRefresh();if(window.stRefresh)window.stRefresh();if(window.dpRefresh)window.dpRefresh();if(window.esRefresh)window.esRefresh();/* les miniatures de l'Index suivent le design choisi */if(window.peintMinis)window.peintMinis(document.getElementById('indexList'));},60);}catch(e){}try{localStorage.setItem('promi_monde',t);}catch(e){}   /* le MONDE, pas le mode clair/sombre : deux choses distinctes */seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});lastChange=performance.now();kick();},getTheme:function(){return theme;},setPalette:function(k){if(PALS[k]){palKey=k;hueShift=0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();}},setHue:function(d){hueShift=+d||0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();},getPalette:function(){return palKey;},palettes:function(){return PALS;},count:function(){return seeds.filter(function(s){return s.kind!=='gray';}).length;}};
window.Toile.repaintWorld=function(pcv,w){
  var c=pcv&&pcv.__c; if(!c||!TH[w])return;
  c.th=w;
  /* les gris du monde suivent le THÈME de l'app : en mode clair ce sont les crèmes.
     On prenait la palette sombre du monde quoi qu'il arrive — d'où un Pixel sombre
     alors que le sélecteur affichait Clair. */
  var pal=isLightM()?GLIGHT:TH[w].g;
  c.seeds.forEach(function(s){s.gray=pal[(Math.random()*5)|0];s.gc=null;});
  window.Toile.repaint(pcv);
};
window.Toile.resetView=function(){view={s:1,ox:0,oy:0};vTarget=null;};
/* CHANTIER 1 — rend la VRAIE Toile hors ecran : memes germes, memes positions,
   meme monde. Contrairement a preview(), qui regenere une grille aleatoire.
   Meme patron que repaint() : on echange les globales, on peint, on restaure. */
window.Toile.renderTo=function(cv,ech,clair){
  if(!cv||!cv.getContext)return false;
  if(!seeds.length){try{seedGray();}catch(e){}}
  ech=ech||2;
  var _g=g,_W=W,_H=H,_v={s:view.s,ox:view.ox,oy:view.oy};
  var _ov=window._shThemeOverride;
  var ok=false;
  try{
    cv.width=Math.max(2,Math.round(W*ech));
    cv.height=Math.max(2,Math.round(H*ech));
    g=cv.getContext('2d'); if(!g)throw 0;
    if(clair!=null)window._shThemeOverride=!!clair;
    view={s:1,ox:0,oy:0};                 /* Toile entiere, sans cadrage */
    g.setTransform(ech,0,0,ech,0,0);
    g.clearRect(0,0,W,H);
    g.fillStyle=(clair!=null?clair:isLightM())?'#EFEADC':'#0B0C12';
    g.fillRect(0,0,W,H);
    RD[theme](performance.now(),0,0,W,H);  /* les VRAIS germes */
    /* CHANTIER 39 — le texte des dalles : frame() appelle _labels apres
       RD[theme], renderTo ne le faisait pas. Sans lui « Avec / Sans texte »
       n'avait aucun effet sur l'image partagee. */
    if(window._shLabels!==false){
      try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l){}
    }
    /* les Promi masques au partage : leur dalle revient au gris du fond.
       On repeint par-dessus plutot que de retirer le germe, ce qui
       changerait le pavage entier. */
    try{ var _hid=window.shareHidden||{};
      if(Object.keys(_hid).length){
        for(var _i=0;_i<seeds.length;_i++){
          var _s=seeds[_i];
          if(_s.pid==null||!_hid[_s.pid])continue;
          var _sv={ci:_s.ci,kind:_s.kind,gc:_s.gc};
          _s.ci=null; _s.kind='gray'; _s.gc=null;
          _s.__sv=_sv;
        }
        g.setTransform(ech,0,0,ech,0,0);
        RD[theme](performance.now(),0,0,W,H);
        for(var _j=0;_j<seeds.length;_j++){
          var _t=seeds[_j]; if(!_t.__sv)continue;
          _t.ci=_t.__sv.ci; _t.kind=_t.__sv.kind; _t.gc=_t.__sv.gc; delete _t.__sv;
        }
        if(window._shLabels!==false){
          try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l2){}
        }
      } }catch(_h){}
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;view=_v;window._shThemeOverride=_ov;
  return ok;
};
window.Toile.repaint=function(pcv){var c=pcv&&pcv.__c;if(!c)return;var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=c.pw;H=c.ph;seeds=c.seeds;theme=c.th;view={s:1,ox:0,oy:0};var dpr=pcv.width/c.pw;g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,c.pw,c.ph);g.fillStyle=isLightM()?(window._shAllColored?'#DBD0BA':'#EFEADC'):'#0B0C12';g.fillRect(0,0,c.pw,c.ph);RD[c.th](performance.now(),0,0,c.pw,c.ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;};
window.Toile.reGray=function(){seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});lastChange=performance.now();kick();};
window.Toile.reGrayStudio=function(pcv){var c=pcv&&pcv.__c;if(!c)return;c.seeds.forEach(function(s){s.gray=grays()[(Math.random()*5)|0];s.gc=null;});window.Toile.repaint(pcv);};
window.Toile.curWorld=function(){return theme;};
window.Toile.dalleCapture=function(dcv,pid,ech){
  try{
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) return false;
    var cv=document.getElementById('toileCv'); if(!cv) return false;
    var tgt=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){tgt=seeds[i];break;}}
    if(!tgt) return false;
    /* marge : encre, terrazzo et touffe debordent de leur cellule */
    var LIBRE=(theme==='encre'||theme==='terrazzo'||theme==='touffe');
    var sp=Math.sqrt(W*H/Math.max(1,seeds.length));
    var mar=LIBRE?sp*0.85:sp*0.10;
    var lx0=D.minx-mar, ly0=D.miny-mar, lw=D.w+2*mar, lh=D.h+2*mar;
    var sx=(lx0*view.s+view.ox)*DPR, sy=(ly0*view.s+view.oy)*DPR;
    var sw=lw*view.s*DPR, sh=lh*view.s*DPR;
    /* si la marge sort du cadre, on rogne au bord plutot que de renoncer */
    var rx0=Math.max(0,sx), ry0=Math.max(0,sy);
    var rx1=Math.min(cv.width,sx+sw), ry1=Math.min(cv.height,sy+sh);
    if(rx1-rx0<8||ry1-ry0<8) return false;
    lx0=lx0+(rx0-sx)/(view.s*DPR); ly0=ly0+(ry0-sy)/(view.s*DPR);
    lw=(rx1-rx0)/(view.s*DPR); lh=(ry1-ry0)/(view.s*DPR);
    sx=rx0; sy=ry0; sw=rx1-rx0; sh=ry1-ry0;
    ech=ech||1;
    var dw=Math.max(1,Math.round(sw*ech)), dh=Math.max(1,Math.round(sh*ech));
    dcv.width=dw; dcv.height=dh;
    var gg=dcv.getContext('2d'); if(!gg) return false;
    gg.setTransform(1,0,0,1,0,0); gg.clearRect(0,0,dw,dh);
    gg.imageSmoothingQuality='high';
    gg.drawImage(cv, sx, sy, sw, sh, 0, 0, dw, dh);
    /* on ne garde que les pixels de CETTE dalle, avec la regle exacte du moteur */
    var im=gg.getImageData(0,0,dw,dh), d2=im.data, ns=seeds.length;
    for(var yy=0;yy<dh;yy++){
      var ly=ly0+(yy+0.5)*lh/dh;
      for(var xx=0;xx<dw;xx++){
        var lx=lx0+(xx+0.5)*lw/dw, bd=1e18, bs=null;
        for(var q=0;q<ns;q++){var s2=seeds[q];
          var ex=lx-s2.x, ey=ly-s2.y;
          var dq=Math.sqrt(ex*ex+ey*ey)-(s2.w||0);
          if(dq<bd){bd=dq;bs=s2;}}
        var o4=(yy*dw+xx)*4;
        if(bs!==tgt){ d2[o4+3]=0; }
        else {
          /* le fond de la Toile devient transparent, la matiere reste pleine */
          var r=d2[o4],g2=d2[o4+1],b2=d2[o4+2];
          var mx=Math.max(r,g2,b2), mn=Math.min(r,g2,b2);
          if((mx-mn)<26 && mx>150) d2[o4+3]=0;
        }
      }
    }
    gg.putImageData(im,0,0);
    /* recadrage au plus juste */
    var x0=dw,y0=dh,x1=-1,y1=-1;
    for(var y3=0;y3<dh;y3++)for(var x3=0;x3<dw;x3++){
      if(d2[(y3*dw+x3)*4+3]>8){if(x3<x0)x0=x3;if(x3>x1)x1=x3;if(y3<y0)y0=y3;if(y3>y1)y1=y3;}}
    if(x1>x0&&y1>y0){
      var tw=x1-x0+1, th=y1-y0+1;
      var tp=document.createElement('canvas'); tp.width=tw; tp.height=th;
      tp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
      dcv.width=tw; dcv.height=th;
      var g3=dcv.getContext('2d'); g3.setTransform(1,0,0,1,0,0); g3.drawImage(tp,0,0);
    }
    return true;
  }catch(e){ return false; }
};
window.Toile.vue=function(){return {s:view.s,ox:view.ox,oy:view.oy,dpr:DPR};};

/* ════════════════════════════════════════════════════════════════════════════
   ⚑ dalleGeneree — LE MOTEUR DESSINE UNE DALLE DANS LA CELLULE QU'ON LUI DONNE
   Ajout du 9 septembre 2026. ⚠ N'EXISTE QUE DANS CETTE COPIE (scratchpad) :
   `app.html` n'est pas touche, et rien de ce qui existait ici n'est modifie —
   c'est un ajout, pas une reecriture.

   ⚑ POURQUOI IL FALLAIT CA, ET RIEN D'AUTRE.
   Tout ce qu'on avait jusqu'ici PRELEVAIT dans une Toile deja peinte :
     · `dalleTrame` peint puis efface l'alpha hors cellule, PIXEL PAR PIXEL —
       elle coupe donc les marques en deux (demi-pois, demi-carreaux, et
       l'escalier de `pixel` remplace par un polygone lisse) ;
     · l'extraction par la couleur rendait des marques entieres, mais restait
       un decoupage dans une image de Toile — « des photos de la Toile
       detourees encadrees », et Tom a raison de ne pas en vouloir.
   Ici, RIEN N'EST PRELEVE. On demande au moteur de PEINDRE une dalle dans une
   cellule donnee, et il la peint avec son propre code : `RD[monde]`, au pas
   absolu, echelle 1, avec sa trame, ses teintes et ses strates.

   ⚑ LA CLE : ON FABRIQUE LA CELLULE AVEC DES GRAINES, PAS AVEC UN DECOUPAGE.
   La cellule d'une graine est l'intersection des demi-plans de ses
   bissectrices. Donc, pour qu'une graine ait EXACTEMENT le polygone voulu, il
   suffit de poser une voisine en MIROIR de chaque cote : la bissectrice entre
   les deux EST ce cote. Le moteur decide alors lui-meme, avec sa propre regle,
   quelle marque appartient a qui — et une marque reste ENTIERE, exactement
   comme sur la Toile.
   ⚠ Vrai pour un polygone CONVEXE contenant sa graine : c'est le cas de toute
   cellule de Voronoi.

   Les voisines sont posees en `gray` : elles peignent le fond sombre de la
   Toile. La dalle, elle, porte une couleur de palette — jamais confondable.

   opt = {monde, palette, hue, poly:[[x,y]...], site:[x,y], ci, lit, tone, ang, shade}
   ════════════════════════════════════════════════════════════════════════════ */
window.Toile.dalleGeneree=function(dcv,opt){
  opt=opt||{};
  var _g=g,_W=W,_H=H,_s=seeds,_v={s:view.s,ox:view.ox,oy:view.oy};
  var _th=theme,_pk=palKey,_hs=hueShift,_pl=_palLit,ok=false;
  try{
    if(opt.monde&&RD[opt.monde])theme=opt.monde;
    if(opt.palette&&PALS[opt.palette])palKey=opt.palette;
    if(opt.hue!=null)hueShift=+opt.hue||0;
    _palLit=null;
    var P=opt.poly; if(!P||P.length<3) throw 0;
    var i, x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    for(i=0;i<P.length;i++){
      if(P[i][0]<x0)x0=P[i][0]; if(P[i][0]>x1)x1=P[i][0];
      if(P[i][1]<y0)y0=P[i][1]; if(P[i][1]>y1)y1=P[i][1]; }
    var pad=opt.pad!=null?opt.pad:26;
    /* ⚑ LA PHASE — SANS ELLE, CHAQUE CELLULE REDEMARRE SA GRILLE A ZERO.
       Les trames sont ancrees sur des coordonnees ABSOLUES : pois tous les 9,
       tesselles tous les 11, carres tous les 5, sillons tous les 6. Sur la
       Toile il n'y a donc QU'UNE grille pour tout le canevas, et une frontiere
       de dalle n'est qu'un CHANGEMENT DE COULEUR dessus.
       En peignant chaque cellule dans son propre canevas, la grille repartait
       de l'origine de ce canevas : les carreaux ne tombaient plus en face d'une
       cellule a l'autre, et le raccord se voyait. On decale donc l'origine
       d'un multiple de la periode — l'idiome que `dalleTrame` porte deja. */
    var PER={braille:9,mosaique:11,pixel:5,sillons:6}[theme]||0;
    var padX0=0, padY0=0;
    if(PER && opt.phase){
      padX0=((opt.phase[0]%PER)+PER)%PER;
      padY0=((opt.phase[1]%PER)+PER)%PER;
    }
    var pad=pad;
    var dw=Math.ceil(x1-x0+2*pad+padX0), dh=Math.ceil(y1-y0+2*pad+padY0);
    if(dw<8||dh<8) throw 0;
    var sx=opt.site?opt.site[0]:null, sy=opt.site?opt.site[1]:null;
    if(sx==null){ sx=0; sy=0; for(i=0;i<P.length;i++){sx+=P[i][0];sy+=P[i][1];} sx/=P.length; sy/=P.length; }

    /* on translate tout dans le repere du canevas */
    var Q=[]; for(i=0;i<P.length;i++) Q.push([P[i][0]-x0+pad+padX0, P[i][1]-y0+pad+padY0]);
    var qx=sx-x0+pad+padX0, qy=sy-y0+pad+padY0;

    /* LA GRAINE DE LA DALLE */
    var t=mk(qx,qy,'promi');
    t.ci=(opt.ci!=null?opt.ci:0)%PALL().length;
    t.c=curPAL()[t.ci];
    t.lit=(opt.lit!=null?opt.lit:0)%LITS.length;
    if(opt.tone!=null)t.tone=opt.tone;
    if(opt.ang!=null)t.ang=opt.ang;
    if(opt.shade!=null)t.shade=opt.shade;
    t.t0=-99999;                       /* la couleur est deja a son terme */
    t.w=0; t.px=null; t.py=null;
    var SS=[t];

    /* LES VOISINES, EN MIROIR DE CHAQUE COTE : la bissectrice EST le cote */
    var cx=0, cy=0;
    for(i=0;i<Q.length;i++){cx+=Q[i][0];cy+=Q[i][1];}
    cx/=Q.length; cy/=Q.length;
    for(i=0;i<Q.length;i++){
      var a=Q[i], b=Q[(i+1)%Q.length];
      var ex=b[0]-a[0], ey=b[1]-a[1], L=Math.sqrt(ex*ex+ey*ey);
      if(L<1e-6) continue;
      var nx=ey/L, ny=-ex/L;
      if((cx-a[0])*nx+(cy-a[1])*ny>0){nx=-nx;ny=-ny;}      /* vers l'exterieur */
      var h=(qx-a[0])*nx+(qy-a[1])*ny;                      /* < 0 : la graine est dedans */
      var vv=mk(qx-2*h*nx, qy-2*h*ny, 'gray');
      vv.w=0; vv.px=null; vv.py=null;
      SS.push(vv);
    }
    /* de quoi peupler le pourtour, pour que le fond ne soit pas nu */
    var R2=Math.max(dw,dh);
    for(i=0;i<10;i++){
      var an=i/10*6.2832, vv2=mk(qx+Math.cos(an)*R2*1.35, qy+Math.sin(an)*R2*1.35,'gray');
      vv2.w=0; vv2.px=null; vv2.py=null; SS.push(vv2);
    }

    /* ⚑ L'ESPACEMENT DE LA TOILE, POUR LES MONDES LIBRES.
       `Renc`, `Rterr` et `Rtouf` dimensionnent leur marque sur
       sp = racine(W x H / nombre de graines) : un lobe d'encre fait 0,6 sp, une
       fleur de touffe 0,13 a 0,33 sp, un tesson 0,11 a 0,30 sp. Dans un canevas
       de dalle, W x H et le nombre de graines n'ont rien a voir avec ceux de la
       Toile — les marques sortaient donc BEAUCOUP trop petites.
       Mesure, part de matiere dans la MEME cellule, Toile / genere :
          encre 51,1 -> 19,2   touffe 14,7 -> 1,9   terrazzo 22,9 -> 9,5
       alors que les cinq trames tombaient deja a +-4 points.
       On truque donc W et H pour que sp retrouve sa valeur — c'est l'idiome que
       `dalleTrame` porte deja pour ses mondes LIBRE. ⚠ Uniquement pour eux :
       `Rpix` et `Rmos` BOUCLENT sur W et H, les truquer les casserait. */
    var LIBRE=(theme==='encre'||theme==='terrazzo'||theme==='touffe');
    var spRe=opt.sp||Math.sqrt(Math.max(1,_W*_H)/Math.max(1,_s.length));
    /* ⚑ LA GRAINE CIBLE VA AU MILIEU DE LA LISTE, PAS EN TETE.
       `Renc`, `Rterr` et `Rtouf` peignent graine par graine, dans l'ordre du
       tableau : la derniere posee recouvre les autres. En laissant la cible en
       tete, TOUTES ses voisines passaient par-dessus elle — la difference des
       deux rendus ne trouvait presque plus rien, et les trois mondes libres
       sortaient troues (46 000 touffes peintes contre 146 000 pour une trame).
       Sur la Toile, une graine est au milieu de la liste : la moitie de ses
       voisines est derriere elle. On la remet a sa place. */
    var mid=SS.length>>1;
    SS.splice(0,1); SS.splice(mid,0,t);
    seeds=SS; view={s:1,ox:0,oy:0};
    if(LIBRE){ W=spRe*Math.sqrt(SS.length); H=W; }
    else     { W=dw; H=dh; }
    dcv.width=Math.round(dw*DPR); dcv.height=Math.round(dh*DPR);
    g=dcv.getContext('2d'); if(!g) throw 0;
    g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
    var NOW=performance.now();
    g.save(); RD[theme](NOW,0,0,dw,dh); g.restore();

    /* ⚑ LA DALLE SE SEPARE DE SON FOND PAR DIFFERENCE DE DEUX RENDUS.
       C'est le dernier prelevement a supprimer. Garder « les pixels de la
       couleur de la dalle » marchait pour les trames, mais restait un tri dans
       une image — et il RATE une fleur de `touffe`, qui porte trois couleurs :
       le petale a la teinte de la dalle, le lisere est a l'encre, le coeur est
       orange. Mesure : la fleur ressortait sans contour et sans coeur.
       Ici on peint DEUX FOIS le meme jeu de graines, au meme instant, et on ne
       change QU'UNE chose : la graine cible redevient grise. Tout ce qui
       differe entre les deux images appartient donc a cette dalle — son
       lisere et son coeur compris. Rien n'est devine, rien n'est detoure.
       ⚠ Il faut le MEME jeu de graines : `mk()` tire au sort (gray, tone,
       shade, ang, ph). Deux constructions donneraient deux fonds differents et
       la difference serait du bruit. Et le MEME instant : `cOf` depend de now. */
    var im1=g.getImageData(0,0,dcv.width,dcv.height);
    var wasKind=t.kind, wasCi=t.ci, wasC=t.c, wasT0=t.t0;
    t.kind='gray'; t.ci=null; t.c=null; t.gc=null; t.t0=0;
    g.clearRect(0,0,dw,dh);
    g.save(); RD[theme](NOW,0,0,dw,dh); g.restore();
    var im2=g.getImageData(0,0,dcv.width,dcv.height);
    t.kind=wasKind; t.ci=wasCi; t.c=wasC; t.t0=wasT0; t.gc=null;

    var A=im1.data, B2=im2.data, np=A.length;
    for(var q=0;q<np;q+=4){
      var d1=Math.abs(A[q]-B2[q]), d2=Math.abs(A[q+1]-B2[q+1]), d3=Math.abs(A[q+2]-B2[q+2]);
      var d4=Math.abs(A[q+3]-B2[q+3]);
      var dm=Math.max(d1,d2,d3,d4);
      var al=(dm-5)/38; if(al<0)al=0; if(al>1)al=1;
      A[q+3]=Math.round(A[q+3]*al);
    }
    g.clearRect(0,0,dw,dh);
    g.setTransform(1,0,0,1,0,0); g.putImageData(im1,0,0);
    g.setTransform(DPR,0,0,DPR,0,0);

    /* la couleur du corps de la dalle, connue a priori — jamais echantillonnee */
    dcv.__col=PALL()[t.ci][t.lit].slice(0,3);
    dcv.__site=[qx,qy]; dcv.__poly=Q; dcv.__box=[x0-pad,y0-pad,dw,dh];
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;seeds=_s;view=_v;
  theme=_th;palKey=_pk;hueShift=_hs;_palLit=_pl;
  return ok;
};
window.Toile.dalleTrame=function(dcv,pid,k,monde){
  /* Peint la matiere du design actif pour LA dalle du Promi demande,
     decoupee sur sa vraie cellule. Meme mecanique que Toile.repaint.

     LE MONDE D'ALORS -- 4 septembre 2026, decision Tom.
     `monde` est FACULTATIF : {m:design, p:palette, h:teinte}. Absent, la fonction se
     comporte EXACTEMENT comme avant -- les six appels existants ne bougent pas.
     Present, elle peint la dalle dans le monde de SA PLANTATION et non dans le monde
     courant : une dalle est figee au jour ou on l'a plantee, et changer de monde au
     Studio ne repeint pas les anciennes.
     On sauve et on restaure sur l'idiome que la fonction porte deja pour g/W/H/seeds/view.
     ATTENTION _palLit est un MEMO de la palette calculee : il doit etre invalide a
     l'aller (sinon la palette de l'appelant fuit dans la dalle) et restaure au retour
     (sinon celle de la dalle fuit dans la Toile). */
  var _g=g,_W=W,_H=H,_s=seeds,_v={s:view.s,ox:view.ox,oy:view.oy},ok=false;
  var _th=theme,_pk=palKey,_hs=hueShift,_pl=_palLit;
  try{
    if(monde){
      if(monde.m&&RD[monde.m])theme=monde.m;
      if(monde.p&&PALS[monde.p])palKey=monde.p;
      if(monde.h!=null)hueShift=+monde.h||0;
      _palLit=null;
    }
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) throw 0;
    k=k||1;
    /* Sur la Toile, encre / terrazzo / touffe DEBORDENT de leur cellule :
       les decouper dessus les tronquait. On leur laisse une marge et aucun
       decoupage ; les mondes a trame restent contenus dans leur cellule. */
    var LIBRE=(theme==='encre'||theme==='terrazzo'||theme==='touffe');
    var spReal=Math.sqrt(_W*_H/Math.max(1,_s.length))*k;
    var pad=Math.round(spReal*(LIBRE?0.85:0.30));   /* marge : la vraie cellule ponderee peut deborder du polygone */
    /* Les motifs a trame sont ancres sur les coordonnees absolues de la Toile
       (points tous les 9, tesselles tous les 11, carres tous les 5, sillons tous les 6).
       En deplacant la cellule il faut donc translater d'un multiple de la periode,
       sinon le motif ne retombe pas au meme endroit que sur la Toile. */
    var PER={braille:9,mosaique:11,pixel:5,sillons:6}[theme]||0;
    var padX=pad, padY=pad;
    if(PER&&k===1){
      /* alignement EXACT, fractions comprises : un arrondi suffit a decaler un motif a gros pas */
      padX=pad+((D.minx-pad)%PER+PER)%PER;
      padY=pad+((D.miny-pad)%PER+PER)%PER;
    }
    var dw=Math.ceil(D.w*k+2*padX), dh=Math.ceil(D.h*k+2*padY);
    dcv.width=Math.round(dw*DPR); dcv.height=Math.round(dh*DPR);
    seeds=_s.map(function(s){var o={};for(var q in s)o[q]=s[q];
      o.x=(s.x-D.minx)*k+padX; o.y=(s.y-D.miny)*k+padY;
      o.px=(s.px!=null)?((s.px-D.minx)*k+padX):null;
      o.py=(s.py!=null)?((s.py-D.miny)*k+padY):null;
      o.w=(s.w||0)*k; return o;});
    W=dw; H=dh; view={s:1,ox:0,oy:0};
    if(LIBRE){
      var ti=-1;
      for(var z=0;z<seeds.length;z++){if(seeds[z].pid===pid&&seeds[z].kind!=='gray'){ti=z;break;}}
      if(ti>=0){
        for(var z2=0;z2<seeds.length;z2++){ if(z2===ti) continue;
          seeds[z2].x=-1e7; seeds[z2].y=-1e7; seeds[z2].px=null; seeds[z2].py=null; }
        /* sp doit valoir celui de la Toile : sp = racine(W*H / nombre de graines) */
        var nn=Math.max(1,seeds.length);
        W=spReal*Math.sqrt(nn); H=W;
      }
    }
    g=dcv.getContext('2d'); if(!g) throw 0;
    g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
    g.save();
    RD[theme](performance.now(),0,0,dw,dh);
    g.restore();
    if(!LIBRE){
      /* Le moteur attribue chaque pixel a la graine la plus proche AU SENS PONDERE
         (distance moins poids). Le polygone de _cellPoly n'en est qu'une approximation :
         des que les poids different, la vraie frontiere est courbe. On refait donc
         l'attribution pixel par pixel, avec la regle exacte du moteur. */
      var tg2=null;
      for(var z2=0;z2<seeds.length;z2++){if(seeds[z2].pid===pid&&seeds[z2].kind!=='gray'){tg2=seeds[z2];break;}}
      if(tg2){
        var img2=g.getImageData(0,0,dcv.width,dcv.height), dd=img2.data;
        var iw=dcv.width, ih=dcv.height, sx2=dw/iw, sy2=dh/ih, ns=seeds.length;
        for(var yy=0;yy<ih;yy++){
          var ly=(yy+0.5)*sy2;
          for(var xx=0;xx<iw;xx++){
            var o4=(yy*iw+xx)*4;
            if(dd[o4+3]===0) continue;
            var lx=(xx+0.5)*sx2, bd2=1e18, bs2=null;
            for(var q2=0;q2<ns;q2++){var sq=seeds[q2];
              var ex=lx-sq.x, ey=ly-sq.y;
              var dq=Math.sqrt(ex*ex+ey*ey)-(sq.w||0);
              if(dq<bd2){bd2=dq;bs2=sq;}}
            if(bs2!==tg2) dd[o4+3]=0;
          }
        }
        g.putImageData(img2,0,0);
      }
    }
    /* on recadre au plus juste sur la matiere : plus aucune marge morte */
    try{
      var im=g.getImageData(0,0,dcv.width,dcv.height).data;
      var x0=dcv.width,y0=dcv.height,x1=-1,y1=-1;
      for(var yy=0;yy<dcv.height;yy++)for(var xx=0;xx<dcv.width;xx++){
        if(im[(yy*dcv.width+xx)*4+3]>8){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(yy<y0)y0=yy;if(yy>y1)y1=yy;}}
      if(x1>x0&&y1>y0){
        var tw=x1-x0+1, th=y1-y0+1;
        var tmp=document.createElement('canvas'); tmp.width=tw; tmp.height=th;
        tmp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
        dcv.width=tw; dcv.height=th;
        var g2=dcv.getContext('2d'); g2.setTransform(1,0,0,1,0,0); g2.clearRect(0,0,tw,th);
        g2.drawImage(tmp,0,0);
      }
    }catch(e){}
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;seeds=_s;view=_v;
  theme=_th;palKey=_pk;hueShift=_hs;_palLit=_pl;
  return ok;
};
/* le monde courant, en LECTURE SEULE : ce qu'on fige sur un Promi a sa plantation */
window.Toile.mondeCourant=function(){return {m:theme,p:palKey,h:hueShift};};
window.Toile.preview=function(pcv,th,pw,ph){if(!TH[th])th='pixel';var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};var dpr=pcv.width/pw;seeds=[];var base=Math.max(20,pw/5.5),gc=Math.max(2,Math.round(pw/base)),gr=Math.max(2,Math.round(ph/base)),cw=pw/gc,ch=ph/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++)seeds.push(mk(cw*(c+.5)+(Math.random()-.5)*cw*.42,ch*(r+.5)+(Math.random()-.5)*ch*.42));var cx=pw*(0.28+Math.random()*0.44),cy=ph*(0.34+Math.random()*0.26);var cen=seeds.filter(function(s){return s.y>ph*0.2&&s.y<ph*0.72&&s.x>pw*0.06&&s.x<pw*0.94;});cen.forEach(function(s){s._sc=((s.x-cx)*(s.x-cx)+(s.y-cy)*(s.y-cy))*(0.35+Math.random()*1.6);});cen.sort(function(a,b){return a._sc-b._sc;});var nc=11+(Math.random()*2|0);   /* 5 dalles colorées de plus dans le Studio */for(var i=0;i<nc&&i<cen.length;i++){var s=cen[i];s.ci=cc(s);s.c=PAL[s.ci];s.kind='promi';s.t0=-99999;}var far=cen.slice(Math.floor(cen.length*0.55));var det=1+(Math.random()*2|0);for(var f=0;f<det&&far.length;f++){var ss2=far[(Math.random()*far.length)|0];if(ss2&&ss2.ci==null){ss2.ci=cc(ss2);ss2.c=PAL[ss2.ci];ss2.kind='promi';ss2.t0=-99999;}}if(window._shAllColored){for(var _ac=0;_ac<seeds.length;_ac++){var _sac=seeds[_ac];if(_sac.ci==null){_sac.ci=cc(_sac);_sac.c=PAL[_sac.ci];_sac.kind='promi';_sac.t0=-99999;}}}tones();try{pcv.__c={seeds:seeds.map(function(s){return {x:s.x,y:s.y,gray:s.gray,gc:null,ci:s.ci,c:s.c,kind:s.kind,tone:s.tone,lit:s.lit,shade:s.shade,ang:s.ang,w:s.w,t0:-99999};}),th:th,pw:pw,ph:ph};}catch(e){}g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,pw,ph);g.fillStyle=isLightM()?(window._shAllColored?'#DBD0BA':'#EFEADC'):'#0B0C12';g.fillRect(0,0,pw,ph);RD[th](performance.now(),0,0,pw,ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;};

var ptrs={},pinch=null;function cp(){var mx=0,my=0;var lx=Math.min(0,W-W*view.s),hx=Math.max(0,W-W*view.s);view.ox=Math.max(lx-mx,Math.min(hx+mx,view.ox));var ly=Math.min(0,H-H*view.s),hy=Math.max(0,H-H*view.s);view.oy=Math.max(ly-my,Math.min(hy+my,view.oy));}
host.style.touchAction='none';
host.addEventListener('pointerdown',function(e){e.stopPropagation();host.setPointerCapture(e.pointerId);vTarget=null;   /* le doigt reprend la main : le cadrage automatique lâche prise */
  ptrs[e.pointerId]={x:e.clientX,y:e.clientY};var k=Object.keys(ptrs);if(k.length===2){var a=ptrs[k[0]],b=ptrs[k[1]];pinch={d:Math.hypot(a.x-b.x,a.y-b.y),s:view.s,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,ox:view.ox,oy:view.oy};}});
host.addEventListener('pointermove',function(e){if(!ptrs[e.pointerId])return;e.stopPropagation();var pr=ptrs[e.pointerId];ptrs[e.pointerId]={x:e.clientX,y:e.clientY};var k=Object.keys(ptrs);if(k.length===2&&pinch){var a=ptrs[k[0]],b=ptrs[k[1]];var d=Math.hypot(a.x-b.x,a.y-b.y);var ns=Math.max(0.4,Math.min(5,pinch.s*d/pinch.d));var cx=(a.x+b.x)/2,cy=(a.y+b.y)/2;view.ox=cx-(pinch.cx-pinch.ox)*(ns/pinch.s);view.oy=cy-(pinch.cy-pinch.oy)*(ns/pinch.s);view.s=ns;cp();kick();}else if(k.length===1){view.ox+=e.clientX-pr.x;view.oy+=e.clientY-pr.y;cp();kick();}});
function pu(e){e.stopPropagation();delete ptrs[e.pointerId];if(Object.keys(ptrs).length<2)pinch=null;}host.addEventListener('pointerup',pu);host.addEventListener('pointercancel',pu);
window.addEventListener('resize',size);
setTimeout(size,60);
})();
