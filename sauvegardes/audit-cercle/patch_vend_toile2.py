# L'ÉCRAN QUI VEND — SEPT CORRECTIONS + LE THÈME (Tom, 12 sept. 2026, troisième arbitrage).
import hashlib, io
F = 'scratchpad/app-vend-toile2.html'
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '3ac4975ccaed06419950963a8804a212', 'copie inattendue : ' + avant
def r(old, new, quoi):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple (%s) : %r' % (quoi, old[:80])
    S = S.replace(old, new); print('  ✔', quoi)

# ── LE PRIX, PARTOUT : 39 € l'année, 5,99 € le mois. Plus de pourcentage. Plus de « 39 € » sur la ligne du dessous (6).
r("Tout Promi pour <b>3,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>29&nbsp;€</b> · soit 2,42&nbsp;€/mois · −39&nbsp;%.",
  "Tout Promi pour <b>5,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>39&nbsp;€</b> · soit 3,25&nbsp;€/mois.", 'prix · .pl-sub')
r('<button class="pl-buy prim" id="buyMonth">Essayer 14 jours, puis 3,99&nbsp;€/mois</button>',
  '<button class="pl-buy prim" id="buyMonth">Essayer 14 jours</button>', 'prix · #buyMonth')
r('<button class="pl-buy sec" id="buyYear">Prendre l\'année</button>',
  '<button class="pl-buy sec" id="buyYear">ou prendre l\'année</button>', 'prix · #buyYear (6 · plus de 39 € en double)')
r("px.textContent = '29\\u00a0€'", "px.textContent = '39\\u00a0€'", 'prix · ancien lot')
r("so.textContent = 'soit 2,42\\u00a0€/mois · −39\\u00a0%'", "so.textContent = 'soit 3,25\\u00a0€/mois'", 'prix · ancien lot')
# ── LA VITESSE — un tour en 100 s (validé). La sphère reste sur l'Aura.
r("var G = { AUTO:6.283185307/120,",
  "var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept. 2026). 84 s TROP VIF (5 sept.), 120 s TROP LENT (12 sept.). */",
  'G.AUTO : un tour en 100 s')

BLOC = r"""
<style id="lot-CERCLE-TOILE-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — UNE VRAIE TOILE (Tom, 12 sept. 2026, sept corrections).
   UNE SEULE RUPTURE : la matière du pavage. UN SEUL MOUVEMENT : une dalle qui mue toutes les 4,5 s.
   1 · le ✕ FERMER est CELUI DU PRODUIT (`.closeb`) — on ne le redessine pas, on cesse de le masquer.
   2 · l'air est repris EN ENTIER : la Toile passe de 276 à 218, tous les écarts sont redonnés.
   3 · plus de diversité : couleurs et tailles choisies pour leur ÉCART, cellules qui CROISENT la fenêtre (≥ 12).
   4 · une autre Toile à chaque ouverture (fenêtre, choix, matières) — exception assumée au semis déterministe,
       qui régit la Toile d'un Promi et d'une Nuée, pas une composition d'écran.
   5 · le bouton porte le chevron du produit et une ombre dure plus franche.
   6 · « 39 € » ne paraît plus qu'une fois. 7 · la ligne du dessous prend la SECONDE COUCHE de l'encart signature,
       IMMOBILE (dans l'encart elle tourne — la faire tourner ici casserait la règle du mouvement unique).
   Le corps suit le thème comme partout ; seul le cadre de la Toile reste plus chaud que la page, dans les deux.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ */
#plusScreen>#plHeroCv,#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat,#plusScreen>.pl-plans,
#plusScreen>.pl-note,#plusScreen>.pl-eb,#plusScreen>.enh,#plusScreen #plCadre{display:none!important}
#plusScreen::before,.frame #plusScreen::before{display:none!important;content:none!important}
/* 1 · le ✕ FERMER reste CELUI DU PRODUIT : aucune règle ici, seulement le droit de passer au-dessus du cadre */
#plusScreen>.closeb{z-index:6!important}
#plusScreen #pcCadre{position:absolute!important;width:390px!important;height:844px!important;margin:0!important;
  pointer-events:none;z-index:3;background:transparent!important}
#plusScreen #pcCadre>*{position:absolute!important;margin:0!important;box-sizing:border-box!important}
/* LES ENCRES — le corps suit le thème (Tom) */
#plusScreen #pcCadre{--pc-ink:#1A1613;--pc-sub:#8A7E70;--pc-cadre:#E7D8C4;--pc-sec:#EADFCE;--pc-sec2:#DCCBB2;--pc-secl:#CDB894}
.frame:not(.light) #plusScreen #pcCadre,#device:not(.light) #plusScreen #pcCadre{
  --pc-ink:#F4EEE1;--pc-sub:#A79C8E;--pc-cadre:#26202E;--pc-sec:#221E30;--pc-sec2:#2E2740;--pc-secl:#3C3352}
/* 2 · LA TOILE — 346 × 218, fond franchement écarté de la page */
#plusScreen #pcCadre .pc-toile{left:22px!important;top:86px!important;width:346px!important;height:218px!important;
  border-radius:28px!important;background:var(--pc-cadre)!important;overflow:hidden!important}
#plusScreen #pcCadre .pc-toile canvas{position:absolute;left:0;top:0;width:346px;height:218px;display:block}
#plusScreen #pcCadre .pc-h{left:49.5px!important;top:336px!important;width:291px!important;
  font-family:Fraunces,Georgia,serif;font-weight:600;font-size:32px;line-height:38px;color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-sub{left:49.5px!important;top:382px!important;width:291px!important;
  font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:15px;line-height:22px;color:var(--pc-sub);
  -webkit-text-fill-color:var(--pc-sub);white-space:nowrap}
#plusScreen #pcCadre .pc-arg{left:49.5px!important;width:291px!important}
#plusScreen #pcCadre .pc-arg b{display:block;font-family:ApfelMid,system-ui,sans-serif;font-weight:500;font-size:17px;
  line-height:22px;color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-arg i{display:block;font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;
  font-size:13px;line-height:18px;color:var(--pc-sub);-webkit-text-fill-color:var(--pc-sub)}
#plusScreen #pcCadre .pc-prix{left:49.5px!important;top:612px!important;width:291px!important;
  display:flex!important;align-items:baseline!important;justify-content:space-between!important}
#plusScreen #pcCadre .pc-prix b{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:40px;line-height:40px;
  color:var(--pc-ink);-webkit-text-fill-color:var(--pc-ink)}
#plusScreen #pcCadre .pc-prix i{font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:13px;
  color:var(--pc-sub);-webkit-text-fill-color:var(--pc-sub)}
/* 5 · LE CTA PRIMAIRE — framboise, ombre DURE plus franche, chevron du produit */
#plusScreen #pcCadre #buyMonth{left:22px!important;top:680px!important;width:346px!important;max-width:346px!important;
  height:58px!important;min-height:58px!important;border-radius:29px!important;border:0!important;
  display:flex!important;align-items:center!important;justify-content:center!important;gap:10px!important;
  background:#FA2258!important;color:#FFF4F6!important;-webkit-text-fill-color:#FFF4F6!important;
  font-family:ApfelMid,system-ui,sans-serif!important;font-weight:500!important;font-size:17px!important;
  letter-spacing:.005em!important;box-shadow:0 4px 0 0 #A50E36!important;pointer-events:auto!important;
  position:absolute!important;overflow:hidden!important;transition:box-shadow .11s linear,transform .11s linear}
#plusScreen #pcCadre #buyMonth:active{box-shadow:0 0 0 0 #A50E36!important;transform:translateY(4px)}
#plusScreen #pcCadre #buyMonth .pc-sig{position:absolute;left:0;top:0;width:346px;height:58px;opacity:0;pointer-events:none}
#plusScreen #pcCadre #buyMonth .pc-lb,#plusScreen #pcCadre #buyMonth .pc-go{position:relative;z-index:2}
#plusScreen #pcCadre #buyMonth .pc-go{font-size:20px;font-weight:500;opacity:.9;transform:translateY(-1px)}
/* 7 · LE CTA SECONDAIRE — la SECONDE COUCHE de l'encart signature, immobile, hors du mauve */
#plusScreen #pcCadre #buyYear{left:22px!important;top:756px!important;width:346px!important;max-width:346px!important;
  height:44px!important;min-height:0!important;border:1px solid var(--pc-secl)!important;border-radius:22px!important;
  background:var(--pc-sec)!important;display:flex!important;align-items:center!important;justify-content:center!important;
  box-shadow:none!important;font-family:ApfelMid,system-ui,sans-serif!important;font-weight:500!important;font-size:15px!important;
  color:var(--pc-ink)!important;-webkit-text-fill-color:var(--pc-ink)!important;text-decoration:none!important;
  pointer-events:auto!important;position:absolute!important;overflow:hidden!important}
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
  var CADW = 346, CADH = 218, MONDES_C = ['sillons', 'gravure', 'terrazzo'];
  var N_MIN = 12, N_MAX = 14, PERIODE = 4500, MUE = 900, CASC = 420, PAS = 18;
  var MOTS = { h:'Le Cercle', sub:'ta parole, et celle qu’on te tient',
    args:[['L’autre moitié de ta Toile','ce que tes proches tiennent envers toi'],
          ['Une parole n’est pas l’autre','récurrence, rappel, importance, mémoire'],
          ['Ta Toile change de matière','Sillons, Gravure, Terrazzo']],
    prix:['39 €','soit 3,25 €/mois'], legal:'Sans engagement · résiliable à tout moment' };
  var TOPS = [434, 488, 542];
  var CAD=null, CV=null, G=null, DAL=[], raf=0, prochaine=0, mue=null, ouvertA=0, iMue=-1;
  function ps(){ return document.getElementById('plusScreen'); }
  function el(t,c){ var e=document.createElement(t); if(c) e.className=c; return e; }
  var CACHE = {};
  function matiere(id, m){
    var k = id+'|'+(m||''); if(CACHE[k]!==undefined) return CACHE[k];
    var base={}; try{ base=window.Toile.mondeCourant()||{}; }catch(_){ }
    var c=document.createElement('canvas'), ok=false;
    try{ ok=window.Toile.dalleTrame(c, id, 1, m?{m:m,p:base.p,h:base.h}:undefined); }catch(_){ }
    return (CACHE[k] = (ok&&c.width)?c:null);
  }
  /* la couleur moyenne d'une dalle rendue — on la LIT dans la matière, on ne la reconstruit pas */
  function teinte(cv){
    if(cv.__teinte) return cv.__teinte;
    var g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data, r=0,v=0,b=0,n=0;
    for(var i=0;i<d.length;i+=16){ if(d[i+3]<40) continue; r+=d[i]; v+=d[i+1]; b+=d[i+2]; n++; }
    return (cv.__teinte = n?[r/n,v/n,b/n]:[0,0,0]);
  }
  function ecart(a,b){ return Math.hypot(a[0]-b[0],a[1]-b[1],a[2]-b[2]); }
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
  /* 3+4 · la fenêtre : on RETIENT les cellules qui la CROISENT (≥12), et on en TIRE une différente à chaque ouverture */
  function fenetre(cells){
    var s=CADW/390, vh=CADH/s;
    var y0=Math.min.apply(null,cells.map(function(c){return c.y;}));
    var y1=Math.max.apply(null,cells.map(function(c){return c.y+c.h;}));
    var bonnes=[];
    for(var t=y0; t<=Math.max(y0,y1-vh); t+=6){
      var n=0;
      for(var i=0;i<cells.length;i++){ var c=cells[i];
        if(c.y+c.h > t && c.y < t+vh) n++; }               /* CROISE, pas « centre dedans » */
      if(n>=N_MIN) bonnes.push({t:t,n:n});
    }
    if(!bonnes.length){ var best=y0,bn=-1;
      for(var t2=y0;t2<=Math.max(y0,y1-vh);t2+=6){ var m=0;
        for(var j=0;j<cells.length;j++){ var cc=cells[j]; if(cc.y+cc.h>t2&&cc.y<t2+vh) m++; }
        if(m>bn){bn=m;best=t2;} }
      bonnes=[{t:best,n:bn}];
    }
    var pick=bonnes[(Math.random()*bonnes.length)|0];
    return {s:s, oy:pick.t, vh:vh, dedans:pick.n, bandes:bonnes.length};
  }
  function prepare(){
    var cells=recense(); if(!cells.length) return false;
    var F=fenetre(cells);
    var dans=cells.filter(function(c){ return c.y+c.h>F.oy && c.y<F.oy+F.vh; });
    if(!dans.length) dans=cells.slice();
    var dpr=Math.min(2,window.devicePixelRatio||1), base=null;
    try{ base=(window.Toile.mondeCourant()||{}).m; }catch(_){ }
    /* 3 · DIVERSITÉ : on rend chaque candidate, on lit sa teinte, et on choisit pour l'ÉCART de couleur ET de taille */
    var cand=dans.map(function(c){ var cv=matiere(c.id,base); return cv?{c:c,cv:cv,t:teinte(cv),aire:c.w*c.h}:null; }).filter(Boolean);
    if(cand.length>N_MAX){
      var choisi=[cand.splice((Math.random()*cand.length)|0,1)[0]];
      while(choisi.length<N_MAX && cand.length){
        var bi=0,bs=-1;
        for(var i=0;i<cand.length;i++){
          var dc=1e9, da=1e9;
          for(var j=0;j<choisi.length;j++){
            dc=Math.min(dc, ecart(cand[i].t,choisi[j].t));
            da=Math.min(da, Math.abs(Math.sqrt(cand[i].aire)-Math.sqrt(choisi[j].aire)));
          }
          var sc=dc+da*2.2;                                  /* couleur ET taille */
          if(sc>bs){bs=sc;bi=i;}
        }
        choisi.push(cand.splice(bi,1)[0]);
      }
      cand=choisi;
    }
    cand.sort(function(a,b){ return (a.c.y-b.c.y)||(a.c.x-b.c.x); });
    /* 4 · TROIS en matière Cercle, tirées à chaque ouverture, et les trois mondes distribués au hasard */
    var idx=cand.map(function(_,i){return i;});
    for(var k=idx.length-1;k>0;k--){ var q=(Math.random()*(k+1))|0; var tmp=idx[k]; idx[k]=idx[q]; idx[q]=tmp; }
    var trois=idx.slice(0,3), mondes=MONDES_C.slice();
    for(var k2=mondes.length-1;k2>0;k2--){ var q2=(Math.random()*(k2+1))|0; var t2=mondes[k2]; mondes[k2]=mondes[q2]; mondes[q2]=t2; }
    DAL=cand.map(function(o,i){
      var p=trois.indexOf(i), m=(p>=0)?mondes[p]:base;
      var cv=(p>=0)?matiere(o.c.id,m):o.cv; if(!cv) return null;
      var dw=cv.width/dpr, dh=cv.height/dpr, padX=(dw-o.c.w)/2, padY=(dh-o.c.h)/2;
      return {id:o.c.id, monde:m, cercle:p>=0, cv:cv, base:base,
              X:(o.c.x-padX)*F.s, Y:(o.c.y-padY-F.oy)*F.s, W:dw*F.s, H:dh*F.s};
    }).filter(Boolean);
    CV.width=Math.round(CADW*dpr); CV.height=Math.round(CADH*dpr);
    G=CV.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
    var tt=DAL.map(function(d){return teinte(d.cv);});
    var sp=0; for(var a=0;a<tt.length;a++) for(var b=a+1;b<tt.length;b++) sp=Math.max(sp,ecart(tt[a],tt[b]));
    window._vendToile={dalles:DAL.length, cercle:DAL.filter(function(d){return d.cercle;}).map(function(d){return d.monde;}),
      fenetre:{y:Math.round(F.oy), hauteur:Math.round(F.vh), echelle:+F.s.toFixed(4), dedans:F.dedans, bandes:F.bandes},
      base:base, ecartCouleurMax:Math.round(sp),
      tailles:DAL.map(function(d){return Math.round(Math.sqrt(d.W*d.H));})};
    return DAL.length>0;
  }
  function bez(t){ var lo=0,hi=1,u=t,i,x;
    for(i=0;i<18;i++){ u=(lo+hi)/2; var v=1-u; x=3*v*v*u*0.32+u*u*u; if(x<t) lo=u; else hi=u; }
    var v2=1-u; return 3*v2*v2*u*0.72+3*v2*u*u*1+u*u*u; }
  function peint(t){
    G.clearRect(0,0,CADW,CADH);
    for(var i=0;i<DAL.length;i++){
      var d=DAL[i], age=t-ouvertA-i*PAS, a=age<=0?0:(age>=CASC?1:bez(age/CASC));
      if(a<=0) continue;
      if(mue&&mue.i===i){ var p=Math.min(1,(t-mue.t0)/MUE), e=bez(p);
        G.globalAlpha=a*(1-e); G.drawImage(d.cv,d.X,d.Y,d.W,d.H);
        G.globalAlpha=a*e;     G.drawImage(mue.cv,d.X,d.Y,d.W,d.H);
      } else { G.globalAlpha=a; G.drawImage(d.cv,d.X,d.Y,d.W,d.H); }
    }
    G.globalAlpha=1;
  }
  function image(t){
    raf=0; var s=ps(); if(!s||!s.classList.contains('show')) return;
    if(!ouvertA) ouvertA=t;
    if(!mue && t>=prochaine && DAL.length){
      iMue=(iMue+1)%DAL.length; var d=DAL[iMue];
      /* une dalle Cercle redevient ce qu'elle était, une autre prend une matière Cercle : on en garde TROIS */
      var suite = d.cercle ? d.base : MONDES_C[(Math.random()*3)|0];
      var cv=matiere(d.id,suite);
      if(cv&&cv!==d.cv) mue={i:iMue,t0:t,cv:cv,monde:suite};
      prochaine=t+PERIODE;
    }
    if(mue && t-mue.t0>=MUE){ var dd=DAL[mue.i]; dd.cv=mue.cv; dd.monde=mue.monde; dd.cercle=(mue.monde!==dd.base); mue=null; }
    peint(t); raf=requestAnimationFrame(image);
  }
  function signature(mo){
    if(!mo||mo.__sigPose) return; mo.__sigPose=1;
    mo.addEventListener('pointerup', function(){
      var sig=mo.__sig; if(!sig||!DAL.length) return;
      var src=matiere(DAL[0].id,null); if(!src) return;
      var dpr=Math.min(2,window.devicePixelRatio||1);
      sig.width=Math.round(346*dpr); sig.height=Math.round(58*dpr);
      var g=sig.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
      var sw=src.width/dpr, sh=src.height/dpr, k=Math.max(346/sw,58/sh);
      g.clearRect(0,0,346,58); g.drawImage(src,(346-sw*k)/2,(58-sh*k)/2,sw*k,sh*k);
      var d0=performance.now();
      (function pas(){ var p=(performance.now()-d0)/400;
        if(p>=1){ sig.style.opacity=0; return; }
        sig.style.opacity=String(Math.sin(p*Math.PI)*0.85); requestAnimationFrame(pas); })();
    }, {passive:true});
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
    if(yr){ yr.textContent=''; var yl=el('span'); yl.textContent='ou prendre l’année'; yr.appendChild(yl); CAD.appendChild(yr); }
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
assert S.count('</body>') == 1
S = S.replace('</body>', BLOC + '</body>'); print('  ✔ lot-CERCLE-TOILE (v2) posé en fin de fichier')
io.open(F,'w',encoding='utf-8').write(S)
print('copie', avant, '→', hashlib.md5(S.encode('utf-8')).hexdigest())
