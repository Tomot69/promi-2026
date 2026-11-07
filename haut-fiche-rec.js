/* haut-fiche-rec.js — l'enregistreur de la sentinelle C-255 (redteam_haut_fiche.py, banc-haut-fiche.html). v184a, 7 nov. 2026.
   Posé dans la fenêtre de l'app (window.HF). Il relève, à CHAQUE IMAGE, la place (en pt de l'appareil 390 × 844) et la présence des éléments du haut d'une
   fiche — en-tête, ligne « Avec … » / phrase, titre, ligne d'état, le + des membres, les Noyaux — et la barre Peaufiner, avec le défilement de la fiche.
   Il juge lui-même (le même code dans WebKit et dans Safari iOS) : aucun élément qui défile ne bouge d'autre chose que du défilement (un saut), l'en-tête et la
   barre ne bougent pas, et, revenu en haut, chaque élément est à sa place d'ouverture et présent. Il ne touche à rien de l'app. */
(function(){
  var W = window, D = document;
  var IDS = {qui:'dptQui', titre:'dptTitre', etat:'dptQuand', plus:'cerclePlusMembres', noyaux:'dAura', barre:'dpDetails'};
  function dp(){ return D.getElementById('detailPoster'); }
  function ech(){ var d=dp(); return W._echDp ? W._echDp(d) : 1; }
  function el(k){ if(k==='tete'){ var d=dp(); return d && d.querySelector(':scope > .enh'); } return D.getElementById(IDS[k]); }
  function vu(e){ if(!e) return false; var cs=getComputedStyle(e), r=e.getBoundingClientRect(); if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<0.05||r.height<2) return false;
    for(var a=e.parentElement; a && a!==D.body; a=a.parentElement){ var c=getComputedStyle(a); if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false; } return true; }
  var CLES=['tete','qui','titre','etat','plus','noyaux','barre'];
  function releve(){ var d=dp(), dv=D.getElementById('device'); if(!d||!dv) return null; var R=dv.getBoundingClientRect(), k=ech(), o={st:Math.round(d.scrollTop*100)/100, t:performance.now()};
    CLES.forEach(function(c){ var e=el(c); if(!e){ o[c]=null; return; } var r=e.getBoundingClientRect(); o[c]=[Math.round((r.top-R.top)/k*10)/10, vu(e)?1:0, Math.round(r.height/k)]; });
    var q=el('qui'); o.quiTx=q ? (q.textContent||'').trim().slice(0,40) : ''; return o; }
  var F=null, run=false;
  function boucle(){ if(!run) return; var r=releve(); if(r) F.push(r); requestAnimationFrame(boucle); }
  /* juge une suite d'images : un élément qui défile se déplace EXACTEMENT de −Δdéfilement (± 1,5 pt) ; l'en-tête et la barre ne bougent pas (± 0,5) */
  function sauts(fr, nature){ var pire={v:0}, L=[];
    for(var i=1;i<fr.length;i++){ var a=fr[i-1], b=fr[i], ds=b.st-a.st;
      ['qui','titre','etat','noyaux'].concat(nature==='cercle'?['plus']:[]).forEach(function(c){ if(!a[c]||!b[c]) return;
        if(a[c][1]!==b[c][1] && c!=='plus') L.push({i:i, el:c, quoi:'présence '+a[c][1]+'→'+b[c][1], st:b.st});
        if(!a[c][1]||!b[c][1]) return;
        var e=Math.abs((b[c][0]-a[c][0]) + ds); if(e>pire.v) pire={v:e, el:c, i:i, st:b.st}; if(e>1.5) L.push({i:i, el:c, quoi:'saut '+e.toFixed(1)+' pt', st:b.st}); });
      if(a.tete&&b.tete){ var et=Math.abs(b.tete[0]-a.tete[0]); if(et>0.5) L.push({i:i, el:'tete', quoi:'en-tête bougé '+et.toFixed(1), st:b.st}); }
      if(b.barre && b.barre[1] && Math.abs(b.barre[0]-760)>0.5) L.push({i:i, el:'barre', quoi:'barre à '+b.barre[0], st:b.st}); }
    return {pire:pire, defauts:L.slice(0,12), n:L.length, images:fr.length}; }
  function compare(o, r, nature){ var L=[]; ['tete','qui','titre','etat','noyaux','barre'].concat(nature==='cercle'?['plus']:[]).forEach(function(c){
      if(!o[c]) return; if(!r[c]){ L.push(c+' absent'); return; }
      if(o[c][1] && !r[c][1]) L.push(c+' caché');
      if(Math.abs(r[c][0]-o[c][0])>0.5) L.push(c+' '+o[c][0]+'→'+r[c][0]); });
    if(nature==='cercle' && !/^Avec /.test(r.quiTx||'')) L.push('ligne « Avec … » : « '+r.quiTx+' »');
    return L; }
  W.HF = { releve:releve, start:function(){ F=[]; run=true; requestAnimationFrame(boucle); }, stop:function(){ run=false; var f=F; F=null; return f; },
           sauts:sauts, compare:compare };
})();
