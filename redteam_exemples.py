#!/usr/bin/env python3
"""redteam_exemples.py — ⚑ v179b (Tom, E4 point 4) : LES PHRASES D'EXEMPLE DE LA PAGE + NE REVIENNENT JAMAIS DEUX FOIS DE SUITE.

« Garantis qu'une même phrase ne revient jamais deux fois de suite, y compris quand la liste repart de zéro. La liste elle-même ne change pas. »
  A · 50 ouvertures RÉELLES de la page + d'un Promi (le + de l'accueil, au doigt, puis X) : la phrase montrée (le titre de la phrase) ne se répète jamais
      d'une ouverture à la suivante ; les deux premières sont les phrases fixes 1 et 2 de la liste (v115) ;
  B · 2 000 ouvertures par liste (soi, faire, demander, chiche, nuee), la page + ouverte puis refermée dans la page (le tirage de l'app, `_ppExemple`,
      le sac gardé d'une ouverture à l'autre) : aucune répétition immédiate, même quand le sac repart de zéro ; chaque phrase de la liste sort ;
  C · la liste n'a pas changé (le nombre de phrases de chaque liste, en dur).
Rouge sur v178 (`--fichier=zz-v178.html`, B) : au remplissage du sac, la dernière phrase pouvait ressortir aussitôt.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
N_REEL = 50
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    tailles = pg.evaluate("()=>{ const E=window._ppExemplesListes; const o={}; for(const k in E.L) o[k]=E.L[k].length; o.nuee=E.NU.liste.length; return o; }")
    print('  listes :', tailles)
    juge('C · les listes ne changent pas (nombre de phrases)', tailles == {'soi': 20, 'faire': 16, 'demander': 15, 'chiche': 29, 'nuee': 40}, tailles)
    # B · le tirage de l'app, 2 000 ouvertures par liste
    R = pg.evaluate("""()=>{ const cs=document.getElementById('createSheet'), out={}; const E=window._ppExemplesListes;
      const ouvre=async()=>{}; const listes=Object.keys(E.L).concat(['nuee']);
      for(const t of listes){ for(const k of Object.keys(localStorage)) if(k.indexOf('promi_ex_')===0) localStorage.removeItem(k);
        let prev=null, rep=0, vus=new Set(), n=0, premiers=[];
        for(let i=0;i<2000;i++){ cs.classList.add('show'); window._ppExempleRaz(); const v=window._ppExemple(t); cs.classList.remove('show');
          if(v===prev) rep++; prev=v; vus.add(v); n++; if(i<2) premiers.push(v); }
        const a=(t==='nuee')?E.NU.liste:E.L[t]; out[t]={rep:rep, vus:vus.size, total:a.length, premiers:premiers, fixes:[a[0],a[1]]}; }
      return out; }""")
    for t, r in R.items():
        juge('B · [%s] 2 000 ouvertures : aucune répétition immédiate, sac compris ; toutes les phrases sortent' % t, r['rep'] == 0 and r['vus'] == r['total'], '%d répétitions · %d / %d phrases' % (r['rep'], r['vus'], r['total']))
    pg.evaluate("()=>{ for(const k of Object.keys(localStorage)) if(k.indexOf('promi_ex_')===0) localStorage.removeItem(k); }")
    # A · 50 ouvertures réelles au doigt
    vues = []
    for i in range(N_REEL):
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(450); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(1500)
        v = pg.evaluate("()=>{ const e=document.querySelector('#csPhrase .ph-m[data-ph=\"titre\"]'); return e?e.textContent.trim():null; }")
        vues.append(v)
        pg.evaluate("()=>{ const x=document.querySelector('#createSheet .closeb'); if(x) x.click(); else closeAll(); }"); pg.wait_for_timeout(450)
    reps = [i for i in range(1, len(vues)) if vues[i] == vues[i - 1]]
    juge('A · %d ouvertures réelles de la page + : aucune phrase deux fois de suite' % N_REEL, len([v for v in vues if v]) == N_REEL and not reps, 'répétitions aux ouvertures %s · %d phrases distinctes' % (reps, len(set(vues))))
    juge('A · aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
