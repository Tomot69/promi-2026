import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
# 1 · le dessin d'un sujet de partage
a="  /* ══ LA VUE ENTIÈRE (C-051) ══ */\n  function sourceVue(){"
r(a,"""  /* ⚑ v137 (Tom, 8 oct. 2026, C-068) — LE PARTAGE DU DESSIN : le dessin posé et NON MASQUÉ du sujet partagé (une parole, ou un Cercle),
     entier, avec sa nature. Un dessin masqué pour soi n'est jamais rendu ici ; une photo n'y passe jamais (ce n'est pas un dessin). */
  window._dessinPartage=function(s){ try{ if(!s) return null; var d=null, nat=null;
      if(s.nuee){ d=cercles()[s.nuee]||null; nat='Cercle'; }
      else if(s.ids && s.ids.length===1){ var p=promises.filter(function(x){ return x.id===s.ids[0]; })[0]; if(p){ d=p.dessin||null; nat=p.chiche?'Chiche':'Promi'; } }
      if(!pose_(d) || d.masque) return null; return {cv:entier(d, 3), fond:d.fond, nat:nat}; }catch(_){ return null; } };
"""+a)
# 2 · la planche du partage
a=" g.fillStyle=ground; g.fillRect(0,0,W,H);\n"
r(a,a+""" /* ⚑ v137 (Tom, 8 oct. 2026, C-068) — LE PARTAGE DU DESSIN. « Seul un dessin se partage, jamais une photo importée. L'image partagée porte
    par défaut la mention de la nature (Promi, Chiche ou Cercle) et le logo en bas à gauche. Un réglage, dans les Réglages, masque la
    mention : il ne reste alors que le dessin et le logo. Le logo est toujours là. Un dessin masqué pour soi n'est jamais partagé. »
    Quand le rond Partager d'une fiche est touché et que cette parole (ou ce Cercle) porte un dessin posé et non masqué, l'image EST le
    dessin, entier (rendu de ses traits, jamais une capture), sur son fond ; en bas à gauche le logo, et au-dessus de lui la mention.
    Sans dessin (ou masqué) : Mon Folio réduit à la parole, comme avant — la case y rend la DALLE, jamais la photo. */
 var _dps=null; try{ _dps=(window._partageFiche && window._partageFiche.actif && window._partageFiche.actif() && window._dessinPartage) ? window._dessinPartage(window._partageFicheSujet) : null; }catch(_e){ _dps=null; }
 try{ var _scr=document.getElementById('shareScreen'); if(_scr && _scr.classList.contains('sh-dessin')!==!!_dps) _scr.classList.toggle('sh-dessin', !!_dps); }catch(_e){}
 window._shDessinSeul=!!_dps;
 if(_dps && _dps.cv && _dps.cv.width){
   var _f=String(_dps.fond||ground), _m=/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(_f), _lum=_m?(0.2126*parseInt(_m[1],16)+0.7152*parseInt(_m[2],16)+0.0722*parseInt(_m[3],16)):0;
   var _enc=_lum>140?'#201908':'#F7F0DE', _ment=!(window._dessinMention && window._dessinMention()===false);
   g.fillStyle=_f; g.fillRect(0,0,W,H);
   var _k=Math.min(W/_dps.cv.width, H/_dps.cv.height), _w=_dps.cv.width*_k, _h=_dps.cv.height*_k; g.drawImage(_dps.cv, (W-_w)/2, (H-_h)/2, _w, _h);
   var _mg=W*0.066, _fs=W*0.092, _yl=H-_mg; g.textAlign='left'; g.textBaseline='alphabetic'; g.fillStyle=_enc;
   g.font='400 '+_fs+'px PromiLate,Gilbert,system-ui'; g.fillText('Promi', _mg, _yl);
   if(_ment){ g.font='700 '+(W*0.040)+'px Gilbert,system-ui'; try{ g.letterSpacing=(W*0.004)+'px'; }catch(_e){} g.fillText(String(_dps.nat).toUpperCase(), _mg, _yl-_fs*0.98); try{ g.letterSpacing='0px'; }catch(_e){} }
   try{ cv.setAttribute('data-dessin-partage', _dps.nat+'|'+(_ment?1:0)+'|'+_enc); window._plancheComp=[]; }catch(_e){}
   return; }
 try{ cv.removeAttribute('data-dessin-partage'); }catch(_e){}
""")
# 3 · l'export : ni mot-marque du haut ni QR sur un dessin partagé
r("      marque(g, Wc, Hc);\n      try{ _shPreviewQR(g, Wc, Hc); }catch(_){}","      if(!window._shDessinSeul){ marque(g, Wc, Hc);\n      try{ _shPreviewQR(g, Wc, Hc); }catch(_){} }   /* v137 (C-068) : le dessin partagé porte SON logo, en bas à gauche */")
r("  window._partageFiche={ deja:function(){ return performance.now()-tDoigt<800; }, rends:rends };","  window._partageFiche={ deja:function(){ return performance.now()-tDoigt<800; }, rends:rends, actif:function(){ return !!AV; } };")
# 4 · le réglage
a='<script id="lot-V136-PHRASE">'
r(a,"""<style id="lot-V137-MENTION-css">
/* v137 (C-068) — l'aperçu d'un dessin partagé : le mot-marque du haut et le QR se retirent, le dessin porte son logo en bas à gauche */
#device#device #shareScreen.sh-dessin #shBadge, #device#device #shareScreen.sh-dessin #shQR{display:none!important}
</style>
<script id="lot-V137-MENTION">
/* ⚑ v137 (Tom, 8 oct. 2026, C-068) — LE RÉGLAGE DE LA MENTION. « Un réglage, dans les Réglages, masque la mention : il ne reste alors que
   le dessin et le logo. Le logo est toujours là. » Une rangée du groupe « Partager » des Réglages, mémorisée (`promi_dessin_mention`,
   '0' = masquée). Les mots (« Mention sur un dessin partagé », « affichée », « masquée ») : les plus sobres, à valider (Q416). */
(function(){
  var K='promi_dessin_mention';
  window._dessinMention=function(){ try{ return localStorage.getItem(K)!=='0'; }catch(_){ return true; } };
  function maj(c){ var v=c.querySelector('.v'), on=window._dessinMention(); if(v) v.textContent=(on?'affichée':'masquée')+' ›'; c.setAttribute('aria-pressed', on?'true':'false'); c.setAttribute('aria-label','Mention sur un dessin partagé, '+(on?'affichée':'masquée')); }
  function pose(){ var inv=document.getElementById('setInvite'); if(!inv || document.getElementById('setMention')) return !!inv;
    var c=document.createElement('div'); c.className='scard'; c.id='setMention'; c.setAttribute('role','button'); c.tabIndex=0;
    c.innerHTML='<span class="k">Mention sur un dessin partagé</span><span class="v ac"></span>';
    inv.parentNode.insertBefore(c, inv.nextSibling); maj(c);
    c.addEventListener('click', function(){ try{ localStorage.setItem(K, window._dessinMention()?'0':'1'); }catch(_){ } maj(c); try{ if(window._shDessinSeul && window.shareRender) window.shareRender(); }catch(_){ } });
    return true; }
  if(!pose()){ var n=0, t=setInterval(function(){ if(pose() || ++n>40) clearInterval(t); }, 250); }
})();
</script>
"""+a)
io.open('app.html','w',encoding='utf-8').write(S)
