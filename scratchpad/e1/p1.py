import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
LOT = r"""<style id="lot-E1-GESTES-css">
/* ⚑ E1 (C-074) — LA MAIN FANTÔME. Une couche posée AU-DESSUS de l'écran, dans l'appareil : elle ne prend aucun toucher, ne touche à aucun
   canevas et ne fait bouger aucune dalle (A1). Aucune opacité, aucune transition, aucune animation CSS (A2) : elle paraît et disparaît d'un coup. */
#device #gesteFantome{position:absolute;left:0;top:0;width:390px;height:844px;z-index:9400;pointer-events:none;overflow:hidden;margin:0;padding:0;max-width:none}
#device #gesteFantome svg{position:absolute;left:0;top:0;display:block;max-width:none;overflow:visible}
</style>
<script id="lot-E1-GESTES">
/* ⚑ E1 (Tom, 10 oct. 2026, C-074) — LES GESTES APPRIS EN SITUATION (ENGAGEMENT.md, E1 ; les amendements priment).
   « Chaque geste s'apprend une fois, au moment exact où il devient utile, en le voyant faire — jamais dans un tutoriel en amont. »
   UN SEUL COMPOSANT, `GesteFantome` : `montrer(idGeste, elementCible, chemin)` et `oublier(idGeste)`.
   · la main paraît après 600 ms sans toucher sur l'écran concerné, joue le geste DEUX fois au plus (900 ms de pause), disparaît au premier
     toucher n'importe où ; le drapeau `geste_vu_<id>` est posé DÈS la première apparition : plus jamais, sauf « Revoir les gestes » ;
   · A2 : au trait plein, OPAQUE, à l'encre du mode ; ni transparence ni fondu — elle paraît et disparaît en une image ; elle porte `data-eng` ;
   · A1 : elle se dessine au-dessus de l'écran ; rien n'est posé sur la Toile, aucune dalle ne bouge ;
   · « Réduire les animations » : la main est IMMOBILE au départ du geste, avec une flèche du trajet ; aucune animation ;
   · A3 : aucun texte à l'impératif — le seul mot du lot est le libellé de l'entrée de rejeu, dans `TEXTES_ENGAGEMENT`.
   L'INVENTAIRE (`GesteFantome.inventaire()`) : chaque geste, son écran, sa condition, s'il est branché. */
(function(){
  var T=window.TEXTES_ENGAGEMENT=window.TEXTES_ENGAGEMENT||{};
  T.gestes_rejeu='Revoir les gestes';        /* TEXTE PROVISOIRE — Tom */
  T.gestes_rejeu_valeur='revoir ›';          /* TEXTE PROVISOIRE — Tom */
  T.gestes_rejeu_fait='c’est remis ›';       /* TEXTE PROVISOIRE — Tom */
  var INACTIF=600, PAUSE=900, TOURS=2, PRE='geste_vu_';
  function $(i){ return document.getElementById(i); }
  function dev(){ return $('device'); }
  function vu(id){ try{ return localStorage.getItem(PRE+id)==='1'; }catch(_){ return false; } }
  function marque(id){ try{ localStorage.setItem(PRE+id,'1'); }catch(_){ } }
  function reduit(){ try{ return !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }catch(_){ return false; } }
  function clair(){ var d=dev(); return !!(d && d.classList.contains('light')); }
  /* des points de l'écran (client) vers les points de l'appareil (390 × 844) */
  function versAppareil(P){ var d=dev().getBoundingClientRect(), k=d.width/390||1; return P.map(function(p){ var o={x:(p.x-d.left)/k, y:(p.y-d.top)/k}; if(p.appui) o.appui=p.appui; return o; }); }
  var NS='http://www.w3.org/2000/svg';
  function svg(n, a){ var e=document.createElementNS(NS,n); for(var k in a) e.setAttribute(k,a[k]); return e; }
  /* la main : un index tendu, le bout du doigt au point (17 ; 2) de son dessin */
  var MAIN='M13 4.5a4 4 0 0 1 8 0v15.2l8.6 1.9a5.2 5.2 0 0 1 4.1 5.1v9.3a11.5 11.5 0 0 1-11.5 11.5h-4.4a11.5 11.5 0 0 1-9.6-5.2l-6.7-10.4a3.5 3.5 0 0 1 5.7-4.1l5.8 6.4z';
  var A=null;   /* le geste en cours : {id, pts, couche, main, t0, tours, raf} */
  function couche(){ var c=$('gesteFantome'); if(c) return c; c=document.createElement('div'); c.id='gesteFantome'; c.setAttribute('data-eng','geste-fantome'); c.setAttribute('aria-hidden','true'); dev().appendChild(c); return c; }
  function arrete(){ if(!A) return; try{ cancelAnimationFrame(A.raf); }catch(_){ } clearTimeout(A.tm); var c=$('gesteFantome'); if(c && c.parentNode) c.parentNode.removeChild(c); A=null; }
  function longueurs(P){ var s=[0]; for(var i=1;i<P.length;i++) s.push(s[i-1]+Math.hypot(P[i].x-P[i-1].x, P[i].y-P[i-1].y)); return s; }
  function place(m, x, y, pose){ m.setAttribute('transform','translate('+(x-17).toFixed(1)+' '+(y-2+(pose?0:-7)).toFixed(1)+')'); }
  function montrer(id, cible, chemin){
    if(!id || !chemin || !chemin.length || !dev()) return false; arrete();
    var P=versAppareil(chemin), enc=clair()?'#201908':'#F7F0DE', fond=clair()?'#F7F0DE':'#050302';
    var c=couche(), s=svg('svg',{width:390, height:844, viewBox:'0 0 390 844'}); c.appendChild(s);
    c.setAttribute('data-geste', id); c.setAttribute('data-mode', reduit()?'immobile':'anime');
    var L=longueurs(P), tot=L[L.length-1], appui=P[0].appui||0;
    if(reduit()){
      /* immobile : la flèche du trajet (s'il y en a un), puis la main posée à son départ */
      if(tot>6){ var d='M'+P.map(function(p){ return p.x.toFixed(1)+' '+p.y.toFixed(1); }).join(' L'), b=P[P.length-1], a=P[Math.max(0,P.length-2)], vx=b.x-a.x, vy=b.y-a.y, n=Math.hypot(vx,vy)||1; vx/=n; vy/=n;
        function aile(g){ var q=g*Math.PI/180; return (b.x-(vx*Math.cos(q)-vy*Math.sin(q))*12).toFixed(1)+' '+(b.y-(vx*Math.sin(q)+vy*Math.cos(q))*12).toFixed(1); }
        s.appendChild(svg('path',{d:d, fill:'none', stroke:fond, 'stroke-width':7, 'stroke-linecap':'round', 'stroke-linejoin':'round'}));
        s.appendChild(svg('path',{d:d, fill:'none', stroke:enc, 'stroke-width':3, 'stroke-linecap':'round', 'stroke-linejoin':'round', 'data-fleche':'1'}));
        s.appendChild(svg('path',{d:'M'+aile(-32)+' L'+b.x.toFixed(1)+' '+b.y.toFixed(1)+' L'+aile(32), fill:'none', stroke:enc, 'stroke-width':3, 'stroke-linecap':'round', 'stroke-linejoin':'round'})); }
      var m0=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m0); place(m0, P[0].x, P[0].y, true);
      A={id:id, pts:P, immobile:true}; marque(id); return true; }
    var m=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m); place(m, P[0].x, P[0].y, false);
    var AVANT=260, D=tot>6 ? Math.max(700, Math.min(1500, tot*5)) : 0, APRES=260, UN=AVANT+appui+D+APRES;
    A={id:id, pts:P, main:m, t0:performance.now(), tours:0}; marque(id);
    function pos(u){ var d=u*tot, i=1; while(i<L.length-1 && L[i]<d) i++; var a=P[i-1], b=P[i]||a, seg=(L[i]-L[i-1])||1, f=Math.max(0,Math.min(1,(d-L[i-1])/seg)); return {x:a.x+(b.x-a.x)*f, y:a.y+(b.y-a.y)*f}; }
    function image(){ if(!A || A.id!==id) return; var t=performance.now()-A.t0;
      if(t>=UN){ A.tours++; if(A.tours>=TOURS){ arrete(); return; }
        m.setAttribute('visibility','hidden'); A.tm=setTimeout(function(){ if(!A || A.id!==id) return; A.t0=performance.now(); m.setAttribute('visibility','visible'); place(m, P[0].x, P[0].y, false); A.raf=requestAnimationFrame(image); }, PAUSE); return; }
      if(t<AVANT) place(m, P[0].x, P[0].y, t>AVANT*0.5);
      else if(t<AVANT+appui) place(m, P[0].x, P[0].y, true);
      else if(t<AVANT+appui+D){ var u=(t-AVANT-appui)/D; u=u*u*(3-2*u); var q=pos(u); place(m, q.x, q.y, true); }
      else { var e=P[P.length-1]; place(m, e.x, e.y, t<AVANT+appui+D+APRES*0.5); }
      A.raf=requestAnimationFrame(image); }
    A.raf=requestAnimationFrame(image); return true; }
  function oublier(id){ try{ localStorage.removeItem(PRE+id); }catch(_){ } if(A && A.id===id) arrete(); }
  function oublierTout(){ try{ Object.keys(localStorage).forEach(function(k){ if(k.indexOf(PRE)===0) localStorage.removeItem(k); }); }catch(_){ } arrete(); relance(); }

  /* ══ L'INVENTAIRE. `quand()` rend {cible, chemin} (points de l'ÉCRAN) quand le geste devient utile, sinon rien. ══ */
  function devant(sel){ var e=typeof sel==='string'?document.querySelector(sel):sel, d=dev(); if(!e || !d) return false; var r=d.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height*0.6); return !!(h && e.contains(h)); }
  function rect(e){ if(!e) return null; var r=e.getBoundingClientRect(); return (r.width>8 && r.height>8) ? r : null; }
  function k(){ return dev().getBoundingClientRect().width/390||1; }
  function onde(cv, base, amp, x0, x1){ var r=rect(cv), f; try{ f=window._onde.onde(base, amp); }catch(_){ return null; } if(!r || !f) return null; var kk=r.width/390, P=[];
    for(var x=x0; x<=x1+0.1; x+=11) P.push({x:r.left+x*kk, y:r.top+f(x)*kk}); return P; }
  function fiche(){ var dp=$('detailPoster'); if(!dp || !dp.classList.contains('show') || !devant(dp)) return null; if(dp.classList.contains('s2-ouv') || $('dessinMode') || $('vueEntiere')) return null;
    if(dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee')) return null; try{ if(typeof cur==='undefined' || !cur || cur.draft) return null; return {dp:dp, p:cur}; }catch(_){ return null; } }
  function traitFiche(chiche){ var F=fiche(); if(!F || F.p.status==='tenu' || !!F.p.chiche!==chiche) return null; var cv=$('dpTrameCv'), t=cv && (cv.getAttribute('data-trait')||'').split(','); if(!t || t.length<4) return null;
    var P=onde(cv, +t[0], +t[1], 30, t[3]==='moitie' ? 195 : 360); return P ? {cible:$('tenirZone'), chemin:P} : null; }
  var GESTES=[
   {id:'tenir', ecran:'la fiche d’un Promi', quand_dit:'la fiche est ouverte sur un Promi pas encore tenu', geste:'tracer le trait, du rond de gauche vers le milieu', branche:true, quand:function(){ return traitFiche(false); }},
   {id:'chiche', ecran:'la fiche d’un Chiche', quand_dit:'la fiche est ouverte sur un Chiche pas encore tenu', geste:'tracer sa moitié du trait', branche:true, quand:function(){ return traitFiche(true); }},
   {id:'planter', ecran:'la page +', quand_dit:'la page + est ouverte sur une nature (Promi, Chiche ou Cercle), Peaufiner fermé', geste:'tracer le trait pour planter (entier pour un Cercle)', branche:true, quand:function(){
      var cs=$('createSheet'); if(!cs || !cs.classList.contains('show') || !cs.classList.contains('pp') || cs.classList.contains('pp-choix') || cs.classList.contains('pp-peauf') || !devant(cs) || $('dessinMode')) return null;
      var e=null; try{ e=window._ppEcran && window._ppEcran(); }catch(_){ } var cv=$('csTrameCv'); if(!e || !cv || !e.base) return null;
      var P=onde(cv, e.base, e.amp, 30, e.nat==='nuee' ? 360 : 195); return P ? {cible:cs, chemin:P} : null; }},
   {id:'pelote', ecran:'l’Aura', quand_dit:'l’Aura est ouverte, la Pelote est à l’écran', geste:'poser le doigt sur la Pelote et glisser : elle se creuse et tourne', branche:true, quand:function(){
      var sc=$('auraScreen'), bo=$('auBoule'); if(!sc || !bo || !sc.classList.contains('show') || !devant(sc)) return null; var r=rect(bo); if(!r || r.top<dev().getBoundingClientRect().top) return null;
      var cx=r.left+r.width/2, cy=r.top+r.height/2, w=r.width*0.17; return {cible:bo, chemin:[{x:cx-w, y:cy+w*0.25, appui:260},{x:cx-w*0.3, y:cy},{x:cx+w, y:cy-w*0.25}]}; }},
   {id:'noyau', ecran:'Partager', quand_dit:'le Noyau est affiché sur l’image à partager (hors Mon Folio)', geste:'appui long (260 ms) sur le Noyau, puis le déplacer', branche:true, quand:function(){
      var sc=$('shareScreen'), cv=$('shCanvas'); if(!sc || !cv || !sc.classList.contains('show') || !window.shNoyau || !devant(sc)) return null; try{ if(typeof shareMode!=='undefined' && shareMode!=='toile') return null; }catch(_){ }
      var r=rect(cv); if(!r) return null; var x=r.left+r.width*(window.shNyX===undefined?0.5:window.shNyX), y=r.top+r.height*(window.shNyY===undefined?0.5:window.shNyY);
      return {cible:cv, chemin:[{x:x, y:y, appui:420},{x:x-r.width*0.10, y:y-r.height*0.07},{x:x-r.width*0.18, y:y-r.height*0.16}]}; }},
   {id:'fil', ecran:'le Fil', quand_dit:'le Fil est ouvert et porte au moins un bandeau', geste:'appui maintenu sur un bandeau : il déplie ce qu’on peut y faire', branche:true, quand:function(){
      var fv=$('feedView'); if(!fv || !devant(fv)) return null; var c=fv.querySelector('.s4-carte'), r=rect(c); if(!r) return null; return {cible:c, chemin:[{x:r.left+r.width*0.5, y:r.top+r.height*0.55, appui:900}]}; }},
   {id:'studio-monde', ecran:'le Studio', quand_dit:'le Studio est ouvert', geste:'glisser de côté sur la Toile : le monde suivant', branche:true, quand:function(){
      var sc=$('studioScreen'), bg=$('stBg'); if(!sc || !bg || !devant(sc)) return null; var r=rect(bg), d=dev().getBoundingClientRect(); if(!r) return null; var y=d.top+d.height*0.36;
      return {cible:bg, chemin:[{x:d.left+d.width*0.70, y:y},{x:d.left+d.width*0.50, y:y-6*k()},{x:d.left+d.width*0.30, y:y}]}; }},
   {id:'studio-couleur', ecran:'le Studio', quand_dit:'le Studio est ouvert, le glissement de monde déjà montré', geste:'appui maintenu (480 ms) puis glisser : de côté la teinte, de haut en bas la palette', branche:true, quand:function(){
      if(!vu('studio-monde')) return null; var sc=$('studioScreen'), bg=$('stBg'); if(!sc || !bg || !devant(sc)) return null; var d=dev().getBoundingClientRect(), y=d.top+d.height*0.36;
      return {cible:bg, chemin:[{x:d.left+d.width*0.40, y:y, appui:620},{x:d.left+d.width*0.52, y:y},{x:d.left+d.width*0.64, y:y}]}; }},
   {id:'bande', ecran:'la fiche (Promi, Chiche, Cercle)', quand_dit:'la bande haute porte une photo ou un dessin posé', geste:'toucher la bande : la photo ou le dessin en entier', branche:true, quand:function(){
      var dp=$('detailPoster'); if(!dp || !dp.classList.contains('show') || !devant(dp) || dp.classList.contains('s2-ouv') || $('dessinMode') || $('vueEntiere')) return null;
      var a=false; try{ a=!!(window._dessin && window._dessin.visible && window._dessin.visible()) || !!(typeof cur!=='undefined' && cur && cur.photo); }catch(_){ } if(!a) return null;
      try{ if(typeof cur!=='undefined' && cur && cur.status!=='tenu' && !vu(cur.chiche?'chiche':'tenir')) return null; }catch(_){ }   /* le trait d'abord */
      var d=dev().getBoundingClientRect(); return {cible:dp, chemin:[{x:d.left+d.width*0.5, y:d.top+d.height*0.19, appui:240}]}; }},
   {id:'dessin', ecran:'le mode dessin', quand_dit:'le mode dessin est ouvert, la surface encore vide', geste:'tracer sur la surface', branche:true, quand:function(){
      var md=$('dessinMode'), s=md && md.querySelector('.dz-surface'); if(!s || !devant(md)) return null; try{ var e=window._dessin.etat(); if(e && e.traits>0) return null; }catch(_){ } var r=rect(s); if(!r) return null;
      var P=[], n=14; for(var i=0;i<=n;i++){ var u=i/n; P.push({x:r.left+r.width*(0.28+0.44*u), y:r.top+r.height*(0.42+0.07*Math.sin(u*Math.PI*2))}); } return {cible:s, chemin:P}; }},
   /* ── recensés, NON branchés ── */
   {id:'aura-apparait', ecran:'l’accueil', quand_dit:'l’Aura paraît dans la barre (au premier tenu)', geste:'la main désigne l’Aura', branche:false, raison:'appartient à E2bis (C-076) : l’identifiant est réservé, rien n’est branché'},
   {id:'pelote-folio', ecran:'Partager · Mon Folio', quand_dit:'la Pelote est posée dans le Folio', geste:'appui long (380 ms) sur la Pelote, puis la déplacer', branche:false, raison:'le Folio ne publie pas la place de la Pelote à l’écran : la main ne saurait pas où se poser'},
   {id:'toile-pince', ecran:'l’accueil', quand_dit:'la Toile est à l’écran', geste:'pincer pour approcher ou reculer ; double toucher pour recadrer', branche:false, raison:'geste à deux doigts, et sur la Toile : la main fantôme n’a qu’un doigt, et rien ne se pose sur la Toile (A1)'},
   {id:'fiche-cercle-defile', ecran:'la fiche d’un Cercle', quand_dit:'le fil du Cercle dépasse l’écran', geste:'glisser vers le haut : le fil défile', branche:false, raison:'un défilement ordinaire, pas un geste à apprendre'}
  ];
  /* ══ LE GUET : rien ne tourne tant qu'il ne reste aucun geste branché à montrer. ══ */
  var dernier=performance.now(), cand=null, candT=0, guet=null;
  function reste(){ return GESTES.some(function(g){ return g.branche && !vu(g.id); }); }
  function onb(){ var o=$('promiOnb'); return !!(o && !o.classList.contains('gone') && getComputedStyle(o).display!=='none'); }
  function tic(){ if(A && !A.immobile) return; if(document.hidden || onb() || $('tutoOv')){ cand=null; return; }
    var trouve=null; for(var i=0;i<GESTES.length;i++){ var g=GESTES[i]; if(!g.branche || vu(g.id)) continue; var q=null; try{ q=g.quand(); }catch(_){ q=null; } if(q){ trouve={g:g, q:q}; break; } }
    if(A && A.immobile){ if(!trouve || trouve.g.id!==A.id){ var encore=null; try{ var ga=GESTES.filter(function(x){ return x.id===A.id; })[0]; encore=ga && ga.quand_immobile ? ga.quand_immobile() : null; }catch(_){ } } return; }
    if(!trouve){ cand=null; if(!reste()){ clearInterval(guet); guet=null; } return; }
    var t=performance.now(); if(cand!==trouve.g.id){ cand=trouve.g.id; candT=t; return; }
    if(t-candT>=INACTIF && t-dernier>=INACTIF){ cand=null; montrer(trouve.g.id, trouve.q.cible, trouve.q.chemin); } }
  function relance(){ if(!guet && reste()) guet=setInterval(tic, 200); }
  ['pointerdown','touchstart','keydown','wheel'].forEach(function(n){ document.addEventListener(n, function(){ dernier=performance.now(); cand=null; if(A) arrete(); }, {capture:true, passive:true}); });
  /* un écran qui change sous une main immobile (mouvement réduit) : elle part avec lui */
  setInterval(function(){ if(!A || !A.immobile) return; var g=GESTES.filter(function(x){ return x.id===A.id; })[0], q=null; try{ q=g && g.quand ? g.quand() : null; }catch(_){ } if(!q) arrete(); }, 400);
  window.GesteFantome={montrer:montrer, oublier:oublier, oublierTout:oublierTout, arrete:arrete,
    inventaire:function(){ return GESTES.map(function(g){ return {id:g.id, ecran:g.ecran, condition:g.quand_dit, geste:g.geste, branche:!!g.branche, raison:g.raison||'', vu:vu(g.id)}; }); },
    etat:function(){ return A ? {id:A.id, immobile:!!A.immobile, tours:A.tours||0} : null; }, regle:{INACTIF:INACTIF, PAUSE:PAUSE, TOURS:TOURS}};
  relance();

  /* ══ LE REJEU (E1, point 4) : « le point d'entrée existant de obReplay devient “Revoir les gestes” et efface les drapeaux geste_vu_*.
        Ne pas créer d'autre entrée, ne rien ajouter au Studio. » La rangée `#replayOnb` des Réglages change de mot et de rôle ; elle ne
        relance plus la présentation. On lit le geste (aux Réglages un toucher ne produit pas toujours de `click`, v137). ══ */
  function rejeu(){ var c=$('replayOnb'); if(!c || c.getAttribute('data-e1')) return !!c; c.setAttribute('data-e1','1'); c.setAttribute('role','button'); c.tabIndex=0;
    var kk=c.querySelector('.k'), v=c.querySelector('.v'); if(kk) kk.textContent=T.gestes_rejeu; if(v) v.textContent=T.gestes_rejeu_valeur; c.setAttribute('aria-label', T.gestes_rejeu);
    var G=null, tF=0;
    function fait(e){ if(e){ try{ e.preventDefault(); e.stopImmediatePropagation(); }catch(_){ } } if(performance.now()-tF<500) return; tF=performance.now(); oublierTout(); if(v){ v.textContent=T.gestes_rejeu_fait; setTimeout(function(){ v.textContent=T.gestes_rejeu_valeur; }, 2400); } }
    c.onclick=null;
    c.addEventListener('pointerdown', function(e){ G={x:e.clientX, y:e.clientY, t:performance.now()}; }, true);
    c.addEventListener('pointerup', function(e){ var g=G; G=null; if(!g || Math.hypot(e.clientX-g.x, e.clientY-g.y)>10 || performance.now()-g.t>600) return; fait(e); }, true);
    c.addEventListener('click', fait, true);
    c.addEventListener('keydown', function(e){ if(e.key==='Enter' || e.key===' ') fait(e); });
    return true; }
  if(!rejeu()){ var n=0, t=setInterval(function(){ if(rejeu() || ++n>40) clearInterval(t); }, 250); }
})();
</script>
"""
a='<style id="lot-V137-MENTION-css">'
r(a, LOT+a)
io.open('app.html','w',encoding='utf-8').write(S)
