import sys; sys.path.insert(0,'.'); sys.path.insert(0,'scratchpad/v159')
from playwright.sync_api import sync_playwright
from banc_tom import *
import importlib.util
spec=importlib.util.spec_from_file_location('bal','scratchpad/v159/balaye.py')
SRC=open('scratchpad/v159/balaye.py').read().split('res=[]')[0]
exec(SRC.replace("F = sys.argv[1]","F='app.html' #"))
PIEGE="""()=>{window.__ap=[];['sync','setTheme','setPalette','setHue','addPromi','removePromi','renderTo'].forEach(n=>{var f=Toile[n];Toile[n]=function(){var a=arguments;window.__ap.push(n+':'+(n==='sync'?(a[0]||[]).length:String(a[0]).slice(0,20))+' @'+(new Error().stack.split('\\n')[1]||'').slice(-40));return f.apply(this,a)};Object.assign(Toile[n],f)})}"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, stockage={'promi_monde':'terrazzo'}); toile_pleine(ctx, 25); pg = ouvre(ctx, 'app.html')
    pg.evaluate(PIEGE)
    for page in ['studio','aura','index','fil','reglages','fiche','plus']:
        pg.evaluate("()=>{window.__ap=[]}"); ouvrir(pg, page); print(page, pg.evaluate("()=>window.__ap"))
    b.close()
