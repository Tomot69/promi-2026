/* ⚑ v144 (Tom, 12 oct. 2026, C-094) — LE GUIDE D'ACCUEIL. (L'écriture de v143 : sauvegardes/app-avant-v144.html.)
   Ce que Tom a décidé sur iPhone :
   · LE STUDIO À SA TAILLE NORMALE (plus d'agrandissement de l'icône ni du mot) ; le + garde ses + 10 % ;
   · « PLUS TARD » EST RETIRÉ, du guide comme de l'onboarding : « le parcours est court, on ne le passe pas » (exception nommée de R6) ;
     toucher ailleurs fait toujours AVANCER le guide (du Studio au + ; au +, il se retire) ;
   · LA SUITE NATURELLE DE L'ONBOARDING : l'accueil posé, le flou commence 0,6 s plus tard, D'UN SEUL MOUVEMENT À VITESSE RÉGULIÈRE — les six
     formes partent ENSEMBLE et grandissent ensemble, courbe douce, 1,8 s (v143 : départs décalés de 0 à 0,25 s et courbe marquée — « vite et
     lent à la fois ») ; elles RESTENT ensuite (v143 les remplaçait par une couche unique : le flou « sautait » à cet instant) ;
   · DU STUDIO AU +, PAS DE SAUT : la zone nette est une LOUPE — une fenêtre ronde à bord doux qui montre la barre nette (une copie de ses
     cinq entrées, posée au-dessus du flou). Elle quitte le Studio et GLISSE vers le + en 1,2 s ; les six formes se réorganisent autour (elles
     se déplacent et tournent, par `transform`) ; puis la phrase du + paraît. Si l'on a touché le Studio, le flou reste posé SOUS le Studio
     ouvert : au retour sur l'accueil la loupe glisse de même — le flou ne repart pas de zéro.
   LA TECHNIQUE (dictée par Tom en v143, gardée) : on n'anime jamais le rayon du flou ni sa découpe ; les formes portent le flou des murs
   (4,8 px, constant) et ne changent que par `transform`. La loupe et son contenu ne changent que par `transform` eux aussi (un par image,
   écrit par la page : deux nœuds, aucun recalcul de mise en page).
   ⚑ EXCEPTIONS NOMMÉES : A2 — les six formes, et elles seules, portent une transition CSS sur `transform` ; A3 — la phrase du Studio est un
   impératif voulu par Tom. Aucune opacité, aucun fondu. Tout nœud porte `data-eng`. */
(function(){
  var T=window.TEXTES_ENGAGEMENT=window.TEXTES_ENGAGEMENT||{};
  /* TEXTE — Tom (lot v143) */
  T.guide={ studio:'Choisis d’abord le monde qui te ressemble, au Studio.',
            plus:'Promi, Chiche ou Cercle : tout commence par ce +.' };
  T.imperatifVoulu=(T.imperatifVoulu||[]).concat([T.guide.studio]);   /* A3 : l'exception nommée, lue par redteam_engagement et redteam_guide */
  T.sansPlusTard=true;                                                  /* R6 : l'exception nommée (Tom, v144) — ni le guide ni l'onboarding n'ont de « Plus tard » */
  function $(i){ return document.getElementById(i); }
  var dev=$('device'); if(!dev) return;
  var CLE='promi_guide', ATTENTE=600, INSTALLE=1800, PHRASE_A=1300, GLISSE=1200, RETOUR=450, DISSOUT=360, TACHES=6, GROS={studio:1, plus:1.10}, FLOU=4.8,
      LOUPE_R=52, LOUPE_A={studio:0.72, plus:1}, BZ=[0.33,0.12,0.67,0.88], COURBE='cubic-bezier('+BZ.join(',')+')';   /* une courbe douce, presque régulière : ni arrêt ni accélération marquée */
  var LS={g:function(k){ try{ return localStorage.getItem(k); }catch(_){ return null; } }, s:function(k,v){ try{ localStorage.setItem(k,v); }catch(_){ } }};
  function reduit(){ try{ return !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }catch(_){ return false; } }
  function onbOuvert(){ var o=$('promiOnb'); return !!($('onbV') || (o && !o.classList.contains('gone') && getComputedStyle(o).display!=='none')); }
  function accueil(){ try{ if(onbOuvert()) return false; var r=dev.getBoundingClientRect(), E=document.elementsFromPoint(r.left+r.width/2, r.top+r.height*0.45);
      for(var i=0;i<E.length;i++){ var h=E[i]; if(h.closest && h.closest('#guide')) continue; return !(h.closest && h.closest('.screen, .sheet, .poster, #feedView, #entierVue, #dessinMode, #accRappelCompte')); } return false; }catch(_){ return false; } }
  /* l'accueil est POSÉ : la Toile ne tourne plus, aucune parole n'arrive ni ne part, aucun doigt à l'instant */
  var tDoigt=0, doigt=0; ['pointerdown','touchstart','touchmove','touchend','pointerup','wheel','keydown'].forEach(function(n){ document.addEventListener(n,function(e){ tDoigt=performance.now(); if(n==='touchstart'||n==='pointerdown') doigt=1; if(n==='touchend'||n==='pointerup') doigt=0; },{capture:true,passive:true}); });
  function calme(){ try{ var st=window.Toile_state&&window.Toile_state(); if(st&&st.running) return false; }catch(_){ }
    if(window._tirageActive || doigt) return false; return performance.now()-tDoigt>250; }
  var etat=null, attente=null, tAcc=0, trou=null, tVu=0, vuStudio=false, tPose=0, figeMs=null, anim=0, C=null, ou='studio';
  function k(){ return (dev.getBoundingClientRect().width/390)||1; }
  function eng(n, quoi){ n.setAttribute('data-eng', quoi); return n; }
  /* la même courbe que la transition CSS des formes (une cubique de Bézier, résolue par dichotomie) */
  function douce(v){ if(v<=0) return 0; if(v>=1) return 1; var a=0, b=1, t=v, i, x; for(i=0;i<22;i++){ t=(a+b)/2; x=3*(1-t)*(1-t)*t*BZ[0]+3*(1-t)*t*t*BZ[2]+t*t*t; if(x<v) a=t; else b=t; } return 3*(1-t)*(1-t)*t*BZ[1]+3*(1-t)*t*t*BZ[3]+t*t*t; }
  /* les six formes : une grille 2 × 3 bousculée ; chacune est une ellipse à bord doux, tournée, assez grande pour que leurs cœurs pleins se
     rejoignent et couvrent l'écran ; elles partent ensemble et finissent ensemble */
  function formes(){ var sd=((Date.now()&0x7fffffff)|1), R=function(){ sd=(Math.imul(sd,1103515245)+12345)&0x7fffffff; return sd/0x7fffffff; }, L=[];
    for(var n=0;n<TACHES;n++){ var gx=n%2, gy=(n/2)|0;
      L.push({x:98+gx*194+(R()-0.5)*70, y:140+gy*282+(R()-0.5)*90, w:640+R()*110, h:640+R()*110, rot:(R()*180)|0,
              gx:(R()-0.5)*56, gy:(R()-0.5)*56, grot:((R()-0.5)*70)|0, gs:1+R()*0.10}); }   /* gx… : où chaque forme va quand elles se réorganisent (du Studio au +) */
    return L; }
  function tr(f, s, u){ u=u||0; return 'translate(-50%,-50%) translate('+(f.gx*u).toFixed(2)+'px,'+(f.gy*u).toFixed(2)+'px) rotate('+(f.rot+f.grot*u).toFixed(2)+'deg) scale('+(s*(1+(f.gs-1)*u)).toFixed(4)+')'; }
  function poseFormes(g, Z, depart){ var L=[];
    Z.forEach(function(f){ var n=eng(document.createElement('div'),'guide-tache'); n.className='gd-t'; n.setAttribute('aria-hidden','true');
      n.style.cssText='left:'+f.x.toFixed(1)+'px;top:'+f.y.toFixed(1)+'px;width:'+f.w.toFixed(0)+'px;height:'+f.h.toFixed(0)+'px;transform:'+tr(f,depart,0);
      g.insertBefore(n, g.firstChild); L.push(n); });
    return L; }
  /* la copie nette d'une entrée : l'élément et ses descendants, avec leur style CALCULÉ (les règles de la barre ne l'atteignent pas hors
     d'elle), et ses deux pseudo-éléments (l'anneau et le disque du +) rendus par de vrais nœuds */
  var PROPS=['display','flex-direction','align-items','justify-content','place-items','align-content','justify-items','gap','width','height','box-sizing','color','background-color','background-image','background-size','background-position','background-repeat','border-radius','border-top','border-right','border-bottom','border-left','font-family','font-weight','font-size','line-height','letter-spacing','text-transform','white-space','fill','stroke','stroke-width','box-shadow','outline','outline-offset'];
  function style(src, dst, pseudo){ var cs=getComputedStyle(src, pseudo||null); PROPS.forEach(function(p){ try{ dst.style.setProperty(p, cs.getPropertyValue(p)); }catch(_){ } });
    dst.style.setProperty('-webkit-text-fill-color', cs.getPropertyValue('color')); dst.style.margin='0'; dst.style.padding=cs.getPropertyValue('padding'); dst.style.maxWidth='none'; }
  function pseudo(src, hote, quel){ var cs=getComputedStyle(src, quel), c=cs.getPropertyValue('content'); if(!c || c==='none' || c==='normal') return;
    var n=document.createElement('div'); style(src, n, quel); n.style.position='absolute';
    ['left','top','right','bottom','z-index','transform'].forEach(function(p){ n.style.setProperty(p, cs.getPropertyValue(p)); });
    n.style.pointerEvents='none'; hote.appendChild(n); }
  function copie(src){ var n=src.cloneNode(false); n.removeAttribute('id'); n.removeAttribute('class'); style(src, n);
    if(src.namespaceURI!=='http://www.w3.org/2000/svg'){ pseudo(src, n, '::before'); }
    for(var c=src.firstChild;c;c=c.nextSibling){ if(c.nodeType===3) n.appendChild(document.createTextNode(c.nodeValue));
      else if(c.nodeType===1){ if(c.namespaceURI==='http://www.w3.org/2000/svg'){ var s=c.cloneNode(true); s.removeAttribute('id'); var q=getComputedStyle(c); s.style.width=q.width; s.style.height=q.height; s.style.color=q.color; s.style.flex='none';
          /* le tracé garde ce que la feuille lui donne (le trait du +, son épaisseur) : hors de la barre, ses règles ne l'atteignent plus */
          var A=c.querySelectorAll('*'), B2=s.querySelectorAll('*'); for(var z=0;z<A.length && z<B2.length;z++){ var qa=getComputedStyle(A[z]); B2[z].style.stroke=qa.stroke; B2[z].style.strokeWidth=qa.strokeWidth; B2[z].style.fill=qa.fill; } s.style.position=q.position==='absolute'?'absolute':'relative'; s.style.zIndex='2'; n.appendChild(s); }
        else if(getComputedStyle(c).display!=='none' && c.id!=='filDot'){ var e=copie(c); e.style.position='relative'; e.style.zIndex='2'; n.appendChild(e); } } }
    if(src.namespaceURI!=='http://www.w3.org/2000/svg'){ pseudo(src, n, '::after'); }
    return n; }
  function boite(e){ var D=dev.getBoundingClientRect(), kk=k(), r=e.getBoundingClientRect(); return {x:(r.left-D.left)/kk, y:(r.top-D.top)/kk, w:r.width/kk, h:r.height/kk}; }
  function centreVu(cible){ var D=dev.getBoundingClientRect(), kk=k(), x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
    [].forEach.call(cible.querySelectorAll('svg, .l'), function(e){ var q=e.getBoundingClientRect(); if(q.width<2) return; x0=Math.min(x0,(q.left-D.left)/kk); x1=Math.max(x1,(q.right-D.left)/kk); y0=Math.min(y0,(q.top-D.top)/kk); y1=Math.max(y1,(q.bottom-D.top)/kk); });
    if(!(x1>x0)){ var b=boite(cible); return {x:b.x+b.w/2, y:b.y+b.h/2, w:b.w, h:b.h}; } return {x:(x0+x1)/2, y:(y0+y1)/2, w:x1-x0, h:y1-y0}; }
  /* LA LOUPE : une fenêtre ronde à bord doux (`#guideLoupe`), et dedans la barre nette (`#guideLoupeIn` : le fond de la barre et ses cinq
     entrées, copiés à leur place, en cotes de l'appareil). La fenêtre se déplace et grandit ; son contenu compense EXACTEMENT, pour rester à
     sa place à l'écran, et grossit autour du + (de 1 à 1,10). */
  function poseLoupe(g){ var st=$('studioBtn'), pl=$('createBtn'); if(!st || !pl) return null; var bs=centreVu(st), bp=boite(pl); if(bp.w<8 || bs.w<2) return null;
    var cs={x:bs.x, y:bs.y}, cp={x:bp.x+bp.w/2, y:bp.y+bp.h/2};
    var lo=eng(document.createElement('div'),'guide-net'); lo.id='guideLoupe'; lo.setAttribute('aria-hidden','true');
    lo.style.cssText='left:'+(cs.x-LOUPE_R).toFixed(2)+'px;top:'+(cs.y-LOUPE_R).toFixed(2)+'px;width:'+(2*LOUPE_R)+'px;height:'+(2*LOUPE_R)+'px';
    /* le contenu n'est pas grand comme l'appareil : une bande autour de la barre (un calque de 390 × 844 à la densité 3 coûtait une image de 130 ms à sa première peinture) */
    var oy=Math.max(0, Math.min(cs.y, cp.y)-90), ih=Math.min(844-oy, 180);
    var inn=eng(document.createElement('div'),'guide-net'); inn.id='guideLoupeIn';
    inn.style.cssText='left:'+(-(cs.x-LOUPE_R)).toFixed(2)+'px;top:'+(oy-(cs.y-LOUPE_R)).toFixed(2)+'px;height:'+ih.toFixed(0)+'px;transform-origin:'+cp.x.toFixed(2)+'px '+(cp.y-oy).toFixed(2)+'px';
    var fond=$('accBarreFond')||document.querySelector('#device .acc-barre');
    if(fond){ var bf=boite(fond), f=document.createElement('div'); style(fond, f); f.style.position='absolute'; f.style.left=bf.x.toFixed(2)+'px'; f.style.top=(bf.y-oy).toFixed(2)+'px'; f.style.width=bf.w.toFixed(2)+'px'; f.style.height=bf.h.toFixed(2)+'px'; inn.appendChild(f); }
    ['studioBtn','souffleBtn','createBtn','indexBtn','filBtn'].forEach(function(id){ var e=$(id); if(!e) return; var b=boite(e); if(b.w<4) return; var n=copie(e);
      n.style.position='absolute'; n.style.left=b.x.toFixed(2)+'px'; n.style.top=(b.y-oy).toFixed(2)+'px'; n.style.width=b.w.toFixed(2)+'px'; n.style.height=b.h.toFixed(2)+'px'; n.style.overflow='visible'; n.style.pointerEvents='none'; n.setAttribute('data-copie', id); inn.appendChild(n); });
    [].forEach.call(inn.querySelectorAll('*'), function(e){ eng(e,'guide-net'); });
    lo.appendChild(inn); g.appendChild(lo);
    return {lo:lo, inn:inn, cs:cs, cp:cp, bs:bs, bp:bp}; }
  /* la loupe à l'avancée u (0 : sur le Studio, 1 : sur le +) — les formules sont exactes : le contenu ne dérive pas */
  function loupeA(u){ if(!C) return; var a=LOUPE_A.studio+(LOUPE_A.plus-LOUPE_A.studio)*u, G=1+(GROS.plus-1)*u, dx=(C.cp.x-C.cs.x), dy=(C.cp.y-C.cs.y);
    var tx=dx*u, ty=dy*u, b=G/a, ex=dx-dx*(1-u)/a, ey=dy-dy*(1-u)/a;
    C.lo.style.transform='translate('+tx.toFixed(3)+'px,'+ty.toFixed(3)+'px) scale('+a.toFixed(5)+')';
    C.inn.style.transform='translate('+(-ex).toFixed(3)+'px,'+(-ey).toFixed(3)+'px) scale('+b.toFixed(5)+')';
    C.u=u; }
  /* l'entrée d'origine que la loupe recouvre est cachée (sa copie nette est dessus : sans cela son image floutée ferait un halo autour) */
  var cache=null;
  function montreOriginal(){ if(!cache) return; try{ cache.n.style.removeProperty('visibility'); if(cache.av) cache.n.style.setProperty('visibility', cache.av, cache.pr); }catch(_){ } cache=null; }
  function cacheOriginal(quoi){ var cible=$(quoi==='studio'?'studioBtn':'createBtn'); if(cache && cache.n===cible) return; montreOriginal(); if(!cible) return;
    try{ cache={n:cible, av:cible.style.getPropertyValue('visibility'), pr:cible.style.getPropertyPriority('visibility')}; cible.style.setProperty('visibility','hidden','important'); }catch(_){ } }
  function retire(){ cancelAnimationFrame(anim); anim=0; montreOriginal(); var g=$('guide'); if(g){ clearTimeout(g.__tp); clearTimeout(g.__tf); g.remove(); } dev.classList.remove('guide-studio'); dev.classList.remove('guide-plus'); trou=null; C=null; }
  /* la phrase et la cible d'une étape */
  function zone(quoi){ if(!C) return null; if(quoi==='studio') return {x:C.cs.x, y:C.cs.y, w:C.bs.w+12, h:C.bs.h+12, r:14, l:C.bs.w};
    var d=Math.max(C.bp.w,C.bp.h)*GROS.plus+10; return {x:C.cp.x, y:C.cp.y, w:d, h:d, r:999, l:C.bp.w*GROS.plus}; }
  function deshabille(){ ['guidePhrase','guideCible'].forEach(function(i){ var n=$(i); if(n) n.remove(); }); }
  function habille(g, quoi, phraseVue){ deshabille(); trou=zone(quoi); if(!trou) return false; ou=quoi;
    g.setAttribute('data-guide', quoi); dev.classList.remove('guide-studio','guide-plus'); dev.classList.add('guide-'+quoi); cacheOriginal(quoi);
    var p=eng(document.createElement('div'),'guide-phrase'); p.id='guidePhrase'; p.textContent=T.guide[quoi]; g.appendChild(p);
    var c=eng(document.createElement('div'),'guide-cible'); c.id='guideCible'; c.setAttribute('role','button'); c.tabIndex=0; c.setAttribute('aria-label', quoi==='studio'?'Studio':'Planter');
    c.style.cssText='position:absolute;left:'+(trou.x-trou.w/2)+'px;top:'+(trou.y-trou.h/2)+'px;width:'+trou.w+'px;height:'+trou.h+'px;border-radius:'+Math.min(trou.r,trou.w/2)+'px;margin:0;padding:0;max-width:none;background:transparent'; g.appendChild(c);
    var h=p.offsetHeight||70; p.style.top=Math.round(392-h/2)+'px'; if(phraseVue===false) p.style.visibility='hidden';
    etat=quoi; return true; }
  function montre(quoi, sansRevelation){ retire(); figeMs=null; window._tEvol=performance.now()+400;   /* (le garde dure 1,6 s, la révélation 1,8 : il part 0,4 s « plus tard ») · les tâches de fond attendent (C-112) : une dalle de la collection, 20 à 36 ms, tombait dans la révélation */
    var g=eng(document.createElement('div'),'guide'); g.id='guide'; dev.appendChild(g);
    C=poseLoupe(g); if(!C){ g.remove(); etat=null; return false; }
    loupeA(quoi==='plus'?1:0);
    if(!habille(g, quoi, !!(reduit()||sansRevelation))){ retire(); etat=null; return false; }
    g.addEventListener('click', function(e){ e.stopPropagation(); e.preventDefault(); if(etat==='glisse' || etat==='part') return;
      var D2=dev.getBoundingClientRect(), q=k(), x=(e.clientX-D2.left)/q, yy=(e.clientY-D2.top)/q;
      if(trou && Math.abs(x-trou.x)<=trou.w/2+4 && Math.abs(yy-trou.y)<=trou.h/2+4){ if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); return; }
      if(etat==='studio'){ glisse(); return; }       /* toucher ailleurs pendant l'étape du Studio : la loupe glisse vers le +, le flou reste */
      finir(); }, true);
    g.addEventListener('keydown', function(e){ if(e.key!=='Enter' && e.key!==' ') return; var q=e.target; if(q && q.id==='guideCible'){ e.preventDefault(); if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); } });
    tPose=performance.now(); g.setAttribute('data-pose', ''+Math.round(tPose));
    var Z=formes(); g.__Z=Z;
    if(reduit() || sansRevelation){ g.__L=poseFormes(g, Z, 1); g.setAttribute('data-entier','1'); return true; }
    var L=poseFormes(g, Z, 0.0005); g.__L=L;
    /* la phrase ne paraît qu'une fois le fond flouté sous elle : posée dès le départ, elle se lisait mal sur les titres encore nets des dalles */
    g.__tp=setTimeout(function(){ var q=$('guidePhrase'); if(q && figeMs==null) q.style.visibility='visible'; }, PHRASE_A);
    /* deux images plus tard (la première pose est peinte à taille nulle), les six formes prennent leur taille ENSEMBLE : c'est le navigateur qui anime */
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ if(!g.parentNode || figeMs!=null) return; tPose=performance.now(); g.setAttribute('data-depart', ''+Math.round(tPose));
      L.forEach(function(n,i){ n.style.transition='transform '+INSTALLE+'ms '+COURBE; n.style.transform=tr(Z[i],1,0); }); }); });
    g.__tf=setTimeout(function(){ if(!g.parentNode || figeMs!=null) return; g.setAttribute('data-entier','1'); }, INSTALLE+60);
    return true; }
  /* DU STUDIO AU + : la loupe glisse, les formes se réorganisent, puis la phrase du + paraît */
  function glisse(sansAnim){ var g=$('guide'); if(!g || !C) return false; if(etat==='glisse') return true;
    deshabille(); clearTimeout(g.__tp); montreOriginal(); trou=null; etat='glisse'; window._tEvol=performance.now(); g.setAttribute('data-guide','glisse'); dev.classList.remove('guide-studio');
    function fin(){ anim=0; loupeA(1); g.setAttribute('data-glisse-fin', ''+Math.round(performance.now())); if(!$('guide')) return; habille(g,'plus'); }
    if(reduit() || sansAnim){ (g.__L||[]).forEach(function(n,i){ n.style.transition='none'; n.style.transform=tr(g.__Z[i],1,1); }); fin(); return true; }
    (g.__L||[]).forEach(function(n,i){ n.style.transition='transform '+GLISSE+'ms '+COURBE; n.style.transform=tr(g.__Z[i],1,1); });
    var t0=performance.now(); g.setAttribute('data-glisse', ''+Math.round(t0));
    (function pas(now){ if(!$('guide') || etat!=='glisse') return; var u=Math.min(1, (performance.now()-t0)/GLISSE); loupeA(douce(u)); if(u<1) anim=requestAnimationFrame(pas); else fin(); })();
    return true; }
  /* pour les captures : l'installation, ou le glissement, arrêtés à un instant donné (aucune transition) */
  function fige(ms){ var g=$('guide'); if(!g || !g.__L) return; figeMs=ms; clearTimeout(g.__tf); clearTimeout(g.__tp); g.removeAttribute('data-entier');
    g.__L.forEach(function(n,i){ n.style.transition='none'; n.style.transform=tr(g.__Z[i], Math.max(0.0005, douce(ms/INSTALLE)), 0); });
    var _q=$('guidePhrase'); if(_q) _q.style.visibility=(ms>=PHRASE_A?'visible':'hidden');
    if(ms>=INSTALLE) g.setAttribute('data-entier','1'); }
  function figeGlisse(ms){ var g=$('guide'); if(!g || !g.__L || !C) return; cancelAnimationFrame(anim); anim=0; figeMs=ms; deshabille(); montreOriginal(); etat='glisse'; var u=douce(Math.max(0,Math.min(1,ms/GLISSE)));
    g.__L.forEach(function(n,i){ n.style.transition='none'; n.style.transform=tr(g.__Z[i],1,u); }); loupeA(u); if(ms>=GLISSE){ habille(g,'plus'); } }
  /* le Studio touché : il s'ouvre PAR-DESSUS le guide (le flou reste posé dessous, sans phrase) ; au retour sur l'accueil, la loupe glisse vers le + */
  function versStudio(){ var g=$('guide'); deshabille(); if(g) clearTimeout(g.__tp); montreOriginal(); trou=null; etat='au-studio'; tVu=performance.now(); vuStudio=false; tAcc=0; try{ $('studioBtn').click(); }catch(_){ } }
  function versPlus(){ retire(); etat=null; attente=null; try{ var ch=$('accChoix'); if(ch) ch.classList.add('ouvert'); else $('createBtn').click(); }catch(_){ } }
  /* toucher ailleurs à l'étape du + : le flou se retire (les formes se referment), le guidage est fini */
  function finir(){ attente=null; var g=$('guide'); if(!g){ etat=null; return; } clearTimeout(g.__tf); clearTimeout(g.__tp); cancelAnimationFrame(anim); anim=0; etat='part';
    deshabille(); var lo=$('guideLoupe'); if(lo) lo.remove(); C=null; dev.classList.remove('guide-studio','guide-plus'); montreOriginal();
    if(reduit() || !g.__Z){ retire(); etat=null; return; }
    var u=(ou==='plus')?1:0;
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ (g.__L||[]).forEach(function(n,i){ var z=g.__Z[i]||g.__Z[0]; n.style.transition='transform '+DISSOUT+'ms '+COURBE; n.style.transform=tr(z,0.0005,u); }); }); });
    setTimeout(function(){ if(g.parentNode) g.remove(); if(etat==='part') etat=null; }, DISSOUT+120); }
  /* la veille : l'état se lit sur ce qui est à l'écran */
  setInterval(function(){ var now=performance.now();
    if(attente){ if(!attente.rejeu && LS.g(CLE)==='1'){ attente=null; return; }
      if(accueil() && calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=ATTENTE){ attente=null; tAcc=0; LS.s(CLE,'1'); montre('studio'); } } else tAcc=0; return; }
    if(etat==='au-studio'){ var a=accueil();
      if(!a){ vuStudio=true; tAcc=0; }
      else if(vuStudio || now-tVu>6000){ if(calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=RETOUR){ tAcc=0; if(!glisse()){ retire(); etat=null; } } } else tAcc=0; } }   /* le Studio refermé, avec ou sans choix (6 s : un Studio qui ne s'ouvrirait pas) */
    else if(etat==='studio' || etat==='plus' || etat==='glisse'){
      if(!accueil()){ retire(); etat=null; } } }, 60);
  /* `?guide=1` le rejoue à l'ouverture ; `&gfige=800` arrête l'installation à cet instant ; `&getape=plus` montre la seconde étape ;
     `&gglisse=600` arrête le glissement du Studio au + à cet instant (pour le regarder dans Safari) */
  try{ if(/[?&]guide=1(&|$)/.test(location.search)) setTimeout(function(){ attente={rejeu:true}; tAcc=0; }, 1500); }catch(_){ }
  try{ var _gf=/[?&]gfige=(\d+)/.exec(location.search), _ge=/[?&]getape=plus/.test(location.search), _gg=/[?&]gglisse=(\d+)/.exec(location.search);
    if(_gf||_ge||_gg) setTimeout(function(){ attente=null; montre(_ge?'plus':'studio', !!_gg); if(_gf) fige(+_gf[1]); if(_gg) figeGlisse(+_gg[1]); }, 4200); }catch(_){ }
  window._guide={ attend:function(rejeu){ attente={rejeu:!!rejeu}; tAcc=0; }, montre:montre, finir:finir, glisse:glisse, figeA:fige, figeGlisse:figeGlisse,
    etat:function(){ var g=$('guide'); return {etat:etat, attente:!!attente, trou:trou, vu:LS.g(CLE), entier:!!(g&&g.getAttribute('data-entier')), formes:g?g.querySelectorAll('.gd-t').length:0, u:C?C.u:null}; },
    regle:{INSTALLE:INSTALLE, DISSOUT:DISSOUT, ATTENTE:ATTENTE, FLOU:FLOU, TACHES:TACHES, GROS:GROS, PHRASE_A:PHRASE_A, GLISSE:GLISSE, RETOUR:RETOUR, COURBE:COURBE} };
})();
