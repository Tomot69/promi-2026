# L'ÉCRAN QUI VEND — TOILE DENSE (Tom, 12 sept., quatrième arbitrage). Cinq corrections.
import hashlib, io
F='scratchpad/app-vend-toile3.html'; S=io.open(F,encoding='utf-8').read()
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
  '<button class="pl-buy sec" id="buyYear">ou prendre l\'année — 39&nbsp;€</button>', '2 · « 39 € » revient sur la ligne du dessous')
r("px.textContent = '29\\u00a0€'", "px.textContent = '39\\u00a0€'", 'prix · ancien lot')
r("so.textContent = 'soit 2,42\\u00a0€/mois · −39\\u00a0%'", "so.textContent = 'soit 3,25\\u00a0€/mois'", 'prix · ancien lot')
r("var G = { AUTO:6.283185307/120,",
  "var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept. 2026). 84 s TROP VIF, 120 s TROP LENT. */",
  'G.AUTO : un tour en 100 s')

BLOC = r"""
<style id="lot-CERCLE-TOILE-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — LA VRAIE TOILE, DENSE (Tom, 12 sept. 2026) : « une Toile clairsemée n'est pas une Toile,
   et c'est ce qu'on vend ». Le fond du cadre est la Toile ENTIÈRE (`Toile.renderTo`, cellules neutres comprises),
   recadrée ; les trois matières Cercle sont posées PAR-DESSUS, sur leurs vraies cellules.
   L'effet de panneau ne vient plus d'un aplat (il masquerait la densité) mais d'un FILET de 2 px en halo et du
   rayon 28 — la densité n'est pas sacrifiée à la lisibilité du cadre.
   POLICES : celles du produit — Bricolage 600/700 titres et libellés, Apfel 400 / ApfelMid 500 texte,
   Fraunces 600 pour « Le Cercle » et « 39 € » (décision Tom, à inscrire en Q194).
   UNE SEULE RUPTURE : la matière du pavage. UN SEUL MOUVEMENT : une dalle qui mue toutes les 4,5 s.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#plusScreen>#plHeroCv,#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat,#plusScreen>.pl-plans,
#plusScreen>.pl-note,#plusScreen>.pl-eb,#plusScreen #plCadre{display:none!important}
#plusScreen::before,.frame #plusScreen::before{display:none!important;content:none!important}
/* le plateau perd sa pilule et son titre, MAIS GARDE son ✕ : le closer du produit vit dedans (`.enh > .closeb`) */
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
/* 3 · LA TOILE — baissée de 12 et raccourcie d'autant : le reste de la composition ne bouge pas */
#plusScreen #pcCadre .pc-toile{left:22px!important;top:98px!important;width:346px!important;height:206px!important;
  border-radius:28px!important;overflow:hidden!important;background:var(--pc-filet)!important;
  box-shadow:0 0 0 2px var(--pc-filet)!important}
#plusScreen #pcCadre .pc-toile canvas{position:absolute;left:0;top:0;width:346px;height:206px;display:block}
/* 1 · LES POLICES DU PRODUIT */
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
#plusScreen #pcCadre #buyMonth{left:22px!important;top:680px!important;width:346px!important;max-width:346px!important;
  height:58px!important;min-height:58px!important;border-radius:29px!important;border:0!important;
  display:flex!important;align-items:center!important;justify-content:center!important;gap:10px!important;
  background:#FA2258!important;color:#FFF4F6!important;-webkit-text-fill-color:#FFF4F6!important;
  font-family:Bricolage,system-ui,sans-serif!important;font-weight:700!important;font-size:17px!important;
  letter-spacing:-.01em!important;box-shadow:0 4px 0 0 #A50E36!important;pointer-events:auto!important;
  position:absolute!important;overflow:hidden!important;transition:box-shadow .11s linear,transform .11s linear}
#plusScreen #pcCadre #buyMonth:active{box-shadow:0 0 0 0 #A50E36!important;transform:translateY(4px)}
#plusScreen #pcCadre #buyMonth .pc-sig{position:absolute;left:0;top:0;width:346px;height:58px;opacity:0;pointer-events:none}
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
  var CADW=346, CADH=206, MONDES_C=['sillons','gravure','terrazzo'];
  var N_MIN=12, N_MAX=14, PERIODE=4500, MUE=900, CASC=420, PAS=18;
  var MOTS={ h:'Le Cercle', sub:'ta parole, et celle qu’on te tient',
    args:[['L’autre moitié de ta Toile','ce que tes proches tiennent envers toi'],
          ['Une parole n’est pas l’autre','récurrence, rappel, importance, mémoire'],
          ['Ta Toile change de matière','Sillons, Gravure, Terrazzo']],
    prix:['39 €','soit 3,25 €/mois'], legal:'Sans engagement · résiliable à tout moment' };
  var TOPS=[434,488,542];
  var CAD=null, CV=null, G=null, BASE=null, BW=0, BH=0, F=null, OVL=[], raf=0, prochaine=0, mue=null, ouvertA=0, iMue=-1;
  function ps(){ return document.getElementById('plusScreen'); }
  function el(t,c){ var e=document.createElement(t); if(c) e.className=c; return e; }
  var CACHE={};
  function matiere(id,m){
    var k=id+'|'+(m||''); if(CACHE[k]!==undefined) return CACHE[k];
    var base={}; try{ base=window.Toile.mondeCourant()||{}; }catch(_){ }
    var c=document.createElement('canvas'), ok=false;
    try{ ok=window.Toile.dalleTrame(c,id,1,m?{m:m,p:base.p,h:base.h}:undefined); }catch(_){ }
    return (CACHE[k]=(ok&&c.width)?c:null);
  }
  /* l'écart d'une cellule entre deux matières, en niveaux — c'est LUI qui dit si une matière « se voit » */
  function ecartMat(a,b){
    if(!a||!b) return 0;
    var W=Math.min(a.width,b.width), H=Math.min(a.height,b.height);
    if(W<4||H<4) return 0;
    var da=a.getContext('2d').getImageData(0,0,W,H).data, db=b.getContext('2d').getImageData(0,0,W,H).data;
    var s=0,n=0;
    for(var i=0;i<da.length;i+=16){ if(da[i+3]<24&&db[i+3]<24) continue;
      s+=(Math.abs(da[i]-db[i])+Math.abs(da[i+1]-db[i+1])+Math.abs(da[i+2]-db[i+2]))/3; n++; }
    return n?s/n:0;
  }
  function recense(){
    var ids=[];
    try{ ids=(typeof promises!=='undefined'?promises:[]).filter(function(p){return !p.draft&&!p.req;}).map(function(p){return p.id;}); }catch(_){ }
    if(!ids.length) return [];
    try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(_){ }
    var out=[];
    ids.forEach(function(id){ var d=null; try{ d=window.Toile.dalleAbs(id); }catch(_){ }
      if(d&&d.w>0&&d.h>0) out.push({id:id,x:d.minx,y:d.miny,w:d.w,h:d.h}); });
    return out;
  }
  /* 4 · LA FENÊTRE — échelle ET position tirées à chaque ouverture, parmi celles qui montrent 12 à 14 dalles colorées.
     Reculer ou avancer l'échelle est un ZOOM sur la vraie Toile, jamais un étirement (§4). */
  function fenetre(cells){
    var S0=CADW/390, bons=[];
    [S0, S0*1.07, S0*1.15, S0*1.24, S0*1.34].forEach(function(s){
      var vw=CADW/s, vh=CADH/s;
      if(vw>BW+0.5||vh>BH+0.5) return;
      for(var ox=0; ox<=BW-vw; ox+=18)
        for(var oy=0; oy<=BH-vh; oy+=18){
          var n=0;
          for(var i=0;i<cells.length;i++){ var c=cells[i];
            if(c.y+c.h>oy&&c.y<oy+vh&&c.x+c.w>ox&&c.x<ox+vw) n++; }
          if(n>=N_MIN&&n<=N_MAX+4) bons.push({s:s,ox:ox,oy:oy,vw:vw,vh:vh,n:n});
        }
    });
    if(!bons.length){ var s2=S0, vw2=CADW/s2, vh2=CADH/s2, best=null;
      for(var oy2=0; oy2<=BH-vh2; oy2+=12){ var m=0;
        for(var j=0;j<cells.length;j++){ var cc=cells[j]; if(cc.y+cc.h>oy2&&cc.y<oy2+vh2) m++; }
        if(!best||m>best.n) best={s:s2,ox:0,oy:oy2,vw:vw2,vh:vh2,n:m}; }
      return best;
    }
    return bons[(Math.random()*bons.length)|0];
  }
  function prepare(){
    var dpr=Math.min(2,window.devicePixelRatio||1), base=null;
    try{ base=(window.Toile.mondeCourant()||{}).m; }catch(_){ }
    /* LA TOILE ENTIÈRE, cellules neutres comprises — c'est elle le fond du cadre */
    BASE=document.createElement('canvas');
    var ok=false; try{ ok=window.Toile.renderTo(BASE,2); }catch(_){ }
    if(!ok||!BASE.width) return false;
    BW=BASE.width/2; BH=BASE.height/2;
    var cells=recense(); if(!cells.length) return false;
    F=fenetre(cells); if(!F) return false;
    var dans=cells.filter(function(c){ return c.y+c.h>F.oy&&c.y<F.oy+F.vh&&c.x+c.w>F.ox&&c.x<F.ox+F.vw; });
    if(dans.length<3) dans=cells.slice();
    /* 5 · LE TERRAZZO D'ABORD : il s'écarte 45 % moins que les deux autres (mesuré). On lui donne la cellule où il
       se voit le PLUS — écart × taille — puis on tire parmi les meilleures pour garder la variation. */
    var notes=dans.map(function(c){
      var b=matiere(c.id,base), t=matiere(c.id,'terrazzo');
      return {c:c, e:ecartMat(b,t), aire:c.w*c.h};
    }).sort(function(a,b){ return (b.e*Math.sqrt(b.aire))-(a.e*Math.sqrt(a.aire)); });
    var hautes=notes.slice(0,Math.max(1,Math.min(3,notes.length)));
    var terr=hautes[(Math.random()*hautes.length)|0];
    var reste=dans.filter(function(c){ return c!==terr.c; });
    for(var k=reste.length-1;k>0;k--){ var q=(Math.random()*(k+1))|0; var tp=reste[k]; reste[k]=reste[q]; reste[q]=tp; }
    var deux=['sillons','gravure']; if(Math.random()<0.5) deux.reverse();
    var choix=[{c:terr.c,m:'terrazzo',e:terr.e}];
    for(var z=0; z<2 && z<reste.length; z++){ var b2=matiere(reste[z].id,base), m2=matiere(reste[z].id,deux[z]);
      choix.push({c:reste[z], m:deux[z], e:ecartMat(b2,m2)}); }
    OVL=choix.map(function(o){
      var cv=matiere(o.c.id,o.m); if(!cv) return null;
      var dw=cv.width/dpr, dh=cv.height/dpr, padX=(dw-o.c.w)/2, padY=(dh-o.c.h)/2;
      return {id:o.c.id, monde:o.m, base:base, cv:cv, ecart:Math.round(o.e), cell:o.c,
              X:(o.c.x-padX-F.ox)*F.s, Y:(o.c.y-padY-F.oy)*F.s, W:dw*F.s, H:dh*F.s, a:1};
    }).filter(Boolean);
    CV.width=Math.round(CADW*dpr); CV.height=Math.round(CADH*dpr);
    G=CV.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
    window._vendToile={ dense:true, toile:[BW,BH], fenetre:{s:+F.s.toFixed(3), ox:Math.round(F.ox), oy:Math.round(F.oy),
      largeur:Math.round(F.vw), hauteur:Math.round(F.vh)}, dallesVues:dans.length, base:base,
      cercle:OVL.map(function(o){ return {id:o.id, monde:o.monde, ecart:o.ecart}; }),
      sig:[+F.s.toFixed(3), Math.round(F.ox), Math.round(F.oy)].join('/')+'|'
          + dans.map(function(c){return c.id;}).sort(function(a,b){return a-b;}).join(',')+'|'
          + OVL.map(function(o){return o.id+':'+o.monde;}).sort().join(',') };
    return true;
  }
  function bez(t){ var lo=0,hi=1,u=t,i,x;
    for(i=0;i<18;i++){ u=(lo+hi)/2; var v=1-u; x=3*v*v*u*0.32+u*u*u; if(x<t) lo=u; else hi=u; }
    var v2=1-u; return 3*v2*v2*u*0.72+3*v2*u*u*1+u*u*u; }
  function peint(t){
    G.clearRect(0,0,CADW,CADH);
    var ageB=t-ouvertA, aB=ageB<=0?0:(ageB>=CASC?1:bez(ageB/CASC));
    G.globalAlpha=aB;
    G.drawImage(BASE, F.ox*2, F.oy*2, F.vw*2, F.vh*2, 0, 0, CADW, CADH);
    for(var i=0;i<OVL.length;i++){
      var o=OVL[i], age=t-ouvertA-i*PAS, a=age<=0?0:(age>=CASC?1:bez(age/CASC));
      var al=a*o.a;
      if(mue&&mue.i===i){ var p=Math.min(1,(t-mue.t0)/MUE), e=bez(p);
        al = a*(mue.vers ? e : 1-e); }
      if(al<=0) continue;
      G.globalAlpha=al; G.drawImage(o.cv,o.X,o.Y,o.W,o.H);
    }
    G.globalAlpha=1;
  }
  function image(t){
    raf=0; var s=ps(); if(!s||!s.classList.contains('show')) return;
    if(!ouvertA) ouvertA=t;
    /* UN SEUL MOUVEMENT : toutes les 4,5 s, UNE matière Cercle se retire ou se pose */
    if(!mue && t>=prochaine && OVL.length){
      iMue=(iMue+1)%OVL.length;
      mue={i:iMue, t0:t, vers:!OVL[iMue].a};       /* elle est là → elle s'en va ; elle n'y est pas → elle revient */
      prochaine=t+PERIODE;
    }
    if(mue && t-mue.t0>=MUE){ OVL[mue.i].a = mue.vers?1:0; mue=null; }
    peint(t); raf=requestAnimationFrame(image);
  }
  function signature(mo){
    if(!mo||mo.__sigPose) return; mo.__sigPose=1;
    mo.addEventListener('pointerup',function(){
      var sig=mo.__sig; if(!sig||!OVL.length) return;
      var src=matiere(OVL[0].id,null); if(!src) return;
      var dpr=Math.min(2,window.devicePixelRatio||1);
      sig.width=Math.round(346*dpr); sig.height=Math.round(58*dpr);
      var g=sig.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
      var sw=src.width/dpr, sh=src.height/dpr, k=Math.max(346/sw,58/sh);
      g.clearRect(0,0,346,58); g.drawImage(src,(346-sw*k)/2,(58-sh*k)/2,sw*k,sh*k);
      var d0=performance.now();
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
    if(mo){ mo.textContent=''; var sig=el('canvas','pc-sig'); var lb=el('span','pc-lb'); lb.textContent='Essayer 14 jours';
      var go=el('span','pc-go'); go.textContent='›';
      mo.appendChild(sig); mo.appendChild(lb); mo.appendChild(go); mo.__sig=sig; CAD.appendChild(mo); }
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
  function demarre(){ CACHE={}; if(!bati()||!prepare()) return; ouvertA=0; prochaine=0; mue=null; iMue=-1;
    if(!raf) raf=requestAnimationFrame(image); }
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
S=S.replace('</body>',BLOC+'</body>'); print('  ✔ lot-CERCLE-TOILE (v3, dense) posé en fin de fichier')
io.open(F,'w',encoding='utf-8').write(S)
print('copie', avant, '→', hashlib.md5(S.encode('utf-8')).hexdigest())
