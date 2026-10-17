#!/usr/bin/env python3
"""
redteam_onboarding_texte.py — L'ONBOARDING : SES DALLES ET SES TEXTES (v146, Tom, 14 oct. 2026 — C-123, C-124, C-126).
Le parcours entier au doigt (CDP), stockage vierge, 390 × 844, en CLAIR puis en SOMBRE. LA DÉCISION, EN DUR :
  11.1  « Prénom, donc. » et « Petite ou grande promesse, elle compte. » : entre 75 et 85 % de la taille de la phrase de promesse (qui reste à 35 px) ;
        en clair #291547 ; en sombre, la couleur d'aujourd'hui (la crème) ;
  11.2  le message de fin plus gros (titre ≥ 40 px, phrase de ton ≥ 19 px, lignes ≥ 16,5 px — 35, 16, 16 avant), en clair #291547 ; Promi, Chiche et Cercle
        gardent leur couleur (celle de `natCol`, inchangée) ;
  11.3  les mots de Tom ne changent pas (hors 11.4) : le texte entier, espaces ramenés, est celui d'avant avec le seul titre changé ; des lignes courtes ;
        les mots-clés (Primo, Deuxio, Tertio, La suite t'appartient.) en PromiLate ; « Deuxio » penché de 3° (v129) ;
  11.4  « Promi planté ! » (espace insécable) ; « Promi » en PromiLate, #0E78F2 en clair ; dessous la phrase de ton ; RIEN d'autre avant le toucher ; au
        toucher, le reste paraît ;
  11.5  le bloc remonte d'au moins 60 pt (150 avant), il passe au-dessus des dalles : sur l'image, une bande de 12 pt sous le bloc ne porte que le fond ;
  —     aucun contour ni ombre sur aucune lettre ;
  C-123 à « Promi planté ! », les voisines NAISSENT une à une (relevé du moteur image par image : chacune à son heure, ≥ 100 ms d'écart, chacune pousse
        sur plusieurs images) ; la Toile d'avant se retire sans saut (sur l'image : aucune image ne change plus de 40 % de l'écran) ;
  C-126 la page du premier trait, en clair : « trace pour planter » en #00341A ; le départ de la flèche en orange (des pixels #FB4C0D au départ du trait).
Preuve (§7) : `--fichier=zz-avant-v146.html` — il rougit (11.1, 11.4, 11.5, C-126).
⚑ v148 (Tom, C-124 §8 et §9) — remis au niveau des décisions : le texte à 25 pt (−7 %) ; « Promi planté ! » SEUL au départ, plus bas ; un toucher par
paragraphe (trois), le bloc remonte à chaque pas ; à la fin son haut ≤ 90 et 12 pt de fond sous lui. Original : sauvegardes/redteam_onboarding_texte-avant-v148.py.
"""
import io, sys, re
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []").replace("def juge(", "def _j("))
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')   # après l'emprunt : il réécrit F
URL = 'http://127.0.0.1:8752/' + F
VIOLET, BLEU, CREME = (41, 21, 71), (14, 120, 242), (247, 240, 222)
AVANT_FIN = 'C’est planté.Ton premier Promi, ta première dalle sur ta Toile. Plus qu’à le tenir.Primo, un Promi, c’est ta parole donnée. Deuxio, un Chiche, c’est un coup de culot. Tertio, un Cercle, c’est tout cela à la fois, mais à plusieurs.Le reste se découvre en traçant. La suite t’appartient.'
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-110s %s' % ('✅' if c else '❌', nom, str(d)[:230]), flush=True)
def rgb(s): m = re.findall(r'[\d.]+', s or ''); return tuple(int(float(x)) for x in m[:3]) if len(m) >= 3 else None
def pres(a, b, t=24): return a is not None and sum(abs(a[i] - b[i]) for i in range(3)) <= t
ST = """(ids)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, o={}; ids.forEach(i=>{ const e=document.getElementById(i); if(!e) return; const c=getComputedStyle(e); if(c.display==='none') return; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect();
  o[i]={fs:parseFloat(c.fontSize), col:c.color, f:c.fontFamily.split(',')[0].replace(/["']/g,'').trim(), b:[(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k]}; }); return o; }"""
CONT = """()=>[...document.querySelectorAll('#onbV, #onbV *')].filter(e=>{ const c=getComputedStyle(e); return (c.textShadow&&c.textShadow!=='none') || (parseFloat(c.webkitTextStrokeWidth)||0)>0; }).map(e=>e.id||e.className).slice(0,4)"""
FIN = """()=>{ const f=document.getElementById('onbFin'); if(!f) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const q=s=>f.querySelector(s); const C=e=>e?getComputedStyle(e):null;
  const vis=e=>{ if(!e) return false; let v=e; while(v&&v!==f.parentElement){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden') return false; v=v.parentElement; } return true; };
  const t=q('.onbv-titre'), pm=q('.onbv-pmot'), to=q('.onbv-ton'), L=[...f.querySelectorAll('.onbv-l')], K=[...f.querySelectorAll('.onbv-k')], N=[...f.querySelectorAll('.onbv-nat')], r=f.getBoundingClientRect();
  const dx=f.querySelector('.onbv-deux');
  return {texte:(f.textContent||'').replace(/\\u00a0/g,'\\u00a0'), titre:t?t.textContent:null, titreFs:t?parseFloat(C(t).fontSize):0, titreCol:t?C(t).color:null, pm:pm?{f:C(pm).fontFamily.split(',')[0].replace(/["']/g,'').trim(), col:C(pm).color}:null,
    tonFs:to?parseFloat(C(to).fontSize):0, tonCol:to?C(to).color:null, tonVu:vis(to), lignes:L.map(l=>({fs:parseFloat(C(l).fontSize), col:C(l).color, vu:vis(l), t:l.textContent})), cles:K.map(x=>({t:x.textContent, f:C(x).fontFamily.split(',')[0].replace(/["']/g,'').trim()})),
    nats:N.map(x=>({t:x.textContent, col:C(x).color})), deux:dx?C(dx).transform:null, haut:(r.top-D.top)/k, bas:(r.bottom-D.top)/k}; }"""
def image(pg): return Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
def matiere_bas(im, d, fond):
    """la part du bas de l'écran (y 420 → 800) qui porte des cellules : ce qui n'est pas le fond de la Toile, hors de la dalle bleue de la parole"""
    px = im.load(); n = t = 0
    for y in range(420, 800, 4):
        for x in range(10, 380, 4):
            c = px[int(d[0] + x * d[2]), int(d[1] + y * d[2])]; t += 1
            if c[2] > c[0] + 40: continue
            if sum(abs(c[i] - fond[i]) for i in range(3)) > 14: n += 1
    return n / float(t)
def diff(a, b):
    A, Bb = a.resize((130, 281)).load(), b.resize((130, 281)).load(); n = 0
    for y in range(281):
        for x in range(130):
            if sum(abs(A[x, y][i] - Bb[x, y][i]) for i in range(3)) > 30: n += 1
    return n / (130.0 * 281)
def parcours(b, th):
    T = 'clair' if th == 'light' else 'sombre'; print('\n── %s' % T)
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, color_scheme='dark' if th == 'dark' else 'light')
    if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); parole(pg); s = pg.evaluate(ST, ['onbDit', 'onbPh', 'onbSous']); ph = s.get('onbPh', {}).get('fs', 0)
    for i, nom in (('onbDit', '« Prénom, donc. »'), ('onbSous', '« Petite ou grande promesse… »')):
        e = s.get(i); r = e['fs'] / ph if e and ph else 0
        # ⚑ v148 (Tom, C-124 §8) — CONTRAT RÉÉCRIT : « les textes Atkinson de la page du premier Promi réduits de 6 à 8 % » : 25 pt (27 en v147, 75–85 % de la
        #   phrase en v146) ; la phrase de promesse reste à 35. Original : sauvegardes/redteam_onboarding_texte-avant-v148.py
        juge('[%s] 11.1 · %s : 25 pt (v148 : −7 %%, %.0f %% de la phrase), la phrase reste à 35 px' % (T, nom, r * 100), e and abs(e['fs'] - 25) <= 0.2 and ph == 35, '%s px / %s px' % (e and e['fs'], ph))
        juge('[%s] 11.1 · %s : %s' % (T, nom, 'en violet #291547' if th == 'light' else 'la crème d\'aujourd\'hui'), e and pres(rgb(e['col']), VIOLET if th == 'light' else CREME), e and e['col'])
    if s.get('onbDit') and s.get('onbPh'):
        bd = s['onbDit']['b']; juge('[%s] 11.1 · « Prénom, donc. » ne touche pas la phrase (au moins 8 pt d\'air)' % T, bd[1] + bd[3] + 8 <= s['onbPh']['b'][1], 'bas %.0f · phrase à %.0f' % (bd[1] + bd[3], s['onbPh']['b'][1]))
    saisie(pg); tr = pg.evaluate(ST, ['onbTrace']).get('onbTrace')
    if th == 'light':
        juge('[clair] C-126 · « trace pour planter » (PromiLate) en vert foncé #00341A', tr and tr['f'] == 'PromiLate' and pres(rgb(tr['col']), (0, 52, 26)), tr and tr['col'])
        im = image(pg); d = dev(pg); z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); const r=c.getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}"); px = im.load(); n = 0
        for y in range(int(z[1]), int(z[1] + z[3]), 2):
            for x in range(int(z[0]), int(z[0] + z[2] * 0.3), 2):
                c = px[x, y]
                if abs(c[0] - 251) + abs(c[1] - 76) + abs(c[2] - 13) < 60: n += 1
        juge('[clair] C-126 · le départ de la flèche est orange #FB4C0D (lu sur l\'image, au départ du trait)', n >= 6, '%d pixels orange' % n)
    pg.evaluate("()=>{ window.__vo=[]; const t0=performance.now(); (function f(){ try{ if(window.Toile&&Toile.voisinesEtat) window.__vo.push([Math.round(performance.now()-t0), Toile.voisinesEtat()]); }catch(e){} if(performance.now()-t0<6000) requestAnimationFrame(f); })(); }")
    trace(pg, cdp); d = dev(pg); ims = []
    for i in range(30): ims.append(image(pg)); pg.wait_for_timeout(110)
    fond = (223, 202, 164) if th == 'light' else (5, 3, 2)
    m = [matiere_bas(im, d, fond) for im in ims]; dmax = max(diff(a, b_) for a, b_ in zip(ims, ims[1:]))
    k0 = min(range(len(m)), key=lambda i: m[i])   # le creux : la Toile d'avant est partie, les voisines commencent à naître
    fin_ = max(m[k0:]); pal = [v for a, v in zip(m[k0:], m[k0 + 1:]) if v - a > 0.004]
    sauts = [b_ - a for a, b_ in zip(m[k0:], m[k0 + 1:])] or [1]
    juge('[%s] C-123 · à « Promi planté ! » : rien n\'arrive d\'un coup — aucune image ne change plus de 40 %% de l\'écran (la Toile d\'avant se retire en flaques)' % T, dmax <= 0.40, 'la plus grande différence entre deux images : %.0f %%' % (dmax * 100))
    VO = pg.evaluate("()=>window.__vo||[]"); nv = max((len(v[1]) for v in VO), default=0); debut = []; duree = []
    for k in range(nv):
        L = [(t, v[k]) for t, v in VO if len(v) > k]; t1 = next((t for t, f in L if f > 0.02), None); t2 = next((t for t, f in L if f >= 0.98), None)
        if t1 is not None: debut.append(t1)
        if t1 is not None and t2 is not None: duree.append(t2 - t1)
    ec = sorted(debut); pas_ = [b_ - a for a, b_ in zip(ec, ec[1:])]
    juge('[%s] C-123 · les voisines naissent une à une : %d voisines, chacune à son heure (≥ 100 ms d\'écart) et chacune pousse sur plusieurs images (≥ 150 ms jusqu\'à sa taille, puis elle dépasse d\'un rien et se pose : 520 ms) — relevé du moteur, image par image' % (T, nv),
         nv >= 4 and len(debut) == nv and min(pas_ or [0]) >= 100 and min(duree or [0]) >= 150, 'naissances à %s ms · poussées de %s ms' % (ec, sorted(duree)[:3]))
    f0 = pg.evaluate(FIN); pg.wait_for_timeout(600); f0 = pg.evaluate(FIN)
    if not f0: juge('[%s] le message de fin existe' % T, False); ctx.close(); return
    juge('[%s] 11.4 · le titre est « Promi planté ! » (espace insécable avant « ! »)' % T, (f0['titre'] or '') == 'Promi planté !' or (f0['titre'] or '') == 'Promi planté !', repr(f0['titre']))
    juge('[%s] 11.4 · « Promi » en PromiLate, %s' % (T, '#0E78F2' if th == 'light' else 'le bleu de la nature'), f0['pm'] and f0['pm']['f'] == 'PromiLate' and (pres(rgb(f0['pm']['col']), BLEU) if th == 'light' else not pres(rgb(f0['pm']['col']), BLEU, 40)), f0['pm'])
    juge('[%s] 11.4 · ⚑ v148 (C-124 §9.1) : avant le toucher, le titre SEUL — ni la phrase de ton, ni aucune ligne' % T, not f0['tonVu'] and not any(l['vu'] for l in f0['lignes']), 'ton %s · %d ligne(s) visibles' % (f0['tonVu'], sum(1 for l in f0['lignes'] if l['vu'])))
    juge('[%s] 11.2 · plus gros : titre ≥ 40 px, phrase de ton ≥ 19 px, lignes ≥ 16,5 px (35 · 16 · 16 avant)' % T, f0['titreFs'] >= 40 * 0.8 - 0.1 and f0['tonFs'] >= 19 and min([l['fs'] for l in f0['lignes']] or [0]) >= 16.5,
         'titre %.1f · ton %.1f · lignes %.1f (échelle du bloc)' % (f0['titreFs'], f0['tonFs'], min([l['fs'] for l in f0['lignes']] or [0])))
    if th == 'light':
        juge('[clair] 11.2 · le texte en violet #291547 (titre, ton, lignes)', pres(rgb(f0['titreCol']), VIOLET) and pres(rgb(f0['tonCol']), VIOLET) and all(pres(rgb(l['col']), VIOLET) for l in f0['lignes']), '%s · %s' % (f0['titreCol'], f0['tonCol']))
    else:
        juge('[sombre] 11.2 · les couleurs d\'aujourd\'hui : la crème', pres(rgb(f0['titreCol']), CREME) and all(pres(rgb(l['col']), CREME) for l in f0['lignes']), f0['titreCol'])
    nat = pg.evaluate("()=>{ const c=document.getElementById('device').classList.contains('light'); const fd=c?[223,202,164]:[5,3,2]; const N={promi:[130,174,248],chiche:[255,184,210],cercle:[201,168,245]}; const o={}; for(const k in N){ let v=N[k]; try{ v=window._teinte.ajuste(v, fd, 5); }catch(e){} o[k]='rgb('+v[0]+', '+v[1]+', '+v[2]+')'; } return o; }")
    juge('[%s] 11.2 · Promi, Chiche, Cercle gardent leur couleur (la teinte de leur nature, comme avant)' % T, f0['nats'] and all(x['col'] == nat.get(x['t'].lower()) for x in f0['nats']), [(x['t'], x['col']) for x in f0['nats']][:4])
    juge('[%s] 11.3 · lignes courtes ; mots-clés en PromiLate (Primo, Deuxio, Tertio, La suite t\'appartient.) ; Deuxio penché' % T, len(f0['lignes']) >= 5 and [c['t'] for c in f0['cles']] == ['Primo,', 'Deuxio,', 'Tertio,', 'La suite t’appartient.'] and all(c['f'] == 'PromiLate' for c in f0['cles']) and f0['deux'] not in (None, 'none'),
         '%d lignes · %s · %s' % (len(f0['lignes']), [c['t'] for c in f0['cles']], f0['deux']))
    nouveau = re.sub(r'\s+', ' ', AVANT_FIN.replace('C’est planté.', 'Promi planté !')).replace('. ', '.').replace(' ', '')
    lu = re.sub(r'\s+', ' ', f0['texte'].replace(' ', ' ')).replace('. ', '.').replace(' ', '')
    juge('[%s] 11.3 · aucun mot de Tom changé hors 11.4 (le texte entier, espaces ramenés)' % T, lu == nouveau, '' if lu == nouveau else 'lu : %s' % f0['texte'][:160])
    juge('[%s] 11.5 · ⚑ v148 (C-124 §9.1) : au départ, le titre seul est PLUS BAS qu\'en v147 (son haut > 90)' % T, f0['haut'] > 90.5, 'haut %.0f' % f0['haut'])
    d = dev(pg); vus = []
    for k_ in range(3):   # ⚑ v148 (C-124 §9.2–9.4) : un toucher, un paragraphe
        toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 120 * d[2])
        for _ in range(80):
            pg.wait_for_timeout(150); e_ = pg.evaluate("()=>(window._onbFinPas&&_onbFinPas())||{pas:0,enCours:true}")
            if e_['pas'] >= k_ + 1 and not e_['enCours']: break
        pg.wait_for_timeout(400); fk = pg.evaluate(FIN); vus.append((fk['tonVu'], sum(1 for l in fk['lignes'] if l['vu']), round(fk['haut'])))
    juge('[%s] 11.4 · ⚑ v148 (C-124 §9.2) : chaque toucher fait paraître UN paragraphe — la phrase de ton, puis Primo · Deuxio · Tertio, puis la fin ; le bloc remonte à chaque pas' % T,
         len(vus) == 3 and vus[0][0] and vus[0][1] == 0 and 0 < vus[1][1] < vus[2][1] and vus[0][2] >= vus[1][2] >= vus[2][2], 'après chaque toucher (ton, lignes, haut) : %s' % vus)
    f1 = pg.evaluate(FIN); im = image(pg); px = im.load(); ban = 0; tot = 0
    juge('[%s] 11.5 · à la fin, le bloc a remonté (son haut ≤ 90)' % T, f1['haut'] <= 90.5, 'haut %.0f' % f1['haut'])
    for y in range(int(f1['bas']) + 2, int(f1['bas']) + 14):
        for x in range(12, 378, 3):
            c = px[int(d[0] + x * d[2]), int(d[1] + y * d[2])]; tot += 1
            fond = (223, 202, 164) if th == 'light' else (5, 3, 2)
            if sum(abs(c[i] - fond[i]) for i in range(3)) > 30: ban += 1
    juge('[%s] 11.4 · après trois touchers, tout est là (toutes les lignes)' % T, all(l['vu'] for l in f1['lignes']), '%d sur %d' % (sum(1 for l in f1['lignes'] if l['vu']), len(f1['lignes'])))
    juge('[%s] 11.5 · le bloc passe AU-DESSUS des dalles : sur l\'image, 12 pt sous lui ne portent que le fond de la Toile' % T, tot and ban <= tot * 0.02, '%d pixels hors du fond sur %d (bas du bloc %.0f)' % (ban, tot, f1['bas']))
    c = pg.evaluate(CONT); juge('[%s] aucun contour ni ombre sur aucune lettre de l\'onboarding' % T, not c, c)
    im.save('planche-v146/onboarding-fin-%s.png' % T)
    juge('[%s] aucune erreur de page' % T, not er, er[:2]); ctx.close()
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    parcours(b, 'light'); parcours(b, 'dark'); b.close()
print('\n  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
