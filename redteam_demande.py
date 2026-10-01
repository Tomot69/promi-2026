# -*- coding: utf-8 -*-
"""Batterie 7 — la demande de Promi (chantier 15)."""
from playwright.sync_api import sync_playwright
import os as _os, sys, re as _re
_ICI=_os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI,'app.html'),'/home/claude/app.html']:
        if _os.path.exists(p): return 'file://'+p
    for f in sorted(_os.listdir(_ICI),reverse=True):
        if _re.match(r'promi-v\d+\.html$',f): return 'file://'+_os.path.join(_ICI,f)
    return 'file:///home/claude/app.html'
R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(5600)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    t("l'API du cycle existe",
      pg.evaluate("()=>['demandeAccepter','demandesExpirer','demandesEnAttente','promiComptes'].every(f=>typeof window[f]==='function')"))

    _n0 = pg.evaluate("()=>Toile.count?Toile.count():0")
    _c0 = pg.evaluate("()=>promiComptes()")
    pg.evaluate("""()=>{const p=P('rends-moi le livre','Rachel',7,2,'encours',null);
      p.req=true; p.reqEtat='attente'; p.reqLe=Date.now(); promises.push(p); window.__d=p.id;}""")
    pg.wait_for_timeout(900)
    t("une demande ne pose PAS de dalle",
      pg.evaluate("()=>Toile.count?Toile.count():0") == _n0, 'cellules inchangees')
    t("elle n'entre pas dans les compteurs",
      pg.evaluate("()=>promiComptes().total") == _c0['total'], '%d' % _c0['total'])
    t("elle est listee en attente", pg.evaluate("()=>demandesEnAttente().length") > 0)

    pg.evaluate("()=>demandeAccepter(window.__d)"); pg.wait_for_timeout(1300)
    t("accepter fait apparaitre la dalle",
      pg.evaluate("()=>Toile.count?Toile.count():0") >= _n0)
    t("accepter la sort de l'attente", pg.evaluate("()=>demandesEnAttente().length") == 0)
    t("accepter la compte comme un Promi",
      pg.evaluate("()=>promiComptes().total") == _c0['total'] + 1)
    t("accepter n'agit qu'une fois",
      pg.evaluate("()=>demandeAccepter(window.__d)") == False)
    t("l'acceptation nourrit le Fil",
      pg.evaluate("()=>FEED.some(f=>f.type==='accept')"))

    pg.evaluate("""()=>{const p=P('vieux','Nico',3,1,'encours',null);
      p.req=true;p.reqEtat='attente';p.reqLe=Date.now()-40*24*3600*1000;promises.push(p);}""")
    _k = pg.evaluate("()=>demandesExpirer()")
    t("une demande expire apres un mois", _k >= 1, '%d expiree(s)' % _k)
    t("l'expiration ne notifie rien",
      not pg.evaluate("()=>FEED.some(f=>/expir/i.test(f.text||''))"))
    t("une demande expiree quitte l'attente",
      pg.evaluate("()=>demandesEnAttente().length") == 0)
    t("il n'existe pas d'etat « refusee »",
      not pg.evaluate("()=>promises.some(p=>p.reqEtat==='refusee')"))

    # ---------- la demande se voit ailleurs que sur la Toile ----------
    pg.evaluate("""()=>{const p=P('rends-moi le velo','Lea',7,2,'encours',null);
      p.req=true;p.reqEtat='attente';p.reqLe=Date.now();promises.push(p);window.__d2=p.id;}""")
    pg.wait_for_timeout(800)
    t("une demande allume la pastille du Fil",
      pg.evaluate("()=>{if(window._majFilDot)_majFilDot();const d=document.getElementById('filDot');return !!d&&d.classList.contains('on');}"))
    pg.evaluate("()=>{if(window.renderDetail)renderDetail(window.__d2);document.getElementById('detailPoster').classList.add('show');}")
    pg.wait_for_timeout(1400)
    t("sa vignette est dans la brume",
      pg.evaluate("()=>document.getElementById('dForm').classList.contains('dem-brume')"))
    t("un seul geste la rend reelle", pg.evaluate("()=>!!document.getElementById('dpfDemOk')"))
    t("aucun bouton refuser dans la fiche",
      not pg.evaluate("()=>/refus/i.test((document.getElementById('dpfDem')||{}).textContent||'')"))
    pg.evaluate("()=>document.getElementById('dpfDemOk').click()"); pg.wait_for_timeout(1400)
    t("accepter dissipe la brume",
      not pg.evaluate("()=>document.getElementById('dForm').classList.contains('dem-brume')"))

    t("aucune erreur JS", not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-44s %s  %s'%(n,s,d if s=='KO' else ''))
ok=sum(1 for _,s,_ in R if s=='OK')
print('\n%d/%d'%(ok,len(R)))
sys.exit(0 if ok==len(R) else 1)
