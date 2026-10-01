(function(){
/* Index — trame : UNE image dessinée une seule fois, aucun filtre CSS/SVG vivant */
function ixPid(){try{if(typeof promises==="undefined")return null;var a=promises.filter(function(p){return !p.draft;});
 if(!a.length)return null;return a[(new Date().getDate()+a.length)%a.length].id;}catch(e){return null;}}
/* ——— SYSTÈME DE TRAME (réutilisable sur toutes les pages) ———
   Dessine UNE dalle de la Toile, pleine, sans texte, avec le contour arrondi
   et le trait du monde actif choisi au Studio. */
/* ——— LES DALLES VALIDEES ———
   Une image par design du Studio, deposee au projet. Aucun rendu genere,
   aucun contour, aucun flou, aucun voile : on pose la dalle, rien d'autre. */
/* ⚑ v29 (Tom, 23 sept.) — LES PHOTOS DE DALLES SONT RETIRÉES DU FICHIER. Une image webp par monde était « déposée
   au projet » et posée à la place du moteur (redteam_decoupe, famille F). Une dalle est peinte par le moteur, jamais
   une photo. Le chargeur reste, vide : `_pdImgs` et `_pdReady` sont encore lus ailleurs, sans rien y trouver. */
var PROMI_DALLES={};
var _pdImgs={},_pdReady={};
(function(){for(var w in PROMI_DALLES){(function(w){var im=new Image();
  im.onload=function(){_pdReady[w]=true;
    try{if(window.ixTrame)window.ixTrame();}catch(e){}
    try{if(window.fdRefresh)window.fdRefresh();}catch(e){}
    try{if(window.stRefresh)window.stRefresh();}catch(e){}
    try{if(window.dpRefresh)window.dpRefresh();}catch(e){}
    try{if(window.esRefresh)window.esRefresh();}catch(e){}};
  im.src=PROMI_DALLES[w];_pdImgs[w]=im;})(w);}})();
function _pdWorld(){
  try{ if(window.Toile&&window.Toile.getTheme){var t=window.Toile.getTheme(); if(t&&_pdImgs[t])return t;} }catch(e){}
  try{ if(window.Toile&&window.Toile.curWorld){var c=window.Toile.curWorld(); if(c&&_pdImgs[c])return c;} }catch(e){}
  try{ if(typeof state!=='undefined'&&state&&_pdImgs[state.structure])return state.structure; }catch(e){}
  return 'encre';
}
function _pdSurface(el){
 try{ for(var n=el;n&&n!==document.documentElement;n=n.parentElement){
   var c=getComputedStyle(n).backgroundColor;
   if(c&&c!=="transparent"&&!/rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*\)/.test(c))return c;
 } }catch(e){}
 return "#fff";
}

function promiTrame(cvId,hostId,opt){try{
 opt=opt||{};
 var cv=document.getElementById(cvId),host=document.getElementById(hostId);
 if(!cv||!host)return;
 var W=host.clientWidth|0,H=host.clientHeight|0;if(W<60||H<60)return;
 var dpr=Math.min(2,window.devicePixelRatio||1);
 cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
 var g=cv.getContext("2d");if(!g)return;
 var op=cv.offsetParent||cv.parentElement;
 if(op&&op!==host){
   /* offsetLeft/offsetTop ignorent les transformations CSS : l'ecran peut etre
      en pleine animation d'ouverture, le calage reste juste. */
   var _off=function(e){var x=0,y=0;for(var n=e;n;n=n.offsetParent){x+=n.offsetLeft;y+=n.offsetTop;}return [x,y];};
   var a=_off(host),c=_off(op);
   cv.style.left=Math.round(a[0]-c[0])+"px";cv.style.top=Math.round(a[1]-c[1])+"px";
   cv.style.width=W+"px";cv.style.height=H+"px";}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,W,H);
 /* ⚑ v29 (Tom, 23 sept.) — PLUS JAMAIS UNE PHOTO. Sans dalle fournie, ce peintre posait l'image webp du monde
    (`PROMI_DALLES`, « déposée au projet ») : une image à la place du moteur, l'infraction la plus grave que
    redteam_decoupe ait prise (famille F, 86 poses). Il pose désormais la VRAIE dalle d'un Promi — celle de
    l'appelant (`opt.id`), ou celle du jour (`ixPid`, la même que l'Index) — rendue À SA TAILLE et posée 1:1.
    Pas de Promi, pas de dalle : rien n'est inventé à la place. */
 var _id=(opt.id!=null)?opt.id:ixPid(); if(_id==null)return;
 var TARGET=W*(opt.size||0.52);
 var im=window._rendDalle?window._rendDalle(_id, TARGET*dpr, TARGET*dpr, opt.courant?{courant:1}:undefined):null;   /* v30 · le monde de plantation, sauf les tuiles de la page + */
 if(!im||!im.width)return;
 if(opt.teinte){ try{ im=opt.teinte(im)||im; }catch(_){} }
 var dw=im.width/dpr,dh=im.height/dpr;
 var marge=(opt.right===undefined?0.03:opt.right);
 var L=W-Math.round(W*marge)-dw, T=Math.round(H*(opt.y||0.40))-dh/2;
 /* LA SCISSION EST ABANDONNEE. Chaque appelant passait encore cut:0.84 ;
    on force zero ici pour qu'aucun appel ne puisse la reintroduire. */
 var CUT=0;
 function pose(blur){g.save();
   if(blur){try{g.filter="blur(28px)";}catch(e){}}
   window._poseUn(g, im, L+dw/2, T+dh/2);
   g.restore();}
 /* LA DALLE, NETTE, EN UNE SEULE PASSE.
    Avant : trois couches — une dalle floutee a gauche de la coupe, un VOILE
    CLAIR rectangulaire de 0 a CUT, puis la dalle nette a droite. Le bord
    droit de ce voile dessinait la ligne verticale et la bande horizontale
    visibles dans toute l'app. Supprimees : une seule dalle, nette. */
 g.save(); g.globalAlpha = 1; pose(false); g.restore();
 /* ⚑ Q74 · LA ZONE DE MATIÈRE, DÉCLARÉE LÀ OÙ ELLE EST CALCULÉE — et pas mesurée après
    coup sur l'alpha : la trame teinte tout le canevas en `source-atop`, la boîte de
    l'alpha couvre alors 776 × 720 sur 780 × 836, c'est-à-dire l'écran entier. Un masque
    pareil avalerait l'entête et la phrase : ce serait la fraude que le § 8 bis interdit.
    `L, T, dw, dh` sont en pixels d'écran du host, comme `cv.style.width`. */
 try{ cv.setAttribute('data-matiere',
   [Math.round(L),Math.round(T),Math.round(dw),Math.round(dh)].join(','));
   /* ⚠ ET LA BASE SUR LAQUELLE ELLE EST CALCULÉE — le canevas est souvent redessiné à
      une autre taille ensuite ; le lecteur remet à l'échelle. */
   cv.setAttribute('data-matiere-base', W+','+H); }catch(e){}
 /* teinte par type (masquée à la dalle) */
 if(opt.tint){try{g.save();g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='source-atop';g.globalAlpha=0.8;g.fillStyle=opt.tint;g.fillRect(0,0,cv.width,cv.height);g.restore();}catch(e){}}
}catch(e){}}
window.promiTrame=promiTrame;
function ixTrame(){promiTrame("ixTrameCv","indexSheet",{cut:0,size:0.52,y:0.40});}
window.ixTrame=ixTrame;
function auTrame(){promiTrame("auTrameCv","auraScreen",{cut:0,size:0.52,y:0.40,courant:1});}   /* v68 : le décor de l'Aura suit le Studio (v34 : seules la Pelote et « Ce que tu as tenu » gardent la plantation) — il le DÉCLARE */
window.auTrame=auTrame;
/* pieces jointes a la creation : meme composant que la fiche */
(function(){var _csF=[];
 function rend(){try{if(window.renderFilesInto)renderFilesInto("csFiles",_csF,{canDel:function(){return true;},after:rend});}catch(e){}}
 window.csGetFiles=function(){return _csF;};
 window.csSens=function(){return window._csSens||"faire";};
 function majSens(){var s=window.csSens();
  var t=document.getElementById("csLabTitre"),q=document.getElementById("csLabQui"),
      i=document.getElementById("fTitle"),b=document.getElementById("addPromi"),
      h=document.getElementById("csSub");
  var dem=(s==="demander");
  if(t)t.textContent=dem?"Le Promi que tu demandes":"Le Promi";
  if(q){var qt=document.getElementById("csLabQuiTxt");if(qt)qt.textContent=dem?"À qui tu le demandes":"Pour qui";}
  if(i)i.placeholder=dem?"de m\u2019appeler dimanche…":"de rappeler Sam avant dimanche…";
  if(b)b.textContent=dem?"Demander ce Promi":"Planter le Promi";
  var vis=document.getElementById("promiForm");
  if(h&&vis&&getComputedStyle(vis).display!=="none")
   h.textContent=dem?"tu demandes un Promi — la dalle apparaîtra chez la personne":"une parole de plus sur ta Toile";
  try{if(window.csDalles)csDalles();}catch(_c){}
 }
 window.csMajSens=majSens;
 var _PA=[[.50,.03],[.86,.20],[.97,.58],[.74,.98],[.26,.96],[.05,.60],[.13,.22]];
 var _PB=[[.42,.04],[.80,.15],[.98,.47],[.85,.87],[.43,.97],[.09,.73],[.03,.31]];
 function _clip(pts,sz){var o=[];for(var k=0;k<pts.length;k++)o.push((pts[k][0]*sz).toFixed(1)+"px "+(pts[k][1]*sz).toFixed(1)+"px");
  return "polygon("+o.join(",")+")";}
 /* une seule mecanique pour toute l'app : le champ le dit, on ne bloque pas par un message */
 window.promiRequis=function(el){try{
  if(!el)return true; var v=(el.value||"").trim(); if(v){el.classList.remove("req-vide");return true;}
  el.classList.remove("req-vide"); void el.offsetWidth; el.classList.add("req-vide");
  try{if(navigator.vibrate)navigator.vibrate(12);}catch(_v){}
  try{el.focus({preventScroll:false});}catch(_f){}
  return false;
 }catch(e){return true;}};
 document.addEventListener("input",function(e){
  var t=e.target; if(t&&t.classList&&t.classList.contains("req-vide")&&(t.value||"").trim())
   t.classList.remove("req-vide");
 },true);
 /* tout bouton qui porte data-requis refuse un champ vide, partout dans l'app */
 document.addEventListener("click",function(e){
  var b=e.target&&e.target.closest?e.target.closest("[data-requis]"):null;if(!b)return;
  var el=document.getElementById(b.getAttribute("data-requis"));
  if(el&&!window.promiRequis(el)){e.preventDefault();e.stopPropagation();}
 },true);
 window.dfKind=function(){return window._dfKind||"solo";};
 /* le meme + que l'Index, le Fil et les fiches : une ligne, un +, une pastille */
 window.csWho={};
 function _whoRend(box){var w=document.getElementById(box);if(!w)return;
  var L=window.csWho[box]||[];
  var ex=[].slice.call(w.querySelectorAll(".chip[data-fixe]"));
  var add=L.map(function(n,i){return '<div class="chip on" data-who="'+box+'|'+i+'">'+
   String(n).replace(/[<>&]/g,"")+' <span style="opacity:.6">✕</span></div>';}).join("");
  w.innerHTML=ex.map(function(e){return e.outerHTML;}).join("")+add;}
 window.csWhoList=function(box){return (window.csWho[box]||[]).slice();};
 document.addEventListener("click",function(e){
  var b=e.target&&e.target.closest?e.target.closest("[data-addwho]"):null;
  if(b){e.preventDefault();var p=b.getAttribute("data-addwho").split("|");
   var inp=document.getElementById(p[0]);var v=inp&&inp.value.trim();
   if(!v)return; (window.csWho[p[1]]=window.csWho[p[1]]||[]).push(v);
   inp.value="";_whoRend(p[1]);return;}
  var d=e.target&&e.target.closest?e.target.closest("[data-who]"):null;
  if(d){var q=d.getAttribute("data-who").split("|");
   if(window.csWho[q[0]]){window.csWho[q[0]].splice(+q[1],1);_whoRend(q[0]);}}
 });
 document.addEventListener("keydown",function(e){
  if(e.key!=="Enter")return;var t=e.target;if(!t||!t.id)return;
  var b=document.querySelector('[data-addwho^="'+t.id+'|"]');
  if(b){e.preventDefault();b.click();}
 });
 var _nF=[];
 window.nFirstList=function(){return _nF;};
 window.nFirstReset=function(){_nF.length=0;_nFrend();};
 function _nFrend(){var w=document.getElementById("nFirstList");if(!w)return;
  w.innerHTML=_nF.map(function(t,i){return '<div class="nf-item"><span>'+
   String(t).replace(/[<>&]/g,"")+'</span><button type="button" data-nf="'+i+'">✕</button></div>';}).join("");}
 document.addEventListener("click",function(e){
  var t=e.target&&e.target.closest?e.target.closest("#nFirstPlus"):null;
  if(t){e.preventDefault();var f=document.getElementById("nFirst");
   var v=f&&f.value.trim();if(v){_nF.push(v);f.value="";_nFrend();}return;}
  var d=e.target&&e.target.closest?e.target.closest("[data-nf]"):null;
  if(d){e.preventDefault();_nF.splice(+d.getAttribute("data-nf"),1);_nFrend();}
 });
 function majDf(){var k=window.dfKind();
  var t=document.getElementById("dfTitle"),b=document.getElementById("addDraft"),
      h=document.getElementById("csSub"),n=document.querySelector("#draftExtra .f-nuee");
  if(t)t.placeholder=(k==="nuee")?"le nom du Cercle…":"ce que tu mets de côté…";
  if(b)b.textContent=(k==="nuee")?"Mettre le Cercle de côté":"Mettre de côté";
  var vd=document.getElementById("draftForm");
  if(h&&vd&&getComputedStyle(vd).display!=="none")
   h.textContent="une esquisse — une dalle sur ta Toile, et rien n\u2019est envoyé";
  var n2=document.querySelector("#draftForm .f-nuee");
  if(n2)n2.style.display=(k==="innuee")?"":"none";
  try{if(window.csDalles)csDalles();}catch(_){}
 }
 window.dfMaj=majDf;
 document.addEventListener("click",function(e){
  var b=e.target&&e.target.closest?e.target.closest("#dfKind button"):null;if(!b)return;
  e.preventDefault();var all=document.querySelectorAll("#dfKind button");
  for(var k=0;k<all.length;k++)all[k].classList.remove("on");
  b.classList.add("on");window._dfKind=b.getAttribute("data-dk");majDf();
 });
 document.addEventListener("click",function(e){
  var b=e.target&&e.target.closest?e.target.closest("#draftMoreBtn"):null;if(!b)return;
  var x=document.getElementById("draftExtra");if(!x)return;
  x.style.display=(x.style.display==="none")?"":"none";
 });
 /* le type courant pilote la couleur des + et des chevrons */
 document.addEventListener("click",function(e){
  var t=e.target&&e.target.closest?e.target.closest("#createSheet .tile[data-kind]"):null;
  if(!t)return;var sh=document.getElementById("createSheet");
  if(sh)sh.setAttribute("data-kind",t.getAttribute("data-kind"));
  setTimeout(function(){try{
   var k=t.getAttribute("data-kind");
   if(k==="promi"&&window.csMajSens)csMajSens();
   if(k==="draft"&&window.dfMaj)dfMaj();
   var x=document.getElementById("draftExtra");if(x&&k!=="draft")x.style.display="none";
   var y=document.getElementById("promiExtra");if(y&&k!=="promi")y.style.display="none";
  }catch(_){}},30);
  setTimeout(function(){try{if(window.csDalles)csDalles();}catch(_){}},60);
 });

 window.csDalles=function(){try{
  var w=(typeof _pdWorld==="function")?_pdWorld():"encre";
  var img=(typeof PROMI_DALLES!=="undefined"&&PROMI_DALLES[w])?PROMI_DALLES[w]:null;
  var col=(window.KC&&KC.Ch)?KC.Ch:"#82AEF8";
  var els=document.querySelectorAll("#csSens .cs-dl,#dfKind .cs-dl");
  for(var k=0;k<els.length;k++){var e=els[k];
   e.style.clipPath="none";
   if(img){e.style.backgroundImage="url("+img+")";
    e.style.setProperty("--dlm","url("+img+")");}
   var _tc=e.getAttribute("data-d");
   e.style.setProperty("--dlc",_tc==="c"?"#E6D8FA":col);
   var d2=e.getAttribute("data-d");
   var bp=(d2==="b")?"22% 68%":(d2==="c"?"86% 14%":"50% 50%");
   var bs=(d2==="b")?"176% 176%":(d2==="c"?"118% 118%":"contain");
   e.style.removeProperty("background-position");
   e.style.removeProperty("background-size");
   e.style.setProperty("--dlbp",bp);e.style.setProperty("--dlbs",bs);}
 }catch(e){}};
 document.addEventListener("click",function(e){
  var b=e.target&&e.target.closest?e.target.closest("#csSens button"):null;if(!b)return;
  e.preventDefault();
  var all=document.querySelectorAll("#csSens button");
  for(var k=0;k<all.length;k++)all[k].classList.remove("on");
  b.classList.add("on");window._csSens=b.getAttribute("data-sens");majSens();
 });
 window.csResetFiles=function(){_csF.length=0;rend();};
 document.addEventListener("click",function(e){
   var b=e.target&&e.target.closest?e.target.closest("#csPlus"):null;if(!b)return;
   e.preventDefault();try{_pickFiles(function(fs){(fs||[]).forEach(function(f){_csF.push(f);});rend();});}catch(_){}
 });
})();
function shTrame(){/* Partager n'a plus de trame : fond uni + grain (cf. --sh-bleu) */}
window.shTrame=shTrame;
/* Pincer pour zoomer, glisser pour recadrer. L'image est figee : seul le cadrage bouge,
   la Toile ne recompose jamais. */
(function(){
 var pts={},d0=0,z0=1,px=0,py=0,mx0=0,my0=0;
 window.shZoom=1; window.shPanX=0; window.shPanY=0;
 function el(){return document.getElementById('shPreviewArea');}
 function app(){var w=document.getElementById('shWrap'); if(!w)return;
  w.style.transform='translate('+window.shPanX.toFixed(1)+'px,'+window.shPanY.toFixed(1)+'px) '+
   'scale('+window.shZoom.toFixed(3)+')';
  w.style.transformOrigin='center center';}
 window.shZoomReset=function(){window.shZoom=1;window.shPanX=0;window.shPanY=0;app();};
 function ctr(){var k=Object.keys(pts);if(k.length<2)return null;
  var a=pts[k[0]],b=pts[k[1]];return {d:Math.hypot(a.x-b.x,a.y-b.y),
   x:(a.x+b.x)/2,y:(a.y+b.y)/2};}
 document.addEventListener('pointerdown',function(e){
  var z=el(); if(!z||!z.contains(e.target))return;
  pts[e.pointerId]={x:e.clientX,y:e.clientY};
  var c=ctr(); if(c){d0=c.d;z0=window.shZoom;}
  else{px=e.clientX;py=e.clientY;mx0=window.shPanX;my0=window.shPanY;}
 },true);
 document.addEventListener('pointermove',function(e){
  if(!(e.pointerId in pts))return;
  /* le Noyau est pris : le cadrage ne bouge pas. Sans ce garde-fou, la
     Toile glissait EN MEME TEMPS que le Noyau — les deux etaient lies. */
  if(window._shGelCadrage){ pts[e.pointerId]={x:e.clientX,y:e.clientY};
    px=e.clientX; py=e.clientY; mx0=window.shPanX; my0=window.shPanY; return; }
  pts[e.pointerId]={x:e.clientX,y:e.clientY};
  var c=ctr();
  if(c&&d0>0){ window.shZoom=Math.max(1,Math.min(12,z0*c.d/d0)); app(); e.preventDefault(); return; }
  if(Object.keys(pts).length===1&&window.shZoom>1.01){
   window.shPanX=mx0+(e.clientX-px); window.shPanY=my0+(e.clientY-py); app(); e.preventDefault(); }
 },true);
 function up(e){ delete pts[e.pointerId]; d0=0;
  if(!Object.keys(pts).length&&window.shZoom<=1.02)window.shZoomReset(); }
 document.addEventListener('pointerup',up,true);
 document.addEventListener('pointercancel',up,true);
})();
try{if(document.fonts&&document.fonts.load){
  document.fonts.load('400 40px "PromiLate"');
  document.fonts.ready.then(function(){try{if(window.shareRender&&
   document.getElementById('shareScreen').classList.contains('show'))shareRender();}catch(e){}});
}}catch(e){}
(function(){
 function T(id){return document.getElementById(id);}
 document.addEventListener("click",function(e){
  var s=T("shareScreen"); if(!s)return;
  if(e.target.closest&&(e.target.closest("#shTrayBtn")||e.target.closest("#shFmtTxt"))){s.classList.toggle("sh-tray-open");return;}
  if(e.target.closest&&e.target.closest("#shGo")){var b=T("shShareBtn");if(b)b.click();return;}
  /* un tap ailleurs referme le tiroir */
  if(s.classList.contains("sh-tray-open")&&!(e.target.closest&&e.target.closest("#shTray"))){
   s.classList.remove("sh-tray-open");}
     });
 /* le libelle du format et le bouton melanger suivent l'etat */
 document.addEventListener("click",function(e){
  var w=e.target&&e.target.closest?e.target.closest("#shBadge"):null;if(!w)return;
  var m=document.getElementById("shWordmark");if(m)m.classList.toggle("sig");
 });
 /* le Noyau pose sur l'epreuve, sa taille, et le texte des dalles */
 window.shNoyau=false; window.shNySize="m"; window.shChiffre=false; window.shLabels=true;
 function maj(sel,el){var g=document.querySelectorAll(sel);
  for(var i=0;i<g.length;i++)g[i].classList.toggle("on",g[i]===el);}
 document.addEventListener("click",function(e){
  var t=e.target; if(!t.closest)return;
  if(t.closest("#shNyOff")||t.closest("#shNyOn")){
   var pose=!!t.closest("#shNyOn");
   window.shNoyau=pose;
   maj("#shNyRow button",T(pose?"shNyOn":"shNyOff"));
   var s4=T("shareScreen"); if(s4)s4.classList.toggle("sh-ny-on",pose);
   if(window.shareRender)shareRender();return;}
  var sz=t.closest("#shNySizeRow button[data-ns]");
  if(sz){window.shNySize=sz.getAttribute("data-ns");
   maj("#shNySizeRow button[data-ns]",sz); if(window.shareRender)shareRender();return;}
  if(t.closest("#shNyPct")){var b=T("shNyPct");window.shChiffre=!window.shChiffre;
   b.classList.toggle("on",window.shChiffre); if(window.shareRender)shareRender();return;}
  if(t.closest("#shBadge")||t.closest("#shWordmark")){
   var s3=T("shareScreen"); if(!s3)return;
   var sg2=!s3.classList.contains("sh-sig");
   s3.classList.toggle("sh-sig",sg2);
   maj("#shWmRow button",T(sg2?"shWmSig":"shWmBri"));
   /* le % suit le mot-marque : il faut repeindre */
   try{if(window.shareRender)shareRender();}catch(_){}
   e.preventDefault(); e.stopPropagation(); return;}
  if(t.closest("#shWmBri")||t.closest("#shWmSig")){
   var sg=!!t.closest("#shWmSig"); maj("#shWmRow button",T(sg?"shWmSig":"shWmBri"));
   var s2=T("shareScreen"); if(s2)s2.classList.toggle("sh-sig",sg);
   try{if(window.shareRender)shareRender();}catch(_){}
   return;}
  if(t.closest("#shTxOn")||t.closest("#shTxOff")){
   var on=!!t.closest("#shTxOn"); maj("#shTxRow button",T(on?"shTxOn":"shTxOff"));
   window.shLabels=on;
   try{if(typeof state!=="undefined")state.labels=on;}catch(_){}
   if(window.shareRender)shareRender();return;}
 });
 /* la ligne des Reglages ouvre le meme flux que le bouton du tiroir */
 document.addEventListener('click',function(e){
  var r=e.target&&e.target.closest?e.target.closest('#setInvite'):null; if(!r)return;
  var b=document.getElementById('shInviteBtn'); if(b)b.click();
 });
 window.shFoot=function(){try{
  var qp=document.querySelector('#shTray .sh-lab.qp'), op=document.getElementById('shOptVis');
  var mos=(typeof shareMode!=='undefined'&&shareMode==='mosaic');
  if(op&&op.parentElement)op.parentElement.style.display=mos?'none':'';
  if(qp)qp.style.display=mos?'none':'';
  var t=T("shFmtTxt"); if(t){var b=document.querySelector("#shFormats .sh-fmt.on");
   if(b){var n=b.querySelector("b"),d=b.querySelector("em");
    t.textContent=(n?n.textContent:"")+(d?" · "+d.textContent:"");}}
 }catch(e){}};
})();
/* le grain de l'image de profil est la reference : on le publie en variable */
try{(function(){var c=document.createElement("canvas");c.width=c.height=96;
 var g=c.getContext("2d");if(!g)return;var im=g.createImageData(96,96),d=im.data;
 for(var i=0;i<d.length;i+=4){var v=140+Math.random()*115;
  d[i]=d[i+1]=d[i+2]=v;d[i+3]=Math.random()*26;}
 g.putImageData(im,0,0);
 document.documentElement.style.setProperty("--grain-url","url("+c.toDataURL()+")");})();
}catch(e){}
/* le fond de Partager suit la palette du Studio */
window.shCadre=function(){try{
 var t=document.querySelector("#shareScreen>.sh-top"),
     b=document.querySelector("#shareScreen>.sh-bot"),
     a=document.getElementById("shPreviewArea");
 if(!t||!b||!a)return;
 /* rien a borner : l'epreuve prend le cadre entier. On ne garde la mesure
    des barres que pour ne jamais laisser un bouton sortir de l'ecran. */
 t.style.maxHeight=(a.clientHeight*0.34)+"px";
 b.style.maxHeight=(a.clientHeight*0.42)+"px";
}catch(e){}};
window.shFond=function(){try{ /* plus de teinte : le fond suit le mode clair/sombre */
 /* la feuille prend exactement la hauteur du device : les % ne resolvent pas ici */
 var _s=document.getElementById('shareScreen');

}catch(e){}};
/* appui long sur l'apercu : on efface le chrome pour voir l'epreuve seule */
(function(){var t=null,sc=null;
 function on(){sc=document.getElementById("shareScreen");if(sc)sc.classList.add("sh-solo");}
 function off(){if(sc)sc.classList.remove("sh-solo");if(t){clearTimeout(t);t=null;}}
 document.addEventListener("pointerdown",function(e){
   var a=e.target&&e.target.closest?e.target.closest("#shPreviewArea"):null;if(!a)return;
   if(t)clearTimeout(t);t=setTimeout(on,260);},{passive:true});
 ["pointerup","pointercancel","pointerleave"].forEach(function(ev){
   document.addEventListener(ev,off,{passive:true});});
})();
function ixCount(){try{var el=document.getElementById("ixCount");if(el&&typeof promises!=="undefined")el.textContent=(function(){var n=promises.filter(function(p){return !p.req&&!p.draft;}).length,m=(typeof NUE!=='undefined')?Object.keys(NUE).length:0;return n+' parole'+(n>1?'s':'')+' · '+m+' Cercle'+(m>1?'s':'');})();/* les gardés de côté comptent : voir buildIndex */
 var sb=document.getElementById("ixSub");if(sb&&typeof NUE!=="undefined"){var n=Object.keys(NUE).length;sb.textContent="tous tes Promi \u00b7 "+n+" Cercle"+(n>1?"s":"");}}catch(e){}}
window.ixCount=ixCount;
document.addEventListener("click",function(e){
 var t=e.target&&e.target.closest?e.target.closest("#ixToFeed"):null;if(!t)return;
 try{var sh=document.getElementById("indexSheet");if(sh)sh.classList.remove("show");
 var sc=document.getElementById("scrim");if(sc)sc.classList.remove("show");}catch(_){}
 try{if(typeof openFeed==="function")openFeed();}catch(_){}
});
function fdTrame(){promiTrame("fdTrameCv","feedView",{cut:0,size:0.52,y:0.40});}
(function(){try{var d=document.getElementById('device'),s=document.getElementById('settingsScreen');
  if(d&&s&&s.parentElement!==d)d.appendChild(s);
  var es=document.getElementById('essaimSheet');
  if(d&&es&&es.parentElement!==d)d.appendChild(es);
  /* le fond reste fixe : seul le contenu defile */
  if(s&&!document.getElementById('stScroll')){
    var sc=document.createElement('div'); sc.id='stScroll';
    var kids=[].slice.call(s.children);
    kids.forEach(function(c){ if(c.id==='stTrameCv')return;
      if(c.className&&(''+c.className).indexOf('closeb')>=0)return; sc.appendChild(c); });
    s.appendChild(sc);
  }
}catch(e){}})();
function stTrame(){
  /* LES REGLAGES N'ONT PAS DE COUPE. promiTrame() dessine volontairement une
     scission verticale a 84 % — dalle floutee a gauche, voile clair, dalle
     nette a droite. C'est la regle des autres ecrans, pas celle-ci : le
     moodboard demande une dalle simple, grande, vers le haut, tres effacee.
     C'est cet appel qui repeignait le fond « au bout d'un moment ». */
  if(window._trameReglages) _trameReglages();
}
function dpTrame(){
  /* ⚑ v29 — la dalle n'est plus rendue ici à k = 1 : promiTrame la rend à sa taille ; la teinte du Chiche
     s'applique à CE rendu, 1:1. */
  if(!(typeof cur!=="undefined"&&cur&&!cur.draft&&window.Toile&&Toile.dalleAbs&&Toile.dalleAbs(cur.id))) return;
  var _chiche=!!cur.chiche;
  function teinte(src){
  /* Chiche : la bande de la fiche porte l'identité framboise, comme la Nuée porte
     le mauve (§4). VRAIE dalle du moteur, seulement TEINTÉE — jamais une forme
     inventée. Blend 'color' + remontée de luminance 'source-atop' (sinon ton-sur-ton),
     puis 'destination-in' pour garder l'alpha. */
  try{ if(src&&src.width&&_chiche){
    var _fc=document.createElement("canvas"); _fc.width=src.width; _fc.height=src.height;
    var _fx=_fc.getContext("2d");
    if(_fx){ _fx.drawImage(src,0,0);
      _fx.globalCompositeOperation="color"; _fx.fillStyle="#FFB8D2"; _fx.fillRect(0,0,_fc.width,_fc.height);
      _fx.globalCompositeOperation="source-atop"; _fx.fillStyle="rgba(255,183,208,.30)"; _fx.fillRect(0,0,_fc.width,_fc.height);
      _fx.globalCompositeOperation="destination-in"; _fx.drawImage(src,0,0);
      _fx.globalCompositeOperation="source-over"; src=_fc; } } }catch(e){}
  return src; }
  /* sur la page d'une dalle, elle deborde franchement sur la zone nette */
  promiTrame("dpTrameCv","detailPoster",{cut:0,size:0.52,y:0.40,right:0.05,id:cur.id,teinte:teinte});
}
function esTrame(){promiTrame("esTrameCv","essaimSheet",{cut:0,size:0.52,y:0.40});}
window.dpTrame=dpTrame; window.esTrame=esTrame;
window.stTrame=stTrame;
window.fdTrame=fdTrame;
function fdCount(){try{var el=document.getElementById("fdCount");
 /* ⚑ LES GESTES QUI VIENNENT D'AILLEURS, pas le nombre d'entrées — le cadre 76 écrit 4
    au-dessus de cinq bandeaux (voir `_s4Fil`, et QUESTIONS · Q79). `FEED.length` reste le
    secours tant que la grille n'a rien composé. */
 if(el&&typeof FEED!=="undefined")
   el.textContent=(window._filAutrui!=null)?window._filAutrui:FEED.length;}catch(e){}}
window.fdCount=fdCount;
function fdRefresh(){fdCount();fdTrame();}
function stRefresh(){stTrame();}
window.stRefresh=stRefresh;
function dpRefresh(){dpTrame();}
window.dpRefresh=dpRefresh;
function esRefresh(){esTrame();}
window.esRefresh=esRefresh;
window.fdRefresh=fdRefresh;
function ixRefresh(){ixCount();ixTrame();}
window.ixRefresh=ixRefresh;
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){setTimeout(ixRefresh,400);});
else setTimeout(ixRefresh,400);
})();