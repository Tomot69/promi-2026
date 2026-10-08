# -*- coding: utf-8 -*-
"""redteam_partage_dessin.py — LE PARTAGE DU DESSIN (v137, C-068).

Décision (Tom, 8 oct. 2026), mot pour mot : « On peut importer une photo ou dessiner, mais seul un dessin se partage, jamais une photo
importée. L'image partagée porte par défaut la mention de la nature (Promi, Chiche ou Cercle) et le logo en bas à gauche. Un réglage,
dans les Réglages, masque la mention : il ne reste alors que le dessin et le logo. Le logo est toujours là. Un dessin masqué pour soi
n'est jamais partagé. »

Au vrai doigt (rond Partager de la fiche), WebKit, deux thèmes. L'image jugée est L'EXPORT (`_shExporteCanevas`) ; les textes posés sont
piégés au tracé (`fillText`), les couleurs lues dans les pixels. Le fond du dessin (#12FF34), la couleur de son trait (#FF00AA) et celle
de la photo (#00E5FF) ne sont dans aucune palette : on les cherche à l'image.
  A · une PHOTO importée n'est jamais dans l'image partagée (0 pixel de la photo), aucune mention, aucun logo de dessin
  B · un dessin posé : l'image porte le dessin (fond et trait), le logo « Promi » en bas à gauche, la mention de la nature au-dessus
      (PROMI, CHICHE, CERCLE) ; ni mot-marque du haut ni QR
  C · le réglage des Réglages (au doigt) masque la mention : le logo reste, à la même place ; le réglage est mémorisé
  D · un dessin MASQUÉ pour soi n'est jamais emporté (0 pixel de son fond ni de son trait), et l'image n'est pas celle d'un dessin
Preuve : rouge sur l'état d'avant (python3 redteam_partage_dessin.py zz-av137.html).
"""
import sys
from playwright.sync_api import sync_playwright
F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'
CAP = '--captures' in sys.argv
ok = [0]; ko = []
def t(nom, c, d=''):
    if c: ok[0] += 1
    else: ko.append(nom)
    print('%s  %-78s %s' % ('OK' if c else 'KO', nom, str(d)[:200]))
PIEGE = r"""()=>{ if(window.__pg) return; window.__pg=true; window.__ft=[]; const f=CanvasRenderingContext2D.prototype.fillText;
  CanvasRenderingContext2D.prototype.fillText=function(s,x,y){ try{ window.__ft.push({c:this.canvas, s:String(s), x:x/(this.canvas.width||1)*(this.getTransform?this.getTransform().a:1), y:y/(this.canvas.height||1)*(this.getTransform?this.getTransform().d:1), font:this.font}); }catch(e){} return f.apply(this,arguments); }; }"""
EXPORT = r"""()=>{ window.__ft=[]; const tb=HTMLCanvasElement.prototype.toBlob; HTMLCanvasElement.prototype.toBlob=function(){};
  let cv=null; try{ cv=window._shExporteCanevas(); }catch(e){} HTMLCanvasElement.prototype.toBlob=tb; if(!cv) return null;
  const ft=window.__ft.filter(f=>f.c===cv).map(f=>({s:f.s,x:f.x,y:f.y,font:f.font})); const w=Math.round(cv.width/6), h=Math.round(cv.height/6), c=document.createElement('canvas'); c.width=w; c.height=h; const g=c.getContext('2d'); g.imageSmoothingEnabled=false; g.drawImage(cv,0,0,w,h);
  const d=g.getImageData(0,0,w,h).data; const n=(R,G,B)=>{ let k=0; for(let i=0;i<d.length;i+=4){ if(Math.abs(d[i]-R)+Math.abs(d[i+1]-G)+Math.abs(d[i+2]-B)<24) k++; } return k/(w*h); };
  return {w:cv.width, h:cv.height, fond:n(0x12,0xFF,0x34), trait:n(0xFF,0x00,0xAA), photo:n(0x00,0xE5,0xFF), ft:ft, attr:cv.getAttribute('data-dessin-partage'), url:(window.__cap? cv.toDataURL('image/png'):null)}; }"""
DESSIN = "{fond:'#12FF34', traits:[], pose:true, masque:false, poses:[{c:'#FF00AA', t:8, g:false, pts:[60,200,0,0.5, 120,260,16,0.5, 200,330,32,0.5, 280,280,48,0.5, 330,220,64,0.5]}]}"
PHOTO = "(()=>{const c=document.createElement('canvas'); c.width=c.height=64; const g=c.getContext('2d'); g.fillStyle='#00E5FF'; g.fillRect(0,0,64,64); return c.toDataURL('image/png');})()"
def logo(ft): return [f for f in ft if f['s'] == 'Promi' and 'PromiLate' in f['font'] and f['x'] < 0.15 and f['y'] > 0.85]
def mention(ft, mot): return [f for f in ft if f['s'] == mot and 'Gilbert' in f['font'] and f['x'] < 0.15 and f['y'] > 0.75]
def partage(pg):
    bb = pg.evaluate("()=>{const e=document.querySelector('#dpDetails .dpd-part'); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width}}")
    if bb and bb['w']: pg.touchscreen.tap(bb['x'], bb['y'])
    pg.wait_for_timeout(2600)
    return pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('show')")
def ferme(pg): pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
        pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
        pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){ try{ setLight(t==='light'); }catch(e){ d.classList.toggle('light',t==='light'); } } }", th)
        pg.evaluate(PIEGE)
        if CAP: pg.evaluate("()=>{window.__cap=true}")
        # A · une photo
        pg.evaluate("()=>{ const p=promises.find(q=>q.title==='faire les crêpes'); p.dessin=null; p.photo=%s; closeAll(); }" % PHOTO); pg.wait_for_timeout(700)
        pg.evaluate("()=>openDetail(promises.find(q=>q.title==='faire les crêpes').id)"); pg.wait_for_timeout(2200)
        o = partage(pg); e = pg.evaluate(EXPORT) or {}
        t('[%s] A · le partage s\'ouvre sur une fiche à photo' % T, o)
        t('[%s] A · la photo importée n\'est pas dans l\'image partagée' % T, e.get('photo', 1) == 0 and not e.get('attr'), 'photo %.4f · attr %s' % (e.get('photo', -1), e.get('attr')))
        ferme(pg)
        # B · un dessin, pour chaque nature
        for nat, prep, ouv in (('PROMI', "const p=promises.find(q=>q.title==='faire les crêpes'); p.photo=null; p.dessin=%s;" % DESSIN, "openDetail(promises.find(q=>q.title==='faire les crêpes').id)"),
                               ('CHICHE', "const p=promises.find(q=>q.title==='courir dimanche'); p.dessin=%s;" % DESSIN, "openDetail(promises.find(q=>q.title==='courir dimanche').id)"),
                               ('CERCLE', "const o=JSON.parse(localStorage.getItem('promi_dessins_cercle')||'{}'); o['potager']=%s; localStorage.setItem('promi_dessins_cercle', JSON.stringify(o));" % DESSIN, "openEssaim('potager')")):
            pg.evaluate("()=>{ try{localStorage.removeItem('promi_dessin_mention')}catch(e){} %s }" % prep); pg.evaluate("()=>{ %s }" % ouv); pg.wait_for_timeout(2400)
            o = partage(pg); e = pg.evaluate(EXPORT) or {}; ft = e.get('ft', [])
            t('[%s] B · %s : l\'image est le dessin (fond et trait)' % (T, nat), o and e.get('fond', 0) > 0.5 and e.get('trait', 0) > 0.0005, 'fond %.3f · trait %.4f' % (e.get('fond', 0), e.get('trait', 0)))
            t('[%s] B · %s : le logo en bas à gauche, la mention au-dessus' % (T, nat), len(logo(ft)) == 1 and len(mention(ft, nat)) == 1 and mention(ft, nat)[0]['y'] < logo(ft)[0]['y'], [(f['s'], round(f['x'], 3), round(f['y'], 3)) for f in ft])
            t('[%s] B · %s : rien d\'autre n\'est écrit (ni mot-marque du haut, ni intitulé)' % (T, nat), len(ft) == 2, [f['s'] for f in ft])
            if CAP and e.get('url') and nat == 'PROMI' and th == 'light':
                import base64; open('planche-v137/partage-dessin-avec-mention.png', 'wb').write(base64.b64decode(e['url'].split(',')[1]))
            if nat == 'PROMI':
                # C · le réglage, au doigt, dans les Réglages
                ferme(pg); pg.evaluate("()=>{ const s=document.getElementById('settingsBtn')||document.querySelector('[data-open=\"settings\"]'); if(s) s.click(); else if(window.openSettings) openSettings(); }"); pg.wait_for_timeout(1500)
                pg.evaluate("()=>{const e=document.getElementById('setMention'); if(e) e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(900)
                bb = pg.evaluate("()=>{const e=document.getElementById('setMention'); if(!e) return null; const r=e.getBoundingClientRect(); const c=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2); return {x:r.x+r.width/2,y:r.y+r.height/2,ok:!!(c&&(c===e||e.contains(c))),txt:e.textContent}}")
                t('[%s] C · la rangée « Mention sur un dessin partagé » est aux Réglages, joignable' % T, bool(bb and bb['ok'] and 'affichée' in bb['txt']), bb)
                if bb: pg.touchscreen.tap(bb['x'], bb['y']); pg.wait_for_timeout(500)
                st = pg.evaluate("()=>({k:localStorage.getItem('promi_dessin_mention'), txt:(document.getElementById('setMention')||{}).textContent})")
                t('[%s] C · un toucher la masque, c\'est mémorisé' % T, st['k'] == '0' and 'masquée' in (st['txt'] or ''), st)
                ferme(pg); pg.evaluate("()=>openDetail(promises.find(q=>q.title==='faire les crêpes').id)"); pg.wait_for_timeout(2200)
                o = partage(pg); e2 = pg.evaluate(EXPORT) or {}; f2 = e2.get('ft', [])
                t('[%s] C · mention masquée : le dessin et le logo, rien d\'autre' % T, o and e2.get('fond', 0) > 0.5 and len(logo(f2)) == 1 and len(f2) == 1, [f['s'] for f in f2])
                t('[%s] C · le logo n\'a pas bougé' % T, bool(logo(ft) and logo(f2)) and abs(logo(ft)[0]['x'] - logo(f2)[0]['x']) < 0.002 and abs(logo(ft)[0]['y'] - logo(f2)[0]['y']) < 0.002)
                if CAP and e2.get('url') and th == 'light':
                    import base64; open('planche-v137/partage-dessin-sans-mention.png', 'wb').write(base64.b64decode(e2['url'].split(',')[1]))
            ferme(pg)
        # D · un dessin masqué pour soi
        pg.evaluate("()=>{ try{localStorage.removeItem('promi_dessin_mention')}catch(e){} promises.find(q=>q.title==='faire les crêpes').dessin.masque=true; openDetail(promises.find(q=>q.title==='faire les crêpes').id); }"); pg.wait_for_timeout(2200)
        o = partage(pg); e = pg.evaluate(EXPORT) or {}
        t('[%s] D · un dessin masqué pour soi n\'est jamais emporté' % T, o and e.get('fond', 1) == 0 and e.get('trait', 1) == 0 and not e.get('attr') and not logo(e.get('ft', [])), 'fond %.4f · trait %.4f · attr %s' % (e.get('fond', -1), e.get('trait', -1), e.get('attr')))
        ferme(pg)
        t('[%s] aucune erreur de page' % T, not er, er[:2])
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: sys.exit(1)
