import sys, os; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
src=open('scratchpad/v207/haut_ecrans.py').read(); SONDE=eval(src[src.index('SONDE="""')+6:src.index('"""',src.index('SONDE="""')+9)+3])
PLEIN="window.__zsInsets=[47,0,34,0]; document.addEventListener('DOMContentLoaded',function(){ var st=document.createElement('style'); st.textContent='.frame{padding:0!important;--fit:1!important}#device{border-radius:0!important;box-shadow:none!important}'; document.head.appendChild(st); });"
def montre(pg, nom):
    L=[x for x in pg.evaluate(SONDE, 53) if 'v187Bande' not in x]; print('==', nom, len(L)); [print('    ', x) for x in L[:10]]
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=B.contexte(b, onb=False, guide=False); ctx.add_init_script(PLEIN); pg=B.ouvre(ctx,'app.html',attente=7000)
    montre(pg,'onboarding prénom')
    B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000); B.attend_parole(pg); montre(pg,'onboarding parole')
    ctx.close()
    ctx=B.contexte(b); B.toile_pleine(ctx,10); ctx.add_init_script(PLEIN); pg=B.ouvre(ctx,'app.html')
    for nom,js in [('personne',"()=>{ closeAll(); try{ openPerson('Marion'); }catch(e){ try{ window._ouvrePersonne&&_ouvrePersonne('Marion'); }catch(_){} } }"),
                   ('ma parole',"()=>{ closeAll(); try{ ouvreCercle(); }catch(e){} }"),
                   ('dessin',"()=>{ closeAll(); const p=promises.find(x=>!x.draft&&!x.nuee); openDetail(p.id); setTimeout(()=>{ try{ window._dessin&&_dessin.ouvre&&_dessin.ouvre(); }catch(e){} },1500); }"),
                   ('veille',"()=>{ closeAll(); try{ window._veille&&_veille().part&&_veille().part(); }catch(e){} }")]:
        pg.evaluate(js); pg.wait_for_timeout(3500); montre(pg,nom)
    b.close()
