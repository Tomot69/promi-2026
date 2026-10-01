# -*- coding: utf-8 -*-
"""LE GESTE DE COULEUR DU STUDIO — AU VRAI DOIGT, horodaté par le CDP (§8).
   Contrats écrits EN DUR, depuis Q125 et la décision de Tom du 20 sept. 2026."""
import sys, time
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
MAINTIEN=480; COURSE=390; PAS_PAL=48
ok=[0]; ko=[]
def t(nom,bon,det=''):
    (ok.__setitem__(0,ok[0]+1) if bon else ko.append(nom))
    print('  %-60s %s  %s'%(nom,'OK ' if bon else 'KO ',det))

def doigt(cdp,x,y,ms):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}],'timestamp':ms/1000.0})
def bouge(cdp,x,y,ms):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y}],'timestamp':ms/1000.0})
def leve(cdp,ms):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[],'timestamp':ms/1000.0})

ETAT="()=>{var T=window.Toile;return {hue:T.getHue(),pal:T.getPalette(),monde:T.getTheme(),arme:window._studioGesteCouleur?window._studioGesteCouleur.arme():null};}"

with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True,is_mobile=True)
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    t("le lot est posé", pg.evaluate("()=>!!window._studioGesteCouleur"))
    t("Toile.getHue existe", pg.evaluate("()=>typeof window.Toile.getHue==='function'"))
    cst=pg.evaluate("()=>window._studioGesteCouleur")
    t("les constantes sont celles décidées (480 · 390 · 48)",
      cst and cst['MAINTIEN']==MAINTIEN and cst['COURSE']==COURSE and cst['PAS_PAL']==PAS_PAL, str(cst))

    # un point au milieu de la Toile, loin des plateaux
    pt=pg.evaluate("()=>{var d=document.getElementById('device').getBoundingClientRect();return [d.left+d.width/2, d.top+d.height*0.42];}")
    av=pg.evaluate(ETAT)

    # 1 · un appui maintenu arme le geste
    ms=1000; doigt(cdp,pt[0],pt[1],ms); pg.wait_for_timeout(MAINTIEN+220)
    t("l'appui maintenu arme le geste", pg.evaluate("()=>window._studioGesteCouleur.arme()")==True)

    # 2 · l'horizontale fait varier la TEINTE, et elle suit le doigt
    for i in range(1,7):
        ms+=40; bouge(cdp,pt[0]+i*20,pt[1],ms)
    pg.wait_for_timeout(400)
    ap=pg.evaluate(ETAT)
    att=((av['hue']+120*(360/COURSE))%360)
    t("l'horizontale fait varier la teinte", abs(ap['hue']-av['hue'])>1, "%.1f → %.1f"%(av['hue'],ap['hue']))
    t("la teinte suit le doigt, sans accélération (Q125)", abs(ap['hue']-att)<1.5, "attendu %.1f, lu %.1f"%(att,ap['hue']))

    # 3 · on revient EXACTEMENT d'où l'on vient
    for i in range(5,-1,-1):
        ms+=40; bouge(cdp,pt[0]+i*20,pt[1],ms)
    pg.wait_for_timeout(400)
    r=pg.evaluate(ETAT)
    t("on revient exactement d'où l'on vient (Q125)", abs(r['hue']-av['hue'])<0.5, "%.3f vs %.3f"%(av['hue'],r['hue']))

    # 4 · la verticale change de PALETTE
    for i in range(1,5):
        ms+=40; bouge(cdp,pt[0],pt[1]+i*PAS_PAL,ms)
    pg.wait_for_timeout(500)
    r2=pg.evaluate(ETAT)
    t("la verticale change de palette", r2['pal']!=av['pal'], "%s → %s"%(av['pal'],r2['pal']))
    # et on revient
    for i in range(3,-1,-1):
        ms+=40; bouge(cdp,pt[0],pt[1]+i*PAS_PAL,ms)
    pg.wait_for_timeout(400)
    r3=pg.evaluate(ETAT)
    t("la palette revient d'où elle vient", r3['pal']==av['pal'], "%s"%r3['pal'])
    ms+=60; leve(cdp,ms); pg.wait_for_timeout(400)
    t("le geste se désarme au lever du doigt", pg.evaluate("()=>window._studioGesteCouleur.arme()")==False)

    # 5 · LE GLISSEMENT DE MONDE GARDE LA MAIN — un glissement franc, sans attendre
    pg.goto(URL); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    m0=pg.evaluate(ETAT)
    ms=1000; doigt(cdp,pt[0]+90,pt[1],ms)
    for i in range(1,8):
        ms+=25; bouge(cdp,pt[0]+90-i*18,pt[1],ms)
    ms+=25; leve(cdp,ms); pg.wait_for_timeout(700)
    m1=pg.evaluate(ETAT)
    t("un glissement franc change encore de MONDE", m1['monde']!=m0['monde'], "%s → %s"%(m0['monde'],m1['monde']))
    t("et il n'a pas armé le geste de couleur", pg.evaluate("()=>window._studioGesteCouleur.arme()")==False)
    t("et il n'a pas touché à la teinte", abs(m1['hue']-m0['hue'])<0.01, "%.3f vs %.3f"%(m0['hue'],m1['hue']))
    b.close()
print('\n%d/%d'%(ok[0],ok[0]+len(ko)))
if ko: print('KO :', ' · '.join(ko))
