# -*- coding: utf-8 -*-
import io
P='app.html'; S=io.open(P,encoding='utf-8').read()
# ── le CSS : on garde « Plus tard » et le mot de trace de l'onboarding ; le guide est réécrit
i=S.index("/* le guide */\n#device #guide{position:absolute;"); j=S.index("</style>\n<script id=\"lot-V141-GUIDE\">", i)
CSS = """/* le guide — ⚑ v146 (C-094, 2e récidive) : DES FLAQUES. Plus de `backdrop-filter`, plus de formes, plus de loupe : un canevas (`#guideEau`) montre
   l'accueil flouté à l'avance là où il y a de l'eau ; la zone nette est un trou dans l'eau, par où l'on voit l'accueil VRAI. Aucune transition,
   aucune animation CSS (A2). */
#device #guide{position:absolute;left:0;top:0;width:390px;height:844px;z-index:69;/* SOUS les écrans (70) : le Studio s'ouvre par-dessus */margin:0;padding:0;max-width:none;overflow:hidden;background:transparent}
#device #guideEau{position:absolute;left:0;top:0;width:390px;height:844px;margin:0;padding:0;max-width:none;pointer-events:none;display:block}
/* la phrase (§11.7, Tom) : plus grosse (34 px, 30 avant), AUCUN contour ; les mots-clés en PromiLate. En clair : le violet #291547, les
   mots-clés en #0E78F2, les natures dans leur couleur (posée en ligne, la règle de l'onboarding) ; en sombre : la crème d'aujourd'hui. */
#device #guidePhrase{position:absolute;left:30px;width:330px;margin:0;padding:0;max-width:none;text-align:center;text-wrap:balance;pointer-events:none;
  font-family:var(--f-libelle);font-weight:700;font-size:34px;line-height:1.14;color:var(--c-creme95);-webkit-text-fill-color:var(--c-creme95);text-shadow:none;-webkit-text-stroke:0}
#device.light #guidePhrase:not(:where(#detailPoster,#detailPoster *,#createSheet,#createSheet *,.th-sombre,.th-sombre *)){color:var(--c-mauve12);-webkit-text-fill-color:var(--c-mauve12)}
#device #guidePhrase .gd-cle{font-family:var(--f-marque);font-weight:400;font-size:.86em;text-transform:uppercase;letter-spacing:.01em;font-style:normal}
#device.light #guidePhrase .gd-cle:not(:where(#detailPoster,#detailPoster *,#createSheet,#createSheet *,.th-sombre,.th-sombre *)){color:var(--c-cobalt50);-webkit-text-fill-color:var(--c-cobalt50)}
#device #guidePhrase .gd-nat{font-style:normal}
#device #guide, #device #guide *{transition:none!important;animation:none!important}
"""
S=S[:i]+CSS+S[j:]
# ── le script
i=S.index("<script id=\"lot-V141-GUIDE\">"); j=S.index("</script>", i)+len("</script>")
JS = r"""<script src="variantes/flaques.js"></script>
<script id="lot-V141-GUIDE">
/* ⚑ v146 (Tom, 14 oct. 2026 — C-094, 2e RÉCIDIVE) — LE GUIDE D'ACCUEIL : DES FLAQUES. (L'écriture de v144 : sauvegardes/app-avant-v146.html.)
   LA CAUSE DE LA RÉCIDIVE, écrite avant le code : la demande portait sur une MATIÈRE vivante, aléatoire et ciblée ; la livraison a été une
   DÉCOUPE géométrique, trop large, qui se déplace. v144 : six ellipses à bord doux qui grandissent ensemble, puis une loupe RONDE qui GLISSE du
   Studio au + (« ça arrive tout d'un coup, puis ça se fixe sur le Studio et ça se translate sur un axe horizontal ») ; v145, sur la page de
   variantes : des nappes, un disque parfait autour du Studio qui montrait l'Aura et l'encart, des lettres cernées. Aucun juge ne regardait la
   NATURE du mouvement : ils mesuraient qu'un masque grandissait et qu'une icône était nette.
   CE QUE TOM VEUT, étape par étape (les durées : `Flaques.GUIDE`, les mêmes que la page promi-guide-variantes.html?flaques=1) :
   4.1 LA COUVERTURE — des flaques de flou naissent au hasard, grossissent, se rejoignent, couvrent l'écran (1,4 s) ;
   4.2 LA PHRASE paraît, sans aucun contour (ses lettres se traceront par le module de §13 quand Tom l'aura vu : `?trace=1` le montre déjà) ;
   4.3 LE STUDIO — la zone nette paraît par les mêmes flaques, plus petites, DANS un entourage à peine irrégulier, serré sur l'icône et son
       mot : on ne voit ni l'Aura ni le contour de la barre (0,7 s) ;
   4.4 elle DISPARAÎT sur elle-même, par le même effet à l'envers (0,7 s) ;
   4.5 LE + : pareil, sur le + seul ;
   4.6 LA FIN : les flaques se vident (1,2 s).
   Interdit : disque ou ellipse parfaits, translation, tout ce qui arrive d'un coup, contour sur les lettres.
   LA TECHNIQUE : aucun `backdrop-filter`. L'accueil est flouté À L'AVANCE, une fois (la Toile est recopiée de son canevas ; le plateau et la
   barre sont repeints depuis leurs cotes et leurs styles calculés ; trois moyennes glissantes valent le flou des murs, 4,8 pt). À chaque
   image, le contour du niveau de l'eau est tracé en vecteurs et découpe cette image ; la zone nette est un TROU : on y voit l'accueil vrai,
   net, et c'est lui qu'on touche. Le moteur des flaques est variantes/flaques.js (un seul fichier pour l'app et pour la page).
   Ce qui ne change pas : le moment (l'accueil posé, 0,6 s de calme), les chemins (le Studio touché s'ouvre par-dessus ; l'étape du + vient
   toujours ensuite ; toucher ailleurs fait avancer ; au +, toucher ailleurs finit), aucun « Plus tard » (R6, exception nommée), la phrase du
   Studio (A3, exception nommée). Aucune opacité, aucun fondu, aucune transition CSS (l'exception de A2 de v143 n'a plus d'objet). Tout nœud
   porte `data-eng`. */
(function(){
  var T=window.TEXTES_ENGAGEMENT=window.TEXTES_ENGAGEMENT||{};
  /* TEXTE — Tom (lot v143) */
  T.guide={ studio:'Choisis d’abord le monde qui te ressemble, au Studio.',
            plus:'Promi, Chiche ou Cercle : tout commence par ce +.' };
  /* §11.7 — les mots-clés (PromiLate, en couleur) : « Studio » et « monde » dans la phrase du Studio ; le mot qui nomme l'action dans celle du + */
  T.guideCles={ studio:['monde','Studio'], plus:['commence'] };
  T.imperatifVoulu=(T.imperatifVoulu||[]).concat([T.guide.studio]);   /* A3 : l'exception nommée, lue par redteam_engagement et redteam_guide */
  T.sansPlusTard=true;                                                  /* R6 : l'exception nommée (Tom, v144) */
  function $(i){ return document.getElementById(i); }
  var dev=$('device'); if(!dev) return;
  var F=window.Flaques, GD=(F&&F.GUIDE)||{};
  var CLE='promi_guide', ATTENTE=GD.ATTENTE||600, COUVRE=GD.COUVRE||1400, OUVRE=GD.OUVRE||700, FERME=GD.FERME||700, RETIRE=GD.RETIRE||1200, FLOU=GD.FLOU||4.8, RETOUR=450;
  var LS={g:function(k){ try{ return localStorage.getItem(k); }catch(_){ return null; } }, s:function(k,v){ try{ localStorage.setItem(k,v); }catch(_){ } }};
  function reduit(){ try{ return !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }catch(_){ return false; } }
  function onbOuvert(){ var o=$('promiOnb'); return !!($('onbV') || (o && !o.classList.contains('gone') && getComputedStyle(o).display!=='none')); }
  function accueil(){ try{ if(onbOuvert()) return false; var r=dev.getBoundingClientRect(), E=document.elementsFromPoint(r.left+r.width/2, r.top+r.height*0.45);
      for(var i=0;i<E.length;i++){ var h=E[i]; if(h.closest && h.closest('#guide')) continue; return !(h.closest && h.closest('.screen, .sheet, .poster, #feedView, #entierVue, #dessinMode, #accRappelCompte')); } return false; }catch(_){ return false; } }
  /* l'accueil est POSÉ : la Toile ne tourne plus, aucune parole n'arrive ni ne part, aucun doigt à l'instant */
  var tDoigt=0, doigt=0; ['pointerdown','touchstart','touchmove','touchend','pointerup','wheel','keydown'].forEach(function(n){ document.addEventListener(n,function(e){ tDoigt=performance.now(); if(n==='touchstart'||n==='pointerdown') doigt=1; if(n==='touchend'||n==='pointerup') doigt=0; },{capture:true,passive:true}); });
  function calme(){ try{ var st=window.Toile_state&&window.Toile_state(); if(st&&st.running) return false; }catch(_){ }
    if(window._tirageActive || doigt) return false; return performance.now()-tDoigt>250; }
  var etat=null, attente=null, tAcc=0, trou=null, tVu=0, vuStudio=false, tPose=0, SC=null, jeu=0, ou='studio', uC=0, uN=0, vivAv=null, traceCtl=null;
  var TRACE=false; try{ TRACE=/[?&]trace=1(&|$)/.test(location.search); }catch(_){ }
  function k(){ return (dev.getBoundingClientRect().width/390)||1; }
  function eng(n, quoi){ n.setAttribute('data-eng', quoi); return n; }
  function boite(e){ var D=dev.getBoundingClientRect(), kk=k(), r=e.getBoundingClientRect(); return [ (r.left-D.left)/kk, (r.top-D.top)/kk, r.width/kk, r.height/kk ]; }
  /* ce qu'on VOIT d'une entrée de la barre : son icône et son mot */
  function vu(cible){ var D=dev.getBoundingClientRect(), kk=k(), x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
    [].forEach.call(cible.querySelectorAll('svg, .l'), function(e){ var q=e.getBoundingClientRect(); if(q.width<2) return; x0=Math.min(x0,(q.left-D.left)/kk); x1=Math.max(x1,(q.right-D.left)/kk); y0=Math.min(y0,(q.top-D.top)/kk); y1=Math.max(y1,(q.bottom-D.top)/kk); });
    if(!(x1>x0)) return boite(cible); return [x0, y0, x1-x0, y1-y0]; }

  /* ── L'ACCUEIL, FLOUTÉ À L'AVANCE ───────────────────────────────────────────────────────────────────────────────────────────────
     La Toile est recopiée de son canevas. Le plateau, la barre (et le rappel du compte s'il est là) sont repeints nœud par nœud : fond,
     contour, coins, pseudo-éléments (l'anneau et le disque du +), dessins, textes — à leurs cotes et à leurs styles CALCULÉS. Tout sera
     flouté à 4,8 pt : c'est une image de fond, jamais ce qu'on lit (ce qu'on lit, c'est l'accueil vrai, par le trou). */
  function accueilImage(){
    var c=document.createElement('canvas'); c.width=390; c.height=844; var x=c.getContext('2d'), D=dev.getBoundingClientRect(), kk=k(), P=[];
    function R(e){ var q=e.getBoundingClientRect(); return [(q.left-D.left)/kk,(q.top-D.top)/kk,q.width/kk,q.height/kk]; }
    function opaque(col){ var m=/rgba?\(([^)]+)\)/.exec(col||''); if(!m) return false; var p=m[1].split(','); return p.length<4 || parseFloat(p[3])>0.02; }
    function rond(X,Y,W,H,r){ r=Math.max(0,Math.min(r,W/2,H/2)); x.beginPath(); x.moveTo(X+r,Y); x.arcTo(X+W,Y,X+W,Y+H,r); x.arcTo(X+W,Y+H,X,Y+H,r); x.arcTo(X,Y+H,X,Y,r); x.arcTo(X,Y,X+W,Y,r); x.closePath(); }
    function rayon(cs, W, H){ var v=cs.borderTopLeftRadius||'0'; return /%/.test(v) ? parseFloat(v)/100*Math.min(W,H) : (parseFloat(v)||0); }
    function image(src, b){ P.push(new Promise(function(ok){ var im=new Image(); im.onload=function(){ try{ x.drawImage(im, b[0], b[1], b[2], b[3]); }catch(_){ } ok(); }; im.onerror=function(){ ok(); }; im.src=src; })); }
    function caisse(cs, b){ var r=rayon(cs, b[2], b[3]), bw=parseFloat(cs.borderTopWidth)||0;
      if(opaque(cs.backgroundColor)){ rond(b[0],b[1],b[2],b[3],r); x.fillStyle=cs.backgroundColor; x.fill(); }
      var bi=/url\(["']?(data:[^"')]+)["']?\)/.exec(cs.backgroundImage||''); if(bi) image(bi[1], b);
      if(bw>0.2 && cs.borderTopStyle!=='none' && opaque(cs.borderTopColor)){ rond(b[0]+bw/2,b[1]+bw/2,b[2]-bw,b[3]-bw,Math.max(0,r-bw/2)); x.lineWidth=bw; x.strokeStyle=cs.borderTopColor; x.stroke(); } }
    function pseudo(e, quel, b){ var cs=getComputedStyle(e, quel), ct=cs.content; if(!ct || ct==='none' || ct==='normal') return;
      var w=parseFloat(cs.width), h=parseFloat(cs.height); if(!(w>0 && h>0)) return; var l=parseFloat(cs.left), t=parseFloat(cs.top);
      if(isNaN(l)) l=(b[2]-w)/2; if(isNaN(t)) t=(b[3]-h)/2; caisse(cs, [b[0]+l, b[1]+t, w, h]); }
    function dessin(svg){ var b=R(svg); if(b[2]<1 || b[3]<1) return; var s=svg.cloneNode(true), A=svg.querySelectorAll('*'), B2=s.querySelectorAll('*'), q=getComputedStyle(svg);
      s.setAttribute('xmlns','http://www.w3.org/2000/svg'); s.setAttribute('width', b[2]); s.setAttribute('height', b[3]); s.style.color=q.color;
      for(var z=0;z<A.length && z<B2.length;z++){ var qa=getComputedStyle(A[z]); B2[z].setAttribute('stroke', qa.stroke); B2[z].setAttribute('fill', qa.fill); B2[z].setAttribute('stroke-width', qa.strokeWidth); B2[z].removeAttribute('style'); B2[z].removeAttribute('class'); }
      try{ image('data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(s)), b); }catch(_){ } }
    function texte(n, cs){ var t=n.nodeValue; if(!t || !t.trim()) return; var rg=document.createRange(); rg.selectNodeContents(n); var q=rg.getBoundingClientRect(); if(q.width<1) return;
      if(cs.textTransform==='uppercase') t=t.toUpperCase(); x.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily; x.fillStyle=cs.color; x.textBaseline='middle'; x.textAlign='center';
      try{ x.letterSpacing=cs.letterSpacing==='normal'?'0px':cs.letterSpacing; }catch(_){ }
      x.fillText(t.trim(), (q.left-D.left)/kk+q.width/kk/2, (q.top-D.top)/kk+q.height/kk/2); }
    function noeud(e){ var cs=getComputedStyle(e); if(cs.display==='none' || cs.visibility==='hidden') return; var b=R(e); if(b[2]<0.5 || b[3]<0.5) return;
      if(e.namespaceURI==='http://www.w3.org/2000/svg'){ dessin(e); return; }
      caisse(cs, b); pseudo(e, '::before', b); pseudo(e, '::after', b);
      for(var ch=e.firstChild; ch; ch=ch.nextSibling){ if(ch.nodeType===3) texte(ch, cs); else if(ch.nodeType===1) noeud(ch); } }
    try{ x.fillStyle=(window.Toile&&Toile.fondToile)?Toile.fondToile():(getComputedStyle(dev).backgroundColor||'#000'); x.fillRect(0,0,390,844); }catch(_){ }
    try{ var tc=$('toileCv'); if(tc && tc.width){ var tb=R(tc); x.drawImage(tc, tb[0], tb[1], tb[2], tb[3]); } }catch(_){ }
    [$('accPlat'), document.querySelector('#device .acc-barre'), $('accRappelCompte')].forEach(function(e){ if(e){ try{ noeud(e); }catch(_){ } } });
    return Promise.all(P).then(function(){ return c; });
  }

  /* ── LA SCÈNE ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── */
  function retire(){ jeu++; try{ if(traceCtl && traceCtl.stop) traceCtl.stop(); }catch(_){ } traceCtl=null; var g=$('guide'); if(g) g.remove(); dev.classList.remove('guide-studio','guide-plus'); trou=null; SC=null; uC=0; uN=0;
    if(vivAv!==null){ window._vivantOff=vivAv; vivAv=null; } }
  function deshabille(){ try{ if(traceCtl && traceCtl.stop) traceCtl.stop(); }catch(_){ } traceCtl=null; ['guidePhrase','guideCible'].forEach(function(i){ var n=$(i); if(n) n.remove(); }); }
  function cible(quoi){ var st=$('studioBtn'), pl=$('createBtn'); if(!st || !pl) return null;
    if(quoi==='studio'){ var b=vu(st); if(b[2]<2) return null; return {b:(F.avecAir?F.avecAir(b, GD.AIR_STUDIO):b), marge:GD.MARGE_STUDIO||5, o:{creux:4}}; }
    var p=boite(pl); if(p[2]<8) return null; return {b:p, marge:GD.MARGE_PLUS||5, o:{creux:4, carre:2.15, irregulier:0.03}}; }
  /* la phrase : les mots de Tom, tels quels ; ses mots-clés et ses noms de nature sont enveloppés, jamais changés */
  function phraseHTML(quoi){ var t=T.guide[quoi], clairA=dev.classList.contains('light');
    function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
    var NAT={Promi:null, Chiche:[255,184,210], Cercle:[201,168,245]}, mots=(T.guideCles[quoi]||[]).concat(quoi==='plus'?['Promi','Chiche','Cercle']:[]), out='', i=0;
    while(i<t.length){ var pris=null;
      for(var m=0;m<mots.length;m++){ var w=mots[m]; if(t.substr(i,w.length)===w && !/[A-Za-zÀ-ÿ]/.test(t.charAt(i+w.length)) && !(i>0 && /[A-Za-zÀ-ÿ]/.test(t.charAt(i-1)))){ pris=w; break; } }
      if(!pris){ out+=esc(t.charAt(i)); i++; continue; }
      if(pris in NAT){ var col='';
        if(clairA){ if(pris==='Promi') col='var(--c-cobalt50)'; else { var c=NAT[pris]; try{ c=window._teinte.ajuste(c, [223,202,164], 5); }catch(_){ } col='rgb('+c[0]+', '+c[1]+', '+c[2]+')'; } }
        out+='<i class="gd-nat" data-n="'+pris.toLowerCase()+'"'+(col?' style="color:'+col+';-webkit-text-fill-color:'+col+'"':'')+'>'+esc(pris)+'</i>'; }
      else out+='<i class="gd-cle">'+esc(pris)+'</i>';
      i+=pris.length; }
    return out; }
  function habille(g, quoi){ deshabille(); var c=cible(quoi); if(!c) return false; ou=quoi;
    g.setAttribute('data-guide', quoi); dev.classList.remove('guide-studio','guide-plus'); dev.classList.add('guide-'+quoi);
    var p=eng(document.createElement('div'),'guide-phrase'); p.id='guidePhrase'; p.innerHTML=phraseHTML(quoi); [].forEach.call(p.querySelectorAll('*'), function(e){ eng(e,'guide-phrase'); }); g.appendChild(p);
    var h=p.offsetHeight||80; p.style.top=Math.round(372-h/2)+'px';
    /* §13 : le tracé des lettres n'est PAS branché tant que Tom n'a pas vu promi-trace-lettres.html ; `?trace=1` le montre en place */
    if(TRACE && window.TraceLettres && !reduit()){ try{ traceCtl=window.TraceLettres.trace(p, null, {cps:50, depart:'h', attributs:{'data-eng':'guide-phrase'}}); }catch(_){ traceCtl=null; } }
    var ent=SC.cible(c.b, c.marge, ((Date.now()&0xffff)|1), c.o), eb=ent.boite;
    trou={x:eb[0]+eb[2]/2, y:eb[1]+eb[3]/2, w:eb[2], h:eb[3], b:c.b};
    var bt=eng(document.createElement('div'),'guide-cible'); bt.id='guideCible'; bt.setAttribute('role','button'); bt.tabIndex=0; bt.setAttribute('aria-label', quoi==='studio'?'Studio':'Planter');
    bt.style.cssText='position:absolute;left:'+eb[0].toFixed(1)+'px;top:'+eb[1].toFixed(1)+'px;width:'+eb[2].toFixed(1)+'px;height:'+eb[3].toFixed(1)+'px;border-radius:'+(Math.min(eb[2],eb[3])/2).toFixed(1)+'px;margin:0;padding:0;max-width:none;background:transparent'; g.appendChild(bt);
    return true; }
  /* une animation : u de a à b en `ms` ; chaque image dessine le niveau ; rend une promesse (fausse si le guide a changé entre-temps) */
  function joue(ms, a, b, pose){ var id=jeu; window._tEvol=performance.now();
    return new Promise(function(ok){ if(reduit() || ms<=0){ pose(b); if(SC) SC.peint(); return ok(id===jeu); }
      var t0=performance.now(); (function f(){ if(id!==jeu || !SC) return ok(false); var u=Math.min(1,(performance.now()-t0)/ms); pose(a+(b-a)*u); SC.peint(); if(u<1) requestAnimationFrame(f); else ok(true); })(); }); }
  function couv(u){ uC=u; SC.couvre(u); var g=$('guide'); if(g) g.setAttribute('data-couv', u.toFixed(3)); }
  function net(u){ uN=u; SC.net(u); var g=$('guide'); if(g) g.setAttribute('data-net', u.toFixed(3)); }
  /* une étape : sa phrase, puis sa zone nette qui s'ouvre en flaques */
  function etape(quoi, pose){ var g=$('guide'); if(!g || !SC) return Promise.resolve(false); if(!habille(g, quoi)){ retire(); etat=null; return Promise.resolve(false); }
    etat=quoi; net(0); if(pose){ net(1); SC.peint(); return Promise.resolve(true); }
    return joue(OUVRE, 0, 1, net); }
  function montre(quoi, sansRevelation){ retire(); if(!F || !F.Scene) { etat=null; return false; } var id=++jeu; etat='prepare'; window._tEvol=performance.now()+400;
    var g=eng(document.createElement('div'),'guide'); g.id='guide'; dev.appendChild(g);
    var cv=eng(document.createElement('canvas'),'guide-eau'); cv.id='guideEau'; cv.setAttribute('aria-hidden','true'); g.appendChild(cv);
    vivAv=!!window._vivantOff; window._vivantOff=true;                 /* la Toile ne bouge pas sous l'image floutée */
    g.addEventListener('click', function(e){ e.stopPropagation(); e.preventDefault(); if(etat==='part' || etat==='prepare' || etat==='couvre' || etat==='vers-plus') return;
      var D2=dev.getBoundingClientRect(), q=k(), x=(e.clientX-D2.left)/q, yy=(e.clientY-D2.top)/q;
      if(trou && Math.abs(x-trou.x)<=trou.w/2+4 && Math.abs(yy-trou.y)<=trou.h/2+4){ if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); return; }
      if(etat==='studio'){ versLePlus(); return; }                    /* toucher ailleurs pendant l'étape du Studio : sa zone se referme, celle du + s'ouvre */
      finir(); }, true);
    g.addEventListener('keydown', function(e){ if(e.key!=='Enter' && e.key!==' ') return; var q=e.target; if(q && q.id==='guideCible'){ e.preventDefault(); if(etat==='studio') versStudio(); else if(etat==='plus') versPlus(); } });
    tPose=performance.now(); g.setAttribute('data-pose', ''+Math.round(tPose));
    accueilImage().then(function(net0){ if(id!==jeu || !$('guide')) return; var t0=performance.now(), flou=F.floute(net0, FLOU); g.setAttribute('data-flou-ms', ''+Math.round(performance.now()-t0));
      SC=F.Scene(cv, {l:390, h:844, densite:2, flou:flou, graine:((Date.now()&0xffffff)|1), creux:GD.CREUX||10, rayon:GD.RAYON||150});
      g.__flou=flou; g.__net=net0;
      if(reduit() || sansRevelation){ couv(1); SC.peint(); g.setAttribute('data-entier','1'); etape(quoi, true); return; }
      etat='couvre'; g.setAttribute('data-depart', ''+Math.round(performance.now()));
      joue(COUVRE, 0, 1, couv).then(function(ok){ if(!ok) return; g.setAttribute('data-entier','1'); etape(quoi, false); }); });
    return true; }
  /* DU STUDIO AU + : la zone du Studio se referme sur elle-même, puis celle du + s'ouvre — rien ne se déplace */
  function versLePlus(pose){ var g=$('guide'); if(!g || !SC) return false; if(etat==='vers-plus') return true; etat='vers-plus'; g.setAttribute('data-guide','vers-plus'); dev.classList.remove('guide-studio');
    var av=$('guidePhrase'); if(av) av.remove(); try{ if(traceCtl && traceCtl.stop) traceCtl.stop(); }catch(_){ } traceCtl=null; var bt=$('guideCible'); if(bt) bt.remove(); trou=null;
    (pose?Promise.resolve(true):joue(FERME, uN, 0, net)).then(function(ok){ if(!ok) return; SC.sansCible(); SC.peint(); etape('plus', !!pose); });
    return true; }
  /* le Studio touché : il s'ouvre PAR-DESSUS le guide (l'eau reste posée dessous) ; au retour sur l'accueil, sa zone se referme et celle du + s'ouvre */
  function versStudio(){ var g=$('guide'); deshabille(); trou=null; etat='au-studio'; tVu=performance.now(); vuStudio=false; tAcc=0; if(g) g.setAttribute('data-guide','au-studio'); try{ $('studioBtn').click(); }catch(_){ } }
  /* le + touché : les trois natures s'ouvrent, et les flaques se vident (la zone du + reste nette jusqu'au bout) */
  function versPlus(){ attente=null; var g=$('guide'); deshabille(); etat='part'; if(g){ g.style.pointerEvents='none'; g.setAttribute('data-guide','part'); }
    try{ var ch=$('accChoix'); if(ch) ch.classList.add('ouvert'); else $('createBtn').click(); }catch(_){ }
    if(!SC){ retire(); etat=null; return; } SC.tire(true); var id=jeu;
    joue(RETIRE, 1, 0, couv).then(function(){ if(id===jeu){ retire(); etat=null; } }); }
  /* toucher ailleurs à l'étape du + : sa zone se referme sur elle-même, puis les flaques se vident — le guidage est fini */
  function finir(){ attente=null; var g=$('guide'); if(!g){ etat=null; return; } if(etat==='part') return; etat='part'; deshabille(); dev.classList.remove('guide-studio','guide-plus'); g.setAttribute('data-guide','part');
    if(!SC || reduit()){ retire(); etat=null; return; } var id=jeu;
    joue(FERME, uN, 0, net).then(function(ok){ if(!ok || !SC) return false; SC.sansCible(); SC.tire(true); return joue(RETIRE, 1, 0, couv); }).then(function(){ if(id===jeu){ retire(); etat=null; } }); }
  /* pour les captures et les juges : un état arrêté (aucune horloge) — la couverture à `ms`, ou la zone nette d'une étape à `ms` */
  function fige(ms){ if(!SC) return false; jeu++; deshabille(); SC.sansCible(); etat='couvre'; couv(Math.max(0,Math.min(1,ms/COUVRE))); net(0); SC.peint(); var g=$('guide'); if(g){ if(ms>=COUVRE) g.setAttribute('data-entier','1'); else g.removeAttribute('data-entier'); } return true; }
  function figeNet(quoi, ms){ var g=$('guide'); if(!SC || !g) return false; jeu++; couv(1); if(!habille(g, quoi)) return false; etat=quoi; net(Math.max(0,Math.min(1,ms/OUVRE))); SC.peint(); return true; }
  /* la veille : l'état se lit sur ce qui est à l'écran */
  setInterval(function(){ var now=performance.now();
    if(attente){ if(!attente.rejeu && LS.g(CLE)==='1'){ attente=null; return; }
      if(accueil() && calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=ATTENTE){ attente=null; tAcc=0; LS.s(CLE,'1'); montre('studio'); } } else tAcc=0; return; }
    if(etat==='au-studio'){ var a=accueil();
      if(!a){ vuStudio=true; tAcc=0; }
      else if(vuStudio || now-tVu>6000){ if(calme()){ if(!tAcc) tAcc=now; if(now-tAcc>=RETOUR){ tAcc=0; if(!versLePlus()){ retire(); etat=null; } } } else tAcc=0; } }   /* le Studio refermé, avec ou sans choix (6 s : un Studio qui ne s'ouvrirait pas) */
    else if(etat==='studio' || etat==='plus' || etat==='vers-plus' || etat==='couvre'){
      if(!accueil()){ retire(); etat=null; } } }, 60);
  /* `?guide=1` le rejoue à l'ouverture ; `&gfige=800` arrête la couverture à cet instant ; `&getape=plus` montre la seconde étape ;
     `&gnet=350` arrête l'ouverture de la zone nette à cet instant (pour le regarder dans Safari) */
  try{ if(/[?&]guide=1(&|$)/.test(location.search)) setTimeout(function(){ attente={rejeu:true}; tAcc=0; }, 1500); }catch(_){ }
  try{ var _gf=/[?&]gfige=(\d+)/.exec(location.search), _ge=/[?&]getape=plus/.test(location.search), _gn=/[?&]gnet=(\d+)/.exec(location.search);
    if(_gf||_ge||_gn) setTimeout(function(){ attente=null; montre(_ge?'plus':'studio', true); setTimeout(function(){ if(_gf) fige(+_gf[1]); if(_gn) figeNet(_ge?'plus':'studio', +_gn[1]); }, 900); }, 4200); }catch(_){ }
  window._guide={ attend:function(rejeu){ attente={rejeu:!!rejeu}; tAcc=0; }, montre:montre, finir:finir, versLePlus:versLePlus, figeA:fige, figeNet:figeNet, image:accueilImage,
    etat:function(){ var g=$('guide'); return {etat:etat, attente:!!attente, trou:trou, vu:LS.g(CLE), entier:!!(g&&g.getAttribute('data-entier')), couv:uC, net:uN, eau:!!(g&&$('guideEau')), flouMs:g?+(g.getAttribute('data-flou-ms')||0):0,
      creux:SC?SC.R.creux.length:0, relief:SC?[SC.R.nx, SC.R.ny]:null, trace:!!traceCtl}; },
    scene:function(){ return SC; },
    regle:{COUVRE:COUVRE, OUVRE:OUVRE, FERME:FERME, RETIRE:RETIRE, ATTENTE:ATTENTE, FLOU:FLOU, RETOUR:RETOUR, MARGE_STUDIO:GD.MARGE_STUDIO, MARGE_PLUS:GD.MARGE_PLUS} };
})();
</script>"""
S=S[:i]+JS+S[j:]
io.open(P,'w',encoding='utf-8').write(S); print('ok')
