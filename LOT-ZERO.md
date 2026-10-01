# Lot zéro — à coller dans Claude Code

> Ce lot **ne modifie rien**. Il vérifie que la chaîne fonctionne.
> Copiez tout ce qui suit la ligne.

---

Bonjour. Tu reprends le développement de **Promi**, une application mobile
française prototypée dans un fichier HTML unique nommé `app.html`.

**Ce premier échange est un test de la chaîne. Tu ne modifies aucun fichier.**

---

## 1 · Lis les documents

Dans cet ordre :

1. `CLAUDE.md` — les règles permanentes, elles font autorité
2. `PROMI-PRESENTATION.md` — ce qu'est le projet
3. `ETAT-DES-LIEUX.md` — où on en est, y compris ce qui est cassé
4. `DECISIONS.md` — les arbitrages déjà pris
5. `PARCOURS.md` — la spécification des écrans
6. `DESIGN-MESURE.md` — le design en valeurs mesurées

## 2 · Prouve-moi que tu as compris

Réponds en français, en trois phrases courtes :

- **Ce qu'est Promi**, et ce qu'il n'est pas
- **La règle des trois tons**
- **Pourquoi il ne faut pas nettoyer le CSS**

Puis, en une phrase chacun, cite **trois interdits** de `CLAUDE.md`.

## 3 · Lance les tests

```bash
python3 redteam_ecrans.py
python3 redteam.py
python3 redteam2.py
python3 redteam3.py
python3 redteam_demande.py
python3 redteam_toile.py
python3 redteam_geste.py
```

Donne-moi les sept scores dans un tableau, avec le score attendu à côté :

| Batterie | Obtenu | Attendu |
|---|---|---|
| redteam_ecrans | ? | 142/142 |
| redteam | ? | 15/15 |
| redteam2 | ? | 10/10 |
| redteam3 | ? | 18/18 |
| redteam_demande | ? | 19/19 |
| redteam_toile | ? | 16/16 |
| redteam_geste | ? | 13/13 |

## 4 · Lance le contrôle du design

```bash
python3 releve-design.py
```

Colle-moi la sortie **telle quelle**.

Elle doit afficher `✅ AUCUN ÉCART. Le design est intact.`

## 5 · Fais-moi une capture

Sans rien modifier, ouvre `app.html` dans un navigateur headless et capture
**la fiche d'un Promi à tenir**, en mode clair, au format 390 × 844.

Voici comment :

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    pg.goto('file:///CHEMIN/ABSOLU/VERS/app.html')
    pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                "if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.querySelectorAll('.frame,.device')"
                ".forEach(e=>e.classList.add('light'))")
    pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();}")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const x=document.querySelector('#indexSheet .ix-bloc.vif');"
                "if(x)x.click();}")
    pg.wait_for_timeout(2600)
    pg.screenshot(path='temoin.png')
    b.close()
```

## 6 · Dis-moi ce qui te paraît risqué

Après avoir tout lu : y a-t-il quelque chose dans ces documents qui te semble
contradictoire, ambigu ou impossible à tenir ? Dis-le maintenant.

---

**Rappel : tu ne modifies aucun fichier dans ce lot.**
Si tu as besoin d'écrire quelque chose, demande-moi d'abord.
