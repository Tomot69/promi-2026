import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""        if(cur.chiche && cur.avec && cur.avec!==_w) _m += ' · avec '+cur.avec;
      }
      if(qw.textContent!==_m) qw.textContent=_m;""",
"""        if(cur.chiche && cur.avec && cur.avec!==_w) _m += ' · avec '+cur.avec;
      }
      /* ⚑ v136 (Tom, 7 oct. 2026, C-069) — LA PHRASE COMPLÈTE, DANS LA FICHE D'UN PROMI OU D'UN CHICHE : « La ligne À moi / À Rachel
         disparaît, la phrase la remplace. » Le titre reste dans `#dptTitre` (le plus visible) ; cette ligne porte le reste de la phrase. */
      var _F = (!cur.draft && window._phraseFiche) ? window._phraseFiche(cur, qw.getAttribute('data-deplie')===String(cur.id)) : null;
      if(_F){ if(qw.getAttribute('data-phrase')!==_F.sig){ qw.innerHTML=_F.html; qw.setAttribute('data-phrase',_F.sig); qw.setAttribute('aria-label',_F.voix); } }
      else { qw.removeAttribute('data-phrase'); qw.removeAttribute('aria-label'); if(qw.textContent!==_m) qw.textContent=_m; }""")
r("""    pose(ti ,{top:e.yTitre+'px', color:encre, '-webkit-text-fill-color':encre, 'font-size':e.titreFs+'px'});""",
"""    /* v136 (C-069) : la phrase peut tenir sur deux lignes et plus (plusieurs personnes, liste dépliée) — le titre et ce qui le suit
       descendent de ce qu'elle prend en plus d'une ligne (une cote dérivée : bas réel de la phrase, jamais une cote figée, §8) */
    var _yT=e.yTitre; try{ if(qui && qui.getAttribute('data-phrase')){ qui.style.setProperty('white-space','normal','important'); var _scq=(dp.clientWidth||W)/W, _hq=qui.getBoundingClientRect().height/_scq, _lh1=parseFloat(getComputedStyle(qui).lineHeight)/1||e.quiFs*1.2; if(_hq>_lh1*1.5) _yT=Math.round(e.yTitre+_hq-_lh1); } }catch(_q){}
    pose(ti ,{top:_yT+'px', color:encre, '-webkit-text-fill-color':encre, 'font-size':e.titreFs+'px'});""")
r("    var yEtat = Math.round(e.yTitre + hTitre + 26.3);","    var yEtat = Math.round(_yT + hTitre + 26.3);")
a='<script id="lot-V136-HALO0">'; assert S.count(a)==1
S=S.replace(a,'''<style id="lot-V136-PHRASE-css">
/* v136 (C-069) : la phrase de la fiche — une ligne discrète au-dessus du titre ; « + x personnes » est un bouton sans dessin, dans le texte */
#device #detailPoster #dptQui[data-phrase]{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;max-width:342px!important}
#device #detailPoster #dptQui .dpt-plus{all:unset;cursor:pointer;font:inherit;color:inherit;-webkit-text-fill-color:currentColor;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1.5px}
</style>
<script id="lot-V136-PHRASE">
/* ⚑ v136 (Tom, 7 oct. 2026, C-069) — LA PHRASE COMPLÈTE DANS LES FICHES PROMI ET CHICHE. « Dans les fiches seulement, jamais dans le Fil ni
   l'Index, et pour les Promi et les Chiche (pas les Cercles) : on remet la phrase entière, que le titre seul ne suffit pas à faire
   comprendre. […] Le titre reste l'élément le plus visible. […] Au-delà de quelques personnes : « … + x personnes ». Toucher cette mention
   déroule la liste complète dans la phrase, qui s'allonge vers le bas. »
   LES FORMES sont celles de la page + (lot de la phrase, `verbe`) — on n'en invente pas :
     à soi            « Je me promets de »                       à quelqu'un      « Je promets à Rachel de »
     à plusieurs      « Je promets à Rachel, Marion et Nico de » au-delà de TROIS « Je promets à Rachel, Marion + 3 personnes de »
     reçue            « Rachel me promet de »                    demandée         « Rachel, promets-moi de » · « …, promettez-moi de »
     Chiche lancé     « À Marion · avec Rachel · chiche de »     Chiche à soi     « Chiche de »
     Chiche reçu      « Marion me lance : chiche de »            (mot manquant, le plus sobre — à valider)
   « de » s'élide devant une voyelle ou un h (« d'aller »). Le titre n'est PAS dans cette ligne : il reste `#dptTitre`. */
(function(){
  var QUELQUES=3;
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function gens(v, p){ var w=String(v||'').trim(); if(!w || /^moi$/i.test(w)) return [];
    if(/groupe|nu[ée]e|tout le monde/i.test(w) && p && p.nuee){ try{ var m=(window.membresNuee?membresNuee(p.nuee):[])||[]; if(m.length) return m.slice(); }catch(_){ } }
    return w.split(/\\s*[,·]\\s*|\\s+et\\s+/).map(function(x){ return x.trim(); }).filter(function(x){ return x && !/^moi$/i.test(x); }); }
  function liste(L, deplie, id){ var n=L.length;
    if(n<=QUELQUES || deplie){ var t = n===1 ? L[0] : L.slice(0,n-1).join(', ')+' et '+L[n-1]; return {txt:t, html:'<b>'+esc(t)+'</b>'}; }
    var debut=L.slice(0,2).join(', '), reste=n-2, mot='+\\u00a0'+reste+'\\u00a0personnes';
    return {txt:debut+' '+mot, html:'<b>'+esc(debut)+'</b> <button type="button" class="dpt-plus" data-pid="'+esc(id)+'" aria-expanded="false" aria-label="'+esc(mot)+' : voir toute la liste">'+mot+'</button>'}; }
  function de(titre){ return /^[aeiouyhàâäéèêëîïôöûüù]/i.test(String(titre||'').trim()) ? 'd\\u2019' : 'de'; }
  window._phraseFiche=function(p, deplie){ if(!p || p.draft || p.nuee===true) return null;
    var D=de(p.title), W=gens(p.who, p), A=gens(p.avec, p), from=String(p.from||'moi').trim(), recu=!!from && !/^moi$/i.test(from), txt, html;
    function fin(pre, preH){ txt=pre+' '+D; html=preH+' '+D; }
    if(p.chiche){
      if(recu){ fin(from+' me lance\\u00a0: chiche', '<b>'+esc(from)+'</b> me lance\\u00a0: chiche'); }
      else { var lw=W.length?liste(W, deplie, p.id):null, la=(A.length && String(p.avec)!==String(p.who))?liste(A, deplie, p.id):null, pt='', ph='';
        if(lw){ pt+='À '+lw.txt; ph+='À '+lw.html; }
        if(la){ pt+=(pt?' · ':'')+(pt?'avec ':'Avec ')+la.txt; ph+=(ph?' · ':'')+(ph?'avec ':'Avec ')+la.html; }
        if(pt){ fin(pt+' · chiche', ph+' · chiche'); } else { fin('Chiche','Chiche'); } } }
    else if(recu){ fin(from+' me promet', '<b>'+esc(from)+'</b> me promet'); }
    else if(p.req){ var lr=liste(W.length?W:[String(p.who||'')], deplie, p.id), v=(W.length>1)?'promettez-moi':'promets-moi'; fin(lr.txt+', '+v, lr.html+', '+v); }
    else if(!W.length){ fin('Je me promets','Je me promets'); }
    else { var l=liste(W, deplie, p.id); fin('Je promets à '+l.txt, 'Je promets à '+l.html); }
    return {txt:txt, html:html, voix:txt+' '+String(p.title||''), sig:String(p.id)+'|'+(deplie?1:0)+'|'+txt}; };
  /* « + x personnes » : un toucher déroule la liste dans la phrase (elle s'allonge vers le bas). On lit le geste, la fiche ne produit pas
     toujours de `click` au doigt (§8) ; le clic qui suivrait n'a rien d'autre à faire. */
  function deroule(b){ var q=document.getElementById('dptQui'); if(!q || !b) return; q.setAttribute('data-deplie', b.getAttribute('data-pid')); q.removeAttribute('data-phrase');
    try{ if(window._ficheTrait) window._ficheTrait(); }catch(_){ } try{ if(window._fichePose) window._fichePose(); }catch(_){ } }
  var G=null;
  document.addEventListener('pointerdown', function(e){ var b=e.target && e.target.closest && e.target.closest('#dptQui .dpt-plus'); G=b?{b:b,x:e.clientX,y:e.clientY,t:performance.now()}:null; }, true);
  document.addEventListener('pointerup', function(e){ var g=G; G=null; if(!g) return; if(Math.abs(e.clientX-g.x)>10||Math.abs(e.clientY-g.y)>10||performance.now()-g.t>600) return; e.preventDefault(); e.stopPropagation(); deroule(g.b); }, true);
  document.addEventListener('click', function(e){ var b=e.target && e.target.closest && e.target.closest('#dptQui .dpt-plus'); if(b && e.detail===0){ deroule(b); } }, true);
  (window._rangeurs=window._rangeurs||[]).push(function(){ var q=document.getElementById('dptQui'); if(q){ q.removeAttribute('data-deplie'); q.removeAttribute('data-phrase'); } });
})();
</script>
'''+a)
io.open('app.html','w',encoding='utf-8').write(S)
