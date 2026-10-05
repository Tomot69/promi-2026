import io
S=io.open('app.html',encoding='utf-8').read()
lot = r'''<style id="lot-V131-ENTIER-css">
/* ⚑ v131 (Tom, 5 oct. 2026, C-051) — VOIR UNE PHOTO (ou un dessin) EN ENTIER. Un fond PLEIN, la seiche — jamais une transparence, ni
   une ombre, ni un fondu (la Pelote est le seul volume). L'image entière, sans recadrage : on y voit aussi ce que l'encart du haut cachait. */
#device #entierVue{position:absolute;left:0;top:0;width:100%;height:100%;z-index:400;display:none;background:var(--c-seiche10);margin:0;padding:0;border:0;border-radius:inherit;overflow:hidden}
#device #entierVue.ouv{display:block}
#device #entierVue img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:contain;display:block;margin:0;max-width:none}
#device #entierVue .ev-x{position:absolute;top:40px;right:24px;height:60px;padding:0 4px 0 12px;display:flex;align-items:center;background:none;border:0;margin:0;
  font-family:var(--f-libelle);font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--c-creme95);-webkit-text-fill-color:var(--c-creme95);cursor:pointer}
</style>
<script id="lot-V131-ENTIER">
/* ⚑ v131 (Tom, C-051) — « Dans toute fiche, toucher la bande quand elle porte un dessin ou une photo (jamais la dalle) l'affiche en
   entier, par-dessus le reste de l'écran. […] Un nouveau toucher, ou ✕, referme. VoiceOver : « Voir la photo en entier ». »
   Construit pour les PHOTOS (le dessin viendra avec l'outil : `source()` rendra alors aussi le dessin).
   · le toucher se lit sur le geste lui-même (appui puis lever sans glisser) : la fiche ne produit pas toujours de `click` au doigt (§8) ;
   · « dans la bande » se lit sur ce qui est PEINT : le canevas de la bande est opaque jusqu'à l'onde, transparent dessous ;
   · rien ne survit à `closeAll` : la vue inscrit son rangeur. La fiche dessous n'est pas touchée (aucun style, aucune classe). */
(function(){
  function dev(){ return document.getElementById('device'); }
  function fiche(){ var dp=document.getElementById('detailPoster'); return (dp && dp.classList.contains('show')) ? dp : null; }
  /* ce que la bande porte : une photo (le dessin viendra) — jamais la dalle */
  function source(){ try{ var dp=fiche(); if(!dp) return null;
      if(dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) return null;      /* un Cercle ne porte pas de photo aujourd'hui */
      if(typeof cur!=='undefined' && cur && cur.photo) return {src:cur.photo, quoi:'photo'}; }catch(_){ } return null; }
  function vue(){ var v=document.getElementById('entierVue'); if(v) return v; var d=dev(); if(!d) return null;
    v=document.createElement('div'); v.id='entierVue'; v.setAttribute('role','dialog'); v.setAttribute('aria-modal','true');
    v.innerHTML='<img alt=""><button type="button" class="ev-x" aria-label="Fermer">✕ Fermer</button>';
    d.appendChild(v); return v; }
  function ouverte(){ var v=document.getElementById('entierVue'); return !!(v && v.classList.contains('ouv')); }
  function ferme(){ var v=document.getElementById('entierVue'); if(!v || !v.classList.contains('ouv')) return false;
    v.classList.remove('ouv'); var im=v.querySelector('img'); if(im) im.removeAttribute('src'); return true; }
  function ouvre(){ var s=source(), v=s&&vue(); if(!v) return false;
    v.setAttribute('aria-label', s.quoi==='photo' ? 'La photo en entier' : 'Le dessin en entier');
    var im=v.querySelector('img'); im.src=s.src; im.alt = s.quoi==='photo' ? 'La photo de cette parole, en entier' : 'Le dessin de cette parole, en entier';
    v.classList.add('ouv'); return true; }
  window._entier={ouvre:ouvre, ferme:ferme, ouverte:ouverte};
  (window._rangeurs = window._rangeurs || []).push(function(){ ferme(); });

  /* le point est-il DANS LA BANDE, sur ce qu'elle peint, et sur rien d'autre (ni le plateau, ni le bouton photo, ni un menu) ? */
  function dansBande(x, y){ var dp=fiche(), cv=document.getElementById('dpTrameCv'); if(!dp || !cv) return false;
    var h=document.elementFromPoint(x, y); if(!h) return false;
    if(h.closest && h.closest('.enh, .ph-photo-nid, .ph-photo-btn, button, a, input, textarea, #dpDetails, #entierVue')) return false;
    if(!(h===cv || h===dp || (dp.contains(h) && !h.closest('#dpMain')))) return false;
    var r=cv.getBoundingClientRect(); if(x<r.left||x>r.right||y<r.top||y>r.bottom) return false;
    try{ var px=cv.getContext('2d').getImageData(Math.round((x-r.left)*cv.width/r.width), Math.round((y-r.top)*cv.height/r.height), 1, 1).data; return px[3]>200; }catch(_){ return false; } }

  /* le geste : appui puis lever, moins de 10 px, moins de 600 ms — et le clic qui pourrait suivre est avalé une fois */
  var G=null, AVALE=0;
  document.addEventListener('pointerdown', function(e){ G={x:e.clientX, y:e.clientY, t:performance.now(), vue:ouverte()}; }, true);
  document.addEventListener('pointerup', function(e){ var g=G; G=null; if(!g) return;
    if(Math.abs(e.clientX-g.x)>10 || Math.abs(e.clientY-g.y)>10 || performance.now()-g.t>600) return;
    if(g.vue){ if(ouverte()){ ferme(); AVALE=performance.now(); e.preventDefault(); e.stopPropagation(); } return; }      /* un nouveau toucher, ou ✕ : referme */
    if(!source() || !dansBande(e.clientX, e.clientY)) return;
    if(ouvre()){ AVALE=performance.now(); e.preventDefault(); e.stopPropagation(); } }, true);
  document.addEventListener('click', function(e){
    if(performance.now()-AVALE<450){ AVALE=0; e.preventDefault(); e.stopPropagation(); return; }
    /* un clic sans geste (clavier, lecteur d'écran) */
    if(ouverte()){ if(e.target && e.target.closest && e.target.closest('#entierVue')){ ferme(); e.preventDefault(); e.stopPropagation(); } return; }
    if(e.target && e.target.id==='dpTrameCv' && e.detail===0 && source()){ if(ouvre()){ e.preventDefault(); e.stopPropagation(); } } }, true);
  document.addEventListener('keydown', function(e){
    if(ouverte() && (e.key==='Escape' || e.key==='Enter' || e.key===' ')){ ferme(); e.preventDefault(); return; }
    if((e.key==='Enter' || e.key===' ') && e.target && e.target.id==='dpTrameCv' && source()){ if(ouvre()) e.preventDefault(); } }, true);

  /* VoiceOver : la bande ne se déclare commande QUE lorsqu'elle porte une photo ; on compare avant d'écrire (§8) */
  function annonce(){ var cv=document.getElementById('dpTrameCv'); if(!cv) return; var s=source();
    var veut = s ? (s.quoi==='photo' ? 'Voir la photo en entier' : 'Voir le dessin en entier') : null;
    if(veut){ if(cv.getAttribute('aria-label')!==veut){ cv.setAttribute('role','button'); cv.setAttribute('tabindex','0'); cv.setAttribute('aria-label', veut); cv.setAttribute('data-entier','1'); } }
    else if(cv.getAttribute('data-entier')){ cv.removeAttribute('role'); cv.removeAttribute('tabindex'); cv.removeAttribute('aria-label'); cv.removeAttribute('data-entier'); } }
  ['_fichePose','_ficheTrait'].forEach(function(nom){ var f=window[nom];
    if(typeof f==='function' && !f.__entier){ var g=function(){ var r=f.apply(this,arguments); try{ annonce(); }catch(_){ } return r; }; g.__entier=true; for(var k in f){ try{ g[k]=f[k]; }catch(_){ } } window[nom]=g; } });
  window._entier.annonce=annonce;
})();
</script>
</body>'''
assert S.count("</script>\n</body>")==1
S=S.replace("</script>\n</body>", "</script>\n"+lot)
io.open('app.html','w',encoding='utf-8').write(S)
