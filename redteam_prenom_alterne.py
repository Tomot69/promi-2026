#!/usr/bin/env python3
"""⚑ v211 (C-309, Tom, 19 nov. 2026) — « l'exemple « promets-moi » alterne entre « Bruno-Stanislas » et « Fabienne-Gudule » : à chaque retour dans ce mode après un autre
mode, et à chaque fermeture puis réouverture de la page +. Le prénom qui change se détrace puis se trace (C-279). Les deux phrases tiennent en entier aux échelles 1 et 0,79. »
Critère : une suite de changements de mode et de réouvertures donne Bruno-Stanislas, Fabienne-Gudule, Bruno-Stanislas… sans aucun changement sec.
Au doigt (le verbe touché), WebKit, stockage neuf, échelles 1 (430 × 932) et 0,79 (330 × 714). Quatre entrées dans « promets-moi » (deux dans la même ouverture, puis
une réouverture, deux encore) :
  A · la suite des prénoms est B, F, B, F ;
  B · à chaque image de chaque entrée : le texte de la place ne change QUE découpée à vide (le détracé fini) — jamais d'un texte entier à un autre ;
  C · la phrase tient : aucun « … », la place sur une ligne, à 24 pt au moins du bord droit.
`--fichier=`"""
import sys
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ATTENDU = ['Bruno-Stanislas', 'Fabienne-Gudule', 'Bruno-Stanislas', 'Fabienne-Gudule']
REC = r"""()=>{ window.__pr=[]; let on=true; window.__prStop=()=>{on=false;}; const f=()=>{ if(!on) return; const e=document.querySelector('#csPhrase .ph-m[data-ph="qui"]');
  if(e){ const w=e.querySelector('.v200-mt')||e; window.__pr.push([e.textContent, getComputedStyle(w).clipPath]); } else window.__pr.push([null, null]);
  requestAnimationFrame(f); }; requestAnimationFrame(f); }"""
TIENT = r"""()=>{ const dev=document.getElementById('device').getBoundingClientRect(), k=dev.width/390, e=document.querySelector('#csPhrase .ph-m[data-ph="qui"]'), ph=document.getElementById('csPhrase');
  const g=document.createRange(); g.selectNodeContents(e); const r=g.getBoundingClientRect(); const T=[], W=document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n;
  while((n=W.nextNode())){ if(!n.textContent.trim()) continue; const q=document.createRange(); q.selectNodeContents(n); [...q.getClientRects()].forEach(x=>{ if(x.width>1) T.push(x.top+x.height/2); }); }   /* les LIGNES du texte (le visage n'en est pas une) */
  T.sort((a,b)=>a-b); let lignes=T.length?1:0; for(let i=1;i<T.length;i++) if(T[i]-T[i-1]>8*k) lignes++;
  return {texte:ph.textContent.replace(/\s+/g,' ').trim(), lignes:lignes, droite:+((dev.right-r.right)/k).toFixed(1)}; }"""
VIDE = lambda c: c and c.startswith('polygon(0px 0px, 0px 0px')
R = []
def juge(nom, ok, det=''):
    R.append(ok); print(('✅' if ok else '❌'), nom, '' if ok else det, flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((430, 932, '1'), (330, 714, '0,79')):
        ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
        def ouvre():
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900)
            pg.evaluate("()=>{ document.getElementById('createBtn').click(); setTimeout(()=>document.querySelector('#accChoix .acc-pil[data-k=promi]').click(),600); }"); pg.wait_for_timeout(3800)
        def sens(): return pg.evaluate("()=>window._phrase&&window._phrase.sens")
        def bascule(log=False):
            if log: pg.evaluate(REC)
            B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2600)
            if log: pg.evaluate("()=>__prStop()"); return pg.evaluate("()=>__pr")
        suite = []; secs = []; tient = []
        ouvre()
        for tour in range(4):
            for _ in range(4):
                fr = bascule(log=True)
                if sens() == 'demander':
                    t = pg.evaluate(TIENT); suite.append(pg.evaluate("()=>document.querySelector('#csPhrase .ph-m[data-ph=\"qui\"]').textContent")); tient.append(t)
                    for a, z in zip(fr, fr[1:]):
                        if a[0] is not None and z[0] is not None and a[0] != z[0] and not (VIDE(a[1]) or VIDE(z[1])): secs.append((len(suite), a[0], z[0], a[1][:30], z[1][:30]))
                    break
            bascule()
            if tour == 1: ouvre()
        T = '[échelle %s]' % ech
        juge(T + ' A · la suite des prénoms : %s' % ' · '.join(suite), suite == ATTENDU, suite)
        juge(T + ' B · aucun changement sec du prénom (%d passages lus image par image)' % len(suite), not secs and len(suite) == 4, secs[:3])
        bad = [t for t in tient if '…' in t['texte'] or t['lignes'] != 1 or t['droite'] < 24 - 0.5]
        juge(T + ' C · la phrase tient (aucun « … », la place sur une ligne, ≥ 24 pt du bord) — %s' % ['%s : %s pt' % (s.split('-')[0], t['droite']) for s, t in zip(suite, tient)], not bad and len(tient) == 4, bad[:2])
        ctx.close()
    b.close()
print('\n%d/%d' % (sum(R), len(R)))
sys.exit(0 if all(R) else 1)
