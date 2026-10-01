#!/usr/bin/env python3
"""
redteam_apercus.py — UN APERÇU DE TOILE PORTE TOUJOURS DE LA MATIÈRE COLORÉE.

⚑ Né du lot v25 (Tom, 22 sept. 2026) : *« C'est le troisième lot où un écran sort vide sans
que rien ne rougisse. »* Le fond du Studio était devenu beige uni depuis le lot v17 — six
lots, et aucune batterie ne l'a vu, parce qu'elles mesurent des COTES, des MOTS et des
CONTRASTES, jamais « est-ce qu'il y a encore de la matière ».

LA RÈGLE QU'IL PORTE, ET ELLE EST ÉCRITE EN DUR (§7) :
  Le Studio montre le MONDE : sa Toile d'aperçu doit porter de la matière colorée, dans les
  deux thèmes, quel que soit le monde. L'app pose `_shAllColored` pour cela (Q132 : « sinon
  ~12 dalles dans un coin »).

POURQUOI LE DÉFAUT EXISTAIT, ET POURQUOI IL ÉTAIT INVISIBLE AUX JUGES :
  L'exception Ingénu (v17) fait dire la NATURE à la couleur — `cOf` lit `s.nat`, et une
  cellule sans nature prend le crème dalle. C'est juste pour la vraie Toile (« une cellule
  colorée qui ne porte aucune parole »). Mais un APERÇU n'a aucune parole : toutes ses
  cellules tombaient sur le crème. Le canevas était PEINT — un contrôle qui compte les pixels
  non transparents voyait 13 167 pixels et concluait « ça marche ». **On ne compte donc pas
  ce qui est peint : on compte ce qui est COLORÉ**, et on le compare à un plancher décidé.

CE QU'ON COMPTE, ET POURQUOI PAS AUTREMENT :
  la part de pixels qui portent une couleur FRANCHE ET FROIDE — saturation ≥ 0,22 et teinte
  hors de la bande chaude 18°-72°. ⚠ Un simple « max−min > 40 » ne suffit pas : les crèmes
  et les sables du mode clair le passent, et le juge déclarait VERT un Studio visiblement
  mort (37,6 % sur la version cassée). Avec la teinte, la version cassée tombe à **3,6 %**
  dans les deux thèmes et sur les cinq mondes — le défaut n'a plus où se cacher.
  ⚠ On mesure la ZONE DE TOILE (sous le plateau, au-dessus du panneau), jamais l'écran
  entier : le panneau porte ses quatre pastilles de palette, qui sont colorées même quand
  la Toile est morte — c'est exactement ce qui rendait le défaut crédible à l'œil.

Usage :  python3 redteam_apercus.py
"""
import colorsys, io, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image

URL = os.environ.get("APP_APERCUS", "http://127.0.0.1:8752/app.html")
# ⚑ UN PLANCHER PAR MONDE, ET IL EST RELEVÉ SUR LA RÉFÉRENCE, PAS CHOISI.
#   Un monde ne couvre pas la même part de l'écran : Braille pose des points, Touffe des
#   brins — ils sont NORMALEMENT plus clairsemés qu'Encre ou Pixel. Un plancher unique
#   déclarait donc faux ce qui était juste. On lit la valeur rendue par la version d'avant
#   le lot v17 (`sauvegardes/app-avant-lot-v17.html`, les deux thèmes), et on place le
#   plancher assez bas pour la respiration du monde, assez haut pour prendre l'effondrement :
#
#     monde      référence v17   version cassée   plancher
#     encre        45,4 · 43,5      3,6 ·  3,6       30
#     mosaique     46,1 · 42,5      3,6 ·  3,6       30
#     touffe       15,0 · 16,1      5,5 ·  5,5       10
#     braille      24,3 · 19,3      3,6 ·  3,6       14
#     pixel        65,4 · 65,1      3,6 ·  3,6       45
MONDES = {'encre': 30.0, 'mosaique': 30.0, 'touffe': 10.0, 'braille': 14.0, 'pixel': 45.0}
PLANCHER = MONDES['encre']          # le Studio s'ouvre sur Encre
TMP = "/tmp/_apercus"

ok_n = ko_n = 0


def ok(t):
    global ok_n; ok_n += 1; print("  ✅ %s" % t)


def ko(t, d=""):
    global ko_n; ko_n += 1; print("  ❌ %s%s" % (t, (" — " + d) if d else ""))


def colore(chemin, y0=0.20, y1=0.78):
    """part de pixels de couleur franche ET FROIDE dans la bande donnée — voir l'en-tête"""
    im = Image.open(chemin).convert("RGB")
    w, h = im.size
    im = im.crop((0, int(h * y0), w, int(h * y1)))
    px = list(im.getdata())
    n = 0
    for r, g, b in px:
        mx, mn = max(r, g, b), min(r, g, b)
        if mx == 0 or (mx - mn) / mx < 0.22:
            continue
        teinte = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[0] * 360
        if 18 <= teinte <= 72:          # crèmes, beiges, sables : ce n'est pas une dalle
            continue
        n += 1
    return 100.0 * n / len(px)


def main():
    os.makedirs(TMP, exist_ok=True)
    with sync_playwright() as P:
        b = P.chromium.launch()
        ctx = b.new_context(viewport={"width": 430, "height": 932}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

        for th in ("dark", "light"):
            pg.evaluate("(t)=>{if(window.setTheme)setTheme(t)}", th); pg.wait_for_timeout(700)
            pg.evaluate("()=>{ if(window.closeAll) closeAll(); }"); pg.wait_for_timeout(500)
            pg.evaluate("()=>{var x=document.getElementById('studioBtn'); if(x) x.click();}")
            pg.wait_for_timeout(2600)

            # A · la Toile du Studio porte de la matière colorée
            f = os.path.join(TMP, "studio-%s.png" % th)
            pg.locator("#device").screenshot(path=f)
            c = colore(f)
            nom = "A le fond du Studio porte de la matière colorée [%s]" % th
            if c < PLANCHER:
                ko(nom, "%.1f %% de pixels colorés, plancher %.0f %%" % (c, PLANCHER))
            else:
                ok(nom + "  (%.1f %%)" % c)

            # B · les graines de l'aperçu SE DÉCLARENT (§8 : on lit ce que l'app publie)
            d = pg.evaluate("""()=>{const bg=document.getElementById('stBg'); const c=bg&&bg.__c;
              if(!c||!c.seeds) return null;
              let ap=0, ci=0; const h={};
              for(const s of c.seeds){ if(s.apercu) ap++; if(s.ci!=null){ci++; h[s.ci]=(h[s.ci]||0)+1;} }
              return {n:c.seeds.length, apercu:ap, colorees:ci, tons:Object.keys(h).length};}""")
            nom = "B les graines de l'aperçu se déclarent [%s]" % th
            if not d:
                ko(nom, "aucune graine publiée sur #stBg.__c")
            elif d['apercu'] != d['n']:
                ko(nom, "%d graines sur %d portent `apercu` — le drapeau se perd à la recopie" % (d['apercu'], d['n']))
            elif d['colorees'] != d['n']:
                ko(nom, "%d graines colorées sur %d (_shAllColored, Q132)" % (d['colorees'], d['n']))
            elif d['tons'] < 3:
                ko(nom, "un seul ton sur %d graines : la rotation de la palette est perdue" % d['n'])
            else:
                ok(nom + "  (%d graines, %d tons)" % (d['n'], d['tons']))

            # C · chaque monde gratuit porte sa matière
            # ⚠ CETTE PASSE REPEINT `#stBg` : elle défait ce qu'elle a fait (§7) en
            #   rouvrant le Studio à la fin, sinon le thème suivant mesure la Toile
            #   que la sonde vient de poser, et non celle que l'app compose.
            manque = []
            for m in MONDES:
                pose = pg.evaluate("""(m)=>{ try{ const t=window.Toile;
                  const bg=document.getElementById('stBg');
                  if(!t||!t.preview||!bg) return false;
                  const av=window._shAllColored; window._shAllColored=true;
                  t.preview(bg, m, 390, 844);
                  window._shAllColored=av; return true; }catch(e){ return String(e); } }""", m)
                if pose is not True:
                    manque.append("%s (%s)" % (m, pose)); continue
                pg.wait_for_timeout(500)
                f = os.path.join(TMP, "monde-%s-%s.png" % (m, th))
                pg.locator("#device").screenshot(path=f)
                cm = colore(f)
                if cm < MONDES[m]:
                    manque.append("%s %.1f %% (plancher %.0f)" % (m, cm, MONDES[m]))
            nom = "C les cinq mondes gratuits portent leur matière [%s]" % th
            if manque:
                ko(nom, " · ".join(manque))
            else:
                ok(nom)
            # on rend l'écran tel qu'on l'a trouvé
            pg.evaluate("()=>{ if(window.closeAll) closeAll(); }"); pg.wait_for_timeout(400)

            # D · LA DEUXIÈME OUVERTURE VAUT LA PREMIÈRE
            # ⚠ `buildStudio` peint `#stBg` lui-même, sans `_shAllColored` ; le semis juste
            #   était accroché à l'observateur de `.show`, et `#studioScreen` NE PERD JAMAIS
            #   cette classe (comme `#auraScreen`). Dès la deuxième ouverture, l'app rendait
            #   14 cellules colorées sur 72 — « ~12 dalles dans un coin », le défaut de Q132.
            pg.evaluate("()=>{var x=document.getElementById('studioBtn'); if(x) x.click();}")
            pg.wait_for_timeout(2600)
            d2 = pg.evaluate("""()=>{const bg=document.getElementById('stBg'); const c=bg&&bg.__c;
              if(!c||!c.seeds) return null; let ci=0;
              for(const s of c.seeds) if(s.ci!=null) ci++;
              return {n:c.seeds.length, colorees:ci};}""")
            f2 = os.path.join(TMP, "studio2-%s.png" % th)
            pg.locator("#device").screenshot(path=f2)
            c2 = colore(f2)
            nom = "D la deuxième ouverture vaut la première [%s]" % th
            if not d2:
                ko(nom, "aucune graine publiée")
            elif d2['colorees'] != d2['n']:
                ko(nom, "%d cellules colorées sur %d — buildStudio a repeint sans _shAllColored"
                   % (d2['colorees'], d2['n']))
            elif c2 < PLANCHER:
                ko(nom, "%.1f %% de pixels colorés, plancher %.0f %%" % (c2, PLANCHER))
            else:
                ok(nom + "  (%d/%d, %.1f %%)" % (d2['colorees'], d2['n'], c2))
            pg.evaluate("()=>{ if(window.closeAll) closeAll(); }"); pg.wait_for_timeout(400)

            # E · LE FOND D'UN APERÇU EST CELUI DE LA VRAIE TOILE
            # ⚑ v26 (Tom) : « sur Braille on dirait qu'il y a un voile sombre ». Les pois n'ont
            #   pas bougé — pas 9 px, rayon 2,9, **34,9 %** de couverture, inchangés depuis le
            #   lot v14. C'est le FOND qui différait : `#120E05` dans l'aperçu contre `#201908`
            #   sur la vraie Toile, 16 niveaux de luminance. Invisible sur Encre ou Pixel, qui
            #   couvrent tout ; flagrant sur Braille et Touffe, dont les deux tiers sont ce fond.
            #   ⚠ TROIS fonctions le peignaient (`preview`, `repaintWorld`, `repaint`) : corriger
            #   l'une ne changeait rien, `repaint` repasse à chaque frémissement (§7).
            f = pg.evaluate("""()=>{ const T=window.Toile;
              if(!T||!T.fondToile) return null;
              return {sombre:T.fondToile(false), clair:T.fondToile(true)}; }""")
            nom = "E le fond d'un aperçu est celui de la vraie Toile [%s]" % th
            if not f:
                ko(nom, "aucun `Toile.fondToile` : le fond est encore écrit à trois endroits")
            elif f['sombre'].upper() != '#201908':
                ko(nom, "fond sombre %s au lieu de #201908 (celui du mode)" % f['sombre'])
            else:
                ok(nom + "  (sombre %s · clair %s)" % (f['sombre'], f['clair']))

        b.close()

    print("\n%s  %d/%d" % ("✅" if ko_n == 0 else "❌", ok_n, ok_n + ko_n))
    return ko_n


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
