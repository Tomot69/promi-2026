<script id="lot-V141-GUIDE">
/* ⚑ v143 (Tom, 12 oct. 2026, C-094) — LE GUIDE D'ACCUEIL, REFAIT. (Les écritures de v141 et v142 : sauvegardes/app-avant-v143.html.)
   « Le flou arrive à un moment bizarre, son remplissage n'est ni beau ni fluide, et l'étape du + n'arrive jamais. »
   CE QUI N'ALLAIT PAS, NOMMÉ : ① le moment — le guide partait 0,8 s après que l'accueil était DEVANT, pendant que la Toile bougeait encore
   (la première dalle qui se pose, la vue qui se cadre) ; ② la technique — la découpe du flou (`clip-path:path()`) était recalculée et
   réécrite à chaque image : Safari re-tramait la zone floutée à chaque image ; ③ l'étape du + — elle n'arrivait que si le Studio avait été
   VU ouvert puis refermé ; un toucher ailleurs finissait tout.
   AUJOURD'HUI :
   · LE MOMENT : l'accueil entièrement posé — l'onboarding refermé, la Toile rendue, plus rien ne bouge, aucun doigt — puis 1,2 s de calme ;
   · LA TECHNIQUE (dictée par Tom) : on n'anime jamais le rayon du flou, ni sa découpe. Six FORMES à bord doux (un dégradé radial en masque,
     posé une fois) portent le flou des murs (4,8 px, constant) et GRANDISSENT PAR `transform` (de 0 à leur taille), courbe douce
     (ease-in-out), jusqu'à se rejoindre en 1,6 s : aucun calcul par image dans la page. Puis UNE couche floutée entière les remplace ;
   · ce qui reste net est une COPIE de l'entrée (son icône et son mot, ou le + et son encart), posée AU-DESSUS du flou, agrandie de 15 % (le
     Studio) ou de 10 % (le +) : le flou n'a plus de trou à découper ;
   · LES ÉTAPES : le Studio — « Choisis d'abord le monde qui te ressemble, au Studio. » (un impératif VOULU par Tom : exception nommée de A3) ;
     puis TOUJOURS le + — Studio refermé avec ou sans choix, ou toucher ailleurs pendant l'étape du Studio : « Promi, Chiche ou Cercle :
     tout commence par ce +. ». Seul « Plus tard » arrête tout. À l'étape du +, toucher le + ouvre les trois natures ; toucher ailleurs finit.
   ⚑ EXCEPTION NOMMÉE À A2 (« aucune transition ») : les six formes du flou, et elles seules, portent une transition CSS sur `transform` —
   c'est la technique demandée, la seule que le navigateur anime sans repasser par la page. Aucune opacité, aucun fondu. Tout nœud porte `data-eng`. */
(function(){
  var T=window.TEXTES_ENGAGEMENT=window.TEXTES_ENGAGEMENT||{};
  /* TEXTE — Tom (lot v143) */
  T.guide={ studio:'Choisis d’abord le monde qui te ressemble, au Studio.',
            plus:'Promi, Chiche ou Cercle : tout commence par ce +.',
            plusTard:'Plus tard' };
  T.imperatifVoulu=(T.imperatifVoulu||[]).concat([T.guide.studio]);   /* A3 : l'exception nommée, lue par redteam_engagement et redteam_guide */
  function $(i){ return document.getElementById(i); }
  var dev=$('device'); if(!dev) return;
  var CLE='promi_guide', INSTALLE=1600, DISSOUT=360, ATTENTE=1200, TACHES=6, GROS={studio:1.15, plus:1.10}, FLOU=4.8;
  var LS={g:function(k){ try{ return localStorage.getItem(k); }catch(_){ return null; } }, s:function(k,v){ try{ localStorage.setItem(k,v); }catch(_){ } }};
  function reduit(){ try{ return !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }catch(_){ return false; } }
  function onbOuvert(){ var o=$('promiOnb'); return !!($('onbV') || (o && !o.classList.contains('gone') && getComputedStyle(o).display!=='none')); }
  function accueil(){ try{ if(onbOuvert()) return false; var r=dev.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height*0.45);
      return !!(h && !(h.closest && h.closest('.screen, .sheet, .poster, #feedView, #entierVue, #dessinMode, #accRappelCompte, #guide'))); }catch(_){ return false; } }
  /* plus rien ne bouge : la Toile ne tourne plus, aucune parole n'arrive ni ne part, aucun doigt depuis une seconde */
  var tDoigt=0; ['pointerdown','touchstart','touchmove','touchend','wheel','keydown'].forEach(function(n){ document.addEventListener(n,function(){ tDoigt=performance.now(); },{capture:true,passive:true}); });
  function calme(){ try{ var st=window.Toile_state&&window.Toile_state(); if(st&&st.running) return false; }catch(_){ }
    if(window._tirageActive) return false; var n=performance.now(); if(window._tMouv && n-window._tMouv<900) return false; if(window._tEcran && n-window._tEcran<900) return false;
    return n-tDoigt>1000; }
  var etat=null, attente=null, tAcc=0, trou=null, tVu=0, vuStudio=false, tFin=0, tPose=0, figeMs=null;
  function k(){ return (dev.getBoundingClientRect().width/390)||1; }
  function eng(n, quoi){ n.setAttribute('data-eng', quoi); return n; }
  function ease(v){ return v<=0?0:(v>=1?1:(v<0.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2)); }   /* ease-in-out (cubique) — la même courbe que la transition CSS */
  /* les six formes : une grille 2 × 3 bousculée ; chacune est une ellipse à bord doux, tournée, assez grande pour que leurs cœurs pleins se
     rejoignent et couvrent l'écran ; elles naissent l'une après l'autre (0 à 0,25 s) et finissent ENSEMBLE à 1,6 s */
  function formes(){ var sd=((Date.now()&0x7fffffff)|1), R=function(){ sd=(Math.imul(sd,1103515245)+12345)&0x7fffffff; return sd/0x7fffffff; }, L=[], o=[0,1,2,3,4,5];
    for(var i=5;i>0;i--){ var j=(R()*(i+1))|0, t=o[i]; o[i]=o[j]; o[j]=t; }
    for(var n=0;n<TACHES;n++){ var gx=n%2, gy=(n/2)|0;
      L.push({x:98+gx*194+(R()-0.5)*70, y:140+gy*282+(R()-0.5)*90, w:600+R()*110, h:600+R()*110, rot:(R()*180)|0, d:o[n]*50}); }
    return L; }
  function tr(f, s){ return 'translate(-50%,-50%) rotate('+f.rot+'deg) scale('+s.toFixed(4)+')'; }
  function poseFormes(g, Z, depart){ var L=[];
    Z.forEach(function(f,i){ var n=eng(document.createElement('div'),'guide-tache'); n.className='gd-t'; n.setAttribute('aria-hidden','true');
      n.style.cssText='left:'+f.x.toFixed(1)+'px;top:'+f.y.toFixed(1)+'px;width:'+f.w.toFixed(0)+'px;height:'+f.h.toFixed(0)+'px;transform:'+tr(f,depart);
      g.insertBefore(n, g.firstChild); L.push(n); });
    return L; }
  function entier(g){ var f=$('guideFlou'); if(f) return f; f=eng(document.createElement('div'),'guide-flou'); f.id='guideFlou'; f.setAttribute('aria-hidden','true'); g.insertBefore(f, g.firstChild); return f; }
  function retireFormes(){ var g=$('guide'); if(!g) return; [].slice.call(g.querySelectorAll('.gd-t')).forEach(function(n){ n.remove(); }); }
  /* la copie nette de l'entrée, au-dessus du flou : l'élément et ses descendants, avec leur style CALCULÉ (les règles de la barre ne
     l'atteignent pas hors d'elle), et ses deux pseudo-éléments (l'anneau et le disque du +) rendus par de vrais nœuds */
  var PROPS=['display','flex-direction','align-items','justify-content','gap','width','height','box-sizing','color','background-color','background-image','background-size','background-position','background-repeat','border-radius','border-top','border-right','border-bottom','border-left','font-family','font-weight','font-size','line-height','letter-spacing','text-transform','white-space','fill','stroke','stroke-width','box-shadow','outline','outline-offset'];
  function style(src, dst, pseudo){ var cs=getComputedStyle(src, pseudo||null); PROPS.forEach(function(p){ try{ dst.style.setProperty(p, cs.getPropertyValue(p)); }catch(_){ } });
    dst.style.setProperty('-webkit-text-fill-color', cs.getPropertyValue('color')); dst.style.margin='0'; dst.style.padding=cs.getPropertyValue('padding'); dst.style.maxWidth='none'; }
  function pseudo(src, hote, quel){ var cs=getComputedStyle(src, quel), c=cs.getPropertyValue('content'); if(!c || c==='none' || c==='normal') return;
    var n=document.createElement('div'); style(src, n, quel); n.style.position='absolute';
    ['left','top','right','bottom','z-index','transform'].forEach(function(p){ n.style.setProperty(p, cs.getPropertyValue(p)); });
    n.style.pointerEvents='none'; hote.appendChild(n); }
  function copie(src){ var n=src.cloneNode(false); n.removeAttribute('id'); n.removeAttribute('class'); style(src, n);
    if(src.namespaceURI!=='http://www.w3.org/2000/svg'){ pseudo(src, n, '::before'); }
    for(var c=src.firstChild;c;c=c.nextSibling){ if(c.nodeType===3) n.appendChild(document.createTextNode(c.nodeValue));
      else if(c.nodeType===1){ if(c.namespaceURI==='http://www.w3.org/2000/svg'){ var s=c.cloneNode(true); s.removeAttribute('id'); var q=getComputedStyle(c); s.style.width=q.width; s.style.height=q.height; s.style.color=q.color; s.style.flex='none'; s.style.position=q.position==='absolute'?'absolute':'relative'; s.style.zIndex='2'; n.appendChild(s); }
        else if(getComputedStyle(c).display!=='none' && c.id!=='filDot'){ var e=copie(c); e.style.position='relative'; e.style.zIndex='2'; n.appendChild(e); } } }
    if(src.namespaceURI!=='http://www.w3.org/2000/svg'){ pseudo(src, n, '::after'); }
    return n; }
  function poseNet(g, quoi){ var cible=$(quoi==='studio'?'studioBtn':'createBtn'); if(!cible) return null;
    var D=dev.getBoundingClientRect(), kk=k(), r=cible.getBoundingClientRect(); if(r.width<8) return null;
    var x=(r.left-D.left)/kk, y=(r.top-D.top)/kk, w=r.width/kk, h=r.height/kk, gr=GROS[quoi];
    var n=copie(cible); eng(n,'guide-net'); n.id='guideNet'; n.setAttribute('aria-hidden','true');
    n.style.position='absolute'; n.style.left=x.toFixed(2)+'px'; n.style.top=y.toFixed(2)+'px'; n.style.width=w.toFixed(2)+'px'; n.style.height=h.toFixed(2)+'px';
    n.style.transformOrigin='50% 50%'; n.style.transform='scale('+gr+')'; n.style.pointerEvents='none'; n.style.overflow='visible';
    [].forEach.call(n.querySelectorAll('*'), function(e){ eng(e,'guide-net'); });
    g.appendChild(n);
    /* la zone qu'on touche : ce qu'on VOIT de l'entrée agrandie (l'icône et le mot ; le + et son encart rond), 6 pt d'air */
    var cx=x+w/2, cy=y+h/2, ux0=1e9, ux1=-1e9, uy0=1e9, uy1=-1e9;
    if(quoi==='studio'){ [].forEach.call(cible.querySelectorAll('svg, .l'), function(e){ var q=e.getBoundingClientRect(); if(q.width<2) return; ux0=Math.min(ux0,(q.left-D.left)/kk); ux1=Math.max(ux1,(q.right-D.left)/kk); uy0=Math.min(uy0,(q.top-D.top)/kk); uy1=Math.max(uy1,(q.bottom-D.top)/kk); });
      if(!(ux1>ux0)){ ux0=x; ux1=x+w; uy0=y; uy1=y+h; }
      return {x:cx, y:cy, w:(ux1-ux0)*gr+12, h:(uy1-uy0)*gr+12, r:14, l:w*gr}; }
    return {x:cx, y:cy, w:Math.max(w,h)*gr+10, h:Math.max(w,h)*gr+10, r:999, l:w*gr}; }
  function retire(){ var g=$('guide'); if(g) g.remove(); dev.classList.remove('guide-studio'); dev.classList.remove('guide-plus'); trou=null; clearTimeout(tFin); }
  /* la phrase, « Plus tard », la cible : posés avec l'étape (ils changent sans rejouer le flou quand on passe du Studio au +) */
  function habille(g, quoi){ ['guideNet','guidePhrase','guideTard','guideCible'].forEach(function(i){ var n=$(i); if(n) n.remove(); });
    trou=poseNet(g, quoi); if(!trou) return false;
    g.setAttribute('data-guide', quoi); dev.classList.remove('guide-studio','guide-plus'); dev.classList.add('guide-'+quoi);
    var p=eng(document.createElement('div'),'guide-phrase'); p.id='guidePhrase'; p.textContent=T.guide[quoi]; g.appendChild(p);
    var t=eng(document.createElement('div'),'plus-tard'); t.id='guideTard'; t.setAttribute('role','button'); t.tabIndex=0; t.textContent=T.guide.plusTard; g.appendChild(t);
    var c=eng(document.createElement('div'),'guide-cible'); c.id='guideCible'; c.setAttribute('role','button'); c.tabIndex=0; c.setAttribute('aria-label', quoi==='studio'?'Studio':'Planter');
    c.style.cssText='position:absolute;left:'+(trou.x-trou.w/2)+'px;top:'+(trou.y-trou.h/2)+'px;width:'+trou.w+'px;height:'+trou.h+'px;border-radius:'+Math.min(trou.r,trou.w/2)+'px;margin:0;padding:0;max-width:none;background:transparent'; g.appendChild(c);
    var h=p.offsetHeight||70, y=Math.round(392-h/2); p.style.top=y+'px'; t.style.top=(y+h+22)+'px';
    etat=quoi; return true; }
  function montre(quoi, sansRevelation){ retire(); figeMs=null;
    var g=eng(document.createElement('div'),'guide'); g.id='guide'; dev.appendChild(g);
    if(!habille(g, quoi)){ g.remove(); etat=null; return false; }
    g.addEventListener('click', function(e){ e.stopPropagation(); e.preventDefault(); var D2=dev.getBoundingClientRect(), q=k(), x=(e.clientX-D2.left)/q, yy=(e.clientY-D2.top)/q;
      if(e.target && e.target.closest && e.target.closest('#guideTard')){ finir(); return; }
      if(trou && Math.abs(x-trou.x)<=trou.w/2+4 && Math.abs(yy-trou.y)<=trou.h/2+4){ if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); return; }
      if(etat==='studio'){ habille(g,'plus'); return; }       /* toucher ailleurs pendant l'étape du Studio : l'étape du + vient ensuite, le flou reste */
      finir(); }, true);
    g.addEventListener('keydown', function(e){ if(e.key!=='Enter' && e.key!==' ') return; var q=e.target; if(q && q.id==='guideTard'){ e.preventDefault(); finir(); } else if(q && q.id==='guideCible'){ e.preventDefault(); if(etat==='studio') versStudio(); else versPlus(); } });
    tPose=performance.now(); g.setAttribute('data-pose', ''+Math.round(tPose));
    if(reduit() || sansRevelation){ entier(g); g.setAttribute('data-entier','1'); return true; }
    var Z=formes(), L=poseFormes(g, Z, 0.0005); g.__Z=Z; g.__L=L;
    /* deux images plus tard (la première pose est peinte à taille nulle), les formes prennent leur taille : c'est le navigateur qui anime */
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ if(!g.parentNode || figeMs!=null) return; tPose=performance.now(); g.setAttribute('data-depart', ''+Math.round(tPose));
      L.forEach(function(n,i){ var f=Z[i]; n.style.transition='transform '+(INSTALLE-f.d)+'ms cubic-bezier(0.65,0,0.35,1) '+f.d+'ms'; n.style.transform=tr(f,1); }); }); });
    tFin=setTimeout(function(){ if(!g.parentNode || figeMs!=null) return; entier(g); retireFormes(); g.setAttribute('data-entier','1'); }, INSTALLE+140);
    return true; }
  /* pour les captures : l'installation arrêtée à un instant donné (aucune transition : chaque forme à la taille qu'elle a à cet instant) */
  function fige(ms){ var g=$('guide'); if(!g || !g.__L) return; figeMs=ms; clearTimeout(tFin); var f0=$('guideFlou'); if(f0) f0.remove(); g.removeAttribute('data-entier');
    if(!g.querySelector('.gd-t')) g.__L=poseFormes(g, g.__Z, 0.0005);
    g.__L.forEach(function(n,i){ var f=g.__Z[i]; n.style.transition='none'; n.style.transform=tr(f, Math.max(0.0005, ease((ms-f.d)/(INSTALLE-f.d)))); });
    if(ms>=INSTALLE){ entier(g); retireFormes(); g.setAttribute('data-entier','1'); } }
  function versStudio(){ retire(); etat='au-studio'; tVu=performance.now(); vuStudio=false; tAcc=0; try{ $('studioBtn').click(); }catch(_){ } }
  function versPlus(){ retire(); etat=null; attente=null; try{ var ch=$('accChoix'); if(ch) ch.classList.add('ouvert'); else $('createBtn').click(); }catch(_){ } }
  /* « Plus tard », ou toucher ailleurs à l'étape du + : le flou se retire (les formes se referment), le guidage est fini */
  function finir(){ attente=null; var g=$('guide'); if(!g){ etat=null; return; } clearTimeout(tFin); etat='part';
    ['guideNet','guidePhrase','guideTard','guideCible'].forEach(function(i){ var n=$(i); if(n) n.remove(); }); dev.classList.remove('guide-studio','guide-plus');
    if(reduit() || !g.__Z){ retire(); etat=null; return; }
    var f=$('guideFlou'); if(f){ g.__L=poseFormes(g, g.__Z, 1); f.remove(); } else g.__L=[].slice.call(g.querySelectorAll('.gd-t'));
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ (g.__L||[]).forEach(function(n,i){ var z=g.__Z[i]||g.__Z[0]; n.style.transition='transform '+DISSOUT+'ms cubic-bezier(0.65,0,0.35,1)'; n.style.transform=tr(z,0.0005); }); }); });
    setTimeout(function(){ if(g.parentNode) g.remove(); if(etat==='part') etat=null; }, DISSOUT+120); }
  /* la veille : l'état se lit sur ce qui est à l'écran */
  setInterval(function(){ var now=performance.now();
    if(attente){ if(!attente.rejeu && LS.g(CLE)==='1'){ attente=null; return; }
      if(accueil() && calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=ATTENTE){ attente=null; tAcc=0; LS.s(CLE,'1'); montre('studio'); } } else tAcc=0; return; }
    if(etat==='au-studio'){ var a=accueil();
      if(!a){ vuStudio=true; tAcc=0; }
      else if(vuStudio || now-tVu>6000){ if(calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=ATTENTE){ tAcc=0; montre('plus'); } } else tAcc=0; } }   /* le Studio refermé, avec ou sans choix (6 s : un Studio qui ne s'ouvrirait pas) */
    else if(etat==='studio' || etat==='plus'){
      var couvert=onbOuvert(); if(!couvert){ try{ var r=dev.getBoundingClientRect(), E=document.elementsFromPoint(r.left+r.width/2, r.top+r.height*0.45);
          for(var i=0;i<E.length;i++){ var h=E[i]; if(h.closest && h.closest('#guide')) continue; couvert=!!(h.closest && h.closest('.screen, .sheet, .poster, #feedView, #entierVue, #dessinMode, #accRappelCompte')); break; } }catch(_){ } }
      if(couvert){ retire(); etat=null; } } }, 120);
  /* `?guide=1` le rejoue à l'ouverture ; `&gfige=800` l'arrête à cet instant ; `&getape=plus` montre la seconde étape (pour le regarder dans Safari) */
  try{ if(/[?&]guide=1(&|$)/.test(location.search)) setTimeout(function(){ attente={rejeu:true}; tAcc=0; }, 1500); }catch(_){ }
  try{ var _gf=/[?&]gfige=(\d+)/.exec(location.search), _ge=/[?&]getape=plus/.test(location.search); if(_gf||_ge) setTimeout(function(){ attente=null; montre(_ge?'plus':'studio'); if(_gf) fige(+_gf[1]); }, 4200); }catch(_){ }
  window._guide={ attend:function(rejeu){ attente={rejeu:!!rejeu}; tAcc=0; }, montre:montre, finir:finir, figeA:fige,
    etat:function(){ var g=$('guide'); return {etat:etat, attente:!!attente, trou:trou, vu:LS.g(CLE), entier:!!(g&&g.getAttribute('data-entier')), formes:g?g.querySelectorAll('.gd-t').length:0}; },
    regle:{INSTALLE:INSTALLE, DISSOUT:DISSOUT, ATTENTE:ATTENTE, FLOU:FLOU, TACHES:TACHES, GROS:GROS} };
})();
</script>
