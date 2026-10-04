/* PLANCHE v127 (C-042) — posé PAR-DESSUS l'app par le script de planche, jamais dans l'app. */
window.OV=(function(){
  var IC={
    plume:'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1-4L16.2 4.8a2.1 2.1 0 0 1 3 3L8 19l-4 1z"/><path d="M14 7l3 3"/></svg>',
    gomme:'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19h10"/><path d="M4.6 14.2l8.6-8.6a2 2 0 0 1 2.8 0l2.4 2.4a2 2 0 0 1 0 2.8L10.2 19H8.4l-3.8-3.4a1 1 0 0 1 0-1.4z"/><path d="M9.6 9.2l5.2 5.2"/></svg>',
    annuler:'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 13L4.5 8.5 9 4"/><path d="M4.5 8.5H14a5.5 5.5 0 0 1 0 11h-3"/></svg>',
    S1:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="5.2"><circle cx="12" cy="12" r="7.2" stroke-dasharray="9.1 2.21" stroke-dashoffset="-1.1"/></svg>',
    oeil:'<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.6"/></svg>',
    oeilNon:'<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.6"/><path d="M4 20L20 4"/></svg>' };
  function S2(){ var b=document.getElementById('studioBtn'), s=b&&b.querySelector('svg'); if(!s) return IC.S1; var c=s.cloneNode(true); c.setAttribute('width','22'); c.setAttribute('height','22'); c.style.cssText='width:22px;height:22px'; return c.outerHTML; }
  var CORPS={promi:'#335382', chiche:'#7C3F58', cercle:'#5D4978'}, CHAMP={promi:'#82AEF8', chiche:'#FFB8D2', cercle:'#C9A8F5'};
  function el(css, html){ var d=document.createElement('div'); d.style.cssText='position:absolute;box-sizing:border-box;'+css; if(html!=null) d.innerHTML=html; return d; }
  function racine(){ var o=document.getElementById('ovC042'); if(o) o.remove(); var dv=document.getElementById('device'), r=dv.getBoundingClientRect(); o=el('position:fixed;left:'+r.left+'px;top:'+r.top+'px;width:390px;height:844px;z-index:2147483000;pointer-events:none;overflow:hidden;border-radius:28px'); o.style.position='fixed'; o.id='ovC042'; document.body.appendChild(o); return o; }
  function nettoie(){ var o=document.getElementById('ovC042'); if(o) o.remove(); [].forEach.call(document.querySelectorAll('[data-ov-dy]'), function(e){ e.style.transform=e.getAttribute('data-ov-tr')||''; e.removeAttribute('data-ov-dy'); }); [].forEach.call(document.querySelectorAll('[data-ov-clone]'), function(e){ e.remove(); }); [].forEach.call(document.querySelectorAll('[data-ov-cache]'), function(e){ e.style.visibility=''; e.removeAttribute('data-ov-cache'); }); }
  function disque(x, y, ic, enc, inv, sel, d, bord){ d=d||44; return el('left:'+x+'px;top:'+y+'px;width:'+d+'px;height:'+d+'px;border-radius:50%;border:'+(bord==null?2:bord)+'px solid '+enc+';display:flex;align-items:center;justify-content:center;color:'+(sel?inv:enc)+';background:'+(sel?enc:'transparent'), ic); }
  function mot(t, enc, taille){ return '<span style="font-family:var(--f-libelle);font-weight:700;font-size:'+(taille||15)+'px;letter-spacing:.02em;text-transform:uppercase;color:'+enc+';-webkit-text-fill-color:'+enc+';white-space:nowrap">'+t+'</span>'; }
  function dessin(o, c){ var cv=document.createElement('canvas'), D=3; cv.width=390*D; cv.height=420*D; cv.style.cssText='position:absolute;left:0;top:0;width:390px;height:420px'; o.appendChild(cv); var g=cv.getContext('2d'); g.scale(D,D);
    var E='#201908', y=c.yDessin, k=c.petit?0.62:1;
    if(c.dessin==='trois'){ var T=['#FF3E00','#5600D6','#E60073','#0040FF','#201908','#00C85A','#FFB8D2','#F6FF00','#FFF7DE'];
      PEN.trace(g, PEN.mot(34, y+36, 70*k), 8, 'E2', T[1]); PEN.trace(g, PEN.coeur(300, y+4, 30*k), 8, 'E2', T[0]); PEN.trace(g, PEN.etoile(232, y-18, 22*k), 4.5, 'E2', T[3]);
      PEN.trace(g, PEN.lent(40, y+62, 150*k), 4.5, 'E2', T[2]); PEN.trace(g, PEN.rapide(210, y+62, 120*k), 4.5, 'E2', T[5]); PEN.trace(g, PEN.coeur(60, y-36, 14*k), 2.5, 'E2', T[7]); PEN.trace(g, PEN.etoile(340, y+52, 14*k), 2.5, 'E2', T[8]); PEN.trace(g, PEN.point(190,y-40), 8, 'E2', T[6]); PEN.trace(g, PEN.point(206,y-34), 8, 'E2', T[4]); }
    else if(c.dessin){ PEN.trace(g, PEN.mot(40, y+36, 70*k), 4.5, c.effile||'E2', c.encreDessin||E); PEN.trace(g, PEN.coeur(292, y+2, 28*k), 4.5, c.effile||'E2', c.encreDessin||E); } }
  /* la rangée d'outils */
  function rangee(o, c){ var enc=c.encCorps, inv=c.corps, y=c.yRow, sel=c.sel, sym=(c.symbole==='S2')?S2():IC.S1, outils=[['plume',IC.plume,'Plume'],['gomme',IC.gomme,'Gomme'],['annuler',IC.annuler,'Annuler'],['couleur',sym,'Couleur']];
    if(c.compo==='A'){ outils.forEach(function(t,i){ o.appendChild(disque(24+i*58, y, t[1], enc, inv, sel===t[0])); });
      o.appendChild(el('left:'+(366-104)+'px;top:'+y+'px;width:104px;height:44px;border-radius:22px;background:'+enc+';display:flex;align-items:center;justify-content:center', mot('Poser', inv))); c.xOutil={plume:24,gomme:82,annuler:140,couleur:198}; }
    if(c.compo==='B'){ var pf=c.plateau, pe=c.encPlateau, yb=c.yBande; o.appendChild(el('left:24px;top:'+yb+'px;width:342px;height:60px;border-radius:30px;border:2px solid '+pe+';background:'+pf));
      outils.forEach(function(t,i){ o.appendChild(disque(34+i*50, yb+8, t[1], pe, pf, sel===t[0], 44, sel===t[0]?2:0)); });
      o.appendChild(el('left:'+(366-24-70)+'px;top:'+yb+'px;width:70px;height:60px;display:flex;align-items:center;justify-content:flex-end', mot('Poser', pe)));
      o.appendChild(el('left:'+(366-24-70-15)+'px;top:'+(yb+16)+'px;width:2px;height:28px;background:'+pe+';opacity:.9')); c.xOutil={plume:34,gomme:84,annuler:134,couleur:184}; c.yOutils=yb+8; }
    if(c.compo==='C'){ var x=24; c.xOutil={}; outils.concat([['poser','', 'Poser']]).forEach(function(t){ var s=sel===t[0], plein=s||t[0]==='poser'; var p=el('left:'+x+'px;top:'+y+'px;height:44px;border-radius:22px;border:2px solid '+enc+';padding:0 15px 0 '+(t[1]?11:15)+'px;display:flex;align-items:center;gap:7px;color:'+(plein?inv:enc)+';background:'+(plein?enc:'transparent'), t[1]+mot(t[2], plein?inv:enc, 13)); o.appendChild(p); c.xOutil[t[0]]=x; x+=p.getBoundingClientRect().width/(document.getElementById('device').getBoundingClientRect().width/390)+8; }); }
    if(c.yOutils==null) c.yOutils=y; }
  function tailles(o, c){ var enc=(c.compo==='B')?c.encPlateau:c.encCorps, fond=(c.compo==='B')?c.plateau:c.corps, x=c.xOutil[c.sel]||24, y=c.yOutils-54;
    var p=el('left:'+x+'px;top:'+y+'px;width:118px;height:44px;border-radius:22px;border:2px solid '+enc+';background:'+fond+';display:flex;align-items:center;justify-content:space-evenly');
    [6,10,16].forEach(function(d,i){ var h=el('position:relative;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;'+(i===(c.taille==null?1:c.taille)?'border:2px solid '+enc+';':'')); h.style.position='relative'; h.appendChild((function(){ var q=document.createElement('i'); q.style.cssText='display:block;width:'+d+'px;height:'+d+'px;border-radius:50%;background:'+enc; return q; })()); p.appendChild(h); }); o.appendChild(p); }
  function couleur(o, c){ var enc=c.encCorps, fond=c.corps, y=c.yRow+54, P=c.palette||['#82AEF8','#FFB8D2','#C9A8F5','#EFE3C7'], ong=c.onglet||'TRAIT';
    var p=el('left:24px;top:'+y+'px;width:342px;height:128px;border-radius:30px;border:2px solid '+enc+';background:'+fond); o.appendChild(p);
    ['TRAIT','FOND'].forEach(function(t,i){ var s=t===ong; p.appendChild(el('left:'+(10+i*161)+'px;top:10px;width:157px;height:44px;border-radius:22px;border:2px solid '+enc+';background:'+(s?enc:'transparent')+';display:flex;align-items:center;justify-content:center', mot(t==='TRAIT'?'Trait':'Fond', s?fond:enc))); });
    var tons=P.slice(); if(ong==='TRAIT') tons.push(c.encreMode); var fondAct=c.fondChoisi||CHAMP[c.nat];
    tons.forEach(function(t,i){ var gris=(ong==='TRAIT'&&t.toUpperCase()===fondAct.toUpperCase()), d=el('left:'+(16+i*64)+'px;top:66px;width:44px;height:44px;border-radius:50%;border:2px solid '+enc+';background:'+t+';opacity:'+(gris?.28:1)); p.appendChild(d);
      if((ong==='TRAIT'&&i===(c.tonChoisi==null?4:c.tonChoisi))||(ong==='FOND'&&t.toUpperCase()===fondAct.toUpperCase())) p.appendChild(el('left:'+(16+i*64-5)+'px;top:61px;width:54px;height:54px;border-radius:50%;border:2px solid '+enc)); }); }
  function montre(c){ nettoie(); var o=racine(), L=document.documentElement.classList.contains('light')||!!document.querySelector('.light'); c.light=c.light!=null?c.light:L;
    c.corps=c.light?'#F7F0DE':CORPS[c.nat]; c.encCorps=c.light?'#201908':'#F7F0DE'; c.plateau=c.light?'#F7F0DE':'#050302'; c.encPlateau=c.light?'#201908':'#F7F0DE'; c.encreMode=c.light?'#201908':'#F7F0DE';
    if(c.cacheBas){ o.appendChild(el('left:0;top:'+c.cacheBas[0]+'px;width:390px;height:'+(c.cacheBas[1]-c.cacheBas[0])+'px;background:'+c.corps)); }
    if(c.descend){ [].forEach.call(document.querySelectorAll(c.descend[0]), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.transform='translateY('+c.descend[1]+'px)'; }); }
    if(c.cachePhoto){ [].forEach.call(document.querySelectorAll('.ph-photo-btn'), function(e){ e.setAttribute('data-ov-cache','1'); e.style.visibility='hidden'; }); }
    if(c.dessin) dessin(o, c);
    if(c.compo) rangee(o, c);
    if(c.etat==='tailles') tailles(o, c);
    if(c.etat==='couleur') couleur(o, c);
    if(c.oeil){ o.appendChild(disque(c.oeil[0], c.oeil[1], c.oeil[2]?IC.oeilNon:IC.oeil, '#201908', '', false, 34, 1)); }
    if(c.pilules){ c.pilules.forEach(function(p){ o.appendChild(el('right:'+(390-p[0])+'px;top:'+p[1]+'px;height:44px;border-radius:22px;border:2px solid #F7F0DE;background:#201908;padding:0 20px;display:flex;align-items:center', mot(p[2], '#F7F0DE'))); }); }
    return c; }
  return {montre:montre, nettoie:nettoie};
})();
