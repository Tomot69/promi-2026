# -*- coding: utf-8 -*-
"""UN CHAMP BLANC N'EXISTE JAMAIS.

   LA RÈGLE (décision Tom, 29 août 2026, sans exception)
   ─────────────────────────────────────────────────────
   « Le champ porte toujours sa couleur pleine de nature. Bleu pour un Promi, framboise pour
     un Chiche, mauve pour une Nuée. Dans les deux thèmes, sur tous les écrans — fiche,
     page +, carte d'Index, bandeau du Fil, Nuée, gardé de côté. La dalle se pose dessus,
     jamais à la place. »

   CE QUI A DÉCLENCHÉ CE CONTRÔLE : sur la page + en thème clair, le champ sortait CRÈME —
   la couleur du corps. La dalle flottait sur du vide et « trace pour planter » était posé
   sur du crème. Cause : j'avais lu Q83 de travers. « Un gardé de côté n'a pas de DALLE » ne
   dit rien du CHAMP — et la même décision précisait « sa carte d'Index garde le champ de
   nature en pointillé, SANS MATIÈRE ». Ce qui manque à un gardé de côté, c'est la matière,
   jamais la couleur. Trois écrans avaient le champ éteint : la page +, la fiche, la carte.

   COMMENT ON MESURE : au-dessus du trait, on échantillonne le champ au pixel et on refuse
      · toute couleur de CORPS (§1.3), claire ou sombre ;
      · tout pixel transparent — un champ qui ne peint rien laisse voir le corps dessous,
        c'est le même défaut vu de l'autre côté.
   On échantillonne LE HAUT du champ (les 28 premiers pour cent), toujours au-dessus de la
   vague quelle que soit sa base. Le bandeau du Fil a sa vague À LA VERTICALE : on y prend la
   bande de GAUCHE, pour la même raison.
"""
import sys, os
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_CHAMP', "http://127.0.0.1:8752/app.html")

# §1.3 — les corps d'écran, et les deux surfaces du produit. Aucun ne peut être un champ.
# ⚑ VALEURS REPRISES LE 16 SEPTEMBRE 2026 (Tom : nouvelle palette). La RÈGLE ne bouge pas —
#   « un champ blanc n'existe jamais, le champ porte toujours sa nature » ; seules les valeurs
#   des deux surfaces changent, et le corps sombre d'une carte de Nuée avec elles :
#     crème  #F4EEE1 → #F7F0DE        encre  #16171B → #201908
#     carte Nuée (sombre) #271B45 → #1B1426 — le mauve passant à #291547 (L*12), l'ancien corps
#     tombait à ΔE 6,2 de son propre champ ; on prend le corps sombre de Nuée du §3, plus sourd.
#   Sans cette reprise, le juge accusait le CHAMP mauve d'être l'ancien corps (#2A1749 à 4 unités
#   de #271B45) — il condamnait un écran juste.
#   Version d'avant : sauvegardes/redteam_champ-avant-PALETTE-16sept.py
CORPS = ['#12142A', '#25101A', '#1A1230',      # fiche Promi · Chiche · Nuée (sombre)
         '#1C2049', '#37141F', '#1B1426',      # carte d'Index (sombre)
         '#F7F0DE', '#201908']                 # crème et encre, les deux surfaces

ECRANS = [
 ('fiche tenue',   "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',"()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('chiche lancé',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; if(p)openDetail(p.id);}"),
 ('gardé de côté', "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('page +',        "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('page + Nuée',   "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][1]; if(x)x.click();},300);}"),
 ('Index 2',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('Index 3',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
 ('Fil',           "()=>{closeAll(); setView('fil');}"),
 ('Nuée',          "()=>{closeAll(); openEssaim('potager');}"),
 ('Nuée vide',     "()=>{closeAll(); openEssaim('atelier');}"),
 ("l'instant arrive",  "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}}"),
 ("l'instant referme", "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('referme');}catch(e){}},900);}}"),
 ("l'instant après",   "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}"),
]

MESURE = r"""(corps)=>{
  const hex=h=>[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];
  const CORPS=corps.map(hex);
  /* ⚠ LA TOLÉRANCE EST SERRÉE, ET C'EST VOULU. Un champ est un `fillStyle` : ses pixels
     sont EXACTS. Large, le seuil attrapait les GRAINES d'une Nuée vide (§10.6 : « la Toile
     sans promesse est semée de graines dans les tons crème, DANS LES DEUX THÈMES ») —
     mesuré #F9F1E5, #F1E7E6, #EFE4E7, des mélanges de graines translucides qui frôlent le
     crème sans en être. Ce sont de la MATIÈRE posée sur un champ mauve, pas un champ nu :
     les confondre condamnerait un écran juste. */
  const proche=(r,v,b)=>CORPS.find(c=>Math.abs(c[0]-r)<5&&Math.abs(c[1]-v)<5&&Math.abs(c[2]-b)<5);
  const hx=(r,v,b)=>'#'+[r,v,b].map(n=>n.toString(16).padStart(2,'0')).join('').toUpperCase();
  const out=[];
  /* les champs : celui d'une fiche, celui de la page +, ceux des cartes et des bandeaux */
  const champs=[];
  /* ⚠ ON NE JUGE QUE CE QUI EST À L'ÉCRAN. `#csTrameCv` reste `display:block` DANS une
     feuille fermée : mesuré tel quel, il sortait « transparent » sur les cinq fiches, alors
     que personne ne le voit. On demande donc la visibilité RÉELLE — ancêtres compris. */
  const vu=e=>{ if(e.checkVisibility) return e.checkVisibility({checkOpacity:true,
                                                               checkVisibilityCSS:true});
    for(let n=e;n&&n.nodeType===1;n=n.parentNode){ const s=getComputedStyle(n);
      if(s.display==='none'||s.visibility==='hidden'||+s.opacity<0.05) return false; }
    return true; };
  ['dpTrameCv','csTrameCv'].forEach(id=>{ const c=document.getElementById(id);
    if(c && vu(c) && c.getBoundingClientRect().width>40){
      /* ⚠ UNE NUÉE VIDE EST SEMÉE DE GRAINES CRÈME (§10.6, « dans les deux thèmes ») : sur
         CET écran, et lui seul, la peinture ne peut pas distinguer une graine d'un corps.
         C'est la DÉCLARATION qui juge — elle, elle est nette. On ne desserre rien ailleurs. */
      const dp=document.getElementById('detailPoster');
      /* assainissement (30 sept.) : la première moitié de ce test était `(…===false && false)`, toujours fausse — retirée */
      const vide = (()=>{ try{ return !!(typeof curNuee!=='undefined' && curNuee
                 && !promises.filter(q=>q.nuee===curNuee && !q.draft).length); }catch(e){ return false; } })();
      champs.push({cv:c, nom:'#'+id, vertical:false, graines:vide});
    } });
  document.querySelectorAll('#device .s4-carte').forEach((d,k)=>{
    if(!vu(d)) return;
    const c=d.querySelector('canvas'); if(!c) return;
    const r=d.getBoundingClientRect(); if(r.width<40||r.height<30) return;
    const t=(d.textContent||'').trim().slice(0,22);
    /* le bandeau du Fil est plus large que haut : sa vague est VERTICALE */
    champs.push({cv:c, nom:'carte '+k+' « '+t+' »', vertical:(r.width>r.height*1.6)});
  });
  champs.forEach(ch=>{
    const c=ch.cv; let g; try{ g=c.getContext('2d'); }catch(e){ return; }
    if(!g||!c.width||!c.height) return;
    let d; try{ d=g.getImageData(0,0,c.width,c.height).data; }catch(e){ return; }
    /* la zone SÛREMENT au-dessus du trait : les 28 premiers pour cent, en haut — ou à
       gauche pour un bandeau, dont la vague descend à la verticale. */
    const x0=2, y0=2;
    const x1=ch.vertical? Math.round(c.width*0.28) : c.width-2;
    const y1=ch.vertical? c.height-2 : Math.round(c.height*0.28);
    const pasX=Math.max(1,Math.round((x1-x0)/28)), pasY=Math.max(1,Math.round((y1-y0)/28));
    let vus=0, faute=null, vide=0;
    for(let y=y0;y<y1;y+=pasY) for(let x=x0;x<x1;x+=pasX){
      const i=((y*c.width)+x)*4;
      if(d[i+3]<200){ vide++; continue; }
      vus++;
      if(!faute){ const m=proche(d[i],d[i+1],d[i+2]);
        if(m) faute={col:hx(d[i],d[i+1],d[i+2]), x:x, y:y}; }
    }
    /* ── 1 · LA DÉCLARATION. Le peintre écrit ce qu'il a versé (`data-champ`) : c'est le
         seul juge possible là où la MATIÈRE recouvre le champ — sur une Nuée vide, les
         graines du §10.6 sont crème dans les deux thèmes et tombent pile sur la couleur du
         corps. On compare la COMPOSITION, pas la peinture (CLAUDE.md §7). */
    const dec=(c.getAttribute('data-champ')||'').trim();
    if(!dec){ out.push(ch.nom+' : le champ ne DECLARE rien — aucun peintre ne le remplit'); return; }
    const m=dec.match(/^#([0-9a-f]{6})$/i);
    if(m){ const q=hex('#'+m[1]);
      if(proche(q[0],q[1],q[2]))
        out.push(ch.nom+' : le champ est DÉCLARÉ à la couleur du corps '+dec.toUpperCase()); }
    /* ── 2 · LA PEINTURE. On refuse un champ transparent, et tout pixel de corps. */
    /* ⚑ assainissement (30 sept.) — un champ où AUCUN point n'a été relevé n'est plus sauté en silence (« on ne juge pas ») : il est
       NOMMÉ. Un contrôle qui ne mesure rien ne passe pas au vert. */
    if(!vus && !vide){ out.push(ch.nom+' : champ NON MESURÉ (aucun point relevé au-dessus du trait)'); return; }
    if(vide > (vus+vide)*0.5)
      out.push(ch.nom+' : le champ est TRANSPARENT (' + Math.round(100*vide/(vus+vide))
               + ' % des points) — le corps se voit dessous');
    else if(faute && !ch.graines)
      out.push(ch.nom+' : le champ porte la COULEUR DU CORPS ' + faute.col
               + ' (au point ' + faute.x + ',' + faute.y + ')');
  });
  return out;
}"""

def releve(pg, js):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
    try: pg.evaluate(js)
    except Exception: pass
    pg.wait_for_timeout(2000)
    prec, stable = None, 0
    for _ in range(20):
        pg.wait_for_timeout(250)
        n = pg.evaluate("()=>document.querySelectorAll('#device canvas[data-peint],"
                        "#device canvas[data-matiere]').length + '/' +"
                        "[...document.querySelectorAll('#device *')].filter(e=>{"
                        "const r=e.getBoundingClientRect();return r.width>4&&r.height>4;}).length")
        stable = stable + 1 if n == prec else 0
        prec = n
        if stable >= 2: break
    pg.wait_for_timeout(300)
    return pg.evaluate(MESURE, CORPS)

if __name__ == '__main__':
    ok = ko = 0
    lignes = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate('()=>{var o=document.getElementById("promiOnb");'
                    'if(o){o.classList.add("gone");o.style.display="none";}}')
        for th in ('dark','light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, js in ECRANS:
                fautes = releve(pg, js)
                E = '%s [%s]' % (nom, th)
                if fautes:
                    ko += 1
                    lignes.append('%-30s KO  %s' % (E, ' · '.join(fautes[:3])))
                else:
                    ok += 1
                    lignes.append('%-30s OK' % E)
        b.close()
    print()
    for l in lignes: print('  ' + l)
    print('\n%d/%d' % (ok, ok+ko))
    sys.exit(0 if ko == 0 else 1)
