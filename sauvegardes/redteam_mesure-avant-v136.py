#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_mesure.py — LE RELEVÉ `?mesure=1` NE DÉCALE RIEN, ET LA PELOTE RESTE VISIBLE (v125, Tom, 3 oct. 2026).

« Le cadre de mesure se superpose à la page, sans rien déplacer, et la Pelote reste visible. Juge : les cotes de l'Aura sont
identiques au point près avec et sans ?mesure=1. »
  1 · chaque bloc de l'Aura (plateau, Pelote, ombre, bouton, phrase, Noyaux, légende, chiffres…) a la même boîte, à 0,5 pt près,
      avec et sans `?mesure=1`, dans les deux thèmes ;
  2 · le cadre du relevé existe avec `?mesure=1`, et il ne recouvre AUCUN point de la Pelote (sa boîte et celle de `#auBoule` ne se
      croisent pas) ;
  3 · il ne prend pas le doigt sur la Pelote : au centre de la boule, `elementFromPoint` rend la prise de la Pelote, comme sans lui.
Preuve : sur `une copie de `sauvegardes/app-avant-v125.html` posée à la racine, le cadre est posé à y 108, sur la Pelote → ROUGE.
"""
import sys
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
TOL = 0.5
COTES = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, sc=document.getElementById('auraScreen'); const R={};
  const B=(nom,e)=>{ if(!e) return; const r=e.getBoundingClientRect(); if(!r.width&&!r.height) return; R[nom]=[(r.left-dv.left)/k,(r.top-dv.top)/k,r.width/k,r.height/k].map(v=>Math.round(v*100)/100); };
  B('plateau', sc.querySelector('.enh')); B('pelote', document.getElementById('auBoule')); B('halo', document.getElementById('auPeloteHalo')); B('ombre', document.getElementById('auPeloteOmbre')); B('bouton', document.getElementById('auPartage'));
  let n=0; sc.querySelectorAll('*').forEach(e=>{ if(e.id==='auMesure'||e.closest('#auMesure')) return; if(e.children.length) return; const t=(e.textContent||'').trim(); if(!t) return; const r=e.getBoundingClientRect(); if(!r.height) return; B('texte '+(n++)+' « '+t.slice(0,18)+' »', e); });
  /* les dessins nommés ; les dalles (canevas sans nom, recadrés au plus juste sur une matière qui respire) ne sont pas des cotes */
  sc.querySelectorAll('canvas[id],svg').forEach((e,i)=>{ if(e.id==='auBouleGL') return; B('dessin '+i+' '+(e.id||''), e); });
  const m=document.getElementById('auMesure'), mr=m&&m.getBoundingClientRect(), pr=document.getElementById('auBoule').getBoundingClientRect();
  const croise=mr ? !(mr.right<=pr.left||mr.left>=pr.right||mr.bottom<=pr.top||mr.top>=pr.bottom) : null;
  const c=document.elementFromPoint(pr.left+pr.width/2, pr.top+pr.height/2);
  return {R, mesure:!!m, croise, auCentre:c?(c.id||c.className||c.tagName):null, defile:sc.scrollTop}; }"""
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail))
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        V = {}
        for q in ('', '?mesure=1'):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, reduced_motion='reduce')
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
            pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + FICHIER + q); pg.wait_for_timeout(6800)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}", th); pg.wait_for_timeout(500)
            pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
            pg.wait_for_timeout(5000)
            V[q] = pg.evaluate(COTES); ctx.close()
        a, m = V[''], V['?mesure=1']
        ecarts = []
        for nom in sorted(set(a['R']) | set(m['R'])):
            x, y = a['R'].get(nom), m['R'].get(nom)
            if not x or not y: ecarts.append('%s : %s / %s' % (nom, x, y)); continue
            d = max(abs(x[i] - y[i]) for i in range(4))
            if d > TOL: ecarts.append('%s : %s → %s' % (nom, x, y))
        juge('[%s] les %d cotes de l\'Aura sont les mêmes avec et sans ?mesure=1 (à %.1f pt)' % (th, len(a['R']), TOL), not ecarts and len(a['R']) > 20, ' · '.join(ecarts[:4]))
        juge('[%s] le cadre du relevé existe' % th, m['mesure'] is True and a['mesure'] is False)
        juge('[%s] il ne recouvre aucun point de la Pelote' % th, m['croise'] is False, 'croise=%s' % m['croise'])
        juge('[%s] au centre de la Pelote, le doigt touche ce qu\'il touchait sans le relevé (la prise de la Pelote)' % th, m['auCentre'] == a['auCentre'] and 'au-prise' in str(m['auCentre']), '%s / %s' % (a['auCentre'], m['auCentre']))
        juge('[%s] la page n\'a pas défilé' % th, a['defile'] == m['defile'], '%s / %s' % (a['defile'], m['defile']))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
sys.exit(1 if ko else 0)
