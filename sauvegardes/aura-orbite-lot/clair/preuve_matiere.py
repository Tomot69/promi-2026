# La famille 10 du juge (« la matière ») PROUVÉE contre un vrai défaut (CLAUDE.md §7) : le code testé est
# celui du juge, importé (MATIERE et ses constantes). Sur la copie A2 :
#   · tel quel                 → ne doit RIEN signaler
#   · la « 2 » posée en clair   → doit prendre les dalles NOYÉES et le CONTOUR dissous (poil clair, peau assombrie)
#   · la boule sombre en clair  → doit prendre l'ÉCART (poil = corps sombre §1.3, peau claire : ≈ 138)
#   python3 preuve_matiere.py URL
import sys, os, importlib.util
from playwright.sync_api import sync_playwright
APP = '/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
sp = importlib.util.spec_from_file_location('juge_aura', os.path.join(APP, 'releve-aura.py'))
J = importlib.util.module_from_spec(sp); sp.loader.exec_module(J)
URL = sys.argv[1]

def verdict(th, mm, dk):
    f = []
    if abs(mm['boule'] - J.ECART_BOULE[th]) > J.ECART_TOL: f.append('écart %.1f (décidé %.0f)' % (mm['boule'], J.ECART_BOULE[th]))
    if mm['contour'] < J.CONTOUR_MIN: f.append('contour %.1f' % mm['contour'])
    if not mm['iles']: f.append('aucune île')
    elif th == 'light' and dk and dk['iles'] and (mm['med'] < dk['med'] - J.DALLES_MARGE or mm['min'] < dk['min'] - J.DALLES_MARGE):
        f.append('dalles noyées (%.1f/%.1f contre %.1f/%.1f)' % (mm['med'], mm['min'], dk['med'], dk['min']))
    return f

ok = True
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def peintes(n=8):
        p0 = pg.evaluate("()=>_aura.etat().peints")
        for _ in range(300):
            if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
            pg.wait_for_timeout(50)
    def ouvre(th):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
    def mesure(fond):
        pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
        e = pg.evaluate("()=>_aura.etat().erreur")
        if e: print('❌  PREUVE INVALIDE : erreur du peintre', e[:200]); b.close(); sys.exit(2)
        pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_avec=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); window.__m_sans=null;}")
        pg.evaluate("()=>_aura.sansIles(true)"); peintes()
        pg.evaluate("()=>{const cv=document.getElementById('auBoule'); window.__m_sans=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice();}")
        pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
        m = pg.evaluate(J.MATIERE, [fond]); pg.evaluate("()=>_aura.fige(false)"); return m
    ouvre('dark'); dk = mesure([22, 23, 27])
    print('sombre (référence) : écart %.1f · contour %.1f · dalles %d, plus faible %s, médiane %s' % (dk['boule'], dk['contour'], dk['iles'], dk['min'] and round(dk['min'], 1), dk['med'] and round(dk['med'], 1)))
    ouvre('light')
    CAS = [('tel quel (A2)', None, None, None, False),
           ('la « 2 » posée en clair', [0xCB, 0xAA, 0xFF], None, 0.0, True),
           ('la boule sombre en clair', [0x12, 0x14, 0x2A], None, None, True)]
    print('\n%-30s %-10s %s' % ('', 'attendu', 'le juge dit'))
    for nom, sol, peauc, t, faute in CAS:
        pg.evaluate("(c)=>_aura.regleSol(c)", sol); pg.evaluate("(t)=>_aura.reglePeau(t)", t); pg.evaluate("(c)=>_aura.reglePeauC(c)", peauc)
        mm = mesure([244, 238, 225]); f = verdict('light', mm, dk)
        bon = bool(f) == faute; ok &= bon
        print('%-30s %-10s %s  %s' % (nom, 'PRIS' if faute else 'passe', '; '.join(f) if f else 'rien', '✅' if bon else '❌'))
    pg.evaluate("()=>{_aura.regleSol(null); _aura.reglePeau(null); _aura.reglePeauC(null);}")
    b.close()
print('\n%s' % ('✅  la famille « la matière » mord' if ok else '❌  la famille « la matière » ne mord pas'))
sys.exit(0 if ok else 1)
