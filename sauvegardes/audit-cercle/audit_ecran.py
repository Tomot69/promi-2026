# LE CERCLE — AUDIT À L'ÉCRAN, NŒUD PAR NŒUD (11 sept. 2026).
# La carte (carte-lecture.md) est une LECTURE du code : ce script la confronte à l'écran.
# Deux thèmes × deux modes (gratuit / Cercle payé) × chaque surface du Cercle. Pour chaque nœud :
# texte propre, boîte (cotes écran 390), visible, police, couleurs, flou (le sien ET celui d'un ancêtre),
# opacité effective, qui reçoit le doigt au centre. Les portes sont touchées À LA SOURIS au point de
# l'élément (pas par .click()) : c'est ce que ferait un doigt, et ça passe par les écouteurs de capture.
# Viewport 430 × 932 → #device fait exactement 390 × 844 (CLAUDE.md §8, « un comparateur ment »).
# Usage : python3 sauvegardes/audit-cercle/audit_ecran.py [URL]
import json, os, sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ecran')
os.makedirs(OUT, exist_ok=True)

DUMP = r"""(root)=>{
 const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
 const R=document.querySelector(root); if(!R) return {absent:true};
 const cn=(e)=>typeof e.className==='string'?e.className:((e.className&&e.className.baseVal)||'');
 const nom=(e)=>e.id?'#'+e.id:e.tagName.toLowerCase()+(cn(e).trim()?'.'+cn(e).trim().split(/\s+/).join('.'):'');
 const out=[];
 for(const e of [R,...R.querySelectorAll('*')]){
   const cs=getComputedStyle(e), tag=e.tagName.toLowerCase();
   let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent; own=own.replace(/\s+/g,' ').trim();
   const deco=cs.backgroundColor!=='rgba(0, 0, 0, 0)'||cs.backgroundImage!=='none'||parseFloat(cs.borderTopWidth)>0||cs.boxShadow!=='none'||cs.filter!=='none';
   if(!own && !['canvas','button','input','img'].includes(tag) && !deco && !e.id) continue;
   if(['path','circle','rect','line','defs','stop','lineargradient','g','i'].includes(tag) && !own) continue;
   const vis=e.checkVisibility?e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}):true;
   const r=e.getBoundingClientRect();
   let op=1, filt=[], p=e; while(p&&p!==document.documentElement){const c=getComputedStyle(p); op*=parseFloat(c.opacity); if(c.filter!=='none') filt.push((p===e?'':nom(p)+'>')+c.filter); p=p.parentElement;}
   const x=(r.left-dv.left)/s, y=(r.top-dv.top)/s, w=r.width/s, h=r.height/s;
   let hit=null; const cx=r.left+r.width/2, cy=r.top+r.height/2;
   if(vis && r.width>1 && r.height>1 && cx>=0 && cy>=0 && cx<innerWidth && cy<innerHeight){
     const h0=document.elementFromPoint(cx,cy); hit=h0?((h0===e||e.contains(h0))?'soi':nom(h0).slice(0,60)):null; }
   out.push({sel:nom(e).slice(0,80), txt:own.slice(0,110), vis, x:+x.toFixed(1), y:+y.toFixed(1), w:+w.toFixed(1), h:+h.toFixed(1),
     dans:(x>-1&&y>-1&&x+w<391&&y+h<845), ff:cs.fontFamily.split(',')[0].replace(/["']/g,''), fs:cs.fontSize, fw:cs.fontWeight, fst:cs.fontStyle,
     col:cs.color, fill:cs.webkitTextFillColor, bg:cs.backgroundColor, bgi:cs.backgroundImage.slice(0,70),
     bd:cs.borderTopWidth+' '+cs.borderTopStyle+' '+cs.borderTopColor, rad:cs.borderTopLeftRadius,
     sh:cs.boxShadow, tsh:cs.textShadow, op:+op.toFixed(2), filt, pe:cs.pointerEvents, cur:cs.cursor, onclick:!!e.onclick, hit});
 }
 return out; }"""

ETAT = r"""()=>({
  couches:[...document.querySelectorAll('.show')].map(e=>e.id).filter(i=>i&&i!=='scrim').sort().join(','),
  premium:document.getElementById('device').classList.contains('premium'),
  isPremium:(typeof isPremium!=='undefined')?isPremium:null,
  toast:(document.querySelector('.toast.show,#toast.show,.toast')||{}).textContent||'',
  studio:(document.getElementById('studioScreen')||{className:''}).className,
  owned:(typeof _ownedDesigns!=='undefined')?Object.keys(_ownedDesigns):null,
  monde:(window.Toile&&Toile.curWorld)?Toile.curWorld():null,
  pinceau:window.promiPinceau?window.promiPinceau(null):null,
  ls:Object.keys(localStorage).filter(k=>k.indexOf('promi')===0).sort().join(',')})"""

HERO = r"""()=>{const c=document.getElementById('plHeroCv'); if(!c) return null; const r=c.getBoundingClientRect();
  let n=0,t=0; try{const g=c.getContext('2d'); const d=g.getImageData(0,0,c.width,c.height).data; for(let i=3;i<d.length;i+=40){t++; if(d[i]>10)n++;}}catch(e){return 'illisible'}
  return {w:c.width,h:c.height,affiche:[+r.width.toFixed(0),+r.height.toFixed(0)],peint:+(n/t*100).toFixed(1)}}"""

BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
AU_CENTRE = "(sel)=>{const e=document.querySelector(sel); if(!e) return null; e.scrollIntoView({block:'center'}); return true;}"

SCENES = {
  'reglages':      ([(BASE,200),("()=>document.getElementById('settingsBtn').click()",1700)], '#settingsScreen', '#settingsScreen .s2-cercle'),
  'peauf_promi':   ([(BASE,200),("()=>openDetail(126)",1300),(PEAUF,1500)], '#detailPoster .dpd-corps', '#detailPoster .s2-cercle'),
  'peauf_chiche':  ([(BASE,200),("()=>openDetail(127)",1300),(PEAUF,1500)], '#detailPoster .dpd-corps', '#detailPoster .s2-cercle'),
  'peauf_nuee':    ([(BASE,200),("()=>openEssaim('potager')",1500),(PEAUF,1500)], '#detailPoster', None),
  'pageplus_peauf':([(BASE,200),("()=>document.getElementById('createBtn').click()",500),
                    ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}",900),
                    ("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu();}",600),
                    # la porte du Peaufiner de la page + est #csBotBar (peaufBranche, l. 17804), PAS .dpd-tog —
                    # le premier passage (11 sept.) cliquait .dpd-tog et n'ouvrait rien : scène refaite par audit_complement.py
                    ("()=>{const x=document.getElementById('csBotBar'); if(x) x.click();}",1500)], '#createSheet', '#createSheet .s2-cercle'),
  'aura':          ([(BASE,200),("()=>document.getElementById('souffleBtn').click()",3200)], '#auraScreen', None),
  'aura_aide':     ([(BASE,200),("()=>document.getElementById('souffleBtn').click()",2600),("()=>document.getElementById('auraInfoBtn').click()",1200)], '#auraHelp', '#ahCercleCta'),
  'studio':        ([(BASE,200),("()=>document.getElementById('studioBtn').click()",1900)], '#studioScreen', None),
  'personne':      ([(BASE,200),("()=>openPerson('Rachel')",1700)], '#personSheet', None),
  'accueil':       ([(BASE,400)], '#device', '#cercleTopBtn'),
}

def capture(pg, nom):
    pg.locator('#device').screenshot(path=os.path.join(OUT, nom + '.png'))

def joue(pg, steps):
    for js, w in steps:
        try: pg.evaluate(js)
        except Exception as e: print('   (étape en erreur : %s)' % str(e)[:100])
        pg.wait_for_timeout(w)

def clic_doigt(pg, sel):
    """Amène l'élément au centre de son conteneur, puis clique À LA SOURIS au point : si un autre nœud
    reçoit le doigt à cet endroit, c'est lui qui prend le clic — comme sur un téléphone."""
    ok = pg.evaluate(AU_CENTRE, sel)
    if not ok: return 'absent'
    pg.wait_for_timeout(350)
    b = pg.evaluate("""(sel)=>{const e=document.querySelector(sel); const r=e.getBoundingClientRect();
        if(r.width<2||r.height<2) return null; const x=r.left+r.width/2, y=r.top+r.height/2;
        const h=document.elementFromPoint(x,y); const cn=(n)=>n?(n.id?'#'+n.id:n.tagName.toLowerCase()+'.'+String(n.className&&n.className.baseVal!==undefined?n.className.baseVal:n.className).split(' ')[0]):null;
        return {x,y,recoit:(h&&(h===e||e.contains(h)))?'soi':cn(h)};}""", sel)
    if not b: return 'invisible (0×0)'
    pg.mouse.click(b['x'], b['y'])
    return b['recoit']

R = {'scenes': {}, 'portes': {}, 'achats': {}, 'studio_mondes': {}, 'pinceaux': {}}

with sync_playwright() as p:
    br = p.chromium.launch()
    def page_neuve():
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page()
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>document.fonts.ready")
        return ctx, pg

    ctx, pg = page_neuve()
    R['depart'] = pg.evaluate(ETAT)
    for th in ('dark', 'light'):
        for mode in ('gratuit', 'cercle'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
            pg.evaluate("(v)=>setPremium(v)", mode == 'cercle'); pg.wait_for_timeout(300)
            cle = '%s_%s' % (th, mode)
            print('\n════ %s' % cle)
            # 1 · les surfaces, nœud par nœud
            for nom, (steps, racine, cible) in SCENES.items():
                joue(pg, steps)
                if cible: pg.evaluate(AU_CENTRE, cible); pg.wait_for_timeout(400)
                d = pg.evaluate(DUMP, racine)
                e = pg.evaluate(ETAT)
                R['scenes'].setdefault(nom, {})[cle] = {'etat': e, 'noeuds': d}
                capture(pg, '%s_%s' % (cle, nom))
                nv = (len([n for n in d if n['vis']]) if isinstance(d, list) else 'ABSENT')
                cer = [n['txt'] for n in d if isinstance(d, list) and n['vis'] and n['txt'] and ('Cercle' in n['txt'] or '✦' in n['txt'] or '€' in n['txt'])] if isinstance(d, list) else []
                print('  %-15s couches=%s  nœuds visibles=%s  %s' % (nom, e['couches'], nv, (' | '.join(cer))[:200]))
            # 2 · le Studio, monde par monde (les trois du Cercle + un libre)
            for monde in ('terrazzo', 'gravure', 'sillons', 'eclats', 'encre'):
                joue(pg, SCENES['studio'][0])
                how = pg.evaluate("""(m)=>{const d=document.querySelector('#studioScreen [data-w="'+m+'"]'); if(d){d.click(); return 'data-w';}
                    return 'aucun [data-w] pour '+m+' — portes vues : '+[...document.querySelectorAll('#studioScreen [data-w]')].map(x=>x.dataset.w).join(',');}""", monde)
                pg.wait_for_timeout(1500)
                d = pg.evaluate(DUMP, '#studioScreen'); e = pg.evaluate(ETAT)
                R['studio_mondes'].setdefault(monde, {})[cle] = {'comment': how, 'etat': e, 'noeuds': d}
                capture(pg, '%s_studio_%s' % (cle, monde))
                vis = [n['sel'] + ' « ' + n['txt'] + ' »' for n in d if n['vis'] and n['txt'] and n['dans']] if isinstance(d, list) else []
                print('  studio %-9s %s · classes=%s · %s' % (monde, how, e['studio'][:90], ' | '.join(v for v in vis if ('€' in v or 'Cercle' in v or '✦' in v))[:220]))
            # 3 · les portes du Cercle, touchées au point
            portes = [
              ('#cercleTopBtn',  [(BASE,300)]),
              ('#openPlusTop',   SCENES['reglages'][0]),
              ('#detailPoster .s2-encart', SCENES['peauf_promi'][0]),
              ('#detailPoster .s2-cercle .s2-reg', SCENES['peauf_promi'][0]),
              ('#ahCercleCta',   SCENES['aura_aide'][0]),
              ('#stLockCta',     SCENES['studio'][0] + [("()=>{const d=document.querySelector('#studioScreen [data-w=\"terrazzo\"]'); if(d) d.click();}",1500)]),
              ('#karmaCercle',   SCENES['aura'][0]),
              ('#resetApp',      None),
            ]
            for sel, steps in portes:
                if steps is None: continue   # #resetApp efface l'état : joué à part, sur une page neuve
                joue(pg, steps)
                avant = pg.evaluate(ETAT)
                recoit = clic_doigt(pg, sel)
                pg.wait_for_timeout(1200)
                apres = pg.evaluate(ETAT); hero = pg.evaluate(HERO)
                R['portes'].setdefault(sel, {})[cle] = {'recoit': recoit, 'avant': avant, 'apres': apres, 'hero': hero}
                ouvert = 'plusScreen' in apres['couches']
                print('  porte %-34s doigt→%-28s Cercle ouvert=%s  premium %s→%s  héros=%s' % (sel, str(recoit)[:28], ouvert, avant['premium'], apres['premium'], hero))
                if ouvert and sel in ('#cercleTopBtn', '#openPlusTop'):
                    # la page du Cercle elle-même, en haut puis tout en bas
                    for pos in ('haut', 'bas'):
                        pg.evaluate("(p)=>{const s=document.getElementById('plusScreen'); s.scrollTop = p==='haut'?0:s.scrollHeight;}", pos)
                        pg.wait_for_timeout(500)
                        d = pg.evaluate(DUMP, '#plusScreen')
                        R['scenes'].setdefault('plus_%s_%s' % (sel[1:], pos), {})[cle] = {'etat': apres, 'noeuds': d, 'hero': pg.evaluate(HERO),
                            'scroll': pg.evaluate("()=>{const s=document.getElementById('plusScreen'); return [s.scrollTop,s.scrollHeight,s.clientHeight];}")}
                        capture(pg, '%s_plus_%s_%s' % (cle, sel[1:], pos))
            # 4 · le pinceau : ce qui est payant, et ce que coûte le choisir
            joue(pg, SCENES['pageplus_peauf'][0][:4])
            rail = pg.evaluate("""()=>[...document.querySelectorAll('#csPinceau .pc-t')].map(b=>({n:b.dataset.t, bord:getComputedStyle(b).borderTopStyle,
                  txt:b.textContent.trim(), vis:b.checkVisibility?b.checkVisibility():true}))""")
            choix = pg.evaluate("""()=>{const b=document.querySelector('#csPinceau .pc-t[data-t="Doublé"]'); if(!b) return 'absent';
                  b.click(); return window.promiPinceau?window.promiPinceau(null):'?';}""")
            pg.wait_for_timeout(700)
            prix = pg.evaluate("()=>[...document.querySelectorAll('#createSheet *')].filter(e=>e.checkVisibility&&e.checkVisibility()&&/€/.test([...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(''))).map(e=>e.textContent.trim().slice(0,60))")
            capture(pg, '%s_pinceau_pageplus_double' % cle)
            joue(pg, SCENES['peauf_promi'][0])
            pg.evaluate(AU_CENTRE, '#dpTraitReg'); pg.wait_for_timeout(400)
            peauf_val = pg.evaluate("()=>{const r=document.getElementById('dpTraitReg'); return r?r.textContent.replace(/\\s+/g,' ').trim().slice(0,160):'absent';}")
            capture(pg, '%s_pinceau_peaufiner' % cle)
            R['pinceaux'][cle] = {'rail': rail, 'choisir_double': choix, 'prix_affiches_page_plus': prix, 'peaufiner': peauf_val}
            print('  pinceaux : %d dans le rail, %d en pointillé · choisir « Doublé » → %s · prix à l’écran %s · Peaufiner « %s »' % (
                len(rail), len([r for r in rail if r['bord'] == 'dashed']), choix, prix, peauf_val[:80]))
    ctx.close()

    # 5 · les achats, et ce qui survit au rechargement — page neuve à chaque fois
    for bouton in ('#buyYear', '#buyMonth'):
        ctx, pg = page_neuve()
        joue(pg, [(BASE, 300)]); clic_doigt(pg, '#cercleTopBtn'); pg.wait_for_timeout(1200)
        r = clic_doigt(pg, bouton); pg.wait_for_timeout(1500)
        apres = pg.evaluate(ETAT)
        capture(pg, 'achat_%s' % bouton[1:])
        pg.reload(); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        recharge = pg.evaluate(ETAT)
        R['achats'][bouton] = {'recoit': r, 'apres': apres, 'apres_rechargement': recharge}
        print('\n  achat %s  doigt→%s  → premium=%s couches=%s toast=« %s » · après rechargement premium=%s' % (
            bouton, r, apres['premium'], apres['couches'], apres['toast'][:60], recharge['premium']))
        ctx.close()
    # adoption d'un monde à 1 €
    ctx, pg = page_neuve()
    joue(pg, SCENES['studio'][0] + [("()=>{const d=document.querySelector('#studioScreen [data-w=\"gravure\"]'); if(d) d.click();}", 1500)])
    avant = pg.evaluate(ETAT)
    r = clic_doigt(pg, '#stLockBuy'); pg.wait_for_timeout(1500)
    apres = pg.evaluate(ETAT); capture(pg, 'achat_stLockBuy')
    pg.reload(); pg.wait_for_timeout(6800)
    recharge = pg.evaluate(ETAT)
    R['achats']['#stLockBuy'] = {'recoit': r, 'avant': avant, 'apres': apres, 'apres_rechargement': recharge}
    print('  adoption 1 €  doigt→%s  owned %s→%s monde %s→%s · après rechargement owned=%s monde=%s' % (
        r, avant['owned'], apres['owned'], avant['monde'], apres['monde'], recharge['owned'], recharge['monde']))
    ctx.close()
    # « Réinitialiser (test) » — donne-t-il le Cercle ?
    ctx, pg = page_neuve()
    joue(pg, SCENES['reglages'][0]); r = clic_doigt(pg, '#resetApp'); pg.wait_for_timeout(1800)
    apres = pg.evaluate(ETAT)
    R['achats']['#resetApp'] = {'recoit': r, 'apres': apres}
    print('  #resetApp  doigt→%s  → premium=%s toast=« %s »' % (r, apres['premium'], apres['toast'][:70]))
    ctx.close()
    br.close()

json.dump(R, open(os.path.join(OUT, 'audit.json'), 'w'), ensure_ascii=False, indent=1)
print('\nécrit : %s/audit.json + %d captures' % (OUT, len([f for f in os.listdir(OUT) if f.endswith('.png')])))
