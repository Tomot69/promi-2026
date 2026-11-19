"""v214 (Tom, 19 nov. 2026, C-316) — toucher le mot PROMI de l'accueil ouvre Ma Parole ! en gratuit, rien pour un membre.
Au vrai doigt (banc_tom), deux thèmes, échelles 1 et 0,79. Corrige C-200 ④ (v164b)."""
import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
FICHIER=next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')),'app.html')
ok=[]; ko=[]
def juge(nom, v):
  (ok if v else ko).append(nom); print(('OK  ' if v else 'KO  ')+nom)
OUV="()=>{var s=document.getElementById('plusScreen'); if(!s) return false; var r=s.getBoundingClientRect(); return s.classList.contains('show') && r.top<200 && getComputedStyle(s).visibility!=='hidden'}"
with sync_playwright() as p:
  b=p.webkit.launch()
  for sombre in (False,True):
    for vw,vh,ech in ((430,932,'1'),(330,714,'0,79')):
      for paye in (False,True):
        ctx=B.contexte(b, sombre=sombre, vw=vw, vh=vh); pg=B.ouvre(ctx,FICHIER); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        if paye: pg.evaluate("()=>{try{setPremium(true)}catch(_){}}"); pg.wait_for_timeout(500)
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800)
        c=pg.evaluate("()=>{var m=document.querySelector('.acc-plat .acc-mm'); if(!m) return null; var r=m.getBoundingClientRect(); var e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2); return [r.x+r.width/2,r.y+r.height/2, !!(e&&(e===m||m.contains(e)))]}")
        nom='%s · %s · %s'%('sombre' if sombre else 'clair', ech, 'membre' if paye else 'gratuit')
        if not c: juge(nom+' : le mot PROMI existe', False); ctx.close(); continue
        juge(nom+' : PROMI joignable au doigt', c[2])
        B.tap(pg, c[0], c[1], appareil=False); pg.wait_for_timeout(1400)
        o=pg.evaluate(OUV)
        juge(nom+(' : Ma Parole ! s\'ouvre' if not paye else ' : rien ne s\'ouvre'), o if not paye else not o)
        juge(nom+' : aucune erreur', not errs)
        ctx.close()
  b.close()
print('\n%d/%d'%(len(ok),len(ok)+len(ko)))
