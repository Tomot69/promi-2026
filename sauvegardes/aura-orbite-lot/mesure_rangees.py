# Ce que le bord de l'écran COUPE vraiment, à l'ouverture, selon le nombre de paroles tenues
# (3, 5, 6, 9 — simulé dans la page en passant des Promi à « tenu », jamais sur disque) et la
# longueur de la phrase (une ligne / deux lignes). On mesure le DESSIN des dalles (le canevas,
# pas sa boîte), la part cachée par le bord, et le trou à droite d'une rangée incomplète.
# Images sur disque, jamais envoyées.   python3 mesure_rangees.py URL SORTIE
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
MES = r"""()=>{ const cad=document.getElementById('auCadre'), cr=cad.getBoundingClientRect(), s=cr.width/390;
  const Y=(v)=>(v-cr.top)/s+cad.scrollTop, X=(v)=>(v-cr.left)/s;
  const cells=[...document.querySelectorAll('#auraScreen .au-c')].map(c=>{ const cv=c.querySelector('canvas'), sp=c.querySelector('span');
    const a=cv?cv.getBoundingClientRect():null, b=sp.getBoundingClientRect();
    return {x:X(c.getBoundingClientRect().left), dessin:a&&a.height?[Y(a.top),Y(a.bottom)]:null, libelle:[Y(b.top),Y(b.bottom)]}; });
  const tops=[...new Set(cells.map(c=>Math.round(c.libelle[0])))].sort((a,b)=>a-b);
  const rangees=tops.map(t=>cells.filter(c=>Math.round(c.libelle[0])===t));
  const bt=document.querySelector('#auraScreen .au-bt').getBoundingClientRect();
  return {n:cells.length, rangees:rangees.map(R=>({k:R.length, dessins:R.map(c=>c.dessin), libelles:R.map(c=>c.libelle)})),
          bouton:[Y(bt.top),Y(bt.bottom)], lignes:(()=>{const rg=document.createRange(); rg.selectNodeContents(document.querySelector('#auraScreen .au-mot'));
            return new Set([...rg.getClientRects()].map(x=>Math.round(x.top))).size;})()}; }"""
RES = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for N in (3, 4, 5, 6, 9):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>localStorage.removeItem('promi_orbite_ordre')")
        # N paroles tenues : on passe des Promi « à moi » à tenu (ou on en retire), dans la page seulement
        got = pg.evaluate("""(N)=>{ const mine=promises.filter(p=>p&&!p.draft&&!p.req&&(!p.from||p.from==='moi'));
            let T=mine.filter(p=>p.status==='tenu'); const autres=mine.filter(p=>p.status!=='tenu');
            while(T.length<N && autres.length){ const p=autres.shift(); p.status='tenu'; T.push(p); }
            while(T.length>N){ T.pop().status='encours'; }
            return mine.filter(p=>p.status==='tenu').length; }""", N)
        pg.evaluate("()=>setTheme('dark')"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>12)"): break
        pg.wait_for_timeout(1200)
        for i, nom in ((1, 'une_ligne'), (0, 'deux_lignes')):
            pg.evaluate("(i)=>_aura.mot(i)", i); pg.wait_for_timeout(700)
            pg.evaluate("()=>{document.getElementById('auCadre').scrollTop=0;}"); pg.wait_for_timeout(300)
            m = pg.evaluate(MES); m['tenus'] = got
            pg.query_selector('#device').screenshot(path=os.path.join(OUT, 'rangees_%d_%s.png' % (N, nom)))
            RES['%d %s' % (N, nom)] = m
            print('\n%d tenues (%d dalles) · phrase %s' % (got, m['n'], nom.replace('_', ' ')))
            for j, R in enumerate(m['rangees']):
                vis = []
                for d in R['dessins']:
                    if not d: vis.append('—'); continue
                    h = d[1] - d[0]; cache = max(0.0, min(h, d[1] - 844)); vis.append('%d %% caché' % round(100 * cache / h) if cache > 0 else 'entier')
                lib = ['caché' if l[0] >= 844 else ('coupé' if l[1] > 844 else 'visible') for l in R['libelles']]
                print('   rangée %d : %d dalle(s)%s · dessins %s · libellés %s' % (j + 1, R['k'], (' — TROU de %d à droite' % (3 - R['k'])) if R['k'] < 3 else '', ', '.join(vis), ', '.join(lib)))
            print('   bouton : haut %.1f (%s)' % (m['bouton'][0], 'sous le pli' if m['bouton'][0] >= 844 else ('ENTIER' if m['bouton'][1] <= 822 else 'COUPÉ')))
        pg.close()
    b.close()
json.dump(RES, open(os.path.join(OUT, 'rangees.json'), 'w'), indent=1)
