#!/usr/bin/env python3
"""redteam_marges.py — LES PHRASES SUGGÉRÉES DE LA PAGE + (v115, Tom) : marge droite = marge gauche (24), retour à la ligne plutôt
que réduction, et la MÊME mise en page à 390 × 844, à 375 × 667 (iPhone SE) et sur un profil iPhone (appareil réduit par transformation —
le défaut du 30 sept. ne se voyait que là). Rougi : python3 redteam_marges.py sauvegardes/app-avant-v115.html"""
import json, sys
from playwright.sync_api import sync_playwright
LISTES=None   # lues DANS l'app (window._ppExemplesListes) : si Tom réécrit les listes, le juge les suit
import os, shutil
URL=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
if '/' in URL: shutil.copy(URL,'zz-marges.html'); URL='zz-marges.html'
OUVRE={'soi':"()=>{closeAll();document.getElementById('createBtn').click()}",}
def ouvrir(pg,t):
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(500)
    kind='nuee' if t=='nuee' else ('chiche' if t=='chiche' else 'promi')
    pg.evaluate("(k)=>{const x=document.querySelector('#createSheet .tile[data-kind=\"'+k+'\"]');x&&x.click()}",kind); pg.wait_for_timeout(1500)
    if t=='demander': pg.evaluate("()=>{window._phrase.sens='demander';window._phraseRendu()}")
    if t=='soi': pg.evaluate("()=>{window._phrase.sens='faire';window._phrase.faireAutre=false;window._phraseRendu()}")
    if t=='faire': pg.evaluate("()=>{window._phrase.sens='faire';window._phrase.faireAutre=true;window._phraseRendu()}")
    pg.wait_for_timeout(600)
MES="""(a)=>{ const [t,ph]=a;
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const sel = t==='nuee' ? '#nueePhrase .ph-m[data-np="nom"]' : '#csPhrase .ph-m[data-ph="titre"]';
  const e=document.querySelector(sel); if(!e) return {err:'pastille introuvable'};
  const R=[...e.getClientRects()]; const box=(t==='nuee'?document.getElementById('nueePhrase'):document.getElementById('csPhrase')).getBoundingClientRect();
  const rg=document.createRange(); rg.selectNodeContents(e); const T=[];
  [...rg.getClientRects()].forEach(q=>{ if(q.width<1||q.height<1) return; const c=(q.top+q.bottom)/2; if(T.some(b=>c>b[0]&&c<b[1])) return; T.push([q.top,q.bottom]); });
  const lignes=T.length;
  const fs=parseFloat(getComputedStyle(e).fontSize);
  return {lignes, droite:(dv.right-Math.max(...R.map(r=>r.right)))/s, gauche:(box.left-dv.left)/s, fs, n:R.length}; }"""
res={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for vw,opt in ((430,dict(viewport={'width':430,'height':932},device_scale_factor=2)),(375,dict(viewport={'width':375,'height':667},device_scale_factor=2)),('iphone',dict(p.devices['iPhone 13']))):
        ctx=b.new_context(**opt)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+URL); pg.wait_for_timeout(6500)
        X=pg.evaluate("()=>window._ppExemplesListes"); LISTES={'soi':X['L']['soi'],'faire':X['L'].get('faire',[]),'demander':X['L']['demander'],'chiche':X['L']['chiche'],'nuee':X['NU'].get('liste') or (X['NU']['projets']+X['NU']['road']+X['NU']['mariages'])}
        LISTES={k:v for k,v in LISTES.items() if v}
        for t,a in LISTES.items():
            ouvrir(pg,t)
            for ph in a:
                pg.evaluate("(a)=>{const [t,ph]=a; window._ppExemple=()=>ph; window._ppExempleCourant=ph; if(t==='nuee') window._nueePhraseRendu(); else window._phraseRendu();}",[t,ph])
                r0=None
                for _ in range(8):
                    pg.wait_for_timeout(350); r=pg.evaluate(MES,[t,ph])
                    if r==r0: break
                    r0=r
                res.setdefault(t,{}).setdefault(ph,{})[vw]=r
        ctx.close()
    b.close()
if URL=='zz-marges.html': os.remove(URL)
json.dump(res,open('scratchpad/v114/phrases.json','w'),ensure_ascii=False,indent=1)
mauvais=0; alaligne=[]
for t,d in res.items():
    for ph,v in d.items():
        for vue,m in v.items():
            if 'err' in m: print('✗',t,vue,ph,m['err']); mauvais+=1; continue
            if m['droite'] < m['gauche']-0.05: print('✗ %-8s %-7s marge droite %.1f < gauche %.1f  « %s »'%(t,vue,m['droite'],m['gauche'],ph)); mauvais+=1
        a,c,i=v[430],v[375],v['iphone']
        if not any('err' in x for x in (a,c,i)) and not (a['lignes']==c['lignes']==i['lignes'] and a['fs']==c['fs']==i['fs']):
            print('✗ %-8s la mise en page change avec l\'écran  « %s » : %s'%(t,ph,[(x['lignes'],x['fs']) for x in (a,c,i)])); mauvais+=1
        if a.get('lignes',1)>1: alaligne.append('%s · « %s » (%d lignes, %s px)'%(t,ph,a['lignes'],a['fs']))
print('passent à la ligne : %d / %d'%(len(alaligne),sum(len(d) for d in res.values())))
print('✅ marges égales, même mise en page à 390, 375 et sur iPhone' if not mauvais else '❌ %d défaut(s)'%mauvais)
sys.exit(1 if mauvais else 0)
