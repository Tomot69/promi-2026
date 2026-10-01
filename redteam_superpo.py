# -*- coding: utf-8 -*-
"""JAMAIS DE SUPERPOSITION — le balayage des recouvrements de texte.

   LA RÈGLE (exigence Tom, 3 septembre 2026)
   ─────────────────────────────────────────
   « Jamais de mauvaises mises en page, de superposition etc. »
   Deux textes visibles ne se recouvrent jamais, sur aucun écran, dans aucun thème.

   POURQUOI UNE BATTERIE À PART. Les juges de section vérifient les recouvrements DANS
   leur écran, sur une liste de nœuds nommés. Celui-ci balaie TOUS les textes de TOUS les
   écrans, sans liste : c'est le filet qui attrape ce qu'aucun inventaire ne prévoit.

   ⚠ DEUX PIÈGES, ET LES DEUX M'ONT EU AVANT D'ÊTRE ÉCRITS ICI.
   1 · `elementFromPoint` NE REND QUE LE DESSUS. Exiger d'y trouver LES DEUX nœuds rend le
       contrôle impossible à satisfaire — donc MORT. Vérifié : une sonde qui superposait
       l'état et le titre sur les six fiches n'était pas prise. C'est `elementsFromPoint`,
       au pluriel, qui donne la pile.
   2 · LA PILE CONTIENT CE QUI EST DERRIÈRE. Un écran fermé vit encore dans le DOM : sans
       coupe, le titre « Promi » de la Toile compte comme recouvrant chaque fiche — 138
       faux sur 13 écrans. On coupe la pile AU PREMIER FOND OPAQUE : ce qui est derrière
       un aplat n'est pas visible, donc ne recouvre rien.

   PROUVÉ DANS LES DEUX SENS, comme le §7 l'exige : avec une sonde qui remonte l'état
   de 56 px dans le titre → PRIS sur les six fiches et les deux thèmes ; sans la sonde
   → 0 sur 13 écrans × 2 thèmes.
"""
import json
from playwright.sync_api import sync_playwright
ECR=[('fiche à tenir',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',"()=>{closeAll(); const p=promises.filter(q=>q.title==='ramasser les courges')[0]; if(p)openDetail(p.id);}"),
 ('fiche tenue',"()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('chiche lancé',"()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; if(p)openDetail(p.id);}"),
 ('chiche duo',"()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('gardé de côté',"()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('Nuée',"()=>{closeAll(); openEssaim('potager');}"),
 ('page +',"()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Index',"()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('Fil',"()=>{closeAll(); setView('fil');}"),
 ('Partager',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click();}"),
 ('Réglages',"()=>{closeAll(); document.getElementById('settingsBtn').click();}"),
 ("l'instant","()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},800);}}")]
JS="""()=>{const dv=document.getElementById('device');const D=dv.getBoundingClientRect();const k=D.width/390;
 const n=[];
 document.querySelectorAll('#device *').forEach(e=>{
   const c=getComputedStyle(e);
   if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return;
   const t=[...e.childNodes].filter(x=>x.nodeType===3).map(x=>x.textContent.trim()).join('');
   if(!t) return;
   const r=e.getBoundingClientRect(); if(r.width<4||r.height<4) return;
   const x=(r.left-D.left)/k, y=(r.top-D.top)/k, w=r.width/k, h=r.height/k;
   if(y+h<0||y>844) return;
   n.push({e:e, t:t.slice(0,18), x:x, y:y, w:w, h:h});});
 const out=[];
 for(let i=0;i<n.length;i++) for(let j=i+1;j<n.length;j++){
   const a=n[i],b=n[j];
   /* un nœud et son propre enfant ne se recouvrent pas : ils sont le même texte */
   if(a.e.contains(b.e)||b.e.contains(a.e)) continue;
   const ox=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x);
   const oy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
   if(ox<=3||oy<=3) continue;
   /* ⚑ ON CONFIRME AU DOIGT (CLAUDE.md §8) : un écran FERMÉ vit encore dans le DOM et son
      texte garde un rectangle. Sans cette confirmation, le titre de la Toile « compte »
      comme recouvrant chaque fiche, et le balayage rend 138 faux. Le doigt tranche : au
      centre du recouvrement, on doit trouver L'UN DES DEUX, sinon aucun n'est visible là. */
   const cx=Math.max(a.x,b.x)+ox/2, cy=Math.max(a.y,b.y)+oy/2;
   /* ⚠ `elementFromPoint` NE REND QUE LE DESSUS : exiger d'y trouver LES DEUX rend le
      contrôle impossible à satisfaire — donc mort. C'est `elementsFromPoint`, au pluriel,
      qui donne la PILE ; un recouvrement est réel quand les deux y sont. */
   let pile=document.elementsFromPoint(D.left+cx*k, D.top+cy*k)||[];
   /* ⚠ ET ON COUPE LA PILE AU PREMIER FOND OPAQUE. `elementsFromPoint` rend TOUT ce qui est
      sous le point, y compris les écrans FERMÉS qui vivent encore dans le DOM derrière une
      feuille. Sans cette coupe, le titre « Promi » de la Toile compte comme recouvrant
      chaque fiche : 138 faux sur 13 écrans. Ce qui est derrière un aplat opaque n'est pas
      visible, donc ne recouvre rien. */
   let sol=pile.length;
   for(let z=0;z<pile.length;z++){
     const bg=getComputedStyle(pile[z]).backgroundColor;
     const m=bg.match(/[\d.]+/g);
     if(m && (m.length<4 || +m[3]>0.92)){ sol=z; break; }
   }
   pile=pile.slice(0,sol+1);
   const vuA = pile.some(z=>z===a.e||a.e.contains(z));
   const vuB = pile.some(z=>z===b.e||b.e.contains(z));
   if(!vuA || !vuB) continue;
   out.push([a.t,b.t,Math.round(ox),Math.round(oy)]);
 }
 return out.slice(0,6);}"""

with sync_playwright() as pw:
    b=pw.chromium.launch(); tot=0
    for th in ('dark','light'):
        for nom,nav in ECR:
            pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
            pg.goto("http://127.0.0.1:8752/app.html");pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)",th);pg.wait_for_timeout(500)
            pg.evaluate(nav);pg.wait_for_timeout(2800)
            r=pg.evaluate(JS)
            if r:
                tot+=len(r); print(f"⚠ {th:5s} {nom:16s}")
                for a,c,ox,oy in r: print(f"      « {a} » ⨯ « {c} »  {ox}×{oy}")
            pg.close()
    print("\nrecouvrements de texte :", tot)
    b.close()
