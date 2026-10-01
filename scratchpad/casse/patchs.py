# -*- coding: utf-8 -*-
"""Les sept correctifs, un par un, dans l'ordre. Chacun est (nom, ancien, nouveau)."""

P1_OLD = """    /* LA LISTE D'ENTRÉES SE MÉMORISE. `_s4Index` remplace le contenu de #indexList : au
       second appel les `.ix-bloc` de l'app n'existent plus, et l'écran restait figé sur la
       densité du premier rendu (constaté au duo — « 3 par ligne » redonnait 2 par ligne).
       On garde donc ce que `buildIndex` a décidé — l'ordre, le filtre et le tri — et on
       peut reposer la présentation autant de fois qu'on veut. */
    var blocs=[].slice.call(li.querySelectorAll('.ix-bloc'));
    if(blocs.length){ window._s4Entrees=blocs.map(function(b){
      return b.hasAttribute('data-nuee') ? {nuee:b.getAttribute('data-nuee')}
                                         : {id:+b.getAttribute('data-id')}; }); }
    var ent=window._s4Entrees||[];
    if(!ent.length) return;"""
P1_NEW = """    /* LA LISTE D'ENTRÉES SE MÉMORISE — MAIS SEULEMENT QUAND `buildIndex` VIENT DE PARLER.
       ⚠ LE CACHE AVALAIT LE FILTRE. Une recherche sans résultat fait écrire à `buildIndex`
       un « Rien ici » et AUCUN `.ix-bloc` : je lisais alors zéro bloc, je gardais les 28
       entrées d'avant et je les reposais — la recherche ne filtrait plus rien (CASSE A6).
       « Zéro entrée » est une réponse, pas une absence de réponse. */
    if(window._s4Frais){
      window._s4Entrees=[].slice.call(li.querySelectorAll('.ix-bloc')).map(function(b){
        return b.hasAttribute('data-nuee') ? {nuee:b.getAttribute('data-nuee')}
                                           : {id:+b.getAttribute('data-id')}; });
      window._s4Vide = li.innerHTML;
      window._s4Frais = false;
    }
    var ent=window._s4Entrees||[];
    if(!ent.length){
      if(window._s4Vide && /ix-empty/.test(window._s4Vide)) li.innerHTML=window._s4Vide;
      return;
    }"""
P1B_OLD = """    window.buildIndex=function(){ var r=_biOrig.apply(this,arguments);
      try{ libelles(); armer(); window._s4Index(); }catch(_){}
      return r; };"""
P1B_NEW = """    window.buildIndex=function(){ var r=_biOrig.apply(this,arguments);
      window._s4Frais = true;
      try{ libelles(); armer(); window._s4Index(); }catch(_){}
      return r; };"""

P2_OLD = """    var lus=items.map(function(it){
      var pid=it.getAttribute('data-pid'), nk=it.getAttribute('data-nuee');
      var tx=it.querySelector('.fd-tx'), tt=it.querySelector('.fd-t');
      return {pid:pid?+pid:null, nk:nk,
              texte:tx?(tx.textContent||'').trim():'', quand:tt?(tt.textContent||'').trim():''};
    });
    li.innerHTML=''; li.appendChild(gr);
    lus.forEach(function(F,i){"""
P2_NEW = """    var lus=items.map(function(it){
      var pid=it.getAttribute('data-pid'), nk=it.getAttribute('data-nuee');
      var tx=it.querySelector('.fd-tx'), tt=it.querySelector('.fd-t');
      /* ⚠ LES ACTIONS DU FIL SE RELÈVENT ET SE REPOSENT — ELLES NE SE PERDENT PAS.
         Le Fil est le SEUL endroit d'où l'on tient une parole sans ouvrir de fiche. */
      var actes=[].slice.call(it.querySelectorAll('[data-keep],[data-post],[data-releve],[data-react]'))
        .map(function(a){
          var q = a.hasAttribute('data-keep') ? 'keep'
                : a.hasAttribute('data-post') ? 'post'
                : a.hasAttribute('data-releve') ? 'releve' : 'react';
          return {quoi:q, fid:+(a.getAttribute('data-'+q)||0),
                  mot:(a.textContent||'').trim(), fort:a.classList.contains('fd-acc')||q==='keep'||q==='releve'};});
      return {pid:pid?+pid:null, nk:nk, actes:actes,
              texte:tx?(tx.textContent||'').trim():'', quand:tt?(tt.textContent||'').trim():''};
    });
    li.innerHTML=''; li.appendChild(gr);
    var yCur=0;
    gr.style.height=(lus.reduce(function(a,F){return a+PAS+(F.actes.length?62:0);},0)+40)+'px';
    lus.forEach(function(F,i){"""
P2B_OLD = """      d.style.cssText='left:'+X+'px;top:'+(i*PAS)+'px;width:'+W+'px;height:'+H+'px;'
        +'border-radius:22px;background:'+fond+';';"""
P2B_NEW = """      d.style.cssText='left:'+X+'px;top:'+yCur+'px;width:'+W+'px;height:'+H+'px;'
        +'border-radius:22px;background:'+fond+';';"""
P2C_OLD = """      if(p){ var ii=p.id; d.onclick=function(){ setView('toile'); openDetail(ii); }; }
      else if(F.nk){ var kk=F.nk; d.onclick=function(){ setView('toile'); openEssaim(kk); }; }
    });
  }catch(err){} };"""
P2C_NEW = """      if(p){ var ii=p.id; d.onclick=function(){ setView('toile'); openDetail(ii); }; }
      else if(F.nk){ var kk=F.nk; d.onclick=function(){ setView('toile'); openEssaim(kk); }; }
      yCur += PAS;
      /* LE GESTE, sous le bandeau. Pastille d'action du §3.5. Le bandeau reste celui du
         moodboard — 358 × 128, trois boîtes fixes — on n'y touche pas. */
      if(F.actes.length){
        var barre=document.createElement('div');
        barre.className='s4-actes';
        barre.style.cssText='position:absolute;left:'+(X+16)+'px;top:'+(yCur-12)+'px;'
          +'height:50px;display:flex;align-items:center;gap:12px;z-index:3';
        F.actes.forEach(function(A){
          var t=document.createElement('button');
          t.className='s4-acte'+(A.fort?' fort':'');
          t.textContent=A.mot;
          t.style.cssText='height:50px;border-radius:25px;padding:0 19px;box-sizing:border-box;'
            +'font-family:Bricolage,system-ui,sans-serif;font-weight:700;font-size:16px;'
            +'line-height:1;cursor:pointer;background:transparent;'
            +(A.fort ? ('border:3px solid '+e.col+';color:'+e.col+';-webkit-text-fill-color:'+e.col)
                     : ('border:0;color:'+e.colTexte+';-webkit-text-fill-color:'+e.colTexte));
          t.onclick=function(ev){ ev.stopPropagation();
            try{
              if(A.quoi==='keep') feedKeep(A.fid);
              else if(A.quoi==='post') feedPostpone(A.fid);
              else if(A.quoi==='releve') feedReleve(A.fid);
              else if(A.quoi==='react'){ feedReacted[A.fid]=!feedReacted[A.fid]; buildFeed(); }
              if(window.syncAll) syncAll();
            }catch(_){}
          };
          barre.appendChild(t);
        });
        gr.appendChild(barre);
        yCur += 62;
      }
    });
  }catch(err){} };"""

P3_OLD = """    inp.oninput = function(){
      P.titre = inp.value;
      try{ var t = document.getElementById('fTitle'); if(t){ t.value = inp.value;
        t.dispatchEvent(new Event('input', {bubbles:true})); } }catch(_){}
    };"""
P3_NEW = """    inp.oninput = function(){
      P.titre = inp.value;
      try{ var t = document.getElementById('fTitle'); if(t){ t.value = inp.value;
        t.dispatchEvent(new Event('input', {bubbles:true})); } }catch(_){}
      /* ⚠ LA PHRASE SUIT LE DOIGT (CASSE A1). On ne rejoue PAS `_phraseRendu()` ici : il
         reconstruit #csPhrase, donc il détruirait le champ qui reçoit la frappe. On met à
         jour LE SEUL créneau touché, puis on redonne ses cotes à l'écran (§2.8). */
      try{
        var m = document.querySelector('#csPhrase [data-ph=titre]');
        if(m){
          var v = (inp.value||'').trim();
          m.classList.toggle('ph-vide', !v);
          var cible = m.querySelector('.ph-mot') || m;
          cible.textContent = v || (inp.getAttribute('placeholder')||'');
        }
        if(window._ppTout) _ppTout();
      }catch(_){}
    };"""

P4_OLD = """    if(_avec) h += '<em>avec</em> ' + pl('avec', P.avec, false) + '<br>';"""
P4_NEW = """    /* ⚠ LE SECOND CRÉNEAU D'UN CHICHE EST LE COMPAGNON, ET IL S'AFFICHE TOUJOURS
       (décision Tom). Vide, il prend le contour pointillé de la pastille vide (§2.8). */
    h += '<em>avec</em> ' + pl('avec', _avec ? P.avec : 'qui ?', !_avec) + '<br>';"""

P5_OLD = """    var qui=document.getElementById('dptQui'), ti=document.getElementById('dptTitre'), qd=document.getElementById('dptQuand');
    pose(qui,{top:e.yQui+'px', color:e.colTexte, '-webkit-text-fill-color':e.colTexte, 'font-size':e.quiFs+'px'});"""
P5_NEW = """    var qui=document.getElementById('dptQui'), ti=document.getElementById('dptTitre'), qd=document.getElementById('dptQuand');
    /* ⚠ LE MOT D'ÉTAT D'UN CHICHE (CASSE C5) : « LANCÉ », pas « EN COURS ». Les trois mots
       sont ceux des cadres 72 à 77 ; la fiche et la carte d'Index se contredisaient. */
    if(qd && e.nat==='chiche'){
      var duo2 = !!(p && p.avec);
      qd.textContent = (p && p.status==='tenu') ? (duo2 ? 'TENU À DEUX' : 'TENUE')
                     : (p && p.status==='rate') ? 'À RELEVER' : 'LANCÉ';
    }
    pose(qui,{top:e.yQui+'px', color:e.colTexte, '-webkit-text-fill-color':e.colTexte, 'font-size':e.quiFs+'px'});"""

P6_OLD = """      liste.appendChild(B.reg('IMPORTANT', lu('impSeg'), {hote:B.emprunte('impSeg')}));
      liste.appendChild(B.reg('URGENT', lu('urgSeg'), {hote:B.emprunte('urgSeg')}));"""
P6_NEW = """      /* ⚠ « URGENT » NE REVIENT PAS (décision Tom) : le concept est abandonné, et l'app le
         savait déjà — l. 9705, « Urgent supprimé », suivi d'une règle qui masque #urgSeg.
         J'avais pris ce masquage pour un oubli de portage. Voir CLAUDE.md §9. */"""

P6B_OLD = """      <div class="arr" data-mode="urgence"><div class="ag" id="ag-urgence"></div><div class="at"><div class="an">Urgence</div><div class="ad">les plus urgents se densifient au cœur</div></div></div>"""
P6B_NEW = """      <!-- « Urgence » retiré : concept abandonné (décision Tom, 18 août 2026). -->"""

# ⚠ LE `.field` SE RETIRE EN ENTIER, SA FERMETURE COMPRISE. Mon premier motif s'arrêtait
# sur le `</div>` de `.impseg` et laissait celui de `.field` orphelin : le HTML se
# déséquilibrait, toute la structure du formulaire se décalait, et la section 2 passait de
# 0 à 212 écarts (« entête (-16, 1528) »). Ce n'était pas un conflit de conception, c'était
# une erreur de découpe.
P6C_OLD = ('<div class="field"><label>Urgent&nbsp;?</label><div class="impseg" id="urgSeg">'
           '<div class="is" data-urg="1">·</div><div class="is on" data-urg="2">··</div>'
           '<div class="is" data-urg="3">···</div></div></div>')
P6C_NEW = '<!-- « Urgent ? » retiré du formulaire : concept abandonné (décision Tom). -->'

P7_BLOC = """
<style id="lot-REPARATIONS-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════
   RÉPARATIONS (CASSE.md) — bloc neuf, aucune règle existante touchée.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
/* §3.8 · LE BLOC DU CERCLE EST FLOUTÉ : les quatre réglages montrent ce que Le Cercle
   ouvre, ils ne l'ouvrent pas. Sans le flou, un réglage payant se lit comme un gratuit. */
#device #detailPoster .s2-cercle > .s2-reg,
#device #settingsScreen .s2-cercle > .s2-reg,
#device #createSheet .s2-cercle > .s2-reg{
  filter:blur(2.4px)!important;pointer-events:none!important;cursor:default!important}
/* l'encart reste NET : seule superposition autorisée du produit (§3.8). */
#device .s2-cercle > .s2-encart,
#device .s2-cercle > .set-cercle{filter:none!important;pointer-events:auto!important}
</style>
</body>"""

CORRECTIFS = [
    ('A6 · la recherche de l\'Index',   [(P1_OLD,P1_NEW),(P1B_OLD,P1B_NEW)]),
    ('A7 · TENIR et REPORTER au Fil',   [(P2_OLD,P2_NEW),(P2B_OLD,P2B_NEW),(P2C_OLD,P2C_NEW)]),
    ('A1 · la phrase suit le doigt',    [(P3_OLD,P3_NEW)]),
    ('C7 · le compagnon du Chiche',     [(P4_OLD,P4_NEW)]),
    ('C5 · un Chiche dit « LANCÉ »',    [(P5_OLD,P5_NEW)]),
    ('C1 · URGENT retiré',              [(P6_OLD,P6_NEW),(P6B_OLD,P6B_NEW),(P6C_OLD,P6C_NEW)]),
    ('§3.8 · le Cercle flouté',         [('</body>', P7_BLOC)]),
]
