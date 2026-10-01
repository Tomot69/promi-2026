# L'ÉCRAN QUI VEND — TOILE DE DÉMONSTRATION, ENGENDRÉE (Tom, 12 sept., cinquième arbitrage).
import hashlib, io
F='scratchpad/app-vend-toile4.html'; S=io.open(F,encoding='utf-8').read()
avant=hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant=='3ac4975ccaed06419950963a8804a212', 'copie inattendue : '+avant
def r(old,new,quoi):
    global S
    assert S.count(old)==1, 'motif absent ou multiple (%s) : %r'%(quoi,old[:80])
    S=S.replace(old,new); print('  ✔',quoi)
r("Tout Promi pour <b>3,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>29&nbsp;€</b> · soit 2,42&nbsp;€/mois · −39&nbsp;%.",
  "Tout Promi pour <b>5,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>39&nbsp;€</b> · soit 3,25&nbsp;€/mois.", 'prix · .pl-sub')
r('<button class="pl-buy prim" id="buyMonth">Essayer 14 jours, puis 3,99&nbsp;€/mois</button>',
  '<button class="pl-buy prim" id="buyMonth">Essayer 14 jours</button>', 'prix · #buyMonth')
r('<button class="pl-buy sec" id="buyYear">Prendre l\'année</button>',
  '<button class="pl-buy sec" id="buyYear">ou prendre l\'année — 39&nbsp;€</button>', 'prix · #buyYear')
r("px.textContent = '29\\u00a0€'", "px.textContent = '39\\u00a0€'", 'prix · ancien lot')
r("so.textContent = 'soit 2,42\\u00a0€/mois · −39\\u00a0%'", "so.textContent = 'soit 3,25\\u00a0€/mois'", 'prix · ancien lot')
r("var G = { AUTO:6.283185307/120,", "var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept.). */", 'G.AUTO : 100 s')

BLOC = r"""
<style id="lot-CERCLE-TOILE-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — UNE TOILE DE DÉMONSTRATION, ENGENDRÉE (Tom, 12 sept. 2026) :
   « ce n'est plus la Toile de l'utilisateur, c'est une Toile de démonstration. Générée, dense, riche — ce qu'une
   Toile peut devenir, pas ce qu'il a. » Elle règle le cas de celui qui n'a rien planté.
   ⚑ LES FORMES VIENNENT DU MOTEUR (§4 règle 1, §9) : je ne pose que des GERMES — des positions — et c'est
   `Toile.repaint` qui peint. Les germes d'une Toile engendrée ont tous un poids NUL (mesuré) : le pavage est donc
   un Voronoï simple, et l'attribution d'un pixel à sa cellule se refait avec la règle exacte du moteur.
   ⚑ HUIT MATIÈRES DANS UN MÊME PAVAGE : les mêmes germes sont rendus dans les huit mondes (huit images alignées
   au pixel), puis composés cellule par cellule. C'est la seule façon sans toucher au code de la Toile.
   ⚑ LES COULEURS VIENNENT DU STUDIO (`Toile.cols()`), jamais du design : la Toile parle la couleur de
   l'utilisateur, même si sa matière est inventée.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#plusScreen>#plHeroCv,#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat,#plusScreen>.pl-plans,
#plusScreen>.pl-note,#plusScreen>.pl-eb,#plusScreen #plCadre{display:none!important}
#plusScreen::before,.frame #plusScreen::before{display:none!important;content:none!important}
#plusScreen>.enh{background:none!important;background-color:transparent!important;border:0!important;
  box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
#plusScreen>.enh>.pl-eb{visibility:hidden!important}
#plusScreen>.closeb{z-index:6!important}
#plusScreen #pcCadre{position:absolute!important;width:390px!important;height:844px!important;margin:0!important;
  pointer-events:none;z-index:3;background:transparent!important}
#plusScreen #pcCadre>*{position:absolute!important;margin:0!important;box-sizing:border-box!important}
#plusScreen #pcCadre{--pc-ink:#1A1613;--pc-sub:#8A7E70;--pc-filet:#E0CFB6;--pc-sec:#EADFCE;--pc-sec2:#DCCBB2;--pc-secl:#CDB894}
.frame:not(.light) #plusScreen #pcCadre,#device:not(.light) #plusScreen #pcCadre{
  --pc-ink:#F4EEE1;--pc-sub:#A79C8E;--pc-filet:#2E2740;--pc-sec:#221E30;--pc-sec2:#2E2740;--pc-secl:#3C3352}
#plusScreen #pcCadre .pc-toile{left:22px!important;top:98px!important;width:346px!important;height:206px!important;
  border-radius:28px!important;overflow:hidden!important;background:var(--pc-filet)!important;
  box-shadow:0 0 0 2px var(--pc-filet)!important}
#plusScreen #pcCadre .pc-toile canvas{position:absolute;left:0;top:0;width:346px;height:206px;display:block}
#plusScreen #pcCadre .pc-h{left:49.5px!important;top:336px!important;width:291px!important;
  font-family:Fraunces,Georgia,serif;font-weight:600;font-size:32px;line-height:38px;color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-sub{left:49.5px!important;top:382px!important;width:291px!important;
  font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:15px;line-height:22px;color:var(--pc-sub);
  -webkit-text-fill-color:var(--pc-sub);white-space:nowrap}
#plusScreen #pcCadre .pc-arg{left:49.5px!important;width:291px!important}
#plusScreen #pcCadre .pc-arg b{display:block;font-family:Bricolage,system-ui,sans-serif;font-weight:600;font-size:17px;
  line-height:22px;letter-spacing:-.01em;color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-arg i{display:block;font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;
  font-size:13px;line-height:18px;color:var(--pc-sub);-webkit-text-fill-color:var(--pc-sub)}
#plusScreen #pcCadre .pc-prix{left:49.5px!important;top:612px!important;width:291px!important;
  display:flex!important;align-items:baseline!important;justify-content:space-between!important}
#plusScreen #pcCadre .pc-prix b{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:40px;line-height:40px;
  color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-prix i{font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:13px;
  color:var(--pc-sub);-webkit-text-fill-color:var(--pc-sub)}
/* ⚑ LE BOUTON — l'appel à l'action. Deux gestes, minuscules : il SE POSE à l'ouverture (il descend de 6 px et son
   ombre dure apparaît), puis un ÉCLAT le traverse toutes les 5,2 s en 620 ms. Le reste de l'écran ne bouge pas. */
#plusScreen #pcCadre #buyMonth{left:22px!important;top:680px!important;width:346px!important;max-width:346px!important;
  height:58px!important;min-height:58px!important;border-radius:29px!important;border:0!important;
  display:flex!important;align-items:center!important;justify-content:center!important;gap:10px!important;
  background:#FA2258!important;color:#FFF4F6!important;-webkit-text-fill-color:#FFF4F6!important;
  font-family:Bricolage,system-ui,sans-serif!important;font-weight:700!important;font-size:17px!important;
  letter-spacing:-.01em!important;box-shadow:0 4px 0 0 #A50E36!important;pointer-events:auto!important;
  position:absolute!important;overflow:hidden!important;transition:box-shadow .11s linear,transform .11s linear}
#plusScreen #pcCadre #buyMonth.pc-pose{animation:pcPose .52s cubic-bezier(.32,.72,0,1) both}
@keyframes pcPose{from{transform:translateY(-6px);box-shadow:0 0 0 0 #A50E36}to{transform:none;box-shadow:0 4px 0 0 #A50E36}}
#plusScreen #pcCadre #buyMonth:active{box-shadow:0 0 0 0 #A50E36!important;transform:translateY(4px)}
#plusScreen #pcCadre #buyMonth .pc-eclat{position:absolute;top:0;left:-45%;width:30%;height:100%;z-index:1;pointer-events:none;
  background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.30) 50%,rgba(255,255,255,0));
  transform:skewX(-14deg);animation:pcEclat 5.2s linear infinite}
@keyframes pcEclat{0%{left:-45%}12%{left:125%}100%{left:125%}}
@media (prefers-reduced-motion:reduce){#plusScreen #pcCadre #buyMonth .pc-eclat{animation:none;opacity:0}
  #plusScreen #pcCadre #buyMonth.pc-pose{animation:none}}
#plusScreen #pcCadre #buyMonth .pc-sig{position:absolute;left:0;top:0;width:346px;height:58px;opacity:0;pointer-events:none;z-index:0}
#plusScreen #pcCadre #buyMonth .pc-lb,#plusScreen #pcCadre #buyMonth .pc-go{position:relative;z-index:2}
#plusScreen #pcCadre #buyMonth .pc-go{font-size:20px;font-weight:500;opacity:.9;transform:translateY(-1px)}
#plusScreen #pcCadre #buyYear{left:22px!important;top:756px!important;width:346px!important;max-width:346px!important;
  height:44px!important;min-height:0!important;border:1px solid var(--pc-secl)!important;border-radius:22px!important;
  background:var(--pc-sec)!important;display:flex!important;align-items:center!important;justify-content:center!important;
  box-shadow:none!important;font-family:Bricolage,system-ui,sans-serif!important;font-weight:600!important;font-size:15px!important;
  letter-spacing:-.01em!important;color:var(--pc-ink)!important;-webkit-text-fill-color:var(--pc-ink)!important;
  text-decoration:none!important;pointer-events:auto!important;position:absolute!important;overflow:hidden!important}
#plusScreen #pcCadre #buyYear::before{content:'';position:absolute;left:-30%;top:-140%;width:160%;height:380%;
  background:linear-gradient(118deg,var(--pc-sec2) 0%,var(--pc-sec) 46%,var(--pc-sec2) 100%);
  transform:rotate(-12deg);z-index:0;pointer-events:none}
#plusScreen #pcCadre #buyYear>*{position:relative;z-index:1}
#plusScreen #pcCadre .pc-legal{left:22px!important;top:816px!important;width:346px!important;text-align:center!important;
  font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:11px;line-height:14px;color:var(--pc-sub);
  -webkit-text-fill-color:var(--pc-sub)}
</style>
<script id="lot-CERCLE-TOILE">
(function(){
  var CADW=346, CADH=206, MONDES=['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'];
  var NGERMES=62, PART_COL=0.86, PERIODE=4500, MUE=900, CASC=420;
  var MOTS={ h:'Le Cercle', sub:'ta parole, et celle qu’on te tient',
    args:[['L’autre moitié de ta Toile','ce que tes proches tiennent envers toi'],
          ['Une parole n’est pas l’autre','récurrence, rappel, importance, mémoire'],
          ['Ta Toile change de matière','Sillons, Gravure, Terrazzo']],
    prix:['39 €','soit 3,25 €/mois'], legal:'Sans engagement · résiliable à tout moment' };
  var TOPS=[434,488,542];
  var CAD=null, CV=null, G=null, raf=0, prochaine=0, mue=null, ouvertA=0, dpr=1;
  var MONDECV=[], OWN=null, BOX=[], SEED=[], IMG=null, SRC=[];
  function ps(){ return document.getElementById('plusScreen'); }
  function el(t,c){ var e=document.createElement(t); if(c) e.className=c; return e; }
  /* ── LE SEMIS : des POSITIONS, pas des formes. Un gabarit de germe pris au moteur (Toile.preview) est cloné,
       comme le fait déjà `Toile_previewLive` : tous les champs existent et sont du bon type. ── */
  function semis(tpl, PAL){
    var n=NGERMES, gc=Math.max(5,Math.round(Math.sqrt(n*CADW/CADH))), gr=Math.max(4,Math.round(n/gc));
    var cw=CADW/gc, ch=CADH/gr, out=[];
    for(var r0=0;r0<gr;r0++) for(var c0=0;c0<gc;c0++){
      var s={}; for(var k in tpl) s[k]=tpl[k];
      s.x=cw*(c0+.5)+(Math.random()-.5)*cw*.62;
      s.y=ch*(r0+.5)+(Math.random()-.5)*ch*.62;
      s.tx=s.x; s.ty=s.y; s.px=null; s.py=null; s.w=0; s.wt=0; s.t0=-99999; s.gc=null;
      s.ang=Math.random()*Math.PI; s.tone=[1.0,0.76,1.24,0.88,1.12][(Math.random()*5)|0];
      if(Math.random()<PART_COL){ s.kind='promi'; s.ci=(Math.random()*PAL.length)|0; s.c=PAL[s.ci]; }
      else { s.kind='gray'; s.ci=null; s.c=null; }
      out.push(s);
    }
    return out;
  }
  function rendMonde(seeds, monde){
    var cv=document.createElement('canvas'); cv.width=Math.round(CADW*dpr); cv.height=Math.round(CADH*dpr);
    cv.__c={seeds:seeds.map(function(s){ var o={}; for(var k in s) o[k]=s[k]; return o; }), th:monde, pw:CADW, ph:CADH};
    try{ window.Toile.repaint(cv); }catch(_){ return null; }
    return cv;
  }
  /* l'attribution d'un pixel à sa cellule — la règle EXACTE du moteur (poids nuls sur une Toile engendrée : mesuré) */
  function attribue(seeds){
    var W=Math.round(CADW*dpr), H=Math.round(CADH*dpr), own=new Int16Array(W*H), n=seeds.length;
    BOX=[]; for(var i=0;i<n;i++) BOX.push({x0:W,y0:H,x1:0,y1:0});
    for(var y=0;y<H;y++){ var ly=(y+0.5)/dpr;
      for(var x=0;x<W;x++){ var lx=(x+0.5)/dpr, bd=1e18, bi=0;
        for(var q=0;q<n;q++){ var ex=lx-seeds[q].x, ey=ly-seeds[q].y, d=ex*ex+ey*ey; if(d<bd){bd=d;bi=q;} }
        own[y*W+x]=bi; var b=BOX[bi];
        if(x<b.x0)b.x0=x; if(x>b.x1)b.x1=x; if(y<b.y0)b.y0=y; if(y>b.y1)b.y1=y;
      } }
    return own;
  }
  function compose(){
    var W=Math.round(CADW*dpr), H=Math.round(CADH*dpr);
    var img=G.createImageData(W,H), d=img.data;
    for(var i=0;i<OWN.length;i++){
      var s=SRC[SEED[OWN[i]].m], o=i*4;
      d[o]=s[o]; d[o+1]=s[o+1]; d[o+2]=s[o+2]; d[o+3]=s[o+3];
    }
    return img;
  }
  function prepare(){
    dpr=Math.min(2,window.devicePixelRatio||1);
    var PAL=[]; try{ PAL=window.Toile.cols()||[]; }catch(_){ }
    if(!PAL.length) return false;
    /* un gabarit de germe, pris au moteur */
    var A=document.createElement('canvas'); A.width=Math.round(CADW*dpr); A.height=Math.round(CADH*dpr);
    try{ window.Toile.preview(A,'encre',CADW,CADH); }catch(_){ return false; }
    if(!A.__c||!A.__c.seeds||!A.__c.seeds.length) return false;
    var tpl=A.__c.seeds.filter(function(s){ return s.kind!=='gray'; })[0]||A.__c.seeds[0];
    var seeds=semis(tpl,PAL);
    MONDECV=[]; SRC=[];
    for(var m=0;m<MONDES.length;m++){
      var cv=rendMonde(seeds,MONDES[m]); if(!cv) return false;
      MONDECV.push(cv); SRC.push(cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data);
    }
    OWN=attribue(seeds);
    /* CHAQUE CELLULE PREND UNE MATIÈRE AU HASARD, parmi les HUIT — c'est le mélange que Tom demande */
    SEED=seeds.map(function(s,i){ return {i:i, m:(Math.random()*MONDES.length)|0, gray:s.kind==='gray'}; });
    CV.width=Math.round(CADW*dpr); CV.height=Math.round(CADH*dpr);
    G=CV.getContext('2d');
    IMG=compose();
    var comptes={}; SEED.forEach(function(s){ var w=MONDES[s.m]; comptes[w]=(comptes[w]||0)+1; });
    window._vendToile={ engendree:true, germes:seeds.length, colores:seeds.filter(function(s){return s.kind!=='gray';}).length,
      matieres:comptes, palette:PAL.length, dpr:dpr,
      sig:seeds.map(function(s,i){ return Math.round(s.x)+','+Math.round(s.y)+':'+SEED[i].m+':'+(s.ci==null?'g':s.ci); }).join('|') };
    return true;
  }
  function bez(t){ var lo=0,hi=1,u=t,i,x;
    for(i=0;i<18;i++){ u=(lo+hi)/2; var v=1-u; x=3*v*v*u*0.32+u*u*u; if(x<t) lo=u; else hi=u; }
    var v2=1-u; return 3*v2*v2*u*0.72+3*v2*u*u*1+u*u*u; }
  /* LA MUE — une seule cellule, et on ne retouche QUE sa boîte : recomposer les 285 000 pixels par image
     coûterait trop cher (CLAUDE §8 : un mouvement se calcule sur le temps réel, pas sur le compte d'images). */
  function mueImage(t){
    var m=mue, b=BOX[m.i], W=Math.round(CADW*dpr);
    var w=b.x1-b.x0+1, h=b.y1-b.y0+1; if(w<1||h<1) return;
    var p=Math.min(1,(t-m.t0)/MUE), e=bez(p);
    var img=G.createImageData(w,h), d=img.data, a=SRC[m.de], c=SRC[m.vers];
    for(var y=0;y<h;y++) for(var x=0;x<w;x++){
      var gx=b.x0+x, gy=b.y0+y, gi=gy*W+gx, o=(y*w+x)*4, go=gi*4;
      if(OWN[gi]!==m.i){ var s=SRC[SEED[OWN[gi]].m];
        d[o]=s[go]; d[o+1]=s[go+1]; d[o+2]=s[go+2]; d[o+3]=s[go+3]; continue; }
      d[o]=a[go]+(c[go]-a[go])*e; d[o+1]=a[go+1]+(c[go+1]-a[go+1])*e;
      d[o+2]=a[go+2]+(c[go+2]-a[go+2])*e; d[o+3]=a[go+3]+(c[go+3]-a[go+3])*e;
    }
    G.putImageData(img,b.x0,b.y0);
  }
  function image(t){
    raf=0; var s=ps(); if(!s||!s.classList.contains('show')) return;
    if(!ouvertA){ ouvertA=t; G.putImageData(IMG,0,0); }
    /* la pose : un balayage en diagonale sur 420 ms — la cascade, à 62 cellules, ne peut pas se faire cellule par cellule */
    var age=t-ouvertA;
    if(age<CASC){
      var e=bez(age/CASC);
      G.putImageData(IMG,0,0);
      G.save(); G.globalCompositeOperation='destination-in';
      var W=CV.width, H=CV.height, gd=G.createLinearGradient(0,0,W,H), q=e*1.35;
      gd.addColorStop(0,'rgba(0,0,0,1)');
      gd.addColorStop(Math.max(0,Math.min(1,q-0.18)),'rgba(0,0,0,1)');
      gd.addColorStop(Math.max(0,Math.min(1,q)),'rgba(0,0,0,0)');
      gd.addColorStop(1,'rgba(0,0,0,0)');
      G.fillStyle=gd; G.fillRect(0,0,W,H); G.restore();
      raf=requestAnimationFrame(image); return;
    }
    if(!mue && t>=prochaine && SEED.length){
      var k=(Math.random()*SEED.length)|0, de=SEED[k].m, vers=(de+1+((Math.random()*(MONDES.length-1))|0))%MONDES.length;
      mue={i:k, de:de, vers:vers, t0:t}; prochaine=t+PERIODE;
    }
    if(mue){ mueImage(t);
      if(t-mue.t0>=MUE){ SEED[mue.i].m=mue.vers; IMG=compose(); mue=null; } }
    else if(!prochaine){ prochaine=t+PERIODE; }
    raf=requestAnimationFrame(image);
  }
  function signature(mo){
    if(!mo||mo.__sigPose) return; mo.__sigPose=1;
    mo.addEventListener('pointerup',function(){
      var sig=mo.__sig; if(!sig||!MONDECV.length) return;
      var src=MONDECV[0];
      sig.width=Math.round(346*dpr); sig.height=Math.round(58*dpr);
      var g=sig.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
      var sw=src.width/dpr, sh=src.height/dpr, k=Math.max(346/sw,58/sh);
      g.clearRect(0,0,346,58); g.drawImage(src,(346-sw*k)/2,(58-sh*k)/2,sw*k,sh*k);
      var d0=performance.now(); window._vendSignature=(window._vendSignature||0)+1;
      (function pas(){ var p=(performance.now()-d0)/400;
        if(p>=1){ sig.style.opacity=0; return; }
        sig.style.opacity=String(Math.sin(p*Math.PI)*0.85); requestAnimationFrame(pas); })();
    },{passive:true});
  }
  function bati(){
    var s=ps(); if(!s) return false;
    if(CAD&&CAD.isConnected) return true;
    CAD=el('div'); CAD.id='pcCadre';
    var t=el('div','pc-toile'); CV=document.createElement('canvas'); t.appendChild(CV); CAD.appendChild(t);
    var h=el('div','pc-h'); h.textContent=MOTS.h; CAD.appendChild(h);
    var su=el('div','pc-sub'); su.textContent=MOTS.sub; CAD.appendChild(su);
    MOTS.args.forEach(function(a,i){ var d=el('div','pc-arg'); d.style.setProperty('top',TOPS[i]+'px','important');
      var b=el('b'); b.textContent=a[0]; var q=el('i'); q.textContent=a[1]; d.appendChild(b); d.appendChild(q); CAD.appendChild(d); });
    var p=el('div','pc-prix'); var pb=el('b'); pb.textContent=MOTS.prix[0]; var pi=el('i'); pi.textContent=MOTS.prix[1];
    p.appendChild(pb); p.appendChild(pi); CAD.appendChild(p);
    var mo=document.getElementById('buyMonth'), yr=document.getElementById('buyYear');
    if(mo){ mo.textContent=''; var sig=el('canvas','pc-sig'); var ec=el('span','pc-eclat');
      var lb=el('span','pc-lb'); lb.textContent='Essayer 14 jours'; var go=el('span','pc-go'); go.textContent='›';
      mo.appendChild(sig); mo.appendChild(ec); mo.appendChild(lb); mo.appendChild(go); mo.__sig=sig; CAD.appendChild(mo); }
    if(yr){ yr.textContent=''; var yl=el('span'); yl.textContent='ou prendre l’année — 39 €'; yr.appendChild(yl); CAD.appendChild(yr); }
    var lg=el('div','pc-legal'); lg.textContent=MOTS.legal; CAD.appendChild(lg);
    s.appendChild(CAD); signature(mo); return true;
  }
  function off(e,anc){ var x=0,y=0; while(e&&e!==anc){ x+=e.offsetLeft; y+=e.offsetTop; e=e.offsetParent; } return [x,y]; }
  function pose(){
    var s=ps(), dv=document.getElementById('device'); if(!s||!dv||!bati()) return;
    var fr=s.closest('.frame')||document.body, a=off(dv,fr), b=off(s,fr);
    CAD.style.setProperty('left',(a[0]-b[0])+'px','important'); CAD.style.setProperty('top',(a[1]-b[1])+'px','important');
  }
  function demarre(){
    if(!bati()) return;
    var t0=performance.now(); if(!prepare()) return;
    window._vendToile.ms=Math.round(performance.now()-t0);
    ouvertA=0; prochaine=0; mue=null;
    var mo=document.getElementById('buyMonth');
    if(mo){ mo.classList.remove('pc-pose'); void mo.offsetWidth; mo.classList.add('pc-pose'); }
    if(!raf) raf=requestAnimationFrame(image);
  }
  function arrete(){ if(raf){ cancelAnimationFrame(raf); raf=0; } }
  window._vendToileGo=demarre;
  var ouvert=false;
  function veille(){
    var s=ps(); if(!s) return;
    new MutationObserver(function(){
      var o=s.classList.contains('show'); if(o===ouvert) return; ouvert=o;
      if(o){ try{ s.scrollTop=0; pose(); }catch(_){ } setTimeout(demarre,0); } else arrete();
    }).observe(s,{attributes:true,attributeFilter:['class']});
  }
  try{ bati(); pose(); veille(); }catch(_){ }
})();
</script>
"""
assert S.count('</body>')==1
S=S.replace('</body>',BLOC+'</body>'); print('  ✔ lot-CERCLE-TOILE (v4, engendrée) posé en fin de fichier')
io.open(F,'w',encoding='utf-8').write(S)
print('copie', avant, '→', hashlib.md5(S.encode('utf-8')).hexdigest())
