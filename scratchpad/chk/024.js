
/* ============================================================
   FICHE UNIQUE DE DALLE NUÉE (spec Swift : une dalle = une fiche)
   Design aligné moodboard 07 : membres en pilules + « + inviter »,
   harmonie du groupe, promesses en mini-dalles, séparateurs.
   ============================================================ */
(function(){
  if(typeof window.NUECREATOR==='undefined'){ NUECREATOR={famille:'moi',projet:'moi',soi:'moi',lisbonne:'Rachel'}; }
  if(typeof window.NUETHEME==='undefined'){ NUETHEME={famille:'Nos rituels de famille',projet:'Le lancement, ensemble',lisbonne:'Notre city-trip à trois'}; }
  if(typeof window.NUENOTE==='undefined'){ NUENOTE={lisbonne:'On cale ici les dates, le budget et les bonnes adresses. Chacun ajoute ses idées.'}; }
  if(typeof window.NUEFILES==='undefined'){ NUEFILES={}; }
  try{ NUEEMEM.famille=NUEEMEM.famille||['Maman','Mimi']; NUEEMEM.projet=NUEEMEM.projet||['Adrien']; }catch(e){}
  /* pièces jointes de démonstration — pour que la fonctionnalité soit visible d'emblée */
  try{
    NUEFILES.famille=NUEFILES.famille||[{name:'liste-cadeaux.pdf',type:'application/pdf',size:52000,by:'moi'}];
    NUEFILES.lisbonne=NUEFILES.lisbonne||[{name:'itineraire-samedi.gpx',type:'application/gpx',size:20480,by:'Nico'},{name:'reservation-hotel.pdf',type:'application/pdf',size:61000,by:'moi'}];
    var _pf=promises.filter(function(p){return p.nuee&&p.nuee!=='soi'&&!p.draft;})[0];
    if(_pf) _pf.files=_pf.files||[{name:'photo-repere.jpg',type:'image/jpeg',size:180000,by:'moi'}];
  }catch(e){}

  window.syncAll=function(){
  /* on ne reconstruit QUE ce qui est visible : reconstruire les cinq
     surfaces a chaque changement faisait clignoter l'app. */
  /* ⚑ v60 (rythme) — `offsetParent` NON NUL NE VEUT PAS DIRE VISIBLE (§8) : un écran fermé est glissé hors champ, pas en
     display:none. L'Index fermé passait donc pour ouvert, et CHAQUE plantation le reconstruisait — ses cartes et leurs dalles,
     ~440 ms, pile au moment où la dalle arrive sur la Toile (mesuré : 16 images au lieu de 45 pour l'arrivée dans Pochade).
     Un écran est visible s'il porte la classe que le code pose : `.show`, ou `.in` pour le Fil. Les écrans fermés se
     rebâtissent à leur ouverture (`ouvrirIndex` → `buildIndex`, `setView('fil')` → `buildFeed`). */
  var vis = function(id){ var e=document.getElementById(id);
    return !!e && (e.classList.contains('show') || e.classList.contains('in')); };
  try{if(window._trameReglages && vis('settingsScreen'))_trameReglages();}catch(e){}try{if(typeof buildIndex==='function' && vis('indexSheet'))buildIndex();}catch(e){}try{if(typeof buildFeed==='function' && vis('feedView'))buildFeed();}catch(e){}try{if(typeof render==='function')render();}catch(e){}try{if(typeof updateFeedDot==='function')updateFeedDot();}catch(e){}try{if(typeof buildAura==='function' && vis('auraScreen'))buildAura();}catch(e){}
  /* apres chaque reconstruction : les dalles, les teintes, la lisibilite */
  try{ if(window.peintMinis){peintMinis(document.getElementById('indexList'));
    peintMinis(document.getElementById('feedList'));} }catch(e){}
  try{ if(window._teinterTenues)setTimeout(_teinterTenues,80); }catch(e){}
  try{ if(window._teinterFil)setTimeout(_teinterFil,80); }catch(e){}
  try{ if(window._majFilDot)_majFilDot(); }catch(e){}
};
  function _fileKind(t,name){t=(''+(t||'')).toLowerCase();name=(''+(name||'')).toLowerCase();var ext=name.split('.').pop();
    if(t.indexOf('image')===0||['png','jpg','jpeg','gif','webp','heic'].indexOf(ext)>=0)return 'img';
    if(t.indexOf('pdf')>=0||ext==='pdf')return 'pdf';
    if(ext==='gpx'||t.indexOf('gpx')>=0)return 'gpx';
    if(['xls','xlsx','csv','numbers'].indexOf(ext)>=0||t.indexOf('sheet')>=0||t.indexOf('excel')>=0||t.indexOf('csv')>=0)return 'sheet';
    if(['doc','docx','txt','md','pages','key','ppt','pptx'].indexOf(ext)>=0||t.indexOf('word')>=0)return 'doc';
    return 'file';}
  function _fileGlyph(k){var s='<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">';
    if(k==='pdf')return s+'<path d="M6 3h9l3 3v15H6z"/><path d="M15 3v3h3"/><path d="M9 13h1.5a1.3 1.3 0 0 0 0-2.6H9V16"/></svg>';
    if(k==='sheet')return s+'<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 10h16M4 15h16M10 4v16"/></svg>';
    if(k==='gpx')return s+'<path d="M12 21s7-6.5 7-11a7 7 0 1 0-14 0c0 4.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.3"/></svg>';
    if(k==='doc')return s+'<path d="M6 3h9l3 3v15H6z"/><path d="M15 3v3h3"/><path d="M9 12h6M9 15.5h6M9 8.5h3"/></svg>';
    return s+'<path d="M6 3h9l3 3v15H6z"/><path d="M15 3v3h3"/></svg>';}
  function _fileSize(n){if(n==null)return '';if(n<1024)return n+' o';if(n<1048576)return Math.round(n/1024)+' Ko';return (n/1048576).toFixed(1)+' Mo';}

  function _pickFiles(cb){var inp=document.getElementById('dpFileInput');if(!inp)return;inp.value='';
    inp.onchange=function(){var fs=[].slice.call(inp.files||[]);if(!fs.length){cb([]);return;}var out=[],pending=fs.length;
      fs.forEach(function(file){var o={name:file.name,type:file.type,size:file.size,by:'moi',d:Date.now(),thumb:null};
        if((''+(file.type||'')).indexOf('image')===0){var r=new FileReader();r.onload=function(){o.thumb=r.result;out.push(o);if(--pending===0)cb(out);};r.onerror=function(){out.push(o);if(--pending===0)cb(out);};r.readAsDataURL(file);}
        else{out.push(o);if(--pending===0)cb(out);}});};
    inp.click();}

  window.renderFilesInto=function(mount,list,opts){opts=opts||{};var el=document.getElementById(mount);if(!el)return;
    var canDel=opts.canDel||function(f){return f.by==='moi';};
    el.innerHTML=list.length?list.map(function(f,ix){var k=_fileKind(f.type,f.name);
      var vis=(k==='img'&&f.thumb)?'<span class="dpf-th" style="background-image:url('+f.thumb+')"></span>':'<span class="dpf-ic dpf-'+k+'">'+_fileGlyph(k)+'</span>';
      var rm=canDel(f)?'<button class="dpf-rm" data-rm="'+ix+'" title="retirer">\u2715</button>':'';
      var by=(f.by&&f.by!=='moi')?(' \u00b7 '+_esc(f.by)):'';
      return '<div class="dpf-row">'+vis+'<div class="dpf-meta"><div class="dpf-n">'+_esc(f.name)+'</div><div class="dpf-s">'+_fileSize(f.size)+by+'</div></div>'+rm+'</div>';}).join(''):'<div class="dpf-empty">aucun fichier \u2014 appuie sur +</div>';
    el.querySelectorAll('.dpf-rm').forEach(function(b){b.onclick=function(){list.splice(+b.dataset.rm,1);if(opts.after)opts.after();};});};

  function _peintGlypheNuee(){var dg=document.getElementById('dForm');if(!dg)return;dg.innerHTML='';
    var GS=138,gd=Math.min(3,window.devicePixelRatio||1);var cv=document.createElement('canvas');cv.width=GS*gd;cv.height=GS*gd;cv.style.width=GS+'px';cv.style.height=GS+'px';dg.appendChild(cv);
    var g2=cv.getContext('2d');g2.scale(gd,gd);
    var poly=[[0.50,0.05],[0.85,0.20],[0.96,0.56],[0.76,0.96],[0.28,0.97],[0.06,0.62],[0.14,0.23]];
    g2.beginPath();poly.forEach(function(pt,ix){var x=pt[0]*GS,y=pt[1]*GS;ix?g2.lineTo(x,y):g2.moveTo(x,y);});g2.closePath();
    g2.fillStyle='#E6D8FA';g2.shadowColor='rgba(0,0,0,.28)';g2.shadowBlur=14;g2.shadowOffsetY=6;g2.fill();g2.shadowBlur=0;g2.shadowOffsetY=0;
    var cl=[[0.41,0.44,0.15],[0.63,0.38,0.11],[0.58,0.63,0.11],[0.38,0.64,0.09]];
    cl.forEach(function(c,i){g2.beginPath();g2.fillStyle=i?'rgba(255,255,255,.5)':'rgba(255,255,255,.82)';g2.arc(c[0]*GS,c[1]*GS,c[2]*GS,0,6.2832);g2.fill();});}

  function _nqFiles(key){NUEFILES[key]=NUEFILES[key]||[];return NUEFILES[key];}

  function _nqMembers(){var key=curNuee;var el=document.getElementById('nqMembers');if(!el)return;var mem=NUEEMEM[key]||[];
    var h='<span class="nqm nqm-me">'+avatarHTML('moi')+'Toi'+(NUECREATOR[key]==='moi'?' <span class="nqm-crown">\u2726</span>':'')+'</span>';
    mem.forEach(function(n){h+='<span class="nqm">'+avatarHTML(n)+_esc(n)+'<span class="nqm-rm" data-rm="'+_esc(n)+'">\u2715</span></span>';});
    h+='<span class="nqm nqm-add" id="nqInvChip">\uFF0B inviter</span>';
    el.innerHTML=h;
    el.querySelectorAll('.nqm-rm').forEach(function(b){b.onclick=function(){NUEEMEM[key]=(NUEEMEM[key]||[]).filter(function(x){return x!==b.dataset.rm;});if(window.syncAll)window.syncAll();renderNueeDetail();};});
    var chip=document.getElementById('nqInvChip'),row=document.getElementById('nqInviteRow');
    if(chip)chip.onclick=function(){if(row){var sh=(row.style.display==='none'||!row.style.display);row.style.display=sh?'flex':'none';if(sh){var i=document.getElementById('nqInvite');if(i)i.focus();}}};}

  function _nqHarmony(){var key=curNuee;var el=document.getElementById('nqAura'),fold=document.getElementById('nqHarmFold');if(!el)return;
    var items=promises.filter(function(p){return !p.draft&&p.nuee===key;});var mem=(NUEEMEM[key]||[]).length;
    if(!items.length&&!mem){if(fold)fold.style.display='none';return;}
    if(fold)fold.style.display='';
    var tenu=items.filter(function(p){return p.status==='tenu';}).length;var pct=items.length?Math.round(tenu/items.length*100):0;
    var prem=false;try{prem=(typeof isPremium!=='undefined')&&isPremium;}catch(e){}
    var prem2=prem;
    var bar='<div class=\'nqh-bar\'><div class=\'nqh-fill\' style=\'width:'+pct+'%\'></div><span class=\'nqh-pct\'>'+pct+'%</span></div>';
    var recip=prem2?'<div class=\'nqh-recip\'>r\u00e9ciprocit\u00e9 visible \u00b7 ce que les autres tiennent envers toi</div>':'<div class=\'nqh-cercle\'>\u2726 Ma Parole ! \u2014 vois la r\u00e9ciprocit\u00e9 (les autres envers toi)</div>';
    el.innerHTML='<div class=\'nqh-wrap2\'>'+bar+'<div class=\'nqh-sub\'>'+items.length+' Promi'+(items.length>1?'s':'')+' \u00b7 '+pct+'% tenus</div>'+recip+'</div>';
    var cc=el.querySelector('.nqh-cercle:not(.on)');if(cc)cc.onclick=function(){try{if(typeof closeAll==='function')closeAll();if(typeof ouvreCercle==='function')ouvreCercle();var ps=document.getElementById('plusScreen');if(ps)ps.classList.add('show');}catch(e){}};}

  function _nqList(){var key=curNuee;var el=document.getElementById('nqList');if(!el)return;var items=promises.filter(function(p){return p.nuee===key&&!p.draft;});
    el.innerHTML=items.length?items.map(function(p){var s=p.status==='tenu'?'tenue':p.status==='rate'?'\u00e0 tenir':'en cours';var mc=(typeof miniCell==='function')?miniCell(p):nueeBullet();var rl=(typeof relLabel==='function')?relLabel(p):'';return '<div class="row" data-id="'+p.id+'">'+mc+'<div style="flex:1;min-width:0"><div class="a">'+_esc(p.title)+'</div><div class="b">'+rl+' \u00b7 '+s+'</div></div><div class="chev">\u203a</div></div>';}).join(''):'<div class="b" style="padding:8px 0">aucun Promi \u2014 plante le premier ci-dessus</div>';
    el.querySelectorAll('.row[data-id]').forEach(function(r){r.onclick=function(){openDetail(+r.dataset.id);};});
    try{if(typeof peintMinis==='function'){peintMinis(el);setTimeout(function(){peintMinis(el);},220);}}catch(e){}}

  window.renderNueeDetail=function(){var key=curNuee;if(!key)return;var dp=document.getElementById('detailPoster');if(!dp)return;
    dp.classList.remove('dp-promi','dp-draft','dp-innuee');dp.classList.add('dp-nuee','dp-mode-nuee');
    try{dp.style.setProperty('--dalle-c','rgb(137,107,211)');}catch(e){}
    _peintGlypheNuee();
    var nom=(typeof NUE!=='undefined'&&NUE[key])||key;var tt=document.getElementById('dTitleTxt');if(tt)tt.textContent=nom;else{var dt0=document.getElementById('dTitle');if(dt0)dt0.textContent=nom;}
    var mem=NUEEMEM[key]||[];var nb=promises.filter(function(p){return !p.draft&&p.nuee===key;}).length;
    var meta=document.getElementById('dMeta');if(meta)meta.textContent=nb+' Promi'+(nb>1?'s':'')+' \u00b7 '+mem.length+' membre'+(mem.length!==1?'s':'');
    var pb=document.getElementById('dpPromiBody');if(pb)pb.style.display='none';
    var au=document.getElementById('dAura');if(au)au.style.display='none';
    var blk=document.getElementById('dpNuee');if(blk)blk.style.display='block';var _ty=document.getElementById('dpType');if(_ty)_ty.textContent='Cercle';
    var rn=document.getElementById('mgRename');if(rn)rn.style.display='none';
    var th=document.getElementById('nqTheme');if(th)th.value=(NUETHEME[key]||'');
    var no=document.getElementById('nqNote');if(no)no.value=(NUENOTE[key]||'');
    var irow=document.getElementById('nqInviteRow');if(irow)irow.style.display='none';
    _nqMembers();_nqHarmony();_nqList();
    renderFilesInto('dpFilesNuee',_nqFiles(key),{canDel:function(f){return f.by==='moi'||NUECREATOR[key]==='moi';},after:renderNueeDetail});
    var dr=document.getElementById('nqDissolveRow');if(dr)dr.style.display=(NUECREATOR[key]==='moi')?'':'none';};

  window.openNueeDetail=function(key){if(!key)return;if(typeof NUE!=='undefined'&&!(key in NUE))NUE[key]=key;curNuee=key;cur=null;
    renderNueeDetail();
    if(typeof closeAll==='function')closeAll();
    var dp=document.getElementById('detailPoster');if(dp)dp.classList.add('show');
    try{if(typeof scrim!=='undefined'&&scrim)scrim.classList.add('show');}catch(e){}
    try{requestAnimationFrame(function(){if(window.dpRefresh)window.dpRefresh();});}catch(e){}};

  function _renderPromiFiles(){if(!cur)return;cur.files=cur.files||[];renderFilesInto('dpFilesPromi',cur.files,{canDel:function(f){return true;},after:_renderPromiFiles});}
  var _origOpenDetail=openDetail;
  window.openDetail=function(id){
    /* #Brouillon (lot 17) : un brouillon n'ouvre PAS une fiche — il ROUVRE la page +
       dans son état, prêt à planter (le Brouillon est un état, pas une fiche figée). */
    try{ var _pd=promises.find(function(x){return x.id===id;}); if(_pd&&_pd.draft&&window.reprendreBrouillon){ window.reprendreBrouillon(_pd); return; } }catch(_){}
    curNuee=null;var dp=document.getElementById('detailPoster');if(dp)dp.classList.remove('dp-mode-nuee');
    var pb=document.getElementById('dpPromiBody');if(pb)pb.style.display='';
    var blk=document.getElementById('dpNuee');if(blk)blk.style.display='none';
    _origOpenDetail(id);
    try{_renderPromiFiles();}catch(e){}try{_dkUpdate();}catch(e){}};

  window._nqDissolve=function(key,del){if(del){promises=promises.filter(function(p){return p.nuee!==key;});}else{promises.forEach(function(p){if(p.nuee===key)p.nuee=null;});}
    try{delete NUE[key];}catch(e){}try{delete NUEEMEM[key];}catch(e){}try{delete NUETHEME[key];}catch(e){}try{delete NUENOTE[key];}catch(e){}try{delete NUEFILES[key];}catch(e){}try{delete NUECREATOR[key];}catch(e){}
    curNuee=null;if(typeof closeAll==='function')closeAll();try{if(typeof relayout==='function')relayout();}catch(e){}if(window.syncAll)window.syncAll();try{if(typeof caption==='function')caption();}catch(e){}};

  function _dkUpdate(){if(!cur||!cur.draft)return;var dk=cur.draftKind||((cur.nuee&&cur.nuee!=='soi')?'innuee':'solo');cur.draftKind=dk;
    var seg=document.getElementById('draftKindSeg');if(seg)seg.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.dk===dk);});
    var lab=document.getElementById('labNuee'),chips=document.getElementById('dNueeChips'),info=document.getElementById('dNueeInfo'),note=document.getElementById('dkNueeNote');
    var showNuee=(dk==='innuee'),showNote=(dk==='nuee');
    if(lab)lab.style.display=showNuee?'':'none';if(chips)chips.style.display=showNuee?'':'none';if(info&&!showNuee)info.style.display='none';if(note)note.style.display=showNote?'':'none';}
  window._dkUpdate=_dkUpdate;
  function wire(){
    var dks=document.getElementById('draftKindSeg');if(dks)dks.querySelectorAll('button').forEach(function(b){b.onclick=function(){if(!cur)return;cur.draftKind=b.dataset.dk;if(b.dataset.dk==='solo'||b.dataset.dk==='nuee')cur.nuee=null;_dkUpdate();if(typeof render==='function')render();};});
    var th=document.getElementById('nqTheme');if(th){var s=function(){if(curNuee)NUETHEME[curNuee]=th.value.trim();};th.onchange=s;th.onblur=s;}
    var no=document.getElementById('nqNote');if(no){var s2=function(){if(curNuee)NUENOTE[curNuee]=no.value;};no.onchange=s2;no.onblur=s2;}
    var inv=document.getElementById('nqInvite'),invb=document.getElementById('nqInviteAdd');
    function addMem(){if(!curNuee||!inv)return;var v=inv.value.trim();if(v){NUEEMEM[curNuee]=NUEEMEM[curNuee]||[];NUEEMEM[curNuee].push(v);inv.value='';if(window.syncAll)window.syncAll();renderNueeDetail();}}
    if(invb)invb.onclick=addMem;if(inv)inv.addEventListener('keydown',function(e){if(e.key==='Enter')addMem();});
    var ap=document.getElementById('nqAddPromi');if(ap)ap.onclick=function(){if(curNuee&&typeof openCreateForNuee==='function')openCreateForNuee(curNuee);};
    var dis=document.getElementById('nqDissolve');if(dis)dis.onclick=function(){if(!curNuee)return;var key=curNuee;var nm=(typeof NUE!=='undefined'&&NUE[key])||key;if(typeof toast==='function'){toast('Dissoudre \u00ab '+nm+' \u00bb ?','Lib\u00e9rer les Promi',function(){_nqDissolve(key,false);},'Tout supprimer',function(){_nqDissolve(key,true);});}else{_nqDissolve(key,false);}};
    var pp=document.getElementById('dpPlusPromi');if(pp)pp.onclick=function(){if(!cur)return;cur.files=cur.files||[];_pickFiles(function(fs){fs.forEach(function(f){cur.files.push(f);});_renderPromiFiles();});};
    var pn=document.getElementById('dpPlusNuee');if(pn)pn.onclick=function(){if(!curNuee)return;var L=_nqFiles(curNuee);_pickFiles(function(fs){fs.forEach(function(f){L.push(f);});renderNueeDetail();});};
    var dt=document.getElementById('dTitle'),ok=document.getElementById('dRenameOk'),rinp=document.getElementById('dRenameInput'),rn=document.getElementById('mgRename');
    if(dt)dt.onclick=function(){if(curNuee){if(rn){rn.style.display='flex';if(rinp){rinp.value=(typeof NUE!=='undefined'&&NUE[curNuee])||curNuee;rinp.focus();}}}else{if(typeof _ouvreRenommage==='function')_ouvreRenommage();}};
    if(ok)ok.onclick=function(){if(curNuee){var v=rinp?rinp.value.trim():'';if(v)NUE[curNuee]=v;if(rn)rn.style.display='none';renderNueeDetail();if(window.syncAll)window.syncAll();}else{if(!cur)return;var v2=rinp?rinp.value.trim():'';if(v2){cur.title=v2;if(typeof renderDetail==='function')renderDetail();if(typeof render==='function')render();}if(rn)rn.style.display='none';}};
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wire);else wire();
})();
