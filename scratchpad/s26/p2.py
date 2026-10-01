import io
S=io.open('app.html',encoding='utf-8').read()

# 4a — etatTrait entre dans le bloc S4 (il vivait dans l'IIFE de l'onde)
oldA="  var NATCOL=O.NATCOL, NATCLAIR=O.NATCLAIR, NATTRAIT=O.NATTRAIT||O.NATCLAIR, TERRA=O.TERRA, MENTHE=O.MENTHE;"
assert S.count(oldA)==1, "A %d"%S.count(oldA)
newA=("  var NATCOL=O.NATCOL, NATCLAIR=O.NATCLAIR, NATTRAIT=O.NATTRAIT||O.NATCLAIR, TERRA=O.TERRA, MENTHE=O.MENTHE;\n"
 "  /* ⚠ 23 SEPTEMBRE 2026 — UNE CARTE DU FIL MANQUAIT, ET LA CONSOLE NE DISAIT RIEN.\n"
 "     `etatEvenement` appelle `etatTrait('tenu', l)` quand l'événement est une parole tenue.\n"
 "     `etatTrait` vit dans l'IIFE de l'onde ; ici elle n'existe pas — `ReferenceError`, et\n"
 "     `_s4Fil` perd la carte en silence. Mesuré : `_filComp` déclare **5** entrées, le Fil\n"
 "     n'en peignait que **4** ; la manquante est p127 (« Marion a relevé · courir dimanche »),\n"
 "     la SEULE dont l'événement porte `etat:'tenue'`. C'est le piège du §8 — une aide partagée\n"
 "     entre deux blocs se prend sur `window._onde`, jamais par portée. */\n"
 "  var etatTrait=O.etatTrait||function(k,l){ return NATTRAIT.promi; };")
S=S.replace(oldA,newA)

# 4b — le titre du bandeau du Fil remonte, puis retrecit
oldB = """      gr.appendChild(d);
      /* ⛑ LE NOMBRE DE L'ENTÊTE DU FIL COMPTE LES GESTES QUI VIENNENT D'AILLEURS."""
assert S.count(oldB)==1, "B %d"%S.count(oldB)
newB = """      gr.appendChild(d);
      /* ⛑ 23 SEPTEMBRE 2026 (Tom) — « LE TEXTE TROP LONG EST TRONQUÉ EN BAS. IL DOIT
         REMONTER — IL Y A LA PLACE AU-DESSUS. LES ÉLÉMENTS S'AJUSTENT TOUJOURS AVEC DES
         ESPACES LOGIQUES. » La carte d'Index a reçu ce traitement le 23 ; LE BANDEAU DU FIL
         NON. Sa boîte de titre fait 42 px et `#device .s4-ti{font-size:24px!important}` la
         peint à 24 : **une ligne tient (24 × 1,04 = 25), deux débordent (49,9 > 42)** et
         `overflow:hidden` les coupe.
         LES ESPACES SONT CEUX DE LA CARTE, ET ILS NE BOUGENT PAS : événement 28 de haut,
         **6** jusqu'au titre, titre jusqu'à **92**, **6** jusqu'à l'état (98). Ce qui bouge,
         c'est le HAUT : le titre grandit VERS LE HAUT depuis 92, et l'événement monte avec
         lui — jusqu'à 8 px du bord, le plancher de la carte. La boîte passe donc de 42 à
         **50** au plus, et deux lignes à 24 px y tiennent pile.
         ET SEULEMENT ENSUITE ON RÉTRÉCIT (1 px à la fois, plancher 11 px du §6, `important`
         — sans lui la règle à 24 gagne et la boucle tourne pour rien, §8).
         ⚠ UNE CARTE DONT LE TITRE TIENT SUR UNE LIGNE NE BOUGE PAS D'UN PIXEL : `h` part de
         42, `top` retombe à 50, l'événement à 16 — les cotes d'origine, par construction. */
      (function(carte){
        var t=carte.querySelector('.s4-ti'), ve=carte.querySelector('.s4-ev');
        if(!t) return;
        var BAS=92, GAP=6, HEV=28, HAUT_MIN=8, H0=42;
        var fs=parseFloat(getComputedStyle(t).fontSize)||24;
        t.style.setProperty('height','auto','important');
        var voulu=Math.ceil(t.scrollHeight)||0;
        var h=Math.max(H0, Math.min(voulu, BAS-HAUT_MIN-GAP-HEV));
        t.style.setProperty('height',h+'px','important');
        t.style.setProperty('top',(BAS-h)+'px','important');
        if(ve) ve.style.setProperty('top',Math.max(HAUT_MIN,(BAS-h)-GAP-HEV)+'px','important');
        for(var k=0; k<12 && t.scrollHeight > t.clientHeight+1 && fs>11; k++){
          fs-=1; t.style.setProperty('font-size', fs+'px', 'important'); }
        try{ carte.setAttribute('data-titre-cote',[voulu,h,BAS-h,Math.round(fs)].join(',')); }catch(_){}
      })(d);
      /* ⛑ LE NOMBRE DE L'ENTÊTE DU FIL COMPTE LES GESTES QUI VIENNENT D'AILLEURS."""
S=S.replace(oldB,newB)
io.open('app.html','w',encoding='utf-8').write(S)
print("ok")
