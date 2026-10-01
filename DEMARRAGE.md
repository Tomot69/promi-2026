# Démarrage — pas à pas

> Pour quelqu'un qui n'a jamais utilisé Claude Code.
> **Faites les étapes dans l'ordre. Ne sautez rien.**

---

## Étape 1 · Ranger les fichiers

Dans votre dossier `Promi 2026`, vous devez avoir **tous ces fichiers, à plat** —
pas dans des sous-dossiers, pas dans un zip.

```
Promi 2026/
│
├── app.html                    ← le prototype (renommé !)
│
├── CLAUDE.md                   ← les règles
├── PROMI-PRESENTATION.md
├── ETAT-DES-LIEUX.md
├── DECISIONS.md
├── PARCOURS.md
├── DESIGN-MESURE.md
├── VERIFIER.md
├── FICHIERS.md
├── DEMARRAGE.md                ← ce document
├── LOT-ZERO.md
├── PREMIER-LOT.md
│
├── verifier-installation.py
├── releve-design.py
├── design-reference.json
│
├── redteam_ecrans.py
├── redteam.py
├── redteam2.py
├── redteam3.py
├── redteam_demande.py
├── redteam_toile.py
├── redteam_geste.py
│
└── MOODBOARD-parcours.html     ← référence visuelle
```

### ⚠ Le point le plus important

Le fichier du prototype s'appelle `promi-v592.html`.
**Il doit s'appeler `app.html`** — c'est le nom qu'attendent tous les scripts.

Renommez-le dans le Finder, ou tapez dans le Terminal :

```bash
cd ~/Documents/"IA projetcs"/Promi/"Promi App"/"Promi 2026"
mv promi-v592.html app.html
```

---

## Étape 2 · Ouvrir le Terminal au bon endroit

**Le plus simple :** dans le Finder, clic droit sur le dossier `Promi 2026` →
**Services** → **Nouveau terminal au dossier**.

Sinon, ouvrez le Terminal et tapez :

```bash
cd ~/Documents/"IA projetcs"/Promi/"Promi App"/"Promi 2026"
```

**Pour vérifier que vous êtes au bon endroit**, tapez `ls` : vous devez voir la
liste des fichiers ci-dessus.

---

## Étape 3 · Vérifier que tout est en place

Tapez :

```bash
python3 verifier-installation.py
```

### Si vous voyez

```
TOUT EST EN PLACE.
```

Passez à l'étape 4.

### Si vous voyez des ✗

Le script vous dit **exactement quoi faire**. Les cas les plus courants :

**Playwright absent** → tapez ces deux lignes, l'une après l'autre :
```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```
*(La seconde télécharge un navigateur, comptez quelques minutes.)*

**Node absent** → allez sur [nodejs.org](https://nodejs.org), téléchargez la
version **LTS**, installez-la, fermez et rouvrez le Terminal.

**app.html manquant** → voir l'étape 1.

Puis **relancez** `python3 verifier-installation.py` jusqu'à obtenir
`TOUT EST EN PLACE`.

---

## Étape 4 · Le lot zéro — tester la chaîne

**Ce lot ne modifie rien.** Il sert uniquement à vérifier que Claude Code sait
lire les documents et lancer les tests.

Ouvrez `LOT-ZERO.md`, copiez **tout le contenu**, et collez-le dans Claude Code.

### Ce que vous devez recevoir

1. Un résumé du projet en trois phrases
2. Les sept scores de tests
3. Le résultat de `releve-design.py`
4. **Aucune modification du fichier**

### Si Claude Code modifie quelque chose

**Arrêtez-le.** Dites :

> « Le lot zéro ne modifie rien. Annule et recommence en ne faisant que lire. »

---

## Étape 5 · Le premier vrai lot

Seulement quand le lot zéro s'est bien passé.

Ouvrez `PREMIER-LOT.md`, copiez tout, collez dans Claude Code.

---

## Les trois phrases à retenir

Quand vous ne savez pas quoi dire à Claude Code :

> **« Relance `releve-design.py` et montre-moi la sortie. »**
> Pour vérifier que le design n'a pas bougé.

> **« Donne-moi la cause, pas une nouvelle règle par-dessus. »**
> Quand quelque chose est cassé.

> **« Arrête. Reviens à la version précédente et dis-moi ce qui bloque. »**
> Quand ça patine depuis deux tentatives.

---

## Comment sauvegarder avant chaque lot

**Avant chaque lot**, faites une copie du prototype :

```bash
cp app.html sauvegardes/app-$(date +%H%M).html
```

*(Créez d'abord le dossier : `mkdir sauvegardes`)*

Si un lot casse tout, vous revenez à la copie :

```bash
cp sauvegardes/app-1430.html app.html
```

**C'est votre filet de sécurité.** Ne travaillez jamais sans.
