import json, sys
from playwright.sync_api import sync_playwright
D=json.load(open('scratchpad/v114/listes.json')); L=D['L']; NU=D['NU']
LISTES={'soi':L['soi'],'demander':L['demander'],'chiche':L['chiche'],'nuee':NU['projets']+NU['road']+NU['mariages']}
URL=sys.argv[1] if len(sys.argv)>1 else 'app.html'
OUVRE={'soi':"()=>{closeAll();document.getElementById('createBtn').click()}",}
def ouvrir(pg,t):
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(500)
    kind='nuee' if t=='nuee' else ('chiche' if t=='chiche' else 'promi')
    pg.evaluate("(k)=>{const x=document.querySelector('#createSheet .tile[data-kind=\"'+k+'\"]');x&&x.click()}",kind); pg.wait_for_timeout(1500)
    if t=='demander': pg.evaluate("()=>{window._phrase.sens='demander';window._phraseRendu()}")
    if t=='soi': pg.evaluate("()=>{window._phrase.sens='faire';window._phrase.faireAutre=false;window._phraseRendu()}")
    pg.wait_for_timeout(600)
MES="""(a)=>{ const [t,ph]=a; window._ppExemple=()=>ph; window._ppExempleCourant=ph;
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
    for vw,vh in ((430,932),(375,667)):  # 430×932 donne #device à 390×844 exactement ; 375×667 = l'iPhone SE
        ctx=b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+URL); pg.wait_for_timeout(6500)
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
json.dump(res,open('scratchpad/v114/phrases.json','w'),ensure_ascii=False,indent=1)
for t,d in res.items():
    for ph,v in d.items():
        a,c=v[430],v[375]
        if 'err' in a: print(t,ph,a); continue
        flag=' ✗ DÉBORDE' if a['droite']<a['gauche']-0.5 else ''
        if a['lignes']>1 or flag or a!=c: print('%-8s %-50s 390: %d l. marge D %.1f (G %.1f) fs %.1f | 375: %d l. D %.1f%s'%(t,ph[:50],a['lignes'],a['droite'],a['gauche'],a['fs'],c['lignes'],c['droite'],flag))
