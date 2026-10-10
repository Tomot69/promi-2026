import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:70]); S=S.replace(o,n)
ICO='<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" data-symbole="enregistrer"><path d="M16 7 L16 20 M16 20 L11.5 15.5 M16 20 L20.5 15.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 19 L8.5 25 L23.5 25 L23.5 19" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
# 1 · la vue en entier : l'icône seule, pour une photo comme pour un dessin
rep("""<button type="button" class="ev-garde" data-v139="enregistrer">Enregistrer la photo</button>';""",
    """<button type="button" class="ev-garde enr-btn" data-v139="enregistrer" aria-label="Enregistrer">"""+ICO+"""</button>';   /* v140 (C-091) : une icône seule, la même partout ; VoiceOver « Enregistrer » */""")
rep("""    var eg=v.querySelector('.ev-garde'); if(eg){ eg.style.display = s.quoi==='photo' ? '' : 'none'; }   /* v139 : seulement pour une photo */""",
    """    var eg=v.querySelector('.ev-garde'); if(eg){ eg.style.display=''; eg.setAttribute('data-quoi', s.quoi); }   /* v140 (C-091) : photo ET dessin */""")
rep("""    var ext=(/^data:image\\/(png|webp|gif)/.exec(src)||[])[1]||'jpg', nom='promi-photo.'+ext;""",
    """    var _eg=v.querySelector('.ev-garde'), ext=(/^data:image\\/(png|webp|gif)/.exec(src)||[])[1]||'jpg', nom=((_eg&&_eg.getAttribute('data-quoi')==='dessin')?'promi-dessin.':'promi-photo.')+ext;""")
rep("""#device #entierVue .ev-garde{position:absolute;left:50%;bottom:46px;transform:translateX(-50%);height:44px;padding:0 20px;border-radius:22px;""",
    """#device #entierVue .ev-garde.enr-btn{width:44px;padding:0;display:grid;place-items:center}
#device #entierVue .ev-garde.enr-btn svg{width:28px;height:28px;display:block}
#device #entierVue .ev-garde{position:absolute;left:50%;bottom:46px;transform:translateX(-50%);height:44px;padding:0 20px;border-radius:22px;""")
# 2 · le lot : l'icône au plateau de l'accueil — enregistrer l'image de sa Toile
LOT = r"""
<style id="lot-V140-ENREGISTRER-css">
/* v140 (Tom, 10 oct. 2026, C-091) — UN SEUL BOUTON ENREGISTRER, PARTOUT : une icône seule, sans texte, la même grammaire que ses voisines */
#device .acc-plat #enrToile{left:186px!important}
</style>
<script id="lot-V140-ENREGISTRER">
/* ⚑ v140 (Tom, 10 oct. 2026, C-091) — « Un seul bouton Enregistrer, partout. Une icône seule, sans texte, discrète, la même partout où l'on
   peut enregistrer : photo en plein écran, dessin en plein écran, la Toile (pour enregistrer son image) […]. VoiceOver : “Enregistrer”.
   Même grammaire que les icônes de fiche. » OÙ ELLE PARAÎT : ① la vue en entier d'une photo ; ② la vue en entier d'un dessin (`.ev-garde`,
   `lot-V131-ENTIER`) ; ③ le plateau de l'accueil, à gauche de Partager : l'image de la Toile telle qu'on la voit (thème, monde, titres),
   rendue par le moteur (`Toile.renderTo`), jamais une capture d'écran. La feuille de partage du téléphone quand elle prend un fichier
   (elle porte « Enregistrer l'image »), sinon un téléchargement. */
(function(){
  var ICO='__ICO__';
  function fichier(src, nom){ try{ window._enrCompte=(window._enrCompte||0)+1; window._enrDernier={nom:nom, n:src.length};
      function telecharge(){ try{ var a=document.createElement('a'); a.href=src; a.download=nom; a.rel='noopener'; document.body.appendChild(a); a.click(); a.parentNode.removeChild(a); }catch(_){ } }
      try{ if(navigator.share && navigator.canShare && /^data:/.test(src)){ var p=src.split(','), bin=atob(p[1]), u=new Uint8Array(bin.length); for(var i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i);
          var fi=new File([u], nom, {type:(/^data:([^;]+)/.exec(src)||[])[1]||'image/png'}); if(navigator.canShare({files:[fi]})){ navigator.share({files:[fi]}).catch(function(){}); return true; } } }catch(_){ }
      telecharge(); return true; }catch(_){ return false; } }
  function toile(){ try{ var TL=window.Toile; if(!TL || !TL.renderTo) return false; var d=document.getElementById('device'), cv=document.createElement('canvas');
      if(!TL.renderTo(cv, 3, !!(d && d.classList.contains('light')))) return false;
      return fichier(cv.toDataURL('image/png'), 'promi-toile.png'); }catch(_){ return false; } }
  window._enr={icone:ICO, fichier:fichier, toile:toile};
  function pose(){ var pl=document.getElementById('accPlat'); if(!pl) return false; if(document.getElementById('enrToile')) return true;
    var b=document.createElement('div'); b.className='dctrl enr-btn'; b.id='enrToile'; b.setAttribute('role','button'); b.setAttribute('tabindex','0'); b.setAttribute('aria-label','Enregistrer');
    b.innerHTML=ICO; b.onclick=function(ev){ ev.stopPropagation(); toile(); };
    var sh=document.getElementById('shareBtn'); if(sh && sh.parentNode===pl) pl.insertBefore(b, sh); else pl.appendChild(b); return true; }
  (function essaie(n){ if(!pose() && n<100) setTimeout(function(){ essaie(n+1); }, 100); })(0);
})();
</script>
""".replace('__ICO__',ICO)
rep("</body>\n\n</html>", LOT+"</body>\n\n</html>")
io.open('app.html','w',encoding='utf-8').write(S)
