
(function(){function w(){
  /* LOT 3 : on GARDE les sous-titres des tuiles (PARCOURS §1) — ne plus retirer .hsub. */
  /* LOT 4 : mise en page des cartes (grille empilée) déléguée au bloc CSS lot4-moodboard.
     On ne force plus de styles inline ici — l'inline battrait le CSS. */
  var tiles=[].slice.call(document.querySelectorAll('#createSheet .tile'));
  tiles.forEach(function(t){t.addEventListener('click',function(){
    tiles.forEach(function(x){x.classList.toggle('on',x===t);});
    var k=t.dataset.kind;try{window.createKind=k;}catch(e){}
    var pf=document.getElementById('promiForm'),nf=document.getElementById('nueeForm'),df=document.getElementById('draftForm');
    if(pf)pf.style.display=(k==='promi')?'block':'none';
    if(nf)nf.style.display=(k==='nuee')?'block':'none';
    if(df)df.style.display=(k==='draft')?'block':'none';
    var cs=document.getElementById('createSheet');if(cs)cs.setAttribute('data-kind',k);
    setHead(k);colorLabels();if(window.renderCsDalle)window.renderCsDalle();
  },true);});
  function colorLabels(){var cs=document.getElementById('createSheet');if(!cs)return;/* LOT 6 : fond coloré → labels crème (plus de teinte de nature, invisible sur son propre fond). */var col='#F3E7D1';cs.querySelectorAll('#promiForm .field label,#nueeForm .field label,#draftForm .field label').forEach(function(l){l.style.setProperty('color',col,'important');});cs.querySelectorAll('.field.f-nuee label').forEach(function(l){l.style.setProperty('color',col,'important');});}
  window._csColorLabels=colorLabels;window._csSetHead=setHead;
  function setHead(k){var m={promi:['Nouveau','Promi','#82AEF8','une parole de plus sur ta Toile'],chiche:['Nouveau','Chiche','#FFB8D2','tu le lances \u2014 la dalle attend sa r\u00e9ponse'],nuee:['Nouveau','Cercle','#E6D8FA','un Cercle, et chacun y plante la sienne'],draft:['Nouveau','Gardé','#DD4D23','une id\u00e9e \u00e0 m\u00fbrir, gard\u00e9e pour toi']};var t=m[k]||m.promi;var h2=document.getElementById('csH2'),sub=document.getElementById('csSub');if(h2)h2.innerHTML=t[0]+' <span class="it" id="csTypeWord" style="color:'+t[2]+'">'+t[1]+'</span>';if(sub)sub.textContent=t[3];}
  try{var _cs=document.getElementById('createSheet');if(_cs&&!_cs.getAttribute('data-kind'))_cs.setAttribute('data-kind','promi');}catch(e){}try{setHead('promi');}catch(e){}try{colorLabels();}catch(e){}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',w);else w();})();
