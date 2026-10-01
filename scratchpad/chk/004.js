


var _dalles=0;
setTimeout(function(){try{var ov=document.getElementById('promiOnb');if(ov&&!ov.classList.contains('gone'))obFill(OB_FILL_AUTH);}catch(e){}},420);
var _semTimer=null;
function setDalles(target){
  var T=window.Toile;
  if(!T||!T.plantOne){setTimeout(function(){setDalles(target);},120);return;}
  var tot=T.cells();
  var n=(target<=1)?Math.round(target*tot):Math.min(tot,target|0);
  _dalles=n;
  try{clearInterval(_semTimer);}catch(e){}
  var cur=T.colored();

  /* PREMIER AFFICHAGE (l'authentification) : la Toile est pleine d'emblée,
     exactement comme avant — on ne fait pas attendre l'écran d'accueil. */
  if(cur===0&&n>0){
    for(var i=0;i<n;i++)T.plantOne(true);
    try{T.applyReserve();}catch(e){}
    try{T.redraw();}catch(e){}
    return;
  }

  /* ENSUITE, chaque dalle s'INSÈRE : elle se fait une place, les voisines
     s'écartent, la Toile se repose. Par petits lots, pour ne jamais traîner. */
  var pas=Math.max(1, Math.round(Math.abs(n-cur)/13));
  _semTimer=setInterval(function(){
    var c=T.colored();
    if(c===n){
      try{clearInterval(_semTimer);}catch(e){}
      try{T.applyReserve();}catch(e){}
      return;
    }
    var k=Math.min(pas, Math.abs(n-c));
    for(var q=0;q<k;q++){ if(c<n)T.plantOne(); else T.unplantOne(); }
    try{T.applyReserve();}catch(e){}
  }, 95);
}

var pseudoReady=false;
function toPseudo(){
  document.getElementById('authScreen').style.display='none';
  document.getElementById('pseudoScreen').style.display='flex';
  pseudoReady=false;
  setTimeout(function(){pseudoReady=true;},450);try{obFill(OB_FILL_NAME);}catch(e){}
  setTimeout(function(){var el=document.getElementById('pseudoInput');if(el)el.focus();},520);
}
function prefill(name){var el=document.getElementById('pseudoInput');if(el&&name){el.value=name;liveName(name);}}
function liveName(v){var n=document.getElementById('liveName');if(n)n.textContent=v&&v.trim()?(' '+v.trim()):'';}
document.getElementById('btnApple').onclick=function(){/* Firebase signInWithApple -> prénom Apple */prefill('Tom');toPseudo();};
document.getElementById('btnGoogle').onclick=function(){/* Firebase signInWithGoogle -> prénom Google */prefill('Tom');toPseudo();};

var _pin=document.getElementById('pseudoInput');if(_pin)_pin.addEventListener('input',function(){liveName(this.value);});
var pseudoValidated=false;
document.getElementById('btnContinue').onclick=function(){
  if(!pseudoReady)return;
  if(!pseudoValidated){
    var n=(document.getElementById('pseudoInput').value||'').trim()||'toi';
    liveName(n);
    document.getElementById('pseudoField').style.display='none';
    document.getElementById('pseudoTag').textContent='Ici, tes promesses prennent vie.';
    this.textContent='Explorer';this.classList.remove('apple');this.classList.add('blue');
    document.getElementById('pseudoScreen').classList.add('validated');
    pseudoValidated=true;try{obFill(OB_FILL_NAME2);}catch(e){}
  } else {
    document.getElementById('pseudoScreen').style.display='none';
    document.getElementById('onboard').style.display='flex';
    obI=0;maxSeen=0;renderOb();initObSwipe();
  }
};
var OB=[
 {viz:'toile',t:'Tiens tes<br><span style="color:var(--verm)">promesses.</span>',s:"Un Promi, c'est une <b>promesse</b> — à <b>toi-même</b> ou à un <b>proche</b>. Chacune construit ta <b>Toile</b>, dalle après dalle. <b>Partage-la au monde.</b>"},
 {viz:'nue',t:'Les <span style="color:var(--verm)">Cercles.</span>',s:'Des Promi <b>réunis autour d’un thème</b> : un week-end, la famille, le couple… Invite tes proches à y planter les leurs.'},
 {viz:'fil',t:'Tes Promi,<br><span style="color:var(--verm)">deux vues.</span>',s:'Deux façons de voir <b>les mêmes Promi</b> : le <b>Fil</b> qui défile, ou la <b>Toile</b> en dalles.'},
 {viz:'kar',t:'Ton <span style="color:var(--verm)">Aura,</span><br>ce que tu dégages.',s:'Pas de note ni de score : juste ton <b>harmonie</b>, sans pression. Ton Noyau grandit à mesure que tu tiens parole.'},
 {studio:true,t:'Compose ta<br><span style="color:var(--verm)">Toile.</span>',s:'Choisis l\u2019ambiance de tes dalles. Fais glisser le galet : la couleur se r\u00e9v\u00e8le. Tu pourras tout changer plus tard dans le Studio.'},
 {create:true,t:'Ton premier<br><span style="color:var(--verm)">Promi.</span>',s:'Il est pour <b>toi</b> — et devient ta première dalle. Plus tard, tu en enverras à tes proches.'}
];
var obI=0,maxSeen=0,obDraw='fil';
function renderOb(){
  /* au rejeu, le premier Promi est déjà planté : on ne le redemande pas, on passe au tuto */
  if(_obReplaying&&OB[obI]&&OB[obI].create){obFinish();return;}
  var s=OB[obI];try{obSetX(0,false);}catch(e){}document.getElementById('obTitle').innerHTML=s.t;document.getElementById('obTag').innerHTML=s.s;var cr=!!s.create;var stu=!!s.studio;var cv=document.getElementById('obCv');cv.style.display=(cr||stu)?'none':'block';document.getElementById('obCreate').style.display=cr?'block':'none';var _obst=document.getElementById('obStudio');if(_obst)_obst.style.display=stu?'block':'none';if(stu){try{initObJauge();}catch(e){}}var _fin=_obReplaying && obI===OB.length-2;
  document.getElementById('btnOb').textContent=cr?'Planter mon premier Promi':(_fin?'C’est reparti':'Suivant');try{obFill(OB_FILL[obI]!=null?OB_FILL[obI]:1);}catch(e){}if(!cr){cv.dataset.viz=s.viz;try{IntroViz.run(cv);}catch(e){}/* une seule reprise, et uniquement si le canvas est resté à sa taille par défaut   (panneau pas encore mis en page). Relancer plus d'une fois redémarrerait l'animation. */try{requestAnimationFrame(function(){if(cv.width===300&&cv.height===150){try{IntroViz.run(cv);}catch(e){}}});}catch(e){}}else{try{cancelAnimationFrame(window.IntroVizRAF);}catch(e){}}var dd=document.getElementById('obDots'),html='';for(var k=0;k<OB.length;k++)html+='<span class="ob-dot'+(k===obI?' on':'')+'"></span>';dd.innerHTML=html;}


var _obSwipeInit=false;
function obSlideEls(){return [document.querySelector('#onboard .ob-top'),document.querySelector('#onboard .ob-mid')];}
function obSetX(px,anim){obSlideEls().forEach(function(e){if(!e)return;e.style.transition=anim?'transform .28s cubic-bezier(.22,.61,.36,1),opacity .28s':'none';e.style.transform='translateX('+px+'px)';e.style.opacity=String(Math.max(0,1-Math.abs(px)/260));});}
function initObSwipe(){if(_obSwipeInit)return;_obSwipeInit=true;var ob=document.getElementById('onboard');var sx=null,dx=0,drag=false;
 ob.addEventListener('pointerdown',function(e){if(e.target.closest('.btn,#obPromiInput,#obSkip,#obStudio'))return;sx=e.clientX;dx=0;drag=true;});
 ob.addEventListener('pointermove',function(e){if(!drag||sx==null)return;dx=e.clientX-sx;
   var canFwd=(obI<OB.length-1 && obI+1<=maxSeen), canBack=true;
   if(dx<0&&!canFwd)dx*=0.28;
   if(dx>0&&!canBack)dx*=0.28;
   obSetX(dx,false);});
 function endSwipe(){if(!drag)return;drag=false;var d=dx;sx=null;dx=0;
   var canFwd=(obI<OB.length-1 && obI+1<=maxSeen);
   if(d<-60&&canFwd){obI++;obSetX(0,true);renderOb();}
   else if(d>60){ if(obI>0){obI--;obSetX(0,true);renderOb();} else { document.getElementById('onboard').style.display='none';var ps=document.getElementById('pseudoScreen');ps.style.display='flex';obSetX(0,false);try{obFill(OB_FILL_NAME);}catch(e){} } }
   else {obSetX(0,true);} }
 ob.addEventListener('pointerup',endSwipe);ob.addEventListener('pointercancel',endSwipe);
}
var _obPlanted=false;
var _obReplaying=false;   /* rejeu : le compte, le pseudo et le premier Promi sont déjà faits */
document.getElementById('btnOb').onclick=function(){
  /* slide studio : il faut avoir exploré au moins un autre style pour continuer */
  var _obst=document.getElementById('obStudio');
  if(_obst&&_obst.offsetParent&&!window._obExplored){
    var dz=document.getElementById('obStDesigns');
    if(dz){dz.style.animation='none';void dz.offsetWidth;dz.style.animation='obShake .4s';}
    return;
  }
  /* on rejoue : son premier Promi existe déjà, on s'arrête avant cet écran */
  var _last=_obReplaying ? (OB.length-2) : (OB.length-1);
  if(obI<_last){obI++;if(_obReplaying){while(OB[obI]&&(OB[obI].studio||OB[obI].create)&&obI<_last)obI++;}if(obI>maxSeen)maxSeen=obI;renderOb();return;}
  if(_obReplaying){ obFinish(); return; }
  if(_obPlanted)return;                                  /* verrou : un seul premier Promi */
  var v=(document.getElementById('obPromiInput').value||'').trim();
  if(!v){
    var f=document.querySelector('#promiOnb .oc-field');
    if(f){f.classList.remove('oc-shake');void f.offsetWidth;f.classList.add('oc-shake');}
    try{var inp=document.getElementById('obPromiInput');if(inp)inp.focus();}catch(e){}
    return;
  }
  _obPlanted=true;
  try{var nm=(document.getElementById('pseudoInput').value||'').trim();if(nm)USER.name=nm;}catch(e){}
  try{
    if(_obReplaying){                                    /* on rejoue : on ne touche à RIEN de ses données */
      if(typeof obFinish==='function')obFinish();
      return;
    }
    obResetData();                                       /* la vie commence ici : plus rien de la démo */
    var np=P(v,'Moi',7,2,'encours',undefined,'moi');
    computeBox();np.x=box.x+box.w/2;np.y=box.y+box.h/2;np.tx=np.x;np.ty=np.y;
    promises.push(np);
    if(window.Toile&&window.Toile.sync)window.Toile.sync([np.id]);   /* 1 Promi = 1 dalle, reliée */
    if(typeof render==='function')render();
    if(typeof caption==='function')caption();
    if(typeof queueSave==='function')queueSave();
  }catch(e){}
  obFinish();
  setTimeout(function(){try{window._tutoSeen=false;startTuto(true);}catch(e){}},420);
};




/* la trame se pose sur les pages, jamais sur Partager / le Studio / Karma */
(function(){
  var SANS={shareScreen:1, studioScreen:1, auraScreen:1, sealOv:1};
  var _pend=false;
  function pose(){
    _pend=false;
    document.querySelectorAll('.sheet, .poster, .screen').forEach(function(e){
      var veut=!SANS[e.id], a=e.classList.contains('trame');
      /* on n'ÉCRIT que si ça change vraiment : réécrire la classe déclenche une
         mutation d'attribut, qui réveille les autres observateurs — et la page fige */
      if(veut&&!a)e.classList.add('trame');
      else if(!veut&&a)e.classList.remove('trame');
    });
  }
  pose();
  /* les feuilles créées plus tard en héritent aussi, sans marteler le DOM */
  if(window.MutationObserver){
    new MutationObserver(function(){
      if(_pend)return; _pend=true;
      requestAnimationFrame(pose);
    }).observe(document.getElementById('device')||document.body,{childList:true, subtree:true});
  }
})();


/* la trame se pose sur les pages, jamais sur Partager / le Studio / Karma */
(function(){
  var SANS={shareScreen:1, studioScreen:1, auraScreen:1, sealOv:1};
  function pose(){
    document.querySelectorAll('.sheet, .poster, .screen').forEach(function(e){
      if(SANS[e.id]){e.classList.remove('trame');return;}
      e.classList.add('trame');
    });
  }
  pose();
  /* les feuilles créées plus tard en héritent aussi */
  if(window.MutationObserver){
    new MutationObserver(pose).observe(document.getElementById('device')||document.body,
      {childList:true, subtree:true});
  }
})();

/* --- le téléphone ne défile JAMAIS sur lui-même ---
   Quand un champ situé bas dans une feuille prend le focus, le navigateur fait
   défiler TOUS les conteneurs pour l'amener à l'écran — y compris #device, qui
   est pourtant en overflow:hidden. Le téléphone entier glissait alors vers le
   haut (scrollTop jusqu'à 600px) : la Toile sortait du cadre et ne revenait pas.
   Seules les feuilles ont le droit de défiler. */
(function(){
  var dev=document.getElementById('device'); if(!dev)return;
  function pin(){ if(dev.scrollTop||dev.scrollLeft){dev.scrollTop=0;dev.scrollLeft=0;} }
  dev.addEventListener('scroll',pin,{passive:true});
  setInterval(pin,400);
})();

/* --- le téléphone entier tient dans la fenêtre, sans jamais se déformer --- */
function fitDevice(){
  var f=document.querySelector('.frame'); if(!f)return;
  var vw=document.documentElement.clientWidth, vh=window.innerHeight||document.documentElement.clientHeight;
  var s=Math.min(1, vw/(390+28), vh/(844+28));      /* le cadre + son padding */
  if(!(s>0))s=1;
  f.style.setProperty('--fit', s.toFixed(4));
}
fitDevice();
addEventListener('resize',fitDevice);
addEventListener('orientationchange',fitDevice);

/* ===================== ONBOARDING — intégration à l'app ===================== */
(function(){
  var ov=document.getElementById('promiOnb'), dev=document.getElementById('device');
  if(!ov||!dev)return;
  if(ov.parentNode!==dev)dev.appendChild(ov);            /* l'overlay vit DANS le téléphone */
  /* les proportions de l'onboarding suivent le TÉLÉPHONE, jamais la fenêtre */
  function fit(){
    /* cotes de MISE EN PAGE du téléphone (844px), pas ses cotes à l'écran :
       le tout est mis à l'échelle, les proportions internes ne bougent pas */
    var h=dev.offsetHeight, w=dev.offsetWidth;
    if(!h)return;
    var k=Math.max(.72, Math.min(1, h/844));          /* 844px = le téléphone de référence */
    ov.style.setProperty('--dh', Math.round(h)+'px');
    ov.style.setProperty('--dw', Math.round(w)+'px');
    ov.style.setProperty('--k', k.toFixed(4));
    var cv=document.getElementById('obCv');
    if(cv&&cv.dataset.viz&&cv.offsetParent!==null){try{IntroViz.run(cv);}catch(e){}}
  }
  fit();
  window.addEventListener('resize',fit);
  try{new ResizeObserver(fit).observe(dev);}catch(e){}
  window._obFit=fit;
})();

/* --- l'app démarre sur la vie de l'utilisateur, pas sur un jeu de démo --- */
function obResetData(){
  try{
    promises.length=0;                                  /* aucun Promi de démonstration */
    if(typeof NUE==='object')Object.keys(NUE).forEach(function(k){delete NUE[k];});
    if(typeof NUEEMEM==='object')Object.keys(NUEEMEM).forEach(function(k){delete NUEEMEM[k];});
    if(Array.isArray(FEED))FEED.length=0;
    if(Array.isArray(PEOPLE))PEOPLE.length=0;
    try{feedReacted={};}catch(e){}
    try{shareHidden={};}catch(e){}
  }catch(e){}
}

/* --- mode clair pendant tout l'onboarding (la Toile crème fait ressortir les dalles) --- */
var _obThemeBefore=null;
function obLightOn(){try{if(_obThemeBefore===null)_obThemeBefore=(typeof theme!=='undefined'?theme:'dark');if(typeof setTheme==='function')setTheme('light');}catch(e){}}
function obLightOff(){/* on RESTE en clair : l'app s'ouvre en clair après l'onboarding */_obThemeBefore=null;}

/* --- ENCRE ADAPTATIVE : la police se découpe selon la dalle qui est dessous ---
   On échantillonne la Toile sous chaque bloc de texte et on bascule l'encre
   (claire sur dalle sombre, sombre sur dalle claire/colorée). Aucun contour, aucun voile. */
var OB_INK_SEL='#promiOnb .wordmark, #promiOnb .tag, #promiOnb #pseudoTag, #promiOnb .ob-h, #promiOnb .ob-p, #promiOnb .oc-to, #promiOnb .legal, #promiOnb #obSkip';

/* --- L'ENCRE DE L'ONBOARDING ---
   La Toile fait de la place au texte (voir Toile.reserve) : sous un bloc de
   texte, les dalles prennent la teinte la plus claire de la palette. L'encre
   peut donc rester fixe et sombre — lisible partout, sans rien recalculer. */
function obInkStart(){
  try{
    document.querySelectorAll('#promiOnb .ink-map').forEach(function(e){
      e.classList.remove('ink-map');e.style.backgroundImage='';
    });
  }catch(e){}
}
function obInkStop(){ obInkStart(); }
function obInkTick(){}

/* --- fin / relance / persistance --- */
var _obFinished=false;
function obFinish(){
  if(_obFinished)return; _obFinished=true;
  /* la Toile ne garde QUE les Promi réels : 1 Promi = 1 dalle, reliée */
  try{
    setDalles(0);                                   /* les dalles de l'onboarding s'effacent */
    if(window.Toile&&window.Toile.sync){
      var _ids=promises.filter(function(p){return !p.draft;}).map(function(p){return p.id;});
      window.Toile.sync(_ids);
    }
  }catch(e){}
  obInkStop();
  obLightOff();
  try{if(window.Toile&&window.Toile.redraw)setTimeout(window.Toile.redraw,60);}catch(e){}   /* le texte des dalles revient */
  var ov=document.getElementById('promiOnb'); if(ov)ov.classList.add('gone');
  try{localStorage.setItem('promi_onb','1');}catch(e){}
  try{if(typeof render==='function')render();}catch(e){}
  if(_obReplaying){                                   /* on rejouait : on enchaîne sur le tuto */
    _obReplaying=false;
    setTimeout(function(){try{window._tutoSeen=false;startTuto(true);}catch(e){}},420);
  }
}
function obReplay(){
  var ov=document.getElementById('promiOnb'); if(!ov)return;
  try{document.querySelectorAll('.screen.show,.sheet.show').forEach(function(e){e.classList.remove('show');});}catch(e){}
  try{var sc=document.getElementById('scrim');if(sc)sc.classList.remove('show');}catch(e){}
  ov.classList.remove('gone');
  _obReplaying=true;                                   /* on rejoue : ni compte, ni pseudo, ni premier Promi */
  try{if(window.Toile&&window.Toile.resetView)window.Toile.resetView();}catch(e){}
  document.getElementById('authScreen').style.display='none';
  /* on reprend à « Enchanté …, ici tes promesses prennent vie » */
  var ps=document.getElementById('pseudoScreen');ps.style.display='flex';ps.classList.add('validated');
  document.getElementById('pseudoField').style.display='none';
  document.getElementById('pseudoTag').textContent='Ici, tes promesses prennent vie.';
  var bc=document.getElementById('btnContinue');bc.textContent='Explorer';bc.classList.remove('apple');bc.classList.add('blue');
  document.getElementById('onboard').style.display='none';
  pseudoValidated=true;obI=0;maxSeen=0;_obPlanted=true;_obFinished=false;
  /* le bouton s'arme APRÈS que l'écran s'installe : sinon le clic qui a lancé la
     relance (dans les Réglages) retombe sur « Explorer » et saute l'écran */
  pseudoReady=false;setTimeout(function(){pseudoReady=true;},450);
  try{liveName(USER.name||'toi');}catch(e){}   /* on connaît déjà son nom */
  obLightOn();
  try{obFill(OB_FILL_NAME2);}catch(e){}   /* la Toile reprend là où « Enchanté » la laisse */
  obInkStart();
}
/* démarrage : on ne rejoue pas l'onboarding s'il a déjà été fait (rejouable depuis les Réglages) */
/* part de la Toile colorée, écran par écran */
var OB_FILL=[0.30,0.42,0.54,0.66,0.82,1.00];   /* elle n'est PLEINE qu'au dernier slide : celui du premier Promi */   /* les 5 slides : ça monte, sans jamais redescendre */
var OB_FILL_AUTH=1.00;                    /* authentification : toute la Toile est colorée */
var OB_FILL_NAME=0.16;                    /* « Enchanté » : la Toile retombe presque à vide */
var OB_FILL_NAME2=0.26;                   /* « Ici, tes promesses prennent vie » : la complétion démarre */
function obReserveZones(){
  try{
    var cv=document.getElementById('toileCv'); if(!cv||!cv.clientWidth)return;
    var cr=cv.getBoundingClientRect(); if(!cr.width||!cr.height)return;
    /* de l'écran vers le repère de la Toile (px de mise en page), quelle que soit l'échelle */
    var sx=cv.clientWidth/cr.width, sy=cv.clientHeight/cr.height;
    var rects=[];
    /* TOUS les blocs de texte : la Toile s'éclaircit sous chacun d'eux */
    ['#promiOnb .wordmark','#promiOnb .tag','#promiOnb #pseudoTag',
     '#promiOnb .ob-h','#promiOnb .ob-p','#promiOnb .oc-lbl2','#promiOnb .oc-to',
     '#promiOnb .legal','#promiOnb #obSkip'].forEach(function(sel){
      var e=document.querySelector(sel);
      if(!e||e.offsetParent===null)return;
      var r=e.getBoundingClientRect(); if(!r.width||!r.height)return;
      rects.push({x:(r.left-cr.left)*sx, y:(r.top-cr.top)*sy,
                  w:r.width*sx, h:r.height*sy, pad:6});
    });
    if(window.Toile&&window.Toile.reserve)window.Toile.reserve(rects);
  }catch(e){}
}
function obFill(part){try{obReserveZones();setDalles(part);}catch(e){}}
/* la Toile bouge en permanence pendant l'onboarding : on re-éclaircit les dalles
   passées sous le texte, sinon un titre finirait sur une dalle sombre */
setInterval(function(){
  var ov=document.getElementById('promiOnb');
  if(!ov||ov.classList.contains('gone'))return;
  try{obReserveZones();window.Toile&&window.Toile.applyReserve&&window.Toile.applyReserve();}catch(e){}
},260);

(function(){
  var done=false; try{done=localStorage.getItem('promi_onb')==='1';}catch(e){}
  var ov=document.getElementById('promiOnb');
  if(done){
    if(ov)ov.classList.add('gone');
    /* la Toile porte exactement les Promi réels — 1 Promi = 1 dalle, reliée */
    setTimeout(function(){
      try{
        if(!window.Toile||!window.Toile.sync)return;
        var ids=promises.filter(function(p){return !p.draft;}).map(function(p){return p.id;});
        window.Toile.sync(ids);
      }catch(e){}
    },320);
    /* utilisateur qui revient : on lui rend le thème qu'il avait */
    /* le thème est appliqué APRÈS l'init de l'app (qui repose ses valeurs par défaut).
       Sans choix mémorisé, l'app s'ouvre en CLAIR. */
    setTimeout(function(){
      try{
        var th=null; try{th=localStorage.getItem('promi_theme');}catch(e){}
        /* v20 (Q301) : sans choix mémorisé, le thème suit celui du téléphone */
        if(!th){try{th=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}catch(e){th='light';}}
        if(typeof setTheme==='function')setTheme(th);
      }catch(e){}
    },260);
  }
  /* v20 : l'onboarding neuf (lot-ONB-V20) prend la main au premier lancement ; plus de thème forcé */
})();

