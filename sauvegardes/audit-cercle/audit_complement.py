# LE CERCLE — COMPLÉMENT DE L'AUDIT À L'ÉCRAN (11 sept. 2026).
# Ce que le premier passage (audit_ecran.py) n'a pas su jouer ou pas regardé :
#   A · le Peaufiner de la PAGE + — ouvert par sa vraie porte, #csBotBar (le premier passage cliquait .dpd-tog)
#   B · un pinceau payant (0,50 €) choisi puis PLANTÉ sans rien payer : le trait est-il gardé ?
#   C · l'écran de partage : aucun ✦, aucun flou 2,4, aucun encart (Q113 — personne ne doit savoir qui paie)
#   D · la fiche d'une personne : « comment ça évolue » en gratuit (Q183 : le graphe va au Cercle)
#   E · en Cercle payé : un réglage défloué se touche-t-il ? fait-il quelque chose ?
# Mêmes conditions que le premier passage : 430 × 932 (le #device à 390 × 844), DPR 2, captures sur disque.
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ecran')
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_ecran.py'), encoding='utf-8').read()
# on reprend DUMP / ETAT / BASE / PEAUF / AU_CENTRE tels quels, sans rejouer le premier passage
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_ecran.py')}
exec(src.split("R = {'scenes'")[0], ns)
DUMP, ETAT, BASE, PEAUF, AU_CENTRE, joue, capture, clic_doigt = (ns[k] for k in
    ('DUMP', 'ETAT', 'BASE', 'PEAUF', 'AU_CENTRE', 'joue', 'capture', 'clic_doigt'))

PAGEPLUS = [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 500),
  ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
  ("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu();}", 700)]
TXT = r"""(root)=>{const R=document.querySelector(root); if(!R) return null; const out=[];
  R.querySelectorAll('*').forEach(e=>{ if(!(e.checkVisibility&&e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))) return;
    let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent; own=own.replace(/\s+/g,' ').trim(); if(own) out.push(own.slice(0,90)); });
  return out;}"""
SIGNES = r"""(root)=>{const R=document.querySelector(root); if(!R) return null; const r={etoile:[],flou:[],cercle:[]};
  R.querySelectorAll('*').forEach(e=>{ if(!(e.checkVisibility&&e.checkVisibility())) return; const c=getComputedStyle(e);
    let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent;
    if(/✦|✧/.test(own)) r.etoile.push(own.trim().slice(0,50)); if(/Cercle/.test(own)) r.cercle.push(own.trim().slice(0,50));
    if(/blur/.test(c.filter)) r.flou.push((e.id||e.className.toString().split(' ')[0])+':'+c.filter); });
  return r;}"""

R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark', 'light'):
        for mode in ('gratuit', 'cercle'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("(v)=>setPremium(v)", mode == 'cercle'); pg.wait_for_timeout(400)
            cle = '%s_%s' % (th, mode); print('\n════ %s' % cle); R[cle] = {}
            # A · le Peaufiner de la page +, par #csBotBar, au point
            joue(pg, PAGEPLUS)
            rec = clic_doigt(pg, '#csBotBar'); pg.wait_for_timeout(1500)
            ouvert = pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-peauf')")
            bloc = pg.evaluate("()=>{const b=document.querySelector('#createSheet .s2-cercle'); return b?{vis:b.checkVisibility(),n:b.children.length}:null;}")
            lignes = pg.evaluate("()=>[...document.querySelectorAll('#createSheet .s2-liste > *')].map(e=>(e.querySelector('.s2-lab')||e).textContent.replace(/\\s+/g,' ').trim().slice(0,40))")
            for pos in ('haut', 'bas'):
                pg.evaluate("(p)=>{const c=document.querySelector('#createSheet > .dpd-corps'); if(c) c.scrollTop = p==='haut'?0:c.scrollHeight;}", pos)
                pg.wait_for_timeout(500); capture(pg, '%s_pageplus_peauf_%s' % (cle, pos))
            R[cle]['pageplus_peauf'] = {'doigt': rec, 'ouvert': ouvert, 'bloc_cercle': bloc, 'lignes': lignes,
                                        'noeuds': pg.evaluate(DUMP, '#createSheet > .dpd-corps')}
            print('  A · page + Peaufiner : doigt→%s ouvert=%s · bloc du Cercle=%s\n      lignes : %s' % (rec, ouvert, bloc, ' | '.join(lignes)))
            # B · un pinceau payant, choisi puis planté
            joue(pg, PAGEPLUS)
            clic_doigt(pg, '#csPinceau .pc-t[data-t="Doublé"]'); pg.wait_for_timeout(600)
            choisi = pg.evaluate("()=>window.promiPinceau?window.promiPinceau(null):null")
            avant = pg.evaluate("()=>promises.map(p=>p.id)")
            pg.evaluate("()=>{const t=document.getElementById('fTitle'); if(t && !t.value) t.value='aller voir la mer'; document.getElementById('addPromi').click();}")
            pg.wait_for_timeout(2600)
            neuf = pg.evaluate("(av)=>promises.filter(p=>av.indexOf(p.id)<0).map(p=>({id:p.id,titre:p.title||p.t||p.titre,trait:p.trait||null}))", avant)
            R[cle]['pinceau_plante'] = {'choisi': choisi, 'plante': neuf}
            print('  B · pinceau payant choisi=%s → planté : %s' % (choisi, neuf))
            if neuf:
                pg.evaluate("(id)=>{ try{closeAll();}catch(e){} openDetail(id); }", neuf[0]['id']); pg.wait_for_timeout(1800)
                capture(pg, '%s_pinceau_plante_fiche' % cle)
                pg.evaluate("(id)=>{ try{closeAll();}catch(e){} const i=promises.findIndex(p=>p.id===id); if(i>=0) promises.splice(i,1); try{render();}catch(e){} }", neuf[0]['id'])
            # C · le partage, depuis une fiche et depuis le dock
            for nom, steps in (('partage_fiche', [(BASE, 200), ("()=>openDetail(126)", 1300), ("()=>{const b=document.querySelector('#detailPoster .dpd-part'); if(b) b.click();}", 2200)]),
                               ('partage_dock', [(BASE, 200), ("()=>{const b=document.getElementById('shareBtn')||[...document.querySelectorAll('#device *')].find(e=>/^PARTAGER$/i.test((e.textContent||'').trim())); if(b) b.click();}", 2400)])):
                joue(pg, steps)
                e = pg.evaluate(ETAT); s = pg.evaluate(SIGNES, '#shareScreen')
                capture(pg, '%s_%s' % (cle, nom))
                R[cle][nom] = {'couches': e['couches'], 'signes': s}
                print('  C · %s : couches=%s · ✦=%s · Cercle=%s · flou=%s' % (nom, e['couches'], s and s['etoile'], s and s['cercle'], s and s['flou'][:4]))
            # D · la fiche d'une personne
            joue(pg, [(BASE, 200), ("()=>openPerson('Rachel')", 1800)])
            t = pg.evaluate(TXT, '#personSheet') or []
            evol = [x for x in t if 'volue' in x or 'Cercle' in x or '✦' in x]
            pg.evaluate("()=>{const x=[...document.querySelectorAll('#personSheet *')].find(e=>/volue/.test(e.textContent)&&e.children.length<3); if(x) x.scrollIntoView({block:'center'});}")
            pg.wait_for_timeout(500); capture(pg, '%s_personne_evolue' % cle)
            R[cle]['personne'] = {'textes': t, 'evolue_cercle': evol, 'signes': pg.evaluate(SIGNES, '#personSheet')}
            print('  D · fiche de Rachel : %s' % evol)
            # E · un réglage du bloc (défloué en Cercle) : se touche-t-il, fait-il quelque chose ?
            joue(pg, [(BASE, 200), ("()=>openDetail(126)", 1300), (PEAUF, 1500)])
            av = pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .s2-cercle .s2-reg')].map(r=>r.textContent.replace(/\\s+/g,' ').trim())")
            rec = clic_doigt(pg, '#detailPoster .s2-cercle .s2-reg:nth-child(2)'); pg.wait_for_timeout(1200)
            ap = pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .s2-cercle .s2-reg')].map(r=>r.textContent.replace(/\\s+/g,' ').trim())")
            e = pg.evaluate(ETAT); capture(pg, '%s_reglage_touche' % cle)
            R[cle]['reglage_touche'] = {'doigt': rec, 'avant': av, 'apres': ap, 'couches': e['couches'],
                                        'recurrence_du_promi': pg.evaluate("()=>{const p=promises.find(x=>x.id===126); return p?{rec:p.rec||p.recur||p.recurrence||null, rappel:p.rappel||null, imp:p.imp}:null;}")}
            print('  E · toucher RÉCURRENCE : doigt→%s · avant %s · après %s · couches=%s' % (rec, av[1:2], ap[1:2], e['couches']))
    br.close()
json.dump(R, open(os.path.join(OUT, 'complement.json'), 'w'), ensure_ascii=False, indent=1)
print('\nécrit : %s/complement.json' % OUT)
