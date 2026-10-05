/* PLANCHE v130 (C-042) — posé PAR-DESSUS l'app par le script de planche, jamais dans l'app. Rangée A SOUS le trait, déploiements SOUS la rangée ; rien dans la bande. */
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
  function nettoie(){ var o=document.getElementById('ovC042'); if(o) o.remove(); [].forEach.call(document.querySelectorAll('[data-ov-dy]'), function(e){ e.style.removeProperty('transform'); if(e.getAttribute('data-ov-tr')) e.style.transform=e.getAttribute('data-ov-tr'); e.removeAttribute('data-ov-dy'); }); [].forEach.call(document.querySelectorAll('[data-ov-clone]'), function(e){ e.remove(); }); [].forEach.call(document.querySelectorAll('[data-ov-cache]'), function(e){ e.style.removeProperty('visibility'); e.removeAttribute('data-ov-cache'); }); }
  function disque(x, y, ic, enc, inv, sel, d, bord){ d=d||44; return outil(el('left:'+x+'px;top:'+y+'px;width:'+d+'px;height:'+d+'px;border-radius:50%;border:'+(bord==null?2:bord)+'px solid '+enc+';display:flex;align-items:center;justify-content:center;color:'+(sel?inv:enc)+';background:'+(sel?enc:'transparent'), ic)); }
  function outil(e){ e.setAttribute('data-ov-outil','1'); return e; }
  function mot(t, enc, taille){ return '<span style="font-family:var(--f-libelle);font-weight:700;font-size:'+(taille||15)+'px;letter-spacing:.02em;text-transform:uppercase;color:'+enc+';-webkit-text-fill-color:'+enc+';white-space:nowrap">'+t+'</span>'; }
  function dessin(o, c){ var cv=document.createElement('canvas'), D=3; cv.width=390*D; cv.height=420*D; cv.style.cssText='position:absolute;left:0;top:0;width:390px;height:420px'; o.appendChild(cv); var g=cv.getContext('2d'); g.scale(D,D);
    var E='#201908', y=c.yDessin, k=c.petit?0.62:1;
    if(c.dessin==='trois'){ var T=['#FF3E00','#5600D6','#E60073','#0040FF','#201908','#00C85A','#FFB8D2','#F6FF00','#FFF7DE'];
      PEN.trace(g, PEN.mot(34, y+36, 70*k), 8, 'E2', T[1]); PEN.trace(g, PEN.coeur(300, y+4, 30*k), 8, 'E2', T[0]); PEN.trace(g, PEN.etoile(232, y-18, 22*k), 4.5, 'E2', T[3]);
      PEN.trace(g, PEN.lent(40, y+62, 150*k), 4.5, 'E2', T[2]); PEN.trace(g, PEN.rapide(210, y+62, 120*k), 4.5, 'E2', T[5]); PEN.trace(g, PEN.coeur(60, y-36, 14*k), 2.5, 'E2', T[7]); PEN.trace(g, PEN.etoile(340, y+52, 14*k), 2.5, 'E2', T[8]); PEN.trace(g, PEN.point(190,y-40), 8, 'E2', T[6]); PEN.trace(g, PEN.point(206,y-34), 8, 'E2', T[4]); }
    else if(c.dessin){ PEN.trace(g, PEN.mot(c.petit?56:40, y+36, 70*k), c.base||4.5, c.effile||'E2', c.encreDessin||E); PEN.trace(g, PEN.coeur(c.petit?262:292, y+2, 28*k), c.base||4.5, c.effile||'E2', c.encreDessin||E); } }
  /* la rangée d'outils */
  function rangee(o, c){ var enc=c.encCorps, inv=c.corps, y=c.yRow, sel=c.sel, sym=(c.symbole==='S2')?S2():IC.S1, outils=[['plume',IC.plume,'Plume'],['gomme',IC.gomme,'Gomme'],['annuler',IC.annuler,'Annuler'],['couleur',sym,'Couleur']];
    if(c.compo==='A'){ outils.forEach(function(t,i){ o.appendChild(disque(24+i*58, y, t[1], enc, inv, sel===t[0])); });
      o.appendChild(outil(el('left:'+(366-104)+'px;top:'+y+'px;width:104px;height:44px;border-radius:22px;background:'+enc+';display:flex;align-items:center;justify-content:center', mot('Poser', inv)))); c.xOutil={plume:24,gomme:82,annuler:140,couleur:198}; }
    if(c.compo==='B'){ var pf=c.plateau, pe=c.encPlateau, yb=c.yBande; o.appendChild(el('left:24px;top:'+yb+'px;width:342px;height:60px;border-radius:30px;border:2px solid '+pe+';background:'+pf));
      outils.forEach(function(t,i){ o.appendChild(disque(34+i*50, yb+8, t[1], pe, pf, sel===t[0], 44, sel===t[0]?2:0)); });
      o.appendChild(el('left:'+(366-24-70)+'px;top:'+yb+'px;width:70px;height:60px;display:flex;align-items:center;justify-content:flex-end', mot('Poser', pe)));
      o.appendChild(el('left:'+(366-24-70-15)+'px;top:'+(yb+16)+'px;width:2px;height:28px;background:'+pe+';opacity:.9')); c.xOutil={plume:34,gomme:84,annuler:134,couleur:184}; c.yOutils=yb+8; }
    if(c.compo==='C'){ var x=24; c.xOutil={}; outils.concat([['poser','', 'Poser']]).forEach(function(t){ var s=sel===t[0], plein=s||t[0]==='poser'; var p=el('left:'+x+'px;top:'+y+'px;height:44px;border-radius:22px;border:2px solid '+enc+';padding:0 15px 0 '+(t[1]?11:15)+'px;display:flex;align-items:center;gap:7px;color:'+(plein?inv:enc)+';background:'+(plein?enc:'transparent'), t[1]+mot(t[2], plein?inv:enc, 13)); o.appendChild(p); c.xOutil[t[0]]=x; x+=p.getBoundingClientRect().width/(document.getElementById('device').getBoundingClientRect().width/390)+8; }); }
    if(c.yOutils==null) c.yOutils=y; }
  function tailles(o, c){ var enc=(c.compo==='B')?c.encPlateau:c.encCorps, fond=(c.compo==='B')?c.plateau:c.corps, x=c.xOutil[c.sel]||24, y=c.yOutils+52;
    var p=el('left:'+x+'px;top:'+y+'px;width:118px;height:44px;border-radius:22px;border:2px solid '+enc+';background:'+fond+';display:flex;align-items:center;justify-content:space-evenly');
    [6,10,16].forEach(function(d,i){ var h=el('position:relative;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;'+(i===(c.taille==null?1:c.taille)?'border:2px solid '+enc+';':'')); h.style.position='relative'; h.appendChild((function(){ var q=document.createElement('i'); q.style.cssText='display:block;width:'+d+'px;height:'+d+'px;border-radius:50%;background:'+enc; return q; })()); p.appendChild(h); }); o.appendChild(outil(p)); }
  function couleur(o, c){ var enc=c.encCorps, fond=c.corps, y=c.yRow+52, P=c.palette||['#82AEF8','#FFB8D2','#C9A8F5','#EFE3C7'], ong=c.onglet||'TRAIT';
    var p=el('left:24px;top:'+y+'px;width:342px;height:114px;border-radius:30px;border:2px solid '+enc+';background:'+fond); o.appendChild(outil(p));
    ['TRAIT','FOND'].forEach(function(t,i){ var s=t===ong; p.appendChild(el('left:'+(8+i*163)+'px;top:6px;width:159px;height:44px;border-radius:22px;border:2px solid '+enc+';background:'+(s?enc:'transparent')+';display:flex;align-items:center;justify-content:center', mot(t==='TRAIT'?'Trait':'Fond', s?fond:enc))); });
    var tons=P.slice(); if(ong==='TRAIT') tons.push(c.encreMode); var fondAct=c.fondChoisi||CHAMP[c.nat];
    tons.forEach(function(t,i){ var gris=(ong==='TRAIT'&&t.toUpperCase()===fondAct.toUpperCase()), d=el('left:'+(16+i*64)+'px;top:58px;width:44px;height:44px;border-radius:50%;border:2px solid '+enc+';background:'+t+';opacity:'+(gris?.28:1)); p.appendChild(d);
      if((ong==='TRAIT'&&i===(c.tonChoisi==null?4:c.tonChoisi))||(ong==='FOND'&&t.toUpperCase()===fondAct.toUpperCase())) p.appendChild(el('left:'+(16+i*64-4)+'px;top:54px;width:52px;height:52px;border-radius:50%;border:2px solid '+enc)); }); }
  /* v128 — le dessin REMPLACE la dalle : la bande sans sa matière (planche seulement : on repeint le champ là où la dalle est peinte) */
  function sansDalle(o, c){ var cv=document.getElementById('dpTrameCv'); if(!cv) return; var dv=document.getElementById('device').getBoundingClientRect(), r=cv.getBoundingClientRect();
    var k=document.createElement('canvas'); k.width=cv.width; k.height=cv.height; k.style.cssText='position:absolute;left:'+(r.left-dv.left)+'px;top:'+(r.top-dv.top)+'px;width:'+r.width+'px;height:'+r.height+'px';
    var g=k.getContext('2d'); g.drawImage(cv,0,0); var I=g.getImageData(0,0,k.width,k.height), d=I.data, W=k.width, H=k.height, ch=CHAMP[c.nat], R=parseInt(ch.slice(1,3),16), G=parseInt(ch.slice(3,5),16), B=parseInt(ch.slice(5,7),16);
    function garde(i){ var r=d[i], gg=d[i+1], b=d[i+2]; return (0.3*r+0.59*gg+0.11*b)<95 || (r>185&&gg<140&&b<95); }   /* le trait (sombre ou orange) reste */
    var out=new Uint8ClampedArray(d.length); out.set(d); var pas=Math.max(2,Math.round(W/390*2));
    for(var y=0;y<H;y++) for(var x=0;x<W;x++){ var i=(y*W+x)*4; if(d[i+3]<200) continue; if(Math.abs(d[i]-R)+Math.abs(d[i+1]-G)+Math.abs(d[i+2]-B)<12) continue; if(garde(i)) continue;
        var pres=false; for(var q=0;q<4&&!pres;q++){ var xx=x+[pas,-pas,0,0][q], yy=y+[0,0,pas,-pas][q]; if(xx>=0&&yy>=0&&xx<W&&yy<H&&garde((yy*W+xx)*4)) pres=true; } if(pres) continue;
        out[i]=R; out[i+1]=G; out[i+2]=B; out[i+3]=255; }
    I.data.set(out); g.putImageData(I,0,0);
    /* le plateau reste devant : on ajoure la copie à sa place (24, 40, 342 × 60, rayon 30, trait compris) */
    if(!c.epure){ var sx=W/r.width, ox=(24-(r.left-dv.left))*sx, oy=(40-(r.top-dv.top))*sx, pw=342*sx, ph=60*sx, rr=30*sx; g.globalCompositeOperation='destination-out'; g.beginPath(); g.moveTo(ox+rr,oy); g.arcTo(ox+pw,oy,ox+pw,oy+ph,rr); g.arcTo(ox+pw,oy+ph,ox,oy+ph,rr); g.arcTo(ox,oy+ph,ox,oy,rr); g.arcTo(ox,oy,ox+pw,oy,rr); g.closePath(); g.fill(); g.globalCompositeOperation='source-over'; }
    o.appendChild(k); }
  function fleche(o, c){ var cv=document.createElement('canvas'), D=3; cv.width=390*D; cv.height=844*D; cv.style.cssText='position:absolute;left:0;top:0;width:390px;height:844px'; o.appendChild(cv); var g=cv.getContext('2d'); g.scale(D,D);
    var x=c.fleche[0], y=c.fleche[1], x0=x-78, y0=y-62; g.strokeStyle='#201908'; g.lineWidth=4.5; g.lineCap='round'; g.lineJoin='round';
    g.beginPath(); g.moveTo(x0,y0); g.quadraticCurveTo(x-18,y0-6,x-9,y-12); g.stroke(); g.beginPath(); g.moveTo(x-22,y-15); g.lineTo(x-7,y-9); g.lineTo(x-4,y-25); g.stroke(); }
  function menu(o, c){ var ch=document.querySelector('.chip'), cs=ch?getComputedStyle(ch):null, h=c.menu.h||33, ecart=c.menu.ecart||4, fs=cs?parseFloat(cs.fontSize):13, fam=cs?cs.fontFamily:'var(--f-libelle)', pad=cs?parseFloat(cs.paddingLeft):14, y=c.menu.y;
    window._ovChip=cs?{h:ch.getBoundingClientRect().height, fs:cs.fontSize, fam:cs.fontFamily.split(',')[0], pad:cs.paddingLeft, rayon:cs.borderRadius, trait:cs.borderTopWidth, tt:cs.textTransform, poids:cs.fontWeight}:null;
    c.menu.items.forEach(function(t){ o.appendChild(el('right:'+(390-c.menu.x)+'px;top:'+y+'px;height:'+h+'px;border-radius:'+(h/2)+'px;border:2px solid #F7F0DE;background:#201908;padding:0 '+Math.max(12,pad)+'px;display:flex;align-items:center', '<span style="font-family:'+fam.replace(/"/g,"'")+';font-weight:'+(cs?cs.fontWeight:700)+';font-size:'+fs+'px;letter-spacing:.02em;text-transform:'+(cs?cs.textTransform:'uppercase')+';color:#F7F0DE;-webkit-text-fill-color:#F7F0DE;white-space:nowrap">'+t+'</span>')); y+=h+ecart; }); }
  /* v129 — LE MODE DESSIN LIBÈRE L'ÉCRAN : les disques et leurs noms disparaissent ; l'encart du haut ne garde que son contour, au trait fin */
  function epure(o, c){ var P=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect();
    function cache(e){ if(!e) return; e.setAttribute('data-ov-cache','1'); e.style.setProperty('visibility','hidden','important'); }
    var toi=(c.epure===2)?null:[].filter.call(P.querySelectorAll('*'), function(e){ return e.children.length===0 && (e.textContent||'').trim()==='Toi'; })[0];
    if(toi){ var n=toi; while(n.parentElement && n.parentElement!==P && n.getBoundingClientRect().width<200) n=n.parentElement; cache(n); }
    [].forEach.call(P.querySelectorAll('.enh'), function(e){ var r=e.getBoundingClientRect(); if(r.top-dv.top<110) cache(e); });
    o.appendChild(el('left:24px;top:40px;width:342px;height:60px;border-radius:30px;border:1px solid #201908;background:transparent')); }
  function montre(c){ nettoie(); var o=racine(), L=document.documentElement.classList.contains('light')||!!document.querySelector('.light'); c.light=c.light!=null?c.light:L;
    var _bg=(getComputedStyle(document.getElementById('detailPoster')).backgroundColor.match(/[\d.]+/g)||[247,240,222]).map(Number); c.corps='rgb('+_bg[0]+','+_bg[1]+','+_bg[2]+')'; c.encCorps=((0.2126*_bg[0]+0.7152*_bg[1]+0.0722*_bg[2])>128)?'#201908':'#F7F0DE'; c.plateau=c.light?'#F7F0DE':'#050302'; c.encPlateau=c.light?'#201908':'#F7F0DE'; c.encreMode=c.light?'#201908':'#F7F0DE';
    if(c.cacheBas){ o.appendChild(el('left:0;top:'+c.cacheBas[0]+'px;width:390px;height:'+(c.cacheBas[1]-c.cacheBas[0])+'px;background:'+c.corps)); }
    if(c.descend){ [].forEach.call(document.querySelectorAll(c.descend[0]), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.transform='translateY('+c.descend[1]+'px)'; }); }
    if(c.cacheSel){ c.cacheSel.forEach(function(s){ [].forEach.call(document.querySelectorAll(s), function(e){ e.setAttribute('data-ov-cache','1'); e.style.setProperty('visibility','hidden','important'); }); }); }
    if(c.descendSel){ c.descendSel[0].forEach(function(s){ [].forEach.call(document.querySelectorAll(s), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.setProperty('transform','translateY('+c.descendSel[1]+'px)','important'); }); }); }
    if(c.seulTitre){ var P=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect(), ti=document.getElementById('dptTitre');
      [].forEach.call(P.querySelectorAll('*'), function(e){ if(e===ti||e.contains(ti)||ti.contains(e)) return; if(e.closest('#dpDetails')) return; var r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return; if(e.tagName==='CANVAS'&&e.id==='dpTrameCv') return;
        if(r.top-dv.top>=c.seulTitre[0]-1 && e.children.length===0 || (e.tagName==='CANVAS'&&r.top-dv.top>=c.seulTitre[0]-1)){ e.setAttribute('data-ov-cache','1'); e.style.setProperty('visibility','hidden','important'); } });
      [].forEach.call(P.querySelectorAll('*'), function(e){ if(e===ti||e.contains(ti)||ti.contains(e)||e.closest('#dpDetails')||e.id==='dpTrameCv') return; var r=e.getBoundingClientRect(), cs=getComputedStyle(e); if(r.top-dv.top>=c.seulTitre[0]-1 && r.top-dv.top<760 && (parseFloat(cs.borderTopWidth)>0 || (cs.backgroundColor!=='rgba(0, 0, 0, 0)' && cs.backgroundColor!==getComputedStyle(P).backgroundColor) || cs.backgroundImage!=='none')){ e.setAttribute('data-ov-cache','1'); e.style.setProperty('visibility','hidden','important'); ti.style.setProperty('visibility','visible','important'); } });
      ti.setAttribute('data-ov-tr', ti.style.transform||''); ti.setAttribute('data-ov-dy','1'); ti.style.setProperty('transform','translateY('+c.seulTitre[1]+'px)','important'); }
    if(c.bloc){ [].forEach.call(document.querySelectorAll(c.bloc[0]), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.setProperty('transform','translateY('+c.bloc[1]+'px)','important'); }); }
    if(c.cachePhoto){ [].forEach.call(document.querySelectorAll('.ph-photo-btn'), function(e){ e.setAttribute('data-ov-cache','1'); e.style.setProperty('visibility','hidden','important'); }); }
    if(c.sansDalle) sansDalle(o, c);
    if(c.epure) epure(o, c);
    if(c.photoMock){ o.appendChild(disque(c.photoMock[0], c.photoMock[1], '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.2"/></svg>', '#201908', '', false, 34, 1)); }
    if(c.dessin) dessin(o, c);
    if(c.fleche) fleche(o, c);
    if(c.menu) menu(o, c);
    if(c.compo) rangee(o, c);
    if(c.etat==='tailles') tailles(o, c);
    if(c.etat==='couleur') couleur(o, c);
    if(c.oeil){ o.appendChild(disque(c.oeil[0], c.oeil[1], c.oeil[2]?IC.oeilNon:IC.oeil, '#201908', '', false, 34, 1)); }
    if(c.pilules){ c.pilules.forEach(function(p){ o.appendChild(el('right:'+(390-p[0])+'px;top:'+p[1]+'px;height:44px;border-radius:22px;border:2px solid #F7F0DE;background:#201908;padding:0 20px;display:flex;align-items:center', mot(p[2], '#F7F0DE'))); }); }
    return c; }
  function preuve(){ var dv=document.getElementById('device').getBoundingClientRect(), L=[].map.call(document.querySelectorAll('#ovC042 [data-ov-outil]'), function(e){ var r=e.getBoundingClientRect(); return [r.top-dv.top, r.bottom-dv.top]; });
    return {n:L.length, haut:Math.min.apply(null,L.map(function(x){return x[0];})), bas:Math.max.apply(null,L.map(function(x){return x[1];}))}; }
  return {montre:montre, nettoie:nettoie, preuve:preuve};
})();
