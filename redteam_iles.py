"""⚑ v203 (Tom, C-275 §5) — LES ÎLES DE LA PELOTE NE SE NOIENT PAS : 24 palettes × 2 thèmes, chaque île à ΔE ≥ 15 (le plancher de Q192) de la boule autour d'elle,
mesurée là où le moteur la pose (la MATIÈRE de releve-aura : avec et sans les îles, à vue figée). Les couleurs sont les tons EXACTS de la palette (C-204, C-275) :
aucune couleur dérivée pour tenir le plancher.
⚑ EXCEPTION VALIDÉE PAR TOM (14 nov. 2026, retours de v203) : « Alangui en clair : accepté tel quel (couleurs exactes de la palette, aucune couleur dérivée). Ne
cherche plus à atteindre 15 sur cette palette. » Ses quatre tons sont sourds : en clair, aucune hauteur de rampe (0,3 à 3,2) n'atteint 15 (mesuré 8 à 14). Elle
est mesurée et écrite, jamais jugée.
Chromium (le rendu de la Pelote par la carte graphique est le même), 430 × 932 ×2. --palettes=alangui,ingenu · --fichier="""
import sys, re, io, json
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
SEUL = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--palettes=')), None)
PLANCHER = 15.0
EXCEPTIONS = {('alangui', 'light'): 'Tom, 14 nov. 2026 : couleurs exactes acceptées telles quelles'}
src = io.open('releve-aura.py', encoding='utf-8').read()
MATIERE = re.search(r'MATIERE = r"""(.*?)"""', src, re.S).group(1).replace('FACE', '0.35')
res = []; exc = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.add_init_script("try{localStorage.removeItem('promi_pelote_palier')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def attends(c, ms=15000):
        t = 0
        while t < ms:
            if pg.evaluate(c): return True
            pg.wait_for_timeout(100); t += 100
    def peintes(n=2):
        p0 = pg.evaluate("()=>_aura.etat().peints"); attends("()=>_aura.etat().peints>=%d" % (p0 + n))
    pals = pg.evaluate("Object.keys(Toile.palettes())")
    for pal in (SEUL or pals):
        for th in ('light', 'dark'):
            pg.evaluate("([t,p])=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); setTheme(t); Toile.setPalette(p); }", [th, pal]); pg.wait_for_timeout(300)
            pg.evaluate("()=>{try{localStorage.removeItem('promi_pelote_palier');}catch(e){} _aura.palier(0); document.getElementById('souffleBtn').click()}")
            attends("()=>{const e=_aura.etat(); return e&&e.pret&&e.frames>12}"); pg.wait_for_timeout(500)
            pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); peintes(8)
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__m_sans=null;}")
            pg.evaluate("()=>_aura.sansIles(true)"); peintes(8)
            pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
            pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
            mm = pg.evaluate(MATIERE, [[5, 3, 2] if th == 'dark' else [247, 240, 222]]); pg.evaluate("()=>_aura.fige(false)")
            d = [x['dE'] for x in mm.get('dalles', [])]; mn = min(d) if d else None
            nom = '%s · %s' % (pal, 'clair' if th == 'light' else 'sombre')
            if (pal, th) in EXCEPTIONS:
                exc.append(nom); print('➖ %-28s exception validée — la plus faible ΔE %s (%s)' % (nom, mn and round(mn, 1), EXCEPTIONS[(pal, th)]), flush=True); continue
            ok = bool(d) and mn >= PLANCHER; res.append(ok)
            print('%s %-28s %d îles · la plus faible ΔE %s' % ('✅' if ok else '❌', nom, len(d), mn and round(mn, 1)), flush=True)
    b.close()
print('%d/%d · exceptions validées : %s' % (sum(res), len(res), ', '.join(exc) or 'aucune'))
sys.exit(0 if all(res) else 1)
