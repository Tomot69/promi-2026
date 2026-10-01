
/* ⚑ v104 — TOUCHER UN MUR (la phrase reprise en v105 : au centre du mur, sans plateau, le temps d'être lue). « Quand on touche un mur, une phrase monte du bas et reste. Ensuite, toucher n'importe où à l'écran
   ouvre la page de l'offre. Sauf la toute première fois : la page s'ouvre automatiquement, pour qu'on découvre qu'elle existe. »
   Le compteur est GLOBAL (toutes zones, par personne, gardé : `promi_murs`), les 21 phrases dans l'ordre, puis au hasard sans
   répéter la précédente ; il repart à zéro après une longue absence de contact avec un mur (ABSENCE, à valider — QUESTIONS).
   Un mur se reconnaît à sa GÉOMÉTRIE (le toucher tombe dans son rectangle) : ses réglages sont en pointer-events:none, le doigt
   ne les atteint jamais — et c'est voulu, rien de flouté ne doit s'ouvrir. La page de l'offre s'ouvre PAR-DESSUS (`_cercleDessus`),
   sans rien fermer : on retrouve l'écran où l'on était. « Ma Parole ! » : le nom neuf de l'offre, dans ces phrases seulement. */
(function(){
  var MP='Ma Parole !';
  var PHRASES=['Eh non ! Mais avec '+MP+', oui.','Toujours pas. Avec '+MP+', si.','Je vois bien que ça te titille. '+MP+' lève tout ça.',
    'Tiens tiens, on dirait que ça commence à t’intéresser…','Tu connais déjà la solution, me semble-t-il.','Tu sais où trouver '+MP+' maintenant.',
    'Je commence à connaître tes habitudes.','Je crois qu’on commence à bien se connaître.','C’est sûr de sûr que tu ne veux pas essayer ?',
    'Allons bon. Nous y voilà à nouveau.','Entre nous, tu sais très bien ce qu’il faudrait faire.','À ce stade, autant arrêter de négocier, non ?',
    'Tu peux continuer. Je ne dirai rien.','Tu sais, je ne vais pas te juger.',MP+' aussi, ça peut durer longtemps.',
    'Je crois que tu essaies de me faire changer d’avis.','On pourrait presque appeler ça une tradition.','Tu commencerais presque à connaître le chemin.',
    'On commence à avoir nos petites habitudes.','Je vais finir par croire que tu viens juste me voir.','On se dit directement à la prochaine ?'];
  var ABSENCE=14*24*3600*1000;   /* à valider (QUESTIONS) : « une longue absence » */
  window._murPhrases=PHRASES;
  function lit(){ try{ return JSON.parse(localStorage.getItem('promi_murs')||'{}')||{}; }catch(_){ return {}; } }
  function ecrit(o){ try{ localStorage.setItem('promi_murs', JSON.stringify(o)); }catch(_){} }
  function paye(){ try{ return !!(isPremium || document.getElementById('device').classList.contains('premium')); }catch(_){ return false; } }
  function vu(e){ if(!e||!e.getClientRects().length) return false; var s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden') return false;
    var sc=e.closest('.screen,.sheet,.poster,#studioScreen,#auraScreen,#auraHelp'); if(sc && !sc.classList.contains('show') && !sc.classList.contains('in')) return false; return true; }
  function murs(){ var L=[]; if(paye()) return L;
    var add=function(sel){ document.querySelectorAll(sel).forEach(function(e){ if(vu(e)) L.push(e); }); };
    add('#detailPoster .s2-cercle:not(.v16-seul)'); add('#createSheet.pp-peauf .s2-cercle:not(.v16-seul)');
    if(document.querySelector('#auCadre.au-voile')) add('#auCadre.au-voile .au-gr2');
    add('#auraHelp .ah-locked');
    add('#notifScreen .nt-mur');   /* v109 : la mémoire des paroles en l'air et le choix de l'heure */
    var st=document.getElementById('studioScreen');
    if(st && (st.classList.contains('stp-verrou')||st.classList.contains('world-locked')) && !st.classList.contains('st-entre')) ['#stpTons','#stpVue','#stpDots','#stpLab'].forEach(function(s){ var e=st.querySelector(s); if(e&&vu(e)) L.push(e); });
    return L; }
  function dans(x,y){ var L=murs(); for(var i=0;i<L.length;i++){ var r=L[i].getBoundingClientRect(); if(x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom){
      /* le premier plan doit être le mur (ou ce qui le porte), pas une feuille posée dessus */
      var h=document.elementFromPoint(x,y); if(!h || L[i].contains(h) || h.contains(L[i]) || (h.closest&&h.closest('#detailPoster,#createSheet,#auraScreen,#auraHelp,#studioScreen')===L[i].closest('#detailPoster,#createSheet,#auraScreen,#auraHelp,#studioScreen'))) return L[i]; } } return null; }
  function el(){ var p=document.getElementById('murPhrase'); if(!p){ p=document.createElement('div'); p.id='murPhrase'; p.setAttribute('role','status'); var d=document.getElementById('device'); (d||document.body).appendChild(p); } return p; }
  /* v105 — AU CENTRE DU MUR TOUCHÉ (la part visible de son rectangle, dans l'appareil), en gros : 34 px, réduite par pas de 1 jusqu'à
     tenir en TROIS lignes au plus (plancher 18). Cotes en unités de l'appareil (390), l'échelle de .frame retirée. */
  var TAILLE_MAX=34, TAILLE_MIN=18, LIGNES=3, LH=1.16; function fsMinH(){ return Math.ceil(TAILLE_MIN*LH*LIGNES); }
  function pose(mur){ var p=el(), dv=document.getElementById('device'); if(!dv) return; var D=dv.getBoundingClientRect(), k=(D.width/390)||1;
    var r=mur?mur.getBoundingClientRect():D; var x0=Math.max(r.left,D.left), x1=Math.min(r.right,D.right), y0=Math.max(r.top,D.top), y1=Math.min(r.bottom,D.bottom);
    if(!(x1-x0>60 && y1-y0>40)){ x0=D.left; x1=D.right; y0=D.top; y1=D.bottom; }
    var w=Math.min(342, (x1-x0)/k-24), cx=((x0+x1)/2-D.left)/k, cy=((y0+y1)/2-D.top)/k;
    p.style.setProperty('width', w+'px','important'); p.style.setProperty('left',(cx-w/2)+'px','important');
    /* et elle tient dans la hauteur visible du mur : posée hors du flou, elle chevaucherait un texte net (vu dans l'Aura, un mur d'une rangée) */
    var dispo=Math.max(fsMinH(), (y1-y0)/k-8);
    var fs=TAILLE_MAX; for(;fs>TAILLE_MIN;fs--){ p.style.setProperty('font-size',fs+'px','important'); if(p.scrollHeight <= Math.ceil(fs*LH*LIGNES)+1 && p.scrollHeight <= dispo) break; }
    p.style.setProperty('font-size',fs+'px','important');
    var h=p.scrollHeight, top=cy-h/2, H=D.height/k; top=Math.max(24, Math.min(H-h-24, top));   /* jamais hors de l'appareil */
    p.style.setProperty('top',top+'px','important'); p.setAttribute('data-taille', fs); }
  /* v105 — SI LE MUR N'EST PAS ASSEZ À L'ÉCRAN pour porter la phrase (vu dans l'Aura : 70 px de « Ce qu'on t'a tenu » au bas de
     l'écran), on fait défiler SON conteneur pour l'amener au centre, puis on pose. Jamais la page entière : seul l'ancêtre qui défile. */
  function defilant(e){ for(var q=e&&e.parentElement;q&&q.id!=='device';q=q.parentElement){ var s=getComputedStyle(q); if(/(auto|scroll)/.test(s.overflowY) && q.scrollHeight>q.clientHeight+2) return q; } return null; }
  function amene(mur, fin){ var dv=document.getElementById('device'); if(!mur||!dv){ fin(); return; }
    var D=dv.getBoundingClientRect(), r=mur.getBoundingClientRect(), vis=Math.min(r.bottom,D.bottom)-Math.max(r.top,D.top);
    if(vis >= Math.min(r.height, 200)){ fin(); return; }
    var sc=defilant(mur); if(!sc){ fin(); return; }
    var delta=(r.top+r.height/2)-(D.top+D.height/2), cible=Math.max(0, Math.min(sc.scrollHeight-sc.clientHeight, sc.scrollTop+delta/((D.width/390)||1)));
    try{ sc.scrollTo({top:cible, behavior:'smooth'}); }catch(_){ sc.scrollTop=cible; }
    setTimeout(fin, 420); }
  /* v105 — « trop rapide : on n'a pas le temps de lire. Assez longtemps pour qu'on la lise sans se presser, sans que ce soit long. »
     Le temps de lecture se CALCULE sur la phrase : 1,4 s + 60 ms par caractère, entre 3 et 5,5 s. */
  function duree(t){ return Math.max(3000, Math.min(5500, 1400 + 60*t.length)); }
  window._murDuree=duree;
  function peint(t){ var p=el(); p.textContent=''; var parts=t.split(MP); parts.forEach(function(s,i){ if(s) p.appendChild(document.createTextNode(s)); if(i<parts.length-1){ var m=document.createElement('span'); m.className='mp'; m.textContent=MP; p.appendChild(m); } }); }
  function suivante(){ var o=lit(), now=Date.now(); if(!o.n || !o.t || now-o.t>ABSENCE){ o.n=0; o.der=null; }
    var i; if(o.n<PHRASES.length) i=o.n; else { do{ i=Math.floor(Math.random()*PHRASES.length); }while(PHRASES.length>1 && i===o.der); }
    o.n=(o.n||0)+1; o.t=now; o.der=i; var premiere=!o.decouvert; o.decouvert=1; ecrit(o); return {i:i, premiere:premiere}; }
  var leve=false, tAuto=null, tMontee=0;
  function monte(mur){ var s=suivante(), t=PHRASES[s.i]; leve=true; tMontee=performance.now(); clearTimeout(tAuto);
    amene(mur, function(){ peint(t); pose(mur); var p=el(); void p.offsetWidth; p.classList.add('leve'); tMontee=performance.now();
      var T=duree(t); window._murEtat={i:s.i, premiere:s.premiere, t:tMontee, duree:T};
      /* elle reste le temps d'être lue, puis s'efface ; la toute première fois, l'offre s'ouvre à la fin de cette lecture */
      clearTimeout(tAuto); tAuto=setTimeout(s.premiere ? offre : baisse, T); }); }
  function baisse(){ clearTimeout(tAuto); var p=document.getElementById('murPhrase'); if(p) p.classList.remove('leve'); leve=false; }
  function offre(){ baisse(); try{ if(window._cercleDessus) window._cercleDessus(); else if(typeof ouvreCercle==='function') ouvreCercle(); }catch(_){} }
  window._murBaisse=baisse; window._murOffre=offre;
  /* ⚠ UN TOUCHER, PAS UN CLIC : sur le Peaufiner, la fin du geste est annulée par ses propres écouteurs — le navigateur ne
     synthétise AUCUN clic (mesuré en WebKit, au doigt). On lit donc le toucher : appui puis lever, sans glisser (< 10 px, < 600 ms).
     Le clic qui peut suivre (souris, ou clic synthétisé ailleurs) est AVALÉ s'il tombe sous 700 ms. */
  var d0=null, avaleJusque=0;
  function agit(x,y,ev){
    if(leve){ var ps=document.getElementById('plusScreen'); if(ps&&ps.classList.contains('show')){ baisse(); return false; }
      if(performance.now()-tMontee<450) return true;   /* le toucher qui l'a fait paraître ne l'emporte pas */
      offre(); return true; }
    var m=dans(x,y); if(!m) return false; monte(m); return true; }
  window.addEventListener('pointerdown', function(ev){ d0={x:ev.clientX,y:ev.clientY,t:performance.now(),id:ev.pointerId}; }, true);
  window.addEventListener('pointerup', function(ev){ var d=d0; d0=null; if(!d||d.id!==ev.pointerId) return;
    if(Math.hypot(ev.clientX-d.x, ev.clientY-d.y)>10 || performance.now()-d.t>600) return;
    if(agit(ev.clientX, ev.clientY, ev)){ avaleJusque=performance.now()+700; ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  window.addEventListener('click', function(ev){ if(performance.now()<avaleJusque){ avaleJusque=0; ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  /* la phrase ne survit pas à l'écran qui l'a fait monter (CLAUDE §8) */
  (window._rangeurs=window._rangeurs||[]).push(baisse);
})();
