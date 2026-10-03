# Inventaire de joignabilité — engendré par `redteam_joignable.py`

Source : `app.html`. 283 éléments interactifs relevés sur 36 écrans (mode clair, 390 × 844), 2 injoignables distincts ; 394 gestionnaires lus, 4 fonctions absentes.

## A · Injoignables au rendu

| Élément | Écrans | Cause | Dette |
|---|---|---|---|
| `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-cercle>div.s2-reg.s2-couleur«LA COULEUR#FFB8D2»` | Peaufiner, Peaufiner Chiche | mur flouté (pointer-events:none) | mur de Ma Parole ! : réglage flouté du gratuit, sans prise par décision (v104) |
| `div#npCercle.s2-cercle>div.s2-reg.s2-couleur«LA COULEUR#FFB8D2»` | Peaufiner Nuée | mur flouté (pointer-events:none) | mur de Ma Parole ! : réglage flouté du gratuit, sans prise par décision (v104) |

## B · Fonctions absentes appelées par un gestionnaire, et gestionnaires posés sur un nœud disparu

| Gestionnaire | Cause | Dette |
|---|---|---|
| `#fToAll · onchange` | le nœud `#fToAll` n'existe plus : aucun `id` de ce nom, ni à la source ni au rendu | nœud disparu : code mort hors de Q363 — à retirer sur décision |
| `c · onclick → promiDeconnexion()` | la fonction `promiDeconnexion` n'existe nulle part | point de branchement de Firebase : voulu |
| `document · onclick → ouvrirPersonne() [après un return]` | la fonction `ouvrirPersonne` n'existe nulle part | garde morte : openPerson, juste après, fait le travail |
| `document · onclick → renderPerson() [après un return]` | la fonction `renderPerson` n'existe nulle part | garde morte : openPerson, juste avant, fait le travail |

## C · Tous les éléments relevés

| Écran | Élément | Par | x, y | l × h | Joignable | Cause |
|---|---|---|---|---|---|---|
| Aura | `div#auraScreen.screen.s-karma>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| Aura | `#auraInfoBtn` | natif | 218, 78 | 20 × 20 | oui |  |
| Aura | `div#auCadre.au-cadre.au-voile>div.au-bo>div.au-prise«»` | écouteur | 195, 254 | 296 × 296 | oui |  |
| Aura | `#auPartage` | natif | 195, 487 | 342 × 60 | oui |  |
| Aura | `div#auCadre.au-cadre.au-voile>div.au-nx«ToiAdrienMarionNicoRache»` | écouteur | 207, 689 | 366 × 107 | oui |  |
| Conditions | `div#legalScreen.screen.s-set>div.enh>div.closeb«✕ Fermer»` | écouteur | 296, 70 | 84 × 18 | oui |  |
| Fil | `#fdClose` | on… | 296, 70 | 84 × 18 | oui |  |
| Fil | `#fdSearch` | natif | 174, 142 | 208 × 24 | oui |  |
| Fil | `#fdTriBtn` | natif | 340, 142 | 52 × 52 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«ChicheMarion te lance un»` | on… | 195, 268 | 358 × 128 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«Promià moiplanter un arb»` | on… | 195, 408 | 358 × 128 | oui |  |
| Fil | `#feedView` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«CercleAdrien a plantésem»` | on… | 195, 548 | 358 × 128 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«PromiRachel a tracé sa m»` | on… | 195, 596 | 358 × 128 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«Promià Rachelfaire les c»` | on… | 195, 688 | 358 × 128 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«CercleRachel t’invite à »` | on… | 195, 736 | 358 × 128 | oui |  |
| Fil | `div#feedList>div.s4-grille>div.s4-carte«ChicheMarion a relevécou»` | on… | 195, 828 | 358 × 128 | oui |  |
| Index 2 | `div#indexSheet.sheet.trame>div.enh>div.closeb«✕ Fermer»` | on… | 296, 84 | 84 × 18 | oui |  |
| Index 2 | `#ixSearch` | natif | 174, 170 | 208 × 24 | oui |  |
| Index 2 | `#ixTriBtn` | natif | 340, 170 | 52 × 52 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promià moiplanter un arb»` | on… | 107, 331 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promià Rachelfaire les c»` | on… | 284, 331 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Cercleavec +4le potager9»` | on… | 107, 541 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Chicheà Marioncourir dim»` | on… | 284, 541 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promià Rachelrapporter l»` | on… | 107, 556 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promide Nicorapporter la»` | on… | 107, 556 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promide Rachelt'apprendr»` | on… | 284, 556 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promide Marionvenir dima»` | on… | 284, 556 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Cerclepersol'atelier du »` | on… | 107, 729 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promigardé de côtéappele»` | on… | 284, 729 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Promià moinager le mardi»` | on… | 107, 751 | 165 × 198 | oui |  |
| Index 2 | `div#indexList>div.s4-grille>div.s4-carte«Chicheà Marionle grand p»` | on… | 284, 751 | 165 × 198 | oui |  |
| Index 3 | `div#indexSheet.sheet.trame>div.enh>div.closeb«✕ Fermer»` | on… | 296, 84 | 84 × 18 | oui |  |
| Index 3 | `#ixSearch` | natif | 174, 170 | 208 × 24 | oui |  |
| Index 3 | `#ixTriBtn` | natif | 340, 170 | 52 × 52 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promià moiplanter un arb»` | on… | 77, 299 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promià Rachelfaire les c»` | on… | 195, 299 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Cercleavec +4le potager9»` | on… | 313, 299 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Chicheà Marioncourir dim»` | on… | 77, 444 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promià moinager le mardi»` | on… | 195, 444 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Chicheà Marionle grand p»` | on… | 313, 444 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promià Rachelrapporter l»` | on… | 77, 589 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promide Rachelt'apprendr»` | on… | 195, 589 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promide Nicorapporter la»` | on… | 313, 589 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promide Marionvenir dima»` | on… | 77, 734 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Cerclepersol'atelier du »` | on… | 195, 734 | 106 × 133 | oui |  |
| Index 3 | `div#indexList>div.s4-grille>div.s4-carte«Promigardé de côtéappele»` | on… | 313, 734 | 106 × 133 | oui |  |
| Nuée | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| Nuée | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«CHICHE RELEVÉvider le co»` | on… | 195, 422 | 342 × 94 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUarroser tous les soi»` | on… | 195, 422 | 342 × 79 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-ocre«à tenirsemer les radisà »` | on… | 195, 422 | 342 × 79 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en coursarroser les toma»` | on… | 195, 447 | 342 × 79 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUmonter la serre avan»` | on… | 195, 535 | 342 × 94 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en courstailler la vigne»` | on… | 195, 538 | 342 × 79 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en coursramasser les cou»` | on… | 195, 629 | 342 × 79 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-ocre«à tenirreprendre l'arros»` | on… | 195, 641 | 342 × 94 | oui |  |
| Nuée | `#nfAdd` | natif | 195, 711 | 342 × 62 | oui |  |
| Nuée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUrécupérer les plants»` | on… | 195, 747 | 342 × 94 | oui |  |
| Nuée | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Nuée | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Nuée défilée | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUmonter la serre avan»` | on… | 195, 234 | 342 × 94 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-ocre«à tenirreprendre l'arros»` | on… | 195, 340 | 342 × 94 | oui |  |
| Nuée défilée | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en coursarroser les toma»` | on… | 195, 435 | 342 × 79 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUrécupérer les plants»` | on… | 195, 446 | 342 × 94 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en courstailler la vigne»` | on… | 195, 526 | 342 × 79 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«CHICHE RELEVÉvider le co»` | on… | 195, 552 | 342 × 94 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-cours«en coursramasser les cou»` | on… | 195, 617 | 342 × 79 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-menthe«TENUarroser tous les soi»` | on… | 195, 651 | 342 × 79 | oui |  |
| Nuée défilée | `#nfAdd` | natif | 195, 699 | 342 × 62 | oui |  |
| Nuée défilée | `div#dpNueeFil>div.nf-liste>div.nf-item.nf-ocre«à tenirsemer les radisà »` | on… | 195, 742 | 342 × 79 | oui |  |
| Nuée défilée | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Nuée défilée | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Nuée vide | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| Nuée vide | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Nuée vide | `#nfAdd` | natif | 195, 717 | 342 × 62 | oui |  |
| Nuée vide | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Nuée vide | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Nuée vide défilée | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| Nuée vide défilée | `#nfAdd` | natif | 195, 218 | 342 × 62 | oui |  |
| Nuée vide défilée | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Nuée vide défilée | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Nuée vide défilée | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Partager | `div#shareScreen.screen.s-share>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| Partager | `#shWrap` | écouteur | 195, 393 | 316 × 562 | oui |  |
| Partager | `#shareScreen` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Partager | `#shBadge` | natif | 85, 656 | 71 × 17 | oui |  |
| Partager | `#shcPeaufiner` | on… | 195, 717 | 342 × 62 | oui |  |
| Partager | `#shInviteBtn` | natif | 108, 789 | 168 × 62 | oui |  |
| Partager | `#shShareBtn` | natif | 282, 789 | 168 × 62 | oui |  |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-tete>div.s2-fermer«✕ FERMER»` | écouteur | 321, 56 | 91 × 13 | oui |  |
| Peaufiner | `#dpTraitReg` | écouteur | 195, 142 | 342 × 64 | oui |  |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg«AVANTjeudi 15un jouren l»` | écouteur | 195, 222 | 342 × 64 | oui |  |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg«DANS UN CERCLEaucuneAucu»` | écouteur | 195, 302 | 342 × 64 | oui |  |
| Peaufiner | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Peaufiner | `#dNote` | natif | 195, 426 | 292 × 56 | oui |  |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-cercle>div.s2-reg.s2-couleur«LA COULEUR#FFB8D2»` | écouteur | 195, 430 | 342 × 64 | NON | mur flouté (pointer-events:none) |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg.s2-vis2«PIÈCES JOINTES0 fichierp»` | écouteur | 195, 530 | 342 × 92 | oui |  |
| Peaufiner | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg.v16-danger«SUPPRIMER CE PROMI»` | écouteur | 195, 598 | 342 × 64 | oui |  |
| Peaufiner | `#dCommentInput` | natif | 195, 651 | 292 × 23 | oui |  |
| Peaufiner | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Peaufiner | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-tete>div.s2-fermer«✕ FERMER»` | écouteur | 321, 56 | 91 × 13 | oui |  |
| Peaufiner Chiche | `#dpTraitReg` | écouteur | 195, 142 | 342 × 64 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg«À QUI JE LANCEMarionMMar»` | écouteur | 195, 222 | 342 × 64 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg«AVECMarionMMarionNNicoRR»` | écouteur | 195, 302 | 342 × 64 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg«AVANTmardi 6un jouren l’»` | écouteur | 195, 382 | 342 × 64 | oui |  |
| Peaufiner Chiche | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-cercle>div.s2-reg.s2-couleur«LA COULEUR#FFB8D2»` | écouteur | 195, 430 | 342 × 64 | NON | mur flouté (pointer-events:none) |
| Peaufiner Chiche | `#dNote` | natif | 195, 506 | 292 × 56 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg.v16-danger«SUPPRIMER CE CHICHE»` | écouteur | 195, 598 | 342 × 64 | oui |  |
| Peaufiner Chiche | `div#dpdCorps.dpd-corps.peauf-reglages>div.s2-liste>div.s2-reg.s2-vis2«PIÈCES JOINTES0 fichierv»` | écouteur | 195, 610 | 342 × 92 | oui |  |
| Peaufiner Chiche | `#dCommentInput` | natif | 195, 724 | 292 × 23 | oui |  |
| Peaufiner Chiche | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Peaufiner Chiche | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Peaufiner Nuée | `#npFermer` | écouteur | 321, 56 | 91 × 19 | oui |  |
| Peaufiner Nuée | `div#npTrait.np-carte>div.pc-glisse>div.pc-rail>button.pc-t.on«Plein»` | natif | 87, 182 | 78 × 44 | oui |  |
| Peaufiner Nuée | `div#npTrait.np-carte>div.pc-glisse>div.pc-rail>button.pc-t«Coulé»` | natif | 175, 182 | 78 × 44 | oui |  |
| Peaufiner Nuée | `div#npTrait.np-carte>div.pc-glisse>div.pc-rail>button.pc-t«Peigné»` | natif | 263, 182 | 78 × 44 | oui |  |
| Peaufiner Nuée | `#nqNote` | natif | 195, 297 | 292 × 23 | oui |  |
| Peaufiner Nuée | `#nfAdd` | natif | 198, 380 | 348 × 68 | oui |  |
| Peaufiner Nuée | `#npMemb` | écouteur | 195, 396 | 342 × 64 | oui |  |
| Peaufiner Nuée | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| Peaufiner Nuée | `div#npCercle.s2-cercle>div.s2-reg.s2-couleur«LA COULEUR#FFB8D2»` | écouteur | 195, 482 | 342 × 64 | NON | mur flouté (pointer-events:none) |
| Peaufiner Nuée | `#dCommentInput` | natif | 195, 605 | 292 × 23 | oui |  |
| Peaufiner Nuée | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Peaufiner Nuée | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| Peaufiner gardé de côté | `div#createSheet.sheet.trame>div.enh>div.closeb«FERMER»` | on… | 297, 70 | 83 × 34 | oui |  |
| Peaufiner gardé de côté | `#planterZone` | écouteur | 195, 312 | 390 × 118 | oui |  |
| Peaufiner gardé de côté | `div#csPhrase.pp-phrase>div.ph-txt>span.ph-b«Je me promets»` | on… | 171, 452 | 293 × 60 | oui |  |
| Peaufiner gardé de côté | `div#csPhrase.pp-phrase>div.ph-txt>span.ph-m«appeler Mamie»` | on… | 194, 524 | 263 × 51 | oui |  |
| Peaufiner gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t.on«Plein»` | natif | 63, 645 | 78 × 44 | oui |  |
| Peaufiner gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Coulé»` | natif | 151, 645 | 78 × 44 | oui |  |
| Peaufiner gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Peigné»` | natif | 239, 645 | 78 × 44 | oui |  |
| Peaufiner gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Sec»` | natif | 327, 645 | 78 × 44 | oui |  |
| Peaufiner gardé de côté | `div#createSheet.sheet.trame>div.pp-garder«garder de côté»` | écouteur | 78, 716 | 107 × 16 | oui |  |
| Peaufiner gardé de côté | `#csBotBar` | écouteur | 195, 802 | 390 × 84 | oui |  |
| Politique | `div#legalScreen.screen.s-set>div.enh>div.closeb«✕ Fermer»` | écouteur | 296, 70 | 84 × 18 | oui |  |
| Réglages | `div#settingsScreen.screen.s-set>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| Réglages | `#setAva` | on… | 195, 218 | 78 × 78 | oui |  |
| Réglages | `#setNameInput` | natif | 189, 287 | 45 × 35 | oui |  |
| Réglages | `#openPlusTop` | on… | 195, 379 | 342 × 90 | oui |  |
| Réglages | `#openStudio2` | on… | 195, 470 | 342 × 64 | oui |  |
| Réglages | `#privCard` | on… | 195, 472 | 342 × 64 | oui |  |
| Réglages | `#resetData` | on… | 195, 472 | 342 × 64 | oui |  |
| Réglages | `#compteCard` | natif | 195, 472 | 342 × 64 | oui |  |
| Réglages | `#logoutCard` | natif | 195, 472 | 342 × 64 | oui |  |
| Réglages | `#delAccount` | natif | 195, 472 | 342 × 64 | oui |  |
| Réglages | `#cguCard` | natif | 195, 532 | 342 × 64 | oui |  |
| Réglages | `#replayOnb` | on… | 195, 548 | 342 × 64 | oui |  |
| Réglages | `#polCard` | natif | 195, 610 | 342 × 64 | oui |  |
| Réglages | `#setInvite` | natif | 195, 664 | 342 × 64 | oui |  |
| Réglages | `#aboutCard` | natif | 195, 688 | 342 × 64 | oui |  |
| Réglages | `#notifCard` | natif | 195, 780 | 342 × 64 | oui |  |
| Studio | `div#stpHaut>div.closeb«✕ Fermer»` | on… | 293, 70 | 91 × 19 | oui |  |
| Studio | `#studioScreen` | écouteur | 195, 422 | 422 × 876 | oui |  |
| Studio | `div#stpTons>div.stp-ton«»` | on… | 75, 620 | 54 × 54 | oui |  |
| Studio | `div#stpVue>div.stp-d«»` | on… | 81, 724 | 44 × 44 | oui |  |
| Studio | `div#stpVue>div.stp-d.on«»` | on… | 145, 724 | 44 × 44 | oui |  |
| Vie privée | `div#privScreen.screen.s-set>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| Vie privée | `#pvExport` | on… | 195, 525 | 342 × 54 | oui |  |
| Vie privée | `#pvReset` | on… | 195, 585 | 342 × 54 | oui |  |
| accueil | `#shareBtn` | on… | 284, 70 | 44 × 44 | oui |  |
| accueil | `#settingsBtn` | on… | 334, 70 | 44 × 44 | oui |  |
| accueil | `div#accPlat.acc-plat>span.acc-mm«Ma Parole !»` | natif | 104, 72 | 103 × 33 | oui |  |
| accueil | `#stage` | écouteur | 195, 422 | 390 × 844 | oui |  |
| accueil | `#toileCv` | écouteur | 195, 422 | 390 × 844 | oui |  |
| accueil | `#studioBtn` | on… | 70, 760 | 90 × 51 | oui |  |
| accueil | `#souffleBtn` | on… | 124, 760 | 90 × 51 | oui |  |
| accueil | `#createBtn` | on… | 195, 760 | 68 × 68 | oui |  |
| accueil | `#indexBtn` | natif | 266, 760 | 90 × 51 | oui |  |
| accueil | `#filBtn` | écouteur | 320, 760 | 90 × 51 | oui |  |
| aide de l'Aura | `div#auraHelp.screen.tuto-fond>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| chiche lancé | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| chiche lancé | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 221 | 34 × 34 | oui |  |
| chiche lancé | `#tenirZone` | écouteur | 195, 303 | 390 × 118 | oui |  |
| chiche lancé | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| chiche lancé | `div#dAura.aura-band>div.aura-track>div.kring«Marion»` | on… | 171, 427 | 70 × 83 | oui |  |
| chiche lancé | `div#dAura.aura-band>div.aura-track>div.kring«Rachel»` | on… | 255, 427 | 70 × 83 | oui |  |
| chiche lancé | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| chiche lancé | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| fiche chiche | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| fiche chiche | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 331 | 34 × 34 | oui |  |
| fiche chiche | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| fiche chiche | `div#dAura.aura-band>div.aura-track>div.kring«Marion»` | on… | 171, 495 | 70 × 83 | oui |  |
| fiche chiche | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| fiche chiche | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| fiche en cours | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| fiche en cours | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 221 | 34 × 34 | oui |  |
| fiche en cours | `#tenirZone` | écouteur | 195, 303 | 390 × 118 | oui |  |
| fiche en cours | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| fiche en cours | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| fiche en cours | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| fiche tenue | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| fiche tenue | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 335 | 34 × 34 | oui |  |
| fiche tenue | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| fiche tenue | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| fiche tenue | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| fiche à tenir | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| fiche à tenir | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 221 | 34 × 34 | oui |  |
| fiche à tenir | `#tenirZone` | écouteur | 195, 303 | 390 × 118 | oui |  |
| fiche à tenir | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| fiche à tenir | `div#dAura.aura-band>div.aura-track>div.kring«Rachel»` | on… | 171, 427 | 70 × 83 | oui |  |
| fiche à tenir | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| fiche à tenir | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| gardé de côté | `div#createSheet.sheet.trame>div.enh>div.closeb«FERMER»` | on… | 297, 70 | 83 × 34 | oui |  |
| gardé de côté | `#planterZone` | écouteur | 195, 312 | 390 × 118 | oui |  |
| gardé de côté | `div#csPhrase.pp-phrase>div.ph-txt>span.ph-b«Je me promets»` | on… | 171, 452 | 293 × 60 | oui |  |
| gardé de côté | `div#csPhrase.pp-phrase>div.ph-txt>span.ph-m«appeler Mamie»` | on… | 194, 524 | 263 × 51 | oui |  |
| gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t.on«Plein»` | natif | 63, 645 | 78 × 44 | oui |  |
| gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Coulé»` | natif | 151, 645 | 78 × 44 | oui |  |
| gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Peigné»` | natif | 239, 645 | 78 × 44 | oui |  |
| gardé de côté | `div#csPinceauRail.pc-rail>button.pc-t«Sec»` | natif | 327, 645 | 78 × 44 | oui |  |
| gardé de côté | `div#createSheet.sheet.trame>div.pp-garder«garder de côté»` | écouteur | 78, 716 | 107 × 16 | oui |  |
| gardé de côté | `#csBotBar` | écouteur | 195, 802 | 390 × 84 | oui |  |
| l'instant après | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| l'instant après | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| l'instant après | `div#dAura.aura-band>div.aura-track>div.kring«Rachel»` | on… | 171, 439 | 70 × 83 | oui |  |
| l'instant après | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| l'instant après | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| l'instant arrive | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| l'instant arrive | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| l'instant arrive | `div#dAura.aura-band>div.aura-track>div.kring«Rachel»` | on… | 171, 483 | 70 × 83 | oui |  |
| l'instant arrive | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| l'instant arrive | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| l'instant referme | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| l'instant referme | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| l'instant referme | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| l'instant referme | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| le Cercle | `div#plusScreen.screen.s-plus>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| le Cercle | `#buyMonth` | natif | 195, 709 | 346 × 58 | oui |  |
| le Cercle | `#buyYear` | natif | 195, 778 | 346 × 44 | oui |  |
| menu photo | `div#detailPoster.poster.mgmt>div.enh>div.closeb«FERMER»` | on… | 298, 70 | 80 × 12 | oui |  |
| menu photo | `div#detailPoster.poster.mgmt>div.ph-photo-nid>div.ph-photo-menu>button«Importer une image»` | natif | 262, 234 | 208 × 44 | oui |  |
| menu photo | `div#detailPoster.poster.mgmt>div.ph-photo-nid>div.ph-photo-menu>button«La dalle d’origine»` | natif | 269, 286 | 193 × 44 | oui |  |
| menu photo | `div#detailPoster.poster.mgmt>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 335 | 34 × 34 | oui |  |
| menu photo | `#detailPoster` | écouteur | 195, 422 | 390 × 844 | oui |  |
| menu photo | `#dpdTog` | écouteur | 195, 802 | 390 × 84 | oui |  |
| menu photo | `div#dpdTog.dpd-tog>span.dpd-part«Partager»` | on… | 343, 802 | 46 × 46 | oui |  |
| page + | `div#createSheet.sheet.trame>div.enh>div.closeb«FERMER»` | on… | 297, 70 | 83 × 34 | oui |  |
| page + | `div#createSheet.sheet.trame>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 215 | 34 × 34 | oui |  |
| page + | `#planterZone` | écouteur | 195, 280 | 390 × 118 | oui |  |
| page + | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-b«Je me promets»` | on… | 171, 420 | 293 × 60 | oui |  |
| page + | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«me coucherle jour même»` | on… | 187, 492 | 211 × 57 | oui |  |
| page + | `div#csPinceauRail.pc-rail>button.pc-t.on«Plein»` | natif | 63, 707 | 78 × 44 | oui |  |
| page + | `div#csPinceauRail.pc-rail>button.pc-t«Coulé»` | natif | 151, 707 | 78 × 44 | oui |  |
| page + | `div#csPinceauRail.pc-rail>button.pc-t«Peigné»` | natif | 239, 707 | 78 × 44 | oui |  |
| page + | `div#csPinceauRail.pc-rail>button.pc-t«Sec»` | natif | 327, 707 | 78 × 44 | oui |  |
| page + | `#csBotBar` | écouteur | 195, 802 | 390 × 84 | oui |  |
| page + Chiche | `div#createSheet.sheet.trame>div.enh>div.closeb«FERMER»` | on… | 297, 70 | 83 × 34 | oui |  |
| page + Chiche | `div#createSheet.sheet.trame>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 151 | 34 × 34 | oui |  |
| page + Chiche | `#planterZone` | écouteur | 195, 216 | 390 × 118 | oui |  |
| page + Chiche | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«qui ose ?»` | on… | 128, 352 | 150 × 49 | oui |  |
| page + Chiche | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-b.ph-b-fixe«Chiche»` | on… | 82, 416 | 116 × 52 | oui |  |
| page + Chiche | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«dire oui pourune fois»` | on… | 170, 480 | 194 × 49 | oui |  |
| page + Chiche | `div#csPhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«qui en est ?»` | on… | 188, 608 | 181 × 49 | oui |  |
| page + Chiche | `div#csPinceauRail.pc-rail>button.pc-t.on«Plein»` | natif | 63, 727 | 78 × 44 | oui |  |
| page + Chiche | `div#csPinceauRail.pc-rail>button.pc-t«Coulé»` | natif | 151, 727 | 78 × 44 | oui |  |
| page + Chiche | `div#csPinceauRail.pc-rail>button.pc-t«Peigné»` | natif | 239, 727 | 78 × 44 | oui |  |
| page + Chiche | `div#csPinceauRail.pc-rail>button.pc-t«Sec»` | natif | 327, 727 | 78 × 44 | oui |  |
| page + Chiche | `#csBotBar` | écouteur | 195, 802 | 390 × 84 | oui |  |
| page + Nuée | `div#createSheet.sheet.trame>div.enh>div.closeb«FERMER»` | on… | 297, 70 | 83 × 34 | oui |  |
| page + Nuée | `div#createSheet.sheet.trame>div.ph-photo-nid>button.ph-photo-btn«Photo»` | natif | 349, 183 | 34 × 34 | oui |  |
| page + Nuée | `#planterZoneN` | écouteur | 195, 248 | 390 × 118 | oui |  |
| page + Nuée | `div#nueePhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«Week-endà Marseille»` | on… | 238, 455 | 184 × 54 | oui |  |
| page + Nuée | `div#nueePhrase.pp-phrase>div.ph-txt.ph-coupe>span.ph-m.ph-vide«tout le monde»` | on… | 223, 593 | 231 × 54 | oui |  |
| page + Nuée | `div#csPinceauRail.pc-rail>button.pc-t.on«Plein»` | natif | 63, 690 | 78 × 44 | oui |  |
| page + Nuée | `div#csPinceauRail.pc-rail>button.pc-t«Coulé»` | natif | 151, 690 | 78 × 44 | oui |  |
| page + Nuée | `div#csPinceauRail.pc-rail>button.pc-t«Peigné»` | natif | 239, 690 | 78 × 44 | oui |  |
| page + Nuée | `div#csPinceauRail.pc-rail>button.pc-t«Sec»` | natif | 327, 690 | 78 × 44 | oui |  |
| page + Nuée | `#csBotBar` | écouteur | 195, 802 | 390 × 84 | oui |  |
| personne | `div#personSheet.sheet.tuto-fond>div.enh>div.closeb«✕ Fermer»` | on… | 296, 70 | 84 × 18 | oui |  |
| personne | `div#psCartes.ps-cartes>div.s4-grille>div.s4-carte«Promià Rachelfaire les c»` | on… | 77, 462 | 106 × 133 | oui |  |
| personne | `div#psCartes.ps-cartes>div.s4-grille>div.s4-carte«Chicheà Marioncourir dim»` | on… | 195, 462 | 106 × 133 | oui |  |
| personne | `div#psCartes.ps-cartes>div.s4-grille>div.s4-carte«Promiau groupereprendre »` | on… | 313, 462 | 106 × 133 | oui |  |
| personne | `div#psCartes.ps-cartes>div.s4-grille>div.s4-carte«Promià Rachelrapporter l»` | on… | 77, 607 | 106 × 133 | oui |  |
| personne | `div#psCartes.ps-cartes>div.s4-grille>div.s4-carte«Promide Rachelt'apprendr»` | on… | 195, 607 | 106 × 133 | oui |  |
| personne | `div#psCadre>div.ps-col>div.ps-pile>div.ps-bt«+ Planter un Promi»` | natif | 108, 791 | 167 × 62 | oui |  |
| personne | `div#psCadre>div.ps-col>div.ps-pile>div.ps-bt«+ Lancer un Chiche»` | natif | 283, 791 | 167 × 62 | oui |  |
| À propos | `div#aboutScreen.screen.s-set>div.enh>div.closeb«✕ Fermer»` | écouteur | 296, 70 | 84 × 18 | oui |  |
| À propos | `div.v16-corps>div.v16-cr>p.v16-petit>a«creativecommons.org/lice»` | natif | 351, 492 | 30 × 19 | oui |  |
