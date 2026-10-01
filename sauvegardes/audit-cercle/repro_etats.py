# LE CERCLE — LES FUITES D'ÉTAT, REJOUÉES SEULES, SUR DES PARCOURS RÉELS (11 sept. 2026).
# L'audit les a vues dans son propre enchaînement (thème → mode → scènes) : ça ne suffit pas à les écrire comme
# défauts. Chaque parcours part d'une PAGE NEUVE et ne fait que ce qu'un utilisateur ferait ; les achats passent par
# les vrais boutons, au point (setPremium n'est appelé à la main que pour la FIN d'abonnement, qu'aucun bouton ne joue).
#   P1 · gratuit → Studio → Terrazzo (verrouillé) → « débloque-les tous » → Prendre l'année → rouvrir le Studio
#   P2 · gratuit → Studio → Terrazzo → revenir sur Encre (gratuit)
#   P3 · abonné → Studio → Terrazzo → fermer → fin d'abonnement → la Toile, le Studio
#   P4 · abonné → fin d'abonnement → Réglages (l'encart)
#   P5 · abonné → Studio → Mosaïque (gratuit) → fin d'abonnement → le monde
import json, os, sys
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'ecran')
ns = {'__file__': os.path.join(D, 'audit_ecran.py')}
exec(open(os.path.join(D, 'audit_ecran.py'), encoding='utf-8').read().split("R = {'scenes'")[0], ns)
ETAT, BASE, joue, capture, clic_doigt = (ns[k] for k in ('ETAT', 'BASE', 'joue', 'capture', 'clic_doigt'))
STUDIO = [(BASE, 200), ("()=>document.getElementById('studioBtn').click()", 1900)]
def monde(m): return ("()=>{const d=document.querySelector('#studioScreen [data-w=\"%s\"]'); if(d) d.click();}" % m, 1500)
VU = r"""()=>{const s=document.getElementById('studioScreen'); const t=[...s.querySelectorAll('#stpNom,#stBuyTx,.sc-t,.sc-s')]
  .filter(e=>e.checkVisibility&&e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})).map(e=>e.textContent.trim());
  return {classes:s.className, visible:t, monde:(window.Toile&&Toile.curWorld)?Toile.curWorld():null,
          encart:(document.querySelector('#openPlusTop .sc-t')||{}).textContent||null};}"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    def neuve(theme='dark'):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", theme); pg.wait_for_timeout(300)
        return ctx, pg
    for th in ('dark', 'light'):
        # P1
        ctx, pg = neuve(th); joue(pg, STUDIO + [monde('terrazzo')])
        a = pg.evaluate(VU)
        r1 = clic_doigt(pg, '#stLockCta'); pg.wait_for_timeout(1200)
        r2 = clic_doigt(pg, '#buyYear'); pg.wait_for_timeout(1600)
        b = pg.evaluate(ETAT)
        joue(pg, STUDIO); c = pg.evaluate(VU); capture(pg, 'repro_P1_%s_studio_rouvert' % th)
        R['P1_' + th] = {'terrazzo_gratuit': a, 'doigt_cta': r1, 'doigt_annee': r2, 'apres_achat': b, 'studio_rouvert': c}
        print('P1 %s  gratuit sur Terrazzo : %s\n       achat → premium=%s, ouvre %s · Studio rouvert : %s' % (th, a['visible'], b['premium'], b['couches'], c))
        ctx.close()
        # P2
        ctx, pg = neuve(th); joue(pg, STUDIO + [monde('terrazzo'), monde('encre')])
        v = pg.evaluate(VU); capture(pg, 'repro_P2_%s_encre_apres_terrazzo' % th)
        R['P2_' + th] = v; print('P2 %s  Encre après Terrazzo : %s' % (th, v)); ctx.close()
        # P3
        ctx, pg = neuve(th); pg.evaluate("()=>setPremium(true)"); joue(pg, STUDIO + [monde('terrazzo')])
        pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(500); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(800)
        m_toile = pg.evaluate("()=>(window.Toile&&Toile.curWorld)?Toile.curWorld():null")
        capture(pg, 'repro_P3_%s_toile_apres_fin' % th)
        joue(pg, STUDIO); v = pg.evaluate(VU); capture(pg, 'repro_P3_%s_studio_apres_fin' % th)
        R['P3_' + th] = {'monde_toile': m_toile, 'studio': v}
        print('P3 %s  fin d’abonnement sur Terrazzo : la Toile reste en %s · Studio : %s' % (th, m_toile, v)); ctx.close()
        # P4
        ctx, pg = neuve(th); pg.evaluate("()=>setPremium(true)"); pg.wait_for_timeout(400); pg.evaluate("()=>setPremium(false)")
        joue(pg, [(BASE, 200), ("()=>document.getElementById('settingsBtn').click()", 1700),
                  ("()=>{const b=document.getElementById('openPlusTop'); if(b) b.scrollIntoView({block:'center'});}", 500)])
        e = pg.evaluate("()=>{const b=document.getElementById('openPlusTop'); return {texte:b.textContent.replace(/\\s+/g,' ').trim(), vis:b.checkVisibility()};}")
        capture(pg, 'repro_P4_%s_reglages_apres_fin' % th)
        R['P4_' + th] = e; print('P4 %s  Réglages après la fin : %s' % (th, e)); ctx.close()
        # P5
        ctx, pg = neuve(th); pg.evaluate("()=>setPremium(true)"); joue(pg, STUDIO + [monde('mosaique')])
        avant = pg.evaluate("()=>Toile.curWorld()")
        pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(800)
        apres = pg.evaluate("()=>Toile.curWorld()")
        R['P5_' + th] = {'avant': avant, 'apres': apres}; print('P5 %s  Mosaïque (gratuit) avant la fin : %s → après : %s' % (th, avant, apres)); ctx.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'repro.json'), 'w'), ensure_ascii=False, indent=1)
print('écrit repro.json')
