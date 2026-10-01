#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRÔLE DES FILETS — aucun trait horizontal nulle part, sauf s'il est au moodboard.

   Le moodboard n'a QUASIMENT aucun filet horizontal : ses séparations sont des
   respirations, pas des lignes. Ce contrôle parcourt chaque écran, liste tout
   border-top / border-bottom / box-shadow inset HORIZONTAL visible (largeur réelle,
   couleur non transparente) et ÉCHOUE si le filet n'est pas porté par un élément
   sanctionné par le moodboard.

   ÉLÉMENTS SANCTIONNÉS (les seuls filets du moodboard) :
     · la barre Peaufiner — filet haut 1px  (ph-1..8 : box-shadow inset 0 1px 0)
     · le filet sous la carte message de la fiche (.dpm-filet — CLAUDE.md §3)

   Tout autre filet = parasite → KO, avec la liste des coupables par écran.

       python3 redteam_filets.py        attendu : 0 filet parasite

   ⚑ v114 (Tom, 30 sept. 2026) — ET LE FILET DU TRAIT, PEINT DANS UN CANEVAS. La première partie ne balaie que le DOM :
   elle ne voyait PAS le filet crème (#F7F0DE, 0,8 px) que le peintre du trait et celui des disques posent dans leur
   canevas — ni liste blanche, ni tolérance : un angle mort. (Le crème du filet est ADOUCI : `_FILET_DOUX` =
   rgba(247,240,222,.55) ; un premier piège qui ne cherchait que #F7F0DE ne prenait rien, même sur la version fautive.) La seconde partie PIÈGE le tracé (stroke en crème sur un
   canevas de la fiche ou de la page +), écran par écran, deux thèmes, WebKit.
   LISTE BLANCHE NOMINATIVE — UNE SEULE ENTRÉE : « fiche tenue » (la terre #2B1020). Là le filet est EXIGÉ : la crête
   #0B4A2A n'y est qu'à Δlum 15,7 de la terre, c'est le filet qui la rend lisible (CLAUDE.md §3). Partout ailleurs : zéro.
   Rougi sur la version fautive : python3 redteam_filets.py --app=zz-fautive-v113.html (copie de sauvegardes/app-avant-v113.html).
"""
import sys as _sys
import os as _os
from playwright.sync_api import sync_playwright

_ICI = _os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI, 'app.html'), '/home/claude/app.html']:
        if _os.path.exists(p): return 'file://' + p
    return 'file:///home/claude/app.html'

# éléments dont un filet horizontal EST au moodboard (id ou classe, sous-chaîne)
SANCTIONNES = ('csBotBar', 'cbb', 'dpDetails', 'dpdTog', 'dpd-tog',   # barre Peaufiner
               'dpm-filet', 'dpMsg', 'mg-note-line',                  # filet carte message
               'ix-hair')                                             # hairline cs-top (1px moodboard)

SCAN = r"""(sanct)=>{
  const root = document.querySelector('#detailPoster.show')
            || document.querySelector('#settingsScreen.show,#settingsScreen.open')
            || document.querySelector('#createSheet');
  if(!root) return [];
  const bad=[];
  const ok = (e)=>{ let n=e; for(let i=0;i<4&&n;i++){ const sig=(n.id||'')+' '+(typeof n.className==='string'?n.className:'');
      if(sanct.some(s=>sig.indexOf(s)>=0)) return true; n=n.parentElement; } return false; };
  // trouve la RÈGLE CSS qui pose le filet (dernière règle gagnante qui matche l'élément)
  const cause = (e, kind)=>{ let win=null;
    for(const sheet of document.styleSheets){ let rules; try{rules=sheet.cssRules;}catch(_){continue;}
      for(const r of rules){ if(!r.selectorText||!r.style) continue; let v='';
        if(kind==='shadow') v=r.style.boxShadow;
        else v=r.style.borderTop||r.style.borderBottom||r.style.borderTopWidth||r.style.borderBottomWidth||r.style.borderTopColor||r.style.borderBottomColor||(r.style.border&&r.style.border!=='0'&&r.style.border!=='none'?r.style.border:'');
        if(!v) continue;
        try{ if(e.matches(r.selectorText)) win=r.selectorText+'  {'+(kind==='shadow'?('box-shadow:'+r.style.boxShadow):('border:'+v))+'}'; }catch(_){}
      } }
    return win||'(règle inline ou non trouvée)'; };
  // sélecteur lisible de l'élément
  const sel = (e)=>{ let s=e.tagName.toLowerCase(); if(e.id)s='#'+e.id; else if(typeof e.className==='string'&&e.className.trim())s+='.'+e.className.trim().split(/\s+/).slice(0,2).join('.'); return s; };
  root.querySelectorAll('*').forEach(e=>{
    const c=getComputedStyle(e); const b=e.getBoundingClientRect();
    if(b.width<40 || c.display==='none' || c.visibility==='hidden' || +c.opacity<0.05) return;
    // on ne vise que les SÉPARATEURS horizontaux larges — pas les contours de
    // pastilles (bord sur 4 côtés / pilule) ni les fins soulignés de champ étroits.
    const radius = parseFloat(c.borderTopLeftRadius)||0;
    const box4 = parseFloat(c.borderLeftWidth)>=0.5 && parseFloat(c.borderRightWidth)>=0.5;
    const largeur = b.width / (root.getBoundingClientRect().width||390);
    if(radius>=40 || box4) return;                 // pastille / boîte : ce n'est pas un filet
    let hit=null;
    ['Top','Bottom'].forEach(s=>{ const w=parseFloat(c['border'+s+'Width']); const col=c['border'+s+'Color'];
      if(w>=0.5 && col && !/,\s*0\)\s*$/.test(col) && col!=='rgba(0, 0, 0, 0)' && largeur>=0.5) hit='border'+s+' '+w.toFixed(1)+'px '+col; });
    const m=c.boxShadow.match(/(?:rgba?\([^)]*\)|#\w+)\s+0px\s+(-?[\d.]+)px\s+0px/);
    if(m && Math.abs(parseFloat(m[1]))>=0.5 && largeur>=0.5) hit=hit||('shadow '+c.boxShadow.slice(0,38));
    if(hit && !ok(e)){
      const kind = hit.indexOf('shadow')>=0 ? 'shadow' : 'border';
      const at = Math.round(b.top) + (hit.indexOf('Bottom')>=0||/0px (-?[\d.]+)px 0px/.test(hit)&&hit.indexOf('-')<0 ? Math.round(b.height):0);
      bad.push(sel(e)+'  ['+hit+']  y≈'+Math.round(b.top)+'\n        └ '+cause(e,kind));
    }
  });
  return [...new Set(bad)];
}"""

def newpage(b, theme):
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    pg.goto(_url()); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if theme=='light': pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.add('light'))")
    else: pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.remove('light'))")
    return pg

R = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ['light', 'dark']:
        # page + trois natures
        for k in ['promi', 'nuee', 'draft']:
            pg = newpage(b, theme)
            pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(700)
            pg.evaluate("(k)=>{const t=document.querySelector('#createSheet .tile[data-kind='+JSON.stringify(k)+']');if(t)t.click();}", k); pg.wait_for_timeout(1200)
            R.append(('page+ %s [%s]' % (k, theme), pg.evaluate(SCAN, list(SANCTIONNES)))); pg.close()
        # fiches
        for st, name in [('rate', 'fiche a-tenir'), ('tenu', 'fiche tenue')]:
            pg = newpage(b, theme)
            pg.evaluate("(s)=>{const ps=promises.filter(x=>!x.draft&&!x.nuee);const p=ps[0];p.status=s;p.who='Rachel';p.title='rendre le livre';openDetail(p.id);}", st)
            pg.wait_for_timeout(2400); R.append(('%s [%s]' % (name, theme), pg.evaluate(SCAN, list(SANCTIONNES)))); pg.close()
        # fiche nuee
        pg = newpage(b, theme)
        pg.evaluate("()=>{if(window.openNueeDetail)window.openNueeDetail('nTest');}"); pg.wait_for_timeout(2400)
        R.append(('fiche nuee [%s]' % theme, pg.evaluate(SCAN, list(SANCTIONNES)))); pg.close()
    b.close()

total = 0
for name, bad in R:
    total += len(bad)
    mark = 'OK' if not bad else 'KO(%d)' % len(bad)
    print('%-22s %s' % (name, mark))
    for x in bad: print('      · ' + x)
print('\n%s — %d filet(s) parasite(s)' % ('OK' if total==0 else 'ECHEC', total))

# ── SECONDE PARTIE — le filet du trait et des disques, piégé dans le canevas ───────────────────────────────
APP = next((a.split('=',1)[1] for a in _sys.argv if a.startswith('--app=')), 'app.html')
FILET_BLANCHE = {'fiche tenue'}          # nominative : la terre d'une fiche tenue, et rien d'autre
PIEGE = """(()=>{const o=CanvasRenderingContext2D.prototype.stroke;
  CanvasRenderingContext2D.prototype.stroke=function(){ try{ const s=this.strokeStyle;
    const t=String(s).toLowerCase().replace(/\\s/g,''); if(t==='#f7f0de' || t.indexOf('rgba(247,240,222,')===0 || t==='rgb(247,240,222)'){ const c=this.canvas, sc=c.closest&&c.closest('#detailPoster,#createSheet');
      if(sc) (window.__filets=window.__filets||[]).push((c.id||c.className||'canvas')+'@'+sc.id); } }catch(_){}
    return o.apply(this,arguments); }; })();"""
ECRANS = [('fiche promi',   "()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id)}"),
          ('fiche chiche',  "()=>{closeAll();openDetail(promises.find(p=>p.title==='courir dimanche').id)}"),
          ('fiche cercle',  "()=>{closeAll();openEssaim('potager')}"),
          ('fiche tenue',   "()=>{closeAll();openDetail(promises.find(p=>p.title==='planter un arbre').id)}"),
          ('page+ promi',   "()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()},400)}"),
          ('page+ chiche',  "()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][1];x&&x.click()},400)}"),
          ('page+ cercle',  "()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()},400)}")]
T = []
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}" + PIEGE)
    pg.goto('http://127.0.0.1:8752/' + APP); pg.wait_for_timeout(7000)
    for th in ('dark', 'light'):
        pg.evaluate("t=>setTheme(t)", th); pg.wait_for_timeout(400)
        for nom, js in ECRANS:
            pg.evaluate("()=>{window.__filets=[]}"); pg.evaluate(js); pg.wait_for_timeout(2600)
            f = pg.evaluate("()=>{const sc=document.querySelector('#detailPoster.show,#createSheet.show');return (window.__filets||[]).filter(x=>sc&&x.endsWith('@'+sc.id))}")
            n = len(f); veut = nom in FILET_BLANCHE
            ok = (n > 0) if veut else (n == 0)
            T.append(ok)
            print('%-14s [%s]  filet %-4s %s  %s' % (nom, th, 'oui' if n else 'non', '(exigé — liste blanche)' if veut else '', 'OK' if ok else 'KO  ← ' + ', '.join(sorted(set(f)))[:120]))
    b.close()
print('\nfilet du trait : %d/%d' % (sum(T), len(T)))
if total or not all(T): _sys.exit(1)
