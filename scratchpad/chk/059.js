
/* ═══════════════════════════════════════════════════════════════════════════════════════
   LE JEU DE DÉMONSTRATION DE LA PLANCHE (décision Tom, 20 août 2026).
   « Mêmes promesses, mêmes titres, mêmes personnes, mêmes mondes, mêmes états que
     promi-moodboard-H.html et promi-nuee-toile.html. C'est un jeu de démonstration, pas une
     fonction — tu peuples, tu n'inventes rien. »

   POURQUOI. Sans lui, « identique au pixel » ne veut rien dire : la planche montre SES
   Promi (« le grand plongeoir », « faire les crêpes », quatre entrées au Fil) et l'app LES
   SIENS (« garder les clés », « relire mon CV », douze entrées). Le comparateur mesurait
   deux jeux de données, pas deux dessins.

   D'OÙ VIENNENT CES MOTS. De la planche, lus au texte, pas de mémoire — l'extraction est
   dans `scratchpad/extrait_jeu.py`, son relevé dans `scratchpad/jeu_planche.json`. Chaque
   titre ci-dessous figure dans un cadre, avec sa personne et son état :
       cadres 34 à 71  · les fiches      (planter un arbre · faire les crêpes · nager le
                                          mardi · aller voir la mer · courir dimanche ·
                                          le grand plongeoir · appeler Mamie)
       cadre 58        · le fil du potager (arroser tous les soirs · semer les radis)
       cadre 60        · l'atelier du samedi, « Avec toi seulement », aucun Promi
       promi-nuee-toile · les autres Promi du potager
   AUCUN TITRE N'EST INVENTÉ. Là où la planche ne dit rien, on ne remplit pas.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  function jeu(){
    if(typeof P !== 'function') return false;
    /* ⚑ CHANTIER 78 (Tom, 14 sept. 2026) : « le jeu de démonstration ne se charge que s'il n'y a pas de sauvegarde — on ne
       perd pas ce qu'on a fait ». Une sauvegarde qui porte des Promi : on la garde, on ne pose que le décor de la planche. */
    var _sauve=!!window._etatRelu;   /* la sauvegarde relue AU CHARGEMENT (loadState) — pas celle que l'app vient d'écrire */
    if(_sauve){ try{ window.NUEHT=window.NUEHT||{}; if(NUE.potager) NUEHT.potager=347.3; if(NUE.atelier) NUEHT.atelier=261.8;
        window.NUEORD=window.NUEORD||{}; var _cr=promises.filter(function(p){return p.title==='faire les crêpes';})[0]; if(_cr&&NUE.potager) NUEORD.potager=_cr.id+0.5;
        var _gp=promises.filter(function(p){return p.title==='le grand plongeoir';})[0]; if(_gp&&NUE.atelier) NUEORD.atelier=_gp.id+0.5; }catch(_){}
      window._jeuPlanche={promi:promises.length, nuees:Object.keys(NUE).length, sauvegarde:true}; return true; }
    try{
      /* ── LES NUÉES (cadres 58 et 60) ── */
      for(var k in NUE) delete NUE[k];
      NUE.potager = 'le potager';
      NUE.atelier = "l'atelier du samedi";
      if(typeof NUEEMEM !== 'undefined'){
        for(var k2 in NUEEMEM) delete NUEEMEM[k2];
        /* ⚠ QUATRE AUTRES, ET « MOI » EN PLUS — les deux cadres se recoupent :
           cadre 58 (la fiche)  « Avec Rachel, Adrien, +3 »  → 2 nommés + Léa, Nico, moi
           cadre 72 (l'Index)   « avec +4 »                  → les 4 autres que moi
           Avec cinq autres, l'Index écrivait « avec +5 ». */
        NUEEMEM.potager = ['Rachel','Adrien','Léa','Nico'];
        NUEEMEM.atelier = [];                                          /* « Avec toi seulement » */
      }

      /* ── LES PROMESSES ──
           P(titre, à qui, échéance, intensité, état, nuée, de qui)
           état : 'tenu' = TENUE · 'rate' = À TENIR · 'encours' = EN COURS            */
      var L = [];
      function pousse(p, extra){ if(extra) for(var a in extra) p[a]=extra[a]; L.push(p); return p; }

      /* les fiches du moodboard, dans l'ordre où l'Index les montre (cadre 72) */
      pousse(P('planter un arbre','moi',12,2,'tenu',null));                    /* TENUE · 12 mars */
      pousse(P('faire les crêpes','Rachel',2,2,'rate',null));                  /* À TENIR · 2 J   */
      /* ⚠ « courir dimanche » EST UN CHICHE LANCÉ, PAS ENCORE RELEVÉ — et c'est ce que
         disent les cadres : 52 « Marion complètera si elle relève », 72 « LANCÉ ».
         Avec `status:'rate'`, `motEtat` écrivait « À TENIR » : l'état d'un Promi, pas
         d'un Chiche (l. 18044, `p.status==='rate'` passe devant `p.chiche`).
         Le « RELEVÉ · À TENIR À DEUX » du cadre 76 est l'ÉVÉNEMENT du Fil, plus tard —
         il est porté par `ev` sur l'entrée du journal, pas par la promesse. */
      pousse(P('courir dimanche','Marion',7,2,'encours',null),
             {chiche:true, chicheEtat:'lance', avec:'Rachel'});
      pousse(P('nager le mardi','moi',4,2,'encours',null));                    /* EN COURS · depuis le 4 avril */
      /* cadre 56 : « À Marion » — et « TENU À DEUX », parce que Marion elle-même l'a
         relevé. Le compagnon est donc la destinataire, pas un tiers : on ne l'écrit pas
         deux fois (voir la ligne « À Marion · avec Rachel » du cadre 42, qui, elle, EST
         un tiers). */
      pousse(P('le grand plongeoir','Marion',3,2,'tenu',null),
             {chiche:true, chicheEtat:'releve', avec:'Marion'});
      /* ⚠ « aller voir la mer » N'EST PAS PLANTÉE. Comme « m'appeler » (cadre 8) et
         « venir dimanche » (cadre 10), c'est un exemple de PHRASE sur la page + (cadres 2,
         4, 18, 24 à 33) — jamais un Promi de l'Index. Le cadre 74 tranche : l'Index de la
         planche porte HUIT entrées, et elle n'y est pas. Avec elle, le compte passait à 13
         là où l'entête écrit **12** = 5 Promi hors Nuée + 6 au potager + 1 gardé de côté. */
      /* ⚠ « m'appeler » (cadre 8) et « venir dimanche » (cadre 10) ne sont PAS dans ce jeu :
         ce sont des exemples de PHRASE sur la page +, pas des Promi plantés. Les compter
         donnerait « Index 14 » là où le cadre 72 écrit **Index 12** — et 12 est exactement
         6 Promi hors Nuée + 6 dans le potager. Le compte de la planche tranche. */

      /* ── LE POTAGER — SIX PROMI, ALIGNÉS SUR `promi-nuee-toile.html` ──
         (Décision Tom, 29 août : cette planche porte la loi, elle fait foi pour la Nuée.)
         Ses cadres 8 et 10 nomment QUATRE Promi et les montrent dans cet ordre ; ce sont
         eux que la fiche de Nuée affiche. Le moodboard H en nomme deux autres, et **le Fil
         et l'Index en dépendent** — cadre 76 « Adrien a planté : semer les radis »,
         cadre 72 « le potager · 6 PROMI ». On garde donc les six, les quatre d'abord.
         Aucun titre n'est inventé : chacun figure dans un cadre.
         ⚠ Le compte de tenus devient 3 (monter la serre · récupérer les plants · arroser
         tous les soirs) là où les cadres 58 et 72 écrivent « 1 TENU » : c'est l'arithmétique
         du jeu réuni, et c'est le désaccord que la décision tranche. Voir QUESTIONS. */
      pousse(P('monter la serre avant les gelées','le groupe',5,2,'tenu','potager','moi'));
      pousse(P("reprendre l'arrosage automatique",'le groupe',5,2,'rate','potager','Rachel'));
      pousse(P('récupérer les plants de tomates','le groupe',7,2,'tenu','potager','Adrien'));
      /* ⚠ UN CHICHE RELEVÉ N'EST PAS UNE PAROLE TENUE. Le cadre 8 écrit « 4 PROMI ·
         2 TENUS » en comptant *monter la serre* et *récupérer les plants*, et laisse
         *vider le composteur* de côté : relever un chiche, c'est l'accepter, pas l'avoir
         tenu. Avec `status:'tenu'` le compte sortait à « 4 tenus » au lieu de 3. */
      pousse(P('vider le composteur à deux','le groupe',6,2,'encours','potager','Marion'),
             {chiche:true, chicheEtat:'releve', avec:'Adrien'});
      pousse(P('arroser tous les soirs','le groupe',3,2,'tenu','potager','moi'));
      pousse(P('semer les radis','le groupe',2,2,'rate','potager','Adrien'));
      /* ⚑ TROIS PROMI DE DÉMONSTRATION EN PLUS — mots donnés par Tom, 29 août 2026.
         « Ce n'est pas inventer une fonction, c'est peupler la démo — comme le jeu de la
         planche. » À moi, en cours.
         ⚠ ARITHMÉTIQUE, ET JE LA DIS : le potager en portait SIX (les quatre que
         `promi-nuee-toile` nomme, plus « arroser tous les soirs » et « semer les radis »,
         dont le Fil et l'Index du moodboard H dépendent). Avec ces trois-là il en porte
         NEUF, pas sept — l'encart et l'entête de l'Index suivent le contenu réel, ils ne
         récitent pas un nombre. Les cadres 58 et 72 écrivent 7 et 12 : c'est le désaccord
         connu entre les deux planches et le jeu réuni (QUESTIONS.md · Q95). */
      pousse(P('arroser les tomates','moi',6,2,'encours','potager','moi'));
      pousse(P('tailler la vigne','moi',8,2,'encours','potager','moi'));
      pousse(P('ramasser les courges','moi',11,2,'encours','potager','moi'));

      /* ⚑ LE SECOND PROMI DE RACHEL — mot donné par Tom, 29 août 2026. Son anneau ne
         portait qu'un seul arc (« faire les crêpes », à tenir) : orange plein, là où les
         cadres 44 et 96 le montrent menthe + lilas. Avec une parole tenue de plus, il
         porte un tenu ET un à tenir, comme le cadre le suppose. */
      pousse(P('rapporter le livre','Rachel',14,2,'tenu',null));

      /* ⚑ TROIS PROMESSES REÇUES — titres de Tom, 14 sept. 2026 (Q215) : ce qu'un proche te promet, à toi seul.
         « Rachel te promet de t'apprendre à nager » · « Nico te promet de rapporter la perceuse » · « Marion te promet de venir dimanche ». */
      pousse(P("t'apprendre à nager",'moi',7,2,'encours',null,'Rachel'));
      pousse(P('rapporter la perceuse','moi',5,2,'tenu',null,'Nico'));
      pousse(P('venir dimanche','moi',3,2,'rate',null,'Marion'));

      /* gardé de côté (cadre 62) */
      pousse(P('appeler Mamie','moi',9,2,'encours',null), {draft:true});

      promises.length = 0;
      L.forEach(function(p){ promises.push(p); });

      /* ⚑ LA PLACE D'UNE NUÉE DANS L'ORDRE DE PLANTATION. L'app ne date pas le lancement
         d'une Nuée ; l'Index au repos en a besoin depuis la décision du 20 août. On pose
         donc le rang que les cadres 72 et 74 montrent — le potager entre « faire les
         crêpes » et « courir dimanche ». À défaut, `buildIndex` range une Nuée à sa
         PREMIÈRE plantation : c'est le comportement de toutes les autres. */
      /* ⚑ LA HAUTEUR DE TRAIT FIGÉE À LA PLANTATION (§2.5), relevée dans les DEUX cadres
         de l'Index — 2 par ligne (cadre 72) et 3 par ligne (cadre 74). Les deux échelles
         redonnent la même valeur à 1,5 px près, ce qui vérifie la loi du §3.9 bis :
             boîte = base_figée × h/600 + 13 × l/173 + 20
             cadre 72 (h 198)   135 · 107 · 147 ·  99 · 123 · 131
             cadre 74 (h 133)    97 ·  78 · 105 ·  73 ·  89 ·  94 ·  86 ·  81
             hauteur figée      311 · 226 · 347 · 202 · 275 · 298 · 262 · 239
         Elle appartient au PROMI, pas à son état : c'est ce que dit « figée à la
         plantation ». Rien n'est inventé — chaque nombre sort d'un chemin SVG du cadre. */
      /* ⚑ LE JOUR DE LA LIGNE D'ÉTAT, lu dans les cadres de fiche. L'app ne garde aucune
         date : elle n'a que des échéances en jours. Ces mots-là sont ceux des cadres —
         34/48 « TENUE · 12 MARS », 46 « EN COURS · DEPUIS LE 4 AVRIL », 42/56 « TENU À
         DEUX · 3 AOÛT », 52 « LANCÉ · PAS ENCORE RELEVÉ », 62 « GARDÉ DE CÔTÉ · 2 AVRIL ».
         « faire les crêpes » n'en a pas : son temps sort de `motDuTemps` (cadre 36
         « À TENIR · DIMANCHE »), et c'est le produit qui le dit. */
      /* ⚠ « FAIRE LES CRÊPES » A SON MOT, LUI AUSSI — cadre 44 : « À TENIR · DANS 2 JOURS ».
         Il n'en avait pas, et son temps sortait de `motDuTemps`, qui calcule un jour de
         semaine sur `Date.now()` : l'app écrivait « LUNDI » aujourd'hui et écrira
         « MERCREDI » la semaine prochaine. Un écran qui change avec l'horloge n'est pas
         comparable à un cadre — c'est la même famille de défaut que la couleur de dalle
         tirée au hasard. Le mot vient du cadre, il ne se calcule plus.
         ⚠ DEUX CADRES SE CONTREDISENT : le 36 écrit « À TENIR · DIMANCHE », le 44 « DANS
         2 JOURS ». On suit le 44, qui est LE cadre de la fiche à tenir — et il s'accorde
         avec sa carte d'Index, « À TENIR · 2 J ». Noté dans QUESTIONS.md. */
      var JOUR = {'planter un arbre':'12 mars', 'nager le mardi':'depuis le 4 avril',
                  'le grand plongeoir':'3 août', 'courir dimanche':'pas encore relevé',
                  'appeler Mamie':'2 avril', 'faire les crêpes':'dans 2 jours'};
      promises.forEach(function(p){ if(JOUR[p.title]) p.leJour=JOUR[p.title]; });

      var HT = {'planter un arbre':310.9, 'faire les crêpes':226.1, 'courir dimanche':201.8,
                'nager le mardi':274.5, 'le grand plongeoir':298.8, 'appeler Mamie':239.3};
      promises.forEach(function(p){ if(HT[p.title]!=null) p.ht=HT[p.title]; });
      window.NUEHT = window.NUEHT || {};
      NUEHT.potager = 347.3; NUEHT.atelier = 261.8;

      window.NUEORD = window.NUEORD || {};
      try{ var _cr=promises.filter(function(p){return p.title==='faire les crêpes';})[0];
           if(_cr) NUEORD.potager = _cr.id + 0.5;
           var _gp=promises.filter(function(p){return p.title==='le grand plongeoir';})[0];
           if(_gp) NUEORD.atelier = _gp.id + 0.5;   /* cadre 74 : l'atelier avant Mamie */
      }catch(_){}

      /* ── LE FIL (cadre 76) ──
           Le Fil ne se déduit pas des promesses : il a son propre journal, `FEED`. La carte
           en tire son eyebrow en RETIRANT le titre entre guillemets du texte de l'événement
           (l. ~18162) — on écrit donc les tournures de la planche, titre entre guillemets,
           et l'eyebrow tombe juste tout seul. Cinq entrées, dans l'ordre du cadre. */
      try{
        if(typeof FEED !== 'undefined'){
          FEED.length = 0;
          var pid = function(t){ var q=promises.filter(function(p){return p.title===t;})[0]; return q?q.id:null; };
          /* feedAdd empile en tête : on pose donc du DERNIER au PREMIER du cadre */
          /* ⚑ `ev` = L'ÉTAT DE L'ÉVÉNEMENT, lu dans le cadre 76 — nature, couleur, mot.
             Le bandeau dit ce qui s'est passé, pas où en est le Promi aujourd'hui : la
             planche montre « le grand plongeoir » TENU À DEUX sur sa fiche (cadre 56) et
             À RELEVER dans le Fil (cadre 76). Voir `etatEvenement`. */
          /* ⚠ `feedAdd` ne recopie que les champs qu'elle connaît (l. 6582) : on ne la
             réécrit pas — on pose `ev` sur l'entrée qu'elle vient d'empiler. */
          var evPose = function(spec){ if(FEED[0]) FEED[0].ev = spec; };
          feedAdd('kept',        'Marion a relevé : « courir dimanche »',        {pid:pid('courir dimanche'), from:'Marion', t:'hier'});
          evPose({nat:'chiche', etat:'tenue', mode:'complet', mot:'RELEVÉ · À TENIR À DEUX'});
          feedAdd('received',    'à Rachel : « faire les crêpes »',              {pid:pid('faire les crêpes'), t:'2 j'});
          feedAdd('added',       'Adrien a planté : « semer les radis »',        {pid:pid('semer les radis'), from:'Adrien', t:''});
          evPose({nat:'nuee', mode:'complet'});
          feedAdd('kept',        'à moi : « planter un arbre »',                 {pid:pid('planter un arbre'), t:'il y a 2 h'});
          /* ⚠ LE TYPE PORTE LA FONCTION. « TENIR » et « REPORTER » ne s'affichent que sous
             un événement REÇU (`received`) : avec `chiche_recu` seul, `redteam_fonctions`
             perdait « TENIR depuis le Fil » et « un bandeau ouvre sa fiche ». Le mot de la
             planche est gardé — l'eyebrow se déduit du texte, pas du type. */
          feedAdd('received', 'Marion te lance un chiche : « le grand plongeoir »',
                                 {pid:pid('le grand plongeoir'), from:'Marion', unread:true, t:''});
          evPose({nat:'chiche', etat:'lance', mode:'moitie', mot:'À RELEVER'});
          /* ⚑ v89 (Q347) — les deux états neufs, posés SOUS les cinq bandeaux du cadre 76 (sa composition ne bouge pas) */
          try{ var _pm=promises.filter(function(p){ return p.from && p.from!=='moi' && !p.draft && !p.req && p.status!=='tenu' && p.status!=='kept' && p.status!=='rate' && p.title!=='le grand plongeoir' && (p.title||'').length<=20; })[0];   /* titre d'une ligne, comme les cinq du cadre */
            if(_pm){ FEED.push({id:_fid++, type:'moitie', text:(_pm.from||'Marion')+' a tracé sa moitié : « '+_pm.title+' »', pid:_pm.id, from:_pm.from, t:'il y a 1 h', unread:true,
              ev:{nat:(_pm.chiche?'chiche':'promi'), etat:'lance', mode:'moitie', mot:'À RELEVER'}}); }
            FEED.push({id:_fid++, type:'invitation', text:'Rachel t’invite à rejoindre « le jardin partagé »', nuee:'jardin-partage', nom:'le jardin partagé', from:'Rachel', t:'il y a 3 h', unread:true,
              ev:{nat:'nuee', mode:'complet'}}); }catch(_){}
          try{ if(typeof buildFeed==='function') buildFeed(); }catch(_){}
          try{ if(typeof updateFeedDot==='function') updateFeedDot(); }catch(_){}
        }
      }catch(_){}

      /* ── la Toile doit connaître les nouvelles dalles, comme après une plantation ── */
      try{ if(window.Toile && Toile.sync)
        Toile.sync(promises.filter(function(p){ return !p.draft; }).map(function(p){ return p.id; })); }catch(_){}
      try{ if(typeof computeBox==='function') computeBox(); }catch(_){}
      try{ if(typeof relayout==='function') relayout(); }catch(_){}
      try{ if(typeof render==='function') render(); }catch(_){}
      try{ if(window.syncAll) syncAll(); }catch(_){}
      try{ if(typeof caption==='function') caption(); }catch(_){}
      window._jeuPlanche = {promi:promises.length, nuees:Object.keys(NUE).length};
      return true;
    }catch(e){ window._jeuPlancheErr = ''+e; return false; }
  }
  window._jeuPlancheRejoue = jeu;
  /* au chargement, une fois — avant que l'œil ou un juge ne regarde */
  /* ⚑ chantier 71 : le minuteur (400 ms) passait souvent AVANT DOMContentLoaded, qui rejouait le jeu sans garde — ids décalés de 16 */
  if(document.readyState !== 'loading') jeu();
  else document.addEventListener('DOMContentLoaded', function(){ if(!window._jeuPlanche) jeu(); });
  setTimeout(function(){ if(!window._jeuPlanche) jeu(); }, 400);
})();
