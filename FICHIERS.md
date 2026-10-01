# Les fichiers du dossier local

---

## À la racine

| Fichier | Rôle | État |
|---|---|---|
| **`CLAUDE.md`** | Les règles permanentes, relues à chaque session | ✅ livré |
| **`PROMI-PRESENTATION.md`** | Ce qu'est Promi, pour qui n'en a jamais entendu parler | ✅ livré |
| **`ETAT-DES-LIEUX.md`** | Où on en est, sans complaisance | ✅ livré |
| **`DECISIONS.md`** | Tous les arbitrages, les pièges, les questions ouvertes | ✅ livré |
| **`PARCOURS.md`** | La spécification des écrans — **fait référence** | ✅ livré |
| **`VERIFIER.md`** | Comment vérifier sans lire le code | ✅ livré |
| **`DEMARRAGE.md`** | **À lire en premier** — installation pas à pas | ✅ livré |
| **`LOT-ZERO.md`** | Le test de la chaîne, sans modification | ✅ livré |
| **`PREMIER-LOT.md`** | Le premier vrai lot | ✅ livré |
| **`LOTS-SUIVANTS.md`** | Les six lots d'après, dans l'ordre | ✅ livré |
| **`verifier-installation.py`** | Contrôle que tout est en place | ✅ livré |
| **`FICHIERS.md`** | Ce document | ✅ livré |
| **`DESIGN-MESURE.md`** | Le design en valeurs mesurées — **un contrat** | ✅ livré |
| **`releve-design.py`** | Le script qui vérifie que le design n'a pas bougé | ✅ livré |
| **`design-reference.json`** | La référence figée sur la v592 | ✅ livré |

## Le prototype

| Fichier | Rôle | État |
|---|---|---|
| **`promi-v592.html`** | Le prototype — maquette vivante et spécification | ✅ à jour |

**Renommez-le `app.html`** dans le dossier de travail : c'est le nom qu'attendent
les scripts de test.

## Les batteries de tests

| Fichier | Contrôles |
|---|---|
| `redteam_ecrans.py` | 142 — la principale |
| `redteam.py` | 15 |
| `redteam2.py` | 10 |
| `redteam3.py` | 18 |
| `redteam_demande.py` | 19 |
| `redteam_toile.py` | 16 |
| `redteam_geste.py` | 13 |

✅ **Les sept fichiers sont livrés avec ce transfert.** Ce sont 233 contrôles
accumulés au fil des versions — ils ne se régénèrent pas, gardez-les.

Ils attendent un fichier nommé **`app.html`** dans le même dossier.

## Le moodboard

| Fichier | Rôle | État |
|---|---|---|
| `MOODBOARD-parcours.html` | Le moodboard visuel | 📎 conservez-le comme référence visuelle, mais **c'est `PARCOURS.md` qui fait foi** |

## Le contrôle du design

```bash
python3 releve-design.py            # après chaque lot
python3 releve-design.py --figer    # après un lot que TU as validé
```

Il relève **148 propriétés sur 26 éléments dans 6 configurations** et les compare
à `design-reference.json`.

```
✅  AUCUN ÉCART. Le design est intact.
❌  N ÉCARTS avec la référence
❌  N COULEURS FAUTIVES
```

**C'est ton garde-fou principal.** Exige sa sortie à chaque livraison.

---

## Les prérequis techniques

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
node --version    # pour la vérification de syntaxe
```
