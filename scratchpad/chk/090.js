
(function(){
  /* 4 · le Fil ouvert est une classe que le code pose (§8) : on la reflète sur #device, en comparant avant d'écrire */
  function fil(){ var f=document.getElementById('feedView'), d=document.getElementById('device'); if(!f||!d) return;
    var o=f.classList.contains('in'); if(d.classList.contains('vue-fil')!==o) d.classList.toggle('vue-fil', o); }
  function veille(){ var f=document.getElementById('feedView'); if(!f){ setTimeout(veille,300); return; }
    new MutationObserver(fil).observe(f,{attributes:true,attributeFilter:['class']}); fil(); }
  if(document.readyState!=='loading') veille(); else document.addEventListener('DOMContentLoaded', veille);

  /* 6 · LA FICHE D'INFORMATION DE L'AURA, à jour de ce que l'écran montre (Tom, 14 sept.). En gratuit : la sphère, la phrase,
     les Noyaux, ce que tu as tenu, partager. Avec le Cercle : ce que le Cercle ouvre VRAIMENT aujourd'hui — ses cinq réglages et
     ses trois designs. Ses blocs d'Aura (graphes, réciprocité) ne sont pas dessinés (Q196.2) : ils ne sont plus annoncés. */
  var ILL={
    sphere:'<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="15" fill="#82AEF8"/><path d="M17 17 Q21 14 24 18 Q25 22 20 23 Q16 22 17 17Z" fill="#C9A8F5"/><path d="M27 26 Q32 24 33 29 Q32 33 28 32 Q25 30 27 26Z" fill="#DD4D23"/></svg>',
    phrase:'<svg viewBox="0 0 48 48" fill="none" stroke="#C9A8F5" stroke-width="2.6" stroke-linecap="round"><path d="M10 18H38M10 25H34M10 32H26"/></svg>',
    noyaux:'<svg viewBox="0 0 48 48" fill="none" stroke-width="3.2"><circle cx="16" cy="24" r="8" stroke="__TENU__"/><circle cx="34" cy="24" r="6" stroke="#DD4D23"/></svg>',   /* ⚑ 22 sept. : l'icône DÉPEINT des arcs — elle porte donc les valeurs d'état, et elle bascule */
    tenu:'<svg viewBox="20 20 152 168" fill="#00341A"><path d="M40 34 Q80 24 94 56 Q102 90 66 98 Q30 102 26 68 Q22 40 40 34Z"/><path d="M120 62 Q160 56 166 92 Q170 126 132 132 Q100 134 100 100 Q100 70 120 62Z" fill="#291547"/><path d="M58 122 Q96 116 106 148 Q110 178 74 182 Q42 184 40 152 Q40 128 58 122Z" fill="#C9A8F5"/></svg>',
    partage:'<svg viewBox="0 0 48 48" fill="none" stroke="#82AEF8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M24 30V10"/><path d="M17 17l7-7 7 7"/><path d="M14 24v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V24"/></svg>',
    reglages:'<svg viewBox="0 0 48 48" fill="none" stroke="#C9A8F5" stroke-width="2.6"><rect x="8" y="12" width="32" height="10" rx="5"/><rect x="8" y="27" width="32" height="10" rx="5"/></svg>',
    designs:'<svg viewBox="0 0 48 48"><circle cx="17" cy="19" r="8" fill="#DD4D23"/><circle cx="31" cy="19" r="8" fill="#82AEF8"/><circle cx="24" cy="31" r="8" fill="#C9A8F5"/></svg>'
  };
  function carte(ill,t,s){ return '<div class="ah-card"><div class="ah-ill">'+String(ILL[ill]).replace('__TENU__','#00341A')+'</div><div class="ah-tx"><div class="ah-t">'+t+'</div><div class="ah-s">'+s+'</div></div></div>'; }
  function aide(){
    var h=document.getElementById('auraHelp'); if(!h) return; var l=h.querySelector('.ah-list'); if(!l || l.getAttribute('data-a-jour')==='1') return;
    var lg=h.querySelector('.ah-legend');
    /* ⚑ 21 sept. — l'aide est posée sur la PAGE : elle bascule comme la légende de l'Aura. */
    if(lg) lg.innerHTML='<span><i style="background:#00341A"></i>TENUES</span>'
      +'<span><i style="background:#291547"></i>EN COURS</span>'
      +'<span><i style="background:#DD4D23"></i>À TENIR</span>';
    l.innerHTML='<div class="ah-sect"><span class="ah-badge free">En gratuit</span></div>'
      /* ⚑ v94 (Tom, 28 sept. : « courts, clairs et informatifs, mais dans le ton — on parle de la tendance de l'harmonie entre les gens
         et soi, pas d'une définition technique. Et la Pelote doit y être expliquée ») — il renverse « l'aide dit ce qu'on peut faire, pas
         ce que c'est » pour la Pelote. Mots à valider : QUESTIONS · Q350. */
      +carte('sphere','La Pelote','Chaque parole tenue y devient une île : elle s’étoffe à mesure que tu tiens. Touche une île pour la revoir.')
      +carte('phrase','La phrase','Sous la Pelote, quelques mots pour te rappeler ce que tu as déjà tenu.')
      +carte('noyaux','Les Noyaux','<b>Toi</b>, puis chaque personne avec qui tu échanges des paroles. L’anneau dit où vous en êtes : <b>tenu</b>, <b>en cours</b>, <b>à tenir</b>.')
      +carte('tenu','Ce que tu as tenu','Tes paroles tenues, dans l’ordre où tu les as tenues. Touche-en une pour la revoir.')
      +carte('partage','Partager ma Pelote','Une image à partager : on y voit que tu tiens parole, jamais ce que tu as promis.')
      +'<div class="ah-sect"><span class="ah-badge prem">Avec Ma Parole !</span></div>'
      +'<div class="ah-cercle-cta set-cercle" id="ahCercleCta" role="button"><div class="sc-tx"><div class="sc-t">✦ Ma Parole !</div></div><div class="sc-go">›</div></div>'
      +'<div class="ah-locked" id="ahLocked">'
      +carte('reglages','Peaufiner, avec Ma Parole !','Récurrence, rappel, importance, mémoire et <b>la couleur</b> de ta dalle — sur chaque Promi, Chiche et Cercle.')
      +carte('designs','Les designs signature','Ramage, Madrure et Volubilis pour ta Toile.')   /* v95 (Tom) : trois des payants, les plus vendeurs — les anciens noms étaient des noms de code */
      +'</div>';
    l.setAttribute('data-a-jour','1');
    /* l'encart garde sa porte : il ouvre le Cercle, comme avant */
    var cta=document.getElementById('ahCercleCta');
    if(cta) cta.addEventListener('click', function(ev){ ev.stopPropagation(); try{ h.classList.remove('show'); var pl=document.getElementById('plusScreen'); if(pl) pl.classList.add('show'); }catch(_){}   /* la porte d'origine (l. ~9025) */ });
  }
  if(document.readyState!=='loading') aide(); else document.addEventListener('DOMContentLoaded', aide);
  setTimeout(aide, 600);
})();
