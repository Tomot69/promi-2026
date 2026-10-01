# Le parcours — spécification

> Traduction du moodboard en décisions écrites.
> **C'est ce document qui fait référence, pas le HTML du moodboard.**
>
> Un lot d'intégration se réfère à une section numérotée d'ici.

---

## 0 · La trame commune

Tous les écrans de fiche et de création suivent cette structure.
**Aucune exception.**

| Zone | Hauteur | Contenu |
|---|---|---|
| **HAUT** | 176–210 px fixes | la dalle · à gauche : sur la **fiche**, la **nature** `#dptNat` (Fraunces **30 px**) — le mot-marque « Promi » 20 px n'existe **que sur la page +** (lot 1), pas sur la fiche · `✕ FERMER` à droite, à 50 px du haut |
| **TITRE** | auto, suivi de 24 px | ce qu'on lit en premier |
| **CORPS** | le reste | le contenu **commence en haut** et respire vers le bas |
| **TRAIT** | **164 px** (canvas ; conteneur fiche 176 px), précédé de 24 px | le geste, toujours entier |
| **PEAUFINER** | 62 px | même typographie, même filet, même place |

**Interdits :**
- `margin-top: auto` sur le corps — il crée un trou
- un élément qui mord sur la zone HAUT
- un trait rogné par le bas de l'écran

---

## 1 · L'écran de choix

**Déclenché par :** le bouton `+` du dock.

### Contenu

```
[dalle]                          zone HAUT
Promi                    ✕ FERMER

Qu'est-ce                        zone TITRE, Bricolage 32 px
que tu promets ?

┌──────────────────────────┐     zone CORPS
│ Un Promi                 │     bleu #3A54FF, plein, coché
│ à quelqu'un, ou à toi    │     rayon 22 px
└──────────────────────────┘
┌──────────────────────────┐
│ Une Nuée                 │     contour, texte crème
│ un groupe, un projet     │
└──────────────────────────┘
┌──────────────────────────┐
│ Un brouillon             │     contour
│ pour y revenir           │
└──────────────────────────┘
```

### Comportement

**Toucher une carte ne change pas d'écran.** La carte s'étend, les deux autres se
replient en bandeaux, et le formulaire se déplie dessous. On revient en touchant
une autre carte.

### Typographie

- Titre de carte : Bricolage 21 px, 800
- Sous-titre : 12,5 px, opacité 72 %

---

## 2 · La page + — la phrase

**Fond :** bleu `#3A54FF` (Promi) · mauve `#8A5CF0` (Nuée) · encre (brouillon)

### La phrase

```
Je promets ⇄ ✦
à Rachel
de rendre le livre
avant · un jour
```

**Bricolage 28–30 px, interligne 1.56.**

### Les éléments

| Élément | Apparence | Comportement |
|---|---|---|
| **« Je promets »** | pastille **menthe** `#2BE88C`, encre `#06231A`, rayon 13 px, padding 2/13/4, avec la flèche | au toucher : retourne la phrase |
| **La flèche** | deux traits horizontaux, **pointes opposées**, 17 px | animation : flip horizontal 320 ms, `cubic-bezier(.22,1,.36,1)` |
| **✦** | menthe, 0,72 em, `vertical-align: .2em` | décoratif |
| **« à », « de », « avant »** | opacité 42 %, même graisse | non touchables |
| **Les mots variables** | pastille **encre** (`--on-surf`), **texte crème** (`--surf`), rayon 12 px | au toucher : ouvre les choix |
| *(corrigé lot 2B)* | l'ancienne spec disait « pastille blanche, encre du fond » — **faux** : blanc sur fond crème est invisible (prouvé en capture). Le mot rempli est une pastille sombre à texte clair. | |
| **Un mot vide** | transparent, opacité 38 %, souligné de 2,5 px | idem |
| **Un mot touché** | transparent, contour 2 px | idem |

### Les choix

Ils s'ouvrent **sous la phrase**, dans le même écran.

```
AVANT QUAND                      libellé 11 px, .16em, opacité 60 %
[un jour] [demain] [5 jours] [2 semaines] [ce mois-ci]
```

- Transition : `max-height` sur 340 ms, `cubic-bezier(.22,1,.36,1)`
- Pastilles : 13/19 px, rayon 999, contour 1,4 px
- Pastille active : aplat plein, 800

**Pour le titre**, un champ de saisie remplace les pastilles : Bricolage 22 px,
filet de 1,5 px en dessous.

### Les destinataires

```
hors Nuée    Moi · [prénoms récents] · +
dans Nuée    tout le monde · Moi · [prénoms] 
```

**Le premier est coché par défaut.** « Moi » porte son avatar dégradé
(`linear-gradient(135deg, #8A5CF0, #3A54FF)`), 21–24 px.

### L'échéance

**« un jour » est le défaut**, précédé d'un **point médian** `·` à 50 % d'opacité.
D�s qu'une vraie date est choisie, le point disparaît.

### Le sens inverse

```
Rachel,
promets-moi ⇄ ✦
de m'appeler
avant · dimanche
```

Le prénom passe en tête, le verbe bascule en dessous. Le libellé du champ
devient `À QUI TU LE DEMANDES`.

### Le bas

Le **trait pour planter**, libellé `glisse pour planter →`.
Puis **Peaufiner**.

> **✅ Intégré au lot 1.** Valeurs **mesurées**, alignées au pixel sur le geste de
> tenir de la fiche : hauteur **164 px** (canvas ; conteneur 176), **rayon 0** (pas
> 26), fond clair `rgba(22,23,27,.055)` / sombre `rgba(255,255,255,.12)`, libellé
> **17 px / 800 / bas 26 px**, point gauche **r=19 plein**, point droit **contour
> r=19 (α .40, trait 2,5) + plein r=6 (α .40)**. C'est un **duplicata isolé** du
> geste (le CSS `.tenir` est scopé `#detailPoster`) — à mutualiser dans un lot dédié.
> Le bouton « PLANTER LE PROMI » reste accessible par la bascule « bouton ».

---

## 3 · Peaufiner déplié

Le haut se réduit à la nature. Le titre passe en 26 px avec un sous-titre
*« à Rachel · dans 5 jours »*.

### Le contenu

Une ligne par réglage : **icône à gauche, nom, valeur à droite**.

```
☁  Dans une Nuée                        —
≡  Une note                             —
📎 Pièces jointes                       —
✦  Important ?                          ··
```

Filet de séparation à 18 % sous chaque ligne.

### L'encart Cercle

```
✦ LE CERCLE
Récurrence · Rappel intelligent
```

Rayon 20 px, contour 1,3 px. **Jamais flouté** — on voit ce qui existe.

### Comportement

**Le trait reste accessible** : on peut planter sans refermer.

Peaufiner s'ouvre **au clic ET au geste** — `touchmove` de plus de 26 px vers le
haut, ou molette. Le scroll n'est jamais bloqué.

---

## 4 · La fiche d'un Promi

**Fond :** orange `#F07A2E` (à tenir) · menthe `#2BE88C` (tenue)
**Corps :** plus clair que le haut — voir `CLAUDE.md § 3`

### Le titre

```
à Rachel                    17 px, 700, opacité 78 %
rendre le livre             Bricolage 34 px (26 si long), interligne 1.06
À TENIR                     10,5 px, .16em, 700, opacité 74 %
```

Un titre long réduit sa taille pour tenir sur **deux lignes maximum**, sans
changer la hauteur du bloc.

### Le corps

**Une carte** pour le dernier commentaire :

```
┌────────────────────────────────┐
│ RACHEL, HIER                   │  10,5 px, .14em, opacité 78 %
│ pas de presse ♥                │  15 px, interligne 1.5
│ ─────────────────────────────  │
│ 💬 répondre…                    │  ligne de réponse, opacité 55 %
└────────────────────────────────┘
```

Fond : blanc à 15 %. Rayon 20 px.

**Puis une seule ligne de pastilles**, libellés courts :

```
[≡ note]  [📎 1]  [☁ Famille]
```

> **⚠ Non intégré.** La ligne « répondre… » n'est pas dans la carte ; les
> commentaires sont dans Peaufiner.

### Quand c'est vide

Trois boutons à icône, en contour, au même emplacement :

```
[💬 dire un mot]  [≡ une note]  [📎 joindre]
```

**Une invitation, pas un trou.**

---

## 5 · La fiche d'un Promi tenu

Même trame que le § 4. En plus :

- **La trace** au centre du corps : le trait réellement tracé, redessiné en SVG,
  82 % de largeur, épaisseur 4,6 px
- Le dernier commentaire avec sa ligne de réponse — **un Promi tenu se commente
  encore**
- Les pastilles : `[≡ note] [📎 1]`
- **Pas de trait** — il n'y a plus rien à tenir
- Le partage est dans la ligne Peaufiner

**Supprimé :** « Belle parole. » comme bloc, et les deux gros boutons.

---

## 6 · La fiche d'une Nuée

### Le haut

Une **planche de dalles** : celles des Promi du groupe, **opaques et nettes**,
posées en quinconce sur le voile mauve.

Positions relatives : `[0.50,0.42,0.46] [0.16,0.30,0.34] [0.80,0.26,0.32]
[0.30,0.68,0.30] [0.68,0.72,0.28] [0.04,0.66,0.24]` — six maximum.

Avec Firebase, chaque dalle portera **le monde de celui qui l'a plantée**.

### Le titre

```
Nuée                        signature, sur la planche
avec Maman                  qui en est
Famille                     Bricolage 48 px
3 paroles · 1 tenue         le compte, jamais un pourcentage
```

### Le corps

```
[+ Planter un Promi]  [⇧]      contour, pleine largeur + icône ronde

mardi                          la grammaire du Fil
rappeler dimanche              aplat de l'état
à Maman              [dalle]   la vraie dalle à droite
```

**Pas de geste, pas de disques, pas de trace** — on ne tient pas une Nuée.

**Les traits de la fiche** prennent la teinte de **la dernière dalle plantée**.

---

## 7 · Partager

**C'est `shareScreen`.** On ne duplique pas la page.

### Le sélecteur

```
depuis le dock      [Ma Toile] [Mes Promi]
depuis un Promi     [rendre…] [Ma Toile] [Mes Promi]
depuis une Nuée     [Week-end…] [Ma Toile] [Mes Promi]
```

L'onglet contextuel porte **le début du vrai titre** suivi de `…`.
Il est actif à l'ouverture. **Il ne s'installe pas** : rouvrir depuis le dock
ramène `Ma Toile / Mes Promi`.

### La prévisualisation

| Source | Contenu |
|---|---|
| **Ma Toile** | six dalles sur l'encre, opacité 1 |
| **Un Promi** | fond de l'état · la dalle **au premier plan** · « à Rachel » · le titre en 30 px |
| **Une Nuée** | fond mauve · cinq dalles en constellation · les prénoms · le nom en 30 px |

**Aucun statut écrit.** **Aucun chiffre.** Le mot-marque « Promi » en Fraunces
15 px, haut à gauche, opacité 78 %.

### Les formats

```
[9:16]  [1:1]  [4:5]
```

### Le bouton

Une **icône ronde de 62 px**, fond encre, sans texte. À côté, les `⋯` dans un
rond de même taille en contour.

---

## 8 · Le brouillon

**Non intégré.** Spécification complète :

### L'écran de création

```
Brouillon                   signature terracotta
                            liseré pointillé terracotta 2,5 px sur tout l'écran

Ce sera                     Bricolage 20 px, terracotta
[un Promi] [une Nuée]       pastilles, « un Promi » pré-coché

Ce que tu mets de côté
offrir des fleurs à Maman…  Bricolage 27 px, filet terracotta

À qui
[Moi] [Maman] [Rachel] [+]  encre crème, JAMAIS terracotta sur terracotta

[Garder pour plus tard]     bouton terracotta plein — pas un trait
```

### Un brouillon en cours de plantation

Le fond porte **la couleur de ce qu'il va devenir** (bleu ou mauve).
Par-dessus, **quatre rappels terracotta** :

1. liseré pointillé 3 px encadrant l'écran
2. pastille `BROUILLON` en contour, haut à droite
3. filet du titre en terracotta
4. bouton d'action en terracotta plein

---

## 9 · Ce qui revient partout

| Élément | Règle |
|---|---|
| **Le geste** | **164 px** (canvas ; conteneur 176), **rayon 0**, deux points, un trait. Part du **centre du rond gauche**. Courbes quadratiques. Toujours entier. |
| **Peaufiner** | 62 px, en bas, avec l'icône de partage à droite |
| **✕ FERMER** | haut à droite, 50 px du haut, avec le texte |
| **Promi** (mot-marque) | Fraunces, haut à gauche, 20 px — **sur la page + uniquement** (lot 1). Sur la **fiche**, le haut-gauche est la **nature** `#dptNat` en Fraunces **30 px**, pas un mot-marque 20 px. |
| **« Moi »** | premier, avec son avatar dégradé |
| **Les boutons ronds** | icône seule, jamais de texte |
| **Les pastilles** | contour = vide · aplat plein = rempli |
