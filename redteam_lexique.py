#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_lexique.py — v135 (Tom, 6 oct. 2026, C-065) : LES TERMES BANNIS ET LA LOI DES POINTS, jugés à l'écran.
« Ajoute à redteam un juge des termes bannis et de la loi des points. »

  A · LES TERMES BANNIS (CLAUDE.md §2, liste complétée par Tom le 18 août et le 23 sept. 2026) — EN DUR ci-dessous. Aucun texte AFFICHÉ
      (texte rendu, libellé VoiceOver, texte d'invite d'un champ), sur aucun écran, dans les deux thèmes, ne porte l'un de ces termes.
      « échéance » n'est banni que comme LIBELLÉ DE CHAMP : il est pris quand il est, seul, le texte d'un libellé.
  B · LA LOI DES POINTS (Tom, 4 oct. 2026, v128) : « Les points disent qu'il manque quelque chose : une moitié de trait, un mot, un
      engagement. Ils ne servent jamais à autre chose. Exception nominative : les trois petits points du choix de taille de l'outil de
      dessin. » On cherche à l'écran : ① tout petit nœud ROND et PLEIN (≤ 14 pt, aussi haut que large, sans texte) ; ② tout texte fait
      seulement de points. LISTE BLANCHE NOMINATIVE : `.dz-tailles` (le choix de taille du dessin). Ce qui existait à la naissance du
      juge est NOMMÉ dans `lexique-dette.json` (il se solde, il ne grandit jamais) ; tout point NOUVEAU fait rougir.
      ⚠ Ce que le juge ne voit pas : un point PEINT dans un canevas (le pointillé d'un trait — qui, lui, dit qu'une moitié manque).

Usage : python3 redteam_lexique.py [fichier.html] [--figer] [--sonde=terme|point]
Les sondes fabriquent la version fautive dans la page : il doit y rougir."""
import sys, re, io, json, os
from playwright.sync_api import sync_playwright
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
SONDE=next((a.split('=')[1] for a in sys.argv if a.startswith('--sonde=')), None); FIGER='--figer' in sys.argv
BANNIS=['tâche','to-do','todo','objectif','valider','urgent','score','brouillon','orbite','la sphère','belle parole','en replanter un','dire un mot']
DETTE_F='lexique-dette.json'
src=io.open('redteam_maparole.py',encoding='utf-8').read()
m=re.search(r'^src\s*=.*$', src, re.M)
# la liste des écrans est celle de redteam_air, relue comme le fait redteam_maparole
air=io.open('redteam_air.py',encoding='utf-8').read()
ECRANS=[(m.group(1), m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$", air, re.M)]
SCAN=r"""(BANNIS)=>{ const dv=document.getElementById('device').getBoundingClientRect(), termes=[], points=[];
  const vu=e=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return null; if(r.right<dv.left||r.left>dv.right||r.bottom<dv.top||r.top>dv.bottom) return null;
    for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return null; } return r; };
  const T=document.createTreeWalker(document.getElementById('device').parentElement||document.body, NodeFilter.SHOW_ELEMENT); let e;
  while((e=T.nextNode())){ const r=vu(e); if(!r) continue; const cs=getComputedStyle(e);
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join(' ').replace(/\s+/g,' ').trim();
    const dits=[txt, e.getAttribute('aria-label')||'', e.getAttribute('placeholder')||''];
    for(const d of dits){ if(!d) continue; const bas=d.toLowerCase();
      for(const b of BANNIS){ const k=bas.search(new RegExp('(^|[^a-zàâçéèêëîïôûùüÿœ])'+b.replace(/[-]/g,'[- ]?')+'(s?)($|[^a-zàâçéèêëîïôûùüÿœ])')); if(k>=0) termes.push(b+' ← « '+d.slice(0,60)+' »'); }
      if(/^\s*échéance\s*:?\s*$/i.test(d)) termes.push('échéance (libellé de champ) ← « '+d+' »'); }
    const nom=(e.id?('#'+e.id):'')+(typeof e.className==='string'&&e.className?('.'+e.className.trim().split(/\s+/).slice(0,2).join('.')):'')||e.tagName.toLowerCase();
    if(e.closest('.dz-tailles')) continue;                      /* l'exception nominative */
    if(txt && /^[\s·.•‧∙⋅●○]+$/.test(txt) && (txt.match(/[·.•‧∙⋅●○]/g)||[]).length>=2) points.push('texte de points '+nom+' « '+txt.slice(0,20)+' »');
    if(!txt && !e.children.length && e.tagName!=='CANVAS' && e.tagName!=='INPUT' && e.tagName!=='TEXTAREA'){ const k=dv.width/390, w=r.width/k, h=r.height/k;
      const bg=cs.backgroundColor, plein=bg&&bg!=='rgba(0, 0, 0, 0)'&&cs.backgroundImage==='none';
      const rond=parseFloat(cs.borderTopLeftRadius)>=Math.min(r.width,r.height)/2-0.6;
      if(plein && rond && w<=14 && h<=14 && w>=2 && Math.abs(w-h)<=1) points.push('point '+nom+' '+Math.round(w)+'×'+Math.round(h)); } }
  return {termes:[...new Set(termes)], points:[...new Set(points.map(p=>p.replace(/\d+×\d+$/,'').trim()))]} }"""
dette=json.load(open(DETTE_F,encoding='utf-8')) if os.path.exists(DETTE_F) else {'points':[]}
R=[]
def ok(n,c,d=''): R.append(bool(c)); print(('  ✅ ' if c else '  ❌ ')+n+((' — '+str(d)[:300]) if d!='' else ''))
vus=set(); termes=set(); errs=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)[:140])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(500)
        for prem in (False, True):
            pg.evaluate("(v)=>{try{setPremium(v)}catch(e){}}", prem)
            for nom,js in ECRANS:
                try:
                    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(250)
                    pg.evaluate(js); pg.wait_for_timeout(1700)
                    if SONDE=='terme' and nom==ECRANS[0][0]: pg.evaluate("()=>{ const d=document.createElement('div'); d.textContent='3 tâches à valider'; d.style.cssText='position:absolute;left:30px;top:300px;z-index:999'; document.getElementById('device').appendChild(d); }")
                    if SONDE=='point' and nom==ECRANS[0][0]: pg.evaluate("()=>{ const d=document.createElement('i'); d.className='sonde-point'; d.style.cssText='position:absolute;left:30px;top:300px;width:8px;height:8px;border-radius:50%;background:#DD4D23;z-index:999'; document.getElementById('device').appendChild(d); }")
                    r=pg.evaluate(SCAN, BANNIS)
                    for t in r['termes']: termes.add('%s [%s] · %s'%(nom, th[0], t))
                    for q in r['points']: vus.add(q)
                except Exception as ex: errs.append('%s : %s'%(nom, str(ex)[:80]))
        ctx.close()
    b.close()
if FIGER:
    json.dump({'_':'Points présents à la naissance de redteam_lexique (v135, 6 oct. 2026). La liste se solde, elle ne grandit jamais.','points':sorted(vus)}, open(DETTE_F,'w',encoding='utf-8'), ensure_ascii=False, indent=1); print('dette figée : %d point(s)'%len(vus)); dette={'points':sorted(vus)}
neufs=sorted(v for v in vus if v not in dette['points']); soldes=sorted(v for v in dette['points'] if v not in vus)
ok('A · aucun terme banni affiché (%d écrans × 2 thèmes × gratuit et Ma Parole !)'%len(ECRANS), not termes, ' | '.join(sorted(termes)[:6]))
ok('B · aucun point NOUVEAU hors de l\'exception nominative (dette nommée : %d ; retrouvés : %d ; soldés depuis : %d)'%(len(dette['points']), len(vus)-len(neufs), len(soldes)), not neufs, ' | '.join(neufs[:8]))
ok('les écrans s\'ouvrent (%d)'%len(ECRANS), len(ECRANS)>=30 and not errs, errs[:2])
if dette['points']: print('\ndette nommée de la loi des points :'); [print('   ·', x) for x in dette['points']]
print('\nredteam_lexique%s : %d/%d'%((' [sonde %s]'%SONDE) if SONDE else '', sum(R), len(R)))
sys.exit(0 if all(R) else 1)
