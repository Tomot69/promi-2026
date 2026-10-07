#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_entier.py — v131 (C-051) : VOIR UNE PHOTO EN ENTIER.
Décision Tom (5 oct. 2026) : « Dans toute fiche, toucher la bande quand elle porte un dessin ou une photo (jamais la dalle) l'affiche en
entier, par-dessus le reste de l'écran. Le reste passe sur un fond sombre plein (la seiche, sans transparence). On voit alors aussi ce que
l'encart du haut cachait. Un nouveau toucher, ou ✕, referme. VoiceOver : « Voir la photo en entier ». »
AU VRAI DOIGT (contexte tactile, `touchscreen.tap`), deux thèmes. Valeurs EN DUR : la seiche #050302 = rgb(5, 3, 2).
  1 · toucher la photo dans la bande l'ouvre en entier : la vue couvre tout l'appareil, fond seiche OPAQUE, l'image entière (son haut
      et son bas, que la bande recadrait, se voient à l'écran — lus sur la capture) ;
  2 · un nouveau toucher referme, et la fiche est INTACTE (même arbre, mêmes classes, mêmes styles, même défilement) ; ✕ referme aussi ;
  3 · toucher une DALLE n'ouvre rien (fiche Promi sans photo, fiche de Cercle) ; ni le plateau, ni le bouton photo n'ouvrent la vue ;
  4 · VoiceOver : la bande s'annonce « Voir la photo en entier » quand elle porte une photo, et ne s'annonce pas sinon ;
  5 · `closeAll` referme la vue ; aucune erreur de page.
Usage : python3 redteam_entier.py [fichier.html]     — il ROUGIT sur l'état d'avant (zz-v130.html : aucune vue)."""
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
SEICHE='rgb(5, 3, 2)'; HAUT=(230,40,160); BAS=(20,200,120)        # la photo d'essai : un bandeau magenta en haut, vert en bas, le milieu gris
R=[]
def ok(nom, cond, detail=''):
    R.append((nom,bool(cond))); print(('  ✅ ' if cond else '  ❌ ')+nom+((' — '+str(detail)) if (detail!='' and not cond) else ''))
PHOTO=r"""()=>{ const c=document.createElement('canvas'); c.width=300; c.height=900; const g=c.getContext('2d'); g.fillStyle='rgb(128,128,128)'; g.fillRect(0,0,300,900);
  g.fillStyle='rgb(230,40,160)'; g.fillRect(0,0,300,90); g.fillStyle='rgb(20,200,120)'; g.fillRect(0,810,300,90); return c.toDataURL('image/png'); }"""
EMP=r"""()=>{ /* « intacte » se juge sur le RENDU : la place, la couleur, la police, le texte de chaque nœud. L'attribut `style` lui-même est
     réécrit par les passes de l'app après chaque toucher (le plateau : `margin` en abrégé puis en long ; la passe des polices retire puis
     repose sa famille) et la racine retire au sort son grain (`gsN`) et son décor (`--ghost-ink`) : ce n'est pas l'état de la fiche.
     Et l'opacité de `#tenirCv` (l'invite du geste) RESPIRE en continu : elle n'est pas comparée. */
  const dp=document.getElementById('detailPoster'); const L=[dp].concat([...dp.querySelectorAll('*')]).map(e=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e);
    return e.tagName+'|'+(e===dp?'':(e.getAttribute('class')||''))+'|'+[r.left,r.top,r.width,r.height].map(v=>Math.round(v*2)/2).join(',')+'|'+c.color+'|'+c.backgroundColor+'|'+c.fontFamily.split(',')[0]+'|'+c.fontSize+'|'+c.display+'|'+c.visibility+'|'+(e.id==='tenirCv'?'(le geste respire)':c.opacity)+'|'+(e.children.length?'':(e.textContent||'').slice(0,30)); });
  let h=0; const s=dp.className.replace(/\bgs\d+\b/g,'').trim()+'|'+L.join('\n'); for(let i=0;i<s.length;i++){ h=(h*31+s.charCodeAt(i))|0; }
  return {h:h, n:L.length, show:dp.classList.contains('show'), top:Math.round(dp.getBoundingClientRect().top), sc:dp.scrollTop}; }"""
VUE=r"""()=>{ const v=document.getElementById('entierVue'), dv=document.getElementById('device').getBoundingClientRect(); if(!v||!v.classList.contains('ouv')) return {ouv:false};
  const r=v.getBoundingClientRect(), cs=getComputedStyle(v), im=v.querySelector('img'), ri=im.getBoundingClientRect(), h=document.elementFromPoint(dv.left+dv.width/2, dv.top+dv.height/2);
  return {ouv:true, couvre:Math.abs(r.left-dv.left)<1&&Math.abs(r.top-dv.top)<1&&Math.abs(r.width-dv.width)<1&&Math.abs(r.height-dv.height)<1, fond:cs.backgroundColor, opacite:cs.opacity, ombre:cs.boxShadow, img:cs.backgroundImage,
    devant:!!(h&&v.contains(h)), fit:getComputedStyle(im).objectFit, nat:[im.naturalWidth,im.naturalHeight], label:v.getAttribute('aria-label'), x:!!v.querySelector('.ev-x')}; }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        print('══',th)
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(600)
        dv=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        def pt(x,y): return (dv[0]+x*dv[2]/390, dv[1]+y*dv[3]/844)
        def ouverte(): return bool(pg.evaluate("()=>{const v=document.getElementById('entierVue'); return !!(v&&v.classList.contains('ouv'))}"))
        # ── une fiche Promi qui porte une photo
        pg.evaluate("(src)=>{ closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; p.photo=src; openDetail(p.id); }", pg.evaluate(PHOTO)); pg.wait_for_timeout(3000)
        lab=pg.evaluate("()=>{const c=document.getElementById('dpTrameCv'); return [c.getAttribute('aria-label'), c.getAttribute('role')]}")
        ok('[%s] 4 · la bande qui porte une photo s\'annonce « Voir la photo en entier », en commande'%th, lab==['Voir la photo en entier','button'], lab)
        pg.wait_for_timeout(900); avant=pg.evaluate(EMP)
        pg.touchscreen.tap(*pt(195,215)); pg.wait_for_timeout(500)
        v=pg.evaluate(VUE)
        ok('[%s] 1 · toucher la photo dans la bande l\'ouvre en entier'%th, v.get('ouv'), v)
        ok('[%s] 1 · la vue couvre tout l\'appareil et passe devant le reste'%th, v.get('couvre') and v.get('devant'), v)
        ok('[%s] 1 · fond plein : la seiche #050302, opacité 1, ni ombre ni dégradé'%th, v.get('fond')==SEICHE and v.get('opacite')=='1' and v.get('ombre')=='none' and v.get('img')=='none', v)
        ok('[%s] 1 · l\'image entière, sans recadrage (contain)'%th, v.get('fit')=='contain' and v.get('nat')==[300,900], v)
        im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB') if v.get('ouv') else None
        def proche(c,d): return im is not None and sum(abs(a-b_) for a,b_ in zip(c,d))<45
        cx,_=pt(195,0); hy=pt(0,30)[1]; by=pt(0,814)[1]
        ok('[%s] 1 · on voit le haut ET le bas de la photo, que la bande recadrait (lus sur la capture)'%th, im is not None and proche(im.getpixel((int(cx*2),int(hy*2))),HAUT) and proche(im.getpixel((int(cx*2),int(by*2))),BAS), (im.getpixel((int(cx*2),int(hy*2))), im.getpixel((int(cx*2),int(by*2)))) if im else '')
        coin=im.getpixel((int(pt(20,422)[0]*2), int(pt(20,422)[1]*2))) if im else None
        ok('[%s] 1 · à côté de l\'image, le fond est la seiche (lu sur la capture)'%th, coin is not None and sum(abs(a-b_) for a,b_ in zip(coin,(5,3,2)))<12, coin)
        pg.touchscreen.tap(*pt(195,600)); pg.wait_for_timeout(500)
        ok('[%s] 2 · un nouveau toucher referme'%th, not ouverte())
        pg.wait_for_timeout(900); apres=pg.evaluate(EMP)
        ok('[%s] 2 · la fiche est intacte (même arbre, mêmes classes, mêmes styles, même défilement)'%th, avant==apres and apres['show'], (avant,apres))
        pg.touchscreen.tap(*pt(195,215)); pg.wait_for_timeout(500); o1=ouverte()
        c=pg.evaluate("()=>{const e=document.querySelector('#entierVue .ev-x'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
        if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(500)
        pg.wait_for_timeout(900); e2=pg.evaluate(EMP); ok('[%s] 2 · ✕ referme, et la fiche est toujours là, intacte'%th, o1 and not ouverte() and e2==avant, (o1, ouverte(), avant, e2))
        # à la souris aussi
        pg.mouse.click(*pt(195,215)); pg.wait_for_timeout(400); o2=ouverte(); pg.mouse.click(*pt(195,600)); pg.wait_for_timeout(400)
        ok('[%s] 1-2 · à la souris : ouvre, puis referme'%th, o2 and not ouverte())
        # ── ni le plateau ni le bouton photo n'ouvrent la vue
        pg.touchscreen.tap(*pt(120,70)); pg.wait_for_timeout(450); a=ouverte()
        if a: pg.evaluate("()=>window._entier&&_entier.ferme()")
        ok('[%s] 3 · toucher le plateau n\'ouvre pas la vue'%th, not a)
        c=pg.evaluate("()=>{const e=[...document.querySelectorAll('#detailPoster .ph-photo-btn')].filter(x=>x.getBoundingClientRect().width>0)[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
        if c and pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"): pg.touchscreen.tap(*c); pg.wait_for_timeout(500)
        ok('[%s] 3 · toucher le bouton photo n\'ouvre pas la vue'%th, bool(c) and not ouverte(), c)
        # ── closeAll referme
        pg.evaluate("()=>{ closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; openDetail(p.id); }"); pg.wait_for_timeout(2600)
        pg.touchscreen.tap(*pt(195,215)); pg.wait_for_timeout(450); o3=ouverte(); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(300)
        ok('[%s] 5 · closeAll referme la vue'%th, o3 and not ouverte())
        # ── une DALLE n'ouvre rien : fiche Promi sans photo, fiche de Cercle
        pg.evaluate("()=>{ closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; p.photo=null; openDetail(p.id); }"); pg.wait_for_timeout(2800)
        lab=pg.evaluate("()=>{const c=document.getElementById('dpTrameCv'); return [c.getAttribute('aria-label'), c.getAttribute('role')]}")
        pg.wait_for_timeout(900); av=pg.evaluate(EMP); pg.touchscreen.tap(*pt(195,215)); pg.wait_for_timeout(1400)
        ok('[%s] 3 · toucher une DALLE (fiche Promi sans photo) n\'ouvre rien, la fiche ne bouge pas'%th, not ouverte() and pg.evaluate(EMP)==av)
        ok('[%s] 4 · une bande qui porte une dalle ne s\'annonce pas'%th, lab==[None,None], lab)
        pg.evaluate("()=>{ closeAll(); openEssaim('potager'); }"); pg.wait_for_timeout(2800)
        pg.touchscreen.tap(*pt(195,150)); pg.wait_for_timeout(500)
        ok('[%s] 3 · toucher les dalles d\'une fiche de Cercle n\'ouvre rien'%th, not ouverte())
        # ⚑ v136 (Tom, 7 oct. 2026, C-067) — « Même comportement dès la création, sur la page + » : un dessin posé sur la page +
        #   s'ouvre en entier au toucher de la bande ; un second toucher rend la page + telle quelle ; sans dessin ni photo, rien ne s'ouvre.
        EMPP="""()=>[...document.querySelectorAll('#createSheet *')].filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect(), s=getComputedStyle(e); return [e.tagName, Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height), s.color, s.fontSize].join(',')}).join('|')"""
        pg.evaluate("()=>{ closeAll(); try{setPremium(true)}catch(e){} document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(900)
        for _k in range(3): pg.evaluate("()=>{const t=document.querySelectorAll('#createSheet .tile')[0]; if(t) t.click();}"); pg.wait_for_timeout(500)
        pg.wait_for_timeout(1700)
        pg.touchscreen.tap(*pt(195,110)); pg.wait_for_timeout(500)
        ok('[%s] 6 · page + sans dessin ni photo : toucher la bande n\'ouvre rien'%th, not ouverte())
        if pg.evaluate("()=>!!(window._dessin&&window._dessin.ouvre&&window._dessin.ouvre())"):
            pg.wait_for_timeout(400); pg.mouse.move(120,300); pg.mouse.down()
            for _i in range(22): pg.mouse.move(120+_i*9,300+(_i%6)*11)
            pg.mouse.up(); pg.wait_for_timeout(200); pg.evaluate("()=>document.querySelector('#dessinMode [data-outil=poser]').click()"); pg.wait_for_timeout(1200)
        avp=pg.evaluate(EMPP); labp=pg.evaluate("()=>document.getElementById('csTrameCv').getAttribute('aria-label')")
        ok('[%s] 6 · page + : la bande qui porte un dessin s\'annonce « Voir le dessin en entier »'%th, labp=='Voir le dessin en entier', labp)
        pg.touchscreen.tap(*pt(195,110)); pg.wait_for_timeout(600)
        vp=pg.evaluate("()=>{const v=document.getElementById('entierVue'), im=v&&v.querySelector('img'), D=document.getElementById('device').getBoundingClientRect(); if(!v||!im) return null; const r=v.getBoundingClientRect(); return {ouv:v.classList.contains('ouv'), nat:im.naturalWidth, plein:Math.abs(r.width-D.width)<1&&Math.abs(r.height-D.height)<1, fond:getComputedStyle(v).backgroundColor}}")
        ok('[%s] 6 · page + : toucher le dessin l\'affiche en entier, sur tout l\'appareil, fond plein'%th, bool(vp) and vp['ouv'] and vp['nat']>0 and vp['plein'] and 'rgba' not in vp['fond'], vp)
        pg.touchscreen.tap(*pt(195,420)); pg.wait_for_timeout(600)
        ok('[%s] 6 · page + : un second toucher referme, la page + est telle quelle (rendu de chaque nœud)'%th, not ouverte() and pg.evaluate(EMPP)==avp)
        pg.evaluate("()=>{ try{ window._dessin.retire(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(400)
        ok('[%s] 5 · aucune erreur de page'%th, not errs, errs[:2])
        ctx.close()
    b.close()
n=sum(1 for _,c in R if c); print('\nredteam_entier : %d/%d'%(n,len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
