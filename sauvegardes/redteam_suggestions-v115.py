#!/usr/bin/env python3
"""
redteam_suggestions.py — LES SUGGESTIONS DE LA PAGE + (v115, Tom). Pour chaque liste (Promi à soi, « promets-moi », Chiche, Cercle) :
les phrases 1 et 2 sont FIXES (1re et 2e ouverture), la troisième est tirée SANS REMISE parmi les phrases 3…N — aucune ne revient
avant que toutes soient passées —, et le tirage est GARDÉ d'une ouverture à l'autre (on recharge la page au milieu).
On simule 3 × N ouvertures par liste. Rougi : python3 redteam_suggestions.py sauvegardes/app-avant-v115.html
"""
import sys, os
from playwright.sync_api import sync_playwright
ARG=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
if ARG.startswith('sauvegardes/'):
    import shutil; shutil.copy(ARG, 'zz-sugg.html'); ARG='zz-sugg.html'
OUVRE="""(t)=>{ const cs=document.getElementById('createSheet'); const av=cs.classList.contains('show');
  cs.classList.add('show'); window._ppExempleRaz(); const v=window._ppExemple(t); if(!av) cs.classList.remove('show'); return v; }"""
LISTE="""(t)=>{ const X=window._ppExemplesListes; return t==='nuee' ? [].concat(X.NU.projets||[],X.NU.road||[],X.NU.mariages||[]) : X.L[t]; }"""
ok=True
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(6500)
    for t in ('soi','demander','chiche','nuee'):
        pg.evaluate("(t)=>{ for(const k of Object.keys(localStorage)) if(k.indexOf('promi_ex_')===0) localStorage.removeItem(k); }", t)
        a=pg.evaluate(LISTE,t); N=len(a); seq=[]
        for k in range(3*N):
            if k==N:   # le tirage est gardé d'une ouverture à l'autre : on recharge la page au milieu
                pg.reload(); pg.wait_for_timeout(6500)
            seq.append(pg.evaluate(OUVRE,t))
        err=[]
        if seq[0]!=a[0]: err.append('ouverture 1 = « %s » (attendu la phrase 1)'%seq[0])
        if seq[1]!=a[1]: err.append('ouverture 2 = « %s » (attendu la phrase 2)'%seq[1])
        reste=seq[2:]; M=N-2
        for c in range(0,len(reste),M):
            cyc=reste[c:c+M]
            dup=[x for x in set(cyc) if cyc.count(x)>1]
            if dup: err.append('cycle %d : %d répétition(s) avant épuisement (« %s »…)'%(c//M+1,len(dup),dup[0])); break
            fix=[x for x in cyc if x in (a[0],a[1])]
            if fix: err.append('cycle %d : la phrase 1 ou 2 est tirée'%(c//M+1)); break
            if len(cyc)==M and set(cyc)!=set(a[2:]): err.append('cycle %d : %d phrase(s) jamais tirée(s)'%(c//M+1, len(set(a[2:])-set(cyc)))); break
        print('%-9s N=%-2d %d ouvertures  %s' % (t, N, len(seq), 'OK' if not err else '✗ '+' ; '.join(err)))
        ok = ok and not err
    b.close()
if ARG=='zz-sugg.html': os.remove(ARG)
print('✅ tirage sans remise' if ok else '❌ le tirage répète')
sys.exit(0 if ok else 1)
