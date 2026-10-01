
/* ⚑ v21 (Tom, 22 sept.) — « une ligne du Fil n'a toujours pas sa dalle : reprendre l'arrosage automatique,
   un Promi de Rachel dans le potager. C'est la troisième fois. »
   CAUSE, prouvée : une entrée du journal dont le `pid` ne désigne plus le Promi (ou plus aucun) — la carte
   n'a alors AUCUN Promi : pas de dalle, et `_s4Fil` écrivait le texte brut du journal en titre, d'où le
   guillemet « orphelin en fin de ligne. (Mesuré aussi : un Promi sans cellule sur la Toile sort sans dalle.)
   PARADE, avant chaque construction du Fil : 1 · on RELIE par le titre entre guillemets une entrée dont le
   pid ne résout pas ou désigne un autre titre (même personne d'abord) ; 2 · un Promi du journal sans
   cellule sur la Toile y est relié (Toile.sync, l'API publique — on ne touche pas au code de la Toile) ;
   3 · les guillemets deviennent insécables : « et le mot qui le suit ne se séparent jamais. */
(function(){
  var NB='\u00a0';
  function insecable(t){ return (''+(t||'')).replace(/«\s*/g,'«'+NB).replace(/\s*»/g,NB+'»'); }
  function titreDe(t){ var m=(''+(t||'')).match(/«\s*([^»]*?)\s*»/); return m?m[1].replace(/\u00a0/g,' ').trim():null; }
  function repare(){
    try{
      if(typeof FEED==='undefined'||typeof promises==='undefined') return;
      var manque=false;
      FEED.forEach(function(f){
        if(f.text) f.text=insecable(f.text);
        var ti=titreDe(f.text); if(!ti) return;
        var p=f.pid!=null?promises.filter(function(q){return q.id===f.pid;})[0]:null;
        if(!p || (p.title||'').trim()!==ti){
          var c=promises.filter(function(q){return (q.title||'').trim()===ti;});
          var bon=c.filter(function(q){return f.from && (q.from===f.from||q.who===f.from);})[0]||c[0];
          if(bon){ f.pid=bon.id; p=bon; }
        }
        if(p && !p.draft && window.Toile && Toile.dalleAbs && !Toile.dalleAbs(p.id)) manque=true;
      });
      if(manque && window.Toile && Toile.sync) Toile.sync(promises.filter(function(q){return !q.draft;}).map(function(q){return q.id;}));
    }catch(_){}
  }
  window._filRepare=repare;
  var _fa=window.feedAdd;
  if(typeof _fa==='function') window.feedAdd=function(type,text,opts){ return _fa.call(this,type,insecable(text),opts); };
  var _bf=window.buildFeed;
  if(typeof _bf==='function') window.buildFeed=function(){ repare(); return _bf.apply(this,arguments); };
})();
