# LA BASCULE DU RAYON — un seul propriétaire, la hauteur mesurée (Tom, 11 sept.). Patch sur app.html, motif unique.
import hashlib, io, os
RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = os.path.join(RACINE, 'app.html')
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '53aae6471a35bab225ea0b974b98c644', 'app.html a changé depuis le lot du mur : ' + avant

def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:90]
    S = S.replace(old, new)

# 1 · le CSS du lot : la règle « trois lignes et plus → 30 » (une CLASSE) cède à la règle de HAUTEUR, portée par le script
remplace("""/* ⚑ P (chantier 65, décision Tom) : un champ de TROIS LIGNES ET PLUS — libellé, texte, ligne de visibilité — prend le
   rayon 30 du grand panneau de la grammaire. Rayon = hauteur ÷ 2 collait le début de la 1re et de la dernière ligne à la
   courbe (3,0 / 2,5 px, contre 12,9 / 13,7 pour le champ à deux lignes) ; à 30, l'écart reste 14 quel que soit le
   nombre de lignes, sans toucher à l'interligne. Mesuré : planche 3, § 5. Les champs d'une et deux lignes gardent h ÷ 2. */
#device #detailPoster .s2-reg.s2-zone,.frame #detailPoster .s2-reg.s2-zone,
#device #createSheet.pp-peauf .s2-reg.s2-zone,.frame #createSheet.pp-peauf .s2-reg.s2-zone,
#device #detailPoster .s2-reg.s2-zone.s2-z104,.frame #detailPoster .s2-reg.s2-zone.s2-z104,
#device #createSheet.pp-peauf .s2-reg.s2-zone.s2-z104,
.frame #createSheet.pp-peauf .s2-reg.s2-zone.s2-z104{border-radius:30px!important}
""", """/* ⚑ LE RAYON D'UN CHAMP N'EST PLUS ÉCRIT ICI. La règle « trois lignes et plus → 30 » (P, Q202) visait une CLASSE ; Tom
   l'a reprise en HAUTEUR (11 sept.) : « rayon = moitié de la hauteur jusqu'à [la hauteur où la pilule commence à manger
   le texte], 30 au-delà ». Son seul propriétaire est `rayon()` dans le script de ce lot (SEUIL_PILULE, mesuré). Deux
   écrivains pour une propriété se défont l'un l'autre (CLAUDE §7) : celui-ci s'est retiré. */
""")

# 2 · le script du lot : la règle, son seuil mesuré, et ses deux porteurs (les zones, les autres rangées de Peaufiner)
remplace("""  var GLYPHE = 22, LH = 22.5;
  function nbLignes(t){""", """  var GLYPHE = 22, LH = 22.5;
  /* ⚑ LA BASCULE DU RAYON — Tom, 11 sept. : « rayon = moitié de la hauteur jusqu'à deux lignes, 30 au-delà. Un champ à une
     ligne garde sa pilule, un champ qui s'ouvre gagne l'air qu'il lui faut. La loi du §2 tient là où elle a du sens, et
     cède seulement là où elle produit un défaut. Mesure le seuil exact — à quelle hauteur la pilule commence à manger le
     texte — et pose la bascule là, pas à un nombre de lignes arbitraire. »
     MESURÉ SUR L'ENCRE (sauvegardes/audit-cercle/seuil_encre.py, _analyse, _bascule) : chaque champ capturé, sa distance
     encre → courbe intérieure recalculée pour tout rayon. « Manger » = serrer l'encre plus que ne le fait un champ OUVERT
     au rayon 30 (P, validé) : son air le plus serré vaut C = 15,19 (NOTE de la page +, la ligne de visibilité). Un champ à
     deux rangées qui s'ouvre (rangée du haut à sa place, rangée du bas clouée au bas) tient C en pilule jusqu'à 94,53 pour
     le plus serré (PIÈCES JOINTES de la page +), 96,21 (Nuée), 105,95 (fiche). ⇒ la bascule est à 94,5 : tout champ de
     92 garde sa pilule, tout champ de 104 et plus prend 30. Les réglages d'une ligne (64) ne sont jamais mangés : leur
     ligne passe par l'axe. ⚠ UN SEUL PROPRIÉTAIRE : cette fonction. La Nuée (lot-NUEE-PEAUFINER, `pose`) l'appelle ;
     les rangées de Peaufiner la reçoivent ci-dessous. */
  var SEUIL_PILULE = 94.5;
  function rayon(h){ return h <= SEUIL_PILULE ? h / 2 : 30; }
  window._rayonChamp = rayon; window._seuilPilule = SEUIL_PILULE;
  function nbLignes(t){""")

remplace("""    P(z, 'height', (H0 + (n - 1) * lh) + 'px');
    if(z.getAttribute('data-cercle-lignes') !== String(n)) z.setAttribute('data-cercle-lignes', String(n));
  }
  function caleTout(){
    document.querySelectorAll('#detailPoster .s2-zone, #createSheet.pp-peauf .s2-zone').forEach(caleZone);
  }""", """    P(z, 'height', (H0 + (n - 1) * lh) + 'px');
    P(z, 'border-radius', rayon(H0 + (n - 1) * lh) + 'px');      /* la hauteur CALCULÉE, jamais relue (§8) */
    if(z.getAttribute('data-cercle-lignes') !== String(n)) z.setAttribute('data-cercle-lignes', String(n));
  }
  /* les autres rangées de Peaufiner (une ligne, deux rangées) : leur hauteur vient du CSS et ne dépend pas du rayon —
     la lire ne crée aucune boucle. Échelle du champ lui-même (largeur rendue ÷ largeur de mise en page). */
  function arrondit(r){
    if(!r || !r.isConnected || r.classList.contains('s2-zone')) return;
    var q = r.getBoundingClientRect(); if(!q.height) return;
    var h = Math.round(q.height / ((q.width / (r.offsetWidth || q.width)) || 1) * 100) / 100;
    P(r, 'border-radius', rayon(h) + 'px');
  }
  function caleTout(){
    document.querySelectorAll('#detailPoster .s2-zone, #createSheet.pp-peauf .s2-zone').forEach(caleZone);
    document.querySelectorAll('#detailPoster .s2-liste .s2-reg, #createSheet.pp-peauf .s2-liste .s2-reg').forEach(arrondit);
  }""")

# 3 · l'observateur : la zone est recalée DANS LA FOULÉE de la mutation (micro-tâche), plus à l'image suivante.
#     Mesuré (sonde_pp_note2.py) : la page + REBÂTIT sa zone de note sans cesse (six zones en 2,5 s, au défilement aussi) ;
#     entre un rebâtissage et l'image suivante, la zone neuve était à 118 avec trois lignes de texte (dernière ligne à 0,5).
remplace("""    if(h) new MutationObserver(passe).observe(h, {childList:true, subtree:true});""",
         """    /* ⚠ la zone de la page + est rebâtie sans cesse (mesuré : six zones en 2,5 s) : on la recale DANS LA FOULÉE de la
       mutation, avant toute image — à l'image suivante, la zone neuve restait un instant à 118 avec trois lignes. */
    if(h) new MutationObserver(function(){ try{ caleTout(); }catch(_){ } passe(); }).observe(h, {childList:true, subtree:true});""")

# 4 · la Nuée : sa carte demande son rayon à la règle (elle portait « b.ph ? 30 : b.h/2 », une classe de plus)
remplace("""                'border-radius':(b.ph ? 30 : b.h/2)+'px',""",
         """                'border-radius':(window._rayonChamp ? window._rayonChamp(b.h) : b.h/2)+'px',   /* la règle de hauteur (lot-CERCLE-MUR) */""")

io.open(F, 'w', encoding='utf-8').write(S)
print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())
