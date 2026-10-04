# PLANCHE C-042 — l'outil de dessin, posé par-dessus l'app rendue (rien n'est construit dans l'app). @3x, clair et sombre.
import sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
clip={'x':20,'y':44,'width':390,'height':844}
PEN=open('scratchpad/v127/dessin/pen.js',encoding='utf-8').read(); OV=open('scratchpad/v127/dessin/ov.js',encoding='utf-8').read()
FICHES={'promi':"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}",
        'chiche':"()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; openDetail(p.id);}",
        'cercle':"()=>{closeAll(); openEssaim('potager');}"}
# cotes par fiche : la rangée sous la bande (yRow), posée au bas de la bande (yBande), le dessin (yDessin)
GEO={'promi':dict(yRow=316,yBande=186,yDessin=150,cacheBas=[311,368]),
     'chiche':dict(yRow=316,yBande=186,yDessin=150,cacheBas=[311,368]),
     'cercle':dict(yRow=200,yBande=104,yDessin=128,petit=1,descend=['#detailPoster .ov-bas',56])}
MARQUE_CERCLE = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('detailPoster'); let n=0;
  [...P.querySelectorAll('*')].forEach(e=>{ if(e.closest('.ov-bas')||e.tagName==='CANVAS'||e.id==='ovC042'||e.closest('#ovC042')) return; const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); if(r.height<8||r.width<8||cs.position==='static') return; const y=r.top-dv.top;
    if(y>=205 && y<760 && r.bottom-dv.top<=765 && !/peauf|dpd|barre/i.test(e.className+' '+e.id)){ e.classList.add('ov-bas'); n++; } }); return n; }"""
def prise(pg, nom):
    pg.wait_for_timeout(350); f='scratchpad/v127/dessin/%s.png'%nom; pg.screenshot(path=f, clip=clip); return f
def planche(titre, cases, cols, sortie, sombre):
    ims=[(t,Image.open(f).convert('RGB')) for t,f in cases]; w,h=ims[0][1].size; M=54; T=96; H0=150
    rows=(len(ims)+cols-1)//cols; bg=(240,236,226) if not sombre else (28,24,20); enc=(32,25,8) if not sombre else (247,240,222)
    P=Image.new('RGB',(M+cols*(w+M), H0+rows*(h+T+M)), bg); d=ImageDraw.Draw(P)
    try: ft=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',52); fg=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',70)
    except Exception: ft=fg=None
    d.text((M,44),titre,fill=enc,font=fg)
    for i,(t,im) in enumerate(ims):
        x=M+(i%cols)*(w+M); y=H0+(i//cols)*(h+T+M); d.text((x,y+22),t,fill=enc,font=ft); P.paste(im,(x,y+T))
    P.save(sortie); print(sortie, P.size)
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        S='sombre' if th=='dark' else 'clair'
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}"%th)
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:160])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{ if(document.documentElement.classList.contains('light')!==(t==='light')) setTheme(t) }catch(e){} }", th); pg.wait_for_timeout(900)
        pg.evaluate(PEN); pg.evaluate(OV)
        # A · la rangée d'outils : trois compositions × trois fiches
        cases=[]
        for nat in ('promi','chiche','cercle'):
            pg.evaluate("()=>OV.nettoie()"); pg.evaluate(FICHES[nat]); pg.wait_for_timeout(3000)
            if nat=='cercle': print('cercle : blocs descendus', pg.evaluate(MARQUE_CERCLE))
            for compo,lab in (('A','A · sous la bande, icônes'),('B','B · au bas de la bande, icônes'),('C','C · sous la bande, icônes + mots')):
                c=dict(GEO[nat]); c.update(nat=nat, compo=compo, sel='plume', dessin='simple', cachePhoto=1, light=(th=='light'))
                if compo=='B': c.pop('cacheBas',None); c.pop('descend',None)
                pg.evaluate("(c)=>{OV.montre(c)}", c); cases.append(('%s — %s'%(lab,{'promi':'Promi','chiche':'Chiche','cercle':'Cercle'}[nat]), prise(pg,'A-%s-%s-%s'%(compo,nat,th))))
        cases=[cases[i] for i in (0,3,6,1,4,7,2,5,8)]
        planche('C-042 · A · la rangée d\'outils — %s'%S, cases, 3, 'planche-v127/dessin-A-rangee-%s.png'%S, th=='dark')
        for k,compo in enumerate('ABC'): planche('C-042 · A · composition %s — %s'%(compo,S), cases[k*3:k*3+3], 3, 'planche-v127/dessin-A-rangee-%s-tel-%s.png'%(S,compo), th=='dark')
        # B, D, E · les états, sur la fiche Promi, composition A
        pg.evaluate("()=>OV.nettoie()"); pg.evaluate(FICHES['promi']); pg.wait_for_timeout(3000); E=[]
        base=dict(GEO['promi']); base.update(nat='promi', compo='A', dessin='simple', cachePhoto=1, light=(th=='light'))
        def etat(lab, nom, **k):
            c=dict(base); c.update(k); pg.evaluate("(c)=>{OV.montre(c)}", c); E.append((lab, prise(pg,'E-%s-%s'%(nom,th))))
        etat('plume choisie','plume',sel='plume')
        etat('gomme choisie','gomme',sel='gomme')
        etat('B · tailles (2e toucher sur la plume)','tailles',sel='plume',etat='tailles',taille=1)
        etat('B · tailles, sur la gomme','taillesg',sel='gomme',etat='tailles',taille=2)
        etat('D · S1 · couleur déployée, TRAIT','S1',sel='couleur',symbole='S1',etat='couleur',onglet='TRAIT',tonChoisi=4)
        etat('D · S2 (Studio) · couleur déployée, FOND','S2',sel='couleur',symbole='S2',etat='couleur',onglet='FOND')
        planche('C-042 · B, D, E · les états (fiche Promi, composition A) — %s'%S, E, 3, 'planche-v127/dessin-BDE-etats-%s.png'%S, th=='dark')
        planche('C-042 · E · plume, gomme, tailles — %s'%S, E[:3], 3, 'planche-v127/dessin-BDE-%s-tel-1.png'%S, th=='dark'); planche('C-042 · B, D · tailles, couleur — %s'%S, E[3:], 3, 'planche-v127/dessin-BDE-%s-tel-2.png'%S, th=='dark')
        # E · hors du mode dessin : masquage, menu photo, page +, trois palettes
        F=[]
        def hors(lab, nom, **k):
            c=dict(nat='promi', light=(th=='light'), yDessin=150); c.update(k); pg.evaluate("(c)=>{OV.montre(c)}", c); F.append((lab, prise(pg,'F-%s-%s'%(nom,th))))
        hors('masquage (coin de la bande) — dessin affiché','oeil',dessin='simple',oeil=[24,204,0])
        hors('dessin masqué','oeilnon',oeil=[24,204,1])
        hors('une bande avec trois palettes mêlées','trois',dessin='trois',oeil=[24,204,0])
        pg.evaluate("()=>OV.nettoie()"); pg.evaluate("()=>{document.querySelector('.ph-photo-btn').click()}"); pg.wait_for_timeout(900)
        r=pg.evaluate(r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const L=[...document.querySelectorAll('#detailPoster *')].filter(e=>e.children.length===0&&/ORIGINE/i.test(e.textContent||'')); const e=L[0]; if(!e) return null; let n=e; while(n.parentElement&&getComputedStyle(n).backgroundColor==='rgba(0, 0, 0, 0)') n=n.parentElement; const c=n.cloneNode(true); c.setAttribute('data-ov-clone','1'); (c.children.length?[...c.querySelectorAll('*')].filter(x=>x.children.length===0)[0]:c).textContent='Dessiner'; const r=n.getBoundingClientRect(); n.parentElement.appendChild(c); const cs=getComputedStyle(n); if(cs.position==='absolute'||cs.position==='fixed'){ c.style.setProperty('top',(parseFloat(cs.top)+52)+'px','important'); } return [n.tagName,n.className,cs.position,Math.round(r.top-dv.top)]; }""")
        print('menu photo :', r); F.append(('« Dessiner » dans le menu photo', prise(pg,'F-menu-%s'%th)))
        pg.evaluate("()=>{OV.nettoie(); closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3800)
        q=pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); const e=[...document.querySelectorAll('.ph-photo-btn')].filter(x=>x.getBoundingClientRect().width>0).pop(); if(!e) return null; const r=e.getBoundingClientRect(); return [r.right-dv.left, r.top-dv.top]}")
        if not q: q=[366,154]
        if q: pg.evaluate("(c)=>{OV.montre(c)}", dict(nat='promi', light=(th=='light'), pilules=[[q[0], max(56,q[1]-104), 'Importer une image'],[q[0], max(108,q[1]-52), 'Dessiner']]))
        F.append(('« Dessiner » sur la page +', prise(pg,'F-plus-%s'%th)))
        planche('C-042 · E · masquage, « Dessiner », trois palettes — %s'%S, F, 3, 'planche-v127/dessin-E-autres-%s.png'%S, th=='dark')
        planche('C-042 · E · masquage, trois palettes — %s'%S, F[:3], 3, 'planche-v127/dessin-E-%s-tel-1.png'%S, th=='dark'); planche('C-042 · E · « Dessiner » — %s'%S, F[3:], 2, 'planche-v127/dessin-E-%s-tel-2.png'%S, th=='dark')
        ctx.close()
    b.close()
