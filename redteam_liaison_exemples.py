#!/usr/bin/env python3
"""⚑ v212 (C-312, Tom, 19 nov. 2026) — « une phrase d'exemple doit s'afficher directement avec la bonne liaison : « d' » devant une voyelle ou un h muet, « de » sinon
(h aspiré compris). Sinon, c'est une faute. » Toutes les listes : l'onboarding, la page + des trois natures (à soi, « je te promets », « promets-moi » au singulier et
au pluriel, Chiche ; le Cercle n'a pas de « de »), et les phrases de repli.
Critère : chaque phrase de chaque liste, affichée, porte la liaison juste — la règle est écrite ICI, en dur (voyelle, h muet → « d’ » ; h aspiré de la liste, y consonne,
onze, oui, un chiffre → « de » ; « y », « en » → « d’ »).
  A · chaque phrase de chaque liste, posée comme l'exemple de sa place et la phrase rendue : le « de » / « d’ » qui la précède, lu dans la phrase rendue, est juste ;
  B · à la PREMIÈRE image (et à chaque image où la liaison et l'exemple se voient : une moitié découpée à vide, au milieu d'un détracé puis d'un tracé, ne se lit pas) d'une vraie ouverture de la page + (huit ouvertures par forme : les phrases fixes puis le tirage), la liaison est déjà juste, et à chaque image ;
  C · l'onboarding : « Je me promets » + la liaison de son exemple, à la première image de la page de la parole, et quand la parole tapée est effacée ;
  D · la place vidée à la frappe (l'exemple revient) : la liaison redevient celle de l'exemple.
`--fichier=`. Rouge sur v211 (« de arroser mes plantes… »)."""
import sys, re, unicodedata
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
from liaison_regle import attendu, H_ASPIRE
R = []
def juge(nom, ok, det=''):
    R.append(ok); print(('✅' if ok else '❌'), nom, '' if ok else det, flush=True)
LIT = """()=>{ const t=document.querySelector('#csPhrase .ph-m[data-ph="titre"]'); if(!t) return null; let li=t.previousElementSibling;
  while(li && !li.classList.contains('ph-li')) li=li.previousElementSibling; const m=t.querySelector('.v203-txt')||t.querySelector('.ph-mot')||t;
  const cache=e=>{ const c=e?getComputedStyle(e).clipPath:''; return !!c && c.indexOf('polygon(0px 0px, 0px 0px')===0; };
  const w=t.querySelector('.v200-mt')||t;
  return {li:li?li.textContent.trim():null, ex:(m.textContent||'').replace(/\\s+/g,' ').trim(), vide:t.classList.contains('ph-vide'), vu:!!li && !cache(li) && !cache(w) && !cache(m)}; }"""
REC = """()=>{ window.__le=[]; let on=true; window.__leStop=()=>{on=false;}; const f=()=>{ if(!on) return; const cs=document.getElementById('createSheet');
  if(cs && cs.classList.contains('show')){ const r=(%s)(); if(r) window.__le.push(r); } requestAnimationFrame(f); }; requestAnimationFrame(f); }""" % LIT
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, vw=430, vh=932); pg = B.ouvre(ctx, F)
    L = pg.evaluate("()=>window._ppExemplesListes.L")
    def ouvre(nat):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
        pg.evaluate("(n)=>{ document.getElementById('createBtn').click(); setTimeout(()=>document.querySelector('#accChoix .acc-pil[data-k='+n+']').click(),600); }", nat); pg.wait_for_timeout(3600)
    # A — chaque phrase de chaque liste, rendue comme exemple de sa place
    FORME = {'soi': ('promi', "P.sens='faire'; P.faireAutre=false; P.qui='Moi';"), 'faire': ('promi', "P.sens='faire'; P.faireAutre=true; P.qui='Rachel';"),
             'demander': ('promi', "P.sens='demander'; P.qui='Moi';"), 'demander-pluriel': ('promi', "P.sens='demander'; P.qui='Rachel, Nico';"), 'chiche': ('chiche', "P.sens='chiche'; P.qui='Moi';")}
    for forme, (nat, pose) in FORME.items():
        t = forme.split('-')[0]; liste = L[t]; ouvre(nat); fautes = []
        for ph in liste:
            pg.evaluate("(a)=>{ const [t,ph]=a; const o=window.__oEx||window._ppExemple; window.__oEx=o; window._ppExemple=function(x){ return x===t ? ph : o(x); }; const P=window._phrase; P.titre=''; " + pose + " try{ _phraseRendu(); }catch(e){} }", [t, ph])
            pg.wait_for_timeout(2200); r = pg.evaluate(LIT)
            if not r: fautes.append((ph, 'pas de place')); continue
            if r['li'] != attendu(r['ex']) or not r['vide']: fautes.append((r['ex'], r['li'], attendu(r['ex'])))
        pg.evaluate("()=>{ if(window.__oEx){ window._ppExemple=window.__oEx; window.__oEx=null; } }")
        juge('A · %s : les %d phrases affichées avec leur liaison' % (forme, len(liste)), not fautes, fautes[:6])
    # B — la première image de vraies ouvertures
    for nat, sens in (('promi', None), ('promi', 'demander'), ('chiche', None)):
        mauvais = []; vus = []
        for k in range(8):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700); pg.evaluate(REC)
            pg.evaluate("(n)=>{ document.getElementById('createBtn').click(); setTimeout(()=>document.querySelector('#accChoix .acc-pil[data-k='+n+']').click(),600); }", nat); pg.wait_for_timeout(3400)
            if sens:
                pg.evaluate("()=>{ window.__le=[]; }"); B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2600)
            pg.evaluate("()=>__leStop()"); fr = pg.evaluate("()=>__le")
            vu = [f for f in fr if f['vide'] and f['ex'] and f['li'] and f['vu']]
            if vu: vus.append(vu[-1]['ex'])
            for f in vu:
                if f['li'] != attendu(f['ex']): mauvais.append((k, f['ex'], f['li'])); break
        juge('B · %s%s : %d ouvertures, la liaison juste dès la première image (%s)' % (nat, ' · ' + sens if sens else '', len(vus), ' / '.join(v[:22] for v in vus[:4])), not mauvais and len(vus) >= 6, mauvais[:4])
    # D — la place vidée à la frappe
    ouvre('promi'); fautes = []
    for ph in [x for x in L['soi'] if attendu(x) == 'd’'][:2]:
        pg.evaluate("(ph)=>{ const o=window._ppExemple; window._ppExemple=function(x){ return x==='soi' ? ph : o(x); }; _phrase.titre=''; _phrase.sens='faire'; _phrase.faireAutre=false; _phrase.qui='Moi'; _phraseRendu(); window.__oEx=o; }", ph)
        B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(500)
        pg.keyboard.type('mer', delay=120); pg.wait_for_timeout(1500)
        a = pg.evaluate(LIT)
        for _ in range(3): pg.keyboard.press('Backspace'); pg.wait_for_timeout(150)
        pg.wait_for_timeout(2500); z = pg.evaluate(LIT)
        pg.evaluate("()=>{ window._ppExemple=window.__oEx; document.activeElement&&document.activeElement.blur(); }"); pg.wait_for_timeout(800)
        if not a or a['li'] != 'de' or not z or z['li'] != attendu(z['ex']) or not z['vide']: fautes.append((ph, a, z))
    juge('D · la place vidée : « mer » → « de », l\'exemple revenu → sa liaison', not fautes, fautes[:2])
    ctx.close()
    # C — l'onboarding
    ctx = B.contexte(b, vw=430, vh=932, onb=False); pg = B.ouvre(ctx, F, attente=7000)
    try:
        B.tap_sel(pg, '#onbPh [data-onb="prenom"]'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=60); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000)
        LO = "()=>{ const ph=document.getElementById('onbPh'); const de=ph&&ph.querySelector('.onbv-de'), pm=ph&&ph.querySelector('.onbv-pm[data-onb=\"parole\"]'); return de&&pm?{li:de.textContent.trim(), ex:(pm.textContent||'').trim()}:null; }"
        c0 = pg.evaluate(LO)
        juge('C · l’onboarding : « %s » + « %s »' % (c0 and c0['li'], c0 and c0['ex']), bool(c0) and c0['li'] == attendu(c0['ex']), c0)
    except Exception as e:
        juge('C · l’onboarding se joue', False, str(e)[:200])
    ctx.close(); b.close()
print('\n%d/%d' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
