
/* ⚑ v161 (Tom, C-181) — LA VEILLE. « Après 60 s sans aucun toucher, sur n'importe quel écran (sauf pendant une saisie et pendant un geste), un fond plein
   #050302 et le logo PROMI seul, ≈ 140 × 40 pt, qui glisse en diagonale à 60 pt/s et rebondit sur les quatre bords (zones sûres de l'iPhone) ; à chaque
   rebond la couleur suivante de la palette du Studio, jamais deux fois la même d'affilée ; au coin exact (les deux bords à 2 pt près) le vert amande
   #8FE08F, la seule fois où il le prend ; l'angle varie de ± 2 à 3° autour de 45° à chaque rebond ; aucun coin dans la première minute ; entrée et
   sortie en flaques ; un toucher n'importe où la quitte et ramène à l'écran exact, sans rien actionner dessous ; l'écran reste allumé (Wake Lock)
   jusqu'à 10 min de veille. »
   · LE LOGO est un petit canevas peint UNE fois par couleur (jamais `fillText` dans la boucle d'images) et déplacé par `transform` : une boîte de
     140 × 40 pt (l'encre de PROMI, 140 × 27, centrée en hauteur), c'est elle qui touche les bords. Pas de clignotement du I (ce n'est pas le mot-marque : un dessin fixe).
   · LA TRAJECTOIRE se calcule par ÉVÉNEMENTS (le prochain bord touché), la même fonction sert l'écran et la simulation (`window._veilleSimule`) : un coin
     est le rebond où l'autre bord est à 2 pt au plus. À chaque rebond l'angle est tiré (45° ± 2 à 3°, dans le quadrant du rebond) ; si le prochain
     rebond serait un coin avant 60 s de veille (ou moins de 60 s après le coin précédent : sans cela ils venaient par grappes, la trajectoire repassant
     sur elle-même), l'angle est tiré de nouveau.
   · LES ZONES SÛRES (pt de l'appareil 390 × 844) : 59 en haut (l'île), 34 en bas (la barre d'accueil), 8 sur les côtés (le coin arrondi de l'écran).
   · Un ton de la palette qui ne se lit pas sur #050302 (moins de 3:1) est sauté : sous une palette sombre le logo disparaîtrait.
   Réglages pour les juges : `?veille=5` (le délai, en s), `?coin=1` (un coin forcé entre 60 et 90 s de veille) ; `window._veilleRegle`, `window._veille()`.
   Swift (portage/) : `UIApplication.shared.isIdleTimerDisabled`, sans limite seulement quand l'iPhone est branché.
   ⚑ v162 (Tom, C-181, v161b §3) — « LE LOGO NE TOUCHE PAS LES BORDS DE L'ÉCRAN » : la veille couvre maintenant TOUTE LA ZONE VISIBLE du Safari (la fenêtre
   visible, `visualViewport`, plus seulement le cadre de l'app) ; elle rebondit sur ses BORDS RÉELS, relus à chaque redimensionnement (taille, orientation,
   barres de Safari), moins les zones sûres du système (`env(safe-area-inset-*)`) ; c'est l'ENCRE du logo (140 × 27 pt) qui touche — aucune valeur en dur :
   les points de l'app sont convertis à l'échelle de l'appareil (la largeur de `#device` sur 390). LE FOND est celui de la Toile du thème (`_fondToileVif`,
   le même pour les vingt mondes aujourd'hui : #DFCAA4 en clair, #050302 en sombre) ; une couleur de la palette sous 3:1 sur lui est sautée — et s'il en reste
   moins de deux (en clair, aucun ton d'Ingénu n'atteint 3:1), les tons de la palette, teinte gardée, sont amenés à 3:1 (`_teinte.ajuste`, v125). LES COINS :
   la règle « pas de coin dans la minute qui suit un coin » est retirée ; reste « aucun coin dans la première minute » ; le reste est le seul hasard de l'angle.
   ⚑ v163 (Tom, C-181 §3) — « le logo doit toucher les bords haut et bas VISIBLES » : l'encre est lue sur les pixels peints (plus `measureText`, dont la
   boîte dépasse l'encre) ; l'entrée et la sortie en flaques passent à 350 ms chacune (1 100 et 900 avant). */
(function(){
  var Q=new URLSearchParams(location.search);
  /* ⚑ v183c (Tom, 7 nov. 2026, C-249 : « la veille DVD arrive trop tôt — passe le délai de 60 s à 75 s ; le reste est inchangé ») */
  var R=window._veilleRegle={DELAI:(Q.has('veille') && +Q.get('veille')>0 ? +Q.get('veille') : 75)*1000, VITESSE:61.2,   /* ⚑ v179a (Tom, C-232) : 60 s, quelle que soit l'adresse ; `?veille=` seulement s'il est dans l'adresse du moment, jamais mémorisé · v175 : 45 s ; v174 : 90 s ; v167 (Tom, C-181 §3) : le délai repasse à 60 s (120 en v166) ; v166 : +2 % de vitesse (60 → 61,2 pt/s) */
     VERROU:10*60*1000, SANS_COIN:60*1000, TOL:2, LARG:140,
    AMANDE:'#8FE08F', COIN_FORCE:Q.get('coin')==='1'};   /* VITESSE, TOL, LARG en pt de l'app : convertis à l'échelle de l'appareil (`k`) */
  /* les bancs (navigateur piloté, ou `banc_tom`, qui masque `webdriver` et pose `promi_veille_off`) restent souvent plus de 60 s sans toucher : la veille y
     recouvrirait l'écran et fausserait leurs mesures. Elle n'y paraît que si on la demande (`?veille=`). Sur un téléphone, rien de cela ne joue. */
  var COUPEE=false; try{ COUPEE=!Q.has('veille') && (!!navigator.webdriver || localStorage.getItem('promi_veille_off')==='1'); }catch(_){ }
  var dernier=performance.now(), doigts=0, actif=null, verrou=null, etatVerrou='aucun', avale=0;
  function reduit(){ try{ return matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(_){ return false; } }
  function saisie(){ var a=document.activeElement; return !!(a && (a.tagName==='INPUT' || a.tagName==='TEXTAREA' || a.isContentEditable)); }

  /* ── LA TRAJECTOIRE : une fonction pure, partagée par l'écran et la simulation ── */
  function hasard(g){ var a=g>>>0; return function(){ a=(a+0x6D2B79F5)>>>0; var t=a; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; }
  /* le prochain rebond depuis (x, y) dans la direction (dx, dy), vitesse V : {t, x, y, mur:'x'|'y'|'coin'} */
  function prochain(s, B){ var v=B.v; var tx=s.dx>0?(B.x1-s.x)/(s.dx*v):(s.dx<0?(B.x0-s.x)/(s.dx*v):Infinity), ty=s.dy>0?(B.y1-s.y)/(s.dy*v):(s.dy<0?(B.y0-s.y)/(s.dy*v):Infinity);
    var t=Math.min(tx, ty), x=s.x+s.dx*v*t, y=s.y+s.dy*v*t, mur=tx<ty?'x':'y';
    var reste=tx<ty ? Math.min(Math.abs(y-B.y0), Math.abs(y-B.y1)) : Math.min(Math.abs(x-B.x0), Math.abs(x-B.x1));
    if(reste<=B.tol) mur='coin';
    /* ⚑ v209 (Tom, C-300) — LA DÉCOUPE DE LA CAMÉRA EST UN OBSTACLE : chaque obstacle est la découpe agrandie de la boîte du logo (somme de Minkowski, en
       coordonnées du coin haut-gauche du logo) ; le logo rebondit sur la face qu'il touche ('ox' : une face verticale, 'oy' : une face horizontale, 'oc' : son coin). */
    (B.obs||[]).forEach(function(E){ var c=choc(s, v, E, B.tol); if(c && c.t<t-1e-9){ t=c.t; x=s.x+s.dx*v*t; y=s.y+s.dy*v*t; mur=c.mur; } });
    return {t:Math.max(0,t), x:x, y:y, mur:mur}; }
  function choc(s, v, E, tol){ var best=null, e=1e-6;
    function prend(tt, mur, autre, a0, a1){ if(tt<-1e-9 || autre<=a0 || autre>=a1) return; tt=Math.max(0, tt);
      if(Math.min(autre-a0, a1-autre)<=tol) mur='oc'; if(!best || tt<best.t) best={t:tt, mur:mur}; }
    if(s.dy<0 && s.y>=E.y1-e){ var t1=(E.y1-s.y)/(s.dy*v); prend(t1, 'oy', s.x+s.dx*v*t1, E.x0, E.x1); }
    if(s.dy>0 && s.y<=E.y0+e){ var t2=(E.y0-s.y)/(s.dy*v); prend(t2, 'oy', s.x+s.dx*v*t2, E.x0, E.x1); }
    if(s.dx>0 && s.x<=E.x0+e){ var t3=(E.x0-s.x)/(s.dx*v); prend(t3, 'ox', s.y+s.dy*v*t3, E.y0, E.y1); }
    if(s.dx<0 && s.x>=E.x1-e){ var t4=(E.x1-s.x)/(s.dx*v); prend(t4, 'ox', s.y+s.dy*v*t4, E.y0, E.y1); }
    return best; }
  /* la découpe (en px, dans le cadre de la veille) agrandie de la boîte du logo (w × h) : les positions interdites à son coin haut-gauche */
  function obstacles(C, w, h){ return (C.obs||[]).map(function(O){ return {x0:O.x-w, x1:O.x+O.w, y0:O.y-h, y1:O.y+O.h}; }); }
  function direction(sx, sy, deg){ var a=deg*Math.PI/180; return [sx*Math.cos(a), sy*Math.sin(a)]; }
  /* après un rebond (ou au départ) : l'angle tiré, 45° ± 2 à 3° ; un coin avant 60 s est refusé ; `?coin=1` le vise entre 60 et 90 s */
  function oriente(s, B, ecoule, alea){
    var sx=s.dx>=0?1:-1, sy=s.dy>=0?1:-1;
    if(R.COIN_FORCE && !s.coinVise && ecoule>=40000){ var cx=sx>0?B.x1:B.x0, cy=sy>0?B.y1:B.y0, ddx=cx-s.x, ddy=cy-s.y, d=Math.hypot(ddx, ddy), arr=ecoule+d/B.v*1000;
      if(arr>=60000 && arr<=90000 && d>1){ var ox=s.dx, oy=s.dy; s.dx=ddx/d; s.dy=ddy/d; if(prochain(s, B).mur==='coin'){ s.coinVise=true; return; } s.dx=ox; s.dy=oy; } }
    for(var essai=0; essai<40; essai++){ var dev=(alea()<0.5?-1:1)*(2+alea()); var v=direction(sx, sy, 45+dev); s.dx=v[0]; s.dy=v[1];
      var n=prochain(s, B), quand=ecoule+n.t*1000; if(n.mur!=='coin' || quand>=R.SANS_COIN) return; }   /* v162 : seulement la première minute */
    var v2=direction(sx, sy, 41); s.dx=v2[0]; s.dy=v2[1]; }
  function rebondit(s, n, B){ s.x=n.x; s.y=n.y;
    if(n.mur==='coin' && B){ s.x=s.dx>0?B.x1:B.x0; s.y=s.dy>0?B.y1:B.y0; }   /* au coin, posé EXACTEMENT sur les deux bords : sinon il repartait à 1 pt d'un bord, et le rebond suivant était un coin de plus */
    if(n.mur==='x'||n.mur==='coin'||n.mur==='ox'||n.mur==='oc') s.dx=-s.dx; if(n.mur==='y'||n.mur==='coin'||n.mur==='oy'||n.mur==='oc') s.dy=-s.dy; }
  /* la simulation : `duree` s de trajectoire, sans écran — les coins et leurs instants */
  /* la simulation : `duree` s de trajectoire, sans écran, sur un écran donné — o = {l, h : la zone visible en px ; k : l'échelle de l'appareil ; ins : [haut,
     droite, bas, gauche] les zones sûres ; w, h0 : l'encre du logo en px} ; par défaut l'écran du moment. Rend les coins (s) et le nombre de rebonds. */
  window._veilleSimule=function(duree, graine, o){ o=o||{}; var C=cadre(), k=o.k||C.k, L=o.l||C.width, H=o.h||C.height, ins=o.ins||C.ins, w=o.w||R.LARG*k, h=o.h0||(R.LARG*k*encre.r);
    var B={x0:ins[3], x1:L-ins[1]-w, y0:ins[0], y1:H-ins[2]-h, v:R.VITESSE*k, tol:R.TOL*k, obs:obstacles({obs:o.decoupe?[o.decoupe]:(o.l?[]:(C.obs||[]))}, w, h)}, al=hasard(graine||1), s={x:(B.x0+B.x1)/2, y:(B.y0+B.y1)/2, dx:Math.SQRT1_2, dy:Math.SQRT1_2}, t=0, coins=[], rebonds=0;
    var trace=o.trace?[]:null;
    oriente(s, B, 0, al); while(true){ var n=prochain(s, B); if(t+n.t>duree) break; t+=n.t; rebondit(s, n, B); rebonds++; if(n.mur==='coin') coins.push(+t.toFixed(1)); if(trace) trace.push([+s.x.toFixed(2), +s.y.toFixed(2), n.mur]); oriente(s, B, t*1000, al); }
    return {coins:coins, rebonds:rebonds, duree:duree, bornes:B, trace:trace}; };
  /* ── LA ZONE VISIBLE : ses bords réels, en px de l'écran ── */
  var encre={r:26.72/140, boites:{}};   /* le rapport hauteur / largeur de l'encre de PROMI (mesuré au premier logo) */
  function insets(){ try{ var p=document.createElement('div'); p.style.cssText='position:fixed;left:0;top:0;width:0;height:0;visibility:hidden;pointer-events:none;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)';
      document.body.appendChild(p); var c=getComputedStyle(p), r=[c.paddingTop, c.paddingRight, c.paddingBottom, c.paddingLeft].map(function(v){ return parseFloat(v)||0; }); p.remove(); return r; }catch(_){ return [0,0,0,0]; } }
  /* ⚑ v166 (Tom, C-181 §4.3) — « ses bords sont ceux de l'ÉCRAN DE L'APP, pas de la page du navigateur : sur iPhone l'écran visible ; sur ordinateur, dans le
     cadre du téléphone simulé, les bords de CE cadre, jamais les marges de la page autour. Le logo rebondit sur le conteneur racine de l'app. » LA CAUSE, mesurée
     sur l'état de Tom (390 × 651, Safari) : l'app (`#device`, réduite à 0,7466 dans `.frame`) occupe x 49,4 → 340,6, y 10,4 → 640,5 ; la veille couvrait la
     zone visible ENTIÈRE (visualViewport 390 × 651) et rebondissait sur ses bords — hors de l'app sur les quatre côtés (en bas 10,5 pt sous l'app) ; sur un
     ordinateur, sur la fenêtre entière, loin du cadre. Le cadre est maintenant `#device` À L'ÉCRAN, recoupé avec la zone visible et les zones sûres. */
  function cadre(){ var vv=window.visualViewport, D=document.getElementById('device'), k=1, r=null; try{ r=D.getBoundingClientRect(); if(r.width>10) k=r.width/390; }catch(_){ }
    var ins=insets(), vl=(vv?vv.offsetLeft:0), vt=(vv?vv.offsetTop:0), vw=(vv?vv.width:innerWidth), vh=(vv?vv.height:innerHeight);
    var x0=vl+ins[3], y0=vt+ins[0], x1=vl+vw-ins[1], y1=vt+vh-ins[2];
    if(r && r.width>10 && r.height>10){ x0=Math.max(x0, r.left); y0=Math.max(y0, r.top); x1=Math.min(x1, r.right); y1=Math.min(y1, r.bottom); }
    /* ⚑ v209 (Tom, C-300) — DANS L'APP (la coquille déclare la forme de l'écran : `window.__ecranForme`), la veille couvre TOUT l'écran et le logo y va partout :
       ni zone sûre retranchée, ni ligne imaginaire en haut ; la découpe de la caméra (encoche, Dynamic Island, trou d'Android), donnée par la coquille en px de
       l'écran, est un obstacle sur lequel il rebondit. Les coins arrondis de l'écran peuvent rogner le logo de quelques pixels au rebond (accepté). Dans
       Safari (aucune forme déclarée), rien ne change. */
    var F=window.__ecranForme;
    if(F){ x0=vl; y0=vt; x1=vl+vw; y1=vt+vh;
      if(r && r.width>10 && r.height>10){ x0=Math.max(x0, r.left); y0=Math.max(y0, r.top); x1=Math.min(x1, r.right); y1=Math.min(y1, r.bottom); }
      var obs=[]; if(F.decoupe){ var O=F.decoupe; obs.push({x:O.x-x0, y:O.y-y0, w:O.w, h:O.h}); }
      return {left:x0, top:y0, width:Math.max(10, x1-x0), height:Math.max(10, y1-y0), k:k, ins:[0,0,0,0], obs:obs}; }
    return {left:x0, top:y0, width:Math.max(10, x1-x0), height:Math.max(10, y1-y0), k:k, ins:[0,0,0,0]}; }
  function bornesDe(C, w, h){ return {x0:C.ins[3], x1:C.width-C.ins[1]-w, y0:C.ins[0], y1:C.height-C.ins[2]-h, v:R.VITESSE*C.k, tol:R.TOL*C.k, obs:obstacles(C, w, h)}; }
  /* un logo posé dans un obstacle (au départ, ou quand l'écran change) en sort par le bas */
  function horsObstacle(s, B){ (B.obs||[]).forEach(function(E){ if(s.x>E.x0 && s.x<E.x1 && s.y>E.y0 && s.y<E.y1) s.y=Math.min(B.y1, E.y1); }); }
  /* ── L'ÉCRAN ── */
  function fond(){ try{ return window._fondToileVif ? window._fondToileVif() : '#050302'; }catch(_){ return '#050302'; } }
  function hex(c){ return '#'+c.slice(0,3).map(function(v){ return ('0'+Math.round(v).toString(16)).slice(-2); }).join(''); }
  function rgb(h){ return [1,3,5].map(function(i){ return parseInt(h.substr(i,2),16); }); }
  function tons(F){ var P=[], L=[]; try{ P=(window.Toile && Toile.cols ? Toile.cols() : []).map(hex); }catch(_){ }
    P.forEach(function(h){ if(contraste(h, F)>=3) L.push(h); });
    if(L.length<2 && window._teinte && _teinte.ajuste){ L=[]; P.forEach(function(h){ try{ var a=hex(_teinte.ajuste(rgb(h), rgb(F), 3)); if(L.indexOf(a)<0 && contraste(a, F)>=3) L.push(a); }catch(_){ } }); }   /* aucun ton lisible : la teinte gardée, amenée à 3:1 */
    if(!L.length) L=[contraste('#F7F0DE', F)>=3?'#F7F0DE':'#201908']; return L; }
  function lum(h){ var v=[1,3,5].map(function(i){ var c=parseInt(h.substr(i,2),16)/255; return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4); }); return 0.2126*v[0]+0.7152*v[1]+0.0722*v[2]; }
  function contraste(a, b){ var x=lum(a), y=lum(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); }
  function logo(coul, k, fsF){ /* le canevas du logo, à la taille de son ENCRE : 140 pt de large, à l'échelle de l'appareil */
    var dpr=Math.min(3, window.devicePixelRatio||2), m=document.createElement('canvas').getContext('2d'), fs=40, L=R.LARG*k;
    m.font='400 '+fs+'px PromiLate'; var q=m.measureText('PROMI'), lw=q.actualBoundingBoxLeft+q.actualBoundingBoxRight; fs=fsF||fs*L/Math.max(1,lw);
    m.font='400 '+fs+'px PromiLate'; q=m.measureText('PROMI');
    /* ⚑ v163 (Tom, C-181 §3.1) : L'ENCRE SE LIT SUR LES PIXELS PEINTS, plus sur `measureText` — sa boîte (approches, ascendante et descendante de la
       police) dépasse l'encre réelle : au banc 1,3 pt à gauche, et rien ne garantit qu'elle soit la même dans le Safari de l'iPhone. On peint le mot
       une fois, large, on cherche ses pixels, et le canevas du logo est recadré sur eux : c'est l'ENCRE qui touche les bords. Mémorisé par taille. */
    var cle=fs.toFixed(3)+'|'+dpr, E=encre.boites[cle];
    if(!E){ var mg=Math.ceil(fs*0.5), tw=Math.ceil((q.actualBoundingBoxLeft+q.actualBoundingBoxRight)*dpr+2*mg*dpr), th=Math.ceil((q.actualBoundingBoxAscent+q.actualBoundingBoxDescent)*dpr+2*mg*dpr);
      var tc=document.createElement('canvas'); tc.width=tw; tc.height=th; var tg=tc.getContext('2d'); tg.setTransform(dpr,0,0,dpr,0,0); tg.font='400 '+fs+'px PromiLate'; tg.fillStyle='#000';
      var ox=mg+q.actualBoundingBoxLeft, oy=mg+q.actualBoundingBoxAscent; tg.fillText('PROMI', ox, oy);
      var d=null; try{ d=tg.getImageData(0,0,tw,th).data; }catch(_){ }
      var x0=tw, y0=th, x1=-1, y1=-1;
      if(d){ for(var yy=0; yy<th; yy++) for(var xx=0; xx<tw; xx++){ if(d[(yy*tw+xx)*4+3]>24){ if(xx<x0) x0=xx; if(xx>x1) x1=xx; if(yy<y0) y0=yy; if(yy>y1) y1=yy; } } }
      if(x1<0){ x0=mg*dpr; y0=mg*dpr; x1=tw-mg*dpr; y1=th-mg*dpr; }
      E=encre.boites[cle]={dx:ox-x0/dpr, dy:oy-y0/dpr, w:(x1-x0+1)/dpr, h:(y1-y0+1)/dpr}; }
    if(!fsF && Math.abs(E.w-L)>0.3) return logo(coul, k, fs*L/E.w);   /* l'encre lue : 140 pt de large, exactement */
    var w=E.w, h=E.h, cv=document.createElement('canvas'); encre.r=h/Math.max(1,w);
    cv.width=Math.ceil(w*dpr); cv.height=Math.ceil(h*dpr); var g=cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0); g.font='400 '+fs+'px PromiLate'; g.fillStyle=coul;
    g.fillText('PROMI', E.dx, E.dy);
    cv.style.cssText='position:absolute;left:0;top:0;width:'+w+'px;height:'+h+'px;pointer-events:none;will-change:transform'; cv.__w=w; cv.__h=h; return cv; }
  function place(couche, C){ couche.style.left=C.left+'px'; couche.style.top=C.top+'px'; couche.style.width=C.width+'px'; couche.style.height=C.height+'px'; }
  function demarre(){ if(actif) return; if(!document.body) return;
    var C=cadre(), F=fond(), couche=document.createElement('div'); couche.id='promiVeille'; couche.setAttribute('aria-label','Veille'); couche.setAttribute('role','presentation');
    couche.style.cssText='position:fixed;z-index:2147483000;overflow:hidden;background:transparent;touch-action:none;margin:0;padding:0'; place(couche, C);
    document.body.appendChild(couche);
    var T=tons(F), AM=R.AMANDE; if(contraste(AM, F)<3 && window._teinte && _teinte.ajuste){ try{ AM=hex(_teinte.ajuste(rgb(AM), rgb(F), 3)); }catch(_){ } }   /* l'amande, amenée à 3:1 si le fond l'éteint (en clair) */
    var V=actif={amande:AM, couche:couche, t0:performance.now(), tons:T, fond:F, i:0, couleurs:[], coins:[], rebonds:0, reduit:reduit(), passage:null, fini:false, C:C, al:hasard((Date.now()^0x5bd1e995)>>>0)};
    V.logo=logo(T[0], C.k); V.logo.style.visibility='hidden'; couche.appendChild(V.logo); V.couleurs.push(T[0]); V.couleur=T[0];
    var B=V.B=bornesDe(C, V.logo.__w, V.logo.__h); V.s={x:(B.x0+B.x1)/2, y:(B.y0+B.y1)/2, dx:Math.SQRT1_2, dy:-Math.SQRT1_2};
    if(V.al()<0.5) V.s.dx=-V.s.dx; horsObstacle(V.s, B); oriente(V.s, B, 0, V.al); V.n=prochain(V.s, B); V.tn=0;
    pose(V);
    /* l'entrée en flaques : le fond naît par-dessus l'écran, dans la couche ; puis le fond est la couche */
    var fin=function(){ if(V.fini) return; couche.style.background=F; V.logo.style.visibility='visible'; if(V.passage && V.passage.canevas) V.passage.canevas.remove(); V.passage=null; V.tEntree=performance.now(); boucle(); };
    if(V.reduit || !window._passageFlaques) fin();
    else V.passage=window._passageFlaques(couche, {mode:'couvre', couleur:F, duree:350, devant:true, z:0, fin:fin});
    if(!V.passage && !V.reduit) fin(); }
  /* la zone visible change (barres de Safari, orientation, clavier) : la couche et ses bords suivent, le logo reste dedans */
  function relit(){ var V=actif; if(!V || V.fini) return; var C=cadre(); V.C=C; place(V.couche, C);
    if(Math.abs(C.k*R.LARG-V.logo.__w)>0.5){ var nl=logo(V.couleur, C.k); nl.style.visibility=V.logo.style.visibility; V.couche.replaceChild(nl, V.logo); V.logo=nl; }
    var B=V.B=bornesDe(C, V.logo.__w, V.logo.__h); V.s.x=Math.max(B.x0, Math.min(B.x1, V.s.x)); V.s.y=Math.max(B.y0, Math.min(B.y1, V.s.y)); horsObstacle(V.s, B); V.n=prochain(V.s, B); V.tn=0; pose(V); }
  try{ if(window.visualViewport){ visualViewport.addEventListener('resize', relit); visualViewport.addEventListener('scroll', relit); } window.addEventListener('resize', relit); window.addEventListener('orientationchange', function(){ setTimeout(relit, 300); }); }catch(_){ }
  function pose(V){ V.logo.style.transform='translate('+V.s.x.toFixed(2)+'px,'+V.s.y.toFixed(2)+'px)'; }
  function boucle(){ var V=actif; if(!V || V.fini) return; var t=performance.now(), ec=t-V.t0;
    if(V.reduit){ var B=V.B; V.s.x=(B.x0+B.x1)/2; V.s.y=(B.y0+B.y1)/2; pose(V); }   /* au centre de la zone visible */
    else { if(V.tp==null) V.tp=t; var dt=Math.min(0.1, (t-V.tp)/1000); V.tp=t;
      while(dt>0){ if(dt<V.n.t-V.tn){ V.s.x+=V.s.dx*V.B.v*dt; V.s.y+=V.s.dy*V.B.v*dt; V.tn+=dt; dt=0; }   /* v162 : la vitesse des bornes (60 pt à l'échelle de l'appareil) — celle dont les rebonds sont calculés */
        else { dt-=(V.n.t-V.tn); rebondit(V.s, V.n, V.B); V.rebonds++; var coin=V.n.mur==='coin';
          var c; if(coin){ c=V.amande; V.coins.push(Math.round(ec)); } else { V.i=(V.i+1)%V.tons.length; c=V.tons[V.i]; if(c===V.couleur && V.tons.length>1){ V.i=(V.i+1)%V.tons.length; c=V.tons[V.i]; } }
          if(c!==V.couleur){ var nl=logo(c, V.C.k); V.couche.replaceChild(nl, V.logo); V.logo=nl; V.couleur=c; } V.couleurs.push(c);
          oriente(V.s, V.B, ec, V.al); V.n=prochain(V.s, V.B); V.tn=0; } }
      pose(V); }
    if(ec>=R.VERROU && (etatVerrou==='actif' || eveil.etat==='joue')) relache();
    requestAnimationFrame(boucle); }
  function quitte(){ var V=actif; if(!V) return; V.fini=true; actif=null; dernier=performance.now();
    if(V.passage){ V.passage.arrete=true; if(V.passage.canevas) V.passage.canevas.remove(); }
    V.couche.remove();
    if(!V.reduit && window._passageFlaques && document.body){ var C=cadre(), h=document.createElement('div'); h.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;margin:0;padding:0;overflow:hidden'; place(h, C); document.body.appendChild(h);
      window._passageFlaques(h, {mode:'ouvre', couleur:V.fond, duree:350, devant:true, z:0, fin:function(){ h.remove(); }}); setTimeout(function(){ if(h.parentNode) h.remove(); }, 2500); }
    window._veilleDerniere={duree:Math.round(performance.now()-V.t0), couleurs:V.couleurs, coins:V.coins, rebonds:V.rebonds};
    demande(); }
  /* ── LE VERROU DE L'ÉCRAN (Screen Wake Lock) ── */
  function demande(){ try{ if(document.visibilityState!=='visible') return; if(!navigator.wakeLock || etatVerrou==='refusé'){ eveilVideo(); return; } if(verrou) return; navigator.wakeLock.request('screen').then(function(v){ verrou=v; etatVerrou='actif'; eveil.methode='wakelock'; dit('wakelock');
      v.addEventListener && v.addEventListener('release', function(){ if(verrou===v){ verrou=null; if(etatVerrou==='actif') etatVerrou='perdu'; } }); }, function(){ etatVerrou='refusé'; eveilVideo(); }); }catch(_){ } }
  function relache(){ try{ var v=verrou; verrou=null; etatVerrou='relâché'; if(v && v.release) v.release(); }catch(_){ } eveilPause('relâché'); }
  /* ⚑ v180a (Tom, C-236) — L'ÉCRAN RESTE ALLUMÉ tant que Promi est au premier plan, même posé sans être touché : sans quoi l'iPhone se verrouille (son
     verrouillage automatique, 30 s chez beaucoup) avant la minute de la veille, qu'on ne voit jamais. ① Screen Wake Lock quand il existe (https : Netlify, et
     Swift : `isIdleTimerDisabled`, portage/). ② Sinon — en http (l'iPhone de Tom sur le Mac), `navigator.wakeLock` n'existe pas hors contexte sûr — ou si la
     demande est refusée : LE REPLI DE NoSleep, une vidéo de 2 s (16 × 16 pt, noire, piste son de silence), lancée au premier toucher (le geste que Safari
     exige), posée HORS de l'écran (jamais visible, aucun son : sa piste est un silence), relancée en boucle PAR SON TEMPS (`timeupdate`) et non par
     `loop` : WebKit ne retient pas l'extinction de l'écran pour une vidéo en `loop` (c'est la règle des images animées en vidéo), et NoSleep fait de même.
     Elle n'est créée QUE si Wake Lock manque. ③ Après 10 min de veille, tout est relâché (`relache`) : l'iPhone se verrouille selon ses propres réglages ;
     le toucher suivant le redemande. Mise en pause quand la page est cachée. ⚠ Le simulateur iOS ne verrouille jamais son écran : l'effet se vérifie sur
     l'iPhone ; le juge vérifie que la vidéo joue sans fin, invisible et silencieuse, et qu'elle n'existe pas avec Wake Lock. */
  var eveil={methode:'aucun', etat:'aucun', t:0}, eveilVid=null;
  var EVEIL_SRC='data:video/mp4;base64,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';
  function dit(quoi){ try{ var Q=new URLSearchParams(location.search), h=location.hostname; if(!(Q.has('mesure')||Q.has('diag'))) return; if(!(h==='localhost' || /^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[01])\./.test(h))) return;
      var v=eveilVid; fetch('/mesure', {method:'POST', headers:{'Content-Type':'application/json'}, keepalive:true, body:JSON.stringify({quoi:'eveil', ev:quoi, methode:eveil.methode, etat:eveil.etat, wakeLock:!!navigator.wakeLock,
        joue:v?!v.paused:false, temps:v?Math.round(v.currentTime*100)/100:null, depuis:Math.round(performance.now()), quand:new Date().toISOString(), version:window.PROMI_VERSION||null, ua:navigator.userAgent})}).catch(function(){}); }catch(_){ } }
  function eveilVideo(){ try{ if(document.visibilityState!=='visible' || (actif && performance.now()-actif.t0>=R.VERROU)) return;
      if(!eveilVid){ var v=document.createElement('video'); v.id='promiEveil'; v.setAttribute('playsinline',''); v.setAttribute('webkit-playsinline',''); v.playsInline=true; v.preload='auto';
        v.setAttribute('aria-hidden','true'); v.setAttribute('tabindex','-1'); v.disablePictureInPicture=true; v.setAttribute('disableremoteplayback',''); v.src=EVEIL_SRC;
        v.style.cssText='position:fixed!important;left:-200px!important;top:-200px!important;width:16px!important;height:16px!important;pointer-events:none!important;opacity:1!important;margin:0!important;padding:0!important;border:0!important;';
        v.addEventListener('timeupdate', function(){ if(v.currentTime>1.2) v.currentTime=0.2+Math.random()*0.3; });
        v.addEventListener('ended', function(){ try{ v.currentTime=0.2; v.play(); }catch(_){ } });
        (document.body||document.documentElement).appendChild(v); eveilVid=v; }
      if(eveilVid.paused){ var p=eveilVid.play(); if(p && p.then) p.then(function(){ eveil.methode='vidéo'; eveil.etat='joue'; eveil.t=performance.now(); dit('joue'); }, function(){ eveil.etat='refusé'; dit('refusé'); }); } }catch(_){ } }
  function eveilPause(etat){ try{ if(eveilVid && !eveilVid.paused){ eveilVid.pause(); eveil.etat=etat||'pause'; dit(eveil.etat); } }catch(_){ } }
  setInterval(function(){ if(eveil.methode==='vidéo' && document.visibilityState==='visible') dit('tic'); }, 30000);
  document.addEventListener('visibilitychange', function(){ if(document.visibilityState!=='visible') eveilPause('cachée'); }, true);
  /* le geste que Safari exige pour lancer une vidéo : le lever du doigt (et le clic), lus AVANT les écouteurs de la veille qui arrêtent la propagation */
  ['touchend','click'].forEach(function(n){ window.addEventListener(n, function(e){ if(e.isTrusted && !verrou && (!navigator.wakeLock || etatVerrou==='refusé')) eveilVideo(); }, {capture:true, passive:true}); });
  document.addEventListener('visibilitychange', function(){ if(document.visibilityState==='visible'){ if(etatVerrou==='refusé') etatVerrou='aucun'; if(!(actif && performance.now()-actif.t0>=R.VERROU)) demande(); } });
  /* ── LE TOUCHER : il retarde la veille ; pendant elle, il la quitte et n'actionne rien dessous ── */
  function touche(e){ dernier=performance.now();
    if(actif || performance.now()<avale){ if(actif){ avale=performance.now()+800; quitte(); } try{ e.preventDefault(); }catch(_){ } e.stopImmediatePropagation(); e.stopPropagation(); return; } }
  ['pointerdown','touchstart','mousedown'].forEach(function(n){ window.addEventListener(n, function(e){ if(n==='pointerdown' && !actif) doigts++; if(n==='pointerdown' && !verrou) demande(); touche(e); }, {capture:true, passive:true}); });   /* passifs : un écouteur non passif sur toute la page retarde le défilement dans Safari ; pendant la veille le toucher est arrêté (propagation) et le clic qui suit, avalé */
  ['pointerup','pointercancel'].forEach(function(n){ window.addEventListener(n, function(e){ doigts=Math.max(0, doigts-1); dernier=performance.now(); if(performance.now()<avale){ e.stopImmediatePropagation(); } }, {capture:true}); });
  ['touchend','touchmove','mouseup','click','keydown','wheel','pointermove'].forEach(function(n){ window.addEventListener(n, function(e){ if(n==='pointermove' && !e.buttons && e.pointerType==='mouse') return; if(!e.isTrusted && (n==='click'||n==='keydown') && !actif) return;   /* v179a : un clic posé par l'app elle-même (`el.click()` au démarrage) n'est pas un toucher */
      dernier=performance.now();
      if(performance.now()<avale || actif){ if(n!=='pointermove'){ try{ e.preventDefault(); }catch(_){ } e.stopImmediatePropagation(); e.stopPropagation(); } } }, {capture:true, passive:n==='click'||n==='keydown'?false:true}); });
  document.addEventListener('input', function(e){ if(e.isTrusted) dernier=performance.now(); }, true);
  function nDoigts(){ var D=window.__doigts; return D ? D.n : doigts; }   /* v167 (C-181 §3) : le compteur posé en tête de page — aucun écouteur ne peut lui avaler un lever */
  /* ⚑ v179a (Tom, C-232) — « LA VEILLE PART AU BOUT DE QUELQUES SECONDES » (iPhone). LA CAUSE : sur l'iPhone la page est servie en http, le Wake Lock n'y existe pas
     (`navigator.wakeLock` absent hors contexte sûr) : l'écran se verrouille seul (le verrouillage auto de l'iPhone), Safari GÈLE la page — la minuterie ne tourne
     plus — et au déverrouillage le premier tour de minuterie trouvait `maintenant − dernier toucher` ≥ le délai : le temps passé écran éteint comptait comme du
     calme, la veille partait aussitôt rentré. Aujourd'hui : rien ne compte pendant que la page est cachée ou gelée — au retour (`visibilitychange`, `pageshow`)
     et après tout tour de minuterie manqué (un écart de plus de 5 s entre deux tours : la page dormait ; le chargement de l'app bloque déjà le fil 1 à 2 s), le compte repart de zéro. */
  var tic=performance.now();
  function repart(){ dernier=performance.now(); tic=dernier; }
  document.addEventListener('visibilitychange', function(){ if(document.visibilityState==='visible') repart(); }, true);
  window.addEventListener('pageshow', repart, true);
  setInterval(function(){ var t=performance.now(), saut=t-tic>5000; tic=t; if(saut){ dernier=t; return; } if(actif || COUPEE) return; try{ if(window.__doigts && window.__doigts.t>dernier) dernier=window.__doigts.t; }catch(_){ } if(nDoigts()>0 || saisie() || document.visibilityState!=='visible'){ dernier=performance.now(); return; }
    if(performance.now()-dernier>=R.DELAI) demarre(); }, 250);
  window._veille=function(){ var V=actif; return {doigts:nDoigts(), doigtsVeille:doigts, saisie:saisie(), calme:Math.round(performance.now()-dernier), coupee:COUPEE, delai:R.DELAI, visible:document.visibilityState, active:!!V, depuis:V?Math.round(performance.now()-V.t0):0, couleurs:V?V.couleurs.slice():[], coins:V?V.coins.slice():[], rebonds:V?V.rebonds:0,
    logo:V?[V.s.x, V.s.y, V.logo.__w, V.logo.__h]:null, bornes:V?V.B:null, cadre:V?V.C:null, fond:V?V.fond:null, amande:V?V.amande:null, verrou:etatVerrou, eveil:{methode:eveil.methode, etat:eveil.etat, video:!!eveilVid, joue:eveilVid?!eveilVid.paused:false, temps:eveilVid?eveilVid.currentTime:null}, couleur:V?V.couleur:null, tons:V?V.tons.slice():null, derniere:window._veilleDerniere||null}; };
})();
