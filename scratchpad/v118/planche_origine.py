# planche @3x — Q365 : trois dalles d'origine (dont une en conflit) sur chaque nature
import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S = 3; CAS = {'promi': ['irascible', 'truculent', 'signal'], 'chiche': ['irascible', 'primesautier', 'signal']}
caps = {}; notes = {}
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setTheme('light')}"); pg.wait_for_timeout(500)
    ids = pg.evaluate("""()=>({promi:(promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.photo&&!q.chiche&&q.status!=='tenu')||{}).id, chiche:(promises.find(q=>q.chiche&&!q.draft&&!q.photo&&q.status!=='tenu')||{}).id})""")
    for nat, pid in ids.items():
        for pal in CAS[nat]:
            pg.evaluate("([id,pal])=>{ closeAll(); const p=promises.find(q=>q.id===id); p.__av=p.__av||{m:p.monde,o:p.dalleOrigine}; p.monde={m:'encre',p:pal,h:0}; p.dalleOrigine=true; openDetail(id); }", [pid, pal])
            pg.wait_for_timeout(1700)
            notes[(nat, pal)] = pg.evaluate("()=>document.getElementById('dpTrameCv').getAttribute('data-origine')")
            caps[(nat, pal)] = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':520}))).convert('RGB')
        pg.evaluate("(id)=>{ closeAll(); const p=promises.find(q=>q.id===id); if(p.__av){ p.monde=p.__av.m; p.dalleOrigine=p.__av.o; delete p.__av; } }", pid)
    # un Cercle : le menu photo y propose-t-il l'option ?
    pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(1800)
    bt = pg.evaluate("()=>{const b=document.querySelector('#detailPoster .ph-photo-btn'); if(!b) return null; const r=b.getBoundingClientRect(); return r.width?{x:r.left+r.width/2,y:r.top+r.height/2}:null}")
    mots = None
    if bt:
        pg.touchscreen.tap(bt['x'], bt['y']); pg.wait_for_timeout(800)
        mots = pg.evaluate("()=>{const m=document.querySelector('.ph-photo-menu'); return m?[...m.querySelectorAll('button')].map(b=>b.textContent):null}")
    caps[('cercle', '')] = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':520}))).convert('RGB')
    print('Cercle — bouton photo :', bool(bt), '· menu :', mots)
    b.close()
for k, v in notes.items(): print(k, v)
w, h = caps[('promi', 'irascible')].size; G = 60; T = 150
pl = Image.new('RGB', (3*w + 4*G, 3*(h + T) + G), (247, 240, 222)); d = ImageDraw.Draw(pl)
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 46)
except Exception: f = ImageFont.load_default()
NOM = {'irascible': 'Irascible', 'truculent': 'Truculent', 'signal': 'Ingénu', 'primesautier': 'Primesautier'}
for r, nat in enumerate(('promi', 'chiche')):
    for c, pal in enumerate(CAS[nat]):
        x = G + c*(w + G); y = G + r*(h + T); n = notes[(nat, pal)] or '|'; br, de = n.split('|')
        d.text((x, y), '%s · plantée sous %s' % ('Promi' if nat == 'promi' else 'Chiche', NOM[pal]), fill=(32, 25, 8), font=f)
        d.text((x, y + 60), ('couleur d’origine' if br == 'origine' else 'CONFLIT → rampe de Q30') + ' · ΔE au champ %s' % de.replace('.', ','), fill=(32, 25, 8), font=f)
        pl.paste(caps[(nat, pal)], (x, y + T - 10))
y = G + 2*(h + T)
d.text((G, y), 'Cercle — sa fiche n’a pas de bouton photo : l’option n’y existe pas', fill=(32, 25, 8), font=f)
d.text((G, y + 60), '(un Cercle n’a pas de monde de plantation ; sa bande est une petite Toile)', fill=(32, 25, 8), font=f)
pl.paste(caps[('cercle', '')], (G, y + T - 10))
pl.save('planche-v118/planche-dalle-origine.png'); print(pl.size)
k = 1500 / pl.size[0]; pl.resize((1500, int(pl.size[1]*k))).save('scratchpad/v118/origine-vue.png')
