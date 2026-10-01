> # ⚠ ARCHIVE — NE PAS PORTER (assainissement, Tom, 30 septembre 2026)
> Ce document décrit l'état d'**août 2026** (moodboard H) : ses **couleurs, polices et libellés sont périmés** (palette d'avant
> le 16 septembre, Fraunces / Bricolage / Apfel retirées, « Nuée » devenue « Cercle », « Le Cercle » devenu « Ma Parole ! »).
> Il reste utile pour la **géométrie et l'intention** d'origine. **Ce qui est vrai aujourd'hui : `ETAT-30-SEPTEMBRE-2026.md`.**

# Moodboard — toutes les valeurs, nœud par nœud

**Extraction automatique de `MOODBOARD-parcours.html`. Aucune interprétation :
c'est le fichier tel qu'il est, arbre complet des neuf écrans.**

C'est la source de vérité. Quand une valeur de l'app diffère de celle-ci,
c'est l'app qui a tort.

## Les neuf écrans

| | Écran | Fond |
|---|---|---|
| `ph-0` | le choix des trois natures | `#16171B` encre |
| `ph-1` | la phrase · Je promets | `#3A54FF` bleu |
| `ph-2` | la phrase · promets-moi | `#3A54FF` bleu |
| `ph-3` | la phrase · dans une Nuée | violet |
| `ph-4` | à qui · hors Nuée | `#3A54FF` bleu |
| `ph-5` | à qui · dans une Nuée | violet |
| `ph-6` | **fiche · titre court 34px · À TENIR** | `#F07A2E` orange |
| `ph-7` | **fiche · titre long 26px · À TENIR** | `#F07A2E` orange |
| `ph-8` | **fiche · TENUE · avec le tracé** | `#2BE88C` menthe |

## Classes de base

```
.ph    352 × 762 · flex column · border-radius 48 (châssis de maquette)
.big   Bricolage 800 · letter-spacing -.05em · line-height 1.06
```

## La structure, identique sur les neuf écrans

```
zone dalle      flex:0 0 auto · height 210px (150px si un chooser est ouvert)
mot-marque      absolute · left 22 · top 48 · 20px/600 · opacité .9
FERMER          absolute · right 22 · top 50 · 11px · ls .14em · opacité .78
                croix SVG 13×13 stroke 1.8 + le mot « FERMER »
corps           flex:1 1 auto · padding 0 22px · min-height 0
barre du bas    flex:0 0 auto · height 62px · padding 0 22px
                filet inset 0 1px 0 · Bricolage 17/800 · ls -.035em
                ▾ opacité .5 · 12px · gap 16
```

## Détails de DA faciles à manquer

**En état « à qui » (`ph-4`, `ph-5`) :**
- la zone dalle passe de **210 à 150px**, et la dalle change de position
- la phrase entière passe à **22px, opacité .6**, `line-height 1.58`
- le padding du bloc phrase passe de `24px 22px 0` à **`22px 22px 26px`**
- **le mot en cours d'édition** prend un **contour blanc 2px**
  (`box-shadow:inset 0 0 0 2px #fff`) au lieu du fond blanc plein
- **les autres mots remplis** passent en `rgba(255,255,255,.34)`
- pastilles : `gap:9px` · `flex-wrap:wrap`

**Les mots de la phrase (`ph-1`) :**
- rempli → fond `#fff`, texte couleur de nature, `radius 12`, `padding 1px 9px 3px`
- vide → fond `rgba(255,255,255,.28)`, texte `#fff`, mêmes rayon et padding
- liaisons « à / de / avant » → opacité **.45**
- l'étoile ✦ → `#2BE88C`, `font-size .74em`, `vertical-align .2em`

**La pastille « Je promets » :**
- fond `#2BE88C` · texte `#06231A` · `radius 13` · `padding 2px 13px 4px`
- `letter-spacing -.045em` · `gap 9px` · contient la flèche SVG 17×17

---


## ph-0 CHOIX

<div> .ph | background:#16171B
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#16171B
    <img> | position:absolute;left:10%;top:16%;width:28%;opacity:1;z-index:2
    <img> | position:absolute;left:58%;top:30%;width:22%;opacity:1;z-index:2
    <img> | position:absolute;left:34%;top:58%;width:18%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#F4EEE1;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#F4EEE1;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:26px 22px 26px
    <div> .big | font-size:32px;color:#F4EEE1
      « Qu’est-ce »
      « que tu promets ? »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | display:flex;flex-direction:column;gap:11px
      <div> | padding:20px 22px;border-radius:22px;background:#3A54FF;color:#fff
        <div> .big | font-size:21px
          « Un Promi »
        <div> | font-size:12.5px;opacity:.72;margin-top:4px
          « à quelqu’un, ou à toi »
      <div> | padding:20px 22px;border-radius:22px;box-shadow:inset 0 0 0 1.4px rgba(244,238,225,.2);color:#F4EEE1
        <div> .big | font-size:21px
          « Une Nuée »
        <div> | font-size:12.5px;opacity:.72;margin-top:4px
          « un groupe, un projet »
      <div> | padding:20px 22px;border-radius:22px;box-shadow:inset 0 0 0 1.4px rgba(244,238,225,.2);color:#F4EEE1
        <div> .big | font-size:21px
          « Un brouillon »
        <div> | font-size:12.5px;opacity:.72;margin-top:4px
          « pour y revenir »
  <div> | flex:0 0 auto;height:62px


## ph-1 PHRASE je promets

<div> .ph | background:#3A54FF
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#3A54FF
    <img> | position:absolute;left:24%;top:22%;width:34%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:1 1 auto;padding:24px 22px 0;min-height:0;color:#fff
    <div> .big | font-size:29px;line-height:1.56
      <span> | display:inline-flex;align-items:center;gap:9px;background:#2BE88C;color:#06231A;border-radius:13px;padding:2px 13px 4px;font-family:Bricolage,system-ui,sans-serif;font-weight:800;letter-spacing:-.045em
        « Je promets »
        <svg> viewBox="0 0 22 22" w=17 h=17 | flex:none
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
      <span> | color:#2BE88C;font-size:.74em;vertical-align:.2em
        « ✦ »
      <span> | opacity:.45
        « à »
      <span> | background:#fff;color:#3A54FF;border-radius:12px;padding:1px 9px 3px
        « Rachel »
      <span> | opacity:.45
        « de »
      <span> | background:#fff;color:#3A54FF;border-radius:12px;padding:1px 9px 3px
        « rendre le livre »
      <span> | opacity:.45
        « avant »
      <span> | background:rgba(255,255,255,.28);color:#fff;border-radius:12px;padding:1px 9px 3px
        « un jour »
    <div> | font-size:12.5px;opacity:.58;margin-top:26px
      « touche »
      <b> | color:#2BE88C
        « Je promets »
      « pour inverser le sens »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.12);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour planter → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.28)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »


## ph-2 PHRASE promets-moi

<div> .ph | background:#3A54FF
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#3A54FF
    <img> | position:absolute;left:24%;top:22%;width:34%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:1 1 auto;padding:24px 22px 0;min-height:0;color:#fff
    <div> .big | font-size:29px;line-height:1.56
      <span> | background:#fff;color:#3A54FF;border-radius:12px;padding:1px 9px 3px
        « Rachel »
      « , »
      <span> | display:inline-flex;align-items:center;gap:9px;background:#2BE88C;color:#06231A;border-radius:13px;padding:2px 13px 4px;font-family:Bricolage,system-ui,sans-serif;font-weight:800;letter-spacing:-.045em
        « promets-moi »
        <svg> viewBox="0 0 22 22" w=17 h=17 | flex:none
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
      <span> | color:#2BE88C;font-size:.74em;vertical-align:.2em
        « ✦ »
      <span> | opacity:.45
        « de »
      <span> | background:#fff;color:#3A54FF;border-radius:12px;padding:1px 9px 3px
        « m’appeler »
      <span> | opacity:.45
        « avant »
      <span> | background:#fff;color:#3A54FF;border-radius:12px;padding:1px 9px 3px
        « dimanche »
    <div> | font-size:12.5px;opacity:.58;margin-top:26px
      « touche »
      <b> | color:#2BE88C
        « promets-moi »
      « pour inverser le sens »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.12);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour planter → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.28)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »


## ph-3 PHRASE dans une Nuee

<div> .ph | background:#8A5CF0
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#8A5CF0
    <img> | position:absolute;left:30%;top:22%;width:30%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:1 1 auto;padding:24px 22px 0;min-height:0;color:#fff
    <div> .big | font-size:29px;line-height:1.56
      <span> | display:inline-flex;align-items:center;gap:9px;background:#2BE88C;color:#06231A;border-radius:13px;padding:2px 13px 4px;font-family:Bricolage,system-ui,sans-serif;font-weight:800;letter-spacing:-.045em
        « Je promets »
        <svg> viewBox="0 0 22 22" w=17 h=17 | flex:none
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
      <span> | color:#2BE88C;font-size:.74em;vertical-align:.2em
        « ✦ »
      <span> | opacity:.45
        « à »
      <span> | background:#fff;color:#8A5CF0;border-radius:12px;padding:1px 9px 3px
        « tout le monde »
      <span> | opacity:.45
        « de »
      <span> | background:#fff;color:#8A5CF0;border-radius:12px;padding:1px 9px 3px
        « réserver le van »
      <span> | opacity:.45
        « avant »
      <span> | background:rgba(255,255,255,.28);color:#fff;border-radius:12px;padding:1px 9px 3px
        « un jour »
    <div> | font-size:12.5px;opacity:.58;margin-top:26px
      « dans »
      <b>
        « Week-end à Lisbonne »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.12);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour planter → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.28)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »


## ph-4 A QUI hors Nuee

<div> .ph | background:#3A54FF
  <div> | position:relative;flex:0 0 auto;height:150px;overflow:hidden;background:#3A54FF
    <img> | position:absolute;left:26%;top:26%;width:24%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:22px 22px 26px;color:#fff
    <div> .big | font-size:22px;line-height:1.58;opacity:.6
      <span> | display:inline-flex;align-items:center;gap:9px;background:#2BE88C;color:#06231A;border-radius:13px;padding:2px 13px 4px;font-family:Bricolage,system-ui,sans-serif;font-weight:800;letter-spacing:-.045em
        « Je promets »
        <svg> viewBox="0 0 22 22" w=17 h=17 | flex:none
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
      « à »
      <span> | box-shadow:inset 0 0 0 2px #fff;border-radius:12px;padding:1px 9px 3px;opacity:1
        « Rachel »
      « de »
      <span> | background:rgba(255,255,255,.34);color:#fff;border-radius:12px;padding:1px 9px 3px
        « rendre le livre »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | color:#fff
      <div> | font-size:11px;letter-spacing:.16em;opacity:.6;margin-bottom:14px
        « À QUI »
      <div> | display:flex;flex-wrap:wrap;gap:9px
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Moi »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;background:#fff;color:#3A54FF;font-weight:800
          « Rachel »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Nico »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Adrien »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Maman »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « + »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.12);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour planter → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.28)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »


## ph-5 A QUI dans une Nuee

<div> .ph | background:#8A5CF0
  <div> | position:relative;flex:0 0 auto;height:150px;overflow:hidden;background:#8A5CF0
    <img> | position:absolute;left:32%;top:26%;width:22%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:22px 22px 26px;color:#fff
    <div> .big | font-size:22px;line-height:1.58;opacity:.6
      <span> | display:inline-flex;align-items:center;gap:9px;background:#2BE88C;color:#06231A;border-radius:13px;padding:2px 13px 4px;font-family:Bricolage,system-ui,sans-serif;font-weight:800;letter-spacing:-.045em
        « Je promets »
        <svg> viewBox="0 0 22 22" w=17 h=17 | flex:none
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
          <path> stroke-width=2.2
      « à »
      <span> | box-shadow:inset 0 0 0 2px #fff;border-radius:12px;padding:1px 9px 3px;opacity:1
        « tout le monde »
      « de »
      <span> | background:rgba(255,255,255,.34);color:#fff;border-radius:12px;padding:1px 9px 3px
        « réserver le van »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | color:#fff
      <div> | font-size:11px;letter-spacing:.16em;opacity:.6;margin-bottom:14px
        « À QUI »
      <div> | display:flex;flex-wrap:wrap;gap:9px
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;background:#fff;color:#8A5CF0;font-weight:800
          « tout le monde »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Rachel »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Nico »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Maman »
        <div> | padding:13px 19px;border-radius:999px;font-size:14.5px;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.4)
          « Moi »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.12);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour planter → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.28)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »


## ph-6 FICHE titre court

<div> .ph | background:#F07A2E
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#F07A2E
    <img> | position:absolute;left:26%;top:20%;width:34%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:24px 22px 24px;color:#fff
    <div> | font-size:17px;font-weight:700;opacity:.78
      « à »
      <b> | opacity:1
        « Rachel »
    <div> .big | font-size:34px;margin-top:9px;line-height:1.06
      « rendre le livre »
    <div> | font-size:10.5px;letter-spacing:.16em;font-weight:700;margin-top:13px;opacity:.74
      « À TENIR »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | color:#fff
      <div> | padding:17px 19px 4px;border-radius:20px;background:rgba(255,255,255,.15)
        <div> | font-size:10.5px;letter-spacing:.14em;opacity:.78;margin-bottom:8px
          « RACHEL, HIER »
        <div> | font-size:15px;line-height:1.5
          « pas de presse ♥ »
        <div> | display:flex;align-items:center;gap:11px;padding:14px 4px 0;color:#fff
          <svg> viewBox="0 0 24 24" w=17 h=17 stroke-width=1.8
            <path>
          <span> | font-size:14px;opacity:.55
            « répondre… »
        <div> | height:1.2px;background:rgba(255,255,255,.24);margin-top:10px
      <div> | display:flex;gap:7px;margin-top:12px
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « note »
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « 1 »
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « Famille »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.14);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour tenir → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.3)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »
      <svg> viewBox="0 0 24 24" w=19 h=19 stroke-width=1.8
        <path>
        <path>
        <path>


## ph-7 FICHE titre long

<div> .ph | background:#F07A2E
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#F07A2E
    <img> | position:absolute;left:26%;top:20%;width:34%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#fff;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#fff;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:24px 22px 24px;color:#fff
    <div> | font-size:17px;font-weight:700;opacity:.78
      « à »
      <b> | opacity:1
        « Rachel »
    <div> .big | font-size:26px;margin-top:9px;line-height:1.06
      « rapporter les photos du week-end »
    <div> | font-size:10.5px;letter-spacing:.16em;font-weight:700;margin-top:13px;opacity:.74
      « À TENIR »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | color:#fff
      <div> | padding:17px 19px 4px;border-radius:20px;background:rgba(255,255,255,.15)
        <div> | font-size:10.5px;letter-spacing:.14em;opacity:.78;margin-bottom:8px
          « RACHEL, HIER »
        <div> | font-size:15px;line-height:1.5
          « pas de presse ♥ »
        <div> | display:flex;align-items:center;gap:11px;padding:14px 4px 0;color:#fff
          <svg> viewBox="0 0 24 24" w=17 h=17 stroke-width=1.8
            <path>
          <span> | font-size:14px;opacity:.55
            « répondre… »
        <div> | height:1.2px;background:rgba(255,255,255,.24);margin-top:10px
      <div> | display:flex;gap:7px;margin-top:12px
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « note »
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « 1 »
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(255,255,255,.34)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « Famille »
  <div> | flex:0 0 auto;padding:22px 22px 12px
    <div> | height:118px;border-radius:26px;position:relative;background:rgba(255,255,255,.14);overflow:hidden
      <svg> viewBox="0 0 308 118" | width:100%;height:100%;display:block
        <circle>
        <circle> stroke-width=2.2
        <circle>
      <div> | position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:13px;font-weight:800;color:#fff
        « glisse pour tenir → »
      <div> | position:absolute;right:14px;top:12px;font-size:10.5px;opacity:.5;padding:5px 11px;border-radius:999px;box-shadow:inset 0 0 0 1px currentColor;color:#fff
        « bouton »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#fff;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,.3)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »
      <svg> viewBox="0 0 24 24" w=19 h=19 stroke-width=1.8
        <path>
        <path>
        <path>


## ph-8 FICHE TENUE

<div> .ph | background:#2BE88C
  <div> | position:relative;flex:0 0 auto;height:210px;overflow:hidden;background:#2BE88C
    <img> | position:absolute;left:26%;top:20%;width:34%;opacity:1;z-index:2
  <div> | position:absolute;left:22px;top:48px;z-index:9;font-family:Georgia,serif;font-weight:600;font-size:20px;letter-spacing:-.02em;color:#06231A;opacity:.9
    « Promi »
  <div> | position:absolute;right:22px;top:50px;z-index:9;display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.14em;color:#06231A;opacity:.78
    <svg> viewBox="0 0 24 24" w=13 h=13 stroke-width=1.8
      <path>
    « FERMER »
  <div> | flex:0 0 auto;padding:24px 22px 20px;color:#06231A
    <div> | font-size:17px;font-weight:700;opacity:.7
      « à »
      <b> | opacity:1
        « Rachel »
    <div> .big | font-size:34px;margin-top:9px;line-height:1.06
      « rendre le livre »
    <div> | font-size:10.5px;letter-spacing:.16em;font-weight:700;margin-top:13px;opacity:.64
      « TENUE »
  <div> | flex:1 1 auto;padding:0 22px;min-height:0
    <div> | color:#06231A
      <div> | text-align:center;margin-bottom:24px
        <svg> viewBox="0 0 300 62" | width:82%%;height:62px
          <path> stroke-width=4.6
      <div> | padding:17px 19px 4px;border-radius:20px;background:rgba(6,35,26,.1)
        <div> | font-size:10.5px;letter-spacing:.14em;opacity:.72;margin-bottom:8px
          « RACHEL, À L’INSTANT »
        <div> | font-size:15px;line-height:1.5
          « merci ♥ »
        <div> | display:flex;align-items:center;gap:11px;padding:14px 4px 0;color:#06231A
          <svg> viewBox="0 0 24 24" w=17 h=17 stroke-width=1.8
            <path>
          <span> | font-size:14px;opacity:.55
            « répondre… »
        <div> | height:1.2px;background:rgba(6,35,26,.2);margin-top:10px
      <div> | display:flex;gap:7px;margin-top:12px
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(6,35,26,.26)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « note »
        <div> | display:inline-flex;align-items:center;gap:7px;padding:11px 15px;border-radius:999px;font-size:12.5px;white-space:nowrap;box-shadow:inset 0 0 0 1.3px rgba(6,35,26,.26)
          <svg> viewBox="0 0 24 24" w=15 h=15 stroke-width=1.8
            <path>
          « 1 »
  <div> | flex:0 0 auto;height:62px;padding:0 22px;color:#06231A;display:flex;align-items:center;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(6,35,26,.24)
    <span> | font-family:Bricolage,system-ui,sans-serif;font-size:17px;font-weight:800;letter-spacing:-.035em
      « Peaufiner »
    <div> | display:flex;align-items:center;gap:16px
      <span> | opacity:.5;font-size:12px
        « ▾ »
      <svg> viewBox="0 0 24 24" w=19 h=19 stroke-width=1.8
        <path>
        <path>
        <path>
---

## La flèche de retournement — correction n°1 du moodboard

Elle vit dans la pastille « Je promets ». **Deux arcs tête-bêche avec de vraies
pointes** — un retournement, pas un trait continu.

```html
<svg viewBox="0 0 22 22" width="17" height="17" style="flex:none">
  <path d="M3 8h16"                stroke-width="2.2" stroke-linecap="round"/>
  <path d="M15.4 4.6 L19 8 L15.4 11.4" fill="none" stroke-width="2.2"
        stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M19 15H3"               stroke-width="2.2" stroke-linecap="round"/>
  <path d="M6.6 11.6 L3 15 L6.6 18.4"  fill="none" stroke-width="2.2"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

La couleur du trait suit le texte de la pastille : `#06231A` sur menthe.

---

## Le panneau du geste — les trois cercles

```html
<svg viewBox="0 0 308 118" style="width:100%;height:100%;display:block">
  <circle cx="42"  cy="52" r="18" fill="#fff"/>
  <circle cx="266" cy="52" r="18" fill="none" stroke="#fff"
          stroke-width="2.2" opacity=".45"/>
  <circle cx="266" cy="52" r="6"  fill="#fff" opacity=".45"/>
</svg>
```

**Panneau : `height:118px` · `border-radius:26px` · `overflow:hidden`**
fond `rgba(255,255,255,.12)` sur la page + · `rgba(255,255,255,.14)` sur la fiche

---

## Le tracé de la fiche tenue — ph-8

Quand le Promi est tenu, **le panneau du geste disparaît** et ce tracé le
remplace, **en haut du corps** :

```html
<div style="text-align:center;margin-bottom:24px">
  <svg viewBox="0 0 300 62" style="width:82%;height:62px">
    <path d="M20,44 C56,10 96,52 138,28 C176,6 220,46 278,20"
          fill="none" stroke="#06231A" stroke-width="4.6" stroke-linecap="round"/>
  </svg>
</div>
```
