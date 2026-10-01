# LA PLANCHE DES TROIS PARTIS — écran qui vend (Tom, 12 sept.)
# Règle que je me donne : CHAQUE BLOC EST UN MORCEAU RÉEL DU PRODUIT, découpé dans une capture.
#   · le prix / « Prendre l'année » / l'essai / les notes : UNE SEULE bande découpée dans l'écran d'aujourd'hui
#     (css 276 → 600) — donc inchangés par construction, je ne les retype pas.
#   · les traits : les deux vraies ondes d'une fiche de Chiche (mode 'points' et mode 'duo')
#   · les quatre réglages : le vrai mur flouté de Peaufiner, ses quatre rangées, sans son encart
#   · les trois mondes : la vraie rangée de dalles de l'écran d'aujourd'hui, noms compris
# Seuls les MOTS d'étiquette sont posés — et ce sont ceux de l'app : « En gratuit » / « Avec le Cercle »
# (badges de l'aide de l'Aura), « ce que je tiens » / « ce qu'on me tient » (légende des anneaux).
import io, json, os
from PIL import Image
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(D, 'partis')
FOLD = 844
# ── 1 · les découpes dans l'écran réel (DPR 2 : css × 2)
DEC = {'prix': (276, 600), 'dalles': (132, 258)}
fonds = {}
for th in ('dark', 'light'):
    im = Image.open(os.path.join(P, '%s_vend_actuel.png' % th)).convert('RGB')
    fonds[th] = '#%02X%02X%02X' % im.getpixel((4, 4))
    for nom, (y0, y1) in DEC.items():
        c = im.crop((0, y0 * 2, im.width, y1 * 2)); c.save(os.path.join(P, '%s_bloc_%s.png' % (th, nom)))
        print('%-6s %-7s css %d→%d  →  %dx%d px' % (th, nom, y0, y1, c.width, c.height))
print('fonds :', fonds)
# ── 2 · les hauteurs css réelles de chaque pièce (lues sur les fichiers, pas devinées)
def css(f):
    im = Image.open(os.path.join(P, f)); return im.width / 2.0, im.height / 2.0
H = {k: css(k + '.png') for k in
     ['dark_bande_gratuit','dark_bande_cercle','dark_mur_rangees','dark_anneaux_encours','dark_bloc_prix','dark_bloc_dalles']}
for k, v in H.items(): print('  %-26s %.0f x %.0f css' % (k, v[0], v[1]))
G, C_, M, A, PR, DA = (H['dark_bande_gratuit'][1], H['dark_bande_cercle'][1], H['dark_mur_rangees'][1],
                       H['dark_anneaux_encours'][1], H['dark_bloc_prix'][1], H['dark_bloc_dalles'][1])
TRIAL = 188   # « Essayer 14 jours » commence à 188 css DANS la bande du prix (css 464 − 276)
# ── 3 · les trois partis : (clé, titre, sous-titre, liste de blocs {y, quoi, …})
def parti_A():
    y = []; t = 118
    y.append({'y': t, 'mot': 'En gratuit'});                t += 18
    y.append({'y': t, 'img': 'bande_gratuit', 'h': G});     t += G + 24
    y.append({'y': t, 'mot': 'Avec le Cercle'});            t += 18
    y.append({'y': t, 'img': 'bande_cercle', 'h': C_});     t += C_ + 20
    prix = t; y.append({'y': t, 'img': 'bloc_prix', 'h': PR}); t += PR + 30
    y.append({'y': t, 'img': 'mur_rangees', 'h': M, 'x': 24, 'w': 342}); t += M + 30
    y.append({'y': t, 'img': 'bloc_dalles', 'h': DA});      t += DA + 40
    return y, prix, t
def parti_B():
    y = []; t = 130
    y.append({'y': t, 'img': 'bande_cercle', 'h': C_});     t += C_ + 8
    y.append({'y': t, 'duo': ('ce que je tiens', 'ce qu’on me tient')}); t += 34
    prix = t; y.append({'y': t, 'img': 'bloc_prix', 'h': PR}); t += PR + 34
    y.append({'y': t, 'img': 'mur_rangees', 'h': M, 'x': 24, 'w': 342}); t += M + 30
    y.append({'y': t, 'img': 'bloc_dalles', 'h': DA});      t += DA + 40
    return y, prix, t
def parti_C():
    y = []; t = 112
    y.append({'y': t, 'mot': 'En gratuit'});                t += 18
    y.append({'y': t, 'img': 'bande_gratuit', 'h': G});     t += G + 22
    y.append({'y': t, 'mot': 'Avec le Cercle'});            t += 18
    y.append({'y': t, 'img': 'bande_cercle', 'h': C_});     t += C_ + 18
    y.append({'y': t, 'img': 'anneaux_encours', 'h': A, 'x': 24, 'w': 342}); t += A + 20
    prix = t; y.append({'y': t, 'img': 'bloc_prix', 'h': PR}); t += PR + 30
    y.append({'y': t, 'img': 'mur_rangees', 'h': M, 'x': 24, 'w': 342}); t += M + 30
    y.append({'y': t, 'img': 'bloc_dalles', 'h': DA});      t += DA + 40
    return y, prix, t
PARTIS = [('A', 'LA PAIRE', 'le même trait, deux fois : une moitié · les deux moitiés', parti_A),
          ('B', 'LE TRAIT SEUL', 'la forme, et les mots de l’Aura sous ses deux moitiés', parti_B),
          ('C', 'L’AURA NOMMÉE', 'la paire, puis les anneaux : les deux côtés d’un lien', parti_C)]
# ── 4 · l'HTML
def panneau(th, blocs, haut):
    s = ['<div class="pan %s" style="height:%dpx;background:%s">' % (th, int(haut), fonds[th])]
    for b in blocs:
        if 'mot' in b:
            s.append('<div class="mot" style="top:%dpx">%s</div>' % (b['y'], b['mot']))
        elif 'duo' in b:
            s.append('<div class="duo" style="top:%dpx"><span>%s</span><span>%s</span></div>' % (b['y'], b['duo'][0], b['duo'][1]))
        else:
            x = b.get('x', 0); w = b.get('w', 390)
            s.append('<img style="top:%dpx;left:%dpx;width:%dpx;height:%dpx" src="%s_%s.png">' % (b['y'], x, w, int(round(b['h'])), th, b['img']))
    if haut > FOLD: s.append('<div class="pli" style="top:%dpx"><i></i><b>le pli — 844</b></div>' % FOLD)
    s.append('</div>')
    return '\n'.join(s)
H_ = []
for cle, titre, sous, fn in PARTIS:
    blocs, prix, haut = fn()
    trial = prix + TRIAL
    H_.append({'parti': cle, 'prix_y': prix, 'essai_y': trial, 'essai_sous_le_pli': trial + 62 > FOLD, 'hauteur': haut})
    page = ['<!doctype html><meta charset="utf-8"><title>parti %s</title>' % cle,
        '<style>body{margin:0;background:#6E6E76;font-family:Bricolage,system-ui,sans-serif;display:flex;gap:30px;padding:30px;align-items:flex-start}',
        '.pan{position:relative;width:390px;overflow:hidden;border-radius:22px}',
        '.pan img{position:absolute;display:block}',
        '.mot{position:absolute;left:24px;font-family:ApfelMid,system-ui,sans-serif;font-weight:500;font-size:13px;letter-spacing:.02em}',
        '.pan.dark .mot,.pan.dark .duo{color:rgba(244,238,225,.66)} .pan.light .mot,.pan.light .duo{color:rgba(22,23,27,.62)}',
        '.duo{position:absolute;left:24px;width:342px;display:flex;justify-content:space-between;font-family:ApfelMid,system-ui,sans-serif;font-weight:500;font-size:13px}',
        '.pli{position:absolute;left:0;width:390px} .pli i{display:block;border-top:1px dashed rgba(255,90,90,.85)}',
        '.pli b{position:absolute;right:6px;top:3px;font-size:10px;letter-spacing:.12em;color:rgba(255,90,90,.95)}',
        '</style>', panneau('dark', blocs, haut), panneau('light', blocs, haut)]
    f = os.path.join(P, 'parti-%s.html' % cle); io.open(f, 'w', encoding='utf-8').write('\n'.join(page))
    print('  écrit', os.path.basename(f), '· hauteur %d · essai à y=%d' % (haut, trial))
# ── 5 · rendu
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 900, 'height': 1000}, device_scale_factor=1).new_page()
    for cle, *_ in PARTIS:
        pg.goto('http://127.0.0.1:8752/sauvegardes/audit-cercle/partis/parti-%s.html' % cle, timeout=60000)
        pg.wait_for_timeout(1400)
        pg.screenshot(path=os.path.join(P, 'PLANCHE-%s.png' % cle), full_page=True)
        print('  rendu PLANCHE-%s.png' % cle)
    br.close()
json.dump(H_, open(os.path.join(P, 'planche.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(H_, ensure_ascii=False))
