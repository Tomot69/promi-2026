
/* ===== Tri réel des listes : réordonne les sections selon le mode ===== */
(function(){
  window.ixPersonCycle=0;
  function _secKind(lab){var c=lab.className||'';if(/g-nuees/.test(c))return 'nuee';if(/g-promis/.test(c))return 'promi';if(/g-draft|g-brouillons/.test(c))return 'brouillon';return 'personne';}

  function _computePersonOrder(){var mode=(typeof ixSortMode!=='undefined')?ixSortMode:'recent';if(mode!=='personne'){window._ixPOrder=null;return;}var persons=[];promises.forEach(function(p){if(p.draft)return;var k=_personKey(p);var pk=_isMoiKey(k)?'__moi':k;if(persons.indexOf(pk)<0)persons.push(pk);});var real=persons.filter(function(k){return k!=='__moi';});real.sort(function(a,b){return (''+a).localeCompare(''+b);});if(real.length){var kk=((window.ixPersonCycle%real.length)+real.length)%real.length;real=real.slice(kk).concat(real.slice(0,kk));}var order=real.concat(['__moi']);var map={};order.forEach(function(k,i){map[k]=i;});window._ixPOrder=map;}
  window.applyIndexSort=function(){
    var list=document.getElementById('indexList');if(!list)return;
    var mode=(typeof ixSortMode!=='undefined')?ixSortMode:'recent';
    var kids=[].slice.call(list.children),pre=[],groups=[],cur=null;
    kids.forEach(function(n){
      if(n.classList&&n.classList.contains('grouplab')){cur={kind:_secKind(n),nodes:[n]};groups.push(cur);}
      else if(cur){cur.nodes.push(n);}
      else pre.push(n);
    });
    if(!groups.length)return;
    /* cycle Personne : rotation des lignes de la section Personnes */
    if(mode==='personne'){
      var pg=null;groups.forEach(function(g){if(g.kind==='personne')pg=g;});
      if(pg){var rows=pg.nodes.slice(1);if(rows.length>1){var k=((window.ixPersonCycle%rows.length)+rows.length)%rows.length;pg.nodes=[pg.nodes[0]].concat(rows.slice(k)).concat(rows.slice(0,k));}}
    }
    var order=(mode==='nuee')?['nuee','personne','promi','brouillon']
             :(mode==='personne')?['personne','nuee','promi','brouillon']
             :(mode==='brouillon')?['brouillon','nuee','personne','promi']
             :['nuee','personne','promi','brouillon'];
    var sorted=[];order.forEach(function(k){groups.forEach(function(g){if(g.kind===k)sorted.push(g);});});
    groups.forEach(function(g){if(sorted.indexOf(g)<0)sorted.push(g);});
    var frag=document.createDocumentFragment();
    pre.forEach(function(n){frag.appendChild(n);});
    sorted.forEach(function(g){g.nodes.forEach(function(n){frag.appendChild(n);});});
    list.appendChild(frag);
  };

  window.applyFeedSort=function(){
    var list=document.getElementById('feedList');if(!list)return;
    var mode=(typeof fdSortMode!=='undefined')?fdSortMode:'recent';
    if(mode!=='brouillon')return;
    var items=[].slice.call(list.children),drafts=[],rest=[];
    items.forEach(function(it){var pid=it.getAttribute&&it.getAttribute('data-pid');var p=pid?promises.find(function(x){return x.id==pid;}):null;(p&&p.draft?drafts:rest).push(it);});
    var frag=document.createDocumentFragment();drafts.concat(rest).forEach(function(n){frag.appendChild(n);});list.appendChild(frag);
  };

  /* on enrobe buildIndex / buildFeed pour appliquer le tri après chaque reconstruction */
  if(typeof window.buildIndex==='function'){var _bi=window.buildIndex;window.buildIndex=function(){try{_computePersonOrder();}catch(e){}var r=_bi.apply(this,arguments);try{applyIndexSort();}catch(e){}return r;};}
  if(typeof window.buildFeed==='function'){var _bf=window.buildFeed;window.buildFeed=function(){var r=_bf.apply(this,arguments);try{applyFeedSort();}catch(e){}return r;};}

  function wireSort(){
    var ix=document.querySelectorAll('#ixSort button');
    ix.forEach(function(b){b.onclick=function(){
      var m=b.dataset.s;
      if(m==='personne'&&(typeof ixSortMode!=='undefined'&&ixSortMode==='personne'))window.ixPersonCycle=(window.ixPersonCycle||0)+1;
      else if(m==='personne')window.ixPersonCycle=0;
      try{ixSortMode=m;}catch(e){}
      ix.forEach(function(x){x.classList.toggle('on',x===b);});
      buildIndex();
    };});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wireSort);else wireSort();
})();
