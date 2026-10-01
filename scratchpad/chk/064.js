
/* ⚑ LE PARTAGE · VARIANTE 2 — « la feuille ». Décision Tom, 30 août 2026.

   CE QUI EST DÉPLACÉ, JAMAIS REFAIT — les QUATORZE réglages, au complet (§9) :
     #shMode (le sujet) · #shFormats + #shCustom (cinq formats + sur mesure, jusqu'à 4K)
     #shTheme (le fond) · #shWmQr (le QR) · #shWmRow (le mot-marque)
     #shTxRow (le texte des dalles) · #shNyRow + #shNySizeRow (le Noyau et sa taille)
     #shNoyauParts (ce qu'il montre) · #shQpRail + #shOptScope (quels Promi — la portée)
     #shInviteBtn + #shShareBtn (les deux actions) · #shInviteNote (les 3 Nuées offertes)
   Disparaissent : le `⋯` (#shTrayBtn) et le `↗` (#shGo) — le tiroir est la FEUILLE, et
   #shGo ne faisait que cliquer #shShareBtn. Aucune fonction n'est perdue (Q109). */
(function(){
  var BAS=560, HAUT=300, AMP=36;
  var NAT={promi:'#82AEF8',chiche:'#FFB8D2',nuee:'#C9A8F5'};
  /* ⚑ §2.1 bis, 18 sept. 2026 — mêmes valeurs que NATTRAIT : le trait se lit sur le champ
     pastel, donc il est SOMBRE. La Nuée l'était déjà ; le Promi et le Chiche la rejoignent. */
  var CLA={promi:'#022140',chiche:'#3D0F23',nuee:'#43291C'};

  function onde(base,amp){
    var mont=amp*0.34,a=amp*0.62;
    function y(x){var t=Math.max(0,Math.min(1,x/390));
      return base-mont*t-a*Math.sin(2*Math.PI*1.5*t);}
    return {y:y,d:function(x){return y(x+0.5)-y(x-0.5);}};
  }
  function chemin(base,amp){
    var o=onde(base,amp),seg=390/6,xs=[0],k=0;
    while(k<389.5){xs.push(k);k+=seg;} xs.push(390);
    var s='M'+xs[0].toFixed(2)+' '+o.y(xs[0]).toFixed(2);
    for(var i=0;i<xs.length-1;i++){var p=xs[i],q=xs[i+1],h=(q-p)/3;
      s+='C'+(p+h).toFixed(2)+' '+(o.y(p)+o.d(p)*h).toFixed(2)+' '+
         (q-h).toFixed(2)+' '+(o.y(q)-o.d(q)*h).toFixed(2)+' '+
         q.toFixed(2)+' '+o.y(q).toFixed(2);}
    return s;
  }
  function ruban(base,amp,x1){
    var o=onde(base,amp),n=44,x0=-10,H=[],B=[],i;
    for(i=0;i<=n;i++){var x=x0+(x1-x0)*i/n,e=(22+(1.5-22)*(i/n))/2,dd=o.d(x),L=Math.sqrt(1+dd*dd);
      H.push([x-dd/L*e,o.y(x)+e/L]); B.push([x+dd/L*e,o.y(x)-e/L]);}
    var s='M'+H[0][0].toFixed(1)+' '+H[0][1].toFixed(1);
    for(i=1;i<H.length;i++)s+='L'+H[i][0].toFixed(1)+' '+H[i][1].toFixed(1);
    for(i=B.length-1;i>=0;i--)s+='L'+B[i][0].toFixed(1)+' '+B[i][1].toFixed(1);
    return s+'Z';
  }
  /* §2.6, première ligne — « RIEN DE TRACÉ » : amorce seule 0 → 42, chevron, points
     64 → 390. Sur le partage rien n'est promis : c'est le seul trait qui n'affirme rien.
     Le trait est posé sur le CHAMP PLEIN : la teinte claire, les deux thèmes (§2.1 bis). */
  function traitSVG(base,amp,col){
    var o=onde(base,amp),hh=Math.round(base+amp+60),s='',coupe=42;
    s+='<path d="'+ruban(base,amp,coupe+6)+'" fill="'+col+'"/>';
    var ang=Math.atan2(o.y(coupe+8)-o.y(coupe-8),16)*180/Math.PI;
    s+='<g transform="translate('+coupe.toFixed(1)+' '+o.y(coupe).toFixed(1)+') rotate('+ang.toFixed(1)+')">'+
       '<path d="M-7 -10 L6 0 L-7 10" stroke="'+col+'" stroke-width="6" fill="none" '+
       'stroke-linecap="round" stroke-linejoin="round"/></g>';
    for(var x=coupe+22;x<387;x+=18)
      s+='<circle cx="'+x.toFixed(1)+'" cy="'+o.y(x).toFixed(1)+'" r="4.5" fill="'+col+'"/>';
    return {svg:'<svg width="390" height="'+hh+'" viewBox="0 0 390 '+hh+'" fill="none" '+
                'style="display:block">'+s+'</svg>', h:hh, min:minOnde(base,amp)};
  }
  function minOnde(base,amp){ var o=onde(base,amp),m=1e9;
    for(var x=0;x<=390;x+=3) m=Math.min(m,o.y(x)); return m; }

  /* Q110 · le champ prend la nature de CE QU'ON PARTAGE */
  function nature(){
    try{
      if(window.curNuee) return 'nuee';
      var p=window._shSujet;
      if(p&&p.kind==='chiche') return 'chiche';
    }catch(e){}
    return 'promi';
  }
  function clair(){ try{return !!document.querySelector('.frame.light,.device.light,#device.light');}catch(e){return false;} }
  function fondClair(){
    try{var b=document.querySelector('#shTheme button[data-t="light"]');
        return !!(b&&b.classList.contains('on'));}catch(e){return false;}
  }
  function ratio(){
    try{ if(typeof shFmtA==='function'){var a=shFmtA(); if(a>0) return a;} }catch(e){}
    return 9/19.5;
  }

  function cale(){
    try{
      var sc=document.getElementById('shareScreen'),dv=document.getElementById('device'),
          cd=document.getElementById('shcCadre');
      if(!sc||!dv||!cd) return;
      var a=sc.getBoundingClientRect(),b=dv.getBoundingClientRect();
      if(!a.width||!b.width) return;
      var k=b.width/390;
      cd.style.left=((b.left-a.left)/k).toFixed(2)+'px';
      cd.style.top =((b.top -a.top )/k).toFixed(2)+'px';
      sc.classList.toggle('shc-clair', clair());
      sc.classList.toggle('shc-fondclair', fondClair());
    }catch(e){}
  }

  var PLAN=[
    ['LE SUJET','#shMode'],
    ['LE FORMAT','#shFormats','#shCustom'],
    ['LE FOND DE L’IMAGE','#shTheme'],
    ['LE MOT-MARQUE','#shWmRow'],
    ['LE QR','#shWmQr'],
    ['LE TEXTE DES DALLES','#shTxRow'],
    ['LE NOYAU','#shNyRow','#shNySizeRow'],
    ['CE QU’IL MONTRE','#shNoyauParts'],
    ['QUELS PROMI','#shQpRail','#shOptScope']
  ];

  function bati(){
    var sc=document.getElementById('shareScreen'); if(!sc) return null;
    sc.classList.add('sh-feuille');
    if(document.getElementById('shcCadre')) return sc;
    var cd=document.createElement('div'); cd.id='shcCadre';
    sc.insertBefore(cd,sc.firstChild);

    var ch=document.createElement('div'); ch.id='shcChamp';
    ch.setAttribute('data-champ','#82AEF8');   /* le peintre déclare ce qu'il verse (§7) */
    cd.appendChild(ch);
    var tr=document.createElement('div'); tr.id='shcTrait'; cd.appendChild(tr);

    var ti=document.createElement('div'); ti.id='shcTitre';
    ti.innerHTML='<div class="t">Partage<span class="ti-x blink">r</span></div><div class="f">✕ FERMER</div>';   /* v39 (Tom) : le « r » clignote comme le « s » de Réglages et le « i » de Promi */
    ti.querySelector('.f').onclick=function(){
      var c=document.querySelector('#shareScreen>.closeb');
      if(c) c.click(); else sc.classList.remove('show');
    };
    cd.appendChild(ti);

    var ra=document.createElement('div'); ra.id='shcRail';
    ra.innerHTML='<i></i><i></i><i></i><i></i><i></i>';
    ra.onclick=function(){ tire(true); };
    cd.appendChild(ra);

    var pi=document.createElement('div'); pi.id='shcPile';
    PLAN.forEach(function(p,i){
      var c=document.createElement('div'); c.className='shc-reg';
      c.setAttribute('data-reg',''+i);
      c.innerHTML='<div class="l">'+p[0]+'</div>';
      pi.appendChild(c);
    });
    var nt=document.createElement('div'); nt.className='shc-note'; nt.id='shcNote';
    pi.appendChild(nt);
    cd.appendChild(pi);

    var ba=document.createElement('div'); ba.id='shcBarre'; cd.appendChild(ba);

    /* LA POIGNÉE — on tire l'onde. Un glissement vertical franc suffit ; on ne lit
       JAMAIS l'état dans une hauteur rendue, c'est la classe qui le porte (§8). */
    var y0=null,fait=false;
    sc.addEventListener('pointerdown',function(e){
      if(e.target&&e.target.closest&&e.target.closest('#shcBarre,#shWrap,.shc-reg')) {y0=null;return;}
      y0=e.clientY; fait=false;
    },true);
    sc.addEventListener('pointermove',function(e){
      if(y0==null||fait) return;
      var dy=e.clientY-y0;
      if(Math.abs(dy)>34){ fait=true; tire(dy<0); }
    },true);
    sc.addEventListener('pointerup',function(){y0=null;fait=false;},true);
    return sc;
  }

  function tire(haut){
    var sc=document.getElementById('shareScreen'); if(!sc) return;
    sc.classList.toggle('sh-haut', !!haut);
    dispose();
  }
  window.shcTire=tire;

  /* on RANGE les commandes existantes dans leurs réglages */
  function range(){
    var sc=document.getElementById('shareScreen'),pi=document.getElementById('shcPile');
    if(!sc||!pi) return;
    PLAN.forEach(function(p,i){
      var cel=pi.querySelector('[data-reg="'+i+'"]'); if(!cel) return;
      for(var k=1;k<p.length;k++){
        var src=sc.querySelector(p[k]);
        if(src&&src.parentNode!==cel) cel.appendChild(src);
      }
    });
    var nt=document.getElementById('shcNote'),no=document.getElementById('shInviteNote');
    if(nt&&no&&nt.textContent!==no.textContent) nt.textContent=no.textContent;
    var ba=document.getElementById('shcBarre');
    if(ba){
      /* ⚠ Q113 · AUCUN ✦ SUR CET ÉCRAN. `#shInviteBtn` portait « ✦  Inviter sur Promi » :
         le ✦ est le signe du Cercle, et personne ne doit pouvoir savoir que quelqu'un ne
         paie pas. Le mot complet n'est pas perdu — il vit dans la note de la feuille
         (« 3 Nuées offertes, pour toi et la personne invitée »). */
      [['shInviteBtn','Inviter'],['shShareBtn','Partager']].forEach(function(q){
        var b=document.getElementById(q[0]); if(!b) return;
        if(b.parentNode!==ba) ba.appendChild(b);
        if(b.textContent.trim()!==q[1]) b.textContent=q[1];
      });
    }
    var pa=document.getElementById('shPreviewArea'),cd=document.getElementById('shcCadre');
    if(pa&&cd&&pa.parentNode!==cd) cd.insertBefore(pa,document.getElementById('shcTrait'));
  }

  function dispose(){
    var sc=document.getElementById('shareScreen'); if(!sc) return;
    range();
    var haut=sc.classList.contains('sh-haut');
    var base=haut?HAUT:BAS;
    var nat=nature(), col=CLA[nat], fond=NAT[nat];
    var t=traitSVG(base,AMP,col);

    var ch=document.getElementById('shcChamp');
    if(ch){ ch.style.height=t.h+'px'; ch.style.background=fond;
      ch.setAttribute('data-champ',fond);
      var cp='path("'+chemin(base,AMP)+' L390 0 L0 0 Z")';
      ch.style.clipPath=cp; ch.style.webkitClipPath=cp; }
    var tr=document.getElementById('shcTrait'); if(tr) tr.innerHTML=t.svg;
    var ba=document.getElementById('shcBarre'); if(ba) ba.style.background=fond;
    var sb=document.getElementById('shShareBtn');
    if(sb){ sb.style.color=fond; sb.style.webkitTextFillColor=fond; }
    /* le rail est posé sur le CORPS, pas sur le champ : il suit ce qui est peint sous lui
       (Q116). En thème clair, #C4A2F5 sur crème tombe sous le seuil 42 du §3. */
    var colRail = clair() ? fond : col;
    [].forEach.call(document.querySelectorAll('#shcRail i'),function(e){e.style.background=colRail;});

    /* Q112 · L'IMAGE EST LA DALLE : elle se pose dans le champ AU RATIO CHOISI, et sa
       FORME dit le format. Boîte utile : de y=100 au minimum de l'onde moins 12 (§2.7). */
    var wrap=document.getElementById('shWrap');
    /* ⚑ v21 — SECOND PROPRIÉTAIRE (§7) : ce calage date de Q112 (« l'image dans le champ »), remplacé par le lot
       « plein » (l'image est l'écran). Il écrivait encore 234 × 415 à chaque passe — l'aperçu alternait avec le
       316 × 562 du lot plein pendant la première seconde. Quand le lot plein tient l'écran, il n'écrit plus. */
    var _plein=(document.getElementById('shareScreen')||{classList:{contains:function(){return false;}}}).classList.contains('sh-plein');
    if(wrap && !_plein){
      var hDispo=Math.max(60, t.min-12-100), a=ratio();
      var h=Math.min(hDispo, 342/a), w=h*a;
      if(w>342){ w=342; h=342/a; }
      wrap.style.width=w.toFixed(1)+'px';
      wrap.style.height=h.toFixed(1)+'px';
      wrap.style.left=((390-w)/2).toFixed(1)+'px';
      wrap.style.top=(100+(hDispo-h)/2).toFixed(1)+'px';
      try{ var cv=document.getElementById('shCanvas');
        if(cv&&window.shPaint) window.shPaint(); }catch(e){}
    }

    var ra=document.getElementById('shcRail');
    if(ra) ra.style.top=Math.round(t.min+62)+'px';
    var pi=document.getElementById('shcPile');
    if(pi){
      var y=Math.round(base+AMP*0.62+30);
      pi.style.top=y+'px';
      /* la feuille DÉFILE sous la barre — sans hauteur bornée, tout ce qui passe 760
         devenait inatteignable (`#shcCadre` est en overflow:hidden). */
      pi.style.height=Math.max(80,760-y)+'px';
      pi.style.overflowY='auto';
      pi.style.webkitOverflowScrolling='touch';
    }
  }
  window.shcDispose=dispose;

  function pose(){
    if(!bati()) return;
    cale(); dispose();
    [60,240,700].forEach(function(t){setTimeout(function(){cale();dispose();},t);});
  }
  window.shcPose=pose;

  /* ⚠ `shareRender()` DIMENSIONNE L'APERÇU LUI-MÊME (il pose une taille en ligne sur
     #shWrap). Ma mise en page ne se rejouait qu'aux événements du doigt : après un
     `shareRender()` appelé de l'extérieur, l'aperçu repassait à SA taille et le geste du
     Noyau tombait à côté — `redteam_geste` est passé de 13/13 à 12/13, « l'aimant de la
     ligne du QR attire » (mesuré : le canevas passait de 218 × 388 à 341 × 607).
     On repose DERRIÈRE elle, comme le lot du Studio le fait derrière buildStudio. */
  try{
    var _sr=window.shareRender;
    if(typeof _sr==='function'){
      window.shareRender=function(){
        var r=_sr.apply(this,arguments);
        try{requestAnimationFrame(dispose);}catch(e){dispose();}
        return r;
      };
    }
  }catch(e){}
  try{
    var sc0=document.getElementById('shareScreen');
    if(sc0){
      ['pointerup','click','change'].forEach(function(ev){
        sc0.addEventListener(ev,function(){
          setTimeout(function(){cale();dispose();},40);
          setTimeout(function(){cale();dispose();},300);
        },true);
      });
    }
  }catch(e){}
  try{
    var _ob=new MutationObserver(function(){
      var s=document.getElementById('shareScreen'); if(!s) return;
      /* ⚠ comparer l'état AVANT d'agir : sinon l'observateur se réveille lui-même (§8) */
      var ouvert=s.classList.contains('show');
      if(ouvert===_ob._v) return;
      _ob._v=ouvert;
      if(ouvert) setTimeout(pose,40); else s.classList.remove('sh-haut');
    });
    _ob.observe(document.getElementById('shareScreen')||document.body,
                {attributes:true,attributeFilter:['class']});
  }catch(e){}
  try{window.addEventListener('resize',function(){setTimeout(cale,60);});}catch(e){}
  if(document.readyState!=='loading') setTimeout(pose,400);
  else document.addEventListener('DOMContentLoaded',function(){setTimeout(pose,400);});
})();
